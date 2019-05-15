# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Function.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Function Work View."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.Utilities import boolean_to_integer
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, Gtk
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

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Function package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Function')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_gendata_labels = [
            _("Function Code:"),
            _("Function Description:"),
            _("Remarks:")
        ]

        # Initialize private scalar attributes.
        self._function_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # General data page widgets.
        self.chkSafetyCritical = ramstk.RAMSTKCheckButton(
            label=_("Function is safety critical."),
            tooltip=_("Indicates whether or not the selected function is "
                      "safety critical."))

        self.txtCode = ramstk.RAMSTKEntry(
            width=125, tooltip=_("A unique code for the selected function."))
        self.txtName = ramstk.RAMSTKEntry(
            width=800, tooltip=_("The name of the selected function."))
        self.txtRemarks = ramstk.RAMSTKTextView(
            Gtk.TextBuffer(),
            width=800,
            tooltip=_("Enter any remarks associated with the "
                      "selected function."))

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._on_edit, 'mvw_editing_function')
        pub.subscribe(self._do_load_page, 'selected_function')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the Gtk.ButtonBox() for the Function class Work View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Function class Work
                 View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = []
        _callbacks = []
        _icons = []

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def __make_ui(self):
        """
        Make the Function class Gtk.Notebook() general data page.

        :return: None
        :rtype: None
        """
        (_frame, _fixed, __,
         _y_pos) = RAMSTKWorkView.make_general_data_page(self)

        _fixed.put(self.chkSafetyCritical, 5, _y_pos[2] + 110)

        # Connect to callback functions for editable Gtk.Widgets().
        self._lst_handler_id.append(
            self.txtCode.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtName.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.chkSafetyCritical.connect('toggled', self._on_toggled, 3))

        self.pack_start(self.__make_buttonbox(), False, False, 0)
        self.pack_start(_frame, True, True, 0)
        self.show_all()

        return None

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text('')
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text('')
        self.txtName.handler_unblock(self._lst_handler_id[1])

        _buffer = self.txtRemarks.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[2])
        _buffer.set_text('')
        _buffer.handler_block(self._lst_handler_id[2])

        self.chkSafetyCritical.handler_block(self._lst_handler_id[3])
        self.chkSafetyCritical.set_active(False)
        self.chkSafetyCritical.handler_unblock(self._lst_handler_id[3])

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

        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(attributes['function_code']))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text(str(attributes['name']))
        self.txtName.handler_unblock(self._lst_handler_id[1])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[2])
        _textbuffer.set_text(str(attributes['remarks']))
        _textbuffer.handler_unblock(self._lst_handler_id[2])

        self.chkSafetyCritical.handler_block(self._lst_handler_id[3])
        self.chkSafetyCritical.set_active(int(attributes['safety_critical']))
        self.chkSafetyCritical.handler_unblock(self._lst_handler_id[3])

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

        return None

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
        if key == 'function_code':
            self.txtCode.handler_block(self._lst_handler_id[0])
            self.txtCode.set_text(str(value))
            self.txtCode.handler_unblock(self._lst_handler_id[0])
        elif key == 'name':
            self.txtName.handler_block(self._lst_handler_id[1])
            self.txtName.set_text(str(value))
            self.txtName.handler_unblock(self._lst_handler_id[1])
        elif key == 'remarks':
            _textbuffer = self.txtRemarks.do_get_buffer()
            _textbuffer.handler_block(self._lst_handler_id[2])
            _textbuffer.set_text(str(value))
            _textbuffer.handler_unblock(self._lst_handler_id[2])
        elif key == 'safety_critical':
            self.chkSafetyCritical.handler_block(self._lst_handler_id[3])
            self.chkSafetyCritical.set_active(int(value))
            self.chkSafetyCritical.handler_unblock(self._lst_handler_id[3])

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
        _key = ''
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            _key = 'function_code'
            _text = str(entry.get_text())
        elif index == 1:
            _key = 'name'
            _text = str(entry.get_text())
        elif index == 2:
            _key = 'remarks'
            _text = self.txtRemarks.do_get_text()

        pub.sendMessage(
            'wvw_editing_function',
            module_id=self._function_id,
            key=_key,
            value=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_toggled(self, togglebutton, index):
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param togglebutton: the RAMSTKToggleButton() that called this method.
        :type: :class:`ramstk.gui.gtk.ramstk.Button.RAMSTKToggleButton`
        :param int index: the index in the signal handler ID list.
        :return: None
        :rtype: None
        """
        togglebutton.handler_block(self._lst_handler_id[index])

        _key = 'safety_critical'
        _text = boolean_to_integer(self.chkSafetyCritical.get_active())

        togglebutton.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage(
            'wvw_editing_function',
            module_id=self._function_id,
            key=_key,
            value=_text)

        return None
