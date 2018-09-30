# -*- coding: utf-8 -*-
"""``RAMSTK`` lives on `GitHub <https://github.com/weibullguy/ramstk>`_."""
import os
import sys
import glob

from setuptools import find_packages, setup
from setuptools.command.install import install as _install
from setuptools.command.sdist import sdist

# Read the contents of your README file
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as f:
    __long_description__ = f.read()

__appname__ = 'RAMSTK'
__version__ = '1.0.0'
__author__ = "Doyle 'weibullguy' Rowland"
__email__ = "doyle.rowland@reliaqual.com"
__trove__ = [
    'Development Status :: 4 - Beta', 'Environment :: Win32 (MS Windows)',
    'Environment :: X11 Applications :: GTK',
    'Intended Audience :: Other Audience',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 2.7',
    'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
]

if not sys.version_info[0] == 2:
    sys.exit("Sorry, Python 3 is not supported yet.")

# Lists of required packages for RAMSTK.
INSTALL_REQUIRES = [
    'defusedxml', 'lifelines', 'matplotlib==1.4.3', 'numpy', 'pandas',
    'PyPubSub==3.3.0', 'scipy', 'sortedcontainers==1.5.9', 'SQLAlchemy',
    'SQLAlchemy-Utils', 'statsmodels', 'treelib', 'xlrd', 'xlwt'
]
TEST_REQUIRES = [
    'pytest', 'pytest-cov', 'coverage', 'coveralls', 'codacy-coverage'
]

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


class Install(_install):
    """Custom install class for RAMSTK."""

    @staticmethod
    def pre_install_script():
        """Execute before install."""
        import shutil

        _builddir = os.path.abspath('.') + '/build'
        if os.path.isdir(_builddir):
            print("Cleaning build directory: {0:s}...").format(_builddir)
            for _file in os.listdir(_builddir):
                _file_path = os.path.join(_builddir, _file)
                try:
                    if os.path.isfile(_file_path):
                        os.unlink(_file_path)
                    elif os.path.isdir(_file_path):
                        shutil.rmtree(_file_path)
                except Exception as _error:
                    print(_error)

        _eggfile = os.path.abspath('.') + '/src/RAMSTK.egg-info'
        print("Removing old egg...")
        try:
            if os.path.isfile(_eggfile):
                os.unlink(_eggfile)
        except Exception as _error:
            print(_error)

    @staticmethod
    def post_install_script():
        """Execute after install."""
        pass

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
        except Exception as _error:
            print(_error)
            print('No messages catalogs found.')

        sdist.run(self)


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
        url='https://github.com/weibullguy/ramstk',
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
            'ramstk.Configuration', 'ramstk.RAMSTK', 'ramstk.Utilities'
        ],
        classifiers=__trove__,
        entry_points={
            'console_scripts': ['ramstk = ramstk.RAMSTK:main'],
        },
        data_files=[('share/applications',
                     ['data/RAMSTK.desktop']), ('share/pixmaps',
                                                ['data/icons/RAMSTK.png']),
                    ('share/RAMSTK', ['data/RAMSTK.conf']), ('share/RAMSTK', [
                        'data/Site.conf'
                    ]), ('share/RAMSTK',
                         ['data/ramstk_common.rtk']), ('share/RAMSTK/layouts',
                                                       LAYOUT_FILES[0]),
                    ('share/RAMSTK/icons/16x16',
                     ICON16_FILES[0]), ('share/RAMSTK/icons/32x32',
                                        ICON32_FILES[0])],
        package_data={},
        dependency_links=[],
        zip_safe=True,
        cmdclass={
            'install': Install,
            'sdist': Sdist
        },
    )
