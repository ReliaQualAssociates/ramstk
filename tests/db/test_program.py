# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.db.test_program.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for program database methods and operations."""

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.db.program import do_create_program_db, do_make_programdb_tables
from ramstk.models.programdb import RAMSTKRevision

TEST_PROGRAM_DB = BaseDatabase()
TEST_PROGRAM_DB.do_connect('sqlite:///:memory:')


def test_create_program_db_tables():
    """do_make_programdb_tables() should return None when successfully creating the tables in the RAMSTK common database."""
    assert do_make_programdb_tables(TEST_PROGRAM_DB.engine) is None
    assert TEST_PROGRAM_DB.do_insert(RAMSTKRevision()) is None
    assert TEST_PROGRAM_DB.get_last_id('ramstk_revision',
                                       'fld_revision_id') == 1


def test_do_create_program_db():
    """do_create_program_db() should return None when successfully creating a RAMSTK common database."""
    TEST_PROGRAM_DB.do_disconnect()
    TEST_PROGRAM_DB.do_connect('sqlite:///:memory:')

    assert do_create_program_db(TEST_PROGRAM_DB.engine,
                                TEST_PROGRAM_DB.session) is None

    _record = TEST_PROGRAM_DB.session.query(RAMSTKRevision).filter(
        RAMSTKRevision.revision_id == 1).first()
    assert _record.availability_logistics == 1.0
    assert _record.name == ''
    assert _record.remarks == ''
