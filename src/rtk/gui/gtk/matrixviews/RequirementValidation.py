# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.matrixviews.RequirementValidation.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""The Requirement:Validation Matrix View Module."""

from pubsub import pub

# Import other RAMSTK modules.
from rtk.gui.gtk.rtk.Widget import _, gtk
from rtk.gui.gtk import rtk


class MatrixView(gtk.HBox, rtk.RAMSTKBaseMatrix):
    """
    This is the Requirement:Validation RAMSTK Matrix View.

    Attributes of the Requirement:Validation Matrix View are:
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the Requirement:Validation Matrix View.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`rtk.RAMSTK.RAMSTK`
        """
        gtk.HBox.__init__(self)
        rtk.RAMSTKBaseMatrix.__init__(self, controller, **kwargs)

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
                          _(u"Requirement\nValidation") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays requirement/validation matrix for the "
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

    def _do_request_create(self, __button):
        """
        Save the currently selected Validation:Requirement Matrix row.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_create(
            self._revision_id, self._matrix_type)

    def _do_request_update(self, __button):
        """
        Save the currently selected Requirement:Validation Matrix row.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_do_update_matrix(
            self._revision_id, self._matrix_type)

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Create the buttonbox for the Requirement:Validation Matrix View.

        :return: _buttonbox; the gtk.ButtonBox() for the Requirement:Validation
                             Matrix View.
        :rtype: :py:class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Save the Requirement:Validation Matrix to the open RAMSTK "
              u"Program database."),
            _(u"Create or refresh the Requirement:Validation Matrix.")
        ]
        _callbacks = [self._do_request_update, self._do_request_create]
        _icons = ['save', 'view-refresh']

        _buttonbox = rtk.RAMSTKBaseMatrix._make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def _on_select_revision(self, module_id):
        """
        Load the Requirement:Validation Matrix View with matrix information.

        :param int revision_id: the Revision ID to select the
                                Requirement:Validation matrix for.
        :return: None
        :rtype: None
        """
        self._revision_id = module_id

        self._dtc_data_controller = self._mdcRAMSTK.dic_controllers[
            'requirement']
        (_matrix, _column_hdrs,
         _row_hdrs) = self._dtc_data_controller.request_do_select_all_matrix(
             self._revision_id, self._matrix_type)
        if _matrix is not None:
            rtk.RAMSTKBaseMatrix.do_load_matrix(self, _matrix, _column_hdrs,
                                                _row_hdrs, _(u"Requirement"))

        return None
