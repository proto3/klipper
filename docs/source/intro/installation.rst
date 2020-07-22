Klipper installation and setup
==============================

Installation
------------
Klipper-plasma is basically Klipper with extra features for plasma. Thus it is
definitely recommended to have a look at the `official documentation`_.
Everything you would learn here applies to Klipper-plasma.

However, the installation described on the `installation page`_ applies to a
Raspberry Pi with Octoprint, which is the common setup for 3D printing, but not
our case. We don't need Octoprint and have no particular interest in using RPi.

Here are the commands you would need to install Klipper-plasma on Ubuntu 18.04.

.. prompt:: bash $

   git clone git@github.com:proto3/klipper-plasma.git
   ./klipper/scripts/install-ubuntu-18.04.sh

*Note that Klipper provides installation scripts for some common distributions.
One can find those in klipper/scripts.*


Once installed, Klipper will always start at boot time. Now you need to flash
your MCU, for this simply follow the instructions in **Building and flashing the
micro-controller** from the official `installation page`_.

.. _official documentation: https://www.klipper3d.org/Overview.html
.. _installation page: https://www.klipper3d.org/Installation.html

Configuration file
------------------

During installation, a printer.cfg file is created in your home directory. This
is where you need to set all your machine parameters, then everytime Klipper
connects to the MCU, it will upload configuration to it. This means the MCU
knows  nothing about the machine until the PC hosted side connects to it. **By
the way, a device to prevent any unexpected plasma triggering event before
connection is under developement. (Probably a small circuit with a lock/unlock
protocol in the middle of the trigger wire)**

The `example configuration`_ from the original Klipper helps you to configure
everything but plasma features.

.. _`example configuration`: https://github.com/KevinOConnor/klipper/blob/master/config/example.cfg

When it's done, you can complete it with the following parameters to enable
plasma related features.

.. code-block:: yaml

   # Empty section to enable integrated THC
   # Note that is also needs all the rt_ keys in stepper_z section.
   [torch_height_controller]

   [stepper_z]
   step_pin: ar46
   dir_pin: ar48
   enable_pin: ar62
   step_distance: 0.0025
   endstop_pin: ar18
   position_endstop: 0
   homing_speed: 10
   position_max: 100
   # The following keys are for real time mode (used by THC), when THC is
   # running, they override z speed and acceleration values, so choose these
   # values carefuly.
   # Frequency at which z stepper frequency is updated.
   rt_control_freq: 500
   # Frequency updates between each voltage reading.
   # In this particular case 500 / 5 = 100Hz readings.
   rt_input_cycle: 5
   # Factor applied to input voltage to compute target speed. Bigger values
   # means higher sensitivity, changing the sign change the direction.
   rt_input_factor: -30
   # Maximum stepper frequency in steps.s-1 (not millimeters !)
   rt_max_freq: 10000
   # Maximum stepper acceleration in steps.s-2
   rt_max_acc: 200000
   # Affine coefficients to compensate for input voltage divider
   # plasma_voltage = a * adc_voltage + b
   rt_a_coeff: 36.639
   rt_b_coeff: 50.001

   # This is the standard way of using Klipper probe, have look to the official
   # documentation for more option on this.
   [probe]
   pin: ar19
   z_offset: 0.0

   [plasma]
   # Output pin to trigger plasma.
   # It use the same syntax as any pin (^ to pullup, ! to inverse)
   start_pin: ar57
   # Input pin to read plasma arc transfer.
   transfer_pin: ar58
   # Time after which plasma ignition aborts if no transfer occurs.
   # Keep this value under 2000ms for now.
   transfer_timeout_ms: 1000

For your configuration changes to be applied, you need to restart Klipper, which
is always background running. Use the following command to do this.

.. prompt:: bash $

   sudo systemctl restart klipper
