# Xiaomi Router AX1800

Full local control of **Xiaomi Mi Router AX1800 (RM1800)** routers, including **Mesh** setups (main router + repeater), with no dependency on the cloud or the Chinese app.

The project has two parts, both using the router's own local (LuCI) API:

| Part | Folder | What it is |
|---|---|---|
| Home Assistant integration | `custom_components/miwifi_ax` | Creates one **device** per router with sensors, switches, buttons and presence tracking, plus the **Routers** panel in the sidebar |
| PC panel | `desktop/` | The same interface as the HA panel, running standalone on the PC — handy when HA or the network is in trouble |

There is a single interface (styled after the original, exposing **all** functions — including the ones the firmware hides): `desktop/painel.html`. The HA panel is generated from it by `python tools/build_ha_panel.py`.

**Languages:** the whole project is bilingual — **English** and **Brazilian Portuguese**.
- In Home Assistant, the panel, entity names, device names and messages follow the system language (English by default, Portuguese when HA is set to Portuguese).
- In the PC panel and the Android app, use the **PT · EN** links next to the router selector (initial choice follows the system language, English by default).

## Home Assistant integration

### Installation
1. Copy `custom_components/miwifi_ax` to `/config/custom_components/` (or add this repository to HACS as a *custom repository* of type *Integration*).
2. Restart Home Assistant.
3. **Settings → Devices & services → Add integration → "Xiaomi Router AX1800"**.
4. Enter the IP address and admin password of the main router. Mesh nodes are discovered from the main router's topology and **added automatically** using the main router's password; the role (main/repeater) is detected on its own.
5. In **Configure** (on the main router): choose which devices to track (presence) and the panel address used by the *Visit* button.

### Entities
- **Sensors:** uptime, memory, repeater signal to the main router (wireless backhaul only), clients per band, channels, width, power, firmware, router time and clock offset, devices online/known, devices per connection (wired / 2.4 GHz / 5 GHz / guest — list in the attributes), IP reservations (list in the attributes), MAC filter, blocked intrusions, public IP, IPv6, gateway, DNS, internet connected for, download/upload now, peaks and totals.
- **Binary sensors:** internet, ISP cable, repeater in Mesh, firmware update, Wi-Fi 2.4/5 GHz, unified Wi-Fi, anti-intrusion, firewalls, WPS.
- **Switches:** LED (main and repeater), QoS, guest network, MU-MIMO, Wi-Fi 5 compatibility mode, quick connect, AIoT scan, priority for many devices, MAC filter.
- **Buttons:** restart, refresh data.
- **Zigbee-aware channel search:** sensor *Last channel search* and, in the main router options, a periodic scan (off / 1–30 days, hour, only if worth it) that keeps 2.4 GHz at 20 MHz on the least crowded channel that doesn't overlap the Zigbee channel (read from ZHA). See [`docs/FINDINGS.md`](docs/FINDINGS.md#13-zigbee-aware-24-ghz-channel-search-panel--integration).
- **Tracking:** chosen devices (online/offline, IP, connection, speed).
- **Service** `miwifi_ax.definir_internet` (`mac`, `liberar`): blocks/allows a device's internet access.
- **Service** `miwifi_ax.salvar_log` (`device_id`, optional): saves each router's system-log package to `/config/miwifi_ax_logs` (newest 20 per router). The router's own log only covers the last ~1.5 h, so call it soon after an unexpected restart (e.g. from an automation when the *Uptime* sensor comes back below 1 h). The package contains the Wi-Fi passwords (base64) — keep it private.

By default only *Internet* (main router) and *Restart* (each router) are **enabled**; everything else comes **disabled** — enable only what you use. The integration only queries what some enabled entity needs (less traffic and fewer database writes). The firmware check, which contacts Xiaomi's servers, runs at most every 6 h.

When the admin password changes, HA asks for re-authentication of the main router only; Mesh nodes pick up the main router's new password by themselves.

### "Routers" panel (sidebar)
Visible to administrators. It uses the login already stored by the integration (no password prompt), and works in the HA app and away from home. The device page's **Visit** button opens the panel on the right router (configurable in the options — it can point to the PC panel instead).

## PC panel

```bash
python desktop/painel.py
```

Opens at `http://127.0.0.1:8099` (listens on this computer only). The admin password is typed into the page itself, goes straight to the router (same method as the official interface) and is **not stored**. Router addresses are set with the **⚙ Routers** button (saved in `%APPDATA%\MiWiFiPainel`). Every change asks for confirmation.

Hidden functions exposed: guest network, disconnecting weak-signal devices, AIoT scan, priority for many devices, Wi-Fi region, time zone without daylight saving, per-device internet blocking, and direct calls to every internal function (catalog with descriptions and example calls in [`docs/FUNCTIONS.md`](docs/FUNCTIONS.md)).

## Panel outside Home Assistant

### Windows — `MiWiFiPainel-Setup-<version>.exe`
Installs the local panel (the same as `desktop/`) as a program: Start menu shortcut,
desktop shortcut (optional) and start with Windows (optional, unchecked).
When opened, the panel starts at `http://127.0.0.1:8099` and the browser opens by itself; opening it again
just reopens the page; the **Exit** button shuts it down. The password is typed into the page and is not stored;
router addresses are kept in `%APPDATA%\MiWiFiPainel`.

Build: `powershell -File instalador\windows\build.ps1` (requires `uv` and Inno Setup 6).

### Android — `MiWiFiPainel-<version>.apk`
Standalone app: talks directly to the routers over the home network (no Home
Assistant needed) and shows the same panel. A built-in Java server (`instalador/android/src`)
plays the role of `painel.py`: login with SHA1+nonce hashing, a tolerant HTTP/1.0 client (the repeater
sends malformed headers), confirmation before any change, and masked passwords.

Build: `uv run --with pillow python instalador/android/build_apk.py` — no Gradle, just the
JDK and the Android SDK (build-tools 34, platforms;android-34). The signing key is created in
`instalador/android/assinatura/` (outside git): without it, a new version won't install over the old one.

Ready-made builds are on the [Releases](../../releases) page.

## Technical notes

The full record of findings (API, hidden functions, official app, pitfalls) is in [`docs/FINDINGS.md`](docs/FINDINGS.md).

- Login: `nonce = 0_<deviceId>_<timestamp>_<random>`, password sent as `sha1(nonce + sha1(password + key))`, `POST /cgi-bin/luci/api/xqsystem/login` → `stok`.
- Guest network: `xqnetwork/set_wifi_without_restart` with `wifiIndex=3` and `on=0|1` (applies in seconds without restarting the Wi-Fi).
- LED: `misystem/led?on=0|1`.
- The firmware's "(UTC−3) Brasília" time zone applies the old daylight saving rule; use "(UTC−3) Fortaleza".
- IPv6: in *Native* mode the prefix changes on every reconnection; *NAT6* (`xqnetwork/set_wan6`, `wanType=nat`) gives the LAN a fixed prefix.
- Scheduled restart and guest network setup in the official app go through Xiaomi's cloud.

Features that have **not been tested on a real router yet** are listed in [`docs/FINDINGS.md`](docs/FINDINGS.md#12-test-status).

Tested with firmware 1.0.399 (Chinese version). Unofficial project, not affiliated with Xiaomi. Use at your own risk.
