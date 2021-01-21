# -*- coding: utf-8 -*-
#
#       ramstk.exim.imports.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Import module."""

# Standard Library Imports
import inspect
import math
from collections import OrderedDict
from datetime import date
from typing import Any, Dict

# Third Party Imports
# noinspection PyPackageRequirements
import numpy as np
# noinspection PyPackageRequirements
import pandas as pd
# noinspection PyPackageRequirements
from dateutil import parser
from pubsub import pub

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKAllocation, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKFunction, RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKReliability,
    RAMSTKRequirement, RAMSTKSimilarItem, RAMSTKValidation
)


def _do_replace_nan(value: Any, default: Any) -> Any:
    """Check for NaN values and replace any with the default value.

    :param value: the value to check for NaN.
    :param default: the default value to replace NaN.
    :return: _value; the passed value or the default if the passed value
        was NaN.
    """
    _value = value

    # Check for Python NaN's.
    try:
        if math.isnan(value):
            _value = default
    # Non-numeric values raise a type error, so we can just move along.
    except TypeError:
        pass

    # Check for numpy NaN's.
    if value is np.nan:
        _value = default

    return _value


def _get_input_value(mapper: Dict[str, Any], df_row: pd.Series, field: str,
                     default: Any) -> Any:
    """Retrieve the input value for a field from the Pandas dataframe.

    :param mapper: the field mapping dict to use as the Rosetta stone.
    :param df_row: the row from the pandas DataFrame containing the input
        data.
    :param field: the name of the RAMSTK database field to retrieve the
        data for.
    :param default: the default value to assign to the field.
    :return: _value
    :rtype: the value of the requested input field or the default.
    """
    try:
        _value = df_row.at[mapper[field]]
    except KeyError:
        _value = default

    _value = _do_replace_nan(_value, default)

    # If it's supposed to be a date, make it a date.
    if default == date.today():
        _value = parser.parse(_value)

    return _value


class Import:
    """Contains the methods for importing data to a program database."""

    # Ordered dictionaries of RAMSTK inputs field headers.  Must use
    # OrderedDict to ensure they are always in the same order during program
    # flow.
    _dic_field_map = {
        'Function':
        OrderedDict([('Revision ID', ''), ('Function ID', ''), ('Level', ''),
                     ('Function Code', ''), ('Function Name', ''),
                     ('Parent', ''), ('Remarks', ''), ('Safety Critical', ''),
                     ('Type', '')]),
        'Requirement':
        OrderedDict([('Revision ID', ''), ('Requirement ID', ''),
                     ('Derived?', ''), ('Requirement', ''),
                     ('Figure Number', ''), ('Owner', ''), ('Page Number', ''),
                     ('Parent ID', ''), ('Priority', ''),
                     ('Requirement Code', ''), ('Specification', ''),
                     ('Requirement Type', ''), ('Validated?', ''),
                     ('Validated Date', '')]),
        'Hardware':
        OrderedDict([('Revision ID', ''), ('Hardware ID', ''),
                     ('Alternate Part Number', ''), ('CAGE Code', ''),
                     ('Category ID', ''), ('Composite Ref. Des.', ''),
                     ('Cost', ''), ('Cost Type', ''), ('Description', ''),
                     ('Duty Cycle', ''), ('Figure Number', ''), ('LCN', ''),
                     ('Level', ''), ('Manufacturer', ''), ('Mission Time', ''),
                     ('Name', ''), ('NSN', ''), ('Page Number', ''),
                     ('Parent Assembly', ''), ('Part', ''),
                     ('Part Number', ''), ('Quantity', ''),
                     ('Reference Designator', ''), ('Remarks', ''),
                     ('Repairable', ''), ('Specification', ''),
                     ('Subcategory ID', ''), ('Tagged Part', ''),
                     ('Year of Manufacture', '')]),
        'Design Electric':
        OrderedDict([('Hardware ID', ''), ('Application ID', ''), ('Area', ''),
                     ('Capacitance', ''), ('Configuration ID', ''),
                     ('Construction ID', ''), ('Contact Form ID', ''),
                     ('Contact Gauge', ''), ('Contact Rating ID', ''),
                     ('Current Operating', ''), ('Current Rated', ''),
                     ('Current Ratio', ''), ('Environment Active ID', ''),
                     ('Environment Dormant ID', ''), ('Family ID', ''),
                     ('Feature Size', ''), ('Frequency Operating', ''),
                     ('Insert ID', ''), ('Insulation ID', ''),
                     ('Manufacturing ID', ''), ('Matching ID', ''),
                     ('N Active Pins', ''), ('N Circuit Planes', ''),
                     ('N Cycles', ''), ('N Elements', ''),
                     ('N Hand Soldered', ''), ('N Wave Soldered', ''),
                     ('Operating Life', ''), ('Overstress', ''),
                     ('Package ID', ''), ('Power Operating', ''),
                     ('Power Rated', ''), ('Power Ratio', ''), ('Reason', ''),
                     ('Resistance', ''), ('Specification ID', ''),
                     ('Technology ID', ''), ('Temperature, Active', ''),
                     ('Temperature, Case', ''), ('Temperature, Dormant', ''),
                     ('Temperature, Hot Spot', ''),
                     ('Temperature, Junction', ''), ('Temperature, Knee', ''),
                     ('Temperature, Rated Max', ''),
                     ('Temperature, Rated Min', ''), ('Temperature Rise', ''),
                     ('Theta JC', ''), ('Type ID', ''),
                     ('Voltage, AC Operating', ''),
                     ('Voltage, DC Operating', ''), ('Voltage ESD', ''),
                     ('Voltage, Rated', ''), ('Voltage Ratio', ''),
                     ('Weight', ''), ('Years in Production', '')]),
        'Design Mechanic':
        OrderedDict([('Hardware ID', ''), ('Altitude, Operating', ''),
                     ('Application ID', ''), ('Balance ID', ''),
                     ('Clearance', ''), ('Casing ID', ''),
                     ('Contact Pressure', ''), ('Deflection', ''),
                     ('Diameter, Coil', ''), ('Diameter, Inner', ''),
                     ('Diameter, Outer', ''), ('Diameter, Wire', ''),
                     ('Filter Size', ''), ('Flow, Design', ''),
                     ('Flow, Operating', ''), ('Frequency, Operating', ''),
                     ('Friction', ''), ('Impact ID', ''),
                     ('Allowable Leakage', ''), ('Length', ''),
                     ('Length, Compressed', ''), ('Length, Relaxed', ''),
                     ('Design Load', ''), ('Load ID', ''),
                     ('Operating Load', ''), ('Lubrication ID', ''),
                     ('Manufacturing ID', ''), ('Material ID', ''),
                     ('Meyer Hardness', ''), ('Misalignment Angle', ''),
                     ('N Ten', ''), ('N Cycles', ''), ('N Elements', ''),
                     ('Offset', ''), ('Particle Size', ''),
                     ('Contact Pressure', ''), ('Differential Pressure', ''),
                     ('Downstream Pressure', ''), ('Rated Pressure', ''),
                     ('Upstream Pressure', ''), ('Design RPM', ''),
                     ('Operating RPM', ''), ('Service ID', ''),
                     ('Spring Index', ''), ('Surface Finish', ''),
                     ('Technology ID', ''), ('Thickness', ''),
                     ('Torque ID', ''), ('Type ID', ''),
                     ('Design Viscosity', ''), ('Dynamic Viscosity', ''),
                     ('% Water', ''), ('Minimum Width', '')]),
        'Reliability':
        OrderedDict([('Hardware ID', ''), ('Additive Adjustment Factor', ''),
                     ('Failure Distribution ID', ''),
                     ('Failure Rate Method ID', ''),
                     ('Failure Rate Model', ''),
                     ('Specified Failure Rate', ''),
                     ('Failure Rate Type ID', ''), ('Location Parameter', ''),
                     ('Specified MTBF', ''),
                     ('Multiplicative Adjustment Factor', ''),
                     ('Quality ID', ''), ('Reliability Goal', ''),
                     ('Reliability Goal Measure ID', ''),
                     ('Scale Parameter', ''), ('Shape Parameter', ''),
                     ('Survival Analysis ID', '')]),
        'Validation':
        OrderedDict([('Revision ID', ''), ('Validation ID', ''),
                     ('Acceptable Maximum', ''), ('Acceptable Mean', ''),
                     ('Acceptable Minimum', ''), ('Acceptable Variance', ''),
                     ('s-Confidence', ''), ('Average Task Cost', ''),
                     ('Maximum Task Cost', ''), ('Minimum Task Cost', ''),
                     ('Start Date', ''), ('End Date', ''),
                     ('Task Description', ''), ('Unit of Measure', ''),
                     ('Name', ''), ('Task Status', ''), ('Task Type', ''),
                     ('Task Specification', ''), ('Average Task Time', ''),
                     ('Maximum Task Time', ''), ('Minimum Task Time', '')])
    }

    def __init__(self) -> None:
        """Initialize an ImportProject module instance."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dao: BaseDatabase = BaseDatabase()
        self._df_input_data: pd.DataFrame = pd.DataFrame({})

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_connect, 'succeed_connect_program_database')
        pub.subscribe(self._do_map_to_field, 'request_map_to_field')
        pub.subscribe(self._do_read_db_fields, 'request_db_fields')
        pub.subscribe(self._do_read_file, 'request_read_import_file')
        pub.subscribe(self._do_import, 'request_import')

    def _do_connect(self, dao: BaseDatabase) -> None:
        """Connect data manager to a database.

        :param dao: the BaseDatabase() instance (data access object)
            representing the connected RAMSTK Program database.
        """
        self._dao = dao

    def _do_import(self, module: str) -> None:
        """Insert a new entity to the RAMSTK db with values from external file.

        :param module: the name of the RAMSTK module to import.
        :return: None
        :rtype: None
        """
        _entities = []

        # pylint: disable=unused-variable
        for __, _row in self._df_input_data.iterrows():
            if module == 'Function':
                _entity = self._do_insert_function(_row)
                _entities.append(_entity)
            elif module == 'Requirement':
                _entity = self._do_insert_requirement(_row)
                _entities.append(_entity)
            elif module == 'Hardware':
                _entity = self._do_insert_hardware(_row)
                _entities.append(_entity)
                _entity = self._do_insert_allocation(_row)
                _entities.append(_entity)
                _entity = self._do_insert_similar_item(_row)
                _entities.append(_entity)
                _entity = self._do_insert_design_electric(_row)
                _entities.append(_entity)
                _entity = self._do_insert_mil_hdbk_f(_row)
                _entities.append(_entity)
                _entity = self._do_insert_design_mechanic(_row)
                _entities.append(_entity)
                _entity = self._do_insert_nswc(_row)
                _entities.append(_entity)
                _entity = self._do_insert_reliability(_row)
                _entities.append(_entity)
            elif module == 'Validation':
                _entity = self._do_insert_validation(_row)
                _entities.append(_entity)

        try:
            self._dao.do_insert_many(_entities)  # type: ignore
            pub.sendMessage(
                'succeed_import_module',
                module=module,
            )
        except (AttributeError, DataAccessError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: There was a problem importing {0} records.  '
                'This is usually caused by key violations; check the '
                'ID and/or parent ID fields in the import file.').format(
                    module, _method_name)
            pub.sendMessage(
                'fail_import_module',
                error_message=_error_msg,
            )

    def _do_insert_allocation(self, row: pd.Series) -> RAMSTKAllocation:
        """Insert a new Allocation record to the RAMSTK database.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _allocation; an instance of the RAMSTKAllocation database
            table record.
        :rtype: :class:`ramstk.models.programdb.RAMSTKAllocation`
        """
        _allocation = RAMSTKAllocation()
        _map = self._dic_field_map['Hardware']

        _allocation.revision_id = _get_input_value(_map, row, 'Revision ID', 1)
        _allocation.hardware_id = _get_input_value(_map, row, 'Hardware ID', 1)
        _allocation.parent_id = _get_input_value(_map, row, 'Parent Assembly',
                                                 1)

        return _allocation

    def _do_insert_design_electric(self,
                                   row: pd.Series) -> RAMSTKDesignElectric:
        """Insert a new Design Electric entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.models.programdb.RAMMSTKDesignElectric`
        """
        _design_electric = RAMSTKDesignElectric()

        _map = self._dic_field_map['Hardware']

        _design_electric.hardware_id = _get_input_value(
            _map, row, 'Hardware ID', 1)

        _map = self._dic_field_map['Design Electric']
        _design_electric.set_attributes({
            'application_id':
            _get_input_value(_map, row, 'Application ID', 0),
            'area':
            _get_input_value(_map, row, 'Area', 0.0),
            'capacitance':
            _get_input_value(_map, row, 'Capacitance', 0.000001),
            'configuration_id':
            _get_input_value(_map, row, 'Configuration ID', 0),
            'construction_id':
            _get_input_value(_map, row, 'Construction ID', 0),
            'contact_form_id':
            _get_input_value(_map, row, 'Contact Form ID', 0),
            'contact_gauge':
            _get_input_value(_map, row, 'Contact Gauge', 20),
            'contact_rating_id':
            _get_input_value(_map, row, 'Contact Rating ID', 0),
            'current_operating':
            _get_input_value(_map, row, 'Current Operating', 0.0),
            'current_rated':
            _get_input_value(_map, row, 'Current Rated', 0.0),
            'current_ratio':
            _get_input_value(_map, row, 'Current Ratio', 0.0),
            'environment_active_id':
            _get_input_value(_map, row, 'Environment Active ID', 0),
            'environment_dormant_id':
            _get_input_value(_map, row, 'Environment Dormant ID', 0),
            'family_id':
            _get_input_value(_map, row, 'Family ID', 0),
            'feature_size':
            _get_input_value(_map, row, 'Feature Size', 1.0),
            'frequency_operating':
            _get_input_value(_map, row, 'Frequency Operating', 0.0),
            'insert_id':
            _get_input_value(_map, row, 'Insert ID', 0),
            'insulation_id':
            _get_input_value(_map, row, 'Insulation ID', 0),
            'manufacturing_id':
            _get_input_value(_map, row, 'Manufacturing ID', 0),
            'matching_id':
            _get_input_value(_map, row, 'Matching ID', 0),
            'n_active_pins':
            _get_input_value(_map, row, 'N Active Pins', 0),
            'n_circuit_planes':
            _get_input_value(_map, row, 'N Circuit Planes', 1),
            'n_cycles':
            _get_input_value(_map, row, 'N Cycles', 0),
            'n_elements':
            _get_input_value(_map, row, 'N Elements', 0),
            'n_hand_soldered':
            _get_input_value(_map, row, 'N Hand Soldered', 0),
            'n_wave_soldered':
            _get_input_value(_map, row, 'N Wave Soldered', 0),
            'operating_life':
            _get_input_value(_map, row, 'Operating Life', 0.0),
            'overstress':
            _get_input_value(_map, row, 'Overstress', 0),
            'package_id':
            _get_input_value(_map, row, 'Package ID', 0),
            'power_operating':
            _get_input_value(_map, row, 'Power Operating', 0.0),
            'power_rated':
            _get_input_value(_map, row, 'Power Rated', 0.0),
            'power_ratio':
            _get_input_value(_map, row, 'Power Ratio', 0.0),
            'reason':
            _get_input_value(_map, row, 'Reason', ''),
            'resistance':
            _get_input_value(_map, row, 'Resistance', 0.0),
            'specification_id':
            _get_input_value(_map, row, 'Specification ID', 0),
            'technology_id':
            _get_input_value(_map, row, 'Technology ID', 0),
            'temperature_active':
            _get_input_value(_map, row, 'Temperature, Active', 30.0),
            'temperature_case':
            _get_input_value(_map, row, 'Temperature, Case', 0.0),
            'temperature_dormant':
            _get_input_value(_map, row, 'Temperature, Dormant', 25.0),
            'temperature_hot_spot':
            _get_input_value(_map, row, 'Temperature, Hot Spot', 0.0),
            'temperature_junction':
            _get_input_value(_map, row, 'Temperature, Junction', 0.0),
            'temperature_knee':
            _get_input_value(_map, row, 'Temperature, Knee', 25.0),
            'temperature_rated_max':
            _get_input_value(_map, row, 'Temperature, Rated Max', 0.0),
            'temperature_rated_min':
            _get_input_value(_map, row, 'Temperature, Rated Min', 0.0),
            'temperature_rise':
            _get_input_value(_map, row, 'Temperature Rise', 0.0),
            'theta_jc':
            _get_input_value(_map, row, 'Theta JC', 0.0),
            'type_id':
            _get_input_value(_map, row, 'Type ID', 0),
            'voltage_ac_operating':
            _get_input_value(_map, row, 'Voltage, AC Operating', 0.0),
            'voltage_dc_operating':
            _get_input_value(_map, row, 'Voltage, DC Operating', 0.0),
            'voltage_esd':
            _get_input_value(_map, row, 'Voltage ESD', 0.0),
            'voltage_rated':
            _get_input_value(_map, row, 'Voltage, Rated', 0.0),
            'voltage_ratio':
            _get_input_value(_map, row, 'Voltage Ratio', 0.0),
            'weight':
            _get_input_value(_map, row, 'Weight', 1.0),
            'years_in_production':
            _get_input_value(_map, row, 'Years in Production', 2)
        })

        return _design_electric

    def _do_insert_design_mechanic(self,
                                   row: pd.Series) -> RAMSTKDesignMechanic:
        """Insert a new Design Mechanic entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.models.programdb.RAMMSTKDesignMechanic`
        """
        _design_mechanic = RAMSTKDesignMechanic()

        _map = self._dic_field_map['Hardware']
        _design_mechanic.hardware_id = _get_input_value(
            _map, row, 'Hardware ID', 1)

        _map = self._dic_field_map['Design Mechanic']
        _design_mechanic.set_attributes({
            'altitude_operating':
            _get_input_value(_map, row, 'Altitude, Operating', 0.0),
            'application_id':
            _get_input_value(_map, row, 'Application ID', 0),
            'balance_id':
            _get_input_value(_map, row, 'Balance ID', 0),
            'clearance':
            _get_input_value(_map, row, 'Clearance', 0.0),
            'casing_id':
            _get_input_value(_map, row, 'Casing ID', 0),
            'contact_pressure':
            _get_input_value(_map, row, 'Contact Pressure', 0.0),
            'deflection':
            _get_input_value(_map, row, 'Deflection', 0.0),
            'diameter_coil':
            _get_input_value(_map, row, 'Diameter, Coil', 0.0),
            'diameter_inner':
            _get_input_value(_map, row, 'Diameter, Inner', 0.0),
            'diameter_outer':
            _get_input_value(_map, row, 'Diameter, Outer', 0.0),
            'diameter_wire':
            _get_input_value(_map, row, 'Diameter, Wire', 0.0),
            'filter_size':
            _get_input_value(_map, row, 'Filter Size', 0.0),
            'flow_design':
            _get_input_value(_map, row, 'Flow, Design', 0.0),
            'flow_operating':
            _get_input_value(_map, row, 'Flow, Operating', 0.0),
            'frequency_operating':
            _get_input_value(_map, row, 'Frequency, Operating', 0.0),
            'friction':
            _get_input_value(_map, row, 'Friction', 0.0),
            'impact_id':
            _get_input_value(_map, row, 'Impact ID', 0),
            'leakage_allowable':
            _get_input_value(_map, row, 'Allowable Leakage', 0.0),
            'length':
            _get_input_value(_map, row, 'Length', 0.0),
            'length_compressed':
            _get_input_value(_map, row, 'Length, Compressed', 0.0),
            'length_relaxed':
            _get_input_value(_map, row, 'Length, Relaxed', 0.0),
            'load_design':
            _get_input_value(_map, row, 'Design Load', 0.0),
            'load_id':
            _get_input_value(_map, row, 'Load ID', 0),
            'load_operating':
            _get_input_value(_map, row, 'Operating Load', 0.0),
            'lubrication_id':
            _get_input_value(_map, row, 'Lubrication ID', 0),
            'manufacturing_id':
            _get_input_value(_map, row, 'Manufacturing ID', 0),
            'material_id':
            _get_input_value(_map, row, 'Material ID', 0),
            'meyer_hardness':
            _get_input_value(_map, row, 'Meyer Hardness', 0.0),
            'misalignment_angle':
            _get_input_value(_map, row, 'Misalignment Angle', 0.0),
            'n_ten':
            _get_input_value(_map, row, 'N Ten', 0),
            'n_cycles':
            _get_input_value(_map, row, 'N Cycles', 0.0),
            'n_elements':
            _get_input_value(_map, row, 'N Elements', 0),
            'offset':
            _get_input_value(_map, row, 'Offset', 0.0),
            'particle_size':
            _get_input_value(_map, row, 'Particle Size', 0.0),
            'pressure_contact':
            _get_input_value(_map, row, 'Contact Pressure', 0.0),
            'pressure_delta':
            _get_input_value(_map, row, 'Differential Pressure', 0.0),
            'pressure_downstream':
            _get_input_value(_map, row, 'Downstream Pressure', 0.0),
            'pressure_rated':
            _get_input_value(_map, row, 'Rated Pressure', 0.0),
            'pressure_upstream':
            _get_input_value(_map, row, 'Upstream Pressure', 0.0),
            'rpm_design':
            _get_input_value(_map, row, 'Design RPM', 0.0),
            'rpm_operating':
            _get_input_value(_map, row, 'Operating RPM', 0.0),
            'service_id':
            _get_input_value(_map, row, 'Service ID', 0),
            'spring_index':
            _get_input_value(_map, row, 'Spring Index', 0),
            'surface_finish':
            _get_input_value(_map, row, 'Surface Finish', 0.0),
            'technology_id':
            _get_input_value(_map, row, 'Technology ID', 0),
            'thickness':
            _get_input_value(_map, row, 'Thickness', 0.0),
            'torque_id':
            _get_input_value(_map, row, 'Torque ID', 0),
            'type_id':
            _get_input_value(_map, row, 'Type ID', 0),
            'viscosity_design':
            _get_input_value(_map, row, 'Design Viscosity', 0.0),
            'viscosity_dynamic':
            _get_input_value(_map, row, 'Dynamic Viscosity', 0.0),
            'water_per_cent':
            _get_input_value(_map, row, '% Water', 0.0),
            'width_minimum':
            _get_input_value(_map, row, 'Minimum Width', 0.0)
        })

        return _design_mechanic

    def _do_insert_function(self, row: pd.Series) -> RAMSTKFunction:
        """Insert a new Function entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.models.programdb.ramskfunction.RAMSTKFunction`
        """
        _function = RAMSTKFunction()
        _map = self._dic_field_map['Function']

        _function.revision_id = _get_input_value(_map, row, 'Revision ID', 1)
        _function.function_id = _get_input_value(_map, row, 'Function ID', 1)
        _function.function_code = _get_input_value(_map, row, 'Function Code',
                                                   '')
        _function.level = _get_input_value(_map, row, 'Level', 0)
        _function.name = _get_input_value(_map, row, 'Function Name', '')
        _function.parent_id = _get_input_value(_map, row, 'Parent', 1)
        _function.remarks = _get_input_value(_map, row, 'Remarks', '')
        _function.safety_critical = _get_input_value(_map, row,
                                                     'Safety Critical', 0)
        _function.type_id = _get_input_value(_map, row, 'Type', '')

        return _function

    def _do_insert_hardware(self, row: pd.Series) -> RAMSTKHardware:
        """Insert a new Hardware entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.models.programdb.ramstkhardware.RAMSTKHardware`
        """
        _hardware = RAMSTKHardware()
        _map = self._dic_field_map['Hardware']

        _hardware.revision_id = _get_input_value(_map, row, 'Revision ID', 1)
        _hardware.hardware_id = _get_input_value(_map, row, 'Hardware ID', 1)
        _hardware.alt_part_number = _get_input_value(_map, row,
                                                     'Alternate Part Number',
                                                     '')
        _hardware.cage_code = _get_input_value(_map, row, 'CAGE Code', '')
        _hardware.category_id = _get_input_value(_map, row, 'Category ID', 0)
        _hardware.comp_ref_des = _get_input_value(_map, row,
                                                  'Composite Ref. Des.', '')
        _hardware.cost = _get_input_value(_map, row, 'Cost', 0.0)
        _hardware.cost_type_id = _get_input_value(_map, row, 'Cost Type', 0)
        _hardware.description = _get_input_value(_map, row, 'Description', '')
        _hardware.duty_cycle = _get_input_value(_map, row, 'Duty Cycle', 100.0)
        _hardware.figure_number = _get_input_value(_map, row, 'Figure Number',
                                                   '')
        _hardware.lcn = _get_input_value(_map, row, 'LCN', '')
        _hardware.level = _get_input_value(_map, row, 'Level', 0)
        _hardware.manufacturer_id = _get_input_value(_map, row, 'Manufacturer',
                                                     0)
        _hardware.mission_time = _get_input_value(_map, row, 'Mission Time',
                                                  24.0)
        _hardware.name = _get_input_value(_map, row, 'Name', '')
        _hardware.nsn = _get_input_value(_map, row, 'NSN', '')
        _hardware.page_number = _get_input_value(_map, row, 'Page Number', '')
        _hardware.parent_id = _get_input_value(_map, row, 'Parent Assembly', 1)
        _hardware.part = _get_input_value(_map, row, 'Part', 0)
        _hardware.part_number = _get_input_value(_map, row, 'Part Number', '')
        _hardware.quantity = _get_input_value(_map, row, 'Quantity', 1)
        _hardware.ref_des = _get_input_value(_map, row, 'Reference Designator',
                                             '')
        _hardware.remarks = _get_input_value(_map, row, 'Remarks', '')
        _hardware.repairable = _get_input_value(_map, row, 'Repairable', 1)
        _hardware.specification_number = _get_input_value(
            _map, row, 'Specification', '')
        _hardware.subcategory_id = _get_input_value(_map, row,
                                                    'Subcategory ID', 0)
        _hardware.tagged_part = _get_input_value(_map, row, 'Tagged Part', 0)
        _hardware.year_of_manufacture = _get_input_value(
            _map, row, 'Year of Manufacture', 1900)

        return _hardware

    def _do_insert_mil_hdbk_f(self, row: pd.Series) -> RAMSTKMilHdbkF:
        """Insert a new MIL-HDBK-217F entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.models.programdb.RAMSTKMilHdbkF`
        """
        _mil_hdbk_f = RAMSTKMilHdbkF()

        _map = self._dic_field_map['Hardware']
        _mil_hdbk_f.hardware_id = _get_input_value(_map, row, 'Hardware ID', 1)

        return _mil_hdbk_f

    def _do_insert_nswc(self, row: pd.Series) -> RAMSTKNSWC:
        """Insert a new NSWC entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.models.programdb.ramstknswc.RAMSTKNSWC`
        """
        _nswc = RAMSTKNSWC()

        _map = self._dic_field_map['Hardware']
        _nswc.hardware_id = _get_input_value(_map, row, 'Hardware ID', 1)

        return _nswc

    def _do_insert_reliability(self, row: pd.Series) -> RAMSTKReliability:
        """Insert a new Reliability entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.models.programdb.RAMSTKReliability`
        """
        _reliability = RAMSTKReliability()

        _map = self._dic_field_map['Hardware']
        _reliability.hardware_id = _get_input_value(_map, row, 'Hardware ID',
                                                    1)

        _map = self._dic_field_map['Reliability']
        _reliability.add_adj_factor = _get_input_value(
            _map, row, 'Additive Adjustment Factor', 0.0)
        _reliability.failure_distribution_id = _get_input_value(
            _map, row, 'Failure Distribution ID', 0)
        _reliability.hazard_rate_method_id = _get_input_value(
            _map, row, 'Failure Rate Method ID', 0)
        _reliability.hazard_rate_model = _get_input_value(
            _map, row, 'Failure Rate Model', '')
        _reliability.hazard_rate_specified = _get_input_value(
            _map, row, 'Specified Failure Rate', 0.0)
        _reliability.hazard_rate_type_id = _get_input_value(
            _map, row, 'Failure Rate Type ID', 0)
        _reliability.location_parameter = _get_input_value(
            _map, row, 'Location Parameter', 0.0)
        _reliability.mtbf_specified = _get_input_value(_map, row,
                                                       'Specified MTBF', 0.0)
        _reliability.mult_adj_factor = _get_input_value(
            _map, row, 'Multiplicative Adjustment Factor', 1.0)
        _reliability.quality_id = _get_input_value(_map, row, 'Quality ID', 0)
        _reliability.reliability_goal = _get_input_value(
            _map, row, 'Reliability Goal', 100.0)
        _reliability.reliability_goal_measure_id = _get_input_value(
            _map, row, 'Reliability Goal Measure ID', 0)
        _reliability.scale_parameter = _get_input_value(
            _map, row, 'Scale Parameter', 0.0)
        _reliability.shape_parameter = _get_input_value(
            _map, row, 'Shape Parameter', 0.0)
        _reliability.survival_analysis_id = _get_input_value(
            _map, row, 'Survival Analysis ID', 0)

        return _reliability

    def _do_insert_requirement(self, row: pd.Series) -> RAMSTKRequirement:
        """Insert a new Requirement entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.models.programdb.RAMSTKRequirement`
        """
        _requirement = RAMSTKRequirement()
        _map = self._dic_field_map['Requirement']

        _requirement.revision_id = _get_input_value(_map, row, 'Revision ID',
                                                    1)
        _requirement.requirement_id = _get_input_value(_map, row,
                                                       'Requirement ID', 1)
        _requirement.derived = _get_input_value(_map, row, 'Derived?', 0)
        _requirement.description = _get_input_value(_map, row, 'Requirement',
                                                    '')
        _requirement.figure_number = _get_input_value(_map, row,
                                                      'Figure Number', '')
        _requirement.owner = _get_input_value(_map, row, 'Owner', '')
        _requirement.page_number = _get_input_value(_map, row, 'Page Number',
                                                    '')
        _requirement.parent_id = _get_input_value(_map, row, 'Parent ID', 1)
        _requirement.priority = _get_input_value(_map, row, 'Priority', 1)
        _requirement.requirement_code = _get_input_value(
            _map, row, 'Requirement Code', '')
        _requirement.specification = _get_input_value(_map, row,
                                                      'Specification', '')
        _requirement.requirement_type = _get_input_value(
            _map, row, 'Requirement Type', '')
        _requirement.validated = _get_input_value(_map, row, 'Validated?', 0)
        _requirement.validated_date = _get_input_value(_map, row,
                                                       'Validated Date',
                                                       date.today())

        return _requirement

    def _do_insert_similar_item(self, row: pd.Series) -> RAMSTKSimilarItem:
        """Insert a new Similar Item record to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _similar_item; an instance of the RAMSTKSimilarItem database
            table record.
        :rtype: :class:`ramstk.models.programdb.RAMSTKSimilarItem`
        """
        _similar_item = RAMSTKSimilarItem()
        _map = self._dic_field_map['Hardware']

        _similar_item.revision_id = _get_input_value(_map, row, 'Revision ID',
                                                     1)
        _similar_item.hardware_id = _get_input_value(_map, row, 'Hardware ID',
                                                     1)
        _similar_item.parent_id = _get_input_value(_map, row,
                                                   'Parent Assembly', 1)

        return _similar_item

    def _do_insert_validation(self, row: pd.Series) -> RAMSTKValidation:
        """Insert a new Validation entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input
            data.
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKValidation.RAMSTKValidation`
        """
        _validation = RAMSTKValidation()
        _map = self._dic_field_map['Validation']

        _validation.revision_id = _get_input_value(_map, row, 'Revision ID', 1)
        _validation.validation_id = _get_input_value(_map, row,
                                                     'Validation ID', 1)
        _validation.acceptable_maximum = _get_input_value(
            _map, row, 'Acceptable Maximum', 0.0)
        _validation.acceptable_mean = _get_input_value(_map, row,
                                                       'Acceptable Mean', 0.0)
        _validation.acceptable_minimum = _get_input_value(
            _map, row, 'Acceptable Minimum', 0.0)
        _validation.acceptable_variance = _get_input_value(
            _map, row, 'Acceptable Variance', 0.0)
        _validation.confidence = _get_input_value(_map, row, 's-Confidence',
                                                  75.0)
        _validation.cost_average = _get_input_value(_map, row,
                                                    'Average Task Cost', 0.0)
        _validation.cost_maximum = _get_input_value(_map, row,
                                                    'Maximum Task Cost', 0.0)
        _validation.cost_minimum = _get_input_value(_map, row,
                                                    'Minimum Task Cost', 0.0)
        _validation.date_start = _get_input_value(_map, row, 'Start Date',
                                                  date.today())
        _validation.date_end = _get_input_value(_map, row, 'End Date',
                                                date.today())
        _validation.description = _get_input_value(_map, row,
                                                   'Task Description', '')
        _validation.measurement_unit = _get_input_value(
            _map, row, 'Unit of Measure', '')
        _validation.name = _get_input_value(_map, row, 'Name', '')
        _validation.status = _get_input_value(_map, row, 'Task Status', 0.0)
        _validation.task_type = _get_input_value(_map, row, 'Task Type', '')
        _validation.task_specification = _get_input_value(
            _map, row, 'Task Specification', '')
        _validation.time_average = _get_input_value(_map, row,
                                                    'Average Task Time', 0.0)
        _validation.time_maximum = _get_input_value(_map, row,
                                                    'Maximum Task Time', 0.0)
        _validation.time_minimum = _get_input_value(_map, row,
                                                    'Minimum Task Time', 0.0)

        return _validation

    def _do_map_to_field(self, module: str, import_field: str,
                         format_field: str) -> None:
        """Map the external column to the RAMSTK database table field.

        :param module: the RAMSTK module to map header fields for.
        :param import_field: the string used for the column header in the
            import file.
        :param format_field: the string used for default titles in the
            RAMSTK layout file.
        :return: None
        :rtype: None
        """
        self._dic_field_map[module][format_field] = import_field

    def _do_read_db_fields(self, module: str) -> None:
        """Return the database field names in a list.

        :param module: the name of the work stream module to return
            database field names for.
        :return: None
        :rtype: None
        """
        _db_fields = []
        for _field in self._dic_field_map[module]:
            _db_fields.append(_field)

        pub.sendMessage(
            'succeed_read_db_fields',
            db_fields=_db_fields,
        )

    def _do_read_file(self, file_type: str, file_name: str) -> None:
        """Read contents of input file into a pandas DataFrame().

        :param file_type: the type of file to import from.  Supported files
            types are:
                - CSV (using a semi-colon (;) delimiter)
                - Excel
        :param file_name: the name, with full path, of the file to export
            the RAMSTK Program database data to.
        :return: None
        :rtype: None
        """
        if file_type == 'csv':
            self._df_input_data = pd.read_csv(file_name,
                                              sep=';',
                                              na_values=[''],
                                              parse_dates=True)
        elif file_type == 'text':
            self._df_input_data = pd.read_csv(file_name,
                                              sep=' ',
                                              na_values=[''],
                                              parse_dates=True)
        elif file_type == 'excel':
            self._df_input_data = pd.read_excel(file_name)

        pub.sendMessage(
            'succeed_read_import_file',
            import_fields=list(self._df_input_data.axes[1].tolist()[1:]),
        )
