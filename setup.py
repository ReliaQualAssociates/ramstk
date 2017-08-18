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
        author="Andrew 'Weibullguy' Rowland",
        author_email="andrew.rowland@reliaqual.com",
        license='BSD-3',
        url='http://www.reliaqual.com/rtk',
        python_requires='>=2.7, <4',
        keywords='reliability RAMS engineering quality',
        scripts=[],
        packages=[
            'rtk.usage',
            'rtk.requirement',
            'rtk.revision',
            'rtk.hardware',
            'rtk.software',
            'rtk.testing',
            'rtk._reports_',
            'rtk.stakeholder',
            'rtk.analyses',
            'rtk.datamodels',
            'rtk.survival',
            'rtk.incident',
            'rtk.validation',
            'rtk.dao',
            'rtk._assistants_',
            'rtk.gui',
            'rtk.failure_definition',
            'rtk.function',
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
            'rtk.analyses.statistics',
            'rtk.analyses.pof',
            'rtk.analyses.fmea',
            'rtk.analyses.allocation',
            'rtk.analyses.survival',
            'rtk.analyses.hazard',
            'rtk.analyses.prediction',
            'rtk.analyses.similar_item',
            'rtk.analyses.pof.gui',
            'rtk.analyses.pof.gui.gtk',
            'rtk.analyses.fmea.gui',
            'rtk.analyses.fmea.gui.gtk',
            'rtk.analyses.allocation.gui',
            'rtk.analyses.allocation.gui.gtk',
            'rtk.analyses.hazard.gui',
            'rtk.analyses.hazard.gui.gtk',
            'rtk.analyses.similar_item.gui',
            'rtk.analyses.similar_item.gui.gtk',
            'rtk.datamodels.matrix',
            'rtk.survival.__gui',
            'rtk.survival.__gui.gtk',
            'rtk.incident.component',
            'rtk.incident.action',
            'rtk.gui.gtk',
            'rtk.gui.gtk.mwi'
        ],
        py_modules=[
            'rtk.Utilities',
            'rtk.Configuration',
            'rtk.imports',
            'rtk.RTK',
            'rtk.__init__'
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
