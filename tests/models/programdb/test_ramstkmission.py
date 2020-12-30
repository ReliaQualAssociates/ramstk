# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkmission.py is part of The RAMSTK
#       Project
#
# All rights reserved.
""" Test class for testing the RAMSTKMission module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMission

ATTRIBUTES = {
    'description': 'Test Mission',
    'mission_time': 0.0,
    'time_units': 'hours'
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKMission():
    """Class for testing the RAMSTKMission model."""
    @pytest.mark.integration
    def test_ramstkmission_create(self, test_program_dao):
        """ __init__() should create an RAMSTKMission model. """
        DUT = test_program_dao.session.query(RAMSTKMission).first()

        assert isinstance(DUT, RAMSTKMission)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_mission'
        assert DUT.revision_id == 1
        assert DUT.mission_id == 2
        assert DUT.description == 'Test Mission 2'
        assert DUT.mission_time == 0.0
        assert DUT.time_units == 'hours'

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a tuple of attribute values. """
        DUT = test_program_dao.session.query(RAMSTKMission).first()

        _attributes = DUT.get_attributes()
        assert _attributes['description'] == 'Test Mission 2'
        assert _attributes['mission_time'] == 0.0
        assert _attributes['time_units'] == 'hours'

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKMission).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKMission).first()

        ATTRIBUTES['mission_time'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['mission_time'] == 0.0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKMission).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
