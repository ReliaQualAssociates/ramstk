# -*- coding: utf-8 -*-
#
#       tests.data.storage.programdb.test_ramstkmilhdbkf.py is part of The
#       RAMSTK Project
#
# All rights reserved.
"""Test class for testing the RAMSTKMilHdbkF module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.data.storage.programdb.RAMSTKMilHdbkF import RAMSTKMilHdbkF

ATTRIBUTES = {
    'A1': 0.0,
    'A2': 0.0,
    'B1': 0.0,
    'B2': 0.0,
    'C1': 0.0,
    'C2': 0.0,
    'lambdaBD': 0.0,
    'lambdaBP': 0.0,
    'lambdaCYC': 0.0,
    'lambdaEOS': 0.0,
    'piA': 0.0,
    'piC': 0.0,
    'piCD': 0.0,
    'piCF': 0.0,
    'piCR': 0.0,
    'piCV': 0.0,
    'piCYC': 0.0,
    'piE': 0.0,
    'piF': 0.0,
    'piI': 0.0,
    'piK': 0.0,
    'piL': 0.0,
    'piM': 0.0,
    'piMFG': 0.0,
    'piN': 0.0,
    'piNR': 0.0,
    'piP': 0.0,
    'piPT': 0.0,
    'piQ': 0.0,
    'piR': 0.0,
    'piS': 0.0,
    'piT': 0.0,
    'piTAPS': 0.0,
    'piU': 0.0,
    'piV': 0.0
}


@pytest.mark.integration
def test_ramstkmilhdbkf_create(test_dao):
    """ __init__() should create an RAMSTKMilHdbkF model. """
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKMilHdbkF).first()

    assert isinstance(DUT, RAMSTKMilHdbkF)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_mil_hdbk_f'
    assert DUT.hardware_id == 1
    assert DUT.A1 == 0.0
    assert DUT.A2 == 0.0
    assert DUT.B1 == 0.0
    assert DUT.B2 == 0.0
    assert DUT.C1 == 0.0
    assert DUT.C2 == 0.0
    assert DUT.lambdaBD == 0.0
    assert DUT.lambdaBP == 0.0
    assert DUT.lambdaCYC == 0.0
    assert DUT.lambdaEOS == 0.0
    assert DUT.piA == 0.0
    assert DUT.piC == 0.0
    assert DUT.piCD == 0.0
    assert DUT.piCF == 0.0
    assert DUT.piCR == 0.0
    assert DUT.piCV == 0.0
    assert DUT.piCYC == 0.0
    assert DUT.piE == 0.0
    assert DUT.piF == 0.0
    assert DUT.piI == 0.0
    assert DUT.piK == 0.0
    assert DUT.piL == 0.0
    assert DUT.piM == 0.0
    assert DUT.piMFG == 0.0
    assert DUT.piN == 0.0
    assert DUT.piNR == 0.0
    assert DUT.piP == 0.0
    assert DUT.piPT == 0.0
    assert DUT.piQ == 0.0
    assert DUT.piR == 0.0
    assert DUT.piS == 0.0
    assert DUT.piT == 0.0
    assert DUT.piTAPS == 0.0
    assert DUT.piU == 0.0
    assert DUT.piV == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKMilHdbkF).first()

    _attributes = DUT.get_attributes()

    assert isinstance(_attributes, dict)
    assert _attributes['hardware_id'] == 1
    assert _attributes['A1'] == 0.0
    assert _attributes['A2'] == 0.0
    assert _attributes['B1'] == 0.0
    assert _attributes['B2'] == 0.0
    assert _attributes['C1'] == 0.0
    assert _attributes['C2'] == 0.0
    assert _attributes['lambdaBD'] == 0.0
    assert _attributes['lambdaBP'] == 0.0
    assert _attributes['lambdaCYC'] == 0.0
    assert _attributes['lambdaEOS'] == 0.0
    assert _attributes['piA'] == 0.0
    assert _attributes['piC'] == 0.0
    assert _attributes['piCD'] == 0.0
    assert _attributes['piCF'] == 0.0
    assert _attributes['piCR'] == 0.0
    assert _attributes['piCV'] == 0.0
    assert _attributes['piCYC'] == 0.0
    assert _attributes['piE'] == 0.0
    assert _attributes['piF'] == 0.0
    assert _attributes['piI'] == 0.0
    assert _attributes['piK'] == 0.0
    assert _attributes['piL'] == 0.0
    assert _attributes['piM'] == 0.0
    assert _attributes['piMFG'] == 0.0
    assert _attributes['piN'] == 0.0
    assert _attributes['piNR'] == 0.0
    assert _attributes['piP'] == 0.0
    assert _attributes['piPT'] == 0.0
    assert _attributes['piQ'] == 0.0
    assert _attributes['piR'] == 0.0
    assert _attributes['piS'] == 0.0
    assert _attributes['piT'] == 0.0
    assert _attributes['piTAPS'] == 0.0
    assert _attributes['piU'] == 0.0
    assert _attributes['piV'] == 0.0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKMilHdbkF).first()

    assert DUT.set_attributes(ATTRIBUTES) is None


@pytest.mark.integration
def test_set_attributes_none_value(test_dao):
    """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKMilHdbkF).first()

    ATTRIBUTES['piA'] = None

    assert DUT.set_attributes(ATTRIBUTES) is None
    assert DUT.get_attributes()['piA'] == 0.0


@pytest.mark.integration
def test_set_attributes_unknown_attributes(test_dao):
    """set_attributes() should raise an AttributeError when passed an unknown attribute."""
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKMilHdbkF).first()

    with pytest.raises(AttributeError):
        DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
