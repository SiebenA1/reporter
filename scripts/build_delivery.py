# -*- coding: utf-8 -*-
"""
Call pypacker to build a delivery item of the current project.
"""
import time

from pypacker.__main__ import main as pypacker_main

from report_generator import version as vers


def main() -> None:
    """Main function of the build script."""
    version_extension = vers.version

    if vers.enable_draft:
        current_date = time.strftime("%Y%m%d")
        version_extension += f'_{current_date}_draft'

    # FIXME: make config path as an input parameter
    pypacker_config_path = "pypacker_configuration.json"

    pypacker_main([
        '--config', pypacker_config_path,
        '--version-extension', version_extension
    ])


if __name__ == '__main__':
    main()
