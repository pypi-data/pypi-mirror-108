import logging
import os

import yaml

config_file = ".dirganize.yml"

from typing import Dict


def get_mapping() -> Dict[str, str]:
    structure = {}
    mapping = {}

    if os.path.isfile(config_file):
        with open(config_file) as stream:
            structure = yaml.safe_load(stream)

    logging.info(structure)

    for folder, extensions in structure.items():
        for ext in extensions:
            mapping[ext] = folder

    logging.info(mapping)

    return mapping
