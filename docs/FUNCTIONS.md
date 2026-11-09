# Internal functions of the Xiaomi AX1800 (RM1800)

Generated from `desktop/funcoes.json` + `desktop/funcoes_en.json` by `tools/build_ha_panel.py`. **✓** = confirmed (tested on the device or usage seen in the UI/app code); **⚠ INFERRED** = deduced from the name/context only.

| Function | Description | Example call |
|---|---|---|
| `misns/wifi_share_clear` | **⚠ INFERRED** — Erases the guest network settings. |  |
| `misns/wifi_share_info` | ✓ Guest network: on/off, name, password and security. |  |
| `misns/wifi_share_switch` | **⚠ INFERRED** — Local guest network switch used by the cloud; parameters unknown (code 1523). Use set_wifi_without_restart. |  |
| `misystem/active` | ✓ Triggers the speed-history refresh (used after the speed test). |  |
| `misystem/arn_ignore` | **⚠ INFERRED** — Ignores/releases a device flagged by the anti-intrusion feature. |  |
| `misystem/arn_records` | ✓ Log of blocked intrusion attempts. |  |
| `misystem/arn_security` | ✓ Security center: privacy protection, malicious-site firewall and virus-file firewall. |  |
| `misystem/arn_security_switch` | **⚠ INFERRED** — Turns the security center protections on/off. |  |
| `misystem/arn_status` | ✓ Anti-intrusion (防蹭网): on/off, level and count of blocked attempts. |  |
| `misystem/arn_switch` | **⚠ INFERRED** — Turns anti-intrusion on/off and sets the level (parameters unconfirmed). |  |
| `misystem/bandwidth_test` | ✓ Measures internet download speed (QoS test). |  |
| `misystem/c_backup` | ✓ Creates a configuration backup file (keys = parts to include). | `GET {"keys": "mi_basic_info,mi_network_info,mi_wifi_info,mi_lan_info,mi_arn_info"}` |
| `misystem/c_restore` | ✓ Restores the chosen items of the uploaded backup (comma-separated keys); a restart is needed afterwards. | `GET {"keys": "mi_wifi_info,mi_lan_info"}` |
| `misystem/c_upload` | ✓ Uploads a backup (multipart, file in the image field). Only reads the file: returns des.keys {key: description} to choose in c_restore. |  |
| `misystem/channel_scan_result` | ✓ Channel optimization result (current/suggested channel and score). |  |
| `misystem/channel_scan_start` | **⚠ INFERRED** — Starts the Wi-Fi optimization channel scan. |  |
| `misystem/check_status` | ✓ Quick router check used by the app. |  |
| `misystem/device_detail` | **⚠ INFERRED** — Details of one device (needs mac). | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/devicelist` | ✓ Known devices: name, MAC, IP, online, connection type (0 wired, 1 2.4 GHz, 2 5 GHz, 3 guest), speeds and permissions. |  |
| `misystem/ecos_info` | ✓ Ecosystem device information (needs parameters). |  |
| `misystem/extendwifi_scanlist` | **⚠ INFERRED** — Lists nearby networks for wireless repeater mode. |  |
| `misystem/get_dev_bsd` | ✓ Preferred band of a device on unified Wi-Fi (needs parameters). |  |
| `misystem/get_portscan_result` | ✓ Port scan result (needs scan parameters). |  |
| `misystem/get_usb_u3` | ✓ USB 3.0 mode status (no effect on the AX1800, which has no USB). |  |
| `misystem/get_weakdetect_result` | ✓ Weak-password check result (needs scan parameters). |  |
| `misystem/http_status` | ✓ Status of the router's HTTP interception (e.g. warning pages). |  |
| `misystem/http_switch` | **⚠ INFERRED** — Turns HTTP interception on/off. |  |
| `misystem/iperf` | **⚠ INFERRED** — iperf server to measure local network speed. |  |
| `misystem/led` | ✓ LED status; with on=0/1 turns the device lights off/on. | `GET {"on": 1}` |
| `misystem/messages` | ✓ Bell notices: messages[{type 1 new version {version} / 3 5 GHz failure / 4 IP conflict {ip}, timestamp}], count. | `GET {}` |
| `misystem/mi_vpn` | ✓ Turns "Xiaomi services via VPN" on/off (the official page disconnects the VPN first). | `GET {"open": 1}` |
| `misystem/mi_vpn_info` | ✓ "Xiaomi services via VPN": status 1/0. | `GET {}` |
| `misystem/minet_get_state` | ✓ MiNet status (quick setup of Xiaomi devices); returns an error on this device. |  |
| `misystem/net_diagnose_result` | ✓ Network diagnosis result. |  |
| `misystem/net_diagnose_start` | **⚠ INFERRED** — Starts the app's network diagnosis. |  |
| `misystem/netacctl_set` | **⚠ INFERRED** — Sets a device's internet access control. |  |
| `misystem/netacctl_status` | ✓ Per-device internet access control (needs parameters). |  |
| `misystem/newstatus` | ✓ 2.4/5 GHz summary (name and connected clients). Warning: returns the 2.4 GHz password in the 'pssswd' field. |  |
| `misystem/ota` | **⚠ INFERRED** — Over-the-air (OTA) firmware update. |  |
| `misystem/parctl_add` | **⚠ INFERRED** — Parental control: creates a schedule rule. |  |
| `misystem/parctl_delete` | **⚠ INFERRED** — Parental control: removes a rule. |  |
| `misystem/parctl_get_url` | **⚠ INFERRED** — Parental control: blocked-sites list. |  |
| `misystem/parctl_info` | ✓ Parental control: rules per device (needs parameters). |  |
| `misystem/parctl_set_filter` | **⚠ INFERRED** — Parental control: filter mode (allowlist/blocklist). |  |
| `misystem/parctl_set_url` | **⚠ INFERRED** — Parental control: sets blocked sites. |  |
| `misystem/parctl_update` | **⚠ INFERRED** — Parental control: edits a rule. |  |
| `misystem/qos_dev_info` | **⚠ INFERRED** — QoS limit of a specific device (needs parameters). |  |
| `misystem/qos_guest` | ✓ Guest network speed limit (percent, percent_up of the bandwidth). | `GET {"percent": 0.5, "percent_up": 0.5}` |
| `misystem/qos_info` | ✓ QoS settings: on/off, mode, bandwidth, guest network limit and per-device limits. |  |
| `misystem/qos_info_new` | ✓ Newer QoS summary used by the app (bandwidth, limits per MAC). |  |
| `misystem/qos_limits` | ✓ Per-device limits in KB/s (0 = no limit): data = JSON [{mac, maxup, maxdown}]. The official page calls qos_mode with the current mode afterwards. | `POST {"data": "[{\"mac\": \"AA:BB:CC:DD:EE:FF\", \"maxup\": 500, \"maxdown\": 2000}]"}` |
| `misystem/qos_mode` | ✓ QoS mode (mode): auto/gaming/browsing/video/manual. | `GET {"mode": 0}` |
| `misystem/qos_offlimit` | ✓ Removes a device's speed limit (mac). | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/qos_set_dev_info` | **⚠ INFERRED** — Writes a device's QoS limit (used by the app). |  |
| `misystem/qos_switch` | ✓ Turns QoS on/off (on). | `GET {"on": 0}` |
| `misystem/qos_xq` | ✓ Limit for the router's own traffic, as a fraction of the bandwidth (percent, percent_up); read in qos_info.local. | `GET {"percent": 0.9, "percent_up": 0.9}` |
| `misystem/r_ip_conflict` | ✓ Avoids the IP conflict with the upstream router by moving the LAN to the IP suggested in messages (type 4). Restarts the Wi-Fi. | `POST {}` |
| `misystem/repair_status` | ✓ Status of the diagnosis' automatic network repair. |  |
| `misystem/router_common_status` | ✓ Summary for the app: devices, WAN speed and USB. |  |
| `misystem/router_name` | ✓ Router name and location. |  |
| `misystem/set_band` | ✓ Sets the contracted bandwidth (upload/download in Mbps) used by QoS. | `POST {"manual": 1, "upload": 250, "download": 500}` |
| `misystem/set_channel` | **⚠ INFERRED** — Applies the channel suggested by the optimization. |  |
| `misystem/set_dev_bsd` | **⚠ INFERRED** — Pins a device's band on unified Wi-Fi. |  |
| `misystem/set_ota` | **⚠ INFERRED** — Configures automatic firmware updates. |  |
| `misystem/set_router_name` | ✓ Changes name and location (name, locale). | `GET {"name": "WMON-AX1800", "locale": "Escritório"}` |
| `misystem/set_sys_time` | ✓ Sets the time zone (timezone, index) or the time (time 'YYYY-MM-DD hh:mm:ss'). | `POST {"timezone": "<valor da lista de fusos>", "index": 3}` |
| `misystem/smartvpn_info` | ✓ VPN smart split: switch, mode (1 by address, 2 by device), ulist, mlist, name{mac: name}. | `GET {}` |
| `misystem/smartvpn_mac` | ✓ Adds (opt 0) or removes (opt 1) devices from smart split. | `POST {"macs": "AA:BB:CC:DD:EE:FF", "opt": 0}` |
| `misystem/smartvpn_switch` | ✓ Turns smart split on/off and chooses the mode. | `GET {"enable": 1, "mode": 1}` |
| `misystem/smartvpn_url` | ✓ Adds (opt 0) or removes (opt 1) an address from smart split. | `POST {"url": "example.com", "opt": 0}` |
| `misystem/speed_test` | **⚠ INFERRED** — Starts the app's speed test. |  |
| `misystem/speed_test_result` | ✓ Result of the app's speed test. |  |
| `misystem/start_portscan` | **⚠ INFERRED** — Starts a scan of exposed ports. |  |
| `misystem/start_weakdetect` | **⚠ INFERRED** — Starts the weak-password check (Wi-Fi/admin). |  |
| `misystem/status` | ✓ Overall status: uptime, CPU, memory, device count, WAN traffic (current, peak, total) and hardware. |  |
| `misystem/sys_log` | ✓ Generates a system-log package and returns the download path. |  |
| `misystem/sys_time` | ✓ Router time, time zone (timezone + option index) and Mesh role (whc_cap main / whc_re node). |  |
| `misystem/topo_graph` | ✓ Mesh network topology: main router and nodes (name, IP, location, model). |  |
| `misystem/usb_u3` | ✓ Turns USB 3.0 on/off (enable) — no effect on the AX1800. |  |
| `misystem/vas_info` | ✓ Value-added services (Xiaomi ads/plug-ins); empty on this device. |  |
| `misystem/vas_switch` | **⚠ INFERRED** — Turns value-added services on/off. |  |
| `misystem/web_access_info` | ✓ Admin access control: on/off and list of allowed MACs. |  |
| `misystem/web_access_opt` | ✓ Turns access control on/off and adds/removes allowed MACs. | `POST {"open": 1}` |
| `xqdatacenter/identify_device` | **⚠ INFERRED** — Identifies a device's type/manufacturer. |  |
| `xqdatacenter/request` | ✓ Generic numbered-command channel ('api' in the payload) used by the UI and the cloud. |  |
| `xqnetdetect/nettb` | ✓ Quick device → router → internet test: error 0 = ok. | `GET {}` |
| `xqnetdetect/netupspeed` | ✓ Measures internet upload speed. |  |
| `xqnetwork/add_mesh_node` | ✓ Adds a node to the Mesh. locate = room name in Chinese (客厅, 主卧, 次卧, 书房, 厨房, 办公室, 地下室, 卫生间, 阁楼, 阳台, 餐厅). | `POST {"mac": "AA:BB:CC:DD:EE:FF", "locate": "客厅"}` |
| `xqnetwork/add_range_redirect` | ✓ Adds a port range rule. Takes effect after redirect_apply. | `POST {"name": "Jogo", "proto": 3, "fport": 3000, "tport": 3010, "ip": "192.168.0.50"}` |
| `xqnetwork/add_redirect` | ✓ Adds a port rule (force=1 replaces the rule for the same external port). Takes effect after redirect_apply. | `POST {"name": "Servidor", "proto": 1, "sport": 8443, "ip": "192.168.0.50", "dport": 443}` |
| `xqnetwork/add_server` | ✓ Adds a DDNS service. Provider id: 1 No-IP, 2 Oray, 3 3322.org, 4 Dyn. | `GET {"id": 1, "username": "usuario", "password": "senha", "domain": "myhome.ddns.net", "checkinterval": 10, "forceinterval": 24, "enable": 1}` |
| `xqnetwork/check_wan_type` | ✓ Detects the connection type on the WAN port: 1 PPPoE, 2 DHCP, 3 static IP, 99 no cable, other = unknown (returns 0 with PPPoE connected). | `GET {}` |
| `xqnetwork/ddns` | ✓ DDNS services: on (service on), list[{id, servicename, domain, enabled, status 0 error/1 ok/2 connecting, lastupdate, wanip, error}]. | `GET {}` |
| `xqnetwork/ddns_edit` | ✓ Edits a DDNS service (same parameters as add_server). |  |
| `xqnetwork/ddns_reload` | ✓ Forces a DDNS update now. | `GET {}` |
| `xqnetwork/ddns_switch` | ✓ Turns the router's DDNS service on/off. | `GET {"on": 0}` |
| `xqnetwork/del_server` | ✓ Removes a DDNS service. | `GET {"id": 1}` |
| `xqnetwork/delete_redirect` | ✓ Removes a port or range rule (port = external port or the range's start port). | `POST {"port": 8443, "proto": 1}` |
| `xqnetwork/disable_ap` | ✓ Leaves wireless repeater mode and goes back to router (restores previous settings). Returns lanip and ssid. | `GET {}` |
| `xqnetwork/disable_lan_ap` | ✓ Leaves wired repeater mode and goes back to router. Returns ip. | `GET {}` |
| `xqnetwork/dmz` | ✓ DMZ: status (1 = on; 0/2 = off), device ip, router lanip. | `GET {}` |
| `xqnetwork/dmz_off` | ✓ Turns DMZ off (the official page calls dmz_reload afterwards). | `GET {}` |
| `xqnetwork/dmz_reload` | ✓ Reloads the DMZ configuration. | `GET {}` |
| `xqnetwork/edit_device` | ✓ Adds (option=0) or removes (option=1) a MAC from the filter list. | `GET {"mac": "AA:BB:CC:DD:EE:FF", "model": 0, "option": 0}` |
| `xqnetwork/get_addnode_status` | ✓ Node add progress: 0 done, 1 connecting, 2 syncing, 3 expanding (1–2 min), 4 failed. | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `xqnetwork/get_miotrelay_switch` | ✓ Quick connect (畅快连) status for Mi Home devices. |  |
| `xqnetwork/get_miscan_switch` | ✓ AIoT antenna scan status. |  |
| `xqnetwork/get_server` | ✓ One DDNS service's data (username, password, domain, checkinterval, forceinterval, enabled). | `GET {"id": 1}` |
| `xqnetwork/get_son_backhaul_mode` | ✓ 'Priority for many devices' (多终端接入优先) status. |  |
| `xqnetwork/ipv6_status` | ✓ IPv6 status. |  |
| `xqnetwork/lan_dhcp` | ✓ DHCP server settings (range, lease, DNS, gateway). |  |
| `xqnetwork/lan_info` | ✓ Router LAN IP. |  |
| `xqnetwork/mac_bind` | ✓ Creates IP reservations (data = JSON [{ip, mac, name}]). With an already reserved MAC, it replaces the name and IP (tested 2026-11-09) — this is how the panel edits a reservation. | `POST {"data": "[{\"ip\": \"192.168.0.50\", \"mac\": \"AA:BB:CC:DD:EE:FF\", \"name\": \"Aparelho\"}]"}` |
| `xqnetwork/mac_clone` | ✓ Clones a MAC address on the WAN. | `GET {"mac": "8C:DE:F9:92:E0:94"}` |
| `xqnetwork/mac_unbind` | ✓ Removes an IP reservation (mac). | `POST {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `xqnetwork/macbind_info` | ✓ IP reservations (static DHCP) and device list. |  |
| `xqnetwork/manually_add` | ✓ Manually adds a device (name + MAC) to the filter list. |  |
| `xqnetwork/miotrelay_switch` | ✓ Turns quick connect on/off (on). | `POST {"on": 1}` |
| `xqnetwork/miscan_switch` | ✓ Turns the AIoT scan on/off (on). | `POST {"on": 0}` |
| `xqnetwork/mode` | ✓ Work mode: 0 = router, 1 = wireless repeater, 2 = wired repeater. | `GET {}` |
| `xqnetwork/portforward` | ✓ Forwarding rules: ftype 1 = ports (srcport, destip, destport), 2 = ranges (srcport {f, t}, destip). proto 1 TCP, 2 UDP, 3 both. | `GET {"ftype": 1}` |
| `xqnetwork/pppoe_catch` | **⚠ INFERRED** — Captures the PPPoE user/password from an old router connected to the WAN. |  |
| `xqnetwork/pppoe_start` | ✓ Reconnects PPPoE. | `GET {}` |
| `xqnetwork/pppoe_status` | ✓ PPPoE dial-up status (dialing, connected, error). |  |
| `xqnetwork/pppoe_stop` | ✓ Disconnects PPPoE. | `GET {}` |
| `xqnetwork/redirect_apply` | ✓ Applies the forwarding rules (the official page's "保存并生效" button). | `GET {}` |
| `xqnetwork/scan_mesh_node` | ✓ Scans for available Mesh nodes: list[{ssid, mac, rssi}] (rssi < -60 = too far). Takes a few seconds. | `GET {}` |
| `xqnetwork/server_switch` | ✓ Enables/disables a DDNS service (only one active at a time). | `GET {"id": 1, "on": 1}` |
| `xqnetwork/set_all_wifi` | ✓ Unified Wi-Fi: bsd 1 (only on1/ssid1/pwd1/encryption1/channel1/bandwidth1/hidden1/txpwr1) or bsd 0 (also the …2 fields). Restarts the Wi-Fi. |  |
| `xqnetwork/set_dmz` | ✓ Turns DMZ on for an IP. | `POST {"ip": "192.168.0.50"}` |
| `xqnetwork/set_lan_ap` | ✓ Switches to wired repeater (access point; WAN connected to another router). Returns the new ip. | `POST {"ssid": "", "password": ""}` |
| `xqnetwork/set_lan_dhcp` | ✓ Changes or turns off the DHCP server. | `GET {"ignore": 0, "start": 100, "end": 200, "leasetime": "720m", "dns1": "", "dns2": "", "router": "192.168.0.1"}` |
| `xqnetwork/set_lan_ip` | ✓ Changes the router IP (restarts). | `GET {"ip": "192.168.0.1"}` |
| `xqnetwork/set_peer_wifi_auto_ap_mode` | **⚠ INFERRED** — Automatic access-point setup between Mesh nodes. |  |
| `xqnetwork/set_son_backhaul_mode` | ✓ Turns priority for many devices on/off (mode). | `POST {"mode": 0}` |
| `xqnetwork/set_wan` | ✓ Changes the internet connection (PPPoE, DHCP or static IP). | `POST {"wanType": "pppoe", "pppoeName": "usuario", "pppoePwd": "senha-exemplo", "mtu": 1480, "service": "", "special": 0, "dns1": "", "dns2": "", "autoset": 1}` |
| `xqnetwork/set_wan6` | ✓ IPv6 mode (POST): wanType=native (passes the ISP prefix through, which changes on every reconnection), nat (NAT6: home network with fixed prefix fd00:6868:6868::/64) or static; autosetipv6=0/1 (automatic/manual DNS), dns1, dns2. | `POST {"wanType": "nat", "autosetipv6": 1, "dns1": "2001:4860:4860::8888", "dns2": "2606:4700:4700::1111"}` |
| `xqnetwork/set_wan_speed` | ✓ WAN port speed (speed 0 auto/100/1000). | `POST {"speed": 0}` |
| `xqnetwork/set_wifi` | ✓ Changes a Wi-Fi network (wifiIndex 1=2.4 GHz, 2=5 GHz, 3=guest): name, password, security, channel, width, hidden, power; and weak-signal roaming. | `POST {"wifiIndex": 1, "on": 1, "ssid": "MinhaRede", "pwd": "senha-exemplo", "encryption": "psk2", "channel": 0, "bandwidth": 0, "hidden": 0, "txpwr": "max"}` |
| `xqnetwork/set_wifi_ap` | ✓ Switches to wireless repeater of the given network (usage seen on the official page). Optional: nssid/nencryption/npassword for its own Wi-Fi. Returns ip and ssid. | `POST {"ssid": "MinhaRede", "password": "senha", "encryption": "WPA2PSK", "enctype": "AES", "channel": "6", "bandwidth": "20", "band": "2g"}` |
| `xqnetwork/set_wifi_ax` | ✓ Wi-Fi 6 on (ax=1) or Wi-Fi 5 compatibility mode (ax=0). | `POST {"ax": 1}` |
| `xqnetwork/set_wifi_macfilter` | ✓ Turns the MAC filter on/off and sets its mode (model, enable). | `POST {"model": 0, "enable": 1}` |
| `xqnetwork/set_wifi_txbf` | ✓ Turns MU-MIMO on/off (txbf). | `POST {"txbf": 1}` |
| `xqnetwork/set_wifi_txpwr` | ✓ Changes the power of BOTH bands at once (txpwr max/mid/min) in ~5 s without restarting the Wi-Fi (tested 2026-11-09). The screen that used it was removed from the firmware. | `GET {"txpwr": "max"}` |
| `xqnetwork/set_wifi_without_restart` | ✓ Changes only the given fields without restarting Wi-Fi. wifiIndex=3 + on=1/0 turns the guest network on/off; wifiIndex=1/2 + hidden=1/0 hides/shows the SSID (not mirrored to the Mesh node). | `GET {"wifiIndex": 3, "on": 1}` |
| `xqnetwork/wan_info` | ✓ Internet: type (PPPoE/DHCP/static), IP, gateway, DNS, MTU, connected time, IPv6 and MAC in use. |  |
| `xqnetwork/wan_link` | ✓ WAN cable connected (link 1/0). |  |
| `xqnetwork/wifi_detail_all` | ✓ Full Wi-Fi settings per band (name, password, security, channel, width, power, hidden, Wi-Fi 6, MU-MIMO, roaming) and unified Wi-Fi. |  |
| `xqnetwork/wifi_list` | ✓ Scans nearby Wi-Fi networks (for wireless repeater mode): ssid, band, channel, signal, encryption, enctype, bandwidth. | `GET {}` |
| `xqnetwork/wifi_macfilter_info` | ✓ Wi-Fi MAC filter: on/off, mode (blocklist/allowlist) and list. |  |
| `xqnetwork/wifiap_signal` | ✓ Signal quality to the upstream router (node/repeater). |  |
| `xqsmarthome/request_miio` | **⚠ INFERRED** — Bridge to Mi Home (miIO) devices. |  |
| `xqsmarthome/request_smartcontroller` | ✓ Scenes/schedules engine (the app's scheduled reboot). Parameter format not discovered. |  |
| `xqsmarthome/request_yeelink` | **⚠ INFERRED** — Bridge to Yeelight lamps. |  |
| `xqsystem/check_rom_update` | ✓ Checks Xiaomi's servers for a firmware update. |  |
| `xqsystem/country_code` | ✓ Current Wi-Fi region and options (China, Hong Kong, Taiwan, Korea, Europe). |  |
| `xqsystem/del_vpn` | ✓ Removes a VPN server. | `GET {"id": "1"}` |
| `xqsystem/device_list_zigbee` | **⚠ INFERRED** — Zigbee devices of routers with a built-in gateway (not applicable to the AX1800). |  |
| `xqsystem/device_mac` | ✓ MAC of the requesting client. |  |
| `xqsystem/flash_permission` | **⚠ INFERRED** — Checks whether firmware flashing is allowed. |  |
| `xqsystem/get_languages` | ✓ Original UI languages (Simplified Chinese, Traditional HK/TW). |  |
| `xqsystem/init_info` | ✓ Public router information (model, version, region); answers without login. |  |
| `xqsystem/login` | ✓ Admin login (nonce + sha1); returns the session token. |  |
| `xqsystem/oneclick_get_remote_token` | **⚠ INFERRED** — Token for remote cloud access (app binding). |  |
| `xqsystem/privacy` | ✓ Privacy consent accepted. |  |
| `xqsystem/push_settings` | ✓ App notifications (silent mode, authorization). |  |
| `xqsystem/push_switch` | **⚠ INFERRED** — Turns app notifications on/off. |  |
| `xqsystem/reboot` | ✓ Restarts the router. | `GET {"client": "web"}` |
| `xqsystem/renew_token` | **⚠ INFERRED** — Renews the session token. |  |
| `xqsystem/reset` | ✓ Factory reset (format). | `GET {"format": 0}` |
| `xqsystem/router_bind_ok` | ✓ Confirms binding the router to the Xiaomi account (used by the app via the cloud). |  |
| `xqsystem/set_country_code` | ✓ Changes the Wi-Fi region (channels and power). | `POST {"country": "CN"}` |
| `xqsystem/set_language` | ✓ Changes the original UI language. | `POST {"language": "zh_cn"}` |
| `xqsystem/set_mac_filter` | ✓ Blocks (wan=0) or allows (wan=1) a device's internet access. | `POST {"mac": "AA:BB:CC:DD:EE:FF", "wan": 0}` |
| `xqsystem/set_name_password` | ✓ Changes the admin password (proprietary AES encryption). |  |
| `xqsystem/set_privacy` | **⚠ INFERRED** — Stores the privacy consent. |  |
| `xqsystem/set_vpn` | ✓ Adds (empty id) or edits a VPN server. | `POST {"id": "", "oname": "Trabalho", "proto": "l2tp", "server": "vpn.example.com", "username": "usuario", "password": "senha"}` |
| `xqsystem/set_vpnauto` | ✓ Connect the VPN when the router starts (auto 1/0). | `GET {"auto": 1}` |
| `xqsystem/shutdown` | ✓ Powers the router off. | `GET {}` |
| `xqsystem/system_info` | ✓ Model, version, firmware channel, uptime and name. |  |
| `xqsystem/token` | **⚠ INFERRED** — Session token for the app. |  |
| `xqsystem/upgrade_rom` | **⚠ INFERRED** — Starts installing the downloaded firmware. |  |
| `xqsystem/upgrade_status` | **⚠ INFERRED** — Progress of an ongoing firmware update. |  |
| `xqsystem/upload_log` | ✓ Uploads the system logs to Xiaomi. |  |
| `xqsystem/upload_plug` | ✓ Installs a plug-in (requires Xiaomi's signature). |  |
| `xqsystem/upload_rom` | ✓ Uploads a firmware file for a manual update. |  |
| `xqsystem/upnp` | ✓ UPnP: status 1/0 and list[{protocol, name, ip, cport, rport}] of open ports. | `GET {}` |
| `xqsystem/upnp_switch` | ✓ Turns UPnP on/off. | `GET {"switch": 1}` |
| `xqsystem/usbmode` | ✓ Prepares USB for an update (no effect on the AX1800). |  |
| `xqsystem/usbservice` | ✓ Turns USB services on/off during an update. |  |
| `xqsystem/vpn` | ✓ VPN servers: list[{id, oname, proto pptp/l2tp, server, username, password}], current{id, auto, …}. | `GET {}` |
| `xqsystem/vpn_status` | ✓ VPN state: 0 connected, 1 connecting, 2 failed, 3 disconnected, 4 not enabled; uptime; errcode/errmsg. | `GET {}` |
| `xqsystem/vpn_switch` | ✓ Connects (conn 1) or disconnects (conn 0) the VPN. | `GET {"conn": 1, "id": "1"}` |
| `xqsystem/wps` | **⚠ INFERRED** — Starts WPS pairing. |  |
| `xqsystem/wps_cancel` | **⚠ INFERRED** — Cancels WPS pairing. |  |
| `xqsystem/wps_status` | ✓ WPS status (push-button pairing). |  |
