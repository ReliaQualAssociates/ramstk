# -*- coding: utf-8 -*-
"""``RAMSTK`` lives on `GitHub.

<https://github.com/ReliaQualAssociates/ramstk>`_.
"""

# Standard Library Imports
import os
import sys

# Third Party Imports
from setuptools import find_packages, setup
from setuptools.command.install import install as _install
from setuptools.command.sdist import sdist
from setuptools.command.test import test

# Codes to allow colored outputs.
RESET = '\033[0m'
BOLD = '\033[01m'
FG_RED = '\033[31m'
FG_GREEN = '\033[32m'
FG_YELLOW = '\033[93m'
BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
    ====================================
    Unsupported Python Version Detected!
    ====================================

    What a bunch of malarkey!  RAMSTK
    requires Python >= {}.{}, but we've
    detected Python {}.{}.

    """.format(*REQUIRED_PYTHON + CURRENT_PYTHON))
    sys.exit(1)

HERE = os.path.abspath(os.path.dirname(__file__))
# Read the contents of the VERSION file.
with open(os.path.join(HERE, 'VERSION'), encoding='utf-8') as f:
    RAMSTK_VERSION = f.read()

# Read the contents of the README file.
with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    __long_description__ = f.read()

__appname__ = 'RAMSTK'
__version__ = RAMSTK_VERSION
__author__ = "Doyle 'weibullguy' Rowland"
__email__ = "doyle.rowland@reliaqual.com"
__trove__ = [
    'Development Status :: 4 - Beta',
    'Environment :: X11 Applications :: GTK',
    'Intended Audience :: Other Audience',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Education',
    'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
    'Typing :: Typed',
]

# Lists of required packages for RAMSTK.
_req_file = open('requirements.in', 'r')
INSTALL_REQUIRES = _req_file.read().splitlines()
_req_file.close()

_req_file = open('requirements-test.in', 'r')
TEST_REQUIRES = _req_file.read().splitlines()
_req_file.close()

# Build lists of data files to install.
_path = HERE + '/data/'
DATA_FILES = [
    _path + f for f in os.listdir(_path) if os.path.isfile(_path + f)
]
_path = HERE + '/data/layouts/'
LAYOUT_FILES = [
    _path + f for f in os.listdir(_path) if os.path.isfile(_path + f)
]
_path = HERE + '/data/icons/16x16/'
ICON16_FILES = [
    _path + f for f in os.listdir(_path) if os.path.isfile(_path + f)
]
_path = HERE + '/data/icons/32x32/'
ICON32_FILES = [
    _path + f for f in os.listdir(_path) if os.path.isfile(_path + f)
]


class Install(_install):
    """Custom install class for RAMSTK."""
    @staticmethod
    def pre_install_script() -> None:
        """Execute before install."""
        _eggfile = os.path.abspath('.') + '/src/RAMSTK.egg-info'
        print("{0}Removing old rotten RAMSTK egg...{1}".format(
            FG_YELLOW, RESET))
        try:
            if os.path.isfile(_eggfile):
                os.unlink(_eggfile)
        except Exception as _error:  # pylint: disable=broad-except
            print(_error)

    @staticmethod
    def post_install_script() -> None:
        """Execute after install."""
        print("{0}{1}Your shiny new RAMSTK-{2} is "
              "installed!!{3}".format(FG_GREEN, BOLD, __version__, RESET))

    def run(self) -> None:
        """Run the install."""
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()


class Sdist(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created."""
    def run(self) -> None:
        """Run custom sdist command."""
        try:
            self.run_command('compile_catalog')
        except Exception as _error:  # pylint: disable=broad-except
            print(_error)
            print('No messages catalogs found.')

        sdist.run(self)


class MyTest(test):
    """Custom ``test`` command to tell the user to use make test."""
    def run(self) -> None:
        """Run the custom test command."""
        print("{0}{1}Running tests using setup.py is not supported.  "
              "Please execute tests using the Makefile.  Issue make help for "
              "options.{2}".format(FG_RED, BOLD, RESET))


if __name__ == '__main__':
    setup(name=__appname__,
          version=__version__,
          description="The RAMS ToolKit (RAMSTK) is a suite of tools for "
                      "performing and documenting reliability, availability, "
                      "maintainability, and safety (RAMS) analyses",
          long_description=__long_description__,
          long_description_content_type='text/markdown',
          author=__author__,
          author_email=__email__,
          license='BSD-3',
          url='https://github.com/ReliaQualAssociates/ramstk',
          python_requires='>=3.6, <4',
          install_requires=INSTALL_REQUIRES,
          setup_requires=['pytest_runner', 'Babel'],
          tests_require=TEST_REQUIRES,
          keywords='''reliability availability maintainability safety RAMS
        engineering quality''',
          scripts=[],
          packages=find_packages('src', exclude=['tests']),
          package_dir={'': 'src'},
          py_modules=[
              'ramstk.configuration', 'ramstk.exceptions', 'ramstk.logger',
              'ramstk.ramstk', 'ramstk.utilities'
          ],
          data_files=[
              ('share/applications', ['data/RAMSTK.desktop']),
              ('share/pixmaps', ['data/icons/RAMSTK.ico']),
              ('share/pixmaps', ['data/icons/RAMSTK.png']),
              ('share/RAMSTK', DATA_FILES),
              ('share/RAMSTK/layouts', LAYOUT_FILES),
              ('share/RAMSTK/icons/16x16', ICON16_FILES),
              ('share/RAMSTK/icons/32x32', ICON32_FILES),
          ],
          classifiers=__trove__,
          entry_points={
              'console_scripts': ['ramstk = ramstk.__main__:the_one_ring'],
              'gui_scripts': ['ramstk = ramstk.__main__:the_one_ring']
          },
          dependency_links=[],
          zip_safe=True,
          cmdclass={
              'install': Install,
              'sdist': Sdist,
              'test': MyTest,
          })
