# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.ports.units import convert_units
from cosapp.systems import System

from pyturbo.ports import FluidPort, ShaftPort
from pyturbo.thermo import IdealDryAir


class PropellerAero(System):
    """A propeller aero simple model.

    This model is based on the following references:
    https://skybrary.aero/sites/default/files/bookshelf/3698.pdf

    Parameters
    ----------
    FluidLaw: Class, default=IdealDryAir
        Class providing gas characteristics

    Inputs
    ------
    fl_in: FluidPort
        fluid going into the compressor
    sh_in: ShaftPort
        shaft driving the compressor

    eff_poly[-]: float, default=0.9
        polytropic efficiency
    phiP[-]: float, default=0.4
        axial flow velocity coefficient for no power consumption of the compressor

    radius[m]: float, default=1.0
        propeller radius
    inlet_area[m**2]: float, default=1.0
        inlet area

    Outputs
    -------
    utip[m/s]: float, default=0.0
        blade tip speed at inlet
    phi[-]: float, default=0.0
        axial flow velocity coefficient
    psi[-]: float, default=0.0
        load coefficient
    pr[-]: float, default=1.0
        total to total pressure ratio
    tr[-]: float, default=1.0
        total to total temperature ratio

    Design methods
    --------------
    off design:
        psi computed from enthalpy conservation equal psi computed from characteristics

    Good practice
    -------------
    1:
        initiate sh_in.power with the good order of magnitude of shaft power
    """

    def setup(self, FluidLaw=IdealDryAir):
        # properties
        self.add_inward("gas", FluidLaw())

        # inputs/outputs
        self.add_input(FluidPort, "fl_in")
        self.add_input(ShaftPort, "sh_in")

        # geom characteristics
        self.add_inward("radius", 1.0, unit="m", desc="propeller radius")
        self.add_inward("inlet_area", 1.0, unit="m**2", desc="inlet area")

        # aero characteristics
        self.add_inward("eff_poly", 0.9, desc="polytropic efficiency")
        self.add_inward(
            "phiP",
            0.4,
            desc="axial flow velocity coefficient for zero compressor consumption",
        )
        self.add_inward("xnd", 10000.0, unit="rpm", desc="Rotational speed at design point")

        # functional characteristics
        self.add_outward("utip", 0.0, unit="m/s", desc="tip speed")
        self.add_outward("phi", 0.0, unit="", desc="axial flow velocity coefficient")
        self.add_outward("psi", 0.0, unit="", desc="load coefficient")

        self.add_outward("pr", 1.0, unit="", desc="total to total pressure ratio")
        self.add_outward("tr", 1.0, unit="", desc="total to total temperature ratio")

        self.add_outward("pcnr", 100.0, unit="", desc="Percentage of rotational speed vs reference")

        self.add_outward("power", 100.0, unit="hp", desc="Propeller power")
        self.add_outward("thrust", 100.0, unit="N", desc="Propeller thrust")

        # off design
        self.add_outward(
            "eps_psi",
            0.0,
            unit="",
            desc="difference between psi from caracteristics and from enthalpy",
        )
        self.add_equation("eps_psi == 0")
        self.add_unknown("fl_in.W")

    def compute(self):
        # fl_out computed from fl_in, enthalpy and mass conservation
        delta_h = self.sh_in.power / self.fl_in.W
        h = self.gas.h(self.fl_in.Tt) + delta_h
        Tt_out = self.gas.t_f_h(h, tol=1e-6)

        self.tr = Tt_out / self.fl_in.Tt
        self.pr = self.gas.pr(self.fl_in.Tt, Tt_out, self.eff_poly)

        # axial flow coefficient
        self.utip = self.sh_in.N * np.pi / 30.0 * self.radius
        rho = self.gas.density(self.fl_in.Pt, self.fl_in.Tt)
        vm = self.fl_in.W / (rho * self.inlet_area)
        self.phi = vm / self.utip

        # load coefficient
        self.psi = 1 - self.phi / self.phiP
        self.eps_psi = delta_h / self.utip**2 - self.psi

        self.pcnr = self.sh_in.N / self.xnd * 100.0

        # propeller characteristics
        self.power = convert_units(self.sh_in.power, "W", "hp")
        self.thrust = self.inlet_area * self.fl_in.Pt * (1.0 - self.pr)
