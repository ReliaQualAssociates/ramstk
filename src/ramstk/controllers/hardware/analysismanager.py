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
from math import exp
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub
# noinspection PyPackageRequirements
from scipy.stats import expon, lognorm, norm, weibull_min

# RAMSTK Package Imports
from ramstk.analyses import derating, dormancy, stress
from ramstk.analyses.milhdbk217f import milhdbk217f
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


def hazard_rate_from_s_distribution(dist: str = 'expon', **kwargs) -> float:
    """Calculate the MTBF given a s-distribution and parameters.

    :param dist: the name of the distribution to find the hazard rate.
    :return: the calculated value of the hazard rate at time T.
    :rtype: float
    """
    _location = kwargs.get('location', 0.0)
    _scale = kwargs.get('scale', 1.0)
    _shape = kwargs.get('shape', 1.0)
    _time = kwargs.get('time', 1.0)

    if dist == 'expon':
        _hazard_rate = 1.0 / expon.mean(scale=_scale, loc=_location)
    elif dist == 'gaussian':
        _hazard_rate = norm.pdf(_shape, loc=_location, scale=_scale) / norm.sf(
            _shape, loc=_location, scale=_scale)
    elif dist == 'lognorm':
        _hazard_rate = lognorm.pdf(
            _time, _shape, loc=_location, scale=_scale) / lognorm.sf(
                _time, _shape, loc=_location, scale=_scale)
    elif dist == 'weibull':
        _hazard_rate = weibull_min.pdf(
            _time, _shape, loc=_location, scale=_scale) / weibull_min.sf(
                _time, _shape, loc=_location, scale=_scale)
    else:
        _hazard_rate = 0.0

    return _hazard_rate


def hazard_rate_from_specified_mtbf(mtbf: float, time: float = 1.0) -> float:
    """Calculate the hazard rate given an MTBF.

    This function calculates the hazard rate given an MTBF assuming an
    exponential distribution.

        >>> hazard_rate_from_specified_mtbf(10000.0, 1000000.0)
        100.0

        >>> hazard_rate_from_specified_mtbf(10000.0)
        0.0001

        >>> hazard_rate_from_specified_mtbf(0.0)
        0.0

    :param mtbf: the mean time between failure to convert to a hazard rate.
    :param time: the time multiplier for the hazard rate.
    :return: _hazard_rate; the hazard rate equivalent of the MTBF.
    :rtype: float
    """
    try:
        _hazard_rate = time / mtbf
    except ZeroDivisionError:
        _hazard_rate = 0.0

    return _hazard_rate


def mtbf_from_s_distribution(dist: str = 'expon', **kwargs) -> float:
    """Calculate the MTBF given a s-distribution and parameters.

    :param dist: the name of the distribution to find the MTBF.
    :return: the calculated value of the MTBF over time [0, T).
    :rtype: float
    """
    _location = kwargs.get('location', 0.0)
    _scale = kwargs.get('scale', 1.0)
    _shape = kwargs.get('shape', 1.0)

    if dist == 'expon':
        _mtbf = expon.mean(scale=_scale, loc=_location)
    elif dist == 'gaussian':
        _mtbf = norm.mean(scale=_shape, loc=_scale)
    elif dist == 'lognorm':
        _mtbf = lognorm.mean(_shape, scale=_scale, loc=_location)
    elif dist == 'weibull':
        _mtbf = weibull_min.mean(_shape, scale=_scale, loc=_location)
    else:
        _mtbf = 0.0

    return _mtbf


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
        pub.subscribe(super().on_get_tree, 'succeed_get_hardwares_tree')
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
                for _node_id in node.successors(self._tree.identifier):
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
        self._do_calculate_reliabilities(_node)

        # Let everyone know we succeeded calculating the hardware and
        # auto-save the results.
        pub.sendMessage(
            'succeed_calculate_hardware',
            tree=self._tree,
        )
        pub.sendMessage(
            'request_update_hardware',
            node_id=node_id,
        )
        pub.sendMessage(
            'request_get_all_hardware_attributes',
            node_id=node_id,
        )

    def _do_calculate_hazard_rate_active(self, node: treelib.Node) -> float:
        """Calculate the active hazard rate.

        :param node: the treelib.Node() to calculate.
        :return: _hazard_rate_active; the active hazard rate.
        :rtype: float
        """
        _hazard_rate_active: float = 0.0
        _hardware: Dict[str, Any] = node.data

        _time = self.RAMSTK_USER_CONFIGURATION.RAMSTK_HR_MULTIPLIER or 1.0

        if _hardware['reliability'].hazard_rate_type_id == 1:
            _hazard_rate_active = (self._do_predict_active_hazard_rate(node))
        elif _hardware['reliability'].hazard_rate_type_id == 2:
            _hazard_rate_active = _hardware[
                'reliability'].hazard_rate_specified / _time
        elif _hardware['reliability'].hazard_rate_type_id == 3:
            _hazard_rate_active = (hazard_rate_from_specified_mtbf(
                _hardware['reliability'].mtbf_specified, _time))
        elif _hardware['reliability'].hazard_rate_type_id == 4:
            # pylint: disable = unused-variable
            _hazard_rate_active, __ = (
                self._do_calculate_s_distribution(_hardware))

        _hazard_rate_active = (_hazard_rate_active
                               + _hardware['reliability'].add_adj_factor
                               ) * _hardware['reliability'].mult_adj_factor * (
                                   _hardware['hardware'].duty_cycle
                                   / 100.0) * _hardware['hardware'].quantity

        return _hazard_rate_active

    @staticmethod
    def _do_calculate_hazard_rate_dormant(node: treelib.Node) -> float:
        """Calculate the dormant hazard rate.

        :param node: the treelib.Node() to calculate.
        :return: _hazard_rate_dormant; the dormant hazard rate.
        :rtype: float
        """
        _hazard_rate_dormant: float = 0.0
        _hardware: Dict[str, Any] = node.data

        _hw_info = [
            _hardware['hardware'].category_id,
            _hardware['hardware'].subcategory_id,
            _hardware['reliability'].hazard_rate_active,
        ]
        _env_info = [
            _hardware['design_electric'].environment_active_id,
            _hardware['design_electric'].environment_dormant_id,
        ]

        _hazard_rate_dormant = dormancy.do_calculate_dormant_hazard_rate(
            _hw_info, _env_info)

        return _hazard_rate_dormant

    def _do_calculate_hazard_rates(
            self, node: treelib.Node) -> Tuple[float, float, float, float]:
        """Calculate the active, logistics, and mission hazard rates.

        Hazard rate types are:

            #. Assessed (MIL-HDBK-217F, NSWC, etc.)
            #. Specified, Hazard Rate
            #. Specified, MTBF
            #. s-Distribution

        :param node: the treelib.Node() at the top of the tree to to calculate.
        :return: _hazard_rate_active; the active hazard rate.
        :rtype: float
        """
        _hardware: Dict[str, Any] = node.data

        # Iterate through all parts if this is an assembly.
        if _hardware['hardware'].part != 1:
            _hazard_rate_active: float = 0.0
            _hazard_rate_dormant: float = 0.0
            _hazard_rate_logistics: float = 0.0
            _hazard_rate_mission: float = 0.0
            _p_node = node.identifier
            for _node_id in node.successors(self._tree.identifier):
                _node = self._tree.get_node(_node_id)
                (_temp_hr_active, _temp_hr_dormant, _temp_hr_logistics,
                 _temp_hr_mission) = self._do_calculate_hazard_rates(_node)
                _hazard_rate_active += _temp_hr_active
                _hazard_rate_dormant += _temp_hr_dormant
                _hazard_rate_logistics += _temp_hr_logistics
                _hazard_rate_mission += _temp_hr_mission

            self._tree.get_node(_p_node).data[
                'reliability'].hazard_rate_active = _hazard_rate_active
            self._tree.get_node(_p_node).data[
                'reliability'].hazard_rate_dormant = _hazard_rate_dormant
            self._tree.get_node(_p_node).data[
                'reliability'].hazard_rate_logistics = _hazard_rate_logistics
            self._tree.get_node(_p_node).data[
                'reliability'].hazard_rate_mission = _hazard_rate_mission

            self._do_calculate_mtbfs(self._tree.get_node(_p_node))

        else:
            _hardware['reliability'].hazard_rate_active = (
                self._do_calculate_hazard_rate_active(node))
            _hardware['reliability'].hazard_rate_dormant = (
                self._do_calculate_hazard_rate_dormant(node))

            _hardware['reliability'].hazard_rate_logistics = (
                _hardware['reliability'].hazard_rate_active
                + _hardware['reliability'].hazard_rate_dormant
                + _hardware['reliability'].hazard_rate_software)
            _hardware['reliability'].hazard_rate_mission = (
                _hardware['reliability'].hazard_rate_active
                + _hardware['reliability'].hazard_rate_software)

            self._do_calculate_mtbfs(node)

        return (_hardware['reliability'].hazard_rate_active,
                _hardware['reliability'].hazard_rate_dormant,
                _hardware['reliability'].hazard_rate_logistics,
                _hardware['reliability'].hazard_rate_mission)

    def _do_calculate_mtbfs(self, node: treelib.Node) -> None:
        """Calculate the MTBF related metrics.

        Hazard rate types are:

            #. Assessed (MIL-HDBK-217F, NSWC, etc.)
            #. Specified, Hazard Rate
            #. Specified, MTBF
            #. s-Distribution

        :param node: the treelib.Node() at the top of the tree to to calculate.
        :return: None
        :rtype: None
        """
        _hardware: Dict[str, Any] = node.data

        _time = self.RAMSTK_USER_CONFIGURATION.RAMSTK_HR_MULTIPLIER or 1.0

        if _hardware['reliability'].hazard_rate_type_id == 4:
            # pylint: disable = unused-variable
            __, _hardware['reliability'].mtbf_logistics = (
                self._do_calculate_s_distribution(_hardware))
        else:
            try:
                _hardware['reliability'].mtbf_logistics = (
                    _time / _hardware['reliability'].hazard_rate_logistics)
            except ZeroDivisionError:
                _hardware['reliability'].mtbf_logistics = 0.0

        try:
            _hardware['reliability'].mtbf_mission = (
                _time / _hardware['reliability'].hazard_rate_mission)
        except ZeroDivisionError:
            _hardware['reliability'].mtbf_mission = 0.0

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
            for _node_id in node.successors(self._tree.identifier):
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
            for _node_id in node.successors(self._tree.identifier):
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

    def _do_calculate_reliabilities(self, node: treelib.Node) -> None:
        """Calculate the reliability related metrics.

        :return: None
        :rtype: None
        :raises: ZeroDivisionError if the hazard rate multiplier is zero.
        """
        _hardware: Dict[str, Any] = node.data

        if _hardware['reliability'].hazard_rate_type_id != 0:
            self._do_calculate_hazard_rates(node)

        _time = self.RAMSTK_USER_CONFIGURATION.RAMSTK_HR_MULTIPLIER or 1.0

        _hardware['reliability'].reliability_logistics = exp(
            -1.0 * _hardware['reliability'].hazard_rate_logistics / _time)
        _hardware['reliability'].reliability_mission = exp(
            -1.0 * (_hardware['reliability'].hazard_rate_mission / _time)
            * _hardware['hardware'].mission_time)

        # Calculate reliabilities for any child hardware.
        for _node_id in node.successors(self._tree.identifier):
            _node = self._tree.get_node(_node_id)
            self._do_calculate_reliabilities(_node)

    @staticmethod
    def _do_calculate_s_distribution(
            hardware: Dict[str, object]) -> Tuple[float, float]:
        """Calculate the hazard rate or MTBF from a s-distribution.

        :param hardware: the data package for the node to be calculated.
        :return: _hazard_rate_active, _mtbf_active
        :rtype: tuple
        """
        _hazard_rate_active = 0.0
        _mtbf_active = 0.0
        _location = hardware['reliability'].location_parameter  # type: ignore
        _scale = hardware['reliability'].scale_parameter  # type: ignore
        _shape = hardware['reliability'].shape_parameter  # type: ignore
        _time = hardware['hardware'].mission_time  # type: ignore

        try:
            _dist = {
                1: 'expon',
                2: 'expon',
                3: 'weibull',
                4: 'weibull',
                5: 'lognorm',
                6: 'gaussian',
            }[hardware['reliability'].failure_distribution_id]  # type: ignore

            _hazard_rate_active = (hazard_rate_from_s_distribution(
                dist=_dist,
                location=_location,
                scale=_scale,
                shape=_shape,
                time=_time))
            _mtbf_active = (mtbf_from_s_distribution(dist=_dist,
                                                     location=_location,
                                                     scale=_scale,
                                                     shape=_shape))
        except KeyError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Failed to calculate hazard rate and MTBF for hardware '
                'ID {0}.  Attempting to use the specified distribution '
                'method without specifying a distribution.').format(
                    str(hardware['hardware'].hardware_id),  # type: ignore
                    _method_name)
            pub.sendMessage(
                'do_log_info',
                logger_name='INFO',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_calculate_hazard_rate',
                error_message=_error_msg,
            )

        return _hazard_rate_active, _mtbf_active

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

    @staticmethod
    def _do_predict_active_hazard_rate(node: treelib.Node) -> float:
        """Request that the hazard rate prediction be performed.

        :return: None
        :rtype: None
        """
        _hardware: Dict[str, Any] = node.data
        _hazard_rate_active: float = 0

        if _hardware['hardware'].part != 1:
            _hazard_rate_active = _hardware['reliability'].hazard_rate_active
        elif _hardware['reliability'].hazard_rate_method_id in [1, 2]:
            _attributes = {
                **_hardware['hardware'].get_attributes(),
                **_hardware['design_mechanic'].get_attributes(),
                **_hardware['design_electric'].get_attributes(),
                **_hardware['mil_hdbk_217f'].get_attributes(),
                **_hardware['nswc'].get_attributes(),
                **_hardware['reliability'].get_attributes()
            }

            try:
                _hazard_rate_active = (
                    milhdbk217f.do_predict_active_hazard_rate(**_attributes))
            except KeyError:
                _hazard_rate_active = 0.0

        return _hazard_rate_active

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
