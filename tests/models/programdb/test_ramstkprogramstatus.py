# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.progrmdb.test_ramstkprogramstatus.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing RAMSTKProgramStatus module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKProgramStatus

ATTRIBUTES = {
    'cost_remaining': 0.0,
    'date_status': date.today() + timedelta(7),
    'time_remaining': 0.0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKProgramStatus():
    """Class for testing the RAMSTKProgramStatus model."""
    @pytest.mark.integration
    def test_ramstkprogramstatus_create(self, test_program_dao):
        """ __init__() should create an RAMSTKProgramStatus model. """
        DUT = test_program_dao.do_select_all(RAMSTKProgramStatus, _all=False)

        assert isinstance(DUT, RAMSTKProgramStatus)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_program_status'
        assert DUT.revision_id == 1
        assert DUT.status_id == 1
        assert DUT.cost_remaining == 0.0
        assert DUT.date_status == date(2019, 7, 21)
        assert DUT.time_remaining == 0.0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a dict of attribute values. """
        DUT = test_program_dao.do_select_all(RAMSTKProgramStatus, _all=False)

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['status_id'] == 1
        assert _attributes['cost_remaining'] == 0.0
        assert _attributes['date_status'] == date(2019, 7, 21)
        assert _attributes['time_remaining'] == 0.0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.do_select_all(RAMSTKProgramStatus, _all=False)

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.do_select_all(RAMSTKProgramStatus, _all=False)

        ATTRIBUTES['time_remaining'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['time_remaining'] == 0.0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.do_select_all(RAMSTKProgramStatus, _all=False)

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
