# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.dao.test_dao.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for Data Access Object (DAO) module algorithms and models."""

# Standard Library Imports
import os
import tempfile

# Third Party Imports
import pytest
from sqlalchemy.orm import sessionmaker

# RAMSTK Package Imports
from ramstk.dao.DAO import DAO
from ramstk.dao.programdb.RAMSTKRevision import RAMSTKRevision

TEMPDIR = tempfile.gettempdir()

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Doyle "weibullguy" Rowland'


@pytest.mark.integration
def test_dao_create():
    """ __init__() should create a DAO class instance. """
    DUT = DAO()

    assert isinstance(DUT, DAO)
    assert isinstance(DUT.RAMSTK_SESSION, sessionmaker)


@pytest.mark.integration
def test_dao_db_connect(test_configuration):
    """ db_connect() should return False on success connecting to an SQLite database. """
    DUT = DAO()

    _database = test_configuration.RAMSTK_BACKEND + ':///' + \
                test_configuration.RAMSTK_PROG_INFO['database']

    assert not DUT.db_connect(_database)


@pytest.mark.integration
def test_dao_db_create_common(test_configuration):
    """ db_create_common() should return False on success. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_COM_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_common_db.ramstk'
    )

    assert DUT.db_create_common(_database, test=True) is None

    os.remove(TEMPDIR + '/_ramstk_common_db.ramstk')


@pytest.mark.integration
def test_dao_db_create_common_bad_db_name(test_configuration):
    """ db_create_common() should return True on failure. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_COM_BACKEND + ':/' + TEMPDIR +
        '/_ramstk_common_db.ramstk'
    )

    assert DUT.db_create_common(_database, test=True)


@pytest.mark.integration
def test_dao_db_create_program(test_configuration):
    """ db_create_program() should return False on success. """
    # Remove test program database from earlier runs if there is one.
    if os.path.exists(TEMPDIR + '/_ramstk_program_db.ramstk'):
        os.remove(TEMPDIR + '/_ramstk_program_db.ramstk')

    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_program_db.ramstk'
    )

    assert not DUT.db_create_program(_database)


@pytest.mark.integration
def test_dao_db_create_program_bad_db_name(test_configuration):
    """ db_create_program() should return True on failure. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_BACKEND + ':/' + TEMPDIR +
        '/_ramstk_program_db.ramstk'
    )

    assert DUT.db_create_program(_database)


@pytest.mark.integration
def test_dao_db_add(test_configuration):
    """ db_add() should return a zero error code on success when adding a single record to the database. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_program_db.ramstk'
    )
    DUT.db_connect(_database)

    _error_code, _msg = DUT.db_add(
        [
            RAMSTKRevision(),
        ], DUT.session,
    )

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK "
        "Program database."
    )


@pytest.mark.integration
def test_dao_db_add_no_item(test_configuration):
    """ db_add() should return a 1003 error code on failure. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_program_db.ramstk'
    )
    DUT.db_connect(_database)

    _error_code, _msg = DUT.db_add(
        [
            None,
        ], DUT.session,
    )

    assert _error_code == 1
    assert _msg == (
        "RAMSTK ERROR: Adding one or more items to the RAMSTK "
        "Program database."
    )


@pytest.mark.integration
def test_dao_db_add_many(test_configuration):
    """ db_add() should return a zero error code on success when adding multiple records to the database. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_program_db.ramstk'
    )
    DUT.db_connect(_database)

    _revision1 = RAMSTKRevision()
    _revision2 = RAMSTKRevision()
    _revision3 = RAMSTKRevision()

    _error_code, _msg = DUT.db_add(
        [_revision1, _revision2, _revision3],
        DUT.session,
    )

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Adding one or more items to the RAMSTK "
        "Program database."
    )


@pytest.mark.integration
def test_dao_db_update(test_configuration):
    """ db_update() should return a zero error code on success. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_program_db.ramstk'
    )
    DUT.db_connect(_database)

    _revision = RAMSTKRevision()
    DUT.db_add(
        [
            _revision,
        ], DUT.session,
    )

    _revision.availability_logistics = 0.9959
    _revision.availability_mission = 0.9999

    _error_code, _msg = DUT.db_update(DUT.session)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_dao_db_delete(test_configuration):
    """ db_delete() should return a zero error code on success. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_program_db.ramstk'
    )
    DUT.db_connect(_database)

    _revision = RAMSTKRevision()
    DUT.db_add(
        [
            _revision,
        ], DUT.session,
    )

    _error_code, _msg = DUT.db_delete(_revision, DUT.session)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
        "database."
    )


@pytest.mark.integration
def test_dao_db_delete_no_item(test_configuration):
    """ db_delete() should return a 1005 error code on failure. """
    DUT = DAO()
    _database = (
        test_configuration.RAMSTK_BACKEND + ':///' + TEMPDIR +
        '/_ramstk_program_db.ramstk'
    )
    DUT.db_connect(_database)

    _error_code, _msg = DUT.db_delete(None, DUT.session)

    assert _error_code == 1
    assert _msg == (
        "RAMSTK ERROR: Deleting an item from the RAMSTK Program database "
        "with error: Class 'builtins.NoneType' is not mapped."
    )
