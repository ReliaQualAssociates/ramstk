# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Function Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKEntry, RAMSTKLabel,
    RAMSTKTextView, RAMSTKWorkView
)


class GeneralData(RAMSTKWorkView):
    """
    Display general Function attribute data in the RAMSTK Work Book.

    The Function Work View displays all the general data attributes for the
    selected Function. The attributes of a Function General Data Work View are:

    :cvar list _lst_labels: the list of label text.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtCode `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     1    | txtName `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     2    | txtRemarks `changed`                      |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [_("Function Code:"), _("Function Name:"), _("Remarks:")]

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Function Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        RAMSTKWorkView.__init__(self, configuration, logger, module='function')
        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id: int = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkSafetyCritical = RAMSTKCheckButton(
            label=_("Function is safety critical."))
        self.txtCode = RAMSTKEntry()
        self.txtName = RAMSTKEntry()
        self.txtRemarks = RAMSTKTextView(Gtk.TextBuffer())

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_function')
        pub.subscribe(self._on_edit, 'mvw_editing_function')

    def __make_ui(self) -> None:
        """
        Create the Function Work View general data page.

        :return: None
        :rtype: None
        """
        (_x_pos, _y_pos, _fixed) = RAMSTKWorkView.make_ui(self,
                                                          icons=[],
                                                          tooltips=[],
                                                          callbacks=[])

        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[2])
        _fixed.put(self.chkSafetyCritical, 5, _y_pos[2] + 110)

        _label = RAMSTKLabel(_("General\nData"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays general information for the selected Function"))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.txtName.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, None, 1))
        self._lst_handler_id.append(
            self.txtCode.connect('focus-out-event', self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.chkSafetyCritical.connect('toggled', self._on_toggled, 3))

    def __set_properties(self) -> None:
        """
        Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
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

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtName.handler_block(self._lst_handler_id[0])
        self.txtName.set_text('')
        self.txtName.handler_unblock(self._lst_handler_id[0])
        _buffer = self.txtRemarks.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[1])
        _buffer.set_text('')
        _buffer.handler_block(self._lst_handler_id[1])
        self.txtCode.handler_block(self._lst_handler_id[2])
        self.txtCode.set_text('')
        self.txtCode.handler_unblock(self._lst_handler_id[2])
        self.chkSafetyCritical.handler_block(self._lst_handler_id[3])
        self.chkSafetyCritical.do_update(False, self._lst_handler_id[3])
        self.chkSafetyCritical.handler_unblock(self._lst_handler_id[3])

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Function General Data page.

        :param dict attributes: the Function attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._function_id = attributes['function_id']

        RAMSTKWorkView.on_select(
            self,
            title=_("Analyzing Function {0:s} - {1:s}").format(
                str(attributes['function_code']), str(attributes['name'])))

        self.txtName.do_update(str(attributes['name']),
                               self._lst_handler_id[0])
        self.txtRemarks.do_update(str(attributes['remarks']),
                                  self._lst_handler_id[1])
        self.txtCode.do_update(str(attributes['function_code']),
                               self._lst_handler_id[2])
        self.chkSafetyCritical.do_update(int(attributes['safety_critical']),
                                         self._lst_handler_id[3])

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_function', node_id=self._function_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_functions')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_edit(self, node_id: List, package: Dict) -> None:
        """
        Update the Function Work View Gtk.Widgets().

        This method updates the Function Work View Gtk.Widgets() with changes
        to the Function data model attributes.  This method is called whenever
        an attribute is edited in a different RAMSTK View.

        :param list node_id: a list of the ID's of the record in the RAMSTK
            Program database table whose attributes are to be set.  The list is:

                0 - Function ID
                1 - Failure Definition ID
                2 - Usage ID

        :param dict package: the key:value for the attribute being updated.
        :return: None
        :rtype: None
        """
        _module_id = node_id[0]
        [[_key, _value]] = package.items()
        _dic_switch = {
            'name': [self.txtName.do_update, 0],
            'remarks': [self.txtRemarks.do_update, 1],
            'function_code': [self.txtCode.do_update, 2],
            'safety_critical': [self.chkSafetyCritical.do_update, 3]
        }

        _function, _id = _dic_switch.get(_key)
        _function(_value, self._lst_handler_id[_id])

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

        This method sends the 'wvw_editing_function' message.

        :param entry: the Gtk.Entry() that called the method.
        :type entry: :class:`Gtk.Entry`
        :param __event: the Gdk.EventFocus that triggerd the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Function class Gtk.TreeModel()
            associated with the data from the calling Gtk.Entry().
        :return: None
        :rtype: None
        """
        _dic_keys = {0: 'function_code', 1: 'name', 2: 'remarks'}
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        if index in [0, 2]:
            try:
                _new_text: str = str(entry.get_text())
            except ValueError:
                _new_text = ''
        else:
            try:
                _new_text = self.txtRemarks.do_get_text()
            except ValueError:
                _new_text = ''

        pub.sendMessage('wvw_editing_function',
                        node_id=[self._function_id, -1, ''],
                        package={_key: _new_text})

        entry.handler_unblock(self._lst_handler_id[index])

    def _on_toggled(self, togglebutton, index):
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param togglebutton: the RAMSTKToggleButton() that called this method.
        :type: :class:`ramstk.gui.gtk.ramstk.Button.RAMSTKToggleButton`
        :param int index: the index in the signal handler ID list.
        :return: None
        :rtype: None
        """
        _dic_keys = {3: 'safety_critical'}
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        togglebutton.handler_block(self._lst_handler_id[index])

        _new_text = int(togglebutton.get_active())

        pub.sendMessage('wvw_editing_function',
                        node_id=[self._function_id, -1, ''],
                        package={_key: _new_text})

        togglebutton.handler_unblock(self._lst_handler_id[index])
