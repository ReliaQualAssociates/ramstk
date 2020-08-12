# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.workviews.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Revision Work View."""

# Standard Library Imports
from typing import Any, Dict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (RAMSTKEntry, RAMSTKFrame, RAMSTKLabel,
                                       RAMSTKTextView, RAMSTKWorkView)


class GeneralData(RAMSTKWorkView):
    """
    Display general Revision attribute data in the RAMSTK Work Book.

    The Revision Work View displays all the general data attributes for the
    selected Revision. The attributes of a Revision General Data Work View are:

    :cvar dict _dic_keys: the index:database table field dictionary.
    :cvar list _lst_labels: the list of label text.
    """
    # Define private dict class attributes.
    _dic_keys = {
        0: ['name', 'string'],
        1: ['remarks', 'string'],
        2: ['revision_code', 'string']
    }

    # Define private list class attributes.
    _lst_labels = [_("Revision Code:"), _("Revision Name:"), _("Remarks:")]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'revision') -> None:
        """
        Initialize the Revision Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        self._dic_switch: Dict[str, Union[object, str]] = {
            'name': [self.txtName.do_update, 'changed'],
            'remarks': [self.txtRemarks.do_update, 'changed'],
            'revision_code': [self.txtCode.do_update, 'changed']
        }

        self._lst_widgets = [self.txtCode, self.txtName, self.txtRemarks]

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'selected_revision')
        pub.subscribe(self.on_edit, 'mvw_editing_revision')

    def __make_ui(self) -> None:
        """
        Create the Revision Work View general data page.

        :return: None
        :rtype: None
        """
        # This page has the following layout:
        #
        # +-----+---------------------------------------+
        # |  B  |                                       |
        # |  U  |                                       |
        # |  T  |                                       |
        # |  T  |                WIDGETS                |
        # |  O  |                                       |
        # |  N  |                                       |
        # |  S  |                                       |
        # +-----+---------------------------------------+
        #                           buttons ----+--> self
        #                                       |
        #      RAMSTKFixed ------>RAMSTKFrame --+
        # Make the buttons.
        super().make_toolbuttons(icons=[], tooltips=[], callbacks=[])

        # Layout the widgets.
        _fixed = super().make_ui()

        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("General Information"))
        _frame.add(_fixed)
        self.pack_end(_frame, True, True, 0)

        _label = RAMSTKLabel(_("General\nData"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays general information for the selected Revision"))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        self.txtName.dic_handler_id['changed'] = self.txtName.connect(
            'focus-out-event', self._on_focus_out, 0)
        self.txtRemarks.dic_handler_id[
            'changed'] = self.txtRemarks.do_get_buffer().connect(
                'changed', self._on_focus_out, None, 1)
        self.txtCode.dic_handler_id['changed'] = self.txtCode.connect(
            'focus-out-event', self._on_focus_out, 2)

    def __set_properties(self) -> None:
        """
        Set the properties of the General Data Work View and widgets.

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
            tooltip=_("Enter any remarks associated with the "
                      "selected revision."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtName.do_update('', signal='changed')
        self.txtRemarks.do_update('', signal='changed')
        self.txtCode.do_update('', signal='changed')

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Revision General Data page.

        :param dict attributes: the Revision attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        self.txtName.do_update(str(attributes['name']), signal='changed')
        self.txtRemarks.do_update(str(attributes['remarks']), signal='changed')
        self.txtCode.do_update(str(attributes['revision_code']),
                               signal='changed')

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Revision.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_revision', node_id=self._revision_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Revisions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_revisions')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    # pylint: disable=unused-argument
    def _on_focus_out(self, entry: Gtk.Entry, __event: Gdk.EventFocus,
                      index: int) -> None:
        """
        Handle changes made in RAMSTKEntry() and RAMSTKTextView() widgets.

        This method is called by:

            * RAMSTKEntry() 'focus-out-event' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvw_editing_revision' message.

        :param entry: the Gtk.Entry() that called the method.
        :type entry: :class:`Gtk.Entry`
        :param __event: the Gdk.EventFocus that triggerd the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Revision class Gtk.TreeModel()
            associated with the data from the calling Gtk.Entry().
        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_revision')
