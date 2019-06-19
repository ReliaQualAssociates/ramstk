# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.conftest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK test suite configuration module."""

# Standard Library Imports
import csv
import gettext
import glob
import os
import platform
import sys
import tempfile
import xml.etree.ElementTree as ET

# Third Party Imports
import pytest
import xlwt

# RAMSTK Package Imports
import ramstk.Utilities as Utilities
from ramstk.Configuration import Configuration
from ramstk.dao import DAO, do_create_test_database

_ = gettext.gettext

TEMPDIR = tempfile.gettempdir()

try:
    VIRTUAL_ENV = glob.glob(os.environ['VIRTUAL_ENV'])[0]
except KeyError:
    if platform.system() == 'Linux':
        VIRTUAL_ENV = os.getenv('HOME') + '/.local'
    elif platform.system() == 'Windows':
        VIRTUAL_ENV = os.getenv('TEMP')
    else:
        print((
            "The {0:s} system platform is not "
            "supported."
        ).format(platform.system()))
        sys.exit(1)

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_DIR = VIRTUAL_ENV + '/share/RAMSTK'
DATA_DIR = CONF_DIR + '/data'
ICON_DIR = CONF_DIR + '/icons'
TMP_DIR = VIRTUAL_ENV + '/tmp'
LOG_DIR = TMP_DIR + '/logs'
TEST_PROGRAM_DB_PATH = TMP_DIR + '/TestDB.ramstk'
TEST_COMMON_DB_PATH = TMP_DIR + '/TestCommonDB.ramstk'
TEST_PROGRAM_DB_URI = 'sqlite:///' + TEST_PROGRAM_DB_PATH
TEST_COMMON_DB_URI = 'sqlite:///' + TEST_COMMON_DB_PATH

DEBUG_LOG = LOG_DIR + '/RAMSTK_debug.log'
USER_LOG = LOG_DIR + '/RAMSTK_user.log'
IMPORT_LOG = LOG_DIR + '/RAMSTK_import.log'

HEADERS = {
    'Function': [
        'Revision ID',
        'Function ID',
        'Level',
        'Function Code',
        'Function Name',
        'Parent',
        'Remarks',
        'Safety Critical',
        'Type',
    ],
    'Requirement': [
        'Revision ID',
        'Requirement ID',
        'Derived?',
        'Requirement',
        'Figure Number',
        'Owner',
        'Page Number',
        'Parent ID',
        'Priority',
        'Requirement Code',
        'Specification',
        'Requirement Type',
        'Validated?',
        'Validated Date',
    ],
    'Hardware': [
        'Revision ID',
        'Hardware ID',
        'Alt. Part Num.',
        'CAGE Code',
        'Category',
        'Comp. Ref. Des.',
        'Unit Cost',
        'Cost Type',
        'Description',
        'Duty Cycle',
        'Fig. Num.',
        'LCN',
        'Level',
        'Supplier',
        'Mission Time',
        'Name',
        'NSN',
        'Page Num.',
        'Parent ID',
        'Part?',
        'PN',
        'Quantity',
        'Ref. Des.',
        'Remarks',
        'Repairable?',
        'Specification',
        'SubCat',
        'Tagged',
        'Year of Manufacture',
        'App. ID',
        'Area',
        'Capacitance',
        'Configuration',
        'Construction ID',
        'Contact Form',
        'Constact Gauge',
        'Contact Rating ID',
        'Operating Current',
        'Rated Current',
        'Current Ratio',
        'Active Environment',
        'Dormant Environment',
        'Family',
        'Feature Size',
        'Operating Freq.',
        'Insert ID',
        'Insulation ID',
        'Manufacturing ID',
        'Matching',
        'Num. Active Pins',
        'Num. Ckt. Planes',
        'Num. Cycles',
        'Num. Elements',
        'Hand Soldered',
        'Wave Soldered',
        'Operating Life',
        'Overstressed?',
        'Package ID',
        'Operating Power',
        'Rated Power',
        'Power Ratio',
        'Overstress Reason',
        'Resistance',
        'Specification ID',
        'Tech. ID',
        'Active Temp.',
        'Case Temp.',
        'Dormant Temp.',
        'Hot Spot Temp.',
        'Junction Temp.',
        'Knee Temp.',
        'Max. Rated Temp.',
        'Min. Rated Temp.',
        'Temperature Rise',
        'Theta JC',
        'Type',
        'AC Operating Voltage',
        'DC Operating Voltage',
        'ESD Withstand Volts',
        'Rated Voltage',
        'Voltage Ratio',
        'Weight',
        'Years in Prod.',
        'Add. Adj. Factor',
        'Fail. Dist. ID',
        'h(t) Method',
        'h(t) Model',
        'Specified h(t)',
        'h(t) Type',
        'Location',
        'Specified MTBF',
        'Mult. Adj. Factor',
        'Quality',
        'R(t) Goal',
        'R(t) Goal Measure',
        'Scale Parameter',
        'Shape Parameter',
        'Surv. Analysis',
    ],
    'Validation': [
        'Revision ID',
        'Validation ID',
        'Maximum Acceptable',
        'Mean Acceptable',
        'Minimum Acceptable',
        'Acceptable Variance',
        's-Confidence',
        'Avg. Task Cost',
        'Max. Task Cost',
        'Min. Task Cost',
        'Start Date',
        'Finish Date',
        'Description',
        'Unit of Measure',
        'Task Name',
        'Status',
        'Type',
        'Task Spec.',
        'Average Task Time',
        'Maximum Task Time',
        'Minimum Task Time',
    ],
}

# Row data for the Function import test file.
ROW_DATA = [
    [
        1,
        4,
        1,
        'PRESS-001',
        'Maintain system pressure.',
        0,
        'This is a function that is about system pressure.  This remarks box also needs to be larger.',
        1,
        0,
    ],
    [
        1,
        5,
        1,
        'FLOW-001',
        'Maintain system flow.',
        0,
        'These are remarks associated with the function FLOW-001.  The remarks box needs to be bigger.',
        0,
        0,
    ],
]


@pytest.fixture(scope='session')
def test_common_dao():
    """Create a test DAO object for testing against an RAMSTK Common DB."""
    # Create the tmp directory if it doesn't exist.
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    # If there is an existing test database, delete it.
    if os.path.exists(TEST_COMMON_DB_PATH):
        os.remove(TEST_COMMON_DB_PATH)

    # Create and populate an RAMSTK Program test database.
    dao = DAO()
    dao.db_connect(TEST_COMMON_DB_URI)
    dao.db_create_common(TEST_COMMON_DB_URI, test=True)

    yield dao


@pytest.fixture(scope='session')
def test_dao():
    """Create a test DAO object for testing against an RAMSTK Program DB."""
    # Create the tmp directory if it doesn't exist.
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    # If there are existing test databases, delete them.
    if os.path.exists(TEST_PROGRAM_DB_PATH):
        os.remove(TEST_PROGRAM_DB_PATH)
    if os.path.exists(TEMPDIR + '/_ramstk_program_db.ramstk'):
        os.remove(TEMPDIR + '/_ramstk_program_db.ramstk')
    if os.path.exists(TEMPDIR + '/_ramstk_test_db.ramstk'):
        os.remove(TEMPDIR + '/_ramstk_test_db.ramstk')

    # Create and populate an RAMSTK Program test database.
    dao = DAO()
    dao.db_connect(TEST_PROGRAM_DB_URI)
    do_create_test_database(TEST_PROGRAM_DB_URI)

    yield dao


@pytest.fixture(scope='session')
def test_configuration():
    """Create configuration object to use for testing."""
    # Create the data directory if it doesn't exist.
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Create the log directory if it doesn't exist.
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    configuration = Configuration()

    configuration.RAMSTK_SITE_DIR = CONF_DIR
    configuration.RAMSTK_CONF_DIR = CONF_DIR
    configuration.RAMSTK_SITE_CONF = configuration.RAMSTK_CONF_DIR + \
        '/Site.conf'
    configuration.RAMSTK_PROG_CONF = configuration.RAMSTK_CONF_DIR + \
        '/RAMSTK.conf'

    configuration.RAMSTK_COM_BACKEND = 'sqlite'
    configuration.RAMSTK_COM_INFO['host'] = 'localhost'
    configuration.RAMSTK_COM_INFO['socket'] = '3306'
    configuration.RAMSTK_COM_INFO['database'] = TEST_COMMON_DB_PATH
    configuration.RAMSTK_COM_INFO['user'] = 'ramstkcom'
    configuration.RAMSTK_COM_INFO['password'] = 'ramstkcom'

    configuration.RAMSTK_REPORT_SIZE = 'letter'
    configuration.RAMSTK_HR_MULTIPLIER = '1000000.0'
    configuration.RAMSTK_MTIME = '100.0'
    configuration.RAMSTK_DEC_PLACES = '6'
    configuration.RAMSTK_MODE_SOURCE = '1'
    configuration.RAMSTK_TABPOS = {
        'modulebook': 'top',
        'listbook': 'bottom',
        'workbook': 'bottom',
    }

    configuration.RAMSTK_BACKEND = 'sqlite'
    configuration.RAMSTK_PROG_INFO['host'] = 'localhost'
    configuration.RAMSTK_PROG_INFO['socket'] = '3306'
    configuration.RAMSTK_PROG_INFO['database'] = TEST_PROGRAM_DB_PATH
    configuration.RAMSTK_PROG_INFO['user'] = 'johnny.tester'
    configuration.RAMSTK_PROG_INFO['password'] = 'clear.text.password'

    configuration.RAMSTK_DATA_DIR = DATA_DIR
    configuration.RAMSTK_ICON_DIR = ICON_DIR
    configuration.RAMSTK_LOG_DIR = LOG_DIR
    configuration.RAMSTK_PROG_DIR = TMP_DIR

    configuration.RAMSTK_FORMAT_FILE = {
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
    configuration.RAMSTK_COLORS = {
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

    configuration._set_site_configuration()
    configuration.set_user_configuration()

    configuration.RAMSTK_DEBUG_LOG = \
        Utilities.create_logger("RAMSTK.debug", 'DEBUG', DEBUG_LOG)
    configuration.RAMSTK_USER_LOG = \
        Utilities.create_logger("RAMSTK.user", 'INFO', USER_LOG)
    configuration.RAMSTK_IMPORT_LOG = \
        Utilities.create_logger("RAMSTK.user", 'INFO', IMPORT_LOG)

    yield configuration


@pytest.fixture
def test_csv_file_function():
    """Create and populate a *.csv file for testing Function imports."""
    _test_file = TMP_DIR + '/test_inputs_functions.csv'

    with open(_test_file, 'w') as _csv_file:
        filewriter = csv.writer(
            _csv_file,
            delimiter=';',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL,
        )
        filewriter.writerow(HEADERS['Function'])
        filewriter.writerow(ROW_DATA[0])
        filewriter.writerow(ROW_DATA[1])

    yield _test_file


@pytest.fixture
def test_csv_file_requirement():
    """Create and populate a *.csv file for testing Requirement import mapping."""
    _test_file = TMP_DIR + '/test_inputs_requirements.csv'

    with open(_test_file, 'w') as _csv_file:
        filewriter = csv.writer(
            _csv_file,
            delimiter=';',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL,
        )
        filewriter.writerow(HEADERS['Requirement'])

    yield _test_file


@pytest.fixture
def test_csv_file_hardware():
    """Create and populate a *.csv file for testing Hardware import mapping."""
    _test_file = TMP_DIR + '/test_inputs_hardware.csv'

    with open(_test_file, 'w') as _csv_file:
        filewriter = csv.writer(
            _csv_file,
            delimiter=';',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL,
        )
        filewriter.writerow(HEADERS['Hardware'])

    yield _test_file


@pytest.fixture
def test_csv_file_validation():
    """Create and populate a *.csv file for testing Validation import mapping."""
    _test_file = TMP_DIR + '/test_inputs_validation.csv'

    with open(_test_file, 'w') as _csv_file:
        filewriter = csv.writer(
            _csv_file,
            delimiter=';',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL,
        )
        filewriter.writerow(HEADERS['Validation'])

    yield _test_file


@pytest.fixture
def test_excel_file():
    """Create and populate a *.xls file for tests."""
    _test_file = TMP_DIR + '/test_inputs.xls'

    _book = xlwt.Workbook()
    _sheet = _book.add_sheet('Sheet 1', cell_overwrite_ok=True)

    _col = 0
    for _header in HEADERS['Function']:
        _sheet.write(0, _col, _header)
        _col += 1

    _row_num = 1
    for _row in ROW_DATA:
        for _data in enumerate(_row):
            _sheet.write(_row_num, _data[0], _data[1])
        _row_num += 1

    _book.save(_test_file)

    yield _test_file


@pytest.fixture
def test_format_file():
    """Create and populate a RAMSTK layout format file."""
    _test_file = TMP_DIR + '/Test.xml'

    _root = ET.Element('root')
    _tree = ET.SubElement(_root, "tree", name="Test")
    _column = ET.SubElement(_tree, "column")
    _usertitle = ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 0"
    _column = ET.SubElement(_tree, "column")
    _usertitle = ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 1"
    _column = ET.SubElement(_tree, "column")
    _usertitle = ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 2"
    _column = ET.SubElement(_tree, "column")
    _usertitle = ET.SubElement(
        _column,
        "defaulttitle",
    ).text = "Default Title 3"

    _layout = ET.ElementTree(_root)
    _layout.write(_test_file)

    yield _test_file


@pytest.fixture
def test_export_file():
    """Create a test file base for export testing."""
    # This simply creates the base name of the file and directory to create it
    # in.  A test would need to add the appropriate file extension.
    _test_file = TMP_DIR + '/test_export'

    yield _test_file
