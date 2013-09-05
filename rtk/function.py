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

        self.vbxFunction = gtk.VBox()
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
        # TODO: Implement FMECA Worksheet for FUNCTION.

        self._ready = True

    def _toolbar_create(self):
        """ Method to create a toolbar for the FUNCTION Object work book. """

        toolbar = gtk.Toolbar()

        _pos = 0

# Add sibling function button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NEW)
        button.set_tooltip_text(_("Adds a new function at the same indenture level as the selected function to the RTK Program database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.function_add, 0)
        toolbar.insert(button, _pos)
        _pos += 1

# Add child function button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_NEW)
        button.set_tooltip_text(_("Adds a new function one indenture level subordinate to the selected function to the RTK Program database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.function_add, 1)
        toolbar.insert(button, _pos)
        _pos += 1

# Delete function button
        button = gtk.ToolButton(stock_id = gtk.STOCK_DELETE)
        button.set_tooltip_text(_("Removes the currently selected function from the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.function_delete)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Calculate function button
        button = gtk.ToolButton(stock_id = gtk.STOCK_NO)
        button.set_tooltip_text(_("Calculate the functions."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        button.connect('clicked', _calc.calculate_project, self._app, 2)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Save function button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)
        button.set_tooltip_text(_("Saves function changes to the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.function_save)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.show()

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
        textbuffer.set_text(self.model.get_value(self.selected_row, 15))
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

            n_functions = _util.add_items(_("Sibling Function"))

        elif(type_ == 1):
            _parent = "-"
            if self.selected_row is not None:
                _parent = self.model.get_string_from_iter(self.selected_row)

            n_functions = _util.add_items(_("Child Function"))

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

    def function_save(self, widget):
        """
        Saves the Function Object treeview information to the Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        widget -- the gtk.Widget that called this method.
        """

        self.model.foreach(self._save_line_item)

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

        if self.selected_row is not None:
            self._general_data_tab_load()
            self._functional_matrix_tab_load()
            self._assessment_results_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxFunction)
        self._app.winWorkBook.show_all()

        self._app.winWorkBook.set_title(_(u"RTK Work Book: Function"))

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
