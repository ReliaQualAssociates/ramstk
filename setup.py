#!/usr/bin/env python

import os
import sys
import subprocess

import distutils.cmd
import distutils.log

from setuptools import find_packages, setup
from setuptools.command.install import install as _install
from setuptools.command.sdist import sdist

if not sys.version_info[0] == 2:
    sys.exit("Sorry, Python 3 is not supported (yet)")

install_requires = [
    'defusedxml', 'lifelines', 'lxml', 'matplotlib==1.4.3', 'numpy', 'pandas',
    'PyPubSub==3.3.0', 'scipy', 'sortedcontainers', 'SQLAlchemy',
    'SQLAlchemy-Utils', 'statsmodels', 'treelib', 'xlrd', 'xlwt'
]
tests_require = [
    'pytest', 'pytest-cov', 'coverage==4.0.3', 'codacy-coverage',
    'python-coveralls'
]


class FormatFiles(distutils.cmd.Command):
    """Custom command to automatically sort imports and format Python files."""
    description = 'run isort and yapf to fix file formatting'
    user_options = [
        ('parallel=', 'p', 'number of parallel processes to use'),
        ('isort=', None, 'execute isort on the Python files; default is True'),
        ('yapf=', None, 'execute yapf on the Python files; default is True'),
    ]

    def initialize_options(self):
        """Set default values for user options."""
        self.parallel = 1
        self.isort = True
        self.yapf = True

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        # Base command.
        _command = [
            os.path.dirname(os.path.abspath(__file__)) + '/tests/RunTests.py'
        ]

        # Add option to use isort.
        if self.isort:
            _command.append(' --import')

        # Add option to use yapf.
        if self.yapf:
            _command.append(' --format')

        # Add option to use parallel processes (and how many).
        if self.parallel > 1:
            _command.append(' --parallel={0:d}').format(self.parallel)

        # Add the path to search for Python files.
        _command.append(' -r')
        _command.append(' -f ')
        _command.append(os.getcwd() + '/rtk/')
        self.announce(
            'Running {0:s}'.format(_command), level=distutils.log.INFO)

        try:
            subprocess.check_call(_command)
        except subprocess.CalledProcessError as error:
            _msg = ('Command {0:s} failed with exit code {1:s}').format(
                _commad, str(error.returncode))
            print(_msg)
            self.announce(_msg, level=distutils.log.DEBUG)
            sys.exit(error.returncode)


class LintFiles(distutils.cmd.Command):
    """Custom command to lint Python files using the most popular linters."""
    description = 'lint files using flake8, pycodestyle, and pylint'
    user_options = [
        ('parallel=', 'p', 'number of parallel processes to use'),
        ('flake8=', None, 'use flake8 to lint Python files; default is False'),
        ('pycodestyle=', None,
         'use pycodestyle (formally pep8) to lint Python files; default is True'
         ),
        ('pylint-', None, 'use pylint to lint Python files; default is True'),
    ]

    def initialize_options(self):
        """Set default values for user options."""
        self.parallel = 1
        self.flake8 = False
        self.pycodestyle = True
        self.pylint = True

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        # Base command.
        _command = [
            os.path.dirname(os.path.abspath(__file__)) +
            '/tests/RunTests.py --quality'
        ]

        # Add option to run flake8.
        if self.flake8:
            _command.append(' --checker=flake8')

        # Add option to run pycodestyle (formally pep8).
        if self.pycodestyle:
            _command.append(' --checker=pycodestyle')

        # Add option to run pylint.
        if self.pylint:
            _command.append(' --checker=pylint')

        # Add option to use parallel processes (and how many).
        if self.parallel > 1:
            _command.append(' --parallel={0:d}').format(self.parallel)

        # Add the path to search for Python files.
        _command.append(' ' + os.getcwd() + '/rtk')
        self.announce(
            'Running {0:s}'.format(_command), level=distutils.log.INFO)

        try:
            subprocess.check_call(_command)
        except subprocess.CalledProcessError as error:
            _msg = ('Command {0:s} failed with exit code {1:s}').format(
                _commad, str(error.returncode))
            print(_msg)
            self.announce(_msg, level=distutils.log.DEBUG)
            sys.exit(error.returncode)


class SecurityCheck(distutils.cmd.Command):
    """Custom command to execute security checks on Python files."""
    description = 'security check files using bandit'
    user_options = []

    def initialize_options(self):
        """Set default values for user options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        # Base command.
        _command = [
            os.path.dirname(os.path.abspath(__file__)) +
            '/tests/RunTests.py --security'
        ]

        # Add the path to search for Python files.
        _command.append(' ' + os.getcwd() + '/rtk')
        self.announce(
            'Running {0:s}'.format(_command), level=distutils.log.INFO)

        try:
            subprocess.check_call(_command)
        except subprocess.CalledProcessError as error:
            _msg = ('Command {0:s} failed with exit code {1:s}').format(
                _commad, str(error.returncode))
            print(_msg)
            self.announce(_msg, level=distutils.log.DEBUG)
            sys.exit(error.returncode)


class CheckManifest(distutils.cmd.Command):
    """Custom command to quality check MANIFEST.in."""
    description = 'checks for inconsistencies in MANIFEST.in'
    user_options = []

    def initialize_options(self):
        """Set default values for user options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        # Base command.
        _command = [
            os.path.dirname(os.path.abspath(__file__)) +
            '/tests/RunTests.py -- manifest'
        ]

        # Add the path to search for Python files.
        _command.append(' ' + os.getcwd() + '/rtk')
        self.announce(
            'Running {0:s}'.format(_command), level=distutils.log.INFO)

        try:
            subprocess.check_call(_command)
        except subprocess.CalledProcessError as error:
            _msg = ('Command {0:s} failed with exit code {1:s}').format(
                _commad, str(error.returncode))
            print(_msg)
            self.announce(_msg, level=distutils.log.DEBUG)
            sys.exit(error.returncode)


class Benchmark(distutils.cmd.Command):
    """Custom command to benchmark Python code."""
    description = 'benchmarks'
    user_options = [('flake8=', None,
                     'use flake8 to benchmark code; default is True'),
                    ('pycodestyle=', None,
                     'use pycodestyle to benchmark code; default is True')]

    def initialize_options(self):
        """Set default values for user options."""
        self.flake8 = True
        self.pycodestyle = True

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        # Base command.
        _command = [
            os.path.dirname(os.path.abspath(__file__)) + '/tests/RunTests.py'
        ]
        _command.append(' --quality')
        _command.append(' --benchmark')

        # Add checker options.
        if self.flake8:
            _command.append(' --checker=flake8')
        if self.pycodestyle:
            _command.append(' --checker=pycodestyle')

        # Add the path to search for Python files.
        _command.append(' -f ' + os.getcwd() + '/rtk')
        self.announce(
            'Running {0:s}'.format(_command), level=distutils.log.INFO)

        try:
            subprocess.check_call(_command)
        except subprocess.CalledProcessError as error:
            _msg = ('Command {0:s} failed with exit code {1:s}').format(
                _commad, str(error.returncode))
            print(_msg)
            self.announce(_msg, level=distutils.log.DEBUG)
            sys.exit(error.returncode)


class Install(_install):
    def pre_install_script(self):
        import os, shutil

        _builddir = os.path.abspath('.') + '/build'
        print("Cleaning build directory: {0:s}...").format(_builddir)
        if os.path.isdir(_builddir):
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
        name='RTK',
        version='0.5',
        description='''RAMS analysis tool''',
        long_description='''The Reliability ToolKit (RTK) is a suite of tools
        for performing and documenting RAMS analyses.''',
        author="Doyle 'weibullguy' Rowland",
        author_email="andrew.rowland@reliaqual.com",
        license='BSD-3',
        url='https://github.com/weibullguy/rtk',
        python_requires='>=2.7, <4',
        install_requires=install_requires,
        setup_requires=['pytest_runner', 'Babel'],
        tests_require=tests_require,
        keywords='reliability RAMS engineering quality safety',
        scripts=[],
        packages=find_packages(exclude=['tests']),
        py_modules=['rtk.Configuration', 'rtk.RTK', 'rtk.Utilities'],
        classifiers=[
            'Development Status :: 3 - Alpha', 'Programming Language :: Python'
        ],
        entry_points={
            'console_scripts': ['rtk = rtk.RTK:main'],
        },
        data_files=[('share/applications', ['data/RTK.desktop']),
                    ('share/pixmaps', ['data/icons/RTK.png'])],
        package_data={},
        dependency_links=[],
        zip_safe=True,
        cmdclass={
            'format': FormatFiles,
            'lint': LintFiles,
            'check_security': SecurityCheck,
            'check_manifest': CheckManifest,
            'benchmark': Benchmark,
            'install': Install,
            'sdist': Sdist
        },
    )
