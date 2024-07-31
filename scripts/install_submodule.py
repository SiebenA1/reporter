# -*- coding: utf-8 -*-
"""
A module to install all submodules into site-packages
"""
import subprocess
from typing import List


def _update_submodules() -> None:
    """
    Update all submodules to their latest commit on the repository,
    printing the output in real-time.
    """
    print("[INFO] Updating submodules...")

    command_list = ['git', 'submodule', 'update', '--init', '--remote', '--recursive']
    with subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
        # Real-time output and print
        if process.stdout is not None:
            for line in process.stdout:
                print(line, end='')

    if process.returncode != 0:
        raise RuntimeError("[ERROR] Failed to update submodules.")

    print("[INFO] Submodules updated successfully.")


def _get_submodules() -> List[str]:
    """
    Get a list of all submodules in the current Git repository.

    Returns
    -------
    List[str]
        A list containing the paths of all submodules.
    """
    command_list = ['git', 'config', '--file', '.gitmodules', '--get-regexp', 'path']
    result = subprocess.run(command_list, capture_output=True, text=True)

    if not result.stdout:
        raise RuntimeError("[WARNING] No submodules found in current repository.")

    if result.returncode != 0:
        raise RuntimeError("[ERROR] Failed to get submodule list: " + result.stderr)

    submodule_paths = [line.split(' ')[1] for line in result.stdout.strip().split('\n') if line]

    return submodule_paths


def _install_submodule(submodule_path: str) -> None:
    """
    Install a submodule by running `pip install .` in its directory.

    Parameters
    ----------
    submodule_path : str
        The path to the submodule directory.

    Raises
    ------
    RuntimeError
        If the installation process fails.
    """
    with subprocess.Popen(['pip', 'install', '.'], cwd=submodule_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
        # Real-time output and print
        if process.stdout is not None:
            for line in process.stdout:
                print(line, end='')

    if process.returncode != 0:
        raise RuntimeError(f"[ERROR] Failed to install submodule at {submodule_path}")


def main() -> None:
    """
    Main function to find and install all submodules in the current Git repository.
    """
    try:
        submodule_paths = _get_submodules()
        print("[INFO] Found submodules:", submodule_paths)

        _update_submodules()

        for submodule_path in submodule_paths:
            print(f"[INFO] Installing submodule at {submodule_path}...")
            _install_submodule(submodule_path)
            print(f"[INFO] Successfully installed submodule at {submodule_path}.")

    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
