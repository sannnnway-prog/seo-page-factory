#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_MODEL = "doubao-seedream-5-0-pro-260628"


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
    key = config_value("ARK_API_KEY")
    if not key:
        raise SystemExit("error: ARK_API_KEY is not set")
    return key


def normalize_base_url(value: str) -> str:
    return (value or DEFAULT_BASE_URL).strip().rstrip("/")


def redact(text: str, key: str) -> str:
    if key:
        text = text.replace(key, "[REDACTED]")
    return re.sub(r"ark-[A-Za-z0-9_-]+", "ark-[REDACTED]", text)


def request_generation(args: argparse.Namespace, key: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "response_format": args.response_format,
    }
    if args.image:
        encoded_images: list[str] = []
        for image_path in args.image:
            path = Path(image_path)
            if not path.is_file():
                raise SystemExit(f"error: reference image not found: {path}")
            mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            encoded_images.append(f"data:{mime_type};base64,{encoded}")
        payload["image"] = encoded_images[0] if len(encoded_images) == 1 else encoded_images
    if args.extra_json:
        try:
            extra = json.loads(args.extra_json)
        except ValueError as exc:
            raise SystemExit(f"error: --extra-json is not valid JSON: {exc}") from None
        if not isinstance(extra, dict):
            raise SystemExit("error: --extra-json must be a JSON object")
        payload.update(extra)

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    url = normalize_base_url(args.base_url) + "/images/generations"
    request = Request(url, data=body, headers=headers, method="POST")
    try:
        with urlopen(request, timeout=args.timeout) as response:
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
    if data.get("error"):
        raise SystemExit(f"error: provider returned error: {redact(json.dumps(data['error'], ensure_ascii=False), key)}")
    return data


def first_image(data: dict[str, Any]) -> tuple[str, str]:
    items = data.get("data")
    if not isinstance(items, list) or not items:
        raise SystemExit(f"error: response did not contain image data: {data}")
    item = items[0]
    if not isinstance(item, dict):
        raise SystemExit(f"error: unexpected image item: {item!r}")
    if isinstance(item.get("url"), str) and item["url"]:
        return "url", item["url"]
    if isinstance(item.get("b64_json"), str) and item["b64_json"]:
        return "b64_json", item["b64_json"]
    raise SystemExit(f"error: response did not contain url or b64_json: {item}")


def save_image(kind: str, value: str, output: Path, timeout: int) -> Path:
    if kind == "url":
        try:
            with urlopen(Request(value, headers={"User-Agent": "CodexArkSeedream/1.0"}), timeout=timeout) as response:
                content = response.read()
                content_type = response.headers.get("Content-Type", "")
        except HTTPError as exc:
            raise SystemExit(f"error: image download failed with HTTP {exc.code}") from None
        except URLError as exc:
            raise SystemExit(f"error: image download failed: {exc.reason}") from None
        suffix = output.suffix or mimetypes.guess_extension(content_type.split(";", 1)[0].strip()) or ".jpg"
    else:
        content = base64.b64decode(value)
        suffix = output.suffix or ".png"
    if not content:
        raise SystemExit("error: downloaded empty image")
    if not output.suffix:
        output = output.with_suffix(suffix)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images with Volcengine Ark Seedream.")
    parser.add_argument("-p", "--prompt", required=True)
    parser.add_argument("-f", "--file", default="outputs/ark-seedream.png")
    parser.add_argument("-i", "--image", action="append", help="Local reference image; repeat for multi-image input")
    parser.add_argument("--base-url", default=config_value("ARK_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model", default=config_value("ARK_IMAGE_MODEL", DEFAULT_MODEL))
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--response-format", default="url", choices=["url", "b64_json"])
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--extra-json", default="")
    args = parser.parse_args()

    key = read_key()
    data = request_generation(args, key)
    kind, value = first_image(data)
    path = save_image(kind, value, Path(args.file), args.timeout)
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
