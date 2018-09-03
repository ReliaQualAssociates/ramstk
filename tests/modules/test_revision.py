#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.test_revision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Revision algorithms and models."""

from treelib import Tree

import pytest

from rtk.modules.revision import dtmRevision, dtcRevision
from rtk.dao import DAO
from rtk.dao import RAMSTKRevision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'revision_id': 1,
    'availability_logistics': 0.9986,
    'availability_mission': 0.99934,
    'cost': 12532.15,
    'cost_per_failure': 0.0000352,
    'cost_per_hour': 1.2532,
    'hazard_rate_active': 0.0,
    'hazard_rate_dormant': 0.0,
    'hazard_rate_logistics': 0.0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_software': 0.0,
    'mmt': 0.0,
    'mcmt': 0.0,
    'mpmt': 0.0,
    'mtbf_logistics': 0.0,
    'mtbf_mission': 0.0,
    'mttr': 0.0,
    'name': 'Original Revision',
    'reliability_logistics': 0.99986,
    'reliability_mission': 0.99992,
    'remarks': 'This is the original revision.',
    'n_parts': 128,
    'revision_code': 'Rev. -',
    'program_time': 2562,
    'program_time_sd': 26.83,
    'program_cost': 26492.83,
    'program_cost_sd': 15.62
}


@pytest.mark.integration
def test_create_data_model(test_dao):
    """ __init__() should return a Revision data model. """
    DUT = dtmRevision(test_dao)

    assert isinstance(DUT, dtmRevision)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)


@pytest.mark.integration
def test_do_select_all(test_dao):
    """ do_select_all() should return a Tree() object populated with RAMSTKRevision instances on success. """
    DUT = dtmRevision(test_dao)
    _tree = DUT.do_select_all()

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RAMSTKRevision)


@pytest.mark.integration
def test_do_select(test_dao):
    """  do_select() should return an instance of the RAMSTKRevision data model on success. """
    DUT = dtmRevision(test_dao)
    DUT.do_select_all()

    _revision = DUT.do_select(1)

    assert isinstance(_revision, RAMSTKRevision)
    assert _revision.revision_id == 1
    assert _revision.availability_logistics == 1.0


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """ do_select() should return None when a non-existent Revision ID is requested. """
    DUT = dtmRevision(test_dao)
    DUT.do_select_all()

    _revision = DUT.do_select(100)

    assert _revision is None


@pytest.mark.integration
def test_do_insert(test_dao):
    """ do_insert() should return False on success. """
    DUT = dtmRevision(test_dao)
    DUT.do_select_all()

    _error_code, _msg = DUT.do_insert()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Adding one or more items to the RAMSTK "
                    "Program database.")
    assert DUT.last_id == 2


@pytest.mark.integration
def test_do_delete(test_dao):
    """ do_delete() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.do_select_all()
    DUT.do_insert()

    _error_code, _msg = DUT.do_delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                    "database.")


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """ do_delete() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmRevision(test_dao)
    DUT.do_select_all()

    _error_code, _msg = DUT.do_delete(300)

    assert _error_code == 2005
    assert _msg == ("  RAMSTK ERROR: Attempted to delete non-existent Revision "
                    "ID 300.")


@pytest.mark.integration
def test_do_update(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.do_select_all()

    _revision = DUT.tree.get_node(1).data
    _revision.availability_logistics = 0.9832

    _error_code, _msg = DUT.do_update(1)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating the RAMSTK Program database.")


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmRevision(test_dao)
    DUT.do_select_all()

    _error_code, _msg = DUT.do_update(100)

    assert _error_code == 2006
    assert _msg == ("RAMSTK ERROR: Attempted to save non-existent Revision ID "
                    "100.")


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.do_select_all()

    _error_code, _msg = DUT.do_update_all()

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating all Revisions.")


@pytest.mark.integration
def test_create_data_controller(test_dao, test_configuration):
    """ __init__() should return a Revision Data Controller. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcRevision)
    assert isinstance(DUT._dtm_data_model, dtmRevision)


@pytest.mark.integration
def test_request_do_select_all(test_dao, test_configuration):
    """ request_do_select_all() should return a Tree of RAMSTKRevision models. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    _tree = DUT.request_do_select_all()

    assert isinstance(_tree.get_node(1).data, RAMSTKRevision)


@pytest.mark.integration
def test_request_do_select(test_dao, test_configuration):
    """ request_do_select() should return an RAMSTKRevision model. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    _revision = DUT.request_do_select(1)

    assert isinstance(_revision, RAMSTKRevision)


@pytest.mark.integration
def test_request_non_existent_id(test_dao, test_configuration):
    """ request_do_select() should return None when requesting a Revision that doesn't exist. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    _revision = DUT.request_do_select(100)

    assert _revision is None


@pytest.mark.integration
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['revision_code'] == ''


@pytest.mark.integration
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    _error_code, _msg = DUT.request_set_attributes(1, ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKRevision 1 attributes.")


@pytest.mark.integration
def test_request_last_id(test_dao, test_configuration):
    """ request_last_id() should return the last Revision ID used in the RAMSTK Program database. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    _last_id = DUT.request_last_id()

    assert _last_id == 2


@pytest.mark.integration
def test_request_do_insert(test_dao, test_configuration):
    """ request_do_insert() should return False on success."""
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    assert not DUT.request_do_insert()

    DUT.request_do_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_do_delete(test_dao, test_configuration):
    """ request_do_delete() should return False on success."""
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()
    DUT.request_do_insert()

    assert not DUT.request_do_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_do_delete_non_existent_id(test_dao, test_configuration):
    """ request_do_delete() should return True when attempting to delete a non-existent Revision."""
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    assert DUT.request_do_delete(100)


@pytest.mark.integration
def test_request_do_update(test_dao, test_configuration):
    """ request_do_update() should return False on success. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    assert not DUT.request_do_update(DUT.request_last_id())


@pytest.mark.integration
def test_request_do_update_non_existent_id(test_dao, test_configuration):
    """ request_do_update() should return True when attempting to save a non-existent Revision. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    assert DUT.request_do_update(100)


@pytest.mark.integration
def test_request_do_update_all(test_dao, test_configuration):
    """ request_do_update_all() should return False on success. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_do_select_all()

    assert not DUT.request_do_update_all()
