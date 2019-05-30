# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Function.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Function Work View."""

# Third Party Imports
# Import third party modules.
from pubsub import pub

# RAMSTK Package Imports
# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk import (RAMSTKCheckButton, RAMSTKEntry, RAMSTKFrame,
                                   RAMSTKLabel, RAMSTKScrolledWindow,
                                   RAMSTKTextView, do_make_label_group)
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _

# RAMSTK Local Imports
from .WorkView import RAMSTKWorkView


class GeneralData(RAMSTKWorkView):
    """
    Display Function attribute data in the RAMSTK Work Book.

    The Work View displays all the general data attributes for the selected
    Function. The attributes of a Function General Data Work View are:

    :ivar int _function_id: the ID of the Function currently being displayed.
    :ivar chkSafetyCritical: the
                             :class:`ramstk.gui.gtk.ramstk.RAMSTKCheckButton`
                             to display/edit the Function's safety criticality.
    :ivar txtTotalCost: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the Function cost.
    :ivar txtModeCount: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the number of failure modes the function is
                        susceptible to.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtCode `changed`                         |
    +----------+-------------------------------------------+
    |     1    | txtName `changed`                         |
    +----------+-------------------------------------------+
    |     2    | txtRemarks `changed`                      |
    +----------+-------------------------------------------+
    |     3    | chkSafetyCritical `toggled`               |
    +----------+-------------------------------------------+
    """

    _lst_labels = [
        _("Function Code:"),
        _("Function Description:"),
        _("Remarks:")
    ]

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Function package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKWorkView.__init__(self, configuration, module='Function')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._function_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # General data page widgets.

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
        pub.subscribe(self._on_edit, 'mvw_editing_function')
        pub.subscribe(self._do_load_page, 'selected_function')

    def __make_ui(self):
        """
        Make the Function class Gtk.Notebook() general data page.

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(
            RAMSTKWorkView._make_buttonbox(
                self, icons=[], tooltips=[], callbacks=[]))
        self.pack_start(_scrolledwindow, False, False, 0)

        _fixed = Gtk.Fixed()

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame(label=_("General Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = do_make_label_group(self._lst_labels, _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtRemarks, _x_pos, _y_pos[2])
        _fixed.put(self.chkSafetyCritical, 5, _y_pos[2] + 110)

        self.pack_start(_frame, True, True, 0)

        # Create the label for the Gtk.Notebook() tab.
        _label = RAMSTKLabel(
            _("General\nData"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays general information for the selected "
                      "function."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.txtCode.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtName.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.chkSafetyCritical.connect('toggled', self._on_toggled, 3))

    def __set_properties(self):
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
            tooltip=_("Any remarks associated with the selected function."))

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtCode.do_update('', self._lst_handler_id[0])
        self.txtName.do_update('', self._lst_handler_id[1])
        self.txtRemarks.do_update('', self._lst_handler_id[2])
        self.chkSafetyCritical.do_update(False, self._lst_handler_id[3])

    def _do_load_page(self, attributes):
        """
        Load the Function General Data page.

        :param tuple attributes: a dict of attribute key:value pairs for
                                 the selected Function.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._function_id = attributes['function_id']

        RAMSTKWorkView.on_select(
            self,
            title=_("Analyzing Function {0:s} - {1:s}").format(
                str(attributes['function_code']), str(attributes['name'])))

        self.txtCode.do_update(
            str(attributes['function_code']), self._lst_handler_id[0])
        self.txtName.do_update(
            str(attributes['name']), self._lst_handler_id[1])
        self.txtRemarks.do_update(
            str(attributes['remarks']), self._lst_handler_id[2])
        self.chkSafetyCritical.do_update(
            int(attributes['safety_critical']), self._lst_handler_id[3])

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Function.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_function', node_id=self._function_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
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

    def _on_edit(self, module_id, key, value):  # pylint: disable=unused-argument
        """
        Update the Function Work View Gtk.Widgets().

        This method updates the function Work View Gtk.Widgets() with changes
        to the Function data model attributes.  This method is called whenever
        an attribute is edited in a different RAMSTK View.

        :param int module_id: the ID of the Function being edited.  This
                              parameter is required to allow the PyPubSub
                              signals to call this method and the
                              request_set_attributes() method in the
                              RAMSTKDataController.
        :param str key: the key in the Function attributes list of the
                        attribute that was edited.
        :param str value: the new text to update the Gtk.Widget() with.
        :return: None
        :rtype: None
        """
        _dic_switch = {
            'function_code': [self.txtCode.do_update, 0],
            'name': [self.txtName.do_update, 1],
            'remarks': [self.txtRemarks.do_update, 2],
            'safety_critical': [self.chkSafetyCritical.do_update, 3]
        }

        (_function, _id) = _dic_switch.get(key)
        _function(value, self._lst_handler_id[_id])

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * Gtk.Entry() 'changed' signal
            * Gtk.TextView() 'changed' signal

        This method sends the 'wvwEditedFunction' message.

        :param Gtk.Entry entry: the Gtk.Entry() that called the method.
        :param int index: the position in the Function class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Widget().
        :return: None
        :rtype: None
        """
        _dic_keys = {0: 'function_code', 1: 'name', 2: 'remarks'}
        _key = ''
        _text = ''
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = str(entry.get_text())
        except ValueError:
            _new_text = ''

        pub.sendMessage(
            'wvw_editing_function',
            module_id=self._function_id,
            key=_key,
            value=_new_text)

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

        pub.sendMessage(
            'wvw_editing_function',
            module_id=self._function_id,
            key=_key,
            value=_new_text)

        togglebutton.handler_unblock(self._lst_handler_id[index])
