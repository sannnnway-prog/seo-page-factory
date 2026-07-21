#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import socket
import sys
import time
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

DEFAULT_BASE_URL = "https://anywhere.broly.ai/v1"
DEFAULT_MODEL = "kling-v3"
DEFAULT_TIMEOUT_SECONDS = 1200
DEFAULT_POLL_INTERVAL_SECONDS = 8


def user_env(name: str) -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
    except OSError:
        return None
    return str(value).strip() or None


def config_value(name: str, default: str | None = None) -> str | None:
    return user_env(name) or (os.environ.get(name) or "").strip() or default


def read_key() -> str:
    key = config_value("AGNES_API_KEY") or config_value("OPENAI_NEXT_API_KEY")
    if not key:
        raise SystemExit("error: AGNES_API_KEY or OPENAI_NEXT_API_KEY is not set")
    return key


def normalize_base_url(value: str) -> str:
    return (value or DEFAULT_BASE_URL).strip().rstrip("/")


def falsey(value: str | None) -> bool:
    return (value or "").strip().lower() in {"0", "false", "no", "off"}


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def normalize_proxy_url(value: str) -> str:
    value = value.strip()
    if value and "://" not in value:
        value = "http://" + value
    return value


def host_port_from_proxy(proxy_url: str) -> tuple[str, int] | None:
    match = re.match(r"^[a-zA-Z]+://([^:/]+):(\d+)", normalize_proxy_url(proxy_url))
    if not match:
        return None
    return match.group(1), int(match.group(2))


def local_port_open(host: str, port: int) -> bool:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        return True
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False


def windows_proxy_url() -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
        ) as key:
            enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
            if not int(enabled):
                return None
            server, _ = winreg.QueryValueEx(key, "ProxyServer")
    except OSError:
        return None
    server = str(server).strip()
    if ";" in server:
        parts = dict(part.split("=", 1) for part in server.split(";") if "=" in part)
        server = parts.get("https") or parts.get("http") or next(iter(parts.values()), "")
    proxy_url = normalize_proxy_url(server)
    host_port = host_port_from_proxy(proxy_url)
    if host_port and not local_port_open(*host_port):
        return None
    return proxy_url or None


def selected_proxy_url() -> str | None:
    override = config_value("AGNES_PROXY") or config_value("OPENAI_NEXT_PROXY")
    if override:
        return normalize_proxy_url(override)
    setting = config_value("AGNES_USE_PROXY") or config_value("OPENAI_NEXT_USE_PROXY")
    if falsey(setting):
        return None
    if truthy(setting) or setting is None:
        return windows_proxy_url()
    return None


def opener():
    proxy_url = selected_proxy_url()
    return build_opener(ProxyHandler({"http": proxy_url, "https": proxy_url} if proxy_url else {}))


def redact(text: str, key: str) -> str:
    return text.replace(key, "[REDACTED]") if key else text


def request_json(method: str, url: str, key: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if method == "POST":
        headers["Idempotency-Key"] = "agnes-video-" + uuid.uuid4().hex
    req = Request(url, data=body, headers=headers, method=method)
    try:
        with opener().open(req, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"error: HTTP {exc.code}: {redact(raw, key)}") from None
    except URLError as exc:
        raise SystemExit(f"error: request failed: {exc.reason}") from None
    text = raw.decode("utf-8", errors="replace")
    try:
        data = json.loads(text)
    except ValueError:
        raise SystemExit(f"error: expected JSON response, got: {text[:300]}") from None
    if not isinstance(data, dict):
        raise SystemExit(f"error: unexpected response: {data!r}")
    return data


def response_error(data: dict[str, Any]) -> str | None:
    if data.get("success") is False:
        return str(data.get("message") or data.get("error") or "provider returned success=false")
    error = data.get("error")
    if isinstance(error, dict):
        return str(error.get("message") or error.get("code") or error)
    if isinstance(error, str):
        return error
    return None


def recursive_urls(value: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_lower = str(key).lower()
            if isinstance(item, str) and key_lower in {"result_url", "url", "video_url", "output_url"}:
                urls.append(item)
            urls.extend(recursive_urls(item))
    elif isinstance(value, list):
        for item in value:
            urls.extend(recursive_urls(item))
    return urls


def task_id_from(data: dict[str, Any]) -> str | None:
    value = data.get("task_id") or data.get("id") or data.get("taskId")
    return value if isinstance(value, str) and value else None


def download(url: str, output: Path, timeout: int) -> Path:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CodexAgnesVideo/1.0)",
        "Accept": "video/mp4,video/*,*/*;q=0.8",
    }
    try:
        with opener().open(Request(url, headers=headers, method="GET"), timeout=timeout) as response:
            content = response.read()
            content_type = response.headers.get("Content-Type", "")
    except HTTPError as exc:
        raise SystemExit(f"error: video download failed with HTTP {exc.code}: {url}") from None
    except URLError as exc:
        raise SystemExit(f"error: video download failed: {exc.reason}") from None
    if not content:
        raise SystemExit(f"error: downloaded empty video: {url}")
    suffix = output.suffix
    if not suffix:
        suffix = mimetypes.guess_extension(content_type.split(";", 1)[0].strip()) or ".mp4"
        output = output.with_suffix(suffix)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)
    return output


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "duration": args.duration,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
    }
    if args.image:
        payload["images"] = args.image
    if args.negative_prompt:
        payload["negative_prompt"] = args.negative_prompt
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.agnes_mode:
        payload["metadata"] = {"agnes_mode": args.agnes_mode}
    if args.extra_json:
        try:
            extra = json.loads(args.extra_json)
        except ValueError as exc:
            raise SystemExit(f"error: --extra-json is not valid JSON: {exc}") from None
        if not isinstance(extra, dict):
            raise SystemExit("error: --extra-json must be a JSON object")
        payload.update(extra)
    return payload


def submit_task(args: argparse.Namespace, key: str) -> dict[str, Any]:
    url = normalize_base_url(args.base_url) + "/tasks"
    return request_json("POST", url, key, build_payload(args), min(args.submit_timeout, args.timeout))


def poll_task(args: argparse.Namespace, key: str, task_id: str) -> dict[str, Any]:
    url = normalize_base_url(args.base_url) + f"/tasks/{task_id}"
    deadline = time.time() + args.timeout
    last_status = "submitted"
    last_data: dict[str, Any] = {}
    while time.time() < deadline:
        data = request_json("GET", url, key, None, min(60, args.timeout))
        last_data = data
        provider_error = response_error(data)
        if provider_error:
            raise SystemExit(f"error: task {task_id} status query failed: {provider_error}") from None
        status = str(data.get("status") or "").upper()
        if status:
            last_status = status
        if status == "SUCCESS" or recursive_urls(data):
            return data
        if status == "FAILURE":
            reason = data.get("fail_reason") or data.get("message") or data.get("error") or "unknown"
            raise SystemExit(f"error: task {task_id} failed: {reason}")
        time.sleep(args.poll_interval)
    raise SystemExit(f"error: task {task_id} did not finish before timeout; last status: {last_status}; last={last_data}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate videos via Broly/New API task endpoint, defaulting to Kling.")
    parser.add_argument("-p", "--prompt", required=True)
    parser.add_argument("-f", "--file", default="outputs/kling-video.mp4")
    parser.add_argument("--base-url", default=config_value("AGNES_BASE_URL") or config_value("OPENAI_NEXT_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default=config_value("AGNES_MODEL", DEFAULT_MODEL))
    parser.add_argument("--image", action="append", help="Public image URL. Repeat for multiple references/keyframes.")
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--resolution", default="720p")
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--agnes-mode", choices=["keyframes", "reference"], default="")
    parser.add_argument("--timeout", type=int, default=int(config_value("AGNES_TIMEOUT", str(DEFAULT_TIMEOUT_SECONDS)) or DEFAULT_TIMEOUT_SECONDS))
    parser.add_argument("--submit-timeout", type=int, default=360)
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL_SECONDS)
    parser.add_argument("--extra-json", default="")
    args = parser.parse_args()

    key = read_key()
    submitted = submit_task(args, key)
    provider_error = response_error(submitted)
    if provider_error:
        raise SystemExit(f"error: task submit failed: {provider_error}")
    urls = recursive_urls(submitted)
    task_id = task_id_from(submitted)
    result = submitted if urls else None
    if result is None:
        if not task_id:
            raise SystemExit(f"error: task submit response did not contain task_id: {submitted}")
        result = poll_task(args, key, task_id)
        urls = recursive_urls(result)
    if not urls:
        raise SystemExit(f"error: task did not return result_url: {result}")

    path = download(urls[0], Path(args.file), min(300, args.timeout))
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
