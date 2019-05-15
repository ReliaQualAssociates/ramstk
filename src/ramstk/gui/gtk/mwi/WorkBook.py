# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.mwi.WorkBook.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKWorkBook Module."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk import RAMSTKBook

from ramstk.gui.gtk.workviews import wvwAllocation
from ramstk.gui.gtk.workviews import wvwFFMEA, wvwDFMECA
from ramstk.gui.gtk.workviews import wvwHazOps
from ramstk.gui.gtk.workviews import wvwPoF
from ramstk.gui.gtk.workviews import wvwSimilarItem
from ramstk.gui.gtk.workviews import wvwFunctionGD
from ramstk.gui.gtk.workviews import wvwRevisionGD
from ramstk.gui.gtk.workviews import wvwRequirementGD, wvwRequirementAnalysis
from ramstk.gui.gtk.workviews import wvwHardwareGD, wvwHardwareAI, wvwHardwareAR
from ramstk.gui.gtk.workviews import wvwValidationGD, wvwBurndownCurve
from ramstk.gui.gtk.ramstk.Widget import _, Gdk


class WorkBook(RAMSTKBook):
    """This is the Work Book for the pyGTK multiple window interface."""

    def __init__(self, controller):
        """
        Initialize an instance of the Work View class.

        :param controller: the RAMSTK master data controller.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKBook.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_work_views = {
            'revision': [
                wvwRevisionGD(controller),
            ],
            'function': [
                wvwFunctionGD(controller),
                wvwFFMEA(controller),
            ],
            'requirement':
            [wvwRequirementGD(controller),
             wvwRequirementAnalysis(controller)],
            'hardware': [
                wvwHardwareGD(controller),
                wvwAllocation(controller),
                wvwHazOps(controller),
                wvwSimilarItem(controller),
                wvwHardwareAI(controller),
                wvwHardwareAR(controller),
                wvwDFMECA(controller),
                wvwPoF(controller)
            ],
            'validation':
            [wvwValidationGD(controller),
             wvwBurndownCurve(controller)]
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.set_title(_("RAMSTK Work Book"))
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        # On a 1268x1024 screen, the size will be 845x640.
        _width = self._width - 20
        _height = (5 * self._height / 8) - 40

        self.set_default_size(_width, _height)
        self.move((_width / 1), (_height / 2))

        if self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'workbook'].lower() == 'left':
            self.notebook.set_tab_pos(self._left_tab)
        elif self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'workbook'].lower() == 'right':
            self.notebook.set_tab_pos(self._right_tab)
        elif self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'workbook'].lower() == 'top':
            self.notebook.set_tab_pos(self._top_tab)
        else:
            self.notebook.set_tab_pos(self._bottom_tab)

        self._on_module_change(module='revision')

        self.connect('window_state_event', self._on_window_state_event)

        self.add(self.notebook)
        self.show_all()

        return None

    def _on_module_change(self, module=''):
        """
        Load the Work Views for the RAMSTK module selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        RAMSTKBook._on_module_change(self)
        for _workspace in self.dic_work_views[module]:
            self.notebook.insert_page(_workspace, _workspace.hbx_tab_label, -1)

        return _return

    def _on_window_state_event(self, window, event):
        """
        Iconify or deiconify all three books together.

        :return: None
        :rtype: None
        """
        if event.new_window_state == Gdk.WindowState.ICONIFIED:
            for _window in ['listbook', 'modulebook', 'workbook']:
                self._mdcRAMSTK.dic_books[_window].iconify()
        elif event.new_window_state == 0:
            for _window in ['listbook', 'modulebook', 'workbook']:
                self._mdcRAMSTK.dic_books[_window].deiconify()
        elif event.new_window_state == Gdk.WindowState.MAXIMIZED:
            window.maximize()

        return None
