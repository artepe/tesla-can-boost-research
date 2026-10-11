# Safety and security

**This is experimental source code, not automotive safety software.**

## Risks

- Some original scripts transmit CAN frames or attempt to change throttle mapping, drive modes and motor-related values.
- Wrong message IDs, counters, checksums or timing may cause unpredictable results in vehicle networks.
- Unsupported hardware and software versions can behave differently.
- A serial connection working does not prove that a CAN write action is safe or effective.

Do not run CAN transmission, torque, pedal, or drive-control experiments on an occupied or road-going vehicle. Limit development to simulated traffic, offline recordings or suitable isolated bench setups with proper protections. This software has not been validated to satisfy functional-safety requirements.

## Reporting

If you find exposed credentials or security flaws, do not include sensitive details in public issues. Contact the repository maintainer privately using their public GitHub profile.
