# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.workviews.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Revision Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
from pubsub import pub  # type: ignore

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKEntry, RAMSTKPanel, RAMSTKTextView, RAMSTKWorkView
)


class GeneralDataPanel(RAMSTKPanel):
    """The panel to display general data about the selected Revision."""

    def __init__(self) -> None:
        """Initialize an instance of the Revision General Data panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['name', 'string'],
            1: ['remarks', 'string'],
            2: ['revision_code', 'string'],
        }

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Revision Code:"),
            _("Revision Name:"),
            _("Remarks:"),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("General Information")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        self._dic_attribute_updater: Dict[str, Union[object, str]] = {
            'name': [self.txtName.do_update, 'changed'],
            'remarks': [self.txtRemarks.do_update, 'focus-out-event'],
            'revision_code': [self.txtCode.do_update, 'changed'],
        }

        self._lst_widgets: List[object] = [
            self.txtCode,
            self.txtName,
            self.txtRemarks,
        ]

        # Make a fixed type panel.
        self.do_make_panel_fixed()

        self.__do_set_properties()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_revision')

        pub.subscribe(self._do_clear_panel, 'closed_program')
        pub.subscribe(self._do_load_panel, 'selected_revision')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the Revision General Data page widgets.

        :return: None
        :rtype: None
        """
        self.txtName.do_update('', signal='changed')
        self.txtRemarks.do_update('', signal='changed')
        self.txtCode.do_update('', signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Revision General Data page widgets.

        :param dict attributes: the Revision attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['revision_id']

        self.txtName.do_update(str(attributes['name']), signal='changed')
        self.txtRemarks.do_update(str(attributes['remarks']), signal='changed')
        self.txtCode.do_update(str(attributes['revision_code']),
                               signal='changed')

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        self.txtName.dic_handler_id['changed'] = self.txtName.connect(
            'changed', self.on_changed_text, 0, 'wvw_editing_revision')
        self.txtRemarks.dic_handler_id['changed'] = self.txtRemarks.connect(
            'focus-out-event', self.on_focus_out, 1, 'wvw_editing_revision')
        self.txtCode.dic_handler_id['changed'] = self.txtCode.connect(
            'changed', self.on_changed_text, 2, 'wvw_editing_revision')

    def __do_set_properties(self) -> None:
        """Set the properties of the general data panel widgets.

        :return: None
        :rtype: None
        """
        # ----- ENTRIES
        self.txtCode.do_set_properties(
            width=125, tooltip=_("A unique code for the selected revision."))
        self.txtName.do_set_properties(
            width=800, tooltip=_("The name of the selected revision."))
        self.txtRemarks.do_set_properties(
            height=100,
            width=800,
            tooltip=_(
                "Enter any remarks associated with the selected revision."))


class GeneralData(RAMSTKWorkView):
    """Display general Revision attribute data in the RAMSTK Work Book.

    The Revision Work View displays all the general data attributes for the
    selected Revision. The attributes of a Revision General Data Work View are:

    :cvar dict _dic_keys: the index:database table field dictionary.
    :cvar str _module: the name of the module.

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
    _module: str = 'revision'
    _tablabel = _("General\nData")
    _tabtooltip = _("Displays general information for the selected Revision")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Revision Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks: List[object] = [
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons: List[str] = [
            'save',
            'save-all',
        ]
        self._lst_tooltips: List[str] = [
            _("Save changes to the currently "
              "selected Revision."),
            _("Save changes to all Revisions."),
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralData: RAMSTKPanel = GeneralDataPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_revision')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_revision')

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Request to save changes to the currently selected Revision.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_revision', node_id=self._revision_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Request to save change sto all Revisions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_revisions')

    def __make_ui(self) -> None:
        """Build the user interface for the Revision General Data tab.

        :return: None
        :rtype: None
        """
        super().make_tab_label(tablabel=self._tablabel,
                               tooltip=self._tabtooltip)
        super().make_toolbuttons(icons=self._lst_icons,
                                 tooltips=self._lst_tooltips,
                                 callbacks=self._lst_callbacks)

        self.pack_end(self._pnlGeneralData, True, True, 0)
        self.show_all()
