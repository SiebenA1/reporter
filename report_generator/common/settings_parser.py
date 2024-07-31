# -*- coding: utf-8 -*-
"""A module for handling global settings for this tool
"""
import ast
import configparser
from pathlib import Path
import threading
from typing import Any, overload


class MultiSingletonMeta(type):
    """Multi Singleton Metaclass."""
    _instances: dict = {}
    _instance_lock: threading.Lock = threading.Lock()

    def __call__(cls, key, *args, **kwargs):
        if key not in cls._instances:
            with cls._instance_lock:
                if key not in cls._instances:
                    instance = super().__call__(key, *args, **kwargs)
                    cls._instances[key] = instance

        return cls._instances[key]


class SettingsParser(metaclass=MultiSingletonMeta):
    """A customized parser for settings file, inline comment is supported.

    Default comment prefixes are '#' and ';'
    """
    def __init__(self, settings_file: Path):
        self._parser = configparser.RawConfigParser(inline_comment_prefixes=("#", ";"))
        self.settings_file = settings_file

    @property
    def settings_file(self) -> Path:
        """A getter property for input settings_file

        Returns
        -------
        Path
            The path to settings file
        """
        return self._settings_file

    @settings_file.setter
    def settings_file(self, settings_file: Path) -> None:
        """The setter for settings_file attribute

        Parameters
        ----------
        settings_file : Path
            The input path of settings file
        """
        if not settings_file.is_file():
            raise FileNotFoundError(f"The input settings file '{settings_file}' does not exist.")

        self._settings_file = settings_file
        self._parser.read(self._settings_file)

    @property
    def sections(self) -> list[str]:
        """A getter property to get all sections of settings file

        Returns
        -------
        list[str]
            A list of sections of settings file
        """
        return self._parser.sections()

    @overload
    def get(self, section: str) -> dict:
        """To get all key-value pairs from settings file

        Parameters
        ----------
        section : str
            The section in settings file

        Returns
        -------
        dict
            All kv-pairs of input section
        """
        ...

    @overload
    def get(self, section: str, option: str, default: Any | None = None) -> str | Any:
        """To get the value of input section and option

        Parameters
        ----------
        section : str
            The section of settings file
        option : str
            The option of input section
        default : Any | None
            The default value of option if it is not defined, by default None

        Returns
        -------
        str | Any
            The option value of input section
        """
        ...

    def get(self, section: str, option: str = "", default: Any | None = None) -> dict | str | Any:
        """To get the kv-pairs of section or option value from settings file

        Parameters
        ----------
        section : str
            The section in settings file
        option : str, optional
            The option of input section, by default ""
        default : Any | None, optional
            The default value of option if it is not defined, by default None

        Returns
        -------
        dict | str | Any
            The kv-pairs dict of section and option value
        """
        if self._parser.has_section(section):
            kv_pairs = self._convert_dict_string_value({k: v for k, v in self._parser.items(section)})
        else:
            kv_pairs = {}

        if not option:
            return kv_pairs

        option_value = kv_pairs.get(option, default)

        return option_value

    @staticmethod
    def _convert_dict_string_value(kv_dict: dict) -> dict:
        """To convert string to int or float or bool

        Parameters
        ----------
        kv_dict : dict
            The config dict parsed from settings file

        Returns
        -------
        dict
            A dict after converted
        """
        new_kv_dict = {}
        for k in kv_dict.keys():
            try:
                # Handle boolean values as special case
                if kv_dict[k].lower() == 'true':
                    new_kv_dict[k] = True

                elif kv_dict[k].lower() == 'false':
                    new_kv_dict[k] = False

                else:
                    # Use literal_eval to handle int and float
                    new_kv_dict[k] = ast.literal_eval(kv_dict[k])

            except (ValueError, SyntaxError):
                # keep original value
                new_kv_dict[k] = kv_dict[k]

        return new_kv_dict
