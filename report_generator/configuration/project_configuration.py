# -*- coding: utf-8 -*-
from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass
class ProjectConfiguration:
    """The configuration of current project

    The root path is different when the current project is running as a binary or as a script.
    So we need to define two different project paths for different running environments.

    Usage:
    ---
    from project_configuration import ProjectConfiguration


    project_path = ProjectConfiguration.PROJECT_PATH
    """
    # Running as compiled binary else as script
    PROJECT_PATH: Path = Path(sys.argv[0]).resolve().parent if getattr(sys, 'frozen', True) else Path(__file__).parent.parent.parent
    DEFAULT_CONFIG_FILE: Path = PROJECT_PATH.joinpath("config/template_settings.ini")
