# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

from abc import ABC, abstractmethod

from typing import Dict, Union

from OCC.Core.TopoDS import TopoDS_Shape


class JupyterViewable(ABC):
    """JupyterViewable utils."""

    @abstractmethod
    def view(self) -> Union[TopoDS_Shape, Dict[str, TopoDS_Shape]]:
        pass
