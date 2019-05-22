# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.matrixviews.ValidationHardware.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Validation:Hardware Matrix View Module."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, GObject, Gtk
from ramstk.gui.gtk.ramstk import RAMSTKBaseMatrix


class MatrixView(Gtk.HBox, RAMSTKBaseMatrix):
    """
    This is the Validation:Hardware RAMSTK Matrix View.

    Attributes of the Validation:Hardware Matrix View are:
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize the Validation:Hardware Matrix View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        GObject.GObject.__init__(self)
        RAMSTKBaseMatrix.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.pack_start(
            RAMSTKBaseMatrix._make_buttonbox(
                self,
                icons=['view-refresh'],
                tooltips=[
                    _("Create or refresh the Validation:Hardware Matrix.")
                ],
                callbacks=[self._do_request_create]),
            False, False, 0)

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.add(self.matrix)

        self.pack_end(_scrolledwindow, True, True, 0)

        _label = Gtk.Label()
        _label.set_markup("<span weight='bold'>" + _("Validation\nHardware") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(Gtk.Justification.CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _("Displays validation/hardware matrix for the "
              "selected revision."))

        # self.hbx_tab_label.pack_start(_image, True, True, 0)
        self.hbx_tab_label.pack_end(_label, True, True, 0)
        self.hbx_tab_label.show_all()

        self.show_all()

    def _do_request_create(self, __button):
        """
        Create or update the Validation:Hardware Matrix.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_create_validation_matrix',
            node_id=self._revision_id,
            matrix_type=self._matrix_type)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update(self, __button):
        """
        Save the currently selected Validation:Hardware Matrix row.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_validation_matrix',
            node_id=self._revision_id,
            matrix_type=self._matrix_type)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)
