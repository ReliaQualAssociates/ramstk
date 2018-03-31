# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.WorkBook.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKWorkBook Module."""

# Import modules for localization support.
import gettext

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk.rtk import RTKBook

from rtk.gui.gtk.workviews import wvwAllocation
from rtk.gui.gtk.workviews import wvwFMEA
from rtk.gui.gtk.workviews import wvwHazOps
from rtk.gui.gtk.workviews import wvwFunctionGD, wvwFunctionAR
from rtk.gui.gtk.workviews import wvwRevisionGD, wvwRevisionAR
from rtk.gui.gtk.workviews import wvwRequirementGD, wvwRequirementAnalysis
from rtk.gui.gtk.workviews import wvwHardwareGD, wvwHardwareAI, wvwHardwareAR
from rtk.gui.gtk.workviews import wvwValidationGD, wvwBurndownCurve

_ = gettext.gettext


class WorkBook(RTKBook):  # pylint: disable=R0904
    """This is the Work Book for the pyGTK multiple window interface."""

    def __init__(self, controller):
        """
        Initialize an instance of the Work View class.

        :param controller: the RTK master data controller.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKBook.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_work_views = {
            'revision': [wvwRevisionGD(controller),
                         wvwRevisionAR(controller)],
            'function': [
                wvwFunctionGD(controller),
                wvwFMEA(controller),
                wvwFunctionAR(controller)
            ],
            'requirement':
            [wvwRequirementGD(controller),
             wvwRequirementAnalysis(controller)],
            'hardware': [wvwHardwareGD(controller),
                         wvwAllocation(controller),
                         wvwHazOps(controller),
                         wvwHardwareAI(controller),
                         wvwHardwareAR(controller)],
            'validation':
            [wvwValidationGD(controller),
             wvwBurndownCurve(controller)]
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Set the properties for the ModuleBook and it's widgets.
        self.set_title(_(u"RTK Work Book"))
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        # On a 1268x1024 screen, the size will be 845x640.
        _width = self._width - 20
        _height = (5 * self._height / 8) - 40

        self.set_default_size(_width, _height)
        self.move((_width / 1), (_height / 2))

        if controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'left':
            self.notebook.set_tab_pos(self._left_tab)
        elif controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'right':
            self.notebook.set_tab_pos(self._right_tab)
        elif controller.RTK_CONFIGURATION.RTK_TABPOS['workbook'] == 'top':
            self.notebook.set_tab_pos(self._top_tab)
        else:
            self.notebook.set_tab_pos(self._bottom_tab)

        self._on_module_change(module='revision')

        self.add(self.notebook)
        self.show_all()

        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def _on_module_change(self, module=''):
        """
        Load the Work Views for the RTK module selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        RTKBook._on_module_change(self)

        for _workspace in self.dic_work_views[module]:
            self.notebook.insert_page(_workspace, _workspace.hbx_tab_label, -1)

        return _return
