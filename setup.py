#!/usr/bin/env python

import os
import sys
import subprocess
import glob

import distutils.cmd
import distutils.log

from setuptools import find_packages, setup
from setuptools.command.install import install as _install
from setuptools.command.sdist import sdist

# Read the contents of your README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    __long_description__ = f.read()

__appname__ = 'RAMSTK'
__version__ = '1.0.0dev'
__author__ = "Doyle 'weibullguy' Rowland"
__email__ = "andrew.rowland@reliaqual.com"
__trove__ = [
             'Development Status :: 4 - Beta',
             'Environment :: Win32 (MS Windows)',
             'Environment :: X11 Applications :: GTK',
             'Intended Audience :: Other Audience',
             'License :: OSI Approved :: BSD License',
             'Programming Language :: Python :: 2.7',
             'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)'
        ]


if not sys.version_info[0] == 2:
    sys.exit("Sorry, Python 3 is not supported (yet)")

# Lists of required packages for RTK.
install_requires = [
    'defusedxml', 'lifelines', 'lxml', 'matplotlib==1.4.3', 'numpy', 'pandas',
    'PyPubSub==3.3.0', 'scipy', 'sortedcontainers', 'SQLAlchemy',
    'SQLAlchemy-Utils', 'statsmodels', 'treelib', 'xlrd', 'xlwt'
]
tests_require = [
    'pytest', 'pytest-cov', 'coverage==4.0.3', 'codacy-coverage',
    'python-coveralls'
]

# Build lists of data files to install.
layout_files = []
directories = glob.glob('data/layouts/')
for directory in directories:
    files = glob.glob(directory+'*')
    layout_files.append(files)

icon16_files = []
directories = glob.glob('data/icons/16x16/')
for directory in directories:
    files = glob.glob(directory+'*')
    icon16_files.append(files)

icon32_files = []
directories = glob.glob('data/icons/32x32/')
for directory in directories:
    files = glob.glob(directory+'*')
    icon32_files.append(files)


class Install(_install):
    def pre_install_script(self):
        import os, shutil

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
                except Exception as e:
                    print(e)

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()


class Sdist(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created. """

    def run(self):
        try:
            self.run_command('compile_catalog')
        except Exception as e:
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
        url='https://github.com/weibullguy/rtk',
        python_requires='>=2.7, <4',
        install_requires=install_requires,
        setup_requires=['pytest_runner', 'Babel'],
        tests_require=tests_require,
        keywords='''reliability availability maintainability safety RAMS
        engineering quality''',
        scripts=[],
        packages=find_packages('src', exclude=['tests']),
        package_dir={'': 'src'},
        py_modules=['rtk.Configuration', 'rtk.RTK', 'rtk.Utilities'],
        classifiers=__trove__,
        entry_points={
            'console_scripts': ['rtk = rtk.RTK:main'],
        },
        data_files=[('share/applications', ['data/RTK.desktop']),
                    ('share/pixmaps', ['data/icons/RTK.png']),
                    ('share/RTK', ['data/RTK.conf']),
                    ('share/RTK', ['data/Site.conf']),
                    ('share/RTK/layouts', layout_files[0]),
                    ('share/RTK/icons/16x16', icon16_files[0]),
                    ('share/RTK/icons/32x32', icon32_files[0])
                    ],
        package_data={},
        dependency_links=[],
        zip_safe=True,
        cmdclass={
            'install': Install,
            'sdist': Sdist
        },
    )
