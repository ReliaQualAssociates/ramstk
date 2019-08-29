# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.books.listbook.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 List Book Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.revision import lvwFailureDefinition, lvwUsageProfile
from ramstk.views.gtk3.widgets.basebook import RAMSTKBook


class RAMSTKListBook(RAMSTKBook):
    """
    This is the List Book class for the GTK3 multiple window interface.

    The List Book provides the container for any List Views and Matrix Views
    associated with the RAMSTK module selected in the RAMSTK Module View.
    Attributes of the List Book are:

    :ivar dict dic_list_view: dictionary containing the List Views and/or
        Matrix Views to load into the RAMSTK List Book for each RAMSTK module.
        Key is the RAMSTK module name; value is a list of Views associated with
        that RAMSTK module.
    """
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize an instance of the RAMSTK List View class.

        :param configuration: the RAMSTKUserConfiguration() class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        RAMSTKBook.__init__(self, configuration)
        self.dic_books['listbook'] = self

        # Initialize private dictionary attributes.
        self._dic_list_views = {
            'revision': [
                lvwUsageProfile(configuration, logger),
                lvwFailureDefinition(configuration, logger)
            ],
            #    'function':
            #    [mtxFunction(configuration, matrix_type='fnctn_hrdwr')],
            #    'requirement': [
            #        lvwStakeholder(configuration),
            #        mtxRequirement(configuration, matrix_type='rqrmnt_hrdwr'),
            #        mtxRequirement(configuration, matrix_type='rqrmnt_vldtn'),
            #    ],
            #    'hardware': [
            #        mtxHardware(configuration, matrix_type='hrdwr_rqrmnt'),
            #        mtxHardware(configuration, matrix_type='hrdwr_vldtn'),
            #    ],
            #    'validation': [
            #        mtxValidation(configuration, matrix_type='vldtn_rqrmnt'),
            #        mtxValidation(configuration, matrix_type='vldtn_hrdwr'),
            #    ],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')
        pub.subscribe(self._on_close, 'succeed_closed_program')

    def __set_properties(self) -> None:
        """
        Set properties of the RAMSTKListBook and widgets.

        :return: None
        :rtype: None
        """
        try:
            _tab_position = self.dic_tab_position[
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_TABPOS['listbook'].lower(
                )]
        except KeyError:
            _tab_position = self._bottom_tab
        self.notebook.set_tab_pos(_tab_position)

        self.set_title(_("RAMSTK Lists and Matrices"))
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        self.resize((self._width / 3) - 10, (2 * self._height / 7))
        self.move((2 * self._width / 3), 0)

    def _on_close(self) -> None:
        """
        Clear the List Views when a RAMSTK Program database is closed.

        :return: None
        :rtype: None
        """
        for _key in self._dic_list_views:
            for _listview in self._dic_list_views[_key]:
                try:
                    _view = _listview.treeview
                except AttributeError:
                    _view = _listview.matrix

                _model = _view.get_model()
                _columns = _view.get_columns()
                for _column in _columns:
                    _view.remove_column(_column)

                _model.clear()

    def _on_module_change(self, module: str = '') -> None:
        """
        Load the List Views for the RAMSTK module selected in the Module Book.

        :return: None
        :rtype: None
        """
        RAMSTKBook.on_module_change(self)

        for _list in self._dic_list_views[module]:
            self.notebook.insert_page(_list, _list.hbx_tab_label, -1)
