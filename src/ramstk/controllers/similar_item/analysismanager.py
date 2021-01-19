# -*- coding: utf-8 -*-
#
#       ramstk.controllers.similar_itme.analysismanager.py is part of The
#       RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Similar Item Controller Package analysis manager."""

# Standard Library Imports
from collections import OrderedDict
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import similaritem
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """Contain the attributes and methods of the Similar Item analysis manager.

    This class manages the similar item analysis.  Attributes of the
    similar item Analysis Manager are:
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[Any, Any]) -> None:
        """Initialize an instance of the similar item analysis manager.

        :param configuration: the RAMSTKUserConfiguration instance associated
            with the current instance of the RAMSTK application.
        """
        super().__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_hardware_hrs: Dict[int, float] = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._node_hazard_rate: float = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_get_all_attributes,
                      'succeed_get_similar_item_attributes')
        pub.subscribe(super().on_get_tree, 'succeed_get_similar_item_tree')
        pub.subscribe(super().on_get_tree, 'succeed_retrieve_similar_item')
        pub.subscribe(super().on_get_tree, 'succeed_update_similar_item')

        pub.subscribe(self._do_calculate_similar_item,
                      'request_calculate_similar_item')
        pub.subscribe(self._do_roll_up_change_descriptions,
                      'request_roll_up_change_descriptions')
        pub.subscribe(self._on_get_hardware_attributes,
                      'succeed_get_hardwares_tree')

    def _do_calculate_similar_item(self, node_id: int) -> None:
        """Perform a similar item calculates for currently selected item.

        :param node_id: the node (similar item) ID to calculate.
        :return: None
        :rtype: None
        """
        _node: treelib.Node = self._tree.get_node(node_id)

        if _node.data['similar_item'].similar_item_method_id == 1:
            self._do_calculate_topic_633(_node)
            pub.sendMessage(
                'succeed_calculate_similar_item',
                tree=self._tree,
            )
        elif _node.data['similar_item'].similar_item_method_id == 2:
            self._do_calculate_user_defined(_node)
            pub.sendMessage(
                'succeed_calculate_similar_item',
                tree=self._tree,
            )

    def _do_calculate_topic_633(self, node: treelib.Node) -> None:
        """Calculate the similar item hazard rate per topic 6.3.3.

        .. note:: this analysis uses the adjustment factors from RAC/RiAC's The
            Reliability Toolkit, Commercial Practices Edition, section 6.3.3.

        :param node: the treelib.Node() whose similar item results are to be
            calculated.
        :return: None
        :rtype: None
        """
        _attributes: Dict[str,
                          Any] = node.data['similar_item'].get_attributes()

        _environment = {
            'from': _attributes['environment_from_id'],
            'to': _attributes['environment_to_id']
        }
        _quality = {
            'from': _attributes['quality_from_id'],
            'to': _attributes['quality_to_id']
        }
        _temperature = {
            'from': _attributes['temperature_from'],
            'to': _attributes['temperature_to']
        }

        _node_hazard_rate = self._dic_hardware_hrs[_attributes['hardware_id']]

        (_attributes['change_factor_1'], _attributes['change_factor_2'],
         _attributes['change_factor_3'],
         _attributes['result_1']) = similaritem.calculate_topic_633(
             _environment, _quality, _temperature, _node_hazard_rate)

        node.data['similar_item'].change_factor_1 = _attributes[
            'change_factor_1']
        node.data['similar_item'].change_factor_2 = _attributes[
            'change_factor_2']
        node.data['similar_item'].change_factor_3 = _attributes[
            'change_factor_3']
        node.data['similar_item'].result_1 = _attributes['result_1']

    def _do_calculate_user_defined(self, node: treelib.Node) -> None:
        """Calculate the user-defined similar item hazard rate.

        :param node: the treelib.Node() whose similar item results are to be
            calculated.
        :return: None
        :rtype: None
        """
        _attributes: Dict[str,
                          Any] = node.data['similar_item'].get_attributes()

        _sia: Dict[str, Any] = OrderedDict({
            _key: None
            for _key in [
                'hr', 'pi1', 'pi2', 'pi3', 'pi3', 'pi4', 'pi5', 'pi6', 'pi7',
                'pi8', 'pi9', 'pi10', 'uf1', 'uf2', 'uf3', 'uf4', 'uf5', 'ui1',
                'ui2', 'ui3', 'ui4', 'ui5', 'equation1', 'equation2',
                'equation3', 'equation4', 'equation5', 'res1', 'res2', 'res3',
                'res4', 'res5'
            ]
        })

        _sia['hr'] = self._dic_hardware_hrs[_attributes['hardware_id']]

        _sia = similaritem.set_user_defined_change_factors(
            _sia, [
                _attributes['change_factor_1'], _attributes['change_factor_2'],
                _attributes['change_factor_3'], _attributes['change_factor_4'],
                _attributes['change_factor_5'], _attributes['change_factor_6'],
                _attributes['change_factor_7'], _attributes['change_factor_8'],
                _attributes['change_factor_9'], _attributes['change_factor_10']
            ])

        _sia = similaritem.set_user_defined_floats(_sia, [
            _attributes['user_float_1'], _attributes['user_float_2'],
            _attributes['user_float_3'], _attributes['user_float_4'],
            _attributes['user_float_5']
        ])

        _sia = similaritem.set_user_defined_ints(_sia, [
            _attributes['user_int_1'], _attributes['user_int_2'],
            _attributes['user_int_3'], _attributes['user_int_4'],
            _attributes['user_int_5']
        ])

        _sia = similaritem.set_user_defined_functions(_sia, [
            _attributes['function_1'], _attributes['function_2'],
            _attributes['function_3'], _attributes['function_4'],
            _attributes['function_5']
        ])

        _sia = similaritem.set_user_defined_results(_sia, [
            _attributes['result_1'], _attributes['result_2'],
            _attributes['result_3'], _attributes['result_4'],
            _attributes['result_5']
        ])

        _sia = similaritem.calculate_user_defined(_sia)

        node.data['similar_item'].result_1 = _sia['res1']
        node.data['similar_item'].result_2 = _sia['res2']
        node.data['similar_item'].result_3 = _sia['res3']
        node.data['similar_item'].result_4 = _sia['res4']
        node.data['similar_item'].result_5 = _sia['res5']

    def _do_roll_up_change_descriptions(self, node: treelib.Node) -> None:
        """Concatenate child change descriptions for the node ID similar item.

        :param node: the similar item treelib.Node() to "roll-up."
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

        for _node_id in node.successors(self._tree.identifier):
            _node = self._tree.get_node(_node_id)

            _change_description_1 += _node.data[
                'similar_item'].change_description_1 + '\n\n'
            _change_description_2 += _node.data[
                'similar_item'].change_description_2 + '\n\n'
            _change_description_3 += _node.data[
                'similar_item'].change_description_3 + '\n\n'
            _change_description_4 += _node.data[
                'similar_item'].change_description_4 + '\n\n'
            _change_description_5 += _node.data[
                'similar_item'].change_description_5 + '\n\n'
            _change_description_6 += _node.data[
                'similar_item'].change_description_6 + '\n\n'
            _change_description_7 += _node.data[
                'similar_item'].change_description_7 + '\n\n'
            _change_description_8 += _node.data[
                'similar_item'].change_description_8 + '\n\n'
            _change_description_9 += _node.data[
                'similar_item'].change_description_9 + '\n\n'
            _change_description_10 += _node.data[
                'similar_item'].change_description_10 + '\n\n'

        node.data['similar_item'].change_description_1 = _change_description_1
        node.data['similar_item'].change_description_2 = _change_description_2
        node.data['similar_item'].change_description_3 = _change_description_3
        node.data['similar_item'].change_description_4 = _change_description_4
        node.data['similar_item'].change_description_5 = _change_description_5
        node.data['similar_item'].change_description_6 = _change_description_6
        node.data['similar_item'].change_description_7 = _change_description_7
        node.data['similar_item'].change_description_8 = _change_description_8
        node.data['similar_item'].change_description_9 = _change_description_9
        node.data[
            'similar_item'].change_description_10 = _change_description_10

        pub.sendMessage(
            'succeed_roll_up_change_descriptions',
            tree=self._tree,
        )

    def _on_get_hardware_attributes(self, tree) -> None:
        """Set hazard rate attributes when a hardware item is selected.

        :param attributes: the attributes dict for the selected hardware item.
        :return: None
        :rtype: None
        """
        for _node in tree.all_nodes()[1:]:
            _hardware = _node.data['hardware']
            _reliability = _node.data['reliability']
            self._dic_hardware_hrs[
                _hardware.hardware_id] = _reliability.hazard_rate_active
