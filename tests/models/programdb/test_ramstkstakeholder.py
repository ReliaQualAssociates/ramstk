# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkstakeholder.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKStakeholder module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKStakeholder

ATTRIBUTES = {
    'customer_rank': 1,
    'description': 'Test Stakeholder Input',
    'group': '',
    'improvement': 0.0,
    'overall_weight': 0.0,
    'planned_rank': 1,
    'priority': 1,
    'requirement_id': 0,
    'stakeholder': '',
    'user_float_1': 1.0,
    'user_float_2': 1.0,
    'user_float_3': 1.0,
    'user_float_4': 1.0,
    'user_float_5': 1.0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKStakeholder():
    """Class for testing the RAMSTKStakeholder model."""
    @pytest.mark.integration
    def test_ramstkstakeholder_create(self, test_program_dao):
        """ __init__() should create an RAMSTKStakeholder model. """
        DUT = test_program_dao.session.query(RAMSTKStakeholder).first()

        assert isinstance(DUT, RAMSTKStakeholder)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_stakeholder'
        assert DUT.revision_id == 1
        assert DUT.stakeholder_id == 1
        assert DUT.customer_rank == 1
        assert DUT.description == 'Test Stakeholder Input'
        assert DUT.group == ''
        assert DUT.improvement == 0.0
        assert DUT.overall_weight == 0.0
        assert DUT.planned_rank == 1
        assert DUT.priority == 1
        assert DUT.requirement_id == 0
        assert DUT.stakeholder == ''
        assert DUT.user_float_1 == 1.0
        assert DUT.user_float_2 == 1.0
        assert DUT.user_float_3 == 1.0
        assert DUT.user_float_4 == 1.0
        assert DUT.user_float_5 == 1.0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a tuple of attribute values. """
        DUT = test_program_dao.session.query(RAMSTKStakeholder).first()

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['stakeholder_id'] == 1
        assert _attributes['customer_rank'] == 1
        assert _attributes['description'] == 'Test Stakeholder Input'
        assert _attributes['group'] == ''
        assert _attributes['improvement'] == 0.0
        assert _attributes['overall_weight'] == 0.0
        assert _attributes['planned_rank'] == 1
        assert _attributes['priority'] == 1
        assert _attributes['requirement_id'] == 0
        assert _attributes['stakeholder'] == ''
        assert _attributes['user_float_1'] == 1.0
        assert _attributes['user_float_2'] == 1.0
        assert _attributes['user_float_3'] == 1.0
        assert _attributes['user_float_4'] == 1.0
        assert _attributes['user_float_5'] == 1.0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKStakeholder).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKStakeholder).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == 'Stakeholder Input'

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKStakeholder).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
