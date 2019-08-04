# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.tests.configuration.test_userconfiguration.py is part of The
#       RAMSTK Project
#
# All rights reserved.
"""Test class for the User Configuration module algorithms and models."""

# Standard Library Imports
import glob
import sys
from os import environ, getenv, path

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration

try:
    VIRTUAL_ENV = glob.glob(environ['VIRTUAL_ENV'])[0]
except KeyError:
    if sys.platform == 'Linux':
        VIRTUAL_ENV = getenv('HOME') + '/.local'
    elif sys.platform == 'Windows':
        VIRTUAL_ENV = getenv('TEMP')
    else:
        print(("The {0:s} system platform is not "
               "supported.").format(sys.platform))
        sys.exit(1)


@pytest.mark.usefixtures('test_configuration', 'make_shibboly')
class TestCreateUserConfiguration():
    """Class for testing the user configuration module."""
    TMP_DIR = ''

    def on_create_user_configuration(self):
        print(
            "\033[36m\nsucceed_create_user_configuration topic was broadcast.")

    def fail_create_user_configuration_no_confdir(self, error_message):
        assert error_message == ("User's configuration directory "
                                 "/tmp/shibboly/.config/RAMSTK does not exist "
                                 "and could not be created when attempting to "
                                 "create a new user configuration file.")
        print("\033[35m\nfail_create_user_configuration topic was broadcast.")

    def fail_create_user_configuration_no_datadir(self, error_message):
        assert error_message == ("User's data directory "
                                 "/tmp/shibboly/.config/RAMSTK/layouts "
                                 "does not exist and could not be created "
                                 "when attempting to create a new user "
                                 "configuration file.")
        print("\033[35m\nfail_create_user_configuration topic was broadcast.")

    def fail_create_user_configuration_no_icondir(self, error_message):
        assert error_message == ("User's icon directory "
                                 "/tmp/shibboly/.config/RAMSTK/icons "
                                 "does not exist and could not be created "
                                 "when attempting to create a new user "
                                 "configuration file.")
        print("\033[35m\nfail_create_user_configuration topic was broadcast.")

    def fail_create_user_configuration_no_logdir(self, error_message):
        assert error_message == ("User's log directory "
                                 "/tmp/shibboly/.config/RAMSTK/logs "
                                 "does not exist and could not be created "
                                 "when attempting to create a new user "
                                 "configuration file.")
        print("\033[35m\nfail_create_user_configuration topic was broadcast.")

    def fail_create_user_configuration_no_progdir(self, error_message):
        assert error_message == ("Program directory "
                                 "/tmp/shibboly/analyses/ramstk "
                                 "does not exist and could not be created "
                                 "when attempting to create a new user "
                                 "configuration file.")
        print("\033[35m\nfail_create_user_configuration topic was broadcast.")

    @pytest.mark.integration
    def test_initialize_configuration(self):
        """ __init__() should create an instance of the Configuration class. """
        DUT = RAMSTKUserConfiguration()

        assert isinstance(DUT, RAMSTKUserConfiguration)
        assert DUT.RAMSTK_MODE == ''
        assert DUT.RAMSTK_PROG_CONF == ''
        assert DUT.RAMSTK_SITE_CONF == ''
        assert DUT.RAMSTK_DEBUG_LOG == ''
        assert DUT.RAMSTK_IMPORT_LOG == ''
        assert DUT.RAMSTK_USER_LOG == ''

        assert DUT.RAMSTK_COLORS == {}
        assert DUT.RAMSTK_FORMAT_FILE == {}

        assert DUT.RAMSTK_RISK_POINTS == [4, 10]
        assert DUT.RAMSTK_MODE_SOURCE == 1
        assert DUT.RAMSTK_COM_BACKEND == ''
        assert DUT.RAMSTK_BACKEND == ''
        assert DUT.RAMSTK_COM_INFO == {}
        assert DUT.RAMSTK_PROG_INFO == {}
        assert DUT.RAMSTK_MODULES == {}
        assert DUT.RAMSTK_HR_MULTIPLIER == 1000000.0
        assert DUT.RAMSTK_DEC_PLACES == 6
        assert DUT.RAMSTK_MTIME == 100.0
        assert DUT.RAMSTK_TABPOS == {
            'listbook': 'top',
            'modulebook': 'bottom',
            'workbook': 'bottom',
        }
        assert DUT.RAMSTK_GUI_LAYOUT == 'advanced'
        assert DUT.RAMSTK_METHOD == 'STANDARD'
        assert DUT._lst_colors == [
            "revisionfg",
            "functionfg",
            "requirementfg",
            "hardwarefg",
            "validationfg",
            "revisionbg",
            "functionbg",
            "requirementbg",
            "hardwarebg",
            "validationbg",
            "stakeholderbg",
            "stakeholderfg",
        ]
        assert DUT._lst_format_files == [
            "allocation",
            "failure_definition",
            "fmea",
            "function",
            "hardware",
            "hazops",
            "pof",
            "requirement",
            "revision",
            "similaritem",
            "stakeholder",
            "validation",
        ]
        assert DUT.RAMSTK_LOCALE == 'en_US'
        assert DUT.RAMSTK_HOME_DIR == environ['HOME']
        assert DUT.RAMSTK_SITE_DIR == DUT._INSTALL_PREFIX + "/share/RAMSTK"
        assert DUT.RAMSTK_DATA_DIR == DUT.RAMSTK_SITE_DIR + "/layouts"
        assert DUT.RAMSTK_ICON_DIR == DUT.RAMSTK_SITE_DIR + "/icons"
        assert DUT.RAMSTK_LOG_DIR == '/var/log/RAMSTK'
        assert DUT.RAMSTK_PROG_DIR == DUT.RAMSTK_HOME_DIR + "/analyses/ramstk/"
        assert DUT.RAMSTK_CONF_DIR == DUT.RAMSTK_SITE_DIR
        if sys.platform == "linux" or sys.platform == "linux2":
            assert DUT.RAMSTK_OS == 'Linux'
        elif sys.platform == "win32":
            assert DUT.RAMSTK_OS == "Windows"

    @pytest.mark.integration
    def test_create_user_configuration(self):
        """do_create_user_configuration() should broadcast the succcess message on success."""
        pub.subscribe(self.on_create_user_configuration,
                      'succeed_create_user_configuration')

        DUT = RAMSTKUserConfiguration()

        DUT.RAMSTK_HOME_DIR = '/tmp'
        DUT.RAMSTK_SITE_DIR = VIRTUAL_ENV + '/share/RAMSTK'
        DUT.RAMSTK_PROG_CONF = DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK/RAMSTK.toml'

        assert DUT.do_create_user_configuration() is None
        assert DUT.RAMSTK_PROG_CONF == DUT.RAMSTK_CONF_DIR + "/RAMSTK.toml"
        assert path.isdir('/tmp/.config/RAMSTK/icons')
        assert path.isdir('/tmp/.config/RAMSTK/icons/16x16')
        assert path.isdir('/tmp/.config/RAMSTK/icons/32x32')
        assert path.isdir('/tmp/.config/RAMSTK/layouts')
        assert path.isdir('/tmp/.config/RAMSTK/logs')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Allocation.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/FMEA.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/FailureDefinition.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Function.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Hardware.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/HazOps.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Incident.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/PoF.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Requirement.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Revision.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/SimilarItem.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Software.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Stakeholder.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Testing.xml')
        assert path.isfile('/tmp/.config/RAMSTK/layouts/Validation.xml')

        pub.unsubscribe(self.on_create_user_configuration,
                        'succeed_create_user_configuration')

    @pytest.mark.integration
    def test_create_user_configuration_no_confdir(self):
        """do_create_user_configuration() should broadcast the fail message and raise a FileNotFoundError when attempting to create a configuration directory the user lacks write access to."""
        pub.subscribe(self.fail_create_user_configuration_no_confdir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()

        DUT.RAMSTK_HOME_DIR = '/tmp/shibboly'
        DUT._do_make_configuration_dir()

        assert DUT.RAMSTK_CONF_DIR == '/tmp/shibboly/.config/RAMSTK'

        pub.unsubscribe(self.fail_create_user_configuration_no_confdir,
                        'fail_create_user_configuration')

    @pytest.mark.integration
    def test_create_user_configuration_no_datadir(self):
        """do_create_user_configuration() should broadcast the fail message and raise a FileNotFoundError when attempting to create a data directory the user lacks write access to."""
        pub.subscribe(self.fail_create_user_configuration_no_datadir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()

        DUT.RAMSTK_CONF_DIR = '/tmp/shibboly/.config/RAMSTK'
        DUT._do_make_data_dir()

        assert DUT.RAMSTK_DATA_DIR == '/tmp/shibboly/.config/RAMSTK/layouts'

        pub.unsubscribe(self.fail_create_user_configuration_no_datadir,
                        'fail_create_user_configuration')

    @pytest.mark.integration
    def test_create_user_configuration_no_icondir(self):
        """do_create_user_configuration() should broadcast the fail message and raise a FileNotFoundError when attempting to create an icon directory the user lacks write access to."""
        pub.subscribe(self.fail_create_user_configuration_no_icondir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()

        DUT.RAMSTK_CONF_DIR = '/tmp/shibboly/.config/RAMSTK'
        DUT._do_make_icon_dir()

        assert DUT.RAMSTK_ICON_DIR == '/tmp/shibboly/.config/RAMSTK/icons'

        pub.unsubscribe(self.fail_create_user_configuration_no_icondir,
                        'fail_create_user_configuration')

    @pytest.mark.integration
    def test_create_user_configuration_no_logdir(self):
        """do_create_user_configuration() should broadcast the fail message and raise a FileNotFoundError when attempting to create a log directory the user lacks write access to."""
        pub.subscribe(self.fail_create_user_configuration_no_logdir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()

        DUT.RAMSTK_CONF_DIR = '/tmp/shibboly/.config/RAMSTK'
        DUT._do_make_log_dir()

        assert DUT.RAMSTK_LOG_DIR == '/tmp/shibboly/.config/RAMSTK/logs'

        pub.unsubscribe(self.fail_create_user_configuration_no_logdir,
                        'fail_create_user_configuration')

    @pytest.mark.integration
    def test_create_user_configuration_no_progdir(self):
        """do_create_user_configuration() should broadcast the fail message and raise a FileNotFoundError when attempting to create a program directory the user lacks write access to."""
        pub.subscribe(self.fail_create_user_configuration_no_progdir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()

        DUT.RAMSTK_PROG_DIR = '/tmp/shibboly/analyses/ramstk'
        DUT._do_make_program_dir()

        assert DUT.RAMSTK_PROG_DIR == '/tmp/shibboly/analyses/ramstk'

        pub.unsubscribe(self.fail_create_user_configuration_no_progdir,
                        'fail_create_user_configuration')


@pytest.mark.usefixtures('test_toml_user_configuration', 'make_shibboly')
class TestGetterSetter():
    """Class for testing that the user configuration module can be read."""
    def on_fail_get_user_configuration(self, error_message):
        assert error_message == (
            "Failed to read user's RAMSTK configuration "
            "file /home/andrew/.pyenv/versions/3.7.2/envs/ramstk-py3-pygobject/share/RAMSTK/RAMSTKtoml.toml."
        )
        print("\033[35m\nfail_get_user_configuration topic was broadcast.")

    def on_succeed_set_user_configuration(self, configuration):
        assert isinstance(configuration, str)
        print("\033[36m\nsucceed_set_user_configuration topic was broadcast.")

    @pytest.mark.integration
    def test_get_user_configuration(self):
        """get_user_configuration() should broadcast the succcess message on success."""
        DUT = RAMSTKUserConfiguration()
        DUT.RAMSTK_PROG_CONF = VIRTUAL_ENV + '/share/RAMSTK/RAMSTK.toml'

        assert DUT.get_user_configuration() is None
        assert DUT.RAMSTK_COLORS == {
            'functionbg': '#FFFFFF',
            'functionfg': '#000000',
            'hardwarebg': '#FFFFFF',
            'hardwarefg': '#000000',
            'requirementbg': '#FFFFFF',
            'requirementfg': '#000000',
            'revisionbg': '#FFFFFF',
            'revisionfg': '#000000',
            'stakeholderbg': '#FFFFFF',
            'stakeholderfg': '#000000',
            'validationbg': '#FFFFFF',
            'validationfg': '#000000'
        }
        assert DUT.RAMSTK_FORMAT_FILE == {
            'allocation': 'Allocation.toml',
            'failure_definition': 'FailureDefinition.toml',
            'fmea': 'FMEA.toml',
            'function': 'Function.toml',
            'hardware': 'Hardware.toml',
            'hazops': 'HazOps.toml',
            'pof': 'PoF.toml',
            'requirement': 'Requirement.toml',
            'revision': 'Revision.toml',
            'similaritem': 'SimilarItem.toml',
            'stakeholder': 'Stakeholder.toml',
            'validation': 'Validation.toml'
        }
        assert DUT.RAMSTK_BACKEND == 'sqlite'
        assert DUT.RAMSTK_PROG_INFO["host"] == 'localhost'
        assert DUT.RAMSTK_PROG_INFO["socket"] == '3306'
        assert DUT.RAMSTK_PROG_INFO["database"] == ''
        assert DUT.RAMSTK_PROG_INFO["user"] == 'johnny.tester'
        assert DUT.RAMSTK_PROG_INFO["password"] == 'clear.text.password'
        assert DUT.RAMSTK_DATA_DIR == (VIRTUAL_ENV
                                       + '/share/RAMSTK/layouts')
        assert DUT.RAMSTK_ICON_DIR == (VIRTUAL_ENV
                                       + '/share/RAMSTK/icons')
        assert DUT.RAMSTK_LOG_DIR == VIRTUAL_ENV + '/tmp/logs'
        assert DUT.RAMSTK_REPORT_SIZE == 'letter'
        assert DUT.RAMSTK_HR_MULTIPLIER == 1000000.0
        assert DUT.RAMSTK_DEC_PLACES == 6
        assert DUT.RAMSTK_MTIME == 100.0
        assert DUT.RAMSTK_MODE_SOURCE == '1'
        assert DUT.RAMSTK_TABPOS["listbook"] == 'bottom'
        assert DUT.RAMSTK_TABPOS["modulebook"] == 'top'
        assert DUT.RAMSTK_TABPOS["workbook"] == 'bottom'

    @pytest.mark.integration
    def test_get_user_configuration_no_conf_file(self):
        """get_user_configuration() should broadcast the fail message when attempting to read a non-existent user configuration."""
        pub.subscribe(self.on_fail_get_user_configuration,
                      'fail_get_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT.RAMSTK_PROG_CONF = VIRTUAL_ENV + '/share/RAMSTK/RAMSTKtoml.toml'

        assert DUT.get_user_configuration() is None

        pub.unsubscribe(self.on_fail_get_user_configuration,
                        'fail_get_user_configuration')

    @pytest.mark.integration
    def test_set_user_configuration(self):
        """get_user_configuration() should broadcast the fail message when attempting to read a non-existent user configuration."""
        pub.subscribe(self.on_succeed_set_user_configuration,
                      'succeed_set_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT.RAMSTK_PROG_CONF = VIRTUAL_ENV + '/share/RAMSTK/RAMSTK.toml'
        DUT.RAMSTK_PROG_INFO = {
            "host": "localhost",
            "socket": "3306",
            "database": "",
            "user": "johnny.tester",
            "password": "clear.text.password"
        }
        DUT.RAMSTK_FORMAT_FILE = {
            "allocation": "Allocation.toml",
            "failure_definition": "FailureDefinition.toml",
            "fmea": "FMEA.toml",
            "function": "Function.toml",
            "hardware": "Hardware.toml",
            "hazops": "HazOps.toml",
            "pof": "PoF.toml",
            "requirement": "Requirement.toml",
            "revision": "Revision.toml",
            "similaritem": "SimilarItem.toml",
            "stakeholder": "Stakeholder.toml",
            "validation": "Validation.toml"
        }
        DUT.RAMSTK_COLORS = {
            "functionbg": "#FFFFFF",
            "functionfg": "#000000",
            "hardwarebg": "#FFFFFF",
            "hardwarefg": "#000000",
            "requirementbg": "#FFFFFF",
            "requirementfg": "#000000",
            "revisionbg": "#FFFFFF",
            "revisionfg": "#000000",
            "stakeholderbg": "#FFFFFF",
            "stakeholderfg": "#000000",
            "validationbg": "#FFFFFF",
            "validationfg": "#000000"
        }

        assert DUT.set_user_configuration() is None

        pub.unsubscribe(self.on_succeed_set_user_configuration,
                        'succeed_set_user_configuration')

    @pytest.mark.integration
    def test_set_user_configuration_missing_global_data(self):
        """get_user_configuration() should raise a KeyError if one or more global dict variables is missing information."""
        DUT = RAMSTKUserConfiguration()
        DUT.RAMSTK_PROG_CONF = VIRTUAL_ENV + '/share/RAMSTK/RAMSTK.toml'
        DUT.RAMSTK_PROG_INFO = {
            "host": "localhost",
            "socket": "3306",
            "user": "johnny.tester",
            "password": "clear.text.password"
        }

        with pytest.raises(KeyError):
            DUT.set_user_configuration()

    @pytest.mark.integration
    def test_set_user_directories_first_run(self):
        """set_user_directories() should return True on a first run of RAMSTK."""
        DUT = RAMSTKUserConfiguration()
        DUT.RAMSTK_HOME_DIR = '/tmp/shibboly'

        assert DUT.set_user_directories()
        assert DUT.RAMSTK_CONF_DIR == DUT.RAMSTK_SITE_DIR

    @pytest.mark.integration
    def test_set_user_directories_not_first_run(self):
        """set_user_directories() should return False when not a first run of RAMSTK."""
        DUT = RAMSTKUserConfiguration()

        assert not DUT.set_user_directories(first_run=False)
        assert DUT.RAMSTK_CONF_DIR == DUT.RAMSTK_HOME_DIR + "/.config/RAMSTK"
        assert DUT.RAMSTK_PROG_CONF == DUT.RAMSTK_CONF_DIR + "/RAMSTK.toml"
