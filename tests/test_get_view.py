# Copyright (C) 2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from cosapp.base import System
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere

from pyturbo.utils import JupyterViewable
from pyturbo.utils.jupyter_view import get_view

class Sphere(System, JupyterViewable):
    """Simple viewable sphere.

    """
    def setup(self):
        self.add_inward('radius', 1.0, unit='m', desc='Radius of the sphere.')

    def view(self) -> TopoDS_Shape:
        sphere = BRepPrimAPI_MakeSphere(self.radius).Shape()
        return sphere

class SphereKO(System):
    """Simple viewable sphere but that is not of class JupyterViewable.

    """
    def setup(self):
        self.add_inward('radius', 1.0, unit='m', desc='Radius of the sphere.')

    def view(self) -> TopoDS_Shape:
        sphere = BRepPrimAPI_MakeSphere(self.radius).Shape()
        return sphere


class TestGetView:
    """Define tests for get_view."""

    def test_get_view(self):
        assert get_view(Sphere("sys"))['sys']

    def test_not_viewable(self):
        assert get_view(SphereKO("sys")) == {}
