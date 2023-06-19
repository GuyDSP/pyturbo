# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System

from pyturbo.systems.nacelle.nacelle_geom import NacelleGeom


class Nacelle(System):
    """Nacelle simple assembly model.

    Sub-systems
    -----------
    geom: NacelleGeom
        provide the geometry for visualisation

    Inputs
    ------
    kp: KeypointsPort
        nacelle geometrical envelop
    """

    def setup(self):  # noqa: TWI009
        # children
        self.add_child(
            NacelleGeom("geom"),
            pulling=[
                "hilite_kp",
                "ogv_exit_tip_kp",
                "sec_nozzle_exit_kp",
                "fan_diameter",
            ],
        )
