# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from typing import Dict, Union

from OCC.Core.TopoDS import TopoDS_Shape


class JupyterViewable:
    """JupyterViewable utils."""

    def view(self) -> Union[TopoDS_Shape, Dict[str, TopoDS_Shape]]:
        raise NotImplementedError("'JupyterViewable.view' should be implemented in derived classes")
