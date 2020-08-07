[![Documentation Status](https://readthedocs.org/projects/klipper-plasma/badge/?version=latest)](https://klipper-plasma.readthedocs.io/en/latest/?badge=latest)

# Klipper for Plasma

This is a Klipper fork dedicated to plasma CNC machines, work is still in progress and any help is welcome !

**IMPORTANT : This is not a stable release. It is currently in use on a real machine and performs fine, but there are still many input protections missing. A non experienced user can send invalid gcode sequence leading to unattended consequences.**

You can read [documentation here](https://klipper-plasma.readthedocs.io), or have a look at [Sheetah](https://github.com/proto3/Sheetah), a plasma CAM software designed to work in pair with Klipper and enabling THC graphical monitoring.

## Features
- Everything from the original Klipper. This version will kept rebased on official as long as possible to benefits from updates and bugfixes.
- Integrated THC (Torch Height Control).
- THC real-time monitoring.
- THC anti-dive, z axis pauses under a specified feedrate.
- Instant stepper reactivity, required for precise piercing delays but not possible with original Klipper implementation.
- Various plasma related safety improvements (PC independant emergency stop, input commands timeout during cuts, serial link loss detection)
