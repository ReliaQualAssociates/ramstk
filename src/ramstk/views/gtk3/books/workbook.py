# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.books.workbook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Work Book."""

# Standard Library Imports
from typing import Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3.allocation import AllocationWorkView
from ramstk.views.gtk3.failure_definition import FailureDefinitionWorkView
from ramstk.views.gtk3.fmea import FMEAWorkView
from ramstk.views.gtk3.function import FunctionWorkView
from ramstk.views.gtk3.hardware import (
    HardwareAssessmentInputView,
    HardwareAssessmentResultsView,
    HardwareGeneralDataView,
)
from ramstk.views.gtk3.hazard_analysis import HazardsWorkView
from ramstk.views.gtk3.pof import PoFWorkView
from ramstk.views.gtk3.program_status import ProgramStatusWorkView
from ramstk.views.gtk3.requirement import (
    RequirementAnalysisView,
    RequirementGeneralDataView,
)
from ramstk.views.gtk3.revision import RevisionWorkView
from ramstk.views.gtk3.similar_item import SimilarItemWorkView
from ramstk.views.gtk3.stakeholder import StakeholderWorkView
from ramstk.views.gtk3.usage_profile import UsageProfileWorkView
from ramstk.views.gtk3.validation import ValidationGeneralDataView
from ramstk.views.gtk3.widgets import RAMSTKBaseBook, RAMSTKBaseView


class RAMSTKWorkBook(RAMSTKBaseBook):
    """The Work Book for the pyGObject (GTK3) interface."""

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
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
            "revision": [
                RevisionWorkView(configuration, logger),
                UsageProfileWorkView(configuration, logger),
            ],
            "function": [
                FunctionWorkView(configuration, logger),
                HazardsWorkView(configuration, logger),
                FailureDefinitionWorkView(configuration, logger),
            ],
            "requirement": [
                RequirementGeneralDataView(configuration, logger),
                RequirementAnalysisView(configuration, logger),
                StakeholderWorkView(configuration, logger),
            ],
            "hardware": [
                HardwareGeneralDataView(configuration, logger),
                AllocationWorkView(configuration, logger),
                SimilarItemWorkView(configuration, logger),
                HardwareAssessmentInputView(configuration, logger),
                HardwareAssessmentResultsView(configuration, logger),
                FMEAWorkView(configuration, logger),
                PoFWorkView(configuration, logger),
            ],
            "validation": [
                ValidationGeneralDataView(configuration, logger),
                ProgramStatusWorkView(configuration, logger),
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._set_properties("workbook")

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_change, "mvwSwitchedPage")

    def _on_module_change(self, module: str = "") -> None:
        """Load Work Views for the RAMSTK module selected in the Module Book.

        :return: None
        :rtype: None
        """
        for _page in self.get_children():
            self.remove(_page)

        try:
            for _workspace in self.dic_work_views[module]:
                self.insert_page(_workspace, _workspace.hbx_tab_label, -1)
        except KeyError:
            pass
