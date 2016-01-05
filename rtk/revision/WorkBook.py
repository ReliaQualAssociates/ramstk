#!/usr/bin/env python
"""
###############################
Revision Package Work Book View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.revision.WorkBook.py is part of The RTK Project
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
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg
from Assistants import AddRevision

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.VBox):
    """
    The Work Book view displays all the attributes for the selected Revision.
    The attributes of a Work Book view are:

    :ivar _workview: the RTK top level Work View window to embed the Revision
                     Work Book into.
    :ivar _revision_model: the Revision data model whose attributes are being
                           displayed.
    :ivar _usage_model: the Usage Profile data model whose attributes are being
                        displayed.

    :ivar _dic_definitions: dictionary containing pointers to the failure
                            definitions for the Revision being displayed.  Key
                            is the Failure Definition ID; value is the pointer
                            to the Failure Definition data model.

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Revision attribute.

    :ivar dtcRevision: the :class:`rtk.revision.Revision.Revision` data
                       controller to use with this Work Book.
    :ivar dtcProfile: the :class:`rtk.usage.UsageProfile.UsageProfile` data
                       controller to use with this Work Book.
    :ivar dtcDefinitions: the :class:`rtk.failure_definition.Controller` data
                       controller to use with this Work Book.

    :ivar btnAddSibling: the :class`gtk.Button` to add a new item to the Usage
                         Profile at the same level as the selected item.
    :ivar btnAddChild: the :class`gtk.Button` to add a new item to the Usage
                       Profile one level below the selected item.
    :ivar btnRemoveUsage: the :class`gtk.Button` to remove the selected item
                          and any child items from the Usage Profile.
    :ivar btnSaveUsage: the :class`gtk.Button` to save the Usage Profile to the
                        RTK Project database.
    :ivar btnAddDefinition: the :class`gtk.Button` to add a new Failure
                            Definition to the Revision.
    :ivar btnRemoveDefinition: the :class`gtk.Button` to remove the selected
                               Failure Definition.
    :ivar btnSaveDefinitions: the :class`gtk.Button` to save the Failure
                              Definitions to the RTK Project database.

    :ivar tvwMissionProfile: the :class:`gtk.TreeView` to display/edit the
                             usage profile for a Revision.
    :ivar tvwFailureDefinitions: the :class:`gtk.TreeView` to display/edit the
                                 failure definitions for a Revision.

    :ivar txtCode: the :class:`gtk.Entry` to display/edit the Revision code.
    :ivar txtName: the :class:`gtk.Entry` to display/edit the Revision name.
    :ivar txtTotalCost: the :class:`gtk.Entry` to display the Revision cost.
    :ivar txtCostFailure: the :class:`gtk.Entry` to display the Revision cost
                          per failure.
    :ivar txtCostHour: the :class:`gtk.Entry` to display the Revision cost per
                       operating hour.
    :ivar txtPartCount: the :class:`gtk.Entry` to display the numebr of
                        hardware components comprising the Revision.
    :ivar txtRemarks: the :class:`gtk.Entry` to display/edit the Revision
                      remarks.
    :ivar txtActiveHt: the :class:`gtk.Entry` to display the Revision active
                       hazard rate.
    :ivar txtDormantHt: the :class:`gtk.Entry` to display the Revision dormant
                        hazard rate.
    :ivar txtSoftwareHt: the :class:`gtk.Entry` to display the Revision
                         software hazard rate.
    :ivar txtPredictedHt: the :class:`gtk.Entry` to display the Revision
                          logistics hazard rate.
    :ivar txtMissionHt: the :class:`gtk.Entry` to display the Revision mission
                        hazard rate.
    :ivar txtMTBF: the :class:`gtk.Entry` to display the Revision logistics
                   MTBF.
    :ivar txtMissionMTBF: the :class:`gtk.Entry` to display the Revision
                          mission MTBF.
    :ivar txtReliability: the :class:`gtk.Entry` to display the Revision
                          logistics reliability.
    :ivar txtMissionRt: the :class:`gtk.Entry` to display the Revision mission
                        reliability.
    :ivar txtMPMT: the :class:`gtk.Entry` to display the Revision mean
                   preventive maintenance time.
    :ivar txtMCMT: the :class:`gtk.Entry` to display the Revision mean
                   corrective maintenance time.
    :ivar txtMTTR: the :class:`gtk.Entry` to display the Revision mean time to
                   repair.
    :ivar txtMMT: the :class:`gtk.Entry` to display the Revision mean
                  maintenance time.
    :ivar txtAvailability: the :class:`gtk.Entry` to display the Revision
                           logistics availability.
    :ivar txtMissionAt: the :class:`gtk.Entry` to display the Revision mission
                        availability.
    """

    def __init__(self, workview, modulebook):
        """
        Initializes the Work Book view for the Revision package.

        :param rtk.gui.gtk.mwi.WorkView workview: the Work View container to
                                                  insert this Work Book into.
        :param rtk.revision.ModuleBook: the Revision Module Book to associate
                                        with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private scalar attributes.
        self._workview = workview
        self._module_book = modulebook
        self._revision_model = None
        self._usage_model = None

        # Initialize private dict attributes.
        self._dic_definitions = {}

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize public scalar attributes.
        self.dtcRevision = modulebook.dtcRevision
        self.dtcProfile = modulebook.dtcProfile
        self.dtcDefinitions = modulebook.dtcDefinitions
        self.revision_id = None

        # General data tab widgets.
        self.txtCode = _widg.make_entry()
        self.txtName = _widg.make_entry()
        self.txtTotalCost = _widg.make_entry(editable=False)
        self.txtCostFailure = _widg.make_entry(editable=False)
        self.txtCostHour = _widg.make_entry(editable=False)
        self.txtPartCount = _widg.make_entry(editable=False)
        self.txtRemarks = gtk.TextBuffer()

        # Usage profile tab widgets.
        self.btnAddSibling = _widg.make_button(width=35,
                                               image='insert_sibling')
        self.btnAddChild = _widg.make_button(width=35, image='insert_child')
        self.btnRemoveUsage = _widg.make_button(width=35, image='remove')
        self.btnSaveUsage = _widg.make_button(width=35, image='save')
        self.tvwMissionProfile = gtk.TreeView()

        # Failure definition tab widgets.
        self.btnAddDefinition = _widg.make_button(width=35, image='add')
        self.btnRemoveDefinition = _widg.make_button(width=35,
                                                     image='remove')
        self.btnSaveDefinitions = _widg.make_button(width=35, image='save')
        self.tvwFailureDefinitions = gtk.TreeView()

        # Assessment results tab widgets.
        self.txtActiveHt = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        self.txtDormantHt = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtSoftwareHt = _widg.make_entry(width=100, editable=False,
                                              bold=True)
        self.txtPredictedHt = _widg.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtMissionHt = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtMTBF = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtMissionMTBF = _widg.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtReliability = _widg.make_entry(width=100, editable=False,
                                               bold=True)
        self.txtMissionRt = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtMPMT = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtMCMT = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtMTTR = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtMMT = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtAvailability = _widg.make_entry(width=100, editable=False,
                                                bold=True)
        self.txtMissionAt = _widg.make_entry(width=100, editable=False,
                                             bold=True)

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Creates the gtk.ToolBar() for the Revision class work book.

        :return: _toolbar
        :rtype: gtk.ToolBar
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add revision button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new revision to the open RTK "
                                   u"Program database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_add_revision)
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete revision button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Removes the currently selected revision "
                                   u"from the open RTK Program database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_delete_revision)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Calculate revision _button_
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Calculate the currently selected "
                                   u"revision."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_calculate_revision)
        _toolbar.insert(_button, _position)
        _position += 1

        # Create report button.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(_(u"Create Revision reports."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/reports.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Mission and Environmental "
                                          u"Profile"))
        _menu_item.set_tooltip_text(_(u"Creates the mission and environmental "
                                      u"profile report for the currently "
                                      u"selected revision."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Failure Definition"))
        _menu_item.set_tooltip_text(_(u"Creates the failure definition report "
                                      u"for the currently selected revision."))
        #_menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save revision button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Saves the currently selected revision "
                                   u"to the open RTK Program database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_save_revision)
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Revision class gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_general_data_page(_notebook)
        self._create_usage_profile_page(_notebook)
        self._create_failure_definition_page(_notebook)
        self._create_assessment_results_page(_notebook)

        return _notebook

    def _create_general_data_page(self, notebook):
        """
        Creates the Revision Work Book page for displaying general data about
        the selected Revision.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the general
                                      data tab.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _frame = _widg.make_frame(label=_(u"General Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame.add(_scrollwindow)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u"Revision Code:"), _(u"Revision Name:"),
                   _(u"Total Cost:"), _(u"Cost/Failure:"),
                   _(u"Cost/Hour:"), _(u"Total Part Count:"),
                   _(u"Remarks:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels,
                                             _fixed, 5, 5)
        _x_pos += 50

        # Set the tooltips.
        self.txtCode.set_tooltip_text(_(u"A unique code for the selected "
                                        u"revision."))
        self.txtName.set_tooltip_text(_(u"The name of the selected "
                                        u"revision."))
        self.txtTotalCost.set_tooltip_text(_(u"Displays the total cost of "
                                             u"the selected revision."))
        self.txtCostFailure.set_tooltip_text(_(u"Displays the cost per "
                                               u"failure of the selected "
                                               u"revision."))
        self.txtCostHour.set_tooltip_text(_(u"Displays the failure cost "
                                            u"per operating hour for the "
                                            u"selected revision."))
        self.txtPartCount.set_tooltip_text(_(u"Displays the total part "
                                             u"count for the selected "
                                             u"revision."))

        # Place the widgets.
        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtTotalCost, _x_pos, _y_pos[2])
        _fixed.put(self.txtCostFailure, _x_pos, _y_pos[3])
        _fixed.put(self.txtCostHour, _x_pos, _y_pos[4])
        _fixed.put(self.txtPartCount, _x_pos, _y_pos[5])

        # Connect to callback functions.
        _textview = _widg.make_text_view(txvbuffer=self.txtRemarks,
                                         width=400)
        _textview.set_tooltip_text(_(u"Enter any remarks associated with "
                                     u"the selected revision."))
        _view = _textview.get_children()[0].get_children()[0]
        _fixed.put(_textview, _x_pos, _y_pos[6])

        self._lst_handler_id.append(self.txtCode.connect('focus-out-event',
                                                         self._on_focus_out,
                                                         22))
        self._lst_handler_id.append(self.txtName.connect('focus-out-event',
                                                         self._on_focus_out,
                                                         17))
        self._lst_handler_id.append(_view.connect('focus-out-event',
                                                  self._on_focus_out, 20))

        _fixed.show_all()

        # Insert the tab.
        _label_ = gtk.Label()
        _heading_ = _("General\nData")
        _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.show_all()
        _label_.set_tooltip_text(_(u"Displays general information for the "
                                   u"selected revision."))
        notebook.insert_page(_frame,
                             tab_label=_label_,
                             position=-1)

        return False

    def _create_usage_profile_page(self, notebook):
        """
        Creates the Revision Work Book page for displaying usage profiles for
        the selected Revision.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Create the mission profile gtk.TreeView().
        self.tvwMissionProfile.set_tooltip_text(_(u"Displays the usage "
                                                  u"profile for the currently "
                                                  u"selected revision."))
        _model = gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT)
        self.tvwMissionProfile.set_model(_model)

        for i in range(10):
            _column = gtk.TreeViewColumn()
            if i == 0:
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

                _column.set_visible(True)
            elif i == 1:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, 3, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, visible=11)

                _column.set_visible(True)
            elif i == 2:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, 4, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=4)
                _column.set_visible(True)
            elif i == 3 or i == 4:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, i + 2,
                              _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2)
                _column.set_visible(True)
            elif i == 5 or i == 6:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, i + 2,
                              _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2, visible=10)
                _column.set_visible(True)
            else:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _column.set_visible(False)

            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            self.tvwMissionProfile.append_column(_column)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwMissionProfile)

        _frame = _widg.make_frame(label=_(u"Usage Profile"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddSibling, False, False)
        _bbox.pack_start(self.btnAddChild, False, False)
        _bbox.pack_start(self.btnRemoveUsage, False, False)
        _bbox.pack_start(self.btnSaveUsage, False, False)

        # Connect to callback functions.
        self._lst_handler_id.append(
            self.btnAddSibling.connect('clicked', self._on_button_clicked, 3))
        self._lst_handler_id.append(
            self.btnAddChild.connect('clicked', self._on_button_clicked, 4))
        self._lst_handler_id.append(
            self.btnRemoveUsage.connect('clicked', self._on_button_clicked, 5))
        self._lst_handler_id.append(
            self.btnSaveUsage.connect('clicked', self._on_button_clicked, 6))

        self._lst_handler_id.append(
            self.tvwMissionProfile.connect('cursor_changed',
                                           self._on_usage_row_changed))

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Usage\nProfile") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays usage profile for the selected "
                                  u"revision."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_failure_definition_page(self, notebook):
        """
        Creates the Revision Work Book page for displaying failure definitions
        for the selected Revision.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
        self.tvwFailureDefinitions.set_model(_model)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Definition\nNumber</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        self.tvwFailureDefinitions.append_column(_column)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 1)
        _cell.set_property('wrap-width', 450)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._on_failure_cell_edited, 1, _model)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Failure Definition</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)
        self.tvwFailureDefinitions.append_column(_column)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwFailureDefinitions)

        _frame = _widg.make_frame(label=_(u"Failure Definition List"))
        _frame.set_shadow_type(gtk.SHADOW_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddDefinition, False, False)
        _bbox.pack_start(self.btnRemoveDefinition, False, False)
        _bbox.pack_start(self.btnSaveDefinitions, False, False)

        self._lst_handler_id.append(
            self.btnAddDefinition.connect('clicked',
                                          self._on_button_clicked, 8))
        self._lst_handler_id.append(
            self.btnRemoveDefinition.connect('clicked',
                                             self._on_button_clicked, 9))
        self._lst_handler_id.append(
            self.btnSaveDefinitions.connect('clicked',
                                            self._on_button_clicked, 10))

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Failure\nDefinitions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays usage profiles for the selected "
                                  u"revision."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_assessment_results_page(self, notebook):
        """
        Creates the Revision Wrok Book page for displaying assessment results
        for the selected Revision.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        # Reliability results containers.
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = _widg.make_frame(label=_(u"Reliability Results"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display reliability assessment      #
        # results.                                                      #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u"Active Failure Intensity [\u039B(t)]:"),
                   _(u"Dormant \u039B(t):"), _(u"Software \u039B(t):"),
                   _(u"Predicted \u039B(t):"), _(u"Mission \u039B(t):"),
                   _(u"Mean Time Between Failure [MTBF]:"),
                   _(u"Mission MTBF:"), _(u"Reliability [R(t)]:"),
                   _(u"Mission R(t):")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 55

        self.txtActiveHt.set_tooltip_text(_(u"Displays the active failure "
                                            u"intensity for the selected "
                                            u"revision."))
        self.txtDormantHt.set_tooltip_text(_(u"Displays the dormant "
                                             u"failure intensity for the "
                                             u"selected revision."))
        self.txtSoftwareHt.set_tooltip_text(_(u"Displays the software "
                                              u"failure intensity for the "
                                              u"selected revision."))
        self.txtPredictedHt.set_tooltip_text(_(u"Displays the predicted "
                                               u"failure intensity for "
                                               u"the selected revision.  "
                                               u"This is the sum of the "
                                               u"active, dormant, and "
                                               u"software hazard rates."))
        self.txtMissionHt.set_tooltip_text(_(u"Displays the mission "
                                             u"failure intensity for the "
                                             u"selected revision."))
        self.txtMTBF.set_tooltip_text(_(u"Displays the limiting mean time "
                                        u"between failure (MTBF) for the "
                                        u"selected revision."))
        self.txtMissionMTBF.set_tooltip_text(_(u"Displays the mission "
                                               u"mean time between "
                                               u"failure (MTBF) for the "
                                               u"selected revision."))
        self.txtReliability.set_tooltip_text(_(u"Displays the limiting "
                                               u"reliability for the "
                                               u"selected revision."))
        self.txtMissionRt.set_tooltip_text(_(u"Displays the mission "
                                             u"reliability for the "
                                             u"selected revision."))

        _fixed.put(self.txtActiveHt, _x_pos, _y_pos[0])
        _fixed.put(self.txtDormantHt, _x_pos, _y_pos[1])
        _fixed.put(self.txtSoftwareHt, _x_pos, _y_pos[2])
        _fixed.put(self.txtPredictedHt, _x_pos, _y_pos[3])
        _fixed.put(self.txtMissionHt, _x_pos, _y_pos[4])
        _fixed.put(self.txtMTBF, _x_pos, _y_pos[5])
        _fixed.put(self.txtMissionMTBF, _x_pos, _y_pos[6])
        _fixed.put(self.txtReliability, _x_pos, _y_pos[7])
        _fixed.put(self.txtMissionRt, _x_pos, _y_pos[8])

        _fixed.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display maintainability assessment  #
        # results.                                                      #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = _widg.make_frame(label=_(u"Maintainability Results"))
        _frame.set_shadow_type(gtk.SHADOW_NONE)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        # Maintainability results widgets.
        _labels = [_(u"Mean Preventive Maintenance Time [MPMT]:"),
                   _(u"Mean Corrective Maintenance Time [MCMT]:"),
                   _(u"Mean Time to Repair [MTTR]:"),
                   _(u"Mean Maintenance Time [MMT]:"),
                   _(u"Availability [A(t)]:"), _(u"Mission A(t):")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
        _x_pos += 55

        self.txtMPMT.set_tooltip_text(_(u"Displays the mean preventive "
                                        u"maintenance time (MPMT) for the "
                                        u"selected revision."))
        self.txtMCMT.set_tooltip_text(_(u"Displays the mean corrective "
                                        u"maintenance time (MCMT) for the "
                                        u"selected revision."))
        self.txtMTTR.set_tooltip_text(_(u"Displays the mean time to "
                                        u"repair (MTTR) for the selected "
                                        u"revision."))
        self.txtMMT.set_tooltip_text(_(u"Displays the mean maintenance "
                                       u"time (MMT) for the selected "
                                       u"revision.  This includes "
                                       u"preventive and corrective "
                                       u"maintenance."))
        self.txtAvailability.set_tooltip_text(_(u"Displays the logistics "
                                                u"availability for the "
                                                u"selected revision."))
        self.txtMissionAt.set_tooltip_text(_(u"Displays the mission "
                                             u"availability for the "
                                             u"selected revision."))

        _fixed.put(self.txtMPMT, _x_pos, _y_pos[0])
        _fixed.put(self.txtMCMT, _x_pos, _y_pos[1])
        _fixed.put(self.txtMTTR, _x_pos, _y_pos[2])
        _fixed.put(self.txtMMT, _x_pos, _y_pos[3])
        _fixed.put(self.txtAvailability, _x_pos, _y_pos[4])
        _fixed.put(self.txtMissionAt, _x_pos, _y_pos[5])

        _fixed.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Assessment\nResults") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays reliability, maintainability, "
                                  u"and availability assessment results for "
                                  u"the selected revision."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model, usage_model, definitions):
        """
        Method to load the Revision class gtk.Notebook() widgets.

        :param rtk.revision.Revision.Model: the Revision Model to be viewed.
        :param rtk.usage.UsageProfile.Model: the Usage Profile Model to be
                                             viewed.
        :param dict definitions: the list of Failure Definition data model
                                 instances associated with the Revision.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self._revision_model = model
        self._usage_model = usage_model
        self._dic_definitions = definitions
        self.revision_id = self._revision_model.revision_id

        # Load the General Data page.
        self.txtTotalCost.set_text(
            str(locale.currency(self._revision_model.cost)))
        self.txtCostFailure.set_text(
            str(locale.currency(self._revision_model.cost_per_failure)))
        self.txtCostHour.set_text(
            str(locale.currency(self._revision_model.cost_per_hour)))
        self.txtName.set_text(self._revision_model.name)
        self.txtRemarks.set_text(self._revision_model.remarks)
        self.txtPartCount.set_text(
            str('{0:0.0f}'.format(self._revision_model.n_parts)))
        self.txtCode.set_text(str(self._revision_model.code))

        # Load the Usage Profile page.
        self._load_usage_profile()

        # Load the Failure Definitions page.
        self._load_failure_definitions()

        # Load the Assessment Results page.
        self.txtAvailability.set_text(
            str(fmt.format(self._revision_model.availability)))
        self.txtMissionAt.set_text(
            str(fmt.format(self._revision_model.mission_availability)))
        self.txtActiveHt.set_text(str(
            fmt.format(self._revision_model.active_hazard_rate)))
        self.txtDormantHt.set_text(
            str(fmt.format(self._revision_model.dormant_hazard_rate)))
        self.txtMissionHt.set_text(
            str(fmt.format(self._revision_model.mission_hazard_rate)))
        self.txtPredictedHt.set_text(
            str(fmt.format(self._revision_model.hazard_rate)))
        self.txtSoftwareHt.set_text(
            str(fmt.format(self._revision_model.software_hazard_rate)))
        self.txtMMT.set_text(str(fmt.format(self._revision_model.mmt)))
        self.txtMCMT.set_text(str(fmt.format(self._revision_model.mcmt)))
        self.txtMPMT.set_text(str(fmt.format(self._revision_model.mpmt)))
        self.txtMissionMTBF.set_text(
            str(fmt.format(self._revision_model.mission_mtbf)))
        self.txtMTBF.set_text(str(fmt.format(self._revision_model.mtbf)))
        self.txtMTTR.set_text(str(fmt.format(self._revision_model.mttr)))
        self.txtMissionRt.set_text(
            str(fmt.format(self._revision_model.mission_reliability)))
        self.txtReliability.set_text(
            str(fmt.format(self._revision_model.reliability)))

        _title = _(u"RTK Work Book: Revision (Analyzing %s)") % \
            self._revision_model.name
        _workview = self.get_parent()
        _workview.set_title(_title)

        return False

    def _load_usage_profile(self, path=None):
        """
        Loads the Usage Profile gkt.TreeView().

        :keyword str path: the path in the gtk.TreeView() to select as active
                           after loading the Usage Profile.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwMissionProfile.get_model()
        _model.clear()
        for _mission in self._usage_model.dicMissions.values():
            _icon = _conf.ICON_DIR + '32x32/mission.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = (_icon, _mission.mission_id, _mission.description,
                     '', _mission.time_units, 0.0, _mission.time, 0.0, 0.0, 1,
                     0, 0)
            _mission_row = _model.append(None, _data)

            for _phase in _mission.dicPhases.values():
                _icon = _conf.ICON_DIR + '32x32/phase.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _data = (_icon, _phase.phase_id, _phase.code,
                         _phase.description, '', _phase.start_time,
                         _phase.end_time, 0.0, 0.0, 2, 0, 1)
                _phase_row = _model.append(_mission_row, _data)

                for _environment in _phase.dicEnvironments.values():
                    _icon = _conf.ICON_DIR + '32x32/environment.png'
                    _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                    _data = (_icon, _environment.environment_id,
                             _environment.name, '', _environment.units,
                             _environment.minimum, _environment.maximum,
                             _environment.mean, _environment.variance, 3, 1, 0)
                    _model.append(_phase_row, _data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                return False
        _column = self.tvwMissionProfile.get_column(0)
        self.tvwMissionProfile.set_cursor(path, None, False)
        self.tvwMissionProfile.row_activated(path, _column)
        self.tvwMissionProfile.expand_all()

        return False

    def _load_failure_definitions(self, path=None):
        """
        Loads the Failure Definitions gkt.TreeView().

        :keyword str path: the path in the gtk.TreeView() to select as active
                           after loading the Usage Profile.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _revision_id = self._revision_model.revision_id

        _model = self.tvwFailureDefinitions.get_model()
        _model.clear()
        for _definition in self.dtcDefinitions.dicDefinitions[_revision_id].values():
            _data = (_definition.definition_id, _definition.definition)
            _model.append(_data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                return False
        _column = self.tvwFailureDefinitions.get_column(0)
        self.tvwFailureDefinitions.set_cursor(path, None, False)
        self.tvwFailureDefinitions.row_activated(path, _column)
        self.tvwFailureDefinitions.expand_all()

        return False

    def update(self):
        """
        Updates the Work Book widgets with changes to the Revision data model
        attributes.  Called by other views when the Revision data model
        attributes are edited via their gtk.Widgets().
        """

        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(self._revision_model.code))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text(str(self._revision_model.name))
        self.txtName.handler_unblock(self._lst_handler_id[1])

        _textview = self.txtRemarks.get_child()
        _textview.handler_block(self._lst_handler_id[2])
        _textbuffer = _textview.get_buffer()
        _textbuffer.set_text(self._revision_model.remarks)
        _textview.handler_unblock(self._lst_handler_id[2])

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

        if index in [3, 4, 5, 6]:
            (_model,
             _row) = self.tvwMissionProfile.get_selection().get_selected()
            try:
                _path = _model.get_path(_row)
                _id = _model.get_value(_row, 1)
                _level = _model.get_value(_row, 9)
            except TypeError:
                return True
        elif index in [8, 9, 10]:
            (_model,
             _row) = self.tvwFailureDefinitions.get_selection().get_selected()
            try:
                _path = _model.get_path(_row)
                _id = _model.get_value(_row, 0)
            except TypeError:
                return True

        _revision_id = self._revision_model.revision_id

        button.handler_block(self._lst_handler_id[index])
        if index == 3:                      # Add a sibling.
            if _level == 1:                 # _id = Mission ID
                _piter = _model.iter_parent(_row)
                (__, __,
                 _mission_id) = self.dtcProfile.add_mission(_revision_id)
                _attributes = self._usage_model.dicMissions[_mission_id].get_attributes()
                _icon = _conf.ICON_DIR + '32x32/mission.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _data = (_icon, _attributes[0], _attributes[3], '',
                         _attributes[2], 0.0, _attributes[1], 0.0, 0.0, 1, 0,
                         0)
            elif _level == 2:               # _id = Phase ID
                _piter = _model.iter_parent(_row)
                _mission_id = _model.get_value(_piter, 1)
                (__, __,
                 _phase_id) = self.dtcProfile.add_phase(_revision_id, _mission_id)
                _mission = self._usage_model.dicMissions[_mission_id]
                _attributes = _mission.dicPhases[_phase_id].get_attributes()
                _icon = _conf.ICON_DIR + '32x32/phase.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _data = (_icon, _attributes[2], _attributes[5],
                         _attributes[6], '', _attributes[3],
                         _attributes[4], 0.0, 0.0, 2, 0, 1)
            elif _level == 3:               # _id = Environment ID
                _piter = _model.iter_parent(_row)
                _phase_id = _model.get_value(_piter, 1)
                _grand_piter = _model.iter_parent(_piter)
                _mission_id = _model.get_value(_grand_piter, 1)
                (__, __,
                 _environment_id) = self.dtcProfile.add_environment(_revision_id,
                                                                    _mission_id,
                                                                    _phase_id)
                _mission = self._usage_model.dicMissions[_mission_id]
                _phase = _mission.dicPhases[_phase_id]
                _attributes = _phase.dicEnvironments[_environment_id].get_attributes()
                _icon = _conf.ICON_DIR + '32x32/environment.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _data = (_icon, _attributes[4], _attributes[5], '',
                         _attributes[6], _attributes[7], _attributes[8],
                         _attributes[9], _attributes[10], 3, 1, 0)

            # Insert a new row with the new Usage Profile item and then select
            # the newly inserted row for editing.
            _row = _model.insert(_piter, -1, _data)
            _path = _model.get_path(_row)
            self.tvwMissionProfile.set_cursor(_path,
                                              self.tvwMissionProfile.get_column(1),
                                              True)
            self.tvwMissionProfile.row_activated(_path,
                                                 self.tvwMissionProfile.get_column(0))
        elif index == 4:                    # Add a child.
            if _level == 1:                 # _id = Mission ID
                _piter = _row
                (__, __,
                 _phase_id) = self.dtcProfile.add_phase(_revision_id, _id)
                _mission = self._usage_model.dicMissions[_id]
                _attributes = _mission.dicPhases[_phase_id].get_attributes()
                _icon = _conf.ICON_DIR + '32x32/phase.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _data = (_icon, _attributes[2], _attributes[5],
                         _attributes[6], '', _attributes[3],
                         _attributes[4], 0.0, 0.0, 2, 0, 1)
            elif _level == 2:               # _id = Phase ID
                _piter = _model.iter_parent(_row)
                _mission_id = _model.get_value(_piter, 1)
                _piter = _row
                (__, __,
                 _environment_id) = self.dtcProfile.add_environment(_revision_id,
                                                                    _mission_id,
                                                                    _id)
                _mission = self._usage_model.dicMissions[_mission_id]
                _phase = _mission.dicPhases[_id]
                _attributes = _phase.dicEnvironments[_environment_id].get_attributes()
                _icon = _conf.ICON_DIR + '32x32/environment.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _data = (_icon, _attributes[4], _attributes[5], '',
                         _attributes[6], _attributes[7], _attributes[8],
                         _attributes[9], _attributes[10], 3, 1, 0)
            else:
# TODO: Informational dialog to let user know they can't add a child to an environment.
                return False
            # Insert a new row with the new Usage Profile item and then select
            # the newly inserted row for editing.
            _row = _model.insert(_piter, -1, _data)
            _path = _model.get_path(_row)
            self.tvwMissionProfile.set_cursor(_path,
                                              self.tvwMissionProfile.get_column(1),
                                              True)
            self.tvwMissionProfile.row_activated(_path,
                                                 self.tvwMissionProfile.get_column(0))
        elif index == 5:                    # Remove from profile.
            if _level == 1:                 # _id = Mission ID
                _piter = None
                (_results,
                 _error_code) = self.dtcProfile.delete_mission(_revision_id, _id)
            elif _level == 2:               # _id = Phase ID
                _piter = _model.iter_parent(_row)
                _mission_id = _model.get_value(_piter, 1)
                (_results,
                 _error_code) = self.dtcProfile.delete_phase(_revision_id, _mission_id, _id)
            elif _level == 3:               # _id = Environment ID
                _piter = _model.iter_parent(_row)
                _phase_id = _model.get_value(_piter, 1)
                _grand_piter = _model.iter_parent(_piter)
                _mission_id = _model.get_value(_grand_piter, 1)
                (_results,
                 _error_code) = self.dtcProfile.delete_environment(_revision_id, _mission_id, _phase_id, _id)

            if _results:
                try:
                    _path = _model.get_path(_model.iter_next(_piter))
                except TypeError:
                    _path = None
                self._load_usage_profile(_path)
            else:
# TODO: Handle any errors returned.
                print _error_code
        elif index == 6:                    # Save profile.
            self.dtcProfile.save_profile(_revision_id)
        elif index == 8:                    # Add failure definition.
            self.dtcDefinitions.add_definition(_revision_id)
            self._load_failure_definitions()
        elif index == 9:                    # Remove failure definition.
            self.dtcDefinitions.delete_definition(_revision_id, _id)
            self._load_failure_definitions()
        elif index == 10:                   # Save failure definition.
            self.dtcDefinitions.save_definitions(_revision_id)

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Callback function to retrieve gtk.Entry() changes and assign the new
        data to the appropriate Revision data model attribute.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the position in the Revision class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if index == 17:
            _text = entry.get_text()
            self._revision_model.name = _text
        elif index == 20:
            _text = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())
            self._revision_model.remarks = _text
        elif index == 22:
            _text = entry.get_text()
            self._revision_model.code = _text

        self._module_book.update(index, _text)

        return False

    def _on_usage_row_changed(self, treeview):
        """
        Callback function to handle events for the Revision package Work Book
        Usage Profile gtk.TreeView().  It is called whenever a Work Book
        Usage Profile gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the Revision classt gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self.tvwMissionProfile.handler_block(self._lst_handler_id[7])

        (_model, _row) = treeview.get_selection().get_selected()
        _level = _model.get_value(_row, 9)

        _columns = treeview.get_columns()

        # Change the column headings depending on what is being selected.
        if _level == 1:                         # Mission
            _headings = [_(u"Mission ID"), _(u"Description"), _(u"Units"),
                         _(u"Start Time"), _(u"End Time"), _(u""), _(u""),
                         _(u"")]
        elif _level == 2:                       # Mission phase
            _headings = [_(u"Phase ID"), _(u"  Code\t\tDescription"),
                         _(u"Units"), _(u"Start Time"), _(u"End Time"), _(u""),
                         _(u""), _(u"")]
        elif _level == 3:                       # Environment
            _headings = [_(u"Environment ID"), _(u"Condition"), _(u"Units"),
                         _(u"Minimum Value"), _(u"Maximum Value"),
                         _(u"Mean Value"), _(u"Variance"), _(u"")]

        for i in range(7):
            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _headings[i] +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _columns[i].set_widget(_label)

        self.tvwMissionProfile.handler_unblock(self._lst_handler_id[7])

        return False

    def _on_usage_cell_edited(self, __cell, path, new_text, position, model):
        """
        Callback function to handle edits of the Revision package Work Book
        Usage Profile gtk.Treeview()s.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
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

        _revision_id = self._revision_model.revision_id

        _row = model.get_iter(path)
        _id = model.get_value(_row, 1)

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))
        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        # Determine whether we are editing a mission, mission phase, or
        # environment.  Get the values and update the attributes.
        _level = model.get_value(_row, 9)
        if _level == 1:                     # Mission
            _values = (_revision_id, _id) + model.get(_row, 6, 4, 2)
            _mission = self._usage_model.dicMissions[_id]
            _mission.set_attributes(_values)
        elif _level == 2:                   # Mission phase
            _values = model.get(_row, 5, 6, 2, 3)
            _row = model.iter_parent(_row)
            _mission_id = model.get_value(_row, 1)
            _mission = self._usage_model.dicMissions[_mission_id]
            _values = (_revision_id, _mission_id, _id) + _values
            _phase = _mission.dicPhases[_id]
            _phase.set_attributes(_values)
        elif _level == 3:                   # Environment
            _values = model.get(_row, 2, 4, 5, 6, 7, 8)
            _row = model.iter_parent(_row)
            _phase_id = model.get_value(_row, 1)
            _row = model.iter_parent(_row)
            _mission_id = model.get_value(_row, 1)
            _mission = self._usage_model.dicMissions[_mission_id]
            _phase = _mission.dicPhases[_phase_id]
            _values = (_revision_id, _mission_id, _phase_id, 0, _id) + _values
            _environment = _phase.dicEnvironments[_id]
            _environment.set_attributes(_values)

        return False

    def _on_failure_cell_edited(self, __cell, path, new_text, position, model):
        """
        Callback function to handle edits of the Revision package Work Book
        Failure Definition gtk.Treeview()s.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
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

        _row = model.get_iter(path)
        _id = model.get_value(_row, 0)

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        _definition = self._dic_definitions[_id]
        if position == 1:
            _definition.definition = str(new_text)

        return False

    def _request_save_revision(self, __button):
        """
        Sends request to save the selected revision to the Revision data
        controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                         method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _revision_id = self._revision_model.revision_id
        (_results,
         _error_code) = self.dtcRevision.save_revision(_revision_id)

        return False

    def _request_add_revision(self, __button):
        """
        Sends request to add a new revision to the Revision data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Launch the Add Revision gtk.Assistant().
        _dialog = AddRevision(self.dtcRevision)
        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            # Retrieve the new Revision information
            _code = _dialog.txtRevisionCode.get_text()
            _name = _dialog.txtRevisionName.get_text()
            _remarks = _dialog.txtRemarks.get_text(*_dialog.txtRemarks.get_bounds())

            (_results,
             _error_code,
             _last_id) = self.dtcRevision.add_revision(_code, _name, _remarks)

            # If the revision was successfully added to the RTK Project
            # database, add a Usage Profile and empty failure definition dict
            # to the controller.  Finally, add the new Revision to the Module
            # Book gtk.TreeView().
            if _results:
                self.dtcProfile.add_profile(_last_id)
                self.dtcDefinitions.dicDefinitions[_last_id] = {}

                _values = self.dtcRevision.dicRevisions[_last_id].get_attributes()
                _model = self._modulebook.treeview.get_model()
                _model.append(None, _values)

        _dialog.destroy()

        return False

    def _request_delete_revision(self, __button):
        """
        Sends request to delete the selected revision from the Revision data
        controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self._modulebook.treeview.get_selection().get_selected()
        _path = _model.get_path(_row)

        _revision_id = self._revision_model.revision_id

        (_results,
         _error_code) = self.dtcRevision.delete_revision(_revision_id)

        self.dtcProfile.dicProfiles.pop(_revision_id)
        self.dtcDefinitions.dicDefinitions.pop(_revision_id)
# TODO: Delete from treeview and refresh Module Book view.
        #_next_row = _model.iter_next(_row)

        #_model.remove(_row)
        #_model.row_deleted(_path)

        #if _next_row is None:
        #_next_row = _model.get_iter_root()
        #_path = _model.get_path(_next_row)
        #self._modulebook.treeview.set_cursor(_path, None, False)
        #self._modulebook.treeview.row_activated(_path, self._modulebook.treeview.get_column(0))

        return False

    def _request_calculate_revision(self, __button):
        """
        Sends request to calculate the selected revision to the Revision data
        controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _revision_id = self._revision_model.revision_id
        self.dtcRevision.calculate_revision(_revision_id, _conf.RTK_MTIME,
                                            _conf.FRMULT)

        return False
