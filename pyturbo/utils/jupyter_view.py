# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import logging
from typing import Any, Dict

import numpy as np
from cosapp.systems import System

from pyturbo.utils import JupyterViewable

try:
    from pyoccad.render import JupyterThreeJSRenderer
except ImportError:
    raise ImportError("Please install 'pyoccad' before using this module")

from OCC.Core.TopoDS import TopoDS_Shape

logger = logging.getLogger(__name__)


def jupyter_view(
    sys: System, options: Dict[str, Dict[str, Any]] = None, **kwargs
) -> JupyterThreeJSRenderer:
    """Render a system in a Jupyter notebook."""

    kwargs["view_size"] = kwargs.get("view_size", (1800, 800))
    kwargs["camera_target"] = kwargs.get("camera_target", (1.0, 0.0, 0.0))
    kwargs["camera_position"] = kwargs.get("camera_position", (-2.0, 1.0, 2.0))

    renderer = JupyterThreeJSRenderer(**kwargs)

    if options is None:
        options = {}
        if "view_options" in sys:
            options = sys.view_options

    def get_shape_options(name):
        split_name = name.split(".")
        names = [split_name[0]]
        for i in range(1, len(split_name)):
            names.append(".".join((names[-1], split_name[i])))
        opt = {}
        for n in names:
            opt.update(options.get(n, {}))
        return opt

    def add_to_renderer(name, shape):
        if isinstance(shape, TopoDS_Shape):
            opt = get_shape_options(name)
            renderer.add_shape(shape, uid=name, **opt)
        elif isinstance(shape, dict):
            for n, s in shape.items():
                add_to_renderer(".".join((name, n)), s)
        else:
            raise TypeError("Unsupported type")

    for name, shape in get_view(sys).items():
        add_to_renderer(name, shape)

    return renderer


def get_view(sys: System) -> Dict[str, TopoDS_Shape]:
    """Get the view of a JupyterViewable system.

    Stops if itself has a view, else go recursively in the children.
    """
    if not isinstance(sys, JupyterViewable) and hasattr(sys, "view"):
        logger.warning(
            f"System {sys.name!r} has 'view' function but is not of JupyterViewable class."
        )

    if isinstance(sys, JupyterViewable):
        occt_shape = sys.view()
        if not isinstance(occt_shape, (TopoDS_Shape, dict)):
            raise TypeError(
                f"Method view from {sys.name} should return type TopoDS_Shape or dict, \
                return {type(occt_shape)}"
            )
        return {sys.name: occt_shape}

    # check the children
    d = {}
    for child in sys.children.values():
        occt_shape = get_view(child)
        if occt_shape is not {}:
            d[child.name] = occt_shape

    return d


def update_jupyter_view(sys: System, renderer: "JupyterThreeJSRenderer"):
    """Update the Jupyter view."""
    for name, shape in get_view(sys).items():
        renderer.update_shape(shape, uid=name)


def add_nacelle_brand(nacelle_geom: System, renderer: "JupyterThreeJSRenderer", brand_path: str):
    """Add brand on nacelle geometry."""
    try:
        from pythreejs import ImageTexture, MeshStandardMaterial
    except ImportError:
        raise ImportError("Please install 'pythreejs' before using this function")

    logo = ImageTexture(imageUri=brand_path)
    renderer.add_shape(
        nacelle_geom._brand_shape(),
        uid="brand",
        plot_edges=False,
        face_material=MeshStandardMaterial(
            map=logo,
            transparent=True,
            side="DoubleSide",
        ),
        uv_rotation=np.pi / 2,
    )
