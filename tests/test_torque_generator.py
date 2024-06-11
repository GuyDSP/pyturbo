# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pyturbo.systems import TorqueGenerator


class TestTorqueGenerator:
    """Define tests for the torque generator assembly system."""

    def test_run_once(self):
        sys = TorqueGenerator("cmp")

        sys.fl_in.W = 80
        sys.fuel_W = 0.1
        sys.run_once()

        assert sys.fl_out.W == 80.1
