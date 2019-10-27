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
from ramstk.views.gtk3.function import wvwFunctionGD
from ramstk.views.gtk3.revision import wvwRevisionGD
from ramstk.views.gtk3.widgets import RAMSTKBaseBook


class RAMSTKWorkBook(RAMSTKBaseBook):
    """This is the Work Book for the pyGTK multiple window interface."""

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize an instance of the Work View class.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        RAMSTKBaseBook.__init__(self, configuration)

        # Initialize private dictionary attributes.
        self._dic_work_views: Dict[str, List[object]] = {
            'revision': [
                wvwRevisionGD(configuration, logger),
            ],
            'function': [wvwFunctionGD(configuration, logger)],
            #        wvwFFMEA(configuration),
            #    ],
            #    'requirement':
            #    [
            #        wvwRequirementGD(configuration),
            #        wvwRequirementAnalysis(configuration),
            #    ],
            #    'hardware': [
            #        wvwHardwareGD(configuration),
            #        wvwAllocation(configuration),
            #        wvwHazOps(configuration),
            #        wvwSimilarItem(configuration),
            #        wvwHardwareAI(configuration),
            #        wvwHardwareAR(configuration),
            #        wvwDFMECA(configuration),
            #        wvwPoF(configuration),
            #    ],
            #    'validation': [
            #        wvwValidationGD(configuration),
            #        wvwBurndownCurve(configuration),
            #    ],
        }

        # Initialize private list attributes.
        self._lst_handler_id: List[int] = []

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._set_properties('workbook')

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def _on_module_change(self, module: str = '') -> None:
        """
        Load the Work Views for the RAMSTK module selected in the Module Book.

        :return: None
        :rtype: None
        """
        for _page in range(self.get_n_pages()):
            self.remove_page(_page)

        for _workspace in self._dic_work_views[module]:
            self.insert_page(_workspace, _workspace.hbx_tab_label, -1)
