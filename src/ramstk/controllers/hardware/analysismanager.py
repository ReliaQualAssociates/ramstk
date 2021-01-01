# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.AnalysisManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package analysis manager."""

# Standard Library Imports
import inspect
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import derating, stress
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """Contain the attributes and methods of the Hardware analysis manager.

    This class manages the hardware analysis for allocation, MIL-HDBK-217F,
    NSWC, and Similar Item.  Attributes of the hardware Analysis Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[Any, Any]) -> None:
        """Initialize an instance of the hardware analysis manager.

        :param configuration: the RAMSTKUserConfiguration instance associated
            with the current instance of the RAMSTK application.
        """
        super().__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_get_all_attributes,
                      'succeed_get_all_hardware_attributes')
        pub.subscribe(super().on_get_tree, 'succeed_retrieve_hardware')
        pub.subscribe(super().on_get_tree, 'succeed_get_hardware_tree')
        pub.subscribe(super().on_get_tree, 'succeed_update_hardware')

        pub.subscribe(self._do_calculate_hardware,
                      'request_calculate_hardware')
        pub.subscribe(self._do_derating_analysis, 'request_derate_hardware')

    def _do_calculate_cost_metrics(self, node: treelib.Node) -> float:
        """Calculate the cost related metrics.

        :param node: the treelib.Node() at the top of the tree to to calculate.
        :return: _total_cost; the total cost.
        :rtype: float
        """
        _hardware: Dict[str, Any] = node.data
        _total_cost: float = 0.0

        if _hardware['hardware'].cost_type_id == 2:
            if _hardware['hardware'].part == 1:
                _total_cost = _hardware['hardware'].cost * _hardware[
                    'hardware'].quantity
            else:
                for _node_id in node.fpointer:
                    _node = self._tree.get_node(_node_id)
                    _total_cost += self._do_calculate_cost_metrics(_node)
                _total_cost = _total_cost * _hardware['hardware'].quantity
        else:
            _total_cost = _hardware['hardware'].total_cost

        _hardware['hardware'].total_cost = _total_cost

        return _total_cost

    @staticmethod
    def _do_calculate_current_ratio(node: treelib.Node) -> None:
        """Calculate the current ratio.

        :return: None
        :rtype: None
        """
        _hardware = node.data

        try:
            _hardware['design_electric'].current_ratio = (
                stress.calculate_stress_ratio(
                    _hardware['design_electric'].current_operating,
                    _hardware['design_electric'].current_rated))
        except ZeroDivisionError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Failed to calculate current ratio for hardware ID {'
                '0}.  Rated current={2}, operating current={3}.').format(
                    str(_hardware['hardware'].hardware_id), _method_name,
                    _hardware['design_electric'].current_rated,
                    _hardware['design_electric'].current_operating)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_stress_analysis',
                error_message=_error_msg,
            )

    def _do_calculate_hardware(self, node_id: int) -> None:
        """Calculate all metrics for the hardware associated with node ID.

        :param node_id: the node (hardware) ID to calculate metrics.
        :return: None
        :rtype: None
        """
        _node: treelib.Node = self._tree.get_node(node_id)

        self._do_calculate_cost_metrics(_node)
        self._do_calculate_part_count(_node)
        self._do_calculate_power_dissipation(_node)
        self._request_do_stress_analysis(_node)

        # Let everyone know we succeeded calculating the hardware and
        # auto-save the results.
        pub.sendMessage(
            'succeed_calculate_hardware',
            module_tree=self._tree,
        )
        pub.sendMessage('request_update_all_hardware', )

    def _do_calculate_part_count(self, node: treelib.Node) -> int:
        """Calculate the total part count of a hardware item.

        :param node: the treelib.Node() at the top of the tree to to calculate.
        :return: _part_count; the total part count.
        :rtype: int
        """
        _hardware: Dict[str, Any] = node.data
        _part_count: int = 0

        if _hardware['hardware'].part == 1:
            _part_count = _hardware['hardware'].quantity
        else:
            for _node_id in node.fpointer:
                _node = self._tree.get_node(_node_id)
                _part_count += self._do_calculate_part_count(_node)
            _part_count = _part_count * _hardware['hardware'].quantity

        _hardware['hardware'].total_part_count = _part_count

        return _part_count

    def _do_calculate_power_dissipation(self, node: treelib.Node) -> float:
        """Calculate the total power dissipation of a hardware item.

        :param node: the treelib.Node() at the top of the tree to to calculate.
        :return: _power_dissipation; the total power dissipation.
        :rtype: float
        """
        _hardware: Dict[str, Any] = node.data
        _power_dissipation: float = 0.0

        if _hardware['hardware'].part == 1:
            _power_dissipation = _hardware[
                'design_electric'].power_operating * _hardware[
                    'hardware'].quantity
        else:
            for _node_id in node.fpointer:
                _node = self._tree.get_node(_node_id)
                _power_dissipation += self._do_calculate_power_dissipation(
                    _node)
            _power_dissipation = _power_dissipation * _hardware[
                'hardware'].quantity

        _hardware['hardware'].total_power_dissipation = _power_dissipation

        return _power_dissipation

    @staticmethod
    def _do_calculate_power_ratio(node: treelib.Node) -> None:
        """Calculate the power ratio.

        :return: None
        :rtype: None
        """
        _hardware = node.data

        try:
            _hardware[
                'design_electric'].power_ratio = stress.calculate_stress_ratio(
                    _hardware['design_electric'].power_operating,
                    _hardware['design_electric'].power_rated)
        except ZeroDivisionError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Failed to calculate power ratio for hardware ID {'
                '0}.  Rated power={2}, operating power={3}.').format(
                    str(_hardware['hardware'].hardware_id), _method_name,
                    _hardware['design_electric'].power_rated,
                    _hardware['design_electric'].power_operating)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_stress_analysis',
                error_message=_error_msg,
            )

    @staticmethod
    def _do_calculate_voltage_ratio(node: treelib.Node) -> None:
        """Calculate the voltage ratio.

        :return: None
        :rtype: None
        """
        _hardware = node.data

        _voltage_operating = (
            _hardware['design_electric'].voltage_ac_operating
            + _hardware['design_electric'].voltage_dc_operating)

        try:
            _hardware['design_electric'].voltage_ratio = (
                stress.calculate_stress_ratio(
                    _voltage_operating,
                    _hardware['design_electric'].voltage_rated))
        except ZeroDivisionError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Failed to calculate voltage ratio for hardware ID {'
                '0}.  Rated voltage={2}, operating ac voltage={3}, '
                'operating DC voltage={4}.').format(
                    str(_hardware['hardware'].hardware_id), _method_name,
                    _hardware['design_electric'].voltage_rated,
                    _hardware['design_electric'].voltage_ac_operating,
                    _hardware['design_electric'].voltage_dc_operating)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_stress_analysis',
                error_message=_error_msg,
            )

    def _do_derating_analysis(self, node_id: int) -> None:
        """Perform a derating analysis.

        :param node_id: the node (hardware) ID to derate.
        :return: None
        :rtype: None
        """
        self._attributes['reason'] = ""
        self._attributes['overstress'] = False

        def _do_check(overstress: Dict[str, List[float]],
                      stress_type: str) -> None:
            """Check the overstress condition and build a reason message.

            :param overstress: the dict containing the results of the
                overstress analysis.
            :param stress_type: the overstress type being checked.
            :return: None
            :rtype: None
            """
            if overstress['harsh'][0]:
                self._attributes['overstress'] = True
                self._attributes['reason'] = self._attributes['reason'] + (
                    "Operating {0:s} is less than limit in a "
                    "harsh environment.\n".format(str(stress_type)))
            if overstress['harsh'][1]:
                self._attributes['overstress'] = True
                self._attributes['reason'] = self._attributes['reason'] + (
                    "Operating {0:s} is greater than limit "
                    "in a harsh environment.\n".format(str(stress_type)))
            if overstress['mild'][0]:
                self._attributes['overstress'] = True
                self._attributes['reason'] = self._attributes['reason'] + (
                    "Operating {0:s} is less than limit in a "
                    "mild environment.\n".format(str(stress_type)))
            if overstress['mild'][1]:
                self._attributes['overstress'] = True
                self._attributes['reason'] = self._attributes['reason'] + (
                    "Operating {0:s} is greater than limit "
                    "in a mild environment.\n".format(str(stress_type)))

        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested hardware item.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_all_hardware_attributes', node_id=node_id)

        _limits = self.RAMSTK_USER_CONFIGURATION.RAMSTK_STRESS_LIMITS[
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
        # ISSUE: Implement temperture stress limits in _do_check().
        # //
        # // In the method _do_check() and _do_derating_analysis() in the
        # // Hardware module analysis manager, there is no check for excessive
        # // delta temperature or high temperature limits.  These either need
        # // to be removed because no hardware item has temperature limits or
        # // the checks need to be implemented.  This will require new tests.
        #  _deltat_limits = {
        #     'harsh': [0.0, _limits[6]],
        #     'mild': [0.0, _limits[7]]
        #  }
        #  _maxt_limits = {'harsh': [0.0, _limits[8]], 'mild': [0.0, _limits[
        #  9]]}

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

    def _request_do_stress_analysis(self, node: treelib.Node) -> None:
        """Perform a stress analysis.

        :param node: the treelib.Node() at the top of the tree to to calculate.
        :return: None
        :rtype: None
        """
        _hardware = node.data

        if _hardware['hardware'].category_id in [1, 2, 5, 6, 7, 8]:
            self._do_calculate_current_ratio(node)

        if _hardware['hardware'].category_id == 3:
            self._do_calculate_power_ratio(node)

        if _hardware['hardware'].category_id in [4, 5, 8]:
            self._do_calculate_voltage_ratio(node)
