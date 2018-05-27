# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkrevision.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKRevision module algorithms and models."""

import pytest

from rtk.dao.programdb.RTKRevision import RTKRevision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


ATTRIBUTES = {
            'revision_id': 1,
            'availability_logistics': 1.0,
            'availability_mission': 1.0,
            'cost': 0.0,
            'cost_per_failure': 0.0,
            'cost_per_hour': 0.0,
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
            'name': 'Test Revision',
            'reliability_logistics': 1.0,
            'reliability_mission': 1.0,
            'remarks': '',
            'n_parts': 0,
            'revision_code': '',
            'program_time': 0.0,
            'program_time_sd': 0.0,
            'program_cost': 0.0,
            'program_cost_sd': 0.0
        }


@pytest.mark.integration
def test_rtkrevision_create(test_dao):
    """ __init__() should create an RTKRevision model. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    assert isinstance(DUT, RTKRevision)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_revision'
    assert DUT.revision_id == 1
    assert DUT.availability_logistics == 1.0
    assert DUT.availability_mission == 1.0
    assert DUT.cost == 0.0
    assert DUT.cost_failure == 0.0
    assert DUT.cost_hour == 0.0
    assert DUT.hazard_rate_active == 0.0
    assert DUT.hazard_rate_dormant == 0.0
    assert DUT.hazard_rate_logistics == 0.0
    assert DUT.hazard_rate_mission == 0.0
    assert DUT.hazard_rate_software == 0.0
    assert DUT.mmt == 0.0
    assert DUT.mcmt == 0.0
    assert DUT.mpmt == 0.0
    assert DUT.mtbf_logistics == 0.0
    assert DUT.mtbf_mission == 0.0
    assert DUT.mttr == 0.0
    assert DUT.name == 'Test Revision'
    assert DUT.reliability_logistics == 1.0
    assert DUT.reliability_mission == 1.0
    assert DUT.remarks == ''
    assert DUT.total_part_count == 1
    assert DUT.revision_code == ''
    assert DUT.program_time == 0.0
    assert DUT.program_time_sd == 0.0
    assert DUT.program_cost == 0.0
    assert DUT.program_cost_sd == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of {attr name:attr value} pairs. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    _values = DUT.get_attributes()

    assert _values['availability_logistics'] == ATTRIBUTES['availability_logistics']


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKRevision {0:d} "
                    "attributes.".format(DUT.revision_id))


@pytest.mark.integration
def test_set_attributes_too_few_passed(test_dao):
    """ set_attributes() should return a 40 error code when passed an attribute dict with a missing key. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    ATTRIBUTES.pop('name')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'name' in attribute "
                    "dictionary passed to RTKRevision.set_attributes().")


@pytest.mark.integration
def test_calculate_hazard_rate(test_dao):
    """ calculate_hazard_rate() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    DUT.hazard_rate_active = 0.00000151
    DUT.hazard_rate_dormant = 0.0000000152
    DUT.hazard_rate_software = 0.0000003
    DUT.hazard_rate_mission = 0.000002

    _error_code, _msg = DUT.calculate_hazard_rate()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Calculating hazard rates for Revision ID 1.')
    assert pytest.approx(DUT.hazard_rate_logistics, 1.8252e-06)


@pytest.mark.integration
def test_calculate_mtbf(test_dao):
    """ calculate_mtbf() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    DUT.hazard_rate_active = 0.00000151
    DUT.hazard_rate_dormant = 0.0000000152
    DUT.hazard_rate_software = 0.0000003
    DUT.hazard_rate_mission = 0.000002
    DUT.calculate_hazard_rate()

    _error_code, _msg = DUT.calculate_mtbf()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Calculating MTBFs for Revision ID 1.')
    assert pytest.approx(DUT.mtbf_logistics, 547885.1632698)
    assert pytest.approx(DUT.mtbf_mission, 500000.0)


@pytest.mark.integration
def test_calculate_reliability(test_dao):
    """ calculate_reliability() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    DUT.hazard_rate_active = 0.00000151
    DUT.hazard_rate_dormant = 0.0000000152
    DUT.hazard_rate_software = 0.0000003
    DUT.hazard_rate_mission = 0.000002
    DUT.calculate_hazard_rate()

    _error_code, _msg = DUT.calculate_reliability(100.0, 1.0)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Calculating reliabilities for Revision ID '
                    '1.')
    assert pytest.approx(DUT.reliability_logistics, 0.9998175)
    assert pytest.approx(DUT.reliability_mission, 0.9998000)


@pytest.mark.integration
def test_calculate_availability(test_dao):
    """ calculate_availability() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    DUT.mpmt = 0.5
    DUT.mcmt = 1.2
    DUT.mttr = 5.8
    DUT.mmt = 0.85
    DUT.mtbf_logistics = 547885.1632698
    DUT.mtbf_mission = 500000.0

    _error_code, _msg = DUT.calculate_availability()

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Calculating availability metrics for '
                    'Revision ID 1.')
    assert pytest.approx(DUT.availability_logistics, 0.9999894)
    assert pytest.approx(DUT.availability_mission, 0.9999884)


@pytest.mark.integration
def test_calculate_availability_divide_by_zero(test_dao):
    """ calculate_availability() should return a non-zero error code when attempting to divide by zero. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    DUT.mttr = 0.0
    DUT.mtbf_logistics = 547885.1632698
    DUT.mtbf_mission = 0.0

    _error_code, _msg = DUT.calculate_availability()

    assert _error_code == 102
    assert _msg == ('RTK ERROR: Zero Division Error when calculating the '
                    'mission availability for Revision ID 1.  Mission MTBF: '
                    '0.000000 MTTR: 0.000000.')


@pytest.mark.integration
def test_calculate_costs(test_dao):
    """ calculate_costs() should return a zero error code on success. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    DUT.cost = 1252.78
    DUT.hazard_rate_logistics = 1.0 / 547885.1632698

    _error_code, _msg = DUT.calculate_costs(100.0)

    assert _error_code == 0
    assert _msg == ('RTK SUCCESS: Calculating cost metrics for Revision ID 1.')
    assert pytest.approx(DUT.cost_failure, 0.002286574)
    assert pytest.approx(DUT.cost_hour, 12.5278)


@pytest.mark.integration
def test_calculate_costs_divide_by_zero(test_dao):
    """ calculate_costs() should return a non-zero error code when attempting to divide by zero. """
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKRevision).first()

    DUT.cost = 1252.78
    DUT.hazard_rate_logistics = 1.0 / 547885.1632698

    _error_code, _msg = DUT.calculate_costs(0.0)

    assert _error_code == 102
    assert _msg == ('RTK ERROR: Zero Division Error when calculating the '
                    'cost per mission hour for Revision ID 1.  Mission time: '
                    '0.000000.')
