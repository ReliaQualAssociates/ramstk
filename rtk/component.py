#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to the
hardware components of the Program.
"""

__author__ = 'Andrew Rowland <andrew.rowland@reliaqual.com>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       component.py is part of The RTK Project
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

# Modules required for plotting.
import matplotlib
matplotlib.use('GTK')
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

# Import other RTK modules.
import calculations as _calc
import configuration as _conf
import utilities as _util
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Component():
    """
    The COMPONENT class is used to represent a component in a system being
    analyzed.
    """

    def _fmeca_widgets_create(self):
        """ Method to create the FMECA widgets. """

        import pango
        from lxml import etree

        # Retrieve the column heading text from the format file.
        path = "/root/tree[@name='FMECA']/column/usertitle"
        heading = etree.parse(_conf.RTK_FORMAT_FILE[9]).xpath(path)

        # Retrieve the column datatype from the format file.
        path = "/root/tree[@name='FMECA']/column/datatype"
        datatype = etree.parse(_conf.RTK_FORMAT_FILE[9]).xpath(path)

        # Retrieve the cellrenderer type from the format file.
        path = "/root/tree[@name='FMECA']/column/widget"
        widget = etree.parse(_conf.RTK_FORMAT_FILE[9]).xpath(path)

        # Retrieve the column position from the format file.
        path = "/root/tree[@name='FMECA']/column/position"
        position = etree.parse(_conf.RTK_FORMAT_FILE[9]).xpath(path)

        # Retrieve whether or not the column is editable from the format file.
        path = "/root/tree[@name='FMECA']/column/editable"
        editable = etree.parse(_conf.RTK_FORMAT_FILE[9]).xpath(path)

        # Retrieve whether or not the column is visible from the format file.
        path = "/root/tree[@name='FMECA']/column/visible"
        visible = etree.parse(_conf.RTK_FORMAT_FILE[9]).xpath(path)

        # Create a list of GObject datatypes to pass to the model.
        types = []
        for i in range(len(position)):
            types.append(datatype[i].text)

        gobject_types = []
        gobject_types = [gobject.type_from_name(types[ix])
            for ix in range(len(types))]

        query = "SELECT fld_category_noun, \
                        fld_category_value \
                 FROM tbl_risk_category"
        risk_category = self._app.COMDB.execute_query(query,
                                                      None,
                                                      self._app.ComCnx)

        bg_color = _conf.RTK_COLORS[6]
        fg_color = _conf.RTK_COLORS[7]

        # Create the model and treeview.
        model = gtk.ListStore(*gobject_types)
        self.tvwFMECA.set_model(model)

        cols = int(len(heading))
        for i in range(cols):
            self._fmeca_col_order.append(int(position[i].text))

            if(widget[i].text == 'combo'):
                cell = gtk.CellRendererCombo()
                cellmodel = gtk.ListStore(gobject.TYPE_STRING,
                                          gobject.TYPE_INT)

                if(i == 11):
                    for j in range(len(risk_category)):
                        cellmodel.append(risk_category[j])

                cell.set_property('has-entry', False)
                cell.set_property('model', cellmodel)
                cell.set_property('text-column', 0)
                cell.set_property('editable', int(editable[i].text))
                cell.connect('edited', _widg.edit_tree, int(position[i].text),
                             model)
            elif(widget[i].text == 'spin'):
                cell = gtk.CellRendererSpin()
                adjustment = gtk.Adjustment(upper=1.0, step_incr=0.05)
                cell.set_property('adjustment', adjustment)
                cell.set_property('digits', 2)
                cell.set_property('editable', int(editable[i].text))
                cell.connect('edited', self._fmeca_tree_edit, i, model)
            elif(widget[i].text == 'check'):
                cell = gtk.CellRendererToggle()
                cell.set_property('activatable', int(editable[i].text))
                cell.connect('toggled', self._fmeca_tree_edit, None, i, model)
            else:
                cell = gtk.CellRendererText()
                cell.set_property('editable', int(editable[i].text))

                if(int(editable[i].text) == 0):
                    cell.set_property('background', 'light gray')
                else:
                    cell.set_property('background', bg_color)
                    cell.set_property('foreground', fg_color)
                    cell.set_property('wrap-width', 250)
                    cell.set_property('wrap-mode', pango.WRAP_WORD)
                    cell.connect('edited', _widg.edit_tree,
                                 int(position[i].text), model)

            column = gtk.TreeViewColumn()
            column.set_visible(int(visible[i].text))
            column.pack_start(cell, True)

            label = gtk.Label(column.get_title())
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            text = "<span weight='bold'>%s</span>" % heading[i].text
            label.set_markup(text)
            label.show_all()
            column.set_widget(label)

            column.set_resizable(True)
            column.set_reorderable(True)
            column.set_sort_column_id(i)
            column.set_sort_indicator(True)

            if(widget[i].text != 'check'):
                column.set_attributes(cell, text=int(position[i].text))
                column.set_cell_data_func(cell, _widg.format_cell,
                                          (int(position[i].text),
                                          datatype[i].text))
                column.connect('notify::width', _widg.resize_wrap, cell)
            else:
                column.set_attributes(cell, active=int(position[i].text))

            self.tvwFMECA.append_column(column)

        self.tvwFMECA.set_tooltip_text(_("Displays the failure mode, effects, and criticality analysis (FMECA) for the selected component."))
        self.tvwFMECA.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        return False

    def _fmeca_tab_create(self):
        """
        Method to create the FMECA gtk.Notebook tab and populate it with the
        appropriate widgets.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwFMECA)

        frame = _widg.make_frame(_label_=_("Failure Mode, Effects, and Criticality Analysis"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _("FMEA/FMECA\nWorksheet")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Failure mode, effects, and criticality analysis (FMECA) for the selected component."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _fmeca_tab_load(self):
        """
        Loads the widgets with FMECA information for the COMPONENT Object.
        """

# Find the revision ID.
        if(_conf.RTK_MODULES[0] == 1):
            _values = (self._app.REVISION.revision_id,
                       self._app.ASSEMBLY.assembly_id)
        else:
            _values = (0, self._app.ASSEMBLY.assembly_id)

# Now load the FMECA gtk.TreeView.
# Load the FMECA failure mode gtk.TreeView.
        query = "SELECT fld_mode_id, fld_mode_description, \
                        fld_mission_phase, fld_local_effect, \
                        fld_next_effect, fld_end_effect, \
                        fld_detection_method, fld_other_indications, \
                        fld_isolation_method, fld_design_provisions, \
                        fld_operator_provisions, fld_severity_class, \
                        fld_hazard_rate_source, fld_effect_probability, \
                        fld_mode_ratio, fld_mode_failure_rate, \
                        fld_mode_op_time, fld_mode_criticality, \
                        fld_rpn_severity, fld_immediate_cause, \
                        fld_root_cause, fld_rpn_occurence, \
                        fld_detection_control, fld_prevention_control, \
                        fld_rpn_detectability, fld_rpn, \
                        fld_recommended_action, fld_action_taken, \
                        fld_rpn_severity_new, fld_rpn_occurrence_new, \
                        fld_rpn_detectability_new, fld_rpn_new, \
                        fld_critical_item, fld_single_point, \
                        fld_remarks \
                 FROM tbl_fmeca \
                 WHERE fld_revision_id=%d \
                 AND fld_assembly_id=%d \
                 ORDER BY fld_mode_id" % _values

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        model = self.tvwFMECA.get_model()
        model.clear()

        if(not results or results == ''):
            return True

        n_modes = len(results)
        for i in range(n_modes):
            _data = [results[i][0], _util.none_to_string(results[i][1]),
                     _util.none_to_string(results[i][2]),
                     _util.none_to_string(results[i][3]),
                     _util.none_to_string(results[i][4]),
                     _util.none_to_string(results[i][5]),
                     _util.none_to_string(results[i][6]),
                     _util.none_to_string(results[i][7]),
                     _util.none_to_string(results[i][8]),
                     _util.none_to_string(results[i][9]),
                     _util.none_to_string(results[i][10]),
                     _util.none_to_string(results[i][11]),
                     _util.none_to_string(results[i][12]), results[i][13],
                     results[i][14], results[i][15], results[i][16],
                     results[i][17], results[i][18],
                     _util.none_to_string(results[i][19]),
                     _util.none_to_string(results[i][20]), results[i][21],
                     _util.none_to_string(results[i][22]),
                     _util.none_to_string(results[i][23]), results[i][24],
                     results[i][25], _util.none_to_string(results[i][26]),
                     _util.none_to_string(results[i][27]), results[i][28],
                     results[i][29], results[i][30], results[i][31],
                     results[i][32], results[i][33],
                     _util.none_to_string(results[i][34])]

            try:
                model.append(_data)
            except TypeError:
                pass

        return False

    def load_notebook(self):
        """ Function to load the gtk.Notebook for the COMPONENT object. """

        self.model = self._app.winParts.tvwPartsList.get_model()
        self.selected_row = self._app.winParts.selected_row

# Remove existing gtk.Notebook pages except the General Data page.
        while(self.notebook.get_n_pages() > 1):
            self.notebook.remove_page(-1)

        self._general_data_tab_load()
        if self._assessment_inputs_widgets_create():
            self._app.debug_log.error("component.py: Failed to create Assessment Inputs tab widgets.")
        if self._assessment_inputs_tab_create():
            self._app.debug_log.error("component.py: Failed to create Assessment Inputs tab.")
        self._assessment_inputs_tab_load()
        if self._assessment_results_widgets_create():
            self._app.debug_log.error("component.py: Failed to create Assessment Results tab widgets.")
        if self._assessment_results_tab_create():
            self._app.debug_log.error("component.py: Failed to create Assessment Results tab.")
        self._assessment_results_tab_load()
        if self._fmeca_widgets_create():
            self._app.debug_log.error("component.py: Failed to create FMECA tab widgets.")
        if self._fmeca_tab_create():
            self._app.debug_log.error("component.py: Failed to create FMECA tab.")
        self._fmeca_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxComponent)
        self._app.winWorkBook.show_all()

        _title_ = _(u"RTK Work Book: Analyzing %s") % \
                  self._app.HARDWARE.model.get_value(self._app.HARDWARE.selected_row, 17)
        self._app.winWorkBook.set_title(_title_)
        self.notebook.set_current_page(0)

        return False

    def _callback_check(self, check, _index_):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check   -- the checkbutton that called the function.
        _index_ -- the position in the Assembly Object _attribute list
                   associated with the data from the calling checkbutton.
        """

        # Update the Hardware Tree.
        self._app.HARDWARE.model.set_value(self._app.HARDWARE.selected_row,
                                           _index_,
                                           check.get_active())

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the combobox that called the function.
        _index_ -- the position in the Component Object tree model
                   associated with the data from the calling combobox.
        """

        elif(_index_ == 543):               # Manufacturer
            cmbmodel = combo.get_model()
            cmbrow = combo.get_active_iter()

            self.txtCAGECode.set_text(str(cmbmodel.get_value(cmbrow, 2)))
            self._app.HARDWARE.model.set_value(self._app.HARDWARE.selected_row,
                                               9,
                                               str(cmbmodel.get_value(cmbrow, 2)))

        if(_index_ < 500):                  # Update the Parts List.
            self.model.set_value(self.selected_row,
                                 _index_,
                                 int(combo.get_active()))
        else:                               # Update the Hardware tree.
            _index_ -= 500
            self._app.HARDWARE.model.set_value(self._app.HARDWARE.selected_row,
                                               _index_,
                                               int(combo.get_active()))

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Component Object tree model
                   associated with the data from the calling entry.
        """

        # Update the COMPONENT object calculation data.
        if(convert == 'text'):
            if(_index_ == 71):
                textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
                _text_ = textbuffer.get_text(*textbuffer.get_bounds())
            else:
                _text_ = entry.get_text()

        elif(convert == 'int'):
            _text_ = int(entry.get_text())

        elif(convert == 'float'):
            _text_ = float(entry.get_text())

        if(_index_ < 500):                  # Update the Parts List.
            self.model.set_value(self.selected_row, _index_, _text_)
        else:                               # Update the Hardware tree.
            _index_ -= 500
            self._app.HARDWARE.model.set_value(self._app.HARDWARE.selected_row,
                                               _index_, _text_)

    def _fmeca_tree_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a FMECA failure mode tree or FMECA tree
        gtk.CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        _type_ = gobject.type_name(model.get_column_type(position))

# If this is the critical item or single point column, toggle the check box.
        if(position == 32 or position == 33):
            model[path][position] = not cell.get_active()
        elif(_type_ == 'gchararray'):
            model[path][position] = str(new_text)
        elif(_type_ == 'gint'):
            model[path][position] = int(new_text)
        elif(_type_ == 'gfloat'):
            model[path][position] = float(new_text)

        return False

    def _fmeca_save(self):
        """
        Saves the Assembly Object FMECA gtk.TreeView information to the
        Program's MySQL or SQLite3 database.
        """

        model = self.tvwFMECA.get_model()
        model.foreach(self._fmeca_save_line_item)

        return False

    def _fmeca_save_line_item(self, model, path, row):
        """
        Saves each row in the Assembly Object FMECA failure mode and FMECA
        worksheet treeview model to the database.

        Keyword Arguments:
        model   -- the Assembly Object FMECA failure mode or FMECA worksheet
                   gtk.TreeModel.
        path_   -- the path of the active row in the Assembly Object
                   FMECA gtk.TreeModel.
        row     -- the selected row in the Assembly Object FMECA
                   gtk.TreeView.
        """

        _values = (model.get_value(row, 1), model.get_value(row, 2),
                   model.get_value(row, 3), model.get_value(row, 4),
                   model.get_value(row, 5), model.get_value(row, 6),
                   model.get_value(row, 7), model.get_value(row, 8),
                   model.get_value(row, 9), model.get_value(row, 10),
                   model.get_value(row, 11), model.get_value(row, 12),
                   model.get_value(row, 13), model.get_value(row, 14),
                   model.get_value(row, 15), model.get_value(row, 16),
                   model.get_value(row, 17), model.get_value(row, 18),
                   model.get_value(row, 19), model.get_value(row, 20),
                   model.get_value(row, 21), model.get_value(row, 22),
                   model.get_value(row, 23), model.get_value(row, 24),
                   model.get_value(row, 25), model.get_value(row, 26),
                   model.get_value(row, 27), model.get_value(row, 28),
                   model.get_value(row, 29), model.get_value(row, 30),
                   model.get_value(row, 31), model.get_value(row, 32),
                   model.get_value(row, 33), model.get_value(row, 34),
                   model.get_value(row, 0))

        query = "UPDATE tbl_fmeca \
                 SET fld_mode_description='%s', 'fld_mission_phase=%d, \
                     fld_local_effect=%d, \
                     fld_next_effect='%s', fld_end_effect='%s', \
                     fld_detection_method='%s', \
                     fld_other_indications='%s', \
                     fld_isolation_method='%s', \
                     fld_design_provisions='%s', \
                     fld_operator_provisions='%s', \
                     fld_severity_class=%d, \
                     fld_hazard_rate_source='%s', \
                     fld_effect_probability=%f, fld_mode_ratio=%f, \
                     fld_mode_failure_rate=%f, fld_mode_op_time=%f, \
                     fld_mode_criticality=%f, fld_rpn_severity=%d, \
                     fld_immediate_cause='%s', fld_root_cause='%s', \
                     fld_rpn_occurence=%d, \
                     fld_detection_control='%s', \
                     fld_prevention_control='%s', \
                     fld_rpn_detectability=%d, fld_rpn=%d, \
                     fld_recommended_action='%s', \
                     fld_action_taken='%s', fld_rpn_severity_new=%d, \
                     fld_rpn_occurrence_new=%d, \
                     fld_rpn_detectability_new=%d, fld_rpn_new=%d, \
                     fld_critical_item=%d, fld_single_point=%d, \
                     fld_remarks='%s' \
                 WHERE fld_mode_id=%d" % _values

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("component.py: Failed to save FMECA information.")
            return True

        return False

    def _mode_add(self):
        """
        Method to add a failure mode to the selected assembly.
        """

# Find the revision ID.
        if(_conf.RTK_MODULES[0] == 1):
            _values = (self._app.REVISION.revision_id,
                       self._app.ASSEMBLY.assembly_id)
        else:
            _values = (0, self._app.ASSEMBLY.assembly_id)

        query = "INSERT INTO tbl_fmeca \
                 (fld_revision_id, fld_assembly_id) \
                 VALUES (%d, %d)" % _values

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("component.py: Failed to add new failure mode.")
            return True

        self._fmeca_worksheet_tab_load()

        return False

    def _mode_delete(self):
        """
        Method to remove the selected failure mode from the selected
        assembly.
        """

        # Find the mode ID.
        selection = self.tvwFMECA.get_selection()
        (model, row) = selection.get_selected()

        _values = (model.get_value(row, 0), )

        query = "DELETE FROM tbl_fmeca \
                 WHERE fld_mode_id=%d" % _values

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("component.py: Failed to delete failure mode.")
            return True

        self._fmeca_worksheet_tab_load()

        return False

    def _notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the Tree Book notebook page is changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = General Data
                    1 = Assessment Inputs
                    2 = Assessment Results
                    3 = FMEA/FMECA
                    4 = Maintenance Planning
                    5 = Reliability Test Planning
        """

        self.btnAddItem.show()
        self.btnRemoveItem.show()
        self.btnAnalyze.show()
        self.btnSaveResults.show()

        if(page_num == 0):                  # General data tab
            self.btnAddItem.set_tooltip_text(_("Add a new component to the currently selected assembly."))
            self.btnRemoveItem.set_tooltip_text(_("Delete the currently selected component from the open RTK Program Database."))
            self.btnAnalyze.set_tooltip_text(_("Calculate the hardware metrics in the open RTK Program Database."))
            self.btnSaveResults.set_tooltip_text(_("Saves changes to the open RTK Program Database."))
        elif(page_num == 1):                # Assessment inputs tab
            self.btnAddItem.set_tooltip_text(_("Add a new component to the currently selected assembly."))
            self.btnRemoveItem.set_tooltip_text(_("Delete the currently selected component from the open RTK Program Database."))
            self.btnAnalyze.set_tooltip_text(_("Calculate the hardware metrics in the open RTK Program Database."))
            self.btnSaveResults.set_tooltip_text(_("Saves changes to the open RTK Program Database."))
        elif(page_num == 2):                # Assessment results tab
            self.btnAddItem.set_tooltip_text(_("Add a new component to the currently selected assembly."))
            self.btnRemoveItem.set_tooltip_text(_("Delete the currently selected component from the open RTK Program Database."))
            self.btnAnalyze.set_tooltip_text(_("Calculate the hardware metrics in the open RTK Program Database."))
            self.btnSaveResults.set_tooltip_text(_("Saves changes to the open RTK Program Database."))
        elif(page_num == 3):                # FMEA/FMECA tab
            self.btnAddItem.set_tooltip_text(_("Add a new failure mode, mechanism, or cause to the selected component."))
            self.btnRemoveItem.set_tooltip_text(_("Deletes the selected failure mode, mechanism, or cause."))
            self.btnAnalyze.set_tooltip_text(_("Calculate criticality for the selected component."))
            self.btnSaveResults.set_tooltip_text(_("Save the FMEA/FMECA for the selected component."))
        else:
            self.btnAddItem.hide()
            self.btnRemoveItem.hide()
            self.btnAnalyze.hide()
            self.btnSaveResults.hide()

        return False

    def _toolbutton_pressed(self, widget):
        """
        Method to react to the COMPONENT Object toolbar button clicked events.

        Keyword Arguments:
        widget -- the toolbar button that was pressed.
        """

        # FMEA calculate criticality.
        # V&V add new task
        # V&V assign existing task
        # Maintenance planning
        # Maintenance planning save changes to selected maintenance policy
        _button_ = widget.get_name()
        _page_ = self.notebook.get_current_page()

        if(_page_ == 0):                    # General data tab.
            if(_button_ == 'Add'):
                self.component_add(widget, None)
            elif(_button_ == 'Remove'):
                self.component_delete(widget)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
            elif(_button_ == 'Save'):
                self._app.HARDWARE.save_hardware()
        elif(_page_ == 1):                  # Assessment inputs tab.
            if(_button_ == 'Add'):
                self.component_add(widget, None)
            elif(_button_ == 'Remove'):
                self.component_delete(widget)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
            elif(_button_ == 'Save'):
                self._app.HARDWARE.save_hardware()
        elif(_page_ == 2):                  # Assessment results tab.
            if(_button_ == 'Add'):
                self.component_add(widget, None)
            elif(_button_ == 'Remove'):
                self.component_delete(widget)
            elif(_button_ == 'Analyze'):
                _calc.calculate_project(widget, self._app, 3)
            elif(_button_ == 'Save'):
                self._app.HARDWARE.save_hardware()
        elif(_page_ == 3):                  # FMEA/FMECA tab.
            if(_button_ == 'Add'):
                #self._mode_add()
                print "Add mode/mechanism/cause"
            elif(_button_ == 'Remove'):
                #self._mode_delete()
                print "Remove mode/mechanism/cause"
            elif(_button_ == 'Analyze'):
                print "Criticality calculations"
            elif(_button_ == 'Save'):
                self._fmeca_save()
        #elif(_page_ == 6):                  # Maintenance planning tab.
        #    if(_button_ == 'Add'):
        #        print "Add maintenance activity"
        #    elif(_button_ == 'Remove'):
        #        print "Remove maintenance activity"
        #    elif(_button_ == 'Analyze'):
        #        print "Maintenance costs"
        #    elif(_button_ == 'Save'):
        #        print "Saving maintenance policy"

        return False
