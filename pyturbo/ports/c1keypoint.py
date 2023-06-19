# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np


class C1Keypoint:
    """A keypoint class including C1-continuity info.

    A C1 keypoint contains both position `pos` and first order derivate `der`.

    The geometry is assumed to be revolution around x-axis and keypoint
    is defined in {r, z} coordinates.
    """

    default_pos = np.ones(2)
    default_der = np.ones(2)

    def __init__(self, pos=default_pos, der=default_der):
        self.pos = pos
        self.der = der

    @property
    def rz(self):
        return self.pos

    @rz.setter
    def rz(self, rz: np.ndarray):
        self.pos = rz

    @property
    def r(self):
        return self.pos[0]

    @r.setter
    def r(self, val: float):
        self.pos[0] = val

    @property
    def z(self):
        return self.pos[1]

    @z.setter
    def z(self, val: float):
        self.pos[1] = val

    @property
    def drdz(self):
        return self.der

    @drdz.setter
    def drdz(self, drdz: np.ndarray):
        self.der = drdz

    @property
    def dr(self):
        return self.der[0]

    @dr.setter
    def dr(self, val: float):
        self.der[0] = val

    @property
    def dz(self):
        return self.der[1]

    @dz.setter
    def dz(self, val: float):
        self.der[1] = val
