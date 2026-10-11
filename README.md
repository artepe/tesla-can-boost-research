# Tesla Model 3 CAN Research Toolkit

> **WORK IN PROGRESS / EXPERIMENTAL / NOT PRODUCTION READY**  
> **KESKENERÄINEN TUTKIMUSPROJEKTI — EI VALMIS KÄYTTÖÖN**

Community research toolkit for inspecting, recording and analyzing Tesla Model 3 / Model Y CAN data. This repository is a **documented research snapshot based on the work of ColinM-sys**; it is **not a confirmed Acceleration Boost unlock** and **not an official Tesla product**.

**Original project:** [ColinM-sys/tesla-can-boost](https://github.com/ColinM-sys/tesla-can-boost)  
**Original author:** Colin McDonough (GitHub: [@ColinM-sys](https://github.com/ColinM-sys))  
**This research packaging / documentation:** [@artepe](https://github.com/artepe)  
**Project status:** Experimental; hardware compatibility and behavior require independent verification.

Read this page in [Finnish / Suomeksi](README.fi.md).

## What is included?

- Passive CAN recording, frame decoding, analysis and port discovery utilities (`tools/`).
- Data-visualization prototypes, including HTML dashboards (`tools/`).
- A community-maintained Tesla DBC signal file (`dbc/Model3CAN.dbc`).
- **Unverified, high-risk CAN transmission experiments inherited from upstream.** These files remain for source inspection and research context, *not* as ready-to-use driving features.

The original Python source files are unchanged from the supplied upstream archive. This packaging adds or revises documentation, credits and dependency manifests. The original upstream README is archived at [`docs/UPSTREAM_README.md`](docs/UPSTREAM_README.md); its claims should **not** be treated as independent verification.

## What is NOT established

- Changing a pedal/drive-mode CAN value does **not** demonstrate unlocking Tesla's official Acceleration Boost feature or additional licensed motor power.
- The included experiments do **not** establish compatibility with a 2019 Model 3 Long Range AWD.
- Support for S3XY Commander / ESP32, macOS or Raspberry Pi has **not** been verified for this snapshot.
- Claims of successful vehicle commands appearing in upstream documentation have **not** been reproduced by the maintainer of this packaging.
- No vehicle-level functional or safety testing has been completed as part of this packaging.

## Safe initial exploration (offline or passive only)

Python 3.10+ is recommended. The scripts primarily target an OBDLink/ELM-compatible serial interface, with platform-specific port configuration present in some scripts.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python tools/scan_ports.py
```

You can read the source and use offline log analysis without connecting to a vehicle. **Do not run any script that transmits CAN frames or changes vehicle controls on a live vehicle.** No CAN write/injection instructions are supplied here.

For an example offline capture format, see the original research code and `tools/can_decode.py`; data formats vary across individual tools and are not yet normalized.

## Structure

```text
├── README.md / README.fi.md       # Project status and basic information
├── ATTRIBUTION.md                 # Sources, credits, licensing notes
├── ROADMAP.md                     # Proposed work, not completed features
├── SECURITY.md                    # Safety and reporting
├── requirements.txt              # Core Python dependency
├── requirements-optional.txt     # Optional experiment UI dependency
├── LICENSE                       # ColinM-sys's original CC BY-NC 4.0 notice
├── dbc/
│   ├── Model3CAN.dbc             # Third-party community CAN database
│   └── LICENSE                   # MIT notice for the DBC source
├── docs/UPSTREAM_README.md        # Original, unverified upstream notes
└── tools/                       # Research and experiment scripts
```

## Roadmap and contributions

See [`ROADMAP.md`](ROADMAP.md). Contributions documenting **passive capture**, repeatable validation, parsing and visualization are welcome. Please do not represent untested drive-control or torque-injection scripts as confirmed features.

## Attribution and licensing

The original work is credited to **Colin McDonough / ColinM-sys**. The inherited project LICENSE is **Creative Commons Attribution–NonCommercial 4.0 (CC BY-NC 4.0)**. The DBC originates from **Josh Wardell's model3dbc**, which has its own **MIT** license (copied to `dbc/LICENSE`). See [`ATTRIBUTION.md`](ATTRIBUTION.md). The original README's "MIT" line conflicts with the project's top-level LICENSE; the latter has been retained, not replaced.

## Safety disclaimer

CAN bus injection and electronic throttle/drive controls can affect acceleration, braking-related behavior or other safety-critical systems. Unexpected behavior, vehicle damage, warranty implications and legal consequences are possible. **Never test active vehicle-control scripts on public roads.** This repository provides no proof of safety or suitability for installation in a road vehicle. Research should be restricted to appropriate isolated laboratory setups. See [`SECURITY.md`](SECURITY.md).

**Tesla and Model 3 / Model Y are trademarks of their respective owner. This is an independent community effort, unaffiliated with Tesla.**
