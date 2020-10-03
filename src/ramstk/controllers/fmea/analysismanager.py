# -*- coding: utf-8 -*-
#
#       ramstk.controllers.fmea.analysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Controller Package analysis manager."""

# Standard Library Imports
from collections import defaultdict
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import criticality
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """
    Contain the attributes and methods of the FMEA analysis manager.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        """
        Initialize an instance of the FMEA analysis manager.

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
        pub.subscribe(self.on_get_tree, 'succeed_get_fmea_tree')
        pub.subscribe(self._on_get_tree, 'succeed_retrieve_hardware_fmea')
        pub.subscribe(self._do_calculate_criticality,
                      'request_calculate_criticality')
        pub.subscribe(self._do_calculate_rpn, 'request_calculate_rpn')

    def _do_calculate_criticality(self, item_hr: float) -> None:
        """
        Calculate the MIL-STD-1629A, Task 102 criticality of a hardware item.

        :param float item_hr: the hazard rate of the hardware item the
            criticality is being calculated for.
        :return: None
        :rtype: None
        """
        _item_criticality = defaultdict(float)
        for _mode in self._tree.children(0):
            _mode.data['mode'].mode_hazard_rate = (
                criticality.calculate_mode_hazard_rate(
                    item_hr, _mode.data['mode'].mode_ratio))
            _mode.data['mode'].mode_criticality = (
                criticality.calculate_mode_criticality(
                    _mode.data['mode'].mode_hazard_rate,
                    _mode.data['mode'].mode_op_time,
                    _mode.data['mode'].effect_probability))
            _item_criticality[_mode.data['mode'].severity_class] += _mode.data[
                'mode'].mode_criticality

        pub.sendMessage('succeed_calculate_fmea_criticality',
                        item_criticality=_item_criticality)

    def _do_calculate_rpn(self, method: str = 'mechanism') -> None:
        """
        Calculate the risk priority number (RPN) of a hardware item's modes.

            .. note:: the severity (S) value will always be associated with a
                failure mode.

            .. note:: the occurrence (O) and detection (D) values may be
                associated with a failure mechanism or a failure cause.  Do not
                mix and match these.  Either both are associated with a
                mechanism or both are associated with a cause.  Regardless of
                the method, the mechanism or cause must be an immediate child
                of the failure mode.  Typically, hardware FMEA use mechanisms
                and FMEAal FMEA use causes.

        :param str method: the method to use when calculating the RPN.  Options
            are mechanism (default) and cause.  Whichever is selected will
            determine where the O and D values come from.
        :return: None
        :rtype: None
        """
        _sod = {'rpn_severity': 10, 'rpn_occurrence': 10, 'rpn_detection': 10}

        for _mode in self._tree.children(0):
            _sod['rpn_severity'] = _mode.data['mode'].rpn_severity
            self.__do_calculate_rpn(_mode, _sod, method)

            _sod['rpn_severity'] = _mode.data['mode'].rpn_severity_new
            self.__do_calculate_rpn(_mode, _sod, method)

        pub.sendMessage('succeed_calculate_rpn', tree=self._tree)

    def __do_calculate_rpn(self, mode: object, sod: Dict[str, int],
                           method: str) -> None:
        """

        :param mode:
        :param sod:
        :param method:
        :return:
        """
        for _child in self._tree.children(str(mode.data['mode'].mode_id)):
            sod['rpn_occurrence'] = _child.data[method].rpn_occurrence
            sod['rpn_detection'] = _child.data[method].rpn_detection
            _child.data[method].rpn = criticality.calculate_rpn(sod)

            sod['rpn_occurrence'] = _child.data[method].rpn_occurrence_new
            sod['rpn_detection'] = _child.data[method].rpn_detection_new
            _child.data[method].rpn_new = criticality.calculate_rpn(sod)

            pub.sendMessage('request_set_fmea_attributes',
                            node_id=[_child.identifier, -1],
                            package={'rpn': _child.data[method].rpn})
            pub.sendMessage('request_set_fmea_attributes',
                            node_id=[_child.identifier, -1],
                            package={'rpn_new': _child.data[method].rpn_new})

    #// TODO: Update RAMSTKAnalysisManager.on_get_tree dmtree argument to tree.
    #//
    #// The analysis manager should be loaded with the tree as soon as the
    #// data manager retrieves it.  The analysis managers should subscribe to
    #// the work stream module's corresponding succeed_retrieve_* message.
    #// These messages are all sent with a data package named tree,
    #// not dmtree.  The RAMSTKAnalysisManager.on_get_tree() method should be
    #// updated to accept tree as the argument, not dmtree.  Each of the work
    #// stream module analysis managers should be updated to subscribe to the
    #// proper message.
    #//
    #// Remove _on_get_tree() method from FMEA analysis manager when this is
    #// complete.
    def _on_get_tree(self, tree: treelib.Tree) -> None:
        """
        Set the analysis manager's treelib Tree().

        :param tree: the data manager's treelib Tree().
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._tree = tree
