# -*- coding: utf-8 -*-
import argparse


def args_parse():
    """
    Parse the arguments
    """
    parser = argparse.ArgumentParser(description="Generate a report from the test result")
    parser.add_argument(
        "--config",
        type=str,
        default="report_generator/configuration/config.json",
        help="The path to the configuration file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="test_results/test_report.docx",
        help="The path to the output file"
    )
    return parser.parse_args()
