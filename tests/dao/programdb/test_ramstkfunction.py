# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtkfunction.py is part of The RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKFunction module algorithms and models."""

import pytest

from rtk.dao.programdb.RAMSTKFunction import RAMSTKFunction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


ATTRIBUTES = {
        'type_id': 0,
        'total_part_count': 0,
        'availability_mission': 1.0,
        'cost': 0.0,
        'hazard_rate_mission': 0.0,
        'mpmt': 0.0,
        'parent_id': 0,
        'mtbf_logistics': 0.0,
        'safety_critical': 0,
        'mmt': 0.0,
        'hazard_rate_logistics': 0.0,
        'remarks': '',
        'function_id': 1,
        'mtbf_mission': 0.0,
        'function_code': 'FUNC-0001',
        'name': u'Function Name',
        'level': 0,
        'mttr': 0.0,
        'mcmt': 0.0,
        'revision_id': 1,
        'availability_logistics': 1.0,
        'total_mode_count': 0
    }


@pytest.mark.integration
def test_rtkfunction_create(test_dao):
    """ __init__() should create an RAMSTKFunction model. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFunction).first()

    assert isinstance(DUT, RAMSTKFunction)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_function'
    assert DUT.revision_id == 1
    assert DUT.function_id == 1
    assert DUT.availability_logistics == 1.0
    assert DUT.availability_mission == 1.0
    assert DUT.cost == 0.0
    assert DUT.function_code == 'FUNC-0001'
    assert DUT.hazard_rate_logistics == 0.0
    assert DUT.hazard_rate_mission == 0.0
    assert DUT.level == 0
    assert DUT.mmt == 0.0
    assert DUT.mcmt == 0.0
    assert DUT.mpmt == 0.0
    assert DUT.mtbf_logistics == 0.0
    assert DUT.mtbf_mission == 0.0
    assert DUT.mttr == 0.0
    assert DUT.name == 'Function Name'
    assert DUT.parent_id == 0
    assert DUT.remarks == ''
    assert DUT.safety_critical == 0
    assert DUT.total_mode_count == 0
    assert DUT.total_part_count == 0
    assert DUT.type_id == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a dict of {attribute name:attribute value} pairs. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFunction).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFunction).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RAMSTK SUCCESS: Updating RAMSTKFunction {0:d} "
                    "attributes.".format(DUT.function_id))


@pytest.mark.integration
def test_set_attributes_too_few_passed(test_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFunction).first()

    ATTRIBUTES.pop('type_id')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == ("RAMSTK ERROR: Missing attribute 'type_id' in attribute "
                    "dictionary passed to RAMSTKFunction.set_attributes().")

    ATTRIBUTES['type_id'] = 0


@pytest.mark.integration
def test_calculate_mtbf(test_dao):
    """ calculate_mtbf() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFunction).first()

    DUT.hazard_rate_logistics = 0.0000003
    DUT.hazard_rate_mission = 0.000002

    _error_code, _msg = DUT.calculate_mtbf()
    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Calculating MTBF metrics for Function ID 1.')
    assert pytest.approx(DUT.mtbf_logistics, 3333333.3333333)
    assert pytest.approx(DUT.mtbf_mission, 500000.0)


@pytest.mark.integration
def test_calculate_availability(test_dao):
    """ calculate_availability() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFunction).first()

    DUT.mpmt = 0.5
    DUT.mcmt = 1.2
    DUT.mttr = 5.8
    DUT.mmt = 0.85
    DUT.mtbf_logistics = 547885.1632698
    DUT.mtbf_mission = 500000.0

    _error_code, _msg = DUT.calculate_availability()
    assert _error_code == 0
    assert _msg == ('RAMSTK SUCCESS: Calculating availability metrics for '
                    'Function ID 1.')
    assert pytest.approx(DUT.availability_logistics, 0.9999894)
    assert pytest.approx(DUT.availability_mission, 0.9999884)


@pytest.mark.integration
def test_calculate_availability_divide_by_zero(test_dao):
    """ calculate_availability() should return a non-zero error code when attempting to divide by zero. """
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKFunction).first()

    DUT.mttr = 0.0
    DUT.mtbf_logistics = 547885.1632698
    DUT.mtbf_mission = 0.0

    _error_code, _msg = DUT.calculate_availability()
    assert _error_code == 102
    assert _msg == ('RAMSTK ERROR: Zero Division Error when calculating the '
                    'mission availability for Function ID 1.  Mission MTBF: '
                    '0.000000 MTTR: 0.000000.')
