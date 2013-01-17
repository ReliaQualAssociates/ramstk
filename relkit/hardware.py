#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
the hardware of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.py is part of The RelKit Project
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

# Import other RelKit modules.
import configuration as _conf
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Hardware:
    """
    The HARDWARE meta-class is simply the treeview that holds and displays
    the system tree in the RelKit Treebook.  The HARDWARE meta-class also
    includes functions for interacting with the treeview.
    """

    # TODO: Write code to update notebook widgets when editing the System treeview.

    TARGETS = [('extTreeView', gtk.TARGET_SAME_WIDGET, 1024)]

    def __init__(self, application):
        """
        Initializes the HARDWARE Object.

        Keyword Arguments:
        application -- the RelKit application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.ispart = False
        self.assembly = None
        self._assembly_id = 0
        self.system_ht = 0.0

        self._col_order = []

        # Create an empty dictionary to hold the Assembly ID/Hardware Tree
        # treemodel paths.  This is used to keep the Hardware Tree and the
        # Parts List in sync.
        self._treepaths = {}

        self._ready = True

    def create_tree(self):
        """
        Creates the HARDWARE treeview and connects it to callback functions to
        handle editting.  Background and foreground colors can be set using the
        user-defined values in the RelKit configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RELIAFREE_COLORS[6]
        fg_color = _conf.RELIAFREE_COLORS[7]
        (self.treeview, self._col_order) = _widg.make_treeview('Hardware', 3,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)

        self.treeview.set_tooltip_text(_("Displays an indentured list (tree) of hardware."))
        self.treeview.set_enable_tree_lines(True)
        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the Hardware treeview model with system information.  This
        information can be stored either in a MySQL or SQLite3 database.
        """

        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,)
        else:
            values = (0,)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_system WHERE fld_revision_id=%d"
        if(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_system WHERE fld_revision_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        n_assemblies = len(results)

        _pixbuf = False
        cols = self.treeview.get_columns()
        for i in range(len(cols)):
            if(cols[i].get_visible() is True and _pixbuf is False):
                _viscol = i
                _pixbuf = True

        self.model.clear()
        self.selected_row = None

        # Create an empty dictionary to hold the Assembly ID/Hardware Tree
        # treemodel paths.  This is used to keep the Hardware Tree and the
        # Parts List in sync.
        self._treepaths = {}

        # Load the model with the returned results.
        for i in range(n_assemblies):

            if(results[i][62] == '-'):          # Its the top level element.
                piter = None
                self.system_ht = results[i][32]
            elif(results[i][62] != '-'):        # Its a child element.
                piter = self.model.get_iter_from_string(results[i][62])

            # Select the image to display.  If there is a problem with the
            # part (overstressed, etc.), display the !.  If it is an assembly,
            # display the assembly icon.  If it is a part, display the part
            # icon.
            if(results[i][60] == 1):
                icon = _conf.ICON_DIR + '32x32/overstress.png'
            elif(results[i][63] == 0):
                icon = _conf.ICON_DIR + '32x32/assembly.png'
            else:
                icon = _conf.ICON_DIR + '32x32/part.png'

            icon = gtk.gdk.pixbuf_new_from_file_at_size(icon, 16, 16)
            data_ = results[i] + (icon,)

            row = self.model.append(piter, data_)

            self._treepaths[results[i][68]] = self.model.get_path(row)

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the HARDWARE Object gtk.TreeView.

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the Hardware Object TreeView.
        """

        for i in columns:
            self.model.set_value(self.selected_row, i, values[i])

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the HARDWARE Object
        gtk.TreeView.

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
        Callback function to handle events for the HARDWARE Object
        gtk.TreeView.  It is called whenever the HARDWARE Object gtk.TreeView
        is clicked or a row is activated.  It will save the previously selected
        row in the HARDWARE Object gtk.TreeView and, if the previously
        selected item is a COMPONENT Object, the Parts List.  Then it loads
        the ASSEMBLY Object and, if the newly selected item is a Component,
        the COMPONENT Object.

        Keyword Arguments:
        treeview -- the HARDWARE Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        # Save the previously selected row in the Hardware tree.
        if self.selected_row is not None:
            path_ = self.model.get_path(self.selected_row)
            self._save_line_item(self.model, path_, self.selected_row)

        # Save the previously selected row in the Parts List.
        if self._app.winParts.selected_row is not None and \
           self.selected_row is not None and \
           self.model.get_value(self.selected_row, 63) == 1:
            path_ = self._app.winParts.model.get_path(self._app.winParts.selected_row)
            self._app.winParts.save_line_item(self._app.winParts.model,
                                              path_,
                                              self._app.winParts.selected_row)

        selection = self.treeview.get_selection()
        (self.model, self.selected_row) = selection.get_selected()
        self._assembly_id = self.model.get_value(self.selected_row, 1)

        _path_ = self.model.get_string_from_iter(self.selected_row)

        # Build the queries to select the reliability tests and program
        # incidents associated with the selected HARDWARE.
        if(_conf.BACKEND == 'mysql'):
            qryParts = "SELECT * FROM tbl_system \
                        WHERE fld_part=1 \
                        AND fld_revision_id=%d \
                        AND fld_parent_assembly='%s'"
            qryIncidents = "SELECT * FROM tbl_incident\
                            WHERE fld_revision_id=%d \
                            AND fld_hardware_id=%d \
                            ORDER BY fld_incident_id"
            qryDatasets = "SELECT * FROM tbl_dataset \
                           WHERE fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            qryParts = "SELECT * FROM tbl_system \
                        WHERE fld_part=1 \
                        AND fld_revision_id=? \
                        AND fld_parent_assembly=?"
            qryIncidents = "SELECT * FROM tbl_incident \
                            WHERE fld_revision_id=? \
                            AND fld_hardware_id=? \
                            ORDER BY fld_incident_id"
            qryDatasets = "SELECT * FROM tbl_dataset \
                           WHERE fld_assembly_id=?"

        # Find the current revision if using the revision module, otherwise
        # set this to the default value.
        if(_conf.RELIAFREE_MODULES[0] == 1):
            values1 = (self._app.REVISION.revision_id, _path_)
            values2 = (self._app.REVISION.revision_id, self._assembly_id)
        else:
            values1 = (0, _path_)
            values2 = (0, self._assembly_id)

        self._app.winParts.load_part_tree(qryParts,
                                          values1)
        self._app.winParts.load_incident_tree(qryIncidents,
                                              values2)
        self._app.winParts.load_dataset_tree(qryDatasets,
                                             (self._assembly_id,))

        if self.selected_row is not None:
            if(self.model.get_value(self.selected_row, 63) == 0):
                self.ispart = False
                self.assembly = _path_
                #self._app.winParts.filter_parts_list(3)
                self._app.ASSEMBLY.load_notebook()

            elif(self.model.get_value(self.selected_row, 63) == 1):
                self.ispart = True
                self.assembly = self.model.get_value(self.selected_row, 62)
                #self._app.winParts.filter_parts_list(3)
                self._find_parts_list_row()
                self._app.COMPONENT.load_notebook()

            return False
        else:
            return True

    def _find_parts_list_row(self):
        """
        Finds the corresponding row in the Parts List when a selected row in
        the HARDWARE Object gtk.TreeView is a COMPONENT Object.
        """

        row = self._app.winParts.model.get_iter_first()
        while(self._app.winParts.model.get_value(row, 1) != self._assembly_id):
            row = self._app.winParts.model.iter_next(row)

        if(row is not None):
            self._app.winParts.selected_row = row
            _path_ = self._app.winParts.model.get_path(row)
            self._app.winParts.tvwPartsList.set_cursor(_path_)

        return False

    def hardware_save(self):
        """
        Saves the HARDWARE Object gtk.TreeView information to the Program's
        MySQL or SQLite3 database.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the HARDWARE Object gtk.TreeView model to the
        Program's MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the HARDWARE Object gtk.Treemodel.
        path_ -- the path of the active row in the HARDWARE Object
                 gtk.Treemodel.
        row   -- the selected row in the HARDWARE Object gtk.TreeView.
        """

        if(_conf.BACKEND == 'mysql'):
            ht_model = self._app.ProgCnx.escape_string(model.get_value(row, self._col_order[88]))
        elif(_conf.BACKEND == 'sqlite3'):
            ht_model = model.get_value(row, self._col_order[88])

        values = (model.get_value(row, self._col_order[2]),
                  model.get_value(row, self._col_order[3]),
                  model.get_value(row, self._col_order[4]),
                  model.get_value(row, self._col_order[5]),
                  model.get_value(row, self._col_order[6]),
                  model.get_value(row, self._col_order[7]),
                  model.get_value(row, self._col_order[8]),
                  model.get_value(row, self._col_order[9]),
                  model.get_value(row, self._col_order[10]),
                  model.get_value(row, self._col_order[11]),
                  model.get_value(row, self._col_order[12]),
                  model.get_value(row, self._col_order[13]),
                  model.get_value(row, self._col_order[14]),
                  model.get_value(row, self._col_order[15]),
                  model.get_value(row, self._col_order[16]),
                  model.get_value(row, self._col_order[17]),
                  model.get_value(row, self._col_order[18]),
                  model.get_value(row, self._col_order[19]),
                  model.get_value(row, self._col_order[20]),
                  model.get_value(row, self._col_order[21]),
                  model.get_value(row, self._col_order[22]),
                  model.get_value(row, self._col_order[23]),
                  model.get_value(row, self._col_order[24]),
                  model.get_value(row, self._col_order[25]),
                  model.get_value(row, self._col_order[26]),
                  model.get_value(row, self._col_order[27]),
                  model.get_value(row, self._col_order[28]),
                  model.get_value(row, self._col_order[29]),
                  model.get_value(row, self._col_order[30]),
                  model.get_value(row, self._col_order[31]),
                  model.get_value(row, self._col_order[32]),
                  model.get_value(row, self._col_order[33]),
                  model.get_value(row, self._col_order[34]),
                  model.get_value(row, self._col_order[35]),
                  model.get_value(row, self._col_order[36]),
                  model.get_value(row, self._col_order[37]),
                  model.get_value(row, self._col_order[38]),
                  model.get_value(row, self._col_order[39]),
                  model.get_value(row, self._col_order[40]),
                  model.get_value(row, self._col_order[41]),
                  model.get_value(row, self._col_order[42]),
                  model.get_value(row, self._col_order[43]),
                  model.get_value(row, self._col_order[44]),
                  model.get_value(row, self._col_order[45]),
                  model.get_value(row, self._col_order[46]),
                  model.get_value(row, self._col_order[47]),
                  model.get_value(row, self._col_order[48]),
                  model.get_value(row, self._col_order[49]),
                  model.get_value(row, self._col_order[50]),
                  model.get_value(row, self._col_order[51]),
                  model.get_value(row, self._col_order[52]),
                  model.get_value(row, self._col_order[53]),
                  model.get_value(row, self._col_order[54]),
                  model.get_value(row, self._col_order[55]),
                  model.get_value(row, self._col_order[56]),
                  model.get_value(row, self._col_order[57]),
                  model.get_value(row, self._col_order[58]),
                  model.get_value(row, self._col_order[59]),
                  model.get_value(row, self._col_order[60]),
                  model.get_value(row, self._col_order[61]),
                  model.get_value(row, self._col_order[62]),
                  model.get_value(row, self._col_order[63]),
                  model.get_value(row, self._col_order[64]),
                  model.get_value(row, self._col_order[65]),
                  model.get_value(row, self._col_order[66]),
                  model.get_value(row, self._col_order[67]),
                  model.get_value(row, self._col_order[68]),
                  model.get_value(row, self._col_order[69]),
                  model.get_value(row, self._col_order[70]),
                  model.get_value(row, self._col_order[71]),
                  model.get_value(row, self._col_order[72]),
                  model.get_value(row, self._col_order[73]),
                  model.get_value(row, self._col_order[74]),
                  model.get_value(row, self._col_order[75]),
                  model.get_value(row, self._col_order[76]),
                  model.get_value(row, self._col_order[77]),
                  model.get_value(row, self._col_order[78]),
                  model.get_value(row, self._col_order[79]),
                  model.get_value(row, self._col_order[80]),
                  model.get_value(row, self._col_order[81]),
                  model.get_value(row, self._col_order[82]),
                  model.get_value(row, self._col_order[83]),
                  model.get_value(row, self._col_order[84]),
                  model.get_value(row, self._col_order[85]),
                  model.get_value(row, self._col_order[86]),
                  model.get_value(row, self._col_order[87]),
                  ht_model,
                  model.get_value(row, self._col_order[89]),
                  model.get_value(row, self._col_order[90]),
                  self._app.REVISION.revision_id,
                  model.get_value(row, self._col_order[1]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_system \
                     SET fld_add_adj_factor=%f, fld_allocation_type=%d, \
                         fld_alt_part_number='%s', fld_assembly_criticality=%f, \
                         fld_attachments='%s', fld_availability=%f, \
                         fld_availability_mission=%f, fld_cage_code='%s', \
                         fld_calculation_model=%d, fld_category_id=%d, \
                         fld_comp_ref_des='%s', fld_cost=%f, \
                         fld_cost_failure=%f, fld_cost_hour=%f, \
                         fld_cost_type=%f, fld_description='%s', \
                         fld_detection_fr=%f, fld_detection_percent=%f, \
                         fld_duty_cycle=%f, fld_entered_by='%s', \
                         fld_environment_active=%d, fld_environment_dormant=%d, \
                         fld_failure_dist=%d, fld_failure_parameter_1=%f, \
                         fld_failure_parameter_2=%f, fld_failure_parameter_3=%f, \
                         fld_failure_rate_active=%f, fld_failure_rate_dormant=%f, \
                         fld_failure_rate_mission=%f, fld_failure_rate_percent=%f, \
                         fld_failure_rate_predicted=%f, fld_failure_rate_software=%f, \
                         fld_failure_rate_specified=%f, fld_failure_rate_type=%d, \
                         fld_figure_number='%s', fld_humidity=%f, \
                         fld_image_file='%s', fld_isolation_fr=%f, \
                         fld_isolation_percent=%f, fld_lcn='%s', \
                         fld_level=%d, fld_manufacturer=%d, \
                         fld_mcmt=%f, fld_mission_time=%f, \
                         fld_mmt=%f, fld_modified_by='%s', \
                         fld_mpmt=%f, fld_mtbf_mission=%f, \
                         fld_mtbf_predicted=%f, fld_mtbf_specified=%f, \
                         fld_mttr=%f, fld_mttr_add_adj_factor=%f, \
                         fld_mttr_mult_adj_factor=%f, fld_mttr_specified=%f, \
                         fld_mttr_type=%d, fld_mult_adj_factor=%f, \
                         fld_name='%s', fld_nsn='%s', \
                         fld_overstress=%d, fld_page_number='%s', \
                         fld_parent_assembly='%s', fld_part=%d, \
                         fld_part_number='%s', fld_percent_isolation_group_ri=%f, \
                         fld_percent_isolation_single_ri=%f, fld_quantity=%d, \
                         fld_ref_des='%s', fld_reliability_mission=%f, \
                         fld_reliability_predicted=%f, fld_remarks='%s', \
                         fld_repair_dist=%d, fld_repair_parameter_1=%f, \
                         fld_repair_parameter_2=%f, fld_repairable=%d, \
                         fld_rpm=%f, fld_specification_number='%s', \
                         fld_subcategory_id=%d, fld_tagged_part=%d, \
                         fld_temperature_active=%f, fld_temperature_dormant=%f, \
                         fld_total_part_quantity=%d, fld_total_power_dissipation=%f, \
                         fld_vibration=%f, fld_weibull_data_set=%d, \
                         fld_weibull_file='%s', fld_year_of_manufacture=%d, \
                         fld_ht_model='%s', fld_reliability_goal_measure=%d, \
                         fld_reliability_goal=%f \
                 WHERE fld_revision_id=%d AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_system \
                     SET fld_add_adj_factor=?, fld_allocation_type=?, \
                         fld_alt_part_number=?, fld_assembly_criticality=?, \
                         fld_attachments=?, fld_availability=?, \
                         fld_availability_mission=?, fld_cage_code=?, \
                         fld_calculation_model=?, fld_category_id=?, \
                         fld_comp_ref_des=?, fld_cost=?, \
                         fld_cost_failure=?, fld_cost_hour=?, \
                         fld_cost_type=?, fld_description=?, \
                         fld_detection_fr=?, fld_detection_percent=?, \
                         fld_duty_cycle=?, fld_entered_by=?, \
                         fld_environment_active=?, fld_environment_dormant=?, \
                         fld_failure_dist=?, fld_failure_parameter_1=?, \
                         fld_failure_parameter_2=?, fld_failure_parameter_3=?, \
                         fld_failure_rate_active=?, fld_failure_rate_dormant=?, \
                         fld_failure_rate_mission=?, fld_failure_rate_percent=?, \
                         fld_failure_rate_predicted=?, fld_failure_rate_software=?, \
                         fld_failure_rate_specified=?, fld_failure_rate_type=?, \
                         fld_figure_number=?, fld_humidity=?, \
                         fld_image_file=?, fld_isolation_fr=?, \
                         fld_isolation_percent=?, fld_lcn=?, \
                         fld_level=?, fld_manufacturer=?, \
                         fld_mcmt=?, fld_mission_time=?, \
                         fld_mmt=?, fld_modified_by=?, \
                         fld_mpmt=?, fld_mtbf_mission=?, \
                         fld_mtbf_predicted=?, fld_mtbf_specified=?, \
                         fld_mttr=?, fld_mttr_add_adj_factor=?, \
                         fld_mttr_mult_adj_factor=?, fld_mttr_specified=?, \
                         fld_mttr_type=?, fld_mult_adj_factor=?, \
                         fld_name=?, fld_nsn=?, \
                         fld_overstress=?, fld_page_number=?, \
                         fld_parent_assembly=?, fld_part=?, \
                         fld_part_number=?, fld_percent_isolation_group_ri=?, \
                         fld_percent_isolation_single_ri=?, fld_quantity=?, \
                         fld_ref_des=?, fld_reliability_mission=?, \
                         fld_reliability_predicted=?, fld_remarks=?, \
                         fld_repair_dist=?, fld_repair_parameter_1=?, \
                         fld_repair_parameter_2=?, fld_repairable=?, \
                         fld_rpm=?, fld_specification_number=?, \
                         fld_subcategory_id=?, fld_tagged_part=?, \
                         fld_temperature_active=?, fld_temperature_dormant=?, \
                         fld_total_part_quantity=?, fld_total_power_dissipation=?, \
                         fld_vibration=?, fld_weibull_data_set=?, \
                         fld_weibull_file=?, fld_year_of_manufacture=?,"" \
                         fld_ht_model=?, fld_reliability_goal_measure=?, \
                         fld_reliability_goal=? \
                    WHERE fld_revision_id=? AND fld_assembly_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("hardware.py: Failed to save hardware to system table.")
            return True

        return False
