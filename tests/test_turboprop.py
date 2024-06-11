# Copyright (C) 2024, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import pytest

from pyturbo.systems.turboprop import Turboprop


class TestTurboprop:
    """Define tests for the turboprop assembly system."""

    sys = Turboprop("tp")

    def test_run_once(self):
        sys = self.sys

        sys.run_once()

        assert True
