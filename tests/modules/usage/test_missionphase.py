#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.usage.test_missionphase.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing the Mission Phase class."""

from treelib import Tree

import pytest

from rtk.modules.usage import dtmMissionPhase
from rtk.dao import DAO
from rtk.dao import RAMSTKMissionPhase

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return a Mission Phase data model. """
    DUT = dtmMissionPhase(test_dao)

    assert isinstance(DUT, dtmMissionPhase)
    assert DUT.last_id is None
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKMissionPhase instances on success. """
    DUT = dtmMissionPhase(test_dao)

    _tree = DUT.do_select_all(mission_id=1)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKMissionPhase)


@pytest.mark.integration
def test_do_select_all_non_existent_id(test_dao):
    """ do_select_all() should return an empty Tree() when passed a Mission ID that doesn't exist. """
    DUT = dtmMissionPhase(test_dao)

    _tree = DUT.do_select_all(mission_id=100)

    assert isinstance(_tree, Tree)
    assert len(_tree.all_nodes()) == 1


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKMissionPhase data model on success. """
    DUT = dtmMissionPhase(test_dao)
    DUT.do_select_all(mission_id=1)

    _phase = DUT.do_select(1)

    assert isinstance(_phase, RAMSTKMissionPhase)
    assert _phase.phase_id == 1
    assert _phase.description == 'Test Mission Phase 1'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when passed a Phase ID that doesn't exist. """
    DUT = dtmMissionPhase(test_dao)
    DUT.do_select_all(mission_id=1)

    assert DUT.do_select(100) is None


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return False on success. """
    DUT = dtmMissionPhase(test_dao)
    DUT.do_select_all(mission_id=1)

    _error_code, _msg = DUT.do_insert(mission_id=1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program '
                    'database.')
    assert DUT.last_id == 2


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return False on success. """
    DUT = dtmMissionPhase(test_dao)
    DUT.do_select_all(mission_id=1)

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Deleting an item from the RAMSTK Program '
                    'database.')


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Phase ID that doesn't exist. """
    DUT = dtmMissionPhase(test_dao)
    DUT.do_select_all(mission_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ('  RAMSTK ERROR: Attempted to delete non-existent Mission '
                    'Phase ID 300.')


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmMissionPhase(test_dao)
    DUT.do_select_all(mission_id=1)

    _phase = DUT.do_select(1)
    _phase.description = 'Test Mission Phase 1'

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Mission Phase ID that doesn't exist. """
    DUT = dtmMissionPhase(test_dao)
    DUT.do_select_all(mission_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == ('RAMSTK ERROR: Attempted to save non-existent Mission Phase '
                    'ID 100.')


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmMissionPhase(test_dao)
    DUT.do_select_all(mission_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all records in the usage profile "
                    "mission phase table.")
