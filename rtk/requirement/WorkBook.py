#!/usr/bin/env python
"""
##################################
Requirement Package Work Book View
##################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.requirement.WorkBook.py is part of The RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

from datetime import datetime

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
from Assistants import AddRequirement

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
    The Work Book view displays all the attributes for the selected
    Requirement.  The attributes of a Work Book view are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Requirement attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |      0   |                                           |
    +----------+-------------------------------------------+
    |      1   |                                           |
    +----------+-------------------------------------------+
    |      2   | txtRequirement `focus_out_event`          |
    +----------+-------------------------------------------+
    |      3   |                                           |
    +----------+-------------------------------------------+
    |      4   | cmbRqmtType `changed`                     |
    +----------+-------------------------------------------+
    |      5   | cmbPriority `changed`                     |
    +----------+-------------------------------------------+
    |      6   | txtSpecification `focus_out_event`        |
    +----------+-------------------------------------------+
    |      7   | txtPageNumber `focus_out_event`           |
    +----------+-------------------------------------------+
    |      8   | txtFigureNumber `focus_out_event`         |
    +----------+-------------------------------------------+
    |      9   | chkDerived `toggled`                      |
    +----------+-------------------------------------------+
    |     10   | cmbOwner `changed`                        |
    +----------+-------------------------------------------+
    |     11   | chkValidated `toggled`                    |
    +----------+-------------------------------------------+
    |     12   | txtValidateDate `changed`                 |
    +----------+-------------------------------------------+
    |     13   | btnValidateDate `clicked`                 |
    +----------+-------------------------------------------+
    |     14   | btnAddInput `clicked`                     |
    +----------+-------------------------------------------+
    |     15   | btnDeleteInput `clicked`                  |
    +----------+-------------------------------------------+
    |     16   | btnCalculateInputs `clicked`              |
    +----------+-------------------------------------------+
    |     17   | btnSaveInputs `clicked`                   |
    +----------+-------------------------------------------+

    :ivar _modulebook: the :py:class:`rtk.requirement.ModuleBook` associated
                       with this Work Book.
    :ivar _rqmt_model: the :py:class:`rtk.requirement.Requirement.Model` whose
                       attributes are being displayed.
    :ivar _stakeholder_model: the :py:class:`rtk.stakeholder.Stakeholder.Model`
                              whose attributes are being displayed.
    :ivar self.dtcRequirement: the :py:class:`rtk.requirement.Requirement.Requirement`
                               data controller associated with this Work Book.
    :ivar dtcStakeholder: the :py:class:`rtk.stakeholder.Stakeholder.Syakeholder`
                          data controller associated with this Work Book.
    :ivar dtcMatrices: the :py:class:`rtk.gui.gtk.Matrix.Matrix` data
                       controller associated with this Work Book.
    :ivar gtk.Button btnAddInput: the gtk.Button() used to add a Stakeholder
                                  input.
    :ivar gtk.Button btnRemoveInput: the gtk.Button() used to delete a
                                     Stakeholder input.
    :ivar gtk.Button btnCalculateInputs: the gtk.Button() used to calculate
                                         Stakeholder input priorities.
    :ivar gtk.Button btnSaveInputs: the gtk.Button() used to save Stakeholder
                                    inputs.
    :ivar gtk.Button btnValidateDate: the gtk.Button() used to launch a
                                      calendar for selecting the date the
                                      Requirement was validated.
    :ivar gtk.CheckButton chkDerived: the gtk.CheckButton() used to indicate
                                      whether or not the selected Requirement
                                      is derived.
    :ivar gtk.CheckButton chkValidated: the gtk.CheckButton() used to indicate
                                        whether or not the selected Requirement
                                        has been validated.
    :ivar gtk.ComboBox cmbOwner: the gtk.ComboBox() used to select the owning
                                 organization for the Requirement.
    :ivar gtk.ComboBox cmbRqmtType: the gtk.ComboBox() used to select the type
                                    of Requirement.
    :ivar gtk.ComboBox cmbPriority: the gtk.ComboBox() used to select the
                                    priority of the Requirement.
    :ivar gtk.Entry txtCode: the gtk.Entry() used to enter and display the
                             unique, identifying code for the Requirement.
    :ivar gtk.Entry txtSpecification: the gtk.Entry() used to enter and display
                                      any specification associated with the
                                      Requirement.
    :ivar gtk.Entry txtPageNumber: the gtk.Entry() used to enter and display
                                   the page number of the specification
                                   associated with the Requirement.
    :ivar gtk.Entry txtFigureNumber: the gtk.Entry() used to enter and display
                                     the figure number in the specification
                                     associated with the Requirement.
    :ivar gtk.Entry txtValidatedDate: the gtk.Entry() used to enter and display
                                      the date the Requirement was validated.
    :ivar gtk.TextView txtRequirement: the gtk.TextView() used to enter and
                                       display the description of the
                                       Requirement.
    :ivar gtk.TreeView tvwStakeholderInput: the gtk.TreeView() used to display
                                            and edit the Stakeholder inputs
                                            from which the Requirements are
                                            derived.
    :ivar gtk.TreeView tvwClear: the gtk.TreeView() used to display and edit
                                 the clarity assessment of the Requirement.
    :ivar gtk.TreeView tvwComplete: the gtk.TreeView() used to display and edit
                                    the completeness assessment of the
                                    Requirement.
    :ivar gtk.TreeView tvwConsistent: the gtk.TreeView() used to display and
                                      edit the consistency assessment of the
                                      Requirement.
    :ivar gtk.TreeView tvwVerifiable: the gtk.TreeView() used to display and
                                      edit the verifiability assessment of the
                                      Requirement.
    """

    def __init__(self, modulebook):
        """
        Initializes the Work Book view for the Requirement package.

        :param modulebook: the :py:class:`rtk.requirement.ModuleBook` to
                           associate with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Define private dict attributes.

        # Define private list attributes.
        self._lst_handler_id = [i for i in range(18)]

        # Define private scalar attributes.
        self._modulebook = modulebook
        self._rqmt_model = None
        self._stakeholder_model = None

        # Define public dict attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.dtcRequirement = modulebook.mdcRTK.dtcRequirement
        self.dtcStakeholder = modulebook.mdcRTK.dtcStakeholder
        self.dtcMatrices = modulebook.mdcRTK.dtcMatrices

        # Stakeholder input page widgets.
        (self.tvwStakeholderInput,
         self._lst_stakeholder_col_order) = Widgets.make_treeview(
             'Stakeholder', 10)

        self.btnAddInput = Widgets.make_button(width=35, image='add')
        self.btnRemoveInput = Widgets.make_button(width=35, image='remove')
        self.btnCalculateInputs = Widgets.make_button(width=35,
                                                      image='calculate')
        self.btnSaveInputs = Widgets.make_button(width=35, image='save')

        # General data page widgets.
        self.btnValidateDate = Widgets.make_button(height=25, width=25,
                                                   label="...",
                                                   image='calendar')

        self.chkDerived = Widgets.make_check_button()
        self.chkValidated = Widgets.make_check_button()

        self.cmbOwner = Widgets.make_combo(simple=False)
        self.cmbRqmtType = Widgets.make_combo(simple=False)
        self.cmbPriority = Widgets.make_combo(width=50, simple=True)

        self.txtCode = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtFigureNumber = Widgets.make_entry()
        self.txtPageNumber = Widgets.make_entry()
        self.txtRequirement = Widgets.make_text_view(width=400)
        self.txtSpecification = Widgets.make_entry()
        self.txtValidatedDate = Widgets.make_entry(width=100)

        # Requirement analysis page widgets.
        self.tvwClear = gtk.TreeView()
        self.tvwComplete = gtk.TreeView()
        self.tvwConsistent = gtk.TreeView()
        self.tvwVerifiable = gtk.TreeView()

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Requirement class work book.

        :return: _toolbar
        :rtype: gtk.ToolBar()
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add sibling requirement button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new requirement at the same level "
                                   u"as the selected requirement."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR +
                             '32x32/insert_sibling.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_add_requirement, 0)
        _toolbar.insert(_button, _position)
        _position += 1

        # Add child (derived) requirement button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new requirement subordinate to "
                                   u"the selected requirement."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/insert_child.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_add_requirement, 1)
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete requirement button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_delete_requirement)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Create report buttons.
        # FIXME: See bug 183.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(_(u"Create Requirement reports."))
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/reports.png')

        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Stakeholder Inputs"))
        _menu_item.set_tooltip_text(_(u"Creates the stakeholder inputs report "
                                      u"for the currently selected revision."))
        # _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Requirements Listing"))
        _menu_item.set_tooltip_text(_(u"Creates the requirements listing "
                                      u"for the currently selected revision."))
        # _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"V&V Task Listing"))
        _menu_item.set_tooltip_text(_(u"Creates a report of the V&V tasks "
                                      u"for the currently selected revision "
                                      u"sorted by requirement."))
        # _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _position)
        _position += 1
        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save requirement button.
        _button = gtk.ToolButton()
        _image = gtk.Image()

        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_save_requirements)
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Requirement class gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook()
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

        self._create_stakeholder_input_page(_notebook)
        self._create_general_data_page(_notebook)
        self._create_analysis_page(_notebook)

        return _notebook

    def _create_stakeholder_input_page(self, notebook):
        """
        Method to create the Stakeholder Input gtk.Notebook() page and
        populate it with the appropriate widgets.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the
                                      Stakeholder inputs page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwStakeholderInput)

        _frame = Widgets.make_frame(label=_(u"Stakeholder Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddInput, False, False)
        _bbox.pack_start(self.btnRemoveInput, False, False)
        _bbox.pack_start(self.btnCalculateInputs, False, False)
        _bbox.pack_start(self.btnSaveInputs, False, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display stakeholder input           #
        # information.                                                  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.btnAddInput.set_tooltip_text(_(u"Adds one or more stakeholder "
                                            u"inputs to the list."))
        self.btnRemoveInput.set_tooltip_text(_(u"Removes the selected "
                                               u"stakeholder inputs from the "
                                               u"list."))
        self.btnCalculateInputs.set_tooltip_text(_(u"Calculates the "
                                                   u"stakeholder input "
                                                   u"improvement factors and "
                                                   u"overall weightings."))
        self.btnSaveInputs.set_tooltip_text(_(u"Saves the stakeholder input "
                                              u"list."))

        # Set the has-entry property for stakeholder and affinity group
        # gtk.CellRendererCombo cells.  Connect the edited signal to the
        # callback function that updates the model to include the new
        # entry that is manually entered by the user.
        for i in [1, 3]:
            _cell = self.tvwStakeholderInput.get_column(
                self._lst_stakeholder_col_order[i]).get_cell_renderers()
            _cell[0].set_property('has-entry', True)
            _cell[0].connect('edited', self._add_to_combo, i)

        # Set the priority, customer rating, and planned rating
        # gtk.CellRendererSpin to integer spins with increments of 1.
        # Make it an integer spin by setting the number of digits to 0.
        for i in range(4, 7):
            _cell = self.tvwStakeholderInput.get_column(
                self._lst_stakeholder_col_order[i]).get_cell_renderers()
            _adjustment = _cell[0].get_property('adjustment')
            _adjustment.set_step_increment(1)
            _cell[0].set_property('adjustment', _adjustment)
            _cell[0].set_property('digits', 0)

        # Center fields and connect to the callback.
        for i in [2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            _cell = self.tvwStakeholderInput.get_column(
                self._lst_stakeholder_col_order[i]).get_cell_renderers()
            _cell[0].set_alignment(xalign=0.5, yalign=0.5)
            _cell[0].connect('edited', self._on_stakeholder_cell_edit, i)

        # Connect to callback functions.
        self._lst_handler_id[14] = self.btnAddInput.connect(
            'clicked', self._on_button_clicked, 14)
        self._lst_handler_id[15] = self.btnRemoveInput.connect(
            'clicked', self._on_button_clicked, 15)
        self._lst_handler_id[16] = self.btnCalculateInputs.connect(
            'clicked', self._on_button_clicked, 16)
        self._lst_handler_id[17] = self.btnSaveInputs.connect(
            'clicked', self._on_button_clicked, 17)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Stakeholder\nInputs") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(_(u"Displays stakeholder inputs."))
        _label.show_all()
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_general_data_page(self, notebook):
        """
        Method to create the Requirement class gtk.Notebook() page for
        displaying general data about the selected Requirement.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the general
                                       data tab.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _frame = Widgets.make_frame(label=_(u"General Information"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the requirement type gtk.ComboBox().
        _model = self.cmbRqmtType.get_model()
        _model.clear()
        _model.append(None, ["", "", ""])
        # Each _type is [Description, Code, ID]
        for __, _type in enumerate(Configuration.RTK_REQUIREMENT_TYPES):
            _model.append(None, [_type[0], _type[1], ""])

        # Load the owner gtk.ComboBox().
        _model = self.cmbOwner.get_model()
        _owners = self._modulebook.dicOwners.keys()
        _owners.sort()
        _model.clear()
        _model.append(None, ["", "", ""])
        for _owner in _owners:
            _model.append(None, [_owner, "", ""])

        # Load the priority gtk.Combo().
        _results = [['1'], ['2'], ['3'], ['4'], ['5']]
        _model = self.cmbPriority.get_model()
        Widgets.load_combo(self.cmbPriority, _results)

        _labels = [_(u"Requirement ID:"), _(u"Requirement:"),
                   _(u"Requirement Type:"), _(u"Specification:"),
                   _(u"Page Number:"), _(u"Figure Number:"),
                   _(u"Derived:"), _(u"Validated:"), _(u"Owner:"),
                   _(u"Priority:"), _(u"Validated Date:")]
        (_x_pos, _y_pos) = Widgets.make_labels(_labels[2:10], _fixed, 5, 140)
        _x_pos += 50

        # Create the tooltips.
        self.txtCode.set_tooltip_text(_(u"Displays the unique code for "
                                        u"the selected requirement."))
        self.txtRequirement.set_tooltip_text(_(u"Detailed description of the "
                                               u"requirement."))
        self.cmbRqmtType.set_tooltip_text(_(u"Selects and displays the "
                                            u"type of requirement for the "
                                            u"selected requirement."))
        self.txtSpecification.set_tooltip_text(_(u"Displays the internal "
                                                 u"or industry "
                                                 u"specification "
                                                 u"associated with the "
                                                 u"selected requirement."))
        self.txtPageNumber.set_tooltip_text(_(u"Displays the "
                                              u"specification page number "
                                              u"associated with the "
                                              u"selected requirement."))
        self.txtFigureNumber.set_tooltip_text(_(u"Displays the "
                                                u"specification figure "
                                                u"number associated with "
                                                u"the selected "
                                                u"requirement."))
        self.chkDerived.set_tooltip_text(_(u"Whether or not the selected "
                                           u"requirement is derived."))
        self.chkValidated.set_tooltip_text(_(u"Whether or not the "
                                             u"selected requirement has "
                                             u"been verified and "
                                             u"validated."))
        self.txtValidatedDate.set_tooltip_text(_(u"Displays the date the "
                                                 u"selected requirement "
                                                 u"was verified and "
                                                 u"validated."))
        self.btnValidateDate.set_tooltip_text(_(u"Launches the calendar "
                                                u"to select the date the "
                                                u"requirement was "
                                                u"validated."))
        self.cmbOwner.set_tooltip_text(_(u"Displays the responsible "
                                         u"organization or individual for "
                                         u"the selected requirement."))
        self.cmbPriority.set_tooltip_text(_(u"Selects and displays the "
                                            u"priority of the selected "
                                            u"requirement."))

        # Place the widgets.
        _label = Widgets.make_label(_labels[0], 150, 25)
        _fixed.put(_label, 5, 5)
        _fixed.put(self.txtCode, _x_pos, 5)

        _label = Widgets.make_label(_labels[1], 150, 25)
        _fixed.put(_label, 5, 35)
        _fixed.put(self.txtRequirement, _x_pos, 35)
        _fixed.put(self.cmbRqmtType, _x_pos, _y_pos[0])
        _fixed.put(self.txtSpecification, _x_pos, _y_pos[1])
        _fixed.put(self.txtPageNumber, _x_pos, _y_pos[2])
        _fixed.put(self.txtFigureNumber, _x_pos, _y_pos[3])
        _fixed.put(self.chkDerived, _x_pos, _y_pos[4])
        _fixed.put(self.chkValidated, _x_pos, _y_pos[5])

        _label = Widgets.make_label(_labels[10], 150, 25)

        _fixed.put(_label, _x_pos + 25, _y_pos[5])

        _fixed.put(self.txtValidatedDate, _x_pos + 200, _y_pos[5])
        _fixed.put(self.btnValidateDate, _x_pos + 305, _y_pos[5])
        _fixed.put(self.cmbOwner, _x_pos, _y_pos[6])
        _fixed.put(self.cmbPriority, _x_pos, _y_pos[7])

        # Connect to callback functions.
        _textview = self.txtRequirement.get_child().get_child()
        self._lst_handler_id[2] = _textview.connect('focus-out-event',
                                                    self._on_focus_out, 2)
        self._lst_handler_id[4] = self.cmbRqmtType.connect(
            'changed', self._on_combo_changed, 4)
        self._lst_handler_id[5] = self.cmbPriority.connect(
            'changed', self._on_combo_changed, 5)

        self._lst_handler_id[6] = self.txtSpecification.connect(
            'focus-out-event', self._on_focus_out, 6)
        self._lst_handler_id[7] = self.txtPageNumber.connect(
            'focus-out-event', self._on_focus_out, 7)
        self._lst_handler_id[8] = self.txtFigureNumber.connect(
            'focus-out-event', self._on_focus_out, 8)
        self._lst_handler_id[9] = self.chkDerived.connect('toggled',
                                                          self._on_toggled, 9)
        self._lst_handler_id[10] = self.cmbOwner.connect(
            'changed', self._on_combo_changed, 10)
        self._lst_handler_id[11] = self.chkValidated.connect('toggled',
                                                             self._on_toggled,
                                                             11)
        self._lst_handler_id[12] = self.txtValidatedDate.connect(
            'changed', self._on_focus_out, None, 12)
        self._lst_handler_id[13] = self.btnValidateDate.connect(
            'button-release-event', Widgets.date_select,
            self.txtValidatedDate)

        _fixed.show_all()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"General\nData") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(_(u"Displays general information about the "
                                  u"selected requirement."))
        _label.show_all()
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_analysis_page(self, notebook):
        """
        Method to create the page for analyzing the selected requirement.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the analysis
                                      page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HPaned()

        # Create quadrant #1 (upper left) for determining if the
        # requirement is clear.
        _vpaned = gtk.VPaned()
        _hpaned.pack1(_vpaned, resize=False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwClear)

        _frame = Widgets.make_frame(label=_(u"Clarity of Requirement"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, resize=False)

        # Create quadrant #3 (lower left) for determining if the
        # requirement is complete.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwComplete)

        _frame = Widgets.make_frame(label=_(u"Completeness of Requirement"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, resize=False)

        # Create quadrant #2 (upper right) for determining if the
        # requirement is consistent.
        _vpaned = gtk.VPaned()
        _hpaned.pack2(_vpaned, resize=False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwConsistent)

        _frame = Widgets.make_frame(label=_(u"Consistency of Requirement"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, resize=False)

        # Create quadrant #4 (lower right) for determining if the
        # requirement is verifiable.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwVerifiable)

        _frame = Widgets.make_frame(label=_(u"Verifiability of Requirement"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, resize=False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display requirements analysis       #
        # information.                                                  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_INT)
        self.tvwClear.set_model(_model)
        self.tvwClear.set_property('enable-grid-lines', True)
        self.tvwClear.set_headers_visible(False)

        # Create the columns for the clarity questions.
        _column = gtk.TreeViewColumn()

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('visible', 0)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 650)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _cell.connect('toggled', self._on_analysis_cell_edit, _model, 0)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=2)

        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self.tvwClear.append_column(_column)

        # Create the treeview for the completeness questions.
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_INT)
        self.tvwComplete.set_model(_model)
        self.tvwComplete.set_property('enable-grid-lines', True)
        self.tvwComplete.set_headers_visible(False)

        _column = gtk.TreeViewColumn()

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('visible', 0)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 650)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _cell.connect('toggled', self._on_analysis_cell_edit, _model, 1)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=2)

        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self.tvwComplete.append_column(_column)

        # Create the treeview for the consistent questions.
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_INT)
        self.tvwConsistent.set_model(_model)
        self.tvwConsistent.set_property('enable-grid-lines', True)
        self.tvwConsistent.set_headers_visible(False)

        _column = gtk.TreeViewColumn()

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('visible', 0)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 650)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _cell.connect('toggled', self._on_analysis_cell_edit, _model, 2)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=2)

        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self.tvwConsistent.append_column(_column)

        # Create the treeview for the verifiability questions.
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_INT)
        self.tvwVerifiable.set_model(_model)
        self.tvwVerifiable.set_property('enable-grid-lines', True)
        self.tvwVerifiable.set_headers_visible(False)

        _column = gtk.TreeViewColumn()

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('visible', 0)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 650)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)

        _cell = gtk.CellRendererToggle()
        _cell.set_property('activatable', 1)
        _cell.connect('toggled', self._on_analysis_cell_edit, _model, 3)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, active=2)

        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

        self.tvwVerifiable.append_column(_column)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Analysis") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_tooltip_text(_(u"Analyzes the selected requirement."))
        _label.show_all()
        notebook.insert_page(_hpaned, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Requirement class gtk.Notebook().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._rqmt_model = model

        # Load the Stakeholder Inputs page.
        self._load_stakeholder_input_page()

        try:
            _type = self._rqmt_model.requirement_type
            _idx = self._modulebook.dicRequirementTypes[_type][1]
        except KeyError:
            _idx = 0
        self.cmbRqmtType.set_active(_idx)

        try:
            _owner = self._rqmt_model.owner
            _idx = self._modulebook.dicOwners[_owner][1] + 1
        except KeyError:
            _idx = 0
        self.cmbOwner.set_active(_idx)

        self.chkDerived.set_active(self._rqmt_model.derived)
        self.chkValidated.set_active(self._rqmt_model.validated)

        self.cmbPriority.set_active(int(self._rqmt_model.priority))

        self.txtCode.set_text(self._rqmt_model.requirement_code)
        self.txtFigureNumber.set_text(self._rqmt_model.figure_number)
        self.txtPageNumber.set_text(self._rqmt_model.page_number)
        _textbuffer = self.txtRequirement.get_child().get_child().get_buffer()
        _textbuffer.set_text(self._rqmt_model.description)
        self.txtSpecification.set_text(self._rqmt_model.specification)

        if self._rqmt_model.validated != 1:
            self._rqmt_model.validated_date = Utilities.date_to_ordinal(
                datetime.today())
        self.txtValidatedDate.set_text(
            Utilities.ordinal_to_date(self._rqmt_model.validated_date))

        # Load the requirements analysis page.
        self._load_analysis_page()

        return False

    def _load_stakeholder_input_page(self):
        """
        Method to load the Stakeholder input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _cell = self.tvwStakeholderInput.get_column(
            self._lst_stakeholder_col_order[1]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        for i in range(len(Configuration.RTK_STAKEHOLDERS)):
            _model.append([Configuration.RTK_STAKEHOLDERS[i][0]])

        _cell = self.tvwStakeholderInput.get_column(
            self._lst_stakeholder_col_order[3]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        for i in range(len(Configuration.RTK_AFFINITY_GROUPS)):
            _model.append([Configuration.RTK_AFFINITY_GROUPS[i][0]])

        # Load the Requirement gtk.CellRendererCombo() with a list of existing
        # Requirements.
        _cell = self.tvwStakeholderInput.get_column(
            self._lst_stakeholder_col_order[9]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        _model.append([""])
        for _requirement in self.dtcRequirement.dicRequirements.values():
            _model.append([_requirement.requirement_code + '-' +
                           _requirement.description])

        # Now load the Stakeholder Inputs gtk.TreeView.
        _model = self.tvwStakeholderInput.get_model()
        _model.clear()
        for _input in self.dtcStakeholder.dicStakeholders.values():
            _data = (_input.input_id, _input.stakeholder, _input.description,
                     _input.group, _input.priority, _input.customer_rank,
                     _input.planned_rank, _input.improvement,
                     _input.overall_weight, _input.requirement,
                     _input.lst_user_floats[0], _input.lst_user_floats[1],
                     _input.lst_user_floats[2], _input.lst_user_floats[3],
                     _input.lst_user_floats[4])
            _model.append(None, _data)

        return False

    def _load_analysis_page(self):
        """
        Method to load the requirements analysis page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Load the clarity gtk.TreeView().
        _clear = [_(u"The requirement clearly states what is needed or "
                    u"desired."),
                  _(u"The requirement is unambiguous and not open to "
                    u"interpretation."),
                  _(u"All terms that can have more than one meaning are "
                    u"qualified so that the desired meaning is readily "
                    u"apparent."),
                  _(u"Diagrams, drawings, etc. are used to increase "
                    u"understanding of the requirement."),
                  _(u"The requirement is free from spelling and "
                    u"grammatical errors."),
                  _(u"The requirement is written in non-technical "
                    u"language using the vocabulary of the stakeholder."),
                  _(u"Stakeholders understand the requirement as written."),
                  _(u"The requirement is clear enough to be turned over "
                    u"to an independent group and still be understood."),
                  _(u"The requirement avoids stating how the problem is "
                    u"to be solved or what techniques are to be used.")]

        _count = len(_clear) - len(self._rqmt_model.lst_clear)
        if _count > 0:
            self._rqmt_model.lst_clear = \
                self._rqmt_model.lst_clear + [0] * _count

        _model = self.tvwClear.get_model()
        _model.clear()
        for _index, _clarity in enumerate(_clear):
            _data = [_index, _clarity,
                     self._rqmt_model.lst_clear[_index]]

            _model.append(_data)

        # Load the completeness gtk.TreeView().
        _complete = [_(u"Performance objectives are properly documented "
                       u"from the user's point of view."),
                     _(u"No necessary information is missing from the "
                       u"requirement."),
                     _(u"The requirement has been assigned a priority."),
                     _(u"The requirement is realistic given the technology "
                       u"that will used to implement the system."),
                     _(u"The requirement is feasible to implement given the "
                       u"defined project time frame, scope, structure and "
                       u"budget."),
                     _(u"If the requirement describes something as a "
                       u"'standard' the specific source is cited."),
                     _(u"The requirement is relevant to the problem and its "
                       u"solution."),
                     _(u"The requirement contains no implied design details."),
                     _(u"The requirement contains no implied implementation "
                       u"constraints."),
                     _(u"The requirement contains no implied project "
                       u"management constraints.")]

        _count = len(_complete) - len(self._rqmt_model.lst_complete)
        if _count > 0:
            self._rqmt_model.lst_complete = \
                self._rqmt_model.lst_complete + [0] * _count

        _model = self.tvwComplete.get_model()
        _model.clear()
        for _index, _completeness in enumerate(_complete):
            _data = [_index, _completeness,
                     self._rqmt_model.lst_complete[_index]]
            _model.append(_data)

        # Load the consistency gtk.TreeView().
        _consistent = [_(u"The requirement describes a single need or want; "
                         u"it could not be broken into several different "
                         u"requirements."),
                       _(u"The requirement requires non-standard hardware or "
                         u"must use software to implement."),
                       _(u"The requirement can be implemented within known "
                         u"constraints."),
                       _(u"The requirement provides an adequate basis for "
                         u"design and testing."),
                       _(u"The requirement adequately supports the business "
                         u"goal of the project."),
                       _(u"The requirement does not conflict with some "
                         u"constraint, policy or regulation."),
                       _(u"The requirement does not conflict with another "
                         u"requirement."),
                       _(u"The requirement is not a duplicate of another "
                         u"requirement."),
                       _(u"The requirement is in scope for the project.")]

        _count = len(_consistent) - len(self._rqmt_model.lst_consistent)
        if _count > 0:
            self._rqmt_model.lst_consistent = \
                self._rqmt_model.lst_consistent + [0] * _count

        _model = self.tvwConsistent.get_model()
        _model.clear()
        for _index, _consistency in enumerate(_consistent):
            _data = [_index, _consistency,
                     self._rqmt_model.lst_consistent[_index]]

            _model.append(_data)

        # Load the verifiable gtk.TreeView().
        _verifiable = [_(u"The requirement is verifiable by testing, "
                         u"demonstration, review, or analysis."),
                       _(u"The requirement lacks 'weasel words' (e.g. "
                         u"various, mostly, suitable, integrate, maybe, "
                         u"consistent, robust, modular, user-friendly, "
                         u"superb, good)."),
                       _(u"Any performance criteria are quantified such that "
                         u"they are testable."),
                       _(u"Independent testing would be able to determine "
                         u"whether the requirement has been satisfied."),
                       _(u"The task(s) that will validate and verify the "
                         u"final design satisfies the requirement have been "
                         u"identified."),
                       _(u"The identified V&V task(s) have been added to "
                         u"the validation plan (e.g., DVP)")]

        _count = len(_verifiable) - len(self._rqmt_model.lst_verifiable)
        if _count > 0:
            self._rqmt_model.lst_verifiable = \
                self._rqmt_model.lst_verifiable + [0] * _count

        _model = self.tvwVerifiable.get_model()
        _model.clear()
        for _index, _verify in enumerate(_verifiable):
            _data = [_index, _verify,
                     self._rqmt_model.lst_verifiable[_index]]

            _model.append(_data)

        return False

    def update(self):
        """
        Method to update the Work Book widgets with changes to the Requirement
        data model attributes.  Called by other views when the Requirement data
        model attributes are edited via their gtk.Widgets().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbRqmtType.handler_block(self._lst_handler_id[4])
        try:
            _type = self._rqmt_model.requirement_type
            _idx = self._modulebook.dicRequirementTypes[_type][1]
        except KeyError:
            _idx = 0
        self.cmbRqmtType.set_active(_idx)
        self.cmbRqmtType.handler_unblock(self._lst_handler_id[4])
        self.cmbOwner.handler_block(self._lst_handler_id[10])
        try:
            _owner = self._rqmt_model.owner
            _idx = self._modulebook.dicOwners[_owner][1] + 1
        except KeyError:
            _idx = 0
        self.cmbOwner.set_active(_idx)
        self.cmbOwner.handler_unblock(self._lst_handler_id[10])

        self.chkDerived.set_active(self._rqmt_model.derived)
        self.chkValidated.set_active(self._rqmt_model.validated)
        self.cmbPriority.set_active(int(self._rqmt_model.priority))

        self.txtCode.set_text(self._rqmt_model.requirement_code)
        _textbuffer = self.txtRequirement.get_child().get_child().get_buffer()
        _textbuffer.set_text(self._rqmt_model.description)
        self.txtSpecification.set_text(self._rqmt_model.specification)
        self.txtFigureNumber.set_text(self._rqmt_model.figure_number)
        self.txtPageNumber.set_text(self._rqmt_model.page_number)
        self.txtValidatedDate.set_text(
            Utilities.ordinal_to_date(self._rqmt_model.validated_date))

        return False

    def _on_button_clicked(self, button, index):
        """
        Method to respond to gtk.Button() clicked signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model,
         _row) = self.tvwStakeholderInput.get_selection().get_selected()

        button.handler_block(self._lst_handler_id[index])

        if index == 14:                     # Add a stakeholder input.
            _revision_id = self._rqmt_model.revision_id
            self.dtcStakeholder.add_input(_revision_id)
            self._load_stakeholder_input_page()
        elif index == 15:                   # Delete a stakeholder input.
            _input_id = _model.get_value(_row, 0)
            self.dtcStakeholder.delete_input(_input_id)
            self._load_stakeholder_input_page()
        elif index == 16:                   # Calculate stakeholder inputs.
            _row = _model.get_iter_root()
            while _row is not None:
                _input_id = _model.get_value(_row, 0)
                (_improvement,
                 _overall_weight) = self.dtcStakeholder.calculate_stakeholder(
                     _input_id)

                _model.set_value(_row, 7, _improvement)
                _model.set_value(_row, 8, _overall_weight)
                _row = _model.iter_next(_row)
        elif index == 17:                   # Save stakeholder inputs.
            self.dtcStakeholder.save_all_inputs()

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Method to retrieve gtk.Entry() changes and assign the new data to the
        appropriate Requirement data model attribute.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the position in the Requirement class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        entry.handler_block(self._lst_handler_id[index])

        if index == 2:
            _buffer = self.txtRequirement.get_child().get_child().get_buffer()
            _text = _buffer.get_text(*_buffer.get_bounds())
            self._rqmt_model.description = _text
        elif index == 6:
            _text = self.txtSpecification.get_text()
            self._rqmt_model.specification = _text
        elif index == 7:
            _text = self.txtPageNumber.get_text()
            self._rqmt_model.page_number = _text
        elif index == 8:
            _text = self.txtFigureNumber.get_text()
            self._rqmt_model.figure_number = _text
        elif index == 12:
            _text = Utilities.date_to_ordinal(self.txtValidatedDate.get_text())
            self._rqmt_model.validated_date = _text

        self._modulebook.update(index, _text)

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to retrieve gtk.ComboBox() changes and assign the new data to
        the appropriate Requirement data model attribute.

        :param gtk.CellRendererCombo combo: the gtk.CellRendererCombo() that
                                            called this method.
        :param int index: the position in the Requirement class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _iter = combo.get_active_iter()

        if index == 4:
            _text = _model.get_value(_iter, 0)
            self._rqmt_model.requirement_type = _text
            self._create_code()
        elif index == 5:
            _text = int(_model.get_value(_iter, 0))
            self._rqmt_model.priority = _text
        elif index == 10:
            _text = _model.get_value(_iter, 0)
            self._rqmt_model.owner = _text

        combo.handler_unblock(self._lst_handler_id[index])

        self._modulebook.update(index, _text)

        return False

    def _on_toggled(self, check, index):
        """
        Method to retrieve gtk.CheckButton() changes and assign the new data to
        the appropriate Requirement data model attribute.

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the position in the Requirement class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        check.handler_block(self._lst_handler_id[index])

        if index == 9:
            self._rqmt_model.derived = int(check.get_active())
        elif index == 11:
            self._rqmt_model.validated = int(check.get_active())

        check.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_stakeholder_cell_edit(self, __cell, path, new_text, position):
        """
        Method to handle edits of the Requirement package Work Book Stakeholder
        Input gtk.Treeview()s.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Define local scalar variables.
        _return = False

        _model = self.tvwStakeholderInput.get_model()
        _row = _model.get_iter(path)
        _id = _model.get_value(_row, 0)

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(_model.get_column_type(position))
        if _type == 'gchararray':
            _model[path][position] = str(new_text)
        elif _type == 'gint':
            _model[path][position] = int(new_text)
        elif _type == 'gfloat':
            _model[path][position] = float(new_text)

        _values = (self._rqmt_model.revision_id, _id) + \
                  _model.get(_row, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                             10, 11, 12, 13, 14)

        _stakeholder = self.dtcStakeholder.dicStakeholders[_id]
        (_error_code, _error_msg) = _stakeholder.set_attributes(_values)

        if _error_code != 0:
            _content = "rtk.requirement.WorkBook._on_stakeholder_cell_edited: " \
                       "Received error {0:s} while attempting to " \
                       "edit stakeholder input {1:d}.".format(_error_msg, _id)
            self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"An error occurred while attempting to update the "
                        u"attributes of failure mode {0:d}.".format(_id))
            Widgets.rtk_error(_prompt)

            _return = True

        return _return

    def _on_analysis_cell_edit(self, cell, path, model, category):
        """
        Method to handle edits of the Requirement package Work Book Requirement
        Analysis gtk.Treeview()s.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param gtk.TreeModel model: the gtk.TreeModel() that is being edited.
        :param int category: the category of Requirement analysis questions
                             being answered.  Categories are:
                             * 0 = clarity
                             * 1 = completeness
                             * 2 = consistency
                             * 3 = verifiability
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _answer = Utilities.string_to_boolean(not cell.get_active())
        model[path][2] = _answer

        if category == 0:
            self._rqmt_model.lst_clear[model[path][0]] = _answer
        elif category == 1:
            self._rqmt_model.lst_complete[model[path][0]] = _answer
        elif category == 2:
            self._rqmt_model.lst_consistent[model[path][0]] = _answer
        elif category == 3:
            self._rqmt_model.lst_verifiable[model[path][0]] = _answer

        return False

    def _add_to_combo(self, cell, __path, new_text, index):
        """
        Method to add a new value to a gtk.CellRendererCombo() that has the
        'has-entry' property set to True.

        :param gtk.CellRendererCombo cell: the gtk.CellRendererCombo() calling
                                           this method.
        :param str __path: the path of the currently selected gtk.TreeIter().
        :param str new_text: the new text that was entered into the
                             gtk.CellRendererCombo().
        :param int index: the index of the gtk.CellRendererCombo() that called
                          the method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Define local scalar variables.
        _return = False

        # Get the gtk.CellRendererCombo() gtk.TreeModel().
        _model = cell.get_property('model')

        if index == 1:                      # Stakeholder
            if new_text not in Configuration.RTK_STAKEHOLDERS:
                Configuration.RTK_STAKEHOLDERS.append(new_text)
                _model.append([new_text])
                _query = "INSERT INTO tbl_stakeholders (fld_stakeholder) \
                          VALUES ('{0:s}')".format(new_text)
        elif index == 3:                    # Affinity group.
            if new_text not in Configuration.RTK_AFFINITY_GROUPS:
                Configuration.RTK_AFFINITY_GROUPS.append(new_text)
                _model.append([new_text])
                _query = "INSERT INTO rtk_affinity_groups (fld_group) \
                          VALUES ('{0:s}')".format(new_text)

        (_results,
         _error_code,
         __) = self._modulebook.mdcRTK.site_dao.execute(_query, commit=True)

        # Handle any errors.
        if not _results:
            if index == 1:
                _content = "rtk.requirement.WorkBook._add_to_combo: " \
                           "Received error code {0:d} while adding " \
                           "stakeholder {1:s}.".format(_error_code, new_text)
                _prompt = _(u"An error occurred while adding the new "
                            u"Stakeholder to the RTK Common database.")
            elif index == 3:
                _content = "rtk.requirement.WorkBook._add_to_combo: " \
                           "Received error code {0:d} while adding " \
                           "affinity group {1:s}.".format(_error_code,
                                                          new_text)
                _prompt = _(u"An error occurred while adding the new "
                            u"affinity group to the RTK Common database.")

            self._modulebook.mdcRTK.debug_log.error(_content)
            Widgets.rtk_error(_prompt)

            _return = True

        return _return

    def _request_save_requirements(self, __button):
        """
        Method to send a request to save all requirements to the Requirement
        data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_codes = self.dtcRequirement.save_all_requirements()
        _error_codes = [_code for _code in _error_codes if _code[1] != 0]

        if len(_error_codes) > 0:
            for __, _code in enumerate(_error_codes):
                _content = "rtk.requirement.WorkBook._request_save_requirements: " \
                           "Received error code {1:d} while saving " \
                           "requirement {0:d}.".format(_code[0], _code[1])
                self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"An error occurred while saving one or more "
                        u"requirement.")
            Widgets.rtk_error(_prompt)

            _return = True

        return _return

    def _request_add_requirement(self, __button, level):
        """
        Method to sends a request to add a new requirement to the Requirement
        data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :param int level: the level to add the new Requirement(s).
                          0 = top-level
                          1 = derived

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _revision_id = self._rqmt_model.revision_id
        if level == 0:
            _parent_id = self._rqmt_model.parent_id
        else:
            _parent_id = self._rqmt_model.requirement_id

        # Launch the Add Requirement gtk.Assistant().
        AddRequirement(self._modulebook, level, _revision_id, _parent_id)

        return False

    def _request_delete_requirement(self, __button):
        """
        Method to send a request to delete the selected requirement from the
        Requirement data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Define local scalar variables.
        _return = False
        (_results,
         _error_codes) = self.dtcRequirement.delete_requirement(
             self._rqmt_model.requirement_id)

        if sum(_error_codes) != 0:
            _content = "rtk.requirement.WorkBook._request_delete_requirement: " \
                       "Received error codes [{1:d}, {2:d}] while " \
                       "attempting to delete " \
                       "requirement {0:d}.".format(
                           self._rqmt_model.requirement_id,
                           _error_codes[0], _error_codes[1])
            self._modulebook.mdcRTK.debug_log.error(_content)

            _prompt = _(u"An error occurred while attempting to delete "
                        u"requirement {0:s}.".format(
                            self._rqmt_model.description))
            Widgets.rtk_error(_prompt)

            _return = True

        else:
            # Remove the Requirement from the requiremental Matrices.
            for _matrix_id, _matrix in self.dtcMatrices.dicMatrices.items():
                _row_ids = [_key for _key, _vals in _matrix.dicRows.items()
                            if _vals[0] == self._rqmt_model.requirement_id or
                            _vals[1] == self._rqmt_model.requirement_id]
                for _row_id in _row_ids:
                    self.dtcMatrices.delete_row(_matrix_id, _row_id)

            # Refresh Module Book view.
            self._modulebook.request_load_data()

        return _return

    def _create_code(self):
        """
        Method to create the Requirement code based on the type of requirement
        it is and it's index in the database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Get the model and iter in the Requirement Type gtk.ComboBox().
        _model = self.cmbRqmtType.get_model()
        _row = self.cmbRqmtType.get_active_iter()

        # Get the Requirement code prefix from the Requirement Type
        # gtk.ComboBox() and the suffix from the Requirement ID.
        _prefix = _model.get_value(_row, 1)
        _suffix = self._rqmt_model.requirement_id

        # Pad the suffix (Requirement ID) with zeros so the suffix is four
        # characters wide and then create the code.

        _zeds = 4 - len(str(_suffix))
        _pad = '0' * _zeds
        _code = '{0:s}-{1:s}{2:d}'.format(_prefix, _pad, _suffix)

        self._rqmt_model.requirement_code = _code

        self.txtCode.set_text(_code)

        return False
