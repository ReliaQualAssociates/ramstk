# -*- coding: utf-8 -*-
#
#       ramstk.modules.hardware.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package Data Model."""

# Standard Library Imports
from math import exp

# Third Party Imports
from pubsub import pub
from treelib.exceptions import DuplicatedNodeIdError, NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.analyses.prediction import Component
from ramstk.dao import (
    RAMSTKNSWC, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKHardware, RAMSTKMilHdbkF, RAMSTKReliability,
)
from ramstk.modules import RAMSTKDataModel


class HardwareBoMDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a Hardware Bill of Materials (BoM).

    Class for Hardware BoM data model.  This model builds a Hardware BoM from
    the Hardware, DesignElectric, DesignMechanic, MilHdbkF, NSWC, and
    Reliability data models.  This is a non-hierarchical relationship, such as:

        * Hardware Assembly 1
            - General Data
            - Electrical Design Parameters
            - Mechanical Design Parameters
            - MIL-HDBK-217FN2 Model Parameters
            - NSWC-11 Model Parameters
            - Reliability Parameters

    Attribute keys for the aggregate model are:

    ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'Cac', 'Calt', 'Cb', 'Cbl', 'Cbt',
     'Cbv', 'Cc', 'Ccf', 'Ccp', 'Ccs', 'Ccv', 'Ccw', 'Cd', 'Cdc', 'Cdl', 'Cdp',
     'Cds', 'Cdt', 'Cdw', 'Cdy', 'Ce', 'Cf', 'Cg', 'Cga', 'Cgl', 'Cgp', 'Cgs',
     'Cgt', 'Cgv', 'Ch', 'Ci', 'Ck', 'Cl', 'Clc', 'Cm', 'Cmu', 'Cn', 'Cnp',
     'Cnw', 'Cp', 'Cpd', 'Cpf', 'Cpv', 'Cq', 'Cr', 'Crd', 'Cs', 'Csc', 'Csf',
     'Cst', 'Csv', 'Csw', 'Csz', 'Ct', 'Cv', 'Cw', 'Cy', 'add_adj_factor',
     'alt_part_num', 'altitude_operating', 'application_id', 'area',
     'attachments', 'avail_log_variance', 'avail_mis_variance',
     'availability_logistics', 'availability_mission', 'balance_id',
     'cage_code', 'capacitance', 'casing_id', 'category_id', 'clearance',
     'comp_ref_des', 'configuration_id', 'construction_id', 'contact_form_id',
     'contact_gauge', 'contact_pressure', 'contact_rating_id', 'cost',
     'cost_failure', 'cost_hour', 'cost_type_id', 'current_operating',
     'current_rated', 'current_ratio', 'deflection', 'description',
     'diameter_coil', 'diameter_inner', 'diameter_outer', 'diameter_wire',
     'duty_cycle', 'environment_active_id', 'environment_dormant_id',
     'failure_distribution_id', 'family_id', 'feature_size', 'figure_number',
     'filter_size', 'flow_design', 'flow_operating', 'frequency_operating',
     'friction', 'hardware_id', 'hazard_rate_active', 'hazard_rate_dormant',
     'hazard_rate_logistics', 'hazard_rate_method_id', 'hazard_rate_mission',
     'hazard_rate_model', 'hazard_rate_percent', 'hazard_rate_software',
     'hazard_rate_specified', 'hazard_rate_type_id', 'hr_active_variance',
     'hr_dormant_variance', 'hr_logistics_variance', 'hr_mission_variance',
     'hr_specified_variance', 'impact_id', 'insert_id', 'insulation_id',
     'lambdaBD', 'lambdaBP', 'lambdaCYC', 'lambdaEOS', 'lambda_b', 'lcn',
     'leakage_allowable', 'length', 'length_compressed', 'length_relaxed',
     'level', 'load_design', 'load_id', 'load_operating', 'location_parameter',
     'lubrication_id', 'manufacturer_id', 'manufacturing_id', 'matching_id',
     'material_id', 'meyer_hardness', 'misalignment_angle', 'mission_time',
     'mtbf_log_variance', 'mtbf_logistics', 'mtbf_miss_variance',
     'mtbf_mission', 'mtbf_spec_variance', 'mtbf_specified', 'mult_adj_factor',
     'n_active_pins', 'n_circuit_planes', 'n_cycles', 'n_elements',
     'n_hand_soldered', 'n_ten', 'n_wave_soldered', 'name', 'nsn', 'offset',
     'operating_life', 'overstress', 'package_id', 'page_number', 'parent_id',
     'part', 'part_number', 'particle_size', 'piA', 'piC', 'piCD', 'piCF',
     'piCR', 'piCV', 'piCYC', 'piE', 'piF', 'piI', 'piK', 'piL', 'piM',
     'piMFG', 'piN', 'piNR', 'piP', 'piPT', 'piQ', 'piR', 'piS', 'piT',
     'piTAPS', 'piU', 'piV', 'power_operating', 'power_rated', 'power_ratio',
     'pressure_contact', 'pressure_delta', 'pressure_downstream',
     'pressure_rated', 'pressure_upstream', 'quality_id', 'quantity', 'reason',
     'ref_des', 'reliability_goal', 'reliability_goal_measure_id',
     'reliability_log_variance', 'reliability_logistics',
     'reliability_miss_variance', 'reliability_mission', 'remarks',
     'repairable', 'resistance', 'revision_id', 'rpm_design', 'rpm_operating',
     'scale_parameter', 'service_id', 'shape_parameter', 'specification_id',
     'specification_number', 'spring_index', 'subcategory_id',
     'surface_finish', 'survival_analysis_id', 'tagged_part', 'technology_id',
     'temperature_active', 'temperature_case', 'temperature_dormant',
     'temperature_hot_spot', 'temperature_junction', 'temperature_knee',
     'temperature_rated_max', 'temperature_rated_min', 'temperature_rise',
     'theta_jc', 'thickness', 'torque_id', 'total_cost', 'total_part_count',
     'total_power_dissipation', 'type_id', 'viscosity_design',
     'viscosity_dynamic', 'voltage_ac_operating', 'voltage_dc_operating',
     'voltage_esd', 'voltage_rated', 'voltage_ratio', 'water_per_cent',
     'weight', 'width_minimum', 'year_of_manufacture', 'years_in_production']
    """

    _tag = 'HardwareBoM'

    def __init__(self, dao, **kwargs):
        """
        Initialize a Hardware BoM data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._test = kwargs['test']

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dtm_hardware = HardwareDataModel(dao)
        self.dtm_design_electric = DesignElectricDataModel(dao)
        self.dtm_design_mechanic = DesignMechanicDataModel(dao)
        self.dtm_mil_hdbk_f = MilHdbkFDataModel(dao)
        self.dtm_nswc = NSWCDataModel(dao)
        self.dtm_reliability = ReliabilityDataModel(dao)

    def do_calculate(self, node_id, **kwargs):
        """
        Calculate RAMS attributes for the hardware item.

        :param int hardware_id: the ID of the hardware item to calculate.
        :return: _attributes
        :rtype: dict
        """
        _hr_multiplier = float(kwargs['hr_multiplier'])
        try:
            _attributes = self.tree.get_node(node_id).data
        except AttributeError:
            _attributes = None
            print(node_id)

        if _attributes is not None:
            if _attributes['category_id'] > 0:
                _attributes, __ = Component.calculate(**_attributes)
            else:
                # If the assembly is to be assessed, set the attributes that
                # are the sum of the child attributes to zero.  Without doing
                # this, they will increment each time the system is calculated.
                if _attributes['hazard_rate_type_id'] in [0, 1]:
                    _attributes['hazard_rate_active'] = 0.0
                    _attributes['hazard_rate_dormant'] = 0.0
                    _attributes['hazard_rate_software'] = 0.0
                    _attributes['total_part_count'] = 0
                    _attributes['total_power_dissipation'] = 0.0

                if _attributes['cost_type_id'] in [0, 2]:
                    _attributes['total_cost'] = 0.0

            _attributes['hazard_rate_active'] = (
                _attributes['hazard_rate_active'] / _hr_multiplier
            )
            _attributes['hazard_rate_dormant'] = (
                _attributes['hazard_rate_dormant'] / _hr_multiplier
            )
            _attributes['hazard_rate_software'] = (
                _attributes['hazard_rate_software'] / _hr_multiplier
            )

            _attributes = self._do_calculate_reliability_metrics(_attributes)
            _attributes = self._do_calculate_cost_metrics(_attributes)
            _attributes = self._do_calculate_metric_variances(_attributes)

        # If we're not running a test, let anyone who cares know a Stakeholder
        # input was calculated.
        if not self._test:
            pub.sendMessage('calculated_hardware', attributes=_attributes)

        return _attributes

    @staticmethod
    def _do_calculate_cost_metrics(attributes):
        """
        Calculate the metrics related to hardware costs.

        :param dict attributes: the attributes of the hardware item being
                                calculated.
        :return: attributes; the attributes dict with updated cost metrics.
        :rtype: dict
        """
        if attributes['cost_type_id'] == 1:
            attributes['total_cost'] = (
                attributes['cost'] * attributes['quantity']
            )

        try:
            attributes['cost_hour'] = (
                attributes['total_cost'] / attributes['mission_time']
            )
        except ZeroDivisionError:
            attributes['cost_hour'] = attributes['total_cost']

        attributes['cost_failure'] = (
            attributes['cost_hour'] * attributes['mtbf_logistics']
        )

        if attributes['part'] == 1:
            attributes['total_part_count'] = attributes['quantity']

        return attributes

    @staticmethod
    def _do_calculate_reliability_metrics(attributes):
        """
        Calculate the metrics related to hardware reliability.

        :param dict attributes: the attributes of the hardware item being
                                calculated.
        :return: attributes; the attributes dict with updated reliability
                 metrics.
        :rtype: dict
        """
        if attributes['hazard_rate_type_id'] == 2:
            attributes['hazard_rate_active'] = \
                attributes['hazard_rate_specified']
        elif attributes['hazard_rate_type_id'] == 3:
            attributes['hazard_rate_active'] = (
                1.0 / attributes['mtbf_specified']
            )

        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] +
            attributes['add_adj_factor']
        ) * attributes['mult_adj_factor']

        attributes['hazard_rate_logistics'] = (
            attributes['hazard_rate_active'] +
            attributes['hazard_rate_dormant'] +
            attributes['hazard_rate_software']
        )

        try:
            attributes['mtbf_logistics'] = (
                1.0 / attributes['hazard_rate_logistics']
            )
        except ZeroDivisionError:
            attributes['mtbf_logistics'] = 0.0
        try:
            attributes['mtbf_mission'] = attributes['hazard_rate_mission']
        except ZeroDivisionError:
            attributes['mtbf_mission'] = 0.0

        attributes['reliability_logistics'] = exp(
            -1.0 * (attributes['hazard_rate_logistics']) *
            attributes['mission_time'],
        )

        return attributes

    @staticmethod
    def _do_calculate_metric_variances(attributes):
        """
        Calculate the variances of several hardware metrics.

        :param dict attributes: the attributes of the hardware item being
                                calculated.
        :return: attributes; the attributes dict with updated cost metrics.
        :rtype: dict
        """
        attributes['hr_active_variance'] = attributes[
            'hazard_rate_active'
        ]**2.0
        attributes['hr_dormant_variance'] = attributes[
            'hazard_rate_dormant'
        ]**2.0
        attributes['hr_logistics_variance'] = attributes[
            'hazard_rate_logistics'
        ]**2.0

        try:
            attributes['mtbf_log_variance'] = (
                1.0 / attributes['hr_logistics_variance']
            )
        except ZeroDivisionError:
            attributes['mtbf_log_variance'] = 0.0
        try:
            attributes['mtbf_miss_variance'] = (
                1.0 / attributes['hr_mission_variance']
            )
        except ZeroDivisionError:
            attributes['mtbf_miss_variance'] = 0.0

        return attributes

    def do_calculate_all(self, **kwargs):
        """
        Calculate all items in the system.

        :param float hr_multiplier: the hazard rate multiplier.  This is used
                                    to allow the hazard rates to be entered and
                                    displayed in more human readable numbers,
                                    but have the calculations work out.
                                    Default value is 1E6 so hazard rates will
                                    be entered and displayed as
                                    failures/million hours.
        :param int node_id: the ID of the treelib Tree() node to start the
                            calculation at.
        :return: _cum_results; the list of cumulative results.  The list order
                 is:

                    * 0 - active hazard rate
                    * 1 - dormant hazard rate
                    * 2 - software hazard rate
                    * 3 - total cost
                    * 4 - part count
                    * 5 - power dissipation

        :rtype: list
        """
        _hr_multiplier = kwargs['hr_multiplier']
        _node_id = kwargs['node_id']
        _cum_results = [0.0, 0.0, 0.0, 0.0, 0, 0.0]

        # Check if there are children nodes of the node passed.
        if self.tree.get_node(_node_id).fpointer:
            _attributes = self.tree.get_node(_node_id).data

            # If there are children, calculate each of them first.
            for _subnode_id in self.tree.get_node(_node_id).fpointer:
                _results = self.do_calculate_all(
                    node_id=_subnode_id, hr_multiplier=_hr_multiplier,
                )
                _cum_results[0] += _results[0]
                _cum_results[1] += _results[1]
                _cum_results[2] += _results[2]
                _cum_results[3] += _results[3]
                _cum_results[4] += int(_results[4])
                _cum_results[5] += _results[5]
            # Then calculate the parent node.
            _attributes = self.do_calculate(
                _node_id, hr_multiplier=_hr_multiplier,
            )
            if _attributes is not None:
                _cum_results[0] += _attributes['hazard_rate_active']
                _cum_results[1] += _attributes['hazard_rate_dormant']
                _cum_results[2] += _attributes['hazard_rate_software']
                _cum_results[3] += _attributes['total_cost']
                _cum_results[4] += int(_attributes['total_part_count'])
                _cum_results[5] += _attributes['total_power_dissipation']
        else:
            if self.tree.get_node(_node_id).data is not None:
                _attributes = self.do_calculate(
                    _node_id, hr_multiplier=_hr_multiplier,
                )
                _cum_results[0] += _attributes['hazard_rate_active']
                _cum_results[1] += _attributes['hazard_rate_dormant']
                _cum_results[2] += _attributes['hazard_rate_software']
                _cum_results[3] += _attributes['total_cost']
                _cum_results[4] += int(_attributes['total_part_count'])
                _cum_results[5] += _attributes['total_power_dissipation']

        if self.tree.get_node(
                _node_id,
        ).data is not None and _attributes['part'] == 0:
            _attributes['hazard_rate_active'] = _cum_results[0]
            _attributes['hazard_rate_dormant'] = _cum_results[1]
            _attributes['hazard_rate_software'] = _cum_results[2]
            _attributes['total_cost'] = _cum_results[3]
            _attributes['total_part_count'] = int(_cum_results[4])
            _attributes['total_power_dissipation'] = _cum_results[5]

            _attributes = self._do_calculate_reliability_metrics(_attributes)
            _attributes = self._do_calculate_cost_metrics(_attributes)
            _attributes = self._do_calculate_metric_variances(_attributes)

        return _cum_results

    def do_delete(self, node_id):
        """
        Remove a Hardware item.

        :param int node_id: the ID of the Hardware item to be removed from the
                            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        # Delete the RAMSTKHardware entry.  Other RAMSTK Program database tables will
        # delete their entries based on CASCADE behavior.
        try:
            _hardware = self.dtm_hardware.tree.get_node(node_id).data
            if _hardware is not None:
                _error_code, _msg = self.dao.db_delete(_hardware, _session)
        except AttributeError:
            _error_code = 2005
            _msg = (
                'RAMSTK ERROR: Attempted to delete non-existent Hardware '
                'BoM record ID {0:s}.'
            ).format(str(node_id))

        _session.close()

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code == 0:
            self.tree.remove_node(node_id)
            # CASCADE DELETE removes the records from the database.  Now they
            # need to be removed from the data model trees.
            self.dtm_hardware.tree.remove_node(node_id)
            self.dtm_design_electric.tree.remove_node(node_id)
            self.dtm_design_mechanic.tree.remove_node(node_id)
            self.dtm_mil_hdbk_f.tree.remove_node(node_id)
            self.dtm_nswc.tree.remove_node(node_id)
            self.dtm_reliability.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            # If we're not running a test, let anyone who cares know a Hardware
            # was deleted.
            if not self._test:
                pub.sendMessage('deleted_hardware', tree=self.tree)
                pub.sendMessage('request_delete_allocation', node_id=node_id)
                pub.sendMessage('request_delete_similar_item', node_id=node_id)

        return _error_code, _msg

    def do_insert(self, **kwargs):
        """
        Add a new hardware item.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision_id = kwargs['revision_id']
        _parent_id = kwargs['parent_id']
        _part = kwargs['part']
        _error_code = 0
        _error_msg = ''
        _msg = ''

        _parent = self.dtm_hardware.do_select(_parent_id)
        try:
            _parent_is_part = _parent.part
        except AttributeError:
            _parent_is_part = 0

        if _parent_is_part == 1 and _part == 0:
            _error_code = 3006
            _msg = (
                "RAMSTK ERROR: You can not have a hardware assembly as a "
                "child of a component/piece part."
            )
        elif _parent_is_part == 1 and _part == 1:
            _error_code = 3006
            _msg = (
                "RAMSTK ERROR: You can not have a component/piece part as a "
                "child of another component/piece part."
            )
        else:
            _error_code, _msg = self.dtm_hardware.do_insert(
                revision_id=_revision_id, parent_id=_parent_id, part=_part,
            )

        if _error_code == 0:
            _data = {}
            _hardware_id = self.dtm_hardware.last_id
            _hardware = self.dtm_hardware.do_select(_hardware_id)
            _data = _hardware.get_attributes()

            _error_code, _error_msg = self.dtm_design_electric.do_insert(
                hardware_id=_hardware_id,
            )
            if _error_code != 0:
                _msg = _msg + _error_msg + '\n'
            else:
                _electrical = self.dtm_design_electric.do_select(_hardware_id)
                _data.update(_electrical.get_attributes())

            _error_code, _error_msg = self.dtm_design_mechanic.do_insert(
                hardware_id=_hardware_id,
            )
            if _error_code != 0:
                _msg = _msg + _error_msg + '\n'
            else:
                _mechanical = self.dtm_design_mechanic.do_select(_hardware_id)
                _data.update(_mechanical.get_attributes())

            _error_code, _error_msg = self.dtm_mil_hdbk_f.do_insert(
                hardware_id=_hardware_id,
            )
            if _error_code != 0:
                _msg = _msg + _error_msg + '\n'
            else:
                _mil_hdbk_f = self.dtm_mil_hdbk_f.do_select(_hardware_id)
                _data.update(_mil_hdbk_f.get_attributes())

            _error_code, _error_msg = self.dtm_nswc.do_insert(
                hardware_id=_hardware_id,
            )
            if _error_code != 0:
                _msg = _msg + _error_msg + '\n'
            else:
                _nswc = self.dtm_nswc.do_select(_hardware_id)
                _data.update(_nswc.get_attributes())

            _error_code, _error_msg = self.dtm_reliability.do_insert(
                hardware_id=_hardware_id,
            )
            if _error_code != 0:
                _msg = _msg + _error_msg + '\n'
            else:
                _reliability = self.dtm_reliability.do_select(_hardware_id)
                _data.update(_reliability.get_attributes())

            self.tree.create_node(
                _hardware.comp_ref_des,
                _hardware_id,
                parent=_hardware.parent_id,
                data=_data,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _hardware_id)

            # If we're not running a test, let anyone who cares know a new
            # Hardware was inserted.
            if not self._test:
                pub.sendMessage('inserted_hardware', tree=self.tree)
                pub.sendMessage('request_insert_allocation', revision_id=_revision_id, hardware_id=_hardware_id, parent_id=_parent_id)
                pub.sendMessage('request_insert_similar_item', revision_id=_revision_id, hardware_id=_hardware_id, parent_id=_parent_id)

        return _error_code, _msg

    def do_select(self, node_id, **kwargs):
        """
        Retrieve instance of the RAMSTK<MODULE> model for the Node ID passed.

        :param int node_id: the Node ID of the data package to retrieve.
        :return: the aggregate dict of attributes from each of the data models
                 that comprise a Hardware BoM data model or None if the
                 requested Node ID does not exist.
        :rtype: dict
        """
        _attributes = {}

        _entity = self.dtm_hardware.do_select(node_id)
        if _entity is not None:
            _attributes.update(_entity.get_attributes())
            _attributes.update(
                self.dtm_design_electric.do_select(node_id).get_attributes(),
            )
            _attributes.update(
                self.dtm_design_mechanic.do_select(node_id).get_attributes(),
            )
            _attributes.update(
                self.dtm_mil_hdbk_f.do_select(node_id).get_attributes(),
            )
            _attributes.update(
                self.dtm_nswc.do_select(node_id).get_attributes(),
            )
            _attributes.update(
                self.dtm_reliability.do_select(node_id).get_attributes(),
            )

        return _attributes

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Hardware BoM data from the RAMSTK Program database.

        :param int revision_id: the Revision ID to select the Hardware BoM for.
        :return: None
        :rtype: None
        """
        _revision_id = kwargs['revision_id']
        for _node in self.dtm_hardware.do_select_all(
                revision_id=_revision_id,
        ).all_nodes()[1:]:
            _data = {}
            _hardware_id = _node.data.hardware_id
            _data = _node.data.get_attributes()
            try:
                _electrical = self.dtm_design_electric.do_select_all(
                    hardware_id=_hardware_id,
                )
                _data.update(
                    _electrical.nodes[_hardware_id].data.get_attributes(),
                )
            except KeyError:
                pass

            try:
                _mechanical = self.dtm_design_mechanic.do_select_all(
                    hardware_id=_hardware_id,
                )
                _data.update(
                    _mechanical.nodes[_hardware_id].data.get_attributes(),
                )
            except KeyError:
                pass

            try:
                _mil_hdbk_f = self.dtm_mil_hdbk_f.do_select_all(
                    hardware_id=_hardware_id,
                )
                _data.update(
                    _mil_hdbk_f.nodes[_hardware_id].data.get_attributes(),
                )
            except KeyError:
                pass

            try:
                _nswc = self.dtm_nswc.do_select_all(hardware_id=_hardware_id)
                _data.update(_nswc.nodes[_hardware_id].data.get_attributes())
            except KeyError:
                pass

            try:
                _reliability = self.dtm_reliability.do_select_all(
                    hardware_id=_hardware_id,
                )
                _data.update(
                    _reliability.nodes[_hardware_id].data.get_attributes(),
                )
            except KeyError:
                pass

            try:
                self.tree.create_node(
                    _node.data.comp_ref_des,
                    _hardware_id,
                    parent=_node.data.parent_id,
                    data=_data,
                )

                # pylint: disable=attribute-defined-outside-init
                # It is defined in RAMSTKDataModel.__init__
                try:
                    self.last_id = max(self.last_id, _hardware_id)
                except TypeError:
                    self.last_id = _hardware_id
            except DuplicatedNodeIdError:
                pass

        # If we're not running a test and there were harsware returned,
        # let anyone who cares know the Hardware has been selected.
        if not self._test and self.tree.size() > 1:
            pub.sendMessage('retrieved_hardware', tree=self.tree)

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Hardware ID of the Hardware to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        _code, _msg = self.dtm_hardware.do_update(node_id)

        if _code != 0:
            _error_code += _code
            _msg = _msg + _msg + '\n'

        _code, _error_msg = self.dtm_reliability.do_update(node_id)
        if _code != 0:
            _error_code += _code
            _msg = _msg + _error_msg + '\n'

        _code, _error_msg = self.dtm_design_electric.do_update(node_id)
        if _code != 0:
            _error_code += _code
            _msg = _msg + _error_msg + '\n'

        _code, _error_msg = self.dtm_design_mechanic.do_update(node_id)
        if _code != 0:
            _error_code += _code
            _msg = _msg + _error_msg + '\n'

        _code, _error_msg = self.dtm_mil_hdbk_f.do_update(node_id)
        if _code != 0:
            _error_code += _code
            _msg = _msg + _error_msg + '\n'

        _code, _error_msg = self.dtm_nswc.do_update(node_id)
        if _code != 0:
            _error_code += _code
            _msg = _msg + _error_msg + '\n'

        if _error_code == 0:
            if not self._test:
                _attributes = self.do_select(node_id)
                pub.sendMessage('updated_hardware', attributes=_attributes)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKHardware table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the hardware bill "
                "of materials."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more line items in the hardware "
                "bill of materials did not update."
            )

        return _error_code, _msg


class HardwareDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a Hardware item.

    An RAMSTK Project will consist of one or more Hardware items.  The attributes
    of a Hardware item are:
    """

    _tag = 'Hardware'  # pragma: no cover

    def __init__(self, dao):
        """
        Initialize a Hardware data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Hardware from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKHardware table in the
        connected RAMSTK Program database.  It then add each to the Hardware data
        model treelib.Tree().

        :param int revision_id: the Revision ID to select the hardware for.
        :return: tree; the Tree() of RAMSTKHardware data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _hardware in _session.query(RAMSTKHardware).filter(
                RAMSTKHardware.revision_id == _revision_id,
        ).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _hardware.get_attributes()
            _hardware.set_attributes(_attributes)
            try:
                self.tree.create_node(
                    _hardware.comp_ref_des,
                    _hardware.hardware_id,
                    parent=_hardware.parent_id,
                    data=_hardware,
                )

                # pylint: disable=attribute-defined-outside-init
                # It is defined in RAMSTKDataModel.__init__
                try:
                    self.last_id = max(self.last_id, _hardware.hardware_id)
                except TypeError:
                    self.last_id = _hardware.hardware_id
            except (DuplicatedNodeIdError, NodeIDAbsentError):
                pass

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKHardware table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _hardware = RAMSTKHardware()
        _hardware.revision_id = kwargs['revision_id']
        _hardware.parent_id = kwargs['parent_id']
        _hardware.part = kwargs['part']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _hardware,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _hardware.name,
                _hardware.hardware_id,
                parent=_hardware.parent_id,
                data=_hardware,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = _hardware.hardware_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKHardware table.

        :param int node_id: the ID of the RAMSTKHardware record to be removed from
                            the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Hardware ID {0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Hardware ID of the Hardware to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Hardware ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKHardware table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the hardware table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the hardware table "
                "did not update."
            )

        return _error_code, _msg

    def do_make_composite_ref_des(self, node_id=1):
        """
        Make the composite reference designators.

        :keyword int node_id: the ID of the node to start making the composite
                              reference designators.
        :return: False if successful or True if an error is encountered
        :rtype: bool
        """
        _return = False
        _pref_des = ''

        # Retrieve the parent hardware item's composite reference designator.
        _node = self.tree.get_node(node_id)
        if self.tree.get_node(_node.bpointer).data is not None:
            _pref_des = self.tree.get_node(_node.bpointer).data.comp_ref_des

        if _pref_des != '':
            _node.data.comp_ref_des = _pref_des + ':' + _node.data.ref_des
        else:
            _node.data.comp_ref_des = _node.data.ref_des

        # Now make the composite reference designator for all the chil nodes.
        for _child_node in self.tree.children(node_id):
            self.do_make_composite_ref_des(node_id=_child_node.identifier)

        return _return


class DesignElectricDataModel(RAMSTKDataModel):
    """Contain the attributes and methods of an Electrical Design model."""

    _tag = 'DesignElectric'

    def __init__(self, dao):
        """
        Initialize an Electrical Design parameter data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all RAMSTKDesignElectric records from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKDesignElectric table
        in the connected RAMSTK Program database.  It then add each to the
        Design Electric data model treelib.Tree().

        :return: tree; the treelib Tree() of RAMSTKDesignElectric data models that
                 comprise the DesignElectric tree.
        :rtype: :class:`treelib.Tree`
        """
        _hardware_id = kwargs['hardware_id']

        # Don't use the RAMSTKDataModel.do_select_all() method because we don't
        # want to clear the tree or we'll only be left with the last hardware
        # ID passed.
        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        for _design in _session.query(RAMSTKDesignElectric).\
                filter(RAMSTKDesignElectric.hardware_id == _hardware_id).all():
            try:
                self.tree.create_node(
                    _design.hardware_id,
                    _design.hardware_id,
                    parent=0,
                    data=_design,
                )

                # pylint: disable=attribute-defined-outside-init
                # It is defined in RAMSTKDataModel.__init__
                try:
                    self.last_id = max(self.last_id, _design.hardware_id)
                except TypeError:
                    self.last_id = _design.hardware_id
            except DuplicatedNodeIdError:
                pass

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKDesignElectric table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _design = RAMSTKDesignElectric()
        _design.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _design,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _design.hardware_id,
                _design.hardware_id,
                parent=0,
                data=_design,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _design.hardware_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKDesignElectric table.

        :param int node_id: the ID of the RAMSTKDesignElectric record to be
                            removed from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'DesignElectric record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the DesignElectric ID of the DesignElectric record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent ' \
                   'DesignElectric record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKDesignElectric table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the electrical "
                "design table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more line items in the electrical "
                "design table did not update."
            )

        return _error_code, _msg


class DesignMechanicDataModel(RAMSTKDataModel):
    """Contain the attributes and methods of a Mechanical Design model."""

    _tag = 'DesignMechanic'

    def __init__(self, dao):
        """
        Initialize a Mechanical Design parameter data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all RAMSTKDesignMechanic records from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKDesignMechanic table
        in the connected RAMSTK Program database.  It then add each to the
        Mechanical Design parameter data model treelib.Tree().

        :return: tree; the treelib Tree() of RAMSTKDesignMechanic data models that
                 comprise the DesignMechanic tree.
        :rtype: :class:`treelib.Tree`
        """
        _hardware_id = kwargs['hardware_id']

        # Don't use the RAMSTKDataModel.do_select_all() method because we don't
        # want to clear the tree or we'll only be left with the last hardware
        # ID passed.
        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        for _design in _session.query(RAMSTKDesignMechanic).\
                filter(RAMSTKDesignMechanic.hardware_id == _hardware_id).all():
            try:
                self.tree.create_node(
                    _design.hardware_id,
                    _design.hardware_id,
                    parent=0,
                    data=_design,
                )

                # pylint: disable=attribute-defined-outside-init
                # It is defined in RAMSTKDataModel.__init__
                try:
                    self.last_id = max(self.last_id, _design.hardware_id)
                except TypeError:
                    self.last_id = _design.hardware_id
            except DuplicatedNodeIdError:
                pass

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKDesignMechanic table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _design = RAMSTKDesignMechanic()
        _design.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _design,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _design.hardware_id,
                _design.hardware_id,
                parent=0,
                data=_design,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _design.hardware_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKDesignMechanic table.

        :param int node_id: the ID of the RAMSTKDesignMechanic record to be
                            removed from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'DesignMechanic record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the DesignMechanic ID of the DesignMechanic record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent ' \
                   'DesignMechanic record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKDesignMechanic table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the mechanical "
                "design table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more line items in the mechanical "
                "design table did not update."
            )

        return _error_code, _msg


class MilHdbkFDataModel(RAMSTKDataModel):
    """Contain the attributes and methods of a MIL-HDBK-217F model."""

    _tag = 'MilHdbkF'

    def __init__(self, dao):
        """
        Initialize a MIL-HDBK-217F data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all RAMSTKMilHdbkF records from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKMilHdbkF table
        in the connected RAMSTK Program database.  It then add each to the
        MIL-HDBK-217F data model treelib.Tree().

        :return: tree; the treelib Tree() of RAMSTKMilHdbkF data models that
                 comprise the MilHdbkF tree.
        :rtype: :class:`treelib.Tree`
        """
        _hardware_id = kwargs['hardware_id']

        # Don't use the RAMSTKDataModel.do_select_all() method because we don't
        # want to clear the tree or we'll only be left with the last hardware
        # ID passed.
        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        for _milhdbkf in _session.query(RAMSTKMilHdbkF).\
                filter(RAMSTKMilHdbkF.hardware_id == _hardware_id).all():
            try:
                self.tree.create_node(
                    _milhdbkf.hardware_id,
                    _milhdbkf.hardware_id,
                    parent=0,
                    data=_milhdbkf,
                )

                # pylint: disable=attribute-defined-outside-init
                # It is defined in RAMSTKDataModel.__init__
                try:
                    self.last_id = max(self.last_id, _milhdbkf.hardware_id)
                except TypeError:
                    self.last_id = _milhdbkf.hardware_id
            except DuplicatedNodeIdError:
                pass

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKMilHdbkF table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _milhdbkf = RAMSTKMilHdbkF()
        _milhdbkf.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _milhdbkf,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _milhdbkf.hardware_id,
                _milhdbkf.hardware_id,
                parent=0,
                data=_milhdbkf,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _milhdbkf.hardware_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKMilHdbkF table.

        :param int node_id: the ID of the RAMSTKMilHdbkF record to be
                            removed from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'MilHdbkF record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the MilHdbkF ID of the MilHdbkF record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent ' \
                   'MilHdbkF record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKMilHdbkF table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the MIL-HDBK-217 "
                "table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the MIL-HDBK-217 "
                "table did not update."
            )

        return _error_code, _msg


class NSWCDataModel(RAMSTKDataModel):
    """Contain the attributes and methods of a NSWC model."""

    _tag = 'NSWC'

    def __init__(self, dao):
        """
        Initialize a NSWC data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all RAMSTKNSWC records from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKNSWC table
        in the connected RAMSTK Program database.  It then add each to the
        NSWC data model treelib.Tree().

        :return: tree; the treelib Tree() of RAMSTKNSWC data models that
                 comprise the NSWC tree.
        :rtype: :class:`treelib.Tree`
        """
        _hardware_id = kwargs['hardware_id']

        # Don't use the RAMSTKDataModel.do_select_all() method because we don't
        # want to clear the tree or we'll only be left with the last hardware
        # ID passed.
        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        for _nswc in _session.query(RAMSTKNSWC).\
                filter(RAMSTKNSWC.hardware_id == _hardware_id).all():
            try:
                self.tree.create_node(
                    _nswc.hardware_id, _nswc.hardware_id, parent=0, data=_nswc,
                )

                # pylint: disable=attribute-defined-outside-init
                # It is defined in RAMSTKDataModel.__init__
                try:
                    self.last_id = max(self.last_id, _nswc.hardware_id)
                except TypeError:
                    self.last_id = _nswc.hardware_id
            except DuplicatedNodeIdError:
                pass

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKNSWC table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _nswc = RAMSTKNSWC()
        _nswc.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _nswc,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _nswc.hardware_id, _nswc.hardware_id, parent=0, data=_nswc,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _nswc.hardware_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKNSWC table.

        :param int node_id: the ID of the RAMSTKNSWC record to be
                            removed from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'NSWC record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the NSWC ID of the NSWC record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent ' \
                   'NSWC record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKNSWC table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all records in the NSWC table.")
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the NSWC table "
                "did not update."
            )

        return _error_code, _msg


class ReliabilityDataModel(RAMSTKDataModel):
    """Contain the attributes and methods of a Reliability model."""

    _tag = 'Reliability'

    def __init__(self, dao):
        """
        Initialize a Reliability data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):
        """
        Retrieve all RAMSTKReliability records from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKReliability table
        in the connected RAMSTK Program database.  It then add each to the
        Reliability data model treelib.Tree().

        :param int hardware_id: the ID of the Hardware item to retrieve the
                                Reliability parameters for.
        :return: tree; the treelib Tree() of RAMSTKReliability data models that
                 comprise the Reliability tree.
        :rtype: :class:`treelib.Tree`
        """
        _hardware_id = kwargs['hardware_id']

        # Don't use the RAMSTKDataModel.do_select_all() method because we don't
        # want to clear the tree or we'll only be left with the last hardware
        # ID passed.
        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        for _reliability in _session.query(RAMSTKReliability).\
                filter(RAMSTKReliability.hardware_id == _hardware_id).all():
            try:
                self.tree.create_node(
                    _reliability.hardware_id,
                    _reliability.hardware_id,
                    parent=0,
                    data=_reliability,
                )

                # pylint: disable=attribute-defined-outside-init
                # It is defined in RAMSTKDataModel.__init__
                try:
                    self.last_id = max(self.last_id, _reliability.hardware_id)
                except TypeError:
                    self.last_id = _reliability.hardware_id
            except DuplicatedNodeIdError:
                pass

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKReliability table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _reliability = RAMSTKReliability()
        _reliability.hardware_id = kwargs['hardware_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _reliability,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _reliability.hardware_id,
                _reliability.hardware_id,
                parent=0,
                data=_reliability,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _reliability.hardware_id)

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKReliability table.

        :param int node_id: the ID of the RAMSTKReliability record to be
                            removed from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Reliability record ID ' \
                          '{0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Reliability ID of the Reliability record
                            to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent ' \
                   'Reliability record ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):
        """
        Update all RAMSTKReliability table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the reliability "
                "table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the reliability "
                "table did not update."
            )

        return _error_code, _msg
