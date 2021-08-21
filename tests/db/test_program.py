# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.db.test_program.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for program database methods and operations."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.db.program import do_create_program_db, do_make_programdb_tables
from ramstk.models import RAMSTKRevisionRecord


@pytest.mark.unit
@pytest.mark.usefixtures("test_simple_program_database")
def test_create_program_db_tables(test_simple_program_database):
    """do_make_programdb_tables() should return None when successfully creating
    the tables in the RAMSTK common database."""
    assert do_make_programdb_tables(test_simple_program_database.engine) is None
    assert test_simple_program_database.do_insert(RAMSTKRevisionRecord()) is None
    assert (
        test_simple_program_database.get_last_id("ramstk_revision", "fld_revision_id")
        == 1
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_simple_program_database")
def test_do_create_program_db(test_simple_program_database):
    """do_create_program_db() should return None when successfully creating a
    RAMSTK common database."""
    assert (
        do_create_program_db(
            test_simple_program_database.engine, test_simple_program_database.session
        )
        is None
    )

    _record = (
        test_simple_program_database.session.query(RAMSTKRevisionRecord)
        .filter(RAMSTKRevisionRecord.revision_id == 1)
        .first()
    )
    assert _record.availability_logistics == 1.0
    assert _record.name == ""
    assert _record.remarks == ""
