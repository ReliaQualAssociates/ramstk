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
from ramstk.models.db import BaseDatabase, RAMSTKCommonDB
from ramstk.models.dbrecords import RAMSTKSiteInfoRecord


@pytest.fixture(scope="class")
def test_datamanager(test_common_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut).
    dut = RAMSTKCommonDB()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_create_common, "request_create_common")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "test_datamanager",
    "test_license_file",
    "test_toml_site_configuration",
    "test_toml_user_configuration",
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
            "Unable to read license key file.  Defaulting to a 30-day demo license."
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
            self.on_succeed_create_postgres_common,
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
            self.on_succeed_create_postgres_common,
            "succeed_create_common_database",
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
            self.on_succeed_create_postgres_common,
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
        test_datamanager.do_create_common(
            test_common_dao,
            test_common_db,
            test_license_file.name,
        )

        pub.unsubscribe(
            self.on_succeed_create_postgres_common,
            "succeed_create_common_database",
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

    @pytest.mark.integration
    def test_do_load_site_variables(
        self,
        test_datamanager,
        test_toml_user_configuration,
    ):
        """do_load_site_variables() should return a populated user configuration."""
        _user_configuration = test_datamanager.do_load_site_variables(
            test_toml_user_configuration
        )

        assert _user_configuration.RAMSTK_ACTION_CATEGORY[38] == (
            "ENGD",
            "Engineering, Design",
            "action",
            1,
        )
        assert _user_configuration.RAMSTK_ACTION_STATUS[11] == (
            "Initiated",
            "Action has been initiated.",
            "action",
        )
        assert _user_configuration.RAMSTK_CATEGORIES[1] == "Integrated Circuit"
        assert _user_configuration.RAMSTK_SUBCATEGORIES[1][1] == "Linear"
        assert _user_configuration.RAMSTK_FAILURE_MODES[1][1] == {}
        assert _user_configuration.RAMSTK_STRESS_LIMITS[1] == (
            0.8,
            0.9,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            125.0,
            125.0,
        )
        assert _user_configuration.RAMSTK_INCIDENT_CATEGORY[35] == (
            "HW",
            "Hardware",
            "incident",
            1,
        )
        assert _user_configuration.RAMSTK_INCIDENT_STATUS[1] == (
            "Initiated",
            "Incident has been initiated.",
            "incident",
        )
        assert _user_configuration.RAMSTK_INCIDENT_TYPE[1] == (
            "PLN",
            "Planning",
            "incident",
        )
        assert _user_configuration.RAMSTK_DETECTION_METHODS[1] == (
            "Code Reviews",
            "",
            "detection",
        )
        assert _user_configuration.RAMSTK_HAZARDS[1] == (
            "Acceleration/Gravity",
            "Falls",
        )
        assert _user_configuration.RAMSTK_MANUFACTURERS[1] == (
            "Sprague",
            "New Hampshire",
            "13606",
        )
        assert _user_configuration.RAMSTK_MEASUREMENT_UNITS[1] == (
            "lbf",
            "Pounds Force",
            "unit",
        )
        assert _user_configuration.RAMSTK_VALIDATION_TYPE[17] == (
            "DOE",
            "Manufacturing Test, DOE",
            "validation",
        )
        assert (
            _user_configuration.RAMSTK_DAMAGE_MODELS[1]
            == "Adhesion Wear Model for Bearings"
        )
        assert _user_configuration.RAMSTK_LOAD_HISTORY[1] == "Cycle Counts"
        assert _user_configuration.RAMSTK_MEASURABLE_PARAMETERS[11] == (
            "CN",
            "Contamination, Concentration",
            "damage",
        )
        assert _user_configuration.RAMSTK_AFFINITY_GROUPS[7] == (
            "Reliability",
            "affinity",
        )
        assert _user_configuration.RAMSTK_REQUIREMENT_TYPE[10] == (
            "FUN",
            "Functional",
            "requirement",
        )
        assert _user_configuration.RAMSTK_STAKEHOLDERS[1] == "Customer"
        assert _user_configuration.RAMSTK_RPN_DETECTION[1] == {
            "description": "Design control will almost certainly detect a potential "
            "mechanism/cause and subsequent failure mode.",
            "name": "Almost Certain",
            "rpn_id": 21,
            "rpn_type": "detection",
            "value": 1,
        }
        assert _user_configuration.RAMSTK_RPN_OCCURRENCE[1] == {
            "description": "Failure rate is 1 in 1,500,000.",
            "name": "Remote",
            "rpn_id": 11,
            "rpn_type": "occurrence",
            "value": 1,
        }
        assert _user_configuration.RAMSTK_RPN_SEVERITY[1] == {
            "description": "No effect.",
            "name": "None",
            "rpn_id": 1,
            "rpn_type": "severity",
            "value": 1,
        }
        assert _user_configuration.RAMSTK_SEVERITY[11] == (
            "INS",
            "Insignificant",
            "risk",
            1,
        )
        assert _user_configuration.RAMSTK_USERS[1] == (
            "Tester",
            "Johnny",
            "tester.johnny@reliaqual.com",
            "+1.269.867.5309",
            "1",
        )
        assert _user_configuration.RAMSTK_WORKGROUPS[1] == (
            "Engineering, Design",
            "workgroup",
        )
