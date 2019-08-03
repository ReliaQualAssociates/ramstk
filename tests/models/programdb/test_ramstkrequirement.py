# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkrequirement.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing RAMSTKRequirement module algorithms and models."""

# Standard Library Imports
from datetime import date

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKRequirement

ATTRIBUTES = {
    'derived': 0,
    'description': b'',
    'figure_number': '',
    'owner': '',
    'page_number': '',
    'parent_id': 0,
    'priority': 0,
    'q_clarity_0': 0,
    'q_clarity_1': 0,
    'q_clarity_2': 0,
    'q_clarity_3': 0,
    'q_clarity_4': 0,
    'q_clarity_5': 0,
    'q_clarity_6': 0,
    'q_clarity_7': 0,
    'q_clarity_8': 0,
    'q_complete_0': 0,
    'q_complete_1': 0,
    'q_complete_2': 0,
    'q_complete_3': 0,
    'q_complete_4': 0,
    'q_complete_5': 0,
    'q_complete_6': 0,
    'q_complete_7': 0,
    'q_complete_8': 0,
    'q_complete_9': 0,
    'q_consistent_0': 0,
    'q_consistent_1': 0,
    'q_consistent_2': 0,
    'q_consistent_3': 0,
    'q_consistent_4': 0,
    'q_consistent_5': 0,
    'q_consistent_6': 0,
    'q_consistent_7': 0,
    'q_consistent_8': 0,
    'q_verifiable_0': 0,
    'q_verifiable_1': 0,
    'q_verifiable_2': 0,
    'q_verifiable_3': 0,
    'q_verifiable_4': 0,
    'q_verifiable_5': 0,
    'requirement_code': 'REL-0001',
    'requirement_type': '',
    'specification': '',
    'validated': 0,
    'validated_date': date(2019, 7, 21)
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKRequirement():
    """Class for testing the RAMSTKRequirement model."""
    @pytest.mark.integration
    def test_ramstkrequirement_create(self, test_program_dao):
        """ __init__() should create an RAMSTKRequirement model. """
        DUT = test_program_dao.session.query(RAMSTKRequirement).first()

        assert isinstance(DUT, RAMSTKRequirement)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_requirement'
        assert DUT.revision_id == 1
        assert DUT.requirement_id == 1
        assert DUT.derived == 0
        assert DUT.description == b''
        assert DUT.figure_number == ''
        assert DUT.owner == ''
        assert DUT.page_number == ''
        assert DUT.parent_id == 0
        assert DUT.priority == 0
        assert DUT.requirement_code == 'REL-0001'
        assert DUT.specification == ''
        assert DUT.requirement_type == ''
        assert DUT.validated == 0
        assert DUT.validated_date == date(2019, 7, 21)
        assert DUT.q_clarity_0 == 0
        assert DUT.q_clarity_1 == 0
        assert DUT.q_clarity_2 == 0
        assert DUT.q_clarity_3 == 0
        assert DUT.q_clarity_4 == 0
        assert DUT.q_clarity_5 == 0
        assert DUT.q_clarity_6 == 0
        assert DUT.q_clarity_7 == 0
        assert DUT.q_clarity_8 == 0
        assert DUT.q_complete_0 == 0
        assert DUT.q_complete_1 == 0
        assert DUT.q_complete_2 == 0
        assert DUT.q_complete_3 == 0
        assert DUT.q_complete_4 == 0
        assert DUT.q_complete_5 == 0
        assert DUT.q_complete_6 == 0
        assert DUT.q_complete_7 == 0
        assert DUT.q_complete_8 == 0
        assert DUT.q_complete_9 == 0
        assert DUT.q_consistent_0 == 0
        assert DUT.q_consistent_1 == 0
        assert DUT.q_consistent_2 == 0
        assert DUT.q_consistent_3 == 0
        assert DUT.q_consistent_4 == 0
        assert DUT.q_consistent_5 == 0
        assert DUT.q_consistent_6 == 0
        assert DUT.q_consistent_7 == 0
        assert DUT.q_consistent_8 == 0
        assert DUT.q_verifiable_0 == 0
        assert DUT.q_verifiable_1 == 0
        assert DUT.q_verifiable_2 == 0
        assert DUT.q_verifiable_3 == 0
        assert DUT.q_verifiable_4 == 0
        assert DUT.q_verifiable_5 == 0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a tuple of attribute values. """
        DUT = test_program_dao.session.query(RAMSTKRequirement).first()

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['requirement_id'] == 1
        assert _attributes['derived'] == 0
        assert _attributes['description'] == b''
        assert _attributes['figure_number'] == ''
        assert _attributes['owner'] == ''
        assert _attributes['page_number'] == ''
        assert _attributes['parent_id'] == 0
        assert _attributes['priority'] == 0
        assert _attributes['requirement_code'] == 'REL-0001'
        assert _attributes['specification'] == ''
        assert _attributes['requirement_type'] == ''
        assert _attributes['validated'] == 0
        assert _attributes['validated_date'] == date(2019, 7, 21)
        assert _attributes['q_clarity_0'] == 0
        assert _attributes['q_clarity_1'] == 0
        assert _attributes['q_clarity_2'] == 0
        assert _attributes['q_clarity_3'] == 0
        assert _attributes['q_clarity_4'] == 0
        assert _attributes['q_clarity_5'] == 0
        assert _attributes['q_clarity_6'] == 0
        assert _attributes['q_clarity_7'] == 0
        assert _attributes['q_clarity_8'] == 0
        assert _attributes['q_complete_0'] == 0
        assert _attributes['q_complete_1'] == 0
        assert _attributes['q_complete_2'] == 0
        assert _attributes['q_complete_3'] == 0
        assert _attributes['q_complete_4'] == 0
        assert _attributes['q_complete_5'] == 0
        assert _attributes['q_complete_6'] == 0
        assert _attributes['q_complete_7'] == 0
        assert _attributes['q_complete_8'] == 0
        assert _attributes['q_complete_9'] == 0
        assert _attributes['q_consistent_0'] == 0
        assert _attributes['q_consistent_1'] == 0
        assert _attributes['q_consistent_2'] == 0
        assert _attributes['q_consistent_3'] == 0
        assert _attributes['q_consistent_4'] == 0
        assert _attributes['q_consistent_5'] == 0
        assert _attributes['q_consistent_6'] == 0
        assert _attributes['q_consistent_7'] == 0
        assert _attributes['q_consistent_8'] == 0
        assert _attributes['q_verifiable_0'] == 0
        assert _attributes['q_verifiable_1'] == 0
        assert _attributes['q_verifiable_2'] == 0
        assert _attributes['q_verifiable_3'] == 0
        assert _attributes['q_verifiable_4'] == 0
        assert _attributes['q_verifiable_5'] == 0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKRequirement).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKRequirement).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == b''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKRequirement).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})

    @pytest.mark.integration
    def test_create_code(self, test_program_dao):
        """ create_code() should return False on success. """
        DUT = test_program_dao.session.query(RAMSTKRequirement).first()

        assert not DUT.create_code('PERF')
        assert DUT.requirement_code == 'PERF-0001'
