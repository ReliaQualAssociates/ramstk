# pylint: disable=protected-access
# -*- coding: utf-8 -*-
#
#       tests.modules.hardware.test_hardwarebom.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for testing Hardware BoM module algorithms and models. """

# Third Party Imports
import pytest
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers.hardware import amHardware, dmHardware, mmHardware
from ramstk.dao import DAO
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKReliability
)

ATTRIBUTES = {
    'revision_id': 1,
    'hardware_id': 1,
    'alt_part_number': '',
    'attachments': '',
    'cage_code': '',
    'category_id': 0,
    'comp_ref_des': 'S1',
    'cost': 0.0,
    'cost_failure': 0.0,
    'cost_hour': 0.0,
    'cost_type_id': 0,
    'description': 'Test System',
    'duty_cycle': 100.0,
    'figure_number': '',
    'lcn': '',
    'level': 0,
    'manufacturer_id': 0,
    'mission_time': 100.0,
    'name': '',
    'nsn': '',
    'page_number': '',
    'parent_id': 0,
    'part': 0,
    'part_number': '',
    'quantity': 1,
    'ref_des': 'S1',
    'remarks': b'',
    'repairable': 0,
    'specification_number': '',
    'subcategory_id': 0,
    'tagged_part': 0,
    'total_cost': 0.0,
    'total_part_count': 0,
    'total_power_dissipation': 0.0,
    'year_of_manufacture': 2019,
    'application_id': 0,
    'area': 0.0,
    'capacitance': 0.0,
    'configuration_id': 0,
    'construction_id': 0,
    'contact_form_id': 0,
    'contact_gauge': 0,
    'contact_rating_id': 0,
    'current_operating': 0.0,
    'current_rated': 0.0,
    'current_ratio': 0.0,
    'environment_active_id': 0,
    'environment_dormant_id': 0,
    'family_id': 0,
    'feature_size': 0.0,
    'frequency_operating': 0.0,
    'insert_id': 0,
    'insulation_id': 0,
    'manufacturing_id': 0,
    'matching_id': 0,
    'n_active_pins': 0,
    'n_circuit_planes': 1,
    'n_cycles': 0,
    'n_elements': 0,
    'n_hand_soldered': 0,
    'n_wave_soldered': 0,
    'operating_life': 0.0,
    'overstress': 0,
    'package_id': 0,
    'power_operating': 0.0,
    'power_rated': 0.0,
    'power_ratio': 0.0,
    'reason': b'',
    'resistance': 0.0,
    'specification_id': 0,
    'technology_id': 0,
    'temperature_active': 35.0,
    'temperature_case': 0.0,
    'temperature_dormant': 25.0,
    'temperature_hot_spot': 0.0,
    'temperature_junction': 0.0,
    'temperature_knee': 25.0,
    'temperature_rated_max': 0.0,
    'temperature_rated_min': 0.0,
    'temperature_rise': 0.0,
    'theta_jc': 0.0,
    'type_id': 0,
    'voltage_ac_operating': 0.0,
    'voltage_dc_operating': 0.0,
    'voltage_esd': 0.0,
    'voltage_rated': 0.0,
    'voltage_ratio': 0.0,
    'weight': 0.0,
    'years_in_production': 1,
    'altitude_operating': 0.0,
    'balance_id': 0,
    'clearance': 0.0,
    'casing_id': 0,
    'contact_pressure': 0.0,
    'deflection': 0.0,
    'diameter_coil': 0.0,
    'diameter_inner': 0.0,
    'diameter_outer': 0.0,
    'diameter_wire': 0.0,
    'filter_size': 0.0,
    'flow_design': 0.0,
    'flow_operating': 0.0,
    'friction': 0.0,
    'impact_id': 0,
    'leakage_allowable': 0.0,
    'length': 0.0,
    'length_compressed': 0.0,
    'length_relaxed': 0.0,
    'load_design': 0.0,
    'load_id': 0,
    'load_operating': 0.0,
    'lubrication_id': 0,
    'material_id': 0,
    'meyer_hardness': 0.0,
    'misalignment_angle': 0.0,
    'n_ten': 0,
    'offset': 0.0,
    'particle_size': 0.0,
    'pressure_contact': 0.0,
    'pressure_delta': 0.0,
    'pressure_downstream': 0.0,
    'pressure_rated': 0.0,
    'pressure_upstream': 0.0,
    'rpm_design': 0.0,
    'rpm_operating': 0.0,
    'service_id': 0,
    'spring_index': 0.0,
    'surface_finish': 0.0,
    'thickness': 0.0,
    'torque_id': 0,
    'viscosity_design': 0.0,
    'viscosity_dynamic': 0.0,
    'water_per_cent': 0.0,
    'width_minimum': 0.0,
    'A1': 0.0,
    'A2': 0.0,
    'B1': 0.0,
    'B2': 0.0,
    'C1': 0.0,
    'C2': 0.0,
    'lambdaBD': 0.0,
    'lambdaBP': 0.0,
    'lambdaCYC': 0.0,
    'lambdaEOS': 0.0,
    'piA': 0.0,
    'piC': 0.0,
    'piCD': 0.0,
    'piCF': 0.0,
    'piCR': 0.0,
    'piCV': 0.0,
    'piCYC': 0.0,
    'piE': 0.0,
    'piF': 0.0,
    'piI': 0.0,
    'piK': 0.0,
    'piL': 0.0,
    'piM': 0.0,
    'piMFG': 0.0,
    'piN': 0.0,
    'piNR': 0.0,
    'piP': 0.0,
    'piPT': 0.0,
    'piQ': 0.0,
    'piR': 0.0,
    'piS': 0.0,
    'piT': 0.0,
    'piTAPS': 0.0,
    'piU': 0.0,
    'piV': 0.0,
    'Cac': 0.0,
    'Calt': 0.0,
    'Cb': 0.0,
    'Cbl': 0.0,
    'Cbt': 0.0,
    'Cbv': 0.0,
    'Cc': 0.0,
    'Ccf': 0.0,
    'Ccp': 0.0,
    'Ccs': 0.0,
    'Ccv': 0.0,
    'Ccw': 0.0,
    'Cd': 0.0,
    'Cdc': 0.0,
    'Cdl': 0.0,
    'Cdp': 0.0,
    'Cds': 0.0,
    'Cdt': 0.0,
    'Cdw': 0.0,
    'Cdy': 0.0,
    'Ce': 0.0,
    'Cf': 0.0,
    'Cg': 0.0,
    'Cga': 0.0,
    'Cgl': 0.0,
    'Cgp': 0.0,
    'Cgs': 0.0,
    'Cgt': 0.0,
    'Cgv': 0.0,
    'Ch': 0.0,
    'Ci': 0.0,
    'Ck': 0.0,
    'Cl': 0.0,
    'Clc': 0.0,
    'Cm': 0.0,
    'Cmu': 0.0,
    'Cn': 0.0,
    'Cnp': 0.0,
    'Cnw': 0.0,
    'Cp': 0.0,
    'Cpd': 0.0,
    'Cpf': 0.0,
    'Cpv': 0.0,
    'Cq': 0.0,
    'Cr': 0.0,
    'Crd': 0.0,
    'Cs': 0.0,
    'Csc': 0.0,
    'Csf': 0.0,
    'Cst': 0.0,
    'Csv': 0.0,
    'Csw': 0.0,
    'Csz': 0.0,
    'Ct': 0.0,
    'Cv': 0.0,
    'Cw': 0.0,
    'Cy': 0.0,
    'add_adj_factor': 0.0,
    'availability_logistics': 1.0,
    'availability_mission': 1.0,
    'avail_log_variance': 0.0,
    'avail_mis_variance': 0.0,
    'failure_distribution_id': 0,
    'hazard_rate_active': 0.0,
    'hazard_rate_dormant': 0.0,
    'hazard_rate_logistics': 0.0,
    'hazard_rate_method_id': 0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_model': '',
    'hazard_rate_percent': 0.0,
    'hazard_rate_software': 0.0,
    'hazard_rate_specified': 0.0,
    'hazard_rate_type_id': 0,
    'hr_active_variance': 0.0,
    'hr_dormant_variance': 0.0,
    'hr_logistics_variance': 0.0,
    'hr_mission_variance': 0.0,
    'hr_specified_variance': 0.0,
    'lambda_b': 0.0,
    'location_parameter': 0.0,
    'mtbf_logistics': 0.0,
    'mtbf_mission': 0.0,
    'mtbf_specified': 0.0,
    'mtbf_logistics_variance': 0.0,
    'mtbf_mission_variance': 0.0,
    'mtbf_specified_variance': 0.0,
    'mult_adj_factor': 1.0,
    'quality_id': 0,
    'reliability_goal': 0.0,
    'reliability_goal_measure_id': 0,
    'reliability_logistics': 1.0,
    'reliability_mission': 1.0,
    'reliability_log_variance': 0.0,
    'reliability_miss_variance': 0.0,
    'scale_parameter': 0.0,
    'shape_parameter': 0.0,
    'survival_analysis_id': 0
}


@pytest.mark.integration
def test_data_manager_create(test_dao):
    """__init__() should return a Hardware data manager."""
    DUT = dmHardware(test_dao)

    assert isinstance(DUT, dmHardware)
    assert isinstance(DUT.tree, Tree)
    assert isinstance(DUT.dao, DAO)
    assert DUT._tag == 'hardware'
    assert DUT._root == 0


@pytest.mark.integration
def test_do_select_all(test_dao):
    """do_select_all() should return a Tree() object populated with RAMSTKHardware instances on success."""
    dmHardware(test_dao)

    def on_message(tree):
        assert isinstance(tree, Tree)
        assert isinstance(tree.get_node(1).data['hardware'], RAMSTKHardware)
        assert isinstance(
            tree.get_node(1).data['design_electric'], RAMSTKDesignElectric)
        assert isinstance(
            tree.get_node(1).data['design_mechanic'], RAMSTKDesignMechanic)
        assert isinstance(
            tree.get_node(1).data['mil_hdbk_217f'], RAMSTKMilHdbkF)
        assert isinstance(tree.get_node(1).data['nswc'], RAMSTKNSWC)
        assert isinstance(
            tree.get_node(1).data['reliability'], RAMSTKReliability)

    pub.subscribe(on_message, 'succeed_retrieve_hardware')

    pub.sendMessage('succeed_select_revision', revision_id=1)


@pytest.mark.integration
def test_do_select_design_electric(test_dao):
    """do_select() should return an instance of the RAMSTKDesignElectric on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(1, table='design_electric')

    assert isinstance(_hardware, RAMSTKDesignElectric)
    assert _hardware.application_id == 0
    assert _hardware.power_rated == 0.0


@pytest.mark.integration
def test_do_select_design_mechanic(test_dao):
    """do_select() should return an instance of the RAMSTKDesignMechanic on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(1, table='design_mechanic')

    assert isinstance(_hardware, RAMSTKDesignMechanic)
    assert _hardware.altitude_operating == 0.0
    assert _hardware.impact_id == 0.0


@pytest.mark.integration
def test_do_select_hardware(test_dao):
    """do_select() should return an instance of the RAMSTKHardware on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(1, table='hardware')

    assert isinstance(_hardware, RAMSTKHardware)
    assert _hardware.ref_des == 'S1'
    assert _hardware.cage_code == ''


@pytest.mark.integration
def test_do_select_mil_hdbk_f(test_dao):
    """do_select() should return an instance of the RAMSTKMilHdbkF on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(1, table='mil_hdbk_217f')

    assert isinstance(_hardware, RAMSTKMilHdbkF)
    assert _hardware.piE == 0.0
    assert _hardware.lambdaBD == 0.0


@pytest.mark.integration
def test_do_select_nswc(test_dao):
    """do_select() should return an instance of the RAMSTKNSWC on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(1, table='nswc')

    assert isinstance(_hardware, RAMSTKNSWC)
    assert _hardware.Cac == 0.0
    assert _hardware.Ci == 0.0


@pytest.mark.integration
def test_do_select_reliability(test_dao):
    """do_select() should return an instance of the RAMSTKReliability on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(1, table='reliability')

    assert isinstance(_hardware, RAMSTKReliability)
    assert _hardware.lambda_b == 0.0
    assert _hardware.reliability_goal == 0.0


@pytest.mark.integration
def test_do_select_unknown_table(test_dao):
    """do_select() should raise a KeyError when an unknown table name is requested."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    with pytest.raises(KeyError):
        DUT.do_select(1, table='scibbidy-bibbidy-doo')


@pytest.mark.integration
def test_do_select_non_existent_id(test_dao):
    """do_select() should return None when a non-existent Hardware ID is requested."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    assert DUT.do_select(100, table='hardware') is None


@pytest.mark.integration
def test_do_delete(test_dao):
    """_do_delete() should send the success message with the treelib Tree."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(node_id):
        assert node_id == 8
        assert DUT.last_id == 7

    pub.subscribe(on_message, 'succeed_delete_hardware')

    pub.sendMessage('request_delete_hardware', node_id=DUT.last_id)


@pytest.mark.integration
def test_do_delete_non_existent_id(test_dao):
    """_do_delete() should send the fail message."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(error_msg):
        assert error_msg == 'Attempted to delete non-existent hardware ID 300.'

    pub.subscribe(on_message, 'fail_delete_hardware')

    DUT._do_delete(300)


@pytest.mark.integration
def test_do_insert_sibling_assembly(test_dao):
    """do_insert() should send the success message after successfully inserting a new sibling hardware assembly."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(node_id):
        assert node_id == 8
        assert isinstance(
            DUT.tree.get_node(node_id).data['hardware'], RAMSTKHardware)
        assert isinstance(
            DUT.tree.get_node(node_id).data['design_electric'],
            RAMSTKDesignElectric)
        assert isinstance(
            DUT.tree.get_node(node_id).data['design_mechanic'],
            RAMSTKDesignMechanic)
        assert isinstance(
            DUT.tree.get_node(node_id).data['mil_hdbk_217f'], RAMSTKMilHdbkF)
        assert isinstance(DUT.tree.get_node(node_id).data['nswc'], RAMSTKNSWC)
        assert isinstance(
            DUT.tree.get_node(node_id).data['reliability'], RAMSTKReliability)
        assert DUT.tree.get_node(node_id).data['hardware'].revision_id == 1
        assert DUT.tree.get_node(node_id).data['hardware'].parent_id == 1
        assert DUT.tree.get_node(node_id).data['hardware'].part == 0

    pub.subscribe(on_message, 'succeed_insert_hardware')

    pub.sendMessage('request_insert_hardware', parent_id=1, part=0)


@pytest.mark.integration
def test_do_insert_child_assembly(test_dao):
    """do_insert() should send the success message after successfully inserting a new child hardware assembly."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(node_id):
        assert node_id == 9
        assert isinstance(
            DUT.tree.get_node(node_id).data['hardware'], RAMSTKHardware)
        assert isinstance(
            DUT.tree.get_node(node_id).data['design_electric'],
            RAMSTKDesignElectric)
        assert isinstance(
            DUT.tree.get_node(node_id).data['design_mechanic'],
            RAMSTKDesignMechanic)
        assert isinstance(
            DUT.tree.get_node(node_id).data['mil_hdbk_217f'], RAMSTKMilHdbkF)
        assert isinstance(DUT.tree.get_node(node_id).data['nswc'], RAMSTKNSWC)
        assert isinstance(
            DUT.tree.get_node(node_id).data['reliability'], RAMSTKReliability)
        assert DUT.tree.get_node(node_id).data['hardware'].revision_id == 1
        assert DUT.tree.get_node(node_id).data['hardware'].parent_id == 8
        assert DUT.tree.get_node(node_id).data['hardware'].part == 0

    pub.subscribe(on_message, 'succeed_insert_hardware')

    assert DUT.do_insert(parent_id=8, part=0) is None


@pytest.mark.integration
def test_do_insert_part(test_dao):
    """do_insert() should send the success message after successfully inserting a new hardware part."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(node_id):
        assert node_id == 10
        assert isinstance(
            DUT.tree.get_node(node_id).data['hardware'], RAMSTKHardware)
        assert isinstance(
            DUT.tree.get_node(node_id).data['design_electric'],
            RAMSTKDesignElectric)
        assert isinstance(
            DUT.tree.get_node(node_id).data['design_mechanic'],
            RAMSTKDesignMechanic)
        assert isinstance(
            DUT.tree.get_node(node_id).data['mil_hdbk_217f'], RAMSTKMilHdbkF)
        assert isinstance(DUT.tree.get_node(node_id).data['nswc'], RAMSTKNSWC)
        assert isinstance(
            DUT.tree.get_node(node_id).data['reliability'], RAMSTKReliability)
        assert DUT.tree.get_node(node_id).data['hardware'].revision_id == 1
        assert DUT.tree.get_node(node_id).data['hardware'].parent_id == 9
        assert DUT.tree.get_node(node_id).data['hardware'].part == 1

    pub.subscribe(on_message, 'succeed_insert_hardware')

    assert DUT.do_insert(parent_id=9, part=1) is None


@pytest.mark.integration
def test_do_insert_part_to_part(test_dao):
    """do_insert() should send the fail message when attempting to add a child to a hardware part."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(error_msg):
        assert error_msg == ('Attempting to insert a hardware assembly or '
                             'component/piece part as a child of another '
                             'component/piece part.')

    pub.subscribe(on_message, 'fail_insert_hardware')

    assert DUT.do_insert(parent_id=10, part=1) is None


@pytest.mark.integration
def test_do_update_data_manager(test_dao):
    """ do_update() should return a zero error code on success. """
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(node_id):
        _hardware = DUT.do_select(node_id, table='hardware')
        assert node_id == 10
        assert _hardware.parent_id == 9
        assert _hardware.cost == 0.9832

    pub.subscribe(on_message, 'succeed_update_hardware')

    _hardware = DUT.do_select(10, table='hardware')
    _hardware.cost = 0.9832

    pub.sendMessage('request_update_hardware', node_id=10)


@pytest.mark.integration
def test_do_update_non_existent_id(test_dao):
    """ do_update() should return a non-zero error code when passed a Hardware ID that doesn't exist. """
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(error_msg):
        assert error_msg == ('Attempted to save non-existent hardware item '
                             'with hardware ID 100.')

    pub.subscribe(on_message, 'fail_update_hardware')

    DUT.do_update(100)


@pytest.mark.integration
def test_do_update_all(test_dao):
    """ do_update_all() should return a zero error code on success. """
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(node_id):
        assert DUT.do_select(node_id, table='hardware').hardware_id == node_id

    pub.subscribe(on_message, 'succeed_update_hardware')

    pub.sendMessage('request_update_all_hardware')


@pytest.mark.integration
def test_do_make_comp_ref_des(test_dao):
    """do_make_comp_ref_des() should return a zero error code on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    _hardware = DUT.do_select(8, table='hardware')
    _hardware.ref_des = "SS8"
    _hardware = DUT.do_select(9, table='hardware')
    _hardware.ref_des = "A9"
    _hardware = DUT.do_select(10, table='hardware')
    _hardware.ref_des = "C1"

    pub.sendMessage('request_make_comp_ref_des', node_id=1)

    assert DUT.do_select(8, table='hardware').comp_ref_des == 'S1:SS8'
    assert DUT.do_select(9, table='hardware').comp_ref_des == 'S1:SS8:A9'
    assert DUT.do_select(10, table='hardware').comp_ref_des == 'S1:SS8:A9:C1'


@pytest.mark.integration
def test_do_get_attributes_hardware(test_dao):
    """do_get_attributes() should return a dict of hardware attributes on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(attributes):
        assert isinstance(attributes, dict)
        assert attributes['hardware_id'] == 10
        assert attributes['ref_des'] == 'C1'
        assert attributes['comp_ref_des'] == 'S1:SS8:A9:C1'

    pub.subscribe(on_message, 'succeed_get_hardware_attributes')

    pub.sendMessage('request_get_hardware_attributes',
                    node_id=10,
                    table='hardware')


@pytest.mark.integration
def test_do_get_all_attributes_data_manager(test_dao):
    """do_get_all_attributes() should return a dict of all RAMSTK data tables' attributes on success."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    def on_message(attributes):
        assert isinstance(attributes, dict)
        assert attributes['hardware_id'] == 10
        assert attributes['ref_des'] == 'C1'
        assert attributes['comp_ref_des'] == 'S1:SS8:A9:C1'
        assert attributes['application_id'] == 0
        assert attributes['piE'] == 0.0
        assert attributes['hazard_rate_active'] == 0.0

    pub.subscribe(on_message, 'succeed_get_all_hardware_attributes')

    pub.sendMessage('request_get_all_hardware_attributes', node_id=10)


@pytest.mark.integration
def test_do_set_attributes(test_dao):
    """do_set_attributes() should send the success message."""
    DUT = dmHardware(test_dao)
    DUT.do_select_all(revision_id=1)

    pub.sendMessage('request_set_hardware_attributes',
                    node_id=10,
                    key='name',
                    value='Testing set name from moduleview.')
    assert DUT.do_select(
        10, table='hardware').name == 'Testing set name from moduleview.'

    pub.sendMessage('request_set_hardware_attributes',
                    node_id=10,
                    key='lambdaBD',
                    value=0.003862)
    assert DUT.do_select(10, table='mil_hdbk_217f').lambdaBD == 0.003862


@pytest.mark.integration
def test_analysis_manager_create(test_configuration):
    """__init__() should create an instance of the hardware analysis manager."""
    DUT = amHardware(test_configuration)

    assert isinstance(DUT, amHardware)
    assert isinstance(DUT._attributes, dict)
    assert DUT._attributes == {}
    assert DUT._tree is None


@pytest.mark.integration
def test_get_all_attributes_analysis_manager(test_dao, test_configuration):
    """_get_all_attributes() should update the attributes dict on success."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    pub.sendMessage('request_get_all_hardware_attributes', node_id=1)

    assert DUT._attributes == ATTRIBUTES


@pytest.mark.integration
def test_do_calculate_assembly_specified_hazard_rate(test_dao,
                                                     test_configuration):
    """do_calculate() should calculate reliability metrics and update the _attributes dict with results when specifying the h(t)."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(attributes):
        assert DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER == '1000000.0'
        assert attributes['hazard_rate_type_id'] == 2
        assert attributes['hazard_rate_active'] == pytest.approx(3.1095e-06)
        assert attributes['hazard_rate_dormant'] == 2.3876e-08
        assert attributes['hazard_rate_software'] == 3.876e-07
        assert attributes['hazard_rate_logistics'] == pytest.approx(
            3.520976e-06)
        assert attributes['mtbf_logistics'] == pytest.approx(284012.16026465)
        assert attributes['reliability_logistics'] == pytest.approx(0.02957056)
        assert attributes['hazard_rate_mission'] == pytest.approx(3.4971e-06)
        assert attributes['mtbf_mission'] == pytest.approx(285951.21672243)
        assert attributes['reliability_mission'] == pytest.approx(0.99996479)
        assert attributes['hr_specified_variance'] == pytest.approx(
            5.70063376e-12)
        assert attributes['hr_logistics_variance'] == pytest.approx(
            1.2397272e-11)
        assert attributes['hr_mission_variance'] == pytest.approx(
            1.22297084e-11)
        assert attributes['mtbf_logistics_variance'] == 80662907178.19547
        assert attributes['mtbf_mission_variance'] == 81768098345.03651
        assert attributes['total_part_count'] == 10
        assert attributes['total_power_dissipation'] == 0.0
        assert attributes['cost_type_id'] == 2
        assert attributes['total_cost'] == 5.28
        assert attributes['cost_hour'] == pytest.approx(1.8464688e-05)

    pub.subscribe(on_message, 'succeed_calculate_hardware')

    DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 2)
    DATAMGR.do_set_attributes(1, 'hazard_rate_specified', 2.3876)
    DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.023876)
    DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.3876)
    DATAMGR.do_set_attributes(1, 'add_adj_factor', 0.1)
    DATAMGR.do_set_attributes(1, 'mult_adj_factor', 1.25)
    DATAMGR.do_set_attributes(1, 'mission_time', 10.0)
    DATAMGR.do_set_attributes(1, 'quantity', 1)
    DATAMGR.do_set_attributes(1, 'cost_type_id', 2)
    DATAMGR.do_set_attributes(1, 'cost', 5.28)
    DATAMGR.do_set_attributes(1, 'total_part_count', 10)

    pub.sendMessage('request_calculate_hardware', node_id=1)


@pytest.mark.integration
def test_do_calculate_assembly_specified_mtbf(test_dao, test_configuration):
    """do_calculate() should calculate reliability metrics and update the _attributes dict with results when specifying the MTBF."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(attributes):
        assert DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER == '1000000.0'
        assert attributes['hazard_rate_type_id'] == 3
        assert attributes['hazard_rate_active'] == pytest.approx(
            3.50877193e-06)
        assert attributes['hazard_rate_dormant'] == 0.0
        assert attributes['hazard_rate_software'] == 0.0
        assert attributes['hazard_rate_logistics'] == pytest.approx(
            3.50877193e-06)
        assert attributes['mtbf_logistics'] == 285000.0
        assert attributes['reliability_logistics'] == pytest.approx(
            0.029933652)
        assert attributes['hazard_rate_mission'] == pytest.approx(
            3.50877193e-06)
        assert attributes['mtbf_mission'] == 285000.0
        assert attributes['reliability_mission'] == pytest.approx(0.99996479)
        assert attributes['mtbf_specified_variance'] == 81225000000.0

    pub.subscribe(on_message, 'succeed_calculate_hardware')

    DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 3)
    DATAMGR.do_set_attributes(1, 'mtbf_specified', 285000.0)
    DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.0)
    DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.0)
    DATAMGR.do_set_attributes(1, 'add_adj_factor', 0.0)
    DATAMGR.do_set_attributes(1, 'mult_adj_factor', 1.0)
    DATAMGR.do_set_attributes(1, 'mission_time', 10.0)

    pub.sendMessage('request_calculate_hardware', node_id=1)


@pytest.mark.integration
def test_do_calculate_assembly_zero_hazard_rates(test_dao, test_configuration):
    """do_calculate() should send the fail message when all hazard rates=0.0."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    amHardware(test_configuration)

    def on_message(error_msg):
        assert error_msg == ("Failed to calculate hazard rate and/or MTBF "
                             "metrics for hardware ID 1; too many inputs "
                             "equal to zero.  Specified MTBF=285000.000000, "
                             "active h(t)=0.000000, dormant h(t)=0.000000, "
                             "and software h(t)=0.000000.")

    pub.subscribe(on_message, 'fail_calculate_hardware')

    DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 2)
    DATAMGR.do_set_attributes(1, 'hazard_rate_specified', 0.0)
    DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.0)
    DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.0)

    pub.sendMessage('request_calculate_hardware', node_id=1)


@pytest.mark.integration
def test_do_calculate_assembly_zero_specified_mtbf(test_dao,
                                                   test_configuration):
    """do_calculate() should send the fail message when the specified MTBF=0.0."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    amHardware(test_configuration)

    def on_message(error_msg):
        assert error_msg == ("Failed to calculate hazard rate and/or MTBF "
                             "metrics for hardware ID 1; too many inputs "
                             "equal to zero.  Specified MTBF=0.000000, active "
                             "h(t)=0.000000, dormant h(t)=0.000000, and "
                             "software h(t)=0.000000.")

    pub.subscribe(on_message, 'fail_calculate_hardware')

    DATAMGR.do_set_attributes(1, 'hazard_rate_type_id', 3)
    DATAMGR.do_set_attributes(1, 'mtbf_specified', 0.0)
    DATAMGR.do_set_attributes(1, 'hazard_rate_dormant', 0.0)
    DATAMGR.do_set_attributes(1, 'hazard_rate_software', 0.0)

    pub.sendMessage('request_calculate_hardware', node_id=1)


@pytest.mark.integration
def test_do_calculate_part_mil_hdbk_217f_parts_count(test_dao,
                                                     test_configuration):
    """do_calculate() should calculate reliability metrics and update the _attributes dict with results when performing a MIL-HDBK-217F parts count prediction."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(attributes):
        assert DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER == '1000000.0'
        assert attributes['hazard_rate_type_id'] == 1
        assert attributes['hazard_rate_method_id'] == 1
        assert attributes['hazard_rate_active'] == pytest.approx(9.75e-09)
        assert attributes['hazard_rate_dormant'] == 7.8e-10
        assert attributes['hazard_rate_software'] == 3.876e-07
        assert attributes['hazard_rate_logistics'] == pytest.approx(3.9813e-07)
        assert attributes['mtbf_logistics'] == pytest.approx(2511742.3956999)
        assert attributes['reliability_logistics'] == pytest.approx(0.67157472)
        assert attributes['hazard_rate_mission'] == pytest.approx(3.9735e-07)
        assert attributes['mtbf_mission'] == pytest.approx(2516672.95834906)
        assert attributes['reliability_mission'] == pytest.approx(0.99999603)
        assert attributes['hr_specified_variance'] == 0.0
        assert attributes['hr_logistics_variance'] == pytest.approx(
            1.77431343e-13)
        assert attributes['hr_mission_variance'] == pytest.approx(
            1.57887023e-13)
        assert attributes['mtbf_logistics_variance'] == 6308849862356.259
        assert attributes['mtbf_mission_variance'] == 6333642779285.422
        assert attributes['total_part_count'] == 1
        assert attributes['total_power_dissipation'] == 0.05
        assert attributes['cost_type_id'] == 2
        assert attributes['total_cost'] == 5.28
        assert attributes['cost_hour'] == pytest.approx(2.098008e-06)

    pub.subscribe(on_message, 'succeed_calculate_hardware')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 1)
    DATAMGR.do_set_attributes(10, 'category_id', 1)
    DATAMGR.do_set_attributes(10, 'subcategory_id', 1)
    DATAMGR.do_set_attributes(10, 'quality_id', 1)
    DATAMGR.do_set_attributes(10, 'environment_active_id', 3)
    DATAMGR.do_set_attributes(10, 'environment_dormant_id', 2)
    DATAMGR.do_set_attributes(10, 'n_elements', 100)
    DATAMGR.do_set_attributes(10, 'power_operating', 0.05)
    DATAMGR.do_set_attributes(10, 'hazard_rate_software', 0.3876)
    DATAMGR.do_set_attributes(10, 'add_adj_factor', 0.0)
    DATAMGR.do_set_attributes(10, 'mult_adj_factor', 1.0)
    DATAMGR.do_set_attributes(10, 'mission_time', 10.0)
    DATAMGR.do_set_attributes(10, 'quantity', 1)
    DATAMGR.do_set_attributes(10, 'cost_type_id', 2)
    DATAMGR.do_set_attributes(10, 'cost', 5.28)
    DATAMGR.do_update(10)

    pub.sendMessage('request_calculate_hardware', node_id=10)


@pytest.mark.integration
def test_do_calculate_part_mil_hdbk_217f_parts_stress(test_dao,
                                                      test_configuration):
    """do_calculate() should calculate reliability metrics and update the _attributes dict with results when performing a MIL-HDBK-217F part stress prediction."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(attributes):
        assert DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER == '1000000.0'
        assert attributes['hazard_rate_type_id'] == 1
        assert attributes['hazard_rate_method_id'] == 2
        assert attributes['voltage_ratio'] == 0.5344
        assert attributes['hazard_rate_active'] == pytest.approx(
            2.75691476e-07)
        assert attributes['hazard_rate_dormant'] == pytest.approx(
            2.75691476e-08)
        assert attributes['hazard_rate_software'] == 0.0
        assert attributes['hazard_rate_logistics'] == pytest.approx(
            3.03260624e-07)
        assert attributes['mtbf_logistics'] == pytest.approx(3297493.71115455)
        assert attributes['reliability_logistics'] == pytest.approx(0.73840662)
        assert attributes['hazard_rate_mission'] == pytest.approx(
            2.75691476e-07)
        assert attributes['mtbf_mission'] == pytest.approx(3627243.08227001)
        assert attributes['reliability_mission'] == pytest.approx(0.99999712)
        assert attributes['hr_specified_variance'] == 0.0
        assert attributes['hr_logistics_variance'] == pytest.approx(
            1.77431343e-13)
        assert attributes['hr_mission_variance'] == pytest.approx(
            1.57887023e-13)
        assert attributes['mtbf_logistics_variance'] == 10873464775103.824
        assert attributes['mtbf_mission_variance'] == 13156892377875.629
        assert attributes['total_part_count'] == 1
        assert attributes['total_power_dissipation'] == 0.05
        assert attributes['cost_type_id'] == 2
        assert attributes['total_cost'] == 1.35
        assert attributes['cost_hour'] == pytest.approx(3.7218349e-07)

    pub.subscribe(on_message, 'succeed_calculate_hardware')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 2)
    DATAMGR.do_set_attributes(10, 'category_id', 4)
    DATAMGR.do_set_attributes(10, 'subcategory_id', 1)
    DATAMGR.do_set_attributes(10, 'quality_id', 1)
    DATAMGR.do_set_attributes(10, 'environment_active_id', 3)
    DATAMGR.do_set_attributes(10, 'environment_dormant_id', 2)
    DATAMGR.do_set_attributes(10, 'capacitance', 0.0000033)
    DATAMGR.do_set_attributes(10, 'construction_id', 1)
    DATAMGR.do_set_attributes(10, 'configuration_id', 1)
    DATAMGR.do_set_attributes(10, 'resistance', 0.05)
    DATAMGR.do_set_attributes(10, 'voltage_dc_operating', 3.3)
    DATAMGR.do_set_attributes(10, 'voltage_ac_operating', 0.04)
    DATAMGR.do_set_attributes(10, 'voltage_rated', 6.25)
    DATAMGR.do_set_attributes(10, 'temperature_rated_max', 105.0)
    DATAMGR.do_set_attributes(10, 'temperature_active', 45.0)
    DATAMGR.do_set_attributes(10, 'power_operating', 0.05)
    DATAMGR.do_set_attributes(10, 'hazard_rate_software', 0.0)
    DATAMGR.do_set_attributes(10, 'add_adj_factor', 0.0)
    DATAMGR.do_set_attributes(10, 'mult_adj_factor', 1.0)
    DATAMGR.do_set_attributes(10, 'mission_time', 10.0)
    DATAMGR.do_set_attributes(10, 'quantity', 1)
    DATAMGR.do_set_attributes(10, 'cost_type_id', 2)
    DATAMGR.do_set_attributes(10, 'cost', 1.35)
    DATAMGR.do_update(10)

    pub.sendMessage('request_calculate_hardware', node_id=10)


@pytest.mark.integration
def test_do_calculate_part_zero_rated_current(test_dao, test_configuration):
    """do_calculate() should send the stress ratio calculation fail message when rated current is zero."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    amHardware(test_configuration)

    def on_message(error_msg):
        assert error_msg == ('Failed to calculate current ratio for hardware '
                             'ID 10; rated current is zero.')

    pub.subscribe(on_message, 'fail_stress_analysis')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 2)
    DATAMGR.do_set_attributes(10, 'category_id', 1)
    DATAMGR.do_set_attributes(10, 'current_operating', 0.005)
    DATAMGR.do_set_attributes(10, 'current_rated', 0.0)


@pytest.mark.integration
def test_do_calculate_part_zero_rated_power(test_dao, test_configuration):
    """do_calculate() should send the stress ratio calculation fail message when rated power is zero."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    amHardware(test_configuration)

    def on_message(error_msg):
        assert error_msg == ('Failed to calculate power ratio for hardware '
                             'ID 10; rated power is zero.')

    pub.subscribe(on_message, 'fail_stress_analysis')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 2)
    DATAMGR.do_set_attributes(10, 'category_id', 3)
    DATAMGR.do_set_attributes(10, 'power_operating', 0.05)
    DATAMGR.do_set_attributes(10, 'power_rated', 0.0)

    pub.sendMessage('request_calculate_hardware', node_id=10)

    pub.sendMessage('request_calculate_hardware', node_id=10)


@pytest.mark.integration
def test_do_calculate_part_zero_rated_voltage(test_dao, test_configuration):
    """do_calculate() should send the stress ratio calculation fail message when rated voltage is zero."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    amHardware(test_configuration)

    def on_message(error_msg):
        assert error_msg == ('Failed to calculate voltage ratio for hardware '
                             'ID 10; rated voltage is zero.')

    pub.subscribe(on_message, 'fail_stress_analysis')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 2)
    DATAMGR.do_set_attributes(10, 'category_id', 4)
    DATAMGR.do_set_attributes(10, 'voltage_dc_operating', 3.3)
    DATAMGR.do_set_attributes(10, 'voltage_ac_operating', 0.04)
    DATAMGR.do_set_attributes(10, 'voltage_rated', 0.0)

    pub.sendMessage('request_calculate_hardware', node_id=10)


@pytest.mark.integration
def test_do_derating_analysis_current_stress(test_dao, test_configuration):
    """do_derating_analysis() should set overstress attribute True and build reason message when a component is current overstressed."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(attributes):
        assert DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER == '1000000.0'
        assert attributes['overstress']
        assert attributes['reason'] == (b'Operating current is greater than '
                                        b'limit in a harsh environment.\n'
                                        b'Operating current is greater than '
                                        b'limit in a mild environment.\n')

    pub.subscribe(on_message, 'succeed_derate_hardware')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 2)
    DATAMGR.do_set_attributes(10, 'category_id', 8)
    DATAMGR.do_set_attributes(10, 'current_ratio', 0.95)
    DATAMGR.do_update(10)

    pub.sendMessage('request_derate_hardware', node_id=10)


@pytest.mark.integration
def test_do_derating_analysis_power_stress(test_dao, test_configuration):
    """do_derating_analysis() should set overstress attribute True and build reason message when a component is power overstressed."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(attributes):
        assert DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER == '1000000.0'
        assert attributes['overstress']
        assert attributes['reason'] == (b'Operating power is greater than '
                                        b'limit in a harsh environment.\n'
                                        b'Operating power is greater than '
                                        b'limit in a mild environment.\n')

    pub.subscribe(on_message, 'succeed_derate_hardware')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 2)
    DATAMGR.do_set_attributes(10, 'category_id', 3)
    DATAMGR.do_set_attributes(10, 'power_ratio', 0.95)
    DATAMGR.do_update(10)

    pub.sendMessage('request_derate_hardware', node_id=10)


@pytest.mark.integration
def test_do_derating_analysis_voltage_stress(test_dao, test_configuration):
    """do_derating_analysis() should set overstress attribute True and build reason message when a component is voltage overstressed."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(attributes):
        assert DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER == '1000000.0'
        assert attributes['overstress']
        assert attributes['reason'] == (b'Operating voltage is greater than '
                                        b'limit in a harsh environment.\n'
                                        b'Operating voltage is greater than '
                                        b'limit in a mild environment.\n')

    pub.subscribe(on_message, 'succeed_derate_hardware')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 2)
    DATAMGR.do_set_attributes(10, 'category_id', 4)
    DATAMGR.do_set_attributes(10, 'voltage_ratio', 0.95)
    DATAMGR.do_update(10)

    pub.sendMessage('request_derate_hardware', node_id=10)


@pytest.mark.integration
def test_do_derating_analysis_no_overstress(test_dao, test_configuration):
    """do_derating_analysis() should set overstress attribute False and the reason message should='' when a component is not overstressed."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(attributes):
        assert DUT.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER == '1000000.0'
        assert not attributes['overstress']
        assert attributes['reason'] == b''

    pub.subscribe(on_message, 'succeed_derate_hardware')

    DATAMGR.do_set_attributes(10, 'hazard_rate_type_id', 1)
    DATAMGR.do_set_attributes(10, 'hazard_rate_method_id', 2)
    DATAMGR.do_set_attributes(10, 'category_id', 4)
    DATAMGR.do_set_attributes(10, 'current_ratio', 0.45)
    DATAMGR.do_set_attributes(10, 'power_ratio', 0.35)
    DATAMGR.do_set_attributes(10, 'voltage_ratio', 0.5344)
    DATAMGR.do_update(10)

    pub.sendMessage('request_derate_hardware', node_id=10)


@pytest.mark.integration
def test_on_get_tree(test_dao, test_configuration):
    """_on_get_tree() should assign the data manager's tree to the _tree attribute in response to the succeed_get_hardware_tree message."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(tree):
        assert isinstance(tree, Tree)
        assert isinstance(DUT._tree, Tree)
        assert DUT._tree == tree
        assert isinstance(DUT._tree.get_node(1).data['nswc'], RAMSTKNSWC)

    pub.subscribe(on_message, 'succeed_get_hardware_tree')

    pub.sendMessage('request_get_hardware_tree')


@pytest.mark.integration
def test_do_calculate_all_hardware(test_dao, test_configuration):
    """do_calculate_all_hardware() should calculate the entire system and roll-up results from child to parent hardware items."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = amHardware(test_configuration)

    def on_message(module_tree):
        assert isinstance(module_tree, Tree)
        assert DUT._attributes['hazard_rate_active'] == pytest.approx(
            3.77515059e-05)
        assert DUT._attributes['hazard_rate_dormant'] == pytest.approx(
            3.10691476e-08)
        assert DUT._attributes['hazard_rate_software'] == 2.345e-06
        assert DUT._attributes['total_cost'] == 3993.61
        assert DUT._attributes['total_part_count'] == 313
        assert DUT._attributes['total_power_dissipation'] == pytest.approx(
            63.877)

    pub.subscribe(on_message, 'succeed_calculate_all_hardware')

    # Do a couple of assemblies with a specified h(t)
    DATAMGR.do_set_attributes(5, 'hazard_rate_type_id', 2)
    DATAMGR.do_set_attributes(5, 'hazard_rate_specified', 0.15)
    DATAMGR.do_set_attributes(5, 'hazard_rate_dormant', 0.0035)
    DATAMGR.do_set_attributes(5, 'total_part_count', 89)
    DATAMGR.do_set_attributes(5, 'total_power_dissipation', 45.89)
    DATAMGR.do_set_attributes(5, 'cost', 438.19)
    DATAMGR.do_update(5)

    DATAMGR.do_set_attributes(6, 'hazard_rate_type_id', 2)
    DATAMGR.do_set_attributes(6, 'hazard_rate_specified', 0.045)
    DATAMGR.do_set_attributes(6, 'hazard_rate_software', 2.3)
    DATAMGR.do_set_attributes(6, 'total_part_count', 132)
    DATAMGR.do_set_attributes(6, 'total_power_dissipation', 12.3)
    DATAMGR.do_set_attributes(6, 'cost', 832.98)
    DATAMGR.do_update(6)

    # Do a couple of assemblies with a specified MTBF
    DATAMGR.do_set_attributes(3, 'hazard_rate_type_id', 3)
    DATAMGR.do_set_attributes(3, 'mtbf_specified', 38292)
    DATAMGR.do_set_attributes(3, 'hazard_rate_software', 0.045)
    DATAMGR.do_set_attributes(3, 'total_part_count', 55)
    DATAMGR.do_set_attributes(3, 'total_power_dissipation', 4.67)
    DATAMGR.do_set_attributes(3, 'cost', 1282.95)
    DATAMGR.do_update(3)

    DATAMGR.do_set_attributes(7, 'hazard_rate_type_id', 3)
    DATAMGR.do_set_attributes(7, 'mtbf_specified', 89560)
    DATAMGR.do_set_attributes(7, 'total_part_count', 26)
    DATAMGR.do_set_attributes(7, 'total_power_dissipation', 0.967)
    DATAMGR.do_set_attributes(7, 'cost', 1432.86)
    DATAMGR.do_update(7)

    pub.sendMessage('request_calculate_all_hardware')


@pytest.mark.integration
def test_matrix_manager_create(test_dao):
    """__init__() should create an instance of the hardware matrix manager."""
    DUT = mmHardware(test_dao)

    assert isinstance(DUT, mmHardware)
    assert isinstance(DUT.dao, DAO)
    assert isinstance(DUT._column_tables, dict)
    assert isinstance(DUT._col_tree, Tree)
    assert isinstance(DUT._row_tree, Tree)
    assert DUT.dic_matrices == {}
    assert DUT.dic_column_hdrs == {}
    assert DUT.dic_row_hdrs == {}
    assert DUT.dic_matrices == {}
    assert DUT.n_row == 1
    assert DUT.n_col == 1


@pytest.mark.integration
def test_do_create_matrix(test_dao):
    """_do_create() should create an instance of the hardware matrix manager."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = mmHardware(test_dao)
    DUT._col_tree.create_node(tag='requirements',
                              identifier=0,
                              parent=None,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0001',
                              identifier=1,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='FUNC-0001',
                              identifier=2,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0002',
                              identifier=3,
                              parent=0,
                              data=None)

    pub.sendMessage('succeed_select_revision', revision_id=1)

    assert DUT.do_select('hrdwr_rqrmnt', 1, 0) == 'REL-0001'
    assert DUT.do_select('hrdwr_rqrmnt', 2, 0) == 'FUNC-0001'
    assert DUT.do_select('hrdwr_rqrmnt', 3, 0) == 'REL-0002'
    assert DUT.do_select('hrdwr_rqrmnt', 1, 1) == 2


@pytest.mark.integration
def test_do_delete_row(test_dao):
    """do_delete_row() should remove the appropriate row from the hardware matrices."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = mmHardware(test_dao)
    DUT._col_tree.create_node(tag='requirements',
                              identifier=0,
                              parent=None,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0001',
                              identifier=1,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='FUNC-0001',
                              identifier=2,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0002',
                              identifier=3,
                              parent=0,
                              data=None)

    pub.sendMessage('succeed_select_revision', revision_id=1)

    assert DUT.do_select('hrdwr_rqrmnt', 1, 10) == 0

    pub.sendMessage('succeed_delete_hardware', node_id=10)

    with pytest.raises(KeyError):
        DUT.do_select('hrdwr_rqrmnt', 1, 10)


@pytest.mark.integration
def test_do_delete_matrix_column(test_dao):
    """do_delete_column() should remove the appropriate column from the requested hardware matrix."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = mmHardware(test_dao)
    DUT._col_tree.create_node(tag='requirements',
                              identifier=0,
                              parent=None,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0001',
                              identifier=1,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='FUNC-0001',
                              identifier=2,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0002',
                              identifier=3,
                              parent=0,
                              data=None)

    pub.sendMessage('succeed_select_revision', revision_id=1)

    assert DUT.do_select('hrdwr_rqrmnt', 1, 1) == 2

    pub.sendMessage('succeed_delete_requirement', node_id=1)

    with pytest.raises(KeyError):
        DUT.do_select('hrdwr_rqrmnt', 1, 1)

@pytest.mark.integration
def test_do_insert_row(test_dao):
    """do_insert_row() should add a row to the end of each hardware matrix."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = mmHardware(test_dao)
    DUT._col_tree.create_node(tag='requirements',
                              identifier=0,
                              parent=None,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0001',
                              identifier=1,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='FUNC-0001',
                              identifier=2,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0002',
                              identifier=3,
                              parent=0,
                              data=None)

    pub.sendMessage('succeed_select_revision', revision_id=1)

    with pytest.raises(KeyError):
        DUT.do_select('hrdwr_rqrmnt', 1, 11)

    pub.sendMessage('succeed_insert_hardware', node_id=11)

    assert DUT.do_select('hrdwr_rqrmnt', 1, 11) == 0


@pytest.mark.integration
def test_do_insert_column(test_dao):
    """do_insert_column() should add a column to the right of the requested hardware matrix."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = mmHardware(test_dao)
    DUT._col_tree.create_node(tag='requirements',
                              identifier=0,
                              parent=None,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0001',
                              identifier=1,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='FUNC-0001',
                              identifier=2,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0002',
                              identifier=3,
                              parent=0,
                              data=None)

    pub.sendMessage('succeed_select_revision', revision_id=1)

    with pytest.raises(KeyError):
        DUT.do_select('hrdwr_rqrmnt', 4, 10)

    pub.sendMessage('succeed_insert_requirement', node_id=6)

    assert DUT.do_select('hrdwr_rqrmnt', 6, 10) == 0


@pytest.mark.integration
def test_do_update_analysis_manager(test_dao):
    """do_update() should ."""
    DATAMGR = dmHardware(test_dao)
    DATAMGR.do_select_all(revision_id=1)
    DUT = mmHardware(test_dao)
    DUT._col_tree.create_node(tag='requirements',
                              identifier=0,
                              parent=None,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0001',
                              identifier=1,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='FUNC-0001',
                              identifier=2,
                              parent=0,
                              data=None)
    DUT._col_tree.create_node(tag='REL-0002',
                              identifier=3,
                              parent=0,
                              data=None)

    def on_message():
        assert True

    pub.subscribe(on_message, 'succeed_update_matrix')

    pub.sendMessage('succeed_select_revision', revision_id=1)

    DUT.dic_matrices['hrdwr_rqrmnt'][1][2] = 1
    DUT.dic_matrices['hrdwr_rqrmnt'][1][3] = 2
    DUT.dic_matrices['hrdwr_rqrmnt'][2][2] = 2
    DUT.dic_matrices['hrdwr_rqrmnt'][3][5] = 1

    pub.sendMessage('request_update_hardware_matrix',
                    revision_id=1,
                    matrix_type='hrdwr_rqrmnt')
