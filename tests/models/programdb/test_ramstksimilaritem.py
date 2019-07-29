# -*- coding: utf-8 -*-
#
#       tests.data.storage.programdb.test_ramstksimilaritem.py is part of The
#       RAMSTK Project
#
# All rights reserved.
"""Test class for testing RAMSTKSimilarItem module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKSimilarItem

ATTRIBUTES = {
    'similar_item_method_id': 0,
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
    'function_5': '0',
    'function_4': '0',
    'function_3': '0',
    'function_2': '0',
    'function_1': '0',
    'quality_from_id': 0,
    'change_factor_10': 1.0,
    'user_blob_3': b'',
    'environment_from_id': 0,
    'change_description_7': b'',
    'environment_to_id': 0,
    'result_3': 0.0,
    'temperature_to': 30.0,
    'user_blob_2': b'',
    'user_blob_1': b'',
    'user_blob_5': b'',
    'user_blob_4': b'',
    'result_2': 0.0,
    'change_description_10': b'',
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
    'change_description_6': b'',
    'temperature_from': 30.0,
    'change_description_4': b'',
    'change_description_5': b'',
    'change_description_2': b'',
    'change_description_3': b'',
    'change_description_1': b'',
    'change_description_8': b'',
    'change_description_9': b''
}


@pytest.mark.integration
def test_ramstksimilaritem_create(test_dao):
    """__init__() should create an RAMSTKSimilarItem model."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSimilarItem).first()

    assert isinstance(DUT, RAMSTKSimilarItem)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_similar_item'
    assert DUT.revision_id == 1
    assert DUT.hardware_id == 1
    assert DUT.change_description_1 == b''
    assert DUT.change_description_2 == b''
    assert DUT.change_description_3 == b''
    assert DUT.change_description_4 == b''
    assert DUT.change_description_5 == b''
    assert DUT.change_description_6 == b''
    assert DUT.change_description_7 == b''
    assert DUT.change_description_8 == b''
    assert DUT.change_description_9 == b''
    assert DUT.change_description_10 == b''
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
    assert DUT.function_1 == '0'
    assert DUT.function_2 == '0'
    assert DUT.function_3 == '0'
    assert DUT.function_4 == '0'
    assert DUT.function_5 == '0'
    assert DUT.similar_item_method_id == 1
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
    assert DUT.user_blob_1 == b''
    assert DUT.user_blob_2 == b''
    assert DUT.user_blob_3 == b''
    assert DUT.user_blob_4 == b''
    assert DUT.user_blob_5 == b''
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
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSimilarItem).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)

    assert _attributes['hardware_id'] == 1
    assert _attributes['change_description_1'] == b''
    assert _attributes['change_description_2'] == b''
    assert _attributes['change_description_3'] == b''
    assert _attributes['change_description_4'] == b''
    assert _attributes['change_description_5'] == b''
    assert _attributes['change_description_6'] == b''
    assert _attributes['change_description_7'] == b''
    assert _attributes['change_description_8'] == b''
    assert _attributes['change_description_9'] == b''
    assert _attributes['change_description_10'] == b''
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
    assert _attributes['function_1'] == '0'
    assert _attributes['function_2'] == '0'
    assert _attributes['function_3'] == '0'
    assert _attributes['function_4'] == '0'
    assert _attributes['function_5'] == '0'
    assert _attributes['similar_item_method_id'] == 1
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
    assert _attributes['user_blob_1'] == b''
    assert _attributes['user_blob_2'] == b''
    assert _attributes['user_blob_3'] == b''
    assert _attributes['user_blob_4'] == b''
    assert _attributes['user_blob_5'] == b''
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
    """set_attributes() should return None on success."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSimilarItem).first()

    assert DUT.set_attributes(ATTRIBUTES) is None


@pytest.mark.integration
def test_set_attributes_none_value(test_dao):
    """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSimilarItem).first()

    ATTRIBUTES['change_factor_3'] = None

    assert DUT.set_attributes(ATTRIBUTES) is None
    assert DUT.get_attributes()['change_factor_3'] == 1.0


@pytest.mark.integration
def test_set_attributes_unknown_attributes(test_dao):
    """set_attributes() should raise an AttributeError when passed an unknown attribute."""
    _session = test_dao.RAMSTK_SESSION(
        bind=test_dao.engine, autoflush=False, expire_on_commit=False)
    DUT = _session.query(RAMSTKSimilarItem).first()

    with pytest.raises(AttributeError):
        DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
