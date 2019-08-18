# -*- coding: utf-8 -*-
#
#       ramstk.exim.exports.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Export module."""

# Standard Library Imports
import os

# Third Party Imports
import pandas as pd
from pubsub import pub

# Dictionary of RAMSTK export field headers for each of the workstream modules.
COLUMN_HEADERS = {
    'Function': [
        'revision_id', 'function_id', 'level', 'function_code', 'name',
        'parent_id', 'remarks', 'safety_critical', 'type_id'
    ],
    'Requirement': [
        'revision_id', 'requirement_id', 'derived', 'description',
        'figure_number', 'owner', 'page_number', 'parent_id', 'priority',
        'requirement_code', 'specification', 'requirement_type', 'validated',
        'validated_date'
    ],
    'Hardware': [
        'revision_id', 'hardware_id', 'alt_part_num', 'cage_code',
        'category_id', 'comp_ref_des', 'cost', 'cost_type_id', 'description',
        'duty_cycle', 'figure_number', 'lcn', 'level', 'manufacturer_id',
        'mission_time', 'name', 'nsn', 'page_number', 'parent_id', 'part',
        'part_number', 'quantity', 'ref_des', 'remarks', 'repairable',
        'specification_number', 'subcategory_id', 'tagged_part',
        'year_of_manufacture'
    ],
    'Design Electric': [
        'hardware_id', 'application_id', 'area', 'capacitance',
        'configuration_id', 'construction_id', 'contact_form_id',
        'contact_gauge', 'contact_rating_id', 'current_operating',
        'current_rated', 'current_ratio', 'environment_active_id',
        'environment_dormant_id', 'family_id', 'feature_size',
        'frequency_operating', 'insert_id', 'insulation_id',
        'manufacturing_id', 'matching_id', 'n_active_pins', 'n_circuit_planes',
        'n_cycles', 'n_elements', 'n_hand_soldered', 'n_wave_soldered',
        'operating_life', 'overstress', 'package_id', 'power_operating',
        'power_rated', 'power_ratio', 'reason', 'resistance',
        'specification_id', 'technology_id', 'temperature_active',
        'temperature_case', 'temperature_dormant', 'temperature_hot_spot',
        'temperature_junction', 'temperature_knee', 'temperature_rated_max',
        'temperature_rated_min', 'temperature_rise', 'theta_jc', 'type_id',
        'voltage_ac_operating', 'voltage_dc_operating', 'voltage_esd',
        'voltage_rated', 'voltage_ratio', 'weight', 'years_in_production'
    ],
    'Design Mechanic': [
        'Hardware ID', 'Altitude, Operating', 'Application ID', 'Balance ID',
        'Clearance', 'Casing ID', 'Contact Pressure', 'Deflection',
        'Diameter, Coil', 'Diameter, Inner', 'Diameter, Outer',
        'Diameter, Wire', 'Filter Size', 'Flow, Design', 'Flow, Operating',
        'Frequency, Operating', 'Friction', 'Impact ID', 'Allowable Leakage',
        'Length', 'Length, Compressed', 'Length, Relaxed', 'Design Load',
        'Load ID', 'Operating Load', 'Lubrication ID', 'Manufacturing ID',
        'Material ID', 'Meyer Hardness', 'Misalignment Angle', 'N Ten',
        'N Cycles', 'N Elements', 'Offset', 'Particle Size',
        'Contact Pressure', 'Differential Pressure', 'Downstream Pressure',
        'Rated Pressure', 'Upstream Pressure', 'Design RPM', 'Operating RPM',
        'Service ID', 'Spring Index', 'Surface Finish', 'Technology ID',
        'Thickness', 'Torque ID', 'Type ID', 'Design Viscosity',
        'Dynamic Viscosity', '% Water', 'Minimum Width'
    ],
    'Reliability': [
        'hardware_id', 'add_adj_factor', 'failure_distribution_id',
        'hazard_rate_method_id', 'hazard_rate_model', 'hazard_rate_specified',
        'hazard_rate_type_id', 'location_parameter', 'mtbf_specified',
        'mult_adj_factor', 'quality_id', 'reliability_goal',
        'reliability_goal_measure_id', 'scale_parameter', 'shape_parameter',
        'survival_analysis_id'
    ],
    'Validation': [
        'revision_id', 'validation_id', 'acceptable_maximum',
        'acceptable_mean', 'acceptable_minimum', 'acceptable_variance',
        'confidence', 'cost_average', 'cost_maximum', 'cost_minimum',
        'date_start', 'date_end', 'description', 'measurement_unit', 'name',
        'status', 'task_type', 'task_specification', 'time_average',
        'time_maximum', 'time_minimum'
    ]
}


class Export:
    """Contains the methods for exporting data from a program database."""
    def __init__(self) -> None:
        """Initialize an Export module instance."""
        # Initialize private dictionary attributes.
        self._dic_output_data = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._df_output_data = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_data,
                      'succeed_get_all_function_attributes')
        pub.subscribe(self._do_load_data,
                      'succeed_get_all_requirement_attributes')
        pub.subscribe(self._do_load_data,
                      'succeed_get_all_hardware_attributes')
        pub.subscribe(self._do_load_data,
                      'succeed_get_all_validation_attributes')

    def do_export(self, file_type: str, file_name: str) -> None:
        """
        Export selected RAMSTK module data to external file.

        :param str file_type: the type of file to export the data to.
            Supported files types are:
                - CSV (using a semi-colon (;) delimiter)
                - Excel
                - Text (using a blank space delimiter)
                - PDF [Future]]
        :param str file_name: the name, with full path, of the file to export
            the RAMSTK Progam database data to.
        :return: None
        :rtype: None
        """
        if file_type == 'csv':
            self._df_output_data.to_csv(file_name, sep=';', index=False)
        elif file_type == 'excel':
            _file, _extension = os.path.splitext(file_name)
            if _extension == '.xls':
                _writer = pd.ExcelWriter(file_name, engine='xlwt')
            elif _extension == '.xlsx':
                _writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            elif _extension == '.xlsm':
                _writer = pd.ExcelWriter(file_name, engine='openpyxl')
            else:
                file_name = _file + '.xls'
                _writer = pd.ExcelWriter(file_name, engine='xlwt')
            self._df_output_data.to_excel(_writer, 'Sheet 1', index=False)
            _writer.save()
            _writer.close()
        elif file_type == 'text':
            self._df_output_data.to_csv(file_name, sep=' ', index=False)
        elif file_type == 'pdf':
            print("Portable Document Format")

    @staticmethod
    def do_load_output(module: str, node_id: int) -> None:
        """
        Load the data from the requested RAMSTK module into a Pandas DataFrame.

        :param str module: the RAMSTK module to load for export.
        :param int node_id: the node ID in the Tree() containing the data
            to load.
        :return: None
        :rtype: None
        """
        if module == 'Function':
            pub.sendMessage('request_get_all_function_attributes',
                            node_id=node_id)
        elif module == 'Requirement':
            pub.sendMessage('request_get_all_requirement_attributes',
                            node_id=node_id)
        elif module == 'Hardware':
            pub.sendMessage('request_get_all_hardware_attributes',
                            node_id=node_id)
        elif module == 'Validation':
            pub.sendMessage('request_get_all_validation_attributes',
                            node_id=node_id)

    def _do_load_data(self, attributes) -> None:
        """
        Load the attribute data into a Pandas DataFrame.

        :param dict attributes: the attributes dict to export.
        :return: None
        :rtype: None
        """
        # Remove the hazards analysis data from the attributes dict if loading
        # a function.
        try:
            attributes.pop('hazards')
        except KeyError:
            pass

        for _key in attributes:
            try:
                self._dic_output_data[_key].append(attributes[_key])
            except KeyError:
                self._dic_output_data[_key] = [attributes[_key]]

        self._df_output_data = pd.DataFrame(self._dic_output_data)
