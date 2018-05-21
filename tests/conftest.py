import os
import glob

import pytest

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.dao import DAO

VIRTUAL_ENV = glob.glob(os.environ['VIRTUAL_ENV'])[0]
TMP_DIR = VIRTUAL_ENV + '/tmp'
TEST_PROGRAM_DB_PATH = TMP_DIR + '/TestDB.rtk'
TEST_COMMON_DB_PATH = TMP_DIR + '/TestCommonDB2.rtk'
TEST_PROGRAM_DB_URI = 'sqlite:///' + TEST_PROGRAM_DB_PATH
TEST_COMMON_DB_URI = 'sqlite:///' + TEST_COMMON_DB_PATH


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

    # If there is an existing test database, delete it.
    if os.path.exists(TEST_PROGRAM_DB_PATH):
        os.remove(TEST_PROGRAM_DB_PATH)

    # Create and populate an RTK Program test database.
    dao = DAO()
    dao.db_connect(TEST_PROGRAM_DB_URI)
    dao.db_create_program(TEST_PROGRAM_DB_URI)

    yield dao


@pytest.fixture(scope='session')
def test_configuration():
    """ Create loggers to use for testing. """
    configuration = Configuration()

    configuration.RTK_DEBUG_LOG = \
        Utilities.create_logger("RTK.debug", 'DEBUG', TMP_DIR + '/RTK_debug.log')
    configuration.RTK_USER_LOG = \
        Utilities.create_logger("RTK.user", 'INFO', TMP_DIR + '/RTK_user.log')

    yield configuration
