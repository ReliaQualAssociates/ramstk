#!/usr/bin/env python
""" This is the Class that is used to represent and hold information related
    to the requirements of the Program. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       requirement.py is part of the RTK Project
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


def _vandv_tree_edit(cell, path, new_text, position, model):
    """
    Function called whenever a gtk.CellRenderer is edited in teh V&V task list.

    Keyword Arguments:
    cell     -- the CellRenderer that was edited.
    path     -- the TreeView path of the CellRenderer that was edited.
    new_text -- the new text in the edited CellRenderer.
    position -- the column position of the edited CellRenderer.
    model    -- the TreeModel the CellRenderer belongs to.
    """

    if(position == 4):
        model[path][position] = float(new_text)
    else:
        model[path][position] = new_text

    return False


class Requirement:
    """
    The Requirement class is used to represent the requirements in a
    system being analyzed.
    """

# TODO: Write code to update notebook widgets when editing the Requirements treeview.
# TODO: Add tooltips to all widgets.

# Create the top-level widgets.
    nbkRequirement = gtk.Notebook()
    vbxRequirement = gtk.VBox()

# Create widgets for the toolbar.
    btnAdd = gtk.ToolButton()
    btnAddChild = gtk.ToolButton()
    btnAddSibling = gtk.ToolButton()
    btnAssign = gtk.ToolButton()
    btnRemove = gtk.ToolButton()
    btnSave = gtk.ToolButton()

    cmbVandVTasks = _widg.make_combo(simple=False)

# Create the Stakeholder Inputs tab widgets.

# Create the General Data tab widgets.
    btnValidateDate = _widg.make_button(_height_=25, _width_=25,
                                        _label_="...", _image_=None)

    chkDerived = _widg.make_check_button()
    chkValidated = _widg.make_check_button()

    cmbOwner = _widg.make_combo(simple=False)
    cmbRqmtType = _widg.make_combo(simple=False)

    txtCode = _widg.make_entry(_width_=100, editable=False)
    txtFigureNumber = _widg.make_entry()
    txtPageNumber = _widg.make_entry()
    txtRequirement = gtk.TextBuffer()
    txtSpecification = _widg.make_entry()
    txtValidatedDate = _widg.make_entry(_width_=100)

# Create the Analysis tab widgets.
    chkClearQ1 = _widg.make_check_button()
    chkClearQ2 = _widg.make_check_button()
    chkClearQ3 = _widg.make_check_button()
    chkClearQ4 = _widg.make_check_button()
    chkClearQ5 = _widg.make_check_button()
    chkClearQ6 = _widg.make_check_button()
    chkClearQ7 = _widg.make_check_button()
    chkClearQ8 = _widg.make_check_button()
    chkClearQ9 = _widg.make_check_button()
    chkCompleteQ1 = _widg.make_check_button()
    chkCompleteQ2 = _widg.make_check_button()
    chkCompleteQ3 = _widg.make_check_button()
    chkCompleteQ4 = _widg.make_check_button()
    chkCompleteQ5 = _widg.make_check_button()
    chkCompleteQ6 = _widg.make_check_button()
    chkCompleteQ7 = _widg.make_check_button()
    chkCompleteQ8 = _widg.make_check_button()
    chkCompleteQ9 = _widg.make_check_button()
    chkCompleteQ10 = _widg.make_check_button()
    chkConsistentQ1 = _widg.make_check_button()
    chkConsistentQ2 = _widg.make_check_button()
    chkConsistentQ3 = _widg.make_check_button()
    chkConsistentQ4 = _widg.make_check_button()
    chkConsistentQ5 = _widg.make_check_button()
    chkConsistentQ6 = _widg.make_check_button()
    chkConsistentQ7 = _widg.make_check_button()
    chkConsistentQ8 = _widg.make_check_button()
    chkConsistentQ9 = _widg.make_check_button()
    chkConsistentQ10 = _widg.make_check_button()
    chkVerifiableQ1 = _widg.make_check_button()
    chkVerifiableQ2 = _widg.make_check_button()
    chkVerifiableQ3 = _widg.make_check_button()
    chkVerifiableQ4 = _widg.make_check_button()
    chkVerifiableQ5 = _widg.make_check_button()
    chkVerifiableQ6 = _widg.make_check_button()

# Create the V & V tab widgets.
    scwValidation = gtk.ScrolledWindow()

    tvwValidation = gtk.TreeView()

    def __init__(self, application):
        """
        Initializes the Requirements Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.requirement_id = 0

# Define local dictionary variables.
        self._dic_types = {}
        self._dic_owners = {}

# Define local list variables.
        self._lst_col_order = []

# Find the user's preferred gtk.Notebook tab position.
        if(_conf.TABPOS[2] == 'left'):
            _position = gtk.POS_LEFT
        elif(_conf.TABPOS[2] == 'right'):
            _position = gtk.POS_RIGHT
        elif(_conf.TABPOS[2] == 'top'):
            _position = gtk.POS_TOP
        else:
            _position = gtk.POS_BOTTOM

        self.nbkRequirement.set_tab_pos(_position)
        bg_color = _conf.RTK_COLORS[4]
        fg_color = _conf.RTK_COLORS[5]
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Requirement', 2,
                                                    self._app, None,
                                                    bg_color, fg_color)

# Create the Stakeholder Input tab.
        (self.tvwStakeholderInput,
         self._lst_stakeholder_col_order) = _widg.make_treeview('Stakeholder',
                                                                10, self._app,
                                                                None)
        if self._stakeholder_input_tab_create():
            self._app.debug_log.error("requirement.py: Failed to create Stakeholder Input tab.")

# Create the General Data tab.
        if self._general_data_tab_create():
            self._app.debug_log.error("requirement.py: Failed to create General Data tab.")

# Create the Analysis tab.
        if self._analysis_tab_create():
            self._app.debug_log.error("requirement.py: Failed to create Analysis tab.")

# Create the V & V tab.
        if self._vandv_widgets_create():
            self._app.debug_log.error("requirement.py: Failed to create V & V widgets.")
        if self._vandv_tab_create():
            self._app.debug_log.error("requirement.py: Failed to create V & V tab.")

        toolbar = self._toolbar_create()
        self.vbxRequirement.pack_start(toolbar, expand=False)
        self.vbxRequirement.pack_start(self.nbkRequirement)

        self.nbkRequirement.connect('switch-page', self._notebook_page_switched)

        self._ready = True

    def _toolbar_create(self):
        """
        Method to create a toolbar for the REQUIREMENT Object work book.
        """

        toolbar = gtk.Toolbar()

        _pos = 0

# Add sibling requirement button.
        self.btnAddSibling.set_tooltip_text(_(u"Adds a new requirement at the same indenture level as the selected requirement."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        self.btnAddSibling.set_icon_widget(image)
        self.btnAddSibling.connect('clicked', self._requirement_add, 0)
        toolbar.insert(self.btnAddSibling, _pos)
        _pos += 1

# Add child (derived) requirement button.
        self.btnAddChild.set_tooltip_text(_(u"Adds a new requirement one indenture level subordinate to the selected requirement."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        self.btnAddChild.set_icon_widget(image)
        self.btnAddChild.connect('clicked', self._requirement_add, 1)
        toolbar.insert(self.btnAddChild, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Add button.
        self.btnAdd.set_name('Add')
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAdd.set_icon_widget(image)
        self.btnAdd.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAdd, _pos)
        _pos += 1

# Remove button.
        self.btnRemove.set_name('Remove')
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemove.set_icon_widget(image)
        self.btnRemove.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnRemove, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Save requirement button.
        self.btnSave.set_name('Save')
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSave.set_icon_widget(image)
        self.btnSave.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnSave, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Assign existing V&V task button
        self.btnAssign.set_tooltip_text(_(u"Assigns an exisiting Verification and Validation (V&V) task to the selected requirement."))
        self.btnAssign.set_name('Assign')
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/assign.png')
        self.btnAssign.set_icon_widget(image)
        self.btnAssign.connect('clicked', self._toolbutton_pressed)
        toolbar.insert(self.btnAssign, _pos)
        _pos += 1

        self.cmbVandVTasks.set_tooltip_text(_(u"List of existing V&V activities available to assign to selected requirement."))
        alignment = gtk.Alignment(xalign=0.5, yalign=0.5)
        alignment.add(self.cmbVandVTasks)
        toolitem = gtk.ToolItem()
        toolitem.add(alignment)
        toolbar.insert(toolitem, _pos)

        toolbar.show()

# Hide the toolbar items associated with the V&V tab.
        self.btnAssign.hide()
        self.cmbVandVTasks.hide()

        return(toolbar)

    def _stakeholder_input_tab_create(self):
        """
        Method to create the Stakeholder Input gtk.Notebook tab and populate it
        with the appropriate widgets.
        """

        def _stakeholder_input_widgets_create(self):
            """
            Function to create the widgets to be used on the Stakeholder Input
            tab.
            """

    # Set the has-entry property for stakeholder and affinity group
    # gtk.CellRendererCombo cells.
            _cell_ = self.tvwStakeholderInput.get_column(self._lst_stakeholder_col_order[1]).get_cell_renderers()
            _cell_[0].set_property('has-entry', True)

            _cell_ = self.tvwStakeholderInput.get_column(self._lst_stakeholder_col_order[3]).get_cell_renderers()
            _cell_[0].set_property('has-entry', True)

            for i in range(4, 9):
                _cell_ = self.tvwStakeholderInput.get_column(self._lst_stakeholder_col_order[i]).get_cell_renderers()
                _cell_[0].set_alignment(xalign=0.5, yalign=0.5)

    # Set the priority, customer rating, and planned rating
    # gtk.CellRendererSpin to integer spins with increments of 1.  Make it an
    # integer spin by setting the number of digits to 0.
            for i in range(4, 7):
                _cell_ = self.tvwStakeholderInput.get_column(self._lst_stakeholder_col_order[i]).get_cell_renderers()
                _adjustment_ = _cell_[0].get_property('adjustment')
                _adjustment_.set_step_increment(1)
                _cell_[0].set_property('adjustment', _adjustment_)
                _cell_[0].set_property('digits', 0)

            return False

        if _stakeholder_input_widgets_create(self):
            self._app.debug_log.error("requirement.py: Failed to create Stakeholder Input widgets.")

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwStakeholderInput)

        frame = _widg.make_frame(_label_=_(u"Stakeholder Inputs"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _(u"Stakeholder\nInputs") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_("Displays stakeholder inputs."))
        label.show_all()
        self.nbkRequirement.insert_page(frame,
                                        tab_label=label,
                                        position=-1)

        return False

    def _stakeholder_input_tab_load(self):
        """
        Method to load the stakeholder input tab.
        """

# Load the stakeholder gtk.CellRendererCombo with a list of distinct
# stakeholders already entered into the database.
        _query_ = "SELECT DISTINCT fld_stakeholder \
                   FROM tbl_stakeholder_input \
                   ORDER BY fld_stakeholder ASC"
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        try:
            _n_stakeholders_ = len(_results_)
        except TypeError:
            _n_stakeholders_ = 0

        _cell_ = self.tvwStakeholderInput.get_column(self._lst_stakeholder_col_order[1]).get_cell_renderers()
        _model_ = _cell_[0].get_property('model')
        _model_.clear()
        for i in range(_n_stakeholders_):
            _model_.append([_results_[i][0]])

# Load the stakeholder gtk.CellRendererCombo with a list of distinct affinity
# groups already entered into the database.
        _query_ = "SELECT DISTINCT fld_group \
                   FROM tbl_stakeholder_input \
                   ORDER BY fld_group ASC"
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        try:
            _n_groups_ = len(_results_)
        except TypeError:
            _n_groups_ = 0

        _cell_ = self.tvwStakeholderInput.get_column(self._lst_stakeholder_col_order[3]).get_cell_renderers()
        _model_ = _cell_[0].get_property('model')
        _model_.clear()
        for i in range(_n_groups_):
            _model_.append([_results_[i][0]])

# Load the stakeholder gtk.CellRendererCombo with a list of existing
# requirement codes in the database.
        _query_ = "SELECT fld_requirement_code \
                   FROM tbl_requirements"
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        try:
            _n_requirements_ = len(_results_)
        except TypeError:
            _n_requirements_ = 0

        _cell_ = self.tvwStakeholderInput.get_column(self._lst_stakeholder_col_order[9]).get_cell_renderers()
        _model_ = _cell_[0].get_property('model')
        _model_.clear()
        for i in range(_n_requirements_):
            _model_.append([_results_[i][0]])

# Now load the Stakeholder Inputs gtk.TreeView.
        _query_ = "SELECT fld_input_id, fld_stakeholder, fld_description, \
                          fld_group, fld_priority, fld_customer_rank, \
                          fld_planned_rank, fld_improvement, \
                          fld_overall_weight, fld_requirement_code, \
                          fld_user_float_1, fld_user_float_2, \
                          fld_user_float_3, fld_user_float_4, \
                          fld_user_float_5 \
                   FROM tbl_stakeholder_input \
                   WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(_results_ == '' or not _results_ or _results_ is None):
            return True

        _model_ = self.tvwStakeholderInput.get_model()
        _model_.clear()
        for i in range(len(_results_)):
            _model_.append(None, _results_[i])

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it
        with the appropriate widgets.
        """

        _labels_ = [_("Requirement ID:"), _("Requirement:"),
                    _("Requirement Type:"), _("Specification:"),
                    _("Page Number:"), _("Figure Number:"), _("Derived:"),
                    _("Validated:"), _("Owner:"), _("Validated Date:")]

        def _general_data_widgets_create(self):
            """ Method to create the General Data widgets. """

            self.btnValidateDate.set_tooltip_text(_(u"Launches the calendar to select the date the requirement was validated."))
            self.btnValidateDate.connect('released', _util.date_select,
                                         self.txtValidatedDate)

            self.chkDerived.set_tooltip_text(_("Whether or not the selected requirement is derived."))
            self.chkDerived.connect('toggled', self._callback_check, 6)

            self.chkValidated.set_tooltip_text(_("Whether or not the selected requirement has been verified and validated."))
            self.chkValidated.connect('toggled', self._callback_check, 8)

            self.cmbOwner.set_tooltip_text(_("Displays the responsible organization or individual for the selected requirement."))
            _query_ = "SELECT fld_group_name, fld_group_id FROM tbl_groups"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

# Load the gtk.ComboBox in the Work Book, the gtk.CellRendererCombo in the
# Tree Book, and the local dictionary with the list of groups.  The dictionary
# uses the noun name of the group as the key and the index in the gtk.ComboBox
# as the value.
            _model_ = self.cmbOwner.get_model()
            _cell_ = self.treeview.get_column(self._lst_col_order[10]).get_cell_renderers()
            _cell_model_ = _cell_[0].get_property('model')
            _model_.clear()
            _cell_model_.clear()
            _model_.append(None, ["", "", ""])
            _cell_model_.append([""])
            for i in range(len(_results_)):
                _data_ = [_results_[i][0], str(_results_[i][1]), '']
                _model_.append(None, _data_)
                _cell_model_.append([_results_[i][0]])
                self._dic_owners[_results_[i][0]] = i + 1
            self.cmbOwner.connect('changed', self._callback_combo, 10)

# Load the gtk.ComboBox in the Work Book, the gtk.CellRendererCombo in the
# Tree Book, and the local dictionary with the list of requirement types.  The
# dictionary uses the noun name of the requirement type as the key and the
# index in the gtk.ComboBox as the value.
            self.cmbRqmtType.set_tooltip_text(_("Selects and displays the type of requirement for the selected requirement."))
            _query_ = "SELECT fld_requirement_type_desc, \
                              fld_requirement_type_code, \
                              fld_requirement_type_id \
                       FROM tbl_requirement_type"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbRqmtType, _results_, False)
            _cell_ = self.treeview.get_column(self._lst_stakeholder_col_order[4]).get_cell_renderers()
            _cell_model_ = _cell_[0].get_property('model')
            _cell_model_.clear()
            for i in range(len(_results_)):
                _cell_model_.append([_results_[i][0]])
                self._dic_owners[_results_[i][0]] = i + 1
            self.cmbRqmtType.connect('changed', self._callback_combo, 4)

            self.txtCode.set_tooltip_text(_("Displays the unique code for the selected requirement."))
            self.txtCode.connect('focus-out-event',
                                 self._callback_entry, 'text', 5)

            self.txtFigureNumber.set_tooltip_text(_("Displays the specification figure number associated with the selected requirement."))
            self.txtFigureNumber.connect('focus-out-event',
                                         self._callback_entry, 'text', 13)

            self.txtPageNumber.set_tooltip_text(_("Displays the specification page number associated with the selected requirement."))
            self.txtPageNumber.connect('focus-out-event',
                                       self._callback_entry, 'text', 12)

            self.txtSpecification.set_tooltip_text(_("Displays the internal or industry specification associated with the selected requirement."))
            self.txtSpecification.connect('focus-out-event',
                                          self._callback_entry, 'text', 11)

            self.txtValidatedDate.set_tooltip_text(_("Displays the date the selected requirement was verified and validated."))
            self.txtValidatedDate.connect('focus-out-event',
                                          self._callback_entry, 'text', 9)

            return False

        if _general_data_widgets_create(self):
            self._app.debug_log.error("requirement.py: Failed to create General Data widgets.")

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_(u"General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

# Create the labels for the upper-left and lower-left quadrants.
        _max1_ = 0
        _max2_ = 0
        (_max1_, _y_pos_) = _widg.make_labels(_labels_[2:9], fixed, 5, 140)
        _x_pos_ = max(_max1_, _max2_) + 20

        label = _widg.make_label(_labels_[0], 150, 25)
        fixed.put(label, 5, 5)
        fixed.put(self.txtCode, _x_pos_, 5)
        label = _widg.make_label(_labels_[1], 150, 25)
        fixed.put(label, 5, 35)
        textview = _widg.make_text_view(buffer_=self.txtRequirement, width=400)
        textview.set_tooltip_text(_(u"Detailed description of the requirement."))
        _widget = textview.get_children()[0].get_children()[0]
        _widget.connect('focus-out-event', self._callback_entry, 'text', 3)
        fixed.put(textview, _x_pos_, 35)

        fixed.put(self.cmbRqmtType, _x_pos_, _y_pos_[0])
        fixed.put(self.txtSpecification, _x_pos_, _y_pos_[1])
        fixed.put(self.txtPageNumber, _x_pos_, _y_pos_[2])
        fixed.put(self.txtFigureNumber, _x_pos_, _y_pos_[3])
        fixed.put(self.chkDerived, _x_pos_, _y_pos_[4])
        fixed.put(self.chkValidated, _x_pos_, _y_pos_[5])
        label = _widg.make_label(_labels_[9],
                                 150, 25)
        fixed.put(label, _x_pos_+25, _y_pos_[5])
        fixed.put(self.txtValidatedDate, _x_pos_ + 200, _y_pos_[5])
        fixed.put(self.btnValidateDate, _x_pos_ + 305 , _y_pos_[5])
        fixed.put(self.cmbOwner, _x_pos_, _y_pos_[6])

        fixed.show_all()

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("General\nData") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_("Displays general information about the selected requirement."))
        label.show_all()
        self.nbkRequirement.insert_page(frame,
                                        tab_label=label,
                                        position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the Requirement
        Object.
        """

        try:
            _idx_ = int(self._dic_owners[self.model.get_value(self.selected_row, 10)])
        except KeyError:
            _idx_ = 0
        self.cmbOwner.set_active(_idx_)
        try:
            _idx_ = int(self._dic_owners[self.model.get_value(self.selected_row, 4)])
        except KeyError:
            _idx_ = 0
        self.cmbRqmtType.set_active(_idx_)

        self.chkDerived.set_active(int(self.model.get_value(self.selected_row, 6)))
        self.chkValidated.set_active(int(self.model.get_value(self.selected_row, 8)))

        self.txtCode.set_text(str(self.model.get_value(self.selected_row, 5)))
        self.txtFigureNumber.set_text(str(self.model.get_value(self.selected_row, 13)))
        self.txtPageNumber.set_text(str(self.model.get_value(self.selected_row, 12)))
        self.txtRequirement.set_text(str(self.model.get_value(self.selected_row, 3)))
        self.txtSpecification.set_text(str(self.model.get_value(self.selected_row, 11)))

# Convert the ordinal date to a Y-m-d format.
        if(self.model.get_value(self.selected_row, 9) > 719163):
            _date_ = _util.ordinal_to_date(self.model.get_value(self.selected_row, 9))
        else:
            _date_ = ""
        self.txtValidatedDate.set_text(_date_)

        return False

    def _analysis_tab_create(self):
        """
        Method to the create the tab for analyzing the selected requirement.
        """

        _labels_ = [[_(u"The requirement clearly states what is needed or desired."),
                     _(u"The requirement is unambiguous and not open to interpretation."),
                     _(u"All terms that can have more than one meaning are qualified so that the desired meaning is readily apparent."),
                     _(u"Diagrams, drawings, etc. are used to increase understanding of the requirement."),
                     _(u"The requirement is free from spelling and grammatical errors."),
                     _(u"The requirement is written in non-technical language using the vocabulary of the stakeholder."),
                     _(u"Stakeholders understand the requirement as written."),
                     _(u"The requirement is clear enough to be turned over to an independent group and still be understood."),
                     _(u"The requirement avoids stating how the problem is to be solved or what techniques are to be used.")],
                    [_(u"Performance objectives are properly documented from the user's point of view."),
                     _(u"No necessary information is missing from the requirement."),
                     _(u"The requirement has been assigned a priority."),
                     _(u"The requirement is realistic given the technology that will used to implement the system."),
                     _(u"The requirement is feasible to implement given the defined project timeframe, scope, structure and budget."),
                     _(u"If the requirement describes something as a 'standard' the specific source is cited."),
                     _(u"The requirement is relevant to the problem and its solution."),
                     _(u"The requirement contains no implied design details."),
                     _(u"The requirement contains no implied implementation constraints."),
                     _(u"The requirement contains no implied project management constraints.")],
                    [_(u"The requirement describes a single need or want; it could not be broken into several different requirements."),
                     _(u"The requirement requires non-standard hardware or must use software to implement."),
                     _(u"The requirement can be implemented within known constraints."),
                     _(u"The requirement provides an adequate basis for design and testing."),
                     _(u"The requirement adequately supports the business goal of the project."),
                     _(u"The requirement does not conflict with some constraint, policy or regulation."),
                     _(u"The requirement does not conflict with another requirement."),
                     _(u"The requirement is not a duplicate of another requirement."),
                     _(u"The requirement is in scope for the project.")],
                    [_(u"The requirement is verifiable by testing, demonstration, review, or analysis."),
                     _(u"The requirement lacks 'weasel words' (e.g. various, mostly, suitable, integrate, maybe, consistent, robust, modular,  user-friendly, superb, good)."),
                     _(u"Any performance criteria are quantified such that they are testable."),
                     _(u"Independent testing would be able to determine whether the requirement has been satisfied."),
                     _(u"The task(s) that will validate and verify the final design satisfies the requirement have been identified."),
                     _(u"The identified V&amp;V task(s) have been added to the validation plan (e.g., DVP)")]]

        def _analysis_tab_widgets_create(self):
            """
            Function to create the widgets for the Requirements Analysis tab
            in the REQUIREMENTS Work Book.

            Keyword Arguments:
            self -- the REQUIREMENTS Object.
            """

            self.chkClearQ1.connect('toggled', self._callback_check, 16)
            self.chkClearQ2.connect('toggled', self._callback_check, 17)
            self.chkClearQ3.connect('toggled', self._callback_check, 18)
            self.chkClearQ4.connect('toggled', self._callback_check, 19)
            self.chkClearQ5.connect('toggled', self._callback_check, 20)
            self.chkClearQ6.connect('toggled', self._callback_check, 21)
            self.chkClearQ7.connect('toggled', self._callback_check, 22)
            self.chkClearQ8.connect('toggled', self._callback_check, 23)
            self.chkClearQ9.connect('toggled', self._callback_check, 24)
            #self.chkClearQ10.connect('toggled', self._callback_check, 25)
            self.chkCompleteQ1.connect('toggled', self._callback_check, 26)
            self.chkCompleteQ2.connect('toggled', self._callback_check, 27)
            self.chkCompleteQ3.connect('toggled', self._callback_check, 28)
            self.chkCompleteQ4.connect('toggled', self._callback_check, 29)
            self.chkCompleteQ5.connect('toggled', self._callback_check, 30)
            self.chkCompleteQ6.connect('toggled', self._callback_check, 31)
            self.chkCompleteQ7.connect('toggled', self._callback_check, 32)
            self.chkCompleteQ8.connect('toggled', self._callback_check, 33)
            self.chkCompleteQ9.connect('toggled', self._callback_check, 34)
            self.chkCompleteQ10.connect('toggled', self._callback_check, 35)
            self.chkConsistentQ1.connect('toggled', self._callback_check, 36)
            self.chkConsistentQ2.connect('toggled', self._callback_check, 37)
            self.chkConsistentQ3.connect('toggled', self._callback_check, 38)
            self.chkConsistentQ4.connect('toggled', self._callback_check, 39)
            self.chkConsistentQ5.connect('toggled', self._callback_check, 40)
            self.chkConsistentQ6.connect('toggled', self._callback_check, 41)
            self.chkConsistentQ7.connect('toggled', self._callback_check, 42)
            self.chkConsistentQ8.connect('toggled', self._callback_check, 43)
            self.chkConsistentQ9.connect('toggled', self._callback_check, 44)
            self.chkConsistentQ10.connect('toggled', self._callback_check, 45)
            self.chkVerifiableQ1.connect('toggled', self._callback_check, 46)
            self.chkVerifiableQ2.connect('toggled', self._callback_check, 47)
            self.chkVerifiableQ3.connect('toggled', self._callback_check, 48)
            self.chkVerifiableQ4.connect('toggled', self._callback_check, 49)
            self.chkVerifiableQ5.connect('toggled', self._callback_check, 50)
            self.chkVerifiableQ6.connect('toggled', self._callback_check, 51)

            return False

        if _analysis_tab_widgets_create(self):
            self._app.debug_log.error("requirement.py: Failed to create Requirements Analysis tab widgets.")

        hpaned = gtk.HPaned()
        vpaned = gtk.VPaned()

        hpaned.pack1(vpaned, resize=False)

# Create quadrant #1 (upper left) for determining if the requirement is clear.
        fixed1 = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed1)

        frame = _widg.make_frame(_label_=_(u"Clarity of Requirement"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack1(frame, resize=False)

# Create quadrant #3 (lower left) for determining if the requirement is
# complete.
        fixed2 = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed2)

        frame = _widg.make_frame(_label_=_(u"Completeness of Requirement"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, resize=False)

# Create the labels for quadrant #1.
        _max1_ = 0
        _max2_ = 0
        (_max1_, _y_pos1_) = _widg.make_labels(_labels_[0], fixed1, 5, 5)
        _x_pos_ = max(_max1_, _max2_) + 50

# Create the labels for quadrant #3.
        _max2_ = 0
        (_max2_, _y_pos2_) = _widg.make_labels(_labels_[1], fixed2, 5, 5)
        _x_pos_ = max(_max1_, _max2_) + 50

# Place the quadrant 1 widgets.
        fixed1.put(self.chkClearQ1, _x_pos_, _y_pos1_[0])
        fixed1.put(self.chkClearQ2, _x_pos_, _y_pos1_[1])
        fixed1.put(self.chkClearQ3, _x_pos_, _y_pos1_[2])
        fixed1.put(self.chkClearQ4, _x_pos_, _y_pos1_[3])
        fixed1.put(self.chkClearQ5, _x_pos_, _y_pos1_[4])
        fixed1.put(self.chkClearQ6, _x_pos_, _y_pos1_[5])
        fixed1.put(self.chkClearQ7, _x_pos_, _y_pos1_[6])
        fixed1.put(self.chkClearQ8, _x_pos_, _y_pos1_[7])
        fixed1.put(self.chkClearQ9, _x_pos_, _y_pos1_[8])

# Place the quadrant 3 widgets.
        fixed2.put(self.chkCompleteQ1, _x_pos_, _y_pos2_[0])
        fixed2.put(self.chkCompleteQ2, _x_pos_, _y_pos2_[1])
        fixed2.put(self.chkCompleteQ3, _x_pos_, _y_pos2_[2])
        fixed2.put(self.chkCompleteQ4, _x_pos_, _y_pos2_[3])
        fixed2.put(self.chkCompleteQ5, _x_pos_, _y_pos2_[4])
        fixed2.put(self.chkCompleteQ6, _x_pos_, _y_pos2_[5])
        fixed2.put(self.chkCompleteQ7, _x_pos_, _y_pos2_[6])
        fixed2.put(self.chkCompleteQ8, _x_pos_, _y_pos2_[7])
        fixed2.put(self.chkCompleteQ9, _x_pos_, _y_pos2_[8])
        fixed2.put(self.chkCompleteQ10, _x_pos_, _y_pos2_[9])

        vpaned = gtk.VPaned()
        hpaned.pack2(vpaned, resize=False)

# Create quadrant #2 (upper right) for determining if the requirement is
# consistent.
        fixed1 = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed1)

        frame = _widg.make_frame(_label_=_(u"Consistency of Requirement"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack1(frame, resize=False)

# Create quadrant #4 (lower right) for determining if the requirement is
# verifiable.
        fixed2 = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed2)

        frame = _widg.make_frame(_label_=_(u"Verifiability of Requirement"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, resize=False)

# Create the labels for quadrant #2.
        _max1_ = 0
        _max2_ = 0
        (_max1_, _y_pos1_) = _widg.make_labels(_labels_[2], fixed1, 5, 5)
        _x_pos_ = max(_max1_, _max2_) + 50

# Create the labels for quadrant #2.
        _max2_ = 0
        (_max2_, _y_pos2_) = _widg.make_labels(_labels_[3], fixed2, 5, 5)
        _x_pos_ = max(_max1_, _max2_) + 50

# Place the quadrant #2 widgets.
        fixed1.put(self.chkConsistentQ1, _x_pos_, _y_pos1_[0])
        fixed1.put(self.chkConsistentQ2, _x_pos_, _y_pos1_[1])
        fixed1.put(self.chkConsistentQ3, _x_pos_, _y_pos1_[2])
        fixed1.put(self.chkConsistentQ4, _x_pos_, _y_pos1_[3])
        fixed1.put(self.chkConsistentQ5, _x_pos_, _y_pos1_[4])
        fixed1.put(self.chkConsistentQ6, _x_pos_, _y_pos1_[5])
        fixed1.put(self.chkConsistentQ7, _x_pos_, _y_pos1_[6])
        fixed1.put(self.chkConsistentQ8, _x_pos_, _y_pos1_[7])
        fixed1.put(self.chkConsistentQ9, _x_pos_, _y_pos1_[8])

        fixed2.put(self.chkVerifiableQ1, _x_pos_, _y_pos2_[0])
        fixed2.put(self.chkVerifiableQ2, _x_pos_, _y_pos2_[1])
        fixed2.put(self.chkVerifiableQ3, _x_pos_, _y_pos2_[2])
        fixed2.put(self.chkVerifiableQ4, _x_pos_, _y_pos2_[3])
        fixed2.put(self.chkVerifiableQ5, _x_pos_, _y_pos2_[4])
        fixed2.put(self.chkVerifiableQ6, _x_pos_, _y_pos2_[5])

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("Analysis") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_(u"Analyzes the selected requirement."))
        label.show_all()
        self.nbkRequirement.insert_page(hpaned,
                                        tab_label=label,
                                        position=-1)

        return False

    def _analysis_tab_load(self):
        """
        Method to load the Requirements Analysis tab widgets with the values
        from the RTK Program database.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        self.chkClearQ1.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[16]))
        self.chkClearQ2.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[17]))
        self.chkClearQ3.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[18]))
        self.chkClearQ4.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[19]))
        self.chkClearQ5.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[20]))
        self.chkClearQ6.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[21]))
        self.chkClearQ7.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[22]))
        self.chkClearQ8.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[23]))
        self.chkClearQ9.set_active(_model_.get_value(_row_,
                                            self._lst_col_order[24]))
        #self.chkClearQ10.set_active(_model_.get_value(_row_,
        #                                    self._lst_col_order[25]))
        self.chkCompleteQ1.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[26]))
        self.chkCompleteQ2.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[27]))
        self.chkCompleteQ3.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[28]))
        self.chkCompleteQ4.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[29]))
        self.chkCompleteQ5.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[30]))
        self.chkCompleteQ6.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[31]))
        self.chkCompleteQ7.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[32]))
        self.chkCompleteQ8.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[33]))
        self.chkCompleteQ9.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[34]))
        self.chkCompleteQ10.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[35]))
        self.chkConsistentQ1.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[36]))
        self.chkConsistentQ2.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[37]))
        self.chkConsistentQ3.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[38]))
        self.chkConsistentQ4.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[39]))
        self.chkConsistentQ5.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[40]))
        self.chkConsistentQ6.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[41]))
        self.chkConsistentQ7.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[42]))
        self.chkConsistentQ8.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[43]))
        self.chkConsistentQ9.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[44]))
        self.chkConsistentQ10.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[45]))
        self.chkVerifiableQ1.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[46]))
        self.chkVerifiableQ2.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[47]))
        self.chkVerifiableQ3.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[48]))
        self.chkVerifiableQ4.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[49]))
        self.chkVerifiableQ5.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[50]))
        self.chkVerifiableQ6.set_active(_model_.get_value(_row_,
                                                self._lst_col_order[51]))

        return False

    def _vandv_widgets_create(self):
        """
        Method to create the Verification and Validation Task widgets.
        """

        model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT)
        self.tvwValidation.set_model(model)
        self.tvwValidation.set_tooltip_text(_("Provides read-only list of basic information for Verfication and Validation (V&V) tasks associated with the selected Requirement."))

    def _vandv_tab_create(self):
        """
        Method to create the Verification and Validation Plan gtk.Notebook tab
        and populate it with the appropriate widgets.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwValidation)

        frame = _widg.make_frame(_(u"Verification and Validation Task List"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn(_(u"Task ID"))
        column.set_visible(0)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.tvwValidation.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.connect('edited', _vandv_tree_edit, 1,
                     self.tvwValidation.get_model())
        column = gtk.TreeViewColumn(_(u"Task Description"))
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        self.tvwValidation.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.connect('edited', _vandv_tree_edit, 2,
                     self.tvwValidation.get_model())
        column = gtk.TreeViewColumn(_(u"Start Date"))
        column.set_visible(1)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        self.tvwValidation.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.connect('edited', _vandv_tree_edit, 3,
                     self.tvwValidation.get_model())
        column = gtk.TreeViewColumn(_(u"Due Date"))
        column.set_visible(1)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3)
        self.tvwValidation.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.connect('edited', _vandv_tree_edit, 4,
                     self.tvwValidation.get_model())
        column = gtk.TreeViewColumn(_(u"% Complete"))
        column.set_visible(1)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4)
        self.tvwValidation.append_column(column)

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("V &amp; V Tasks") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_(u"Displays the list of V&V tasks for the selected requirement."))
        label.show_all()
        self.nbkRequirement.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _vandv_tab_load(self):
        """
        Creates the TreeView widget to display the Requirement/Validation task
        relationship matrix.
        """

        _values_ = (self.model.get_value(self.selected_row, self._lst_col_order[0]),
                    self.model.get_value(self.selected_row, self._lst_col_order[1]))

        _query_ = "SELECT t1.fld_validation_id, t1.fld_task_desc, \
                          t1.fld_start_date, t1.fld_end_date, t1.fld_status \
                   FROM tbl_validation AS t1 \
                   INNER JOIN tbl_validation_matrix AS t2 \
                   ON t2.fld_validation_id=t1.fld_validation_id \
                   WHERE t1.fld_revision_id=%d \
                   AND t2.fld_requirement_id=%d \
                   GROUP BY t1.fld_validation_id" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(_results_ == '' or not _results_ or _results_ is None):
            return True

        _n_tasks_ = len(_results_)
        model = self.tvwValidation.get_model()
        model.clear()
        for i in range(_n_tasks_):
            model.append(None, _results_[i])

        root = model.get_iter_root()
        if root is not None:
            path = model.get_path(root)
            self.tvwValidation.expand_all()
            self.tvwValidation.set_cursor('0', None, False)
            col = self.tvwValidation.get_column(0)
            self.tvwValidation.row_activated(path, col)

# Load the list of V&V task to the gtk.ComboBox used to associate existing V&V
# tasks with requirements.
        _query_ = "SELECT DISTINCT(fld_validation_id), \
                          fld_task_desc, fld_task_type \
                   FROM tbl_validation \
                   WHERE fld_revision_id=%d" % self._app.REVISION.revision_id

        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        _tasks_ = []
        for i in range(len(_results_)):
            _tasks_.append((_results_[i][1], _results_[i][0], _results_[i][2]))

        _widg.load_combo(self.cmbVandVTasks, _tasks_, simple=False)

        return False

    def create_tree(self):
        """
        Creates the Requirements TreeView and connects it to callback
        functions to handle editting.  Background and foreground colors can be
        set using the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        self.treeview.set_enable_tree_lines(True)
        #TODO: Load requirement type CellRendererCombo
        #TODO: Load requiquirement owner CellRendererCombo
        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the Requirements treeview model with system information.
        This information can be stored either in a MySQL or SQLite3 database.
        """

# Select everything from the requirements table.
        _query_ = "SELECT * FROM tbl_requirements \
                   WHERE fld_revision_id=%d \
                   ORDER BY fld_requirement_id" % self._app.REVISION.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(_results_ == ''):
            return True

        n_records = len(_results_)
        self.model.clear()
        for i in range(n_records):
            if (_results_[i][self._lst_col_order[7]] == '-'):
                piter = None
            else:
                piter = self.model.get_iter_from_string(_results_[i][self._lst_col_order[7]])

            self.model.append(piter, _results_[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)

        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Requirement
        Object treeview.

        Keyword Arguments:
        treeview -- the Requirement Object treeview.
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
        Callback function to handle events for the REQUIREMENT Object treeview.
        It is called whenever the REQUIREMENT Object treeview is clicked or a
        row is activated.  It will save the previously selected row in the
        REQUIREMENT Object treeview.

        Keyword Arguments:
        treeview -- the Requirement Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        _selection_ = treeview.get_selection()
        (self.model, self.selected_row) = _selection_.get_selected()

        if self.selected_row is not None:
            self.load_notebook()

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the Requirement Object TreeView.

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the Requirement Object
                   TreeView.
        """

        for i in columns:
            self.model.set_value(self.selected_row, i, values[i])

        return False

    def _requirement_add(self, button, type_):
        """
        Method to add a new Requirement to the RTK Program's database.

        Keyword Arguments:
        button -- the gtk.ToolButton() that called this function.
        type_  -- the type of Requirement to add; 0 = sibling, 1 = child.
        """

# Find the selected requirement.
        _selection_ = self.treeview.get_selection()
        (_model_, _row_) = _selection_.get_selected()

# Find the parent or sibling requirement.
        if(type_ == 0):                     # Adding derived requirements.
            _parent_ = "-"
            if _row_ is not None:
                _prow_ = _model_.iter_parent(_row_)
                if _prow_ is not None:
                    _parent_ = _model_.get_string_from_iter(_prow_)
            _title_ = _(u"RTK - Add Derived Requirements")
            _prompt_ = _(u"How many derived requirements to add?")

        elif(type_ == 1):                   # Adding sibling requirements.
            _parent_ = "-"
            if _row_ is not None:
                _parent_ = _model_.get_string_from_iter(_row_)
            _title_ = _(u"RTK - Add Sibbling Requirements")
            _prompt_ = _(u"How many sibling requirements to add?")

        _n_requirements_ = _util.add_items(_title_, _prompt_)
# Now add the number of derived or sibling requirements the user requested.
        for i in range(_n_requirements_):
            _requirement_name_ = "New Requirement_" + str(i)
            _query_ = "INSERT INTO tbl_requirements \
                       (fld_revision_id, fld_assembly_id, \
                        fld_requirement_desc, fld_parent_requirement) \
                       VALUES (%d, %d, '%s', '%s')" % \
                       (self._app.REVISION.revision_id,
                       self._app.ASSEMBLY.assembly_id, _requirement_name_,
                       _parent_)
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("requirement.py: Failed to add requirement.")
                return True

        self._app.REVISION.load_tree()
        self.load_tree()

        return False

    def _requirement_delete(self):
        """
        Deletes the currently selected Requirement from the RTK Program
        database.
        """

        _selection_ = self.treeview.get_selection()
        (_model_, _row_) = _selection_.get_selected()

# Delete any and all the derived requirements.
        _query_ = "DELETE FROM tbl_requirements \
                   WHERE fld_parent_requirement=%d" % \
                   _model_.get_string_from_iter(_row_)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.user_log.error("requirement.py: Failed to delete derived requirement.")
            return True

# Then delete the requirement itself.
        _values_ = (self._app.REVISION.revision_id, \
                    _model_.get_value(_row_, 1))
        _query_ = "DELETE FROM tbl_requirements \
                   WHERE fld_revision_id=%d \
                   AND fld_requirement_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.user_log.error("requirement.py: Failed to delete requirement.")
            return True

        self.load_tree()

        return False

    def requirement_save(self, widget):
        """
        Saves the Requirement Object treeview information to the Program's
        database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _stakeholder_input_add(self):
        """
        Method to add one or more stakeholder inputs to the RTK Program
        database.
        """

        _n_inputs_ = _util.add_items(title=_(u"RTK - Add Stakeholder Inputs"),
                                     prompt=_(u"How many stakeholder inputs to add?"))

        if(_n_inputs_ > 0):
# Find the currently selected stakeholder input, if any, and retrieve the
# revision ID.  If there is no selected stakeholder input, retrieve the
# revision ID from the global REVISION Object variable revision_id
            _selection_ = self.tvwStakeholderInput.get_selection()
            (_model_, _row_) = _selection_.get_selected()

            _revision_id_ = self._app.REVISION.revision_id

            for i in range(_n_inputs_):
                _input_ = "Stakeholder input %d" % i
                _query_ = "INSERT INTO tbl_stakeholder_input \
                           (fld_revision_id, fld_stakeholder, \
                            fld_description, fld_group) \
                           VALUES (%d, '', '%s', '')" % \
                           (_revision_id_, _input_)
                _results_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx,
                                                       commit=True)

                if not _results_:
                    self._app.debug_log.error("requirement.py: Failed to add stakeholder inputs.")
                    return True

            self._stakeholder_input_tab_load()

        return False

    def _stakeholder_input_save(self):
        """
        Method to save the stakeholder inputs to the RTK Program database.
        """

        def _save_line_item(model, path, row):
            """
            Function to save each node in the Stakeholder Input gtk.TreeView.
            """

            _priority_ = model.get_value(row,
                                         self._lst_stakeholder_col_order[4])
            _current_sat_ = model.get_value(row,
                                            self._lst_stakeholder_col_order[5])
            _planned_sat_ = model.get_value(row,
                                            self._lst_stakeholder_col_order[6])
            _user_def_1_ = max(1.0, model.get_value(row,
                                          self._lst_stakeholder_col_order[10]))
            _user_def_2_ = max(1.0, model.get_value(row,
                                          self._lst_stakeholder_col_order[11]))
            _user_def_3_ = max(1.0, model.get_value(row,
                                          self._lst_stakeholder_col_order[12]))
            _user_def_4_ = max(1.0, model.get_value(row,
                                          self._lst_stakeholder_col_order[13]))
            _user_def_5_ = max(1.0, model.get_value(row,
                                          self._lst_stakeholder_col_order[14]))

            _improvement_ = 1.0 + 0.2 * (_planned_sat_ - _current_sat_)
            _overall_ = _priority_ * _improvement_ * _user_def_1_ * \
                        _user_def_2_ * _user_def_3_ * _user_def_4_ * \
                        _user_def_5_

            model.set_value(row, self._lst_stakeholder_col_order[7],
                            _improvement_)
            model.set_value(row, self._lst_stakeholder_col_order[8],
                            _overall_)

            _values_ = (model.get_value(row, self._lst_stakeholder_col_order[1]),
                        model.get_value(row, self._lst_stakeholder_col_order[2]),
                        model.get_value(row, self._lst_stakeholder_col_order[3]),
                        model.get_value(row, self._lst_stakeholder_col_order[4]),
                        model.get_value(row, self._lst_stakeholder_col_order[5]),
                        model.get_value(row, self._lst_stakeholder_col_order[6]),
                        model.get_value(row, self._lst_stakeholder_col_order[7]),
                        model.get_value(row, self._lst_stakeholder_col_order[8]),
                        model.get_value(row, self._lst_stakeholder_col_order[9]),
                        model.get_value(row, self._lst_stakeholder_col_order[10]),
                        model.get_value(row, self._lst_stakeholder_col_order[11]),
                        model.get_value(row, self._lst_stakeholder_col_order[12]),
                        model.get_value(row, self._lst_stakeholder_col_order[13]),
                        model.get_value(row, self._lst_stakeholder_col_order[14]),
                        self._app.REVISION.revision_id,
                        model.get_value(row, self._lst_stakeholder_col_order[0]))
            _query_ = "UPDATE tbl_stakeholder_input \
                       SET fld_stakeholder='%s', fld_description='%s', \
                           fld_group='%s', fld_priority=%d, \
                           fld_customer_rank=%d, fld_planned_rank=%d, \
                           fld_improvement=%f, fld_overall_weight=%f, \
                           fld_requirement_code='%s', fld_user_float_1=%f, \
                           fld_user_float_2=%f, fld_user_float_3=%f, \
                           fld_user_float_4=%f, fld_user_float_5=%f \
                       WHERE fld_revision_id=%d \
                       AND fld_input_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("requirement.py: Failed to save stakeholder inputs.")
                return True

            return False

        self._input_weight()
        _model_ = self.tvwStakeholderInput.get_model()
        _model_.foreach(_save_line_item)

        return False

    def _stakeholder_input_delete(self):
        """
        Method to delete the selected stakeholder input from the RTK Program
        Database.
        """

        (_model_, _row_) = self.tvwStakeholderInput.get_selection().get_selected()

        _query_ = "DELETE FROM tbl_stakeholder_input \
                   WHERE fld_input_id=%d" % \
                   _model_.get_value(_row_, self._lst_stakeholder_col_order[0])
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.user_log.error("requirement.py: Failed to delete requirement.")
            return True

        self._stakeholder_input_tab_load()

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the Requirement Object treeview model to the MySQL
        or SQLite3 database.

        Keyword Arguments:
        model -- the Requirement Object treemodel.
        path_ -- the path of the active row in the Requirement Object
                 treemodel.
        row   -- the selected row in the Requirement Object treeview.
        """

        _date_ = _util.date_to_ordinal(model.get_value(row,
                                            self._lst_col_order[9]))

        _values = (model.get_value(row, self._lst_col_order[2]), \
                   model.get_value(row, self._lst_col_order[3]), \
                   model.get_value(row, self._lst_col_order[4]), \
                   model.get_value(row, self._lst_col_order[5]), \
                   model.get_value(row, self._lst_col_order[6]), \
                   model.get_value(row, self._lst_col_order[7]), \
                   model.get_value(row, self._lst_col_order[8]), \
                   _date_, \
                   model.get_value(row, self._lst_col_order[10]), \
                   model.get_value(row, self._lst_col_order[11]), \
                   model.get_value(row, self._lst_col_order[12]), \
                   model.get_value(row, self._lst_col_order[13]), \
                   model.get_value(row, self._lst_col_order[14]), \
                   model.get_value(row, self._lst_col_order[15]), \
                   model.get_value(row, self._lst_col_order[16]), \
                   model.get_value(row, self._lst_col_order[17]), \
                   model.get_value(row, self._lst_col_order[18]), \
                   model.get_value(row, self._lst_col_order[19]), \
                   model.get_value(row, self._lst_col_order[20]), \
                   model.get_value(row, self._lst_col_order[21]), \
                   model.get_value(row, self._lst_col_order[22]), \
                   model.get_value(row, self._lst_col_order[23]), \
                   model.get_value(row, self._lst_col_order[24]), \
                   model.get_value(row, self._lst_col_order[25]), \
                   model.get_value(row, self._lst_col_order[26]), \
                   model.get_value(row, self._lst_col_order[27]), \
                   model.get_value(row, self._lst_col_order[28]), \
                   model.get_value(row, self._lst_col_order[29]), \
                   model.get_value(row, self._lst_col_order[30]), \
                   model.get_value(row, self._lst_col_order[31]), \
                   model.get_value(row, self._lst_col_order[32]), \
                   model.get_value(row, self._lst_col_order[33]), \
                   model.get_value(row, self._lst_col_order[34]), \
                   model.get_value(row, self._lst_col_order[35]), \
                   model.get_value(row, self._lst_col_order[36]), \
                   model.get_value(row, self._lst_col_order[37]), \
                   model.get_value(row, self._lst_col_order[38]), \
                   model.get_value(row, self._lst_col_order[39]), \
                   model.get_value(row, self._lst_col_order[40]), \
                   model.get_value(row, self._lst_col_order[41]), \
                   model.get_value(row, self._lst_col_order[42]), \
                   model.get_value(row, self._lst_col_order[43]), \
                   model.get_value(row, self._lst_col_order[44]), \
                   model.get_value(row, self._lst_col_order[45]), \
                   model.get_value(row, self._lst_col_order[46]), \
                   model.get_value(row, self._lst_col_order[47]), \
                   model.get_value(row, self._lst_col_order[48]), \
                   model.get_value(row, self._lst_col_order[49]), \
                   model.get_value(row, self._lst_col_order[50]), \
                   model.get_value(row, self._lst_col_order[51]), \
                   model.get_value(row, self._lst_col_order[0]), \
                   model.get_value(row, self._lst_col_order[1]))

        query = "UPDATE tbl_requirements \
                 SET fld_assembly_id=%d, fld_requirement_desc='%s', \
                     fld_requirement_type='%s', fld_requirement_code='%s', \
                     fld_derived=%d, fld_parent_requirement='%s', \
                     fld_validated=%d, fld_validated_date=%d, \
                     fld_owner='%s', fld_specification='%s', \
                     fld_page_number='%s', fld_figure_number='%s', \
                     fld_parent_id=%d, fld_software_id=%d, fld_clear_q1=%d, \
                     fld_clear_q2=%d, fld_clear_q3=%d, fld_clear_q4=%d, \
                     fld_clear_q5=%d, fld_clear_q6=%d, fld_clear_q7=%d, \
                     fld_clear_q8=%d, fld_clear_q9=%d, fld_clear_q10=%d, \
                     fld_complete_q1=%d, fld_complete_q2=%d, \
                     fld_complete_q3=%d, fld_complete_q4=%d, \
                     fld_complete_q5=%d, fld_complete_q6=%d, \
                     fld_complete_q7=%d, fld_complete_q8=%d, \
                     fld_complete_q9=%d, fld_complete_q10=%d, \
                     fld_consistent_q1=%d, fld_consistent_q2=%d, \
                     fld_consistent_q3=%d, fld_consistent_q4=%d, \
                     fld_consistent_q5=%d, fld_consistent_q6=%d, \
                     fld_consistent_q7=%d, fld_consistent_q8=%d, \
                     fld_consistent_q9=%d, fld_consistent_q10=%d, \
                     fld_verifiable_q1=%d, fld_verifiable_q2=%d, \
                     fld_verifiable_q3=%d, fld_verifiable_q4=%d, \
                     fld_verifiable_q5=%d, fld_verifiable_q6=%d \
                 WHERE fld_revision_id=%d \
                 AND fld_requirement_id=%d" % _values
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("requirement.py: Failed to save requirement.")
            return True

        return False

    def _vandv_task_add(self, type_=0):
        """
        Adds a new Verification and Validation task to the selected
        Requirement to the Program's MySQL or SQLite3 database.

        Keyword Arguments:
        type_  -- type of add; 0 = add new task, 1 = assign existing task
        """

        if(type_ == 0):
            _task_name_ = _("New V & V Task")

            if(_conf.RTK_MODULES[0] == 1):
                _values_ = (self._app.REVISION.revision_id, _task_name_)
            else:
                _values_ = (0, _task_name_)

            _query_ = "INSERT INTO tbl_validation \
                       (fld_revision_id, fld_task_desc) \
                       VALUES (%d, '%s')" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)
            if not _results_:
                self._app.debug_log.error("requirement.py: Failed to add V&V task.")
                return True

            if(_conf.BACKEND == 'mysql'):
                _query_ = "SELECT LAST_INSERT_ID()"
            elif(_conf.BACKEND == 'sqlite3'):
                _query_ = "SELECT seq \
                           FROM sqlite_sequence \
                           WHERE name='tbl_validation'"
            _task_id_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

            if(_conf.RTK_MODULES[0] == 1):
                _values_ = (self._app.REVISION.revision_id, _task_id_[0][0],
                            self.model.get_value(self.selected_row, 1))
            else:
                _values_ = (0, _task_id_[0][0],
                            self.model.get_value(self.selected_row, 1))

            _query_ = "INSERT INTO tbl_validation_matrix \
                       (fld_revision_id, fld_validation_id, \
                        fld_requirement_id) \
                       VALUES (%d, %d, %d)" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)
            if not _results_:
                self._app.debug_log.error("requirement.py: Failed to add V&V task.")
                return True

            self._app.VALIDATION.load_tree()

        elif(type_ == 1):
            _model_ = self.cmbVandVTasks.get_model()
            _row_ = self.cmbVandVTasks.get_active_iter()
            _task_id_ = int(_model_.get_value(_row_, 1))

            if(_conf.RTK_MODULES[0] == 1):
                _values_ = (self._app.REVISION.revision_id, _task_id_,
                          self.model.get_value(self.selected_row, 1))
            else:
                _values_ = (0, _task_id_,
                            self.model.get_value(self.selected_row, 1))


            _query_ = "INSERT INTO tbl_validation_matrix \
                       (fld_revision_id, fld_validation_id, \
                        fld_requirement_id) \
                       VALUES (%d, %d, %d)" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("requirement.py: Failed to associate V&V task.")
                return True

        self._vandv_tab_load()

        return False

    def _vandv_tasks_save(self):
        """
        Saves the Validation Task list treeview information to the RTK Program
        database.
        """

        def _save_line_item(model, path_, row, self):
            """
            Saves each task associated with the selected Requirement to the RTK
            Program database.

            Keyword Arguments:
            self  -- the REQUIREMENT object.
            model -- the Validation Task list treemodel.
            path_ -- the path of the active row in the Validation Task list
                     treemodel.
            row   -- the selected row in the Validation Task list treeview.
            """

            _values_ = (model.get_value(row, self._lst_col_order[1]),
                        model.get_value(row, self._lst_col_order[2]),
                        model.get_value(row, self._lst_col_order[3]),
                        model.get_value(row, self._lst_col_order[4]),
                        model.get_value(row, self._lst_col_order[0]))

            _query_ = "UPDATE tbl_validation \
                       SET fld_task_desc='%s', fld_start_date='%s', \
                           fld_end_date='%s', fld_status=%f \
                       WHERE fld_validation_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("requirement.py: Failed to save V&V task.")
                return True

            return False

        model = self.tvwValidation.get_model()
        model.foreach(_save_line_item, self)

        return False

    def load_notebook(self):
        """
        Method to load the gtk.Notebook widgets for the selected REQUIREMENT
        object.
        """

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxRequirement)
        self._app.winWorkBook.show_all()

        if self.selected_row is not None:
            self._stakeholder_input_tab_load()
            self._general_data_tab_load()
            self._analysis_tab_load()
            self._vandv_tab_load()

        self._app.winWorkBook.set_title(_(u"RTK Work Book: Requirement"))

        self.nbkRequirement.set_page(1)

        self.btnAssign.hide()
        self.cmbVandVTasks.hide()

        return False

    def _callback_check(self, check, index):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check -- the checkbutton that called the function.
        index -- the position in the Requirement Object _attribute list
                 associated with the data from the calling checkbutton.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        _model_.set_value(_row_, index, check.get_active())

        return False

    def _callback_combo(self, combo, index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo  -- the combobox that called the function.
        index_ -- the position in the Requirement Object _attribute list
                  associated with the data from the calling combobox.
        """

        try:
            i = int(combo.get_active())
        except TypeError:
            _model_ = combo.get_model()
            _row_ = combo.get_active_iter()
            i = _model_.get_value(_row_, 1)

        if(index_ == 4):                    # Requirement type.
            self._create_code()
            i = combo.get_model().get_value(combo.get_active_iter(), 0)
        elif(index_ == 10):                 # Requirement owner.
            i = combo.get_model().get_value(combo.get_active_iter(), 0)

# Update the Requirement Tree.
        self.model.set_value(self.selected_row, index_, i)

        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        event   -- the gtk.gdk.Event that called this function.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Requirement Object _attribute list
                   associated with the data from the calling entry.
        """

        if(convert == 'text'):
            if(_index_ == 3):
                text_ = self.txtRequirement.get_text(*self.txtRequirement.get_bounds())
            else:
                text_ = entry.get_text()

        elif(convert == 'int'):
            text_ = int(entry.get_text())

        elif(convert == 'float'):
            text_ = float(entry.get_text().replace('$', ''))

# Update the Requirement Tree.
        try:
            self.model.set_value(self.selected_row, _index_, text_)
        except TypeError:                   # There are no requirements.
            return True

        return False

    def _create_code(self):
        """
        This function creates the Requirement code based on the type of
        requirement it is and it's index in the database.
        """

        cmbmodel = self.cmbRqmtType.get_model()
        cmbrow = self.cmbRqmtType.get_active_iter()

        prefix = cmbmodel.get_value(cmbrow, 1)
        suffix = str(self.model.get_value(self.selected_row, 1))

        zeds = 4 - len(suffix)
        pad = '0' * zeds

        code = '%s-%s%s' % (prefix, pad, suffix)

        self.model.set_value(self.selected_row, 5, code)
        self.txtCode.set_text(code)

        return False

    def _input_weight(self):
        """
        Method for calculating the overall weighting of a stakeholder input.
        """

        (_model_, _row_) = self.tvwStakeholderInput.get_selection().get_selected()

        _priority_ = _model_.get_value(_row_,
                                       self._lst_stakeholder_col_order[4])
        _current_sat_ = _model_.get_value(_row_,
                                          self._lst_stakeholder_col_order[5])
        _planned_sat_ = _model_.get_value(_row_,
                                          self._lst_stakeholder_col_order[6])
        _user_def_1_ = max(1.0, _model_.get_value(_row_,
                                        self._lst_stakeholder_col_order[10]))
        _user_def_2_ = max(1.0, _model_.get_value(_row_,
                                        self._lst_stakeholder_col_order[11]))
        _user_def_3_ = max(1.0, _model_.get_value(_row_,
                                        self._lst_stakeholder_col_order[12]))
        _user_def_4_ = max(1.0, _model_.get_value(_row_,
                                        self._lst_stakeholder_col_order[13]))
        _user_def_5_ = max(1.0, _model_.get_value(_row_,
                                        self._lst_stakeholder_col_order[14]))

        _improvement_ = 1.0 + 0.2 * (_planned_sat_ - _current_sat_)
        _overall_ = _priority_ * _improvement_ * _user_def_1_ * _user_def_2_ * \
                    _user_def_3_ * _user_def_4_ * _user_def_5_

        _model_.set_value(_row_, self._lst_stakeholder_col_order[7], _improvement_)
        _model_.set_value(_row_, self._lst_stakeholder_col_order[8], _overall_)

        return False

    def _notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the REQUIREMENT Object's Work Book notebook page is
        changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = Stakeholder Input
                    1 = General Data
                    2 = Analysis
                    3 = V&V Tasks
        """

        if(page_num == 0):
            self.btnAdd.set_tooltip_text(_(u"Adds one or more new stakeholder inputs to the RTK Program Database."))
            self.btnRemove.set_tooltip_text(_(u"Removes the selected stakeholder input from the RTK Program Database."))
            self.btnSave.set_tooltip_text(_(u"Saves the selected stakeholder input to the RTK Program Database."))
            self.btnAdd.show()
            self.btnAddChild.hide()
            self.btnAddSibling.hide()
            self.btnRemove.show()
            self.btnSave.show()
            self.btnAssign.hide()
            self.cmbVandVTasks.hide()
        elif(page_num == 1):
            self.btnRemove.set_tooltip_text(_("Removes the selected requirement from the RTK Program Database."))
            self.btnSave.set_tooltip_text(_("Saves the selected requirement to the RTK Program Database."))
            self.btnAdd.hide()
            self.btnAddChild.show()
            self.btnAddSibling.show()
            self.btnRemove.show()
            self.btnSave.show()
            self.btnAssign.hide()
            self.cmbVandVTasks.hide()
        elif(page_num == 2):
            self.btnRemove.set_tooltip_text(_("Removes the selected requirement from the RTK Program Database."))
            self.btnSave.set_tooltip_text(_("Saves the selected requirement to the RTK Program Database."))
            self.btnAdd.hide()
            self.btnAddChild.show()
            self.btnAddSibling.show()
            self.btnRemove.show()
            self.btnSave.show()
            self.btnAssign.hide()
            self.cmbVandVTasks.hide()
        elif(page_num == 3):
            self.btnAdd.set_tooltip_text(_(u"Adds one or more new V&V tasks to the RTK Program Database and assignes them to the selected requirement."))
            self.btnRemove.set_tooltip_text(_("Removes the selected V&V task from the requirement."))
            self.btnSave.set_tooltip_text(_("Saves the selected requirement to the RTK Program Database."))
            self.btnAdd.show()
            self.btnAddChild.show()
            self.btnAddSibling.show()
            self.btnRemove.show()
            self.btnSave.show()
            self.btnAssign.show()
            self.cmbVandVTasks.show()

    def _toolbutton_pressed(self, button):
        """
        Method to reacte to the ASSEMBLY Object toolbar button clicked events.

        Keyword Arguments:
        button -- the toolbar button that was pressed.
        """

        _button_ = button.get_name()
        _page_ = self.nbkRequirement.get_current_page()

        if(_page_ == 0):                    # Stakeholder Input tab.
            if(_button_ == 'Add'):
                self._stakeholder_input_add()
            elif(_button_ == 'Remove'):
                self._stakeholder_input_delete()
            elif(_button_ == 'Save'):
                self._stakeholder_input_save()
        elif(_page_ == 1 or _page_ == 2):   # General Data tab.
            if(_button_ == 'Remove'):
                self._requirement_delete()
            elif(_button_ == 'Save'):
                self.requirement_save(None)
        elif(_page_ == 3):                  # V&V Tasks tab.
            if(_button_ == 'Add'):
                self._vandv_task_add(0)
            elif(_button_ == 'Assign'):
                self._vandv_task_add(1)
            elif(_button_ == 'Remove'):
                print "Lets remove this validation task"
            elif(_button_ == 'Save'):
                self._vandv_tasks_save()

        return False
