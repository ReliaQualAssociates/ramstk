# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.matrixviews.RequirementSoftware.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Requirement:Software Matrix View Module
-------------------------------------------------------------------------------
"""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk.rtk.Widget import _, gobject, gtk
from rtk.gui.gtk import rtk


class MatrixView(gtk.HBox, rtk.RTKBaseMatrix):
    """
    This is the Requirement:Software RTK Matrix View.  Attributes of the
    Requirement:Software Matrix View are:
    """

    def __init__(self, controller, **kwargs):
        """
        Method to initialize the List View.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.HBox.__init__(self)
        rtk.RTKBaseMatrix.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_data_controller = None
        self._revision_id = None
        self._matrix_type = kwargs['matrix_type']

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Requirement\nSoftware") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays requirement/software matrix for the "
              u"selected revision."))

        # self.hbx_tab_label.pack_start(_image)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.matrix)

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')

    def _do_request_update(self, __button):
        """
        Method to save the currently selected Requirement:Software Matrix row.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_data_controller.request_update_matrix(
            self._revision_id, self._matrix_type)

    def _make_buttonbox(self):
        """
        Method to create the buttonbox for the Requirement:Software Matrix
        View.

        :return: _buttonbox; the gtk.ButtonBox() for the Requirement:Software
                             Matrix View.
        :rtype: :py:class:`gtk.ButtonBox`
        """

        _tooltips = [
            _(u"Save the Requirement:Software Matrix to the open RTK "
              u"Program database."),
        ]
        _callbacks = [
            self._do_request_update,
        ]
        _icons = [
            'save',
        ]

        _buttonbox = rtk.RTKBaseMatrix._make_buttonbox(self, _icons, _tooltips,
                                                       _callbacks, 'vertical')

        return _buttonbox

    def _on_select_revision(self, module_id):
        """
        Method to load the Requirement:Software Matrix View gtk.TreeModel() with
        matrix information whenever a new Revision is selected.

        :param int revision_id: the Revision ID to select the
                                Requirement:Software matrix for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._revision_id = module_id

        self._dtc_data_controller = \
            self._mdcRTK.dic_controllers['requirement']
        (_matrix, _column_hdrs,
         _row_hdrs) = self._dtc_data_controller.request_select_all_matrix(
             self._revision_id, self._matrix_type)

        return rtk.RTKBaseMatrix.do_load_matrix(self, _matrix, _column_hdrs,
                                                _row_hdrs, _(u"Requirement"))
