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
from ramstk.gui.gtk.matrixviews import (
    FunctionHardware, RequirementHardware, RequirementValidation,
    HardwareRequirement, HardwareValidation, ValidationRequirement,
    ValidationHardware)
from ramstk.gui.gtk.ramstk.Widget import _


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

    def __init__(self, configuration):
        """
        Initialize an instance of the RAMSTK List View class.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKBook.__init__(self, configuration)
        self.dic_books['listbook'] = self

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.dic_list_view = {
            'revision':
            [lvwUsageProfile(configuration),
             lvwFailureDefinition(configuration)],
            'function':
            [FunctionHardware(configuration, matrix_type='fnctn_hrdwr')],
            'requirement': [
                lvwStakeholder(configuration),
                RequirementHardware(configuration, matrix_type='rqrmnt_hrdwr'),
                RequirementValidation(configuration, matrix_type='rqrmnt_vldtn')
            ],
            'hardware': [
                HardwareRequirement(configuration, matrix_type='hrdwr_rqrmnt'),
                HardwareValidation(configuration, matrix_type='hrdwr_vldtn')
            ],
            'validation': [
                ValidationRequirement(configuration, matrix_type='vldtn_rqrmnt'),
                ValidationHardware(configuration, matrix_type='vldtn_hrdwr')
            ]
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')
        pub.subscribe(self._on_close, 'closed_program')

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
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
                self.RAMSTK_CONFIGURATION.RAMSTK_TABPOS['listbook'].lower()]
        except KeyError:
            _tab_position = self._bottom_tab
        self.notebook.set_tab_pos(_tab_position)

        self.set_title(_("RAMSTK Lists and Matrices"))
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        self.resize((self._width / 3) - 10, (2 * self._height / 7))
        self.move((2 * self._width / 3), 0)

    def _on_close(self):
        """
        Clear the List Views when a RAMSTK Program database is closed.

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

    def _on_module_change(self, module=''):
        """
        Load the List Views for the RAMSTK module selected in the Module Book.

        :return: None
        :rtype: None
        """
        RAMSTKBook.on_module_change(self)

        for _list in self.dic_list_view[module]:
            self.notebook.insert_page(_list, _list.hbx_tab_label, -1)
