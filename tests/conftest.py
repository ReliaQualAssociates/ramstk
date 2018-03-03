import pytest

import rtk.Utilities as Utilities
from rtk.Configuration import Configuration
from rtk.dao import DAO

TESTDB = 'TestDB.rtk'
TESTDB_PATH = "/tmp/{}".format(TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH


@pytest.fixture(scope='session')
def test_dao():
    """Create a test DAO object for testing against an RTK Program DB."""
    # Create and populate an RTK Program test database.
    dao = DAO()
    dao.db_connect(TEST_DATABASE_URI)
    dao.db_create_program(TEST_DATABASE_URI)

    yield dao


@pytest.fixture(scope='session')
def test_configuration():
    """Create loggers to use for testing."""
    configuration = Configuration()

    configuration.RTK_DEBUG_LOG = \
        Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
    configuration.RTK_USER_LOG = \
        Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

    yield configuration
