# -*- coding: utf-8 -*-
"""
NOX configuration file for:
* lint
* test
* build
* doc
* deploy
* release
"""
import nox


_PROJECT_SRC_PATH: str = 'report_generator'
_PROJECT_TEST_PATH: str = 'tests'

nox.options.reuse_existing_virtualenvs = False
nox.options.no_install = False


@nox.session(python=False)
def lint(session: nox.Session) -> None:
    """Run the linting check."""
    print('[LINT] ----------- Run the linting check -----------')
    session.run('python', '-m', 'cicd.scripts.lint_check',
                '--folder-or-file-path', _PROJECT_SRC_PATH, _PROJECT_TEST_PATH, 'scripts', 'noxfile.py',
                '--config-file', 'pyproject.toml',
                '--lint-tool', 'all')


@nox.session(python=False)
def test(session: nox.Session) -> None:
    """Run the test suite."""
    print('[TEST] ----------- Run the test suite -----------')
    session.run('python', '-m', 'cicd.scripts.unittest_check',
                '--config-file', 'pyproject.toml',
                '--min-total-coverage=80')


@nox.session(python=False)
def install(session: nox.Session) -> None:
    """Install submodules into site-packages."""
    print('[INSTALL] ----------- Install the submodules -----------')
    session.run('python', '-m', 'scripts.install_submodule')


@nox.session
def build(session: nox.Session) -> None:
    """Run the package builder."""
    print('[BUILD] ----------- Run the package builder -----------')
    session.run('python', '-m', 'scripts.install_submodule')
    session.install('-r', './requirements/requirements_build.txt')

    session.run('python', '-m', 'scripts.build_delivery')


@nox.session(python=False)
def doc(session: nox.Session) -> None:
    """Create a documentation."""
    print('[DOC] ----------- Create a user documentation -----------')
    session.run('python', '-m', 'scripts.generate_api_doc')


@nox.session(python=False)
def deploy(session: nox.Session) -> None:
    """Deploy the package."""
    print('[DEPLOY] ----------- Deploy the package -----------')
    session.run('python', '-m', 'scripts.deploy_delivery')


@nox.session(python=False)
def release(session: nox.Session) -> None:
    """Full release session."""
    print('[RELEASE] ----------- Create a full release with doc, build and deploy -----------')

    session.notify('doc')
    session.notify('build')
    session.notify('deploy')


if __name__ == '__main__':
    raise NotImplementedError
