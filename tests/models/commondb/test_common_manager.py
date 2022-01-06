# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.db.test_common.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for common database methods and operations."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest
from mock import patch
from pubsub import pub

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.models import RAMSTKCommonDB, RAMSTKSiteInfoRecord
from ramstk.models.commondb import RAMSTKUser


@pytest.fixture(scope="class")
def test_datamanager(test_common_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut).
    dut = RAMSTKCommonDB()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_create_common, "request_create_common")
    # pub.unsubscribe(dut.do_open_program, "request_open_program")
    # pub.unsubscribe(dut.do_close_program, "request_close_program")
    # pub.unsubscribe(dut.do_save_program, "request_update_program")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "test_datamanager",
    "test_license_file",
    "test_toml_site_configuration",
    "test_common_dao",
)
class TestCommonManager:
    """Class for testing functions to load common variables."""

    def on_succeed_create_postgres_common(self, common_db, database):
        assert isinstance(common_db, BaseDatabase)
        assert database["database"] == "ramstk_common_test_db"
        print(
            "\033[36m\nsucceed_create_common_database topic was broadcast "
            "when creating postgres database"
        )

    def on_fail_read_license(self, error_message):
        assert error_message == (
            "Unable to read license key file.  Defaulting " "to a 30-day demo license."
        )
        print("\033[35m\nfail_read_license topic was broadcast.")

    @pytest.mark.unit
    def test_create_common_manager(self, test_datamanager):
        """__init__() should create an instance of the RAMSTK program manager."""
        assert isinstance(test_datamanager, RAMSTKCommonDB)
        assert isinstance(test_datamanager.common_dao, BaseDatabase)
        assert pub.isSubscribed(
            test_datamanager.do_create_common, "request_create_common"
        )

    @pytest.mark.integration
    @patch(
        "builtins.input",
        side_effect=[
            "y",
            "tester",
            "johnny",
            "johnny.tester@reliaqual.com",
            "+1.269.867.5309",
        ],
    )
    def test_do_create_postgres_common(
        self,
        monkeypatch,
        test_datamanager,
        test_common_dao,
        test_license_file,
        test_toml_site_configuration,
    ):
        """do_create_common() should return None."""
        pub.subscribe(
            self.on_succeed_create_postgres_common, "succeed_create_common_database"
        )

        test_common_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "ramstk_common_test_db",
        }
        test_datamanager.site_configuration = test_toml_site_configuration
        test_datamanager.do_create_common(
            test_common_dao,
            test_common_db,
            test_license_file.name,
        )

        test_datamanager.common_dao.do_connect(test_common_db)
        _record = (
            test_datamanager.common_dao.session.query(RAMSTKSiteInfoRecord)
            .filter(RAMSTKSiteInfoRecord.site_id == 0)
            .first()
        )
        assert _record.product_key == "apowdigfb3rh9214839qu"
        assert _record.expire_on == date(2019, 8, 7)
        test_datamanager.common_dao.do_disconnect()

        pub.unsubscribe(
            self.on_succeed_create_postgres_common, "succeed_create_common_database"
        )

    @pytest.mark.integration
    @patch("builtins.input", return_value="n")
    def test_do_create_postgres_common_no_admin(
        self,
        monkeypatch,
        test_datamanager,
        test_common_dao,
        test_license_file,
        test_toml_site_configuration,
    ):
        """do_create_common() should return None."""
        pub.subscribe(
            self.on_succeed_create_postgres_common, "succeed_create_common_database"
        )

        test_common_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "ramstk_common_test_db",
        }
        test_datamanager.site_configuration = test_toml_site_configuration
        test_datamanager.do_create_common(
            test_common_dao,
            test_common_db,
            test_license_file.name,
        )

        pub.unsubscribe(
            self.on_succeed_create_postgres_common, "succeed_create_common_database"
        )

    @pytest.mark.integration
    @patch("builtins.input", return_value="n")
    def test_do_create_postgres_common_no_license(
        self,
        monkeypatch,
        test_datamanager,
        test_common_dao,
        test_toml_site_configuration,
    ):
        """do_create_common() should return None."""
        pub.subscribe(self.on_fail_read_license, "fail_read_license")

        test_common_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "ramstk_common_test_db",
        }
        test_datamanager.site_configuration = test_toml_site_configuration
        test_datamanager.do_create_common(
            test_common_dao,
            test_common_db,
            "",
        )

        test_datamanager.common_dao.do_connect(test_common_db)
        _record = (
            test_datamanager.common_dao.session.query(RAMSTKSiteInfoRecord)
            .filter(RAMSTKSiteInfoRecord.site_id == -1)
            .first()
        )
        assert _record.product_key == "DEMO"
        assert _record.site_name == "DEMO"
        assert _record.expire_on == date.today() + timedelta(days=30)

        pub.unsubscribe(self.on_fail_read_license, "fail_read_license")
