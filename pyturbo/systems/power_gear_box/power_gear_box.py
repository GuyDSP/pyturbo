# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.ports import ShaftPort


class PowerGearBox(System):
    """Power gear box model.

    Inputs
    ------

    Outputs
    -------

    Design methods
    --------------

    Good practice
    -------------

    """

    def setup(self):

        self.add_inward("speed_ratio", 1.0, unit="")

        # inputs
        self.add_input(ShaftPort, "sh_in")
        self.add_output(ShaftPort, "sh_out")

    def compute(self):

        self.sh_out.N = self.sh_in.N / self.speed_ratio
        self.sh_out.power = self.sh_in.power
