# -*- coding: utf-8 -*-
#
#       ramstk.modules.imports.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Imports Data Model."""

# Standard Library Imports
from collections import OrderedDict
from datetime import date

# Third Party Imports
import numpy as np
import pandas as pd
from dateutil import parser

# RAMSTK Package Imports
from ramstk.dao.programdb import (
    RAMSTKFunction, RAMSTKRequirement, RAMSTKValidation
)
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKAllocation, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKReliability, RAMSTKSimilarItem
)
from ramstk.modules import RAMSTKDataModel


class ImportDataModel(RAMSTKDataModel):
    """Contains the attributes and methods of an Import data model."""

    # Ordered dictionaries of RAMSTK inputs field headers.  Must use OrderdDict
    # to ensure they are always in the same order during program flow.
    _dic_field_map = {
        'Function':
        OrderedDict([
            ('Revision ID', ''),
            ('Function ID', ''),
            ('Level', ''),
            ('Function Code', ''),
            ('Function Name', ''),
            ('Parent', ''),
            ('Remarks', ''),
            ('Safety Critical', ''),
            ('Type', ''),
        ]),
        'Requirement':
        OrderedDict([
            ('Revision ID', ''),
            ('Requirement ID', ''),
            ('Derived?', ''),
            ('Requirement', ''),
            ('Figure Number', ''),
            ('Owner', ''),
            ('Page Number', ''),
            ('Parent ID', ''),
            ('Priority', ''),
            ('Requirement Code', ''),
            ('Specification', ''),
            ('Requirement Type', ''),
            ('Validated?', ''),
            ('Validated Date', ''),
        ]),
        'Hardware':
        OrderedDict([
            ('Revision ID', ''),
            ('Hardware ID', ''),
            ('Alternate Part Number', ''),
            ('CAGE Code', ''),
            ('Category ID', ''),
            ('Composite Ref. Des.', ''),
            ('Cost', ''),
            ('Cost Type', ''),
            ('Description', ''),
            ('Duty Cycle', ''),
            ('Figure Number', ''),
            ('LCN', ''),
            ('Level', ''),
            ('Manufacturer', ''),
            ('Mission Time', ''),
            ('Name', ''),
            ('NSN', ''),
            ('Page Number', ''),
            ('Parent Assembly', ''),
            ('Part', ''),
            ('Part Number', ''),
            ('Quantity', ''),
            ('Reference Designator', ''),
            ('Remarks', ''),
            ('Repairable', ''),
            ('Specification', ''),
            ('Subcategory ID', ''),
            ('Tagged Part', ''),
            ('Year of Manufacture', ''),
        ]),
        'Design Electric':
        OrderedDict([
            ('Hardware ID', ''),
            ('Application ID', ''),
            ('Area', ''),
            ('Capacitance', ''),
            ('Configuration ID', ''),
            ('Construction ID', ''),
            ('Contact Form ID', ''),
            ('Contact Gauge', ''),
            ('Contact Rating ID', ''),
            ('Current Operating', ''),
            ('Current Rated', ''),
            ('Current Ratio', ''),
            ('Environment Active ID', ''),
            ('Environment Dormant ID', ''),
            ('Family ID', ''),
            ('Feature Size', ''),
            ('Frequency Operating', ''),
            ('Insert ID', ''),
            ('Insulation ID', ''),
            ('Manufacturing ID', ''),
            ('Matching ID', ''),
            ('N Active Pins', ''),
            ('N Circuit Planes', ''),
            ('N Cycles', ''),
            ('N Elements', ''),
            ('N Hand Soldered', ''),
            ('N Wave Soldered', ''),
            ('Operating Life', ''),
            ('Overstress', ''),
            ('Package ID', ''),
            ('Power Operating', ''),
            ('Power Rated', ''),
            ('Power Ratio', ''),
            ('Reason', ''),
            ('Resistance', ''),
            ('Specification ID', ''),
            ('Technology ID', ''),
            ('Temperature, Active', ''),
            ('Temperature, Case', ''),
            ('Temperature, Dormant', ''),
            ('Temperature, Hot Spot', ''),
            ('Temperature, Junction', ''),
            ('Temperature, Knee', ''),
            ('Temperature, Rated Max', ''),
            ('Temperature, Rated Min', ''),
            ('Temperature Rise', ''),
            ('Theta JC', ''),
            ('Type ID', ''),
            ('Voltage, AC Operating', ''),
            ('Voltage, DC Operating', ''),
            ('Voltage ESD', ''),
            ('Voltage, Rated', ''),
            ('Voltage Ratio', ''),
            ('Weight', ''),
            ('Years in Production', ''),
        ]),
        'Design Mechanic':
        OrderedDict([
            ('Hardware ID', ''),
            ('Altitude, Operating', ''),
            ('Application ID', ''),
            ('Balance ID', ''),
            ('Clearance', ''),
            ('Casing ID', ''),
            ('Contact Pressure', ''),
            ('Deflection', ''),
            ('Diameter, Coil', ''),
            ('Diameter, Inner', ''),
            ('Diameter, Outer', ''),
            ('Diameter, Wire', ''),
            ('Filter Size', ''),
            ('Flow, Design', ''),
            ('Flow, Operating', ''),
            ('Frequency, Operating', ''),
            ('Friction', ''),
            ('Impact ID', ''),
            ('Allowable Leakage', ''),
            ('Length', ''),
            ('Length, Compressed', ''),
            ('Length, Relaxed', ''),
            ('Design Load', ''),
            ('Load ID', ''),
            ('Operating Load', ''),
            ('Lubrication ID', ''),
            ('Manufacturing ID', ''),
            ('Material ID', ''),
            ('Meyer Hardness', ''),
            ('Misalignment Angle', ''),
            ('N Ten', ''),
            ('N Cycles', ''),
            ('N Elements', ''),
            ('Offset', ''),
            ('Particle Size', ''),
            ('Contact Pressure', ''),
            ('Differential Pressure', ''),
            ('Downstream Pressure', ''),
            ('Rated Pressure', ''),
            ('Upstream Pressure', ''),
            ('Design RPM', ''),
            ('Operating RPM', ''),
            ('Service ID', ''),
            ('Spring Index', ''),
            ('Surface Finish', ''),
            ('Technology ID', ''),
            ('Thickness', ''),
            (
                'Torque ID',
                '',
            ),
            ('Type ID', ''),
            ('Design Viscosity', ''),
            ('Dynamic Viscosity', ''),
            ('% Water', ''),
            ('Minimum Width', ''),
        ]),
        'Reliability':
        OrderedDict([
            ('Hardware ID', ''),
            ('Additive Adjustment Factor', ''),
            ('Failure Distribution ID', ''),
            ('Failure Rate Method ID', ''),
            (
                'Failure Rate Model',
                '',
            ),
            ('Specified Failure Rate', ''),
            ('Failure Rate Type ID', ''),
            ('Location Parameter', ''),
            ('Specified MTBF', ''),
            ('Multiplicative Adjustment Factor', ''),
            ('Quality ID', ''),
            ('Reliability Goal', ''),
            ('Reliability Goal Measure ID', ''),
            ('Scale Parameter', ''),
            ('Shape Parameter', ''),
            ('Survival Analysis ID', ''),
        ]),
        'Validation':
        OrderedDict([
            ('Revision ID', ''),
            ('Validation ID', ''),
            ('Acceptable Maximum', ''),
            ('Acceptable Mean', ''),
            ('Acceptable Minimum', ''),
            ('Acceptable Variance', ''),
            ('s-Confidence', ''),
            ('Average Task Cost', ''),
            ('Maximum Task Cost', ''),
            ('Minimum Task Cost', ''),
            ('Start Date', ''),
            ('End Date', ''),
            ('Task Description', ''),
            ('Unit of Measure', ''),
            ('Name', ''),
            ('Task Status', ''),
            ('Task Type', ''),
            ('Task Specification', ''),
            ('Average Task Time', ''),
            ('Maximum Task Time', ''),
            ('Minimum Task Time', ''),
        ]),
    }

    _tag = 'Imports'
    _root = 0

    def __init__(self, dao):
        """
        Initialize an Import data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_format_headers = []

        # Initialize private scalar attributes.
        self._input_data = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public stcalar attributes.

    def do_read_input(self, file_type, file_name):
        """
        Read contents of input file into a pandas DataFrame().

        :return: None
        :rtype: None
        """
        if file_type == 'csv':
            self._input_data = pd.read_csv(
                file_name,
                sep=';',
                na_values=[''],
                parse_dates=True,
            )
        elif file_type == 'excel':
            self._input_data = pd.read_excel(file_name)

    def do_map_to_field(self, module, exim_field, format_field):
        """
        Map the external column to the RAMSTK database table field.

        :param str module: the RAMSTK module to map header fields for.
        :param str exim_field: the string used for the column header in the
                               import file.
        :param str format_field: the string used for default titles in the RAMSTK
                                 layout file.
        :return: None
        :rtype: None
        """
        self._dic_field_map[module][format_field] = exim_field

    def do_insert(self, **kwargs):
        """
        Insert a new entity to the RAMSTK db with values from external file.

        :param str module: the name of the RAMSTK module to import.
        :return: (_revision_id, _count, _error_code, _msg; the Revision ID the
                 import is associated with, the total number of entities added,
                 the error code and associated message from the RAMSTK Program
                 DAO.
        :rtype: (int, int, int, str)
        """
        _module = kwargs['module']
        _revision_id = 1

        _entities = []
        for _idx, _row in self._input_data.iterrows():
            if _module == 'Function':
                _entity = self._do_insert_function(_row)
                _entities.append(_entity)
                _revision_id = _entity.revision_id
            elif _module == 'Requirement':
                _entity = self._do_insert_requirement(_row)
                _entities.append(_entity)
                _revision_id = _entity.revision_id
            elif _module == 'Hardware':
                _entity = self._do_insert_hardware(_row)
                _entities.append(_entity)
                _revision_id = _entity.revision_id
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
            elif _module == 'Validation':
                _entity = self._do_insert_validation(_row)
                _entities.append(_entity)
                _revision_id = _entity.revision_id

        _error_code, _msg = RAMSTKDataModel.do_insert(self, entities=_entities)

        if _error_code == 0:
            _count = len(_entities)
        else:
            _count = 0

        return _revision_id, _count, _error_code, _msg

    def _do_insert_function(self, row):
        """
        Insert a new Function entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKFunction.RAMSTKFunction`
        """
        _function = RAMSTKFunction()
        _map = self._dic_field_map['Function']

        _function.revision_id = self._get_input_value(
            _map,
            row,
            'Revision ID',
            1,
        )
        _function.function_id = self._get_input_value(
            _map,
            row,
            'Function ID',
            1,
        )
        _function.function_code = self._get_input_value(
            _map,
            row,
            'Function Code',
            '',
        )
        _function.level = self._get_input_value(_map, row, 'Level', 0)
        _function.name = self._get_input_value(_map, row, 'Function Name', '')
        _function.parent_id = self._get_input_value(_map, row, 'Parent', 1)
        _function.remarks = self._get_input_value(_map, row, 'Remarks', b'')
        _function.safety_critical = self._get_input_value(
            _map,
            row,
            'Safety Critical',
            0,
        )
        _function.type_id = self._get_input_value(_map, row, 'Type', '')

        # Ensure the remarks are a byte-object.
        try:
            _function.remarks = _function.remarks.encode('utf-8')
        except AttributeError:
            pass

        return _function

    def _do_insert_requirement(self, row):
        """
        Insert a new Requirement entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKRequirement.RAMSTKRequirement`
        """
        _requirement = RAMSTKRequirement()
        _map = self._dic_field_map['Requirement']

        _requirement.revision_id = self._get_input_value(
            _map,
            row,
            'Revision ID',
            1,
        )
        _requirement.requirement_id = self._get_input_value(
            _map,
            row,
            'Requirement ID',
            1,
        )
        _requirement.derived = self._get_input_value(_map, row, 'Derived?', 0)
        _requirement.description = self._get_input_value(
            _map,
            row,
            'Requirement',
            '',
        )
        _requirement.figure_number = self._get_input_value(
            _map,
            row,
            'Figure Number',
            '',
        )
        _requirement.owner = self._get_input_value(_map, row, 'Owner', '')
        _requirement.page_number = self._get_input_value(
            _map,
            row,
            'Page Number',
            '',
        )
        _requirement.parent_id = self._get_input_value(
            _map,
            row,
            'Parent ID',
            1,
        )
        _requirement.priority = self._get_input_value(_map, row, 'Priority', 1)
        _requirement.requirement_code = self._get_input_value(
            _map,
            row,
            'Requirement Code',
            '',
        )
        _requirement.specification = self._get_input_value(
            _map,
            row,
            'Specification',
            '',
        )
        _requirement.requirement_type = self._get_input_value(
            _map,
            row,
            'Requirement Type',
            '',
        )
        _requirement.validated = self._get_input_value(
            _map,
            row,
            'Validated?',
            0,
        )
        _requirement.validated_date = self._get_input_value(
            _map,
            row,
            'Validated Date',
            date.today(),
        )

        # Ensure the description is a byte-like object.
        try:
            _requirement.description = _requirement.description.encide('utf-8')
        except AttributeError:
            pass

        return _requirement

    def _do_insert_hardware(self, row):
        """
        Insert a new Hardware entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKHardware.RAMSTKHardware`
        """
        _hardware = RAMSTKHardware()
        _map = self._dic_field_map['Hardware']

        _hardware.revision_id = self._get_input_value(
            _map,
            row,
            'Revision ID',
            1,
        )
        _hardware.hardware_id = self._get_input_value(
            _map,
            row,
            'Hardware ID',
            1,
        )
        _hardware.alt_part_num = self._get_input_value(
            _map,
            row,
            'Alternate Part Number',
            '',
        )
        _hardware.cage_code = self._get_input_value(_map, row, 'CAGE Code', '')
        _hardware.category_id = self._get_input_value(
            _map,
            row,
            'Category ID',
            0,
        )
        _hardware.comp_ref_des = self._get_input_value(
            _map,
            row,
            'Composite Ref. Des.',
            '',
        )
        _hardware.cost = self._get_input_value(_map, row, 'Cost', 0.0)
        _hardware.cost_type_id = self._get_input_value(
            _map,
            row,
            'Cost Type',
            0,
        )
        _hardware.description = self._get_input_value(
            _map,
            row,
            'Description',
            '',
        )
        _hardware.duty_cycle = self._get_input_value(
            _map,
            row,
            'Duty Cycle',
            100.0,
        )
        _hardware.figure_number = self._get_input_value(
            _map,
            row,
            'Figure Number',
            '',
        )
        _hardware.lcn = self._get_input_value(_map, row, 'LCN', '')
        _hardware.level = self._get_input_value(_map, row, 'Level', 0)
        _hardware.manufacturer_id = self._get_input_value(
            _map,
            row,
            'Manufacturer',
            0,
        )
        _hardware.mission_time = self._get_input_value(
            _map,
            row,
            'Mission Time',
            24.0,
        )
        _hardware.name = self._get_input_value(_map, row, 'Name', '')
        _hardware.nsn = self._get_input_value(_map, row, 'NSN', '')
        _hardware.page_number = self._get_input_value(
            _map,
            row,
            'Page Number',
            '',
        )
        _hardware.parent_id = self._get_input_value(
            _map,
            row,
            'Parent Assembly',
            1,
        )
        _hardware.part = self._get_input_value(_map, row, 'Part', 0)
        _hardware.part_number = self._get_input_value(
            _map,
            row,
            'Part Number',
            '',
        )
        _hardware.quantity = self._get_input_value(_map, row, 'Quantity', 1)
        _hardware.ref_des = self._get_input_value(
            _map,
            row,
            'Reference Designator',
            '',
        )
        _hardware.remarks = self._get_input_value(_map, row, 'Remarks', '')
        _hardware.repairable = self._get_input_value(
            _map,
            row,
            'Repairable',
            1,
        )
        _hardware.specification_number = self._get_input_value(
            _map,
            row,
            'Specification',
            '',
        )
        _hardware.subcategory_id = self._get_input_value(
            _map,
            row,
            'Subcategory ID',
            0,
        )
        _hardware.tagged_part = self._get_input_value(
            _map,
            row,
            'Tagged Part',
            0,
        )
        _hardware.year_of_manufacture = self._get_input_value(
            _map,
            row,
            'Year of Manufacture',
            1900,
        )

        # Ensure the remarks are a byte-like object.
        try:
            _hardware.remarks = _hardware.remarks.encide('utf-8')
        except AttributeError:
            pass

        return _hardware

    def _do_insert_design_electric(self, row):
        """
        Insert a new Design Electric entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKHardware.RAMSTKHardware`
        """
        _design_electric = RAMSTKDesignElectric()
        _map = self._dic_field_map['Hardware']
        _design_electric.hardware_id = self._get_input_value(
            _map,
            row,
            'Hardware ID',
            1,
        )

        _map = self._dic_field_map['Design Electric']
        _design_electric.application_id = self._get_input_value(
            _map,
            row,
            'Application ID',
            0,
        )
        _design_electric.area = self._get_input_value(_map, row, 'Area', 1.0)
        _design_electric.capacitance = self._get_input_value(
            _map,
            row,
            'Capacitance',
            0.000001,
        )
        _design_electric.configuration_id = self._get_input_value(
            _map,
            row,
            'Configuration ID',
            0,
        )
        _design_electric.construction_id = self._get_input_value(
            _map,
            row,
            'Construction ID',
            0,
        )
        _design_electric.contact_form_id = self._get_input_value(
            _map,
            row,
            'Contact Form ID',
            0,
        )
        _design_electric.contact_gauge = self._get_input_value(
            _map,
            row,
            'Contact Gauge',
            20,
        )
        _design_electric.contact_rating_id = self._get_input_value(
            _map,
            row,
            'Contact Rating ID',
            0,
        )
        _design_electric.current_operating = self._get_input_value(
            _map,
            row,
            'Current Operating',
            0.0,
        )
        _design_electric.current_rated = self._get_input_value(
            _map,
            row,
            'Current Rated',
            0.0,
        )
        _design_electric.current_ratio = self._get_input_value(
            _map,
            row,
            'Current Ratio',
            0.0,
        )
        _design_electric.environment_active_id = self._get_input_value(
            _map,
            row,
            'Environment Active ID',
            0,
        )
        _design_electric.environment_dormant_id = self._get_input_value(
            _map,
            row,
            'Environment Dormant ID',
            0,
        )
        _design_electric.family_id = self._get_input_value(
            _map,
            row,
            'Family ID',
            0,
        )
        _design_electric.feature_size = self._get_input_value(
            _map,
            row,
            'Feature Size',
            1.0,
        )
        _design_electric.frequency_operating = self._get_input_value(
            _map,
            row,
            'Frequency Operating',
            0.0,
        )
        _design_electric.insert_id = self._get_input_value(
            _map,
            row,
            'Insert ID',
            0,
        )
        _design_electric.insulation_id = self._get_input_value(
            _map,
            row,
            'Insulation ID',
            0,
        )
        _design_electric.manufacturing_id = self._get_input_value(
            _map,
            row,
            'Manufacturing ID',
            0,
        )
        _design_electric.matching_id = self._get_input_value(
            _map,
            row,
            'Matching ID',
            0,
        )
        _design_electric.n_active_pins = self._get_input_value(
            _map,
            row,
            'N Active Pins',
            0,
        )
        _design_electric.n_circuit_planes = self._get_input_value(
            _map,
            row,
            'N Circuit Planes',
            0,
        )
        _design_electric.n_cycles = self._get_input_value(
            _map,
            row,
            'N Cycles',
            0,
        )
        _design_electric.n_elements = self._get_input_value(
            _map,
            row,
            'N Elements',
            0,
        )
        _design_electric.n_hand_soldered = self._get_input_value(
            _map,
            row,
            'N Hand Soldered',
            0,
        )
        _design_electric.n_wave_soldered = self._get_input_value(
            _map,
            row,
            'N Wave Soldered',
            0,
        )
        _design_electric.operating_life = self._get_input_value(
            _map,
            row,
            'Operating Life',
            0,
        )
        _design_electric.overstress = self._get_input_value(
            _map,
            row,
            'Overstress',
            0,
        )
        _design_electric.package_id = self._get_input_value(
            _map,
            row,
            'Package ID',
            0,
        )
        _design_electric.power_operating = self._get_input_value(
            _map,
            row,
            'Power Operating',
            0.0,
        )
        _design_electric.power_rated = self._get_input_value(
            _map,
            row,
            'Power Rated',
            0.0,
        )
        _design_electric.power_ratio = self._get_input_value(
            _map,
            row,
            'Power Ratio',
            0.0,
        )
        _design_electric.reason = self._get_input_value(
            _map,
            row,
            'Reason',
            '',
        )
        _design_electric.resistance = self._get_input_value(
            _map,
            row,
            'Resistance',
            0.0,
        )
        _design_electric.specification_id = self._get_input_value(
            _map,
            row,
            'Specification ID',
            0,
        )
        _design_electric.technology_id = self._get_input_value(
            _map,
            row,
            'Technology ID',
            0,
        )
        _design_electric.temperature_active = self._get_input_value(
            _map,
            row,
            'Temperature, Active',
            30.0,
        )
        _design_electric.temperature_case = self._get_input_value(
            _map,
            row,
            'Temperature, Case',
            0.0,
        )
        _design_electric.temperature_dormant = self._get_input_value(
            _map,
            row,
            'Temperature, Dormant',
            25.0,
        )
        _design_electric.temperature_hot_spot = self._get_input_value(
            _map,
            row,
            'Temperature, Hot Spot',
            0.0,
        )
        _design_electric.temperature_junction = self._get_input_value(
            _map,
            row,
            'Temperature, Junction',
            0.0,
        )
        _design_electric.temperature_knee = self._get_input_value(
            _map,
            row,
            'Temperature, Knee',
            0.0,
        )
        _design_electric.temperature_rated_max = self._get_input_value(
            _map,
            row,
            'Temperature, Rated Max',
            0.0,
        )
        _design_electric.temperature_rated_min = self._get_input_value(
            _map,
            row,
            'Temperature, Rated Min',
            0.0,
        )
        _design_electric.temperature_rise = self._get_input_value(
            _map,
            row,
            'Temperature Rise',
            0.0,
        )
        _design_electric.theta_jc = self._get_input_value(
            _map,
            row,
            'Theta JC',
            0.0,
        )
        _design_electric.type_id = self._get_input_value(
            _map,
            row,
            'Type ID',
            0,
        )
        _design_electric.voltage_ac_operating = self._get_input_value(
            _map,
            row,
            'Voltage, AC Operating',
            0.0,
        )
        _design_electric.voltage_dc_operating = self._get_input_value(
            _map,
            row,
            'Voltage, DC Operating',
            0.0,
        )
        _design_electric.voltage_esd = self._get_input_value(
            _map,
            row,
            'Voltage ESD',
            0.0,
        )
        _design_electric.voltage_rated = self._get_input_value(
            _map,
            row,
            'Voltage, Rated',
            0.0,
        )
        _design_electric.voltage_ratio = self._get_input_value(
            _map,
            row,
            'Voltage Ratio',
            0.0,
        )
        _design_electric.weight = self._get_input_value(
            _map,
            row,
            'Weight',
            1.0,
        )
        _design_electric.years_in_production = self._get_input_value(
            _map,
            row,
            'Years in Production',
            2,
        )

        return _design_electric

    def _do_insert_design_mechanic(self, row):
        """
        Insert a new Design Mechanic entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKHardware.RAMSTKHardware`
        """
        # ISSUE: See issue #141 at https://github.com/ReliaQualAssociates/ramstk/issues/141 and add NSWC support to this method.
        _design_mechanic = RAMSTKDesignMechanic()

        _map = self._dic_field_map['Hardware']
        _design_mechanic.hardware_id = self._get_input_value(
            _map,
            row,
            'Hardware ID',
            1,
        )

        _map = self._dic_field_map['Design Mechanic']
        _design_mechanic.altitude_operating = self._get_input_value(
            _map,
            row,
            'Altitude, Operating',
            0.0,
        )
        _design_mechanic.application_id = self._get_input_value(
            _map,
            row,
            'Application ID',
            0,
        )
        _design_mechanic.balance_id = self._get_input_value(
            _map,
            row,
            'Balance ID',
            0,
        )
        _design_mechanic.clearance = self._get_input_value(
            _map,
            row,
            'Clearance',
            0.0,
        )
        _design_mechanic.casing_id = self._get_input_value(
            _map,
            row,
            'Casing ID',
            0,
        )
        _design_mechanic.contact_pressure = self._get_input_value(
            _map,
            row,
            'Contact Pressure',
            0.0,
        )
        _design_mechanic.deflection = self._get_input_value(
            _map,
            row,
            'Deflection',
            0.0,
        )
        _design_mechanic.diameter_coil = self._get_input_value(
            _map,
            row,
            'Diameter, Coil',
            0.0,
        )
        _design_mechanic.diameter_inner = self._get_input_value(
            _map,
            row,
            'Diameter, Inner',
            0.0,
        )
        _design_mechanic.diameter_outer = self._get_input_value(
            _map,
            row,
            'Diameter, Outer',
            0.0,
        )
        _design_mechanic.diameter_wire = self._get_input_value(
            _map,
            row,
            'Diameter, Wire',
            0.0,
        )
        _design_mechanic.filter_size = self._get_input_value(
            _map,
            row,
            'Filter Size',
            0.0,
        )
        _design_mechanic.flow_design = self._get_input_value(
            _map,
            row,
            'Flow, Design',
            0.0,
        )
        _design_mechanic.flow_operating = self._get_input_value(
            _map,
            row,
            'Flow, Operating',
            0.0,
        )
        _design_mechanic.frequency_operating = self._get_input_value(
            _map,
            row,
            'Frequency, Operating',
            0.0,
        )
        _design_mechanic.friction = self._get_input_value(
            _map,
            row,
            'Friction',
            0.0,
        )
        _design_mechanic.impact_id = self._get_input_value(
            _map,
            row,
            'Impact ID',
            0,
        )
        _design_mechanic.leakage_allowable = self._get_input_value(
            _map,
            row,
            'Allowable Leakage',
            0.0,
        )
        _design_mechanic.length = self._get_input_value(
            _map,
            row,
            'Length',
            0.0,
        )
        _design_mechanic.length_compressed = self._get_input_value(
            _map,
            row,
            'Length, Compressed',
            0.0,
        )
        _design_mechanic.length_relaxed = self._get_input_value(
            _map,
            row,
            'Length, Relaxed',
            0.0,
        )
        _design_mechanic.load_design = self._get_input_value(
            _map,
            row,
            'Design Load',
            0.0,
        )
        _design_mechanic.load_id = self._get_input_value(
            _map,
            row,
            'Load ID',
            0,
        )
        _design_mechanic.load_operating = self._get_input_value(
            _map,
            row,
            'Operating Load',
            0.0,
        )
        _design_mechanic.lubrication_id = self._get_input_value(
            _map,
            row,
            'Lubrication ID',
            0,
        )
        _design_mechanic.manufacturing_id = self._get_input_value(
            _map,
            row,
            'Manufacturing ID',
            0,
        )
        _design_mechanic.material_id = self._get_input_value(
            _map,
            row,
            'Material ID',
            0,
        )
        _design_mechanic.meyer_hardness = self._get_input_value(
            _map,
            row,
            'Meyer Hardness',
            0.0,
        )
        _design_mechanic.misalignment_angle = self._get_input_value(
            _map,
            row,
            'Misalignment Angle',
            0.0,
        )
        _design_mechanic.n_ten = self._get_input_value(_map, row, 'N Ten', 0)
        _design_mechanic.n_cycles = self._get_input_value(
            _map,
            row,
            'N Cycles',
            0.0,
        )
        _design_mechanic.n_elements = self._get_input_value(
            _map,
            row,
            'N Elements',
            0,
        )
        _design_mechanic.offset = self._get_input_value(
            _map,
            row,
            'Offset',
            0.0,
        )
        _design_mechanic.particle_size = self._get_input_value(
            _map,
            row,
            'Particle Size',
            0.0,
        )
        _design_mechanic.pressure_contact = self._get_input_value(
            _map,
            row,
            'Contact Pressure',
            0.0,
        )
        _design_mechanic.pressure_delta = self._get_input_value(
            _map,
            row,
            'Differential Pressure',
            0.0,
        )
        _design_mechanic.pressure_downstream = self._get_input_value(
            _map,
            row,
            'Downstream Pressure',
            0.0,
        )
        _design_mechanic.pressure_rated = self._get_input_value(
            _map,
            row,
            'Rated Pressure',
            0.0,
        )
        _design_mechanic.pressure_upstream = self._get_input_value(
            _map,
            row,
            'Upstream Pressure',
            0.0,
        )
        _design_mechanic.rpm_design = self._get_input_value(
            _map,
            row,
            'Design RPM',
            0.0,
        )
        _design_mechanic.rpm_operating = self._get_input_value(
            _map,
            row,
            'Operating RPM',
            0.0,
        )
        _design_mechanic.service_id = self._get_input_value(
            _map,
            row,
            'Service ID',
            0,
        )
        _design_mechanic.spring_index = self._get_input_value(
            _map,
            row,
            'Spring Index',
            0,
        )
        _design_mechanic.surface_finish = self._get_input_value(
            _map,
            row,
            'Surface Finish',
            0.0,
        )
        _design_mechanic.technology_id = self._get_input_value(
            _map,
            row,
            'Technology ID',
            0,
        )
        _design_mechanic.thickness = self._get_input_value(
            _map,
            row,
            'Thickness',
            0.0,
        )
        _design_mechanic.torque_id = self._get_input_value(
            _map,
            row,
            'Torque ID',
            0,
        )
        _design_mechanic.type_id = self._get_input_value(
            _map,
            row,
            'Type ID',
            0,
        )
        _design_mechanic.viscosity_design = self._get_input_value(
            _map,
            row,
            'Design Viscosity',
            0.0,
        )
        _design_mechanic.viscosity_dynamic = self._get_input_value(
            _map,
            row,
            'Dynamic Viscosity',
            0.0,
        )
        _design_mechanic.water_per_cent = self._get_input_value(
            _map,
            row,
            '% Water',
            0.0,
        )
        _design_mechanic.width_minimum = self._get_input_value(
            _map,
            row,
            'Minimum Width',
            0.0,
        )

        return _design_mechanic

    def _do_insert_mil_hdbk_f(self, row):
        """
        Insert a new MIL-HDBK-217F entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKMilHdbkF.RAMSTKMilHdbkF`
        """
        _mil_hdbk_f = RAMSTKMilHdbkF()

        _map = self._dic_field_map['Hardware']
        _mil_hdbk_f.hardware_id = self._get_input_value(
            _map,
            row,
            'Hardware ID',
            1,
        )

        return _mil_hdbk_f

    def _do_insert_nswc(self, row):
        """
        Insert a new NSWC entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKNSWC.RAMSTKNSWC`
        """
        _mil_hdbk_f = RAMSTKNSWC()

        _map = self._dic_field_map['Hardware']
        _mil_hdbk_f.hardware_id = self._get_input_value(
            _map,
            row,
            'Hardware ID',
            1,
        )

        return _mil_hdbk_f

    def _do_insert_reliability(self, row):
        """
        Insert a new Reliability entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKHardware.RAMSTKHardware`
        """
        _reliability = RAMSTKReliability()

        _map = self._dic_field_map['Hardware']
        _reliability.hardware_id = self._get_input_value(
            _map,
            row,
            'Hardware ID',
            1,
        )

        _map = self._dic_field_map['Reliability']
        _reliability.add_adj_factor = self._get_input_value(
            _map,
            row,
            'Additive Adjustment Factor',
            0.0,
        )
        _reliability.failure_distribution_id = self._get_input_value(
            _map,
            row,
            'Failure Distribution ID',
            0,
        )
        _reliability.hazard_rate_method_id = self._get_input_value(
            _map,
            row,
            'Failure Rate Method ID',
            0,
        )
        _reliability.hazard_rate_model = self._get_input_value(
            _map,
            row,
            'Failure Rate Model',
            '',
        )
        _reliability.hazard_rate_specified = self._get_input_value(
            _map,
            row,
            'Specified Failure Rate',
            0.0,
        )
        _reliability.hazard_rate_type_id = self._get_input_value(
            _map,
            row,
            'Failure Rate Type ID',
            0,
        )
        _reliability.location_parameter = self._get_input_value(
            _map,
            row,
            'Location Parameter',
            0.0,
        )
        _reliability.mtbf_specified = self._get_input_value(
            _map,
            row,
            'Specified MTBF',
            0.0,
        )
        _reliability.mult_adj_factor = self._get_input_value(
            _map,
            row,
            'Multiplicative Adjustment Factor',
            1.0,
        )
        _reliability.quality_id = self._get_input_value(
            _map,
            row,
            'Quality ID',
            0,
        )
        _reliability.reliability_goal = self._get_input_value(
            _map,
            row,
            'Reliability Goal',
            100.0,
        )
        _reliability.reliability_goal_measure_id = self._get_input_value(
            _map,
            row,
            'Reliability Goal Measure ID',
            0,
        )
        _reliability.scale_parameter = self._get_input_value(
            _map,
            row,
            'Scale Parameter',
            0.0,
        )
        _reliability.shape_parameter = self._get_input_value(
            _map,
            row,
            'Shape Parameter',
            0.0,
        )
        _reliability.survival_analysis_id = self._get_input_value(
            _map,
            row,
            'Survival Analysis ID',
            0,
        )

        return _reliability

    def _do_insert_allocation(self, row):
        """
        Insert a new Allocation record to the RAMSTK db.

        :param hardware: the Hardware item that was just inserted.
        :return: _allocation; an instance of the RAMSTKAllocation database
                 table record.
        :rtype: :class:`ramstk.dao.programdb.RAMSTKAllocation`
        """
        _allocation = RAMSTKAllocation()
        _map = self._dic_field_map['Hardware']

        _allocation.revision_id = self._get_input_value(
            _map,
            row,
            'Revision ID',
            1,
        )
        _allocation.hardware_id = self._get_input_value(
            _map,
            row,
            'Hardware ID',
            1,
        )
        _allocation.parent_id = self._get_input_value(
            _map,
            row,
            'Parent Assembly',
            1,
        )

        return _allocation

    def _do_insert_similar_item(self, row):
        """
        Insert a new Similar Item record to the RAMSTK db.

        :param hardware: the Hardware item that was just inserted.
        :return: _similar_item; an instance of the RAMSTKSimilarItem database
                 table record.
        :rtype: :class:`ramstk.dao.programdb.RAMSTKSimilarItem`
        """
        _similar_item = RAMSTKSimilarItem()
        _map = self._dic_field_map['Hardware']

        _similar_item.revision_id = self._get_input_value(
            _map,
            row,
            'Revision ID',
            1,
        )
        _similar_item.hardware_id = self._get_input_value(
            _map,
            row,
            'Hardware ID',
            1,
        )
        _similar_item.parent_id = self._get_input_value(
            _map,
            row,
            'Parent Assembly',
            1,
        )

        return _similar_item

    def _do_insert_validation(self, row):
        """
        Insert a new Validation entity to the RAMSTK db.

        :param row: the row from the pandas DataFrame containing the input data.
        :type row: :class:`pandas.Series`
        :return: _entity
        :rtype: :class:`ramstk.dao.programdb.RAMSTKValidation.RAMSTKValidation`
        """
        _validation = RAMSTKValidation()
        _map = self._dic_field_map['Validation']

        _validation.revision_id = self._get_input_value(
            _map,
            row,
            'Revision ID',
            1,
        )
        _validation.validation_id = self._get_input_value(
            _map,
            row,
            'Validation ID',
            1,
        )
        _validation.acceptable_maximum = self._get_input_value(
            _map,
            row,
            'Acceptable Maximum',
            0.0,
        )
        _validation.acceptable_mean = self._get_input_value(
            _map,
            row,
            'Acceptable Mean',
            0.0,
        )
        _validation.acceptable_minimum = self._get_input_value(
            _map,
            row,
            'Acceptable Minimum',
            0.0,
        )
        _validation.acceptable_variance = self._get_input_value(
            _map,
            row,
            'Acceptable Variance',
            0.0,
        )
        _validation.confidence = self._get_input_value(
            _map,
            row,
            's-Confidence',
            75.0,
        )
        _validation.cost_average = self._get_input_value(
            _map,
            row,
            'Average Task Cost',
            0.0,
        )
        _validation.cost_maximum = self._get_input_value(
            _map,
            row,
            'Maximum Task Cost',
            0.0,
        )
        _validation.cost_minimum = self._get_input_value(
            _map,
            row,
            'Minimum Task Cost',
            0.0,
        )
        _validation.date_start = self._get_input_value(
            _map,
            row,
            'Start Date',
            date.today(),
        )
        _validation.date_end = self._get_input_value(
            _map,
            row,
            'End Date',
            date.today(),
        )
        _validation.description = self._get_input_value(
            _map,
            row,
            'Task Description',
            '',
        )
        _validation.measurement_unit = self._get_input_value(
            _map,
            row,
            'Unit of Measure',
            '',
        )
        _validation.name = self._get_input_value(_map, row, 'Name', '')
        _validation.status = self._get_input_value(
            _map,
            row,
            'Task Status',
            0.0,
        )
        _validation.task_type = self._get_input_value(
            _map,
            row,
            'Task Type',
            '',
        )
        _validation.task_specification = self._get_input_value(
            _map,
            row,
            'Task Specification',
            '',
        )
        _validation.time_average = self._get_input_value(
            _map,
            row,
            'Average Task Time',
            0.0,
        )
        _validation.time_maximum = self._get_input_value(
            _map,
            row,
            'Maximum Task Time',
            0.0,
        )
        _validation.time_minimum = self._get_input_value(
            _map,
            row,
            'Minimum Task Time',
            0.0,
        )

        # Ensure the description is a byte-like object, not 'str'.
        try:
            _validation.description = _validation.description.encode('utf-8')
        except AttributeError:
            pass

        return _validation

    def get_db_fields(self, module):
        """
        Get the fixed field names from the field map for the requested module.

        :param str module: the RAMSTK module to get the fixed field names for.
        :return: list of fixed field names.
        :rtype: (list, list)
        """
        try:
            _db_fields = list(self._dic_field_map[module].keys())
            if module.lower() == 'hardware':
                _db_fields += list(
                    self._dic_field_map['Design Electric'].keys(), )[1:]
                _db_fields += list(
                    self._dic_field_map['Reliability'].keys(), )[1:]
        except KeyError:
            _db_fields = []

        try:
            _file_fields = self._input_data.columns
        except AttributeError:
            _file_fields = []

        return (_db_fields, _file_fields)

    @staticmethod
    def _get_input_value(mapper, row, field, default):
        """
        Retrieve the input value for a field from the Pandas dataframe.

        :param dict mapper: the field mapping dict to use as the Rosetta stone.
        :param row: the row from the pandas DataFrame containing the input
                    data.
        :type row: :class:`pandas.Series`
        :param str field: the name of the RAMSTK database field to retrieve the
                          data for.
        :param default: the default value to assign to the field.
        :return: _value
        :rtype: the value of the requested input field or the default.
        """
        try:
            if row.at[mapper[field]] is np.nan:
                _value = default
            elif default == date.today():
                _value = parser.parse(row.at[mapper[field]])
            else:
                _value = row.at[mapper[field]]
        except KeyError:
            _value = default

        return _value
