# pylint: disable=protected-access, no-self-use, missing-docstring
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkvalidation.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKValidation module algorithms and models."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKValidation

ATTRIBUTES = {
    'acceptable_maximum': 0.0,
    'acceptable_mean': 0.0,
    'acceptable_minimum': 0.0,
    'acceptable_variance': 0.0,
    'confidence': 95.0,
    'cost_average': 0.0,
    'cost_ll': 0.0,
    'cost_maximum': 0.0,
    'cost_mean': 0.0,
    'cost_minimum': 0.0,
    'cost_ul': 0.0,
    'cost_variance': 0.0,
    'date_end': date.today() + timedelta(days=30),
    'date_start': date.today(),
    'description': 'Test Validation',
    'measurement_unit': '',
    'name': '',
    'status': 0.0,
    'task_specification': '',
    'task_type': '',
    'time_average': 0.0,
    'time_ll': 0.0,
    'time_maximum': 0.0,
    'time_mean': 0.0,
    'time_minimum': 0.0,
    'time_ul': 0.0,
    'time_variance': 0.0
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKValidation():
    """Class for testing the RAMSTKValidation model."""
    @pytest.mark.integration
    def test_ramstkvalidation_create(self, test_program_dao):
        """ __init__() should create an RAMSTKValidation model. """
        DUT = test_program_dao.session.query(RAMSTKValidation).first()

        assert isinstance(DUT, RAMSTKValidation)

        # Verify class attributes are properly initialized.
        assert DUT.__tablename__ == 'ramstk_validation'
        assert DUT.revision_id == 1
        assert DUT.validation_id == 2
        assert DUT.acceptable_maximum == 0.0
        assert DUT.acceptable_mean == 0.0
        assert DUT.acceptable_minimum == 0.0
        assert DUT.acceptable_variance == 0.0
        assert DUT.confidence == 95.0
        assert DUT.cost_average == 0.0
        assert DUT.cost_ll == 0.0
        assert DUT.cost_maximum == 0.0
        assert DUT.cost_mean == 0.0
        assert DUT.cost_minimum == 0.0
        assert DUT.cost_ul == 0.0
        assert DUT.cost_variance == 0.0
        assert DUT.date_end == date(2019, 8, 20)
        assert DUT.date_start == date(2019, 7, 21)
        assert DUT.description == 'Test Validation'
        assert DUT.measurement_unit == ''
        assert DUT.name == ''
        assert DUT.status == 0.0
        assert DUT.task_specification == ''
        assert DUT.task_type == ''
        assert DUT.time_average == 0.0
        assert DUT.time_ll == 0.0
        assert DUT.time_maximum == 0.0
        assert DUT.time_mean == 0.0
        assert DUT.time_minimum == 0.0
        assert DUT.time_ul == 0.0
        assert DUT.time_variance == 0.0

    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """ get_attributes() should return a dict of attribute values. """
        DUT = test_program_dao.session.query(RAMSTKValidation).first()

        _attributes = DUT.get_attributes()
        assert _attributes['revision_id'] == 1
        assert _attributes['validation_id'] == 2
        assert _attributes['acceptable_maximum'] == 0.0
        assert _attributes['acceptable_mean'] == 0.0
        assert _attributes['acceptable_minimum'] == 0.0
        assert _attributes['acceptable_variance'] == 0.0
        assert _attributes['confidence'] == 95.0
        assert _attributes['cost_average'] == 0.0
        assert _attributes['cost_ll'] == 0.0
        assert _attributes['cost_maximum'] == 0.0
        assert _attributes['cost_mean'] == 0.0
        assert _attributes['cost_minimum'] == 0.0
        assert _attributes['cost_ul'] == 0.0
        assert _attributes['cost_variance'] == 0.0
        assert _attributes['date_end'] == date(2019, 8, 20)
        assert _attributes['date_start'] == date(2019, 7, 21)
        assert _attributes['description'] == 'Test Validation'
        assert _attributes['measurement_unit'] == ''
        assert _attributes['name'] == ''
        assert _attributes['status'] == 0.0
        assert _attributes['task_specification'] == ''
        assert _attributes['task_type'] == ''
        assert _attributes['time_average'] == 0.0
        assert _attributes['time_ll'] == 0.0
        assert _attributes['time_maximum'] == 0.0
        assert _attributes['time_mean'] == 0.0
        assert _attributes['time_minimum'] == 0.0
        assert _attributes['time_ul'] == 0.0
        assert _attributes['time_variance'] == 0.0

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """ set_attributes() should return a zero error code on success. """
        DUT = test_program_dao.session.query(RAMSTKValidation).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKValidation).first()

        ATTRIBUTES['description'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['description'] == ''

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKValidation).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})

    @pytest.mark.integration
    def test_calculate_task_time(self, test_program_dao):
        """ calculate() returns False on successfully calculating tasks times. """
        DUT = test_program_dao.session.query(RAMSTKValidation).first()

        DUT.time_minimum = 25.2
        DUT.time_average = 36.8
        DUT.time_maximum = 44.1

        assert not DUT.calculate_task_time()
        assert DUT.time_ll == pytest.approx(29.90944678)
        assert DUT.time_mean == pytest.approx(36.08333333)
        assert DUT.time_ul == pytest.approx(42.2572199)
        assert DUT.time_variance == pytest.approx(9.9225)

    @pytest.mark.integration
    def test_calculate_task_cost(self, test_program_dao):
        """ calculate() returns False on successfully calculating tasks costs. """
        DUT = test_program_dao.session.query(RAMSTKValidation).first()

        DUT.cost_minimum = 252.00
        DUT.cost_average = 368.00
        DUT.cost_maximum = 441.00
        DUT.confidence = 0.95

        assert not DUT.calculate_task_cost()
        assert DUT.cost_ll == pytest.approx(299.09446782)
        assert DUT.cost_mean == pytest.approx(360.83333333)
        assert DUT.cost_ul == pytest.approx(422.5721988)
        assert DUT.cost_variance == pytest.approx(992.25)
