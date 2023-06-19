# Copyright (C) 2022-2023, twiinIT
# SPDX-License-Identifier: BSD-3-Clause

import json
import os

import numpy as np


def save_to_json(system, filename):
    """Save system data to json file."""
    path = os.path.join(*filename.split(os.path.sep))

    def to_dict(system):
        def save(name, data, dd):
            if isinstance(data, float) or isinstance(data, int):
                dd[name] = data
            elif isinstance(data, np.ndarray):
                dd[name] = data.tolist
            else:
                print(f"Variable {name} of type {type(data)} is not saved.")

        dd = {}
        for _, child in system.children.items():
            dd.update({f"{child.name}.{name}": data for name, data in to_dict(child).items()})

        for name, data in system.inwards.items():
            save(name, data, dd)

        for _, port in system.inputs.items():
            for name, data in port.items():
                save(f"{port.name}.{name}", data, dd)

        return dd

    data = to_dict(system)
    try:
        with open(path, "w") as outfile:
            json.dump(data, outfile)

    except FileNotFoundError:
        raise FileNotFoundError(f"File_path {filename} does not exist.")

    return system
