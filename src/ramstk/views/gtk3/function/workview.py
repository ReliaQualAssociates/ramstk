# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Function Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKEntry, RAMSTKPanel,
    RAMSTKTextView, RAMSTKWorkView
)

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS


class GeneralDataPanel(RAMSTKPanel):
    """The panel to display general data about the selected Function."""
    def __init__(self) -> None:
        """Initialize an instance of the Function General Data panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Function Code:"),
            _("Function Description:"),
            _("Remarks:"),
            '',
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("General Information")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.chkSafetyCritical: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Function is safety critical."))
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        self._dic_attribute_updater = {
            'function_code': [self.txtCode.do_update, 'changed', 0],
            'name': [self.txtName.do_update, 'changed', 5],
            'remarks': [self.txtRemarks.do_update, 'changed', 15],
            'safety_critical':
            [self.chkSafetyCritical.do_update, 'toggled', 17]
        }

        self._lst_widgets = [
            self.txtCode,
            self.txtName,
            self.txtRemarks,
            self.chkSafetyCritical,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_function')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_function')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        self.txtCode.do_update('', signal='changed')
        self.txtName.do_update('', signal='changed')
        self.txtRemarks.do_update('', signal='changed')
        self.chkSafetyCritical.do_update(False, signal='toggled')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Function General Data page widgets.

        :param attributes: the Function attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['function_id']

        self.txtCode.do_update(str(attributes['function_code']),
                               signal='changed')
        self.txtName.do_update(str(attributes['name']), signal='changed')
        self.txtRemarks.do_update(str(attributes['remarks']), signal='changed')
        self.chkSafetyCritical.do_update(int(attributes['safety_critical']),
                                         signal='toggled')

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        self.txtCode.dic_handler_id['changed'] = (self.txtCode.connect(
            'changed',
            super().on_changed_entry, 0, 'wvw_editing_function'))
        self.txtName.dic_handler_id['changed'] = (self.txtName.connect(
            'changed',
            super().on_changed_entry, 1, 'wvw_editing_function'))
        _buffer: Gtk.TextBuffer = self.txtRemarks.do_get_buffer()
        self.txtRemarks.dic_handler_id['changed'] = (_buffer.connect(
            'changed',
            super().on_changed_textview, 2, 'wvw_editing_function',
            self.txtRemarks))
        self.chkSafetyCritical.dic_handler_id['toggled'] = (
            self.chkSafetyCritical.connect('toggled',
                                           super().on_toggled, 3,
                                           'wvw_editing_function'))

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

        # ----- BUTTONS
        self.chkSafetyCritical.do_set_properties(
            tooltip=_("Indicates whether or not the selected function is "
                      "safety critical."))

        # ----- ENTRIES
        self.txtCode.do_set_properties(
            width=125, tooltip=_("A unique code for the selected function."))
        self.txtName.do_set_properties(
            width=800, tooltip=_("The name of the selected function."))
        self.txtRemarks.do_set_properties(
            height=100,
            width=800,
            tooltip=_("Enter any remarks associated with the "
                      "selected function."))


class GeneralData(RAMSTKWorkView):
    """Display general Function attribute data in the RAMSTK Work Book.

    The Function Work View displays all the general data attributes for the
    selected Function. The attributes of a Function General Data Work View are:

    :cvar str _module: the name of the module.
    :cvar str _tablabel: the text to display on the tab's label.
    :cvar str _tabtooltip: the text to display as the tab's tooltip.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'function'
    _tablabel = _("General\nData")
    _tabtooltip = _("Displays general information for the "
                    "selected Function")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Function Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_mnu_labels = [
            _("Save Selected Function"),
            _("Save All Functions"),
        ]
        self._lst_tooltips = [
            _("Save changes to the currently selected function."),
            _("Save changes to all functions."),
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralData: RAMSTKPanel = GeneralDataPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_function')

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the stakeholder input's record ID.

        :param attributes: the attributes dict for the selected stakeholder
            input.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['function_id']
        self._parent_id = attributes['parent_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Function General Data tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        self.pack_end(self._pnlGeneralData, True, True, 0)
        self.show_all()
