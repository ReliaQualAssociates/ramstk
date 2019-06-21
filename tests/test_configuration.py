# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       ramstk.tests.test_configuration.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for the Configuration module algorithms and models."""

# Standard Library Imports
import gettext
import glob
import sys
from os import environ, getenv, path

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.Configuration import (
    RAMSTK_ACTIVE_ENVIRONMENTS, RAMSTK_ALLOCATION_MODELS, RAMSTK_CONTROL_TYPES,
    RAMSTK_COST_TYPES, RAMSTK_CRITICALITY, RAMSTK_DORMANT_ENVIRONMENTS,
    RAMSTK_FAILURE_PROBABILITY, RAMSTK_HR_DISTRIBUTIONS, RAMSTK_HR_MODELS,
    RAMSTK_HR_TYPES, RAMSTK_LIFECYCLE, RAMSTK_MTTR_TYPES, RAMSTK_S_DIST,
    RAMSTK_SW_APPLICATION, RAMSTK_SW_DEV_ENVIRONMENTS, RAMSTK_SW_DEV_PHASES,
    RAMSTK_SW_LEVELS, RAMSTK_SW_TEST_METHODS, Configuration,
)

try:
    VIRTUAL_ENV = glob.glob(environ['VIRTUAL_ENV'])[0]
except KeyError:
    if sys.platform == 'Linux':
        VIRTUAL_ENV = getenv('HOME') + '/.local'
    elif sys.platform == 'Windows':
        VIRTUAL_ENV = getenv('TEMP')
    else:
        print((
            "The {0:s} system platform is not "
            "supported."
        ).format(sys.platform))
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
            "IV",
            1,
        ],
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


@pytest.mark.integration
def test_initialize_configuration():
    """ __init__() should create an instance of the Configuration class. """
    DUT = Configuration()

    assert isinstance(DUT, Configuration)
    assert DUT.RAMSTK_MODE == ''
    assert DUT.RAMSTK_PROG_CONF == ''
    assert DUT.RAMSTK_SITE_CONF == ''
    assert DUT.RAMSTK_DEBUG_LOG == ''
    assert DUT.RAMSTK_IMPORT_LOG == ''
    assert DUT.RAMSTK_USER_LOG == ''

    assert DUT.RAMSTK_COLORS == {}
    assert DUT.RAMSTK_FORMAT_FILE == {}

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
    assert DUT.RAMSTK_MANUFACTURERS == {}
    assert DUT.RAMSTK_MEASUREMENT_UNITS == {}
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

    assert DUT.RAMSTK_RISK_POINTS == [4, 10]
    assert DUT.RAMSTK_MODE_SOURCE == 1
    assert DUT.RAMSTK_COM_BACKEND == ''
    assert DUT.RAMSTK_BACKEND == ''
    assert DUT.RAMSTK_COM_INFO == {}
    assert DUT.RAMSTK_PROG_INFO == {}
    assert DUT.RAMSTK_MODULES == {}
    assert DUT.RAMSTK_PAGE_NUMBER == {}
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
def test_get_site_configuration(test_configuration):
    """
    get_site_configuration() should return False on success
    """
    DUT = test_configuration
    _old_com_info = DUT.RAMSTK_COM_INFO

    assert not DUT.get_site_configuration()
    assert DUT.RAMSTK_COM_BACKEND == 'sqlite'
    assert DUT.RAMSTK_COM_INFO["host"] == 'localhost'
    assert DUT.RAMSTK_COM_INFO["socket"] == '3306'
    assert DUT.RAMSTK_COM_INFO[
        "database"
    ] == DUT.RAMSTK_SITE_DIR + '/ramstk_common.ramstk'
    assert DUT.RAMSTK_COM_INFO["user"] == 'ramstkcom'
    assert DUT.RAMSTK_COM_INFO["password"] == 'ramstkcom'

    DUT.RAMSTK_COM_INFO = _old_com_info


@pytest.mark.integration
def test_set_site_configuration(test_configuration):
    """
    _set_site_configuration() should return False on success
    """
    DUT = test_configuration
    _old_com_info = DUT.RAMSTK_COM_INFO

    assert not DUT._set_site_configuration()
    assert not DUT.get_site_configuration()

    assert DUT.RAMSTK_COM_BACKEND == 'sqlite'
    assert DUT.RAMSTK_COM_INFO["host"] == 'localhost'
    assert DUT.RAMSTK_COM_INFO["socket"] == '3306'
    assert DUT.RAMSTK_COM_INFO[
        "database"
    ] == DUT.RAMSTK_SITE_DIR + '/ramstk_common.ramstk'
    assert DUT.RAMSTK_COM_INFO["user"] == 'ramstkcom'
    assert DUT.RAMSTK_COM_INFO["password"] == 'ramstkcom'

    DUT.RAMSTK_COM_INFO = _old_com_info

@pytest.mark.integration
def test_create_user_configuration():
    """
    create_user_configuration() should return False on success
    """
    DUT = Configuration()

    DUT.RAMSTK_HOME_DIR = '/tmp'
    DUT.RAMSTK_SITE_DIR = VIRTUAL_ENV + '/share/RAMSTK'
    DUT.RAMSTK_PROG_CONF = '/tmp/.config/RAMSTK/RAMSTK.conf'

    assert not DUT.create_user_configuration()
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


@pytest.mark.integration
def test_get_user_configuration(test_configuration):
    """
    get_user_configuration() should return False on success
    """
    DUT = test_configuration

    assert not DUT.get_user_configuration()
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
        'validationfg': '#000000',
    }
    assert DUT.RAMSTK_FORMAT_FILE == {
        'allocation': 'Allocation.xml',
        'failure_definition': 'FailureDefinition.xml',
        'fmea': 'FMEA.xml',
        'function': 'Function.xml',
        'hardware': 'Hardware.xml',
        'hazops': 'HazOps.xml',
        'pof': 'PoF.xml',
        'requirement': 'Requirement.xml',
        'revision': 'Revision.xml',
        'similaritem': 'SimilarItem.xml',
        'stakeholder': 'Stakeholder.xml',
        'validation': 'Validation.xml',
    }
    assert DUT.RAMSTK_BACKEND == 'sqlite'
    assert DUT.RAMSTK_PROG_INFO["host"] == 'localhost'
    assert DUT.RAMSTK_PROG_INFO["socket"] == '3306'
    assert DUT.RAMSTK_PROG_INFO["database"] == (DUT._INSTALL_PREFIX + '/tmp/TestDB.ramstk')
    assert DUT.RAMSTK_PROG_INFO["user"] == 'johnny.tester'
    assert DUT.RAMSTK_PROG_INFO["password"] == 'clear.text.password'
    assert DUT.RAMSTK_DATA_DIR == (
        DUT._INSTALL_PREFIX +
        '/share/RAMSTK/layouts'
    )
    assert DUT.RAMSTK_ICON_DIR == (
        DUT._INSTALL_PREFIX +
        '/share/RAMSTK/icons'
    )
    assert DUT.RAMSTK_LOG_DIR == DUT._INSTALL_PREFIX + '/tmp/logs'
    assert DUT.RAMSTK_REPORT_SIZE == 'letter'
    assert DUT.RAMSTK_HR_MULTIPLIER == 1000000.0
    assert DUT.RAMSTK_DEC_PLACES == 6
    assert DUT.RAMSTK_MTIME == 100.0
    assert DUT.RAMSTK_MODE_SOURCE == '1'
    assert DUT.RAMSTK_TABPOS["listbook"] == 'bottom'
    assert DUT.RAMSTK_TABPOS["modulebook"] == 'top'
    assert DUT.RAMSTK_TABPOS["workbook"] == 'bottom'


@pytest.mark.integration
def test_get_user_configuration_no_prog_conf_file():
    """
    get_user_configuration() should return True when the program config file is missing
    """
    DUT = Configuration()

    assert DUT.get_user_configuration()

@pytest.mark.integration
def test_set_site_variables():
    """
    set_site_variables() should return False on success
    """
    DUT = Configuration()

    assert not DUT.set_site_variables()
    assert DUT.RAMSTK_SITE_DIR == DUT._INSTALL_PREFIX + '/share/RAMSTK'
    assert DUT.RAMSTK_CONF_DIR == DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK'
    assert DUT.RAMSTK_DATA_DIR == (
        DUT.RAMSTK_HOME_DIR +
        "/.config/RAMSTK/layouts"
    )
    assert DUT.RAMSTK_ICON_DIR == DUT.RAMSTK_HOME_DIR + "/.config/RAMSTK/icons"
    assert DUT.RAMSTK_LOG_DIR == DUT.RAMSTK_HOME_DIR + "/.config/RAMSTK/logs"
    assert DUT.RAMSTK_SITE_CONF == DUT.RAMSTK_CONF_DIR + "/Site.conf"


@pytest.mark.integration
def test_set_user_configuration():
    """
    set_user_configuration() should return False on success
    """
    DUT = Configuration()

    DUT.RAMSTK_HOME_DIR = '/tmp'
    DUT.RAMSTK_SITE_DIR = VIRTUAL_ENV + '/share/RAMSTK'
    DUT.RAMSTK_PROG_CONF = '/tmp/.config/RAMSTK/RAMSTK.conf'
    DUT.create_user_configuration()

    DUT.RAMSTK_REPORT_SIZE = 'A4'
    DUT.RAMSTK_HR_MULTIPLIER = 1000.0
    DUT.RAMSTK_MTIME = 24.0
    DUT.RAMSTK_DEC_PLACES = 4
    DUT.RAMSTK_MODE_SOURCE = '1'
    DUT.RAMSTK_TABPOS["listbook"] = 'bottom'
    DUT.RAMSTK_TABPOS["modulebook"] = 'top'
    DUT.RAMSTK_TABPOS["workbook"] = 'bottom'
    DUT.RAMSTK_BACKEND = 'mysql'
    DUT.RAMSTK_PROG_INFO = {"host": 'treebeard', 'socket': 3306, 'database': 'test', 'user': 'me', 'password': 'big.password'}
    DUT.RAMSTK_COLORS = {
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
        'validationfg': '#000000',
    }
    DUT.RAMSTK_FORMAT_FILE = {
        'allocation': 'MyAllocation.txt',
        'failure_definition': 'FailureDefinition.xml',
        'fmea': 'FMEA.xml',
        'function': 'Function.xml',
        'hardware': 'Hardware.xml',
        'hazops': 'HazOps.xml',
        'pof': 'PoF.xml',
        'requirement': 'Requirement.xml',
        'revision': 'Revision.xml',
        'similaritem': 'SimilarItem.xml',
        'stakeholder': 'Stakeholder.xml',
        'validation': 'Validation.xml',
    }

    assert not DUT.set_user_configuration()

    DUT.get_user_configuration()

    assert DUT.RAMSTK_REPORT_SIZE == 'A4'
    assert DUT.RAMSTK_HR_MULTIPLIER == 1000.0
    assert DUT.RAMSTK_MTIME == 24.0
    assert DUT.RAMSTK_DEC_PLACES == 4
    assert DUT.RAMSTK_MODE_SOURCE == '1'
    assert DUT.RAMSTK_FORMAT_FILE['allocation'] == 'MyAllocation.txt'


@pytest.mark.integration
def test_set_user_variables():
    """
    set_user_variables() should return False on success
    """
    DUT = Configuration()

    DUT.RAMSTK_HOME_DIR = '/tmp'

    assert not DUT.set_user_variables()

    DUT.get_user_configuration()

    assert DUT.RAMSTK_CONF_DIR == DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK'
    assert DUT.RAMSTK_PROG_CONF == DUT.RAMSTK_HOME_DIR + '/.config/RAMSTK/RAMSTK.conf'
