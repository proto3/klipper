# Support for plasma cutter
#
# Copyright (C) 2020  Lucas Felix <lucas.felix0738@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

class TorchHeightController:
    def __init__(self, config):
        self.printer = config.get_printer()
        all_mcus = [m for n, m in self.printer.lookup_objects(module='mcu')]
        self.mcu = all_mcus[0]
        self.toolhead = None
        self.rail = None

        self.mcu.register_config_callback(self.build_config)

        # Register commands
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command("M6", self.cmd_M6)
        self.gcode.register_command("M7", self.cmd_M7)
        self.mcu.register_response(self._handle_rt_log, 'stepper_rt_log')
        self.enable = False

    def build_config(self):
        self.toolhead = self.printer.lookup_object('toolhead')
        self.rail = self.toolhead.get_kinematics().rails[2]

    def _handle_rt_log(self, params):
        kin = self.printer.lookup_object('toolhead').get_kinematics()
        s = self.rail.steppers[0]
        pos = params['pos'] * s._step_dist
        if s._invert_dir:
            pos = -pos
        pos -= s._mcu_position_offset
        error = float(params['error_mv']) / 1000
        self.gcode.respond_info('echo: THC_error ' + str(pos) + ' ' + str(error))

    def cmd_M6(self, gcmd):
        if not self.enable:
            self.enable = True
            voltage = gcmd.get_float('V', minval=50., maxval=200.)
            clock = self.mcu.print_time_to_clock(self.toolhead.get_last_move_time())
            self.rail.set_realtime_mode(clock, int(voltage  * 1000))
        else:
            self.gcode._respond_error('THC already on')

    def cmd_M7(self, gcmd):
        if self.enable:
            self.enable = False
            clock = self.mcu.print_time_to_clock(self.toolhead.get_last_move_time())
            self.rail.set_host_mode(clock)
        else:
            self.gcode._respond_error('THC already off')

def load_config(config):
    return TorchHeightController(config)
