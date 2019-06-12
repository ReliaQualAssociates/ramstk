# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.matrixviews.RequirementHardware.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Requirement:Hardware Matrix View Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKBaseMatrix
from ramstk.gui.gtk.ramstk.Widget import Gdk, GObject, Gtk, _


class MatrixView(Gtk.HBox, RAMSTKBaseMatrix):
    """
    This is the Requirement:Hardware RAMSTK Matrix View.

    Attributes of the Requirement:Hardware Matrix View are:
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize the Requirement:Hardware Matrix View.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        GObject.GObject.__init__(self)
        RAMSTKBaseMatrix.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_matrix_labels = {
            'rqrmnt_hrdwr': [
                _("Create or refresh the Requirement:Hardware Matrix."),
                _("Requirement\nHardware"),
                _(
                    "Displays requirement/hardware matrix for the selected "
                    "revision.",
                ),
            ],
            'rqrmnt_sftwr': [
                _("Create or refresh the Requirement:Software Matrix."),
                _("Requirement\nSoftware"),
                _(
                    "Displays requirement/software matrix for the selected "
                    "revision.",
                ),
            ],
            'rqrmnt_vldtn': [
                _("Create or refresh the Requirement:Validation Matrix."),
                _("Requirement\nValidation"),
                _(
                    "Displays requirement/validation matrix for the selected "
                    "revision.",
                ),
            ],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.

    def _do_request_create(self, __button):
        """
        Create or update the Requirement:Hardware matrix.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_create_requirement_matrix',
            node_id=self._revision_id,
            matrix_type=self._matrix_type,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update(self, __button):
        """
        Save the Requirement:Hardware Matrix.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_requirement_matrix',
            node_id=self._revision_id,
            matrix_type=self._matrix_type,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)
