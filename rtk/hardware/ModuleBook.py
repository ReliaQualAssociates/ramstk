#!/usr/bin/env python
"""
############################
Hardware Package Module View
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.gui.gtk.ModuleBook.py is part of The RTK Project
#
# All rights reserved.

import sys

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.widgets as _widg
#from ListBook import ListView
from WorkBook import WorkView

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

# TODO: Fix all docstrings; copy-paste errors.
class ModuleView(object):
    """
    The Module Book view displays all the Hardware items associated with the
    RTK Project in a hierarchical list.  The attributes of a Module Book view
    are:

    :ivar _model: the :class:`rtk.hardware.BoM.Model` data model that is
                  currently selected.

    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View :class:`gtk.TreeView`.
    :ivar _workbook: the :class:`rtk.requirement.WorkBook.WorkView` associated
                     with this instance of the Module View.
    :ivar dtcRequirement: the :class:`rtk.requirement.Requirement.Requirement`
                          data controller to use for accessing the Requirement
                          data models.
    :ivar dtcStakeholder: the :class:`rtk.stakeholder.Stakeholder.Stakeholder`
                          data controller to use for accessing the Stakeholder
                          data models.
    :ivar treeview: the :class:`gtk.TreeView` displaying the list of
                    Requirements.
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Function package.

        :param rtk.hardware.Hardware controller: the instance of the Hardware
                                                 data controller to use with
                                                 this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Hardware
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Hardware view.  Pass -1 to add to the end.
        :param *args: other user arguments to pass to the Module View.
        """

        # Initialize private list attribute
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._model = None
        self._allocation_model = None

        # Initialize public scalar attributes.
        self.dtcBoM = controller
        self.dtcAllocation = args[0][0]
        self.dtcHazard = args[0][1]
        self.dtcSimilarItem = args[0][2]
        self.dtcFMECA = args[0][3]
        self.dtcPoF = args[0][4]

        # Create the main Hardware class treeview.
        # TODO: Update the hardware.xml file to accomodate the prediction stuff.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Hardware', 3,
                                                    None, None,
                                                    _conf.RTK_COLORS[4],
                                                    _conf.RTK_COLORS[5])
        _selection = self.treeview.get_selection()

        self.treeview.set_tooltip_text(_(u"Displays the hierarchical list of "
                                         u"the system hardware."))

        self._lst_handler_id.append(_selection.connect('changed',
                                                       self._on_row_changed))
        #self.treeview.connect('cursor_changed', self._on_row_changed,
        #                      None, None))
        #self._lst_handler_id.append(
        #    self.treeview.connect('row_activated', self._on_row_changed))
        self._lst_handler_id.append(
            self.treeview.connect('button_release_event',
                                  self._on_button_press))

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Hardware") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the system hardware structure "
                                  u"for the selected revision."))

        rtk_view.notebook.insert_page(_scrollwindow, tab_label=_label,
                                      position=position)

        # Create a List View to associate with this Module View.
        self._listbook = None
        #self._listbook = ListView(rtk_view.listview, self, self.dtcMatrices)

        # Create a Work View to associate with this Module View.
        self._workbook = WorkView(rtk_view.workview, self)

    def request_load_data(self, dao, revision_id):
        """
        Loads the Hardware Module Book view gtk.TreeModel() with hardware
        information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_hardware, __) = self.dtcBoM.request_bom(dao, revision_id)
        self.dtcAllocation.request_allocation(dao)
        self.dtcHazard.request_hazard(dao)
        self.dtcSimilarItem.request_similar_item(dao)

        # Only load the hardware associated with the selected Revision.
        _hardware = [_h for _h in _hardware if _h[0] == revision_id]
        _top_reqs = [_h for _h in _hardware if _h[23] == -1]

        # Load all the FMECA and PoF analyses.
        for _h in _hardware:
            self.dtcFMECA.request_fmea(dao, _h[1], None, revision_id)
            self.dtcPoF.request_pof(dao, _h[1])

        # Clear the Hardware Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()

        # Recusively load the Hardware Module View gtk.TreeModel().
        self._load_treeview(dao, _top_reqs, _hardware, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        #self._listbook.load(revision_id)

        return False

    def _load_treeview(self, dao, parents, hardware, model, row=None):
        """
        Method to recursively load the gtk.TreeModel().  Recursive loading is
        needed to accomodate the hierarchical structure of Hardware.

        :param rtk.DAO dao: the Data Access Object to pass to the Hardware data
                            controller.
        :param list parents: the list of top-level requirements to load.
        :param list hardware: the complete list of hardware to use for finding
                              the child hardware for each parent.
        :param gtk.TreeModel model: the Hardware Module View gtk.TreeModel().
        :keyword gtk.TreeIter row: the parent gtk.TreeIter().
        """
# TODO: Is passing the dao object around the best way or is it better as a private instance attribute?
        _icon = _conf.ICON_DIR + '32x32/assembly.png'
        _assembly_icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _icon = _conf.ICON_DIR + '32x32/component.png'
        _component_icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        for _hardware in parents:
            if _hardware[23] == -1:
                row = None
            if _hardware[24] == 0:
                _data = list(_hardware) + [_assembly_icon]
            elif _hardware[24] == 1:
                _data = list(_hardware) + [_component_icon]
            _piter = model.append(row, _data)
            _parent_id = _hardware[1]

            # Find the child requirements of the current parent requirement.
            # These # will be the new parent requirements to pass to this
            # method.
            _parents = [_h for _h in hardware if _h[23] == _parent_id]
            self._load_treeview(dao, _parents, hardware, model, _piter)

        return False

    def update(self, position, new_text):
        """
        Updates the Module Book gtk.TreeView() with changes to the Hardware
        data model attributes.  Called by other views when the Hardware data
        model attributes are edited via their gtk.Widgets().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar next_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_button_press(self, treeview, event):
        """
        Callback method for handling mouse clicks on the Hardware package
        Module Book gtk.TreeView().

        :param gtk.TreeView treeview: the Hardware class gtk.TreeView().
        :param gtk.gdk.Event event: the gtk.gdk.Event() that called this method
                                    (the important attribute is which mouse
                                    button was clicked).
                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if event.button == 1:
            _selection = treeview.get_selection()
            self._on_row_changed(_selection)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _on_row_changed(self, selection):
        """
        Callback method to handle events for the Hardware package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeSelection selection: the Hardware class gtk.TreeView()'s
                                            gtk.TreeSelection().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        selection.handler_block(self._lst_handler_id[0])

        (_model, _row) = selection.get_selected()
        _hardware_id = _model.get_value(_row, 1)

        self._model = self.dtcBoM.dicHardware[_hardware_id]

        self._workbook.load(self._model)

        selection.handler_block(self._lst_handler_id[0])

        return False
