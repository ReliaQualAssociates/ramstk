import os
import glob

import pytest

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.dao import DAO
from rtk.dao.RTKProgramDB import do_create_test_database

VIRTUAL_ENV = glob.glob(os.environ['VIRTUAL_ENV'])[0]
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_DIR = VIRTUAL_ENV + '/tmp'
DATA_DIR = TMP_DIR + '/data'
LOG_DIR = TMP_DIR + '/logs'
TEST_PROGRAM_DB_PATH = TMP_DIR + '/TestDB.rtk'
TEST_COMMON_DB_PATH = TMP_DIR + '/TestCommonDB2.rtk'
TEST_PROGRAM_DB_URI = 'sqlite:///' + TEST_PROGRAM_DB_PATH
TEST_COMMON_DB_URI = 'sqlite:///' + TEST_COMMON_DB_PATH

DEBUG_LOG = LOG_DIR + '/RTK_debug.log'
USER_LOG = LOG_DIR + '/RTK_user.log'
IMPORT_LOG = LOG_DIR + '/RTK_import.log'


@pytest.fixture(scope='session')
def test_common_dao():
    """ Create a test DAO object for testing against an RTK Common DB. """
    # Create the tmp directory if it doesn't exist.
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    # If there is an existing test database, delete it.
    if os.path.exists(TEST_COMMON_DB_PATH):
        os.remove(TEST_COMMON_DB_PATH)

    # Create and populate an RTK Program test database.
    dao = DAO()
    dao.db_connect(TEST_COMMON_DB_URI)
    dao.db_create_common(TEST_COMMON_DB_URI, test=True)

    yield dao


@pytest.fixture(scope='session')
def test_dao():
    """ Create a test DAO object for testing against an RTK Program DB. """
    # Create the tmp directory if it doesn't exist.
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    # If there are existing test databases, delete them.
    if os.path.exists(TEST_PROGRAM_DB_PATH):
        os.remove(TEST_PROGRAM_DB_PATH)
    if os.path.exists('/tmp/_rtk_program_db.rtk'):
        os.remove('/tmp/_rtk_program_db.rtk')
    if os.path.exists('/tmp/_rtk_test_db.rtk'):
        os.remove('/tmp/_rtk_test_db.rtk')

    # Create and populate an RTK Program test database.
    dao = DAO()
    dao.db_connect(TEST_PROGRAM_DB_URI)
    do_create_test_database(TEST_PROGRAM_DB_URI)

    yield dao


@pytest.fixture(scope='session')
def test_configuration():
    """ Create configuration object to use for testing. """
    import fileinput
    from shutil import copyfile

    # Create the data directory if it doesn't exist.
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Create the log directory if it doesn't exist.
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    configuration = Configuration()

    configuration.RTK_CONF_DIR = DATA_DIR
    configuration.RTK_PROG_CONF = configuration.RTK_CONF_DIR + '/RTK.conf'
    copyfile(SRC_DIR + '/data/RTK.conf', configuration.RTK_PROG_CONF)
    for line in fileinput.input(configuration.RTK_PROG_CONF, inplace=True):
        # Inside this loop the STDOUT will be redirected to the file
        # the comma after each print statement is needed to avoid double line
        # breaks.
        print line.replace("database =", "database = " + TEST_PROGRAM_DB_PATH),

    configuration.RTK_COM_BACKEND = 'sqlite'
    configuration.RTK_BACKEND = 'sqlite'
    configuration.RTK_COM_INFO['database'] = TEST_COMMON_DB_PATH
    configuration.RTK_PROG_INFO['database'] = TEST_PROGRAM_DB_PATH

    configuration.RTK_LOG_DIR = TMP_DIR

    configuration.RTK_DEBUG_LOG = \
        Utilities.create_logger("RTK.debug", 'DEBUG', DEBUG_LOG)
    configuration.RTK_USER_LOG = \
        Utilities.create_logger("RTK.user", 'INFO', USER_LOG)
    configuration.RTK_IMPORT_LOG = \
        Utilities.create_logger("RTK.user", 'INFO', IMPORT_LOG)

    yield configuration
