# Findings on the Xiaomi Mi Router AX1800 (RM1800)

Reverse-engineering notes taken while developing this project.
Firmware tested: **1.0.399** (Chinese version, `countrycode CN`), two units in **wired Mesh**
(main router + node). Everything here was observed on the real device; anything not confirmed is stated as such.

## 1. Accessing the local API (LuCI)

### Login
- `GET http://<ip>/cgi-bin/luci/web` returns the login page, whose JavaScript contains:
  - `key: '…'` — a 32-hex constant (`a2ffa5c9be07488bbb04a3a47d3c5f6a` on this version);
  - `deviceId = '…'` — the **MAC of the requester** (the router injects the client's MAC).
- `nonce = "0_<deviceId>_<unix_ts>_<random 0-9999>"`
- `sent_password = sha1(nonce + sha1(password + key))` (hex)
- `POST /cgi-bin/luci/api/xqsystem/login` with `username=admin`, `password=<sent_password>`, `logtype=2`, `nonce` → `{"code":0,"token":"<stok>"}`.
- Subsequent calls use `/cgi-bin/luci/;stok=<stok>/api/<group>/<function>`.
- Expired session → `{"code":401}`: just log in again.
- **Careful:** requesting `/cgi-bin/luci/;stok=…/web/logout` ends the session (this happened while "downloading every page").
- Changing the admin password (`xqsystem/set_name_password`) still uses AES-CBC (key derived from `sha1(old_password+key)`, fixed IV `64175472480004614961023454661220`).

### Malformed responses
Some endpoints reply with **invalid HTTP headers** — e.g. `misystem/led?on=1` on the Mesh node returns something `aiohttp` rejects
(`Invalid header token`). Tolerant clients (urllib, hand-written HTTP/1.0) work. The integration uses its own HTTP/1.0 client.

### Role in the Mesh
`misystem/sys_time` includes `"role"`: `whc_cap` = **main router**, `whc_re` = **node (repeater)**.
`misystem/topo_graph` shows the tree (main → `leafs`).
On the node, most network functions (device list, MAC filter, guest, QoS…) return empty — the main router holds everything.

## 2. Function map (groups `misystem`, `xqnetwork`, `xqsystem`, `misns`)

The full catalog, with descriptions and example calls, is in [`FUNCTIONS.md`](FUNCTIONS.md).

### Found in the web interface (90)
Extracted from the pages `web/home`, `web/setting/{wifi,wan,lannetset,safe,upgrade}`, `web/apsetting/wifi`, `web/store`, `web/prosetting/qos`.

| Area | Read | Write (parameters) |
|---|---|---|
| Status | `misystem/status` (CPU, memory, device count, WAN traffic, hardware), `misystem/newstatus` (clients per band — ⚠ returns the 2.4 GHz password in the misspelled field `pssswd`), `misystem/devicelist`, `misystem/topo_graph`, `misystem/messages` | `xqsystem/reboot` (`client=web`), `xqsystem/shutdown` |
| Wi-Fi | `xqnetwork/wifi_detail_all` (per band: ssid, password, encryption, channel, bandwidth, txpwr, hidden, status, **ax**, **txbf**, weakenable/weakthreshold/kickthreshold; top level: **bsd**), `xqnetwork/get_miotrelay_switch`, `xqnetwork/get_miscan_switch`, `xqnetwork/get_son_backhaul_mode`, `xqsystem/country_code` | `xqnetwork/set_wifi` (`wifiIndex` 1=2.4 GHz, 2=5 GHz, `on, ssid, pwd, encryption, channel, bandwidth, hidden, txpwr`), `set_all_wifi` (unified Wi-Fi), `set_wifi_ax` (`ax`: 1 = Wi-Fi 6, 0 = Wi-Fi 5 compatibility mode), `set_wifi_txbf` (`txbf` = MU-MIMO), `set_wifi_txpwr`, `miotrelay_switch` (`on`, "畅快连"/quick connect), `miscan_switch` (`on`, AIoT scan), `set_son_backhaul_mode` (`mode`, "多终端接入优先"/priority for many devices), `xqsystem/set_country_code` |
| Internet | `xqnetwork/wan_info`, `pppoe_status`, `wan_link`, `ipv6_status`, `check_wan_type` | `set_wan` (`wanType` pppoe/dhcp/static, `pppoeName, pppoePwd, mtu, service, special, dns1, dns2, autoset`, `staticIp, staticMask, staticGateway`), `pppoe_start`, `pppoe_stop`, `set_wan_speed` (`speed` 0/100/1000), `mac_clone` (`mac`), `set_wan6` (`wanType` off/native/static/nat) |
| Local network | `xqnetwork/lan_info`, `lan_dhcp`, `macbind_info` (reservations + full device list) | `set_lan_ip` (`ip`, restarts), `set_lan_dhcp` (`start, end, leasetime "120m", dns1, dns2, router, ignore`), `mac_bind` (`data=[{"ip","mac","name"}]` as JSON) — with an already reserved MAC it **overwrites** name and IP (tested 2026-11-09), `mac_unbind` (`mac`) |
| Security | `xqnetwork/wifi_macfilter_info` (`model` 0=blacklist/1=whitelist, `enable`, `macfilter`), `misystem/web_access_info` | `set_wifi_macfilter` (`model, enable`), `edit_device` (`mac, model, option` 0=add/1=remove), `misystem/web_access_opt` (`open`, `opt`, `mac`), `xqsystem/set_mac_filter` (`mac, wan` 0/1 — **blocks a device's internet access**) |
| QoS | `misystem/qos_info` | `qos_switch` (`on`), `qos_mode` (`mode`), `set_band` (`manual, upload, download` Mbps), `qos_guest` / `qos_xq` (`percent, percent_up`), `qos_limits` (`data` JSON), `qos_offlimit` (`mac`) |
| System | `misystem/sys_time` (`time`, `timezone`, **`index`**, `role`), `misystem/router_name`, `xqsystem/get_languages`, `xqsystem/check_rom_update`, `misystem/sys_log` (generates the log and returns its path) | `misystem/set_sys_time` (`timezone, index` **or** `time "YYYY-MM-DD hh:mm:ss"`), `set_router_name` (`name, locale`), `xqsystem/set_language`, `misystem/c_backup` (`keys`), `c_restore`, `xqsystem/reset` (`format`), `upload_rom`, `upload_plug` |

### Found only in the official app (112 extra names in the APK code)
Read-tested on firmware 1.0.399 — the ones that **exist and respond**:

| Function | Notes |
|---|---|
| `misystem/led` | `{"status":1}`; **`?on=0` turns off, `?on=1` turns on** the device LEDs |
| `misystem/arn_status`, `arn_records`, `arn_security` | anti-intrusion ("防蹭网"): on/off, level, **block counter**; website/virus firewalls |
| `misystem/router_common_status` | summary (devices, WAN speed, USB) |
| `misystem/qos_info_new`, `channel_scan_result`, `smartvpn_info`, `vas_info`, `check_status`, `repair_status` | |
| `xqsystem/system_info`, `vpn`, `vpn_status`, `wps_status`, `push_settings`, `privacy`, `init_info` (no login needed), `device_mac` | |
| `xqnetwork/mode` | network mode |
| `xqsmarthome/request_smartcontroller` | "scenes"/schedules engine (commands `get_multiple_scene_setting`, `get_single_scene_setting`; the parameter format **was not discovered** — the app only uses it through the cloud) |

Reply "wrong parameter" without arguments: `ecos_info`, `netacctl_status`, `parctl_info` (parental control), `get_dev_bsd`.

### Functions hidden by the interface itself
- **Guest network:** the "访客Wi-Fi" block is **commented out** in `web/setting/wifi`. Read: `misns/wifi_share_info` (`info.guest` 1/0, `info.data.{ssid,password,encryption}`).
  Write as suggested by the commented-out code (**does not work** — tested 2026-11-08): `xqnetwork/set_wifi` with **`wifiIndex=3`**, `on, ssid, pwd, encryption` (the SSID cannot equal the 2.4 GHz one).
  - ✓ **Works:** `xqnetwork/set_wifi_without_restart` with **only** `wifiIndex=3` and `on=1/0` (GET). Applies in ~1–5 s, **without restarting the Wi-Fi**, keeping name and password. Sending `ssid`/`pwd` along returns `code 1615` ("访客WiFi设置失败，请检查无线名称和密码" — guest Wi-Fi setup failed, check the name and password). Used by the integration's "Guest network" switch (method found in JuanManuelRomeroGarcia/hass-miwifi).
  - ✗ `xqnetwork/set_wifi` with `wifiIndex=3`: replies `code 0` but changes nothing.
  - ✗ `xqnetwork/set_all_wifi` with `on3, ssid3, encryption3, pwd3…` (documented in RACErace/MiWiFi-API for other models): `code 0`, ignored on the RM1800, and restarts the Wi-Fi (~30 s).
  - `misns/wifi_share_switch` exists locally, but its parameters were not discovered (`code 1523` on every attempt). The app uses the cloud version `/s/sns/wifi_share_switch` (encrypted body).
  - The guest network interface is `wl14` and only shows up in `xqnetwork/wifi_diag_detail_all` (`status` 0/1, `iftype 3`) — not in `wifi_detail_all`. It only exists on the main router; the Mesh node does not broadcast the guest network — not even after being restarted with it on (scan 2026-11-08).
  - Time on air (PC Wi-Fi scan, 2026-11-08): **turning off** — beacons stop within ≤ 10 s (Windows keeps listing the network for minutes from cache; the AP `Uptime` freezes); **turning on** — the network appears ~32–34 s after the command.
- **Hidden SSID without restart:** `xqnetwork/set_wifi_without_restart` with `wifiIndex=1` (or 2) and only `hidden=1` hides the network while keeping name, password, channel and power. **It is not mirrored to the Mesh node** — it must be applied to the repeater too. On the main router it takes effect immediately; on the repeater the option is saved but the radio only starts hiding after the node restarts (PC Wi-Fi scan, 2026-11-08). No known function yet forces a Mesh sync without restarting.
- **Weak-signal disconnection:** hidden forms `roamset24/roamset50` → `set_wifi` with `wifiIndex, weakenable, weakthreshold, kickthreshold`.
- **AIoT** and **priority for many devices** are also commented out on the page.

### Device list
`misystem/devicelist` → `list[]` with `mac, name, oname, ip[{ip, online(s), downspeed, upspeed}], online, isap (8 = Mesh node), parent, authority{wan,…}`, and **`type`**: `0` wired, `1` Wi-Fi 2.4 GHz, `2` Wi-Fi 5 GHz, `3` guest (Xiaomi convention; 3 not yet observed).
With wired Mesh, devices plugged into the node's ports show up as "wired" **without `parent`**; those on the node's Wi-Fi have `parent` = the node's MAC.

## 3. Pitfalls

- **The "(UTC−3) Brasília" time zone applies the old daylight saving rule** (+1 h in November). All UTC−3 options send `timezone=CST+3`, but the router also stores the option's **`index`**. Use **"(UTC−3) Cayenne, Fortaleza"** (`index` 3).
- In the Mesh, the time zone can only be changed on the **main router** and is passed on to the node. Saving the time zone again on the main router forced the node to fix a clock that was **11 h ahead** (no NTP).
- The app's **scheduled restart** applies to the whole Mesh; with the node's clock wrong, it restarted at another time (e.g. the node's "06:00" = 19:00 local), taking down everything connected to it.
- The Chinese app (stable **5.6.7** and developer **5.7.7** — the website advertises 5.6.5/5.7.5) **only ships `armeabi-v7a`** (32-bit): it won't install on newer phones without 32-bit support. It runs on an Android 11 x86 emulator (which translates 32-bit ARM).
- The app talks to the cloud (`api.miwifi.com`): `/r/api/<group>/<function>` relays **the same local functions** to the router, with encrypted parameters and responses (RC4 with the account session). Guest network and schedules in the app also use `/s/guest_wifi/…` and `xqsmarthome/request_smartcontroller`.
- Antivirus software with HTTPS inspection (e.g. Avast) breaks the app's login and Java/Python tools that don't use the Windows certificate store.
- The router is limited (4× Cortex-A53 716 MHz, 256 MB, ~50–60 % memory used at idle). It became visibly unstable with many extra devices connected.

- **Changing the admin password (tested 2026-11-08):**
  - an already open session (`stok`) **remains valid** after the change: the integration keeps working until it needs a new login (HA restart, integration reload);
  - then logging in with the old password returns `code 401` → HA opens "Re-authenticate";
  - the **Mesh copies the new password to the repeater** (it also starts returning 401) → the re-authentication screen offers "use the main router's password";
  - in the integration: the Mesh node stores `usar_senha_principal`; if the saved password is refused, it **tries the main router's current password by itself** and saves it (no prompt). When the main router is re-authenticated, nodes in setup error are reloaded and pick up the new password;
  - **adding nodes:** a node found in the main router's topology is **added automatically** with the main router's password; the "discovered" card (asking for the password) only appears if that fails. A node deleted by the user is kept in `nos_removidos` on the main entry and from then on only shows up as a card (confirming doesn't ask for a password); re-adding it removes it from the list. Tested 2026-11-08: automatic re-adding kept the 11 entities, areas and enablements;
  - two logins in almost the same second (re-authentication validation and the reload right after) give **`code 1582`**: not a wrong password; the integration waits 2 s and retries (up to 4 times).

- **IPv6 in Native mode changes the network prefix on every reconnection** (Vivo PPPoE, 2026-11-08): restarting the router or changing the WAN MAC produced new prefixes (`…:1ec5::` → `…:2cfb::` → `…:13::`). Devices (including Home Assistant) **keep the old addresses** alongside the new ones, which broke Matter pairing with Google until the HA host was rebooted.
  - Adopted solution (2026-11-09): **NAT6** — `xqnetwork/set_wan6` (POST) with `wanType=nat`, `autosetipv6=1`, `dns1`, `dns2`. The LAN then uses the fixed prefix **`fd00:6868:6868::/64`** (the router does NAT66 to the internet), which doesn't change with the ISP. After the switch, one reboot of the HA host cleared the old addresses for good.

## 4. Network diagnostics used
- `xqsystem/init_info` replies **without login** — useful as a "ping" of the web service.
- Each unit's uptime (`misystem/status.upTime`) reveals restarts.
- `xqnetwork/wan_info.uptime` resets on every PPPoE reconnection.

## 5. Official app: stable × developer
Comparison of the APKs `xqapp.apk` (stable, 5.6.7) and `xqapp_dev.apk` (developer, 5.7.7) downloaded from miwifi.com:
- same files and resources; only `AndroidManifest.xml` (version number), the signature and `classes.dex`/`classes2.dex` (24 bytes of difference) change;
- **no new function, endpoint or text** — the 252 API references and all readable strings are identical.

Conclusion: the developer version brings no extra features for this router.

## 6. Integration icon in Home Assistant
HA 2026.x serves custom integration icons from `custom_components/<domain>/brand/`
(`icon.png` 256×256, `icon@2x.png` 512×512, `logo.png`/`logo@2x.png`) through the authenticated route
`/api/brands/integration/<domain>/icon.png`. The folder is only read at startup — HA must be restarted.

## 7. International app (Mi Wi-Fi 5.9.0, APKMirror) × Chinese (5.6.7)
- The international one is **64-bit** (arm64-v8a + armeabi-v7a) and uses the **same package** `com.xiaomi.router` — so one won't install over the other.
- Same 94 cloud routes; only 5 extra local functions (`mesh/adapter`, `misystem/get_usb_u2`, `misystem/usb_u2`, `misystem/set_router_wifiap_init`, `xqnetdetect/nettb2`), **none of which exist** on the AX1800 firmware — they belong to tri-band/USB models.
- Conclusion: it brings no new functions for this router.

## 8. What the Mesh node (repeater) has of its own
Comparing the main router's and the node's responses:
- **Mirror of the main router:** Wi-Fi configuration (channel, width, power, names, state) and notices — identical on both.
- **Specific to each unit:** uptime, CPU, memory, **connected clients per band** (e.g. main 10, node 4), firmware, clock (which can diverge — the node's once ran 11 h ahead), LED and restart.
The integration only creates the node-specific entities on the node.

## 9. Advanced pages (DDNS, port forwarding/DMZ, VPN, UPnP)
The pages `web/prosetting/{ddns,nat,vpn,upnp}` are only linked from the QoS page. Endpoints and parameters (all in [`FUNCTIONS.md`](FUNCTIONS.md)):
- **DDNS:** `xqnetwork/ddns` (list), `add_server` / `ddns_edit` (GET: `id` provider 1 No-IP · 2 Oray · 3 3322.org · 4 Dyn, `username, password, domain, checkinterval` min, `forceinterval` h, `enable`), `get_server`, `del_server`, `server_switch` (`id, on`; only one active), `ddns_reload`, plus the global `ddns_switch`.
- **Port forwarding:** `xqnetwork/portforward?ftype=1|2`; `add_redirect` (POST `name, proto` 1 TCP/2 UDP/3 both, `sport, ip, dport`; `force=1` replaces the rule for that external port), `add_range_redirect` (`fport, tport`), `delete_redirect` (`port, proto`). Rules only take effect after `redirect_apply`.
- **DMZ:** `xqnetwork/dmz` (`status` 1 = on), `set_dmz` (POST `ip`), `dmz_off` + `dmz_reload`.
- **VPN (PPTP/L2TP client):** `xqsystem/vpn`, `vpn_status` (0 connected … 4 not enabled), `set_vpn` (POST, empty `id` = new), `del_vpn`, `vpn_switch` (`conn` 1/0, `id`), `set_vpnauto`; smart split `misystem/smartvpn_info|smartvpn_switch|smartvpn_url|smartvpn_mac` (`opt` 0 add / 1 remove); `mi_vpn` / `mi_vpn_info`.
- **UPnP ("other"):** `xqsystem/upnp`, `upnp_switch` (`switch` 1/0).
- These pages also reference `xqnetwork/scan_mesh_node`, `get_addnode_status`, `add_mesh_node` (adding Mesh nodes from the web UI) — not explored yet.

## 10. Remaining official features (tested 2026-11-09)
- **Wi-Fi power without restart:** `xqnetwork/set_wifi_txpwr?txpwr=max|mid|min` changes **both bands at once** in ~5 s; the radios stay up (`wifi_diag_detail_all` status 1 throughout). The firmware still has the JS for it but the form was removed from the page.
- **Backup restore:** `misystem/c_upload` is a multipart POST with the file in the field `image`; it only parses the file and returns `des.keys` (e.g. `mi_basic_info`, `mi_network_info`, `mi_wifi_info`, `mi_lan_info`, with Chinese labels). Nothing changes until `misystem/c_restore?keys=a,b` — and that needs a restart. Upload tested with a fresh backup (no restore).
- **Adding a Mesh node:** `scan_mesh_node` → `add_mesh_node` (POST `mac`, `locate` = Chinese room name) → poll `get_addnode_status?mac=` (0 done, 1 connecting, 2 syncing, 3 expanding, 4 failed). Not exercised (no spare node).
- **Diagnostics:** `xqnetdetect/nettb` (`error` 0 = ok, ~1.5 s); `xqnetwork/check_wan_type` (1 PPPoE, 2 DHCP, 3 static, 99 no cable; returns 0 while PPPoE is connected).
- **Notices:** `misystem/messages` returns `messages[]` (not `list`): type 1 new firmware, 3 5 GHz failed, 4 IP conflict with `data.ip`, fixed by `misystem/r_ip_conflict` (POST).
- **QoS:** per-device limits `misystem/qos_limits` (KB/s, 0 = none; list only has devices while QoS is on); the router's own limit is `qos_xq`, read back as `qos_info.local`.
- Slow endpoints (scans, diagnosis, uploads) get a 60 s timeout in the integration and both standalone servers.

## 11. App-only features and the full firmware API (2026-11-09)
Parameters taken from the decompiled LuCI controllers of this exact firmware family (RM1800 1.0.394) published in
[dmamontov/miwifi-luci-api](https://github.com/dmamontov/miwifi-luci-api), then checked on the device. The firmware has **448 API
functions**; all of them are now in the catalog ([`FUNCTIONS.md`](FUNCTIONS.md)) — untested ones are marked as inferred.
- **Wi-Fi optimization:** `misystem/channel_scan_start` (analysis only, 2.4 GHz) → after ~10 s `channel_scan_result` →
  `2G{cchannel, cscore, schannel, sscore, ranking}` (interference score: lower is better; here channel 3 = 49, suggested 2 = 16).
  `misystem/set_channel?channel1=&channel2=` applies **and saves** the channel in ~5 s with the radios up (tested; put back to 3).
- **Full diagnostics:** `misystem/net_diagnose_start` → `net_diagnose_result` (`status` 1 = ok after ~5 s; 2 = problem with `wan`
  down/up and `diagnose` 111 DHCP, 112 IP, 113 gateway, 114 ISP, 678 PPPoE server, 633 port busy, 101 PPPoE, 691 PPPoE auth, 100 DNS).
  There is **no network repair** endpoint: `repair_status`/`check_status` are about USB disks. `xqnetdetect/detect` (the app's
  "health check") returned error 500 with `simple=1`.
- **Security check:** `start_portscan` / `get_portscan_result` (`tcp_port`, `udp_port`) and `start_weakdetect` /
  `get_weakdetect_result` (FTP/SSH/Telnet), both with `ip` + `mac` of a LAN device (tested on the HA host: ports 22 80, no weak passwords).
- **Anti-intrusion:** `arn_status` (`open`, `level`, `count`, `wifimode` 1 = MAC filter in block-list model, `wifilevel`/`adminlevel`
  = password strength). `arn_switch` `open` 0/1 **also enables/disables the Wi-Fi MAC filter** (`mode` = filter model to keep);
  `level` alone only changes the level. `arn_records` returned error 500.
- **Security center:** `arn_security` + `arn_security_switch` (POST `info` = JSON `{malicious_url_firewall, virus_file_firewall,
  privacy_protection}`; including `wifi_arn` touches the MAC filter). Tested on/off.
- **Parental control:** `parctl_add` (`mac, enable, frequency "1,2,3,4,5", timeseg "22:00-07:00"` → `id`), `parctl_update`,
  `parctl_delete`, `parctl_info`; site filter `parctl_set_filter` (`mode` none/black/white), `parctl_get_url`,
  `parctl_set_url` (`opt` 0 add / 1 remove). All tested with a dummy MAC and removed.
- **WPS:** `xqsystem/wps`, `wps_cancel`, `wps_status` (0 idle, 1 waiting, 2 connected + `device{mac, company}`, 3–7 failed).
- **Automatic firmware update:** `misystem/ota` / `set_ota` (`auto`, `time` hour, `plugin`).
- **Per-device band (unified Wi-Fi only):** `get_dev_bsd` / `set_dev_bsd` (`mac`, `mode`; restarts the Wi-Fi).
- Not found in the web UI nor tested yet, but present: hardware NAT (`hwnat_status/switch`), Wi-Fi log (`xqsystem/wifi_log`),
  Mesh link metrics (`get_mesh_metric`), traffic history (`device(s)_statistics`, `wan_statistics`), device rename
  (`set_device_nickname`), radios/WAN up/down, router-side ping, and an SSH server (`xqsystem/start_dropbear`).

## 12. Test status

### Tested on the device
| Feature | Result |
|---|---|
| Guest network on/off, hidden SSID, NAT6, quick Wi-Fi power, channel optimization, diagnostics (`nettb`, `net_diagnose`), connection-type detection, open-port / weak-password check, security center, IP reservation edit, backup upload | Work (2026-11-09) |
| Rename a device (`set_device_nickname`) | Works (renamed and restored) |
| Router's own QoS limit (`qos_xq`) | Works, even with QoS off (`qos_info.local` follows) |
| Anti-intrusion level (`arn_switch level`) | Works; level alone does not touch the MAC filter |
| Automatic update settings (`set_ota`) | Works |
| DDNS add / get / edit / enable / disable / delete | Works (dummy No-IP service, removed) |
| VPN add / edit / delete | Works **only if `id` is omitted when adding** — any `id`, even empty, is treated as an edit (code 1583). Editing **changes the id** (it is derived from the contents). Not connected. |
| DMZ | **Refused while any port-forwarding rule exists** (code 1610, "port forwarding is on"). |
| Port and range forwarding + apply | Work; `redirect_apply` takes ~4 s. `add_redirect` **ignores `force`** on this firmware: editing = delete + add (code 1608 otherwise). |
| UPnP off/on | Works |
| WPS start / cancel | Works (status 1 while open, 3 after cancel) |
| Radios off/on (`wifi_down` / `wifi_up`) | Work: 5 GHz clients dropped and returned ~20 s after `wifi_up`. The router **never reports** the radio as off (`status` stays 1 everywhere). |
| Per-device QoS limit (`qos_limits` / `qos_offlimit`) | Works with QoS on (1000/300 KB/s set and removed) |
| Parental control on a real device | Works: during the schedule the device **loses web access** (HTTP blocked; ICMP ping still passes) — the schedule is the period WITHOUT internet. |
| WAN down/up (`wan_down`) | The router **reconnects by itself in ~9 s**; `wan_down` is effectively "force a PPPoE redial". |
| Scheduled off/on (`smart_shutdown`, delays in minutes per XQFunction) | **No effect on this model** (tested on the repeater: never shut down, uptime kept counting) — the hibernation tool `uhbn` is probably absent. |
| Backup → upload → **restore** (all 4 items) → reboot | Works (2026-11-10). A detailed before/after comparison of 27 config groups (Wi-Fi incl. password hashes, guest, LAN/DHCP, 15 reservations, PPPoE, NAT6, MAC filter, QoS, security, DDNS, UPnP, port forwards, LED, OTA, Mesh topology…) showed **no differences**. `c_restore` answers `{ip}`; the router is back in ~1 min. |
| Remove / reboot a Mesh node (`misystem/set_mesh_device`, `mesh_mac` + `op` 1 delete / 2 reboot) | **No effect** (answers code 0; the `whc_ual` tool it calls appears to be missing, like `whcal`). Tried with both node MACs. |
| Factory reset of the **wired** Mesh node (`xqsystem/reset format=0` on the node) → re-join | The node comes back as a plain router (`Xiaomi_XXXX_XXXX`, `inited 1`, `bound 0`) and `scan_mesh_node` on the main router stays **empty**. After a **power cycle**, the node **re-joined the Mesh by itself over the cable** (wired auto-onboarding) — `add_mesh_node` was not needed. It came back with the Wi-Fi config (incl. hidden SSID) and LED as before, but with the default name/location, time-zone `index 0` (clock 11 h off) and plug-in auto-update on. Fix: `set_router_name` on the node, `set_ota` on the node and re-save the time zone **on the main router** (it propagates and corrects the node's clock). The HA integration recovered on its own (same IP via the DHCP reservation; the Mesh copies the admin password). ⚠ Devices cabled through the node lose the home network while it is reset. |
| Guest network *Save* with name/password (panel) | Works — tested by the user on 2026-11-10. |
| Unified Wi-Fi on/off (`set_all_wifi bsd`) | Works — tested by the user on 2026-11-10. When on, both bands take the 2.4 GHz name, password **and hidden flag**; the panel then shows a single Wi-Fi form (shared name/hidden/security/password + per-band channel, width and power), like the original page. |
| Wi-Fi changes and the Mesh node | A full save (`set_wifi` / `set_all_wifi`) on the main router **is copied to the repeater** (names, hidden flag, channel, width — checked 2026-11-10). `set_wifi_without_restart` is **not** copied, and it also **ignores `ssid`** (only `hidden`/`on`/power-type fields change). |
| Zigbee-aware channel search → apply (user, 2026-11-10) | Works: suggested channel 1 applied with a full save; both routers ended on channel 1 at 20 MHz (config and on air). |
| Hardware NAT (`hwnat_switch on=1`) | Accepted and the router **restarts**, but `hwnat_status` stays 0 afterwards. The RM1800 is Qualcomm-based; Xiaomi's `hwnat` switch appears not to apply. |

### Not yet tested
| Feature | Why |
|---|---|
| Adding a Mesh node over Wi-Fi (`scan_mesh_node` → `add_mesh_node`) | No spare node; a factory-reset **wired** node re-joins by itself after a power cycle (see above). |
| Per-device band | Possible now that unified Wi-Fi was tested; `mode` 1/2 inferred; saving restarts the Wi-Fi. |
| Work-mode switch | Blocked on a Mesh main router. |
| Static IPv6 | The ISP provides no static prefix. |
| IP-conflict fix | No conflict on the test network. |
| Zigbee-aware channel: periodic automatic switch | The search and the manual apply are tested; the first automatic run is scheduled. |
| Functions marked **⚠ INFERRED** in [`FUNCTIONS.md`](FUNCTIONS.md) | 250+ functions found only in the decompiled firmware. |

### Present in the firmware but not working on this model
`xqsystem/wifi_log` (returns no data), `misystem/get_mesh_metric` (code 127: the `whcal` tool is missing),
`misystem/get_mesh_device_info` and `xqsystem/app_limit` (error 500), `xqsystem/start_dropbear` (SSH; script absent), `xqsystem/smart_shutdown` (no effect), `misystem/hwnat_switch` (status stays 0).
`xqnetdetect/sys_status` returns status 2 ("no WAN link") even with the internet working.

## 13. Zigbee-aware 2.4 GHz channel search (panel + integration)
Xiaomi's optimization (`channel_scan_*`) returns a single suggestion and ignores Zigbee, which shares the 2.4 GHz band.
On the test network it suggested channel 7, right on top of Zigbee channel 20. The firmware has no way to restrict
the channels used by "automatic" (`avaliable_channels` is a fixed list 1–13 × 20/40 MHz) and no user-defined scheduler,
so this is done by the panel/integration:
- **Scan:** `xqnetwork/wifi_list` (~12–15 s; per network: ssid, bssid, band, channel, signal %, rssi — no width).
  In automatic mode each Mesh node picks its own 2.4 GHz channel (main on 11 and node on 1 at the same time).
- **Score per channel 1–11:** Σ neighbour `signal` × overlap, overlap = 1 − |Δchannel|/4 (20 MHz channels overlap
  up to 3 channels apart); own networks (main/node/guest SSIDs) are ignored; normalized to 0–100 (100 = worst).
- **Zigbee:** a 20 MHz Wi-Fi channel is blocked when its centre is less than 12 MHz from the Zigbee channel centre
  (Wi-Fi ±10 + Zigbee ±1 + 1 MHz guard). Zigbee 20 → Wi-Fi 7–10 blocked. In HA the Zigbee channel is read from the
  running ZHA (`get_zha_data(...).application_controller.state.network_info.channel`) or, as a fallback, from the latest
  backup in `zigbee.db` (`network_backups_vNN.backup_json → $.network_info.channel`). Width is always set to 20 MHz.
- **"Worth it":** the current channel overlaps Zigbee (main or node), the band isn't fixed at 20 MHz, the channel is
  outside 1–11, or the suggestion has ≥ 30 % less interference.
- **Apply:** unified Wi-Fi → `set_all_wifi`; already fixed at 20 MHz → `misystem/set_channel` on the main router and on
  the node (~5 s, Wi-Fi stays up); otherwise a full `set_wifi` save (Wi-Fi restarts ~30 s; copied to the node).
- **Where:** manual search + apply in every panel (computed in the browser on PC/Android; by the integration in HA).
  Periodic search (HA only, integration options or the panel): off / 1 / 3 / 7 / 15 / 30 days, at a chosen hour,
  optionally only when worth it — it applies **without confirmation**, fires `miwifi_ax_canal_trocado` and creates a
  persistent notification. Sensor **Last channel search** (`sensor.*_ultima_busca_de_canal`) holds the full result.
  The Python (`custom_components/miwifi_ax/canal.py`) and JavaScript (`desktop/painel.html`) versions of the algorithm
  are kept identical (checked on the same scan, 2026-11-10).

## 14. Firmware teardown (ROM 1.0.399, 2026-11-10)

Extracted the stock image `miwifi_rm1800_firmware_..._1.0.399.bin` (HDR1 → UBI → SquashFS, standard xz) to confirm
why some functions have no effect on this model and to see the layer below the LuCI API.

- **SoC / platform:** Qualcomm IPQ (ARM 32-bit LE; `qca-hostapd`, `qca-nss-drv`, `qca-ssdk`, `ecm.ko`), Linux 4.4,
  U-Boot 1.0.1, `CHANNEL=release`. Not MediaTek.
- **The LuCI API controllers (`/usr/lib/lua/luci/controller/api/*.lua`) are obfuscated Lua bytecode** (`\x1bFate/Z\x1b`),
  not plain Lua — hence they must be decompiled. Namespaces match §11: `xqnetwork, xqsystem, misystem, xqdatacenter,
  xqnetdetect, xqpassport, xqsmarthome, xqtunnel, miats, misns, cportal`.
- **SSH is blocked by design on release firmware.** `/etc/init.d/dropbear` `start_service()` returns early unless
  `nvram get ssh_en = 1` **and** the version channel is not `release`. The binary, config (port 22, root auth) and
  boot symlink are all present, but the guard means dropbear never starts here. There is no working SSH endpoint;
  enabling it needs the channel changed (flash/exploit), not an API call.
- **Telnet:** `S50telnet` is enabled and `/etc/init.d/telnet`'s safety guard is commented out, so `telnetd` (busybox)
  does listen on port 23 — but login still needs a root password in `/etc/shadow`, unless `/proc/xiaoqiang/ft_mode`
  (factory-test mode) is set, which gives a passwordless shell. Not an open door on a retail unit.
- **hwnat has no init script** (`/etc/init.d/hwnat` is referenced by `miqos` but not shipped). Offload is Qualcomm
  NSS/ECM via `/proc/xqfp/open_fastpath_v3`, owned by QoS: enabling QoS writes `0` (offload off), disabling writes `1`.
  So a `hwnat` toggle can't hold state against QoS — matches "reboots, status stays 0".
- **Mesh `whcal` is not installed** (mesh here is Qualcomm SON: `repacd`, `lbd`, `meshd`, `cab_meshd`), so
  whcal-based metric/device calls have nothing to call.
- **Embedded web UI is only the first-boot setup wizard** (~31 endpoints); the full console (all functions in §11) is
  loaded remotely, not from the device. Setup calls go through `l(url, params)` (GET) / `f(url, params)` (POST).
  The unified Wi-Fi save `set_all_wifi` uses `ssid1/pwd1/encryption1/channel1/bandwidth1` (2.4 GHz) + the same with
  suffix `2` (5 GHz) + `bsd` (band steering, 0|1) + `hidden`; encryption values `WPA2PSK` / `mixed-psk`.
- **`datacenter` daemon** (decompiled with Ghidra 12.1.4): not the traffic engine (`trafficd` is), but the C++ daemon
  for USB storage/hotplug, the plugin system, MAC-filter lookups and a local DB. `APIMapping::redirectRequest` parses
  a JSON body, reads a **numeric command id**, and dispatches through a `std::map<int, handler>` — so `xqdatacenter`
  names map to numeric ids inside the daemon. Nothing here changes the Wi-Fi/network API the integration uses.
