# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.workviews.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Revision Work View."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (RAMSTKEntry, RAMSTKLabel,
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
    _dic_keys = {0: 'name', 1: 'remarks', 2: 'revision_code'}

    # Define private list class attributes.
    _lst_labels = [_("Revision Code:"), _("Revision Name:"), _("Remarks:")]

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Revision Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, 'revision')

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

        self._dic_switch = {
            'name': [self.txtName.do_update, 0],
            'remarks': [self.txtRemarks.do_update, 1],
            'revision_code': [self.txtCode.do_update, 2]
        }

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
        (_x_pos, _y_pos, _fixed) = super().make_ui(icons=[],
                                                   tooltips=[],
                                                   callbacks=[])

        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[2])

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

    def _on_focus_out(
            self,
            entry: Gtk.Entry,
            __event: Gdk.EventFocus,  # pylint: disable=unused-argument
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
        try:
            _key = self._dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(entry.dic_handler_id['changed'])

        try:
            if index in [0, 2]:
                _new_text: str = str(entry.get_text())
            else:
                _new_text = self.txtRemarks.do_get_text()
        except ValueError:
            _new_text = ''

        pub.sendMessage('wvw_editing_revision',
                        node_id=[self._revision_id, -1, ''],
                        package={_key: _new_text})

        entry.handler_unblock(entry.dic_handler_id['changed'])
