# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path

import pytest
from cosapp.drivers import NonLinearSolver

import pyturbo.systems.turbofan.data as tf_data
from pyturbo.systems.turbofan import Turbofan
from pyturbo.utils.jupyter_view import get_view


class TestTurbofan:
    """Define tests for the turbofan assembly system."""

    sys = Turbofan("tf")

    def test_system_setup(self):
        # default constructor
        sys = self.sys

        data_input = ["fl_in"]
        data_output = []
        data_inward = ["fan_diameter", "fuel_W", "pamb"]
        data_outward = ["thrust", "bpr", "opr", "sfc"]

        for data in data_input:
            assert data in sys.inputs
        for data in data_output:
            assert data in sys.outputs
        for data in data_inward:
            assert data in sys.inwards
        for data in data_outward:
            assert data in sys.outwards

    def test_run_once(self):
        sys = self.sys

        sys.fl_in.W = 300.0
        sys.fuel_W = 1.0
        sys.fan_module.splitter_fluid.fluid_fractions[0] = 0.8

        sys.run_once()

        assert sys.fan_module.fan.fl_out.W == pytest.approx(240.0, 1e-3)
        assert sys.fan_module.booster.fl_out.W == pytest.approx(60.0, 1e-3)

    def test_run_CFM(self):
        assert Turbofan("sys", init_file=Path(tf_data.__file__).parent / "CFM56_7.json")

    def test_get_view(self):
        sys = self.sys
        assert get_view(sys) != {}

    @pytest.mark.skip("not relevant")
    def test_run_solver(self):
        sys = Turbofan("sys", init_file=Path(tf_data.__file__).parent / "CFM56_7.json")

        design = sys.add_driver(NonLinearSolver('solver', tol=1e-6, factor = 0.2))
        sys.run_drivers()

        assert True

        design.runner.add_unknown('fuel_W')
        design.runner.add_target('thrust')
        design.runner.design.extend(sys.design_methods['scaling'])

        sys.run_drivers()

        assert pytest.approx(sys.fan_diameter) == 1.549

        design = sys.add_driver(NonLinearSolver('solver', tol=1e-6))
        sys.run_drivers()

        design.runner.add_unknown('fuel_W')
        design.runner.add_target('thrust')
        sys.thrust = 85e3

        sys.run_drivers()

        assert pytest.approx(sys.sfc, rel=1e-2) == 0.37

    def test_run_design_method(self):
        sys = Turbofan("sys", init_file=Path(tf_data.__file__).parent / "CFM56_7.json")

        design = sys.add_driver(NonLinearSolver('solver', tol=1e-6, factor = 0.2))
        sys.run_drivers()

        design.runner.add_unknown('fuel_W')
        design.runner.add_target('thrust')
        design.runner.design.extend(sys.design_methods['scaling'])

        sys.thrust = 200e3

        sys.run_drivers()

        assert pytest.approx(sys.fan_diameter, rel = 0.1) == 2.25
