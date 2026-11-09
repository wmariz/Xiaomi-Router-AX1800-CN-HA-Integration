"""Cliente da API local (LuCI) dos roteadores Xiaomi AX1800."""
from __future__ import annotations

import asyncio
import hashlib
import json
import random
import re
import time
from typing import Any
from urllib.parse import urlencode, urlsplit

import aiohttp

DEFAULT_KEY = "a2ffa5c9be07488bbb04a3a47d3c5f6a"
# endpoints that take long to answer (scans, diagnosis, uploads)
SLOW = {"scan_mesh_node", "wifi_list", "nettb", "c_upload", "check_wan_type", "add_mesh_node"}


def _dechunk(b: bytes) -> bytes:
    out, i = b"", 0
    while i < len(b):
        j = b.find(b"\r\n", i)
        if j < 0:
            break
        try:
            n = int(b[i:j].split(b";")[0], 16)
        except ValueError:
            return b
        if n == 0:
            break
        out += b[j + 2 : j + 2 + n]
        i = j + 2 + n + 2
    return out


def multipart(campos: dict, arquivo: dict) -> tuple[bytes, str]:
    """Corpo multipart/form-data com o arquivo no campo 'image' (como a página oficial envia)."""
    import base64
    import uuid
    limite = "----miwifi" + uuid.uuid4().hex
    partes = [
        f'--{limite}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        for k, v in (campos or {}).items()
    ]
    nome = str(arquivo.get("nome") or "arquivo.bin").replace('"', "")
    partes.append(
        f'--{limite}\r\nContent-Disposition: form-data; name="image"; filename="{nome}"\r\n'
        "Content-Type: application/octet-stream\r\n\r\n".encode()
        + base64.b64decode(arquivo.get("b64") or "")
        + b"\r\n"
    )
    partes.append(f"--{limite}--\r\n".encode())
    return b"".join(partes), f"multipart/form-data; boundary={limite}"


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

    async def _text(self, url: str, data: dict | None = None, bruto: tuple[bytes, str] | None = None, limite: int = 12) -> str:
        """HTTP/1.0 simples e tolerante.

        Alguns endpoints do firmware (ex.: misystem/led?on=1 no repetidor) respondem
        com cabeçalhos malformados, que o parser do aiohttp rejeita. Aqui o corpo é
        extraído sem validar cabeçalhos.
        """
        u = urlsplit(url)
        path = u.path + (f"?{u.query}" if u.query else "")
        corpo = bruto[0] if bruto else (urlencode(data).encode() if data is not None else b"")
        tipo = bruto[1] if bruto else "application/x-www-form-urlencoded"
        if bruto:
            data = {}
        linhas = [
            f"{'POST' if data is not None else 'GET'} {path} HTTP/1.0",
            f"Host: {u.hostname}",
            "Connection: close",
            "User-Agent: miwifi_ax",
        ]
        if data is not None:
            linhas += [f"Content-Type: {tipo}", f"Content-Length: {len(corpo)}"]
        req = ("\r\n".join(linhas) + "\r\n\r\n").encode() + corpo
        writer = None
        try:
            async with asyncio.timeout(limite):
                reader, writer = await asyncio.open_connection(u.hostname, u.port or 80)
                writer.write(req)
                await writer.drain()
                bruto = await reader.read()
        except (OSError, TimeoutError) as err:
            raise MiWiFiConnError(str(err)) from err
        finally:
            if writer is not None:
                writer.close()
        cab, sep, resto = bruto.partition(b"\r\n\r\n")
        if not sep:
            cab, sep, resto = bruto.partition(b"\n\n")
        if b"chunked" in cab.lower():
            resto = _dechunk(resto)
        return resto.decode("utf-8", "replace")

    async def login(self) -> None:
        page = await self._text(f"http://{self.host}/cgi-bin/luci/web")
        dev = re.search(r"deviceId\s*=\s*'([^']+)'", page)
        key = re.search(r"key:\s*'([0-9a-f]{32})'", page)
        k = key.group(1) if key else DEFAULT_KEY
        inner = hashlib.sha1((self._pwd + k).encode()).hexdigest()
        for tentativa in range(4):
            nonce = f"0_{dev.group(1) if dev else ''}_{int(time.time())}_{random.randint(0, 9999)}"
            pwd = hashlib.sha1((nonce + inner).encode()).hexdigest()
            txt = await self._text(
                f"http://{self.host}/cgi-bin/luci/api/xqsystem/login",
                {"username": "admin", "password": pwd, "logtype": 2, "nonce": nonce},
            )
            try:
                j = json.loads(txt)
            except ValueError as err:
                raise MiWiFiConnError("invalid login response") from err
            # 1582: login logo após outro (nonce com o mesmo segundo/recusado) — não é senha errada.
            if j.get("code") == 1582 and tentativa < 3:
                await asyncio.sleep(2)
                continue
            break
        if j.get("code") == 1582:
            raise MiWiFiConnError("router refused back-to-back logins (code 1582)")
        if j.get("code") != 0 or not j.get("token"):
            raise MiWiFiAuthError(f"code {j.get('code')}")
        self._token = j["token"]

    async def call(self, ep: str, params: dict | None = None, post: bool = False, arquivo: dict | None = None) -> dict[str, Any]:
        async with self._lock:
            for tentativa in range(2):
                if not self._token:
                    await self.login()
                url = f"http://{self.host}/cgi-bin/luci/;stok={self._token}/api/{ep}"
                lim = 60 if ep.rsplit("/", 1)[-1] in SLOW else 12
                if arquivo:
                    txt = await self._text(url, bruto=multipart(params or {}, arquivo), limite=lim)
                elif post:
                    txt = await self._text(url, params or {}, limite=lim)
                else:
                    if params:
                        url += "?" + urlencode(params)
                    txt = await self._text(url, limite=lim)
                try:
                    j = json.loads(txt)
                except ValueError:
                    j = {"code": -1, "msg": txt[:200]}
                if isinstance(j, dict) and j.get("code") == 401 and tentativa == 0:
                    self._token = None
                    continue
                return j
            return j

    async def page(self, path: str) -> str:
        """Página da interface web (para descobrir funções). Nunca 'logout'."""
        if "logout" in path or "login" in path:
            return ""
        async with self._lock:
            if not self._token:
                await self.login()
            return await self._text(f"http://{self.host}/cgi-bin/luci/;stok={self._token}/{path}")

    async def safe(self, ep: str, params: dict | None = None) -> dict[str, Any]:
        try:
            j = await self.call(ep, params)
            return j if isinstance(j, dict) else {}
        except MiWiFiConnError:
            raise
        except Exception:  # noqa: BLE001 - endpoint opcional
            return {}
