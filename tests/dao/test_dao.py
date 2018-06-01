# -*- coding: utf-8 -*-
#
#       tests.dao.test_dao.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Data Access Object (DAO) module algorithms and models."""

import os

from sqlalchemy.orm import sessionmaker

import pytest

from rtk.Configuration import Configuration
from rtk.dao.DAO import DAO
from rtk.dao.programdb.RTKRevision import RTKRevision
from rtk.dao.programdb.RTKMission import RTKMission
from rtk.dao.programdb.RTKMissionPhase import RTKMissionPhase
from rtk.dao.programdb.RTKEnvironment import RTKEnvironment

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


@pytest.mark.integration
def test_dao_create():
    """ __init__() should create a DAO class instance. """
    DUT = DAO()

    assert isinstance(DUT, DAO)
    assert isinstance(DUT.RTK_SESSION, sessionmaker)


@pytest.mark.integration
def test_dao_db_connect(test_configuration):
    """ db_connect() should return False on success connecting to an SQLite database. """
    DUT = DAO()

    _database = test_configuration.RTK_BACKEND + ':///' + \
                test_configuration.RTK_PROG_INFO['database']

    assert not DUT.db_connect(_database)


@pytest.mark.integration
def test_dao_db_create_common(test_configuration):
    """ db_create_common() should return False on success. """
    DUT = DAO()
    _database = test_configuration.RTK_COM_BACKEND + ':///' + \
                '/tmp/_rtk_common_db.rtk'

    assert not DUT.db_create_common(_database, test=True)

    os.remove('/tmp/_rtk_common_db.rtk')


@pytest.mark.integration
def test_dao_db_create_common_bad_db_name(test_configuration):
    """ db_create_common() should return True on failure. """
    DUT = DAO()
    _database = (test_configuration.RTK_COM_BACKEND + ':///' +
                 'tmp/_rtk_common_db.rtk')

    assert DUT.db_create_common(_database, test=True)


@pytest.mark.integration
def test_dao_db_create_program(test_configuration):
    """ db_create_program() should return False on success. """
    DUT = DAO()
    _database = (test_configuration.RTK_BACKEND + ':///' +
                '/tmp/_rtk_program_db.rtk')

    assert not DUT.db_create_program(_database)


@pytest.mark.integration
def test_dao_db_create_program_bad_db_name(test_configuration):
    """ db_create_program() should return True on failure. """
    DUT = DAO()
    _database = (test_configuration.RTK_BACKEND + ':///' +
                 'tmp/_rtk_program_db.rtk')

    assert DUT.db_create_program(_database)


@pytest.mark.integration
def test_dao_db_add(test_configuration):
    """ db_add() should return a zero error code on success when adding a single record to the database. """
    DUT = DAO()
    _database = (test_configuration.RTK_BACKEND + ':///' +
                '/tmp/_rtk_program_db.rtk')
    DUT.db_connect(_database)

    _error_code, _msg = DUT.db_add([
            RTKRevision(),
        ], DUT.session)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")


@pytest.mark.integration
def test_dao_db_add_no_item(test_configuration):
    """ db_add() should return a 1003 error code on failure. """
    DUT = DAO()
    _database = (test_configuration.RTK_BACKEND + ':///' +
                '/tmp/_rtk_program_db.rtk')
    DUT.db_connect(_database)

    _error_code, _msg = DUT.db_add([
            None,
        ], DUT.session)

    assert _error_code == 1
    assert _msg == ("RTK ERROR: Adding one or more items to the RTK "
                    "Program database.")


@pytest.mark.integration
def test_dao_db_add_many(test_configuration):
    """ db_add() should return a zero error code on success when adding multiple records to the database. """
    DUT = DAO()
    _database = (test_configuration.RTK_BACKEND + ':///' +
                '/tmp/_rtk_program_db.rtk')
    DUT.db_connect(_database)

    _revision1 = RTKRevision()
    _revision2 = RTKRevision()
    _revision3 = RTKRevision()

    _error_code, _msg = DUT.db_add([_revision1, _revision2, _revision3],
                                              DUT.session)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")


@pytest.mark.integration
def test_dao_db_update(test_configuration):
    """ db_update() should return a zero error code on success. """
    DUT = DAO()
    _database = (test_configuration.RTK_BACKEND + ':///' +
                '/tmp/_rtk_program_db.rtk')
    DUT.db_connect(_database)

    _revision = RTKRevision()
    DUT.db_add([_revision, ], DUT.session)

    _revision.availability_logistics = 0.9959
    _revision.availability_mission = 0.9999

    _error_code, _msg = DUT.db_update(DUT.session)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_dao_db_delete(test_configuration):
    """ db_delete() should return a zero error code on success. """
    DUT = DAO()
    _database = (test_configuration.RTK_BACKEND + ':///' +
                '/tmp/_rtk_program_db.rtk')
    DUT.db_connect(_database)

    _revision = RTKRevision()
    DUT.db_add([_revision, ], DUT.session)

    _error_code, _msg = DUT.db_delete(_revision, DUT.session)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
def test_dao_db_delete_no_item(test_configuration):
    """ db_delete() should return a 1005 error code on failure. """
    DUT = DAO()
    _database = (test_configuration.RTK_BACKEND + ':///' +
                '/tmp/_rtk_program_db.rtk')
    DUT.db_connect(_database)

    _error_code, _msg = DUT.db_delete(None, DUT.session)

    assert _error_code == 1
    assert _msg == ("RTK ERROR: Deleting an item from the RTK Program "
                    "database.")
