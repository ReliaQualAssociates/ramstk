# -*- coding: utf-8 -*-
#
#       tests.data.storage.programdb.test_ramstkreliability.py is part of The
#       RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKReliability module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKReliability

ATTRIBUTES = {
    'add_adj_factor': 0.0,
    'availability_logistics': 1.0,
    'availability_mission': 1.0,
    'avail_log_variance': 0.0,
    'avail_mis_variance': 0.0,
    'failure_distribution_id': 0,
    'hazard_rate_active': 0.0,
    'hazard_rate_dormant': 0.0,
    'hazard_rate_logistics': 0.0,
    'hazard_rate_method_id': 0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_model': '',
    'hazard_rate_percent': 0.0,
    'hazard_rate_software': 0.0,
    'hazard_rate_specified': 0.0,
    'hazard_rate_type_id': 0,
    'hr_active_variance': 0.0,
    'hr_logistics_variance': 0.0,
    'hr_dormant_variance': 0.0,
    'hr_mission_variance': 0.0,
    'hr_specified_variance': 0.0,
    'lambda_b': 0.0,
    'location_parameter': 0.0,
    'mtbf_logistics': 0.0,
    'mtbf_mission': 0.0,
    'mtbf_specified': 0.0,
    'mtbf_logistics_variance': 0.0,
    'mtbf_mission_variance': 0.0,
    'mtbf_specified_variance': 0.0,
    'mult_adj_factor': 1.0,
    'quality_id': 0,
    'reliability_mission': 1.0,
    'reliability_goal_measure_id': 0,
    'reliability_goal': 0.0,
    'reliability_logistics': 1.0,
    'reliability_log_variance': 0.0,
    'reliability_miss_variance': 0.0,
    'scale_parameter': 0.0,
    'shape_parameter': 0.0,
    'survival_analysis_id': 0
}


@pytest.mark.integration
def test_ramstkreliability_create(test_dao):
    """__init__() should create an RAMSTKReliability model."""
    DUT = test_dao.session.query(RAMSTKReliability).first()

    assert isinstance(DUT, RAMSTKReliability)

    # Verify class attributes are properly initialized.  Commented attribute
    # values vary depending on whether this test file is run stand-alone or as
    # a result of python setup.py test.
    assert DUT.__tablename__ == 'ramstk_reliability'
    assert DUT.hardware_id == 1
    assert DUT.add_adj_factor == 0.0
    assert DUT.availability_logistics == 1.0
    assert DUT.availability_mission == 1.0
    assert DUT.avail_log_variance == 0.0
    assert DUT.avail_mis_variance == 0.0
    assert DUT.failure_distribution_id == 0
    # assert DUT.hazard_rate_active == 0.0
    assert DUT.hazard_rate_dormant == 0.0
    # assert DUT.hazard_rate_logistics == 0.0
    assert DUT.hazard_rate_method_id == 0
    # assert DUT.hazard_rate_mission == 0.0
    assert DUT.hazard_rate_model == ''
    assert DUT.hazard_rate_percent == 0.0
    assert DUT.hazard_rate_software == 0.0
    assert DUT.hazard_rate_specified == 0.0
    # assert DUT.hazard_rate_type_id == 0
    # assert DUT.hr_active_variance == 0.0
    assert DUT.hr_dormant_variance == 0.0
    # assert DUT.hr_logistics_variance == 0.0
    # assert DUT.hr_mission_variance == 0.0
    # assert DUT.hr_specified_variance == 0.0
    assert DUT.location_parameter == 0.0
    # assert DUT.mtbf_logistics == 0.0
    # assert DUT.mtbf_mission == 0.0
    assert DUT.mtbf_specified == 0.0
    # assert DUT.mtbf_logistics_variance == 0.0
    # assert DUT.mtbf_mission_variance == 0.0
    # assert DUT.mtbf_specified_variance == 0.0
    assert DUT.mult_adj_factor == 1.0
    assert DUT.quality_id == 0
    #assert DUT.reliability_goal == 0.0
    assert DUT.reliability_goal_measure_id == 0
    # assert DUT.reliability_logistics == 1.0
    # assert DUT.reliability_mission == 1.0
    # assert DUT.reliability_log_variance == 0.0
    # assert DUT.reliability_miss_variance == 0.0
    assert DUT.scale_parameter == 0.0
    assert DUT.shape_parameter == 0.0
    assert DUT.survival_analysis_id == 0
    assert DUT.lambda_b == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """get_attributes() should return a dict of attribute key:value pairs."""
    DUT = test_dao.session.query(RAMSTKReliability).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)
    assert _attributes['hardware_id'] == 1
    assert _attributes['add_adj_factor'] == 0.0
    assert _attributes['availability_logistics'] == 1.0
    assert _attributes['availability_mission'] == 1.0
    assert _attributes['avail_log_variance'] == 0.0
    assert _attributes['avail_mis_variance'] == 0.0
    assert _attributes['failure_distribution_id'] == 0
    # assert _attributes['hazard_rate_active'] == 0.0
    assert _attributes['hazard_rate_dormant'] == 0.0
    # assert _attributes['hazard_rate_logistics'] == 0.0
    assert _attributes['hazard_rate_method_id'] == 0
    # assert _attributes['hazard_rate_mission'] == 0.0
    assert _attributes['hazard_rate_model'] == ''
    assert _attributes['hazard_rate_percent'] == 0.0
    assert _attributes['hazard_rate_software'] == 0.0
    assert _attributes['hazard_rate_specified'] == 0.0
    # assert _attributes['hazard_rate_type_id'] == 0
    # assert _attributes['hr_active_variance'] == 0.0
    assert _attributes['hr_dormant_variance'] == 0.0
    # assert _attributes['hr_logistics_variance'] == 0.0
    # assert _attributes['hr_mission_variance'] == 0.0
    # assert _attributes['hr_specified_variance'] == 0.0
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['location_parameter'] == 0.0
    # assert _attributes['mtbf_logistics'] == 0.0
    # assert _attributes['mtbf_mission'] == 0.0
    assert _attributes['mtbf_specified'] == 0.0
    # assert _attributes['mtbf_logistics_variance'] == 0.0
    # assert _attributes['mtbf_mission_variance'] == 0.0
    # assert _attributes['mtbf_specified_variance'] == 0.0
    assert _attributes['mult_adj_factor'] == 1.0
    assert _attributes['quality_id'] == 0
    #assert _attributes['reliability_goal'] == 0.0
    assert _attributes['reliability_goal_measure_id'] == 0
    # assert _attributes['reliability_logistics'] == 1.0
    # assert _attributes['reliability_mission'] == 1.0
    # assert _attributes['reliability_log_variance'] == 0.0
    # assert _attributes['reliability_miss_variance'] == 0.0
    assert _attributes['scale_parameter'] == 0.0
    assert _attributes['shape_parameter'] == 0.0
    assert _attributes['survival_analysis_id'] == 0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """set_attributes() should return a zero error code on success."""
    DUT = test_dao.session.query(RAMSTKReliability).first()

    assert DUT.set_attributes(ATTRIBUTES) is None


@pytest.mark.integration
def test_set_attributes_none_value(test_dao):
    """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
    DUT = test_dao.session.query(RAMSTKReliability).first()

    ATTRIBUTES['add_adj_factor'] = None

    assert DUT.set_attributes(ATTRIBUTES) is None
    assert DUT.get_attributes()['add_adj_factor'] == 0.0


@pytest.mark.integration
def test_set_attributes_unknown_attributes(test_dao):
    """set_attributes() should raise an AttributeError when passed an unknown attribute."""
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKReliability).first()

    with pytest.raises(AttributeError):
        DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
