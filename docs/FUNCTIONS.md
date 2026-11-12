# Internal functions of the Xiaomi AX1800 (RM1800)

Generated from `desktop/funcoes.json` + `desktop/funcoes_en.json` by `tools/build_ha_panel.py`. **✓** = confirmed (tested on the device or usage seen in the UI/app code); **⚠ INFERRED** = deduced from the name/context only.

| Function | Description | Example call |
|---|---|---|
| `cportal/allow` | **⚠ INFERRED** — Firmware 1.0.394 function (controller captivePortalAllow; untested). |  |
| `miats/ccgame` | **⚠ INFERRED** — Firmware 1.0.394 function (controller turbo_ccgame_call; untested). |  |
| `miats/free_speed_up` | **⚠ INFERRED** — Firmware 1.0.394 function (controller free_speed_up; untested). |  |
| `miats/general_event_get` | **⚠ INFERRED** — Firmware 1.0.394 function (controller general_event_get; untested). |  |
| `miats/get_cw_event_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller get_cw_event_info; untested). |  |
| `miats/get_free_speed_up_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller get_free_speed_up_info; untested). |  |
| `miats/get_gg_block_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller get_ad_block_info; untested). |  |
| `miats/get_new_access` | **⚠ INFERRED** — Firmware 1.0.394 function (controller get_new_access; untested). |  |
| `miats/get_speed_up_total_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller get_speed_up_total_info; untested). |  |
| `miats/get_vip_pay_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller get_vip_pay_info; untested). |  |
| `miats/get_wifi_danger_device` | **⚠ INFERRED** — Firmware 1.0.394 function (controller get_wifi_danger_device; untested). |  |
| `miats/get_wifi_new_block` | **⚠ INFERRED** — Firmware 1.0.394 function (controller get_wifi_new_block; untested). |  |
| `miats/ipv6` | **⚠ INFERRED** — Firmware 1.0.394 function (controller turbo_ipv6_call; untested). |  |
| `miats/remote_call` | **⚠ INFERRED** — Firmware 1.0.394 function (controller remote_call; untested). |  |
| `miats/set_wifi_blist` | **⚠ INFERRED** — Firmware 1.0.394 function (controller set_wifi_black_device; untested). |  |
| `miats/uplink_free_speed_up` | **⚠ INFERRED** — Firmware 1.0.394 function (controller uplink_free_speed_up; untested). |  |
| `miats/uplink_get_free_speed_up_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller uplink_get_free_speed_up_info; untested). |  |
| `miats/uplink_vip_speed_up` | **⚠ INFERRED** — Firmware 1.0.394 function (controller uplink_vip_speed_up; untested). |  |
| `miats/valid_show_cb` | **⚠ INFERRED** — Firmware 1.0.394 function (controller valid_show_cb; untested). |  |
| `miats/validate_token_v2` | **⚠ INFERRED** — Firmware 1.0.394 function (controller validate_token; untested). |  |
| `miats/vip_speed_up` | **⚠ INFERRED** — Firmware 1.0.394 function (controller vip_speed_up; untested). |  |
| `miats/web_enable_show` | **⚠ INFERRED** — Firmware 1.0.394 function (controller web_enable_show; untested). |  |
| `miats/wifi_macfilter_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiMacfilterInfo; untested). |  |
| `misns/authorization_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller authorizationStatus; untested). |  |
| `misns/ios_ready` | **⚠ INFERRED** — Firmware 1.0.394 function (controller iosReady; untested). |  |
| `misns/prepare` | **⚠ INFERRED** — Firmware 1.0.394 function (controller prepare; untested). |  |
| `misns/prepare_bytype` | **⚠ INFERRED** — Firmware 1.0.394 function (controller prepare; untested). |  |
| `misns/prepare_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller prepareStatus; untested). |  |
| `misns/sns_init` | **⚠ INFERRED** — Firmware 1.0.394 function (controller snsInit; untested). |  |
| `misns/sns_list` | **⚠ INFERRED** — Firmware 1.0.394 function (controller snsList; untested). |  |
| `misns/wifi_access` | **⚠ INFERRED** — Firmware 1.0.394 function (controller wifiAccess; untested). |  |
| `misns/wifi_share_blist` | **⚠ INFERRED** — Firmware 1.0.394 function (controller wifiShareBlacklist; untested). |  |
| `misns/wifi_share_blist_edit` | **⚠ INFERRED** — Firmware 1.0.394 function (controller wifiShareBlacklistEdit; untested). |  |
| `misns/wifi_share_clear` | **⚠ INFERRED** — Erases the guest network settings. |  |
| `misns/wifi_share_info` | ✓ Guest network: on/off, name, password and security. |  |
| `misns/wifi_share_info_web` | **⚠ INFERRED** — Firmware 1.0.394 function (controller wifiShareInfoWeb; untested). |  |
| `misns/wifi_share_rent_switch` | **⚠ INFERRED** — Firmware 1.0.394 function (controller wifiShareRentSwitch; untested). |  |
| `misns/wifi_share_switch` | **⚠ INFERRED** — Local guest network switch used by the cloud; parameters unknown (code 1523). Use set_wifi_without_restart. |  |
| `misystem/active` | ✓ Triggers the speed-history refresh (used after the speed test). |  |
| `misystem/app_status_switch` | **⚠ INFERRED** — Firmware 1.0.394 function (controller ustackSwitch; untested). |  |
| `misystem/arn_ignore` | **⚠ INFERRED** — Ignores/releases a device flagged by the anti-intrusion feature. |  |
| `misystem/arn_records` | ✓ Log of blocked intrusion attempts. |  |
| `misystem/arn_security` | ✓ Security center: privacy protection, malicious-site firewall and virus-file firewall. |  |
| `misystem/arn_security_switch` | ✓ Security center: info = JSON with malicious_url_firewall, virus_file_firewall, privacy_protection (0/1); wifi_arn touches the MAC filter. Tested. | `POST {"info": "{\"malicious_url_firewall\": 1}"}` |
| `misystem/arn_status` | ✓ Anti-intrusion (防蹭网): on/off, level and count of blocked attempts. |  |
| `misystem/arn_switch` | **⚠ INFERRED** — Anti-intrusion: open 0/1 (also turns the Wi-Fi MAC filter on/off, model mode 0 block / 1 allow list) and/or level. | `GET {"level": 2}` |
| `misystem/bandwidth_test` | ✓ Measures internet download speed (QoS test). |  |
| `misystem/c_backup` | ✓ Creates a configuration backup file (keys = parts to include). | `GET {"keys": "mi_basic_info,mi_network_info,mi_wifi_info,mi_lan_info,mi_arn_info"}` |
| `misystem/c_restore` | ✓ Restores the chosen items of the uploaded backup (comma-separated keys); a restart is needed afterwards. | `GET {"keys": "mi_wifi_info,mi_lan_info"}` |
| `misystem/c_upload` | ✓ Uploads a backup (multipart, file in the image field). Only reads the file: returns des.keys {key: description} to choose in c_restore. |  |
| `misystem/channel_scan_result` | ✓ Optimization result: 2G{cchannel current, cscore, schannel suggested, sscore (interference: lower is better), ranking, code 0 = ready}. | `GET {}` |
| `misystem/channel_scan_start` | ✓ Starts the 2.4 GHz channel analysis (the app's Wi-Fi optimization); result in channel_scan_result after ~10 s. | `GET {}` |
| `misystem/check_ip_conflict` | ✓ Checks for an IP conflict with the upstream router: ip_conflict "0" = none. |  |
| `misystem/check_status` | ✓ DISK check state — unused on the AX1800. |  |
| `misystem/conf_upload_enable` | **⚠ INFERRED** — Firmware 1.0.394 function (controller confUploadEnable; untested). |  |
| `misystem/debug` | **⚠ INFERRED** — Firmware 1.0.394 function (controller debug; untested). |  |
| `misystem/device_detail` | **⚠ INFERRED** — Details of one device (needs mac). | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/device_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDeviceInfo; untested). |  |
| `misystem/devicelist` | ✓ Known devices: name, MAC, IP, online, connection type (0 wired, 1 2.4 GHz, 2 5 GHz, 3 guest), speeds and permissions. |  |
| `misystem/disk_check` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskCheck; untested). |  |
| `misystem/disk_format` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskFormat; untested). |  |
| `misystem/disk_format_async` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskFormatAsync; untested). |  |
| `misystem/disk_format_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskFormatStatus; untested). |  |
| `misystem/disk_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDiskinfo; untested). |  |
| `misystem/disk_init` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskInit; untested). |  |
| `misystem/disk_repair` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskRepair; untested). |  |
| `misystem/disk_smartctl` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskSmartCtl; untested). |  |
| `misystem/disk_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskStatus; untested). |  |
| `misystem/ecos_info` | ✓ Ecosystem device information (needs parameters). |  |
| `misystem/ecos_switch` | **⚠ INFERRED** — Firmware 1.0.394 function (controller ecosSwitch; untested). |  |
| `misystem/ecos_upgrade` | **⚠ INFERRED** — Firmware 1.0.394 function (controller ecosUpgrade; untested). |  |
| `misystem/ecos_upgrade_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getEcosUpgradeStatus; untested). |  |
| `misystem/extendwifi_scanlist` | **⚠ INFERRED** — Lists nearby networks for wireless repeater mode. |  |
| `misystem/flash_test_cfg` | **⚠ INFERRED** — Firmware 1.0.394 function (controller flashTestConfig; untested). |  |
| `misystem/flash_test_res` | **⚠ INFERRED** — Firmware 1.0.394 function (controller flashTestResGet; untested). |  |
| `misystem/get_config_result` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getConfigResult; untested). |  |
| `misystem/get_dev_bsd` | ✓ Device band in unified Wi-Fi (mac) → bsd, mode. |  |
| `misystem/get_iotdev_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getIotDevStatus; untested). |  |
| `misystem/get_iotdev_status_hidessid` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getIotDevStatusHidessid; untested). |  |
| `misystem/get_mesh_device_info` | ✓ Mesh node info: does NOT work on this model (error 500). |  |
| `misystem/get_mesh_metric` | ✓ Mesh metric: does NOT work on this model (code 127 — the whcal command is not in firmware 1.0.399; Mesh uses Qualcomm repacd/lbd). |  |
| `misystem/get_netwan_mode` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getNetWanMode; untested). |  |
| `misystem/get_portscan_result` | ✓ Result: tcp_port and udp_port (space-separated). | `GET {"ip": "192.168.0.50", "mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/get_unconfig_iotdev_hidessid` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getunConfigIotDevHidessid; untested). |  |
| `misystem/get_usb_u3` | ✓ USB 3.0 mode status (no effect on the AX1800, which has no USB). |  |
| `misystem/get_wan_mac` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWanMac; untested). |  |
| `misystem/get_weakdetect_result` | ✓ Result: ftp_weak_detect, ssh_weak_detect, telnet_weak_detect (empty = none). | `GET {"ip": "192.168.0.50", "mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/get_wifi_pwd` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiPwd; untested). |  |
| `misystem/get_wifi_pwd_url` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiPwdUrl; untested). |  |
| `misystem/get_wifi_ret` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiRet; untested). |  |
| `misystem/http_status` | ✓ Status of the router's HTTP interception (e.g. warning pages). |  |
| `misystem/http_switch` | **⚠ INFERRED** — Turns HTTP interception on/off. |  |
| `misystem/hwnat_status` | ✓ Hardware NAT acceleration: status 1 on / 0 off (0 on both routers on 2026-11-10). The real offload is Qualcomm NSS/ECM via /proc/xqfp, enabled when QoS is off (1.0.399 teardown). |  |
| `misystem/hwnat_switch` | ✓ Turns hardware NAT on/off (on 0/1) and REBOOTS; on this model the status stays 0 afterwards (tested 2026-11-10). There is no init.d/hwnat: NSS/ECM offload is owned by QoS via /proc/xqfp/open_fastpath_v3 (1.0.399 teardown). |  |
| `misystem/io_data` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getIOData; untested). |  |
| `misystem/iperf` | **⚠ INFERRED** — iperf server to measure local network speed. |  |
| `misystem/led` | ✓ LED status; with on=0/1 turns the device lights off/on. | `GET {"on": 1}` |
| `misystem/log_upload` | **⚠ INFERRED** — Firmware 1.0.394 function (controller syslogUpload; untested). |  |
| `misystem/lsusb` | **⚠ INFERRED** — Firmware 1.0.394 function (controller lsusb; untested). |  |
| `misystem/mem_test_cfg` | **⚠ INFERRED** — Firmware 1.0.394 function (controller memTestConfig; untested). |  |
| `misystem/mem_test_res` | **⚠ INFERRED** — Firmware 1.0.394 function (controller memTestResGet; untested). |  |
| `misystem/messages` | ✓ Bell notices: messages[{type 1 new version {version} / 3 5 GHz failure / 4 IP conflict {ip}, timestamp}], count. | `GET {}` |
| `misystem/mi_vpn` | ✓ Turns "Xiaomi services via VPN" on/off (the official page disconnects the VPN first). | `GET {"open": 1}` |
| `misystem/mi_vpn_info` | ✓ "Xiaomi services via VPN": status 1/0. | `GET {}` |
| `misystem/minet_ctrl_state` | **⚠ INFERRED** — Firmware 1.0.394 function (controller minetCtrlState; untested). |  |
| `misystem/minet_get_cfg` | **⚠ INFERRED** — Firmware 1.0.394 function (controller minetGetConfig; untested). |  |
| `misystem/minet_get_state` | ✓ MiNet status (quick setup of Xiaomi devices); returns an error on this device. |  |
| `misystem/minet_grant_dev` | **⚠ INFERRED** — Firmware 1.0.394 function (controller minetGrantDevice; untested). |  |
| `misystem/minet_list_dev` | **⚠ INFERRED** — Firmware 1.0.394 function (controller minetListDevice; untested). |  |
| `misystem/minet_set_cfg` | **⚠ INFERRED** — Firmware 1.0.394 function (controller minetSetConfig; untested). |  |
| `misystem/miwifi` | **⚠ INFERRED** — Firmware 1.0.394 function (controller isMiWiFi; untested). |  |
| `misystem/net_diagnose_result` | ✓ Result: status 1 ok, 2 problem (wan up/down, diagnose 111/112/113/114/678/633/101/691/100, dns), 3 undefined. | `GET {}` |
| `misystem/net_diagnose_start` | ✓ Starts the app's network diagnostics (async). | `GET {}` |
| `misystem/netacctl_set` | **⚠ INFERRED** — Sets a device's internet access control. |  |
| `misystem/netacctl_status` | ✓ Per-device internet access control (needs parameters). |  |
| `misystem/newstatus` | ✓ 2.4/5 GHz summary (name and connected clients). Warning: returns the 2.4 GHz password in the 'pssswd' field. |  |
| `misystem/ota` | **⚠ INFERRED** — Automatic update: auto 0/1, time (hour), plugin 0/1. | `GET {}` |
| `misystem/parctl_add` | ✓ Creates a rule: mac, enable, frequency "1,2,3,4,5", timeseg "22:00-07:00"; returns id. Tested. | `GET {"mac": "AA:BB:CC:DD:EE:FF", "enable": 1, "frequency": "1,2,3,4,5", "timeseg": "22:00-07:00"}` |
| `misystem/parctl_delete` | ✓ Removes a rule (id). Tested. |  |
| `misystem/parctl_get_filter` | **⚠ INFERRED** — Device site filter: urlfilter{mode none/black/white, count}. | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/parctl_get_url` | ✓ Site list (mac, mode black/white). |  |
| `misystem/parctl_info` | **⚠ INFERRED** — Parental control: device rules (mac) — id, enable, frequency [1..7], timeseg {from, to}. | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/parctl_set_filter` | ✓ Sets the site filter (mac, mode none/black/white). Tested. |  |
| `misystem/parctl_set_url` | ✓ Adds (opt 0) or removes (opt 1) a site (mac, mode, url; newurl to replace). Tested. |  |
| `misystem/parctl_update` | ✓ Updates a rule (id, mac, enable, frequency, timeseg). Tested. |  |
| `misystem/password` | **⚠ INFERRED** — Firmware 1.0.394 function (controller changePassword; untested). |  |
| `misystem/pppoe_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getPPPoEStatus; untested). |  |
| `misystem/pppoe_stop` | **⚠ INFERRED** — Firmware 1.0.394 function (controller pppoeStop; untested). |  |
| `misystem/qos_app_entry` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosApp; untested). |  |
| `misystem/qos_dev_info` | **⚠ INFERRED** — QoS limit of a specific device (needs parameters). |  |
| `misystem/qos_guest` | ✓ Guest network speed limit (percent, percent_up of the bandwidth). | `GET {"percent": 0.5, "percent_up": 0.5}` |
| `misystem/qos_info` | ✓ QoS settings: on/off, mode, bandwidth, guest network limit and per-device limits. |  |
| `misystem/qos_info_new` | ✓ Newer QoS summary used by the app (bandwidth, limits per MAC). |  |
| `misystem/qos_limit` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosLimit; untested). |  |
| `misystem/qos_limit_flag` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosLimitFlag; untested). |  |
| `misystem/qos_limits` | ✓ Per-device limits in KB/s (0 = no limit): data = JSON [{mac, maxup, maxdown}]. The official page calls qos_mode with the current mode afterwards. | `POST {"data": "[{\"mac\": \"AA:BB:CC:DD:EE:FF\", \"maxup\": 500, \"maxdown\": 2000}]"}` |
| `misystem/qos_mode` | ✓ QoS mode (mode): auto/gaming/browsing/video/manual. | `GET {"mode": 0}` |
| `misystem/qos_offlimit` | ✓ Removes a device's speed limit (mac). | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/qos_set_dev_info` | **⚠ INFERRED** — Writes a device's QoS limit (used by the app). |  |
| `misystem/qos_switch` | ✓ Turns QoS on/off (on). | `GET {"on": 0}` |
| `misystem/qos_wangzhe` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosWangZhe; untested). |  |
| `misystem/qos_xq` | ✓ Limit for the router's own traffic, as a fraction of the bandwidth (percent, percent_up); read in qos_info.local. | `GET {"percent": 0.9, "percent_up": 0.9}` |
| `misystem/r_ip_conflict` | ✓ Avoids the IP conflict with the upstream router by moving the LAN to the IP suggested in messages (type 4). Restarts the Wi-Fi. | `POST {}` |
| `misystem/register` | **⚠ INFERRED** — Firmware 1.0.394 function (controller register; untested). |  |
| `misystem/repair_status` | ✓ DISK repair state (not network) — unused on the AX1800. |  |
| `misystem/router_common_status` | ✓ Summary for the app: devices, WAN speed and USB. |  |
| `misystem/router_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getRouterBaseInfo; untested). |  |
| `misystem/router_name` | ✓ Router name and location. |  |
| `misystem/set_band` | ✓ Sets the contracted bandwidth (upload/download in Mbps) used by QoS. | `POST {"manual": 1, "upload": 250, "download": 500}` |
| `misystem/set_band_app` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setBandApp; untested). |  |
| `misystem/set_bt` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setBt; untested). |  |
| `misystem/set_channel` | ✓ Applies channels (channel1 = 2.4 GHz, channel2 = 5 GHz); saved to the config; ~5 s without dropping the Wi-Fi (tested). | `GET {"channel1": 6, "channel2": 36}` |
| `misystem/set_config_iotdev_hidessid` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setConfigIotDevHidessid; untested). |  |
| `misystem/set_dev_bsd` | **⚠ INFERRED** — Pins the device band (mac, mode); restarts the Wi-Fi. |  |
| `misystem/set_log` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setConfigLog; untested). |  |
| `misystem/set_mesh_device` | ✓ Removes (op 1) or restarts (op 2) a Mesh node (mesh_mac). No effect on this model (tested 2026-11-10; whcal/whc_ual absent in firmware 1.0.399). |  |
| `misystem/set_mesh_normal` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setMeshInfo; untested). |  |
| `misystem/set_ota` | **⚠ INFERRED** — Sets automatic update (auto, time, plugin). | `GET {"auto": 1, "time": 4, "plugin": 0}` |
| `misystem/set_router_lanap` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setLanApMode; untested). |  |
| `misystem/set_router_lanap_init` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setLanApMode_Init; untested). |  |
| `misystem/set_router_name` | ✓ Changes name and location (name, locale). | `GET {"name": "WMON-AX1800", "locale": "Escritório"}` |
| `misystem/set_router_normal` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setRouterInfo; untested). |  |
| `misystem/set_router_wifiap` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setWifiApMode; untested). |  |
| `misystem/set_router_wifiap_init` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setWifiApMode_Init; untested). |  |
| `misystem/set_sys_time` | ✓ Sets the time zone (timezone, index) or the time (time 'YYYY-MM-DD hh:mm:ss'). | `POST {"timezone": "<valor da lista de fusos>", "index": 3}` |
| `misystem/set_wan` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setWan; untested). |  |
| `misystem/smartvpn_info` | ✓ VPN smart split: switch, mode (1 by address, 2 by device), ulist, mlist, name{mac: name}. | `GET {}` |
| `misystem/smartvpn_mac` | ✓ Adds (opt 0) or removes (opt 1) devices from smart split. | `POST {"macs": "AA:BB:CC:DD:EE:FF", "opt": 0}` |
| `misystem/smartvpn_switch` | ✓ Turns smart split on/off and chooses the mode. | `GET {"enable": 1, "mode": 1}` |
| `misystem/smartvpn_url` | ✓ Adds (opt 0) or removes (opt 1) an address from smart split. | `POST {"url": "example.com", "opt": 0}` |
| `misystem/speed_test` | **⚠ INFERRED** — Starts the app's speed test. |  |
| `misystem/speed_test_result` | ✓ Result of the app's speed test. |  |
| `misystem/start_portscan` | ✓ Scans a device's open ports (ip, mac). | `GET {"ip": "192.168.0.50", "mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/start_weakdetect` | ✓ Tests weak FTP/SSH/Telnet passwords on a device (ip, mac). | `GET {"ip": "192.168.0.50", "mac": "AA:BB:CC:DD:EE:FF"}` |
| `misystem/status` | ✓ Overall status: uptime, CPU, memory, device count, WAN traffic (current, peak, total) and hardware. |  |
| `misystem/sys_log` | ✓ Generates a system-log package and returns the download path. |  |
| `misystem/sys_time` | ✓ Router time, time zone (timezone + option index) and Mesh role (whc_cap main / whc_re node). |  |
| `misystem/tb_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller toolbarInfo; untested). |  |
| `misystem/topo_graph` | ✓ Mesh network topology: main router and nodes (name, IP, location, model). |  |
| `misystem/usb_u3` | ✓ Turns USB 3.0 on/off (enable) — no effect on the AX1800. |  |
| `misystem/vas_info` | ✓ Value-added services (Xiaomi ads/plug-ins); empty on this device. |  |
| `misystem/vas_info_new` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getVasInfoNew; untested). |  |
| `misystem/vas_switch` | **⚠ INFERRED** — Turns value-added services on/off. |  |
| `misystem/vas_switch_new` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setVasInfoNew; untested). |  |
| `misystem/web_access_info` | ✓ Admin access control: on/off and list of allowed MACs. |  |
| `misystem/web_access_opt` | ✓ Turns access control on/off and adds/removes allowed MACs. | `POST {"open": 1}` |
| `xqdatacenter/check_file_exist` | **⚠ INFERRED** — Firmware 1.0.394 function (controller checkFileExist; untested). |  |
| `xqdatacenter/device_id` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDeviceId; untested). |  |
| `xqdatacenter/download` | **⚠ INFERRED** — Firmware 1.0.394 function (controller download; untested). |  |
| `xqdatacenter/fsys_probe` | **⚠ INFERRED** — Firmware 1.0.394 function (controller fsysProbe; untested). |  |
| `xqdatacenter/fsys_resume` | **⚠ INFERRED** — Firmware 1.0.394 function (controller fsysResume; untested). |  |
| `xqdatacenter/identify_device` | **⚠ INFERRED** — Identifies a device's type/manufacturer. |  |
| `xqdatacenter/plugin_ssh` | **⚠ INFERRED** — Firmware 1.0.394 function (controller pluginSSH; untested). |  |
| `xqdatacenter/plugin_ssh_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller pluginSSHStatus; untested). |  |
| `xqdatacenter/request` | ✓ Generic numbered-command channel ('api' in the payload) used by the UI and the cloud. |  |
| `xqdatacenter/thumb` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getThumb; untested). |  |
| `xqdatacenter/upload` | **⚠ INFERRED** — Firmware 1.0.394 function (controller upload; untested). |  |
| `xqnetdetect/detect` | **⚠ INFERRED** — The app's "health check": cpuavg, memoryuse, cputemp, link, wan, gateway, dnsstatus, ping, wifi (password strength), speed, disk (params simple, target; simple=1 gave error 500). |  |
| `xqnetdetect/netspeed` | **⚠ INFERRED** — Firmware 1.0.394 function (controller netspeed; untested). |  |
| `xqnetdetect/nettb` | ✓ Quick device → router → internet test: error 0 = ok. | `GET {}` |
| `xqnetdetect/netupspeed` | ✓ Measures internet upload speed. |  |
| `xqnetdetect/ping_test` | ✓ Ping from the router (url) → result 1 = reachable. |  |
| `xqnetdetect/sys_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getSysInfo; untested). |  |
| `xqnetdetect/sys_status` | ✓ Quick check: status 0 ok, 1 CPU/memory > 90 % or temperature > 70 °C, 2 no WAN link (returns 2 on this model even with internet). |  |
| `xqnetwork/add_mesh_node` | ✓ Adds a node to the Mesh. locate = room name in Chinese (客厅, 主卧, 次卧, 书房, 厨房, 办公室, 地下室, 卫生间, 阁楼, 阳台, 餐厅). | `POST {"mac": "AA:BB:CC:DD:EE:FF", "locate": "客厅"}` |
| `xqnetwork/add_range_redirect` | ✓ Adds a port range rule. Takes effect after redirect_apply. | `POST {"name": "Jogo", "proto": 3, "fport": 3000, "tport": 3010, "ip": "192.168.0.50"}` |
| `xqnetwork/add_redirect` | ✓ Adds a port rule (POST name, proto, sport, ip, dport). No edit on this firmware: force is ignored (code 1608) — delete and re-add. Takes effect after redirect_apply. Tested. | `POST {"name": "Servidor", "proto": 1, "sport": 8443, "ip": "192.168.0.50", "dport": 443}` |
| `xqnetwork/add_server` | ✓ Adds a DDNS service. Provider id: 1 No-IP, 2 Oray, 3 3322.org, 4 Dyn. | `GET {"id": 1, "username": "usuario", "password": "senha", "domain": "myhome.ddns.net", "checkinterval": 10, "forceinterval": 24, "enable": 1}` |
| `xqnetwork/app_set_wifi_ap` | **⚠ INFERRED** — Firmware 1.0.394 function (controller appSetWifiApMode; untested). |  |
| `xqnetwork/app_wifiap_restart` | **⚠ INFERRED** — Firmware 1.0.394 function (controller wifiAPserviceRestart; untested). |  |
| `xqnetwork/avaliable_channels` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getChannels; untested). |  |
| `xqnetwork/channel_scan_result` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getScanResult; untested). |  |
| `xqnetwork/channel_scan_start` | **⚠ INFERRED** — Firmware 1.0.394 function (controller channelScanStart; untested). |  |
| `xqnetwork/check_wan_link` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getAutoWanLink; untested). |  |
| `xqnetwork/check_wan_type` | ✓ Detects the connection type on the WAN port: 1 PPPoE, 2 DHCP, 3 static IP, 99 no cable, other = unknown (returns 0 with PPPoE connected). | `GET {}` |
| `xqnetwork/ddns` | ✓ DDNS services: on (service on), list[{id, servicename, domain, enabled, status 0 error/1 ok/2 connecting, lastupdate, wanip, error}]. | `GET {}` |
| `xqnetwork/ddns_edit` | ✓ Edits a DDNS service (same parameters as add_server). |  |
| `xqnetwork/ddns_reload` | ✓ Forces a DDNS update now. | `GET {}` |
| `xqnetwork/ddns_switch` | ✓ Turns the router's DDNS service on/off. | `GET {"on": 0}` |
| `xqnetwork/del_server` | ✓ Removes a DDNS service. | `GET {"id": 1}` |
| `xqnetwork/delete_redirect` | ✓ Removes a port or range rule (port = external port or the range's start port). | `POST {"port": 8443, "proto": 1}` |
| `xqnetwork/device_statistics` | ✓ Accumulated traffic of one device (mac). |  |
| `xqnetwork/devices_statistics` | ✓ Accumulated traffic of all devices: statistics[{mac, devname, download, upload (bytes), max…speed, online (s)}]. |  |
| `xqnetwork/diag_disk_test` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diagDiskTest; untested). |  |
| `xqnetwork/diag_get_log` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDiagLog; untested). |  |
| `xqnetwork/diag_get_paras` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDiagParas; untested). |  |
| `xqnetwork/diag_hdd_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diagHddStatus; untested). |  |
| `xqnetwork/diag_set_paras` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setDiagParas; untested). |  |
| `xqnetwork/diag_usb_test` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diagUsbTest; untested). |  |
| `xqnetwork/diag_wifi_test` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diagWifiTest; untested). |  |
| `xqnetwork/diagdevicelist` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDiagDeviceList; untested). |  |
| `xqnetwork/diagdiskstatus` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDiagDiskStatus; untested). |  |
| `xqnetwork/diagudiskstatus` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDiagUdiskStatus; untested). |  |
| `xqnetwork/disable_ap` | ✓ Leaves wireless repeater mode and goes back to router (restores previous settings). Returns lanip and ssid. | `GET {}` |
| `xqnetwork/disable_lan_ap` | ✓ Leaves wired repeater mode and goes back to router. Returns ip. | `GET {}` |
| `xqnetwork/dmz` | ✓ DMZ: status (1 = on; 0/2 = off), device ip, router lanip. | `GET {}` |
| `xqnetwork/dmz_off` | ✓ Turns DMZ off (the official page calls dmz_reload afterwards). | `GET {}` |
| `xqnetwork/dmz_reload` | ✓ Reloads the DMZ configuration. | `GET {}` |
| `xqnetwork/edit_device` | ✓ Adds (option=0) or removes (option=1) a MAC from the filter list. | `GET {"mac": "AA:BB:CC:DD:EE:FF", "model": 0, "option": 0}` |
| `xqnetwork/get_addnode_status` | ✓ Node add progress: 0 done, 1 connecting, 2 syncing, 3 expanding (1–2 min), 4 failed. | `GET {"mac": "AA:BB:CC:DD:EE:FF"}` |
| `xqnetwork/get_miotrelay_switch` | ✓ Quick connect (畅快连) status for Mi Home devices. |  |
| `xqnetwork/get_miscan_switch` | ✓ AIoT antenna scan status. |  |
| `xqnetwork/get_netmode` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getNetMode; untested). |  |
| `xqnetwork/get_server` | ✓ One DDNS service's data (username, password, domain, checkinterval, forceinterval, enabled). | `GET {"id": 1}` |
| `xqnetwork/get_son_backhaul_mode` | ✓ 'Priority for many devices' (多终端接入优先) status. |  |
| `xqnetwork/get_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getModeStatus; untested). |  |
| `xqnetwork/get_wifi_weak` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiWeakInfo; untested). |  |
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
| `xqnetwork/qos_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getQosInfo; untested). |  |
| `xqnetwork/qos_limit` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosLimit; untested). |  |
| `xqnetwork/qos_limits` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosLimits; untested). |  |
| `xqnetwork/qos_mode` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosMode; untested). |  |
| `xqnetwork/qos_offlimit` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosOffLimit; untested). |  |
| `xqnetwork/qos_switch` | **⚠ INFERRED** — Firmware 1.0.394 function (controller qosSwitch; untested). |  |
| `xqnetwork/redirect_apply` | ✓ Applies the forwarding rules (the official page's "保存并生效" button). | `GET {}` |
| `xqnetwork/savebind` | **⚠ INFERRED** — Firmware 1.0.394 function (controller saveBind; untested). |  |
| `xqnetwork/scan_mesh_node` | ✓ Scans for available Mesh nodes: list[{ssid, mac, rssi}] (rssi < -60 = too far). Takes a few seconds. | `GET {}` |
| `xqnetwork/server_switch` | ✓ Enables/disables a DDNS service (only one active at a time). | `GET {"id": 1, "on": 1}` |
| `xqnetwork/set_all_wifi` | ✓ Unified Wi-Fi: bsd 1 (only on1/ssid1/pwd1/encryption1/channel1/bandwidth1/hidden1/txpwr1) or bsd 0 (also the …2 fields). Restarts the Wi-Fi. |  |
| `xqnetwork/set_band` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setBand; untested). |  |
| `xqnetwork/set_channel` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setChannel; untested). |  |
| `xqnetwork/set_dmz` | ✓ Turns DMZ on for an IP (POST ip). Refused (code 1610) while any port-forwarding rule exists. Tested. | `POST {"ip": "192.168.0.50"}` |
| `xqnetwork/set_lan_ap` | ✓ Switches to wired repeater (access point; WAN connected to another router). Returns the new ip. | `POST {"ssid": "", "password": ""}` |
| `xqnetwork/set_lan_dhcp` | ✓ Changes or turns off the DHCP server. | `GET {"ignore": 0, "start": 100, "end": 200, "leasetime": "720m", "dns1": "", "dns2": "", "router": "192.168.0.1"}` |
| `xqnetwork/set_lan_ip` | ✓ Changes the router IP (restarts). | `GET {"ip": "192.168.0.1"}` |
| `xqnetwork/set_peer_wifi_auto_ap_mode` | **⚠ INFERRED** — Automatic access-point setup between Mesh nodes. |  |
| `xqnetwork/set_son_backhaul_mode` | ✓ Turns priority for many devices on/off (mode). | `POST {"mode": 0}` |
| `xqnetwork/set_wan` | ✓ Changes the internet connection (PPPoE, DHCP or static IP). | `POST {"wanType": "pppoe", "pppoeName": "usuario", "pppoePwd": "senha-exemplo", "mtu": 1480, "service": "", "special": 0, "dns1": "", "dns2": "", "autoset": 1}` |
| `xqnetwork/set_wan6` | ✓ IPv6 mode (POST): wanType=native (passes the ISP prefix through, which changes on every reconnection), nat (NAT6: home network with fixed prefix fd00:6868:6868::/64) or static; autosetipv6=0/1 (automatic/manual DNS), dns1, dns2. | `POST {"wanType": "nat", "autosetipv6": 1, "dns1": "2001:4860:4860::8888", "dns2": "2606:4700:4700::1111"}` |
| `xqnetwork/set_wan_new` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setWanNew; untested). |  |
| `xqnetwork/set_wan_speed` | ✓ WAN port speed (speed 0 auto/100/1000). | `POST {"speed": 0}` |
| `xqnetwork/set_wifi` | ✓ Changes a Wi-Fi network (wifiIndex 1=2.4 GHz, 2=5 GHz, 3=guest): name, password, security, channel, width, hidden, power; and weak-signal roaming. | `POST {"wifiIndex": 1, "on": 1, "ssid": "MinhaRede", "pwd": "senha-exemplo", "encryption": "psk2", "channel": 0, "bandwidth": 0, "hidden": 0, "txpwr": "max"}` |
| `xqnetwork/set_wifi_ap` | ✓ Switches to wireless repeater of the given network (usage seen on the official page). Optional: nssid/nencryption/npassword for its own Wi-Fi. Returns ip and ssid. | `POST {"ssid": "MinhaRede", "password": "senha", "encryption": "WPA2PSK", "enctype": "AES", "channel": "6", "bandwidth": "20", "band": "2g"}` |
| `xqnetwork/set_wifi_ax` | ✓ Wi-Fi 6 on (ax=1) or Wi-Fi 5 compatibility mode (ax=0). | `POST {"ax": 1}` |
| `xqnetwork/set_wifi_macfilter` | ✓ Turns the MAC filter on/off and sets its mode (model, enable). | `POST {"model": 0, "enable": 1}` |
| `xqnetwork/set_wifi_txbf` | ✓ Turns MU-MIMO on/off (txbf). | `POST {"txbf": 1}` |
| `xqnetwork/set_wifi_txpwr` | ✓ Changes the power of BOTH bands at once (txpwr max/mid/min) in ~5 s without restarting the Wi-Fi (tested 2026-11-09). The screen that used it was removed from the firmware. | `GET {"txpwr": "max"}` |
| `xqnetwork/set_wifi_weak` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setWifiWeakInfo; untested). |  |
| `xqnetwork/set_wifi_without_restart` | ✓ Changes only the given fields without restarting Wi-Fi. wifiIndex=3 + on=1/0 turns the guest network on/off; wifiIndex=1/2 + hidden=1/0 hides/shows the SSID (not mirrored to the Mesh node). | `GET {"wifiIndex": 3, "on": 1}` |
| `xqnetwork/unbindall` | **⚠ INFERRED** — Firmware 1.0.394 function (controller unbindAll; untested). |  |
| `xqnetwork/wan_down` | **⚠ INFERRED** — Brings the WAN down (ifdown wan). |  |
| `xqnetwork/wan_info` | ✓ Internet: type (PPPoE/DHCP/static), IP, gateway, DNS, MTU, connected time, IPv6 and MAC in use. |  |
| `xqnetwork/wan_link` | ✓ WAN cable connected (link 1/0). |  |
| `xqnetwork/wan_speed` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWanSpeed; untested). |  |
| `xqnetwork/wan_statistics` | ✓ Accumulated internet traffic: download, upload (bytes), current and peak speeds. |  |
| `xqnetwork/wan_up` | **⚠ INFERRED** — Brings the WAN up (ifup wan). |  |
| `xqnetwork/wifi_connect_devices` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiConDev; untested). |  |
| `xqnetwork/wifi_detail` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiInfo; untested). |  |
| `xqnetwork/wifi_detail_all` | ✓ Full Wi-Fi settings per band (name, password, security, channel, width, power, hidden, Wi-Fi 6, MU-MIMO, roaming) and unified Wi-Fi. |  |
| `xqnetwork/wifi_diag_detail_all` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDiagAllWifiInfo; untested). |  |
| `xqnetwork/wifi_down` | **⚠ INFERRED** — Turns a band's radio off (wifiIndex 1/2) without changing the config. |  |
| `xqnetwork/wifi_list` | ✓ Scans neighbouring networks (~12–15 s): ssid, bssid, band 2g/5g, channel, signal %, rssi, encryption, enctype (no width). Used by wireless-repeater mode. ⚠ Over-counts the router's own operating channel. | `GET {}` |
| `xqnetwork/wifi_macfilter_info` | ✓ Wi-Fi MAC filter: on/off, mode (blocklist/allowlist) and list. |  |
| `xqnetwork/wifi_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiStatus; untested). |  |
| `xqnetwork/wifi_txpwr_channel` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getWifiChTx; untested). |  |
| `xqnetwork/wifi_up` | **⚠ INFERRED** — Turns a band's radio on (wifiIndex 1/2) without changing the config. |  |
| `xqnetwork/wifiap_restart` | **⚠ INFERRED** — Firmware 1.0.394 function (controller serviceRestart; untested). |  |
| `xqnetwork/wifiap_signal` | ✓ Signal quality to the upstream router (node/repeater). |  |
| `xqpassport/binded` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getBindInfo; untested). |  |
| `xqpassport/login` | **⚠ INFERRED** — Firmware 1.0.394 function (controller passportLogin; untested). |  |
| `xqpassport/plugin_detail` | **⚠ INFERRED** — Firmware 1.0.394 function (controller pluginDetail; untested). |  |
| `xqpassport/plugin_disable` | **⚠ INFERRED** — Firmware 1.0.394 function (controller pluginDisable; untested). |  |
| `xqpassport/plugin_enable` | **⚠ INFERRED** — Firmware 1.0.394 function (controller pluginEnable; untested). |  |
| `xqpassport/plugin_list` | **⚠ INFERRED** — Firmware 1.0.394 function (controller pluginList; untested). |  |
| `xqpassport/rigister` | **⚠ INFERRED** — Firmware 1.0.394 function (controller routerRegister; untested). |  |
| `xqpassport/unbound` | **⚠ INFERRED** — Firmware 1.0.394 function (controller unboundRouter; untested). |  |
| `xqsmarthome/request` | **⚠ INFERRED** — Firmware 1.0.394 function (controller tunnelSmartHomeRequest; untested). |  |
| `xqsmarthome/request_camera` | **⚠ INFERRED** — Firmware 1.0.394 function (controller requestCamera; untested). |  |
| `xqsmarthome/request_miio` | **⚠ INFERRED** — Bridge to Mi Home (miIO) devices. |  |
| `xqsmarthome/request_miiolist` | **⚠ INFERRED** — Firmware 1.0.394 function (controller requestMiioList; untested). |  |
| `xqsmarthome/request_mitv` | **⚠ INFERRED** — Firmware 1.0.394 function (controller requestMitv; untested). |  |
| `xqsmarthome/request_smartcontroller` | ✓ Scenes/schedules engine (the app's scheduled reboot). Parameter format not discovered. |  |
| `xqsmarthome/request_yeelink` | **⚠ INFERRED** — Bridge to Yeelight lamps. |  |
| `xqsystem/app_limit` | ✓ Xunlei/Kuaipan app limits: does NOT work on this model (error 500). |  |
| `xqsystem/app_limit_switch` | **⚠ INFERRED** — Firmware 1.0.394 function (controller appLimitSwitch; untested). |  |
| `xqsystem/are_things_mounted` | **⚠ INFERRED** — Firmware 1.0.394 function (controller areThingsMounted; untested). |  |
| `xqsystem/backup_cancel` | **⚠ INFERRED** — Firmware 1.0.394 function (controller backupCancel; untested). |  |
| `xqsystem/backup_data` | **⚠ INFERRED** — Firmware 1.0.394 function (controller backupData; untested). |  |
| `xqsystem/backup_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller backupStatus; untested). |  |
| `xqsystem/bdata` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getBdataInfo; untested). |  |
| `xqsystem/cancel` | **⚠ INFERRED** — Firmware 1.0.394 function (controller cancelUpgrade; untested). |  |
| `xqsystem/check_rom_update` | ✓ Checks Xiaomi's servers for a firmware update. |  |
| `xqsystem/check_router_name_pending` | **⚠ INFERRED** — Firmware 1.0.394 function (controller checkRouterNamePending; untested). |  |
| `xqsystem/clear_router_name_pending` | **⚠ INFERRED** — Firmware 1.0.394 function (controller clearRouterNamePending; untested). |  |
| `xqsystem/count` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getConDevCount; untested). |  |
| `xqsystem/country_code` | ✓ Current Wi-Fi region and options (China, Hong Kong, Taiwan, Korea, Europe). |  |
| `xqsystem/create_sandbox` | **⚠ INFERRED** — Firmware 1.0.394 function (controller createSandbox; untested). |  |
| `xqsystem/del_vpn` | ✓ Removes a VPN server. | `GET {"id": "1"}` |
| `xqsystem/detection_ts` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDetectionTimestamp; untested). |  |
| `xqsystem/dev_notify` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setDevNotify; untested). |  |
| `xqsystem/device_list` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDeviceList; untested). |  |
| `xqsystem/device_list_zigbee` | **⚠ INFERRED** — Zigbee devices of routers with a built-in gateway (not applicable to the AX1800). |  |
| `xqsystem/device_mac` | ✓ MAC of the requesting client. |  |
| `xqsystem/devicelist` | **⚠ INFERRED** — Firmware 1.0.394 function (controller devicelistForMAgent; untested). |  |
| `xqsystem/disk_check` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskCheck; untested). |  |
| `xqsystem/disk_check_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskCheckStatus; untested). |  |
| `xqsystem/disk_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getDiskInfo; untested). |  |
| `xqsystem/disk_scan` | **⚠ INFERRED** — Firmware 1.0.394 function (controller diskScan; untested). |  |
| `xqsystem/extendwifi_connect_inited_router` | **⚠ INFERRED** — Firmware 1.0.394 function (controller ExtendWifiConnectInitedRouter; untested). |  |
| `xqsystem/extendwifi_get_root_dir_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller ExtendWifiGetRootDirInfo; untested). |  |
| `xqsystem/extendwifi_get_root_dir_useage` | **⚠ INFERRED** — Firmware 1.0.394 function (controller ExtendWifiGetRootDirUseage; untested). |  |
| `xqsystem/extendwifi_request_remote_api` | **⚠ INFERRED** — Firmware 1.0.394 function (controller ExtendWifiRequestRemoteAPI; untested). |  |
| `xqsystem/extendwifi_sign_for_auto_band` | **⚠ INFERRED** — Firmware 1.0.394 function (controller ExtendWifiSignForAutoBand; untested). |  |
| `xqsystem/fac_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getFacInfo; untested). |  |
| `xqsystem/farewell` | **⚠ INFERRED** — Firmware 1.0.394 function (controller farewell; untested). |  |
| `xqsystem/flash_permission` | **⚠ INFERRED** — Checks whether firmware flashing is allowed. |  |
| `xqsystem/flash_rom` | **⚠ INFERRED** — Firmware 1.0.394 function (controller flashRom; untested). |  |
| `xqsystem/flash_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller flashStatus; untested). |  |
| `xqsystem/get_ip` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getIp; untested). |  |
| `xqsystem/get_languages` | ✓ Original UI languages (Simplified Chinese, Traditional HK/TW). |  |
| `xqsystem/get_main_language` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getMainLang; untested). |  |
| `xqsystem/get_sys_avg_load` | ✓ System load: on this model it only returns processCount (cores). |  |
| `xqsystem/information` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getAllInfo; untested). |  |
| `xqsystem/init_info` | ✓ Public router information (model, version, region); answers without login. |  |
| `xqsystem/internet_connect` | **⚠ INFERRED** — Firmware 1.0.394 function (controller isInternetConnect; untested). |  |
| `xqsystem/io_data` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getIOData; untested). |  |
| `xqsystem/is_dropbear_started` | **⚠ INFERRED** — Tells whether the SSH server is running. (controller isDropbearStarted; untested). |  |
| `xqsystem/is_sandbox_created` | **⚠ INFERRED** — Firmware 1.0.394 function (controller isSandboxCreated; untested). |  |
| `xqsystem/lan_wan` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getLanWanSta; untested). |  |
| `xqsystem/login` | ✓ Admin login (nonce + sha1); returns the session token. |  |
| `xqsystem/ma_check` | **⚠ INFERRED** — Firmware 1.0.394 function (controller checkMobileAccel; untested). |  |
| `xqsystem/maccel` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setMobileAccel; untested). |  |
| `xqsystem/main_status_for_app` | **⚠ INFERRED** — Firmware 1.0.394 function (controller mainStatusForApp; untested). |  |
| `xqsystem/mode` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getMacfilterMode; untested). |  |
| `xqsystem/mount_things` | **⚠ INFERRED** — Firmware 1.0.394 function (controller mountThings; untested). |  |
| `xqsystem/net_diagnose_result` | **⚠ INFERRED** — Firmware 1.0.394 function (controller netDiagnoseResult; untested). |  |
| `xqsystem/net_diagnose_start` | **⚠ INFERRED** — Firmware 1.0.394 function (controller netDiagnoseStart; untested). |  |
| `xqsystem/new_router_bind_ok` | **⚠ INFERRED** — Firmware 1.0.394 function (controller newrouterBindOk; untested). |  |
| `xqsystem/nginx` | **⚠ INFERRED** — Firmware 1.0.394 function (controller nginxCacheStatus; untested). |  |
| `xqsystem/nof_switch` | **⚠ INFERRED** — Firmware 1.0.394 function (controller nofSwitch; untested). |  |
| `xqsystem/noflushd` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getNofStatus; untested). |  |
| `xqsystem/oneclick_get_remote_token` | **⚠ INFERRED** — Token for remote cloud access (app binding). |  |
| `xqsystem/ota` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getOTAInfo; untested). |  |
| `xqsystem/passport_bind_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getPassportBindInfo; untested). |  |
| `xqsystem/pred_status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller predownloadInfo; untested). |  |
| `xqsystem/pred_switch` | **⚠ INFERRED** — Firmware 1.0.394 function (controller predownloadSwitch; untested). |  |
| `xqsystem/privacy` | ✓ Privacy consent accepted. |  |
| `xqsystem/push_settings` | ✓ App notifications (silent mode, authorization). |  |
| `xqsystem/push_switch` | **⚠ INFERRED** — Turns app notifications on/off. |  |
| `xqsystem/reboot` | ✓ Restarts the router. | `GET {"client": "web"}` |
| `xqsystem/remove_passport_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller removePassportBindInfo; untested). |  |
| `xqsystem/renew_token` | **⚠ INFERRED** — Renews the session token. |  |
| `xqsystem/reset` | ✓ Factory reset (format 0/1). On a wired Mesh node: it comes back as a plain router and, after a power cycle, re-joins the Mesh by itself (tested 10/11). | `GET {"format": 0}` |
| `xqsystem/router_bind_ok` | ✓ Confirms binding the router to the Xiaomi account (used by the app via the cloud). |  |
| `xqsystem/router_init` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setRouter; untested). |  |
| `xqsystem/router_name` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getRouterName; untested). |  |
| `xqsystem/sdev` | **⚠ INFERRED** — Firmware 1.0.394 function (controller specialDevCount; untested). |  |
| `xqsystem/set_app_limit` | **⚠ INFERRED** — Sets Xunlei/Kuaipan app limits (xlmaxdownload, xlmaxupload, kpmaxdownload, kpmaxupload) — no useful effect outside China. |  |
| `xqsystem/set_country_code` | ✓ Changes the Wi-Fi region (channels and power). | `POST {"country": "CN"}` |
| `xqsystem/set_device_nickname` | **⚠ INFERRED** — Renames a device (mac, name; owner and device optional). |  |
| `xqsystem/set_inited` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setInited; untested). |  |
| `xqsystem/set_language` | ✓ Changes the original UI language. | `POST {"language": "zh_cn"}` |
| `xqsystem/set_mac_filter` | ✓ Blocks (wan=0) or allows (wan=1) a device's internet access. | `POST {"mac": "AA:BB:CC:DD:EE:FF", "wan": 0}` |
| `xqsystem/set_mode` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setMacfilterMode; untested). |  |
| `xqsystem/set_name_password` | ✓ Changes the admin password (proprietary AES encryption). |  |
| `xqsystem/set_ota` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setOTAInfo; untested). |  |
| `xqsystem/set_passport_bound` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setPassportBound; untested). |  |
| `xqsystem/set_payment_info` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setPaymentInfo; untested). |  |
| `xqsystem/set_privacy` | **⚠ INFERRED** — Stores the privacy consent. |  |
| `xqsystem/set_privacy_new` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setPrivacy_new; untested). |  |
| `xqsystem/set_router_name` | **⚠ INFERRED** — Firmware 1.0.394 function (controller setRouterName; untested). |  |
| `xqsystem/set_vpn` | ✓ Adds (WITHOUT the id field — any id, even empty, becomes an edit) or edits (with id) a VPN server. Editing changes the id. Tested. | `POST {"oname": "Trabalho", "proto": "l2tp", "server": "vpn.example.com", "username": "usuario", "password": "senha"}` |
| `xqsystem/set_vpnauto` | ✓ Connect the VPN when the router starts (auto 1/0). | `GET {"auto": 1}` |
| `xqsystem/shutdown` | ✓ Powers the router off. | `GET {}` |
| `xqsystem/sign_order` | **⚠ INFERRED** — Firmware 1.0.394 function (controller signOrder; untested). |  |
| `xqsystem/smart_shutdown` | ✓ Would power the router off and back on after delay1/delay2 MINUTES (XQFunction: sleep 60×delay1; uhbn 2 delay2). No effect on this model (tested 2026-11-10; the uhbn binary is not in firmware 1.0.399). |  |
| `xqsystem/start_dropbear` | ✓ Would start the SSH server (dropbear). Blocked by design: in the 1.0.399 teardown, init.d/dropbear returns early unless the version channel is NOT 'release' and nvram ssh_en=1 — ours is 'release', so there is no working SSH endpoint. |  |
| `xqsystem/start_nginx` | **⚠ INFERRED** — Firmware 1.0.394 function (controller startNginx; untested). |  |
| `xqsystem/status` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getStatusInfo; untested). |  |
| `xqsystem/stop_dropbear` | **⚠ INFERRED** — Stops the router's SSH server. (controller stopDropbear; untested). |  |
| `xqsystem/stop_nginx` | **⚠ INFERRED** — Firmware 1.0.394 function (controller stopNginx; untested). |  |
| `xqsystem/sys_recovery` | **⚠ INFERRED** — Firmware 1.0.394 function (controller sysRecovery; untested). |  |
| `xqsystem/system_info` | ✓ Model, version, firmware channel, uptime and name. |  |
| `xqsystem/token` | **⚠ INFERRED** — Session token for the app. |  |
| `xqsystem/umount_things` | **⚠ INFERRED** — Firmware 1.0.394 function (controller umountThings; untested). |  |
| `xqsystem/upgrade_rom` | **⚠ INFERRED** — Starts installing the downloaded firmware. |  |
| `xqsystem/upgrade_status` | **⚠ INFERRED** — Progress of an ongoing firmware update. |  |
| `xqsystem/upload_log` | ✓ Uploads the system logs to Xiaomi. |  |
| `xqsystem/upload_plug` | ✓ Installs a plug-in (requires Xiaomi's signature). |  |
| `xqsystem/upload_rom` | ✓ Uploads a firmware file for a manual update. |  |
| `xqsystem/upnp` | ✓ UPnP: status 1/0 and list[{protocol, name, ip, cport, rport}] of open ports. | `GET {}` |
| `xqsystem/upnp_switch` | ✓ Turns UPnP on/off. | `GET {"switch": 1}` |
| `xqsystem/usbmode` | ✓ Prepares USB for an update (no effect on the AX1800). |  |
| `xqsystem/usbservice` | ✓ Turns USB services on/off during an update. |  |
| `xqsystem/userdisk_data` | **⚠ INFERRED** — Firmware 1.0.394 function (controller getUserdiskDataInfo; untested). |  |
| `xqsystem/vpn` | ✓ VPN servers: list[{id, oname, proto pptp/l2tp, server, username, password}], current{id, auto, …}. | `GET {}` |
| `xqsystem/vpn_status` | ✓ VPN state: 0 connected, 1 connecting, 2 failed, 3 disconnected, 4 not enabled; uptime; errcode/errmsg. | `GET {}` |
| `xqsystem/vpn_switch` | ✓ Connects (conn 1) or disconnects (conn 0) the VPN. | `GET {"conn": 1, "id": "1"}` |
| `xqsystem/web_url` | **⚠ INFERRED** — Firmware 1.0.394 function (controller redirectUrl; untested). |  |
| `xqsystem/wifi_log` | ✓ Wi-Fi log: on this model it returns only {code: 0}, no data. |  |
| `xqsystem/wps` | **⚠ INFERRED** — Opens WPS pairing (2 min). | `GET {}` |
| `xqsystem/wps_cancel` | **⚠ INFERRED** — Cancels WPS pairing. | `GET {}` |
| `xqsystem/wps_status` | ✓ WPS state: 0 idle, 1 waiting, 2 connected (device{mac, company}), 3–7 failed/expired. | `GET {}` |
| `xqsystem/xunlei_api` | **⚠ INFERRED** — Firmware 1.0.394 function (controller xunlei_api; untested). |  |
| `xqtunnel/request` | **⚠ INFERRED** — Firmware 1.0.394 function (controller tunnelRequest; untested). |  |
