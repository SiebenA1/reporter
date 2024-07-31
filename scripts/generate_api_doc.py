# -*- coding: utf-8 -*-
"""
Create a user documentation from markdown files and docstrings.
"""
from pathlib import Path
import shutil
import subprocess

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

from report_generator import version as vers


def _create_markdown_to_html() -> None:
    """This is the function to create a user documentation from markdown files to html format."""
    print('[DOC] --- MarkdownIt -----------')
    print('[DOC]  Create an user documentation from markdown files')

    md = (
        MarkdownIt('commonmark', {'breaks': True, 'html': True, 'linkify': True, 'typographer': True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable(['table', 'link', 'image'])
    )

    readme_file: Path = Path('README').with_suffix('.md')
    readme_text = readme_file.read_text(encoding='utf-8')
    html_text = md.render(readme_text)
    readme_file.with_suffix('.html').write_text(html_text, encoding='utf-8')
    shutil.move(readme_file.with_suffix('.html'), f"doc/{readme_file.with_suffix('.html')}")

    changelog_file: Path = Path('CHANGELOG').with_suffix('.md')
    changelog_text = changelog_file.read_text(encoding='utf-8')
    html_text = md.render(changelog_text)
    changelog_file.with_suffix('.html').write_text(html_text, encoding='utf-8')
    shutil.move(changelog_file.with_suffix('.html'), f"doc/{changelog_file.with_suffix('.html')}")


def _create_api_documentation() -> None:
    """This is the function to create an api documentation in html format.
    - clean up previous doc to avoid FileExistsError
    - create new api doc from 'report_generator' directory
    - rename to project
    """
    print('[DOC] ----------- pdoc -----------')
    print('[DOC]  Create an api documentation')

    # clean up
    pdoc_results_path = Path(f'doc/{vers.package_name}')
    if pdoc_results_path.exists() and pdoc_results_path.is_dir():
        shutil.rmtree(pdoc_results_path)

    # create api docu
    subprocess.run([
        'pdoc',
        '--html',
        '--config', 'show_source_code=False',
        '--force',
        '--skip-errors',
        '--output-dir', './doc',
        f'{vers.package_name}'], check=False)

    # rename to project
    if vers.package_name:
        api_docu_path = Path(f"{pdoc_results_path}_api_docu")
        if api_docu_path.exists():
            shutil.rmtree(api_docu_path)

        pdoc_results_path.rename(api_docu_path)


def main() -> None:
    """This is the main function to create a user documentation."""
    _create_markdown_to_html()
    _create_api_documentation()


if __name__ == '__main__':
    main()
