from pybuilder.core import Author, use_plugin, init

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("pypi:pybuilder_nose")
# use_plugin("python.unittest")
# use_plugin("python.integrationtest")
use_plugin("python.frosted")
use_plugin("python.flake8")
use_plugin("python.pychecker")
use_plugin("python.pytddmon")
use_plugin("python.distutils")
use_plugin("python.sphinx")

name = 'The Reliability ToolKit (RTK)'
version = '2016.1'

authors = [
    Author('Andrew "weibullguy" Rowland', 'andrew.rowland@reliaqual.com')
]
url = 'http://www.reliaqual.com/rtk'
description = 'RTK is a suite of tools for performing and documenting RAMS \
               analyses.'

license = 'Proprietary'
summary = 'RAMS analysis tool'

default_task = ['clean', 'analyze', 'sphinx_generate_documentation', 'publish']


@init
def set_properties(project):
    project.set_property("dir_source_main_python", "rtk")
    project.set_property("dir_source_main_scripts", "scripts")

    project.set_property("flake8_max_line_length", 80)
    project.set_property("flake8_verbose_output", True)
    project.set_property("flake8_ignore", "E126, E127")

    project.set_property("dir_source_unittest_python", "tests/unit")
    project.set_property("unittest_module_glob", "Test*.py")

    project.set_property("dir_source_integrationtest_python",
                         "tests/integration")
    project.set_property("integrationtest_file_glob", "Test*.py")

    # project.set_property("coverage_threshold_warn", 95)
    # project.set_property("coverage_branch_threshold_warn", 85)
    # project.set_property("coverage_branch_partial_threshold_warn", 90)

    project.set_property("nose_cover-branches", True)
    project.set_property("nose_cover-xml", False)
    project.set_property("nose_cover-min-percentage", 45)
    project.set_property("nose_attr", "unit=True")
    project.set_property("nose_with-html", True)
    project.set_property("nose_html-file",
                         "tests/_test_results/nosetests.html")

    project.set_property("sphinx_config_path", "docs/")
    project.set_property("sphinx_source_dir", "docs/source/")
    project.set_property("sphinx_output_dir", "docs/build/")
