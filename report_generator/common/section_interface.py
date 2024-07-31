# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Dict

from document import Document

from report_generator.common.element_interface import (Title, Paragraph, Image, NormalTextFormat,
                                                       PositiveStatusTextFormat, NegativeStatusTextFormat, Tables)
from report_generator.compontent.global_setting_interface import insert_page_break
from report_generator.common.logger import logger


class Section:
    """
    Base class for all sections in the document
    """

    def __init__(self):
        self.elements = []

    def add_element(self, element: object) -> None:
        """
        Add an element to the section

        Parameters
        ----------
        element : object
            Element to add to the section
        """
        self.elements.append(element)

    def render(self, document: Document) -> None:
        """
        Render the section

        Parameters
        ----------
        document : Document
            Document object to render the section
        """
        for element in self.elements:
            element.render(document)
        insert_page_break(document)


class CaseSection(Section):
    """
    Case section
    """

    def __init__(self, section_dict: dict) -> None:
        """
        Initialize the CaseSection class according to the individual case section requirements in your report.

        Parameters
        ----------
        section_dict : dict
            Dictionary containing the case section information
        """
        super().__init__()
        self.title = section_dict.get("title", "")
        self.result = section_dict.get("result", "")
        self.info = self._format_info(section_dict.get("settings", {}))
        self.condition_result = section_dict.get("condition_result", {})
        self.image_path = section_dict.get("image_path", Path())
        logger.info(f"Initialize a CaseSection for case {self.title}")

    def create_section(self) -> None:
        """
        Create a case section from a dictionary
        """
        self.add_element(Title(text=self.title, level=1))
        if self.result == "PASSED":
            self.add_element(Paragraph(title='', text=self.result, text_format=PositiveStatusTextFormat()))
        elif self.result == "FAILED":
            self.add_element(Paragraph(title='', text=self.result, text_format=NegativeStatusTextFormat()))
        self.add_element(Paragraph(title='Test-Settings', text=self.info, text_format=NormalTextFormat()))
        self.add_element(Tables(condition_result=self.condition_result))
        self.add_element(Image(case_name=self.title, image_path=self.image_path))
        logger.info(f"Create a CaseSection for case {self.title}")

    @staticmethod
    def _format_info(info: Dict[str, str]) -> str:
        """
        Format the information to a string

        Parameters
        ----------
        info : Dict[str, str]
            Information

        Returns
        -------
        str
            Formatted information
        """
        logger.info("Format the settings information to a string.")
        return ", ".join([f"{key}: {value}" for key, value in info.items()])
