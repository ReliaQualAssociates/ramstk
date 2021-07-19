# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.tests.test_ramstk.py is part of The RAMSTK Project
#
# All rights reserved.
"""Class for testing RAMSTK module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.ramstk import RAMSTKProgramManager


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a data manager instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKProgramManager()

    yield dut

    # Unsubscribe from pypubsub topics.
    pub.unsubscribe(dut.do_create_program, "request_create_program")
    pub.unsubscribe(dut.do_open_program, "request_open_program")
    pub.unsubscribe(dut.do_close_program, "request_close_program")
    pub.unsubscribe(dut.do_save_program, "request_update_program")

    # Delete the device under test.
    del dut


@pytest.mark.usefixtures(
    "make_home_config_dir",
    "test_datamanager",
    "test_program_dao",
    "test_toml_user_configuration",
    "test_bald_dao",
)
class TestProgramManager:
    """Test class for the RAMSTK Program Manager."""

    def on_succeed_open_program(self, dao):
        assert isinstance(dao, BaseDatabase)
        print("\033[36m\nsucceed_connect_program_database topic was broadcast")

    def on_fail_open_program_bad_url(self, error_message):
        assert error_message == ("The database bad_database_url.ramstk does not exist.")
        print("\033[35m\nfail_connect_program_database topic was broadcast.")

    def on_fail_open_program_unknown_dialect(self, error_message):
        assert error_message == (
            "Unknown database dialect in database connection dict."
        )
        print("\033[35m\nfail_connect_program_database topic was broadcast.")

    def on_fail_open_program_non_string_url(self, error_message):
        assert error_message == (
            "Unknown dialect or non-string value in " "database connection dict."
        )
        print("\033[35m\nfail_connect_program_database topic was broadcast.")

    def on_succeed_close_program(self):
        print("\033[36m\nsucceed_disconnect_program_database topic was broadcast")

    def on_fail_close_program(self, error_message):
        assert error_message == (
            "Not currently connected to a database.  " "Nothing to close."
        )
        print("\033[35m\nfail_disconnect_program_database topic was broadcast")

    def on_request_update_revision(self):
        print("\033[36m\nrequest_update_all_revisions topic was broadcast")

    def on_request_update_function(self):
        print("\033[36mrequest_update_all_functions topic was broadcast")

    def on_request_update_requirement(self):
        print("\033[36mrequest_update_all_requirements topic was broadcast")

    def on_request_update_stakeholder(self):
        print("\033[36mrequest_update_all_stakeholders topic was broadcast")

    def on_request_update_hardware(self):
        print("\033[36mrequest_update_all_hardware topic was broadcast")

    def on_request_update_validation(self):
        print("\033[36mrequest_update_all_validation topic was broadcast")

    def on_succeed_create_postgres_program(self, program_db, database):
        assert isinstance(program_db, BaseDatabase)
        assert database["database"] == program_db.cxnargs["dbname"]
        print(
            "\033[36m\nsucceed_create_program_database topic was broadcast "
            "when creating postgres database"
        )

    @pytest.mark.unit
    def test_create_program_manager(self):
        """__init__() should create an instance of the RAMSTK program
        manager."""
        DUT = RAMSTKProgramManager()

        assert isinstance(DUT, RAMSTKProgramManager)
        assert isinstance(DUT.dic_managers, dict)
        assert DUT.dic_managers["revision"] == {"data": None}
        assert DUT.dic_managers["function"] == {"analysis": None, "data": None}
        assert DUT.dic_managers["allocation"] == {"analysis": None, "data": None}
        assert DUT.dic_managers["requirement"] == {"data": None}
        assert DUT.dic_managers["similar_item"] == {"analysis": None, "data": None}
        assert DUT.dic_managers["stakeholder"] == {"analysis": None, "data": None}
        assert DUT.dic_managers["hardware"] == {"analysis": None, "data": None}
        assert DUT.dic_managers["fmea"] == {"analysis": None, "data": None}
        assert DUT.dic_managers["options"] == {"data": None}
        assert DUT.dic_managers["pof"] == {"data": None}
        assert DUT.dic_managers["preferences"] == {"data": None}
        assert DUT.dic_managers["program_status"] == {"data": None}
        assert DUT.dic_managers["validation"] == {"analysis": None, "data": None}
        assert DUT.dic_managers["options"] == {"data": None}
        assert isinstance(DUT.program_dao, BaseDatabase)
        assert pub.isSubscribed(DUT.do_create_program, "request_create_program")
        assert pub.isSubscribed(DUT.do_open_program, "request_open_program")
        assert pub.isSubscribed(DUT.do_close_program, "request_close_program")
        assert pub.isSubscribed(DUT.do_save_program, "request_update_program")

        # Unsubscribe from pypubsub topics.
        pub.unsubscribe(DUT.do_create_program, "request_create_program")
        pub.unsubscribe(DUT.do_open_program, "request_open_program")
        pub.unsubscribe(DUT.do_close_program, "request_close_program")
        pub.unsubscribe(DUT.do_save_program, "request_update_program")

    @pytest.mark.integration
    def test_do_open_program(self, test_datamanager, test_program_dao):
        """do_open_program() should connect to the test program database and
        broadcast the success message."""
        pub.subscribe(self.on_succeed_open_program, "succeed_connect_program_database")

        test_program_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_program_dao.cxnargs["dbname"],
        }
        test_datamanager.do_open_program(BaseDatabase(), test_program_db)

        pub.unsubscribe(
            self.on_succeed_open_program, "succeed_connect_program_database"
        )

        test_datamanager.do_close_program()

    @pytest.mark.integration
    def test_do_open_program_bad_url(self, test_datamanager, test_program_dao):
        """do_open_program() should broadcast the fail message when attempting
        to open a bad URL."""
        pub.subscribe(
            self.on_fail_open_program_bad_url, "fail_connect_program_database"
        )

        test_program_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "bad_database_url.ramstk",
        }
        test_datamanager.do_open_program(BaseDatabase(), test_program_db)

        pub.unsubscribe(
            self.on_fail_open_program_bad_url, "fail_connect_program_database"
        )

    @pytest.mark.integration
    def test_do_open_program_unknown_dialect(self, test_datamanager, test_program_dao):
        """do_open_program() should broadcast the fail message when attempting
        to open a database of unsupported dialect."""
        pub.subscribe(
            self.on_fail_open_program_unknown_dialect, "fail_connect_program_database"
        )

        test_program_db = {
            "dialect": "doyleton",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_program_dao.cxnargs["dbname"],
        }
        test_datamanager.do_open_program(BaseDatabase(), test_program_db)

        pub.unsubscribe(
            self.on_fail_open_program_unknown_dialect, "fail_connect_program_database"
        )

    @pytest.mark.integration
    def test_do_open_program_non_string_url(self, test_datamanager, test_program_dao):
        """do_open_program() should broadcast the fail message when attempting
        to open a non-string URL."""
        pub.subscribe(
            self.on_fail_open_program_non_string_url, "fail_connect_program_database"
        )

        test_program_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": 8742.11,
        }
        test_datamanager.do_open_program(BaseDatabase(), test_program_db)

        pub.unsubscribe(
            self.on_fail_open_program_non_string_url, "fail_connect_program_database"
        )

    @pytest.mark.integration
    def test_do_close_program(self, test_datamanager, test_program_dao):
        """do_close_program() should disconnect from the test program database
        and broadcast the success message."""
        pub.subscribe(
            self.on_succeed_close_program, "succeed_disconnect_program_database"
        )

        test_program_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "TestProgramDB",
        }
        test_datamanager.do_open_program(BaseDatabase(), test_program_db)

        assert (
            test_datamanager.program_dao.database
            == "postgresql+psycopg2://postgres:postgres@localhost:5432/TestProgramDB"
        )

        test_datamanager.do_close_program()

        assert test_datamanager.program_dao.session is None

        pub.unsubscribe(
            self.on_succeed_close_program, "succeed_disconnect_program_database"
        )

    @pytest.mark.integration
    def test_do_close_program_none_open(self, test_datamanager, test_program_dao):
        """do_close_program() should broadcast the fail message if it attempts
        to close a database when not connected."""
        pub.subscribe(self.on_fail_close_program, "fail_disconnect_program_database")

        DUT = RAMSTKProgramManager()
        DUT.do_close_program()

        assert isinstance(DUT.program_dao, BaseDatabase)

        pub.unsubscribe(self.on_fail_close_program, "fail_disconnect_program_database")
        pub.unsubscribe(DUT.do_create_program, "request_create_program")
        pub.unsubscribe(DUT.do_open_program, "request_open_program")
        pub.unsubscribe(DUT.do_close_program, "request_close_program")
        pub.unsubscribe(DUT.do_save_program, "request_update_program")

    @pytest.mark.integration
    def test_save_program(self, test_datamanager, test_program_dao):
        """do_save_program() should cause all workstream modules to execute
        their save_all() method."""
        pub.subscribe(self.on_request_update_revision, "request_update_all_revisions")
        pub.subscribe(self.on_request_update_function, "request_update_all_functions")
        pub.subscribe(
            self.on_request_update_requirement, "request_update_all_requirements"
        )
        pub.subscribe(
            self.on_request_update_stakeholder, "request_update_all_stakeholders"
        )
        pub.subscribe(self.on_request_update_hardware, "request_update_all_hardware")
        pub.subscribe(
            self.on_request_update_validation, "request_update_all_validation"
        )

        test_program_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_program_dao.cxnargs["dbname"],
        }
        test_datamanager.do_open_program(BaseDatabase(), test_program_db)
        test_datamanager.do_save_program()

        pub.unsubscribe(self.on_request_update_revision, "request_update_all_revisions")
        pub.unsubscribe(self.on_request_update_function, "request_update_all_functions")
        pub.unsubscribe(
            self.on_request_update_requirement, "request_update_all_requirements"
        )
        pub.unsubscribe(
            self.on_request_update_stakeholder, "request_update_all_stakeholders"
        )
        pub.unsubscribe(self.on_request_update_hardware, "request_update_all_hardware")
        pub.unsubscribe(
            self.on_request_update_validation, "request_update_all_validation"
        )

        test_datamanager.do_close_program()

    @pytest.mark.integration
    def test_do_create_postgres_program(
        self, test_datamanager, test_bald_dao, test_toml_user_configuration
    ):
        """do_create_program() should broadcast the success message when a
        postgres database is created."""
        pub.subscribe(
            self.on_succeed_create_postgres_program, "succeed_create_program_database"
        )

        test_program_db = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_bald_dao.cxnargs["dbname"],
        }
        test_datamanager.user_configuration = test_toml_user_configuration
        test_datamanager.do_create_program(test_bald_dao, test_program_db)

        pub.unsubscribe(
            self.on_succeed_create_postgres_program, "succeed_create_program_database"
        )

        test_datamanager.do_close_program()
