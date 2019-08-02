# -*- coding: utf-8 -*-
#
#       tests.dao.commondb.test_ramstkcategory.py is part of The RAMSTK Project

#
# All rights reserved.
"""Test class for testing the RAMSTKCategory module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.commondb import RAMSTKCategory

ATTRIBUTES = {
    'category_type': 'hardware',
    'category_id': 1,
    'name': 'IC',
    'value': 1,
    'description': 'Integrated Circuit',
    'harsh_ir_limit': 0.8,
    'mild_ir_limit': 0.9,
    'harsh_pr_limit': 1.0,
    'mild_pr_limit': 1.0,
    'harsh_vr_limit': 1.0,
    'mild_vr_limit': 1.0,
    'harsh_deltat_limit': 0.0,
    'mild_deltat_limit': 0.0,
    'harsh_maxt_limit': 125.0,
    'mild_maxt_limit': 125.0,
}


@pytest.mark.integration
def test_ramstkcategory_create(test_common_dao):
    """ __init__() should create an RAMSTKCategory model. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False,
    )
    DUT = _session.query(RAMSTKCategory).first()

    assert isinstance(DUT, RAMSTKCategory)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_category'
    assert DUT.category_id == 1
    assert DUT.name == 'IC'
    assert DUT.description == 'Integrated Circuit'
    assert DUT.cat_type == 'hardware'
    assert DUT.value == 1
    assert DUT.harsh_ir_limit == 0.8
    assert DUT.mild_ir_limit == 0.9
    assert DUT.harsh_pr_limit == 1.0
    assert DUT.mild_pr_limit == 1.0
    assert DUT.harsh_vr_limit == 1.0
    assert DUT.mild_vr_limit == 1.0
    assert DUT.harsh_deltat_limit == 0.0
    assert DUT.mild_deltat_limit == 0.0
    assert DUT.harsh_maxt_limit == 125.0
    assert DUT.mild_maxt_limit == 125.0


@pytest.mark.integration
def test_get_attributes(test_common_dao):
    """ get_attributes() should return a tuple of attributes values on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False,
    )
    DUT = _session.query(RAMSTKCategory).first()

    assert DUT.get_attributes() == ATTRIBUTES


@pytest.mark.integration
def test_set_attributes(test_common_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False,
    )
    DUT = _session.query(RAMSTKCategory).first()

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 0
    assert _msg == (
        "RAMSTK SUCCESS: Updating RAMSTKCategory {0:d} "
        "attributes.".format(DUT.category_id)
    )


@pytest.mark.integration
def test_set_attributes_missing_key(test_common_dao):
    """ set_attributes() should return a 40 error code when passed too few attributes. """
    _session = test_common_dao.RAMSTK_SESSION(
        bind=test_common_dao.engine, autoflush=False, expire_on_commit=False,
    )
    DUT = _session.query(RAMSTKCategory).first()

    ATTRIBUTES.pop('category_type')

    _error_code, _msg = DUT.set_attributes(ATTRIBUTES)

    assert _error_code == 40
    assert _msg == (
        "RAMSTK ERROR: Missing attribute 'category_type' in "
        "attribute dictionary passed to "
        "RAMSTKCategory.set_attributes()."
    )

    ATTRIBUTES['category_type'] = 'hardware'
