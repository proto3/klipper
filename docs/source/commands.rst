Plasma specific commands
========================

M3 *- Start plasma*
*******************
Request plasma to start and blocks until the arc is transferred or timeout
occurs. The timeout value is defined in **[plasma]** configuration
**transfer_timeout_ms**.

Error cases:
    - Ignition timed out
    - Arc lost after ignition
    - Multiple calls to M3 without M5

Errors automatically stop plasma. In any case, M3 has to be rearmed with M5
before it can be called again.

M5 *- Stop plasma*
******************
Stop plasma and rearm M3 command.


M6 *- Enable THC*
*****************
args : **V<voltage v> T<feedrate threshold mm/min> A<minpos mm> B<maxpos mm>**

Enable THC to track a specified voltage by moving the torch up and down.

When XY motion goes under the feedrate threshold, THC slowdown (and eventually
stops). When feedrate goes back above the threshold, THC starts moving again.

The torch move between A and B positions if specified, otherwise on the whole z
range (but never exceeding rail limits).

Example : *M6 V110.5 T2400 A10 B150*

See **[torch_height_controller]** for permanent settings.

M7 *- Disable THC*
******************
Disable THC. When disabling, only MCU knows the exact position of z axis. M6 can
be called again, but no standard z motion can be performed before PC resync its
z position.

M8 *- Resync z position*
************************
Resync PC z position on the MCU.

Example :

.. code-block:: ahk

    M6 V80
    ; THC is active
    M7
    ; THC has stopped, but only MCU knows where z is
    ; M6 can be called again, but not G1 Z
    M8
    ; MCU has sent position to PC, everything is back to normal
    ; G1 Z can be called
    G1 Z42


Cut sequence example
********************

.. code-block:: ahk

    ; absolute mode
    G90
    ; move to piercing position
    G1 F6000 X200 Y300
    ; lower torch until contact
    PROBE
    ; incremental mode
    G91
    ; retract to piercing height
    G1 F3000 Z3.8
    ; start plasma (blocking until transfer)
    M3
    ; wait piercing delay
    G4 P300
    ; move to cutting height
    G1 Z-2.3
    ; absolute mode
    G90
    ; enable THC
    M6 V110 T1800

    ; perform cut
    G1 F2000 X350 Y220
    G1 ...

    ; disable THC
    M7
    ; stop plasma
    M5
    ; resync z axis
    M8
    ; incremental mode
    G91
    ; retract torch
    G1 F1800 Z30
    ; absolute mode
    G90
