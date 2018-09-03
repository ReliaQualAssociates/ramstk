#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkreliability.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKReliability module algorithms and models. """

import pytest

from rtk.dao.programdb.RAMSTKReliability import RAMSTKReliability

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'hazard_rate_percent': 0.0,
    'reliability_mission': 1.0,
    'reliability_goal_measure_id': 0,
    'hazard_rate_specified': 0.0,
    'hazard_rate_active': 0.0,
    'hr_mission_variance': 0.0,
    'reliability_goal': 0.0,
    'mtbf_log_variance': 0.0,
    'quality_id': 0,
    'scale_parameter': 0.0,
    'add_adj_factor': 0.0,
    'availability_mission': 1.0,
    'mtbf_spec_variance': 0.0,
    'mtbf_miss_variance': 0.0,
    'lambda_b': 0.0,
    'hr_specified_variance': 0.0,
    'avail_log_variance': 0.0,
    'hazard_rate_type_id': 0,
    'mtbf_mission': 0.0,
    'failure_distribution_id': 0,
    'reliability_miss_variance': 0.0,
    'avail_mis_variance': 0.0,
    'hazard_rate_method_id': 0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_software': 0.0,
    'mtbf_specified': 0.0,
    'hr_logistics_variance': 0.0,
    'shape_parameter': 0.0,
    'hardware_id': 1,
    'hr_dormant_variance': 0.0,
    'location_parameter': 0.0,
    'survival_analysis_id': 0,
    'hazard_rate_logistics': 0.0,
    'reliability_logistics': 1.0,
    'hazard_rate_model': '',
    'reliability_log_variance': 0.0,
    'hr_active_variance': 0.0,
    'availability_logistics': 1.0,
    'hazard_rate_dormant': 0.0,
    'mtbf_logistics': 0.0,
    'mult_adj_factor': 1.0
}


@pytest.mark.integration
def test_rtkreliability_create(test_dao):
    """ __init__() should create an RAMSTKReliability model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKReliability).first()

    assert isinstance(DUT, RAMSTKReliability)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_reliability'
    assert DUT.hardware_id == 1
    assert DUT.add_adj_factor == 0.0
    assert DUT.availability_logistics == 1.0
    assert DUT.availability_mission == 1.0
    assert DUT.avail_log_variance == 0.0
    assert DUT.avail_mis_variance == 0.0
    assert DUT.failure_distribution_id == 0
    assert DUT.hazard_rate_active == 0.0
    assert DUT.hazard_rate_dormant == 0.0
    assert DUT.hazard_rate_logistics == 0.0
    assert DUT.hazard_rate_method_id == 0
    assert DUT.hazard_rate_mission == 0.0
    assert DUT.hazard_rate_model == ''
    assert DUT.hazard_rate_percent == 0.0
    assert DUT.hazard_rate_software == 0.0
    assert DUT.hazard_rate_specified == 0.0
    assert DUT.hazard_rate_type_id == 0
    assert DUT.hr_active_variance == 0.0
    assert DUT.hr_dormant_variance == 0.0
    assert DUT.hr_logistics_variance == 0.0
    assert DUT.hr_mission_variance == 0.0
    assert DUT.hr_specified_variance == 0.0
    assert DUT.location_parameter == 0.0
    assert DUT.mtbf_logistics == 0.0
    assert DUT.mtbf_mission == 0.0
    assert DUT.mtbf_specified == 0.0
    assert DUT.mtbf_log_variance == 0.0
    assert DUT.mtbf_miss_variance == 0.0
    assert DUT.mtbf_spec_variance == 0.0
    assert DUT.mult_adj_factor == 1.0
    assert DUT.quality_id == 0
    assert DUT.reliability_goal == 0.0
    assert DUT.reliability_goal_measure_id == 0
    assert DUT.reliability_logistics == 1.0
    assert DUT.reliability_mission == 1.0
    assert DUT.reliability_log_variance == 0.0
    assert DUT.reliability_miss_variance == 0.0
    assert DUT.scale_parameter == 0.0
    assert DUT.shape_parameter == 0.0
    assert DUT.survival_analysis_id == 0
    assert DUT.lambda_b == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of attribute key:value pairs. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKReliability).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKReliability).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKReliability {0:d} "
                    "attributes.".format(DUT.hardware_id))


@pytest.mark.integration
def test_set_attributes_missing_key(test_dao):
    """ set_attributes() should return a 40 error code when passed a dict with a missing key. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKReliability).first()

    ATTRIBUTES.pop('shape_parameter')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'shape_parameter' in "
                    "attribute dictionary passed to "
                    "RAMSTKReliability.set_attributes().")

    ATTRIBUTES['shape_parameter'] = 0.0
