"""Local panel for Xiaomi AX1800 (RM1800) routers.

Exposes the internal API (LuCI /api/...) of the main router and the repeater,
including functions that do not appear in the web interface.

Usage:  python painel.py      → opens http://127.0.0.1:8099 in the browser
(the Windows installer turns it into MiWiFiPainel.exe; opening it again just reopens the page)
Listens on 127.0.0.1 only. The password is typed into the page, goes straight to the router
(SHA1 hash with nonce, like the official interface) and is NOT stored.
Only the session (token) is kept in this process's memory.
"""
import hashlib
import json
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import os
import socket
import sys
import threading
import webbrowser

PASTA_CFG = Path(os.environ.get("APPDATA", Path.home())) / "MiWiFiPainel"
ARQ_CFG = PASTA_CFG / "config.json"
# inside the .exe (PyInstaller) the files live in sys._MEIPASS
BASE = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
PADRAO = {"principal": "192.168.0.1", "repetidor": "192.168.0.2"}
IP_RE = re.compile(r"^(25[0-5]|2[0-4]\d|1?\d?\d)(\.(25[0-5]|2[0-4]\d|1?\d?\d)){3}$")


def carregar_cfg():
    try:
        dados = json.loads(ARQ_CFG.read_text(encoding="utf-8"))
        r = {k: v for k, v in dados.get("roteadores", {}).items() if IP_RE.match(str(v))}
        return r or dict(PADRAO)
    except Exception:
        return dict(PADRAO)


def salvar_cfg(roteadores):
    PASTA_CFG.mkdir(parents=True, exist_ok=True)
    ARQ_CFG.write_text(json.dumps({"roteadores": roteadores}, ensure_ascii=False, indent=2), encoding="utf-8")


ROTEADORES = carregar_cfg()
PORTA = 8099
CHAVE_PADRAO = "a2ffa5c9be07488bbb04a3a47d3c5f6a"

# Web interface pages scanned to discover endpoints
PAGINAS = [
    "web/home", "web/setting/wifi", "web/setting/wan", "web/setting/lannetset",
    "web/setting/safe", "web/setting/upgrade", "web/apsetting/wifi",
    "web/store", "web/prosetting/qos",
    "web/prosetting/ddns", "web/prosetting/nat", "web/prosetting/vpn", "web/prosetting/upnp",
]
# Known read endpoints that do not appear in the pages
EXTRAS = [
    "api/misns/wifi_share_info", "api/misystem/status", "api/misystem/sys_time",
    "api/xqnetwork/wan_info", "api/xqnetwork/wifi_detail_all",
    "api/misystem/devicelist", "api/misystem/topo_graph", "api/misystem/messages",
    "api/misystem/qos_info", "api/xqnetwork/get_son_backhaul_mode",
    "api/xqnetwork/get_miscan_switch", "api/xqnetwork/get_miotrelay_switch",
    "api/xqsystem/country_code",
]
# Words that mean the endpoint CHANGES something (confirmation required)
ESCRITA = re.compile(
    r"(^|/)(set_|add_|del|remove|reboot|reset|shutdown|upgrade|flash|login|logout|"
    r"c_restore|c_upload|c_backup|bandwidth_test|scan_|qos_mode|qos_limit|qos_offlimit|qos_guest|"
    r"unbind|bind|apply|start|stop|clean|clear|format|repair|register|renew|grant|update|connect|"
    r"wps$|wps_cancel|iperf|speed_test$|ota$|password|disable|edit_|manually_|mac_clone|r_ip_conflict|"
    r"usb_u3|usbservice|usbmode|upload|web_access_opt|led$|netacctl_set|parctl_(add|delete|update)|request)"
    r"|switch",
    re.I,
)
SENSIVEIS = re.compile(r"(pass|pwd|psk|key|token|stok|secret|sswd|senha)", re.I)

sessoes: dict[str, str] = {}  # router -> token
cache_endpoints: dict[str, list] = {}


def multipart(campos: dict, arquivo: dict) -> tuple[bytes, str]:
    """multipart/form-data body with the file in the 'image' field (as the official page sends it)."""
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


def _http(url, dados=None, timeout=15, tipo="application/x-www-form-urlencoded"):
    req = urllib.request.Request(url, data=dados, method="POST" if dados else "GET")
    if dados:
        req.add_header("Content-Type", tipo)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def login(nome, senha):
    ip = ROTEADORES[nome]
    _, pagina = _http(f"http://{ip}/cgi-bin/luci/web")
    m_dev = re.search(r"deviceId\s*=\s*'([^']+)'", pagina)
    m_key = re.search(r"key:\s*'([0-9a-f]{32})'", pagina)
    device = m_dev.group(1) if m_dev else ""
    chave = m_key.group(1) if m_key else CHAVE_PADRAO
    nonce = f"0_{device}_{int(time.time())}_{random.randint(0, 9999)}"
    interno = hashlib.sha1((senha + chave).encode()).hexdigest()
    hashsenha = hashlib.sha1((nonce + interno).encode()).hexdigest()
    corpo = urllib.parse.urlencode(
        {"username": "admin", "password": hashsenha, "logtype": 2, "nonce": nonce}
    ).encode()
    _, resp = _http(f"http://{ip}/cgi-bin/luci/api/xqsystem/login", corpo)
    j = json.loads(resp)
    if j.get("code") == 0 and j.get("token"):
        sessoes[nome] = j["token"]
        cache_endpoints.pop(nome, None)
        return {"ok": True}
    return {"ok": False, "erro": f"Login recusado (code {j.get('code')})", "resp": mascarar(j)}


def mascarar(obj, mostrar=False):
    if mostrar:
        return obj
    if isinstance(obj, dict):
        return {
            k: ("••••••" if SENSIVEIS.search(k) and isinstance(v, (str, int)) and v != "" else mascarar(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [mascarar(v) for v in obj]
    return obj


def chamar(nome, endpoint, metodo="GET", params=None, mostrar=False, arquivo=None):
    if nome not in sessoes:
        return {"ok": False, "erro": "Faça login neste roteador primeiro."}
    ip, token = ROTEADORES[nome], sessoes[nome]
    endpoint = endpoint.lstrip("/")
    if not endpoint.startswith("api/"):
        endpoint = "api/" + endpoint
    url = f"http://{ip}/cgi-bin/luci/;stok={token}/{endpoint}"
    dados = None
    params = params or {}
    if metodo == "GET" and params:
        url += "?" + urllib.parse.urlencode(params)
    elif metodo == "POST":
        dados = urllib.parse.urlencode(params).encode() or b" "
    tipo = "application/x-www-form-urlencoded"
    if arquivo:
        dados, tipo = multipart(params, arquivo)
    try:
        lento = arquivo or endpoint.rsplit("/", 1)[-1] in {"scan_mesh_node", "wifi_list", "nettb", "c_upload", "check_wan_type", "add_mesh_node"}
        status, txt = _http(url, dados, 60 if lento else 15, tipo)
    except urllib.error.HTTPError as e:
        status, txt = e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # network
        return {"ok": False, "erro": str(e)}
    try:
        corpo = json.loads(txt)
        if isinstance(corpo, dict) and corpo.get("code") == 401:
            sessoes.pop(nome, None)
            return {"ok": False, "erro": "Sessão expirada: faça login de novo.", "status": status}
        return {"ok": True, "status": status, "json": mascarar(corpo, mostrar)}
    except ValueError:
        return {"ok": True, "status": status, "texto": txt[:3000]}


def descobrir(nome):
    if nome in cache_endpoints:
        return cache_endpoints[nome]
    if nome not in sessoes:
        return []
    ip, token = ROTEADORES[nome], sessoes[nome]
    achados = set(EXTRAS)
    for p in PAGINAS:
        try:
            _, html = _http(f"http://{ip}/cgi-bin/luci/;stok={token}/{p}")
        except Exception:
            continue
        achados.update(re.findall(r"api/[a-z_]+/[a-z_0-9]+", html, re.I))
        for src in re.findall(r'src="([^"]+\.js[^"]*)"', html):
            if src.startswith("/"):
                src = f"http://{ip}{src}"
            elif not src.startswith("http"):
                continue
            try:
                _, js = _http(src)
                achados.update(re.findall(r"api/[a-z_]+/[a-z_0-9]+", js, re.I))
            except Exception:
                pass
    lista = sorted(
        ({"endpoint": e, "escrita": bool(ESCRITA.search(e.split("/", 2)[-1]))} for e in achados),
        key=lambda d: (d["escrita"], d["endpoint"]),
    )
    cache_endpoints[nome] = lista
    return lista


def despejar(nome):
    """Saves the original pages + JS (without the token) for offline analysis."""
    if nome not in sessoes:
        return {"ok": False, "erro": "Faça login primeiro."}
    ip, token = ROTEADORES[nome], sessoes[nome]
    pasta = PASTA_CFG / "dump" / nome
    pasta.mkdir(parents=True, exist_ok=True)
    salvos = []
    paginas = set(PAGINAS)
    # finds other pages linked from the home page
    try:
        _, home = _http(f"http://{ip}/cgi-bin/luci/;stok={token}/web/home")
        paginas.update(re.findall(r"/(web/[a-z_/]+)", home.replace(token, "")))
        paginas -= {"web/logout", "web/login"}  # fetching 'logout' ends the session
    except Exception:
        pass
    for p in sorted(paginas):
        try:
            st, html = _http(f"http://{ip}/cgi-bin/luci/;stok={token}/{p}")
        except Exception:
            continue
        if st != 200:
            continue
        (pasta / (p.replace("/", "_") + ".html")).write_text(html.replace(token, "TOKEN"), encoding="utf-8")
        salvos.append(p)
        for src in re.findall(r'src="([^"]+\.js[^"]*)"', html):
            if src.startswith("/"):
                arq = pasta / ("js_" + re.sub(r"[^a-zA-Z0-9_.-]", "_", src.split("?")[0])[-80:])
                if not arq.exists():
                    try:
                        _, js = _http(f"http://{ip}{src}")
                        arq.write_text(js, encoding="utf-8")
                    except Exception:
                        pass
    return {"ok": True, "paginas": salvos, "pasta": str(pasta)}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        dados = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = dict(urllib.parse.parse_qsl(u.query))
        if u.path == "/":
            dados = (BASE / "painel.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(dados)))
            self.end_headers()
            self.wfile.write(dados)
        elif u.path == "/api/estado":
            self._json({"roteadores": ROTEADORES, "logado": {k: k in sessoes for k in ROTEADORES}})
        elif u.path == "/api/endpoints":
            self._json(descobrir(q.get("roteador", "")))
        else:
            self._json({"erro": "não encontrado"}, 404)

    def do_POST(self):
        tam = int(self.headers.get("Content-Length", 0))
        corpo = json.loads(self.rfile.read(tam) or b"{}")
        if self.path == "/api/sair":
            self._json({"ok": True})
            threading.Thread(target=SERVIDOR.shutdown, daemon=True).start()
            return
        if self.path == "/api/config":
            novos = {}
            for item in corpo.get("roteadores", []):
                n = re.sub(r"[^a-z0-9_-]", "", str(item.get("nome", "")).strip().lower())[:30]
                ip = str(item.get("ip", "")).strip()
                if not n or not IP_RE.match(ip):
                    return self._json({"ok": False, "erro": f"Nome ou IP inválido: {item}"}, 400)
                novos[n] = ip
            if not novos:
                return self._json({"ok": False, "erro": "Informe pelo menos um roteador."}, 400)
            for n in list(sessoes):
                if novos.get(n) != ROTEADORES.get(n):
                    sessoes.pop(n, None)  # IP changed: the old session is no longer valid
            ROTEADORES.clear()
            ROTEADORES.update(novos)
            cache_endpoints.clear()
            salvar_cfg(novos)
            return self._json({"ok": True, "roteadores": novos})
        nome = corpo.get("roteador")
        if nome not in ROTEADORES:
            return self._json({"ok": False, "erro": "roteador inválido"}, 400)
        if self.path == "/api/login":
            try:
                return self._json(login(nome, corpo.get("senha", "")))
            except Exception as e:
                return self._json({"ok": False, "erro": str(e)})
        if self.path == "/api/despejar":
            return self._json(despejar(nome))
        if self.path == "/api/logout":
            sessoes.pop(nome, None)
            return self._json({"ok": True})
        if self.path == "/api/chamar":
            ep = corpo.get("endpoint", "")
            arquivo = corpo.get("arquivo") if isinstance(corpo.get("arquivo"), dict) else None
            escrita = bool(ESCRITA.search(ep.split("/")[-1])) or corpo.get("metodo") == "POST" or bool(arquivo)
            if escrita and not corpo.get("confirmado"):
                return self._json({"ok": False, "erro": "Este endpoint altera o roteador: confirme antes."})
            return self._json(
                chamar(nome, ep, corpo.get("metodo", "GET"), corpo.get("params"), corpo.get("mostrar", False), arquivo)
            )
        self._json({"erro": "não encontrado"}, 404)


SERVIDOR: ThreadingHTTPServer | None = None


def _ja_rodando() -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", PORTA)) == 0


if __name__ == "__main__":
    url = f"http://127.0.0.1:{PORTA}"
    if _ja_rodando():  # already running: just show the page
        webbrowser.open(url)
        sys.exit(0)
    SERVIDOR = ThreadingHTTPServer(("127.0.0.1", PORTA), Handler)
    if "--sem-navegador" not in sys.argv:
        threading.Timer(0.6, webbrowser.open, args=(url,)).start()
    if sys.stdout:
        print(f"Painel em {url}  (Ctrl+C ou o botão Sair da página para encerrar)")
    try:
        SERVIDOR.serve_forever()
    except KeyboardInterrupt:
        pass
