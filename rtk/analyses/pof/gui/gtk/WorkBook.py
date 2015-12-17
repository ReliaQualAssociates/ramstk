#!/usr/bin/env python
"""
##########################
PoF Package Work Book View
##########################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.pof.gui.gtk.WorkBook.py is part of The RTK Project
#
# All rights reserved.

import sys

# Modules required for the GUI.
import pango
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
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def get_mechanism_id(mechanism):
    """
    Helper function to return the mechanism id of the passed mechanism object.
    Used to sort the list of failure mechanism objects before loading into the
    gtk.TreeView().

    :param rtk.analyses.pof.Mechanism.model mode: the failure mechanism object
                                                  to return the mechanism id
                                                  for.
    :return mechanism_id: the mechanism id of the passed mechanism object.
    :rtype: int
    """

    return mechanism.mechanism_id


class WorkView(gtk.HBox):
    """
    The Work Book view displays all the attributes for the selected
    Physics of Failure (PoF) Analysis.  The attributes of a Physics of Failure
    Analysis Work Book view are:

    :ivar _lst_priority: default value: [_(u"Test Required"),
                                         _(u"Inspection Topic"),
                                         _(u"Functional Topic"),
                                         _(u"Quality Topic")]
    :ivar _lst_damage_models: default value: []
    :ivar _lst_handler_id: default value: []

    :ivar _hardware_id: default value: None

    :ivar dtcPoF: the PoF data controller.
    :ivar btnAddSibling: gtk.Button() used to add a "sibling" element.
    :ivar btnAddChild: gtk.Button() used to add a "child" element.
    :ivar btnRemove: gtk.Button() used to remove the selected element.
    :ivar btnSavePoF: gkt.Button() used to save the selected PoF Analysis.
    :ivar tvwPoF: gtk.TreeView() used to display the PoF Analysis.
    """

    def __init__(self, controller):
        """
        Initializes the Work Book view for the Physics of Failure Analysis
        module.

        :param rtk.analyses.pof.PoF controller: the PoF data controller.
        """

        gtk.HBox.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_priority = [(0, _("")), (1, _(u"Test Required")),
                              (2, _(u"Inspection Topic")),
                              (3, _(u"Functional Topic")),
                              (4, _(u"Quality Topic"))]
        self._lst_damage_models = [(0, _("")),
                                   (1, _(u"Adhesion Wear Model for Bearings")),
                                   (2, _(u"Arrhenius")),
                                   (3, _(u"Coffin-Manson")),
                                   (4, _(u"Empirical/DOE")), (5, _(u"Eyring")),
                                   (6, _(u"Inverse Power Law")),
                                   (7, _(u"Time Fraction of Damaging "
                                         u"Operating Conditions"))]
        self._lst_operating_parameters = [(0, _("")),
                                          (1, _(u"Ambient Temperature")),
                                          (2, _(u"Contamination, "
                                                u"Concentration")),
                                          (3, _(u"Contamination, "
                                                u"Particle Size")),
                                          (4, _(u"Coolant Temperature")),
                                          (5, _(u"Drag Torque")),
                                          (6, _(u"Dynamic Load")),
                                          (7, _(u"Exhaust Gas Temperature")),
                                          (8, _(u"Load Frequency vs Eigen "
                                                u"Frequency")),
                                          (9, _(u"Lubrication Flow")),
                                          (10, _(u"Lubrication Leak Rate")),
                                          (11, _(u"Maximum Load")),
                                          (12, _(u"Minimum-Maximum Load")),
                                          (13, _(u"Number of Braking Events")),
                                          (14, _(u"Number of Cycles")),
                                          (15, _(u"Number of Overload "
                                                 u"Events")),
                                          (16, _(u"Number of Shifts")),
                                          (17, _(u"Oil Pressure")),
                                          (18, _(u"Oil Temperature")),
                                          (19, _(u"Operating Time at "
                                                 u"Condition")),
                                          (20, _(u"Particle Size")),
                                          (21, _(u"Peak Pressure")),
                                          (22, _(u"RPM")),
                                          (23, _(u"Temperature")),
                                          (24, _(u"Torque"))]
        self._lst_load_history = [(0, _("")), (1, _(u"Cycle Counts")),
                                  (2, _(u"Histogram")),
                                  (3, _(u"Histogram, Bivariate")),
                                  (4, _(u"Level Crossing")),
                                  (5, _(u"Rain Flow Counting")),
                                  (6, _(u"Time at Level")),
                                  (7, _(u"Time at Load (max torque applied)")),
                                  (8, _(u"Time at Maximum"))]

        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._hardware_id = None

        # Initialize public scalar attributes.
        self.dtcPoF = controller

        self.btnAddSibling = _widg.make_button(width=35,
                                               image='insert_sibling')
        self.btnAddChild = _widg.make_button(width=35, image='insert_child')
        self.btnRemove = _widg.make_button(width=35, image='remove')
        self.btnSavePoF = _widg.make_button(width=35, image='save')

        self.tvwPoF = gtk.TreeView()

    def create_page(self):
        """
        Create the Physics of Failure Analysis gtk.Notebook() page for
        displaying the PoF Analysis for the selected Hardware.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the PoF gtk.TreeView().                                #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.tvwPoF.set_tooltip_text(_(u"Displays the physics of failure "
                                       u"analysis for the currently selected "
                                       u"hardware item."))

        _model = gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_INT)
        self.tvwPoF.set_model(_model)

        _headings = [_(u"Mechanism ID"), _(u"Description"),
                     _(u"Proposed\nDamage\nModel"), _(u"Priority"),
                     _(u"Measurable\nOperating\nParameter"),
                     _(u"Means for\nClassifying\nLoad History"),
                     _(u"Boundary\nConditions"), _(u"Remarks"), "", ""]

        for i in range(9):
            _column = gtk.TreeViewColumn()
            if i == 0:                      # ID
                _cell = gtk.CellRendererPixbuf()
                _cell.set_property('visible', 1)
                _cell.set_property('xalign', 0.5)
                _column.pack_start(_cell, False)
                _column.set_attributes(_cell, pixbuf=0)

                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=1)

            elif i == 1:                    # Description
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 2)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

            elif i == 2:                    # Proposed damage model
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                # _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('has-entry', False)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 3)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, background=13,
                                       editable=9)
                for j in range(len(self._lst_damage_models)):
                    _cellmodel.append([self._lst_damage_models[j][1]])
                # for j in range(len(_conf.RTK_DAMAGE_MODELS)):
                #     _cellmodel.append([_conf.RTK_DAMAGE_MODELS[j]])

            elif i == 3:                    # Priority
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                # _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('has-entry', False)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 4)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=4, background=13,
                                       editable=9)
                for j in range(len(self._lst_priority)):
                    _cellmodel.append([self._lst_priority[j][1]])

            elif i == 4:                    # Measurable parameter
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                # _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 5)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=5, background=14,
                                       editable=10)
                for j in range(len(self._lst_operating_parameters)):
                    _cellmodel.append([self._lst_operating_parameters[j][1]])
                # for j in range(len(_conf.RTK_OPERATING_PARAMETERS)):
                #     _cellmodel.append([_conf.RTK_OPERATING_PARAMETERS[j]])

            elif i == 5:                    # Load history
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                # _cellmodel.append([""])
                _cell = gtk.CellRendererCombo()
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 6)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=6, background=14,
                                       editable=10)
                for j in range(len(self._lst_load_history)):
                    _cellmodel.append([self._lst_load_history[j][1]])
                # for j in range(len(_conf.RTK_LOAD_HISTORY)):
                #     _cellmodel.append([_conf.RTK_LOAD_HISTORY[j]])

            elif i == 6:                    # Boundary conditions
                _cell = gtk.CellRendererText()
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 7)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=7, background=15,
                                       editable=11)

            elif i == 7:                    # Remarks
                _cell = gtk.CellRendererText()
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('visible', 1)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edit, 8)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=8, background=16,
                                       editable=12)

            elif i == 8:
                for j in range(7):
                    _cell = gtk.CellRendererText()
                    _cell.set_property('editable', 0)
                    _column.pack_start(_cell, True)
                    _column.set_attributes(_cell, text=j + 9)
                    _column.set_visible(False)

            elif i == 9:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=17)
                _column.set_visible(False)

            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _headings[i] +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column.set_widget(_label)
            _column.set_alignment(0.5)

            _column.set_expand(True)
            _column.set_resizable(True)
            _column.set_min_width(1)

            self.tvwPoF.append_column(_column)

        self.tvwPoF.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        self.pack_start(_bbox, False, True)

        _vbox = gtk.VBox()

        self.pack_end(_vbox, True, True)

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwPoF)

        _frame = _widg.make_frame(label=_(u"Physics of Failure Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddSibling, False, False)
        _bbox.pack_start(self.btnAddChild, False, False)
        _bbox.pack_start(self.btnRemove, False, False)
        _bbox.pack_start(self.btnSavePoF, False, False)

        self.btnAddSibling.set_tooltip_text(_(u"Add a failure mechanism to "
                                              u"the selected hardware item."))
        self.btnAddChild.set_tooltip_text(_(u"Add an operating load to the "
                                            u"selected failure mechanism."))
        self.btnRemove.set_tooltip_text(_(u"Remove the selected failure "
                                          u"mechanism from the selected "
                                          u"hardware item."))
        self.btnSavePoF.set_tooltip_text(_(u"Saves the PoF to the open "
                                           u"RTK Project database."))

        # Connect to callback functions.
        self._lst_handler_id.append(
            self.btnAddSibling.connect('clicked',
                                       self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnAddChild.connect('clicked',
                                     self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnRemove.connect('clicked',
                                   self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.btnSavePoF.connect('clicked',
                                    self._on_button_clicked, 3))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the PoF Analysis.             #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self._lst_handler_id.append(
            self.tvwPoF.connect('cursor_changed', self._on_row_changed))

        return False

    def load_page(self, hardware_id, path=None):
        """
        Function to load the widgets on the PoF Analysis page.

        :param `rtk.hardware.Hardware.Hardware` controller: the Hardware data
                                                            controller instance
                                                            being used by RTK.
        :param int hardware_id: the Hardware ID to load the PoF Analysis for.
        :keyword str path: the path of the parent hardware item in the
                           PoF Analysis gtk.TreeView().
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        self._hardware_id = hardware_id

        _model = self.tvwPoF.get_model()
        _model.clear()

        # Find all the PoF Analysis for the selected Hardware Item.
        _mechanisms = self.dtcPoF.dicPoF[hardware_id].dicMechanisms.values()
        _mechanisms = sorted(_mechanisms, key=get_mechanism_id)
        _piter = [None, None, None]
        for _mechanism in _mechanisms:
            _icon = _conf.ICON_DIR + '32x32/mechanism.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _attributes = _mechanism.get_attributes()
            _data = (_icon, _attributes[1], _attributes[2], '', '', '', '',
                     '', '', 0, 0, 0, 0, 'light gray', 'light gray',
                     'light gray', 'light gray', 1)
            _piter[0] = _model.append(None, _data)

            for _load in _mechanism.dicLoads.values():
                _icon = _conf.ICON_DIR + '32x32/load.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _attributes = _load.get_attributes()
                _damage_model = self._lst_damage_models[_attributes[3]][1]
                _priority = self._lst_priority[_attributes[4]][1]
                _data = (_icon, _attributes[1], _attributes[2], _damage_model,
                         _priority, '', '', '', '', 1, 0, 0, 0, 'white',
                         'light gray', 'light gray', 'light gray', 2)
                _piter[1] = _model.append(_piter[0], _data)

                for _stress in _load.dicStresses.values():
                    _icon = _conf.ICON_DIR + '32x32/stress.png'
                    _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                    _attributes = _stress.get_attributes()
                    _parameter = self._lst_operating_parameters[_attributes[3]][1]
                    _history = self._lst_load_history[_attributes[4]][1]
                    _data = (_icon, _attributes[1], _attributes[2], '', '',
                             _parameter, _history, '', _attributes[5], 0, 1, 0,
                             1, 'light gray', 'white', 'light gray', 'white',
                             3)
                    _piter[2] = _model.append(_piter[1], _data)

                    for _method in _stress.dicMethods.values():
                        _icon = _conf.ICON_DIR + '32x32/method.png'
                        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22,
                                                                     22)
                        _attributes = _method.get_attributes()
                        _data = (_icon, _attributes[1], _attributes[2], '', '',
                                 '', '', _attributes[3], _attributes[4], 0, 0,
                                 1, 1, 'light gray', 'light gray', 'white',
                                 'white', 4)
                        _model.append(_piter[2], _data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                return False
        _column = self.tvwPoF.get_column(0)
        self.tvwPoF.set_cursor(path, None, False)
        self.tvwPoF.row_activated(path, _column)
        self.tvwPoF.expand_all()

        return False

    def _on_button_clicked(self, __button, index):
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _pof = self.dtcPoF.dicPoF[self._hardware_id]

        (_model, _row) = self.tvwPoF.get_selection().get_selected()
        _id = _model.get_value(_row, 1)
        _level = _model.get_value(_row, 17)

        if index == 0:                      # Add sibling
            if _level == 1:                 # Failure Mechanism
                (_results,
                 _error_code,
                 _last_id) = self.dtcPoF.add_mechanism(self._hardware_id)

            elif _level == 2:               # Operating load
                _piter = _model.iter_parent(_row)
                _mechanism_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcPoF.add_load(self._hardware_id,
                                                  _mechanism_id)

            elif _level == 3:               # Operating stress
                _piter = _model.iter_parent(_row)
                _load_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mechanism_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcPoF.add_stress(self._hardware_id,
                                                    _mechanism_id, _load_id)

            elif _level == 4:               # Test method
                _piter = _model.iter_parent(_row)
                _stress_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _load_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mechanism_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcPoF.add_method(self._hardware_id,
                                                    _mechanism_id, _load_id,
                                                    _stress_id)

            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_row))
                except TypeError:
                    _path = None
                self.load_page(self._hardware_id, _path)

        elif index == 1:                    # Add child
            if _level == 1:                 # Failure mechanism
                (_results,
                 _error_code,
                 _last_id) = self.dtcPoF.add_load(self._hardware_id, _id)
            elif _level == 2:               # Operating load
                _piter = _model.iter_parent(_row)
                _mechanism_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcPoF.add_stress(self._hardware_id,
                                                    _mechanism_id, _id)

            elif _level == 3:               # Operating stress
                _piter = _model.iter_parent(_row)
                _load_id = _model.get_value(_piter, 1)
                _piter = _model.iter_parent(_piter)
                _mechanism_id = _model.get_value(_piter, 1)

                (_results,
                 _error_code,
                 _last_id) = self.dtcPoF.add_method(self._hardware_id,
                                                    _mechanism_id, _load_id,
                                                    _id)

            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_row))
                except TypeError:
                    _path = None
                self.load_page(self._hardware_id, _path)

        elif index == 2:                    # Delete selected
            if _level == 1:                 # Failure mechanism
                (_results,
                 _error_code) = self.dtcPoF.delete_mechanism(self._hardware_id,
                                                             _id)

            elif _level == 2:               # Operating load
                _prow = _model.iter_parent(_row)
                _mechanism_id = _model.get_value(_prow, 1)

                (_results,
                 _error_code) = self.dtcPoF.delete_load(self._hardware_id,
                                                        _mechanism_id, _id)

            elif _level == 3:               # Operating stress
                _prow = _model.iter_parent(_row)
                _load_id = _model.get_value(_prow, 1)
                _prow = _model.iter_parent(_prow)
                _mechanism_id = _model.get_value(_prow, 1)

                (_results,
                 _error_code) = self.dtcPoF.delete_stress(self._hardware_id,
                                                          _mechanism_id,
                                                          _load_id, _id)

            elif _level == 4:               # Test method
                _prow = _model.iter_parent(_row)
                _stress_id = _model.get_value(_prow, 1)
                _prow = _model.iter_parent(_prow)
                _load_id = _model.get_value(_prow, 1)
                _prow = _model.iter_parent(_prow)
                _mechanism_id = _model.get_value(_prow, 1)

                (_results,
                 _error_code) = self.dtcPoF.delete_method(self._hardware_id,
                                                          _mechanism_id,
                                                          _load_id, _stress_id,
                                                          _id)

            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_row))
                except TypeError:
                    _path = None
                print _path
                self.load_page(self._hardware_id, _path)

        elif index == 3:                    # Save PoF
            self.dtcPoF.save_pof(self._hardware_id)

        return False

    def _on_cell_edit(self, cell, path, new_text, index):
        """
        Responds to edited signals from the PoF gtk.TreeView().

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that called this
                                      method.
        :param str path: the path of the selected gtk.TreeIter().
        :param str new_text: the new text in the gtk.CellRenderer() that called
                             this method.
        :param int index: the position of the gtk.CellRenderer() in the
                          gtk.TreeModel().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _pof = self.dtcPoF.dicPoF[self._hardware_id]

        (_model, _row) = self.tvwPoF.get_selection().get_selected()
        _id = _model.get_value(_row, 1)
        _level = _model.get_value(_row, 17)

        _convert = gobject.type_name(_model.get_column_type(index))

        if new_text is None:
            _model[path][index] = not cell.get_active()
        elif _convert == 'gchararray':
            _model[path][index] = str(new_text)
        elif _convert == 'gint':
            _model[path][index] = int(new_text)
        elif _convert == 'gfloat':
            _model[path][index] = float(new_text)

        if _level == 1:                 # Failure mechanism
            _mechanism = _pof.dicMechanisms[_id]

            if index == 2:              # Description
                _mechanism.description = new_text

        elif _level == 2:               # Operating load
            _prow = _model.iter_parent(_row)
            _mechanism_id = _model.get_value(_prow, 1)
            _mechanism = _pof.dicMechanisms[_mechanism_id]
            _load = _mechanism.dicLoads[_id]

            if index == 2:
                _load.description = new_text
            elif index == 3:
                _load.damage_model = [i[0] for i in self._lst_damage_models
                                      if i[1] == new_text][0]
            elif index == 4:
                _load.priority = [i[0] for i in self._lst_priority
                                  if i[1] == new_text][0]

        elif _level == 3:               # Operating stress
            _prow = _model.iter_parent(_row)
            _load_id = _model.get_value(_prow, 1)
            _prow = _model.iter_parent(_prow)
            _mechanism_id = _model.get_value(_prow, 1)
            _mechanism = _pof.dicMechanisms[_mechanism_id]
            _load = _mechanism.dicLoads[_load_id]
            _stress = _load.dicStresses[_id]

            if index == 2:
                _stress.description = new_text
            elif index == 5:
                _stress.measurable_parameter = [i[0] for i
                                                in self._lst_operating_parameters
                                                if i[1] == new_text][0]
            elif index == 6:
                _stress.load_history = [i[0] for i in self._lst_load_history
                                        if i[1] == new_text][0]
            elif index == 8:
                _stress.remarks = new_text

        elif _level == 4:               # Test method
            _prow = _model.iter_parent(_row)
            _stress_id = _model.get_value(_prow, 1)
            _prow = _model.iter_parent(_prow)
            _load_id = _model.get_value(_prow, 1)
            _prow = _model.iter_parent(_prow)
            _mechanism_id = _model.get_value(_prow, 1)
            _mechanism = _pof.dicMechanisms[_mechanism_id]
            _load = _mechanism.dicLoads[_load_id]
            _stress = _load.dicStresses[_stress_id]
            _method = _stress.dicMethods[_id]

            if index == 2:
                _method.description = new_text
            elif index == 7:
                _method.boundary_conditions = new_text
            elif index == 8:
                _method.remarks = new_text

        return False

    def _on_row_changed(self, treeview):
        """
        Callback function to handle events for the PoF package Work Book
        gtk.TreeView().  It is called whenever a PoF Work Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the PoF class gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = treeview.get_selection().get_selected()
        _level = _model.get_value(_row, 17)

        _column = treeview.get_column(1)
        _label = _column.get_widget()

        if _level == 1:                     # Failure mechanism.
            self.btnAddSibling.set_tooltip_text(_(u"Add a failure mechanism "
                                                  u"to the selected hardware "
                                                  u"item."))
            self.btnAddChild.set_tooltip_text(_(u"Add an operating load to "
                                                u"the selected failure "
                                                u"mechanism."))
            self.btnAddChild.set_sensitive(True)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected failure "
                                              u"mechanism from the selected "
                                              u"hardware item."))
            _label.set_markup("<span weight='bold'>Mechanism "
                              "Description</span>")
        elif _level == 2:                   # Operating load
            self.btnAddSibling.set_tooltip_text(_(u"Add an operating load "
                                                  u"to the selected failure "
                                                  u"mechanism."))
            self.btnAddChild.set_tooltip_text(_(u"Add an operating stress to "
                                                u"the selected operating "
                                                u"load."))
            self.btnAddChild.set_sensitive(True)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected operating "
                                              u"load from the selected "
                                              u"failure mechanism."))
            _label.set_markup("<span weight='bold'>Load Description</span>")
        elif _level == 3:                   # Operating stress
            self.btnAddSibling.set_tooltip_text(_(u"Add an operating stress "
                                                  u"to the selected operating "
                                                  u"load."))
            self.btnAddChild.set_tooltip_text(_(u"Add a test method to the "
                                                u"selected operating stress."))
            self.btnAddChild.set_sensitive(True)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected operating "
                                              u"stress from the selected "
                                              u"operating load."))
            _label.set_markup("<span weight='bold'>Stress Description</span>")
        elif _level == 4:                   # Test method
            self.btnAddSibling.set_tooltip_text(_(u"Add a potential test "
                                                  u"method to the selected "
                                                  u"operating stress."))
            self.btnAddChild.set_sensitive(False)
            self.btnRemove.set_tooltip_text(_(u"Remove the selected test "
                                              u"method from the selected "
                                              u"operating stress."))
            _label.set_markup("<span weight='bold'>Test Method "
                              "Description</span>")

        _column.set_widget(_label)

        return False
