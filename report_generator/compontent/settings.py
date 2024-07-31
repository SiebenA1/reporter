# -*- coding: utf-8 -*-
import json

from report_generator.module.args_parse import args_parse

SETTINGS: dict = {}
TEXT_FORMAT: dict = {}
args = args_parse()


def parse_config_file(config_path: str):
    """
    Parse the configuration file to fill the settings
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    for key, value in config["SETTINGS"].items():
        SETTINGS[key] = value
    for key, value in config["TEXT_FORMAT"].items():
        TEXT_FORMAT[key] = value


parse_config_file(args.config)
