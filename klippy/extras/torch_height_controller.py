# Support for torch height controller.
#
# Copyright (C) 2020  Lucas Felix <lucas.felix0738@gmail.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

class TorchHeightController:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        all_mcus = [m for n, m in self.printer.lookup_objects(module='mcu')]
        self.mcu = all_mcus[0]
        self.toolhead = None

        self.thc_oid = self.mcu.create_oid()
        self.mcu.add_config_cmd("config_thc oid=%d rate=%u a_coeff=%u"
            " b_coeff=%u" % (self.thc_oid, config.getint('rate'),
            config.getfloat('a_coeff') * (2**10),
            config.getfloat('b_coeff') * 1000))

        self.cmd_queue = self.mcu.alloc_command_queue()
        self.mcu.register_config_callback(self.build_config)
        self.thc_start_cmd = None
        self.thc_stop_cmd = None

        # Register commands
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command("M6", self.cmd_M6)
        self.gcode.register_command("M7", self.cmd_M7)
        self.mcu.register_response(self._handle_sample, 'thc_sample')
        self.enable = False
        self.last_M7 = None

    def build_config(self):
        self.toolhead = self.printer.lookup_object('toolhead')
        self.thc_start_cmd = self.mcu.lookup_command(
            "start_thc oid=%c clock=%u", cq=self.cmd_queue)
        self.thc_stop_cmd = self.mcu.lookup_command(
            "stop_thc oid=%c clock=%u", cq=self.cmd_queue)

    def _handle_sample(self, params):
        voltage = float(params['voltage_mv']) / 1000
        self.gcode.respond_info('echo: THC_error ' + str(voltage))

    def cmd_M6(self, gcmd):
        if not self.enable:
            voltage = gcmd.get_float('V', minval=0, maxval=300)
            last_move = self.toolhead.get_last_move_time()
            clock = self.mcu.print_time_to_clock(last_move)
            self.thc_start_cmd.send([self.thc_oid, clock, int(voltage  * 1000)],
                                     reqclock=clock)
            self.enable = True
        else:
            self.gcode._respond_error('THC already ON')

    def cmd_M7(self, gcmd):
        if self.enable:
            self.last_M7 = self.toolhead.get_last_move_time()
            clock = self.mcu.print_time_to_clock(self.last_M7)
            self.thc_stop_cmd.send([self.thc_oid, clock], reqclock=clock)
            self.enable = False
        else:
            self.gcode._respond_error('THC already OFF')

def load_config(config):
    return TorchHeightController(config)
