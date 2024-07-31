# -*- coding: utf-8 -*-
"""A logger module for showing and collecting log
"""
import logging
from pathlib import Path
import sys
import time

import colorlog

from report_generator.common.settings_parser import SettingsParser


class Logger:
    """A log class for showing console log or saving log to logfile
    """
    def __init__(self, name: str, level: str, log_path: Path, save_logfile: bool = False) -> None:
        # create a logger instance
        self._logger = logging.Logger(name)
        # map the log level
        self._log_level = logging._nameToLevel[level.upper()]

        # create handler with if-statement to avoid multiple initialize
        if not self._logger.handlers:
            self._logger.addHandler(self._create_console_handler(self._log_level))
            if save_logfile:
                log_path.mkdir(parents=True, exist_ok=True)
                filename = f"{name}_{time.strftime('%Y%m%d_%H%M%S')}.log"
                self._logger.addHandler(self._create_file_handler(self._log_level, log_path.joinpath(filename)))

    @property
    def singleton_logger(self) -> logging.Logger:
        return self._logger

    def _create_console_handler(self, log_level: int) -> logging.StreamHandler:
        """To create a console handler with input log_level

        Parameters
        ----------
        log_level : int
            The output log level for logging

        Returns
        -------
        logging.StreamHandler
            A logging handler for console output
        """
        log_format = "%(asctime)s |%(log_color)s %(levelname)-8s | %(filename)s -> %(funcName)s:%(lineno)d - %(message)s"
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(colorlog.ColoredFormatter(fmt=log_format))
        console_handler.setLevel(log_level)

        return console_handler

    def _create_file_handler(self, log_level: int, logfile_path: Path) -> logging.FileHandler:
        """To create a logfile handler with input log_level

        Parameters
        ----------
        log_level : int
            The output log level for logging
        logfile_path : Path
            The output logfile with output path

        Returns
        -------
        logging.FileHandler
            A logging handler for logfile output
        """
        log_format = "%(asctime)s | %(levelname)-8s | %(filename)s -> %(funcName)s:%(lineno)d - %(message)s"
        file_handler = logging.FileHandler(filename=logfile_path, mode='w+', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(fmt=log_format))
        file_handler.setLevel(log_level)
        file_handler.close()

        return file_handler


def create_logger_instance(logger_config: dict) -> logging.Logger:
    """Create a new logger instance with new log level and save_log flag

    Parameters
    ----------
    logger_config : str
        The config dict for creating a logger instance

    Returns
    -------
    logging.Logger
        A new Logger instance

    Example
    -------
    logger_config: {
        name: "davviz",
        level: "debug",
        log_path: "Path to folder",
        save_logfile: True,
        disable_logger: False
    }
    """
    name = logger_config.get("name", "logger")
    level = logger_config.get("level", "debug")
    log_path = Path(logger_config.get("log_path", "logs"))
    save_logfile = logger_config.get("save_logfile", False)
    disable_logger = logger_config.get("disable_logger", False)

    logger = Logger(name=name, level=level, log_path=log_path, save_logfile=save_logfile)
    logger.singleton_logger.disabled = disable_logger

    return logger.singleton_logger


# create singleton logger instance
logger = create_logger_instance(SettingsParser(Path("config/application_settings.ini")).get("logger"))
