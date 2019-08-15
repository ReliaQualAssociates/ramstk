# -*- coding: utf-8 -*-
"""``RAMSTK`` lives on `GitHub <https://github.com/ReliaQualAssociates/ramstk>`_."""

# Standard Library Imports
import glob
import os

# Third Party Imports
from setuptools import find_packages, setup
from setuptools.command.install import install as _install
from setuptools.command.sdist import sdist
from setuptools.command.test import test

# Read the contents of your README file
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    __long_description__ = f.read()

__appname__ = 'RAMSTK'
__version__ = '1.0.4'
__author__ = "Doyle 'weibullguy' Rowland"
__email__ = "doyle.rowland@reliaqual.com"
__trove__ = [
    'Development Status :: 4 - Beta',
    'Environment :: Win32 (MS Windows)',
    'Environment :: X11 Applications :: GTK',
    'Intended Audience :: Other Audience',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
]

# Lists of required packages for RAMSTK.
INSTALL_REQUIRES = [
    'defusedxml', 'lifelines<15.0', 'matplotlib', 'numpy', 'openpyxl',
    'pandas', 'pycairo', 'PyGObject>=3.27', 'PyPubSub', 'scipy',
    'sortedcontainers', 'SQLAlchemy>=1.3.0', 'SQLAlchemy-Utils', 'statsmodels',
    'sympy', 'treelib>=1.5.3', 'xlrd', 'xlsxwriter', 'xlwt'
]
TEST_REQUIRES = ['pytest', 'pytest-cov', 'coveralls', 'codacy-coverage']

# Build lists of data files to install.
LAYOUT_FILES = []
for directory in glob.glob('data/layouts/'):
    files = glob.glob(directory + '*')
    LAYOUT_FILES.append(files)

ICON16_FILES = []
for directory in glob.glob('data/icons/16x16/'):
    files = glob.glob(directory + '*')
    ICON16_FILES.append(files)

ICON32_FILES = []
for directory in glob.glob('data/icons/32x32/'):
    files = glob.glob(directory + '*')
    ICON32_FILES.append(files)

# Codes to allow colored outputs.
RESET = '\033[0m'
BOLD = '\033[01m'
FG_RED = '\033[31m'
FG_GREEN = '\033[32m'
FG_YELLOW = '\033[93m'
BG_BLACK = '\033[40m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'


class Install(_install):
    """Custom install class for RAMSTK."""
    @staticmethod
    def pre_install_script():
        """Execute before install."""
        _eggfile = os.path.abspath('.') + '/src/RAMSTK.egg-info'
        print("{0:s}Removing old rotten RAMSTK egg...{1:s}".format(
            FG_YELLOW, RESET))
        try:
            if os.path.isfile(_eggfile):
                os.unlink(_eggfile)
        except Exception as _error:  # pylint: disable=broad-except
            print(_error)

    @staticmethod
    def post_install_script():
        """Execute after install."""
        print(
            "{0:s}{1:s}Your shiny new RAMSTK-{2:s} is "
            "installed!!{3:s}".format(FG_GREEN, BOLD, __version__, RESET))

    def run(self):
        """Run the install."""
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()


class Sdist(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created."""
    def run(self):
        """Run custom sdist command."""
        try:
            self.run_command('compile_catalog')
        except Exception as _error:  # pylint: disable=broad-except
            print(_error)
            print('No messages catalogs found.')

        sdist.run(self)


class MyTest(test):
    """Custom ``test`` command to tell the user to use make test."""
    def run(self):
        """Run the custom test command."""
        print("{0:s}{1:s}Running tests using setup.py is not supported.  "
              "Please execute tests using the Makefile.  Issue make help for "
              "options.{2:s}".format(FG_RED, BOLD, RESET))


if __name__ == '__main__':
    setup(
        name=__appname__,
        version=__version__,
        description='''The RAMS ToolKit (RAMSTK) is a suite of tools
        for performing and documenting reliability, availability,
        maintainability, and safety (RAMS) analyses''',
        long_description=__long_description__,
        long_description_content_type='text/markdown',
        author=__author__,
        author_email=__email__,
        license='BSD-3',
        url='https://github.com/ReliaQualAssociates/ramstk',
        python_requires='>=2.7, <4',
        install_requires=INSTALL_REQUIRES,
        setup_requires=['pytest_runner', 'Babel'],
        tests_require=TEST_REQUIRES,
        keywords='''reliability availability maintainability safety RAMS
        engineering quality''',
        scripts=[],
        packages=find_packages('src', exclude=['tests']),
        package_dir={'': 'src'},
        py_modules=[
            'ramstk.configuration',
            'ramstk.RAMSTK',
            'ramstk.utilities',
        ],
        classifiers=__trove__,
        entry_points={
            'console_scripts': ['ramstk = ramstk:__main__'],
        },
        package_data={},
        dependency_links=[],
        zip_safe=True,
        cmdclass={
            'install': Install,
            'sdist': Sdist,
            'test': MyTest
        },
    )
