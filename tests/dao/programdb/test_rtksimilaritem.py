#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_rtksimilaritem.py is part of The RTK Project
#
# All rights reserved.
"""Test class for testing the RTKSimilarItem module algorithms and models."""

import pytest

from rtk.dao.programdb.RTKSimilarItem import RTKSimilarItem

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'

ATTRIBUTES = {
    'method_id': 0,
    'quality_to_id': 0,
    'parent_id': 0,
    'change_factor_4': 1.0,
    'change_factor_5': 1.0,
    'change_factor_6': 1.0,
    'change_factor_7': 1.0,
    'change_factor_1': 1.0,
    'change_factor_2': 1.0,
    'change_factor_3': 1.0,
    'change_factor_8': 1.0,
    'change_factor_9': 1.0,
    'function_5': u'',
    'function_4': u'',
    'function_3': u'',
    'function_2': u'',
    'function_1': u'',
    'quality_from_id': 0,
    'change_factor_10': 1.0,
    'user_blob_3': '',
    'environment_from_id': 0,
    'change_description_7': '',
    'hardware_id': 1,
    'environment_to_id': 0,
    'result_3': 0.0,
    'temperature_to': 30.0,
    'user_blob_2': '',
    'user_blob_1': '',
    'user_blob_5': '',
    'user_blob_4': '',
    'result_2': 0.0,
    'change_description_10': '',
    'result_1': 0.0,
    'result_4': 0.0,
    'result_5': 0.0,
    'user_float_5': 0.0,
    'user_float_4': 0.0,
    'user_float_3': 0.0,
    'user_float_2': 0.0,
    'user_float_1': 0.0,
    'user_int_4': 0,
    'user_int_5': 0,
    'user_int_1': 0,
    'user_int_2': 0,
    'user_int_3': 0,
    'change_description_6': '',
    'temperature_from': 30.0,
    'change_description_4': '',
    'change_description_5': '',
    'change_description_2': '',
    'change_description_3': '',
    'change_description_1': '',
    'change_description_8': '',
    'change_description_9': ''
}


@pytest.mark.integration
def test_rtkallocation_create(test_dao):
    """__init__() should create an RTKSimilarItem model."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).first()

    assert isinstance(DUT, RTKSimilarItem)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'rtk_similar_item'
    assert DUT.revision_id == 1
    assert DUT.hardware_id == 1
    assert DUT.change_description_1 == ''
    assert DUT.change_description_2 == ''
    assert DUT.change_description_3 == ''
    assert DUT.change_description_4 == ''
    assert DUT.change_description_5 == ''
    assert DUT.change_description_6 == ''
    assert DUT.change_description_7 == ''
    assert DUT.change_description_8 == ''
    assert DUT.change_description_9 == ''
    assert DUT.change_description_10 == ''
    assert DUT.change_factor_1 == 1.0
    assert DUT.change_factor_2 == 1.0
    assert DUT.change_factor_3 == 1.0
    assert DUT.change_factor_4 == 1.0
    assert DUT.change_factor_5 == 1.0
    assert DUT.change_factor_6 == 1.0
    assert DUT.change_factor_7 == 1.0
    assert DUT.change_factor_8 == 1.0
    assert DUT.change_factor_9 == 1.0
    assert DUT.change_factor_10 == 1.0
    assert DUT.environment_from_id == 0
    assert DUT.environment_to_id == 0
    assert DUT.function_1 == ''
    assert DUT.function_2 == ''
    assert DUT.function_3 == ''
    assert DUT.function_4 == ''
    assert DUT.function_5 == ''
    assert DUT.method_id == 0
    assert DUT.parent_id == 0
    assert DUT.quality_from_id == 0
    assert DUT.quality_to_id == 0
    assert DUT.result_1 == 0.0
    assert DUT.result_2 == 0.0
    assert DUT.result_3 == 0.0
    assert DUT.result_4 == 0.0
    assert DUT.result_5 == 0.0
    assert DUT.temperature_from == 30.0
    assert DUT.temperature_to == 30.0
    assert DUT.user_blob_1 == ''
    assert DUT.user_blob_2 == ''
    assert DUT.user_blob_3 == ''
    assert DUT.user_blob_4 == ''
    assert DUT.user_blob_5 == ''
    assert DUT.user_float_1 == 0.0
    assert DUT.user_float_2 == 0.0
    assert DUT.user_float_3 == 0.0
    assert DUT.user_float_4 == 0.0
    assert DUT.user_float_5 == 0.0
    assert DUT.user_int_1 == 0
    assert DUT.user_int_2 == 0
    assert DUT.user_int_3 == 0
    assert DUT.user_int_4 == 0
    assert DUT.user_int_5 == 0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """get_attributes() should return a dict of attribute values."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['hardware_id'] == 1
    assert _attributes['change_description_1'] == ''
    assert _attributes['change_description_2'] == ''
    assert _attributes['change_description_3'] == ''
    assert _attributes['change_description_4'] == ''
    assert _attributes['change_description_5'] == ''
    assert _attributes['change_description_6'] == ''
    assert _attributes['change_description_7'] == ''
    assert _attributes['change_description_8'] == ''
    assert _attributes['change_description_9'] == ''
    assert _attributes['change_description_10'] == ''
    assert _attributes['change_factor_1'] == 1.0
    assert _attributes['change_factor_2'] == 1.0
    assert _attributes['change_factor_3'] == 1.0
    assert _attributes['change_factor_4'] == 1.0
    assert _attributes['change_factor_5'] == 1.0
    assert _attributes['change_factor_6'] == 1.0
    assert _attributes['change_factor_7'] == 1.0
    assert _attributes['change_factor_8'] == 1.0
    assert _attributes['change_factor_9'] == 1.0
    assert _attributes['change_factor_10'] == 1.0
    assert _attributes['environment_from_id'] == 0
    assert _attributes['environment_to_id'] == 0
    assert _attributes['function_1'] == ''
    assert _attributes['function_2'] == ''
    assert _attributes['function_3'] == ''
    assert _attributes['function_4'] == ''
    assert _attributes['function_5'] == ''
    assert _attributes['method_id'] == 0
    assert _attributes['parent_id'] == 0
    assert _attributes['quality_from_id'] == 0
    assert _attributes['quality_to_id'] == 0
    assert _attributes['result_1'] == 0.0
    assert _attributes['result_2'] == 0.0
    assert _attributes['result_3'] == 0.0
    assert _attributes['result_4'] == 0.0
    assert _attributes['result_5'] == 0.0
    assert _attributes['temperature_from'] == 30.0
    assert _attributes['temperature_to'] == 30.0
    assert _attributes['user_blob_1'] == ''
    assert _attributes['user_blob_2'] == ''
    assert _attributes['user_blob_3'] == ''
    assert _attributes['user_blob_4'] == ''
    assert _attributes['user_blob_5'] == ''
    assert _attributes['user_float_1'] == 0.0
    assert _attributes['user_float_2'] == 0.0
    assert _attributes['user_float_3'] == 0.0
    assert _attributes['user_float_4'] == 0.0
    assert _attributes['user_float_5'] == 0.0
    assert _attributes['user_int_1'] == 0
    assert _attributes['user_int_2'] == 0
    assert _attributes['user_int_3'] == 0
    assert _attributes['user_int_4'] == 0
    assert _attributes['user_int_5'] == 0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """set_attributes() should return a zero error code on success."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == ("RTK SUCCESS: Updating RTKSimilarItem 1 attributes.")


@pytest.mark.integration
def test_set_attributes_too_few_passed(test_dao):
    """set_attributes() should return a 40 error code when passed a dict with missing attributes."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).first()

    _error_code, _msg = DUT.set_attributes({
        'method_id': 0,
        'quality_to_id': 0,
        'parent_id': 0,
        'change_factor_4': 1.0,
        'change_factor_5': 1.0,
        'change_factor_6': 1.0,
        'change_factor_7': 1.0,
        'change_factor_1': 1.0,
        'change_factor_2': 1.0,
        'change_factor_3': 1.0,
        'change_factor_8': 1.0,
        'change_factor_9': 1.0,
        'function_5': u'',
        'function_4': u'',
        'function_3': u'',
        'function_2': u'',
        'function_1': u'',
        'quality_from_id': 0,
        'change_factor_10': 1.0,
        'user_blob_3': '',
        'environment_from_id': 0,
        'change_description_7': '',
        'hardware_id': 1,
        'environment_to_id': 0,
        'result_3': 0.0,
        'temperature_to': 30.0,
        'user_blob_2': '',
        'user_blob_1': '',
        'user_blob_5': '',
        'user_blob_4': '',
        'result_2': 0.0,
        'change_description_10': '',
        'result_1': 0.0,
        'result_4': 0.0,
        'result_5': 0.0,
        'user_float_5': 0.0,
        'user_float_4': 0.0,
        'user_float_2': 0.0,
        'user_float_1': 0.0,
        'user_int_4': 0,
        'user_int_5': 0,
        'user_int_1': 0,
        'user_int_2': 0,
        'user_int_3': 0,
        'change_description_6': '',
        'temperature_from': 30.0,
        'change_description_4': '',
        'change_description_5': '',
        'change_description_2': '',
        'change_description_3': '',
        'change_description_1': '',
        'change_description_8': '',
        'change_description_9': ''
    })

    assert _error_code == 40
    assert _msg == ("RTK ERROR: Missing attribute 'user_float_3' in attribute "
                    "dictionary passed to RTKSimilarItem.set_attributes().")


@pytest.mark.integration
def test_topic_633(test_dao):
    """topic_633() should return False on success."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).filter(
        RTKSimilarItem.hardware_id == 2).all()[0]

    DUT.environment_from_id = 4
    DUT.environment_to_id = 6
    DUT.quality_from_id = 2
    DUT.quality_to_id = 3
    DUT.temperature_from = 38.0
    DUT.temperature_to = 27.5

    assert not DUT.topic_633(0.000003335)
    assert DUT.change_factor_1 == 0.6
    assert DUT.change_factor_2 == 3.3
    assert DUT.change_factor_3 == 1.1
    assert DUT.result_1 == pytest.approx(1.5312213e-06)


@pytest.mark.integration
def test_topic_633_quality_key_error(test_dao):
    """topic_633() should return True when passed a quality ID that isn't in the dict."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).filter(
        RTKSimilarItem.hardware_id == 2).all()[0]

    DUT.environment_from_id = 4
    DUT.environment_to_id = 6
    DUT.quality_from_id = 2
    DUT.quality_to_id = 30
    DUT.temperature_from = 38.0
    DUT.temperature_to = 27.5

    assert DUT.topic_633(0.000003335)
    assert DUT.change_factor_1 == 1.0
    assert DUT.change_factor_2 == 3.3
    assert DUT.change_factor_3 == 1.1
    assert DUT.result_1 == pytest.approx(9.1873278e-07)


@pytest.mark.integration
def test_topic_633_environment_key_error(test_dao):
    """topic_633() should return True when passed an environment ID that isn't in the dict."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).filter(
        RTKSimilarItem.hardware_id == 2).all()[0]

    DUT.environment_from_id = 4
    DUT.environment_to_id = 60
    DUT.quality_from_id = 2
    DUT.quality_to_id = 3
    DUT.temperature_from = 38.0
    DUT.temperature_to = 27.5

    assert DUT.topic_633(0.000003335)
    assert DUT.change_factor_1 == 0.6
    assert DUT.change_factor_2 == 1.0
    assert DUT.change_factor_3 == 1.1
    assert DUT.result_1 == pytest.approx(5.0530303e-06)


@pytest.mark.integration
def test_topic_633_temperature_key_error(test_dao):
    """topic_633() should return True when passed a temperature that can't be converted to a key in the dict."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).filter(
        RTKSimilarItem.hardware_id == 2).all()[0]

    DUT.environment_from_id = 4
    DUT.environment_to_id = 6
    DUT.quality_from_id = 2
    DUT.quality_to_id = 3
    DUT.temperature_from = 380.0
    DUT.temperature_to = 27.5

    assert DUT.topic_633(0.000003335)
    assert DUT.change_factor_1 == 0.6
    assert DUT.change_factor_2 == 3.3
    assert DUT.change_factor_3 == 1.0
    assert DUT.result_1 == pytest.approx(1.6843434e-06)


@pytest.mark.integration
def test_user_defined(test_dao):
    """user_defined() should return False on success."""
    _session = test_dao.RTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RTKSimilarItem).filter(
        RTKSimilarItem.hardware_id == 2).all()[0]

    DUT.change_factor_1 = 1.1
    DUT.change_factor_2 = 0.9
    DUT.change_factor_3 = 1.0
    DUT.change_factor_4 = 0.95
    DUT.change_factor_5 = 1.25
    DUT.function_1 = 'hr * pi1 * pi2 * pi3 * pi4 * pi5'

    assert not DUT.user_defined(0.000003335)
    assert DUT.result_1 == pytest.approx(3.9207094e-06)
