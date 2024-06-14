# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest 

from cosapp.drivers import NonLinearSolver, EulerExplicit

from pyturbo.systems.propeller import Propeller, PropellerAero
from pyturbo.systems.turboprop import Turboprop, TurbopropAero, TurbopropGeom
from pyturbo.systems.power_gear_box import PowerGearBox
from pyturbo.systems.torque_generator import TorqueGenerator

# cls, target, unknown
cls_list = [
    (PowerGearBox, [], []), 
    (PropellerAero, [], []), 
    (Propeller, [], []), 
    (TurbopropAero, [], []),
    (Turboprop, [], []),
    (TurbopropGeom, [], []),
    (TorqueGenerator, [], []), 
    ]

@pytest.mark.parametrize("cls, target, unknown", cls_list)
class TestSystems:
    def test_setup(self, cls, target, unknown):
        cls("sys")
        print('Class name:', cls.__name__)
        assert True

    def test_once(self, cls, target, unknown):
        sys = cls("sys")
        sys.run_once()

        print('Class name:', cls.__name__)
        assert True

    def test_driver(self, cls, target, unknown):
        print('Class name:', cls.__name__)
        sys = cls("sys")
        solver = sys.add_driver(NonLinearSolver('solver'))
        #solver.add_target(target)
        solver.add_unknown(unknown)

        sys.run_drivers()

        assert True

    def test_run_design_methods(self, cls, target, unknown):
        """Test run design methods."""

        print('Class name:', cls.__name__)
        sys = cls("sys")
        for name in sys.design_methods.keys():
            print("Design method : ", name)
            sys1 = cls("sys")
            solver = sys1.add_driver(NonLinearSolver("solver", tol=1e-6))
            #solver.add_target(target)
            solver.add_unknown(unknown)
            sys1.run_drivers()

            solver.extend(sys1.design_methods[name])
            sys1.run_drivers()

            print("Problem : ", solver.problem)
            assert solver.residue() < 1e-6

    def test_transient(self, cls, target, unknown):
        """Test run transient."""

        print('Class name:', cls.__name__)
        sys = cls("sys")
        euler = sys.add_driver(EulerExplicit('euler', time_interval=(0.0, 10.0), dt = 1.0))
        solver = euler.add_child(NonLinearSolver('solver'))
        #solver.add_target(target)
        solver.add_unknown(unknown)
        sys.run_drivers()

        print('time : ', sys.time)
        assert True
