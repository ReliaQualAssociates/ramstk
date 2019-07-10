# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.AnalysisManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package analysis manager."""

# Standard Library Imports
from math import exp

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import Dormancy
from ramstk.analyses.milhdbk217f import MilHdbk217f


class AnalysisManager():
    """
    Contain the attributes and methods of the Hardware analysis manager.

    This class manages the hardware analysis for Allocation, MIL-HDBK-217F,
    NSWC, and Similar Item.  Attributes of the hardware Analysis Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    """

    def __init__(self, configuration, **kwargs):    # pylint: disable=unused-argument
        """
        Initialize an instance of the hardware analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        # Initialize private dictionary attributes.
        self._attributes = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_CONFIGURATION = configuration

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_get_all_attributes,
                      'succeed_get_all_attributes')
        pub.subscribe(self._on_predict_reliability,
                      'succeed_predict_reliability')
        pub.subscribe(self.do_calculate_hardware, 'request_calculate_hardware')

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
                error_msg=("Failed to calculate hazard rate and/or MTBF "
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

    def _on_get_all_attributes(self, attributes):
        """
        Request all the attributes for the hardware associated with node ID.

        :param dict attributes: the attributes dict for the table that was
            selected.
        :return: None
        :rtype: None
        """
        self._attributes = attributes

    def _on_predict_reliability(self, attributes):
        """
        Respond to a successful reliability prediction message.

        :param dict attributes: the aggregate attributes dict updated with
            predicted values.
        :return: None
        :rtype: None
        """
        self._attributes = attributes

    def _request_do_predict_active_hazard_rate(self):
        """
        Request that the hazard rate prediction be performed.

        :return: None
        :rtype: None
        """
        if self._attributes['hazard_rate_method_id'] in [1, 2]:
            MilHdbk217f.do_predict_active_hazard_rate(**self._attributes)

    def do_calculate_hardware(self, node_id):
        """
        Calculate all metrics for the hardware associated with node ID.

        :param int node_id: the node (hardware) ID to calculate metrics.
        :return: None
        :rtype: None
        """
        _hr_multiplier = float(self.RAMSTK_CONFIGURATION.RAMSTK_HR_MULTIPLIER)

        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested hardware item.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_all_attributes', node_id=node_id)

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
            self._request_do_predict_active_hazard_rate()
            self._attributes[
                'hazard_rate_dormant'] = Dormancy.do_calculate_dormant_hazard_rate(
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

        pub.sendMessage('succeed_calculate_hardware',
                        attributes=self._attributes)
        pub.sendMessage('request_update_hardware', node_id=node_id)
