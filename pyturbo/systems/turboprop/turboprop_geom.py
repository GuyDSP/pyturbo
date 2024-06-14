# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from cosapp.systems import System

from pyturbo.ports import C1Keypoint, KeypointsPort
from pyturbo.utils import slope_to_drdz


class TurbopropGeom(System):
    """Turboprop geometry.

    Reference for all dimensions is fan diameter

    Turbofan module is made of components:
        - inlet
        - fan module
        - gas generator
        - turbine
        - trf (turbine rear frame)
        - primary nozzle
        - secondary nozzle
        - plug
        - nacelle
        - shaft

    Pylon attach points are also provided

    Inputs
    ------
    fan_diameter[m]: float, default=1.6
        fan diameter

    inlet_length_ratio[-]: float, default=0.4
        inlet length relative to fan radius
    inlet_radius_ratio[-]: float, default=0.9
        inlet radius relative to fan radius"

    fanmodule_length_ratio[-]: float, default=1.0
        fanmodule length relative to fan radius
    ogv_exit_hqt[-]: float, default=0.6
        fan OGV exit hub-to-tip ratio

    core_inlet_radius_ratio[-]: float, default=0.25
        high-pressure core inlet radius relative to fan radius
    core_exit_radius_ratio[-]: float, default=0.3
        high-pressure core exit radius relative to fan radius
    core_length_ratio[-]: float, default=3.0
        high-pressure core length relative to its radius

    shaft_radius_ratio[-]: float, default=0.1
        shaft radius relative to fan radius

    tcf_exit_radius_ratio[-]: float, default=1.2
        turbine center frame exit radius relative to inlet one
    tcf_length_ratio[-]: float, default=0.15
        turbine center frame length relative its inlet tip radius

    turbine_radius_ratio[-]: float, default=0.65
        turbine radius relative to fan radius
    turbine_length_ratio[-]: float, default=1.0
        turbine length relative to turbine radius
    turbine_fp_exit_hqt[-]: float, default=0.8
        LPT turbine flowpath exit hub-to-tip ratio
    trf_length_ratio[-]: float, default=0.15
        trf length relative to turbine radius

    core_cowl_slope[deg]: float, default=-20.0
        core cowl slope angle

    primary_nozzle_length_ratio[-]: float, default=0.5
        primary nozzle length relative to TRF radius

    secondary_nozzle_length_ratio[-]: float, default=0.2
        secondary nozzle length relative to fan_radius

    pri_nozzle_area_ratio[-]: float, default=0.9
        primary nozzle area ratio
    sec_nozzle_area_ratio[-]: float, default=0.9
        secondary nozzle area ratio

    frd_mount_relative[-]: float, default=0.75
        forward engine mount position relative to tip fan module
    aft_mount_relative[-]: float, default=0.75
        aftward engine mount position relative to tip trf

    Outputs
    -------
    inlet_kp: KeypointsPort
        inlet geometrical envelop
    fanmodule_kp: KeypointsPort
        fan module geometrical envelop
    core_kp: KeypointsPort
        core geometrical envelop
    shaft_kp: KeypointsPort
        shaft geometrical envelop
    tcf_kp: KeypointsPort
        turbine center frame geometrical envelop
    turbine_kp: KeypointsPort
        turbine geometrical envelop
    trf_kp: KeypointsPort
        turbine rear frame geometrical envelop
    primary_nozzle_kp: KeypointsPort
        primary nozzle geometrical envelop
    secondary_nozzle_kp: KeypointsPort
        secondary nozzle geometrical envelop

    fan_inlet_tip_kp[m]: np.array(2), default=np.ones(2)
        fan inlet tip position
    ogv_exit_hub_kp[m]: np.array(2), default=np.ones(2)
        ogv exit hub position
    ogv_exit_tip_kp[m]: np.array(2), default=np.ones(2)
        ogv exit tip position
    turbine_exit_tip_kp[m]: np.array(2), default=np.ones(2)
        turbine exit tip position
    pri_nozzle_exit_kp: C1Keypoint
        primary nozzle exit position
    sec_nozzle_exit_kp[m]: np.array(2), default=np.ones(2)
        secondary nozzle exit tip position
    sec_nozzle_exit_hub_kp: C1Keypoint
        secondary nozzle exit hub position

    frd_mount[m]: np.array(2), default=np.r_[0.9, 0.5]
        forward engine mount
    aft_mount[m]: np.array(2), default=np.r_[0.9, 0.5]
        aftward engine mount

    fan_module_length[m]: float, default=1.0
        fan module length from fan inlet to intermediate case exit",
    engine_length[m]: float, default=1.0
        engine length from fan module to trf
    """

    def setup(self):
        # inwards
        self.add_inward("propeller_diameter", 5.0, unit="m", desc="propeller diameter")

        self.add_inward(
            "propeller_length_ratio",
            0.2,
            unit="",
            desc="propeller length relative to propeller radius",
        )
        self.add_inward(
            "core_inlet_radius_ratio",
            0.25,
            unit="",
            desc="core inlet radius relative to propeller radius",
        )
        self.add_inward(
            "core_exit_radius_ratio",
            1.0,
            unit="",
            desc="core exit radius relative to core inlet",
        )
        self.add_inward(
            "core_length_ratio",
            3.0,
            unit="",
            desc="core length relative to its radius",
        )

        self.add_inward(
            "shaft_radius_ratio",
            0.1,
            unit="",
            desc="shaft radius relative to core radius",
        )
        self.add_inward("core_cowl_slope", -20.0, unit="deg", desc="core cowl slope angle")

        self.add_inward(
            "primary_nozzle_length_ratio",
            0.5,
            unit="",
            desc="primary nozzle length relative to core radius",
        )

        self.add_inward(
            "pri_nozzle_area_ratio", 0.9, unit="", desc="primary nozzle exit area ratio"
        )

        # outwards
        self.add_output(KeypointsPort, "propeller_kp")
        self.add_output(KeypointsPort, "core_kp")
        self.add_output(KeypointsPort, "primary_nozzle_kp")

        self.add_outward("propeller_inlet_tip_kp", np.ones(2), unit="m")
        self.add_outward("pri_nozzle_exit_kp", C1Keypoint())

        self.add_outward(
            "propeller_module_length",
            1.0,
            unit="m",
            desc="propeller length",
        )
        self.add_outward(
            "engine_length", 1.0, unit="m", desc="engine length from propeller to primary nozzle"
        )

    def compute(self):
        # set keypoints to internal components
        propeller_radius = self.propeller_diameter / 2.0

        self.propeller_module_length = propeller_length = (
            propeller_radius * self.propeller_length_ratio
        )

        core_inlet_radius = propeller_radius * self.core_inlet_radius_ratio
        core_exit_radius = core_inlet_radius * self.core_exit_radius_ratio
        core_length = core_inlet_radius * self.core_length_ratio

        primary_nozzle_length = core_inlet_radius * self.primary_nozzle_length_ratio

        self.engine_length = propeller_length + core_length

        # propeller
        self.propeller_kp.inlet_hub = np.r_[0.0, 0.0]
        self.propeller_kp.inlet_tip = np.r_[propeller_radius, 0.0]
        self.propeller_kp.exit_hub = self.propeller_kp.inlet_hub + np.r_[0.0, propeller_length]
        self.propeller_kp.exit_tip = self.propeller_kp.inlet_tip + np.r_[0.0, propeller_length]

        self.propeller_inlet_tip_kp = self.propeller_kp.inlet_tip

        # core
        self.core_kp.inlet_hub = np.r_[0.0, propeller_length]
        self.core_kp.inlet_tip = np.r_[core_inlet_radius, self.core_kp.inlet_hub_z]

        self.core_kp.exit_hub = self.core_kp.inlet_hub + np.r_[0.0, core_length]
        self.core_kp.exit_tip = np.r_[core_exit_radius, self.core_kp.exit_hub_z]

        # primary nozzle
        self.primary_nozzle_kp.inlet_hub = self.core_kp.exit_hub
        self.primary_nozzle_kp.inlet_tip = self.core_kp.exit_tip

        self.primary_nozzle_kp.exit_hub = (
            self.primary_nozzle_kp.inlet_hub + np.r_[0.0, primary_nozzle_length]
        )
        inlet_area = np.pi * (
            self.primary_nozzle_kp.inlet_tip_r**2 - self.primary_nozzle_kp.inlet_hub_r**2
        )
        self.primary_nozzle_kp.exit_tip = np.r_[
            np.sqrt(
                self.pri_nozzle_area_ratio * inlet_area / np.pi
                + self.primary_nozzle_kp.inlet_hub_r**2
            ),
            self.core_kp.exit_tip_z,
        ]

        min_dz = (self.primary_nozzle_kp.exit_tip_r - self.core_kp.exit_tip_r) / np.tan(
            np.radians(self.core_cowl_slope)
        )
        dz = max(min_dz, primary_nozzle_length)
        dr = dz * np.tan(np.radians(self.core_cowl_slope))

        self.pri_nozzle_exit_kp.rz = self.core_kp.exit_tip + np.r_[dr, dz]
        self.pri_nozzle_exit_kp.drdz = slope_to_drdz(self.core_cowl_slope)
