# Funções internas do Xiaomi AX1800 (RM1800)

Gerado de `desktop/funcoes.json`. **✓** = confirmado (testado no aparelho ou uso visto no código da interface/app); **⚠ INFERÊNCIA** = deduzido só pelo nome/contexto.

| Função | Descrição | Exemplo de chamada |
|---|---|---|
| `misns/wifi_share_clear` | **⚠ INFERÊNCIA** — Apaga a configuração da rede de visitante. |  |
| `misns/wifi_share_info` | ✓ Rede de visitante: ligada, nome, senha e segurança. |  |
| `misns/wifi_share_switch` | **⚠ INFERÊNCIA** — Interruptor local da rede de visitante usado pela nuvem; parâmetros desconhecidos (code 1523). Use set_wifi_without_restart. |  |
| `misystem/active` | ✓ Dispara a atualização do histórico de velocidade (usado após o teste de velocidade). |  |
| `misystem/arn_ignore` | **⚠ INFERÊNCIA** — Ignora/libera um aparelho marcado pelo anti-intrusos. |  |
| `misystem/arn_records` | ✓ Registros de tentativas de intrusão bloqueadas. |  |
| `misystem/arn_security` | ✓ Centro de segurança: proteção de privacidade, firewall de sites maliciosos e de arquivos com vírus. |  |
| `misystem/arn_security_switch` | **⚠ INFERÊNCIA** — Liga/desliga as proteções do centro de segurança. |  |
| `misystem/arn_status` | ✓ Anti-intrusos (防蹭网): ligado, nível e contador de tentativas bloqueadas. |  |
| `misystem/arn_switch` | **⚠ INFERÊNCIA** — Liga/desliga o anti-intrusos e define o nível (parâmetros não confirmados). |  |
| `misystem/bandwidth_test` | ✓ Mede a velocidade de download da internet (teste do QoS). |  |
| `misystem/c_backup` | ✓ Gera arquivo de backup da configuração (keys = partes a incluir). | `GET {"keys": "mi_basic_info,mi_network_info,mi_wifi_info,mi_lan_info,mi_arn_info"}` |
| `misystem/c_restore` | ✓ Restaura um backup enviado (keys). |  |
| `misystem/c_upload` | ✓ Envia o arquivo de backup para restaurar. |  |
| `misystem/channel_scan_result` | ✓ Resultado da otimização de canal (canal atual/sugerido e nota). |  |
| `misystem/channel_scan_start` | **⚠ INFERÊNCIA** — Inicia a varredura de canais da otimização de Wi-Fi. |  |
| `misystem/check_status` | ✓ Verificação rápida do roteador usada pelo app. |  |
| `misystem/device_detail` | **⚠ INFERÊNCIA** — Detalhes de um aparelho (pede mac). | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/devicelist` | ✓ Lista de aparelhos conhecidos: nome, MAC, IP, online, tipo de conexão (0 cabo, 1 2,4 GHz, 2 5 GHz, 3 visitante), velocidades e permissões. |  |
| `misystem/ecos_info` | ✓ Informações de dispositivos do ecossistema (pede parâmetros). |  |
| `misystem/extendwifi_scanlist` | **⚠ INFERÊNCIA** — Lista redes próximas para o modo repetidor sem fio. |  |
| `misystem/get_dev_bsd` | ✓ Banda preferida de um aparelho no Wi-Fi unificado (pede parâmetros). |  |
| `misystem/get_portscan_result` | ✓ Resultado da varredura de portas (pede parâmetros de varredura). |  |
| `misystem/get_usb_u3` | ✓ Estado do modo USB 3.0 (sem efeito no AX1800, que não tem USB). |  |
| `misystem/get_weakdetect_result` | ✓ Resultado da verificação de senhas fracas (pede parâmetros de varredura). |  |
| `misystem/http_status` | ✓ Estado da interceptação HTTP do roteador (ex.: páginas de aviso). |  |
| `misystem/http_switch` | **⚠ INFERÊNCIA** — Liga/desliga a interceptação HTTP. |  |
| `misystem/iperf` | **⚠ INFERÊNCIA** — Servidor iperf para medir velocidade da rede local. |  |
| `misystem/led` | ✓ Estado do LED; com on=0/1 apaga/acende as luzes do aparelho. | `GET {"on": 1}` |
| `misystem/messages` | ✓ Avisos do roteador (atualização disponível, falha no 5 GHz, conflito de IP). |  |
| `misystem/minet_get_state` | ✓ Estado do MiNet (configuração rápida de aparelhos Xiaomi); responde erro neste aparelho. |  |
| `misystem/net_diagnose_result` | ✓ Resultado do diagnóstico de rede. |  |
| `misystem/net_diagnose_start` | **⚠ INFERÊNCIA** — Inicia o diagnóstico de rede do app. |  |
| `misystem/netacctl_set` | **⚠ INFERÊNCIA** — Define o controle de acesso à internet de um aparelho. |  |
| `misystem/netacctl_status` | ✓ Controle de acesso à internet por aparelho (pede parâmetros). |  |
| `misystem/newstatus` | ✓ Resumo das redes 2,4/5 GHz (nome e clientes conectados). Atenção: devolve a senha do 2,4 GHz no campo 'pssswd'. |  |
| `misystem/ota` | **⚠ INFERÊNCIA** — Atualização de firmware pelo ar (OTA). |  |
| `misystem/parctl_add` | **⚠ INFERÊNCIA** — Proteção infantil: cria regra de horário. |  |
| `misystem/parctl_delete` | **⚠ INFERÊNCIA** — Proteção infantil: remove regra. |  |
| `misystem/parctl_get_url` | **⚠ INFERÊNCIA** — Proteção infantil: lista de sites bloqueados. |  |
| `misystem/parctl_info` | ✓ Proteção infantil: regras por aparelho (pede parâmetros). |  |
| `misystem/parctl_set_filter` | **⚠ INFERÊNCIA** — Proteção infantil: modo de filtro (lista branca/negra). |  |
| `misystem/parctl_set_url` | **⚠ INFERÊNCIA** — Proteção infantil: define sites bloqueados. |  |
| `misystem/parctl_update` | **⚠ INFERÊNCIA** — Proteção infantil: altera regra. |  |
| `misystem/qos_dev_info` | **⚠ INFERÊNCIA** — Limite de QoS de um aparelho específico (pede parâmetros). |  |
| `misystem/qos_guest` | ✓ Limite de velocidade da rede de visitante (percent, percent_up da banda). | `GET {"percent": 0.5, "percent_up": 0.5}` |
| `misystem/qos_info` | ✓ Configuração do QoS: ligado, modo, banda, limite da rede de visitante e limites por aparelho. |  |
| `misystem/qos_info_new` | ✓ Versão nova do resumo do QoS usada pelo app (banda, limites por MAC). |  |
| `misystem/qos_limits` | ✓ Grava limites de velocidade por aparelho (data em JSON). |  |
| `misystem/qos_mode` | ✓ Modo do QoS (mode): automático/jogos/navegação/vídeo/manual. | `GET {"mode": 0}` |
| `misystem/qos_offlimit` | ✓ Remove o limite de velocidade de um aparelho (mac). | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/qos_set_dev_info` | **⚠ INFERÊNCIA** — Grava o limite de QoS de um aparelho (usado pelo app). |  |
| `misystem/qos_switch` | ✓ Liga/desliga o QoS (on). | `GET {"on": 0}` |
| `misystem/qos_xq` | ✓ Limite de velocidade da rede local (percent, percent_up). |  |
| `misystem/r_ip_conflict` | ✓ Resolve conflito de IP com o roteador acima, mudando a faixa da rede local. |  |
| `misystem/repair_status` | ✓ Estado do reparo automático de rede do diagnóstico. |  |
| `misystem/router_common_status` | ✓ Resumo para o app: aparelhos, velocidade WAN e USB. |  |
| `misystem/router_name` | ✓ Nome e local do roteador. |  |
| `misystem/set_band` | ✓ Informa a banda contratada (upload/download em Mbps) usada pelo QoS. | `POST {"manual": 1, "upload": 250, "download": 500}` |
| `misystem/set_channel` | **⚠ INFERÊNCIA** — Aplica o canal sugerido pela otimização. |  |
| `misystem/set_dev_bsd` | **⚠ INFERÊNCIA** — Fixa a banda de um aparelho no Wi-Fi unificado. |  |
| `misystem/set_ota` | **⚠ INFERÊNCIA** — Configura a atualização automática de firmware. |  |
| `misystem/set_router_name` | ✓ Altera nome e local (name, locale). | `GET {"name": "WMON-AX1800", "locale": "Escritório"}` |
| `misystem/set_sys_time` | ✓ Define o fuso (timezone, index) ou a hora (time 'AAAA-MM-DD hh:mm:ss'). | `POST {"timezone": "<valor da lista de fusos>", "index": 3}` |
| `misystem/smartvpn_info` | ✓ Estado da 'VPN inteligente' (roteamento seletivo por domínio/MAC). |  |
| `misystem/smartvpn_mac` | **⚠ INFERÊNCIA** — Lista de aparelhos que passam pela VPN inteligente. |  |
| `misystem/smartvpn_switch` | **⚠ INFERÊNCIA** — Liga/desliga a VPN inteligente. |  |
| `misystem/smartvpn_url` | **⚠ INFERÊNCIA** — Lista de domínios que passam pela VPN inteligente. |  |
| `misystem/speed_test` | **⚠ INFERÊNCIA** — Inicia o teste de velocidade do app. |  |
| `misystem/speed_test_result` | ✓ Resultado do teste de velocidade do app. |  |
| `misystem/start_portscan` | **⚠ INFERÊNCIA** — Inicia varredura de portas expostas. |  |
| `misystem/start_weakdetect` | **⚠ INFERÊNCIA** — Inicia a verificação de senhas fracas (Wi-Fi/administração). |  |
| `misystem/status` | ✓ Estado geral: tempo ligado, CPU, memória, contagem de aparelhos, tráfego WAN (atual, pico, total) e hardware. |  |
| `misystem/sys_log` | ✓ Gera um pacote com os registros do sistema e devolve o caminho para baixar. |  |
| `misystem/sys_time` | ✓ Hora do roteador, fuso (timezone + índice da opção) e papel na Mesh (whc_cap principal / whc_re nó). |  |
| `misystem/topo_graph` | ✓ Topologia da rede Mesh: roteador principal e nós (nome, IP, local, modelo). |  |
| `misystem/usb_u3` | ✓ Liga/desliga USB 3.0 (enable) — sem efeito no AX1800. |  |
| `misystem/vas_info` | ✓ Serviços de valor agregado (anúncios/plug-ins da Xiaomi); vazio neste aparelho. |  |
| `misystem/vas_switch` | **⚠ INFERÊNCIA** — Liga/desliga serviços de valor agregado. |  |
| `misystem/web_access_info` | ✓ Controle de acesso à administração: ligado e lista de MACs autorizados. |  |
| `misystem/web_access_opt` | ✓ Liga/desliga o controle de acesso e adiciona/remove MACs autorizados. | `POST {"open": 1}` |
| `xqdatacenter/identify_device` | **⚠ INFERÊNCIA** — Identifica o tipo/fabricante de um aparelho. |  |
| `xqdatacenter/request` | ✓ Canal genérico de comandos numerados ('api' no payload) usado pela interface e pela nuvem. |  |
| `xqnetdetect/nettb` | ✓ Diagnóstico rápido: aparelho → roteador → internet. |  |
| `xqnetdetect/netupspeed` | ✓ Mede a velocidade de upload da internet. |  |
| `xqnetwork/add_mesh_node` | ✓ Adiciona um nó Mesh encontrado (mac, locate). |  |
| `xqnetwork/check_wan_type` | ✓ Detecta o tipo de conexão de internet recomendado. |  |
| `xqnetwork/ddns` | ✓ Estado do DDNS: on (ligado), flag, list[] de provedores configurados. |  |
| `xqnetwork/ddns_switch` | ✓ Liga/desliga o DDNS (on=1/0). Testado 2026-11-08 (on=0 → xqnetwork/ddns on=0). | `GET {"on": 0}` |
| `xqnetwork/disable_ap` | ✓ Sai do modo repetidor sem fio (volta a roteador). |  |
| `xqnetwork/disable_lan_ap` | ✓ Sai do modo ponto de acesso (volta a roteador). |  |
| `xqnetwork/dmz` | **⚠ INFERÊNCIA** — DMZ: estado e IP de destino. Significado do status (1 = ligada, 2 = desligada) deduzido — confirmado só o 2 com a DMZ desligada. |  |
| `xqnetwork/edit_device` | ✓ Adiciona (option=0) ou remove (option=1) um MAC da lista do filtro. | `GET {"mac": "AA:BB:CC:DD:EE:FF", "model": 0, "option": 0}` |
| `xqnetwork/get_addnode_status` | ✓ Andamento da inclusão de um nó Mesh. |  |
| `xqnetwork/get_miotrelay_switch` | ✓ Estado da conexão rápida (畅快连) para aparelhos Mi Home. |  |
| `xqnetwork/get_miscan_switch` | ✓ Estado da varredura AIoT da antena. |  |
| `xqnetwork/get_son_backhaul_mode` | ✓ Estado da 'prioridade para muitos aparelhos' (多终端接入优先). |  |
| `xqnetwork/ipv6_status` | ✓ Estado do IPv6. |  |
| `xqnetwork/lan_dhcp` | ✓ Configuração do servidor DHCP (faixa, concessão, DNS, gateway). |  |
| `xqnetwork/lan_info` | ✓ IP da rede local do roteador. |  |
| `xqnetwork/mac_bind` | ✓ Cria reservas de IP (data = JSON [{ip, mac, name}]). | `POST {"data": "[{\"ip\": \"192.168.0.50\", \"mac\": \"AA:BB:CC:DD:EE:FF\", \"name\": \"Aparelho\"}]"}` |
| `xqnetwork/mac_clone` | ✓ Clona um endereço MAC na WAN. | `GET {"mac": "8C:DE:F9:92:E0:94"}` |
| `xqnetwork/mac_unbind` | ✓ Remove uma reserva de IP (mac). | `POST {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `xqnetwork/macbind_info` | ✓ Reservas de IP (DHCP estático) e lista de aparelhos. |  |
| `xqnetwork/manually_add` | ✓ Adiciona manualmente um aparelho (nome + MAC) à lista do filtro. |  |
| `xqnetwork/miotrelay_switch` | ✓ Liga/desliga a conexão rápida (on). | `POST {"on": 1}` |
| `xqnetwork/miscan_switch` | ✓ Liga/desliga a varredura AIoT (on). | `POST {"on": 0}` |
| `xqnetwork/mode` | ✓ Modo de operação da rede. |  |
| `xqnetwork/portforward` | ✓ Redirecionamentos de porta: nome, protocolo (1 TCP, 2 UDP, 3 ambos), porta externa e destino IP:porta. |  |
| `xqnetwork/pppoe_catch` | **⚠ INFERÊNCIA** — Captura usuário/senha PPPoE de um roteador antigo ligado na WAN. |  |
| `xqnetwork/pppoe_start` | ✓ Reconecta o PPPoE. | `GET {}` |
| `xqnetwork/pppoe_status` | ✓ Estado da discagem PPPoE (discando, conectado, erro). |  |
| `xqnetwork/pppoe_stop` | ✓ Desconecta o PPPoE. | `GET {}` |
| `xqnetwork/scan_mesh_node` | ✓ Procura nós Mesh disponíveis para adicionar. |  |
| `xqnetwork/set_all_wifi` | ✓ Altera as duas bandas de uma vez (Wi-Fi unificado; reinicia o Wi-Fi ~30 s). Os campos on3/ssid3/pwd3 da rede de visitante são aceitos mas ignorados no RM1800. | `POST {"bsd": 0, "on1": 1, "ssid1": "Rede24", "pwd1": "senha-exemplo", "encryption1": "psk2", "channel1": 0, "bandwidth1": 0, "hidden1": 0, "txpwr1": "max", "on2": 1, "ssid2": "Rede5", "pwd2": "senha-exemplo", "encryption2": "psk2", "channel2": 0, "bandwidth2": 0, "hidden2": 0, "txpwr2": "max"}` |
| `xqnetwork/set_lan_ap` | ✓ Muda para modo ponto de acesso por cabo. |  |
| `xqnetwork/set_lan_dhcp` | ✓ Altera ou desliga o servidor DHCP. | `GET {"ignore": 0, "start": 100, "end": 200, "leasetime": "720m", "dns1": "", "dns2": "", "router": "192.168.0.1"}` |
| `xqnetwork/set_lan_ip` | ✓ Muda o IP do roteador (reinicia). | `GET {"ip": "192.168.0.1"}` |
| `xqnetwork/set_peer_wifi_auto_ap_mode` | **⚠ INFERÊNCIA** — Configuração automática de ponto de acesso entre nós Mesh. |  |
| `xqnetwork/set_son_backhaul_mode` | ✓ Liga/desliga a prioridade para muitos aparelhos (mode). | `POST {"mode": 0}` |
| `xqnetwork/set_wan` | ✓ Altera a conexão de internet (PPPoE, DHCP ou IP fixo). | `POST {"wanType": "pppoe", "pppoeName": "usuario", "pppoePwd": "senha-exemplo", "mtu": 1480, "service": "", "special": 0, "dns1": "", "dns2": "", "autoset": 1}` |
| `xqnetwork/set_wan6` | ✓ Modo IPv6 (POST): wanType=native (repassa o prefixo da operadora, que muda a cada reconexão), nat (NAT6: rede de casa com prefixo fixo fd00:6868:6868::/64) ou static; autosetipv6=0/1 (DNS automático/manual), dns1, dns2. | `POST {"wanType": "nat", "autosetipv6": 1, "dns1": "2001:4860:4860::8888", "dns2": "2606:4700:4700::1111"}` |
| `xqnetwork/set_wan_speed` | ✓ Velocidade da porta WAN (speed 0 auto/100/1000). | `POST {"speed": 0}` |
| `xqnetwork/set_wifi` | ✓ Altera uma rede Wi-Fi (wifiIndex 1=2,4 GHz, 2=5 GHz, 3=visitante): nome, senha, segurança, canal, largura, oculto, potência; e o roaming por sinal fraco. | `POST {"wifiIndex": 1, "on": 1, "ssid": "MinhaRede", "pwd": "senha-exemplo", "encryption": "psk2", "channel": 0, "bandwidth": 0, "hidden": 0, "txpwr": "max"}` |
| `xqnetwork/set_wifi_ap` | ✓ Muda para modo repetidor sem fio. |  |
| `xqnetwork/set_wifi_ax` | ✓ Wi-Fi 6 ligado (ax=1) ou modo de compatibilidade Wi-Fi 5 (ax=0). | `POST {"ax": 1}` |
| `xqnetwork/set_wifi_macfilter` | ✓ Liga/desliga o filtro de MAC e define o modo (model, enable). | `POST {"model": 0, "enable": 1}` |
| `xqnetwork/set_wifi_txbf` | ✓ Liga/desliga o MU-MIMO (txbf). | `POST {"txbf": 1}` |
| `xqnetwork/set_wifi_txpwr` | ✓ Potência do sinal (txpwr: max/mid/min). |  |
| `xqnetwork/set_wifi_without_restart` | ✓ Muda só os campos enviados sem reiniciar o Wi-Fi. wifiIndex=3 + on=1/0 liga/desliga a rede de visitante; wifiIndex=1/2 + hidden=1/0 oculta/mostra o SSID (não espelha no nó Mesh). | `GET {"wifiIndex": 3, "on": 1}` |
| `xqnetwork/wan_info` | ✓ Internet: tipo (PPPoE/DHCP/fixo), IP, gateway, DNS, MTU, tempo conectado, IPv6 e MAC usado. |  |
| `xqnetwork/wan_link` | ✓ Cabo WAN conectado (link 1/0). |  |
| `xqnetwork/wifi_detail_all` | ✓ Configuração completa do Wi-Fi por banda (nome, senha, segurança, canal, largura, potência, oculto, Wi-Fi 6, MU-MIMO, roaming) e Wi-Fi unificado. |  |
| `xqnetwork/wifi_list` | ✓ Redes Wi-Fi próximas (para o modo repetidor sem fio). |  |
| `xqnetwork/wifi_macfilter_info` | ✓ Filtro de MAC do Wi-Fi: ligado, modo (lista negra/branca) e lista. |  |
| `xqnetwork/wifiap_signal` | ✓ Qualidade do sinal até o roteador acima (nó/repetidor). |  |
| `xqsmarthome/request_miio` | **⚠ INFERÊNCIA** — Ponte para aparelhos Mi Home (miIO). |  |
| `xqsmarthome/request_smartcontroller` | ✓ Motor de cenas/agendamentos (reinício agendado do app). Formato dos parâmetros não descoberto. |  |
| `xqsmarthome/request_yeelink` | **⚠ INFERÊNCIA** — Ponte para lâmpadas Yeelight. |  |
| `xqsystem/check_rom_update` | ✓ Procura atualização de firmware nos servidores da Xiaomi. |  |
| `xqsystem/country_code` | ✓ Região do Wi-Fi atual e opções (China, Hong Kong, Taiwan, Coreia, Europa). |  |
| `xqsystem/del_vpn` | **⚠ INFERÊNCIA** — Apaga uma configuração de VPN. |  |
| `xqsystem/device_list_zigbee` | **⚠ INFERÊNCIA** — Aparelhos Zigbee de roteadores com gateway embutido (não se aplica ao AX1800). |  |
| `xqsystem/device_mac` | ✓ MAC de quem está fazendo a consulta. |  |
| `xqsystem/flash_permission` | **⚠ INFERÊNCIA** — Verifica se a gravação de firmware é permitida. |  |
| `xqsystem/get_languages` | ✓ Idiomas da interface original (chinês simplificado, tradicional HK/TW). |  |
| `xqsystem/init_info` | ✓ Informações públicas do roteador (modelo, versão, região); responde sem login. |  |
| `xqsystem/login` | ✓ Login de administrador (nonce + sha1); devolve o token de sessão. |  |
| `xqsystem/oneclick_get_remote_token` | **⚠ INFERÊNCIA** — Token para acesso remoto pela nuvem (vinculação ao app). |  |
| `xqsystem/privacy` | ✓ Consentimento de privacidade aceito. |  |
| `xqsystem/push_settings` | ✓ Notificações do app (modo silencioso, autorização). |  |
| `xqsystem/push_switch` | **⚠ INFERÊNCIA** — Liga/desliga notificações do app. |  |
| `xqsystem/reboot` | ✓ Reinicia o roteador. | `GET {"client": "web"}` |
| `xqsystem/renew_token` | **⚠ INFERÊNCIA** — Renova o token de sessão. |  |
| `xqsystem/reset` | ✓ Restaura o padrão de fábrica (format). | `GET {"format": 0}` |
| `xqsystem/router_bind_ok` | ✓ Confirma a vinculação do roteador à conta Xiaomi (usado pelo app pela nuvem). |  |
| `xqsystem/set_country_code` | ✓ Muda a região do Wi-Fi (canais e potência). | `POST {"country": "CN"}` |
| `xqsystem/set_language` | ✓ Muda o idioma da interface original. | `POST {"language": "zh_cn"}` |
| `xqsystem/set_mac_filter` | ✓ Bloqueia (wan=0) ou libera (wan=1) a internet de um aparelho. | `POST {"mac": "AA:BB:CC:DD:EE:FF", "wan": 0}` |
| `xqsystem/set_name_password` | ✓ Troca a senha de administrador (criptografia AES própria). |  |
| `xqsystem/set_privacy` | **⚠ INFERÊNCIA** — Grava o consentimento de privacidade. |  |
| `xqsystem/set_vpn` | **⚠ INFERÊNCIA** — Grava a configuração do cliente VPN. |  |
| `xqsystem/shutdown` | ✓ Desliga o roteador. | `GET {}` |
| `xqsystem/system_info` | ✓ Modelo, versão, canal do firmware, tempo ligado e nome. |  |
| `xqsystem/token` | **⚠ INFERÊNCIA** — Token de sessão para o app. |  |
| `xqsystem/upgrade_rom` | **⚠ INFERÊNCIA** — Inicia a atualização de firmware baixada. |  |
| `xqsystem/upgrade_status` | **⚠ INFERÊNCIA** — Andamento de uma atualização de firmware em curso. |  |
| `xqsystem/upload_log` | ✓ Envia os registros do sistema para a Xiaomi. |  |
| `xqsystem/upload_plug` | ✓ Instala um plug-in (exige assinatura da Xiaomi). |  |
| `xqsystem/upload_rom` | ✓ Envia um arquivo de firmware para atualização manual. |  |
| `xqsystem/upnp` | ✓ UPnP: ligado (status 1) e lista de mapeamentos de porta criados automaticamente pelos aparelhos. |  |
| `xqsystem/usbmode` | ✓ Prepara o USB para atualização (sem efeito no AX1800). |  |
| `xqsystem/usbservice` | ✓ Liga/desliga serviços USB durante a atualização. |  |
| `xqsystem/vpn` | ✓ Configuração do cliente VPN (PPTP/L2TP): servidor, usuário, protocolo. |  |
| `xqsystem/vpn_status` | ✓ Estado do cliente VPN (4 = desligado). |  |
| `xqsystem/vpn_switch` | **⚠ INFERÊNCIA** — Liga/desliga o cliente VPN. |  |
| `xqsystem/wps` | **⚠ INFERÊNCIA** — Inicia o pareamento WPS. |  |
| `xqsystem/wps_cancel` | **⚠ INFERÊNCIA** — Cancela o pareamento WPS. |  |
| `xqsystem/wps_status` | ✓ Estado do WPS (pareamento por botão). |  |
