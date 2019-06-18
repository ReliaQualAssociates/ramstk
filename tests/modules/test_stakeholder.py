# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.modules.test_stakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Stakeholder module algorithms and models."""

# Third Party Imports
import pytest
from treelib import Tree

# RAMSTK Package Imports
from ramstk.dao import DAO
from ramstk.dao.programdb import RAMSTKStakeholder
from ramstk.modules.stakeholder import dtcStakeholder, dtmStakeholder

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Doyle "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'stakeholder_id': 1,
    'customer_rank': 2,
    'description': b'Stakeholder Input',
    'group': '',
    'improvement': 0.0,
    'overall_weight': 0.0,
    'planned_rank': 4,
    'priority': 2,
    'requirement_id': 1,
    'stakeholder': '',
    'user_float_1': 1.0,
    'user_float_2': 2.0,
    'user_float_3': 3.0,
    'user_float_4': 4.0,
    'user_float_5': 5.0,
}


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return a Stakeholder model. """
    DUT = dtmStakeholder(test_dao, test=True)

    assert isinstance(DUT, dtmStakeholder)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ vselect_all() should return a Tree() object populated with RAMSTKStakeholder instances on success. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.tree.get_node(1).data, RAMSTKStakeholder)


@pytest.mark.integration
def test_do_select(test_dao):
    """ do_select() should return an instance of the RAMSTKStakeholder data model on success. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _stakeholder = DUT.do_select(1)

    assert isinstance(_stakeholder, RAMSTKStakeholder)
    assert _stakeholder.stakeholder_id == 1
    assert _stakeholder.description == b'Test Stakeholder Input'


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Stakeholder ID is requested. """
    DUT = dtmStakeholder(test_dao, test=True)
    _stakeholder = DUT.do_select(100)

    assert _stakeholder is None


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return False on success. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_insert(revision_id=1)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program '
        'database.'
    )
    assert DUT.last_id == 2


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(2)

    assert _error_code == 0
    assert _msg == (
        'RAMSTK SUCCESS: Deleting an item from the RAMSTK Program '
        'database.'
    )


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Stakeholder ID that doesn't exist. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == (
        '  RAMSTK ERROR: Attempted to delete non-existent '
        'Stakeholder ID 300.'
    )


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _stakeholder = DUT.do_select(1)
    _stakeholder.description = 'Be very reliable.'.encode('utf-8')

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Updating the RAMSTK Program database.')


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Stakeholder ID that doesn't exist. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == (
        'RAMSTK ERROR: Attempted to save non-existent Stakeholder ID '
        '100.'
    )


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating all records in the stakeholder "
        "table."
    )


@pytest.mark.integration
def test_do_calculate_weight(test_dao):
    """ do_calculate() returns False on success and calculated values are correct. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _stakeholder = DUT.do_select(1)

    _stakeholder.planned_rank = 4
    _stakeholder.customer_rank = 2
    _stakeholder.priority = 2
    _stakeholder.user_float_1 = 1.0
    _stakeholder.user_float_2 = 2.0
    _stakeholder.user_float_3 = 3.0
    _stakeholder.user_float_4 = 4.0
    _stakeholder.user_float_5 = 5.0

    assert not DUT.do_calculate(1)
    assert _stakeholder.improvement == 1.4
    assert _stakeholder.overall_weight == pytest.approx(336.0)


@pytest.mark.integration
def test_do_calculate_all(test_dao):
    """ do_calculate_all() returns False on success. """
    DUT = dtmStakeholder(test_dao, test=True)
    DUT.do_select_all(revision_id=1)
    _stakeholder = DUT.do_select(1)

    _stakeholder.planned_rank = 4
    _stakeholder.customer_rank = 2
    _stakeholder.priority = 1
    _stakeholder.user_float_1 = 1.0
    _stakeholder.user_float_2 = 2.0
    _stakeholder.user_float_3 = 3.0
    _stakeholder.user_float_4 = 4.0
    _stakeholder.user_float_5 = 5.0

    assert not DUT.do_calculate_all()
    assert _stakeholder.improvement == 1.4
    assert _stakeholder.overall_weight == pytest.approx(168.0)


@pytest.mark.integration
def test_data_controller_create(test_dao, test_configuration):
    """ __init__() should create a Stakeholder data controller. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcStakeholder)
    assert isinstance(DUT._dtm_data_model, dtmStakeholder)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RAMSTKStakeholder models. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert isinstance(
        DUT._dtm_data_model.tree.get_node(1).data, RAMSTKStakeholder,
    )


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_select() should return an RAMSTKStakeholder model. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    _stakeholder = DUT.request_do_select(1)

    assert isinstance(_stakeholder, RAMSTKStakeholder)


@pytest.mark.integration
def test_request_do_select_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting a Stakeholder that doesn't exist. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    _stakeholder = DUT.request_do_select(100)

    assert _stakeholder is None


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_insert() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(revision_id=1)


@pytest.mark.integration
def test_request_do_insert_wrong_revision(test_dao, test_configuration):
    """ request_insert() should return True on failure. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_insert(revision_id=2)


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Stakeholder. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update(1)


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent Stakeholder. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    assert not DUT.request_do_update_all()


@pytest.mark.integration
def test_request_do_calculate(test_dao, test_configuration):
    """ request_do_calculate() should return False on success. """
    DUT = dtcStakeholder(test_dao, test_configuration, test=True)
    DUT.request_do_select_all(ATTRIBUTES)

    _stakeholder = DUT.request_do_select(1)
    _stakeholder.planned_rank = 4
    _stakeholder.customer_rank = 2
    _stakeholder.priority = 2
    _stakeholder.user_float_1 = 1.0
    _stakeholder.user_float_2 = 2.0
    _stakeholder.user_float_3 = 3.0
    _stakeholder.user_float_4 = 4.0
    _stakeholder.user_float_5 = 5.0

    assert not DUT.request_do_calculate(1)
    assert _stakeholder.improvement == 1.4
    assert _stakeholder.overall_weight == pytest.approx(336.0)
