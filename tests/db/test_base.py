# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.db.test_base.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the BaseDatabase class algorithms and methods."""

# Standard Library Imports
import tempfile

# Third Party Imports
import pytest
from pubsub import pub
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import UnmappedInstanceError

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError
from ramstk.models.db import BaseDatabase
from ramstk.models.dbrecords import (
    RAMSTKFunctionRecord,
    RAMSTKManufacturerRecord,
    RAMSTKRevisionRecord,
    RAMSTKSiteInfoRecord,
)

TEMPDIR = tempfile.gettempdir()


class TestCreateBaseDatabase:
    """Class for BaseDatabase initialization test suite."""

    @pytest.mark.unit
    def test_base_database_create(self):
        """Should create a BaseDatabase class instance."""
        dut = BaseDatabase()

        assert isinstance(dut, BaseDatabase)
        assert dut.engine is None
        assert dut.session is None
        assert not dut.database


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestConnectionMethods:
    """Class for BaseDatabase connection test suite."""

    def on_fail_connect_bad_db_name_type(self, logger_name, message):
        """Listen for do_log_error messages."""
        assert logger_name == "ERROR"
        assert message == (
            "Non-string or blank string value in database connection: 8675309."
        )
        print(
            "\033[35m\n\tfail_connect_program_database topic was broadcast for bad DB "
            "name type"
        )

    def on_fail_connect_unknown_dialect(self, logger_name, message):
        """Listen for do_log_error messages."""
        assert logger_name == "ERROR"
        assert message == "Unknown dialect in database connection: sqldoyle"
        print(
            "\033[35m\n\tfail_connect_program_database topic was broadcast for "
            "unknown dialect"
        )

    @pytest.mark.integration
    def test_do_connect_sqlite(self, test_toml_user_configuration):
        """do_connect() Should return None when connecting to a database."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "sqlite"
        test_toml_user_configuration.RAMSTK_PROG_INFO["database"] = "sqlite"
        DUT = BaseDatabase()

        assert DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO) is None
        assert isinstance(DUT.engine, Engine)
        assert isinstance(DUT.session, scoped_session)

    @pytest.mark.integration
    def test_do_connect_postgresql(self, test_toml_user_configuration):
        """do_connect() Should return None when connecting to a database."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO["database"] = "postgres"

        DUT = BaseDatabase()

        assert DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO) is None
        assert isinstance(DUT.engine, Engine)
        assert isinstance(DUT.session, scoped_session)

    @pytest.mark.integration
    def test_do_connect_bad_database_name_type(self, test_toml_user_configuration):
        """Raise a DataAccessError when passed a non-string database name."""
        pub.subscribe(self.on_fail_connect_bad_db_name_type, "do_log_error_msg")

        test_toml_user_configuration.RAMSTK_PROG_INFO["database"] = 8675309
        DUT = BaseDatabase()
        with pytest.raises(DataAccessError):
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        pub.unsubscribe(self.on_fail_connect_bad_db_name_type, "do_log_error_msg")

    @pytest.mark.integration
    def test_do_connect_bad_database_url(self, test_toml_user_configuration):
        """Raise a OperationalError when passed a bad database URL."""
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "sqlite"
        test_toml_user_configuration.RAMSTK_PROG_INFO["socket"] = "3306"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = "/home/test/testdb.db"
        DUT = BaseDatabase()

        with pytest.raises(DataAccessError):
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.integration
    def test_do_connect_unknown_dialect(self, test_toml_user_configuration):
        """Raise an DataAccessError when passed an unknown database dialect."""
        pub.subscribe(self.on_fail_connect_unknown_dialect, "do_log_error_msg")

        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "sqldoyle"
        DUT = BaseDatabase()
        with pytest.raises(DataAccessError):
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        pub.unsubscribe(self.on_fail_connect_unknown_dialect, "do_log_error_msg")

    @pytest.mark.integration
    def test_do_connect_no_server(self, test_toml_user_configuration):
        """do_connect() Should raise a DataAccessError when the server is off-line."""
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "shibby-shibby-do"
        DUT = BaseDatabase()

        with pytest.raises(DataAccessError):
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.integration
    def test_do_disconnect(self, test_toml_user_configuration):
        """Should return None when successfully closing a database connection."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "sqlite"
        test_toml_user_configuration.RAMSTK_PROG_INFO["database"] = "sqlite"
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        assert DUT.do_disconnect() is None
        assert DUT.session is None
        assert not DUT.database


@pytest.mark.usefixtures(
    "test_common_dao", "test_program_dao", "test_toml_user_configuration"
)
class TestInsertMethods:
    """Class for BaseDatabase insert methods test suite."""

    def on_fail_insert_record(self, logger_name, message):
        """Listen for fail_insert messages."""
        assert logger_name == "ERROR"
        assert (
            message
            == "Database error while adding a record. Error details: : INSERT INTO ramstk_site_info (fld_site_id, fld_site_name, fl...\n                    ^"
        )
        print("\033[35m\n\tfail_insert_record topic was broadcast for bad column type")

    @pytest.mark.integration
    def test_do_insert(self, test_program_dao, test_toml_user_configuration):
        """Should return None when inserting a record into a database table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = test_program_dao.cxnargs["database"]
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _revision = RAMSTKRevisionRecord()
        _revision.revision_id = 4

        assert DUT.do_insert(_revision) is None

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_do_insert_bad_date_field_type(
        self, test_program_dao, test_toml_user_configuration
    ):
        """Should raise a DataAccessError on non-date object for a date type field."""
        pub.subscribe(self.on_fail_insert_record, "do_log_error_msg")

        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = test_program_dao.cxnargs["database"]
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKSiteInfoRecord()
        _record.site_id = 1
        _record.expire_on = 0xA5

        with pytest.raises(DataAccessError):
            DUT.do_insert(_record)

        pub.unsubscribe(self.on_fail_insert_record, "do_log_error_msg")

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_do_insert_none(self, test_program_dao, test_toml_user_configuration):
        """Should raise an UnmappedInstanceError when passed None for the table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = test_program_dao.cxnargs["database"]
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        with pytest.raises(UnmappedInstanceError):
            DUT.do_insert(None)

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_do_insert_duplicate_pk(self, test_common_dao):
        """Raise a DataAccessError when attempting to add a duplicate primary key."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["database"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _record = RAMSTKSiteInfoRecord()
        _record.site_id = 1

        with pytest.raises(DataAccessError):
            DUT.do_insert(_record)
        DUT.do_disconnect()

    @pytest.mark.integration
    def test_do_insert_many(self, test_program_dao, test_toml_user_configuration):
        """Should return None when inserting a record into a database table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = test_program_dao.cxnargs["database"]
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _revision1 = RAMSTKRevisionRecord()
        _revision1.revision_id = 5
        _revision2 = RAMSTKRevisionRecord()
        _revision2.revision_id = 6
        _revision3 = RAMSTKRevisionRecord()
        _revision3.revision_id = 7
        assert DUT.do_insert_many([_revision1, _revision2, _revision3]) is None

        DUT.do_disconnect()


@pytest.mark.usefixtures("test_common_dao", "test_program_dao")
class TestDeleteMethods:
    """Class for BaseDatabase delete methods test suite."""

    def on_fail_delete_foreign_record(self, logger_name, message):
        """Listen for fail_delete messages."""
        assert logger_name == "ERROR"
        assert (
            "Database error when attempting to delete a record. Error details: "
            in message
        )
        print("\033[35m\n\tfail_delete_record topic was broadcast for foreign record")

    def on_fail_delete_missing_table(self, logger_name, message):
        """Listen for fail_delete messages."""
        assert logger_name == "ERROR"
        assert (
            "Database error when attempting to delete a record. Error details: "
            in message
        )
        print("\033[35m\n\tfail_delete_record topic was broadcast for missing table")

    @pytest.mark.integration
    def test_do_delete(self, test_common_dao):
        """Should return None when inserting a record into a database table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["database"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)
        # Why is the ramstk_site_info table not in the database???
        _record = (
            DUT.session.query(RAMSTKSiteInfoRecord)
            .filter(RAMSTKSiteInfoRecord.site_id == 1)
            .all()[0]
        )

        assert DUT.do_delete(_record) is None

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_do_delete_no_table(self, test_program_dao):
        """Raise DataAccessError when attempting to delete a non-existent record."""
        pub.subscribe(self.on_fail_delete_missing_table, "do_log_error_msg")

        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_program_dao.cxnargs["database"],
        }
        DUT = BaseDatabase()
        DUT.do_connect(config)

        _record = RAMSTKFunctionRecord()
        with pytest.raises(DataAccessError):
            DUT.do_delete(_record)

        DUT.do_disconnect()
        pub.unsubscribe(self.on_fail_delete_missing_table, "do_log_error_msg")


@pytest.mark.usefixtures("test_common_dao")
class TestUpdateMethods:
    """Class for BaseDatabase update methods test suite."""

    @pytest.mark.integration
    def test_do_update(self, test_common_dao):
        """Should return None when updating a record in a database table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["database"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _record = RAMSTKSiteInfoRecord()
        _record.site_id = 3
        DUT.do_insert(_record)

        _record.function_enabled = 1
        _record.requirement_enabled = 1
        _record.hardware_enabled = 1
        _record.software_enabled = 1
        _record.rcm_enabled = 1
        _record.fta_enabled = 1

        assert DUT.do_update() is None

        _record = (
            DUT.session.query(RAMSTKSiteInfoRecord)
            .filter(RAMSTKSiteInfoRecord.site_id == 3)
            .all()[0]
        )

        assert _record.function_enabled == 1
        assert _record.requirement_enabled == 1
        assert _record.hardware_enabled == 1
        assert _record.software_enabled == 1
        assert _record.rcm_enabled == 1
        assert _record.fta_enabled == 1

        _record.function_enabled = 0
        _record.requirement_enabled = 0
        _record.hardware_enabled = 0
        _record.software_enabled = 0
        _record.rcm_enabled = 0
        _record.fta_enabled = 0

        assert DUT.do_update() is None

        _record = (
            DUT.session.query(RAMSTKSiteInfoRecord)
            .filter(RAMSTKSiteInfoRecord.site_id == 3)
            .all()[0]
        )

        assert _record.function_enabled == 0
        assert _record.requirement_enabled == 0
        assert _record.hardware_enabled == 0
        assert _record.software_enabled == 0
        assert _record.rcm_enabled == 0
        assert _record.fta_enabled == 0

        DUT.do_disconnect()


@pytest.mark.usefixtures("test_common_dao")
class TestSelectMethods:
    """Class for BaseDatabase query methods test suite."""

    @pytest.mark.integration
    def test_do_select(self, test_common_dao):
        """do_query() Should return None when updating a record in a database table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["database"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _record = (
            DUT.session.query(RAMSTKManufacturerRecord)
            .filter(RAMSTKManufacturerRecord.manufacturer_id == 1)
            .all()[0]
        )

        assert _record.manufacturer_id == 1
        assert _record.description == "Sprague"
        assert _record.location == "New Hampshire"
        assert _record.cage_code == "13606"

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_get_last_id(self, test_common_dao):
        """get_last_id() Should return an integer for the last used ID."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["database"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _record = RAMSTKSiteInfoRecord()
        _record.site_id = 21
        DUT.do_insert(_record)
        _record = RAMSTKSiteInfoRecord()
        _record.site_id = 22
        DUT.do_insert(_record)

        _last_id = DUT.get_last_id(RAMSTKSiteInfoRecord.__tablename__, "fld_site_id")

        assert _last_id == 22

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_get_last_id_passed_attribute(self, test_common_dao):
        """Should return integer for the last used ID."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["database"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _last_id = DUT.get_last_id(RAMSTKSiteInfoRecord.__tablename__, "site_id")

        assert _last_id == 22

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_get_last_id_unknown_column(self, test_common_dao):
        """get_last_id() Should raise an exception when passed an unknown column
        name."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["database"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        with pytest.raises(DataAccessError) as exc_info:
            DUT.get_last_id(
                RAMSTKSiteInfoRecord.__tablename__,
                "fld_column_id",
            )
        assert "UndefinedColumn" in str(exc_info.value)

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_get_last_id_unknown_table(self, test_common_dao):
        """get_last_id() Should raise an exception when passed an unknown table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["database"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        with pytest.raises(DataAccessError):
            DUT.get_last_id(
                RAMSTKFunctionRecord.__tablename__,
                "fld_function_id",
            )
        DUT.do_disconnect()

    @pytest.mark.integration
    def test_get_last_id_empty_table(self):
        """get_last_id() should raise an exception when passed an unknown table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "postgres",
        }
        DUT = BaseDatabase()
        DUT.do_connect(config)

        with pytest.raises(DataAccessError):
            DUT.get_last_id(
                "ramstk_empty_table",
                "fld_empty_id",
            )
        DUT.do_disconnect()

    @pytest.mark.integration
    def test_get_database_list(self):
        """Should return a list of database names available on the server."""
        _database = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "postgres",
        }
        DUT = BaseDatabase()
        DUT.do_connect(_database)

        _databases = DUT.get_database_list(_database)

        DUT.do_disconnect()

        assert isinstance(_databases, list)
        assert "postgres" not in _databases
        assert "template0" not in _databases
        assert "template1" not in _databases

    @pytest.mark.integration
    def test_get_database_list_unknown_dialect(self):
        """Should return a list of database names available on the server."""
        _database = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": "postgres",
        }
        DUT = BaseDatabase()
        DUT.do_connect(_database)

        _database["dialect"] = "doyleton"
        with pytest.raises(DataAccessError):
            DUT.get_database_list(_database)

        DUT.do_disconnect()
