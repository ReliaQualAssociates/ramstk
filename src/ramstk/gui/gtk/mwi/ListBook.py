# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.mwi.ListBook.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK List Book Module."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk import RAMSTKBook
from ramstk.gui.gtk.listviews import (lvwUsageProfile, lvwFailureDefinition,
                                   lvwStakeholder)
from ramstk.gui.gtk.matrixviews import (FunctionHardware, RequirementHardware,
                                     RequirementValidation,
                                     HardwareRequirement, HardwareValidation,
                                     ValidationRequirement, ValidationHardware)
from ramstk.gui.gtk.ramstk.Widget import _, gtk


class ListBook(RAMSTKBook):
    """
    This is the List Book class for the pyGTK multiple window interface.

    The List Book provides the container for any List Views and Matrix Views
    associated with the RAMSTK module selected in the RAMSTK Module View.
    Attributes of the List Book are:

    :ivar dict dic_list_view: dictionary containing the List Views and/or
                              Matrix Views to load into the RAMSTK List Book
                              for each RAMSTK module.  Key is the RAMSTK module
                              name; value is a list of Views associated with
                              that RAMSTK module.
    """

    def __init__(self, controller):
        """
        Initialize an instance of the RAMSTK List View class.

        :param controller: the RAMSTK master data controller.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKBook.__init__(self, controller)

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
                RequirementValidation(controller, matrix_type='rqrmnt_vldtn')
            ],
            'hardware': [
                HardwareRequirement(controller, matrix_type='hrdwr_rqrmnt'),
                HardwareValidation(controller, matrix_type='hrdwr_vldtn')
            ],
            'validation': [
                ValidationRequirement(controller, matrix_type='vldtn_rqrmnt'),
                ValidationHardware(controller, matrix_type='vldtn_hrdwr')
            ]
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Set the properties for the ListBook and it's widgets.
        self.set_title(_(u"RAMSTK Lists and Matrices"))
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        self.set_default_size((self._width / 3) - 10, (2 * self._height / 7))
        self.move((2 * self._width / 3), 0)

        if self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'listbook'].lower() == 'left':
            self.notebook.set_tab_pos(self._left_tab)
        elif self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'listbook'].lower() == 'right':
            self.notebook.set_tab_pos(self._right_tab)
        elif self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_TABPOS[
                'listbook'].lower() == 'top':
            self.notebook.set_tab_pos(self._top_tab)
        else:
            self.notebook.set_tab_pos(self._bottom_tab)

        self.connect('window_state_event', self._on_window_state_event)

        self.add(self.notebook)

        self.show_all()

        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')
        pub.subscribe(self._on_close, 'closedProgram')

    def _on_close(self):
        """
        Update the Modules Views when a RAMSTK Program database is closed.

        :return: None
        :rtype: None
        """
        for _key in self.dic_list_view:
            for _listview in self.dic_list_view[_key]:
                try:
                    _view = _listview.treeview
                except AttributeError:
                    _view = _listview.matrix

                _model = _view.get_model()
                _columns = _view.get_columns()
                for _column in _columns:
                    _view.remove_column(_column)

                _model.clear()

        return None

    def _on_module_change(self, module=''):
        """
        Load the List Views for the RAMSTK module selected in the Module Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        RAMSTKBook._on_module_change(self)

        for _list in self.dic_list_view[module]:
            self.notebook.insert_page(_list, _list.hbx_tab_label, -1)

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
