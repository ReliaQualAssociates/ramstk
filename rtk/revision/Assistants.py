#!/usr/bin/env python
"""
##################################
Revision Package Assistants Module
##################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       Assistants.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
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

# Import other RTK modules.
try:
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class AddRevision(gtk.Dialog):
    """
    This is the assistant that walks the user through the process of adding
    a new revision to the open RTK Program database.
    """

    def __init__(self, controller):
        """
        Initialize on instance of the Add Revision Assistant.

        :param rtk.revision.Revision.Revision controller: the Revision data
                                                          controller instance.
        """

        gtk.Dialog.__init__(self, title=_(u"RTK Revision Addition Assistant"),
                            parent=None,
                            flags=(gtk.DIALOG_MODAL |
                                   gtk.DIALOG_DESTROY_WITH_PARENT),
                            buttons=(gtk.STOCK_APPLY, gtk.RESPONSE_ACCEPT,
                                     gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))

        self._controller = controller
# TODO: Add a checkbox to the assistant to allow the user to select whether or not to duplicate the software structure.
        self.chkFunction = gtk.CheckButton(_(u"_Functions"))
        self.chkFunctionMatrix = gtk.CheckButton(_(u"Functional _Matrix"))
        self.chkRequirements = gtk.CheckButton(_(u"_Requirements"))
        self.chkHardware = gtk.CheckButton(_(u"_Hardware"))
        self.chkFailureInfo = gtk.CheckButton(_(u"Include reliability "
                                                u"information"))
        self.cmbBaseRevision = _widg.make_combo(simple=False)
        self.txtRevisionCode = _widg.make_entry(width=100)
        self.txtRevisionName = _widg.make_entry()
        self.txtRemarks = gtk.TextBuffer()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()
        self.vbox.pack_start(_fixed)        # pylint: disable=E1101

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _query = "SELECT fld_revision_code, fld_name, fld_revision_id \
                  FROM tbl_revisions"
        (_results,
         _error_code, __) = self._controller._dao.execute(_query, commit=False)
        _list = []
        for i in range(len(_results)):
            _list.append([_results[i][0] + '-' + _results[i][1], '',
                          _results[i][2]])
        _widg.load_combo(self.cmbBaseRevision, _list, simple=False)

        _label = _widg.make_label(_(u"This is the RTK Revision Addition "
                                    u"Assistant.  Enter the information "
                                    u"requested below and then press 'Apply' "
                                    u"to add a new Revision to the RTK "
                                    u"Project database."),
                                  width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        _labels = [_(u"Select existing Revision to duplicate:"),
                   _(u"Revision Code:"), _(u"Revision Name:"), _(u"Remarks:")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, _y_pos)
        _x_pos += 50

        # Set the tooltips.
        self.txtRevisionCode.set_tooltip_text(_(u"Enter a code for the new "
                                                u"revision.  Leave blank to "
                                                u"use the default revision "
                                                u"code."))
        self.txtRevisionName.set_tooltip_text(_(u"Enter a name for the new "
                                                u"revision.  Leave blank to "
                                                u"use the default revision "
                                                u"name."))

        # Place the widgets.
        _fixed.put(self.cmbBaseRevision, _x_pos, _y_pos[0])
        _fixed.put(self.txtRevisionCode, _x_pos, _y_pos[1] + 5)
        _fixed.put(self.txtRevisionName, _x_pos, _y_pos[2] + 5)
        _textview = _widg.make_text_view(txvbuffer=self.txtRemarks,
                                         width=300, height=100)
        _fixed.put(_textview, _x_pos, _y_pos[3] + 5)
        _label = _widg.make_label(_(u"Copy the selected information from the "
                                    u"Revision being duplicated..."),
                                  width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, _y_pos[3] + 125)
        _y_pos = _y_pos[3] + _label.size_request()[1] + 130
        _fixed.put(self.chkFunction, 5, _y_pos)
        _fixed.put(self.chkFunctionMatrix, 5, _y_pos + 30)
        _fixed.put(self.chkRequirements, 5, _y_pos + 60)
        _fixed.put(self.chkHardware, 5, _y_pos + 90)
        _fixed.put(self.chkFailureInfo, 5, _y_pos + 120)

        self.show_all()

        #_model = self.cmbBaseRevision.get_model()
        #_row = self.cmbBaseRevision.get_active_iter()
        #_base_revision = int(_model.get_value(_row, 2))

# TODO: Move this to the Function class and simply call it from here.
        #if self.chkFunction.get_active():
        #    _query = "SELECT MAX(fld_function_id) FROM tbl_functions"
        #    _function_id = self._dao.execute(_query, commit=False)

        #    if _function_id[0][0] is not None:
        #        _function_id = _function_id[0][0] + 1

        # Retrieve the information needed to copy the function
        # hierarchy from the base revision to the new revision.
        #        _query = "SELECT fld_code, fld_level, fld_name, \
        #                         fld_parent_id, fld_remarks \
        #                  FROM tbl_functions \
        #                  WHERE fld_revision_id=%d" % _base_revision
        #        _function = self._dao.execute(_query, commit=False)
        #    else:
        #        _function = [('', 0, 'New Function', 0, ''), ]

        #    try:
        #        _n_functions = len(_function)
        #    except TypeError:
        #        _n_functions = 0

            # Copy the function hierarchy for the new revision.
        #    for i in range(_n_functions):
        #        _function_name = _(u"New Function_") + str(i)

        #        _values = (_revision_id, _function_id, _function[i][0],
        #                   _function[i][1], _function[i][2],
        #                   _function[i][3], _function[i][4])
        #        _query = "INSERT INTO tbl_functions \
        #                  (fld_revision_id, fld_function_id, fld_code, \
        #                   fld_level, fld_name, fld_parent_id, \
        #                   fld_remarks) \
        #                  VALUES (%d, %d, '%s', %d, '%s', '%s', '%s')" % \
        #                 _values
        #        self._dao.execute(_query, commit=True)

        #        if self.chkFunctionMatrix.get_active():
        #            _query = "INSERT INTO tbl_functional_matrix \
        #                      (fld_revision_id, fld_function_id) \
        #                      VALUES (%d, %d)" % (_revision_id, _function_id)
        #            self._dao.execute(_query, commit=True)

        #        _function_id += 1
# TODO: Move this to the Requirement class and simply call it from here.
        #    if self.chkRequirements.get_active():
        #        _query = "SELECT MAX(fld_requirement_id) FROM tbl_requirements"
        #        _requirement_id = self._dao.execute(_query, commit=False)

        #        if _requirement_id[0][0] is not None:
        #            _requirement_id = _requirement_id[0][0] + 1

                    # Retrieve the information needed to copy the requirement
                    # hierarchy from the base revision to the new revision.
        #            _query = "SELECT fld_requirement_desc, \
        #                             fld_requirement_code, fld_derived, \
        #                             fld_parent_requirement, fld_owner, \
        #                             fld_specification, fld_page_number, \
        #                             fld_figure_number \
        #                      FROM tbl_requirements \
        #                      WHERE fld_revision_id=%d" % _base_revision
        #            _requirements = self._dao.execute(_query,
        #                                                    commit=False)

        #        try:
        #            _n_requirements = len(_requirements)
        #        except(TypeError, UnboundLocalError):
        #            _n_requirements = 0

                # Copy the requirement hierarchy for the new revision.
        #        for i in range(_n_requirements):
        #            _query = "INSERT INTO tbl_requirements \
        #                      (fld_revision_id, fld_requirement_id, \
        #                       fld_requirement_desc, fld_requirement_code, \
        #                       fld_derived, fld_parent_requirement, \
        #                       fld_owner, fld_specification, \
        #                       fld_page_number, fld_figure_number) \
        #                      VALUES ({0:d}, {1:d}, '{2:s}', '{3:s}', {4:d}, \
        #                              '{5:s}', '{6:s}', '{7:s}', '{8:s}', \
        #                              '{9:s}')".format(
        #                     _revision_id, _requirement_id,
        #                     _requirements[i][0], _requirements[i][1],
        #                     _requirements[i][2], _requirements[i][3],
        #                     _requirements[i][4], _requirements[i][5],
        #                     _requirements[i][6], _requirements[i][7])
        #            self._dao.execute(_query, commit=True)

        #            _requirement_id += 1

        #_query = "SELECT MAX(fld_assembly_id) FROM tbl_system"
        #_assembly_id = self._dao.execute(_query, commit=False)
        #if _assembly_id[0][0] is not None:
        #    _assembly_id = _assembly_id[0][0] + 1

# TODO: Move this to the Hardware class and simply call it from here.
        #if self.chkHardware.get_active():
            # Retrieve the information needed to copy the hardware
            # hierarchy from the base revision to the new revision.
        #    if self.chkFailureInfo.get_active():
        #        _query = "SELECT fld_cage_code, fld_category_id, \
        #                         fld_description, fld_failure_rate_active, \
        #                         fld_failure_rate_dormant, \
        #                         fld_failure_rate_software, \
        #                         fld_failure_rate_specified, \
        #                         fld_failure_rate_type, fld_figure_number, \
        #                         fld_lcn, fld_level, fld_manufacturer, \
        #                         fld_mission_time, fld_name, fld_nsn, \
        #                         fld_page_number, fld_parent_assembly, \
        #                         fld_part, fld_part_number, \
        #                         fld_quantity, fld_ref_des, fld_remarks, \
        #                         fld_specification_number, \
        #                         fld_subcategory_id, fld_mtbf_predicted, \
        #                         fld_mtbf_specified, fld_mtbf_lcl, \
        #                         fld_mtbf_ucl, fld_failure_rate_lcl, \
        #                         fld_failure_rate_ucl \
        #                  FROM tbl_system \
        #                  WHERE fld_revision_id=%d" % _base_revision
        #    else:
        #        _query = "SELECT fld_cage_code, fld_category_id, \
        #                         fld_description, fld_figure_number, \
        #                         fld_lcn, fld_level, fld_manufacturer, \
        #                         fld_mission_time, fld_name, fld_nsn, \
        #                         fld_page_number, fld_parent_assembly, \
        #                         fld_part, fld_part_number, \
        #                         fld_quantity, fld_ref_des, fld_remarks, \
        #                         fld_specification_number, \
        #                         fld_subcategory_id \
        #                  FROM tbl_system \
        #                  WHERE fld_revision_id=%d" % _base_revision
        #    _system = self._dao.execute(_query, commit=False)

        #    try:
        #        _n_hardware = len(_system)
        #    except TypeError:
        #        _n_hardware = 0
            # Copy the hardware hierarchy for the new revision.
        #    for i in range(_n_hardware):
        #        if self.chkFailureInfo.get_active():
        #            _values = (_revision_id, _assembly_id,
        #                       _system[i][0], _system[i][1],
        #                       _system[i][2], _system[i][3],
        #                       _system[i][4], _system[i][5],
        #                       _system[i][6], _system[i][7],
        #                       _system[i][8], _system[i][9],
        #                       _system[i][10], _system[i][11],
        #                       _system[i][12], _system[i][13],
        #                       _system[i][14], _system[i][15],
        #                       _system[i][16], _system[i][17],
        #                       _system[i][18], _system[i][19],
        #                       _system[i][20], _system[i][21],
        #                       _system[i][22], _system[i][23],
        #                       _system[i][24], _system[i][25],
        #                       _system[i][26], _system[i][27],
        #                       _system[i][28], _system[i][29], _who)
        #            _query = "INSERT INTO tbl_system \
        #                      (fld_revision_id, fld_assembly_id, \
        #                       fld_cage_code, fld_category_id, \
        #                       fld_description, fld_failure_rate_active, \
        #                       fld_failure_rate_dormant, \
        #                       fld_failure_rate_software, \
        #                       fld_failure_rate_specified, \
        #                       fld_failure_rate_type, fld_figure_number, \
        #                       fld_lcn, fld_level, fld_manufacturer, \
        #                       fld_mission_time, fld_name, fld_nsn, \
        #                       fld_page_number, fld_parent_assembly, \
        #                       fld_part, fld_part_number, fld_quantity, \
        #                       fld_ref_des, fld_remarks, \
        #                       fld_specification_number, \
        #                       fld_subcategory_id, fld_mtbf_predicted, \
        #                       fld_mtbf_specified, fld_mtbf_lcl, \
        #                       fld_mtbf_ucl, fld_failure_rate_lcl, \
        #                       fld_failure_rate_ucl, fld_entered_by) \
        #                      VALUES (%d, %d, '%s', %d, '%s', %f, %f, \
        #                              %f, %f, %d, '%s', '%s', %d, %d, \
        #                              %f, '%s', '%s', '%s', '%s', %d, \
        #                              '%s', %d, '%s', '%s', '%s', %d, \
        #                              %f, %f, %f, %f, %f, %f, '%s')" % \
        #                     _values
        #            if _system[i][17] == 1:
        #                _part = True
        #            else:
        #                _part = False
        #        else:
        #            _values = (_revision_id, _assembly_id,
        #                       _system[i][0], _system[i][1],
        #                       _system[i][2], _system[i][3],
        #                       _system[i][4], _system[i][5],
        #                       _system[i][6], _system[i][7],
        #                       _system[i][8], _system[i][9],
        #                       _system[i][10], _system[i][11],
        #                       _system[i][12], _system[i][13],
        #                       _system[i][14], _system[i][15],
        #                       _system[i][16], _system[i][17],
        #                       _system[i][18], _who)
        #            _query = "INSERT INTO tbl_system \
        #                      (fld_revision_id, fld_assembly_id, \
        #                       fld_cage_code, fld_category_id, \
        #                       fld_description, fld_figure_number, \
        #                       fld_lcn, fld_level, fld_manufacturer, \
        #                       fld_mission_time, fld_name, fld_nsn, \
        #                       fld_page_number, fld_parent_assembly, \
        #                       fld_part, fld_part_number, fld_quantity, \
        #                       fld_ref_des, fld_remarks, \
        #                       fld_specification_number, \
        #                       fld_subcategory_id, fld_entered_by) \
        #                      VALUES (%d, %d, '%s', %d, '%s', '%s', \
        #                              '%s', %d, %d, %f, '%s', '%s', \
        #                              '%s', '%s', %d, '%s', %d, '%s', \
        #                              '%s', '%s', %d, '%s')" % _values
        #            if _system[i][17] == 1:
        #                _part = True
        #            else:
        #                _part = False

        #        self._dao.execute(_query, commit=True)

        #        _values = (_revision_id, _assembly_id)

                # Add the item to the prediction table if it's a part.
        #        if _part:
        #            _query = "INSERT INTO tbl_prediction \
        #                      (fld_revision_id, fld_assembly_id) \
        #                      VALUES (%d, %d)" % _values
        #            self._dao.execute(_query, commit=True)

        #        _query = "INSERT INTO tbl_allocation \
        #                  (fld_revision_id, fld_assembly_id) \
        #                  VALUES (%d, %d)" % _values
        #        self._dao.execute(_query, commit=True)

        #        _query = "INSERT INTO tbl_risk_analysis \
        #                  (fld_revision_id, fld_assembly_id) \
        #                  VALUES (%d, %d)" % _values
        #        self._dao.execute(_query, commit=True)

        #        _query = "INSERT INTO tbl_similar_item \
        #                  (fld_revision_id, fld_assembly_id) \
        #                 VALUES (%d, %d)" % _values
        #        self._dao.execute(_query, commit=True)

        #        _query = "INSERT INTO tbl_fmeca \
        #                  (fld_revision_id, fld_assembly_id) \
        #                  VALUES(%d, %d)" % _values
        #        self._dao.execute(_query, commit=True)

        #        if self.chkFunctionMatrix.get_active():
        #            _query = "SELECT fld_function_id \
        #                      FROM tbl_functions \
        #                      WHERE fld_revision_id=%d" % _revision_id
        #            _functions = self._dao.execute(_query, commit=False)
        #            for i in range(len(_functions)):
        #                _query = "INSERT INTO tbl_functional_matrix \
        #                          (fld_revision_id, fld_assembly_id, \
        #                           fld_function_id) \
        #                          VALUES(%d, %d, %d)" % \
        #                         (_revision_id, _assembly_id, _functions[i][0])
        #                self._dao.execute(_query, commit=True)

        #        _assembly_id += 1
        #else:
        #    _values = (_revision_id, _assembly_id, _who)
        #    _query = "INSERT INTO tbl_system \
        #                          (fld_revision_id, fld_assembly_id, \
        #                           fld_entered_by) \
        #              VALUES (%d, %d, '%s')" % _values
        #   self._dao.execute(_query, commit=True)

        #    _values = (_revision_id, _assembly_id)
        #    _query = "INSERT INTO tbl_allocation \
        #              (fld_revision_id, fld_assembly_id) \
        #              VALUES (%d, %d)" % _values
        #    self._dao.execute(_query, commit=True)

        #    _query = "INSERT INTO tbl_risk_analysis \
        #              (fld_revision_id, fld_assembly_id) \
        #              VALUES (%d, %d)" % _values
        #    self._dao.execute(_query, commit=True)

        #    _query = "INSERT INTO tbl_similar_item \
        #              (fld_revision_id, fld_assembly_id) \
        #              VALUES (%d, %d)" % _values
        #    self._dao.execute(_query, commit=True)

        #    _query = "INSERT INTO tbl_fmeca \
        #              (fld_revision_id, fld_assembly_id) \
        #              VALUES(%d, %d)" % _values
        #    self._dao.execute(_query, commit=True)


# TODO: Move this to the Software class and simply call it from here.
        #_query = "SELECT MAX(fld_software_id) FROM tbl_software"
        #_module_id = self._dao.execute(_query, commit=False)
        #if _module_id[0][0] is not None:
        #    _module_id = _module_id[0][0] + 1

        #_query = "INSERT INTO tbl_software \
        #          (fld_revision_id, fld_level_id, fld_description, \
        #           fld_parent_module) \
        #          VALUES (%d, 0, 'System Software', '-')" % _revision_id
        #if not self._dao.execute(_query, commit=True):
        #    _util.rtk_error(_(u"Error creating system software hierarchy."))
        #else:
            # Add the new software module to each of risk analysis tables.
        #    for i in range(43):
        #        _query = "INSERT INTO tbl_software_development \
        #                 (fld_software_id, fld_question_id, fld_y) \
        #                 VALUES (%d, %d, 0)" % (_module_id, i)
        #        self._dao.execute(_query, commit=True)
        #    for i in range(50):
        #        _query = "INSERT INTO tbl_srr_ssr \
        #                 (fld_software_id, fld_question_id, fld_y, fld_value) \
        #                 VALUES (%d, %d, 0, 0)" % (_module_id, i)
        #        self._dao.execute(_query, commit=True)
        #    for i in range(39):
        #        _query = "INSERT INTO tbl_pdr \
        #                 (fld_software_id, fld_question_id, fld_y, fld_value) \
        #                 VALUES (%d, %d, 0, 0)" % (_module_id, i)
        #        self._dao.execute(_query, commit=True)
        #    for i in range(72):
        #        _query = "INSERT INTO tbl_cdr \
        #                 (fld_software_id, fld_question_id, fld_y, fld_value) \
        #                 VALUES (%d, %d, 0, 0)" % (_module_id, i)
        #        self._dao.execute(_query, commit=True)
        #    for i in range(24):
        #        _query = "INSERT INTO tbl_trr \
        #                 (fld_software_id, fld_question_id, fld_y, fld_value) \
        #                 VALUES (%d, %d, 0, 0)" % (_module_id, i)
        #        self._dao.execute(_query, commit=True)

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()
