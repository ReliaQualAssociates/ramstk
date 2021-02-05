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
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import dmRevision
from ramstk.db.program import do_create_program_db, do_make_programdb_tables
from ramstk.models.programdb import RAMSTKRevision


@pytest.mark.unit
@pytest.mark.usefixtures('test_simple_program_database')
def test_create_program_db_tables(test_simple_program_database):
    """do_make_programdb_tables() should return None when successfully creating
    the tables in the RAMSTK common database."""
    assert do_make_programdb_tables(
        test_simple_program_database.engine) is None
    assert test_simple_program_database.do_insert(RAMSTKRevision()) is None
    assert test_simple_program_database.get_last_id('ramstk_revision',
                                                    'fld_revision_id') == 1


@pytest.mark.unit
@pytest.mark.usefixtures('test_simple_program_database')
def test_do_create_program_db(test_simple_program_database):
    """do_create_program_db() should return None when successfully creating a
    RAMSTK common database."""
    assert do_create_program_db(test_simple_program_database.engine,
                                test_simple_program_database.session) is None

    _record = test_simple_program_database.session.query(
        RAMSTKRevision).filter(RAMSTKRevision.revision_id == 1).first()
    assert _record.availability_logistics == 1.0
    assert _record.name == ''
    assert _record.remarks == ''


@pytest.mark.usefixtures('test_program_dao')
class TestUpdateMethods:
    """Class to test data controller update methods using actual database."""
    def on_succeed_update_revision(self, tree):
        assert isinstance(tree, Tree)
        print("\033[36m\nsucceed_update_revision topic was broadcast")

    def on_fail_update_revision_wrong_data_type(self, error_message):
        assert error_message == (
            'do_update: The value for one or more attributes for revision ID '
            '1 was the wrong type.')
        print("\033[35m\nfail_update_revision topic was broadcast")

    @pytest.mark.integration
    def test_do_update_data_manager(self, test_program_dao):
        """do_update() should send the succeed_update_revision message on
        success."""
        pub.subscribe(self.on_succeed_update_revision,
                      'succeed_update_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        _revision = DUT.do_select(1, table='revision')
        _revision.name = 'Test Revision'
        DUT.do_update(1)

        DUT.do_select_all()
        _revision = DUT.do_select(1, table='revision')

        assert _revision.name == 'Test Revision'

        pub.unsubscribe(self.on_succeed_update_revision,
                        'succeed_update_revision')

    @pytest.mark.integration
    def test_do_update_wrong_data_type(self, test_program_dao):
        """do_update() should send the fail_update_revision message when passed
        a revision ID that that has a wrong data type for one or more
        attributes."""
        pub.subscribe(self.on_fail_update_revision_wrong_data_type,
                      'fail_update_revision')

        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()
        DUT.tree.get_node(1).data['revision'].cost = None

        DUT.do_update(1)

        pub.unsubscribe(self.on_fail_update_revision_wrong_data_type,
                        'fail_update_revision')

    @pytest.mark.integration
    def test_do_update_root_node(self, test_program_dao):
        """do_update() should end the fail_update_revision message when passed
        a revision ID that has no data package."""
        DUT = dmRevision()
        DUT.do_connect(test_program_dao)
        DUT.do_select_all()

        DUT.do_update(0)
