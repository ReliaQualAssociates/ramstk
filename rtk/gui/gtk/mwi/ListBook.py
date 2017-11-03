# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.ListBook.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
PyGTK Multi-Window Interface List Book
===============================================================================
"""

# Import modules for localization support.
import gettext

from pubsub import pub                              # pylint: disable=E0401

# Import other RTK modules.
# pylint: disable=E0401
from gui.gtk.rtk import RTKBook
from gui.gtk.listviews import lvwUsageProfile, lvwFailureDefinition
from gui.gtk.matrixviews import FunctionHardware

_ = gettext.gettext


class ListBook(RTKBook):                 # pylint: disable=R0904
    """
    This is the List View class for the pyGTK multiple window interface.
    """

    def __init__(self, controller):
        """
        Method to initialize an instance of the RTK List View class.

        :param controller: the RTK master data controller.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKBook.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_list_view = {'revision':
                              [lvwUsageProfile(controller),
                               lvwFailureDefinition(controller)],
                              'function':
                              [FunctionHardware(controller)]}

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Set the properties for the ListBook and it's widgets.
        self.set_title(_(u"RTK Matrices & Lists"))
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        self.set_default_size((self._width / 3) - 10, (2 * self._height / 7))
        self.move((2 * self._width / 3), 0)

        if self._mdcRTK.RTK_CONFIGURATION.RTK_TABPOS['listbook'] == 'left':
            self.notebook.set_tab_pos(self._left_tab)
        elif self._mdcRTK.RTK_CONFIGURATION.RTK_TABPOS['listbook'] == 'right':
            self.notebook.set_tab_pos(self._right_tab)
        elif self._mdcRTK.RTK_CONFIGURATION.RTK_TABPOS['listbook'] == 'top':
            self.notebook.set_tab_pos(self._top_tab)
        else:
            self.notebook.set_tab_pos(self._bottom_tab)

        self.add(self.notebook)

        self.show_all()

        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def _on_module_change(self, module=''):
        """
        Method to load the correct List Views for the RTK module that was
        selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        RTKBook._on_module_change(self)

        for _list in self.dic_list_view[module]:
            self.notebook.insert_page(_list, _list.hbx_tab_label, -1)

        return _return
