#!/usr/bin/env python

import sys
from setuptools import setup
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
        version='0.1',
        description='''RAMS analysis tool''',
        long_description='''The Reliability ToolKit (RTK) is a suite of tools
        for performing and documenting RAMS analyses.''',
        author="Doyle 'weibullguy' Rowland",
        author_email="andrew.rowland@reliaqual.com",
        license='BSD-3',
        url='https://github.com/weibullguy/rtk',
        python_requires='>=2.7, <4',
        keywords='reliability RAMS engineering quality safety',
        scripts=[],
        packages=[
            'rtk.analyses',
            'rtk.analyses.fmea',
            'rtk.dao',
            'rtk.datamodels',
            'rtk.gui',
            'rtk.gui.gtk',
            'rtk.gui.gtk.assistants',
            'rtk.gui.gtk.listviews',
            'rtk.gui.gtk.matrixviews',
            'rtk.gui.gtk.moduleviews',
            'rtk.gui.gtk.mwi',
            'rtk.gui.gtk.rtk',
            'rtk.gui.gtk.workviews',
            'rtk.usage',
            'rtk.analyses.statistics',
            'rtk.analyses.pof',
            'rtk.analyses.allocation',
            'rtk.analyses.survival',
            'rtk.analyses.hazard',
            'rtk.analyses.prediction',
            'rtk.analyses.similar_item',
            'rtk.analyses.pof.gui',
            'rtk.analyses.pof.gui.gtk',
            'rtk.analyses.allocation.gui',
            'rtk.analyses.allocation.gui.gtk',
            'rtk.analyses.hazard.gui',
            'rtk.analyses.hazard.gui.gtk',
            'rtk.analyses.similar_item.gui',
            'rtk.analyses.similar_item.gui.gtk',
            'rtk.hardware',
            'rtk.software',
            'rtk.testing',
            'rtk.survival',
            'rtk.incident',
            'rtk.validation',
            'rtk.hardware.component',
            'rtk.hardware.__gui',
            'rtk.hardware.assembly',
            'rtk.hardware.component.miscellaneous',
            'rtk.hardware.component.relay',
            'rtk.hardware.component.meter',
            'rtk.hardware.component.integrated_circuit',
            'rtk.hardware.component.inductor',
            'rtk.hardware.component.switch',
            'rtk.hardware.component.capacitor',
            'rtk.hardware.component.connection',
            'rtk.hardware.component.resistor',
            'rtk.hardware.component.semiconductor',
            'rtk.hardware.component.capacitor.fixed',
            'rtk.hardware.component.capacitor.electrolytic',
            'rtk.hardware.component.capacitor.variable',
            'rtk.hardware.component.resistor.fixed',
            'rtk.hardware.component.resistor.variable',
            'rtk.hardware.component.semiconductor.optoelectronic',
            'rtk.hardware.component.semiconductor.transistor',
            'rtk.hardware.__gui.gtk',
            'rtk.software.__gui',
            'rtk.software.__gui.gtk',
            'rtk.testing.__gui',
            'rtk.testing.growth',
            'rtk.testing.__gui.gtk',
            'rtk.survival.__gui',
            'rtk.survival.__gui.gtk',
            'rtk.incident.component',
            'rtk.incident.action'
        ],
        py_modules=[
            'rtk.__init__',
            'rtk.Configuration',
            'rtk.FailureDefinition',
            'rtk.Function',
            'rtk.Requirement',
            'rtk.Revision',
            'rtk.RTK',
            'rtk.Stakeholder',
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
        install_requires=[],
        dependency_links=[],
        zip_safe=True,
        cmdclass={'install': install},
    )
