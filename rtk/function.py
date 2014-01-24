#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
the functions of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#    function.py is part of The RTK Project
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
import utilities as _util
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

import gettext
_ = gettext.gettext


class Function:
    """
    The FUNCTION class is used to represent a function in a system being
    analyzed.
    """

    # TODO: Write code to update notebook widgets when editing the Function treeview.
    _gd_tab_labels = [[_("Function Code:"), _("Function Name:"),
                       _("Total Cost:"), _("Total Mode Count:"),
                       _("Total Part Count:"), _("Remarks:")],
                      [], [], []]
    _ar_tab_labels = [[_("Predicted h(t):"), _("Mission h(t):"), _("MTBF:"),
                       _("Mission MTBF:")],
                      [_("MPMT:"), _("MCMT:"), _("MTTR:"), _("MMT:"),
                       _("Availability:"), _("Mission Availability:")],
                      [], []]

    def __init__(self, application):
        """
        Initializes the Function Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.function_id = 0
        self._col_order = []

        self._FunctionMatrix = None

# Find the user's preferred gtk.Notebook tab position.
        self.notebook = gtk.Notebook()
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

        self.notebook.connect('switch-page', self._notebook_page_switched)

# Create the toolbar buttons.
        self.btnAddSibling = gtk.ToolButton()
        self.btnAddChild = gtk.ToolButton()
        self.btnAddMode = gtk.ToolButton()
        self.btnRemoveFunction = gtk.ToolButton()
        self.btnRemoveMode = gtk.ToolButton()
        self.btnCalculate = gtk.ToolButton()
        self.btnSave = gtk.ToolButton()

        self.vbxFunction = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxFunction.pack_start(toolbar, expand=False)
        self.vbxFunction.pack_start(self.notebook)

# Create the General Data tab.
        self.chkSafetyCritical = _widg.make_check_button(_label_=_(u"Function is safety critical."))
        self.txtCode = _widg.make_entry()
        self.txtTotalCost = _widg.make_entry(editable=False, bold=True)
        self.txtName = _widg.make_text_view(width=400)
        self.txtModeCount = _widg.make_entry(editable=False, bold=True)
        self.txtPartCount = _widg.make_entry(editable=False, bold=True)
        self.txtRemarks = _widg.make_text_view(width=400)
        if self._general_data_widgets_create():
            self._app.debug_log.error("function.py: Failed to create General Data tab widgets.")
        if self._general_data_tab_create():
            self._app.debug_log.error("function.py: Failed to create General Data tab.")

# Create the Functional Matrix tab.
# TODO: Move the functional matrix to the parts window?
        self.scwFunctionMatrix = gtk.ScrolledWindow()
        if self._functional_matrix_tab_create():
            self._app.debug_log.error("function.py: Failed to create Functional Matrix tab.")

        # ----- ----- ----- --- Create the Diagrams tab --- ----- ----- ----- #
        # TODO: Implement Diagram Worksheet for FUNCTION.

# Create the Calculation Results tab.
        self.txtPredictedHt = _widg.make_entry(editable=False, bold=True)
        self.txtMissionHt = _widg.make_entry(editable=False, bold=True)
        self.txtMTBF = _widg.make_entry(editable=False, bold=True)
        self.txtMissionMTBF = _widg.make_entry(editable=False, bold=True)
        self.txtMPMT = _widg.make_entry(editable=False, bold=True)
        self.txtMCMT = _widg.make_entry(editable=False, bold=True)
        self.txtMTTR = _widg.make_entry(editable=False, bold=True)
        self.txtMMT = _widg.make_entry(editable=False, bold=True)
        self.txtAvailability = _widg.make_entry(editable=False, bold=True)
        self.txtMissionAt = _widg.make_entry(editable=False, bold=True)
        if self._assessment_results_widgets_create():
            self._app.debug_log.error("function.py: Failed to create Assessment Results widgets.")
        if self._assessment_results_tab_create():
            self._app.debug_log.error("function.py: Failed to create Assessment Results tab.")

        # ----- ----- ----- Create the FMECA Worksheet tab  ----- ----- ----- #
        bg_color = _conf.RTK_COLORS[6]
        fg_color = _conf.RTK_COLORS[7]
        (self.tvwFMECA,
         self._FMECA_col_order) = _widg.make_treeview('FFMECA', 18,
                                                      self._app,
                                                      None,
                                                      bg_color,
                                                      fg_color)

        if self._fmeca_tab_create():
            self._app.debug_log.error("function.py: Failed to create FMECA tab.")

        self._ready = True

    def _toolbar_create(self):
        """ Method to create a toolbar for the FUNCTION Object work book. """

        toolbar = gtk.Toolbar()

        _pos = 0

# Add sibling function button.
        self.btnAddSibling.set_tooltip_text(_("Adds a new function at the same indenture level as the selected function (i.e., a sibling function)."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        self.btnAddSibling.set_icon_widget(image)
        self.btnAddSibling.connect('clicked', self.function_add, 0)
        toolbar.insert(self.btnAddSibling, _pos)
        _pos += 1

# Add child function button.
        self.btnAddChild.set_tooltip_text(_("Adds a new function one indenture level subordinate to the selected function (i.e., a child function)."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        self.btnAddChild.set_icon_widget(image)
        self.btnAddChild.connect('clicked', self.function_add, 1)
        toolbar.insert(self.btnAddChild, _pos)
        _pos += 1

# Add a failure mode button.
        self.btnAddMode.set_tooltip_text(_("Adds a failure mode to the currently selected function."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAddMode.set_icon_widget(image)
        self.btnAddMode.connect('clicked', self._failure_mode_add)
        toolbar.insert(self.btnAddMode, _pos)
        _pos += 1

# Delete function button
        self.btnRemoveFunction.set_tooltip_text(_("Removes the currently selected function."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveFunction.set_icon_widget(image)
        self.btnRemoveFunction.connect('clicked', self.function_delete)
        toolbar.insert(self.btnRemoveFunction, _pos)
        _pos += 1

# Delete a failure mode button.
        self.btnRemoveMode.set_tooltip_text(_("Removes the currently selected failure mode."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveMode.set_icon_widget(image)
        self.btnRemoveMode.connect('clicked', self._failure_mode_delete)
        toolbar.insert(self.btnRemoveMode, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Calculate function button
        self.btnCalculate.set_tooltip_text(_("Calculate the functions."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnCalculate.set_icon_widget(image)
        self.btnCalculate.connect('clicked', _calc.calculate_project, self._app, 2)
        toolbar.insert(self.btnCalculate, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Save function button.
        self.btnSave.set_tooltip_text(_("Saves changes to the selected function."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSave.set_icon_widget(image)
        self.btnSave.set_name('Save')
        self.btnSave.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnSave, _pos)
        _pos += 1

        toolbar.show()

        self.btnAddMode.hide()
        self.btnRemoveMode.hide()

        return(toolbar)

    def _general_data_widgets_create(self):
        """ Method to create the General Data widgets. """

        self.chkSafetyCritical.set_tooltip_text(_("Indicates whether or not the selected function is safety critical."))

        self.txtName.set_tooltip_text(_("Enter the name of the selected function."))
        self.txtName.get_child().get_child().connect('focus-out-event',
                                                     self._callback_entry,
                                                     'text', 14)

        self.txtRemarks.set_tooltip_text(_("Enter any remarks related to the selected function."))
        self.txtRemarks.get_child().get_child().connect('focus-out-event',
                                                        self._callback_entry,
                                                        'text', 15)

        self.txtCode.set_tooltip_text(_("Enter a unique code for the selected function."))
        self.txtCode.connect('focus-out-event',
                             self._callback_entry, 'text', 4)
        self.txtTotalCost.set_tooltip_text(_("Displays the total cost of the selected function."))
        self.txtModeCount.set_tooltip_text(_("Displays the total number of failure modes associated with the selected function."))
        self.txtPartCount.set_tooltip_text(_("Displays the total number of components associated with the selected function."))

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it
        with the appropriate widgets.
        """

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        y_pos = 5

        label = _widg.make_label(self._gd_tab_labels[0][0],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtCode, 155, y_pos)
        y_pos += 30

        label = _widg.make_label(self._gd_tab_labels[0][1],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtName, 155, y_pos)
        y_pos += 110

        label = _widg.make_label(self._gd_tab_labels[0][2],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtTotalCost, 155, y_pos)
        y_pos += 30
        label = _widg.make_label(self._gd_tab_labels[0][3],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtModeCount, 155, y_pos)
        y_pos += 30
        label = _widg.make_label(self._gd_tab_labels[0][4],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtPartCount, 155, y_pos)
        y_pos += 30

        label = _widg.make_label(self._gd_tab_labels[0][5], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRemarks, 155, y_pos)
        y_pos += 110

        fixed.put(self.chkSafetyCritical, 5, y_pos)

        fixed.show_all()

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("General\nData") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_("Displays general information for the selected function."))
        label.show_all()
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the FUNCTION Object.
        """

        self.txtCode.set_text(str(self.model.get_value(self.selected_row, 4)))
        self.txtTotalCost.set_text(str(locale.currency(self.model.get_value(self.selected_row, 5))))
        textbuffer = self.txtName.get_child().get_child().get_buffer()
        textbuffer.set_text(self.model.get_value(self.selected_row, 14))
        textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
        _text_ = self.model.get_value(self.selected_row, 15)
        _text_ = _util.none_to_string(_text_)
        textbuffer.set_text(_text_)
        self.txtModeCount.set_text(str('{0:0.0f}'.format(self.model.get_value(self.selected_row, 16))))
        self.txtPartCount.set_text(str('{0:0.0f}'.format(self.model.get_value(self.selected_row, 17))))

        return False

    def _functional_matrix_tab_create(self):
        """ Method to create the functional matrix tab. """

        # Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Functional\nMatrix") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_("Displays the hardware/function cross-reference matrix."))
        label.show_all()
        self.notebook.insert_page(self.scwFunctionMatrix,
                                  tab_label=label,
                                  position=-1)

        return False

    def _functional_matrix_tab_load(self):
        """
        Creates the TreeView wisget to display the Hardware/Function
        relationship matrix.
        """

        import pango

        functions = []
        row = self.model.get_iter_root()
        while row is not None:
            function_id = self.model.get_value(row, 1)
            code = self.model.get_value(row, 4)
            name = self.model.get_value(row, 14)
            functions.append([function_id, name, code])
            if(self.model.iter_has_child(row)):
                n_children = self.model.iter_n_children(row)
                for i in range(n_children):
                    crow = self.model.iter_nth_child(row, i)
                    function_id = self.model.get_value(crow, 1)
                    code = self.model.get_value(crow, 4)
                    name = self.model.get_value(crow, 14)
                    functions.append([function_id, name, code])

            row = self.model.iter_next(row)

        if(_conf.RTK_MODULES[0] == 1):
            _values = (self._app.REVISION.revision_id,)
        else:
            _values = (0,)
        _assemblies = True
        if(_assemblies):
            query = "SELECT t1.fld_assembly_id, t1.fld_function_id, \
                            t2.fld_ref_des \
                     FROM tbl_functional_matrix AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t2.fld_assembly_id = t1.fld_assembly_id \
                     WHERE t2.fld_revision_id=%d" % _values
        else:
            query = "SELECT t1.fld_assembly_id, t1.fld_function_id, \
                            t2.fld_ref_des \
                     FROM tbl_functional_matrix AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t2.fld_assembly_id = t1.fld_assembly_id \
                     WHERE t2.fld_revision_id=%d \
                     AND t2.fld_part=1" % _values

        _assemblies = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

        if(_assemblies == ''):
            return True

        temp_asmb_id = []
        asmb_dict = {}
        for i in range(len(_assemblies)):
            temp_asmb_id.append(_assemblies[i][0])
            asmb_dict[_assemblies[i][2]] = _assemblies[i][0]

        temp_asmb_id = list(set(temp_asmb_id))

        temp_func_id = []
        for i in range(len(functions)):
            temp_func_id.append(functions[i][0])

        _datamap = [["" for i in range(len(temp_func_id) + 1)] for j in range(len(temp_asmb_id))]

        for i in range(len(_assemblies)):
            try:
                assembly_id = temp_asmb_id.index(_assemblies[i][0])
                function_id = temp_func_id.index(_assemblies[i][1])
                _datamap[assembly_id][0] = _assemblies[i][2] # Ref Des.
                _datamap[assembly_id][function_id + 1] = "<span foreground='black' background='black'> X </span>"
            except ValueError:
                try:
                    assembly_id = temp_asmb_id.index(_assemblies[i][0])
                    _datamap[assembly_id][0] = _assemblies[i][2] # Ref Des.
                    _datamap[assembly_id][1] = ""
                except IndexError:          # Nothing to add.
                    pass

        _datamap = sorted(_datamap, key=lambda _datamap: _datamap[0])

# Make the treeview to display the functional matrix.
        n_functions = len(functions)
        types = ['gchararray'] * (n_functions + 1)
        types = [gobject.type_from_name(types[i]) for i in range(len(types))]
        treemodel = gtk.TreeStore(*types)

        self._FunctionMatrix = gtk.TreeView(treemodel)
        self._FunctionMatrix.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        column = self._FunctionMatrix.get_column(0)
        while column is not None:
            self._FunctionMatrix.remove_column(column)
            column = self._FunctionMatrix.get_column(0)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('cell_background_gdk', gtk.gdk.Color('grey'))
        cell.set_property('font_desc', pango.FontDescription("bold 10"))
        column = gtk.TreeViewColumn()
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 0)
        label = gtk.Label(column.get_title())
        text = "<span weight='bold'>%s</span>" % _("Reference Designator")
        label.set_markup(text)
        column.set_widget(label)
        self._FunctionMatrix.append_column(column)

# List store for cell renderer.
        cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        cellmodel.append([""])
        cellmodel.append(["X"])

        for i in range(n_functions):
            cell = gtk.CellRendererCombo()
            cell.set_property('editable', True)
            cell.set_property('has-entry', False)
            cell.set_property('xalign', 0.5)
            cell.set_property('model', cellmodel)
            cell.set_property('text-column', 0)
            cell.connect('edited', self._edit_functional_matrix, i + 1,
                         temp_func_id, asmb_dict)
            column = gtk.TreeViewColumn()
            column.set_resizable(True)
            column.pack_end(cell)
            column.set_attributes(cell, markup = i + 1)
            label = gtk.Label(column.get_title())
            label.set_property('angle', 90)
            label.set_tooltip_text(functions[i][1])
            label.set_markup("<span weight='bold'>" + functions[i][2] + "</span>")
            label.show_all()
            column.set_widget(label)
            column.connect('notify::width', _widg.resize_wrap, cell)
            self._FunctionMatrix.append_column(column)

        column = gtk.TreeViewColumn("")
        column.set_resizable(True)
        self._FunctionMatrix.append_column(column)

        for i in range(len(_datamap)):
            if(_datamap[i][0] != ''):
                row = treemodel.append(None, _datamap[i])

        if(self.scwFunctionMatrix.get_child() is not None):
            self.scwFunctionMatrix.get_child().destroy()

        self.scwFunctionMatrix.add(self._FunctionMatrix)
        self.scwFunctionMatrix.show_all()

        return False

    def _assessment_results_widgets_create(self):
        """ Method to create Assessment Results widgets. """

# Create quadrant 1 (upper left) widgets.
        self.txtPredictedHt.set_tooltip_text(_("Displays the predicted failure intensity for the selected function."))
        self.txtMissionHt.set_tooltip_text(_("Displays the mission failure intensity for the selected function."))
        self.txtMTBF.set_tooltip_text(_("Displays the limiting mean time between failure (MTBF) for the selected function."))
        self.txtMissionMTBF.set_tooltip_text(_("Displays the mission mean time between failure (MTBF) for the selected function."))

# Create quadrant 2 (upper right) widgets.
        self.txtMPMT.set_tooltip_text(_("Displays the mean preventive maintenance time (MPMT) for the selected function."))
        self.txtMCMT.set_tooltip_text(_("Displays the mean corrective maintenance time (MCMT) for the selected function."))
        self.txtMTTR.set_tooltip_text(_("Displays the mean time to repair (MTTR) for the selected function."))
        self.txtMMT.set_tooltip_text(_("Displays the mean maintenance time (MMT) for the selected function."))
        self.txtAvailability.set_tooltip_text(_("Displays the limiting availability for the selected function."))
        self.txtMissionAt.set_tooltip_text(_("Displays the mission availability for the selected function."))

        return False

    def _assessment_results_tab_create(self):
        """
        Method to create the Calculation Results gtk.Notebook tab and populate
        it with the appropriate widgets.
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
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.txtPredictedHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMTBF, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionMTBF, 155, y_pos)

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
            fixed.put(label, 5, (30 * i + y_pos))

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
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Assessment\nResults") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_("Displays reliability, maintainability, and availability assessment results for the selected function."))
        label.show_all()
        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _assessment_results_tab_load(self):
        """
        Loads the widgets with calculation results for the Function Object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self.txtAvailability.set_text(str(fmt.format(self.model.get_value(self.selected_row, 2))))
        self.txtMissionAt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 3))))
        self.txtMissionHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 6))))
        self.txtPredictedHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 7))))

        self.txtMMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 8))))
        self.txtMCMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 9))))
        self.txtMPMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 10))))

        self.txtMissionMTBF.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 11))))
        self.txtMTBF.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 12))))
        self.txtMTTR.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 13))))

        return False

    def _fmeca_tab_create(self):
        """
        Method to create the FMECA gtk.Notebook tab and populate it with the
        appropriate widgets.
        """

# Load the severity classification gtk.CellRendererCombo.
        _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[11])
        _cell_ = _column_.get_cell_renderers()
        _cellmodel_ = _cell_[0].get_property('model')
        _cellmodel_.clear()
        _query_ = "SELECT fld_criticality_id, fld_criticality_name, \
                          fld_criticality_cat \
                   FROM tbl_criticality"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)

        if(_results_ == '' or not _results_ or _results_ is None):
            _util.application_error(_(u"There was a problem loading the failure criticality list in the Function Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _n_crit_ = len(_results_)
            _cellmodel_.append([""])
            for i in range(_n_crit_):
                _cellmodel_.append([_results_[i][2] + " - " + _results_[i][1]])

# Load the qualitative failure probability gtk.CellRendererCombo.
        _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[13])
        _cell_ = _column_.get_cell_renderers()
        _cellmodel_ = _cell_[0].get_property('model')
        _cellmodel_.clear()
        _query_ = "SELECT * FROM tbl_failure_probability"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)

        if(_results_ == '' or not _results_ or _results_ is None):
            _util.application_error(_(u"There was a problem loading the failure probability list in the Function Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _n_probs_ = len(_results_)
            _cellmodel_.append([""])
            for i in range(_n_probs_):
                _cellmodel_.append([_results_[i][1]])

# Load the RPN severity and RPN severity new gtk.CellRendererCombo.
        _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[20])
        _cell_ = _column_.get_cell_renderers()
        _cellmodel1_ = _cell_[0].get_property('model')
        _cellmodel1_.clear()
        _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[21])
        _cell_ = _column_.get_cell_renderers()
        _cellmodel2_ = _cell_[0].get_property('model')
        _cellmodel2_.clear()
        _query_ = "SELECT fld_severity_name \
                   FROM tbl_rpn_severity \
                   WHERE fld_fmeca_type=0"
        _results_ = self._app.COMDB.execute_query(_query_,
                                                  None,
                                                  self._app.ComCnx)

        if(_results_ == '' or not _results_ or _results_ is None):
            _util.application_error(_(u"There was a problem loading the RPN Severity list in the Function Work Book FMEA/FMECA tab.  This may indicate your RTK common database is corrupt or out of date."))
        else:
            _n_sev_ = len(_results_)
            _cellmodel1_.append([""])
            _cellmodel2_.append([""])
            for i in range(_n_sev_):
                _cellmodel1_.append([_results_[i][0]])
                _cellmodel2_.append([_results_[i][0]])

        #self.tvwFMECA.connect('cursor_changed',
        #                      self._fmeca_treeview_row_changed, None, None)
        #self.tvwFMECA.connect('row_activated',
        #                      self._fmeca_treeview_row_changed)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwFMECA)

        frame = _widg.make_frame(_label_=_(u"Failure Mode, Effects, and Criticality Analysis"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _(u"FMEA/FMECA\nWorksheet")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_(u"Failure mode, effects, and criticality analysis (FMECA) for the selected function."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _fmeca_tab_load(self):
        """ Method to load the FMECA tab information. """

        _model_ = self.tvwFMECA.get_model()
        _model_.clear()

# Load the mission phase gtk.CellRendererCombo.
        _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[2])
        _cell_ = _column_.get_cell_renderers()
        _cellmodel_ = _cell_[0].get_property('model')
        _cellmodel_.clear()

        _query_ = "SELECT fld_phase_id, fld_phase_name, fld_phase_start, \
                        fld_phase_end \
                   FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d" % 0
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(not _results_ or _results_ == '' or _results_ is None):
            _util.application_error(_(u"There was a problem loading the mission phase list in the Function Work Book FMEA/FMECA tab.  This may indicate your RTK program database is corrupt."))
        else:
            _phases_ = len(_results_)
            _cellmodel_.append([""])
            for i in range(_phases_):
                _cellmodel_.append([_results_[i][1]])

# Load the FMEA/FMECA worksheet.
        _query_ = "SELECT fld_mode_id, fld_mode_description, \
                          fld_mission_phase, fld_local_effect, \
                          fld_next_effect, fld_end_effect, \
                          fld_detection_method, fld_other_indications, \
                          fld_isolation_method, fld_design_provisions, \
                          fld_operator_actions, fld_severity_class, \
                          fld_hazard_rate_source, fld_failure_probability, \
                          fld_effect_probability, fld_mode_ratio, \
                          fld_mode_failure_rate, fld_mode_op_time, \
                          fld_mode_criticality, fld_rpn_severity, \
                          fld_rpn_severity_new, fld_critical_item, \
                          fld_single_point, fld_remarks \
                   FROM tbl_fmeca \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=0 \
                   AND fld_function_id=%d" % (self._app.REVISION.revision_id,
                                              self.function_id)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(not _results_ or _results_ == ''):
            return True

        _n_modes_ = len(_results_)
        icon = _conf.ICON_DIR + '32x32/mode.png'
        icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
        for i in range(_n_modes_):
            _data_ = [_results_[i][0],
                      _util.none_to_string(_results_[i][1]),
                      _util.none_to_string(_results_[i][2]),
                      _util.none_to_string(_results_[i][3]),
                      _util.none_to_string(_results_[i][4]),
                      _util.none_to_string(_results_[i][5]),
                      _util.none_to_string(_results_[i][6]),
                      _util.none_to_string(_results_[i][7]),
                      _util.none_to_string(_results_[i][8]),
                      _util.none_to_string(_results_[i][9]),
                      _util.none_to_string(_results_[i][10]),
                      _util.none_to_string(_results_[i][11]),
                      _util.none_to_string(_results_[i][12]),
                      _util.none_to_string(_results_[i][13]),
                      _util.none_to_string(_results_[i][14]),
                      str(_results_[i][15]), str(_results_[i][16]),
                      str(_results_[i][17]), str(_results_[i][18]), "",
                      str(_results_[i][19]), str(_results_[i][20]),
                      _results_[i][21], _results_[i][22],
                      _util.none_to_string(_results_[i][23]),
                      0, '#FFFFFF', True, icon]

            # Load the FMECA gtk.TreeView with the data.
            try:
                _model_.append(None, _data_)
            except TypeError:
                _util.application_error(_(u"Failed to load FMEA/FMECA failure mode %d" % _results_[i][0]))
                pass

        return False

    def create_tree(self):
        """
        Creates the Function TreeView and connects it to callback functions to
        handle editting.  Background and foreground colors can be set using
        the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[2]
        fg_color = _conf.RTK_COLORS[3]
        (self.treeview, self._col_order) = _widg.make_treeview('Function', 1,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)

        self.treeview.set_tooltip_text(_("Displays an indentured list (tree) of functions."))
        self.treeview.set_enable_tree_lines(True)
        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the Function treeview model with system information.  This
        information can be stored either in a MySQL or SQLite3 database.
        """

        if(_conf.RTK_MODULES[0] == 1):
            _values = (self._app.REVISION.revision_id,)
        else:
            _values = (0,)

# Select everything from the function table.
        query = "SELECT * FROM tbl_functions \
                 WHERE fld_revision_id=%d \
                 ORDER BY fld_parent_id" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        if(results == ''):
            return True

        n_records = len(results)
        self.model.clear()
        for i in range(n_records):
            if (results[i][self._col_order[19]] == '-'):
                piter = None
            else:
                piter = self.model.get_iter_from_string(results[i][self._col_order[19]])

            self.model.append(piter, results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

            self.function_id = self.model.get_value(self.selected_row, 1)

            self._functional_matrix_tab_load()

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Hardware Object
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
        Callback function to handle events for the Function Object treeview.
        It is called whenever the Function Object treeview is clicked or a row
        is activated.  It will save the previously selected row in the
        Function Object treeview.

        Keyword Arguments:
        treeview -- the Function Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        selection = self.treeview.get_selection()
        (self.model, self.selected_row) = selection.get_selected()

        if self.selected_row is not None:
            #self._app.winParts.filter_parts_list(1)
            self.function_id = self.model.get_value(self.selected_row, 1)
            self.load_notebook()

            return False
        else:
            return True

    def _update_tree(self, columns, values):
        """
        Updates the values in the Function Object TreeView.

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the Function Object TreeView.
        """

        for i in columns:
            self.model.set_value(self.selected_row, i, values[i])

        return False

    def function_add(self, widget, type_):
        """
        Adds a new Function to the Program's MySQL database.

        Keyword Arguments:
        widget -- the widget that called this function.
        type_  -- the type of Function to add; 0 = sibling, 1 = child.
        """

        # Find the selected function.
        selection = self.treeview.get_selection()
        (model, self.selected_row) = selection.get_selected()

        if(type_ == 0):
            _parent = "-"
            if self.selected_row is not None:
                prow = self.model.iter_parent(self.selected_row)
                if prow is not None:
                    _parent = self.model.get_string_from_iter(prow)

            _title_ = _(u"RTK - Add Sibling Functions")
            _prompt_ = _(u"How many sibling functions to add?")

        elif(type_ == 1):
            _parent = "-"
            if self.selected_row is not None:
                _parent = self.model.get_string_from_iter(self.selected_row)

            _title_ = _(u"RTK - Add Child Functions")
            _prompt_ = _(u"How many child functions to add?")

        n_functions = _util.add_items(_title_, _prompt_)

        for i in range(n_functions):
            _code = str(_conf.RTK_PREFIX[2]) + ' ' + \
                    str(_conf.RTK_PREFIX[3])

            _conf.RTK_PREFIX[3] = _conf.RTK_PREFIX[3] + 1

            function_name = "New Function_" + str(i)

            if(_conf.RTK_MODULES[0] == 1):
                values = (self._app.REVISION.revision_id,
                          function_name, '', _code, _parent)
            else:
                values = (0, function_name, '', _code, _parent)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_functions \
                        (fld_revision_id, fld_name, fld_remarks, fld_code, \
                         fld_parent_id) \
                        VALUES (%d, '%s', '%s', '%s', '%s')"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_functions \
                        (fld_revision_id, fld_name, fld_remarks, fld_code, \
                         fld_parent_id) \
                        VALUES (?, ?, ?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("function.py: Failed to add new function to function table.")
                return True

            if(_conf.BACKEND == 'mysql'):
                query = "SELECT LAST_INSERT_ID()"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "SELECT seq \
                         FROM sqlite_sequence \
                         WHERE name='tbl_functions'"

            function_id = self._app.DB.execute_query(query,
                                                     None,
                                                     self._app.ProgCnx)
            values = (function_id[0][0],)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_functional_matrix \
                        (fld_function_id) \
                        VALUES (%d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_function_id) \
                         VALUES (?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("function.py: Failed to add new function to function table.")
                return True

        self._app.REVISION.load_tree()
        self.load_tree()
        self._functional_matrix_tab_load()

        return False

    def function_delete(self, menuitem):
        """
        Deletes the currently selected Function from the Program's MySQL or
        SQLit3 database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        """

        selection = self.treeview.get_selection()
        (model, row) = selection.get_selected()

        values = (model.get_string_from_iter(row),)
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_functions \
                     WHERE fld_parent_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_functions \
                     WHERE fld_parent_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.user_log.error("function.py: Failed to delete function from function table.")
            return True

        values = (self._app.REVISION.revision_id, \
                  model.get_value(row, 1))
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_functions \
                     WHERE fld_revision_id=%d \
                     AND fld_function_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_functions \
                     WHERE fld_revision_id=? \
                     AND fld_function_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)
        if not results:
            self._app.user_log.error("function.py: Failed to delete function from function table.")
            return True

        self.load_tree()

        return False

    def function_save(self):
        """
        Saves the Function Object treeview information to the Program's
        MySQL or SQLite3 database.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _failure_mode_add(self, button):
        """
        Method to add a failure mode to the FMEA/FMECA for the selected
        function.

        Keyword Arguments:
        button -- the gtk.Toolbutton that called this function.
        """

# Find the id of the next failure mode.
        _query_ = "SELECT seq FROM sqlite_sequence \
                   WHERE name='tbl_fmeca'"
        _last_id_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(not _last_id_):
            _last_id_ = 0
        else:
            _last_id_ = _last_id_[0][0] + 1

# Insert the new failure mode.
        _query_ = "INSERT INTO tbl_fmeca \
                   (fld_revision_id, fld_assembly_id, \
                    fld_function_id, fld_mode_id) \
                   VALUES (%d, 0, %d, %d)" % \
                   (self._app.REVISION.revision_id,
                    self.function_id, _last_id_)
        self._app.DB.execute_query(_query_,
                                   None,
                                   self._app.ProgCnx,
                                   commit=True)

        return False

    def _failure_mode_delete(self, button):
        """
        Method to delete the currently selected failure mode from the
        FMEA/FMECA for the selected function.

        Keyword Arguments:
        button -- the gtk.Toolbutton that called this function.
        """

        _selection_ = self.tvwFMECA.get_selection()
        (_model_, _row_) = _selection_.get_selected()

        _mode_id_ = _model_.get_value(_row_, 0)

        _query_ = "DELETE FROM tbl_fmeca \
                   WHERE fld_function_id=%d \
                   AND fld_mode_id=%d" % (self.function_id, _mode_id_)
        self._app.DB.execute_query(_query_,
                                   None,
                                   self._app.ProgCnx,
                                   commit=True)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the Function Object treeview model to the MySQL or
        SQLite3 database.

        Keyword Arguments:
        model -- the Function Object treemodel.
        path_ -- the path of the active row in the Function Object
                 treemodel.
        row   -- the selected row in the Function Object treeview.
        """

        values = (model.get_value(row, self._col_order[2]), \
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
                  self._app.REVISION.revision_id, \
                  model.get_value(row, self._col_order[1]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_functions \
                     SET fld_availability=%f, fld_availability_mission=%f, \
                         fld_code='%s', fld_cost=%f, fld_failure_rate_mission=%f, \
                         fld_failure_rate_predicted=%f, fld_mmt=%f, fld_mcmt=%f, \
                         fld_mpmt=%f, fld_mtbf_mission=%f, fld_mtbf_predicted=%f, \
                         fld_mttr=%f, fld_name='%s', fld_remarks='%s', \
                         fld_total_mode_quantity=%d, fld_total_part_quantity=%d, \
                         fld_type=%d, fld_parent_id='%s' \
                     WHERE fld_revision_id=%d \
                     AND fld_function_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_functions \
                     SET fld_availability=?, fld_availability_mission=?, \
                         fld_code=?, fld_cost=?, fld_failure_rate_mission=?, \
                         fld_failure_rate_predicted=?, fld_mmt=?, fld_mcmt=?, \
                         fld_mpmt=?, fld_mtbf_mission=?, fld_mtbf_predicted=?, \
                         fld_mttr=?, fld_name=?, fld_remarks=?, \
                         fld_total_mode_quantity=?, fld_total_part_quantity=?, \
                         fld_type=?, fld_parent_id=? \
                     WHERE fld_revision_id=? \
                     AND fld_function_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("function.py: Failed to save function to function table.")
            return True

        return False

    def _fmeca_save(self):
        """
        Saves the ASSEMBLY Object FMECA gtk.TreeView information to the
        Program's MySQL or SQLite3 database.
        """

        _model_ = self.tvwFMECA.get_model()
        _model_.foreach(self._fmeca_save_line_item)

        return False

    def _fmeca_save_line_item(self, model, path, row):
        """
        Saves each row in the Assembly Object FMEA/FMECA treeview model to the
        open RTK database.

        Keyword Arguments:
        model -- the Assembly Object similar item analysis gtk.TreeModel.
        path  -- the path of the active row in the Assembly Object
                 similar item analysis gtk.TreeModel.
        row   -- the selected row in the Assembly Object similar item
                 analysis gtk.TreeView.
        """

# Update the FMECA table.
        _values_ = (model.get_value(row, self._FMECA_col_order[1]), \
                    model.get_value(row, self._FMECA_col_order[2]), \
                    model.get_value(row, self._FMECA_col_order[3]), \
                    model.get_value(row, self._FMECA_col_order[4]), \
                    model.get_value(row, self._FMECA_col_order[5]), \
                    model.get_value(row, self._FMECA_col_order[6]), \
                    model.get_value(row, self._FMECA_col_order[7]), \
                    model.get_value(row, self._FMECA_col_order[8]), \
                    model.get_value(row, self._FMECA_col_order[9]), \
                    model.get_value(row, self._FMECA_col_order[10]), \
                    model.get_value(row, self._FMECA_col_order[11]), \
                    model.get_value(row, self._FMECA_col_order[12]), \
                    model.get_value(row, self._FMECA_col_order[13]), \
                    float(model.get_value(row, self._FMECA_col_order[14])), \
                    float(model.get_value(row, self._FMECA_col_order[15])), \
                    float(model.get_value(row, self._FMECA_col_order[16])), \
                    float(model.get_value(row, self._FMECA_col_order[17])), \
                    float(model.get_value(row, self._FMECA_col_order[18])), \
                    model.get_value(row, self._FMECA_col_order[20]), \
                    model.get_value(row, self._FMECA_col_order[21]),
                    int(model.get_value(row, self._FMECA_col_order[22])), \
                    int(model.get_value(row, self._FMECA_col_order[23])), \
                    model.get_value(row, self._FMECA_col_order[24]), \
                    int(model.get_value(row, self._FMECA_col_order[0])))

        _query_ = "UPDATE tbl_fmeca \
                   SET fld_mode_description='%s', fld_mission_phase='%s', \
                       fld_local_effect='%s', fld_next_effect='%s', \
                       fld_end_effect='%s', fld_detection_method='%s', \
                       fld_other_indications='%s', \
                       fld_isolation_method='%s', \
                       fld_design_provisions='%s', \
                       fld_operator_actions='%s', \
                       fld_severity_class='%s', \
                       fld_hazard_rate_source='%s', \
                       fld_failure_probability='%s', \
                       fld_effect_probability=%f, \
                       fld_mode_ratio=%f, fld_mode_failure_rate=%f, \
                       fld_mode_op_time=%f, fld_mode_criticality=%f, \
                       fld_rpn_severity='%s', fld_rpn_severity_new='%s', \
                       fld_critical_item=%d, fld_single_point=%d, \
                       fld_remarks='%s' \
                   WHERE fld_mode_id=%d" % _values_
        self._app.DB.execute_query(_query_,
                                   None,
                                   self._app.ProgCnx,
                                   commit=True)

        return False

    def _edit_functional_matrix(self, cell, path_, new_text,
                                column, functions, assemblies):
        """
        Callback function to save changes made to the functional matrix
        TreeView.

        Keyword Arguments:
        cell       -- the CellRenderer that was edited.
        path_      -- the path to the CellRenderer being edited.
        new_text   -- the new text in the CellRenderer being edited.
        column     -- the column number of the CellRenderer being edited.
        functions  -- a list of function ids.
        assemblies -- a dictionary with reference designators as keys and
                      assembly ids as values.
        """

        selection = self._FunctionMatrix.get_selection()
        (model, row) = selection.get_selected()

        if(_conf.RTK_MODULES[0] == 1):
            values = (assemblies[model.get_value(row, 0)],
                      functions[column - 1],
                      self._app.REVISION.revision_id)
        else:
            values = (assemblies[model.get_value(row, 0)],
                      functions[column - 1], 0)

        if(new_text == 'X'):
            new_text = "<span foreground='#0BB213' background='#0BB213'> X </span>"

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_assembly_id, fld_function_id, \
                         fld_revision_id) VALUES (%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_assembly_id, fld_function_id, \
                         fld_revision_id) VALUES (?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("function.py: Failed to save Functional Matrix changes.")
                return True

            # Update the prediction table.
            if(_conf.BACKEND == 'mysql'):
                query = "UPDATE tbl_prediction \
                         SET fld_function_id=%d \
                         WHERE fld_assembly_id=%d \
                         AND fld_revision_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "UPDATE tbl_prediction \
                         SET fld_function_id=? \
                         WHERE fld_assembly_id=? \
                         AND fld_revision_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("function.py: Failed to save Functional Matrix changes.")
                return True

        else:
            new_text = "<span foreground='#FD0202' background='#FD0202'>     </span>"

            if(_conf.BACKEND == 'mysql'):
                query = "DELETE FROM tbl_functional_matrix \
                         WHERE fld_assembly_id=%d \
                         AND fld_function_id=%d \
                         AND fld_revision_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "DELETE FROM tbl_functional_matrix \
                         WHERE fld_assembly_id=? \
                         AND fld_function_id=? \
                        AND fld_revision_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("function.py: Failed to save Functional Matrix changes.")
                return True

            if(_conf.RTK_MODULES[0] == 1):
                values = (assemblies[model.get_value(row, 0)], 0,
                          self._app.REVISION.revision_id)
            else:
                values = (assemblies[model.get_value(row, 0)], 0, 0)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_assembly_id, fld_function_id, fld_revision_id) \
                         VALUES (%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_functional_matrix \
                         (fld_assembly_id, fld_function_id, fld_revision_id) \
                         VALUES (?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("function.py: Failed to save Functional Matrix changes.")
                return True

            # Update the prediction table.
            if(_conf.RTK_MODULES[0] == 1):
                values = (functions[column - 1],
                          self._app.REVISION.revision_id)
            else:
                values = (functions[column - 1], 0)

            if(_conf.BACKEND == 'mysql'):
                query = "UPDATE tbl_prediction \
                         SET fld_function_id=0 \
                         WHERE fld_assembly_id=%d \
                         AND fld_revision_id=%d"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "UPDATE tbl_prediction \
                         SET fld_function_id=0 \
                         WHERE fld_assembly_id=? \
                         AND fld_revision_id=?"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("function.py: Failed to save Functional Matrix changes.")
                return True

        model.set_value(row, column, new_text)

        return False

    def load_notebook(self):
        """ Method to load the FUNCTION Object work book. """

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxFunction)
        self._app.winWorkBook.show_all()

        if self.selected_row is not None:
            self._general_data_tab_load()
            self._functional_matrix_tab_load()
            self._assessment_results_tab_load()
            self._fmeca_tab_load()

        self._app.winWorkBook.set_title(_(u"RTK Work Book: Function"))

        self.notebook.set_current_page(0)

        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        event   -- the gtk.gdk.Event that called this function.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Function Object _attribute list
                   associated with the data from the calling entry.
        """

        if(convert == 'text'):
            if(_index_ == 14):
                textbuffer = self.txtName.get_child().get_child().get_buffer()
                text_ = textbuffer.get_text(*textbuffer.get_bounds())
            elif(_index_ == 15):
                textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
                text_ = textbuffer.get_text(*textbuffer.get_bounds())
            else:
                text_ = entry.get_text()

        elif(convert == 'int'):
            text_ = int(entry.get_text())

        elif(convert == 'float'):
            text_ = float(entry.get_text().replace('$', ''))

        # Update the Function Tree.
        self.model.set_value(self.selected_row, _index_, text_)

        return False

    def _notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the Tree Book notebook page is changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = General Data
                    1 = Functional Matrix
                    2 = Assessment Results
                    3 = FMEA
        """

        if(page_num == 3):                  # FMEA/FMECA tab
            self.btnAddSibling.hide()
            self.btnAddChild.hide()
            self.btnAddMode.show()
            self.btnRemoveFunction.hide()
            self.btnRemoveMode.show()
            self.btnCalculate.show()
            self.btnSave.show()
            self.btnSave.set_tooltip_text(_("Saves changes to Functional FMEA for the selected function.."))
        else:
            self.btnAddSibling.show()
            self.btnAddChild.show()
            self.btnAddMode.hide()
            self.btnRemoveFunction.show()
            self.btnRemoveMode.hide()
            self.btnCalculate.show()
            self.btnSave.show()
            self.btnSave.set_tooltip_text(_("Saves changes to the selected function."))

        return False

    def _toolbutton_pressed(self, widget):
        """
        Method to reacte to the ASSEMBLY Object toolbar button clicked events.

        Keyword Arguments:
        widget -- the toolbar button that was pressed.
        """

        # FMEA roll-up lower level FMEA.
        # FMEA calculate criticality.
        # V&V add new task
        # V&V assign existing task
        # Maintenance planning
        # Maintenance planning save changes to selected maintenance policy
        _button_ = widget.get_name()
        _page_ = self.notebook.get_current_page()

        if(_page_ == 0):                    # General data tab.
            if(_button_ == 'Save'):
                self.function_save()
        elif(_page_ == 1):                  # Functional matrix tab.
            if(_button_ == 'Save'):
                self.function_save()
        elif(_page_ == 2):                  # Assessment results tab.
            if(_button_ == 'Save'):
                self.function_save()
        elif(_page_ == 3):                  # FMECA/FMECA tab.
            if(_button_ == 'Save'):
                self._fmeca_save()
