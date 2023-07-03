# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.systems import System
from OCC.Core.TopoDS import TopoDS_Shape
from pyoccad.create import CreateAxis, CreateRevolution, CreateTopology, CreateWire

from pyturbo.ports import KeypointsPort
from pyturbo.utils import rz_to_3d
from pyturbo.utils import JupyterViewable


class GenericSimpleGeom(System, JupyterViewable):
    """A generic simple geometry based on a quasi cylindrical revolution."""

    def setup(self):  # noqa: TWI009
        # inwards/outwards
        self.add_input(KeypointsPort, "kp")

    def view(self) -> TopoDS_Shape:
        w = CreateWire.from_points(
            (
                rz_to_3d(self.kp.inlet_hub),
                rz_to_3d(self.kp.exit_hub),
                rz_to_3d(self.kp.exit_tip),
                rz_to_3d(self.kp.inlet_tip),
            ),
            auto_close=True,
        )

        shell = CreateRevolution.surface_from_curve(w, CreateAxis.oz())
        return CreateTopology.make_compound(shell)
