# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.matrixviews.ValidationHardware.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Validation:Hardware Matrix View Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKBaseMatrix
from ramstk.gui.gtk.ramstk.Widget import Gdk, GObject, Gtk, _


class MatrixView(Gtk.HBox, RAMSTKBaseMatrix):
    """
    This is the Validation:Hardware RAMSTK Matrix View.

    Attributes of the Validation:Hardware Matrix View are:
    """
    _dic_matrix_labels = {
        'vldtn_hrdwr': [
            _("Create or refresh the Validation:Hardware Matrix."),
            _("Validation\nHardware"),
            _(
                "Displays validation/hardware matrix for the selected "
                "revision.",
            ),
        ],
        'vldtn_rqrmnt': [
            _("Create or refresh the Validation:Requirement Matrix."),
            _("Validation\nRequirement"),
            _(
                "Displays validation/requirement matrix for the selected "
                "revision.",
            ),
        ],
    }

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

        # Subscribe to PyPubSub messages.

    def _do_request_create(self, __button):
        """
        Create or update the Validation:Hardware Matrix.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_create_validation_matrix',
            node_id=self._revision_id,
            matrix_type=self._matrix_type,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update(self, __button):
        """
        Save the currently selected Validation:Hardware Matrix row.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_validation_matrix',
            node_id=self._revision_id,
            matrix_type=self._matrix_type,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)
