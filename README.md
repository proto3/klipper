This is a Klipper fork dedicated to plasma CNC machine, work is still in progress and any help is welcome !

**IMPORTANT : This is not a stable version, it looks functional but still, many safety features are missing and plasma could stayed fired with unintended consequences. If you plan to give it a try, please don't do it on the real machine.**

It adds :
- Software THC (Torch Height Control) with realtime display of voltage and Z position for easy PID tuning. I plan to implement speed based THC to prevent torch diving on corners.
- Immediate stepper reaction to trigger motions from external events (like plasma ignition). Klipper all-buffered architecture wouldn't normally allow for immediate reaction.

[![Klipper](docs/img/klipper-logo-small.png)](https://www.klipper3d.org/)

https://www.klipper3d.org/
