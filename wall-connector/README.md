# Wall Connector Gen 3 load management (ESPHome)

> **EXPERIMENTAL — configurations validated with `esphome config`, not yet flashed or tested on this owner's hardware.**
> Read this page in [Finnish / Suomeksi](README.fi.md).

Local, cloud-free dynamic load management for a Tesla Wall Connector Gen 3 on a Finnish three-phase supply. An ESP32 emulates the Neurio energy meter on the charger's RS-485 bus, so the charger's own Dynamic Power Management keeps the most loaded phase under the main-fuse budget. A Shelly Pro 3EM on the main panel supplies the per-phase currents.

This folder is **separate from the CAN research toolkit** in the rest of the repository. Nothing here transmits on the vehicle's CAN bus.

## How it works

- The charger has no local command for "charge at X A"; its local API is read-only.
- The ESP32 answers the charger's Modbus polls as a Neurio meter and publishes a shaped version of the real mains measurement ([Tesla LoadPilot](https://github.com/zany92/tesla-loadpilot) control law).
- The charger only reacts to whether the published value is above or below its configured Max Conductor Limit, and by how much. LoadPilot maps that limit (21 A) onto the house budget (main fuse × 90 %).
- The charger draws the same current on all three phases, so the most loaded phase sets the charging current. A single-phase heat pump makes this matter.

## Boards

| Board | File | Where | Job |
|---|---|---|---|
| ESP32-S3 | `esphome/loadpilot-twc.yaml` | At the charger's RS-485 terminal | Neurio emulation and control law |
| ESP32-C3 | `esphome/loadpilot-meter.yaml` | Anywhere on Wi-Fi | Reads the Shelly Pro 3EM over HTTP (1 Hz) and sends the six contract values over encrypted UDP |
| ESP32-S3 (optional) | `esphome/tesla-ble.yaml` | In the garage, near the car | Exact charging amps and start/stop through the car over BLE |

The C3 is optional. Without it the S3 reads the Shelly through Home Assistant, but charging is blocked whenever Home Assistant restarts. Bluetooth runs on its own board because the charger node must answer each Modbus poll within about 66 ms.

## Firmware compatibility

- Tesla LoadPilot is validated on Wall Connector firmware **26.18** and **26.26.1**.
- The earlier Klangen82 emulator does **not** work on firmware 26.2 and newer.
- Newer firmware (for example 26.34) is untested: climb the commissioning ladder RAW → OMBRE-MAX → ACTIF-MAX before relying on it.

## Setup summary

1. Copy `esphome/secrets.example.yaml` into your ESPHome `secrets.yaml` and fill it in.
2. In `loadpilot-twc.yaml`, set the main fuse and replace `XXXXXXXXXXXX` with your Shelly's ID. In `loadpilot-meter.yaml`, set the Shelly IP.
3. Flash over USB. Switch the charger node's **Signal Mode** to **RAW** immediately: it boots in active mode.
4. Breaker off, then wire a 3.3 V RS-485 module to the charger: A to red, B to white (details in the YAML header).
5. Tesla One: add the meter (detected as Neurio), set CT1–3 to Conductor, lower Max Output Current to 16 A first, then set Max Conductor Limit to 21 A.
6. Check Polling Active, poll interval about 200 ms and Source Active = UDP, then step up to OMBRE-MAX and ACTIF-MAX during a charge.

## Demo

`demo/kuormanhallinta.html` is a self-contained simulation (Finnish UI) of the behaviour: toggle house loads, change the main fuse, switch load management off. Open it in a browser. Values are examples, not measurements.

## Safety

The RS-485 wiring sits next to 230 V inside the Wall Connector. Work with the breaker off, and leave it to a qualified electrician if you are not one. Do not OTA-flash the charger node during a charge.

## Credits

- [Tesla LoadPilot](https://github.com/zany92/tesla-loadpilot) by zany92 (MIT): control law and charger-node package, used as a remote ESPHome package pinned to `v1.4.0`.
- [PVi1/esphome-twc-control](https://github.com/PVi1/esphome-twc-control): Neurio emulation concept. Register map: gist by LucaTNT.
- [yoziru/esphome-tesla-ble](https://github.com/yoziru/esphome-tesla-ble) (AGPL-3.0): used as a remote package pinned to `v2026.10.4`, not copied here.

Not affiliated with, endorsed by or sponsored by Tesla, Inc.
