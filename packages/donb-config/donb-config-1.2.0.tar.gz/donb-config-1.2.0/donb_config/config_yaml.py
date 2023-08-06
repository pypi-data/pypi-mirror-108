# -*- coding: utf-8 -*-

"""
Defines :
 The ConfigYaml class.

"""
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


class ConfigYaml:

    """
    ConfigYaml uses Ruamel.Yaml to implement a version able to deal with
    PathObject.

    The actual yaml dictionary is stored under a .data attribute, and the value
    are converted to Path in the revised __getitem__ method. Calling
    config["some_path_key"] will return a Path object, but the value for the yaml
    object, accessible through config.data["some_path_key"] will still return
    the corresponding string.

    Parameters
    ----------
    config_file_path
        Path to the yaml config file.

    """

    def __init__(self, config_file_path: Path):
        self.config_file_path: Path = config_file_path
        yaml = YAML()
        self.data = yaml.load(self.config_file_path)

    def __getitem__(self, key: str) -> Any:
        value = self.data[key]
        if value.startswith("PathObject:"):
            value = Path(value[len("PathObject:") :])
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        if isinstance(value, Path):
            value = "PathObject:" + str(value.absolute())
        self.data[key] = value

    def save(self) -> None:
        """
        Saves values to the yaml file.

        The method keeps the eventual comments in the original file.
        """
        yaml = YAML()
        yaml.dump(self.data, self.config_file_path)
