# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.models.programdb.test_ramstkallocation.py is part of The RAMSTK
#       Project
#
# All rights reserved.
""" Test class for testing RAMSTKAllocation module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKAllocation

ATTRIBUTES = {
    'availability_alloc': 0.9998,
    'duty_cycle': 100.0,
    'env_factor': 6,
    'goal_measure_id': 1,
    'hazard_rate_alloc': 0.0,
    'hazard_rate_goal': 0.0,
    'included': 1,
    'int_factor': 3,
    'allocation_method_id': 1,
    'mission_time': 100.0,
    'mtbf_alloc': 0.0,
    'mtbf_goal': 0.0,
    'n_sub_systems': 3,
    'n_sub_elements': 3,
    'parent_id': 1,
    'percent_weight_factor': 0.8,
    'reliability_alloc': 0.99975,
    'reliability_goal': 0.999,
    'op_time_factor': 5,
    'soa_factor': 2,
    'weight_factor': 1
}


@pytest.mark.usefixtures('test_program_dao')
class TestRAMSTKAllocation():
    """Class for testing the RAMSTKAllocation model."""
    @pytest.mark.integration
    def test_ramstkallocation_create(self, test_program_dao):
        """__init__() should create an RAMSTKAllocation model."""
        DUT = test_program_dao.session.query(RAMSTKAllocation).first()

        assert isinstance(DUT, RAMSTKAllocation)

        # Verify class attributes are properly initialized.  Commented attribute
        # values vary depending on whether this test file is run stand-alone or as
        # a result of python setup.py test.
        assert DUT.__tablename__ == 'ramstk_allocation'
        assert DUT.revision_id == 1
        assert DUT.hardware_id == 1
        assert DUT.availability_alloc == 0.0
        assert DUT.duty_cycle == 100.0
        assert DUT.env_factor == 1
        assert DUT.goal_measure_id == 1
        assert DUT.hazard_rate_alloc == 0.0
        assert DUT.hazard_rate_goal == 0.0
        assert DUT.included == 1
        assert DUT.int_factor == 1
        assert DUT.allocation_method_id == 1
        # assert DUT.mission_time == 100.0
        assert DUT.mtbf_alloc == 0.0
        assert DUT.mtbf_goal == 0.0
        assert DUT.n_sub_systems == 1
        assert DUT.n_sub_elements == 1
        assert DUT.parent_id == 0
        assert DUT.percent_weight_factor == 0.0
        assert DUT.reliability_alloc == 1.0
        assert DUT.reliability_goal == 1.0
        assert DUT.op_time_factor == 1
        assert DUT.soa_factor == 1
        assert DUT.weight_factor == 1


    @pytest.mark.integration
    def test_get_attributes(self, test_program_dao):
        """get_attributes() should return a dict of attribute values."""
        DUT = test_program_dao.session.query(RAMSTKAllocation).first()

        _attributes = DUT.get_attributes()

        assert isinstance(_attributes, dict)

        assert _attributes['hardware_id'] == 1
        assert _attributes['availability_alloc'] == 0.0
        assert _attributes['duty_cycle'] == 100.0
        assert _attributes['env_factor'] == 1
        assert _attributes['goal_measure_id'] == 1
        assert _attributes['hazard_rate_alloc'] == 0.0
        assert _attributes['hazard_rate_goal'] == 0.0
        assert _attributes['included'] == 1
        assert _attributes['int_factor'] == 1
        assert _attributes['allocation_method_id'] == 1
        # assert _attributes['mission_time'] == 100.0
        assert _attributes['mtbf_alloc'] == 0.0
        assert _attributes['mtbf_goal'] == 0.0
        assert _attributes['n_sub_systems'] == 1
        assert _attributes['n_sub_elements'] == 1
        assert _attributes['parent_id'] == 0
        assert _attributes['percent_weight_factor'] == 0.0
        assert _attributes['reliability_alloc'] == 1.0
        assert _attributes['reliability_goal'] == 1.0
        assert _attributes['op_time_factor'] == 1
        assert _attributes['soa_factor'] == 1
        assert _attributes['weight_factor'] == 1

    @pytest.mark.integration
    def test_set_attributes(self, test_program_dao):
        """set_attributes() should return None on success."""
        DUT = test_program_dao.session.query(RAMSTKAllocation).first()

        assert DUT.set_attributes(ATTRIBUTES) is None

    @pytest.mark.integration
    def test_set_attributes_none_value(self, test_program_dao):
        """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
        DUT = test_program_dao.session.query(RAMSTKAllocation).first()

        ATTRIBUTES['reliability_alloc'] = None

        assert DUT.set_attributes(ATTRIBUTES) is None
        assert DUT.get_attributes()['reliability_alloc'] == 1.0

    @pytest.mark.integration
    def test_set_attributes_unknown_attributes(self, test_program_dao):
        """set_attributes() should raise an AttributeError when passed an unknown attribute."""
        DUT = test_program_dao.session.query(RAMSTKAllocation).first()

        with pytest.raises(AttributeError):
            DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
