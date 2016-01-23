from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.unittest")
# use_plugin("python.integrationtest")
use_plugin("python.frosted")
use_plugin("python.flake8")
use_plugin("python.pychecker")
use_plugin("python.sphinx")
use_plugin("python.distutils")


name = "The Reliability ToolKit (RTK)"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("dir_source_main_python", "rtk")
    project.set_property("dir_source_unittest_python", "tests/unittests")
    project.set_property("unittest_module_glob", "*Tests.py")
    project.set_property("coverage_threshold_warn", 95)
    project.set_property("coverage_branch_threshold_warn", 85)
    project.set_property("coverage_branch_partial_threshold_warn", 90)
    project.set_property("dir_source_integrationtest_python",
                         "tests/integrationtests")
    project.set_property("integrationtest_file_glob", "*Tests.py")
    project.set_property("flake8_max_line_length", 80)
    project.set_property("dir_source_main_scripts", "scripts")
