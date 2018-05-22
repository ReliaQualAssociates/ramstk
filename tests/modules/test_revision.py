#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.modules.test_revision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Test class for testing Revision algorithms and models."""

from treelib import Tree

import pytest

from rtk.modules.revision import dtmRevision, dtcRevision
from rtk.dao import DAO
from rtk.dao import RTKRevision

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
def test_select_all(test_dao):
    """ select_all() should return a Tree() object populated with RTKRevision instances on success. """
    DUT = dtmRevision(test_dao)
    _tree = DUT.select_all(None)

    assert isinstance(_tree, Tree)
    assert isinstance(_tree.get_node(1).data, RTKRevision)


@pytest.mark.integration
def test_select(test_dao):
    """  select() should return an instance of the RTKRevision data model on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(1)

    assert isinstance(_revision, RTKRevision)
    assert _revision.revision_id == 1
    assert _revision.availability_logistics == 1.0


@pytest.mark.integration
def test_select_non_existent_id(test_dao):
    """ select() should return None when a non-existent Revision ID is requested. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(100)

    assert _revision is None


@pytest.mark.integration
def test_insert(test_dao):
    """ insert() should return False on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _error_code, _msg = DUT.insert()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Adding one or more items to the RTK "
                    "Program database.")
    assert DUT.last_id == 2


@pytest.mark.integration
def test_delete(test_dao):
    """ delete() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)
    DUT.insert()

    _error_code, _msg = DUT.delete(DUT.last_id)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Deleting an item from the RTK Program "
                    "database.")


@pytest.mark.integration
def test_delete_non_existent_id(test_dao):
    """ delete() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _error_code, _msg = DUT.delete(300)

    assert _error_code == 2005
    assert _msg == ("  RTK ERROR: Attempted to delete non-existent Revision "
                    "ID 300.")


@pytest.mark.integration
def test_update(test_dao):
    """ update() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.tree.get_node(1).data
    _revision.availability_logistics = 0.9832

    _error_code, _msg = DUT.update(1)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_update_non_existent_id(test_dao):
    """ update() should return a non-zero error code when passed a Revision ID that doesn't exist. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _error_code, _msg = DUT.update(100)

    assert _error_code == 2006
    assert _msg == ("RTK ERROR: Attempted to save non-existent Revision ID "
                    "100.")


@pytest.mark.integration
def test_update_all(test_dao):
    """ update_all() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _error_code, _msg = DUT.update_all()

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating the RTK Program database.")


@pytest.mark.integration
def test_calculate_hazard_rate(test_dao):
    """ calculate_hazard_rate() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(1)
    _revision.hazard_rate_active = 0.00000151
    _revision.hazard_rate_dormant = 0.0000000152
    _revision.hazard_rate_software = 0.0000003
    _revision.hazard_rate_mission = 0.000002

    _error_code, _msg = DUT.calculate_hazard_rate(1)
    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating hazard rates for Revision "
                    "ID 1.")
    assert _revision.hazard_rate_logistics == pytest.approx(1.8252e-06)


@pytest.mark.integration
def test_calculate_mtbf(test_dao):
    """ calculate_mtbf() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(1)
    _revision.hazard_rate_active = 0.00000151
    _revision.hazard_rate_dormant = 0.0000000152
    _revision.hazard_rate_software = 0.0000003
    _revision.hazard_rate_mission = 0.000002
    _revision.calculate_hazard_rate()

    _error_code, _msg = DUT.calculate_mtbf(1)
    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating MTBFs for Revision ID 1.")
    assert _revision.mtbf_logistics == pytest.approx(547885.1632698)
    assert _revision.mtbf_mission == pytest.approx(500000.0)


@pytest.mark.integration
def test_calculate_reliability_divide_by_zero(test_dao):
    """ calculate_reliability() should return a non-zero error code when attempting to divide by zero. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(1)
    _revision.hazard_rate_active = 0.00000151
    _revision.hazard_rate_dormant = 0.0000000152
    _revision.hazard_rate_software = 0.0000003
    _revision.hazard_rate_mission = 0.000002

    _error_code, _msg = DUT.calculate_reliability(1, 100.0, 0.0)
    assert _error_code == 102
    assert _msg == ("RTK ERROR: Zero Division Error when calculating the "
                    "mission reliability for Revision ID 1.  Hazard rate "
                    "multiplier: 0.000000.")


@pytest.mark.integration
def test_calculate_availability(test_dao):
    """ calculate_availability() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(1)
    _revision.mpmt = 0.5
    _revision.mcmt = 1.2
    _revision.mttr = 5.8
    _revision.mmt = 0.85
    _revision.mtbf_logistics = 547885.1632698
    _revision.mtbf_mission = 500000.0

    _error_code, _msg = DUT.calculate_availability(1)
    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating availability metrics for "
                    "Revision ID 1.")
    assert _revision.availability_logistics == pytest.approx(0.9999894)
    assert _revision.availability_mission == pytest.approx(0.9999884)


@pytest.mark.integration
def test_calculate_availability_divide_by_zero(test_dao):
    """ calculate_availability() should return a non-zero error code when attempting to divide by zero. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(1)
    _revision.mttr = 0.0
    _revision.mtbf_logistics = 547885.1632698
    _revision.mtbf_mission = 0.0

    _error_code, _msg = DUT.calculate_availability(1)
    assert _error_code == 102
    assert _msg == ("RTK ERROR: Zero Division Error when calculating the "
                    "mission availability for Revision ID 1.  Mission MTBF: "
                    "0.000000 MTTR: 0.000000.")


@pytest.mark.integration
def test_calculate_costs(test_dao):
    """ calculate_costs() should return a zero error code on success. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(1)
    _revision.cost = 1252.78
    _revision.hazard_rate_logistics = 1.0 / 547885.1632698

    _error_code, _msg = DUT.calculate_costs(1, 100.0)
    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Calculating cost metrics for Revision "
                    "ID 1.")
    assert _revision.cost_failure == pytest.approx(0.002286574)
    assert _revision.cost_hour == pytest.approx(12.5278)


@pytest.mark.integration
def test_calculate_costs_divide_by_zero(test_dao):
    """ calculate_costs() should return a non-zero error code when attempting to divide by zero. """
    DUT = dtmRevision(test_dao)
    DUT.select_all(None)

    _revision = DUT.select(1)
    _revision.cost = 1252.78
    _revision.hazard_rate_logistics = 1.0 / 547885.1632698

    _error_code, _msg = DUT.calculate_costs(1, 0.0)
    assert _error_code == 102
    assert _msg == ("RTK ERROR: Zero Division Error when calculating the cost "
                    "per mission hour for Revision ID 1.  Mission time: "
                    "0.000000.")


@pytest.mark.integration
def test_create_data_controller(test_dao, test_configuration):
    """ __init__() should return a Revision Data Controller. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)

    assert isinstance(DUT, dtcRevision)
    assert isinstance(DUT._dtm_data_model, dtmRevision)


@pytest.mark.integration
def test_request_select_all(test_dao, test_configuration):
    """ request_select_all() should return a Tree of RTKRevision models. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    _tree = DUT.request_select_all(1)

    assert isinstance(_tree.get_node(1).data, RTKRevision)


@pytest.mark.integration
def test_request_select(test_dao, test_configuration):
    """ request_select() should return an RTKRevision model. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _revision = DUT.request_select(1)

    assert isinstance(_revision, RTKRevision)


@pytest.mark.integration
def test_request_non_existent_id(test_dao, test_configuration):
    """ request_select() should return None when requesting a Revision that doesn't exist. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    _revision = DUT.request_select(100)

    assert _revision is None


@pytest.mark.integration
def test_request_get_attributes(test_dao, test_configuration):
    """ request_get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(None)

    _attributes = DUT.request_get_attributes(1)

    assert isinstance(_attributes, dict)
    assert _attributes['revision_code'] == ''


@pytest.mark.integration
def test_request_set_attributes(test_dao, test_configuration):
    """ request_set_attributes() should return a dict of {attribute name:attribute value} pairs. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(None)

    _error_code, _msg = DUT.request_set_attributes(1, ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKRevision 1 attributes.")


@pytest.mark.integration
def test_request_last_id(test_dao, test_configuration):
    """ request_last_id() should return the last Revision ID used in the RTK Program database. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(None)

    _last_id = DUT.request_last_id()

    assert _last_id == 2


@pytest.mark.integration
def test_request_insert(test_dao, test_configuration):
    """ request_insert() should return False on success."""
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_insert()

    DUT.request_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_delete(test_dao, test_configuration):
    """ request_delete() should return False on success."""
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)
    DUT.request_insert()

    assert not DUT.request_delete(DUT.request_last_id())


@pytest.mark.integration
def test_request_delete_non_existent_id(test_dao, test_configuration):
    """ request_delete() should return True when attempting to delete a non-existent Revision."""
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_delete(100)


@pytest.mark.integration
def test_request_update(test_dao, test_configuration):
    """ request_update() should return False on success. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update(DUT.request_last_id())


@pytest.mark.integration
def test_request_update_non_existent_id(test_dao, test_configuration):
    """ request_update() should return True when attempting to save a non-existent Revision. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert DUT.request_update(100)


@pytest.mark.integration
def test_request_update_all(test_dao, test_configuration):
    """ request_update_all() should return False on success. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    assert not DUT.request_update_all()


@pytest.mark.integration
def test_request_calculate_reliability(test_dao, test_configuration):
    """ request_calculate_reliability() should return False on success. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _revision = DUT._dtm_data_model.tree.get_node(1).data
    _revision.hazard_rate_active = 0.00000151
    _revision.hazard_rate_dormant = 0.0000000152
    _revision.hazard_rate_software = 0.0000003
    _revision.hazard_rate_logistics = 1.8252e-06
    _revision.hazard_rate_mission = 0.000002
    _revision.mpmt = 0.5
    _revision.mcmt = 1.2
    _revision.mttr = 5.8
    _revision.mmt = 0.85
    _revision.mtbf_logistics = 547885.1632698
    _revision.mtbf_mission = 500000.0
    _revision.cost = 1252.78

    assert not DUT.request_calculate_reliability(1, 100.0, 1.0)

    assert _revision.hazard_rate_logistics == pytest.approx(1.8252e-06)
    assert _revision.mtbf_logistics == pytest.approx(547885.1632698)
    assert _revision.mtbf_mission == pytest.approx(500000.0)
    assert _revision.reliability_logistics == pytest.approx(0.9998175)
    assert _revision.reliability_mission == pytest.approx(0.99980002)


@pytest.mark.integration
def test_request_calculate_availability(test_dao, test_configuration):
    """ request_calculate_availability() should return False on success. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _revision = DUT._dtm_data_model.tree.get_node(1).data
    _revision.hazard_rate_active = 0.00000151
    _revision.hazard_rate_dormant = 0.0000000152
    _revision.hazard_rate_software = 0.0000003
    _revision.hazard_rate_mission = 0.000002
    _revision.mpmt = 0.5
    _revision.mcmt = 1.2
    _revision.mttr = 5.8
    _revision.mmt = 0.85
    _revision.mtbf_logistics = 547885.1632698
    _revision.mtbf_mission = 500000.0
    _revision.cost = 1252.78

    assert not DUT.request_calculate_availability(1)

    assert _revision.availability_logistics == pytest.approx(0.9999894)
    assert _revision.availability_mission == pytest.approx(0.9999884)


@pytest.mark.integration
def test_request_calculate_cost(test_dao, test_configuration):
    """ request_calculate_cost() should return False on success. """
    DUT = dtcRevision(test_dao, test_configuration, test=True)
    DUT.request_select_all(1)

    _revision = DUT._dtm_data_model.tree.get_node(1).data
    _revision.hazard_rate_active = 0.00000151
    _revision.hazard_rate_dormant = 0.0000000152
    _revision.hazard_rate_software = 0.0000003
    _revision.hazard_rate_mission = 0.000002
    _revision.hazard_rate_logistics = 1.8252e-06
    _revision.mpmt = 0.5
    _revision.mcmt = 1.2
    _revision.mttr = 5.8
    _revision.mmt = 0.85
    _revision.mtbf_logistics = 547885.1632698
    _revision.mtbf_mission = 500000.0
    _revision.cost = 1252.78

    assert not DUT.request_calculate_costs(1, 100.0)

    assert _revision.cost_failure == pytest.approx(0.002286574)
    assert _revision.cost_hour == pytest.approx(12.5278)
