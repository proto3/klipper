Installation and setup
======================

Installation
------------
Klipper for plasma is basically Klipper with extra features for plasma.
Thus it is definitely recommended to have a look at the
`official documentation`_. Everything you would learn here applies to the plasma
version.

However, the installation described on the `installation page`_ concerns a
Raspberry Pi with Octoprint, which is the common setup for 3D printing, but not
for plasma. We don't need Octoprint and have no particular interest in using
RPi.
From now on, consider that we always talk about Klipper for plasma when
mentioning Klipper.

Here are the commands you would need to install Klipper on Ubuntu 18.04.
Notice that installation scripts for some other distributions are also available
in klipper/scripts.

.. prompt:: bash $

   git clone git@github.com:proto3/klipper-plasma.git
   ./klipper/scripts/install-ubuntu-18.04.sh

**Note:** *Klipper is currently moving to Python3. Before this is done, I would
recommend no to use Ubuntu 20.04 or other recent distributions that may have
dropped Python2 support.*


Once installed, Klipper will always start at boot time. Now you need to flash
your MCU, for this, simply follow the instructions in **Building and flashing the
micro-controller** from the official `installation page`_.

.. _official documentation: https://www.klipper3d.org/Overview.html
.. _installation page: https://www.klipper3d.org/Installation.html

Configuration file
------------------

During installation, a **printer.cfg** file is created in your home directory.
This is where you need to set all your machine parameters, then every time the
PC connects to the MCU, it will upload the configuration to it. This means the
MCU knows  nothing about the machine until the PC connects to it. For that
reason the plasma trigger pin logic can never be reversed to ensure it is always
off before MCU is configured.

The `example configuration`_ from the original Klipper helps you to configure
everything but plasma features. When it's done, you can complete it with the
following parameters to enable plasma related features.

.. _`example configuration`: https://github.com/KevinOConnor/klipper/blob/master/config/example.cfg

.. code-block:: yaml

    [stepper_z]
    # --- Add the following keys to z stepper if using THC ---
    # stepper period update frequency in speed mode
    speed_mode_rate: 500
    # stepper max velocity in mm.s-1 in speed mode
    speed_mode_max_velocity: 40
    # stepper max acceleration in mm.s-2 in speed mode
    speed_mode_max_accel: 1000
    #----------------------------------------------------------
    [probe]
    # --- Example of ohmic probe configuration ---
    # Offset is zero as the sensor is the torch itself
    pin: ^!ar18
    z_offset: 0.0
    speed: 10
    #----------------------------------------------------------
    [plasma]
    # pin to trigger plasma, logic is active high
    # and can't be reversed for safety reasons
    start_pin: ar57
    # pin to read arc transfer
    transfer_pin: ^!ar58
    # milliseconds before timeout on plasma ignition
    transfer_timeout_ms: 1000
    #----------------------------------------------------------
    [torch_height_controller]
    # plasma voltage sampling rate
    rate: 100
    # voltage to speed factor, sign is for direction
    # target_speed = speed_coeff * voltage_error
    speed_coeff: -3.0 # in mm.s-1.v-1
    # Affine coefficients for ADC to plasma voltage conversion
    # plasma_voltage = a * adc_input + b
    a_coeff: 31.627
    b_coeff: 49.047
    #----------------------------------------------------------
    [emergency_stop]
    # --- MCU embedded emergency stop ---
    # won't need computer approval to stop everything
    pin: ^ar52

For your configuration changes to be applied, you need to restart Klipper, which
is always background running. Use the following command to do this.

.. prompt:: bash $

   sudo systemctl restart klipper
