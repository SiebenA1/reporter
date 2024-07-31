# -*- coding: utf-8 -*-
"""
Deploys the final build delivery item to gitlab repo.
"""
import os
from pathlib import Path
import subprocess

from report_generator import version as vers

# FIXME: move to the global settings in the future
GIT_PACKAGE_REGISTRY_PATH: str = "https://gitlab.iavgroup.local/api/v4/projects/17657/packages/generic"
LOCAL_DRIVE_FOLDER_PATHS: list[Path] = [
    # TODO: Add folder path you want to upload
]


def _check_for_iav_gitlab_access_settings() -> None:
    """Check if all of required user environment variables are defined.
    Raise an error if not."""
    if not os.getenv('IAV_GITLAB_API_NAME'):
        raise KeyError("[DEPLOY][ERROR] user environment variable \'IAV_GITLAB_API_NAME\' not defined")
    if not os.getenv('IAV_GITLAB_API_TOKEN'):
        raise KeyError("[DEPLOY][ERROR] user environment variable \'IAV_GITLAB_API_TOKEN\' not defined")


def _get_releases_to_deploy(release_file_log_path: Path) -> list:
    """Get a list of available release for deployment.

    Parameters
    ----------
    release_file_log_path: Path
        The path to the delivery log directory where an information about releases is saved.

    Returns
    -------
        A list with available release information files.
    """
    if not release_file_log_path.exists():
        raise ValueError(f"[DEPLOY][ERROR] no delivery item folder available - {release_file_log_path}")

    release_file_list: list = list(release_file_log_path.glob("*.release"))
    if not release_file_list:
        raise ValueError(f"[DEPLOY][ERROR] no *.release files available in delivery item folder - {release_file_log_path}")

    return release_file_list


def main() -> None:
    """This is the main function to deploy a delivery item."""
    if os.getenv('GITLAB_CI'):
        raise NotImplementedError("[DEPLOY][ERROR] CICD not supported")

    print('[DEPLOY] --- curl -----------', flush=True)
    print('[DEPLOY] Locally upload the build release to gitlab package registry with curl.', flush=True)
    _check_for_iav_gitlab_access_settings()

    release_file_log_path: Path = Path(os.getcwd()).joinpath("delivery").joinpath("logs")
    release_file_list: list = _get_releases_to_deploy(release_file_log_path)

    flag_release_found: bool = False
    for release_file in release_file_list:
        print("[DEPLOY][DEBUG]", release_file)
        if not str(release_file.name).startswith(f"{vers.package_name}_"):
            continue
        if f"_v{vers.version.replace('.', '')}_" not in release_file.name:
            continue

        delivery_item: Path = Path(os.getcwd()).joinpath("delivery").joinpath(Path(release_file).stem).with_suffix(
            '.zip')
        print("[DEPLOY][DEBUG]", delivery_item)
        if not delivery_item.exists():
            raise ValueError(f"[DEPLOY][ERROR] delivery item not exists - {delivery_item}")
        flag_release_found = True

        print("[DEPLOY] upload file -", delivery_item)
        deploy_result_file: Path = release_file_log_path.joinpath(delivery_item.name).with_suffix('.deploy')
        subprocess.run([
            'curl',
            '--user', f"{os.getenv('IAV_GITLAB_API_NAME')}:{os.getenv('IAV_GITLAB_API_TOKEN')}",
            '--cacert', rf'{os.getcwd()}\setup\cacert_mozilla_iav.crt',
            '--upload-file', f'{delivery_item}',
            '--output', f"{deploy_result_file}",
            f"https://gitlab.iavgroup.local/api/v4/projects/17657/packages/generic/"
            f"{vers.package_name}/"
            f"v{vers.version}/"
            f"{delivery_item.name}"
        ], check=False)

        if not deploy_result_file.exists():
            raise ValueError(f"[DEPLOY][ERROR] deploy results not exists - {deploy_result_file}")
        if '{"message":"201 Created"}' not in deploy_result_file.read_text(encoding='utf-8'):
            raise ValueError("[DEPLOY][ERROR] upload failed")
        print("[DEPLOY] successfully finished")
        break

    if not flag_release_found:
        raise ValueError("[DEPLOY][ERROR] no found release match to defined version")


if __name__ == '__main__':
    main()
