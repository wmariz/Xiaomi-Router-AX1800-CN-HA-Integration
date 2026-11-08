"""Cliente da API local (LuCI) dos roteadores Xiaomi AX1800."""
from __future__ import annotations

import asyncio
import hashlib
import json
import random
import re
import time
from typing import Any
from urllib.parse import urlencode

import aiohttp

DEFAULT_KEY = "a2ffa5c9be07488bbb04a3a47d3c5f6a"


class MiWiFiAuthError(Exception):
    """Senha recusada."""


class MiWiFiConnError(Exception):
    """Roteador inacessível."""


class MiWiFiApi:
    def __init__(self, session: aiohttp.ClientSession, host: str, password: str) -> None:
        self._s = session
        self.host = host
        self._pwd = password
        self._token: str | None = None
        self._lock = asyncio.Lock()

    async def _text(self, url: str, data: dict | None = None) -> str:
        try:
            async with asyncio.timeout(12):
                if data is None:
                    r = await self._s.get(url)
                else:
                    r = await self._s.post(url, data=data)
                return await r.text()
        except (aiohttp.ClientError, TimeoutError) as err:
            raise MiWiFiConnError(str(err)) from err

    async def login(self) -> None:
        page = await self._text(f"http://{self.host}/cgi-bin/luci/web")
        dev = re.search(r"deviceId\s*=\s*'([^']+)'", page)
        key = re.search(r"key:\s*'([0-9a-f]{32})'", page)
        nonce = f"0_{dev.group(1) if dev else ''}_{int(time.time())}_{random.randint(0, 9999)}"
        k = key.group(1) if key else DEFAULT_KEY
        inner = hashlib.sha1((self._pwd + k).encode()).hexdigest()
        pwd = hashlib.sha1((nonce + inner).encode()).hexdigest()
        txt = await self._text(
            f"http://{self.host}/cgi-bin/luci/api/xqsystem/login",
            {"username": "admin", "password": pwd, "logtype": 2, "nonce": nonce},
        )
        try:
            j = json.loads(txt)
        except ValueError as err:
            raise MiWiFiConnError("resposta inválida no login") from err
        if j.get("code") != 0 or not j.get("token"):
            raise MiWiFiAuthError(f"code {j.get('code')}")
        self._token = j["token"]

    async def call(self, ep: str, params: dict | None = None, post: bool = False) -> dict[str, Any]:
        async with self._lock:
            for tentativa in range(2):
                if not self._token:
                    await self.login()
                url = f"http://{self.host}/cgi-bin/luci/;stok={self._token}/api/{ep}"
                if post:
                    txt = await self._text(url, params or {})
                else:
                    if params:
                        url += "?" + urlencode(params)
                    txt = await self._text(url)
                try:
                    j = json.loads(txt)
                except ValueError:
                    j = {"code": -1, "msg": txt[:200]}
                if isinstance(j, dict) and j.get("code") == 401 and tentativa == 0:
                    self._token = None
                    continue
                return j
            return j

    async def safe(self, ep: str, params: dict | None = None) -> dict[str, Any]:
        try:
            j = await self.call(ep, params)
            return j if isinstance(j, dict) else {}
        except MiWiFiConnError:
            raise
        except Exception:  # noqa: BLE001 - endpoint opcional
            return {}
