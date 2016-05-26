#!/usr/bin/env python
"""
###############################
Function Package Work Book View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.function.WorkBook.py is part of The RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

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

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
from Assistants import AddFunction

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.VBox):
    """
    The Work Book view displays all the attributes for the selected Function.
    The attributes of a Work Book view are:

    :ivar _workview: the RTK top level Work View window to embed the Function
                     Work Book into.
    :ivar _function_model: the Function data model whose attributes are being
                           displayed.

    :ivar _dic_definitions: dictionary containing pointers to the failure
                            definitions for the Function being displayed.  Key
                            is the Failure Definition ID; value is the pointer
                            to the Failure Definition data model.

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Function attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |      0   | txtCode `focus_out_event`                 |
    +----------+-------------------------------------------+
    |      1   | txtName `focus_out_event`                 |
    +----------+-------------------------------------------+
    |      2   | txtRemarks `focus_out_event`              |
    +----------+-------------------------------------------+
    |      3   | Mission gtk.CellRendererCombo() `edited`  |
    +----------+-------------------------------------------+
    |      4   | Phase gtk.CellRendererCombo() `edited`    |
    +----------+-------------------------------------------+
    |      5   | btnAddMode `clicked`                      |
    +----------+-------------------------------------------+
    |      6   | btnRemoveMode `clicked`                   |
    +----------+-------------------------------------------+
    |      7   | btnSaveFMEA `clicked`                     |
    +----------+-------------------------------------------+

    :ivar dtcFunction: the :class:`rtk.function.Function.Function` data
                       controller to use with this Work Book.

    :ivar chkSafetyCritical: the :class:`gtk.CheckButton` to display/edit the
                             Function's safety criticality.

    :ivar txtCode: the :class:`gtk.Entry` to display/edit the Function code.
    :ivar txtName: the :class:`gtk.Entry` to display/edit the Function name.
    :ivar txtTotalCost: the :class:`gtk.Entry` to display the Function cost.
    :ivar txtModeCount: the :class:`gtk.Entry` to display the number of
                        hardware failure modes the Function is susceptible to.
    :ivar txtPartCount: the :class:`gtk.Entry` to display the number of
                        hardware components comprising the Function.
    :ivar txtRemarks: the :class:`gtk.Entry` to display/edit the Function
                      remarks.
    :ivar txtPredictedHt: the :class:`gtk.Entry` to display the Function
                          logistics hazard rate.
    :ivar txtMissionHt: the :class:`gtk.Entry` to display the Function mission
                        hazard rate.
    :ivar txtMTBF: the :class:`gtk.Entry` to display the Function logistics
                   MTBF.
    :ivar txtMissionMTBF: the :class:`gtk.Entry` to display the Function
                          mission MTBF.
    :ivar txtMPMT: the :class:`gtk.Entry` to display the Function mean
                   preventive maintenance time.
    :ivar txtMCMT: the :class:`gtk.Entry` to display the Function mean
                   corrective maintenance time.
    :ivar txtMTTR: the :class:`gtk.Entry` to display the Function mean time to
                   repair.
    :ivar txtMMT: the :class:`gtk.Entry` to display the Function mean
                  maintenance time.
    :ivar txtAvailability: the :class:`gtk.Entry` to display the Function
                           logistics availability.
    :ivar txtMissionAt: the :class:`gtk.Entry` to display the Function mission
                        availability.
    """

    def __init__(self, modulebook):
        """
        Initializes the Work Book view for the Revision package.

        :param modulebook: the :py:class:`rtk.function.ModuleBook` to associate
                           with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Define private dict attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._modulebook = modulebook
        self._function_model = None
        self._fmea_model = None
        self._profile_model = None

        # Define public dict attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.dtcFunction = modulebook.mdcRTK.dtcFunction
        self.dtcFMEA = modulebook.mdcRTK.dtcFMEA
        self.dtcMatrices = modulebook.mdcRTK.dtcMatrices

        # General data page widgets.
        self.chkSafetyCritical = Widgets.make_check_button(
            label=_(u"Function is safety critical."))
        self.txtCode = Widgets.make_entry()
        self.txtTotalCost = Widgets.make_entry(width=75, editable=False,
                                               bold=True)
        self.txtName = Widgets.make_text_view(width=400)
        self.txtModeCount = Widgets.make_entry(width=75, editable=False,
                                               bold=True)
        self.txtPartCount = Widgets.make_entry(width=75, editable=False,
                                               bold=True)
        self.txtRemarks = Widgets.make_text_view(width=400)

        # FMECA worksheet tab widgets.
        self.tvwFMECA = gtk.TreeView()
        self._FMECA_col_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.btnAddMode = Widgets.make_button(width=35, image='add')
        self.btnRemoveMode = Widgets.make_button(width=35, image='remove')
        self.btnSaveFMEA = Widgets.make_button(width=35, image='save')

        # Functional matrix tab widgets.
        self.chkParts = Widgets.make_check_button(label=_(u"Show components."))
        self.chkAssemblies = Widgets.make_check_button(label=_(u"Show "
                                                               u"assemblies."))
        self.tvwFunctionMatrix = gtk.TreeView()

        # Diagram tab widgets.

        # Assessment results tab widgets.
        self.txtPredictedHt = Widgets.make_entry(width=100, editable=False,
                                                 bold=True)
        self.txtMissionHt = Widgets.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtMTBF = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtMissionMTBF = Widgets.make_entry(width=100, editable=False,
                                                 bold=True)
        self.txtMPMT = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtMCMT = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtMTTR = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtMMT = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtAvailability = Widgets.make_entry(width=100, editable=False,
                                                  bold=True)
        self.txtMissionAt = Widgets.make_entry(width=100, editable=False,
                                               bold=True)

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Function class work book.
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add sibling function button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new function at the same "
                                   u"hierarchy level as the selected function "
                                   u"(i.e., a sibling function)."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR +
                             '32x32/insert_sibling.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_add_function, 0)
        _toolbar.insert(_button, _position)
        _position += 1

        # Add child function button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new function one level "
                                   u"subordinate to the selected function "
                                   u"(i.e., a child function)."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/insert_child.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_add_function, 1)
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete function button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Removes the currently selected "
                                   u"function."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_delete_function)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Calculate function button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Calculate the functions."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/calculate.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_calculate_function)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save function button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Saves changes to the selected function."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_save_functions)
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Function class gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_general_data_page(_notebook)
        self._create_fmea_page(_notebook)
        self._create_assessment_results_page(_notebook)

        return _notebook

    def _create_general_data_page(self, notebook):
        """
        Function to create the Function class gtk.Notebook() page for
        displaying general data about the selected Function.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                 gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"General Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information about   #
        # the function.                                                 #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u"Function Code:"), _(u"Function Name:")]
        (_max1, _y_pos1) = Widgets.make_labels(_labels, _fixed, 5, 5)

        _labels = [_(u"Total Cost:"), _(u"Total Mode Count:"),
                   _(u"Total Part Count:"), _(u"Remarks:")]
        _y_start = self.txtName.size_request()[1] + _y_pos1[1] + 5
        (_max2, _y_pos2) = Widgets.make_labels(_labels, _fixed, 5, _y_start)
        _x_pos = max(_max1, _max2) + 50

        # Set the tooltips.
        self.txtCode.set_tooltip_text(_(u"Enter a unique code for the "
                                        u"selected function."))
        self.txtName.set_tooltip_text(_(u"Enter the name of the selected "
                                        u"function."))
        self.txtTotalCost.set_tooltip_text(_(u"Displays the total cost of "
                                             u"the selected function."))
        self.txtModeCount.set_tooltip_text(_(u"Displays the total number "
                                             u"of failure modes "
                                             u"associated with the "
                                             u"selected function."))
        self.txtPartCount.set_tooltip_text(_(u"Displays the total number "
                                             u"of components associated "
                                             u"with the selected "
                                             u"function."))
        self.txtRemarks.set_tooltip_text(_(u"Enter any remarks related to "
                                           u"the selected function."))
        self.chkSafetyCritical.set_tooltip_text(_(u"Indicates whether or "
                                                  u"not the selected "
                                                  u"function is safety "
                                                  u"critical."))

        # Place the widgets.
        _fixed.put(self.txtCode, _x_pos, _y_pos1[0])
        _fixed.put(self.txtName, _x_pos, _y_pos1[1])
        _fixed.put(self.txtTotalCost, _x_pos, _y_pos2[0])
        _fixed.put(self.txtModeCount, _x_pos, _y_pos2[1])
        _fixed.put(self.txtPartCount, _x_pos, _y_pos2[2])
        _fixed.put(self.txtRemarks, _x_pos, _y_pos2[3])
        _fixed.put(self.chkSafetyCritical, 5, _y_pos2[3] + 110)

        # Connect to callback functions for editable gtk.Widgets().
        self._lst_handler_id.append(
            self.txtCode.connect('focus-out-event', self._on_focus_out, 4))
        _textview = self.txtName.get_child().get_child()
        self._lst_handler_id.append(
            _textview.connect('focus-out-event', self._on_focus_out, 14))
        _textview = self.txtRemarks.get_child().get_child()
        self._lst_handler_id.append(
            _textview.connect('focus-out-event', self._on_focus_out, 15))

        # Connect to callback functions for uneditable gtk.Widgets().
        self.txtTotalCost.connect('changed', self._on_changed, 5)
        self.txtModeCount.connect('changed', self._on_changed, 16)
        self.txtPartCount.connect('changed', self._on_changed, 17)

        _fixed.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"General\nData") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(_(u"Displays general information for the "
                                  u"selected function."))
        _label.show_all()
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_assessment_results_page(self, notebook):
        """
        Function to create the Function class gtk.Notebook() page for
        displaying assessment results for teh selected Function.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _hbox = gtk.HBox()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the left half of the page.                                    #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Reliability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        _labels = [_(u"Predicted h(t):"), _(u"Mission h(t):"), _(u"MTBF:"),
                   _(u"Mission MTBF:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 50

        self.txtPredictedHt.set_tooltip_text(_(u"Displays the predicted "
                                               u"failure intensity for "
                                               u"the selected function."))
        self.txtMissionHt.set_tooltip_text(_(u"Displays the mission "
                                             u"failure intensity for the "
                                             u"selected function."))
        self.txtMTBF.set_tooltip_text(_(u"Displays the limiting mean time "
                                        u"between failure (MTBF) for the "
                                        u"selected function."))
        self.txtMissionMTBF.set_tooltip_text(_(u"Displays the mission "
                                               u"mean time between "
                                               u"failure (MTBF) for the "
                                               u"selected function."))

        _fixed.put(self.txtPredictedHt, _x_pos, _y_pos[0])
        _fixed.put(self.txtMissionHt, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTBF, _x_pos, _y_pos[2])
        _fixed.put(self.txtMissionMTBF, _x_pos, _y_pos[3])

        # Connect to callback functions for uneditable gtk.Widgets().
        self.txtMissionHt.connect('changed', self._on_changed, 6)
        self.txtPredictedHt.connect('changed', self._on_changed, 7)
        self.txtMissionMTBF.connect('changed', self._on_changed, 11)
        self.txtMTBF.connect('changed', self._on_changed, 12)

        _fixed.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the right half of the page.                                   #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Maintainability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame)

        _labels = [_(u"MPMT:"), _(u"MCMT:"), _(u"MTTR:"), _(u"MMT:"),
                   _(u"Availability:"), _(u"Mission Availability:")]

        (_x_pos, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 50

        self.txtMPMT.set_tooltip_text(_(u"Displays the mean preventive "
                                        u"maintenance time (MPMT) for the "
                                        u"selected function."))
        self.txtMCMT.set_tooltip_text(_(u"Displays the mean corrective "
                                        u"maintenance time (MCMT) for the "
                                        u"selected function."))
        self.txtMTTR.set_tooltip_text(_(u"Displays the mean time to "
                                        u"repair (MTTR) for the selected "
                                        u"function."))
        self.txtMMT.set_tooltip_text(_(u"Displays the mean maintenance "
                                       u"time (MMT) for the selected "
                                       u"function."))
        self.txtAvailability.set_tooltip_text(_(u"Displays the limiting "
                                                u"availability for the "
                                                u"selected function."))
        self.txtMissionAt.set_tooltip_text(_(u"Displays the mission "
                                             u"availability for the "
                                             u"selected function."))

        _fixed.put(self.txtMPMT, _x_pos, _y_pos[0])
        _fixed.put(self.txtMCMT, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTTR, _x_pos, _y_pos[2])
        _fixed.put(self.txtMMT, _x_pos, _y_pos[3])
        _fixed.put(self.txtAvailability, _x_pos, _y_pos[4])
        _fixed.put(self.txtMissionAt, _x_pos, _y_pos[5])

        # Connect to callback functions for uneditable gtk.Widgets().
        self.txtAvailability.connect('changed', self._on_changed, 2)
        self.txtMissionAt.connect('changed', self._on_changed, 3)
        self.txtMMT.connect('changed', self._on_changed, 8)
        self.txtMCMT.connect('changed', self._on_changed, 9)
        self.txtMPMT.connect('changed', self._on_changed, 10)
        self.txtMTTR.connect('changed', self._on_changed, 13)

        _fixed.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Assessment\nResults") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(_(u"Displays reliability, maintainability, "
                                  u"and availability assessment results for "
                                  u"the selected function."))
        _label.show_all()
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_fmea_page(self, notebook):
        """
        Creates the FMECA gtk.Notebook() page and populates it with the
        appropriate widgets.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
# TODO: Consider re-writing _create_fmea_page; current McCabe metric = 10
        # Create the FMEA gtk.TreeView()
        self.tvwFMECA.set_tooltip_text(_(u"Displays the failure mode and "
                                         u"effects analysis for the currently "
                                         u"selected function."))
        _model = gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_STRING)
        self.tvwFMECA.set_model(_model)

        _headings = [_(u"Mode ID"), _(u"Mode\nDescription"),
                     _(u"Mission"), _(u"Mission Phase"), _(u"Local\nEffect"),
                     _(u"Next\nEffect"), _(u"End\nEffect"),
                     _(u"Design\nProvisions"), _(u"Operator\nActions"),
                     _(u"Severity\nClassification"), _(u"Critical\nFunction"),
                     _(u"Remarks")]

        for i in range(12):
            _column = gtk.TreeViewColumn()

            if i == 0:                      # Image, mode ID
                _cell = gtk.CellRendererPixbuf()
                _cell.set_property('xalign', 0.5)
                _column.pack_start(_cell, False)
                _column.set_attributes(_cell, pixbuf=0)

                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=1)

            elif i == 1:                    # Mode description
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_fmea_cell_edited, 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

            elif i == 2 or i == 3:          # Mission, mission phase
                _cell = gtk.CellRendererCombo()
                _cell.set_property('editable', 1)
                _cell.set_property('has-entry', False)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.1)
                self._lst_handler_id.append(
                    _cell.connect('edited', self._on_fmea_cell_edited, i + 1,
                                  _model))
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1)

            elif i > 3 and i < 9:           # Local, next, end effect, design provisions
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_fmea_cell_edited, i + 1,
                              _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1)

            elif i == 9:                    # Severity classification
                _cell = gtk.CellRendererCombo()
                _cell.set_property('editable', 1)
                _cell.set_property('has-entry', False)
                _cell.set_property('text-column', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_fmea_cell_edited, i + 1,
                              _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1)

            elif i == 10:                   # Critical function
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._on_fmea_cell_edited, -1,
                              i + 1, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=i + 1)

            elif i == 11:                   # Remarks
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_fmea_cell_edited, 12, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 1)

            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _headings[i] +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column.set_widget(_label)
            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

            self.tvwFMECA.append_column(_column)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwFMECA)

        _frame = Widgets.make_frame(label=_(u"Failure Mode and Effects "
                                            u"Analysis"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddMode, False, False)
        _bbox.pack_start(self.btnRemoveMode, False, False)
        _bbox.pack_start(self.btnSaveFMEA, False, False)

        # Connect to callback functions.
        self._lst_handler_id.append(
            self.btnAddMode.connect('clicked', self._on_button_clicked, 5))
        self._lst_handler_id.append(
            self.btnRemoveMode.connect('clicked', self._on_button_clicked, 6))
        self._lst_handler_id.append(
            self.btnSaveFMEA.connect('clicked', self._on_button_clicked, 7))

        # self._lst_handler_id.append(
        #     self.tvwMissionProfile.connect('cursor_changed',
        #                                    self._on_usage_row_changed))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display the functional FMECA.       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the severity classification gtk.CellRendererCombo().
        _column = self.tvwFMECA.get_column(9)
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        _cellmodel.append([""])
        _cell = _column.get_cell_renderers()[0]
        _cell.set_property('model', _cellmodel)
        for _severity in Configuration.RTK_SEVERITY:
            _cellmodel.append([_severity[2] + " - " + _severity[1]])

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"FMEA\nWorksheet") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(_(u"Failure mode and effects analysis (FMEA) "
                                  u"for the selected function."))
        _label.show_all()

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model, fmea_model, *args):
        """
        Method to load the Function class gtk.Notebook() widgets.

        :param model: the :py:class:`rtk.function.Function.Model` to be loaded.
        :param fmea_model: the :py:class:`rtk.analyses.FMEA.Model` to be
                           loaded.
        :param tuple args: any additional arguments to be passed to this
                           method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._function_model = model
        self._fmea_model = fmea_model
        self._profile_model = args[0]

        # Load the General Data page widgets.
        self._load_general_data_page()

        # Load the FMEA page.
        self._load_fmea_page()

        # Load the Assessment Results page.
        self._load_assessment_results_page()

        return False

    def _load_general_data_page(self):
        """
        Method to load the gtk.Widgets() on the General Data page with the
        values of the selected Function's attributes.

        :return: False
        :rtype: bool
        """

        # Load the editable gtk.Widgets().
        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(self._function_model.code))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        _textview = self.txtName.get_child().get_child()
        _textview.handler_block(self._lst_handler_id[1])
        _textbuffer = _textview.get_buffer()
        _textbuffer.set_text(self._function_model.name)
        _textview.handler_unblock(self._lst_handler_id[1])

        _textview = self.txtRemarks.get_child().get_child()
        _textview.handler_block(self._lst_handler_id[2])
        _textbuffer = _textview.get_buffer()
        _textbuffer.set_text(self._function_model.remarks)
        _textview.handler_unblock(self._lst_handler_id[2])

        # Load the non-editable gtk.Widgets().
        self.txtTotalCost.set_text(
            str(locale.currency(self._function_model.cost)))
        self.txtModeCount.set_text(
            str('{0:d}'.format(self._function_model.n_modes)))
        self.txtPartCount.set_text(
            str('{0:d}'.format(self._function_model.n_parts)))

        return False

    def _load_fmea_page(self, path=None):
        """
        Method to loads the functional FMEA gtk.TreeView().

        :keyword str path: the path in the gtk.TreeView() to select as active
                           after loading the FMEA.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Load the mission gtk.CellRendererCombo().
        _column = self.tvwFMECA.get_column(2)
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT)
        _cellmodel.append(["", -1])
        _cell = _column.get_cell_renderers()[0]
        _cell.set_property('model', _cellmodel)
        _cell.connect('changed', self._on_mission_combo_changed, _cellmodel)

        _missions = self._profile_model.dicMissions.values()
        for _mission in _missions:
            _cellmodel.append([_mission.description, _mission.mission_id])

        _model = self.tvwFMECA.get_model()
        _model.clear()
        for _mode in self._fmea_model.dicModes.values():
            _icon = Configuration.ICON_DIR + '32x32/mode.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _attributes = _mode.get_attributes()
            _data = (_icon, _attributes[2], _attributes[3], _attributes[4],
                     _attributes[5], _attributes[6], _attributes[7],
                     _attributes[8], _attributes[12], _attributes[13],
                     _attributes[14], _attributes[24], _attributes[26])
            _model.append(None, _data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                return False
        _column = self.tvwFMECA.get_column(0)
        self.tvwFMECA.set_cursor(path, None, False)
        self.tvwFMECA.row_activated(path, _column)
        self.tvwFMECA.expand_all()

        return False

    def _load_assessment_results_page(self):
        """
        Method to load the gtk.Widgets() on the Assessment Results page with
        the values of the selected Function's attributes.

        :return: False
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'g}'

        self.txtAvailability.set_text(
            str(fmt.format(self._function_model.availability)))
        self.txtMissionAt.set_text(
            str(fmt.format(self._function_model.mission_availability)))
        self.txtMissionHt.set_text(
            str(fmt.format(self._function_model.mission_hazard_rate)))
        self.txtPredictedHt.set_text(
            str(fmt.format(self._function_model.hazard_rate)))

        self.txtMMT.set_text(str(fmt.format(self._function_model.mmt)))
        self.txtMCMT.set_text(str(fmt.format(self._function_model.mcmt)))
        self.txtMPMT.set_text(str(fmt.format(self._function_model.mpmt)))

        self.txtMissionMTBF.set_text(
            str(fmt.format(self._function_model.mission_mtbf)))
        self.txtMTBF.set_text(str(fmt.format(self._function_model.mtbf)))
        self.txtMTTR.set_text(str(fmt.format(self._function_model.mttr)))

        return False

    def _on_button_clicked(self, button, index):
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _function_id = self._function_model.function_id

        (_model, _row) = self.tvwFMECA.get_selection().get_selected()

        button.handler_block(self._lst_handler_id[index])
        if index == 5:                      # Add a mode.
            (__, __,
             _mode_id) = self.dtcFMEA.add_mode(None, _function_id)
            _attributes = self._fmea_model.dicModes[_mode_id].get_attributes()
            _icon = Configuration.ICON_DIR + '32x32/mode.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = (_icon, _attributes[2], _attributes[3], _attributes[4],
                     _attributes[5], _attributes[6], _attributes[7],
                     _attributes[8], _attributes[12], _attributes[13],
                     _attributes[14], _attributes[24], _attributes[26])
            _model.append(None, _data)
        elif index == 6:                    # Delete a mode.
            _mode_id = _model.get_value(_row, 1)
            (_results, _error_code) = self.dtcFMEA.delete_mode(_mode_id, None,
                                                               _function_id)
            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_row))
                except TypeError:
                    _path = None
                self._load_fmea_page(_path)

        elif index == 7:                    # Save FMEA.
            self.dtcFMEA.save_fmea(None, _function_id)

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_changed(self, entry, index):
        """
        Callback method to retrieve uneditable gtk.Entry() changes and update
        the corresponding gtk.CellRenderer() in the Function Module Book.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param int index: the position in the Function class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        from re import sub
        from decimal import Decimal

        if index == 5:
            _text = entry.get_text()
            _text = Decimal(sub(r'[^\d.]', '', _text))
        elif index in [16, 17]:
            _text = int(entry.get_text())
        else:
            _text = float(entry.get_text())

        self._modulebook.update(index, _text)

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Callback method to retrieve editable gtk.Entry() changes, assign the
        new data to the appropriate Function data model attribute, and update
        the corresponding gtk.CellRenderer() in the Function Module Book.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the position in the Function class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if index == 4:
            _text = entry.get_text()
            self._function_model.code = _text
        elif index == 14:
            _textbuffer = self.txtName.get_child().get_child().get_buffer()
            _text = _textbuffer.get_text(*_textbuffer.get_bounds())
            self._function_model.name = _text
        elif index == 15:
            _textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
            _text = _textbuffer.get_text(*_textbuffer.get_bounds())
            self._function_model.remarks = _text

        self._modulebook.update(index, _text)

        return False

    def _on_fmea_cell_edited(self, cell, path, new_text, position, model):
        """
        Callback function to handle edits of the Function package Work Book
        FMEA gtk.Treeview()s.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _return = False

        _function_id = self._function_model.function_id

        _row = model.get_iter(path)
        _id = model.get_value(_row, 1)

        if position == 11:
            new_text = not cell.get_active()

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))
        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        _mode = self._fmea_model.dicModes[_id]
        _values = (_mode.assembly_id, _function_id, _id) + \
                  model.get(_row, 2, 3, 4, 5, 6, 7) + ('', '', '') + \
                  model.get(_row, 8, 9, 10) + \
                  ('', '', 1.0, 0.0, 0.0, 0.0, 0.0, 10, 10) + \
                  (model.get_value(_row, 11), 0, model.get_value(_row, 12))
        (_error_code, _error_msg) = _mode.set_attributes(_values)

        if _error_code != 0:
            _content = "rtk.function.WorkBook._on_fmea_cell_edited: " \
                       "Received error {0:s} while attempting to " \
                       "edit the FMEA for function {1:d}.".format(_error_msg,
                                                                  _function_id)
            self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"An error occurred while attempting to update the "
                        u"attributes of failure mode {0:d}.".format(_id))
            Utilities.rtk_error(_prompt)

            _return = True

        return _return

    def _on_mission_combo_changed(self, __combo, __path, new_iter, cellmodel):
        """
        Loads the Mission Phase gtk.CellRendererCombo() whenever a new Mission
        is selected in the FMEA.

        :param gtk.CellRendererCombo __combo: the gtk.CellRendererCombo() that
                                              called this method.
        :param str __path: the path identifying the edited cell relative to the
                           gtk.TreeView() the combo is part of.
        :param gtk.TreeIter new_iter: the gtk.TreeIter() that was just selected
                                      in the Mission gtk.CellRendererCombo()
                                      gtk.TreeModel().
        :param gtk.TreeModel cellmodel: the gtk.TreeModel() that is embedded in
                                        gtk.CellRendererCombo() that called
                                        this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve the list of Phase models associated with the newly selected
        # Mission.
        try:
            _mission_id = cellmodel.get_value(new_iter, 1)
        except TypeError:
            return True
        try:
            _mission = self._profile_model.dicMissions.values()[_mission_id]
        except IndexError:
            return True

        _phases = _mission.dicPhases.values()

        # Load the mission phase gtk.CellRendererCombo().
        _column = self.tvwFMECA.get_column(3)
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        _cellmodel.append([""])
        _cell = _column.get_cell_renderers()[0]
        _cell.set_property('model', _cellmodel)
        for _phase in _phases:
            _cellmodel.append([_phase.code])

        return False

    def _request_save_functions(self, __button):
        """
        Method to send a request to save all functions to the Function data
        controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_codes = self.dtcFunction.save_all_functions()
        _error_codes = [_code for _code in _error_codes if _code[1] != 0]

        if len(_error_codes) > 0:
            for __, _code in enumerate(_error_codes):
                _content = "rtk.function.WorkBook._request_save_functions: " \
                           "Received error code {1:d} while saving " \
                           "function {0:d}.".format(_code[0], _code[1])
                self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"An error occurred while saving one or more "
                        u"function.")
            Utilities.rtk_error(_prompt)

            _return = True

        return _return

    def _request_add_function(self, __button, level):
        """
        Method to send a request to add a new function to the Function data
        controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _revision_id = self._function_model.revision_id
        if level == 0:
            _parent_id = self._function_model.parent_id
        else:
            _parent_id = self._function_model.function_id

        # Launch the Add Function gtk.Assistant().
        AddFunction(self._modulebook, level, _revision_id, _parent_id)

        self._modulebook.request_load_data()

        return False

    def _request_delete_function(self, __button):
        """
        Method to send a request to delete the selected function from the
        Function data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False
        _function_id = self._function_model.function_id
        _revision_id = self._function_model.revision_id

        (_results,
         _error_codes) = self.dtcFunction.delete_function(_function_id)

        if sum(_error_codes) != 0:
            _content = "rtk.function.WorkBook._request_delete_function: " \
                       "Received error codes [{1:d}, {2:d}] while " \
                       "attempting to delete " \
                       "function {0:d}.".format(_function_id, _error_codes[0],
                                                _error_codes[1])
            self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"An error occurred while attempting to delete "
                        u"function {0:s}.".format(self._function_model.name))
            Utilities.rtk_error(_prompt)

            _return = True

        else:
            # Remove the function from the functional FMEA.
            self.dtcFMEA.dicFFMEA.pop(_function_id)

            # Remove the Function from the functional Matrices.
            for _matrix_id, _matrix in self.dtcMatrices.dicMatrices.items():
                _row_ids = [_key for _key, _vals in _matrix.dicRows.items()
                            if _vals[0] == _function_id or
                            _vals[1] == _function_id]
                _row_ids = sorted(_row_ids, reverse=True)

                for _row_id in _row_ids:
                    self.dtcMatrices.delete_row(_matrix_id, _row_id)

            # Refresh Module Book view.
            self._modulebook.request_load_data(
                self._modulebook.mdcRTK.project_dao, _revision_id)

        return _return

    def _request_calculate_function(self, __button):
        """
        Method to send a request to calculate all of the Functions to the
        Function data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_codes = self.dtcFunction.calculate_function(Configuration.RTK_MTIME)
        _error_codes = [_code for _code in _error_codes if _code[1] != 0]

        if len(_error_codes) == 0:
            self._load_general_data_page()
            self._load_assessment_results_page()
        else:
            for __, _code in enumerate(_error_codes):
                _content = "rtk.function.WorkBook._request_calculate_functions: " \
                           "Received error code {1:d} while calculating " \
                           "function {0:d}.".format(_code[0], _code[1])
                self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"An error occurred while attempting to calculate "
                        u"functions.")
            Utilities.rtk_error(_prompt)

            _return = True

        return _return
