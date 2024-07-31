# -*- coding: utf-8 -*-
"""Main script of current project"""
from report_generator.common.section_interface import CaseSection
from report_generator.common.generate_interface import ReportGenerator
from report_generator.module.args_parse import args_parse


def main():
    args = args_parse()
    doc_gen = ReportGenerator()
    item_list = [
        {
            "title": "CCRs_AEB_test_case_1",
            "result": "PASSED",
            "settings": {"gvt": "30km/h", "ol": "-50%", "vut": "20km/h"},
            "condition_result": {
                "file1": [(['external_relative_longitudinal_distance > 0', 'all'], True)],
                "file2": [(['external_relative_longitudinal_distance > 0', 'all'], True)]
            },
            "image_path": "tests/data_and_request/image_index.json"
        },
        {
            "title": "CCRs_AEB_test_case_2",
            "result": "FAILED",
            "settings": {"gvt": "30km/h", "ol": "-50%", "vut": "30km/h"},
            "condition_result": {
                "file1": [(['external_relative_longitudinal_distance > 0', 'all'], False)],
                "file2": [(['external_relative_longitudinal_distance > 0', 'all'], False)]
            },
            "image_path": "tests/data_and_request/image_index.json"
        }
    ]
    for item in item_list:
        case_section = CaseSection(item)
        case_section.create_section()
        doc_gen.add_section(case_section)
        doc_gen.generate(args.output)


if __name__ == "__main__":
    main()
