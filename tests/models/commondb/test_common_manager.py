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
from sqlalchemy import select

# RAMSTK Package Imports
from ramstk.models.db import BaseDatabase, RAMSTKCommonDB
from ramstk.models.dbrecords import RAMSTKCategoryRecord, RAMSTKSiteInfoRecord


@pytest.fixture(scope="class")
def test_datamanager():
    """Get a table model instance for each test class."""
    # Create the device under test (dut).
    dut = RAMSTKCommonDB()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(
        dut._do_create_database,
        "request_create_common",
    )

    # Delete the device under test.
    del dut


def on_succeed_create_postgres_common(common_db, database):
    """Listen for succeed_create message."""
    assert isinstance(
        common_db,
        BaseDatabase,
    )
    assert database["database"] == "ramstk_common_test_db"
    print(
        "\033[32m\n\tsucceed_create_common_database message was broadcast "
        "when creating postgres database"
    )


def on_fail_read_license(error_message):
    """Listen for fail_read_license message."""
    assert error_message == (
        "Unable to read license key file.  Defaulting to a 30-day demo license."
    )
    print("\033[35m\n\tfail_read_license message was broadcast")


@pytest.mark.usefixtures(
    "test_datamanager",
    "test_license_file",
    "test_toml_site_configuration",
    "test_toml_user_configuration",
)
class TestCommonManager:
    """Class for testing functions to load common variables."""

    @pytest.mark.unit
    def test_create_common_manager(self, test_datamanager):
        """Should create an instance of the common database manager."""
        assert isinstance(
            test_datamanager,
            RAMSTKCommonDB,
        )
        assert isinstance(
            test_datamanager.tables["options"],
            object,
        )
        assert pub.isSubscribed(
            test_datamanager._do_create_database,
            "request_create_common",
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
        test_license_file,
        test_toml_site_configuration,
    ):
        """do_create_common() should return None."""
        pub.subscribe(
            on_succeed_create_postgres_common,
            "succeed_create_common_database",
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
        test_datamanager._do_create_database(
            test_common_db,
            f"{test_toml_site_configuration.RAMSTK_SITE_DIR}/postgres_common_db.sql",
            test_license_file.name,
        )

        test_datamanager.do_connect(test_common_db)
        _record = (
            test_datamanager.session.query(RAMSTKSiteInfoRecord)
            .filter(RAMSTKSiteInfoRecord.site_id == 100)
            .first()
        )
        assert _record.product_key == "apowdigfb3rh9214839qu"
        assert _record.expire_on == date(2019, 8, 7)
        test_datamanager.do_disconnect()

        pub.unsubscribe(
            on_succeed_create_postgres_common,
            "succeed_create_common_database",
        )

    @pytest.mark.integration
    @patch("builtins.input", return_value="n")
    def test_do_create_postgres_common_no_admin(
        self,
        monkeypatch,
        test_datamanager,
        test_license_file,
        test_toml_site_configuration,
    ):
        """do_create_common() should return None."""
        pub.subscribe(
            on_succeed_create_postgres_common,
            "succeed_create_common_database",
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
        test_datamanager._do_create_database(
            test_common_db,
            f"{test_toml_site_configuration.RAMSTK_SITE_DIR}/postgres_common_db.sql",
            test_license_file.name,
        )

        pub.unsubscribe(
            on_succeed_create_postgres_common,
            "succeed_create_common_database",
        )

    @pytest.mark.integration
    @patch("builtins.input", return_value="n")
    def test_do_create_postgres_common_no_license(
        self,
        monkeypatch,
        test_datamanager,
        test_toml_site_configuration,
    ):
        """do_create_common() should return None."""
        pub.subscribe(
            on_fail_read_license,
            "fail_read_license",
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
        test_datamanager._do_create_database(
            test_common_db,
            f""
            f"{test_toml_site_configuration.RAMSTK_SITE_DIR}/postgres_common_db.sql",
            "",
        )

        test_datamanager.do_connect(test_common_db)
        _record = (
            test_datamanager.session.query(RAMSTKSiteInfoRecord)
            .filter(RAMSTKSiteInfoRecord.site_id == -1)
            .first()
        )
        assert _record.product_key == "DEMO"
        assert _record.site_name == "DEMO"
        assert _record.expire_on == date.today() + timedelta(days=30)

        pub.unsubscribe(
            on_fail_read_license,
            "fail_read_license",
        )

    @pytest.mark.skip("Move to test suite for __main__")
    def test_do_load_site_variables(
        self,
        test_datamanager,
        test_toml_user_configuration,
    ):
        """do_load_site_variables() should return a populated user configuration."""
        _user_configuration = test_datamanager.do_load_site_variables(
            test_toml_user_configuration
        )

        assert _user_configuration.RAMSTK_SUBCATEGORIES[1][1] == "Linear"
        assert _user_configuration.RAMSTK_FAILURE_MODES[1][1] == {}

    @pytest.mark.integration
    @patch("builtins.input", return_value="n")
    def test_do_execute_query(
        self,
        monkeypatch,
        test_datamanager,
        test_toml_site_configuration,
    ):
        """do_execute_query() should return a list."""
        _query = select(RAMSTKCategoryRecord).where(
            RAMSTKCategoryRecord.category_type == "action"
        )

        _results = test_datamanager.do_execute_query(_query)

        for _result in _results:
            assert isinstance(_result, RAMSTKCategoryRecord)
            assert _result.category_type == "action"
