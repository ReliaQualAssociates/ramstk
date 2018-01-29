#!/usr/bin/env python

import sys
from setuptools import find_packages, setup
from setuptools.command.install import install as _install

if not sys.version_info[0] == 2:
    sys.exit("Sorry, Python 3 is not supported (yet)")


class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

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
        install_requires=['defusedxml', 'lifelines', 'lxml', 'matplotlib==1.4.3',
                          'numpy', 'pandas', 'PyPubSub==3.3.0', 'scipy',
                          'sortedcontainers', 'SQLAlchemy', 'SQLAlchemy-Utils',
                          'statsmodels', 'treelib', 'xlrd', 'xlwt'],
        keywords='reliability RAMS engineering quality safety',
        scripts=[],
        packages=find_packages(exclude=['tests']),
        py_modules=[
            'rtk.__init__',
            'rtk.Configuration',
            'rtk.RTK',
            'rtk.Utilities',
            'rtk.imports'
        ],
        classifiers=[
             'Development Status :: 3 - Alpha',
             'Programming Language :: Python'
        ],
        entry_points={},
        data_files=[],
        package_data={},
        dependency_links=[],
        zip_safe=True,
        cmdclass={'install': install},
    )
