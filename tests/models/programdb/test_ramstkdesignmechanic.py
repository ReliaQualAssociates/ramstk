# -*- coding: utf-8 -*-
#
#       tests.dao.programdb.test_ramstkdesignmechanic.py is part of The RAMSTK
#       Project
#
# All rights reserved.
"""Test class for testing the RAMSTKDesignMechanic module algorithms and models. """

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKDesignMechanic

ATTRIBUTES = {
    'pressure_upstream': 0.0,
    'frequency_operating': 0.0,
    'surface_finish': 0.0,
    'friction': 0.0,
    'length_compressed': 0.0,
    'load_id': 0,
    'n_cycles': 0,
    'balance_id': 0,
    'lubrication_id': 0,
    'water_per_cent': 0.0,
    'misalignment_angle': 0.0,
    'type_id': 0,
    'rpm_design': 0.0,
    'pressure_downstream': 0.0,
    'diameter_coil': 0.0,
    'manufacturing_id': 0,
    'pressure_contact': 0.0,
    'meyer_hardness': 0.0,
    'rpm_operating': 0.0,
    'length_relaxed': 0.0,
    'impact_id': 0,
    'n_ten': 0,
    'material_id': 0,
    'technology_id': 0,
    'service_id': 0,
    'flow_design': 0.0,
    'application_id': 0,
    'diameter_wire': 0.0,
    'deflection': 0.0,
    'filter_size': 0.0,
    'diameter_inner': 0.0,
    'pressure_rated': 0.0,
    'altitude_operating': 0.0,
    'thickness': 0.0,
    'diameter_outer': 0.0,
    'n_elements': 0,
    'contact_pressure': 0.0,
    'particle_size': 0.0,
    'casing_id': 0,
    'viscosity_dynamic': 0.0,
    'viscosity_design': 0.0,
    'torque_id': 0,
    'leakage_allowable': 0.0,
    'offset': 0.0,
    'width_minimum': 0.0,
    'load_operating': 0.0,
    'spring_index': 0.0,
    'flow_operating': 0.0,
    'pressure_delta': 0.0,
    'length': 0.0,
    'load_design': 0.0,
    'clearance': 0.0
}


@pytest.mark.integration
def test_ramstkdesignmechanic_create(test_dao):
    """ __init__() should create an RAMSTKDesignMechanic model. """
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignMechanic).first()

    assert isinstance(DUT, RAMSTKDesignMechanic)

    # Verify class attributes are properly initialized.
    assert DUT.__tablename__ == 'ramstk_design_mechanic'
    assert DUT.hardware_id == 1
    assert DUT.altitude_operating == 0.0
    assert DUT.application_id == 0
    assert DUT.balance_id == 0
    assert DUT.clearance == 0.0
    assert DUT.casing_id == 0
    assert DUT.contact_pressure == 0.0
    assert DUT.deflection == 0.0
    assert DUT.diameter_coil == 0.0
    assert DUT.diameter_inner == 0.0
    assert DUT.diameter_outer == 0.0
    assert DUT.diameter_wire == 0.0
    assert DUT.filter_size == 0.0
    assert DUT.flow_design == 0.0
    assert DUT.flow_operating == 0.0
    assert DUT.frequency_operating == 0.0
    assert DUT.friction == 0.0
    assert DUT.impact_id == 0
    assert DUT.leakage_allowable == 0.0
    assert DUT.length == 0.0
    assert DUT.length_compressed == 0.0
    assert DUT.length_relaxed == 0.0
    assert DUT.load_design == 0.0
    assert DUT.load_id == 0
    assert DUT.load_operating == 0.0
    assert DUT.lubrication_id == 0
    assert DUT.manufacturing_id == 0
    assert DUT.material_id == 0
    assert DUT.meyer_hardness == 0.0
    assert DUT.misalignment_angle == 0.0
    assert DUT.n_ten == 0
    assert DUT.n_cycles == 0
    assert DUT.n_elements == 0
    assert DUT.offset == 0.0
    assert DUT.particle_size == 0.0
    assert DUT.pressure_contact == 0.0
    assert DUT.pressure_delta == 0.0
    assert DUT.pressure_downstream == 0.0
    assert DUT.pressure_rated == 0.0
    assert DUT.pressure_upstream == 0.0
    assert DUT.rpm_design == 0.0
    assert DUT.rpm_operating == 0.0
    assert DUT.service_id == 0
    assert DUT.spring_index == 0.0
    assert DUT.surface_finish == 0.0
    assert DUT.technology_id == 0
    assert DUT.thickness == 0.0
    assert DUT.torque_id == 0
    assert DUT.type_id == 0
    assert DUT.viscosity_design == 0.0
    assert DUT.viscosity_dynamic == 0.0
    assert DUT.water_per_cent == 0.0
    assert DUT.width_minimum == 0.0


@pytest.mark.integration
def test_get_attributes(test_dao):
    """ get_attributes() should return a tuple of attribute values. """
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignMechanic).first()

    _attributes = DUT.get_attributes()
    assert isinstance(_attributes, dict)
    assert _attributes['pressure_upstream'] == 0.0
    assert _attributes['frequency_operating'] == 0.0
    assert _attributes['surface_finish'] == 0.0
    assert _attributes['friction'] == 0.0
    assert _attributes['length_compressed'] == 0.0
    assert _attributes['load_id'] == 0
    assert _attributes['n_cycles'] == 0
    assert _attributes['balance_id'] == 0
    assert _attributes['lubrication_id'] == 0
    assert _attributes['water_per_cent'] == 0.0
    assert _attributes['misalignment_angle'] == 0.0
    assert _attributes['type_id'] == 0
    assert _attributes['rpm_design'] == 0.0
    assert _attributes['pressure_downstream'] == 0.0
    assert _attributes['diameter_coil'] == 0.0
    assert _attributes['manufacturing_id'] == 0
    assert _attributes['pressure_contact'] == 0.0
    assert _attributes['meyer_hardness'] == 0.0
    assert _attributes['rpm_operating'] == 0.0
    assert _attributes['length_relaxed'] == 0.0
    assert _attributes['impact_id'] == 0
    assert _attributes['n_ten'] == 0
    assert _attributes['material_id'] == 0
    assert _attributes['technology_id'] == 0
    assert _attributes['service_id'] == 0
    assert _attributes['flow_design'] == 0.0
    assert _attributes['application_id'] == 0
    assert _attributes['diameter_wire'] == 0.0
    assert _attributes['deflection'] == 0.0
    assert _attributes['filter_size'] == 0.0
    assert _attributes['diameter_inner'] == 0.0
    assert _attributes['pressure_rated'] == 0.0
    assert _attributes['hardware_id'] == 1
    assert _attributes['altitude_operating'] == 0.0
    assert _attributes['thickness'] == 0.0
    assert _attributes['diameter_outer'] == 0.0
    assert _attributes['n_elements'] == 0
    assert _attributes['contact_pressure'] == 0.0
    assert _attributes['particle_size'] == 0.0
    assert _attributes['casing_id'] == 0
    assert _attributes['viscosity_dynamic'] == 0.0
    assert _attributes['viscosity_design'] == 0.0
    assert _attributes['torque_id'] == 0
    assert _attributes['leakage_allowable'] == 0.0
    assert _attributes['offset'] == 0.0
    assert _attributes['width_minimum'] == 0.0
    assert _attributes['load_operating'] == 0.0
    assert _attributes['spring_index'] == 0.0
    assert _attributes['flow_operating'] == 0.0
    assert _attributes['pressure_delta'] == 0.0
    assert _attributes['length'] == 0.0
    assert _attributes['load_design'] == 0.0
    assert _attributes['clearance'] == 0.0


@pytest.mark.integration
def test_set_attributes(test_dao):
    """ set_attributes() should return a zero error code on success. """
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignMechanic).first()

    assert DUT.set_attributes(ATTRIBUTES) is None


@pytest.mark.integration
def test_set_attributes_none_value(test_dao):
    """set_attributes() should set an attribute to it's default value when the attribute is passed with a None value."""
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignMechanic).first()

    ATTRIBUTES['type_id'] = None

    assert DUT.set_attributes(ATTRIBUTES) is None
    assert DUT.get_attributes()['type_id'] == 0.0


@pytest.mark.integration
def test_set_attributes_unknown_attributes(test_dao):
    """set_attributes() should raise an AttributeError when passed an unknown attribute."""
    _session = test_dao.RAMSTK_SESSION(bind=test_dao.engine,
                                       autoflush=False,
                                       expire_on_commit=False)
    DUT = _session.query(RAMSTKDesignMechanic).first()

    with pytest.raises(AttributeError):
        DUT.set_attributes({'shibboly-bibbly-boo': 0.9998})
