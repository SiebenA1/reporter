"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages

from pathlib import Path
import re

from report_generator import version as vers


root_path = Path(__file__).parent.resolve()
excluded_packages = ["tests", "scripts"]

# initialize variables
package_source_folder = vers.package_name
package_version = vers.version
package_description = vers.description
package_author = vers.author
package_author_email = vers.author_email
repo_url = vers.repo_url


def get_requires(filename: Path) -> list[str]:
    """Get requirements from input file"""
    requirements = []
    with open(filename, "rt") as req_file:
        for line in req_file.read().splitlines():
            if not line.strip().startswith("#"):
                requirements.append(line)
    return requirements


def load_version() -> str:
    """ Loads a file content and parse semver """
    filename = root_path.joinpath(f"{package_source_folder}", "version.py")
    with open(filename, "rt") as version_file:
        version_module_str = version_file.read()
        version = re.search(r"version = '([0-9a-z.-]+)'", version_module_str).group(1)
        return version


def generate_long_description_file() -> str:
    """ Loads the README.md and convert to string"""
    with open(root_path.joinpath('README.md')) as f:
        long_description = f.read()
    return long_description


project_requirements = get_requires(root_path.joinpath("requirements", "requirements_project.txt"))


setup(
    name=f'{package_source_folder}',
    python_requires='>=3.11',
    version=package_version,

    description=package_description,
    long_description=generate_long_description_file(),
    long_description_content_type='text/markdown',

    # Author details
    author=package_author,
    author_email=package_author_email,

    # The project's main homepage.
    url=repo_url,

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Choose your license as you wish
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=excluded_packages),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=project_requirements,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # Note: uncomment entry_points if there is an executable file available
    # entry_points={
    #     'console_scripts': [
    #         f'{package_source_folder} = {package_source_folder}.__main__:main',
    #     ]
    # },
)
