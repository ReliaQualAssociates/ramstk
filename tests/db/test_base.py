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
from sqlalchemy import exc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import UnmappedInstanceError

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models import (
    RAMSTKFunctionRecord,
    RAMSTKRevisionRecord,
    RAMSTKSiteInfoRecord,
)
from ramstk.models.commondb import RAMSTKManufacturer

TEMPDIR = tempfile.gettempdir()


class TestCreateBaseDatabase:
    """Class for BaseDatabase initialization test suite."""

    @pytest.mark.unit
    def test_base_database_create(self):
        """should create a BaseDatabase class instance."""
        DUT = BaseDatabase()

        assert isinstance(DUT, BaseDatabase)
        assert DUT.engine is None
        assert DUT.session is None
        assert DUT.database == ""


@pytest.mark.usefixtures("test_toml_user_configuration")
class TestConnectionMethods:
    """Class for BaseDatabase connection test suite."""

    @pytest.mark.integration
    def test_do_connect_sqlite(self, test_toml_user_configuration):
        """do_connect() should return None when connecting to a database."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "sqlite"
        test_toml_user_configuration.RAMSTK_PROG_INFO["database"] = ""
        DUT = BaseDatabase()

        assert DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO) is None
        assert isinstance(DUT.engine, Engine)
        assert isinstance(DUT.session, scoped_session)
        assert DUT.database == "sqlite:///"

    @pytest.mark.integration
    def test_do_connect_postgresql(self, test_toml_user_configuration):
        """do_connect() should return None when connecting to a database."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO["database"] = ""

        DUT = BaseDatabase()

        assert DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO) is None
        assert isinstance(DUT.engine, Engine)
        assert isinstance(DUT.session, scoped_session)
        assert DUT.database == "postgresql+psycopg2://postgres:postgres@localhost:5432/"

    @pytest.mark.integration
    def test_do_connect_bad_database_name_type(self, test_toml_user_configuration):
        """do_connect() should raise a DataAccessError when passed a non-string
        database name."""
        test_toml_user_configuration.RAMSTK_PROG_INFO["database"] = 8675309
        DUT = BaseDatabase()

        with pytest.raises(DataAccessError):
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.integration
    def test_do_connect_bad_database_url(self, test_toml_user_configuration):
        """do_connect() should raise an exc.OperationalError when passed a bad database
        URL."""
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "sqlite"
        test_toml_user_configuration.RAMSTK_PROG_INFO["socket"] = "3306"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = "/home/test/testdb.db"
        DUT = BaseDatabase()

        with pytest.raises(DataAccessError) as _error:
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.integration
    def test_do_connect_unknown_dialect(self, test_toml_user_configuration):
        """do_connect() should raise an DataAccessError when passed an
        unknown/unsupported database dialect."""
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "sqldoyle"
        DUT = BaseDatabase()

        with pytest.raises(DataAccessError) as _error:
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.integration
    def test_do_connect_no_server(self, test_toml_user_configuration):
        """do_connect() should raise a DataAccessError when the server is off-line."""
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "shibby-shibby-do"
        DUT = BaseDatabase()

        with pytest.raises(DataAccessError) as _error:
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.integration
    def test_do_disconnect(self, test_toml_user_configuration):
        """do_disconnect() should return None when successfully closing a database
        connection."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "sqlite"
        test_toml_user_configuration.RAMSTK_PROG_INFO["database"] = ""
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        assert DUT.do_disconnect() is None
        assert DUT.session is None
        assert DUT.database == ""


@pytest.mark.usefixtures(
    "test_common_dao", "test_program_dao", "test_toml_user_configuration"
)
class TestInsertMethods:
    """Class for BaseDatabase insert methods test suite."""

    def on_fail_insert_record(self, error_message):
        """Method to respond to PyPubSub failure message."""
        assert isinstance(error_message, str)
        print("\033[35m\nfail_insert_record topic was broadcast.")

    @pytest.mark.integration
    def test_do_insert(self, test_program_dao, test_toml_user_configuration):
        """do_insert() should return None when inserting a record into a database
        table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = test_program_dao.cxnargs["dbname"]
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
        """do_insert() should raise a DataAccessError when passed a non-date object for
        a date type field."""
        pub.subscribe(self.on_fail_insert_record, "fail_insert_record")

        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = test_program_dao.cxnargs["dbname"]
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKSiteInfoRecord()
        _record.site_id = 1
        _record.expire_on = 0xA5

        with pytest.raises(DataAccessError):
            DUT.do_insert(_record)

        pub.unsubscribe(self.on_fail_insert_record, "fail_insert_record")

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_do_insert_none(self, test_program_dao, test_toml_user_configuration):
        """do_insert() should raise an UnmappedInstanceError when passed None for the
        table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = test_program_dao.cxnargs["dbname"]
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        with pytest.raises(UnmappedInstanceError):
            DUT.do_insert(None)

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_do_insert_duplicate_pk(self, test_common_dao):
        """do_insert() should raise a DataAccessError when attempting to add a record
        with a duplicate primary key."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["dbname"],
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
        """do_insert() should return None when inserting a record into a database
        table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO["dialect"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["user"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["password"] = "postgres"
        test_toml_user_configuration.RAMSTK_PROG_INFO["host"] = "localhost"
        test_toml_user_configuration.RAMSTK_PROG_INFO["port"] = "5432"
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            "database"
        ] = test_program_dao.cxnargs["dbname"]
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

    def on_fail_delete_foreign_record(self, error_message):
        """Method to respond to PyPubSub failure message."""
        assert error_message == (
            "There was an database error when attempting to delete a record.  "
            'Error returned from database was:\n\trelation "ramstk_mission" '
            "does not exist\nLINE 2: FROM ramstk_mission \n             ^\n."
        )
        print("\033[35m\nfail_delete_record topic was broadcast.")

    def on_fail_delete_missing_table(self, error_message):
        """Method to respond to PyPubSub failure message."""
        assert "is not persisted" in error_message
        print("\033[35m\nfail_delete_record topic was broadcast.")

    @pytest.mark.skip
    def test_do_delete(self, test_common_dao):
        """do_delete() should return None when inserting a record into a database
        table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["dbname"],
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

    @pytest.mark.skip
    def test_do_delete_missing_foreign_table(self, test_program_dao):
        """do_delete() should raise a DataAccessError when attempting to delete a
        record with a foreign key and the foreign table does not exist."""
        pub.subscribe(self.on_fail_delete_foreign_record, "fail_delete_record")

        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_program_dao.cxnargs["dbname"],
        }
        DUT = BaseDatabase()
        DUT.do_connect(config)

        _record = RAMSTKRevisionRecord()
        _record.revision_id = 4
        DUT.do_insert(_record)

        with pytest.raises(DataAccessError):
            DUT.do_delete(_record)

        DUT.do_disconnect()
        pub.unsubscribe(self.on_fail_delete_foreign_record, "fail_delete_record")

    @pytest.mark.integration
    def test_do_delete_no_table(self, test_program_dao):
        """do_delete() should raise a DataAccessError when attempting to delete a
        record from a table that does not exist."""
        pub.subscribe(self.on_fail_delete_missing_table, "fail_delete_record")

        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_program_dao.cxnargs["dbname"],
        }
        DUT = BaseDatabase()
        DUT.do_connect(config)

        _record = RAMSTKFunctionRecord()
        with pytest.raises(DataAccessError):
            DUT.do_delete(_record)

        DUT.do_disconnect()
        pub.unsubscribe(self.on_fail_delete_missing_table, "fail_delete_record")


@pytest.mark.usefixtures("test_common_dao")
class TestUpdateMethods:
    """Class for BaseDatabase update methods test suite."""

    @pytest.mark.integration
    def test_do_update(self, test_common_dao):
        """do_update() should return None when updating a record in a database
        table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["dbname"],
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
        """do_query() should return None when updating a record in a database table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["dbname"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _record = (
            DUT.session.query(RAMSTKManufacturer)
            .filter(RAMSTKManufacturer.manufacturer_id == 1)
            .all()[0]
        )

        assert _record.manufacturer_id == 1
        assert _record.description == "Sprague"
        assert _record.location == "New Hampshire"
        assert _record.cage_code == "13606"

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_get_last_id(self, test_common_dao):
        """get_last_id() should return an integer for the last used ID."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["dbname"],
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
        """get_last_id() should return an integer for the last used ID when passed a
        column name as an attribute."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["dbname"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _last_id = DUT.get_last_id(RAMSTKSiteInfoRecord.__tablename__, "site_id")

        assert _last_id == 22

        DUT.do_disconnect()

    @pytest.mark.integration
    def test_get_last_id_unknown_column(self, test_common_dao):
        """get_last_id() should return 0 when passed an unknown column name."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["dbname"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _last_id = DUT.get_last_id(RAMSTKSiteInfoRecord.__tablename__, "fld_column_id")

        DUT.do_disconnect()

        assert _last_id == 0

    @pytest.mark.integration
    def test_get_last_id_unknown_table(self, test_common_dao):
        """get_last_id() should return 0 when passed an unknown table."""
        config = {
            "dialect": "postgres",
            "user": "postgres",
            "password": "postgres",
            "host": "localhost",
            "port": "5432",
            "database": test_common_dao.cxnargs["dbname"],
        }

        DUT = BaseDatabase()
        DUT.do_connect(config)

        _last_id = DUT.get_last_id(
            RAMSTKFunctionRecord.__tablename__, "fld_function_id"
        )

        DUT.do_disconnect()

        assert _last_id == 0

    @pytest.mark.integration
    def test_get_last_id_empty_table(self):
        """get_last_id() should return 0 when passed an unknown table."""
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

        _last_id = DUT.get_last_id("ramstk_empty_table", "fld_empty_id")

        DUT.do_disconnect()

        assert _last_id == 0

    @pytest.mark.skip
    def test_get_database_list(self):
        """get_database_list() should return a list of database names available on the
        server."""
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

        # How to test this now that the databases are being given a random name conf.py.
        assert "TestCommonDB" in _databases
        assert "TestProgramDB" in _databases
