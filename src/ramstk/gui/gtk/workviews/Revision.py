# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Revision.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Revision Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk import (RAMSTKEntry, RAMSTKFrame, RAMSTKLabel,
                                   RAMSTKScrolledWindow, RAMSTKTextView,
                                   do_make_label_group)
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, Gtk
from .WorkView import RAMSTKWorkView

# from Assistants import AddRevision


class GeneralData(RAMSTKWorkView):
    """
    Display general Revision attribute data in the RAMSTK Work Book.

    The Revision Work View displays all the general data attributes for the
    selected Revision. The attributes of a Revision General Data Work View are:

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
    _lst_labels = [_("Revision Code:"), _("Revision Name:"), _("Remarks:")]

    def __init__(self, configuration, **kwargs):
        """
        Initialize the Revision Work View general data page.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKWorkView.__init__(self, configuration, module='revision')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtCode = RAMSTKEntry()
        self.txtName = RAMSTKEntry()
        self.txtRemarks = RAMSTKTextView(Gtk.TextBuffer())

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_revision')
        pub.subscribe(self._on_edit, 'mvw_editing_revision')

    def __make_ui(self):
        """
        Create the Revision Work View general data page.

        :return: _frame; the Gtk.Frame() to embed in the notebook page.
        :rtype: :class:`Gtk.Frame`
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
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[2])
        self.pack_end(_scrollwindow, True, True, 0)

        _label = RAMSTKLabel(
            _("General\nData"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays general information for the selected Revision"))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.txtName.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtCode.connect('changed', self._on_focus_out, 2))

    def __set_properties(self):
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

    def _do_clear_page(self):
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

    def _do_load_page(self, attributes):
        """
        Load the Revision General Data page.

        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        RAMSTKWorkView.on_select(
            self,
            title=_("Analyzing Revision {0:s} - {1:s}").format(
                str(attributes['revision_code']), str(attributes['name'])))

        self.txtName.do_update(str(attributes['name']), 0)
        self.txtRemarks.do_update(str(attributes['remarks']), 1)
        self.txtCode.do_update(str(attributes['revision_code']), 2)

    def _do_request_update(self, __button):
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

    def _do_request_update_all(self, __button):
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

    def _on_edit(self, module_id, key, value):  # pylint: disable=unused-argument
        """
        Update the Revision Work View Gtk.Widgets().

        This method updates the Revision Work View Gtk.Widgets() with changes
        to the Revision data model attributes.  This method is called whenever
        an attribute is edited in a different RAMSTK View.

        :param int module_id: the ID of the Revision being edited.  This
                              parameter is required to allow the PyPubSub
                              signals to call this method and the
                              request_set_attributes() method in the
                              RAMSTKDataController.
        :param str key: the key in the Revision attributes list of the
                        attribute that was edited.
        :param str value: the new text to update the Gtk.Widget() with.
        :return: None
        :rtype: None
        """
        _dic_switch = {
            'name': [self.txtName.do_update, 0],
            'remarks': [self.txtRemarks.do_update, 1],
            'revision_code': [self.txtCode.do_update, 2]
        }

        (_function, _id) = _dic_switch.get(key)
        _function(value, self._lst_handler_id[_id])

    def _on_focus_out(self, entry, __event, index):
        """
        Handle changes made in RAMSTKEntry() and RAMSTKTextView() widgets.

        This method is called by:

            * RAMSTKEntry() 'focus-out' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvw_editing_revision' message.

        :param entry: the Gtk.Entry() that called the method.
        :type entry: :class:`Gtk.Entry`
        :param __event: the Gdk.EventFocus that triggerd the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Revision class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Entry().
        :return: None
        :rtype: None
        """
        _dic_keys = {0: 'name', 1: 'remarks', 2: 'code'}
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        if index in [0, 2]:
            try:
                _new_text = str(entry.get_text())
            except ValueError:
                _new_text = ''
        else:
            try:
                _new_text = self.txtRemarks.do_get_text()
            except ValueError:
                _new_text = ''

        pub.sendMessage(
            'wvw_editing_revision',
            module_id=self._revision_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])
