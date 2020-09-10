# pylint: disable=protected-access, no-self-use, missing-docstring, invalid-name, unused-argument
# -*- coding: utf-8 -*-
#
#       ramstk.tests.test_configuration.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the Configuration module algorithms and models."""

# Standard Library Imports
import gettext
import glob
import shutil
import sys
from os import environ, getenv, mkdir, path

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTK_ACTIVE_ENVIRONMENTS, RAMSTK_ALLOCATION_MODELS, RAMSTK_CONTROL_TYPES,
    RAMSTK_COST_TYPES, RAMSTK_CRITICALITY, RAMSTK_DORMANT_ENVIRONMENTS,
    RAMSTK_FAILURE_PROBABILITY, RAMSTK_HR_DISTRIBUTIONS, RAMSTK_HR_MODELS,
    RAMSTK_HR_TYPES, RAMSTK_LIFECYCLE, RAMSTK_MTTR_TYPES, RAMSTK_S_DIST,
    RAMSTK_SW_APPLICATION, RAMSTK_SW_DEV_ENVIRONMENTS, RAMSTK_SW_DEV_PHASES,
    RAMSTK_SW_LEVELS, RAMSTK_SW_TEST_METHODS, RAMSTKSiteConfiguration,
    RAMSTKUserConfiguration)

try:
    VIRTUAL_ENV = glob.glob(environ['VIRTUAL_ENV'])[0]
except KeyError:
    if sys.platform == 'Linux' or sys.platform == 'linux':
        VIRTUAL_ENV = getenv('HOME') + '/.local'
    elif sys.platform == 'Windows' or sys.platform == 'windows':
        VIRTUAL_ENV = getenv('TEMP')
    else:
        print(("The {0:s} system platform is not "
               "supported.").format(sys.platform))
        sys.exit(1)

_ = gettext.gettext


@pytest.mark.unit
def test_static_variables():
    """
    Static variables should have the proper data.
    """
    assert RAMSTK_ACTIVE_ENVIRONMENTS == [
        [_("Ground, Benign")],
        [_("Ground, Fixed")],
        [_("Ground, Mobile")],
        [_("Naval, Sheltered")],
        [_("Naval, Unsheltered")],
        [_("Airborne, Inhabited, Cargo")],
        [_("Airborne, Inhabited, Fighter")],
        [_("Airborne, Uninhabited, Cargo")],
        [_("Airborne, Uninhabited, Fighter")],
        [_("Airborne, Rotary Wing")],
        [_("Space, Flight")],
        [_("Missile, Flight")],
        [_("Missile, Launch")],
    ]
    assert RAMSTK_DORMANT_ENVIRONMENTS == [
        [_("Airborne")],
        [_("Ground")],
        [_("Naval")],
        [_("Space")],
    ]
    assert RAMSTK_ALLOCATION_MODELS == [
        ["Equal Apportionment"],
        ["ARINC Apportionment"],
        ["AGREE Apportionment"],
        ["Feasibility of Objectives"],
        ["Repairable Systems Apportionment"],
    ]
    assert RAMSTK_HR_TYPES == [
        [_("Assessed")],
        [_("Defined, Hazard Rate")],
        [_("Defined, MTBF")],
        [_("Defined, Distribution")],
    ]
    assert RAMSTK_HR_MODELS == [
        [_("MIL-HDBK-217F Parts Count")],
        [_("MIL-HDBK-217F Parts Stress")],
        [_("NSWC-11")],
    ]
    assert RAMSTK_HR_DISTRIBUTIONS == [
        [_("1P Exponential")],
        [_("2P Exponential")],
        [_("Gaussian")],
        [_("Lognormal")],
        [_("2P Weibull")],
        [_("3P Weibull")],
    ]
    assert RAMSTK_CONTROL_TYPES == [_("Prevention"), _("Detection")]
    assert RAMSTK_COST_TYPES == [[_("Defined")], [_("Calculated")]]
    assert RAMSTK_MTTR_TYPES == [[_("Defined")], [_("Calculated")]]
    assert RAMSTK_CRITICALITY == [
        [
            _("Catastrophic"),
            _(
                "Could result in death, permanent total disability, loss exceeding "
                "$1M, or irreversible severe environmental damage that violates law "
                "or regulation.", ),
            "I",
            4,
        ],
        [
            _("Critical"),
            _(
                "Could result in permanent partial disability, injuries or "
                "occupational illness that may result in hospitalization of at least "
                "three personnel, loss exceeding $200K but less than $1M, or "
                "reversible environmental damage causing a violation of law or "
                "regulation.", ),
            "II",
            3,
        ],
        [
            _("Marginal"),
            _(
                "Could result in injury or occupational illness resulting in one or "
                "more lost work days(s), loss exceeding $10K but less than $200K, or "
                "mitigatible environmental damage without violation of law or "
                "regulation where restoration activities can be accomplished.",
            ),
            "III",
            2,
        ],
        [
            _("Negligble"),
            _(
                "Could result in injury or illness not resulting in a lost work "
                "day, loss exceeding $2K but less than $10K, or minimal "
                "environmental damage not violating law or regulation.", ),
            "IV", 1
        ]
    ]
    assert RAMSTK_FAILURE_PROBABILITY == [
        [_("Level E - Extremely Unlikely"), 1],
        [_("Level D - Remote"), 2],
        [_("Level C - Occasional"), 3],
        [_("Level B - Reasonably Probable"), 4],
        [_("Level A - Frequent"), 5],
    ]
    assert RAMSTK_SW_DEV_ENVIRONMENTS == [
        [_("Organic"), 1.0, 0.76],
        [_("Semi-Detached"), 1.0, 1.0],
        [_("Embedded"), 1.0, 1.3],
    ]
    assert RAMSTK_SW_DEV_PHASES == [
        [_("Concept/Planning (PCP)")],
        [_("Requirements Analysis (SRA)")],
        [_("Preliminary Design Review (PDR)")],
        [_("Critical Design Review (CDR)")],
        [_("Test Readiness Review (TRR)")],
        [_("Released")],
    ]
    assert RAMSTK_SW_LEVELS == [
        [_("Software System"), 0],
        [_("Software Module"), 0],
        [_("Software Unit"), 0],
    ]
    assert RAMSTK_SW_APPLICATION == [
        [_("Airborne"), 0.0128, 6.28],
        [_("Strategic"), 0.0092, 1.2],
        [_("Tactical"), 0.0078, 13.8],
        [_("Process Control"), 0.0018, 3.8],
        [_("Production Center"), 0.0085, 23.0],
        [_("Developmental"), 0.0123, 132.6],
    ]
    assert RAMSTK_SW_TEST_METHODS == [
        [
            _("Code Reviews"),
            _(
                "Code review is a systematic examination (often known as peer "
                "review) of computer source code.", ),
        ],
        [_("Error/Anomaly Detection"), _("")],
        [_("Structure Analysis"), _("")],
        [_("Random Testing"), _("")],
        [_("Functional Testing"), _("")],
        [_("Branch Testing"), _("")],
    ]
    assert RAMSTK_LIFECYCLE == [
        [_("Design")],
        [_("Reliability Growth")],
        [_("Reliability Qualification")],
        [_("Production")],
        [_("Storage")],
        [_("Operation")],
        [_("Disposal")],
    ]
    assert RAMSTK_S_DIST == [
        ["Constant Probability"],
        ["Exponential"],
        ["Gaussian"],
        ["LogNormal"],
        ["Uniform"],
        ["Weibull"],
    ]


@pytest.mark.usefixtures('make_shibboly', 'make_config_dir',
                         'make_home_config_dir')
class TestCreateConfiguration():
    """Class for testing the site configuration module."""
    def on_create_site_configuration(self):
        print(
            "\033[36m\nsucceed_create_site_configuration topic was broadcast.")

    def on_create_user_configuration(self):
        print(
            "\033[36m\nsucceed_create_user_configuration topic was broadcast.")

    def on_fail_create_user_configuration(self, error_message):
        assert error_message == ('User\'s configuration directory '
                                 '/opt/.config/RAMSTK does not exist and '
                                 'could not be created when attempting to '
                                 'create a new user configuration file.')
        print(
            "\033[35m\nfail_create_user_configuration topic was broadcast; no "
            "configuration directory.")

    def on_fail_create_data_dir(self, error_message):
        assert error_message == ('User\'s data directory '
                                 '/opt/.config/RAMSTK/layouts does not '
                                 'exist and could not be created when '
                                 'attempting to create a new user '
                                 'configuration file.')
        print(
            "\033[35m\nfail_create_user_configuration topic was broadcast; no "
            "data directory.")

    def on_fail_create_icon_dir(self, error_message):
        assert error_message == ('User\'s icon directory '
                                 '/opt/.config/RAMSTK/icons does not '
                                 'exist and could not be created when '
                                 'attempting to create a new user '
                                 'configuration file.')
        print(
            "\033[35m\nfail_create_user_configuration topic was broadcast; no "
            "icon directory.")

    def on_fail_create_log_dir(self, error_message):
        assert error_message == ('User\'s log directory '
                                 '/opt/.config/RAMSTK/logs does not exist '
                                 'and could not be created when '
                                 'attempting to create a new user '
                                 'configuration file.')
        print(
            "\033[35m\nfail_create_user_configuration topic was broadcast; no "
            "log directory.")

    def on_fail_create_program_dir(self, error_message):
        assert error_message == ('Program directory /opt/analyses/ramstk does '
                                 'not exist and could not be created when '
                                 'attempting to create a new user '
                                 'configuration file.')
        print(
            "\033[35m\nfail_create_user_configuration topic was broadcast; no "
            "program directory.")

    @pytest.mark.unit
    def test_initialize_site_configuration(self):
        """ __init__() should create an instance of the site configuration class. """
        DUT = RAMSTKSiteConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV

        assert isinstance(DUT, RAMSTKSiteConfiguration)
        assert DUT.RAMSTK_COM_INFO == {}
        assert DUT.RAMSTK_ACTION_CATEGORY == {}
        assert DUT.RAMSTK_ACTION_STATUS == {}
        assert DUT.RAMSTK_AFFINITY_GROUPS == {}
        assert DUT.RAMSTK_CATEGORIES == {}
        assert DUT.RAMSTK_DAMAGE_MODELS == {}
        assert DUT.RAMSTK_DETECTION_METHODS == {}
        assert DUT.RAMSTK_FAILURE_MODES == {}
        assert DUT.RAMSTK_HAZARDS == {}
        assert DUT.RAMSTK_INCIDENT_CATEGORY == {}
        assert DUT.RAMSTK_INCIDENT_STATUS == {}
        assert DUT.RAMSTK_INCIDENT_TYPE == {}
        assert DUT.RAMSTK_LOAD_HISTORY == {}
        assert DUT.RAMSTK_MANUFACTURERS == {}
        assert DUT.RAMSTK_MEASURABLE_PARAMETERS == {}
        assert DUT.RAMSTK_MEASUREMENT_UNITS == {}
        assert DUT.RAMSTK_MODULES == {}
        assert DUT.RAMSTK_REQUIREMENT_TYPE == {}
        assert DUT.RAMSTK_RPN_DETECTION == {}
        assert DUT.RAMSTK_RPN_OCCURRENCE == {}
        assert DUT.RAMSTK_RPN_SEVERITY == {}
        assert DUT.RAMSTK_SEVERITY == {}
        assert DUT.RAMSTK_STAKEHOLDERS == {}
        assert DUT.RAMSTK_STRESS_LIMITS == {}
        assert DUT.RAMSTK_SUBCATEGORIES == {}
        assert DUT.RAMSTK_USERS == {}
        assert DUT.RAMSTK_VALIDATION_TYPE == {}
        assert DUT.RAMSTK_WORKGROUPS == {}
        assert DUT.RAMSTK_COM_BACKEND == ''

        # If testing RAMSTK that was installed by `pip install -e .`, then you
        # won't be testing files installed in the VIRTUAL_ENV.  Since the
        # RAMSTK files will not be in the VIRTUAL_ENV, sys will not have the
        # real_prefix attribute.  In this case, skip these tests.
        if hasattr(sys, 'real_prefix'):
            if sys.platform == "linux" or sys.platform == "linux2":
                assert DUT.RAMSTK_SITE_DIR == VIRTUAL_ENV + "/share/RAMSTK"
            elif sys.platform == "win32":
                assert DUT.RAMSTK_SITE_DIR == VIRTUAL_ENV + "/RAMSTK"

        assert DUT.RAMSTK_SITE_CONF == DUT.RAMSTK_SITE_DIR + "/Site.toml"

    @pytest.mark.unit
    def test_initialize_user_configuration(self):
        """ __init__() should create an instance of the user configuration class. """
        DUT = RAMSTKUserConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV

        assert DUT.RAMSTK_COLORS == {}
        assert DUT.RAMSTK_FORMAT_FILE == {}
        assert DUT.RAMSTK_PAGE_NUMBER == {
            0: 'revision',
            1: 'function',
            2: 'requirement',
            3: 'hardware',
            4: 'validation'
        }
        assert DUT.RAMSTK_PROG_INFO == {}
        assert DUT.RAMSTK_STRESS_LIMITS == {}
        assert DUT.RAMSTK_TABPOS == {
            "listbook": "top",
            "modulebook": "bottom",
            "workbook": "bottom"
        }
        assert DUT.RAMSTK_RISK_POINTS == [4, 10]
        assert DUT.RAMSTK_MODE == ""
        assert DUT.RAMSTK_MODE_SOURCE == 1  # 1=FMD-97
        assert DUT.RAMSTK_BACKEND == ""
        assert DUT.RAMSTK_REPORT_SIZE == "letter"
        assert DUT.RAMSTK_HR_MULTIPLIER == 1000000.0
        assert DUT.RAMSTK_DEC_PLACES == 6
        assert DUT.RAMSTK_MTIME == 100.0
        assert DUT.RAMSTK_GUI_LAYOUT == "advanced"
        assert DUT.RAMSTK_METHOD == "STANDARD"  # STANDARD or LRM
        assert DUT.RAMSTK_LOCALE == "en_US.UTF8"
        assert DUT.RAMSTK_LOGLEVEL == "INFO"

        # If testing RAMSTK that was installed by `pip install -e .`, then you
        # won't be testing files installed in the VIRTUAL_ENV.  Since the
        # RAMSTK files will not be in the VIRTUAL_ENV, sys will not have the
        # real_prefix attribute.  In this case, skip these tests.
        if sys.platform == "linux" or sys.platform == "linux2":
            assert DUT.RAMSTK_OS == "Linux"
            assert DUT.RAMSTK_HOME_DIR == environ["HOME"]
            if hasattr(sys, 'real_prefix'):
                assert DUT.RAMSTK_CONF_DIR == DUT._INSTALL_PREFIX + "/share/RAMSTK"
        elif sys.platform == "win32":
            assert DUT.RAMSTK_OS == "Windows"
            assert DUT.RAMSTK_HOME_DIR == environ["USERPROFILE"]
            if hasattr(sys, 'real_prefix'):
                assert DUT.RAMSTK_CONF_DIR == environ["PYTHONPATH"] + "/RAMSTK"

        assert DUT.RAMSTK_DATA_DIR == DUT.RAMSTK_CONF_DIR + "/layouts"
        assert DUT.RAMSTK_ICON_DIR == DUT.RAMSTK_CONF_DIR + "/icons"
        assert DUT.RAMSTK_LOG_DIR == DUT.RAMSTK_CONF_DIR + "/logs"
        assert DUT.RAMSTK_PROG_DIR == DUT.RAMSTK_HOME_DIR + "/analyses/ramstk/"

        assert DUT.RAMSTK_PROG_CONF == DUT.RAMSTK_CONF_DIR + "/RAMSTK.toml"
        assert DUT.RAMSTK_USER_LOG == DUT.RAMSTK_LOG_DIR + "/ramstk_run.log"
        assert DUT.RAMSTK_IMPORT_LOG == (DUT.RAMSTK_LOG_DIR
                                         + "/ramstk_import.log")

    @pytest.mark.unit
    def test_create_site_configuration(self):
        """do_create_site_configuration() should broadcast the succcess message on success."""
        pub.subscribe(self.on_create_site_configuration,
                      'succeed_create_site_configuration')

        DUT = RAMSTKSiteConfiguration()

        DUT.RAMSTK_SITE_DIR = VIRTUAL_ENV + '/share/RAMSTK'
        DUT.RAMSTK_SITE_CONF = DUT.RAMSTK_SITE_DIR + '/RAMSTK.toml'

        assert DUT.do_create_site_configuration() is None

        pub.unsubscribe(self.on_create_site_configuration,
                        'succeed_create_site_configuration')

    @pytest.mark.unit
    def test_do_create_user_configuration(self, make_home_config_dir):
        """do_create_user_configuration() should return None on success."""
        pub.subscribe(self.on_create_user_configuration,
                      'succeed_create_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV
        DUT.RAMSTK_HOME_DIR = VIRTUAL_ENV + '/tmp'
        DUT.RAMSTK_PROG_CONF = VIRTUAL_ENV + '/RAMSTK.toml'

        assert DUT.do_create_user_configuration() is None
        assert path.isdir(make_home_config_dir + '/icons')
        assert path.isdir(make_home_config_dir + '/layouts')
        assert path.isdir(make_home_config_dir + '/logs')
        assert path.isdir(make_home_config_dir + '/icons/16x16')
        assert path.isdir(make_home_config_dir + '/icons/32x32')
        assert path.isfile(make_home_config_dir + '/layouts/allocation.toml')
        assert path.isfile(make_home_config_dir + '/layouts/fmea.toml')
        assert path.isfile(make_home_config_dir
                           + '/layouts/failure_definition.toml')
        assert path.isfile(make_home_config_dir + '/layouts/function.toml')
        assert path.isfile(make_home_config_dir + '/layouts/hardware.toml')
        assert path.isfile(make_home_config_dir + '/layouts/hazops.toml')
        # assert path.isfile(make_home_config_dir + '/layouts/incident.toml')
        assert path.isfile(make_home_config_dir + '/layouts/pof.toml')
        assert path.isfile(make_home_config_dir + '/layouts/requirement.toml')
        assert path.isfile(make_home_config_dir + '/layouts/revision.toml')
        assert path.isfile(make_home_config_dir + '/layouts/similar_item.toml')
        # assert path.isfile(make_home_config_dir + '/layouts/Software.toml')
        assert path.isfile(make_home_config_dir + '/layouts/stakeholder.toml')
        # assert path.isfile(make_home_config_dir + '/layouts/Testing.toml')
        assert path.isfile(make_home_config_dir + '/layouts/validation.toml')

        pub.unsubscribe(self.on_create_user_configuration,
                        'succeed_create_user_configuration')

    @pytest.mark.unit
    def test_do_create_user_configuration_no_user_config_dir(self):
        """do_create_user_configuration() should return None on success."""
        pub.subscribe(self.on_fail_create_user_configuration,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV
        DUT.RAMSTK_HOME_DIR = '/opt'

        assert DUT._do_make_configuration_dir() is None

        pub.unsubscribe(self.on_fail_create_user_configuration,
                        'fail_create_user_configuration')

    @pytest.mark.unit
    def test_do_create_user_configuration_no_user_data_dir(self):
        """_do_make_data_dir() should return None on success."""
        pub.subscribe(self.on_fail_create_data_dir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV
        DUT.RAMSTK_CONF_DIR = '/opt/.config/RAMSTK'

        assert DUT._do_make_data_dir() is None

        pub.unsubscribe(self.on_fail_create_data_dir,
                        'fail_create_user_configuration')

    @pytest.mark.unit
    def test_do_create_user_configuration_no_user_icon_dir(self):
        """_do_make_icon_dir() should return None on success."""
        pub.subscribe(self.on_fail_create_icon_dir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV
        DUT.RAMSTK_CONF_DIR = '/opt/.config/RAMSTK'

        assert DUT._do_make_icon_dir() is None

        pub.unsubscribe(self.on_fail_create_icon_dir,
                        'fail_create_user_configuration')

    @pytest.mark.unit
    def test_do_create_user_configuration_no_user_log_dir(self):
        """_do_make_log_dir() should return None on success."""
        pub.subscribe(self.on_fail_create_log_dir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV
        DUT.RAMSTK_CONF_DIR = '/opt/.config/RAMSTK'

        assert DUT._do_make_log_dir() is None

        pub.unsubscribe(self.on_fail_create_log_dir,
                        'fail_create_user_configuration')

    @pytest.mark.unit
    def test_do_create_user_configuration_no_user_program_dir(self):
        """_do_make_prog_dir() should return None on success."""
        pub.subscribe(self.on_fail_create_program_dir,
                      'fail_create_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV
        DUT.RAMSTK_PROG_DIR = '/opt/analyses/ramstk'

        assert DUT._do_make_program_dir() is None

        pub.unsubscribe(self.on_fail_create_program_dir,
                        'fail_create_user_configuration')


@pytest.mark.usefixtures('test_toml_site_configuration',
                         'test_toml_user_configuration', 'make_shibboly',
                         'make_config_dir')
class TestGetterSetter():
    """Class for testing that the site configuration module can be read."""
    def on_fail_get_site_configuration(self, error_message):
        assert error_message == (
            "Failed to read Site configuration file "
            "{0:s}/share/RAMSTK/BigSite.toml.").format(VIRTUAL_ENV)
        print("\033[35m\nfail_get_site_configuration topic was broadcast.")

    def on_succeed_set_site_configuration(self, configuration):
        assert isinstance(configuration, str)
        print("\033[36m\nsucceed_set_site_configuration topic was broadcast.")

    def on_fail_get_user_configuration(self, error_message):
        assert error_message == (
            "Failed to read User configuration file "
            "{0:s}/tmp/.config/RAMSTK/BigUser.toml.").format(VIRTUAL_ENV)
        print("\033[35m\nfail_get_user_configuration topic was broadcast.")

    @pytest.mark.unit
    def test_get_site_configuration(self):
        """get_site_configuration() should broadcast the succcess message on success."""
        DUT = RAMSTKSiteConfiguration()
        DUT.RAMSTK_SITE_CONF = VIRTUAL_ENV + '/share/RAMSTK/Site.toml'

        assert DUT.get_site_configuration() is None
        assert DUT.RAMSTK_COM_BACKEND == 'sqlite'
        assert DUT.RAMSTK_COM_INFO["dialect"] == 'sqlite'
        assert DUT.RAMSTK_COM_INFO["host"] == 'localhost'
        assert DUT.RAMSTK_COM_INFO["port"] == '3306'
        assert DUT.RAMSTK_COM_INFO["database"] == (
            VIRTUAL_ENV + '/share/RAMSTK/ramstk_common.ramstk')
        assert DUT.RAMSTK_COM_INFO["user"] == 'johnny.tester'
        assert DUT.RAMSTK_COM_INFO["password"] == 'clear.text.password'

    @pytest.mark.unit
    def test_get_site_configuration_no_conf_file(self):
        """get_site_configuration() should broadcase the fail message when there is no configuration file."""
        pub.subscribe(self.on_fail_get_site_configuration,
                      'fail_get_site_configuration')

        DUT = RAMSTKSiteConfiguration()
        DUT.RAMSTK_SITE_CONF = VIRTUAL_ENV + "/share/RAMSTK/BigSite.toml"

        assert DUT.get_site_configuration() is None

        pub.unsubscribe(self.on_fail_get_site_configuration,
                        'fail_get_site_configuration')

    @pytest.mark.unit
    def test_set_site_directories(self):
        """set_site_directories() should return None on success."""
        DUT = RAMSTKSiteConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV

        assert DUT.set_site_directories() is None
        assert DUT.RAMSTK_SITE_DIR == DUT._INSTALL_PREFIX + '/share/RAMSTK'
        assert DUT.RAMSTK_SITE_CONF == DUT.RAMSTK_SITE_DIR + "/Site.toml"

    @pytest.mark.unit
    def test_set_site_directories_no_site_conf_file(self):
        """set_site_directories() should return None on success and create a new site configuration file if one doesn't exist."""
        DUT = RAMSTKSiteConfiguration()
        DUT._INSTALL_PREFIX = '/tmp'
        mkdir(DUT._INSTALL_PREFIX + '/share')
        mkdir(DUT._INSTALL_PREFIX + '/share/RAMSTK')

        assert DUT.set_site_directories() is None
        assert DUT.RAMSTK_SITE_DIR == DUT._INSTALL_PREFIX + '/share/RAMSTK'
        assert DUT.RAMSTK_SITE_CONF == DUT.RAMSTK_SITE_DIR + "/Site.toml"
        assert path.isfile('/tmp/share/RAMSTK/Site.toml')

        shutil.rmtree('/tmp/share')

    @pytest.mark.unit
    def test_get_user_configuration(self, test_toml_user_configuration):
        """get_user_configuration() should return None on success."""
        DUT = test_toml_user_configuration

        assert DUT.get_user_configuration() is None
        assert DUT.RAMSTK_COLORS == {
            'functionbg': '#FFFFFF',
            'functionfg': '#000000',
            'hardwarebg': '#FFFFFF',
            'hardwarefg': '#000000',
            'hazardbg': '#FFFFFF',
            'hazardfg': '#000000',
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
            'allocation': 'allocation.toml',
            'failure_definition': 'failure_definition.toml',
            'fmea': 'fmea.toml',
            'function': 'function.toml',
            'hardware': 'hardware.toml',
            'hazard': 'hazops.toml',
            'pof': 'pof.toml',
            'requirement': 'requirement.toml',
            'revision': 'revision.toml',
            'similar_item': 'similar_item.toml',
            'stakeholder': 'stakeholder.toml',
            'validation': 'validation.toml',
        }
        assert DUT.RAMSTK_STRESS_LIMITS == {
            1: [0.8, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            2: [1.0, 1.0, 0.7, 0.9, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            3: [1.0, 1.0, 0.5, 0.9, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            4: [1.0, 1.0, 1.0, 1.0, 0.6, 0.9, 10.0, 0.0, 125.0, 125.0],
            5: [0.6, 0.9, 1.0, 1.0, 0.5, 0.9, 15.0, 0.0, 125.0, 125.0],
            6: [0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            7: [0.75, 0.9, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            8: [0.7, 0.9, 1.0, 1.0, 0.7, 0.9, 25.0, 0.0, 125.0, 125.0],
            9: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0],
            10: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 125.0, 125.0]
        }
        assert DUT.RAMSTK_BACKEND == 'sqlite'
        assert DUT.RAMSTK_PROG_INFO["dialect"] == 'sqlite'
        assert DUT.RAMSTK_PROG_INFO["host"] == 'localhost'
        assert DUT.RAMSTK_PROG_INFO["port"] == '3306'
        assert DUT.RAMSTK_PROG_INFO["database"] == ''
        assert DUT.RAMSTK_PROG_INFO["user"] == ''
        assert DUT.RAMSTK_PROG_INFO["password"] == ''
        assert DUT.RAMSTK_DATA_DIR == DUT.RAMSTK_CONF_DIR + '/layouts'
        assert DUT.RAMSTK_ICON_DIR == DUT.RAMSTK_CONF_DIR + '/icons'
        assert DUT.RAMSTK_LOG_DIR == DUT.RAMSTK_CONF_DIR + '/logs'
        assert DUT.RAMSTK_PROG_DIR == DUT.RAMSTK_HOME_DIR + '/analyses/ramstk'
        assert DUT.RAMSTK_REPORT_SIZE == 'letter'
        assert DUT.RAMSTK_HR_MULTIPLIER == 1000000.0
        assert DUT.RAMSTK_DEC_PLACES == 6
        assert DUT.RAMSTK_MTIME == 100.0
        assert DUT.RAMSTK_MODE_SOURCE == '1'
        assert DUT.RAMSTK_TABPOS["listbook"] == 'bottom'
        assert DUT.RAMSTK_TABPOS["modulebook"] == 'top'
        assert DUT.RAMSTK_TABPOS["workbook"] == 'bottom'
        assert DUT.RAMSTK_USER_LOG == (DUT.RAMSTK_LOG_DIR + "/ramstk_run.log")
        assert DUT.RAMSTK_IMPORT_LOG == (DUT.RAMSTK_LOG_DIR
                                         + "/ramstk_import.log")

    @pytest.mark.unit
    def test_get_user_configuration_no_conf_file(self):
        """get_user_configuration() should broadcase the fail message when there is no configuration file."""
        pub.subscribe(self.on_fail_get_user_configuration,
                      'fail_get_user_configuration')

        DUT = RAMSTKUserConfiguration()
        DUT.RAMSTK_PROG_CONF = VIRTUAL_ENV + "/tmp/.config/RAMSTK/BigUser.toml"

        assert DUT.get_user_configuration() is None

        pub.unsubscribe(self.on_fail_get_user_configuration,
                        'fail_get_user_configuration')

    @pytest.mark.unit
    def test_set_user_configuration(self):
        """set_user_configuration() should return None on success."""
        DUT = RAMSTKUserConfiguration()
        DUT.RAMSTK_PROG_CONF = VIRTUAL_ENV + '/tmp/.config/RAMSTK/RAMSTK.toml'

        # Create a default user configuration file and then read it.
        DUT.do_create_user_configuration()
        DUT.get_user_configuration()

        DUT.RAMSTK_REPORT_SIZE = 'A4'
        DUT.RAMSTK_HR_MULTIPLIER = 1000.0
        DUT.RAMSTK_MTIME = 24.0
        DUT.RAMSTK_DEC_PLACES = 4
        DUT.RAMSTK_BACKEND = 'mysql'
        DUT.RAMSTK_PROG_INFO = {
            'dialect': 'mysql',
            'host': 'treebeard',
            'port': '3306',
            'database': 'test',
            'user': 'me',
            'password': 'big.password'
        }

        assert DUT.set_user_configuration() is None

        DUT.get_user_configuration()

        assert DUT.RAMSTK_REPORT_SIZE == 'A4'
        assert DUT.RAMSTK_HR_MULTIPLIER == 1000.0
        assert DUT.RAMSTK_MTIME == 24.0
        assert DUT.RAMSTK_DEC_PLACES == 4
        assert DUT.RAMSTK_BACKEND == 'mysql'
        assert DUT.RAMSTK_PROG_INFO == {
            'dialect': 'mysql',
            'host': 'treebeard',
            'port': '3306',
            'database': 'test',
            'user': 'me',
            'password': 'big.password'
        }

    @pytest.mark.unit
    def test_set_user_directories(self):
        """set_user_variables() should return None on success when configuration directory structure exists in user's $HOME."""
        DUT = RAMSTKUserConfiguration()
        DUT.RAMSTK_HOME_DIR = VIRTUAL_ENV + '/tmp'

        assert DUT.set_user_directories() is None

        assert DUT.RAMSTK_CONF_DIR == DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK'
        assert DUT.RAMSTK_PROG_CONF == DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK/RAMSTK.toml'
        assert DUT.RAMSTK_DATA_DIR == DUT.RAMSTK_CONF_DIR + '/layouts'
        assert DUT.RAMSTK_ICON_DIR == DUT.RAMSTK_CONF_DIR + '/icons'
        assert DUT.RAMSTK_LOG_DIR == DUT.RAMSTK_CONF_DIR + '/log'
        assert DUT.RAMSTK_PROG_DIR == DUT.RAMSTK_HOME_DIR + '/analyses/ramstk'

    @pytest.mark.unit
    def test_set_user_directories_no_home(self):
        """set_user_variables() should return None on success when configuration directory structure does NOT exist in user's $HOME."""
        DUT = RAMSTKUserConfiguration()
        DUT._INSTALL_PREFIX = VIRTUAL_ENV
        DUT.RAMSTK_HOME_DIR = VIRTUAL_ENV + '/home'

        assert DUT.set_user_directories() is None

        assert DUT.RAMSTK_CONF_DIR == VIRTUAL_ENV + '/share/RAMSTK'
        assert DUT.RAMSTK_PROG_CONF == VIRTUAL_ENV + '/share/RAMSTK/RAMSTK.toml'
        assert DUT.RAMSTK_DATA_DIR == DUT.RAMSTK_CONF_DIR + '/layouts'
        assert DUT.RAMSTK_ICON_DIR == DUT.RAMSTK_CONF_DIR + '/icons'
        assert DUT.RAMSTK_LOG_DIR == DUT.RAMSTK_CONF_DIR + '/log'
        assert DUT.RAMSTK_PROG_DIR == DUT.RAMSTK_HOME_DIR
