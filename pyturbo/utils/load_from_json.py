# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import json
import os

import numpy as np


def load_from_json(system, filename):
    """Add init system data from json file."""
    path = os.path.join(*filename.split(os.path.sep))

    try:
        with open(path, "r") as f:
            params = json.load(f)

            for key, val in params.items():
                try:
                    if isinstance(system[key], np.ndarray):
                        system[key] = np.array(val)
                    else:
                        system[key] = val
                except KeyError:
                    raise KeyError(
                        f"Data {key} in file {filename} unknown in system {system.name}."
                    )

    except FileNotFoundError:
        raise FileNotFoundError(f"File_path {filename} does not exist.")

    return system
