#!/usr/bin/env python

import sys

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


class install(_install):
    def pre_install_script(self):
        import os, shutil

        _builddir = os.path.abspath('.') + '/build'
        print ("Cleaning build directory: {0:s}...").format(_builddir)
        if os.path.isdir(_builddir):
            for _file in os.listdir(_builddir):
                _file_path = os.path.join(_builddir, _file)
                try:
                    if os.path.isfile(_file_path):
                        os.unlink(_file_path)
                    elif os.path.isdir(_file_path):
                        shutil.rmtree(_file_path)
                except Exception as e:
                    print (e)


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
            print ('No messages catalogs found.')

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
        cmdclass={'install': install, 'sdist': Sdist},
    )
