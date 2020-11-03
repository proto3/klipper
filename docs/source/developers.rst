Developers guide
================

Instant reaction implementation
*******************************
Klipper cannot normally move steppers immediately in reaction to an event. The
host has to be informed of the event and then to buffer instructions for
steppers. This generally takes around 250ms with default settings in the code.
However, on thin material, piercing time can be neglected and motion should
start immediately after transfer.

To aim this issue, Klipper plasma introduces a clock shift mechanism. In short,
the host buffers the motion that would immediately follow the event. Then it
sends a plasma_start command that turns plasma on and freeze all time primitives
on the MCU. MCU waits for transfer event or a timeout. When it happens, time
primitives are unfrozen and the MCU sends the time it has spent sleeping for the
host update their respective clock differential.

To be continued...

THC
***

ToDo

JIT input
*********

ToDo

USB watchdog
************

ToDo
