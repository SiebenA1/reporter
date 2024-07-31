# -*- coding: utf-8 -*-
"""
A module to check lint of scripts from input folders
"""
import argparse
import sys
import subprocess
import traceback


def argparser(args: list | None = None) -> argparse.Namespace:
    """An argument parser for lint check

    Parameters
    ----------
    args : list, optional
        The input arguments when run script

    Returns
    -------
    argparse.Namespace
        The Namespace of argument parser
    """
    parser = argparse.ArgumentParser(description="An argument parser for lint check of cn-tv-a project")
    parser.add_argument('--folder-or-file-path', type=str, required=True, nargs="+",
                        help="The path to folders contain python scripts or directly a python script.")
    parser.add_argument('--config-file', type=str, required=True,
                        help="Path to pyproject.toml configuration file.")
    parser.add_argument('--lint-tool', type=str, default='all', choices=['all', 'mypy', 'pylint', 'flake8'],
                        help="To select which lint checking tool will be run. (default: all)")
    return parser.parse_args(args)


def run_command(command: list[str]) -> None:
    """The command in string format

    Parameters
    ----------
    command : list[str]
        A command line in list format
    """
    try:
        retcode = subprocess.call(command)
    except Exception:
        retcode = 100
        print(traceback.format_exc())

    if retcode != 0:
        print(f"[EXIT] exit code: {retcode}, command failed: {' '.join(command)}")
        sys.exit(retcode)


def mypy_lint_check(files: list[str], config_file: str) -> None:
    """To check lint with mypy

    Parameters
    ----------
    files : list[str]
        The folder path or file path of python scripts
    config_file : str
        Path to pyproject.toml config file
    """
    print('[LINT] ----------- MyPy -----------')
    print(' Silencing - Globally: options in pyproject.toml; Local: Comment behind '
          '# type: ignore or type: ignore[code, ...]')
    # https://mypy.readthedocs.io/en/stable/config_file.html
    # https://mypy.readthedocs.io/en/stable/error_codes.html?#silencing-errors-based-on-error-codes

    for file in files:
        command = ['mypy', '--config-file', config_file, file]
        run_command(command)

    print('[LINT] Lint checking with mypy succeed.\n')
        

def pylint_lint_check(files: list[str], config_file: str) -> None:
    """To check lint with pylint

    Parameters
    ----------
    files : list[str]
        The folder path or file path of python scripts
    config_file : str
        Path to pyproject.toml config file
    """
    print('[LINT] ----------- PyLint -----------')
    print('Silencing - Globally: disable=... in pyproject.toml; Local: Comment behind # pylint: disable=...')

    for file in files:
        command = ['pylint', '--exit-zero', '--rcfile', config_file, file]
        run_command(command)

    print('[LINT] Lint checking with pylint succeed.\n')


def flake8_lint_check(files: list[str], config_file: str) -> None:
    """To check lint with flake8

    Parameters
    ----------
    files : list[str]
        The folder path or file path of python scripts
    config_file : str
        Path to pyproject.toml config file
    """
    print('[LINT] ----------- Flake8 -----------')
    print(' Silencing - Globally: disable=... in pyproject.toml; Locally: Comment behind # noqa: E731')
    # https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html
    # nox flake8 is not working with pyproject.toml file

    for file in files:
        # command = f"flake8 --max-line-length 150 --extend-ignore W292,W503 E402 --max-complexity 12 {file}"
        command = ['flake8', '--toml-config', config_file, file]
        run_command(command)

    print('[LINT] Lint checking with flake8 succeed.\n')


def exit_script_with_msg(exit_code: int, msg: str = "") -> None:
    """Exit script with a code and print message

    Parameters
    ----------
    exit_code : int
        The eixt code for an abnormal case
    msg: str, optional
        The message for an abnormal case
    """
    print(f"[EXIT] exit code: {exit_code}, {msg}")
    sys.exit(exit_code)


def main() -> None:
    """
    main script to run lint check functions
    """
    args = argparser(sys.argv[1:])

    lint_check_func = {
        'mypy': mypy_lint_check,
        'pylint': pylint_lint_check,
        'flake8': flake8_lint_check
    }

    if args.lint_tool == 'all':
        for func in lint_check_func.values():
            func(args.folder_or_file_path, args.config_file)

    elif args.lint_tool in lint_check_func:
        lint_check_func[args.lint_tool](args.folder_or_file_path, args.config_file)

    else:
        print(f"[EXIT] exit code: {100}, {args.lint_tool} lint tool is not supported.")
        sys.exit(100)


if __name__=='__main__':
    main()
