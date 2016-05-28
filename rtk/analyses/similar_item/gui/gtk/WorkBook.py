#!/usr/bin/env python
"""
############################################
Similiar Item Analysis Module Work Book View
############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.similiar_item.gui.gtk.WorkBook.py is part of The RTK
#       Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
from lxml import etree
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

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.HBox):                   # pylint: disable=R0902
    """
    The Work Book view displays all the attributes for the selected Similar
    Item Analysis.  The attributes of a Similar Item Analysis Work Book view
    are:

    :ivar list _lst_handler_id: default value: []
    :ivar :py:class:`rtk.analyses.similar_item.SimilarItem.SimilarItem` dtcSimilarItem:
        the Similar Item Analysis data controller.
    :ivar gtk.Button btnEditFunction: the gtk.Button() to launch the function
                                      editor.
    :ivar gtk.Button btnCalculate: the gtk.Button() to calculate the Similar
                                   Item Analysis.
    :ivar gtk.Button btnSave: the gtk.Button() to save the Similar Item
                              Analysis.
    :ivar gtk.ComboBox cmbSimilarItemMethod: the gtk.ComboBox() to select the
                                             the Similar Item Analysis method.
    :ivar gtk.ComboBox cmbFromQuality: the gtk.ComboBox() to select the
                                       surrogate system's quality.
    :ivar gtk.ComboBox cmbToQuality: the gtk.ComboBox() to select the new
                                     system's quality.
    :ivar gtk.ComboBox cmbFromEnvironment: the gtk.ComboBox() to select the
                                           surrogate system's operating
                                           environment.
    :ivar gtk.ComboBox cmbToEnvironment: the gtk.ComboBox() to select the new
                                         system's operating environment.
    :ivar gtk.TreeView tvwSimilarItem: the gtk.TreeView() that displays the
                                       Similar Item Analysis.
    :ivar gtk.Entry txtFromTemperature: the gtk.Entry() to enter the
                                        surrogate system's ambient temperature.
    :ivar gtk.Entry txtToTemperature: the gtk.Entry() to enter the new system's
                                      ambient temperature.
    """

    def __init__(self, controller, modulebook):
        """
        Method to initialize the Work Book view for the Similar Item Analysis
        module.

        :param controller: the :py:class`rtk.analyses.similar_item.SimilarItem.SimilarItem`
                           data controller.
        :param modulebook: the :py:class:`rtk.hardware.ModuleBook` associated
                           with the Hazard.
        """

        gtk.HBox.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._modulebook = modulebook

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.dtcSimilarItem = controller

        self.btnEditFunction = Widgets.make_button(width=35, image='edit')
        self.btnCalculate = Widgets.make_button(width=35, image='calculate')
        self.btnSave = Widgets.make_button(width=35, image='save')

        self.cmbSimilarItemMethod = Widgets.make_combo(width=150)
        self.cmbFromQuality = Widgets.make_combo(width=150)
        self.cmbToQuality = Widgets.make_combo(width=150)
        self.cmbFromEnvironment = Widgets.make_combo(width=150)
        self.cmbToEnvironment = Widgets.make_combo(width=150)

        self.txtFromTemperature = Widgets.make_entry(width=100)
        self.txtToTemperature = Widgets.make_entry(width=100)

        self.tvwSimilarItem = gtk.TreeView()

        # Set tooltips for gtk.Widgets().
        self.btnEditFunction.set_tooltip_text(_(u"Edit the user-defined "
                                                u"similar item analyses."))
        self.btnCalculate.set_tooltip_text(_(u"Calculates the similar item "
                                             u"analysis for the selected "
                                             u"hardware item."))
        self.btnSave.set_tooltip_text(_(u"Saves the selected similiar item "
                                        u"analysis."))
        self.cmbSimilarItemMethod.set_tooltip_text(_(u"Selects the method for "
                                                     u"determining the "
                                                     u"reliability of the new "
                                                     u"design based on the "
                                                     u"reliability of a "
                                                     u"similar item."))
        self.cmbFromQuality.set_tooltip_text(_(u"Selects the quality level of "
                                               u"the baseline, similar item."))
        self.cmbToQuality.set_tooltip_text(_(u"Selects the quality level of "
                                             u"the new design."))
        self.cmbFromEnvironment.set_tooltip_text(_(u"Selects the environment "
                                                   u"category of the "
                                                   u"baseline, similar item."))
        self.cmbToEnvironment.set_tooltip_text(_(u"Selects the environment "
                                                 u"category of the new "
                                                 u"design."))
        self.tvwSimilarItem.set_tooltip_text(_(u"Displays the similar items "
                                               u"analysis for the selected "
                                               u"assembly."))
        self.txtFromTemperature.set_tooltip_text(_(u"Selects the operating, "
                                                   u"ambient temperature of "
                                                   u"the baseline, similar "
                                                   u"item."))
        self.txtToTemperature.set_tooltip_text(_(u"Selects the operating, "
                                                 u"ambient temperature of "
                                                 u"the new design."))

        # Connect to callback functions.
        self._lst_handler_id.append(
            self.btnEditFunction.connect('clicked',
                                         self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnCalculate.connect('clicked', self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnSave.connect('clicked', self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.cmbSimilarItemMethod.connect('changed',
                                              self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbFromQuality.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbToQuality.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbFromEnvironment.connect('changed',
                                            self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.cmbToEnvironment.connect('changed',
                                          self._on_combo_changed, 7))
        self._lst_handler_id.append(
            self.txtFromTemperature.connect('focus-out-event',
                                            self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtToTemperature.connect('focus-out-event',
                                          self._on_focus_out, 9))

        self.show_all()

    def create_page(self):                  # pylint: disable=R0914
        """
        Method to create the Similar Item analysis gtk.Notebook() page for
        displaying the similar item analysis for the selected Hardware.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the Similar Item Analysis gtk.TreeView().              #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _path = "/root/tree[@name='SIA']/column/usertitle"
        _heading = etree.parse(Configuration.RTK_FORMAT_FILE[8]).xpath(_path)

        _path = "/root/tree[@name='SIA']/column/datatype"
        _datatype = etree.parse(Configuration.RTK_FORMAT_FILE[8]).xpath(_path)

        _path = "/root/tree[@name='SIA']/column/widget"
        _widget = etree.parse(Configuration.RTK_FORMAT_FILE[8]).xpath(_path)

        _path = "/root/tree[@name='SIA']/column/position"
        _position = etree.parse(Configuration.RTK_FORMAT_FILE[8]).xpath(_path)

        _path = "/root/tree[@name='SIA']/column/editable"
        _editable = etree.parse(Configuration.RTK_FORMAT_FILE[8]).xpath(_path)

        _path = "/root/tree[@name='SIA']/column/visible"
        _visible = etree.parse(Configuration.RTK_FORMAT_FILE[8]).xpath(_path)

        # Create a list of GObject datatypes to pass to the model.
        _types = []
        for i in range(len(_position)):
            _types.append(_datatype[i].text)

        _gobject_types = []
        _gobject_types = [gobject.type_from_name(_types[i])
                          for i in range(len(_types))]

        # Create the model and treeview.
        _model = gtk.TreeStore(*_gobject_types)
        self.tvwSimilarItem.set_model(_model)

        _columns = int(len(_heading))
        for i in range(_columns):
            _column = gtk.TreeViewColumn()

            # self._col_order.append(int(_position_[i].text))

            if _widget[i].text == 'spin':
                _cell = gtk.CellRendererSpin()
                _adjustment = gtk.Adjustment(upper=5.0, step_incr=0.05)
                _cell.set_property('adjustment', _adjustment)
                _cell.set_property('digits', 2)
            else:
                _cell = gtk.CellRendererText()

            _cell.set_property('editable', int(_editable[i].text))

            if int(_editable[i].text) == 0:
                _cell.set_property('background', 'light gray')
            else:
                _cell.set_property('background', Configuration.RTK_COLORS[6])
                _cell.set_property('foreground', Configuration.RTK_COLORS[7])
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD)
                _cell.connect('edited', self._on_cell_edit,
                              int(_position[i].text))

            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" +
                              _heading[i].text.replace("  ", "\n") + "</span>")
            _label.set_use_markup(True)
            _label.show_all()

            _column.set_visible(int(_visible[i].text))
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=int(_position[i].text))
            _column.set_widget(_label)
            _column.set_cell_data_func(_cell, Widgets.format_cell,
                                       (int(_position[i].text),
                                        _datatype[i].text))
            _column.set_resizable(True)
            _column.connect('notify::width', Widgets.resize_wrap, _cell)

            if i > 0:
                _column.set_reorderable(True)

            self.tvwSimilarItem.append_column(_column)

        self.tvwSimilarItem.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

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
        _scrollwindow.add(self.tvwSimilarItem)

        _frame = Widgets.make_frame(label=_(u"Similar Item Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnEditFunction, False, False)
        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_start(self.btnSave, False, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the similar item analysis.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.Combo()
        _results = [[_(u"Topic 6.3.3"), 0],
                    [_(u"User-Defined"), 1]]

        Widgets.load_combo(self.cmbSimilarItemMethod, _results)

        _results = [[_(u"Space"), 0],
                    [_(u"Full Military"), 1],
                    [_(u"Ruggedized"), 2],
                    [_(u"Commercial"), 3]]

        Widgets.load_combo(self.cmbFromQuality, _results)
        Widgets.load_combo(self.cmbToQuality, _results)

        _results = [[_(u"Ground, Benign"), 0], [_(u"Ground, Mobile"), 1],
                    [_(u"Naval, Sheltered"), 2],
                    [_(u"Airborne, Inhabited, Cargo"), 3],
                    [_(u"Airborne, Rotary Wing"), 4], [_(u"Space, Flight"), 5]]

        Widgets.load_combo(self.cmbFromEnvironment, _results)
        Widgets.load_combo(self.cmbToEnvironment, _results)

        _labels = [_(u"Similar Item Method:"), _(u"From Quality:"),
                   _(u"To Quality:"), _(u"From Environment:"),
                   _(u"To Environment:"), _(u"From Temperature:"),
                   _("To Temperature:")]

        _x_pos = 5
        _label = Widgets.make_label(_labels[0], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _x_pos = _x_pos + _label.size_request()[0] + 25
        _fixed.put(self.cmbSimilarItemMethod, _x_pos, 5)

        _x_pos = 350

        _label = Widgets.make_label(_labels[1], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _width = _label.size_request()[0]
        _label = Widgets.make_label(_labels[3], width=-1)
        _fixed.put(_label, _x_pos, 40)
        _width = max(_width, _label.size_request()[0])
        _label = Widgets.make_label(_labels[5], width=-1)
        _fixed.put(_label, _x_pos, 75)
        _width = max(_width, _label.size_request()[0])
        _x_pos = _x_pos + _width + 25
        _fixed.put(self.cmbFromQuality, _x_pos, 5)
        _fixed.put(self.cmbFromEnvironment, _x_pos, 40)
        _fixed.put(self.txtFromTemperature, _x_pos, 75)

        _x_pos = 650

        _label = Widgets.make_label(_labels[2], width=-1)
        _fixed.put(_label, _x_pos, 5)
        _width = _label.size_request()[0]
        _label = Widgets.make_label(_labels[4], width=-1)
        _fixed.put(_label, _x_pos, 40)
        _width = max(_width, _label.size_request()[0])
        _label = Widgets.make_label(_labels[6], width=-1)
        _fixed.put(_label, _x_pos, 75)
        _width = max(_width, _label.size_request()[0])
        _x_pos = _x_pos + _width + 25
        _fixed.put(self.cmbToQuality, _x_pos, 5)
        _fixed.put(self.cmbToEnvironment, _x_pos, 40)
        _fixed.put(self.txtToTemperature, _x_pos, 75)

        return False

    def load_page(self, controller, hardware_id, path=None):
        """
        Method to load the widgets on the Similar Item Analysis page.

        :param `rtk.hardware.Hardware.Hardware` controller: the Hardware data
                                                            controller instance
                                                            being used by RTK.
        :param int hardware_id: the Hardware ID to load the Similar Item
                                Analysis for.
        :keyword str path: the path of the parent hardware item in the Similar
                           Item Analysis gtk.TreeView().
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        _model = self.tvwSimilarItem.get_model()
        _model.clear()

        # Find all the similar items for the selected Hardware Item.
        _similar_items = [self.dtcSimilarItem.dicSimilarItem[_a]
                          for _a in self.dtcSimilarItem.dicSimilarItem.keys()
                          if self.dtcSimilarItem.dicSimilarItem[_a].parent_id == hardware_id]

        parent_row = None
        for _similar_item in _similar_items:
            _hardware = controller.dicHardware[_similar_item.hardware_id]
            _hazard_rate = _hardware.hazard_rate_logistics
            _name = _hardware.name
            _data = [_similar_item.hardware_id, _similar_item.sia_id, _name,
                     _hazard_rate, _similar_item.from_quality,
                     _similar_item.to_quality, _similar_item.from_environment,
                     _similar_item.to_environment,
                     _similar_item.from_temperature,
                     _similar_item.to_temperature, _similar_item.change_desc_1,
                     _similar_item.change_factor_1,
                     _similar_item.change_desc_2,
                     _similar_item.change_factor_2,
                     _similar_item.change_desc_3,
                     _similar_item.change_factor_3,
                     _similar_item.change_desc_4,
                     _similar_item.change_factor_4,
                     _similar_item.change_desc_5,
                     _similar_item.change_factor_5,
                     _similar_item.change_desc_6,
                     _similar_item.change_factor_6,
                     _similar_item.change_desc_7,
                     _similar_item.change_factor_7,
                     _similar_item.change_desc_8,
                     _similar_item.change_factor_8,
                     _similar_item.change_desc_9,
                     _similar_item.change_factor_9,
                     _similar_item.change_desc_10,
                     _similar_item.change_factor_10,
                     _similar_item.function_1, _similar_item.function_2,
                     _similar_item.function_3, _similar_item.function_4,
                     _similar_item.function_5, _similar_item.result_1,
                     _similar_item.result_2, _similar_item.result_3,
                     _similar_item.result_4, _similar_item.result_5,
                     _similar_item.user_blob_1, _similar_item.user_blob_2,
                     _similar_item.user_blob_3, _similar_item.user_blob_4,
                     _similar_item.user_blob_5, _similar_item.user_float_1,
                     _similar_item.user_float_2, _similar_item.user_float_3,
                     _similar_item.user_float_4, _similar_item.user_float_5,
                     _similar_item.user_int_1, _similar_item.user_int_2,
                     _similar_item.user_int_3, _similar_item.user_int_4,
                     _similar_item.user_int_5, _similar_item.parent_id]
            _model.append(parent_row, _data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                return False
        _column = self.tvwSimilarItem.get_column(0)
        self.tvwSimilarItem.set_cursor(path, None, False)
        self.tvwSimilarItem.row_activated(path, _column)
        self.tvwSimilarItem.expand_all()

        self.cmbSimilarItemMethod.set_active(_similar_items[0].method)
        self.cmbFromQuality.set_active(_similar_items[0].from_quality)
        self.cmbToQuality.set_active(_similar_items[0].to_quality)
        self.cmbFromEnvironment.set_active(_similar_items[0].from_environment)
        self.cmbToEnvironment.set_active(_similar_items[0].to_environment)
        self.txtFromTemperature.set_text(
            str('{0:0.0f}'.format(_similar_items[0].from_temperature)))
        self.txtToTemperature.set_text(
            str('{0:0.0f}'.format(_similar_items[0].to_temperature)))

        return False

    def _edit_function(self):
        """
        Method to edit the Similar Item Analysis functions.

        :returns: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.tvwSimilarItem.get_selection().get_selected()

        _title = _(u"RTK - Edit Similar Item Analysis Functions")
        _label = Widgets.make_label(_(u"You can define up to five functions.  "
                                      u"You can use the system failure rate, "
                                      u"selected assembly failure rate, the "
                                      u"change factor, the user float, the "
                                      u"user integer values, and results of "
                                      u"other functions.\n\n \
        System hazard rate is hr_sys\n \
        Assembly hazard rate is hr\n \
        Change factor is pi[1-8]\n \
        User float is uf[1-3]\n \
        User integer is ui[1-3]\n \
        Function result is res[1-5]"), width=600, height=-1, wrap=True)
        _label2 = Widgets.make_label(_(u"For example, pi1*pi2+pi3, multiplies "
                                       u"the first two change factors and "
                                       u"adds the value to the third change "
                                       u"factor."),
                                     width=600, height=-1, wrap=True)

        # Build the dialog assistant.
        _dialog = Widgets.make_dialog(_title)

        _fixed = gtk.Fixed()

        _y_pos = 10
        _fixed.put(_label, 5, _y_pos)
        _y_pos += _label.size_request()[1] + 10
        _fixed.put(_label2, 5, _y_pos)
        _y_pos += _label2.size_request()[1] + 10

        _label = Widgets.make_label(_(u"User function 1:"))
        _txtFunction1 = Widgets.make_entry()
        _txtFunction1.set_text(_model.get_value(_row, 30))

        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction1, 195, _y_pos)
        _y_pos += 30

        _label = Widgets.make_label(_(u"User function 2:"))
        _txtFunction2 = Widgets.make_entry()
        _txtFunction2.set_text(_model.get_value(_row, 31))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction2, 195, _y_pos)
        _y_pos += 30

        _label = Widgets.make_label(_(u"User function 3:"))
        _txtFunction3 = Widgets.make_entry()
        _txtFunction3.set_text(_model.get_value(_row, 32))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction3, 195, _y_pos)
        _y_pos += 30

        _label = Widgets.make_label(_(u"User function 4:"))
        _txtFunction4 = Widgets.make_entry()
        _txtFunction4.set_text(_model.get_value(_row, 33))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction4, 195, _y_pos)
        _y_pos += 30

        _label = Widgets.make_label(_(u"User function 5:"))
        _txtFunction5 = Widgets.make_entry()
        _txtFunction5.set_text(_model.get_value(_row, 34))
        _fixed.put(_label, 5, _y_pos)
        _fixed.put(_txtFunction5, 195, _y_pos)
        _y_pos += 30

        _chkApplyAll = gtk.CheckButton(label=_(u"Apply to all assemblies."))
        _fixed.put(_chkApplyAll, 5, _y_pos)

        _fixed.show_all()

        _dialog.vbox.pack_start(_fixed)     # pylint: disable=E1101

        # Run the dialog and apply the changes if the 'OK' button is pressed.
        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            # Widgets.set_cursor(self._app, gtk.gdk.WATCH)

            if _chkApplyAll.get_active():
                _row = _model.get_iter_root()
                while _row is not None:
                    _hardware_id = _model.get_value(_row, 0)
                    _similar_item = self.dtcSimilarItem.dicSimilarItem[_hardware_id]
                    _similar_item.function_1 = _txtFunction1.get_text()
                    _similar_item.function_2 = _txtFunction2.get_text()
                    _similar_item.function_3 = _txtFunction3.get_text()
                    _similar_item.function_4 = _txtFunction4.get_text()
                    _similar_item.function_5 = _txtFunction5.get_text()
                    _model.set_value(_row, 30, _similar_item.function_1)
                    _model.set_value(_row, 31, _similar_item.function_2)
                    _model.set_value(_row, 32, _similar_item.function_3)
                    _model.set_value(_row, 33, _similar_item.function_4)
                    _model.set_value(_row, 34, _similar_item.function_5)
                    _row = _model.iter_next(_row)
            else:
                _hardware_id = _model.get_value(_row, 0)
                _similar_item = self.dtcSimilarItem.dicSimilarItem[_hardware_id]
                _similar_item.function_1 = _txtFunction1.get_text()
                _similar_item.function_2 = _txtFunction2.get_text()
                _similar_item.function_3 = _txtFunction3.get_text()
                _similar_item.function_4 = _txtFunction4.get_text()
                _similar_item.function_5 = _txtFunction5.get_text()
                _model.set_value(_row, 30, _similar_item.function_1)
                _model.set_value(_row, 31, _similar_item.function_2)
                _model.set_value(_row, 32, _similar_item.function_3)
                _model.set_value(_row, 33, _similar_item.function_4)
                _model.set_value(_row, 34, _similar_item.function_5)

            # Widgets.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        _dialog.destroy()

        return False

    def _on_button_clicked(self, __button, index):
        """
        Method to respond to gtk.Button() 'clicked' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if index == 0:                      # Edit functions.
            self._edit_function()
        elif index == 1:                    # Calculate the analysis.
            _model = self.tvwSimilarItem.get_model()
            _row = _model.get_iter_root()

            # Retrieve the method of the parent Hardware Item.
            _hardware_id = _model.get_value(_row, 0)
            _similar_item = self.dtcSimilarItem.dicSimilarItem[_hardware_id]
            _method = _similar_item.method
            while _row is not None:
                _hardware_id = _model.get_value(_row, 0)
                _hazard_rate = _model.get_value(_row, 3)
                self.dtcSimilarItem.calculate(_hardware_id, _hazard_rate,
                                              _method)
                _similar_item = self.dtcSimilarItem.dicSimilarItem[_hardware_id]
                _model.set_value(_row, 35, _similar_item.result_1)
                _model.set_value(_row, 36, _similar_item.result_2)
                _model.set_value(_row, 37, _similar_item.result_3)
                _model.set_value(_row, 38, _similar_item.result_4)
                _model.set_value(_row, 39, _similar_item.result_5)
                _row = _model.iter_next(_row)
        elif index == 2:                    # Save the analysis.
            _error_codes = self.dtcSimilarItem.save_all_similar_item()
            _error_codes = [_code for _code in _error_codes if _code[1] != 0]

            if len(_error_codes) != 0:
                for __, _code in enumerate(_error_codes):
                    _content = "rtk.analyses.similar_item.gui.gtk.WorkBook._on_button_clicked: " \
                               "Received error code {1:d} while saving " \
                               "Similar Item for Hardware item " \
                               "{0:d}.".format(_code[0], _code[1])
                    self._modulebook.mdcRTK.debug_log.error(_content)

                _prompt = _(u"One or more errors occurred while attempting to "
                            u"save Similar Item Analysis.")
                Widgets.rtk_error(_prompt)

                _return = True

        return _return

    def _on_cell_edit(self, cell, path, new_text, index):   # pylint: disable=R0912
        """
        Method to respond to gtk.CellRenderer() 'edited' signals from the
        Similar Item gtk.TreeView().

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
# TODO: Re-write _on_cell_edit; current McCabe Complexity metric = 40.
        (_model, _row) = self.tvwSimilarItem.get_selection().get_selected()
        _hardware_id = _model.get_value(_row, 0)
        _similar_item = self.dtcSimilarItem.dicSimilarItem[_hardware_id]

        _convert = gobject.type_name(_model.get_column_type(index))

        if new_text is None:
            _model[path][index] = not cell.get_active()
        elif _convert == 'gchararray':
            _model[path][index] = str(new_text)
        elif _convert == 'gint':
            _model[path][index] = int(new_text)
        elif _convert == 'gfloat':
            _model[path][index] = float(new_text)

        if index == 10:
            _similar_item.change_desc_1 = new_text
        elif index == 11:
            _similar_item.change_factor_1 = float(new_text)
        elif index == 12:
            _similar_item.change_desc_2 = new_text
        elif index == 13:
            _similar_item.change_factor_2 = float(new_text)
        elif index == 14:
            _similar_item.change_desc_3 = new_text
        elif index == 15:
            _similar_item.change_factor_3 = float(new_text)
        elif index == 16:
            _similar_item.change_desc_4 = new_text
        elif index == 17:
            _similar_item.change_factor_4 = float(new_text)
        elif index == 18:
            _similar_item.change_desc_5 = new_text
        elif index == 19:
            _similar_item.change_factor_5 = float(new_text)
        elif index == 20:
            _similar_item.change_desc_6 = new_text
        elif index == 21:
            _similar_item.change_factor_6 = float(new_text)
        elif index == 22:
            _similar_item.change_desc_7 = new_text
        elif index == 23:
            _similar_item.change_factor_7 = float(new_text)
        elif index == 24:
            _similar_item.change_desc_8 = new_text
        elif index == 25:
            _similar_item.change_factor_8 = float(new_text)
        elif index == 26:
            _similar_item.change_desc_9 = new_text
        elif index == 27:
            _similar_item.change_factor_9 = float(new_text)
        elif index == 28:
            _similar_item.change_desc_10 = new_text
        elif index == 29:
            _similar_item.change_factor_10 = float(new_text)
        elif index == 40:
            _similar_item.user_blob_1 = new_text
        elif index == 41:
            _similar_item.user_blob_2 = new_text
        elif index == 42:
            _similar_item.user_blob_3 = new_text
        elif index == 43:
            _similar_item.user_blob_4 = new_text
        elif index == 44:
            _similar_item.user_blob_5 = new_text
        elif index == 45:
            _similar_item.user_float_1 = float(new_text)
        elif index == 46:
            _similar_item.user_float_2 = float(new_text)
        elif index == 47:
            _similar_item.user_float_3 = float(new_text)
        elif index == 48:
            _similar_item.user_float_4 = float(new_text)
        elif index == 49:
            _similar_item.user_float_5 = float(new_text)
        elif index == 50:
            _similar_item.user_int_1 = int(new_text)
        elif index == 51:
            _similar_item.user_int_2 = int(new_text)
        elif index == 52:
            _similar_item.user_int_3 = int(new_text)
        elif index == 53:
            _similar_item.user_int_4 = int(new_text)
        elif index == 54:
            _similar_item.user_int_5 = int(new_text)

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() 'changed' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.tvwSimilarItem.get_selection().get_selected()
        _hardware_id = _model.get_value(_row, 0)

        _similar_item = self.dtcSimilarItem.dicSimilarItem[_hardware_id]

        combo.handler_block(self._lst_handler_id[index])

        if index == 3:                      # SIA method
            _similar_item.method = combo.get_active()
        elif index == 4:                    # From quality
            _similar_item.from_quality = combo.get_active()
        elif index == 5:                    # To quality.
            _similar_item.to_quality = combo.get_active()
        elif index == 6:                    # From environment.
            _similar_item.from_environment = combo.get_active()
        elif index == 7:                    # To environment.
            _similar_item.to_environment = combo.get_active()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Method to respond to gtk.Entry() 'focus_out' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.tvwSimilarItem.get_selection().get_selected()
        _hardware_id = _model.get_value(_row, 0)

        _similar_item = self.dtcSimilarItem.dicSimilarItem[_hardware_id]

        entry.handler_block(self._lst_handler_id[index])

        if index == 8:                      # From temperature.
            _similar_item.from_temperature = float(entry.get_text())
        elif index == 9:                    # To temperature.
            _similar_item.to_temperature = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False
