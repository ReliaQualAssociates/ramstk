#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

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
        name = 'The Reliability ToolKit (RTK)',
        version = '2016.1',
        description = '''RAMS analysis tool''',
        long_description = '''RTK is a suite of tools for performing and documenting RAMS                analyses.''',
        author = "Andrew 'weibullguy' Rowland",
        author_email = "andrew.rowland@reliaqual.com",
        license = 'Proprietary',
        url = 'http://www.reliaqual.com/rtk',
        scripts = [],
        packages = [
            'usage',
            'requirement',
            'revision',
            'hardware',
            'software',
            'testing',
            '_reports_',
            'stakeholder',
            'analyses',
            'datamodels',
            'survival',
            'incident',
            'validation',
            'dao',
            '_assistants_',
            'gui',
            'failure_definition',
            'function',
            'hardware.component',
            'hardware.__gui',
            'hardware.assembly',
            'hardware.component.miscellaneous',
            'hardware.component.relay',
            'hardware.component.meter',
            'hardware.component.integrated_circuit',
            'hardware.component.inductor',
            'hardware.component.switch',
            'hardware.component.capacitor',
            'hardware.component.connection',
            'hardware.component.resistor',
            'hardware.component.semiconductor',
            'hardware.component.capacitor.fixed',
            'hardware.component.capacitor.electrolytic',
            'hardware.component.capacitor.variable',
            'hardware.component.resistor.fixed',
            'hardware.component.resistor.variable',
            'hardware.component.semiconductor.optoelectronic',
            'hardware.component.semiconductor.transistor',
            'hardware.__gui.gtk',
            'software.__gui',
            'software.__gui.gtk',
            'testing.__gui',
            'testing.growth',
            'testing.__gui.gtk',
            'analyses.statistics',
            'analyses.pof',
            'analyses.fmea',
            'analyses.allocation',
            'analyses.survival',
            'analyses.hazard',
            'analyses.prediction',
            'analyses.similar_item',
            'analyses.pof.gui',
            'analyses.pof.gui.gtk',
            'analyses.fmea.gui',
            'analyses.fmea.gui.gtk',
            'analyses.allocation.gui',
            'analyses.allocation.gui.gtk',
            'analyses.hazard.gui',
            'analyses.hazard.gui.gtk',
            'analyses.similar_item.gui',
            'analyses.similar_item.gui.gtk',
            'datamodels.matrix',
            'survival.__gui',
            'survival.__gui.gtk',
            'incident.component',
            'incident.action',
            'gui.gtk',
            'gui.gtk.mwi'
        ],
        py_modules = [
            'Utilities',
            'login',
            'Configuration',
            'imports',
            'RTK',
            'calculations',
            '__init__',
            'partlist'
        ],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
