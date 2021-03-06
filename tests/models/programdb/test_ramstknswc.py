# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstknswc.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKNSWC module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKNSWC

ATTRIBUTES = {
    'Clc': 0.0,
    'Crd': 0.0,
    'Cac': 0.0,
    'Cmu': 0.0,
    'Ck': 0.0,
    'Ci': 0.0,
    'Ch': 0.0,
    'Cn': 0.0,
    'Cm': 0.0,
    'Cl': 0.0,
    'Cc': 0.0,
    'Cb': 0.0,
    'Cg': 0.0,
    'Cf': 0.0,
    'Ce': 0.0,
    'Cd': 0.0,
    'Cy': 0.0,
    'Cbv': 0.0,
    'Cbt': 0.0,
    'Cs': 0.0,
    'Cr': 0.0,
    'Cq': 0.0,
    'Cp': 0.0,
    'Cw': 0.0,
    'Cv': 0.0,
    'Ct': 0.0,
    'Cnw': 0.0,
    'Cnp': 0.0,
    'Csf': 0.0,
    'Calt': 0.0,
    'Csc': 0.0,
    'Cbl': 0.0,
    'Csz': 0.0,
    'Cst': 0.0,
    'Csw': 0.0,
    'Csv': 0.0,
    'Cgl': 0.0,
    'Cga': 0.0,
    'Cgp': 0.0,
    'Cgs': 0.0,
    'Cgt': 0.0,
    'Cgv': 0.0,
    'Ccw': 0.0,
    'Ccv': 0.0,
    'Cpd': 0.0,
    'Ccp': 0.0,
    'Cpf': 0.0,
    'Ccs': 0.0,
    'Ccf': 0.0,
    'Cpv': 0.0,
    'Cdc': 0.0,
    'Cdl': 0.0,
    'Cdt': 0.0,
    'Cdw': 0.0,
    'Cdp': 0.0,
    'Cds': 0.0,
    'Cdy': 0.0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKNSWC():
    """Class for testing the RAMSTKNSWC model."""
    @pytest.mark.integration
    def test_ramstknswc_create(self, test_program_dao):
        """ __init__() should create an RAMSTKNSWC model. """
        DUT = test_program_dao.session.query(RAMSTKNSWC).first()

        assert isinstance(DUT, RAMSTKNSWC)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_nswc'
        assert DUT.hardware_id == 1
        assert DUT.Cac == 0.0
        assert DUT.Calt == 0.0
        assert DUT.Cb == 0.0
        assert DUT.Cbl == 0.0
        assert DUT.Cbt == 0.0
        assert DUT.Cbv == 0.0
        assert DUT.Cc == 0.0
        assert DUT.Ccf == 0.0
        assert DUT.Ccp == 0.0
        assert DUT.Ccs == 0.0
        assert DUT.Ccv == 0.0
        assert DUT.Ccw == 0.0
        assert DUT.Cd == 0.0
        assert DUT.Cdc == 0.0
        assert DUT.Cdl == 0.0
        assert DUT.Cdp == 0.0
        assert DUT.Cds == 0.0
        assert DUT.Cdt == 0.0
        assert DUT.Cdw == 0.0
        assert DUT.Cdy == 0.0
        assert DUT.Ce == 0.0
        assert DUT.Cf == 0.0
        assert DUT.Cg == 0.0
        assert DUT.Cga == 0.0
        assert DUT.Cgl == 0.0
        assert DUT.Cgp == 0.0
        assert DUT.Cgs == 0.0
        assert DUT.Cgt == 0.0
        assert DUT.Cgv == 0.0
        assert DUT.Ch == 0.0
        assert DUT.Ci == 0.0
        assert DUT.Ck == 0.0
        assert DUT.Cl == 0.0
        assert DUT.Clc == 0.0
        assert DUT.Cm == 0.0
        assert DUT.Cmu == 0.0
        assert DUT.Cn == 0.0
        assert DUT.Cnp == 0.0
        assert DUT.Cnw == 0.0
        assert DUT.Cp == 0.0
        assert DUT.Cpd == 0.0
        assert DUT.Cpf == 0.0
        assert DUT.Cpv == 0.0
        assert DUT.Cq == 0.0
        assert DUT.Cr == 0.0
        assert DUT.Crd == 0.0
        assert DUT.Cs == 0.0
        assert DUT.Csc == 0.0
        assert DUT.Csf == 0.0
        assert DUT.Cst == 0.0
        assert DUT.Csv == 0.0
        assert DUT.Csw == 0.0
        assert DUT.Csz == 0.0
        assert DUT.Ct == 0.0
        assert DUT.Cv == 0.0
        assert DUT.Cw == 0.0
        assert DUT.Cy == 0.0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a tuple of attribute values. """
        DUT = test_program_dao.session.query(RAMSTKNSWC).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)
        assert _attributes['Clc'] == 0.0
        assert _attributes['Crd'] == 0.0
        assert _attributes['Cac'] == 0.0
        assert _attributes['Cmu'] == 0.0
        assert _attributes['Ck'] == 0.0
        assert _attributes['Ci'] == 0.0
        assert _attributes['Ch'] == 0.0
        assert _attributes['Cn'] == 0.0
        assert _attributes['Cm'] == 0.0
        assert _attributes['Cl'] == 0.0
        assert _attributes['Cc'] == 0.0
        assert _attributes['Cb'] == 0.0
        assert _attributes['Cg'] == 0.0
        assert _attributes['Cf'] == 0.0
        assert _attributes['Ce'] == 0.0
        assert _attributes['Cd'] == 0.0
        assert _attributes['Cy'] == 0.0
        assert _attributes['Cbv'] == 0.0
        assert _attributes['Cbt'] == 0.0
        assert _attributes['Cs'] == 0.0
        assert _attributes['Cr'] == 0.0
        assert _attributes['Cq'] == 0.0
        assert _attributes['Cp'] == 0.0
        assert _attributes['Cw'] == 0.0
        assert _attributes['Cv'] == 0.0
        assert _attributes['Ct'] == 0.0
        assert _attributes['Cnw'] == 0.0
        assert _attributes['Cnp'] == 0.0
        assert _attributes['Csf'] == 0.0
        assert _attributes['Calt'] == 0.0
        assert _attributes['Csc'] == 0.0
        assert _attributes['Cbl'] == 0.0
        assert _attributes['Csz'] == 0.0
        assert _attributes['Cst'] == 0.0
        assert _attributes['Csw'] == 0.0
        assert _attributes['Csv'] == 0.0
        assert _attributes['Cgl'] == 0.0
        assert _attributes['Cga'] == 0.0
        assert _attributes['Cgp'] == 0.0
        assert _attributes['Cgs'] == 0.0
        assert _attributes['Cgt'] == 0.0
        assert _attributes['Cgv'] == 0.0
        assert _attributes['Ccw'] == 0.0
        assert _attributes['Ccv'] == 0.0
        assert _attributes['Cpd'] == 0.0
        assert _attributes['Ccp'] == 0.0
        assert _attributes['Cpf'] == 0.0
        assert _attributes['Ccs'] == 0.0
        assert _attributes['Ccf'] == 0.0
        assert _attributes['Cpv'] == 0.0
        assert _attributes['Cdc'] == 0.0
        assert _attributes['Cdl'] == 0.0
        assert _attributes['Cdt'] == 0.0
        assert _attributes['Cdw'] == 0.0
        assert _attributes['Cdp'] == 0.0
        assert _attributes['Cds'] == 0.0
        assert _attributes['Cdy'] == 0.0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKNSWC).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKNSWC).first()

        ATTRIBUTES['Cpv'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['Cpv'] == 0.0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKNSWC).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
