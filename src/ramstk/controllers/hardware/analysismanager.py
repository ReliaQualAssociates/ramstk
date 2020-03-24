# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.AnalysisManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package analysis manager."""

# Standard Library Imports
from collections import OrderedDict
from math import exp

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import allocation, derating, dormancy, similaritem, stress
from ramstk.analyses.milhdbk217f import milhdbk217f
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """
    Contain the attributes and methods of the Hardware analysis manager.

    This class manages the hardware analysis for allocation, MIL-HDBK-217F,
    NSWC, and Similar Item.  Attributes of the hardware Analysis Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    """
    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the hardware analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super(AnalysisManager, self).__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_get_all_attributes,
                      'succeed_get_all_hardware_attributes')
        pub.subscribe(self.on_get_tree, 'succeed_get_hardware_tree')
        pub.subscribe(self._on_predict_reliability,
                      'succeed_predict_reliability')
        pub.subscribe(self.do_calculate_hardware, 'request_calculate_hardware')
        pub.subscribe(self._request_do_calculate_all_hardware,
                      'request_calculate_all_hardware')
        pub.subscribe(self.do_derating_analysis, 'request_derate_hardware')
        pub.subscribe(self.do_calculate_allocation_goals,
                      'request_calculate_goals')
        pub.subscribe(self.do_calculate_allocation,
                      'request_allocate_reliability')
        pub.subscribe(self._on_allocate_reliability,
                      'succeed_allocate_reliability')
        pub.subscribe(self.do_calculate_similar_item,
                      'request_calculate_similar_item')
        pub.subscribe(self.do_roll_up_change_descriptions,
                      'request_roll_up_change_descriptions')

    def _do_calculate_cost_metrics(self):
        """
        Calculate the cost related metrics.

        :return: None
        :rtype: None
        """
        self._attributes['total_cost'] = (self._attributes['cost']
                                          * self._attributes['quantity'])
        self._attributes['cost_hour'] = (
            self._attributes['total_cost']
            * self._attributes['hazard_rate_mission'])

        if self._attributes['part'] == 1:
            self._attributes['total_part_count'] = self._attributes['quantity']
            self._attributes['total_power_dissipation'] = (
                self._attributes['power_operating']
                * self._attributes['quantity'])
        else:
            self._attributes['total_part_count'] = (
                self._attributes['total_part_count']
                * self._attributes['quantity'])

    def _do_calculate_current_ratio(self):
        """
        Calculate the current ratio.

        :return: None
        :rtype: None
        """
        try:
            self._attributes['current_ratio'] = stress.calculate_stress_ratio(
                self._attributes['current_operating'],
                self._attributes['current_rated'])
        except ZeroDivisionError:
            pub.sendMessage(
                'fail_stress_analysis',
                error_message=("Failed to calculate current ratio for "
                               "hardware ID {0:s}; rated current is "
                               "zero.").format(
                                   str(self._attributes['hardware_id'])))

    def _do_calculate_hazard_rate_metrics(self):
        """
        Calculate the hazard rate related metrics.

        :return: None
        :rtype: None
        """
        if self._attributes['hazard_rate_type_id'] == 2:
            self._attributes['hazard_rate_active'] = self._attributes[
                'hazard_rate_specified']
        elif self._attributes['hazard_rate_type_id'] == 3:
            self._attributes['hazard_rate_active'] = (
                1.0 / self._attributes['mtbf_specified'])
        elif self._attributes['hazard_rate_type_id'] == 3:
            print("See bug #248.")

        self._attributes['hazard_rate_active'] = (
            self._attributes['hazard_rate_active']
            + self._attributes['add_adj_factor']
        ) * self._attributes['mult_adj_factor']

        self._attributes['hazard_rate_logistics'] = (
            self._attributes['hazard_rate_active']
            + self._attributes['hazard_rate_dormant']
            + self._attributes['hazard_rate_software'])
        self._attributes['hazard_rate_mission'] = (
            self._attributes['hazard_rate_active']
            + self._attributes['hazard_rate_software'])

        # If calculating using an s-distribution, the appropriate s-function
        # will estimate the variances.  Otherwise, assume an EXP distribution.
        if self._attributes['hazard_rate_type_id'] != 4:
            self._attributes['hr_specified_variance'] = self._attributes[
                'hazard_rate_specified']**2.0
            self._attributes['hr_logistics_variance'] = self._attributes[
                'hazard_rate_logistics']**2.0
            self._attributes['hr_mission_variance'] = self._attributes[
                'hazard_rate_mission']**2.0

    def _do_calculate_mtbf_metrics(self):
        """
        Calculate the MTBF related metrics.

        :return: None
        :rtype: None
        :raise: ZeroDivisionError if the logistics or mission hazard rate or
            their variances are zero.
        """
        self._attributes['mtbf_logistics'] = (
            1.0 / self._attributes['hazard_rate_logistics'])
        self._attributes['mtbf_mission'] = (
            1.0 / self._attributes['hazard_rate_mission'])

        # If calculating using an s-distribution, the appropriate s-function
        # will estimate the variances.  Otherwise, assume an EXP distribution.
        if self._attributes['hazard_rate_type_id'] != 4:
            self._attributes['mtbf_logistics_variance'] = (
                1.0 / self._attributes['hr_logistics_variance'])
            self._attributes['mtbf_mission_variance'] = (
                1.0 / self._attributes['hr_mission_variance'])
        if self._attributes['hazard_rate_type_id'] == 3:
            self._attributes['mtbf_specified_variance'] = (
                1.0 / (1.0 / self._attributes['mtbf_specified'])**2.0)

    def _do_calculate_power_ratio(self):
        """
        Calculate the power ratio.

        :return: None
        :rtype: None
        """
        try:
            self._attributes['power_ratio'] = stress.calculate_stress_ratio(
                self._attributes['power_operating'],
                self._attributes['power_rated'])
        except ZeroDivisionError:
            pub.sendMessage(
                'fail_stress_analysis',
                error_message=("Failed to calculate power ratio for "
                               "hardware ID {0:s}; rated power is "
                               "zero.").format(
                                   str(self._attributes['hardware_id'])))

    def _do_calculate_reliability_metrics(self):
        """
        Calculate the reliability related metrics.

        :return: None
        :rtype: None
        """
        try:
            self._do_calculate_hazard_rate_metrics()
            self._do_calculate_mtbf_metrics()
        except ZeroDivisionError:
            pub.sendMessage(
                'fail_calculate_hardware',
                error_message=(
                    "Failed to calculate hazard rate and/or MTBF "
                    "metrics for hardware ID {0:s}; too many inputs "
                    "equal to zero.  Specified MTBF={1:f}, active "
                    "h(t)={2:f}, dormant h(t)={3:f}, and software "
                    "h(t)={4:f}.").format(
                        str(self._attributes['hardware_id']),
                        self._attributes['mtbf_specified'],
                        self._attributes['hazard_rate_active'],
                        self._attributes['hazard_rate_dormant'],
                        self._attributes['hazard_rate_software']))

        self._attributes['reliability_logistics'] = exp(
            -1.0 * (self._attributes['hazard_rate_logistics']) * 1000000.0)
        self._attributes['reliability_mission'] = exp(
            -1.0 * (self._attributes['hazard_rate_mission'])
            * self._attributes['mission_time'])

    def _do_calculate_topic_633(self):
        """
        Calculate the similar item hazard rate per topic 6.3.3.

        .. note:: this analysis uses the adjustment factors from RAC/RiAC's The
            Reliability Tookkit, Commercial Practices Edition, section 6.3.3.

        :return: None
        :rtype: None
        """
        _environment = {
            'from': self._attributes['environment_from_id'],
            'to': self._attributes['environment_to_id']
        }
        _quality = {
            'from': self._attributes['quality_from_id'],
            'to': self._attributes['quality_to_id']
        }
        _temperature = {
            'from': self._attributes['temperature_from'],
            'to': self._attributes['temperature_to']
        }

        (self._attributes['change_factor_1'],
         self._attributes['change_factor_2'],
         self._attributes['change_factor_3'],
         self._attributes['result_1']) = similaritem.calculate_topic_633(
             _environment, _quality, _temperature,
             self._attributes['hazard_rate_active'])

    def _do_calculate_user_defined(self):
        """
        Calculate the user-defined similar item hazard rate.

        :return: None
        :rtype: None
        """
        _sia = OrderedDict({
            _key: None
            for _key in [
                'hr', 'pi1', 'pi2', 'pi3', 'pi3', 'pi4', 'pi5', 'pi6', 'pi7',
                'pi8', 'pi9', 'pi10', 'uf1', 'uf2', 'uf3', 'uf4', 'uf5', 'ui1',
                'ui2', 'ui3', 'ui4', 'ui5', 'equation1', 'equation2',
                'equation3', 'equation4', 'equation5', 'res1', 'res2', 'res3',
                'res4', 'res5'
            ]
        })

        _sia['hr'] = self._attributes['hazard_rate_active']

        _sia = similaritem.set_user_defined_change_factors(
            _sia, [
                self._attributes['change_factor_1'],
                self._attributes['change_factor_2'],
                self._attributes['change_factor_3'],
                self._attributes['change_factor_4'],
                self._attributes['change_factor_5'],
                self._attributes['change_factor_6'],
                self._attributes['change_factor_7'],
                self._attributes['change_factor_8'],
                self._attributes['change_factor_9'],
                self._attributes['change_factor_10']
            ])

        _sia = similaritem.set_user_defined_floats(_sia, [
            self._attributes['user_float_1'], self._attributes['user_float_2'],
            self._attributes['user_float_3'], self._attributes['user_float_4'],
            self._attributes['user_float_5']
        ])

        _sia = similaritem.set_user_defined_ints(_sia, [
            self._attributes['user_int_1'], self._attributes['user_int_2'],
            self._attributes['user_int_3'], self._attributes['user_int_4'],
            self._attributes['user_int_5']
        ])

        _sia = similaritem.set_user_defined_functions(_sia, [
            self._attributes['function_1'], self._attributes['function_2'],
            self._attributes['function_3'], self._attributes['function_4'],
            self._attributes['function_5']
        ])

        _sia = similaritem.set_user_defined_results(_sia, [
            self._attributes['result_1'], self._attributes['result_2'],
            self._attributes['result_3'], self._attributes['result_4'],
            self._attributes['result_5']
        ])

        _sia = similaritem.calculate_user_defined(_sia)

        self._attributes['result_1'] = _sia['res1']
        self._attributes['result_2'] = _sia['res2']
        self._attributes['result_3'] = _sia['res3']
        self._attributes['result_4'] = _sia['res4']
        self._attributes['result_5'] = _sia['res5']

    def _do_calculate_voltage_ratio(self):
        """
        Calculate the voltage ratio.

        :return: None
        :rtype: None
        """
        _voltage_operating = (self._attributes['voltage_ac_operating']
                              + self._attributes['voltage_dc_operating'])

        try:
            self._attributes['voltage_ratio'] = stress.calculate_stress_ratio(
                _voltage_operating, self._attributes['voltage_rated'])
        except ZeroDivisionError:
            pub.sendMessage(
                'fail_stress_analysis',
                error_message=("Failed to calculate voltage ratio for "
                               "hardware ID {0:s}; rated voltage is "
                               "zero.").format(
                                   str(self._attributes['hardware_id'])))

    def _on_allocate_reliability(self, attributes):
        """
        Respond to a successful reliability allocation message.

        :param dict attributes: the aggregate attributes dict updated with
            predicted values.
        :return: None
        :rtype: None
        """
        _attributes = self._tree.get_node(
            attributes['hardware_id']).data['allocation'].get_attributes()

        _attributes['hazard_rate_alloc'] = attributes['hazard_rate_alloc']
        _attributes['mtbf_alloc'] = attributes['mtbf_alloc']
        _attributes['reliability_alloc'] = attributes['reliability_alloc']

        _attributes.pop('revision_id')
        _attributes.pop('hardware_id')
        self._tree.get_node(
            attributes['hardware_id']).data['allocation'].set_attributes(
                _attributes)

    def _on_predict_reliability(self, attributes):
        """
        Respond to a successful reliability prediction message.

        :param dict attributes: the aggregate attributes dict updated with
            predicted values.
        :return: None
        :rtype: None
        """
        self._attributes = attributes

    def _request_do_calculate_all_hardware(self):
        """
        Request that the entire hardware system be calculated.

        :return: None
        :rtype: None
        """
        pub.sendMessage('request_get_hardware_tree')

        _cum_results = self.do_calculate_all_hardware(node_id=1)

        # If the sum of the results is greater than zero, SOMETHING got
        # calculated.  We'll assume that was a success and send the message.
        if sum(_cum_results) > 0.0:
            pub.sendMessage('succeed_calculate_all_hardware',
                            module_tree=self._tree)
            pub.sendMessage('request_update_all_hardware')

    def _request_do_predict_active_hazard_rate(self):
        """
        Request that the hazard rate prediction be performed.

        :return: None
        :rtype: None
        """
        if self._attributes['hazard_rate_method_id'] in [1, 2]:
            milhdbk217f.do_predict_active_hazard_rate(**self._attributes)

    def _request_do_stress_analysis(self):
        """
        Perform a stress analysis.

        :return: None
        :rtype: None
        """
        if self._attributes['category_id'] in [1, 2, 5, 6, 7, 8]:
            self._do_calculate_current_ratio()

        if self._attributes['category_id'] == 3:
            self._do_calculate_power_ratio()

        if self._attributes['category_id'] in [4, 5, 8]:
            self._do_calculate_voltage_ratio()

    def do_calculate_all_hardware(self, **kwargs):
        """
        Calculate all items in the system.

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
        _node_id = kwargs['node_id']
        _cum_results = [0.0, 0.0, 0.0, 0.0, 0, 0.0]

        # Check if there are children nodes of the node passed.
        if self._tree.get_node(_node_id).fpointer:
            # If there are children, calculate each of them first.
            for _subnode_id in self._tree.get_node(_node_id).fpointer:
                _results = self.do_calculate_all_hardware(node_id=_subnode_id)
                _cum_results[0] += _results[0]
                _cum_results[1] += _results[1]
                _cum_results[2] += _results[2]
                _cum_results[3] += _results[3]
                _cum_results[4] += int(_results[4])
                _cum_results[5] += _results[5]
            # Then calculate the parent node.
            self.do_calculate_hardware(_node_id, system=True)
            if self._attributes is not None:
                _cum_results[0] += self._attributes['hazard_rate_active']
                _cum_results[1] += self._attributes['hazard_rate_dormant']
                _cum_results[2] += self._attributes['hazard_rate_software']
                _cum_results[3] += self._attributes['total_cost']
                _cum_results[4] += int(self._attributes['total_part_count'])
                _cum_results[5] += self._attributes['total_power_dissipation']
        else:
            if self._tree.get_node(_node_id).data is not None:
                self.do_calculate_hardware(_node_id, system=True)
                _cum_results[0] += self._attributes['hazard_rate_active']
                _cum_results[1] += self._attributes['hazard_rate_dormant']
                _cum_results[2] += self._attributes['hazard_rate_software']
                _cum_results[3] += self._attributes['total_cost']
                _cum_results[4] += int(self._attributes['total_part_count'])
                _cum_results[5] += self._attributes['total_power_dissipation']

        if (self._tree.get_node(_node_id).data is not None
                and self._attributes['part'] == 0):
            self._attributes['hazard_rate_active'] = _cum_results[0]
            self._attributes['hazard_rate_dormant'] = _cum_results[1]
            self._attributes['hazard_rate_software'] = _cum_results[2]
            self._attributes['total_cost'] = _cum_results[3]
            self._attributes['total_part_count'] = int(_cum_results[4])
            self._attributes['total_power_dissipation'] = _cum_results[5]

        return _cum_results

    def _do_calculate_agree_total_elements(self, node_id):
        """
        Calculate the total number of elements for the AGREE method.

        :param int node_id: the node (hardware) ID of the hardware item whose
            goal is to be allocated.
        :return: _n_elements; the total number of sub-elements under the
            hardware item to be allocated.
        :rtype: int
        """
        _n_elements = 0
        for _node in self._tree.children(node_id):
            _attributes = _node.data['allocation'].get_attributes()
            _n_elements += _attributes['n_sub_elements']

        return _n_elements

    def _do_calculate_arinc_weight_factor(self, node_id):
        """
        Calculate the weight factor for the hardware at node ID.

        The ARINC weight factor is the quotient of the hardware item's hazard
        rate and the overall system hazard rate.

        :param int node_id: the node (hardware) ID of the hardware item whose
            weight factor is being allocated.
        :return: _weight_factor; the ratio of the hardware item's hazard rate
            and the overall system hazard rate.
        :rtype: float
        :raise: ZeroDivisionError if the parent hardware item's hazard rate is
            zero.
        """
        _node = self._tree.get_node(node_id)
        _parent_node = self._tree.parent(node_id)
        try:
            _weight_factor = (_node.data['reliability'].get_attributes()
                              ['hazard_rate_active']
                              / _parent_node.data['reliability'].
                              get_attributes()['hazard_rate_active'])
        except ZeroDivisionError:
            _weight_factor = 0.0
            pub.sendMessage(
                'fail_calculate_arinc_weight_factor',
                error_message=(
                    "Failed to allocate the reliability for hardware "
                    "ID {0:s}; zero hazard rate.").format(str(node_id)))

        return _weight_factor

    def _do_calculate_foo_cumulative_weight(self, node_id):
        """
        Calculate the cumulative weight for the FOO method.

        :param int node_id: the node (hardware) ID of the hardware item whose
            goal is to be allocated.
        :return: _cum_weight; the cumulative weighting factor for the hardware
            item to be allocated.
        :rtype: int
        """
        _cum_weight = 0
        for _node in self._tree.children(node_id):
            _attributes = _node.data['allocation'].get_attributes()
            _attributes['weight_factor'] = (_attributes['int_factor']
                                            * _attributes['soa_factor']
                                            * _attributes['op_time_factor']
                                            * _attributes['env_factor'])
            _cum_weight += _attributes['weight_factor']

        return _cum_weight

    def do_calculate_allocation(self, node_id):
        """
        Allocate a parent reliability goal to it's children.

        :param int node_id: the node (hardware) ID of the hardware item whose
            goal is to be allocated.
        :return: None
        :rtype: None
        """
        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested hardware item.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_all_hardware_attributes', node_id=node_id)

        self._attributes['n_sub_systems'] = len(self._tree.children(node_id))
        for _node in self._tree.children(node_id):
            _attributes = _node.data['allocation'].get_attributes()
            _method_old = _attributes['allocation_method_id']
            _mission_time_old = _attributes['mission_time']
            _attributes['allocation_method_id'] = self._attributes[
                'allocation_method_id']
            _attributes['mission_time'] = self._attributes['mission_time']
            if self._attributes['allocation_method_id'] == 1:
                self._attributes[
                    'n_sub_systems'] = self._do_calculate_agree_total_elements(
                        node_id)
                _attributes['n_sub_systems'] = self._attributes[
                    'n_sub_systems']
                _parent_goal = self._attributes['reliability_goal']
                _cum_weight = 0.0
            elif self._attributes['allocation_method_id'] == 2:
                _attributes[
                    'weight_factor'] = self._do_calculate_arinc_weight_factor(
                        _node.identifier)
                _parent_goal = self._attributes['hazard_rate_goal']
                _cum_weight = 0.0
            elif self._attributes['allocation_method_id'] == 3:
                _attributes['weight_factor'] = (
                    1.0 / self._attributes['n_sub_systems'])
                _parent_goal = self._attributes['reliability_goal']
                _cum_weight = 0.0
            elif self._attributes['allocation_method_id'] == 4:
                _parent_goal = self._attributes['hazard_rate_goal']
                _cum_weight = self._do_calculate_foo_cumulative_weight(node_id)

            allocation.do_allocate_reliability(_parent_goal, _cum_weight,
                                               **_attributes)

            _attributes['allocation_method_id'] = _method_old
            _attributes['mission_time'] = _mission_time_old

    def do_calculate_allocation_goals(self):
        """
        Calculate the allocation goals.

        :return: None
        :rtype: None
        """
        self._attributes = allocation.do_calculate_goals(**self._attributes)

    def do_calculate_hardware(self, node_id, system=False):
        """
        Calculate all metrics for the hardware associated with node ID.

        :param int node_id: the node (hardware) ID to calculate metrics.
        :keyword bool system: indicates whether a single item (default) or the
            entire system is being calculated.
        :return: None
        :rtype: None
        """
        _hr_multiplier = float(self.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER)

        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested hardware item.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_all_hardware_attributes', node_id=node_id)

        # If the assembly is to be calculated, set the attributes that are the
        # sum of the child attributes to zero.  Without doing this, they will
        # increment each time the system is calculated.
        if self._attributes['category_id'] == 0:
            # For h(t) type ID: 1=assessed
            if self._attributes['hazard_rate_type_id'] == 1:
                self._attributes['hazard_rate_active'] = 0.0
                self._attributes['hazard_rate_dormant'] = 0.0
                self._attributes['hazard_rate_software'] = 0.0
                self._attributes['total_part_count'] = 0
                self._attributes['total_power_dissipation'] = 0.0

            # For cost type ID: 2=calculated
            if self._attributes['cost_type_id'] == 2:
                self._attributes['total_cost'] = 0.0
        else:
            self._request_do_stress_analysis()
            self._request_do_predict_active_hazard_rate()
            self._attributes['hazard_rate_dormant'] = \
                dormancy.do_calculate_dormant_hazard_rate(
                    self._attributes['category_id'],
                    self._attributes['subcategory_id'],
                    self._attributes['environment_active_id'],
                    self._attributes['environment_dormant_id'],
                    self._attributes['hazard_rate_active'])

        self._attributes['add_adj_factor'] = (
            self._attributes['add_adj_factor'] / _hr_multiplier)
        self._attributes['hazard_rate_specified'] = (
            self._attributes['hazard_rate_specified'] / _hr_multiplier)
        self._attributes['hazard_rate_active'] = (
            self._attributes['hazard_rate_active'] / _hr_multiplier)
        self._attributes['hazard_rate_dormant'] = (
            self._attributes['hazard_rate_dormant'] / _hr_multiplier)
        self._attributes['hazard_rate_software'] = (
            self._attributes['hazard_rate_software'] / _hr_multiplier)

        self._do_calculate_reliability_metrics()
        self._do_calculate_cost_metrics()

        # If we're only calculating a single component/piece part, we send the
        # success message and a request to update that part in the database.
        # If we're calculating the entire system, we suppress this and make the
        # equivalent *all* calls.
        if not system:
            pub.sendMessage('succeed_calculate_hardware',
                            attributes=self._attributes)
            pub.sendMessage('request_update_hardware', node_id=node_id)

    def do_calculate_similar_item(self, node_id):
        """
        Perform a similar item calculates for currently selected item.

        :param int node_id: the node (hardware) ID to calculate.
        :return: None
        :rtype: None
        """
        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested hardware item.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_all_hardware_attributes', node_id=node_id)

        if self._attributes['similar_item_method_id'] == 1:
            self._do_calculate_topic_633()
        elif self._attributes['similar_item_method_id'] == 2:
            self._do_calculate_user_defined()

    def do_derating_analysis(self, node_id):
        """
        Perform a derating analysis.

        :param int node_id: the node (hardware) ID to derate.
        :return: None
        :rtype: None
        """
        self._attributes['reason'] = ""
        self._attributes['overstress'] = False

        def _do_check(overstress, stress_type):
            """
            Check the overstress condition and build a reason message.

            :param dict overstress: the dict containing the results of the
                overstress analysis.
            :param str stress_type: the overstress type being checked.
            :return: None
            :rtype: None
            """
            if overstress['harsh'][0]:
                self._attributes['overstress'] = True
                self._attributes['reason'] = self._attributes['reason'] + (
                    "Operating {0:s} is less than limit in a "
                    "harsh environment.\n".format(
                        str(stress_type)))
            if overstress['harsh'][1]:
                self._attributes['overstress'] = True
                self._attributes['reason'] = self._attributes['reason'] + (
                    "Operating {0:s} is greater than limit "
                    "in a harsh environment.\n".format(
                        str(stress_type)))
            if overstress['mild'][0]:
                self._attributes['overstress'] = True
                self._attributes['reason'] = self._attributes['reason'] + (
                    "Operating {0:s} is less than limit in a "
                    "mild environment.\n".format(
                        str(stress_type)))
            if overstress['mild'][1]:
                self._attributes['overstress'] = True
                self._attributes['reason'] = self._attributes['reason'] + (
                    "Operating {0:s} is greater than limit "
                    "in a mild environment.\n".format(
                        str(stress_type)))

        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested hardware item.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_all_hardware_attributes', node_id=node_id)

        _limits = self.RAMSTK_CONFIGURATION.RAMSTK_STRESS_LIMITS[
            self._attributes['category_id']]
        _current_limits = {
            'harsh': [0.0, _limits[0]],
            'mild': [0.0, _limits[1]]
        }
        _power_limits = {'harsh': [0.0, _limits[2]], 'mild': [0.0, _limits[3]]}
        _voltage_limits = {
            'harsh': [0.0, _limits[4]],
            'mild': [0.0, _limits[5]]
        }
        _deltat_limits = {
            'harsh': [0.0, _limits[6]],
            'mild': [0.0, _limits[7]]
        }
        _maxt_limits = {'harsh': [0.0, _limits[8]], 'mild': [0.0, _limits[9]]}

        _overstress = derating.check_overstress(
            self._attributes['current_ratio'], _current_limits)
        _do_check(_overstress, "current")
        _overstress = derating.check_overstress(
            self._attributes['power_ratio'], _power_limits)
        _do_check(_overstress, "power")
        _overstress = derating.check_overstress(
            self._attributes['voltage_ratio'], _voltage_limits)
        _do_check(_overstress, "voltage")

        pub.sendMessage('succeed_derate_hardware', attributes=self._attributes)

    def do_get_allocation_goal(self):
        """
        Retrieve the proper allocation goal.

        :return: _goal; the allocation goal measure.
        :rtype: float
        """
        return allocation.get_allocation_goal(**self._attributes)

    def do_roll_up_change_descriptions(self, node_id):
        """
        Concatenate all child change descriptions for the node ID hardware.

        :param int node_id: the node (hardware) ID to "roll-up."
        :return: None
        :rtype: None
        """
        _change_description_1 = ''
        _change_description_2 = ''
        _change_description_3 = ''
        _change_description_4 = ''
        _change_description_5 = ''
        _change_description_6 = ''
        _change_description_7 = ''
        _change_description_8 = ''
        _change_description_9 = ''
        _change_description_10 = ''

        for _node in self._tree.children(node_id):
            _name = _node.data['hardware'].get_attributes()['name']
            _attributes = _node.data['similar_item'].get_attributes()

            _change_description_1 += _name + ':\n' + _attributes[
                'change_description_1'] + '\n\n'
            _change_description_2 += _name + ':\n' + _attributes[
                'change_description_2'] + '\n\n'
            _change_description_3 += _name + ':\n' + _attributes[
                'change_description_3'] + '\n\n'
            _change_description_4 += _name + ':\n' + _attributes[
                'change_description_4'] + '\n\n'
            _change_description_5 += _name + ':\n' + _attributes[
                'change_description_5'] + '\n\n'
            _change_description_6 += _name + ':\n' + _attributes[
                'change_description_6'] + '\n\n'
            _change_description_7 += _name + ':\n' + _attributes[
                'change_description_7'] + '\n\n'
            _change_description_8 += _name + ':\n' + _attributes[
                'change_description_8'] + '\n\n'
            _change_description_9 += _name + ':\n' + _attributes[
                'change_description_9'] + '\n\n'
            _change_description_10 += _name + ':\n' + _attributes[
                'change_description_10'] + '\n\n'

        self._attributes[
            'change_description_1'] = _change_description_1
        self._attributes[
            'change_description_2'] = _change_description_2
        self._attributes[
            'change_description_3'] = _change_description_3
        self._attributes[
            'change_description_4'] = _change_description_4
        self._attributes[
            'change_description_5'] = _change_description_5
        self._attributes[
            'change_description_6'] = _change_description_6
        self._attributes[
            'change_description_7'] = _change_description_7
        self._attributes[
            'change_description_8'] = _change_description_8
        self._attributes[
            'change_description_9'] = _change_description_9
        self._attributes[
            'change_description_10'] = _change_description_10

        pub.sendMessage('succeed_roll_up_change_descriptions',
                        attributes=self._attributes)
