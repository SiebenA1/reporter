# -*- coding: utf-8 -*-
"""
A module to run unittest by pytest and output the coverage
"""
import argparse
import os
import sys
import subprocess
import traceback


def argparser(args: list | None = None) -> argparse.Namespace:
    """An argument parser for unittest

    Parameters
    ----------
    args : list, optional
        The input arguments when run script

    Returns
    -------
    argparse.Namespace
        The Namespace of argument parser
    """
    parser = argparse.ArgumentParser(description="An argument parser for unittest of cn-tv-a project")
    parser.add_argument('--config-file', type=str, required=True,
                        help="Path to pyproject.toml configuration file.")
    parser.add_argument('--min-total-coverage', type=float, default=80,
                        help="The minimum coverage of all unittest in percentage, which can be an integer of float number. (default: 80)")
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


def run_unittest(config_file: str) -> None:
    """To run the unittest with pytest and calculate the coverage

    Parameters
    ----------
    config_file : str
        Path to pyproject.toml config file
    """
    print('[TEST] ----------- PyTest -----------')
    run_command(['coverage', 'erase'])
    run_command(['coverage', 'run', f'--rcfile={config_file}', '-m', 'pytest', '-c', config_file])


def check_total_coverage(config_file: str, min_total_coverage: int | float) -> None:
    """To check if the total coverage is great than minimum coverage

    Parameters
    ----------
    config_file : str
        Path to pyproject.toml config file
    min_total_coverage : int | float
        The minimum coverage for unittest
    """
    print('[TEST] ----------- Coverage -----------')
    run_command(['coverage', 'xml', f'--rcfile={config_file}'])
    run_command(['coverage', 'report', f'--rcfile={config_file}', f'--fail-under={min_total_coverage}'])


def main() -> None:
    """
    main script to run unittest
    """
    args = argparser(sys.argv[1:])

    run_unittest(args.config_file)
    check_total_coverage(args.config_file, args.min_total_coverage)


if __name__=="__main__":
    main()
