# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_database.py is part of The RAMSTK Project
#
# All rights reserved.
"""Class for testing RAMSTK module algorithms and models."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.db import BaseDatabase, RAMSTKProgramDB


@pytest.fixture(scope="class")
def test_datamanager(test_program_dao):
    """Get a table model instance for each test class."""
    # Create the device under test (dut) and connect to the database.
    dut = RAMSTKProgramDB()

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
        """Listen for succeed_connect messages."""
        assert isinstance(dao, BaseDatabase)
        print("\033[36m\n\tsucceed_connect_program_database topic was broadcast")

    def on_fail_open_program_bad_url(self, error_message):
        """Listen for fail_connect messages."""
        assert error_message != ""
        # (
        #    "Fatal:  database \"bad_database_url.ramstk\" does not exist\n: {
        #    'dialect': "
        #    "'postgres', 'user': 'postgres', 'password': 'postgres', 'host': "
        #    "'localhost', 'port': '5432', 'dbname': 'bad_database_url.ramstk'}"
        # )
        print(
            "\033[35m\n\tfail_connect_program_database topic was broadcast on bad URL."
        )

    def on_fail_open_program_unknown_dialect(self, error_message):
        """Listen for fail_connect messages."""
        assert error_message != ""
        # assert error_message == (
        #    "Unknown database dialect in database connection dict: "
        #    "{'dialect': 'doyleton', 'user': 'postgres', 'password': 'postgres', "
        #    "'host': 'localhost', 'port': '5432', 'dbname':
        #    'bad_database_url.ramstk'}."
        # )
        print(
            "\033[35m\n\tfail_connect_program_database topic was broadcast on unknown "
            "dialect."
        )

    def on_fail_open_program_non_string_url(self, error_message):
        """Listen for fail_connect messages."""
        assert isinstance(error_message, str)
        # assert error_message == (
        #    "'Fatal:  database "8742.11" does not exist\n: {\'dialect\': "
        # "\'postgres\', \'user\': \' postgres\', \'password\': \'postgres\', \'host\':"
        # " \'localhost\', \'port\': \'5432\', \ 'dbname\': 8742.11}'"
        # )
        print(
            "\033[35m\n\tfail_connect_program_database topic was broadcast on "
            "non-string URL."
        )

    def on_succeed_close_program(self):
        """Listen for succeed_disconnect messages."""
        print("\033[36m\n\tsucceed_disconnect_program_database topic was broadcast")

    def on_fail_close_program(self, error_message):
        """Listen for fail_disconnect messages."""
        assert error_message == (
            "Not currently connected to a database.  Nothing to close."
        )
        print("\033[35m\n\tfail_disconnect_program_database topic was broadcast")

    def on_request_update_revision(self):
        """Listen for request_update_all messages."""
        print("\033[36m\n\trequest_update_all_revision topic was broadcast")

    def on_request_update_function(self):
        """Listen for request_update_all messages."""
        print("\033[36m\n\trequest_update_all_function topic was broadcast")

    def on_request_update_requirement(self):
        """Listen for request_update_all messages."""
        print("\033[36m\n\trequest_update_all_requirement topic was broadcast")

    def on_request_update_stakeholder(self):
        """Listen for request_update_all messages."""
        print("\033[36m\n\trequest_update_all_stakeholder topic was broadcast")

    def on_request_update_hardware(self):
        """Listen for request_update_all messages."""
        print("\033[36m\n\trequest_update_all_hardware topic was broadcast")

    def on_request_update_validation(self):
        """Listen for request_update_all messages."""
        print("\033[36m\n\trequest_update_all_validation topic was broadcast")

    def on_succeed_create_postgres_program(self, program_db, database):
        """Listen for succeed_create messages."""
        assert isinstance(program_db, BaseDatabase)
        assert database["database"] == program_db.cxnargs["dbname"]
        print(
            "\033[36m\n\tsucceed_create_program_database topic was broadcast "
            "when creating postgres database"
        )

    @pytest.mark.unit
    def test_create_program_manager(self, test_datamanager):
        """__init__() should create an instance of the RAMSTK program manager."""
        assert isinstance(test_datamanager, RAMSTKProgramDB)
        assert isinstance(test_datamanager.dic_tables, dict)
        assert test_datamanager.dic_tables["revision"] == object
        assert test_datamanager.dic_tables["function"] == object
        assert test_datamanager.dic_tables["allocation"] == object
        assert test_datamanager.dic_tables["requirement"] == object
        assert test_datamanager.dic_tables["similar_item"] == object
        assert test_datamanager.dic_tables["stakeholder"] == object
        assert test_datamanager.dic_tables["hardware"] == object
        assert test_datamanager.dic_tables["options"] == object
        assert test_datamanager.dic_tables["program_info"] == object
        assert test_datamanager.dic_tables["program_status"] == object
        assert test_datamanager.dic_tables["validation"] == object
        assert test_datamanager.dic_tables["options"] == object
        assert test_datamanager.dic_views["fmea"] == object
        assert test_datamanager.dic_views["pof"] == object
        assert isinstance(test_datamanager.program_dao, BaseDatabase)
        assert pub.isSubscribed(
            test_datamanager.do_create_program, "request_create_program"
        )
        assert pub.isSubscribed(
            test_datamanager.do_open_program, "request_open_program"
        )
        assert pub.isSubscribed(
            test_datamanager.do_close_program, "request_close_program"
        )
        assert pub.isSubscribed(
            test_datamanager.do_save_program, "request_update_program"
        )

    @pytest.mark.integration
    def test_do_open_program(self, test_datamanager, test_program_dao):
        """Should connect to test program database."""
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
        """Should broadcast the fail message when attempting to open a bad URL."""
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
        """Broadcast fail message when attempting to open db of unsupported dialect."""
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
        """Should broadcast fail message when attempting to open a non-string URL."""
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
        """Should disconnect from test program database."""
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
        """Broadcast fail message on attempts to close database when not connected."""
        pub.subscribe(self.on_fail_close_program, "fail_disconnect_program_database")

        DUT = RAMSTKProgramDB()
        DUT.do_close_program()

        assert isinstance(DUT.program_dao, BaseDatabase)

        pub.unsubscribe(self.on_fail_close_program, "fail_disconnect_program_database")
        pub.unsubscribe(DUT.do_create_program, "request_create_program")
        pub.unsubscribe(DUT.do_open_program, "request_open_program")
        pub.unsubscribe(DUT.do_close_program, "request_close_program")
        pub.unsubscribe(DUT.do_save_program, "request_update_program")

    @pytest.mark.integration
    def test_save_program(self, test_datamanager, test_program_dao):
        """Should cause all workstream modules to execute their save_all() method."""
        pub.subscribe(self.on_request_update_revision, "request_update_all_revision")
        pub.subscribe(self.on_request_update_function, "request_update_all_function")
        pub.subscribe(
            self.on_request_update_requirement, "request_update_all_requirement"
        )
        pub.subscribe(
            self.on_request_update_stakeholder, "request_update_all_stakeholder"
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

        pub.unsubscribe(self.on_request_update_revision, "request_update_all_revision")
        pub.unsubscribe(self.on_request_update_function, "request_update_all_function")
        pub.unsubscribe(
            self.on_request_update_requirement, "request_update_all_requirement"
        )
        pub.unsubscribe(
            self.on_request_update_stakeholder, "request_update_all_stakeholder"
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
        """do_create_program() should broadcast the success message."""
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
