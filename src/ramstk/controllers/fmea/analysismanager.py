# -*- coding: utf-8 -*-
#
#       ramstk.controllers.fmea.analysismanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Controller Package analysis manager."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import criticality
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """Contain the attributes and methods of the FMEA analysis manager."""

    def __init__(
        self, configuration: RAMSTKUserConfiguration, **kwargs: Dict[str, Any]
    ) -> None:
        """Initialize an instance of the FMEA analysis manager.

        :param configuration: the user configuration instance associated
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
        pub.subscribe(super().on_get_tree, "succeed_retrieve_fmea")
        pub.subscribe(super().on_get_tree, "succeed_get_fmea_tree")

        pub.subscribe(self._do_calculate_rpn, "request_calculate_rpn")

    def _do_calculate_rpn(self, method: str = "mechanism") -> None:
        """Calculate the risk priority number (RPN) of a hardware item's modes.

            .. note:: the severity (S) value will always be associated with a
                failure mode.

            .. note:: the occurrence (O) and detection (D) values may be
                associated with a failure mechanism or a failure cause.  Do not
                mix and match these.  Either both are associated with a
                mechanism or both are associated with a cause.  Regardless of
                the method, the mechanism or cause must be an immediate child
                of the failure mode.  Typically, hardware FMEA use mechanisms
                and FMEAal FMEA use causes.

        :param method: the method to use when calculating the RPN.  Options
            are mechanism (default) and cause.  Whichever is selected will
            determine where the O and D values come from.
        :return: None
        :rtype: None
        """
        _sod = {"rpn_severity": 10, "rpn_occurrence": 10, "rpn_detection": 10}

        for _mode in self._tree.children(0):
            _sod["rpn_severity"] = _mode.data["mode"].rpn_severity
            self.__do_calculate_rpn(_mode, _sod, method)

            _sod["rpn_severity"] = _mode.data["mode"].rpn_severity_new
            self.__do_calculate_rpn(_mode, _sod, method)

        pub.sendMessage(
            "succeed_calculate_rpn",
            tree=self._tree,
        )

    def __do_calculate_rpn(
        self, mode: treelib.Node, sod: Dict[str, int], method: str
    ) -> None:
        """Iterate through a failure mode mechanisms/causes to calculate RPNs.

        :param mode: the treelib Node() that contains the failure mode data for
            calculating the RPN.
        :param sod: a dict containing the severity, occurrence,
            and detection values.
        :param method: the method used to calculate the RPN.
        :return: None
        :rtype: None
        """
        for _child in self._tree.children(str(mode.data["mode"].mode_id)):
            sod["rpn_occurrence"] = _child.data[method].rpn_occurrence
            sod["rpn_detection"] = _child.data[method].rpn_detection
            _child.data[method].rpn = criticality.calculate_rpn(sod)

            sod["rpn_occurrence"] = _child.data[method].rpn_occurrence_new
            sod["rpn_detection"] = _child.data[method].rpn_detection_new
            _child.data[method].rpn_new = criticality.calculate_rpn(sod)

            pub.sendMessage(
                "request_set_fmea_attributes",
                node_id=[_child.identifier, -1],
                package={"rpn": _child.data[method].rpn},
            )
            pub.sendMessage(
                "request_set_fmea_attributes",
                node_id=[_child.identifier, -1],
                package={"rpn_new": _child.data[method].rpn_new},
            )
