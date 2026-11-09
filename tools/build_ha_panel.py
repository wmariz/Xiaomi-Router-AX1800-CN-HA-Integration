"""Gera custom_components/miwifi_ax/frontend/miwifi-panel.js a partir de desktop/painel.html.

A página é uma só; no HA ela roda dentro de um web component (shadow DOM) e fala com a
integração via hass.callApi. Rode sempre que alterar desktop/painel.html:
    python tools/build_ha_panel.py
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "desktop" / "painel.html"
DST = BASE / "custom_components" / "miwifi_ax" / "frontend" / "miwifi-panel.js"

import json

# 1) catálogo de funções -> injeta em desktop/painel.html e gera docs/FUNCOES.md
cat = json.loads((BASE / "desktop" / "funcoes.json").read_text(encoding="utf-8"))
cat.pop("_legenda", None)
html = SRC.read_text(encoding="utf-8")
html = re.sub(r"/\*FUNCOES\*/.*?/\*FIM\*/", lambda m: "/*FUNCOES*/" + json.dumps(cat, ensure_ascii=False) + "/*FIM*/", html, flags=re.S)
SRC.write_text(html, encoding="utf-8")
linhas = ["# Funções internas do Xiaomi AX1800 (RM1800)", "",
          "Gerado de `desktop/funcoes.json`. **✓** = confirmado (testado no aparelho ou uso visto no código da interface/app); "
          "**⚠ INFERÊNCIA** = deduzido só pelo nome/contexto.", "",
          "| Função | Descrição | Exemplo de chamada |", "|---|---|---|"]
for ep in sorted(cat):
    tipo, txt = cat[ep][:2]
    ex = cat[ep][2] if len(cat[ep]) > 2 else None
    exs = f"`{ex['m']} {json.dumps(ex['p'], ensure_ascii=False)}`".replace("|", "/") if ex else ""
    linhas.append(f"| `{ep}` | {'✓' if tipo == 'c' else '**⚠ INFERÊNCIA** —'} {txt.replace('|', '/')} | {exs} |")
(BASE / "docs" / "FUNCOES.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
css = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
corpo = re.search(r"<body>(.*?)<script>", html, re.S).group(1)
script = re.search(r"<script>(.*?)</script>\s*</body>", html, re.S).group(1)


def tema_escuro(css: str) -> str:
    """@media (prefers-color-scheme:dark){...} -> regras sob :host([dark]) (segue o tema do HA)."""
    out, i = [], 0
    for m in re.finditer(r"@media \(prefers-color-scheme:dark\)\{", css):
        out.append(css[i:m.start()])
        j, prof = m.end(), 1
        while prof:
            prof += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
        bloco = css[m.end():j - 1]
        for sel, regra in re.findall(r"([^{}]+)\{([^{}]*)\}", bloco):
            sel = ",".join(":host([dark])" if s.strip() == ":root" else f":host([dark]) {s.strip()}" for s in sel.split(","))
            out.append(f"{sel}{{{regra}}}")
        i = j
    out.append(css[i:])
    return "".join(out)


css = tema_escuro(css)
css = css.replace(":root{", ":host{")
css = re.sub(r"(^|\})body\{", r"\1.mw-body{", css)
css += "\n.mw-body{min-height:100vh}\n#hamb{display:contents;color:#fff}\n"


def lit(s: str) -> str:
    return s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


js = f"""// GERADO por tools/build_ha_panel.py a partir de desktop/painel.html — não edite à mão.
const CSS = `{lit(css)}`;
const HTML = `<div class="mw-body">{lit(corpo)}</div>`;

function runPanel() {{
{script}
}}

class MiwifiAxPanel extends HTMLElement {{
  set hass(h) {{
    this._hass = h;
    if (this._mb) this._mb.hass = h;
    this.toggleAttribute("dark", !!(h.themes && h.themes.darkMode));
    if (!this._ok) {{ this._ok = true; this._init(); }}
  }}
  set narrow(n) {{ this._narrow = n; if (this._mb) this._mb.narrow = n; }}
  _init() {{
    const root = this.attachShadow({{ mode: "open" }});
    root.innerHTML = `<style>${{CSS}}</style>${{HTML}}`;
    const slot = root.querySelector("#hamb");
    if (slot && customElements.get("ha-menu-button")) {{
      this._mb = document.createElement("ha-menu-button");
      this._mb.hass = this._hass; this._mb.narrow = this._narrow;
      slot.appendChild(this._mb);
    }}
    window.__MIWIFI_ROOT__ = root;
    window.__MIWIFI_SRV__ = (path, body) => this._srv(path, body);
    runPanel();
  }}
  async _srv(path, body) {{
    const h = this._hass;
    try {{
      if (path === "/api/estado") return await h.callApi("GET", "miwifi_ax/estado");
      if (path === "/api/chamar") return await h.callApi("POST", "miwifi_ax/chamar", body);
      if (path.startsWith("/api/endpoints")) return await h.callApi("GET", "miwifi_ax/endpoints" + path.slice(14));
      return {{ ok: false, erro: "Função disponível só no painel do PC." }};
    }} catch (e) {{
      return {{ ok: false, erro: (e && ((e.body && e.body.message) || e.message || e.error)) || String(e) }};
    }}
  }}
}}
if (!customElements.get("miwifi-ax-panel")) customElements.define("miwifi-ax-panel", MiwifiAxPanel);
"""
DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_text(js, encoding="utf-8")
print(f"gerado {DST.relative_to(BASE)} ({len(js)} bytes)")
