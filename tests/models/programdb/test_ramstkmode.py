# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.TestRAMSTKMode.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing the RAMSTKMode module algorithms and models."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMode

ATTRIBUTES = {
    'effect_local': '',
    'mission': 'Default Mission',
    'other_indications': '',
    'mode_criticality': 0.0,
    'single_point': 0,
    'design_provisions': '',
    'type_id': 0,
    'rpn_severity_new': 1,
    'effect_next': '',
    'detection_method': '',
    'operator_actions': '',
    'critical_item': 0,
    'hazard_rate_source': '',
    'severity_class': '',
    'description': 'Test Functional Failure Mode #1',
    'mission_phase': '',
    'mode_probability': '',
    'remarks': b'',
    'mode_ratio': 0.0,
    'mode_hazard_rate': 0.0,
    'rpn_severity': 1,
    'isolation_method': '',
    'effect_end': '',
    'mode_op_time': 0.0,
    'effect_probability': 0.0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKMode():
    """Class for testing the RAMSTKMode model."""
    @pytest.mark.integration
    def test_ramstkmode_create(self, test_program_dao):
        """ __init__() should create an RAMSTKMode model. """
        DUT = test_program_dao.session.query(RAMSTKMode).first()

        assert isinstance(DUT, RAMSTKMode)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_mode'
        assert DUT.function_id == 1
        assert DUT.hardware_id == -1
        assert DUT.mode_id == 1
        assert DUT.critical_item == 0
        assert DUT.description == 'Test Functional Failure Mode #1'
        assert DUT.design_provisions == ''
        assert DUT.detection_method == ''
        assert DUT.effect_end == ''
        assert DUT.effect_local == ''
        assert DUT.effect_next == ''
        assert DUT.effect_probability == 0.0
        assert DUT.hazard_rate_source == ''
        assert DUT.isolation_method == ''
        assert DUT.mission == 'Default Mission'
        assert DUT.mission_phase == ''
        assert DUT.mode_criticality == 0.0
        assert DUT.mode_hazard_rate == 0.0
        assert DUT.mode_op_time == 0.0
        assert DUT.mode_probability == ''
        assert DUT.mode_ratio == 0.0
        assert DUT.operator_actions == ''
        assert DUT.other_indications == ''
        assert DUT.remarks == ''
        assert DUT.rpn_severity == 1
        assert DUT.rpn_severity_new == 1
        assert DUT.severity_class == ''
        assert DUT.single_point == 0
        assert DUT.type_id == 0


    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a dict of attribute name:value pairs. """
        DUT = test_program_dao.session.query(RAMSTKMode).first()

        _attributes = DUT.get_attributes()
        assert _attributes['function_id'] == 1
        assert _attributes['hardware_id'] == -1
        assert _attributes['mode_id'] == 1
        assert _attributes['critical_item'] == 0
        assert _attributes['description'] == 'Test Functional Failure Mode #1'
        assert _attributes['design_provisions'] == ''
        assert _attributes['detection_method'] == ''
        assert _attributes['effect_end'] == ''
        assert _attributes['effect_local'] == ''
        assert _attributes['effect_next'] == ''
        assert _attributes['effect_probability'] == 0.0
        assert _attributes['hazard_rate_source'] == ''
        assert _attributes['isolation_method'] == ''
        assert _attributes['mission'] == 'Default Mission'
        assert _attributes['mission_phase'] == ''
        assert _attributes['mode_criticality'] == 0.0
        assert _attributes['mode_hazard_rate'] == 0.0
        assert _attributes['mode_op_time'] == 0.0
        assert _attributes['mode_probability'] == ''
        assert _attributes['mode_ratio'] == 0.0
        assert _attributes['operator_actions'] == ''
        assert _attributes['other_indications'] == ''
        assert _attributes['remarks'] == ''
        assert _attributes['rpn_severity'] == 1
        assert _attributes['rpn_severity_new'] == 1
        assert _attributes['severity_class'] == ''
        assert _attributes['single_point'] == 0
        assert _attributes['type_id'] == 0


    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKMode).first()

        assert DUT.set_attributes(ATTRIBUTES) is None


    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKMode).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''


    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKMode).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
