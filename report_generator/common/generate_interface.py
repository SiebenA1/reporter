# -*- coding: utf-8 -*-
import document
from docx import Document
from docx2pdf import convert

from report_generator.common.element_interface import GlobalSetupBuilder
from report_generator.common.section_interface import Section
from report_generator.compontent.global_setting_interface import set_global_formatting
from report_generator.compontent.settings import SETTINGS
from report_generator.common.logger import logger


class ReportGenerator:
    """
    Generate a report with sections
    """
    def __init__(self):
        """
        Initialize the report, clear the sections
        """
        self.sections = []

    def add_section(self, section: 'Section'):
        """
        Add a section to the report

        Parameters
        ----------
        section : Section
            Section to add to the report
        """
        self.sections.append(section)

    @staticmethod
    def global_setup(doc: document) -> None:
        """
        Global setup for the report

        Parameters
        ----------
        doc : Document
            Document object to set up
        """
        # Add headers and footers, and all the text content can be transferred from the parameters
        set_global_formatting(doc)
        left_header_text = SETTINGS.get('header_text')
        footer_text = SETTINGS.get('footer_text')
        middle_footer_text = SETTINGS.get('middle_footer_text')
        logo_path = SETTINGS.get('logo_path')
        builder = GlobalSetupBuilder(doc=doc,
                                     left_header_text=str(left_header_text),
                                     footer_text=str(footer_text),
                                     middle_footer_text=str(middle_footer_text),
                                     image_path=logo_path if logo_path else None)
        builder.header_render(doc).footer_render(doc)
        logger.info("Initialize the global setup for the report.")

    def generate(self, path: str):
        """
        Generate the report to the path

        Parameters
        ----------
        path : str
            Path to save the report
        """
        doc = Document()
        logger.info("Initialize the document.")
        self.global_setup(doc)
        logger.info("Global setup for the document is done.")
        for section in self.sections:
            section.render(doc)
        logger.info("Render all sections to the document.")
        # Save the document as a docx file
        doc.save(path)
        logger.info("Save the document as a docx file.")
        # Convert the docx file to PDF
        convert(path)
        logger.info("Convert the docx file to PDF.")
