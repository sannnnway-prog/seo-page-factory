#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import copy
import http.client
import multiprocessing as mp
import mimetypes
import json
import os
import re
import socket
import sys
import time
import uuid
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener, urlopen

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")


DEFAULT_BASE_URL = "https://anywhere.broly.ai/v1"
DEFAULT_MODEL = "seedream-5.0-pro"
DEFAULT_MODEL_CANDIDATES = ["seedream-5.0-pro", "seedream-5.0-lite", "nano-banana-2", "gpt-image-2"]
DEFAULT_TIMEOUT_SECONDS = 600
DEFAULT_POLL_INTERVAL_SECONDS = 8
MAX_RETRIES = 3


SIZE_MAP = {
    "1k": "1024x1024",
    "square": "1024x1024",
    "portrait": "1024x1536",
    "landscape": "1536x1024",
    "wide": "1792x1024",
    "tall": "1024x1792",
    "2k": "2048x2048",
    "4k": "3840x2160",
}


def normalize_base_url(value: str) -> str:
    value = value.strip().rstrip("/")
    return value or DEFAULT_BASE_URL


def user_env(name: str) -> str | None:
    """Read Windows user env directly so existing Codex threads see refreshed keys."""
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


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def falsey(value: str | None) -> bool:
    return (value or "").strip().lower() in {"0", "false", "no", "off"}


def int_config(name: str, default: int) -> int:
    value = config_value(name)
    if not value:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return max(parsed, 30)


def json_config(name: str) -> dict[str, Any]:
    value = config_value(name, "")
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except ValueError as exc:
        raise SystemExit(f"error: {name} is not valid JSON: {exc}") from None
    if not isinstance(parsed, dict):
        raise SystemExit(f"error: {name} must be a JSON object")
    return parsed


def endpoint(base_url: str, mode: str) -> str:
    path = "/images/edits" if mode == "edit" else "/images/generations"
    return normalize_base_url(base_url) + path


def api_endpoint(base_url: str, path: str) -> str:
    return normalize_base_url(base_url) + "/" + path.lstrip("/")


def task_status_requests(base_url: str, task_id: str) -> list[tuple[str, str, dict[str, Any] | None]]:
    override = config_value("OPENAI_NEXT_TASK_URL", "")
    if override:
        return [("GET", override.replace("{task_id}", task_id), None)]
    base = normalize_base_url(base_url)
    origin = origin_from_base_url(base_url)
    query = urlencode({"p": "0", "size": "10", "task_id": task_id})
    return [
        ("GET", f"{base}/tasks/{task_id}", None),
        ("POST", f"{base}/tasks", {"task_id": task_id}),
        ("POST", f"{base}/tasks", {"id": task_id}),
        ("POST", f"{base}/tasks", {"taskId": task_id}),
        ("GET", f"{origin}/api/task/self?{query}", None),
    ]


def origin_from_base_url(base_url: str) -> str:
    value = normalize_base_url(base_url)
    match = re.match(r"^(https?://[^/]+)", value)
    if not match:
        return value
    return match.group(1)


def normalize_proxy_url(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    if "://" not in value:
        value = "http://" + value
    return value


def host_port_from_proxy(proxy_url: str) -> tuple[str, int] | None:
    proxy_url = normalize_proxy_url(proxy_url)
    match = re.match(r"^[a-zA-Z]+://([^:/]+):(\d+)", proxy_url)
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
    if not server:
        return None
    if ";" in server:
        parts = dict(part.split("=", 1) for part in server.split(";") if "=" in part)
        server = parts.get("https") or parts.get("http") or next(iter(parts.values()), "")
    proxy_url = normalize_proxy_url(server)
    host_port = host_port_from_proxy(proxy_url)
    if host_port and not local_port_open(*host_port):
        return None
    return proxy_url or None


def selected_proxy_url() -> str | None:
    override = config_value("OPENAI_NEXT_PROXY")
    if override:
        return normalize_proxy_url(override)
    setting = config_value("OPENAI_NEXT_USE_PROXY")
    if falsey(setting):
        return None
    if truthy(setting) or setting is None:
        return windows_proxy_url()
    return None


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text[:48] or "image"


def read_key() -> str:
    key = config_value("OPENAI_NEXT_API_KEY")
    if not key:
        raise SystemExit(
            "error: OPENAI_NEXT_API_KEY is not set. Set a dedicated key for the "
            "openai-next third-party endpoint. OPENAI_API_KEY is not used as a fallback."
        )
    return key


def response_images(data: dict[str, Any]) -> list[str]:
    images, _ = recursive_image_values(data)
    return images


def looks_like_image_url(value: str) -> bool:
    if not value.startswith(("http://", "https://")):
        return False
    lower = value.lower().split("?", 1)[0]
    return lower.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")) or any(
        marker in lower for marker in ("/image/", "/images/", "/file/", "/files/", "/cdn/")
    )


def recursive_image_values(value: Any) -> tuple[list[str], list[str]]:
    b64_images: list[str] = []
    urls: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_lower = str(key).lower()
            if isinstance(item, str):
                if key_lower in {"b64_json", "base64", "image_base64"}:
                    b64_images.append(item)
                elif item.startswith("data:image/") and "," in item:
                    b64_images.append(item.split(",", 1)[1])
                elif key_lower in {"url", "image_url", "result_url", "output_url"} and item.startswith(
                    ("http://", "https://")
                ):
                    urls.append(item)
            child_b64, child_urls = recursive_image_values(item)
            b64_images.extend(child_b64)
            urls.extend(child_urls)
    elif isinstance(value, list):
        for item in value:
            child_b64, child_urls = recursive_image_values(item)
            b64_images.extend(child_b64)
            urls.extend(child_urls)
    elif isinstance(value, str):
        if value.startswith("data:image/") and "," in value:
            b64_images.append(value.split(",", 1)[1])
        elif looks_like_image_url(value):
            urls.append(value)
    return b64_images, urls


def response_task_ids(data: dict[str, Any]) -> list[str]:
    task_ids: list[str] = []
    stack: list[Any] = [data]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            task_id = value.get("task_id") or value.get("taskId")
            status = str(value.get("status") or "").lower()
            if isinstance(task_id, str) and status in {"submitted", "pending", "queued", "running", "processing"}:
                task_ids.append(task_id)
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
    return task_ids


def response_error(data: dict[str, Any]) -> str | None:
    if data.get("success") is False:
        return str(data.get("message") or data.get("error") or "provider returned success=false")
    error = data.get("error")
    if isinstance(error, dict):
        message = error.get("message") or error.get("code") or error.get("type")
        return str(message or error)
    if isinstance(error, str):
        return error
    return None


def compact_response_summary(data: dict[str, Any]) -> str:
    def shrink(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: shrink(item) for key, item in list(value.items())[:20]}
        if isinstance(value, list):
            return [shrink(item) for item in value[:5]]
        if isinstance(value, str):
            if value.startswith("data:image/"):
                return value[:40] + f"... len={len(value)}"
            if len(value) > 240:
                return value[:240] + f"... len={len(value)}"
        return value

    text = json.dumps(shrink(data), ensure_ascii=False)
    return text[:1200] + ("..." if len(text) > 1200 else "")


def model_candidates(args: argparse.Namespace) -> list[str]:
    raw = (args.models or "").strip()
    if raw:
        candidates = [item.strip() for item in raw.split(",") if item.strip()]
    elif args.model in DEFAULT_MODEL_CANDIDATES:
        candidates = list(DEFAULT_MODEL_CANDIDATES)
    else:
        candidates = [args.model]
    if not raw and args.model not in candidates:
        candidates.insert(0, args.model)
    seen: set[str] = set()
    unique: list[str] = []
    for model in candidates:
        if model not in seen:
            seen.add(model)
            unique.append(model)
    return unique


def format_candidates(args: argparse.Namespace, model: str) -> list[str]:
    if args.api_format != "auto":
        return [args.api_format]
    if model.startswith("nano-banana") or model.startswith("seedream-"):
        return ["task"]
    return ["openai-image"]


def extra_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = dict(args.extra_json_env or {})
    if args.extra_json_file:
        path = Path(args.extra_json_file)
        if not path.is_file():
            raise SystemExit(f"error: --extra-json-file not found: {path}")
        try:
            parsed_file = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise SystemExit(f"error: --extra-json-file is not valid JSON: {exc}") from None
        if not isinstance(parsed_file, dict):
            raise SystemExit("error: --extra-json-file must contain a JSON object")
        payload.update(parsed_file)
    if args.extra_json:
        try:
            parsed = json.loads(args.extra_json)
        except ValueError as exc:
            raise SystemExit(f"error: --extra-json is not valid JSON: {exc}") from None
        if not isinstance(parsed, dict):
            raise SystemExit("error: --extra-json must be a JSON object")
        payload.update(parsed)
    return payload


def collect_response_images(args: argparse.Namespace, key: str, data: dict[str, Any]) -> list[str]:
    provider_error = response_error(data)
    if provider_error:
        raise RuntimeError(provider_error)

    b64_images, urls = recursive_image_values(data)
    images = list(b64_images)
    for url in urls:
        images.append(base64.b64encode(download_bytes(url, min(120, args.timeout))).decode("ascii"))
    for task_id in response_task_ids(data):
        images.extend(poll_task_images(args, key, task_id))
    return images


def task_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    containers: list[Any] = [data, data.get("data")]
    if isinstance(data.get("data"), dict):
        containers.extend(
            [
                data["data"].get("items"),
                data["data"].get("list"),
                data["data"].get("records"),
            ]
        )
    items: list[dict[str, Any]] = []
    for container in containers:
        if isinstance(container, list):
            items.extend([item for item in container if isinstance(item, dict)])
        elif isinstance(container, dict) and any(key in container for key in ("task_id", "status", "result_url")):
            items.append(container)
    return items


def save_images(images: list[str], output: Path, fmt: str) -> list[Path]:
    output.parent.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for index, b64 in enumerate(images, start=1):
        suffix = output.suffix or f".{fmt}"
        if len(images) == 1:
            path = output.with_suffix(suffix)
        else:
            path = output.with_name(f"{output.stem}-{index}{suffix}")
        path.write_bytes(base64.b64decode(b64))
        paths.append(path)
    return paths


def save_image_bytes(images: list[bytes], output: Path, fmt: str) -> list[Path]:
    output.parent.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for index, content in enumerate(images, start=1):
        suffix = output.suffix or f".{fmt}"
        if len(images) == 1:
            path = output.with_suffix(suffix)
        else:
            path = output.with_name(f"{output.stem}-{index}{suffix}")
        path.write_bytes(content)
        paths.append(path)
    return paths


def file_tuple(path: Path) -> tuple[str, bytes, str]:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return (path.name, path.read_bytes(), mime)


def post_generation(args: argparse.Namespace, key: str, api_format: str) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if api_format == "task":
        headers["Connection"] = "close"
        headers["Idempotency-Key"] = "openai-next-image-" + uuid.uuid4().hex
        payload = {
            "model": args.model,
            "prompt": args.prompt,
            "size": SIZE_MAP.get(args.size, args.size),
            "quality": args.quality,
        }
        if args.format:
            payload["output_format"] = args.format
        payload.update(extra_payload(args))
        body = json.dumps(payload).encode("utf-8")
        return post_bytes(api_endpoint(args.base_url, "/tasks"), headers, body, args.timeout)

    if api_format == "gemini":
        origin = origin_from_base_url(args.base_url)
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": args.prompt}],
                }
            ],
            "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
        }
        payload.update(extra_payload(args))
        body = json.dumps(payload).encode("utf-8")
        return post_bytes(f"{origin}/v1beta/models/{args.model}:generateContent", headers, body, args.timeout)

    if api_format == "chat":
        payload = {
            "model": args.model,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"{args.prompt}\n\nReturn one generated image. "
                        "If possible, include the image as base64 or an image URL."
                    ),
                }
            ],
        }
        payload.update(extra_payload(args))
        body = json.dumps(payload).encode("utf-8")
        return post_bytes(api_endpoint(args.base_url, "/chat/completions"), headers, body, args.timeout)

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "size": SIZE_MAP.get(args.size, args.size),
        "quality": args.quality,
        "n": args.n,
    }
    if args.format:
        payload["response_format"] = "b64_json"
        payload["output_format"] = args.format
    payload.update(extra_payload(args))

    body = json.dumps(payload).encode("utf-8")
    return post_bytes(endpoint(args.base_url, "generate"), headers, body, args.timeout)


def post_edit(args: argparse.Namespace, key: str) -> dict[str, Any]:
    data = {
        "model": args.model,
        "prompt": args.prompt,
        "size": SIZE_MAP.get(args.size, args.size),
        "quality": args.quality,
        "n": str(args.n),
    }
    files: list[tuple[str, tuple[str, bytes, str]]] = []
    for image in args.image or []:
        path = Path(image)
        if not path.is_file():
            raise SystemExit(f"error: reference image not found: {path}")
        files.append(("image[]", file_tuple(path)))
    if args.mask:
        mask = Path(args.mask)
        if not mask.is_file():
            raise SystemExit(f"error: mask not found: {mask}")
        files.append(("mask", file_tuple(mask)))

    boundary = "----openai-next-image-" + uuid.uuid4().hex
    body = build_multipart(data, files, boundary)
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    return post_bytes(endpoint(args.base_url, "edit"), headers, body, args.timeout)


def build_multipart(
    fields: dict[str, str],
    files: list[tuple[str, tuple[str, bytes, str]]],
    boundary: str,
) -> bytes:
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                str(value).encode(),
                b"\r\n",
            ]
        )
    for name, (filename, content, mime) in files:
        chunks.extend(
            [
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode(),
                f"Content-Type: {mime}\r\n\r\n".encode(),
                content,
                b"\r\n",
            ]
        )
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks)


def redact_secrets(text: str, headers: dict[str, str]) -> str:
    auth = headers.get("Authorization", "")
    token = auth.removeprefix("Bearer ").strip()
    if token:
        text = text.replace(token, "[REDACTED]")
        if token.startswith("sk-"):
            text = text.replace(token[3:], "[REDACTED]")
    return re.sub(r"sk-[A-Za-z0-9_-]+", "sk-[REDACTED]", text)


def _post_worker(
    url: str,
    headers: dict[str, str],
    body: bytes,
    socket_timeout: int,
    proxy_url: str | None,
    queue: mp.Queue,
) -> None:
    request = Request(url, data=body, headers=headers, method="POST")
    if proxy_url:
        opener = build_opener(ProxyHandler({"http": proxy_url, "https": proxy_url}))
    else:
        opener = build_opener(ProxyHandler({}))
    try:
        with opener.open(request, timeout=socket_timeout) as response:
            queue.put(("ok", response.read()))
    except HTTPError as exc:
        raw = exc.read()
        text = raw.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text)
            text = json.dumps(parsed, ensure_ascii=False)
        except ValueError:
            pass
        queue.put(("http", exc.code, redact_secrets(text, headers)))
    except URLError as exc:
        queue.put(("urlerror", type(exc.reason).__name__, str(exc.reason)))
    except Exception as exc:
        queue.put(("error", type(exc).__name__, str(exc)))


def post_bytes(url: str, headers: dict[str, str], body: bytes, timeout: int) -> dict[str, Any]:
    # Auto-use the Windows proxy only when it is enabled and reachable. This
    # avoids stale localhost proxy 10061 while still supporting network routes
    # that need Clash/Verge/mihomo to reach the image provider.
    proxy_url = selected_proxy_url()
    transient_errors = (
        ConnectionAbortedError,
        ConnectionRefusedError,
        ConnectionError,
        ConnectionResetError,
        TimeoutError,
        http.client.RemoteDisconnected,
        socket.gaierror,
        socket.timeout,
    )
    transient_error_names = {cls.__name__ for cls in transient_errors} | {
        "RemoteDisconnected",
        "gaierror",
    }
    last_error: str | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        ctx = mp.get_context("spawn")
        queue = ctx.Queue()
        process = ctx.Process(target=_post_worker, args=(url, headers, body, timeout, proxy_url, queue))
        process.daemon = True
        process.start()
        process.join(timeout + 5)
        if process.is_alive():
            process.terminate()
            process.join(10)
            last_error = f"request exceeded hard timeout of {timeout} seconds"
            if attempt < MAX_RETRIES:
                time.sleep(3 * attempt)
                continue
            raise SystemExit(f"error: request failed after {attempt} attempt(s): {last_error}") from None
        if queue.empty():
            last_error = f"worker exited with code {process.exitcode}"
            if attempt < MAX_RETRIES:
                time.sleep(2 * attempt)
                continue
            raise SystemExit(f"error: request failed after {attempt} attempt(s): {last_error}") from None

        result = queue.get()
        kind = result[0]
        if kind == "ok":
            raw = result[1]
            break
        if kind == "http":
            _, code, text = result
            if code in {429, 500, 502, 503, 504} and attempt < MAX_RETRIES:
                last_error = f"HTTP {code}: {text}"
                time.sleep(3 * attempt)
                continue
            raise SystemExit(f"error: HTTP {code}: {text}") from None
        _, error_type, message = result
        last_error = f"{error_type}: {message}"
        if error_type in transient_error_names and attempt < MAX_RETRIES:
            time.sleep(2 * attempt)
            continue
        raise SystemExit(f"error: request failed after {attempt} attempt(s): {last_error}") from None
    else:
        raise SystemExit(f"error: request failed: {last_error or 'unknown network error'}")

    text = raw.decode("utf-8", errors="replace")
    try:
        data = json.loads(text)
    except ValueError:
        data = {"text": text}
    if not isinstance(data, dict):
        raise SystemExit(f"error: unexpected response: {data!r}")
    return data


def request_json(method: str, url: str, headers: dict[str, str], timeout: int) -> dict[str, Any]:
    proxy_url = selected_proxy_url()
    request = Request(url, headers=headers, method=method)
    opener = build_opener(ProxyHandler({"http": proxy_url, "https": proxy_url} if proxy_url else {}))
    try:
        with opener.open(request, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as exc:
        raw = exc.read()
        text = raw.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text)
            text = json.dumps(parsed, ensure_ascii=False)
        except ValueError:
            pass
        raise SystemExit(f"error: HTTP {exc.code}: {redact_secrets(text, headers)}") from None
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


def request_json_body(
    method: str,
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any] | None,
    timeout: int,
) -> dict[str, Any]:
    body = None
    request_headers = dict(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    proxy_url = selected_proxy_url()
    request = Request(url, data=body, headers=request_headers, method=method)
    opener = build_opener(ProxyHandler({"http": proxy_url, "https": proxy_url} if proxy_url else {}))
    try:
        with opener.open(request, timeout=timeout) as response:
            raw = response.read()
    except HTTPError as exc:
        raw = exc.read()
        text = raw.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text)
            text = json.dumps(parsed, ensure_ascii=False)
        except ValueError:
            pass
        raise SystemExit(f"error: HTTP {exc.code}: {redact_secrets(text, request_headers)}") from None
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


def download_bytes(url: str, timeout: int) -> bytes:
    proxy_url = selected_proxy_url()
    opener = build_opener(ProxyHandler({"http": proxy_url, "https": proxy_url} if proxy_url else {}))
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; CodexOpenAINextImage/1.0)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        }
        with opener.open(Request(url, headers=headers, method="GET"), timeout=timeout) as response:
            return response.read()
    except HTTPError as exc:
        raise SystemExit(f"error: image download failed with HTTP {exc.code}: {url}") from None
    except URLError as exc:
        raise SystemExit(f"error: image download failed: {exc.reason}") from None


def poll_task_images(args: argparse.Namespace, key: str, task_id: str) -> list[str]:
    headers = {"Authorization": f"Bearer {key}"}
    deadline = time.time() + args.timeout
    last_status = "submitted"
    last_errors: list[str] = []
    while time.time() < deadline:
        endpoint_errors: list[str] = []
        data = None
        for method, url, payload in task_status_requests(args.base_url, task_id):
            try:
                candidate = request_json_body(method, url, headers, payload, min(60, args.timeout))
            except SystemExit as exc:
                endpoint_errors.append(f"{method} {url}: {exc}")
                continue
            provider_error = response_error(candidate)
            if provider_error:
                endpoint_errors.append(f"{method} {url}: {provider_error}")
                continue
            data = candidate
            break
        if data is None:
            last_errors = endpoint_errors
            time.sleep(DEFAULT_POLL_INTERVAL_SECONDS)
            continue

        for item in task_items(data):
            if item.get("task_id") and item.get("task_id") != task_id:
                continue
            status = str(item.get("status") or "").lower()
            if status:
                last_status = status
            b64_images, urls = recursive_image_values(item)
            images = list(b64_images)
            for url in urls:
                images.append(base64.b64encode(download_bytes(url, min(120, args.timeout))).decode("ascii"))
            if images:
                return images
            if status in {"failure", "failed", "error"}:
                reason = item.get("fail_reason") or item.get("error") or item.get("message") or "unknown"
                raise SystemExit(f"error: image task {task_id} failed: {reason}")
        time.sleep(DEFAULT_POLL_INTERVAL_SECONDS)
    suffix = ""
    if last_errors:
        suffix = "; task endpoint errors: " + " | ".join(last_errors[-4:])
    raise SystemExit(f"error: image task {task_id} did not finish before timeout; last status: {last_status}{suffix}")


def collect_images(args: argparse.Namespace, key: str) -> list[str]:
    images: list[str] = []
    errors: list[str] = []
    count = max(args.n, 1)
    for image_index in range(count):
        generated = False
        attempt_errors: list[str] = []
        request_args = copy.copy(args)
        request_args.n = 1
        for model in model_candidates(args):
            request_args.model = model
            api_formats = ["openai-image"] if request_args.image else format_candidates(args, model)
            for api_format in api_formats:
                try:
                    if request_args.image:
                        data = post_edit(request_args, key)
                    else:
                        data = post_generation(request_args, key, api_format)
                    found = collect_response_images(request_args, key, data)
                except SystemExit as exc:
                    detail = str(exc) or "request failed"
                    attempt_errors.append(f"{model}/{api_format}: {detail}")
                    continue
                except Exception as exc:
                    attempt_errors.append(f"{model}/{api_format}: {type(exc).__name__}: {exc}")
                    continue

                if found:
                    images.extend(found)
                    generated = True
                    break
                attempt_errors.append(
                    f"{model}/{api_format}: response did not contain image data; "
                    f"summary={compact_response_summary(data)}"
                )
            if generated:
                break
        if not generated:
            errors.extend(attempt_errors)
            raise SystemExit(
                f"error: could not generate image {image_index + 1}/{count}; attempts:\n"
                + "\n".join(f"- {error}" for error in errors[-12:])
            )
    return images


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images via an OpenAI-compatible image endpoint.")
    parser.add_argument("-p", "--prompt", default="")
    parser.add_argument("-f", "--file", default=None)
    parser.add_argument("-i", "--image", action="append")
    parser.add_argument("-m", "--mask")
    parser.add_argument("--base-url", default=config_value("OPENAI_NEXT_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default=config_value("OPENAI_NEXT_MODEL", DEFAULT_MODEL))
    parser.add_argument(
        "--models",
        default=config_value("OPENAI_NEXT_MODELS", ""),
        help="Comma-separated fallback model list. Defaults to seedream-5.0-pro,seedream-5.0-lite,nano-banana-2,gpt-image-2.",
    )
    parser.add_argument(
        "--api-format",
        default=config_value("OPENAI_NEXT_API_FORMAT", "auto"),
        choices=["auto", "openai-image", "task", "gemini", "chat"],
        help="Provider API shape to try. auto uses /v1/tasks for seedream/nano-banana and OpenAI images for gpt-image.",
    )
    parser.add_argument(
        "--extra-json",
        default="",
        help="Extra JSON object merged into each provider request, for provider-specific fields.",
    )
    parser.add_argument(
        "--extra-json-file",
        default="",
        help="Path to a JSON object merged into each provider request; useful for large image data URLs.",
    )
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--quality", default="medium", choices=["auto", "low", "medium", "high"])
    parser.add_argument("--timeout", type=int, default=int_config("OPENAI_NEXT_TIMEOUT", DEFAULT_TIMEOUT_SECONDS))
    parser.add_argument("--task-id", default="", help="Recover/download an existing /v1/tasks image task by task_id.")
    parser.add_argument("-n", "--n", type=int, default=1)
    parser.add_argument("--format", default="png", choices=["png", "jpeg", "webp"])
    args = parser.parse_args()
    args.extra_json_env = json_config("OPENAI_NEXT_EXTRA_JSON")

    key = read_key()
    if args.task_id:
        images = poll_task_images(args, key, args.task_id)
    else:
        if not args.prompt:
            raise SystemExit("error: -p/--prompt is required unless --task-id is provided")
        images = collect_images(args, key)
    if not images:
        raise SystemExit("error: response did not contain b64_json/base64 image data")

    out = Path(args.file or f"{slugify(args.prompt)}.{args.format}")
    paths = save_images(images, out, args.format)
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
