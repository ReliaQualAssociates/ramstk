# -*- coding: utf-8 -*-
#
#       ramstk.modules.exports.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Exports Data Model."""

import os
import pandas as pd

# Export other RAMSTK modules.
from rtk.modules import RAMSTKDataModel


class ExportDataModel(RAMSTKDataModel):
    """Contains the attributes and methods of an Export data model."""

    # Dictionary of RAMSTK export field headers.
    _dic_column_headers = {
        'Function': [
            'revision_id', 'function_id', 'level', 'function_code', 'name',
            'parent_id', 'remarks', 'safety_critical', 'type_id'
        ],
        'Requirement': [
            'revision_id', 'requirement_id', 'derived', 'description',
            'figure_number', 'owner', 'page_number', 'parent_id', 'priority',
            'requirement_code', 'specification', 'requirement_type',
            'validated', 'validated_date'
        ],
        'Hardware': [
            'revision_id', 'hardware_id', 'alt_part_num', 'cage_code',
            'category_id', 'comp_ref_des', 'cost', 'cost_type_id',
            'description', 'duty_cycle', 'figure_number', 'lcn', 'level',
            'manufacturer_id', 'mission_time', 'name', 'nsn', 'page_number',
            'parent_id', 'part', 'part_number', 'quantity', 'ref_des',
            'remarks', 'repairable', 'specification_number', 'subcategory_id',
            'tagged_part', 'year_of_manufacture'
        ],
        'Design Electric': [
            'hardware_id', 'application_id', 'area', 'capacitance',
            'configuration_id', 'construction_id', 'contact_form_id',
            'contact_gauge', 'contact_rating_id', 'current_operating',
            'current_rated', 'current_ratio', 'environment_active_id',
            'environment_dormant_id', 'family_id', 'feature_size',
            'frequency_operating', 'insert_id', 'insulation_id',
            'manufacturing_id', 'matching_id', 'n_active_pins',
            'n_circuit_planes', 'n_cycles', 'n_elements', 'n_hand_soldered',
            'n_wave_soldered', 'operating_life', 'overstress', 'package_id',
            'power_operating', 'power_rated', 'power_ratio', 'reason',
            'resistance', 'specification_id', 'technology_id',
            'temperature_active', 'temperature_case', 'temperature_dormant',
            'temperature_hot_spot', 'temperature_junction', 'temperature_knee',
            'temperature_rated_max', 'temperature_rated_min',
            'temperature_rise', 'theta_jc', 'type_id', 'voltage_ac_operating',
            'voltage_dc_operating', 'voltage_esd', 'voltage_rated',
            'voltage_ratio', 'weight', 'years_in_production'
        ],
        'Design Mechanic': [
            'Hardware ID',
            'Altitude, Operating',
            'Application ID',
            'Balance ID',
            'Clearance',
            'Casing ID',
            'Contact Pressure',
            'Deflection',
            'Diameter, Coil',
            'Diameter, Inner',
            'Diameter, Outer',
            'Diameter, Wire',
            'Filter Size',
            'Flow, Design',
            'Flow, Operating',
            'Frequency, Operating',
            'Friction',
            'Impact ID',
            'Allowable Leakage',
            'Length',
            'Length, Compressed',
            'Length, Relaxed',
            'Design Load',
            'Load ID',
            'Operating Load',
            'Lubrication ID',
            'Manufacturing ID',
            'Material ID',
            'Meyer Hardness',
            'Misalignment Angle',
            'N Ten',
            'N Cycles',
            'N Elements',
            'Offset',
            'Particle Size',
            'Contact Pressure',
            'Differential Pressure',
            'Downstream Pressure',
            'Rated Pressure',
            'Upstream Pressure',
            'Design RPM',
            'Operating RPM',
            'Service ID',
            'Spring Index',
            'Surface Finish',
            'Technology ID',
            'Thickness',
            'Torque ID',
            'Type ID',
            'Design Viscosity',
            'Dynamic Viscosity',
            '% Water',
            'Minimum Width',
        ],
        'Reliability': [
            'hardware_id', 'add_adj_factor', 'failure_distribution_id',
            'hazard_rate_method_id', 'hazard_rate_model',
            'hazard_rate_specified', 'hazard_rate_type_id',
            'location_parameter', 'mtbf_specified', 'mult_adj_factor',
            'quality_id', 'reliability_goal', 'reliability_goal_measure_id',
            'scale_parameter', 'shape_parameter', 'survival_analysis_id'
        ],
        'Validation': [
            'revision_id', 'validation_id', 'acceptable_maximum',
            'acceptable_mean', 'acceptable_minimum', 'acceptable_variance',
            'confidence', 'cost_average', 'cost_maximum', 'cost_minimum',
            'date_start', 'date_end', 'description', 'measurement_unit',
            'name', 'status', 'task_type', 'task_specification',
            'time_average', 'time_maximum', 'time_minimum'
        ]
    }

    _tag = 'Exports'

    def __init__(self, dao):
        """
        Initialize an Export data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._output_data = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_export(self, file_type, file_name):
        """
        Export selected RAMSTK module data to external file.

        :param str file_type: the type of file to export the data to.
                              Currently supported files types are:
                                  - CSV (with semi-colon (;) delimiter.
                                  - Excel
                                  - Text
                                  - PDF
        :param str file_name: the name, with full path, of the file to export
                              the RAMSTK Progam database data to.
        :return: None
        :rtype: None
        """
        if file_type == 'csv':
            self._output_data.to_csv(file_name, sep=';', index=False)
        elif file_type == 'excel':
            __, _extension = os.path.splitext(file_name)
            if _extension == '.xls':
                _writer = pd.ExcelWriter(file_name, engine='xlwt')
            elif _extension == '.xlsx':
                _writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            elif _extension == '.xlsm':
                _writer = pd.ExcelWriter(file_name, engine='openpyxl')
            self._output_data.to_excel(_writer, 'Sheet 1', index=False)
            _writer.save()
            _writer.close()
        elif file_type == 'text':
            self._output_data.to_csv(file_name, sep=' ', index=False)
        elif file_type == 'pdf':
            print "Portable Document Format"

        return None

    def do_load_output(self, module, tree):
        """
        Load the data from the requested RAMSTK module into a Pandas DataFrame.

        :param str module: the RAMSTK module to load for export.
        :param tree: the treelib Tree() containing the data entities for the
                     module to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        if module == 'Function':
            self._do_load_function(tree)
        elif module == 'Requirement':
            self._do_load_requirement(tree)
        elif module == 'Hardware':
            self._do_load_hardware(tree)
        elif module == 'Design Electric':
            self._do_load_design_electric(tree)
        elif module == 'Reliability':
            self._do_load_reliability(tree)
        elif module == 'Validation':
            self._do_load_validation(tree)

        return None

    def _do_load_function(self, tree):
        """
        Load the Function entities into a Pandas DataFrame.

        :param tree: the treelib Tree() containing the data entities for the
                     module to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _dic_output_data = {}

        for _header in self._dic_column_headers['Function']:
            _temp = []
            for _node in tree.nodes.values()[1:]:
                _temp.append(_node.data.get_attributes()[_header])
            _dic_output_data[_header] = _temp

        self._output_data = pd.DataFrame(_dic_output_data)

        return None

    def _do_load_requirement(self, tree):
        """
        Load the Requirement entities into a Pandas DataFrame.

        :param tree: the treelib Tree() containing the data entities for the
                     module to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _dic_output_data = {}

        for _header in self._dic_column_headers['Requirement']:
            _temp = []
            for _node in tree.nodes.values()[1:]:
                _temp.append(_node.data.get_attributes()[_header])
            _dic_output_data[_header] = _temp

        self._output_data = pd.DataFrame(_dic_output_data)

        return None

    def _do_load_hardware(self, tree):
        """
        Load the Hardware entities into a Pandas DataFrame.

        :param tree: the treelib Tree() containing the data entities for the
                     module to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _dic_output_data = {}

        for _header in self._dic_column_headers['Hardware']:
            _temp = []
            for _node in tree.nodes.values()[1:]:
                _temp.append(_node.data[_header])
            _dic_output_data[_header] = _temp

        self._output_data = pd.DataFrame(_dic_output_data)

        return None

    def _do_load_design_electric(self, tree):
        """
        Load the Design Electric entities into a Pandas DataFrame.

        :param tree: the treelib Tree() containing the data entities for the
                     module to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _dic_output_data = {}

        for _header in self._dic_column_headers['Design Electric']:
            _temp = []
            for _node in tree.nodes.values()[1:]:
                _temp.append(_node.data.get_attributes()[_header])
            _dic_output_data[_header] = _temp

        self._output_data = pd.DataFrame(_dic_output_data)

        return None

    def _do_load_reliability(self, tree):
        """
        Load the Reliability entities into a Pandas DataFrame.

        :param tree: the treelib Tree() containing the data entities for the
                     module to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _dic_output_data = {}

        for _header in self._dic_column_headers['Reliability']:
            _temp = []
            for _node in tree.nodes.values()[1:]:
                print _node.data.get_attributes()
                _temp.append(_node.data.get_attributes()[_header])
            _dic_output_data[_header] = _temp

        self._output_data = pd.DataFrame(_dic_output_data)

        return None

    def _do_load_validation(self, tree):
        """
        Load the Validation entities into a Pandas DataFrame.

        :param tree: the treelib Tree() containing the data entities for the
                     module to load.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _dic_output_data = {}

        for _header in self._dic_column_headers['Validation']:
            _temp = []
            for _node in tree.nodes.values()[1:]:
                _temp.append(_node.data.get_attributes()[_header])
            _dic_output_data[_header] = _temp

        self._output_data = pd.DataFrame(_dic_output_data)

        return None
