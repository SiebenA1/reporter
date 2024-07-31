# -*- coding: utf-8 -*-
"""
A script to check if the merge request has a valid jira ticket for
CN-TV-A jira project
"""

import argparse
from enum import Enum
import os
import re
import sys


class ExitCode(Enum):
    CI_PIPELINE_SOURCE_ERROR = 100
    MERGE_REQUEST_TITLE_ERROR = 200
    MERGE_REQUEST_DESCRIPTION_ERROR = 300


def argparser(args: list | None = None) -> argparse.Namespace:
    """An argument parser for MR guard

    Parameters
    ----------
    args : list, optional
        The input arguments when run script

    Returns
    -------
    argparse.Namespace
        The Namespace of argument parser
    """
    parser = argparse.ArgumentParser(description="An argument parser for mr guard of cn-tv-a project")
    parser.add_argument('--jira-resource-name', type=str, required=True,
                        help="The jira resource name for checking merge request title and description.")
    return parser.parse_args(args)


def validate_ci_pipeline_source() -> None:
    """To validate if it is a merge_request pipeline
    """
    print(f"[CHECK] Start to check ci pipeline source.")

    ci_pipeline_id = os.getenv("CI_PIPELINE_ID")
    if ci_pipeline_id is None:
        exit_script_with_msg(ExitCode.CI_PIPELINE_SOURCE_ERROR.value,  "the running environment is not a ci pipeline")

    ci_pipeline_source = os.getenv("CI_PIPELINE_SOURCE", "")
    if ci_pipeline_source != "merge_request_event":
        exit_script_with_msg(ExitCode.CI_PIPELINE_SOURCE_ERROR.value, f"ci pipeline source '{ci_pipeline_source}' is not from a merge request")
    
    print(f"[Passed] CI_PIPELINE_SOURCE = {ci_pipeline_source}")


def validate_mr_title(jira_resource_name: str) -> None:
    """To validate if jira resource name is in mr title

    Parameters
    ----------
    jira_resource_name : str
        The jira resource name in iav jira
    """
    print(f"[CHECK] Start to check jira ticket number in merge_request title.")

    mr_title = os.getenv("CI_MERGE_REQUEST_TITLE", "").strip()

    if not re.match(fr"{jira_resource_name}-\d+", mr_title):
        exit_script_with_msg(ExitCode.MERGE_REQUEST_TITLE_ERROR.value, f"merge request title does not contain jira ticket number, title: {mr_title}")
    
    print(f"[Passed] CI_MERGE_REQUEST_TITLE = {mr_title}")


def validate_mr_description(jira_resource_name: str) -> None:
    """To validate if jira ticket link is in mr description

    Parameters
    ----------
    jira_resource_name : str
        The jira resource name in iav jira
    """
    print(f"[CHECK] Start to check jira ticket link in merge_request description.")

    mr_description = os.getenv("CI_MERGE_REQUEST_DESCRIPTION", "")
    jira_ticket_link_pattern = re.compile(fr"https://jira.iavgroup.local/browse/{jira_resource_name}-\d+")

    if not jira_ticket_link_pattern.search(mr_description):
        exit_script_with_msg(ExitCode.MERGE_REQUEST_DESCRIPTION_ERROR.value,
                             f"merge request description does not contain jira ticket link, description: {mr_description}")
    
    print(f"[Passed] CI_MERGE_REQUEST_DESCRIPTION = {mr_description}")


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
    main script to run mr guard logic
    """
    args = argparser(sys.argv[1:])
    print(f"Jira resource name: {args.jira_resource_name}\n")
    
    validate_ci_pipeline_source()

    validate_mr_title(args.jira_resource_name)
    validate_mr_description(args.jira_resource_name)


if __name__=="__main__":
    main()
