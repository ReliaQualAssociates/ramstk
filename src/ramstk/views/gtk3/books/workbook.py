# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.books.workbook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Work Book Module."""

# Standard Library Imports
from typing import Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3.allocation import wvwAllocation
from ramstk.views.gtk3.fmea import wvwFMEA
from ramstk.views.gtk3.function import wvwFunctionGD
from ramstk.views.gtk3.hardware import (
    wvwHardwareAI, wvwHardwareAR, wvwHardwareGD
)
from ramstk.views.gtk3.hazard_analysis import wvwHazOps
from ramstk.views.gtk3.pof import wvwPoF
from ramstk.views.gtk3.requirement import (
    wvwRequirementAnalysis, wvwRequirementGD
)
from ramstk.views.gtk3.revision import wvwRevisionGD
from ramstk.views.gtk3.similar_item import wvwSimilarItem
from ramstk.views.gtk3.validation import wvwBurndownCurve, wvwValidationGD
from ramstk.views.gtk3.widgets import RAMSTKBaseBook, RAMSTKBaseView


class RAMSTKWorkBook(RAMSTKBaseBook):
    """The Work Book for the pyGObject (GTK3) interface."""
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize an instance of the Work View class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_work_views: Dict[str, List[RAMSTKBaseView]] = {
            'revision': [wvwRevisionGD(configuration, logger)],
            'function': [
                wvwFunctionGD(configuration, logger),
                wvwHazOps(configuration, logger)
            ],
            'requirement': [
                wvwRequirementGD(configuration, logger),
                wvwRequirementAnalysis(configuration, logger)
            ],
            'hardware': [
                wvwHardwareGD(configuration, logger),
                wvwAllocation(configuration, logger),
                wvwSimilarItem(configuration, logger),
                wvwHardwareAI(configuration, logger),
                wvwHardwareAR(configuration, logger),
                wvwFMEA(configuration, logger),
                wvwPoF(configuration, logger)
            ],
            'validation': [
                wvwValidationGD(configuration, logger),
                wvwBurndownCurve(configuration, logger)
            ]
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._set_properties('workbook')

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def _on_module_change(self, module: str = '') -> None:
        """Load Work Views for the RAMSTK module selected in the Module Book.

        :return: None
        :rtype: None
        """
        for _page in self.get_children():
            self.remove(_page)

        for _workspace in self.dic_work_views[module]:
            self.insert_page(_workspace, _workspace.hbx_tab_label, -1)
