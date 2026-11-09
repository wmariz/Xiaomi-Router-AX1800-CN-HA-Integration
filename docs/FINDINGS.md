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
