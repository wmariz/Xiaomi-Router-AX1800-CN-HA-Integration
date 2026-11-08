# Descobertas sobre o Xiaomi Mi Router AX1800 (RM1800)

Anotações de engenharia reversa feitas durante o desenvolvimento deste projeto.
Firmware testado: **1.0.399** (versão chinesa, `countrycode CN`), dois aparelhos em **Mesh por cabo**
(principal + nó). Tudo aqui foi observado no aparelho real; onde algo não foi confirmado, está dito.

## 1. Acesso à API local (LuCI)

### Login
- `GET http://<ip>/cgi-bin/luci/web` devolve a página de login com, no JavaScript:
  - `key: '…'` — constante de 32 hex (`a2ffa5c9be07488bbb04a3a47d3c5f6a` nesta versão);
  - `deviceId = '…'` — o **MAC de quem está pedindo** (o roteador injeta o MAC do cliente).
- `nonce = "0_<deviceId>_<unix_ts>_<aleatório 0-9999>"`
- `senha_enviada = sha1(nonce + sha1(senha + key))` (hex)
- `POST /cgi-bin/luci/api/xqsystem/login` com `username=admin`, `password=<senha_enviada>`, `logtype=2`, `nonce` → `{"code":0,"token":"<stok>"}`.
- As chamadas seguintes usam `/cgi-bin/luci/;stok=<stok>/api/<grupo>/<função>`.
- Sessão expirada → `{"code":401}`: basta refazer o login.
- **Cuidado:** acessar `/cgi-bin/luci/;stok=…/web/logout` encerra a sessão (aconteceu ao "baixar todas as páginas").
- A troca de senha de administrador (`xqsystem/set_name_password`) usa ainda AES-CBC (chave derivada de `sha1(senha_antiga+key)`, IV fixo `64175472480004614961023454661220`).

### Respostas malformadas
Alguns endpoints respondem com **cabeçalhos HTTP inválidos** — ex.: `misystem/led?on=1` no nó Mesh devolve algo que o `aiohttp` rejeita
(`Invalid header token`). Clientes tolerantes (urllib, HTTP/1.0 manual) funcionam. A integração usa um cliente HTTP/1.0 próprio.

### Papel na Mesh
`misystem/sys_time` traz `"role"`: `whc_cap` = **principal**, `whc_re` = **nó (repetidor)**.
`misystem/topo_graph` mostra a árvore (principal → `leafs`).
No nó, a maioria das funções de rede (lista de aparelhos, filtro de MAC, visitante, QoS…) responde vazia — o principal concentra tudo.

## 2. Mapa de funções (grupos `misystem`, `xqnetwork`, `xqsystem`, `misns`)

### Encontradas na interface web (90)
Extraídas das páginas `web/home`, `web/setting/{wifi,wan,lannetset,safe,upgrade}`, `web/apsetting/wifi`, `web/store`, `web/prosetting/qos`.

| Área | Leitura | Escrita (parâmetros) |
|---|---|---|
| Estado | `misystem/status` (CPU, memória, contagem de aparelhos, tráfego WAN, hardware), `misystem/newstatus` (clientes por banda — ⚠ devolve a senha do 2,4 GHz no campo com erro de digitação `pssswd`), `misystem/devicelist`, `misystem/topo_graph`, `misystem/messages` | `xqsystem/reboot` (`client=web`), `xqsystem/shutdown` |
| Wi-Fi | `xqnetwork/wifi_detail_all` (por banda: ssid, password, encryption, channel, bandwidth, txpwr, hidden, status, **ax**, **txbf**, weakenable/weakthreshold/kickthreshold; topo: **bsd**), `xqnetwork/get_miotrelay_switch`, `xqnetwork/get_miscan_switch`, `xqnetwork/get_son_backhaul_mode`, `xqsystem/country_code` | `xqnetwork/set_wifi` (`wifiIndex` 1=2,4 GHz, 2=5 GHz, `on, ssid, pwd, encryption, channel, bandwidth, hidden, txpwr`), `set_all_wifi` (Wi-Fi unificado), `set_wifi_ax` (`ax`: 1 = Wi-Fi 6, 0 = modo compatível Wi-Fi 5), `set_wifi_txbf` (`txbf` = MU-MIMO), `set_wifi_txpwr`, `miotrelay_switch` (`on`, "畅快连"/conexão rápida), `miscan_switch` (`on`, varredura AIoT), `set_son_backhaul_mode` (`mode`, "多终端接入优先"), `xqsystem/set_country_code` |
| Internet | `xqnetwork/wan_info`, `pppoe_status`, `wan_link`, `ipv6_status`, `check_wan_type` | `set_wan` (`wanType` pppoe/dhcp/static, `pppoeName, pppoePwd, mtu, service, special, dns1, dns2, autoset`, `staticIp, staticMask, staticGateway`), `pppoe_start`, `pppoe_stop`, `set_wan_speed` (`speed` 0/100/1000), `mac_clone` (`mac`), `set_wan6` (`wanType` off/native/static/nat) |
| Rede local | `xqnetwork/lan_info`, `lan_dhcp`, `macbind_info` (reservas + lista completa de aparelhos) | `set_lan_ip` (`ip`, reinicia), `set_lan_dhcp` (`start, end, leasetime "120m", dns1, dns2, router, ignore`), `mac_bind` (`data=[{"ip","mac","name"}]` em JSON), `mac_unbind` (`mac`) |
| Segurança | `xqnetwork/wifi_macfilter_info` (`model` 0=lista negra/1=branca, `enable`, `macfilter`), `misystem/web_access_info` | `set_wifi_macfilter` (`model, enable`), `edit_device` (`mac, model, option` 0=adicionar/1=remover), `misystem/web_access_opt` (`open`, `opt`, `mac`), `xqsystem/set_mac_filter` (`mac, wan` 0/1 — **bloqueia a internet de um aparelho**) |
| QoS | `misystem/qos_info` | `qos_switch` (`on`), `qos_mode` (`mode`), `set_band` (`manual, upload, download` Mbps), `qos_guest` / `qos_xq` (`percent, percent_up`), `qos_limits` (`data` JSON), `qos_offlimit` (`mac`) |
| Sistema | `misystem/sys_time` (`time`, `timezone`, **`index`**, `role`), `misystem/router_name`, `xqsystem/get_languages`, `xqsystem/check_rom_update`, `misystem/sys_log` (gera e devolve caminho do log) | `misystem/set_sys_time` (`timezone, index` **ou** `time "AAAA-MM-DD hh:mm:ss"`), `set_router_name` (`name, locale`), `xqsystem/set_language`, `misystem/c_backup` (`keys`), `c_restore`, `xqsystem/reset` (`format`), `upload_rom`, `upload_plug` |

### Encontradas só no app oficial (112 nomes a mais no código do APK)
Testadas por leitura no firmware 1.0.399 — as que **existem e respondem**:

| Função | Observação |
|---|---|
| `misystem/led` | `{"status":1}`; **`?on=0` apaga, `?on=1` acende** os LEDs do aparelho |
| `misystem/arn_status`, `arn_records`, `arn_security` | anti-intrusos ("防蹭网"): ligado, nível, **contador de bloqueios**; firewalls de sites/vírus |
| `misystem/router_common_status` | resumo (aparelhos, velocidade WAN, USB) |
| `misystem/qos_info_new`, `channel_scan_result`, `smartvpn_info`, `vas_info`, `check_status`, `repair_status` | |
| `xqsystem/system_info`, `vpn`, `vpn_status`, `wps_status`, `push_settings`, `privacy`, `init_info` (sem login), `device_mac` | |
| `xqnetwork/mode` | modo de rede |
| `xqsmarthome/request_smartcontroller` | motor de "cenas"/agendamentos (comandos `get_multiple_scene_setting`, `get_single_scene_setting`; o formato dos parâmetros **não foi descoberto** — o app só o usa pela nuvem) |

Respondem "parâmetro errado" sem argumentos: `ecos_info`, `netacctl_status`, `parctl_info` (proteção infantil), `get_dev_bsd`.

### Funções escondidas pela própria interface
- **Rede de visitante:** o bloco "访客Wi-Fi" está **comentado** em `web/setting/wifi`. Leitura: `misns/wifi_share_info` (`info.guest` 1/0, `info.data.{ssid,password,encryption}`).
  Escrita (do código comentado): `xqnetwork/set_wifi` com **`wifiIndex=3`**, `on, ssid, pwd, encryption` (o SSID não pode ser igual ao do 2,4 GHz).
  ⚠ A escrita ainda **não foi confirmada** neste firmware.
- **Desconexão por sinal fraco:** formulários `roamset24/roamset50` ocultos → `set_wifi` com `wifiIndex, weakenable, weakthreshold, kickthreshold`.
- **AIoT** e **prioridade para muitos aparelhos** também estão comentados na página.

### Lista de aparelhos
`misystem/devicelist` → `list[]` com `mac, name, oname, ip[{ip, online(s), downspeed, upspeed}], online, isap (8 = nó Mesh), parent, authority{wan,…}`, e **`type`**: `0` cabo, `1` Wi-Fi 2,4 GHz, `2` Wi-Fi 5 GHz, `3` visitante (convenção Xiaomi; o 3 não foi observado ainda).
Com Mesh por cabo, aparelhos ligados nas portas do nó aparecem como "cabo" **sem `parent`**; os do Wi-Fi do nó têm `parent` = MAC do nó.

## 3. Armadilhas encontradas

- **Fuso "(UTC−3) Brasília" aplica o horário de verão antigo** (+1 h em novembro). Todas as opções UTC−3 mandam `timezone=CST+3`, mas o roteador guarda também o **`index`** da opção. Use **"(UTC−3) Caiena, Fortaleza"** (`index` 3).
- Na Mesh, o fuso só pode ser alterado no **principal** e é repassado ao nó. Salvar de novo o fuso no principal forçou o nó a acertar um relógio que estava **11 h adiantado** (sem NTP).
- O **reinício agendado** do app vale para a Mesh toda; com o relógio do nó errado, ele reiniciava em outro horário (ex.: "06:00" do nó = 19:00 locais), derrubando tudo o que estava ligado nele.
- O app chinês **5.6.5 e 5.7.5 só têm `armeabi-v7a`** (32 bits): não instalam em celulares novos sem suporte a 32 bits. Rodam num emulador Android 11 x86 (que traduz ARM 32 bits).
- O app fala com a nuvem (`api.miwifi.com`): `/r/api/<grupo>/<função>` repassa ao roteador **as mesmas funções locais**, com parâmetros e respostas cifrados (RC4 com a sessão da conta). Rede de visitante e agendamentos no app usam também `/s/guest_wifi/…` e `xqsmarthome/request_smartcontroller`.
- Antivírus com inspeção de HTTPS (ex.: Avast) quebram o login do app e ferramentas Java/Python que não usam o repositório de certificados do Windows.
- O roteador é limitado (4× Cortex-A53 716 MHz, 256 MB, ~50–60 % de memória em uso em repouso). Ficou visivelmente instável com muitos aparelhos extras conectados.

## 4. Diagnóstico de rede usado
- `xqsystem/init_info` responde **sem login** — útil como "ping" do serviço web.
- O tempo ligado (`misystem/status.upTime`) de cada aparelho revela reinícios.
- `xqnetwork/wan_info.uptime` zera a cada reconexão PPPoE.
