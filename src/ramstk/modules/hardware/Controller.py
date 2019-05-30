# -*- coding: utf-8 -*-
#
#       ramstk.hardware.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Controller."""

from datetime import date

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
from ramstk.modules import RAMSTKDataMatrix
from ramstk.dao import (RAMSTKHardware, RAMSTKRequirement, RAMSTKTest,
                        RAMSTKValidation)
from . import dtmHardwareBoM

# Set default attributes to be returned when there are none to return.  This
# should only happen when adding the initial, top-level system hardware item.
ATTRIBUTES = {
    'revision_id': 1,
    'hardware_id': 1,
    'alt_part_num': '',
    'attachments': '',
    'cage_code': '',
    'category_id': 0,
    'comp_ref_des': 'S1',
    'cost': 0.0,
    'cost_failure': 0.0,
    'cost_hour': 0.0,
    'cost_type_id': 0,
    'description': 'Description',
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
    'ref_des': '',
    'remarks': '',
    'repairable': 0,
    'specification_number': '',
    'subcategory_id': 0,
    'tagged_part': 0,
    'total_part_count': 0,
    'total_power_dissipation': 0,
    'year_of_manufacture': date.today().year,
    'voltage_ac_operating': 0.0,
    'frequency_operating': 0.0,
    'type_id': 0,
    'resistance': 0.0,
    'package_id': 0,
    'technology_id': 0,
    'n_cycles': 0,
    'n_circuit_planes': 1,
    'contact_gauge': 0,
    'current_operating': 0.0,
    'n_hand_soldered': 0,
    'contact_rating_id': 0,
    'area': 0.0,
    'contact_form_id': 0,
    'years_in_production': 1,
    'n_active_pins': 0,
    'capacitance': 0.0,
    'temperature_case': 0.0,
    'current_rated': 0.0,
    'power_operating': 0.0,
    'configuration_id': 0,
    'temperature_hot_spot': 0.0,
    'temperature_junction': 0.0,
    'current_ratio': 0.0,
    'insulation_id': 0,
    'construction_id': 0,
    'insert_id': 0,
    'theta_jc': 0.0,
    'voltage_dc_operating': 0.0,
    'power_ratio': 0.0,
    'family_id': 0,
    'overstress': 1,
    'voltage_rated': 0.0,
    'feature_size': 0.0,
    'operating_life': 0.0,
    'application_id': 0,
    'weight': 0.0,
    'temperature_rated_max': 0.0,
    'voltage_ratio': 0.0,
    'temperature_rated_min': 0.0,
    'power_rated': 0.0,
    'environment_active_id': 0,
    'specification_id': 0,
    'matching_id': 0,
    'n_elements': 0,
    'environment_dormant_id': 0,
    'reason': '',
    'voltage_esd': 0.0,
    'manufacturing_id': 0,
    'n_wave_soldered': 0,
    'temperature_rise': 0.0,
    'temperature_active': 35.0,
    'temperature_dormant': 25.0,
    'pressure_upstream': 0.0,
    'surface_finish': 0.0,
    'friction': 0.0,
    'length_compressed': 0.0,
    'load_id': 0,
    'balance_id': 0,
    'lubrication_id': 0,
    'water_per_cent': 0.0,
    'misalignment_angle': 0.0,
    'rpm_design': 0.0,
    'pressure_downstream': 0.0,
    'diameter_coil': 0.0,
    'pressure_contact': 0.0,
    'meyer_hardness': 0.0,
    'rpm_operating': 0.0,
    'length_relaxed': 0.0,
    'impact_id': 0,
    'n_ten': 0,
    'material_id': 0,
    'service_id': 0,
    'flow_design': 0.0,
    'diameter_wire': 0.0,
    'deflection': 0.04,
    'filter_size': 0.0,
    'diameter_inner': 0.0,
    'pressure_rated': 0.0,
    'altitude_operating': 0.0,
    'thickness': 0.0,
    'diameter_outer': 0.0,
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
    'clearance': 0.0,
    'piP': 0.0,
    'piC': 0.0,
    'piPT': 0.0,
    'piR': 0.0,
    'piA': 0.0,
    'piK': 0.0,
    'lambdaEOS': 0.00056,
    'piNR': 0.0,
    'piCF': 0.0,
    'piMFG': 0.0,
    'piM': 0.0,
    'piI': 0.0,
    'lambdaBP': 0.0,
    'piL': 0.0,
    'piCYC': 0.0,
    'piN': 0.0,
    'piF': 0.0,
    'lambdaCYC': 0.0,
    'piCV': 0.0,
    'piE': 0.0,
    'piCR': 0.0,
    'A1': 0.00235,
    'piQ': 0.0,
    'A2': 0.0,
    'B1': 0.0,
    'B2': 0.0,
    'lambdaBD': 0.0,
    'piCD': 0.0,
    'C2': 0.0,
    'C1': 0.0,
    'piS': 0.0,
    'piT': 0.0,
    'piU': 0.0,
    'piV': 0.0,
    'piTAPS': 0.0,
    'Clc': 0.0,
    'Crd': 0.0,
    'Cac': 0.0,
    'Cmu': 0.0,
    'Ck': 0.0,
    'Ci': 0.0,
    'Ch': 0.0,
    'Cn': 0.0,
    'Cm': 0.0,
    'Cl': 0.0,
    'Cc': 0.0,
    'Cb': 0.0,
    'Cg': 0.0,
    'Cf': 0.0,
    'Ce': 0.0,
    'Cd': 0.0,
    'Cy': 0.0,
    'Cbv': 0.0,
    'Cbt': 0.0,
    'Cs': 0.0,
    'Cr': 0.0,
    'Cq': 0.0,
    'Cp': 0.0,
    'Cw': 0.0,
    'Cv': 0.0,
    'Ct': 0.0,
    'Cnw': 0.0,
    'Cnp': 0.0,
    'Csf': 0.0,
    'Calt': 0.0,
    'Csc': 0.0,
    'Cbl': 0.0,
    'Csz': 0.0,
    'Cst': 0.0,
    'Csw': 0.0,
    'Csv': 0.0,
    'Cgl': 0.0,
    'Cga': 0.0,
    'Cgp': 0.0,
    'Cgs': 0.0,
    'Cgt': 0.0,
    'Cgv': 0.0,
    'Ccw': 0.0,
    'Ccv': 0.0,
    'Cpd': 0.0,
    'Ccp': 0.0,
    'Cpf': 0.0,
    'Ccs': 0.0,
    'Ccf': 0.0,
    'Cpv': 0.0,
    'Cdc': 0.0,
    'Cdl': 0.0,
    'Cdt': 0.0,
    'Cdw': 0.0,
    'Cdp': 0.0,
    'Cds': 0.0,
    'Cdy': 0.0,
    'hazard_rate_percent': 0.0,
    'reliability_mission': 1.0,
    'reliability_goal_measure_id': 0,
    'hazard_rate_specified': 0.0,
    'hazard_rate_active': 0.05,
    'hr_mission_variance': 0.0,
    'reliability_goal': 0.0,
    'mtbf_log_variance': 0.0,
    'quality_id': 0,
    'scale_parameter': 0.0,
    'add_adj_factor': 0.0,
    'availability_mission': 1.0,
    'mtbf_spec_variance': 0.0,
    'mtbf_miss_variance': 0.0,
    'lambda_b': 0.0,
    'hr_specified_variance': 0.0,
    'avail_log_variance': 0.0,
    'hazard_rate_type_id': 0,
    'mtbf_mission': 0.0,
    'failure_distribution_id': 0,
    'reliability_miss_variance': 0.0,
    'avail_mis_variance': 0.0,
    'hazard_rate_method_id': 0,
    'hazard_rate_mission': 0.0,
    'hazard_rate_software': 0.0,
    'mtbf_specified': 0.0,
    'hr_logistics_variance': 0.0,
    'shape_parameter': 0.0,
    'hr_dormant_variance': 0.0,
    'location_parameter': 0.0,
    'survival_analysis_id': 0,
    'hazard_rate_logistics': 0.0,
    'reliability_logistics': 1.0,
    'hazard_rate_model': 'Test HR Model',
    'reliability_log_variance': 0.0,
    'hr_active_variance': 0.0,
    'availability_logistics': 1.0,
    'hazard_rate_dormant': 0.0,
    'mtbf_logistics': 0.0,
    'mult_adj_factor': 1.0,
    'temperature_knee': 25.0,
    'total_cost': 0.0
}


class HardwareBoMDataController(RAMSTKDataController):
    """
    Provide an interface between the Hardware data model and an RAMSTK view model.

    A single Hardware controller can manage one or more Hardware data models.
    The attributes of a Hardware data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Hardware data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the Hardware Data
                    Model.
        :type dao: :class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmHardwareBoM(dao, **kwargs),
            ramstk_module='hardware BOM',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_hw_rqrmnt_matrix = RAMSTKDataMatrix(
            dao,
            row_table=RAMSTKHardware,
            column_table=RAMSTKRequirement,
            **kwargs)
        self._dmx_hw_tstng_matrix = RAMSTKDataMatrix(
            dao, row_table=RAMSTKHardware, column_table=RAMSTKTest, **kwargs)
        self._dmx_hw_vldtn_matrix = RAMSTKDataMatrix(
            dao,
            row_table=RAMSTKHardware,
            column_table=RAMSTKValidation,
            **kwargs)
        self._hr_multiplier = configuration.RAMSTK_HR_MULTIPLIER

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._request_do_calculate, 'request_calculate_hardware')
        pub.subscribe(self.request_do_calculate_all,
                      'request_calculate_all_hardware')
        pub.subscribe(self._request_do_create_matrix,
                      'request_create_hardware_matrix')
        pub.subscribe(self.request_do_delete, 'request_delete_hardware')
        pub.subscribe(self._request_do_delete_matrix,
                      'request_delete_hardware_matrix')
        pub.subscribe(self._request_do_insert, 'request_insert_hardware')
        pub.subscribe(self._request_do_insert_matrix,
                      'request_insert_hardware_matrix')
        pub.subscribe(self.request_do_make_composite_reference_designator,
                      'request_make_comp_ref_des')
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(self._request_do_select_all_matrix,
                      'request_select_hardware_matrix')
        pub.subscribe(self.request_do_update, 'request_update_hardware')
        pub.subscribe(self.request_do_update_all,
                      'request_update_all_hardware')
        pub.subscribe(self._request_do_update_matrix,
                      'request_update_hardware_matrix')
        pub.subscribe(self._request_set_attributes, 'mvw_editing_hardware')
        pub.subscribe(self._request_set_attributes, 'wvw_editing_hardware')

    def _request_do_calculate(self, node_id, hr_multiplier):
        """
        Request to calculate the selected Hardware item.

        :param int node_id: the Hardware ID of the item to calculate.
        :param float hr_multiplier: the multipliers for the hazard rate.
        :return: _attributes
        :rtype: dict
        """
        _attributes = self._dtm_data_model.do_calculate(
            node_id, hr_multiplier=hr_multiplier)

        # Update the value of calculated attributes.
        for _key in [
                'hazard_rate_percent', 'lambdaBP', 'Cac',
                'hazard_rate_logistics', 'lambdaBD', 'hazard_rate_software',
                'total_power_dissipation', 'Cl', 'temperature_junction', 'piP',
                'Cgs', 'reliability_miss_variance', 'piCYC', 'piU',
                'cost_failure', 'B1', 'B2', 'piNR', 'hazard_rate_dormant',
                'comp_ref_des', 'Csf', 'Csc', 'voltage_ratio', 'Cst', 'Csw',
                'Csv', 'total_cost', 'piCV', 'piCR', 'temperature_case',
                'hr_mission_variance', 'piCD', 'piCF', 'reliability_mission',
                'hazard_rate_active', 'mtbf_log_variance', 'Ccw', 'Ccv', 'Cpd',
                'Ccp', 'Cpf', 'piR', 'overstress', 'reason', 'Ccs', 'Ccf',
                'Cpv', 'Cbl', 'availability_mission', 'piQ', 'Cf',
                'temperature_hot_spot', 'Clc', 'hr_logistics_variance',
                'cost_hour', 'lambda_b', 'lambdaCYC', 'Cd',
                'reliability_logistics', 'C2', 'C1', 'Crd', 'Cmu',
                'current_ratio', 'avail_mis_variance', 'Ck', 'Ci', 'Ch', 'Cn',
                'Cm', 'Cc', 'Cb', 'Cg', 'Ce', 'mtbf_logistics', 'power_ratio',
                'Cy', 'Cbv', 'Cbt', 'reliability_log_variance', 'Cs', 'piTAPS',
                'Cq', 'Cp', 'Cw', 'Cv', 'Ct', 'Cnw', 'hr_specified_variance',
                'Cnp', 'total_part_count', 'Csz', 'Calt', 'lambdaEOS',
                'hazard_rate_mission', 'avail_log_variance', 'piK', 'piL',
                'piM', 'piN', 'Cr', 'Cga', 'piA', 'piC', 'piE', 'piF', 'A1',
                'A2', 'Cgp', 'piS', 'piT', 'Cgt', 'piV', 'Cgv', 'piPT',
                'mtbf_miss_variance', 'hr_active_variance', 'mtbf_mission',
                'piMFG', 'Cgl', 'piI', 'Cdc', 'Cdl', 'hr_dormant_variance',
                'Cdt', 'Cdw', 'Cdp', 'Cds', 'availability_logistics', 'Cdy',
                'temperature_rise'
        ]:
            self._request_set_attributes(node_id, _key, _attributes[_key])

        return _attributes

    def request_do_calculate_all(self, node_id, **kwargs):  # pylint: disable=arguments-differ
        """
        Request to calculate all hardware items.

        :return: list of cumulative results.
        :rtype: list
        """
        return self._dtm_data_model.do_calculate_all(
            node_id=node_id, hr_multiplier=self._hr_multiplier, **kwargs)

    def _request_do_create_matrix(self, revision_id, matrix_type):
        """
        Request to create or refresh a Hardware matrix.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param str matrix_type: the type of the Matrix to select all rows and
        :return: None
        :rtype: None
        """
        _dic_creates = {
            'hrdwr_rqrmnt':
            [self._dmx_hw_rqrmnt_matrix.do_create, 'requirement_id'],
            'hrdwr_vldtn':
            [self._dmx_hw_vldtn_matrix.do_create, 'validation_id'],
            'hrdwr_tstng': [self._dmx_hw_tstng_matrix.do_create, 'test_id']
        }

        try:
            _create_method = _dic_creates[matrix_type][0]
            _col_id = _dic_creates[matrix_type][1]
        except KeyError:
            _create_method = None

        try:
            _create_method(
                revision_id, matrix_type, rkey='hardware_id', ckey=_col_id)
        except TypeError:
            _error_code = 6
            _msg = 'RAMSTK ERROR: Failed to create matrix ' \
                   '{0:s}.'.format(matrix_type)

            RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def _request_do_delete_matrix(self, matrix_type, item_id, row=True):
        """
        Request to remove a row or column from the selected Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
                                Hardware matrix types are:

                                hrdwr_tstng = Hardware:Testing
                                hrdwr_vldtn = Hardware:Validation

        :param int item_id: the ID of the row or column item to remove from the
                            Matrix.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_deletes = {
            'hrdwr_rqrmnt': self._dmx_hw_rqrmnt_matrix.do_delete,
            'hrdwr_vldtn': self._dmx_hw_vldtn_matrix.do_delete,
            'hrdwr_tstng': self._dmx_hw_tstng_matrix.do_delete
        }

        try:
            self._matrix_delete_method = _dic_deletes[matrix_type]
        except KeyError:
            self._matrix_delete_method = None

        return RAMSTKDataController.request_do_delete_matrix(
            self, matrix_type, item_id, row=row)

    def _request_do_insert(self, revision_id, parent_id, part):
        """
        Request to add an RAMSTKHardware table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=revision_id, parent_id=parent_id, part=part)
        # TODO: Move this to seperate method that responds to the 'inserted_hardware' signal.
        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)

            _hardware_id = self.request_last_id()
            _heading = self.request_do_select(_hardware_id)['ref_des']

            # We add a record for each of the Hardware:X matrices.
            for _matrix in ['hrdwr_rqrmnt', 'hrdwr_vldtn']:
                if not part:
                    self.request_do_insert_matrix(
                        _matrix, _hardware_id, heading=_heading, row=True)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def _request_do_insert_matrix(self,
                                  matrix_type,
                                  item_id,
                                  heading,
                                  row=True):
        """
        Request the to add a new row or column to the Data Matrix.

        :param str matrix_type: the type of the Matrix to insert into.  Current
                                Hardware matrix types are:

                                hrdwr_rqrmnt = Hardware:Requirement
                                hrdwr_tstng = Hardware:Testing
                                hrdwr_vldtn = Hardware:Validation

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix.
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_inserts = {
            'hrdwr_rqrmnt': self._dmx_hw_rqrmnt_matrix.do_insert,
            'hrdwr_tstng': self._dmx_hw_tstng_matrix.do_insert,
            'hrdwr_vldtn': self._dmx_hw_vldtn_matrix.do_insert
        }

        try:
            self._matrix_insert_method = _dic_inserts[matrix_type]
        except KeyError:
            self._matrix_insert_method = None

        return RAMSTKDataController.request_do_insert_matrix(
            self, matrix_type, item_id, heading, row=row)

    def request_do_make_composite_reference_designator(self, node_id=1):
        """
        Request the composite reference designators be created.

        :keyword int node_id: the Treelib tree() node ID to start with to make
                              composite reference designators.  Defaults to the
                              top node.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        # Create the composite reference designators in the Hardware model.
        if self._dtm_data_model.dtm_hardware.do_make_composite_ref_des(
                node_id):
            _error_code = 3005
            _msg = 'RAMSTK ERROR: Failed to create all composite reference ' \
                   'designators for Node ID {0:d} and ' \
                   'children.'.format(node_id)

        # If that was successful, update the BoM attributes.
        if _error_code == 0:
            for _node_id in self._dtm_data_model.tree.nodes:
                if _node_id != 0:
                    _attributes = self._request_get_attributes(_node_id)
                    _comp_ref_des = self._dtm_data_model.dtm_hardware.do_select(
                        _node_id).comp_ref_des
                    _attributes['comp_ref_des'] = _comp_ref_des

        return _error_code, _msg

    def _request_do_select_all_matrix(self, revision_id, matrix_type):
        """
        Retrieve all the Matrices associated with the Hardware.

        :param int revision_id: the Revision ID to select the matrices for.
        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Hardware matrix types are:

                                hrdwr_rqrmnt = Hardware:Requirement
                                hrdwr_tstng = Hardware:Testing
                                hrdwr_vldtn = Hardware:Validation

        :return: (_matrix, _column_hdrs, _row_hdrs); the Pandas Dataframe,
                 noun names to use for column headings, noun names to use for
                 row headings.
        :rtype: (:class:`pandas.DataFrame`, dict, dict)
        """
        _matrix = None
        _column_hdrs = []
        _row_hdrs = []

        if matrix_type == 'hrdwr_rqrmnt':
            self._dmx_hw_rqrmnt_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='hardware_id',
                ckey='requirement_id',
                rheader='comp_ref_des',
                cheader='requirement_code')
            _matrix = self._dmx_hw_rqrmnt_matrix.dtf_matrix
            _column_hdrs = self._dmx_hw_rqrmnt_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_hw_rqrmnt_matrix.dic_row_hdrs

        elif matrix_type == 'hrdwr_tstng':
            self._dmx_hw_tstng_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='hardware_id',
                ckey='test_id',
                rheader='comp_ref_des',
                cheader='name')
            _matrix = self._dmx_hw_tstng_matrix.dtf_matrix
            _column_hdrs = self._dmx_hw_tstng_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_hw_tstng_matrix.dic_row_hdrs

        elif matrix_type == 'hrdwr_vldtn':
            self._dmx_hw_vldtn_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='hardware_id',
                ckey='validation_id',
                rheader='comp_ref_des',
                cheader='name')
            _matrix = self._dmx_hw_vldtn_matrix.dtf_matrix
            _column_hdrs = self._dmx_hw_vldtn_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_hw_vldtn_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def _request_do_update_matrix(self, revision_id, matrix_type):
        """
        Request to update the selected Data Matrix.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_type: the type of the Matrix to save.  Current
                                Hardware matrix types are:

                                hrdwr_tstng = Hardware:Testing
                                hrdwr_vldtn = Hardware:Validation

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_updates = {
            'hrdwr_rqrmnt': self._dmx_hw_rqrmnt_matrix.do_update,
            'hrdwr_tstng': self._dmx_hw_tstng_matrix.do_update,
            'hrdwr_vldtn': self._dmx_hw_vldtn_matrix.do_update
        }

        try:
            self._matrix_update_method = _dic_updates[matrix_type]
        except KeyError:
            self._matrix_update_method = None

        return RAMSTKDataController.request_do_update_matrix(
            self, revision_id, matrix_type)

    def _request_get_attributes(self, node_id):
        """
        Get the attributes of the record associated with Node ID and table.

        This is required to be local because the data package for the Hardware
        BoM tree is a dict with the attributes from all tables included.

        :param int node_id: the ID of the Hardware item to get attributes for.
        :return: attributes; the {attribute:value} dict.
        :rtype: dict
        """
        try:
            _attributes = self._dtm_data_model.tree.get_node(node_id).data
        except AttributeError:
            _attributes = ATTRIBUTES

        return _attributes

    def _request_set_attributes(self, module_id, key, value):
        """
        Set the attributes of the record associated with the Module ID.

        :param int module_id: the ID of the record in the RAMSTK Program
                              database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtm_data_model.tree.get_node(module_id).data
        if key in _attributes:
            _attributes[key] = value
        else:
            _return = True

        # Set the attributes for the individual tables.
        _error_code, _msg = self._dtm_data_model.dtm_hardware.do_select(
            module_id).set_attributes(_attributes)
        _return = (_return or RAMSTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_design_electric.do_select(
            module_id).set_attributes(_attributes)
        _return = (_return or RAMSTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_design_mechanic.do_select(
            module_id).set_attributes(_attributes)
        _return = (_return or RAMSTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_mil_hdbk_f.do_select(
            module_id).set_attributes(_attributes)
        _return = (_return or RAMSTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_nswc.do_select(
            module_id).set_attributes(_attributes)
        _return = (_return or RAMSTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        _error_code, _msg = self._dtm_data_model.dtm_reliability.do_select(
            module_id).set_attributes(_attributes)
        _return = (_return or RAMSTKDataController.do_handle_results(
            self, _error_code, _msg, None))

        self._dtm_data_model.tree.get_node(module_id).data = _attributes

        return _return
