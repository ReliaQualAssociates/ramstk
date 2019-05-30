# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.mwi.WorkBook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKWorkBook Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk import RAMSTKBook
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews import (wvwAllocation, wvwBurndownCurve,
                                      wvwFunctionGD, wvwHardwareAI,
                                      wvwHardwareAR, wvwHardwareGD, wvwHazOps,
                                      wvwPoF, wvwRequirementAnalysis,
                                      wvwRequirementGD, wvwRevisionGD,
                                      wvwSimilarItem, wvwValidationGD)
from ramstk.gui.gtk.workviews.fmea import wvwDFMECA, wvwFFMEA


class WorkBook(RAMSTKBook):
    """This is the Work Book for the pyGTK multiple window interface."""

    def __init__(self, configuration):
        """
        Initialize an instance of the Work View class.

        :param controller: the RAMSTK master data controller.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKBook.__init__(self, configuration)
        self.dic_books['workbook'] = self

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_work_views = {
            'revision': [
                wvwRevisionGD(configuration),
            ],
            'function': [
                wvwFunctionGD(configuration),
                wvwFFMEA(configuration),
            ],
            'requirement':
            [
                wvwRequirementGD(configuration),
                wvwRequirementAnalysis(configuration),
            ],
            'hardware': [
                wvwHardwareGD(configuration),
                wvwAllocation(configuration),
                wvwHazOps(configuration),
                wvwSimilarItem(configuration),
                wvwHardwareAI(configuration),
                wvwHardwareAR(configuration),
                wvwDFMECA(configuration),
                wvwPoF(configuration),
            ],
            'validation': [
                wvwValidationGD(configuration),
                wvwBurndownCurve(configuration),
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        #?self._on_module_change(module='revision')

        self.add(self.notebook)
        self.show_all()

    def __set_properties(self):
        """
        Set properties of the RAMSTKListBook and widgets.

        :return: None
        :rtype: None
        """
        try:
            _tab_position = self.dic_tab_position[
                self.RAMSTK_CONFIGURATION.RAMSTK_TABPOS['workbook'].lower()
            ]
        except KeyError:
            _tab_position = self._bottom_tab
        self.notebook.set_tab_pos(_tab_position)

        self.set_title(_("RAMSTK Work Book"))
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        _width = self._width - 20
        _height = (5 * self._height / 8) - 40

        self.resize(_width, _height)
        self.move(1, (_height / 2) + 100)

    def _on_module_change(self, module=''):
        """
        Load the Work Views for the RAMSTK module selected in the Module Book.

        :return: None
        :rtype: None
        """
        RAMSTKBook.on_module_change(self)

        for _workspace in self.dic_work_views[module]:
            self.notebook.insert_page(_workspace, _workspace.hbx_tab_label, -1)
