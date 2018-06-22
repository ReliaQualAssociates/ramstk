# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.mwi.ListBook.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTK List Book Module."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk.rtk import RTKBook
from rtk.gui.gtk.listviews import lvwUsageProfile, lvwFailureDefinition, \
    lvwStakeholder
from rtk.gui.gtk.matrixviews import FunctionHardware, RequirementHardware, \
    RequirementSoftware, RequirementValidation
from rtk.gui.gtk.rtk.Widget import _, gtk


class ListBook(RTKBook):  # pylint: disable=R0904
    """
    This is the List Book class for the pyGTK multiple window interface.

    The List Book provides the container for any List Views and Matrix Views
    associated with the RTK module selected in the RTK Module View.  Attributes
    of the List Book are:

    :ivar dict dic_list_view: dictionary containing the List Views and/or
                              Matrix Views to load into the RTK List Book for
                              each RTK module.  Key is the RTK module name;
                              value is a list of Views associated with that
                              RTK module.
    """

    def __init__(self, controller):
        """
        Initialize an instance of the RTK List View class.

        :param controller: the RTK master data controller.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKBook.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_list_view = {
            'revision':
            [lvwUsageProfile(controller),
             lvwFailureDefinition(controller)],
            'function':
            [FunctionHardware(controller, matrix_type='fnctn_hrdwr')],
            'requirement': [
                lvwStakeholder(controller),
                RequirementHardware(controller, matrix_type='rqrmnt_hrdwr'),
                RequirementSoftware(controller, matrix_type='rqrmnt_sftwr'),
                RequirementValidation(controller, matrix_type='rqrmnt_vldtn')
            ],
            'validation': [],
            'hardware': []
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Set the properties for the ListBook and it's widgets.
        self.set_title(_(u"RTK Matrices and Lists"))
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

        self.connect('window_state_event', self._on_window_state_event)

        self.add(self.notebook)

        self.show_all()

        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')

    def _on_module_change(self, module=''):
        """
        Load the List Views for the RTK module selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        RTKBook._on_module_change(self)

        for _list in self.dic_list_view[module]:
            self.notebook.insert_page(_list, _list.hbx_tab_label, -1)

        return _return

    def _on_window_state_event(self, window, event):
        """
        Iconify or deiconify all three books together.

        :return: None
        :rtype: None
        """
        if event.new_window_state == gtk.gdk.WINDOW_STATE_ICONIFIED:
            for _window in ['listbook', 'modulebook', 'workbook']:
                self._mdcRTK.dic_books[_window].iconify()
        elif event.new_window_state == 0:
            for _window in ['listbook', 'modulebook', 'workbook']:
                self._mdcRTK.dic_books[_window].deiconify()
        elif event.new_window_state == gtk.gdk.WINDOW_STATE_MAXIMIZED:
            window.maximize()

        return None
