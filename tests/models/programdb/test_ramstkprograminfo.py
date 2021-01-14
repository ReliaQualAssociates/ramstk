# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.Test_ramstkprograminfo.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKProgramInfo module algorithms and
models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKProgramInfo

ATTRIBUTES = {
    'created_by': '',
    'created_on': date.today(),
    'last_saved': date.today(),
    'last_saved_by': '',
    'function_active': 1,
    'requirement_active': 1,
    'hardware_active': 1,
    'software_active': 0,
    'rcm_active': 0,
    'testing_active': 0,
    'incident_active': 0,
    'survival_active': 0,
    'vandv_active': 1,
    'hazard_active': 1,
    'stakeholder_active': 1,
    'allocation_active': 1,
    'similar_item_active': 1,
    'fmea_active': 1,
    'pof_active': 1,
    'rbd_active': 0,
    'fta_active': 0,
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKProgramInfo():
    """Class for testing the RAMSTKProgramInfo model."""
    @pytest.mark.integration
    def test_ramstkprograminfo_create(self, test_program_dao):
        """__init__() should create an RAMSTKProgramInfo model."""
        DUT = test_program_dao.session.query(RAMSTKProgramInfo).first()

        assert isinstance(DUT, RAMSTKProgramInfo)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_program_info'
        assert DUT.revision_id == 1
        assert DUT.function_active == 1
        assert DUT.requirement_active == 1
        assert DUT.hardware_active == 1
        assert DUT.software_active == 0
        assert DUT.rcm_active == 0
        assert DUT.testing_active == 0
        assert DUT.incident_active == 0
        assert DUT.survival_active == 0
        assert DUT.vandv_active == 1
        assert DUT.hazard_active == 1
        assert DUT.stakeholder_active == 1
        assert DUT.allocation_active == 1
        assert DUT.similar_item_active == 1
        assert DUT.fmea_active == 1
        assert DUT.pof_active == 1
        assert DUT.rbd_active == 0
        assert DUT.fta_active == 0
        assert DUT.created_on == date.today()
        assert DUT.created_by == ''
        assert DUT.last_saved == date.today()
        assert DUT.last_saved_by == ''

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """get_attributes() should return a dict of attribute values."""
        DUT = test_program_dao.session.query(RAMSTKProgramInfo).first()

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['function_active'] == 1
        assert _attributes['requirement_active'] == 1
        assert _attributes['hardware_active'] == 1
        assert _attributes['software_active'] == 0
        assert _attributes['rcm_active'] == 0
        assert _attributes['testing_active'] == 0
        assert _attributes['incident_active'] == 0
        assert _attributes['survival_active'] == 0
        assert _attributes['vandv_active'] == 1
        assert _attributes['hazard_active'] == 1
        assert _attributes['stakeholder_active'] == 1
        assert _attributes['allocation_active'] == 1
        assert _attributes['similar_item_active'] == 1
        assert _attributes['fmea_active'] == 1
        assert _attributes['pof_active'] == 1
        assert _attributes['rbd_active'] == 0
        assert _attributes['fta_active'] == 0
        assert _attributes['created_on'] == date.today()
        assert _attributes['created_by'] == ''
        assert _attributes['last_saved'] == date.today()
        assert _attributes['last_saved_by'] == ''

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """set_attributes() should return a zero error code on success."""
        DUT = test_program_dao.session.query(RAMSTKProgramInfo).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when
        the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKProgramInfo).first()

        ATTRIBUTES['pof_active'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['pof_active'] == 1

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an
        unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKProgramInfo).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
