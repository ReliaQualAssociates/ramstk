# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.books.listbook.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 List Book Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3.failure_definition import lvwFailureDefinition
from ramstk.views.gtk3.stakeholder import lvwStakeholders
from ramstk.views.gtk3.usage_profile import lvwUsageProfile
from ramstk.views.gtk3.widgets import RAMSTKBaseBook


class RAMSTKListBook(RAMSTKBaseBook):
    """The List Book class for the GTK3 multiple window interface.

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
        """Initialize an instance of the RAMSTK List View class.

        :param configuration: the RAMSTKUserConfiguration() class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        RAMSTKBaseBook.__init__(self, configuration)

        # Initialize private dictionary attributes.
        self._dic_list_views = {
            'revision': [
                lvwUsageProfile(configuration, logger),
                lvwFailureDefinition(configuration, logger)
            ],
            'function': [],
            'requirement': [
                lvwStakeholders(configuration, logger),
            ],
            'hardware': [],
            'validation': []
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._module: str = ''

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._set_properties('listbook')

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_change, 'mvwSwitchedPage')
        pub.subscribe(self._on_close, 'succeed_closed_program')

    def _on_close(self) -> None:
        """Clear the List Views when a RAMSTK Program database is closed.

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
        """Load List Views for the RAMSTK module selected in the Module Book.

        :param module: the name of the RAMSTK workflow module that has
            been selected in the Module Book.
        :return: None
        :rtype: None
        """
        self._module = module

        for _page in self.get_children():
            self.remove(_page)

        for _list in self._dic_list_views[module]:
            self.insert_page(_list, _list.hbx_tab_label, -1)
