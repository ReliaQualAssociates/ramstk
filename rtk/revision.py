#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related
to the revision of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       revision.py is part of the RTK Project
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

# Import other RTK modules.
import calculations as _calc
import configuration as _conf
import widgets as _widg

from _assistants_.adds import AddRevision

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Revision:
    """ This is the REVISION Class for the RTK Project. """

    _gd_tab_labels = [[_("Revision Code:"), _("Revision Name:"),
                       _("Total Cost:"), _("Cost/Failure:"), _("Cost/Hour:"),
                       _("Total Part Count:"), _("Remarks:")], [], [], []]
    _ar_tab_labels = [[_("Active h(t):"), _("Dormant h(t):"),
                       _("Software h(t):"), _("Predicted h(t):"),
                       _("Mission h(t):"), _("MTBF:"), _("Mission MTBF:"),
                       _("Reliability:"), _("Mission R(t):")],
                      [_("MPMT:"), _("MCMT:"), _("MTTR:"), _("MMT:"),
                       _("Availability:"), _("Mission A(t):")], [], []]

    n_attributes = 23

    def __init__(self, application):
        """
        Initializes the REVISION Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.revision_id = 0
        self._col_order = []

        self.vbxRevision = gtk.VBox()
        toolbar = self._toolbar_create()

        # Find the user's preferred gtk.Notebook tab position.
        if(_conf.TABPOS[2] == 'left'):
            _position = gtk.POS_LEFT
        elif(_conf.TABPOS[2] == 'right'):
            _position = gtk.POS_RIGHT
        elif(_conf.TABPOS[2] == 'top'):
            _position = gtk.POS_TOP
        else:
            _position = gtk.POS_BOTTOM

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(_position)

        self.vbxRevision.pack_start(toolbar, expand=False)
        self.vbxRevision.pack_start(self.notebook)

# Create the General Data tab widgets.
        self.txtCode = _widg.make_entry()
        self.txtName = _widg.make_entry()
        self.txtTotalCost = _widg.make_entry(editable=False)
        self.txtCostFailure = _widg.make_entry(editable=False)
        self.txtCostHour = _widg.make_entry(editable=False)
        self.txtPartCount = _widg.make_entry(editable=False)
        self.txtRemarks = gtk.TextBuffer()
        if self._general_data_widgets_create():
            self._app.debug_log.error("revision.py: Failed to create General Data tab widgets.")
        if self._general_data_tab_create():
            self._app.debug_log.error("revision.py: Failed to create General Data tab.")

# Create the Assessment Results tab widgets.
        self.txtActiveHt = _widg.make_entry(editable=False, bold=True)
        self.txtDormantHt = _widg.make_entry(editable=False, bold=True)
        self.txtSoftwareHt = _widg.make_entry(editable=False, bold=True)
        self.txtPredictedHt = _widg.make_entry(editable=False, bold=True)
        self.txtMissionHt = _widg.make_entry(editable=False, bold=True)
        self.txtMTBF = _widg.make_entry(editable=False, bold=True)
        self.txtMissionMTBF = _widg.make_entry(editable=False, bold=True)
        self.txtReliability = _widg.make_entry(editable=False, bold=True)
        self.txtMissionRt = _widg.make_entry(editable=False, bold=True)
        self.txtMPMT = _widg.make_entry(editable=False, bold=True)
        self.txtMCMT = _widg.make_entry(editable=False, bold=True)
        self.txtMTTR = _widg.make_entry(editable=False, bold=True)
        self.txtMMT = _widg.make_entry(editable=False, bold=True)
        self.txtAvailability = _widg.make_entry(editable=False, bold=True)
        self.txtMissionAt = _widg.make_entry(editable=False, bold=True)
        if self._assessment_results_widgets_create():
            self._app.debug_log.error("revision.py: Failed to create Assessment Results widgets.")
        if self._assessment_results_tab_create():
            self._app.debug_log.error("revision.py: Failed to create Assessment Results tab.")

    def _toolbar_create(self):
        """ Method to create the toolbar for the REVISION Object work book. """

        toolbar = gtk.Toolbar()

        _pos = 0

# Add requirement button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_("Adds a new revision to the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.connect('clicked', AddRevision, self._app)
        toolbar.insert(button, _pos)
        _pos += 1

# Delete requirement button
        button = gtk.ToolButton()
        button.set_tooltip_text(_("Removes the currently selected revision from the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.revision_delete)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Calculate requirement button
        button = gtk.ToolButton()
        button.set_tooltip_text(_("Calculate the currently selected revision."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        button.connect('clicked', _calc.calculate_revision, self._app)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Save requirement button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_("Saves the currently selected revision to the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.revision_save)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.show()

        return(toolbar)

    def _general_data_widgets_create(self):
        """ Method to create General Data widgets for the REVISION object. """

# Quadrant 1 (upper left) widgets.
        self.txtCode.set_tooltip_text(_("A unique code for the selected revision."))
        self.txtCode.connect('focus-out-event',
                             self._callback_entry, 'text', 22)

        self.txtName.set_tooltip_text(_("The name of the selected revision."))
        self.txtName.connect('focus-out-event',
                             self._callback_entry, 'text', 17)

        self.txtTotalCost.set_tooltip_text(_("Displays the total cost of the selected revision."))
        self.txtCostFailure.set_tooltip_text(_("Displays the cost per failure of the selected revision."))
        self.txtCostHour.set_tooltip_text(_("Displays the failure cost per operating hour for the selected revision."))
        self.txtPartCount.set_tooltip_text(_("Displays the total part count for the selected revision."))

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it
        with the appropriate widgets for the REVISION object.
        """

# Place the input/output widgets.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        y_pos = 5
        for i in range(len(self._gd_tab_labels[0])):
            label = _widg.make_label(self._gd_tab_labels[0][i],
                                     150, 25)
            label.set_justify(gtk.JUSTIFY_RIGHT)
            fixed.put(label, 5, (i * 30) + y_pos)

        fixed.put(self.txtCode, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtName, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtTotalCost, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtCostFailure, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtCostHour, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtPartCount, 155, y_pos)
        y_pos += 30

        textview = _widg.make_text_view(buffer_=self.txtRemarks, width=400)
        textview.set_tooltip_text(_("Enter any remarks associated with the selected revision."))
        _view_ = textview.get_children()[0].get_children()[0]
        _view_.connect('focus-out-event', self._callback_entry, 'text', 20)
        fixed.put(textview, 155, y_pos)
        y_pos += 130

        fixed.show_all()

# Insert the tab.
        _label_ = gtk.Label()
        _heading_ = _("General\nData")
        _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.show_all()
        _label_.set_tooltip_text(_(u"Displays general information for the selected revision."))
        self.notebook.insert_page(frame,
                                  tab_label=_label_,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the REVISION
        Object.
        """

        # Display data in the widgets.
        self.txtTotalCost.set_text(str(locale.currency(self.model.get_value(self.selected_row, 3))))
        self.txtCostFailure.set_text(str(locale.currency(self.model.get_value(self.selected_row, 4))))
        self.txtCostHour.set_text(str(locale.currency(self.model.get_value(self.selected_row, 5))))
        self.txtName.set_text(self.model.get_value(self.selected_row, 17))
        self.txtRemarks.set_text(self.model.get_value(self.selected_row, 20))
        self.txtPartCount.set_text(str('{0:0.0f}'.format(self.model.get_value(self.selected_row, 21))))
        self.txtCode.set_text(str(self.model.get_value(self.selected_row, 22)))

        return False

    def _assessment_results_widgets_create(self):
        """
        Method to create the Assessment Results widgets for the
        REVISION object.
        """

        # Quadrant 1 (left) widgets.
        self.txtActiveHt.set_tooltip_text(_("Displays the active failure intensity for the selected revision."))
        self.txtDormantHt.set_tooltip_text(_("Displays the dormant failure intensity for the selected revision."))
        self.txtSoftwareHt.set_tooltip_text(_("Displays the software failure intensity for the selected revision."))
        self.txtPredictedHt.set_tooltip_text(_("Displays the predicted failure intensity for the selected revision.  This is the sum of the active, dormant, and software hazard rates."))
        self.txtMissionHt.set_tooltip_text(_("Displays the mission failure intensity for the selected revision."))
        self.txtMTBF.set_tooltip_text(_("Displays the limiting mean time between failure (MTBF) for the selected revision."))
        self.txtMissionMTBF.set_tooltip_text(_("Displays the mission mean time between failure (MTBF) for the selected revision."))
        self.txtReliability.set_tooltip_text(_("Displays the limiting reliability for the selected revision."))
        self.txtMissionRt.set_tooltip_text(_("Displays the mission reliability for the selected revision."))

        # Quadrant #2 (right) widgets.
        self.txtMPMT.set_tooltip_text(_("Displays the mean preventive maintenance time (MPMT) for the selected revision."))
        self.txtMCMT.set_tooltip_text(_("Displays the mean corrective maintenance time (MCMT) for the selected revision."))
        self.txtMTTR.set_tooltip_text(_("Displays the mean time to repair (MTTR) for the selected revision."))
        self.txtMMT.set_tooltip_text(_("Displays the mean maintenance time (MMT) for the selected revision.  This includes preventive and corrective maintenance."))
        self.txtAvailability.set_tooltip_text(_("Displays the limiting availability for the selected revision."))
        self.txtMissionAt.set_tooltip_text(_("Displays the mission availability for the selected revision."))

        return False

    def _assessment_results_tab_create(self):
        """
        Method to create the Assessment Results gtk.Notebook tab and
        populate is with the appropriate widgets for the REVISION object.
        """

        hbox = gtk.HBox()

        # Construct the left half of the page.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Reliability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        y_pos = 5
        for i in range(len(self._ar_tab_labels[0])):
            label = _widg.make_label(self._ar_tab_labels[0][i],
                                     150, 25)
            fixed.put(label, 5, (i * 30) + y_pos)

        fixed.put(self.txtActiveHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtDormantHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtSoftwareHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtPredictedHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMTBF, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionMTBF, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtReliability, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionRt, 155, y_pos)

        fixed.show_all()

        # Construct the right half of the page.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Maintainability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        y_pos = 5
        for i in range(len(self._ar_tab_labels[1])):
            label = _widg.make_label(self._ar_tab_labels[1][i],
                                     150, 25)
            fixed.put(label, 5, (i * 30) + y_pos)

        fixed.put(self.txtMPMT, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMCMT, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMTTR, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMMT, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtAvailability, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionAt, 155, y_pos)

        fixed.show_all()

# Insert the tab.
        _label_ = gtk.Label()
        _heading_ = _("Assessment\nResults")
        _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.show_all()
        _label_.set_tooltip_text(_(u"Displays reliability, maintainability, and availability assessment results for the selected revision."))
        self.notebook.insert_page(hbox,
                                  tab_label=_label_,
                                  position=-1)

        return False

    def _assessment_results_tab_load(self):
        """
        Loads the widgets with assessment results for the REVISION Object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Display data in the widgets.
        self.txtAvailability.set_text(str(fmt.format(self.model.get_value(self.selected_row, 1))))
        self.txtMissionAt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 2))))

        self.txtActiveHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 6))))
        self.txtDormantHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 7))))
        self.txtMissionHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 8))))
        self.txtPredictedHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 9))))
        self.txtSoftwareHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 10))))

        self.txtMMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 11))))
        self.txtMCMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 12))))
        self.txtMPMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 13))))

        self.txtMissionMTBF.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 14))))
        self.txtMTBF.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 15))))
        self.txtMTTR.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 16))))

        self.txtMissionRt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 18))))
        self.txtReliability.set_text(str(fmt.format(self.model.get_value(self.selected_row, 19))))

        return False

    def create_tree(self):
        """
        Creates the REVISION treeview and connects it to callback functions
        to handle editting.  Background and foreground colors can be set
        using the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[0]
        fg_color = _conf.RTK_COLORS[1]
        (self.treeview, self._col_order) = _widg.make_treeview('Revision', 0,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)

        self.treeview.set_tooltip_text(_("Displays the list of revisions."))
        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)
        self.treeview.connect('button_press_event', self._treeview_clicked)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the REVISION Object gtk.TreeModel with revision information.
        This information can be stored either in a MySQL or SQLite3
        database.
        """

        query = "SELECT * FROM tbl_revisions"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        n_records = len(results)

        self.model.clear()
        for i in range(n_records):
            self.model.append(None, results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        root = self.model.get_iter_root()
        if(root is not None):
            path = self.model.get_path(root)
            column = self.treeview.get_column(0)
            self.treeview.row_activated(path, column)

        self.revision_id = self.model.get_value(self.selected_row, 0)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the REVISION Object
        treeview.

        Keyword Arguments:
        treeview -- the Hardware Object treeview.
        event    -- a gtk.gdk.Event that called this function (the
                    important attribute is which mouse button was clicked).
                    1 = left
                    2 = scrollwheel
                    3 = right
                    4 = forward
                    5 = backward
                    8 =
                    9 =
        """

        if(event.button == 1):
            self._treeview_row_changed(treeview, None, 0)
        elif(event.button == 3):
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, treeview, path, column):
        """
        Callback function to handle events for the REVISION Object
        TreeView.  It is called whenever the REVISION Object TreeView row
        is activated.  It will save the previously selected row in the
        REVISION Object TreeView.

        Keyword Arguments:
        treeview -- the Revision Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        selection = self.treeview.get_selection()
        (self.model, self.selected_row) = selection.get_selected()

        # If not selecting the same revision, load everything associated with
        # the new revision.  Otherwise simply load the Revision Object notebook.
        #if(self.model.get_value(self.selected_row, 0) != self.revision_id):
        self.revision_id = self.model.get_value(self.selected_row, 0)
        values = (self.revision_id,)

        # Build the queries to select the components, reliability tests, and
        # program incidents associated with the selected REVISION.
        if(_conf.BACKEND == 'mysql'):
            qryParts = "SELECT t1.*, t2.fld_part_number, t2.fld_ref_des \
                        FROM tbl_prediction AS t1 \
                        INNER JOIN tbl_system AS t2 \
                        ON t1.fld_assembly_id=t2.fld_assembly_id \
                        WHERE t2.fld_revision_id=%d"
            qryIncidents = "SELECT * FROM tbl_incident\
                            WHERE fld_revision_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            qryParts = "SELECT t1.*, t2.fld_part_number, t2.fld_ref_des \
                        FROM tbl_prediction AS t1 \
                        INNER JOIN tbl_system AS t2 \
                        ON t1.fld_assembly_id=t2.fld_assembly_id \
                        WHERE t2.fld_revision_id=?"
            qryIncidents = "SELECT * FROM tbl_incident\
                            WHERE fld_revision_id=?"

        if self.selected_row is not None:
            self._app.REQUIREMENT.requirement_save()
            self._app.REQUIREMENT.load_tree()
            self._app.FUNCTION.function_save()
            self._app.FUNCTION.load_tree()
            self._app.HARDWARE.hardware_save()
            self._app.HARDWARE.load_tree()
            self._app.SOFTWARE.software_save()
            self._app.SOFTWARE.load_tree()
            self._app.VALIDATION.validation_save()
            self._app.VALIDATION.load_tree()
            self._app.winParts.load_part_tree(qryParts, values)
            #self._app.winParts.load_test_tree(qryTests, values)
            self._app.winParts.load_incident_tree(qryIncidents, values)

        self.load_notebook()

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the REVISION Object gtk.TreeModel.

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the REVISION Object
                   gtk.TreeModel.
        """

        for i in columns:
            self.model.set_value(self.selected_row, i, values[i])

        return False

    def revision_delete(self, menuitem, event):
        """
        Deletes the currently selected Revision from the Program's
        MySQL database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        event    -- the gtk.Button event that called this function.
        """

        # First delete the hardware items associated with the revision.
        values = (self.revision_id,)
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_system \
                     WHERE fld_revision_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_system \
                     WHERE fld_revision_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("revision.py: Failed to delete revision from tbl_system.")
            return True

        # Then delete the revision iteself.
        values = (self.revision_id,)
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_revisions \
                     WHERE fld_revision_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_revisions \
                     WHERE fld_revision_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("revision.py: Failed to delete revision from tbl_revisions.")
            return True

        self.load_tree()

        return False

    def revision_save(self, button=None):
        """
        Saves the REVISION Object gtk.TreeModel information to the
        program's MySQL or SQLite3 database.

        Keyword Argumesnts:
        button -- the gtk.Button widgets that called this method.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the REVISION Object gtk.TreeModel to the
        program's MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the REVISION Object gtk.TreeModel.
        path_ -- the path of the active row in the REVISION Object
                 gtk.TreeModel.
        row   -- the selected row in the REVISION Object gtk.TreeModel.
        """

        _values_ = (model.get_value(row, self._col_order[1]), \
                    model.get_value(row, self._col_order[2]), \
                    model.get_value(row, self._col_order[3]), \
                    model.get_value(row, self._col_order[4]), \
                    model.get_value(row, self._col_order[5]), \
                    model.get_value(row, self._col_order[6]), \
                    model.get_value(row, self._col_order[7]), \
                    model.get_value(row, self._col_order[8]), \
                    model.get_value(row, self._col_order[9]), \
                    model.get_value(row, self._col_order[10]), \
                    model.get_value(row, self._col_order[11]), \
                    model.get_value(row, self._col_order[12]), \
                    model.get_value(row, self._col_order[13]), \
                    model.get_value(row, self._col_order[14]), \
                    model.get_value(row, self._col_order[15]), \
                    model.get_value(row, self._col_order[16]), \
                    model.get_value(row, self._col_order[17]), \
                    model.get_value(row, self._col_order[18]), \
                    model.get_value(row, self._col_order[19]), \
                    model.get_value(row, self._col_order[20]), \
                    model.get_value(row, self._col_order[21]), \
                    model.get_value(row, self._col_order[22]), \
                    model.get_value(row, self._col_order[0]))

        _query_ = "UPDATE tbl_revisions \
                   SET fld_availability=%f, fld_availability_mission=%f, \
                       fld_cost=%f, fld_cost_failure=%f, fld_cost_hour=%f, \
                       fld_failure_rate_active=%f, \
                       fld_failure_rate_dormant=%f, \
                       fld_failure_rate_mission=%f, \
                       fld_failure_rate_predicted=%f, \
                       fld_failure_rate_software=%f, fld_mmt=%f, \
                       fld_mcmt=%f, fld_mpmt=%f, fld_mtbf_mission=%f, \
                       fld_mtbf_predicted=%f, fld_mttr=%f, fld_name='%s', \
                       fld_reliability_mission=%f, \
                       fld_reliability_predicted=%f, fld_remarks='%s', \
                       fld_total_part_quantity=%d, fld_revision_code='%s' \
                   WHERE fld_revision_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to save revision to tbl_revisions.")

    def load_notebook(self):
        """ Loads the REVISION Object gtk.Notebook. """

        self._general_data_tab_load()
        self._assessment_results_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxRevision)
        self._app.winWorkBook.show_all()

        _title = _("RTK Work Book: Revision (Analyzing Revision %d)") % \
                 self.revision_id
        self._app.winWorkBook.set_title(_title)

        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        event   -- the gtk.gdk.Event that called this function.
        convert -- the data type to convert the entry contents to.
        index_  -- the position in the REVISION Object gtk.TreeModel
                   associated with the data from the calling entry.
        """
        print _index_
        if(convert == 'text'):
            if(_index_ == 20):
                _text_ = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())
            else:
                _text_ = entry.get_text()

        elif(convert == 'int'):
            _text_ = int(entry.get_text())

        elif(convert == 'float'):
            _text_ = float(entry.get_text().replace('$', ''))

# Update the Revision tree.
        self.model.set_value(self.selected_row, _index_, _text_)

        return False
