# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hazard.analysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hazard Controller Package analysis manager."""

# Standard Library Imports
from collections import OrderedDict
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import fha
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """Contain the attributes and methods of the Hazard analysis manager.

    This class manages the functional hazards analysis (FHA). Attributes
    of the hazard Analysis Manager are:
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        """Initialize an instance of the hazard analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
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
                      'succeed_get_hazard_attributes')
        pub.subscribe(super().on_get_tree, 'succeed_get_hazard_tree')

        pub.subscribe(self.do_calculate_fha, 'request_calculate_fha')

    def do_calculate_fha(self, node_id: int) -> None:
        """Perform a hazards analysis calculation for currently selected item.

        :param node_id: the node (hazard) ID to calculate.
        :return: None
        :rtype: None
        """
        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested hazard.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/hazards.
        pub.sendMessage(
            'request_get_hazard_attributes',
            node_id=node_id,
            table='hazard',
        )

        self._do_calculate_hri()
        self._do_calculate_user_defined()

        pub.sendMessage(
            'request_set_all_hazard_attributes',
            attributes=self._attributes,
        )
        pub.sendMessage('request_get_hazard_tree', )
        pub.sendMessage(
            'succeed_calculate_hazard',
            node_id=node_id,
        )

    def _do_calculate_hri(self) -> None:
        """Calculate the hazard risk index (HRI).

        This method calculates the assembly and system level HRI for both
        before and after mitigation actions.

        :return: None
        :rtype: None
        """
        self._attributes['assembly_hri'] = fha.calculate_hri(
            self._attributes['assembly_probability'],
            self._attributes['assembly_severity'])
        self._attributes['system_hri'] = fha.calculate_hri(
            self._attributes['system_probability'],
            self._attributes['system_severity'])
        self._attributes['assembly_hri_f'] = fha.calculate_hri(
            self._attributes['assembly_probability_f'],
            self._attributes['assembly_severity_f'])
        self._attributes['system_hri_f'] = fha.calculate_hri(
            self._attributes['system_probability_f'],
            self._attributes['system_severity_f'])

    def _do_calculate_user_defined(self) -> None:
        """Calculate the user-defined similar item hazard rate.

        :return: None
        :rtype: None
        """
        _fha = OrderedDict({
            _key: ''
            for _key in [
                'uf1', 'uf2', 'uf3', 'ui1', 'ui2', 'ui3', 'equation1',
                'equation2', 'equation3', 'equation4', 'equation5', 'res1',
                'res2', 'res3', 'res4', 'res5'
            ]
        })

        _fha = fha.set_user_defined_floats(_fha, [
            self._attributes['user_float_1'], self._attributes['user_float_2'],
            self._attributes['user_float_3']
        ])

        _fha = fha.set_user_defined_ints(_fha, [
            self._attributes['user_int_1'], self._attributes['user_int_2'],
            self._attributes['user_int_3']
        ])

        _fha = fha.set_user_defined_functions(_fha, [
            self._attributes['function_1'], self._attributes['function_2'],
            self._attributes['function_3'], self._attributes['function_4'],
            self._attributes['function_5']
        ])

        _fha = fha.set_user_defined_results(_fha, [
            self._attributes['result_1'], self._attributes['result_2'],
            self._attributes['result_3'], self._attributes['result_4'],
            self._attributes['result_5']
        ])

        _fha = fha.calculate_user_defined(_fha)

        self._attributes['result_1'] = float(_fha['res1'])
        self._attributes['result_2'] = float(_fha['res2'])
        self._attributes['result_3'] = float(_fha['res3'])
        self._attributes['result_4'] = float(_fha['res4'])
        self._attributes['result_5'] = float(_fha['res5'])
