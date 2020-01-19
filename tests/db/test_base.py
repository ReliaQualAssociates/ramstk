# pylint: disable=protected-access, no-self-use
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
from ramstk.models.commondb import RAMSTKSiteInfo
from ramstk.models.programdb import RAMSTKFunction, RAMSTKRevision

TEMPDIR = tempfile.gettempdir()


class TestCreateBaseDatabase():
    """Class for BaseDatabase initialization test suite."""
    @pytest.mark.unit
    def test_base_database_create(self):
        """__init__() should create a BaseDatabase class instance."""
        DUT = BaseDatabase()

        assert isinstance(DUT, BaseDatabase)
        assert DUT.engine is None
        assert DUT.session is None
        assert DUT.database == ''


@pytest.mark.usefixtures('test_toml_user_configuration')
class TestConnectionMethods():
    """Class for BaseDatabase connection test suite."""
    @pytest.mark.unit
    def test_do_connect_sqlite(self, test_toml_user_configuration):
        """do_connect() should return None when connecting to a database."""
        test_toml_user_configuration.get_user_configuration()
        DUT = BaseDatabase()

        assert DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO) \
               is None
        assert isinstance(DUT.engine, Engine)
        assert isinstance(DUT.session, scoped_session)
        assert DUT.database == 'sqlite:///'

    @pytest.mark.unit
    def test_do_connect_postgresql(self, test_toml_user_configuration):
        """do_connect() should return None when connecting to a database."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO['dialect'] = 'postgres'
        test_toml_user_configuration.RAMSTK_PROG_INFO['user'] = 'postgres'
        test_toml_user_configuration.RAMSTK_PROG_INFO['password'] = 'postgres'
        test_toml_user_configuration.RAMSTK_PROG_INFO['host'] = 'localhost'
        test_toml_user_configuration.RAMSTK_PROG_INFO['port'] = '5432'
        test_toml_user_configuration.RAMSTK_PROG_INFO['database'] = ''

        DUT = BaseDatabase()

        assert DUT.do_connect(
            test_toml_user_configuration.RAMSTK_PROG_INFO) is None
        assert isinstance(DUT.engine, Engine)
        assert isinstance(DUT.session, scoped_session)
        assert DUT.database == \
               'postgresql+psycopg2://postgres:postgres@localhost:5432/'

    @pytest.mark.unit
    def test_do_connect_bad_database_name_type(self,
                                               test_toml_user_configuration):
        """do_connect() should raise a DataAccessError when passed a non-string database name."""
        test_toml_user_configuration.RAMSTK_PROG_INFO['database'] = 8675309
        DUT = BaseDatabase()

        with pytest.raises(DataAccessError):
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.unit
    def test_do_connect_bad_database_url(self, test_toml_user_configuration):
        """do_connect() should raise an exc.OperationalError when passed a bad
        database URL."""
        test_toml_user_configuration.RAMSTK_PROG_INFO['dialect'] = 'sqlite'
        test_toml_user_configuration.RAMSTK_PROG_INFO['socket'] = '3306'
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = '/home/test/testdb.db'
        DUT = BaseDatabase()

        with pytest.raises(exc.OperationalError):
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.unit
    def test_do_connect_unknown_dialect(self, test_toml_user_configuration):
        """do_connect() should raise an DataAccessError when passed an unknown/unsupported database dialect."""
        test_toml_user_configuration.RAMSTK_PROG_INFO['dialect'] = 'sqldoyle'
        DUT = BaseDatabase()

        with pytest.raises(DataAccessError):
            DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

    @pytest.mark.unit
    def test_do_disconnect(self, test_toml_user_configuration):
        """do_disconnect() should return None when successfully closing a database connection."""
        test_toml_user_configuration.get_user_configuration()
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        assert DUT.do_disconnect() is None
        assert DUT.session is None
        assert DUT.database == ''


@pytest.mark.usefixtures('test_simple_database',
                         'test_toml_user_configuration')
class TestInsertMethods():
    """Class for BaseDatabase insert methods test suite."""
    def on_fail_insert_record(self, error_message):
        """Method to respond to PyPubSub failure message."""
        assert error_message == (
            "There was an database error when attempting to add a record.  "
            "Faulty SQL statement was:\n\tINSERT INTO ramstk_site_info "
            "(fld_product_key, fld_expire_on, fld_function_enabled, "
            "fld_requirement_enabled, fld_hardware_enabled, "
            "fld_vandv_enabled, fld_fmea_enabled) VALUES "
            "(?, ?, ?, ?, ?, ?, ?).\nParameters were:\n\t"
            "[{'fld_expire_on': 165}].")
        print("\033[35m\nfail_insert_record topic was broadcast.")

    @pytest.mark.unit
    def test_do_insert(self, test_simple_database,
                       test_toml_user_configuration):
        """do_insert() should return None when inserting a record into a database table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        assert DUT.do_insert(RAMSTKRevision()) is None

    @pytest.mark.unit
    def test_do_insert_bad_date_field_type(self, test_simple_database,
                                           test_toml_user_configuration):
        """do_insert() should raise a DataAccessError when passed a non-date object for a date type field."""
        pub.subscribe(self.on_fail_insert_record, 'fail_insert_record')

        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKSiteInfo()
        _record.expire_on = 0xA5

        with pytest.raises(DataAccessError):
            DUT.do_insert(_record)

        pub.unsubscribe(self.on_fail_insert_record, 'fail_insert_record')

    @pytest.mark.unit
    def test_do_insert_none(self, test_simple_database,
                            test_toml_user_configuration):
        """do_insert() should raise an UnmappedInstanceError when passed None for the table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        with pytest.raises(UnmappedInstanceError):
            DUT.do_insert(None)

    @pytest.mark.unit
    def test_do_insert_duplicate_pk(self, test_simple_database,
                                    test_toml_user_configuration):
        """do_insert() should raise a DataAccessError when attempting to add a record with a duplicate primary key."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKSiteInfo()
        _record.site_id = 1
        DUT.do_insert(_record)

        _record = RAMSTKSiteInfo()
        _record.site_id = 1

        with pytest.raises(DataAccessError):
            DUT.do_insert(_record)

    @pytest.mark.unit
    def test_do_insert_many(self, test_simple_database,
                            test_toml_user_configuration):
        """do_insert() should return None when inserting a record into a database table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        assert DUT.do_insert_many(
            [RAMSTKRevision(),
             RAMSTKRevision(),
             RAMSTKRevision()]) is None


@pytest.mark.usefixtures('test_simple_database',
                         'test_toml_user_configuration')
class TestDeleteMethods():
    """Class for BaseDatabase delete methods test suite."""
    def on_fail_delete_foreign_record(self, error_message):
        """Method to respond to PyPubSub failure message."""
        assert error_message == (
            "There was an database error when attempting to delete a record.  "
            "Error returned from database was:\n\t"
            "no such table: ramstk_mission.")
        print("\033[35m\nfail_delete_record topic was broadcast.")

    def on_fail_delete_missing_table(self, error_message):
        """Method to respond to PyPubSub failure message."""
        assert "is not persisted" in error_message
        print("\033[35m\nfail_delete_record topic was broadcast.")

    @pytest.mark.unit
    def test_do_delete(self, test_simple_database,
                       test_toml_user_configuration):
        """do_delete() should return None when inserting a record into a database table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKSiteInfo()
        DUT.do_insert(_record)

        assert DUT.do_delete(_record) is None

    @pytest.mark.unit
    def test_do_delete_missing_foreign_table(self, test_simple_database,
                                             test_toml_user_configuration):
        """do_delete() should raise a DataAccessError when attempting to delete a record with a foreign key and the foreign table does not exist."""
        pub.subscribe(self.on_fail_delete_foreign_record, 'fail_delete_record')

        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKRevision()
        DUT.do_insert(_record)

        with pytest.raises(DataAccessError):
            DUT.do_delete(_record)

        pub.unsubscribe(self.on_fail_delete_foreign_record,
                        'fail_delete_record')

    @pytest.mark.unit
    def test_do_delete_no_table(self, test_simple_database,
                                test_toml_user_configuration):
        """do_delete() should raise a DataAccessError when attempting to delete a record from a table that does not exist."""
        pub.subscribe(self.on_fail_delete_missing_table, 'fail_delete_record')

        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKFunction()
        with pytest.raises(DataAccessError):
            DUT.do_delete(_record)

        pub.unsubscribe(self.on_fail_delete_missing_table,
                        'fail_delete_record')


@pytest.mark.usefixtures('test_simple_database',
                         'test_toml_user_configuration')
class TestUpdateMethods():
    """Class for BaseDatabase update methods test suite."""
    @pytest.mark.unit
    def test_do_update(self, test_simple_database,
                       test_toml_user_configuration):
        """do_update() should return None when updating a record in a database table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKSiteInfo()
        DUT.do_insert(_record)

        _record.function_enabled = 2
        _record.requirements_enabled = 3
        _record.hardware_enabled = 4

        assert DUT.do_update() is None

        _record = DUT.session.query(RAMSTKSiteInfo).all()[0]

        assert _record.function_enabled == 2
        assert _record.requirements_enabled == 3
        assert _record.hardware_enabled == 4


@pytest.mark.usefixtures('test_simple_database',
                         'test_toml_user_configuration')
class TestSelectMethods():
    """Class for BaseDatabase query methods test suite."""
    @pytest.mark.unit
    def test_do_select(self, test_simple_database,
                       test_toml_user_configuration):
        """do_query() should return None when updating a record in a database table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _record = RAMSTKSiteInfo()
        DUT.do_insert(_record)

        _record = DUT.session.query(RAMSTKSiteInfo).first()

        assert _record.site_id == 1
        assert _record.function_enabled == 0
        assert _record.requirement_enabled == 0
        assert _record.hardware_enabled == 0

    @pytest.mark.unit
    def test_get_last_id(self, test_simple_database,
                         test_toml_user_configuration):
        """get_last_id() should return an integer for the last used ID."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        DUT.do_insert(RAMSTKSiteInfo())
        DUT.do_insert(RAMSTKSiteInfo())

        _last_id = DUT.get_last_id(RAMSTKSiteInfo.__tablename__, "fld_site_id")

        assert _last_id == 3

    @pytest.mark.unit
    def test_get_last_id_passed_attribute(self, test_simple_database,
                                          test_toml_user_configuration):
        """get_last_id() should return an integer for the last used ID when passed a column name as an attribute."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        _last_id = DUT.get_last_id(RAMSTKSiteInfo.__tablename__, "site_id")

        assert _last_id == 3

    @pytest.mark.unit
    def test_get_last_id_unknown_column(self, test_simple_database,
                                        test_toml_user_configuration):
        """get_last_id() should raise an SQLAlchemy OperationalError when passed an unknown column name."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        with pytest.raises(exc.OperationalError):
            DUT.get_last_id(RAMSTKSiteInfo.__tablename__, "fld_column_id")

    @pytest.mark.unit
    def test_get_last_id_unknown_table(self, test_simple_database,
                                       test_toml_user_configuration):
        """get_last_id() should raise an SQLAlchemy OperationalError when passed an unknown table."""
        test_toml_user_configuration.get_user_configuration()
        test_toml_user_configuration.RAMSTK_PROG_INFO[
            'database'] = test_simple_database
        DUT = BaseDatabase()
        DUT.do_connect(test_toml_user_configuration.RAMSTK_PROG_INFO)

        with pytest.raises(exc.OperationalError):
            DUT.get_last_id(RAMSTKFunction.__tablename__, "fld_function_id")
