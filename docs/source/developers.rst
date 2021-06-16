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

THC stands Torch Height Control. To achieve optimal cutting with plasma, it is important to keep the torch tip-to-plate distance constant at about 0.06" (1.5mm).
The voltage and the distance between torch tip and plate / cutting material being directly proportional, THC is a feedback loop controlling the height of the plasma torch, maintaing a constant distance to the material.
Typically, a plasma cutter operates within 60 to 150V DC. Some CNC-able plasma cutters have a CNC port outputting a ratio of operating voltage. This is done usually with a resistor divider. For example a given model has an operating voltage of max voltage of 125V DC, and a 50:1 resistor divider outputs 2.5VDC maximum.

Klipper plasma can measure in real-time this voltage to constantly adjust the height of the torch and follow the surface of the material. Thin material can warp, even thick material can be bent or uneven, the THC feature compensates for this.


JIT input
*********

ToDo

USB watchdog
************

ToDo
