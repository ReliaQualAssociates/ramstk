# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.test_main.py is part of The RAMSTK Project
#
# All rights reserved.
"""Class for testing RAMSTK main."""

# Third Party Imports
import pytest
from pubsub import pub
from sqlalchemy import select

# RAMSTK Package Imports
from ramstk import __main__
from ramstk.configuration import RAMSTKSiteConfiguration, RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.models.db import BaseDatabase, RAMSTKCommonDB
from ramstk.models.dbrecords import RAMSTKCategoryRecord
from ramstk.models.dbtables import RAMSTKActionTable, RAMSTKSiteInfoTable
from ramstk.models.dbviews import RAMSTKFMEAView


@pytest.fixture(scope="class")
def test_common_datamanager():
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKCommonDB()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(
        dut._do_create_database,
        "request_create_common",
    )

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "test_common_dao",
    "test_toml_site_configuration",
    "test_toml_user_configuration",
)
class TestMain:
    """Test class for the RAMSTK main program."""

    @pytest.mark.unit
    def test_do_read_site_configuration(self):
        """do_read_site_configuration() should return an instance of the
        RAMSTKSiteConfiguration."""
        _site_configuration = __main__.do_read_site_configuration()

        assert isinstance(_site_configuration, RAMSTKSiteConfiguration)
        assert "/share/RAMSTK" in _site_configuration.RAMSTK_SITE_DIR
        assert "/share/RAMSTK/Site.toml" in _site_configuration.RAMSTK_SITE_CONF
        assert _site_configuration.RAMSTK_COM_BACKEND == "sqlite"
        assert _site_configuration.RAMSTK_COM_INFO["dialect"] == "sqlite"
        assert _site_configuration.RAMSTK_COM_INFO["host"] == "localhost"
        assert _site_configuration.RAMSTK_COM_INFO["password"] == "clear.text.password"
        assert _site_configuration.RAMSTK_COM_INFO["port"] == "3306"
        assert _site_configuration.RAMSTK_COM_INFO["user"] == "johnny.tester"

    @pytest.mark.unit
    def test_do_read_user_configuration(self):
        """do_read_user_configuration() should return an instance of the
        RAMSTKUserConfiguration."""
        _user_configuration, _logger = __main__.do_read_user_configuration()

        assert isinstance(_user_configuration, RAMSTKUserConfiguration)
        assert isinstance(_logger, RAMSTKLogManager)

    @pytest.mark.unit
    def test_do_connect_to_site_db(
        self,
        test_common_dao,
    ):
        """do_connect_to_site_db() should return an instance of the RAMSTKCommonDB."""
        test_common_dao.cxnargs["database"] = test_common_dao.cxnargs["database"]
        _site_db = __main__.do_connect_to_site_db(test_common_dao.cxnargs)

        assert isinstance(_site_db, RAMSTKCommonDB)

    @pytest.mark.unit
    def test_do_connect_to_site_db_no_db(
        self,
        test_common_dao,
    ):
        """do_connect_to_site_db() should raise a DataAccessError when the database
        doesn't exist."""
        test_common_dao.cxnargs["database"] = "bud_light"

        with pytest.raises(SystemExit) as _error:
            __main__.do_connect_to_site_db(test_common_dao.cxnargs)

        assert _error.type == SystemExit
        assert (
            _error.value.code == "\x1b[35mUNABLE TO CONNECT TO RAMSTK COMMON "
            "DATABASE!  Check the logs for more information.\x1b[0m"
        )

    @pytest.mark.unit
    def test_do_initialize_databases(
        self,
        test_common_dao,
        test_toml_user_configuration,
    ):
        """do_initialize_databases() should create an instance of each database
        manager."""
        _program_db, _site_db = __main__.do_initialize_databases(
            test_toml_user_configuration,
            test_common_dao,
        )

        assert isinstance(_program_db, BaseDatabase)
        assert isinstance(_program_db.tables["action"], RAMSTKActionTable)
        assert isinstance(_program_db.dic_views["fmea"], RAMSTKFMEAView)
        assert _program_db.user_configuration == test_toml_user_configuration
        assert isinstance(_site_db, BaseDatabase)
        assert isinstance(_site_db.tables["options"], RAMSTKSiteInfoTable)
        assert _site_db.tables["options"].dao == _site_db

    @pytest.mark.unit
    def test_do_load_configuration_list(
        self,
        test_common_dao,
        test_toml_user_configuration,
    ):
        """do_load_configuration_list() should populate the passed configuration list
        from the database."""
        __main__.do_load_configuration_list(
            test_toml_user_configuration.RAMSTK_ACTION_CATEGORY,
            test_common_dao,
            select(RAMSTKCategoryRecord).where(
                RAMSTKCategoryRecord.category_type == "action"
            ),
            "category_id",
            [
                "name",
                "description",
                "value",
            ],
        )

        assert isinstance(test_toml_user_configuration.RAMSTK_ACTION_CATEGORY, dict)
        assert test_toml_user_configuration.RAMSTK_ACTION_CATEGORY == {
            38: ("ENGD", "Engineering, Design", 1),
            39: ("ENGR", "Engineering, Reliability", 1),
            40: ("ENGS", "Engineering, Systems", 1),
            41: ("MAN", "Manufacturing", 1),
            42: ("TEST", "Test", 1),
            43: ("VANDV", "Verification & Validation", 1),
        }
