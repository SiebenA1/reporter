# -*- coding: utf-8 -*-
"""A test module for dummy test"""
from report_generator import version as vers


class TestDemo:
    def test_dummy_function_passed(self) -> None:
        """An example test function based on pytest"""
        print(vers.version)
        succeed = True
        assert succeed

    def test_dummy_function_failed(self) -> None:
        """An example test function based on pytest"""
        print(vers.repo_url)
        succeed = False
        assert not succeed
