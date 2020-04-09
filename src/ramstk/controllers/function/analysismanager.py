# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.analysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Controller Package analysis manager."""

# Standard Library Imports
from collections import OrderedDict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import fha
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """
    Contain the attributes and methods of the Function analysis manager.

    This class manages the functional analysis for functional hazards analysis
    (FHA).  Attributes of the function Analysis Manager are:
    """
    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the function analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super().__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_get_all_attributes,
                      'succeed_get_all_function_attributes')
        pub.subscribe(self.on_get_tree, 'succeed_get_function_tree')
        pub.subscribe(self.do_calculate_fha, 'request_calculate_fha')

    def _do_calculate_hri(self, hazard):
        """
        Calculate the hazard risk index (HRI).

        This method calculates the assembly and system level HRI for both
        before and after mitigation actions.

        :param hazard: the hazard model to calculate the HRI for.
        :type hazard: :class:`ramstk.models.programdb.RAMSTKHazardAnalysis.RAMSTKHazardAnalysis`
        :return: None
        :rtype: None
        """
        _attributes = hazard.get_attributes()
        _hazard_id = _attributes['hazard_id']

        _attributes['assembly_hri'] = fha.calculate_hri(
            _attributes['assembly_probability'],
            _attributes['assembly_severity'])
        _attributes['system_hri'] = fha.calculate_hri(
            _attributes['system_probability'], _attributes['system_severity'])
        _attributes['assembly_hri_f'] = fha.calculate_hri(
            _attributes['assembly_probability_f'],
            _attributes['assembly_severity_f'])
        _attributes['system_hri_f'] = fha.calculate_hri(
            _attributes['system_probability_f'],
            _attributes['system_severity_f'])

        # Update the hazard analysis record attributes.
        _attributes.pop('revision_id')
        _attributes.pop('function_id')
        _attributes.pop('hazard_id')
        self._attributes['hazards'][_hazard_id].set_attributes(_attributes)

    def _do_calculate_user_defined(self, hazard):
        """
        Calculate the user-defined similar item hazard rate.

        :param hazard: the hazard model to calculate the HRI for.
        :type hazard: :class:`ramstk.models.programdb.RAMSTKHazardAnalysis.RAMSTKHazardAnalysis`
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
        _attributes = hazard.get_attributes()
        _hazard_id = _attributes['hazard_id']

        _fha = fha.set_user_defined_floats(_fha, [
            _attributes['user_float_1'], _attributes['user_float_2'],
            _attributes['user_float_3']
        ])

        _fha = fha.set_user_defined_ints(_fha, [
            _attributes['user_int_1'], _attributes['user_int_2'],
            _attributes['user_int_3']
        ])

        _fha = fha.set_user_defined_functions(_fha, [
            _attributes['function_1'], _attributes['function_2'],
            _attributes['function_3'], _attributes['function_4'],
            _attributes['function_5']
        ])

        _fha = fha.set_user_defined_results(_fha, [
            _attributes['result_1'], _attributes['result_2'],
            _attributes['result_3'], _attributes['result_4'],
            _attributes['result_5']
        ])

        _fha = fha.calculate_user_defined(_fha)

        _attributes['result_1'] = float(_fha['res1'])
        _attributes['result_2'] = float(_fha['res2'])
        _attributes['result_3'] = float(_fha['res3'])
        _attributes['result_4'] = float(_fha['res4'])
        _attributes['result_5'] = float(_fha['res5'])

        # Update the hazard analysis record attributes.
        _attributes.pop('revision_id')
        _attributes.pop('function_id')
        _attributes.pop('hazard_id')
        self._attributes['hazards'][_hazard_id].set_attributes(_attributes)

    def do_calculate_fha(self, node_id: int) -> None:
        """
        Perform a hazards analysis calculation for currently selected item.

        :param int node_id: the node (function) ID to calculate.
        :return: None
        :rtype: None
        """
        # Retrieve all the attributes from all the RAMSTK data tables for the
        # requested function.  We need to build a comprehensive dict of
        # attributes to pass to the various analysis methods/functions.
        pub.sendMessage('request_get_all_function_attributes', node_id=node_id)

        _hazards = self._attributes['hazards']
        for _key in _hazards:
            self._do_calculate_hri(_hazards[_key])
            self._do_calculate_user_defined(_hazards[_key])

        pub.sendMessage('succeed_calculate_hazard', node_id=node_id)
