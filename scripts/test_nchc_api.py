#!/usr/bin/env python3
"""Standalone connectivity check for the NCHC GenAI Portal, independent of Hermes.

Usage:
    python3 scripts/test_nchc_api.py

Reads NCHC_API_KEY from the environment, falling back to .env in the repo
root or ~/.hermes/.env. Hits /models (cheap) then sends one tiny chat
completion to confirm the key actually works end to end.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = os.environ.get("NCHC_BASE_URL", "https://portal.genai.nchc.org.tw/api/v1")
TEST_MODEL = "Devstral-2-123B-Instruct-2512"
REPO_ROOT = Path(__file__).resolve().parent.parent


def load_dotenv_value(key: str) -> str:
    if os.environ.get(key):
        return os.environ[key]
    for candidate in (REPO_ROOT / ".env", Path.home() / ".hermes" / ".env"):
        if not candidate.is_file():
            continue
        for line in candidate.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() == key:
                v = v.strip().strip('"').strip("'")
                if v:
                    return v
    return ""


def request(path: str, api_key: str, body: dict | None = None) -> tuple[int, str]:
    url = BASE_URL.rstrip("/") + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if body is not None else "GET")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Accept", "application/json")
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        return -1, str(exc.reason)


def main() -> int:
    print(f"NCHC_BASE_URL = {BASE_URL}")
    api_key = load_dotenv_value("NCHC_API_KEY")
    if not api_key:
        print("✗ 找不到 NCHC_API_KEY（環境變數或 .env 都沒有）。")
        return 1
    print(f"NCHC_API_KEY  = {api_key[:6]}...{api_key[-4:]} (length {len(api_key)})")
    print()

    print("== 1) GET /models ==")
    status, body = request("/models", api_key)
    print(f"HTTP {status}")
    if status == 200:
        try:
            ids = [m.get("id") for m in json.loads(body).get("data", []) if isinstance(m, dict)]
            print(f"✓ 拿到 {len(ids)} 個模型" + (f"，例如：{ids[:5]}" if ids else ""))
        except Exception:
            print("✓ 回傳 200，但內容格式不是預期的 JSON，原文：")
            print(body[:500])
    else:
        print("回傳內容：")
        print(body[:500])
    print()

    print(f"== 2) POST /chat/completions（model={TEST_MODEL}）==")
    status, body = request(
        "/chat/completions",
        api_key,
        {
            "model": TEST_MODEL,
            "messages": [{"role": "user", "content": "回覆兩個字：測試成功"}],
            "max_tokens": 16,
        },
    )
    print(f"HTTP {status}")
    print(body[:800])
    print()

    if status == 200:
        print("✓ 全部通過：金鑰有效，NCHC GenAI Portal 可以正常使用。")
        return 0

    hints = {
        401: "金鑰驗證失敗 —— 確認 NCHC_API_KEY 是否正確、有沒有多餘空白、是否已過期或被停用。",
        403: "被拒絕存取 —— 金鑰可能沒有這個模型的權限，或帳號尚未開通。",
        404: "路徑找不到 —— 可能是 NCHC_BASE_URL 設錯，或 API 路徑有變動。",
        429: "被限流 —— 太多請求，稍後再試。",
    }
    print("✗ 測試失敗。" + hints.get(status, "請確認網路連線與 NCHC 帳號狀態。"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
