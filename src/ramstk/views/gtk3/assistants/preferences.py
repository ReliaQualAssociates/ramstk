# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.preferences.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Configuration Preferences Module."""

# Standard Library Imports
from os.path import basename

# Third Party Imports
import defusedxml.lxml as lxml

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.models.commondb import (RAMSTKRPN, RAMSTKCondition, RAMSTKGroup,
                                    RAMSTKLoadHistory, RAMSTKMeasurement,
                                    RAMSTKUser)
from ramstk.views.gtk3 import Gdk, GObject, Gtk, Pango, _
from ramstk.views.gtk3.widgets import (
    RAMSTKBaseView, RAMSTKComboBox, RAMSTKEntry, RAMSTKFrame, RAMSTKLabel,
    RAMSTKMessageDialog, RAMSTKScrolledWindow, do_make_buttonbox,
    do_make_label_group)


class EditPreferences(Gtk.Window, RAMSTKBaseView):
    """
    Assistant to provide a GUI to set various RAMSTK config preferences.

    RAMSTK preferences are stored in the RAMSTK Site database and the user's
    Site configuration file and Program configuration file.  Configurations
    preferences are stored in Site.conf or RAMSTK.conf in each user's
    $HOME/.config/RAMSTK directory and are applicable only to that specific
    user.  Configuration preferences are edited with the Preferences assistant.
    """
    # Define private list class attributes.
    _lst_labels = [
        _("Module Book tab position:"),
        _("Work Book tab position:"),
        _("List Book tab position:"),
        _("Report size:"),
        _("Failure rate multiplier:"),
        _("Decimal places:"),
        _("Reliability estimation time:"),
        _("Path to RAMSTK configuration files:"),
        _("Path to RAMSTK data files:"),
        _("Path to RAMSTK log files:"),
        _("Select format file to edit:"),
        _("Revision Tree Background Color:"),
        _("Revision Tree Foreground Color:"),
        _("Function Tree Background Color:"),
        _("Function Tree Foreground Color:"),
        _("Requirements Tree Background Color:"),
        _("Requirements Tree Foreground Color:"),
        _("Hardware Tree Background Color:"),
        _("Hardware Tree Foreground Color:"),
        _("Validation  Tree Background Color:"),
        _("Validation Tree Foreground Color:"),
    ]

    def __init__(self, __widget: Gtk.ImageMenuItem,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager, parent: object) -> None:
        """
        Initialize an instance of the Preferences assistant.

        :param __widget: the Gtk.ImageMenuItem() that called this assistant.
        :type __widget: :class:`Gtk.ImageMenuItem`
        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param parent: the RAMSTKDesktop from which this assistant was
            launched.
        :type parent: object
        """
        GObject.GObject.__init__(self)
        RAMSTKBaseView.__init__(self,
                                configuration,
                                logger,
                                module='preferences')

        # Initialize private dictionary attributes.
        self._site_preferences = {}
        self._user_preferences = {}

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_quit, self._do_request_list_add,
            self._do_request_list_remove, self._do_request_update
        ]
        self._lst_icons = ['cancel', 'add', 'remove']
        self._lst_tooltips = [
            _("Quit the RAMSTK preferences assistant without saving."),
            _("Add an entry to the currently selected global list."),
            _("Remove the currently selected item from the global list.")
        ]

        # Initialize private scalar attributes.
        self._dtc_data_controller = None
        self._fmt_file = None
        self._notebook = Gtk.Notebook()
        self._parent = parent

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # What are the general user preferences?
        self.btnConfDir = Gtk.FileChooserButton(
            _("RAMSTK Configuration File Directory"))
        self.btnDataDir = Gtk.FileChooserButton(_("RAMSTK Data Directory"))
        self.btnIconDir = Gtk.FileChooserButton(_("RAMSTK Icon Directory"))
        self.btnLogDir = Gtk.FileChooserButton(_("RAMSTK Log Directory"))

        self.cmbModuleBookTabPosition = RAMSTKComboBox(simple=True)
        self.cmbWorkBookTabPosition = RAMSTKComboBox(simple=True)
        self.cmbListBookTabPosition = RAMSTKComboBox(simple=True)
        self.cmbReportSize = RAMSTKComboBox(simple=True)

        self.txtFRMultiplier = RAMSTKEntry()
        self.txtDecimalPlaces = RAMSTKEntry()
        self.txtMissionTime = RAMSTKEntry()

        # What are the names and, optionally, paths to the format files and the
        # layout of each one?
        self.cmbFormatFiles = RAMSTKComboBox(simple=False)
        self.tvwFormatFile = Gtk.TreeView()

        # What are the desired background and foreground colors for the
        # various RAMSTK TreeView()?
        self.btnRevisionBGColor = Gtk.ColorButton()
        self.btnRevisionFGColor = Gtk.ColorButton()
        self.btnFunctionBGColor = Gtk.ColorButton()
        self.btnFunctionFGColor = Gtk.ColorButton()
        self.btnRequirementsBGColor = Gtk.ColorButton()
        self.btnRequirementsFGColor = Gtk.ColorButton()
        self.btnHardwareBGColor = Gtk.ColorButton()
        self.btnHardwareFGColor = Gtk.ColorButton()
        self.btnSoftwareBGColor = Gtk.ColorButton()
        self.btnSoftwareFGColor = Gtk.ColorButton()
        self.btnValidationBGColor = Gtk.ColorButton()
        self.btnValidationFGColor = Gtk.ColorButton()
        self.btnIncidentBGColor = Gtk.ColorButton()
        self.btnIncidentFGColor = Gtk.ColorButton()
        self.btnTestingBGColor = Gtk.ColorButton()
        self.btnTestingFGColor = Gtk.ColorButton()

        # What RAMSTK global lists are available to edit?
        self.cmbLists = RAMSTKComboBox(simple=False)
        self.tvwListEditor = Gtk.TreeView()

        self._lst_widgets = [
            self.cmbModuleBookTabPosition,
            self.cmbWorkBookTabPosition,
            self.cmbListBookTabPosition,
            self.cmbReportSize,
            self.txtFRMultiplier,
            self.txtDecimalPlaces,
            self.txtMissionTime,
            self.btnConfDir,
            self.btnDataDir,
            self.btnLogDir,
            self.cmbFormatFiles,
            self.btnRevisionBGColor,
            self.btnRevisionFGColor,
            self.btnFunctionBGColor,
            self.btnFunctionFGColor,
            self.btnRequirementsBGColor,
            self.btnRequirementsFGColor,
            self.btnHardwareBGColor,
            self.btnHardwareFGColor,
            self.btnValidationBGColor,
            self.btnValidationFGColor,
        ]

        self.__set_properties()
        self.__make_ui()
        self.__load_comboboxes()
        self.__set_callbacks()

        #self._do_load_page()

    def __make_general_preferences_page(self) -> None:
        """
        Make the Preferences class Gtk.Notebook() general preferences page.

        :return: None
        :rtype: None
        """
        _fixed: Gtk.Fixed = Gtk.Fixed()
        _scrollwindow: RAMSTKScrolledWindow = RAMSTKScrolledWindow(_fixed)
        _frame: RAMSTKFrame = RAMSTKFrame()
        _frame.do_set_properties(title="General Preferences and Directory "
                                 "Paths")
        _frame.add(_scrollwindow)

        # Create and place the labels.  Place the associated widget.
        _y_pos = 5
        _x_pos, _lst_labels = do_make_label_group(self._lst_labels[:10])
        for _idx, _label in enumerate(_lst_labels):
            _minimum: Gtk.Requisition = self._lst_widgets[
                _idx].get_preferred_size()[0]
            if _minimum.height == 0:
                try:
                    _minimum.height = self._lst_widgets[_idx].height
                except AttributeError:
                    _minimum.height = 35

            _fixed.put(_label, 5, _y_pos)
            _fixed.put(self._lst_widgets[_idx], _x_pos + 5, _y_pos)
            _y_pos += _minimum.height + 5

        _label = RAMSTKLabel(_("General\nPreferences"))
        _label.do_set_properties(
            height=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Allows setting general user preferences for RAMSTK."))
        self._notebook.insert_page(_frame, tab_label=_label, position=-1)

    def __make_global_lists_page(self) -> None:
        """
        Make the page used to edit global RAMSTK lists.

        :return: None
        :rtype: None
        """
        _hbox = Gtk.HBox()
        _vbox = Gtk.VBox()
        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Edit RAMSTK Lists"))
        _frame.add(_vbox)
        _fixed = Gtk.Fixed()
        _scrollwindow = Gtk.ScrolledWindow()

        _hbox.pack_end(_frame, True, True, 0)
        _vbox.pack_start(_fixed, False, True, 0)
        _vbox.pack_end(_scrollwindow, True, True, 0)

        _label = RAMSTKLabel(_("Select RAMSTK list to load:"))
        _fixed.put(_label, 5, 5)
        _fixed.put(self.cmbLists, 225, 5)
        _scrollwindow.add(self.tvwListEditor)

        _model = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_STRING,
                               GObject.TYPE_STRING, GObject.TYPE_STRING,
                               GObject.TYPE_STRING)
        for _idx in [0, 1, 2, 3]:
            _cell = Gtk.CellRendererText()
            _cell.set_property('cell-background', '#FFFFFF')
            _cell.set_property('editable', True)
            _cell.set_property('foreground', '#000000')
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', Pango.WrapMode.WORD)
            _cell.set_property('yalign', 0.1)
            _cell.connect('edited', self._do_edit_cell, _idx, _model)
            _column = Gtk.TreeViewColumn("")
            _column.set_alignment(0.5)
            _column.set_visible(True)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_idx)
            self.tvwListEditor.append_column(_column)
        self.tvwListEditor.set_model(_model)

        _lists = [[
            _("Damaging Operating Conditions"), 'damaging_conditions', ''
        ], [_("Means for Classifying Load Histories"), 'load_history', ''],
                  [_("Measureable Parameters"), 'measureable_parameters', ''],
                  [_("RPN Detection"), 'rpn_detection', ''],
                  [_("RPN Occurrence"), 'rpn_occurrence', ''],
                  [_("RPN Severity"), 'rpn_severity', ''],
                  [_("RAMSTK Work Groups"), 'workgroups', ''],
                  [_("RAMSTK Users"), 'users', '']]
        self.cmbLists.do_load_combo(_lists, simple=False)

        _label = RAMSTKLabel(_("Global RAMSTK Lists"))
        _label.do_set_properties(
            justify=Gtk.Justification.CENTER,
            tooltip=_("Edit global RAMSTK lists; lists available to all "
                      "RAMSTK Programs."))
        self.notebook.insert_page(_hbox, tab_label=_label, position=-1)

    def __make_look_and_feel_page(self) -> None:
        """
        Make the Preferences class Gtk.Notebook() look and feel page.

        :return: None
        :rtype: None
        """
        _hpaned = Gtk.HPaned()

        _fixed: Gtk.Fixed = Gtk.Fixed()
        _scrollwindow: RAMSTKScrolledWindow = RAMSTKScrolledWindow(_fixed)
        _frame: RAMSTKFrame = RAMSTKFrame()
        _frame.do_set_properties(title="Module View Background &amp; "
                                 "Foreground Colors")
        _frame.add(_scrollwindow)
        _hpaned.pack1(_frame, True, True)

        # Create and place the labels.  Place the associated widget.
        _y_pos = 5
        _x_pos, _lst_labels = do_make_label_group(self._lst_labels[10:])
        for _idx, _label in enumerate(_lst_labels):
            _minimum: Gtk.Requisition = self._lst_widgets[
                _idx + 10].get_preferred_size()[0]
            if _minimum.height == 0:
                try:
                    _minimum.height = self._lst_widgets[_idx + 10].height
                except AttributeError:
                    _minimum.height = 35

            _fixed.put(_label, 5, _y_pos)
            _fixed.put(self._lst_widgets[_idx + 10], _x_pos + 5, _y_pos)
            _y_pos += _minimum.height + 5

        _labels = [
            _("Default\nTitle"),
            _("User\nTitle"),
            _("Column\nPosition"),
            _("Can\nEdit?"),
            _("Is\nVisible?")
        ]

        self.tvwFormatFile = Gtk.TreeView()
        _model = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING,
                               GObject.TYPE_INT, GObject.TYPE_INT,
                               GObject.TYPE_INT, GObject.TYPE_STRING,
                               GObject.TYPE_STRING, GObject.TYPE_STRING)
        self.tvwFormatFile.set_model(_model)

        for _idx, _text in enumerate([
                _("Default\nTitle"),
                _("User\nTitle"),
                _("Column\nPosition"),
                _("Can\nEdit?"),
                _("Is\nVisible?")
        ]):
            if _idx == 0:
                _cell = Gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('foreground', '#000000')
                _cell.set_property('weight', 700)
                _cell.set_property('weight-set', True)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', Pango.WrapMode.WORD)
            elif _idx in [1, 2]:
                _cell = Gtk.CellRendererText()
                _cell.set_property('background', '#FFFFFF')
                _cell.set_property('editable', 1)
                _cell.set_property('foreground', '#000000')
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', Pango.WrapMode.WORD)
                _cell.connect('edited', self._do_edit_cell, _idx, _model)
            elif _idx > 4:
                _cell = Gtk.CellRendererText()
                _cell.set_property('editable', 0)
            else:
                _cell = Gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._do_toggle_cell, _idx, _model)

            _label = RAMSTKLabel(_text)
            _label.do_set_properties(bold=True,
                                     justify=Gtk.Justification.CENTER)

            _column = Gtk.TreeViewColumn()
            _column.set_widget(_label)
            _column.set_alignment(0.5)
            _column.pack_start(_cell, True)
            if _idx < 3:
                _column.set_attributes(_cell, text=_idx)
            elif _idx > 4:
                _column.set_visible(False)
            else:
                _column.set_attributes(_cell, active=_idx)

            self.tvwFormatFile.append_column(_column)

        _scrollwindow: RAMSTKScrolledWindow = RAMSTKScrolledWindow(
            self.tvwFormatFile)
        _frame: RAMSTKFrame = RAMSTKFrame()
        _frame.do_set_properties(title="Module View Column Layout")
        _frame.add(_scrollwindow)
        _hpaned.pack2(_frame, True, True)

        _label = RAMSTKLabel(_("Look &amp; Feel"))
        _label.do_set_properties(
            justify=Gtk.Justification.CENTER,
            tooltip=_("Allows setting user interface preferences for RAMSTK."))
        self._notebook.insert_page(_hpaned, tab_label=_label, position=-1)

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        _vbox = Gtk.VBox()
        _vbox.pack_start(self._notebook, True, True, 0)
        self.add(_vbox)

        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(
            do_make_buttonbox(self,
                              callbacks=[self._lst_callbacks[0]],
                              icons=[self._lst_icons[0]],
                              orientation='horizontal',
                              tooltips=[self._lst_tooltips[0]]))
        _vbox.pack_end(_scrolledwindow, False, False, 0)

        _n_screens = Gdk.Screen.get_default().get_n_monitors()
        _width = Gdk.Screen.width() / _n_screens
        _height = Gdk.Screen.height()

        self.set_border_width(5)
        self.set_default_size(_width - 450, (4 * _height / 7))
        self.set_modal(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(True)
        self.set_transient_for(self._parent)

        self.__make_general_preferences_page()
        self.__make_look_and_feel_page()
        #self.__make_global_lists_page()

        self.show_all()

    def __load_comboboxes(self) -> None:
        """
        Load the RAMSTKComboBoxes() with their data.

        :return: None
        :rtype: None
        """
        self.cmbModuleBookTabPosition.do_load_combo([["Bottom"], ["Left"],
                                                     ["Right"], ["Top"]])
        self.cmbWorkBookTabPosition.do_load_combo([["Bottom"], ["Left"],
                                                   ["Right"], ["Top"]])
        self.cmbListBookTabPosition.do_load_combo([["Bottom"], ["Left"],
                                                   ["Right"], ["Top"]])
        self.cmbReportSize.do_load_combo([["A4"], ["Letter"]])

        _formats = [[_("Allocation"), 'allocation', ''],
                    [_("(D)FME(C)A"), 'dfmeca', ''],
                    [_("Functional FMEA"), 'ffmea', ''],
                    [_("Function"), 'function', ''],
                    [_("Hardware"), 'hardware', ''],
                    [_("Hazards"), 'hazard', ''],
                    [_("Physics of Failure Analysis"), 'pof', ''],
                    [_("Requirement"), 'requirement', ''],
                    [_("Revision"), 'revision', ''],
                    [_("Similar Item Analysis"), 'similaritem', ''],
                    [_("Stakeholder Input"), 'stakeholder', ''],
                    [_("Validation"), 'validation', '']]
        self.cmbFormatFiles.do_load_combo(_formats, 0, False)

    def __set_callbacks(self) -> None:
        """
        Set the callback functions/methods for each of the widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnConfDir.connect('file-set', self._do_select_path, 0)
        self.btnDataDir.connect('file-set', self._do_select_path, 1)
        self.btnIconDir.connect('file-set', self._do_select_path, 2)
        self.btnLogDir.connect('file-set', self._do_select_path, 3)

        self.btnRevisionBGColor.connect('color-set', self._do_set_color,
                                        'revisionbg')
        self.btnRevisionFGColor.connect('color-set', self._do_set_color,
                                        'revisionfg')
        self.btnFunctionBGColor.connect('color-set', self._do_set_color,
                                        'functionbg')
        self.btnFunctionFGColor.connect('color-set', self._do_set_color,
                                        'functionfg')
        self.btnRequirementsBGColor.connect('color-set', self._do_set_color,
                                            'requirementbg')
        self.btnRequirementsFGColor.connect('color-set', self._do_set_color,
                                            'requirementfg')
        self.btnHardwareBGColor.connect('color-set', self._do_set_color,
                                        'hardwarebg')
        self.btnHardwareFGColor.connect('color-set', self._do_set_color,
                                        'hardwarefg')
        self.btnSoftwareBGColor.connect('color-set', self._do_set_color,
                                        'softwarebg')
        self.btnSoftwareFGColor.connect('color-set', self._do_set_color,
                                        'softwarefg')
        self.btnValidationBGColor.connect('color-set', self._do_set_color,
                                          'validationbg')
        self.btnValidationFGColor.connect('color-set', self._do_set_color,
                                          'validationfg')
        self.btnIncidentBGColor.connect('color-set', self._do_set_color,
                                        'incidentbg')
        self.btnIncidentFGColor.connect('color-set', self._do_set_color,
                                        'incidentfg')
        self.btnTestingBGColor.connect('color-set', self._do_set_color,
                                       'testingbg')
        self.btnTestingFGColor.connect('color-set', self._do_set_color,
                                       'testingfg')

        # ----- COMBOBOXES
        self.cmbFormatFiles.dic_handler_id[
            'changed'] = self.cmbFormatFiles.connect('changed',
                                                     self._on_combo_changed, 0)
        self.cmbLists.dic_handler_id['changed'] = self.cmbLists.connect(
            'changed', self._on_combo_changed, 1)
        self.cmbModuleBookTabPosition.dic_handler_id[
            'changed'] = self.cmbModuleBookTabPosition.connect(
                'changed', self._on_combo_changed, 2)
        self.cmbWorkBookTabPosition.dic_handler_id[
            'changed'] = self.cmbWorkBookTabPosition.connect(
                'changed', self._on_combo_changed, 3)
        self.cmbListBookTabPosition.dic_handler_id[
            'changed'] = self.cmbListBookTabPosition.connect(
                'changed', self._on_combo_changed, 4)
        self.cmbReportSize.dic_handler_id[
            'changed'] = self.cmbReportSize.connect('changed',
                                                    self._on_combo_changed, 5)

    def __set_properties(self) -> None:
        """
        Set the properties of the Preferences assistance widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnConfDir.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.btnDataDir.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.btnIconDir.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.btnLogDir.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        # ----- COMBOBOXES
        self.cmbFormatFiles.do_set_properties(
            tooltip=_("Select the Module View layout to edit."))
        self.cmbLists.do_set_properties(
            tooltip=_("Select global RAMSTK list to edit."))

        # ----- ENTRIES
        self.txtFRMultiplier.do_set_properties(width=75)
        self.txtDecimalPlaces.do_set_properties(width=75)

    @staticmethod
    def _do_edit_cell(__cell, path, new_text, position, model) -> None:
        """
        Handle Gtk.CellRenderer() edits.

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: Gtk.CellRenderer
        :param path: the Gtk.TreeView() path of the Gtk.CellRenderer() that was
                     edited.
        :type path: string
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :type new_text: string
        :param position: the column position of the edited Gtk.CellRenderer().
        :type position: integer
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :type model: Gtk.TreeModel
        """
        _type = GObject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

    def _do_load_format(self, combo) -> None:
        """
        Load the selected Module View format file for editing.

        :return: None
        :rtype: None
        """
        _model = combo.get_model()
        _row = combo.get_active_iter()
        _module = _model.get_value(_row, 1)

        self._fmt_file = (
            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/'
            + self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE[_module])
        if _module == 'dfmeca':
            _fmt_path = "/root/tree[@name='DFMECA']/column"
        elif _module == 'ffmea':
            _fmt_path = "/root/tree[@name='FFMEA']/column"
        elif _module == 'hazard':
            _fmt_path = "/root/tree[@name='Hazard']/column"
        elif _module == 'pof':
            _fmt_path = "/root/tree[@name='PoF']/column"
        elif _module == 'similaritem':
            _fmt_path = "/root/tree[@name='SimilarItem']/column"
        else:
            _fmt_path = "/root/tree[@name='" + _module.title() + "']/column"

        # Retrieve the default heading text from the format file.
        _path = _fmt_path + '/defaulttitle'
        _default = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve the default heading text from the format file.
        _path = _fmt_path + '/usertitle'
        _user = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve the column position from the format file.
        _path = _fmt_path + '/position'
        _position = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve whether or not the column is editable from the format file.
        _path = _fmt_path + '/editable'
        _editable = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve whether or not the column is visible from the format file.
        _path = _fmt_path + '/visible'
        _visible = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve datatypes from the format file.
        _path = _fmt_path + '/datatype'
        _datatype = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve widget types from the format file.
        _path = _fmt_path + '/widget'
        _widget = lxml.parse(self._fmt_file).xpath(_path)

        # Retrieve attribute keys from the format file.
        _path = _fmt_path + '/key'
        _keys = lxml.parse(self._fmt_file).xpath(_path)

        _model = self.tvwFormatFile.get_model()
        _model.clear()
        for _index, __ in enumerate(_default):
            try:
                _key = _keys[_index].text
            except IndexError:
                _key = ''
            _data = [
                _default[_index].text, _user[_index].text,
                int(_position[_index].text),
                int(_editable[_index].text),
                int(_visible[_index].text), _datatype[_index].text,
                _widget[_index].text, _key
            ]
            _model.append(_data)

    def _do_load_list(self, combo) -> None:
        """
        Load the selected global RAMSTK list for editing.

        :return: None
        :rtype: None
        """
        _dic_headers = {
            'damaging_conditions':
            ['', _("Condition Description"), '', '', ''],
            'load_history': ['', _("History Description"), '', '', ''],
            'measureable_parameters':
            ['', _("Parameter Code"),
             _("Parameter Description"), '', ''],
            'rpn_detection': ['',
                              _("Name"),
                              _("Description"),
                              _("Value"), ''],
            'rpn_occurrence':
            ['', _("Name"), _("Description"),
             _("Value"), ''],
            'rpn_severity': ['',
                             _("Name"),
                             _("Description"),
                             _("Value"), ''],
            'workgroups': ['', _("Description"), '', '', ''],
            'users': [
                '',
                _("First Name"),
                _("Last Name"),
                _("User E-Mail"),
                _("User Phone")
            ]
        }
        # Retrieve the name of the list to display; this name is the key for
        # the dict above.
        _model = combo.get_model()
        _row = combo.get_active_iter()
        _list = _model.get_value(_row, 1)
        try:
            _headers = _dic_headers[_list]
        except KeyError:
            _headers = ['', '', '', '', '']

        # Clear out any existing models and columns.
        i = 0
        for _column in self.tvwListEditor.get_columns():
            _label = RAMSTKLabel(_headers[i])
            _label.do_set_properties(justify=Gtk.Justification.CENTER)
            _column.set_widget(_label)
            if _headers[i] == '':
                _column.set_visible(False)
            else:
                _column.set_visible(True)
            i += 1
        _model = self.tvwListEditor.get_model()
        _model.clear()

        i = 0
        _entities = self._site_preferences[_list]
        for _entity in _entities:
            if _list == 'users':
                _data = [
                    i,
                    _entity.get_attributes()['user_fname'],
                    _entity.get_attributes()['user_lname'],
                    _entity.get_attributes()['user_email'],
                    _entity.get_attributes()['user_phone']
                ]
            elif _list in ['rpn_detection', 'rpn_occurrence', 'rpn_severity']:
                _data = [
                    i,
                    _entity.get_attributes()[1],
                    _entity.get_attributes()[2],
                    _entity.get_attributes()[4], ''
                ]
            else:
                _data = [
                    i, _entity.get_attributes()['description'], '', '', ''
                ]
            _model.append(_data)
            i += 1

    def _do_load_page(self, **kwargs) -> None:  # pylint: disable=unused-argument
        """
        Load the current preference values.

        :return: (_error_code, _user_msg, _debug_msg); the error code, message
                 to be displayed to the user, and the message to be written to
                 the debug log.
        :rtype: (int, str, str)
        """
        _positions = {"bottom": 1, "left": 2, "right": 3, "top": 4}
        _papersize = {'a4': 1, 'letter': 2}

        self._site_preferences = self._dtc_data_controller.request_get_preferences(
            site=True, user=False)
        self._user_preferences = self._dtc_data_controller.request_get_preferences(
            site=False, user=True)

        # if self._mdcRAMSTK.loaded:
        # self.chkFunctions.set_active(_results[0][1])
        # self.chkRequirements.set_active(_results[0][2])
        # self.chkSoftware.set_active(_results[0][4])
        # self.chkValidation.set_active(_results[0][5])
        # self.chkRG.set_active(_results[0][6])
        # self.chkIncidents.set_active(_results[0][8])
        # self.chkSurvivalAnalysis.set_active(_results[0][10])

        self.cmbModuleBookTabPosition.set_active(
            _positions[self._user_preferences['tabpos']['modulebook'].lower()])
        self.cmbWorkBookTabPosition.set_active(
            _positions[self._user_preferences['tabpos']['workbook'].lower()])
        self.cmbListBookTabPosition.set_active(
            _positions[self._user_preferences['tabpos']['listbook'].lower()])
        self.cmbReportSize.set_active(
            _papersize[self._user_preferences['report_size'].lower()])

        self.txtFRMultiplier.set_text(self._user_preferences['hr_multiplier'])
        self.txtDecimalPlaces.set_text(self._user_preferences['decimal'])
        self.txtMissionTime.set_text(self._user_preferences['calcreltime'])

        self.btnConfDir.set_current_folder(self._user_preferences['sitedir'])
        self.btnDataDir.set_current_folder(self._user_preferences['datadir'])
        self.btnIconDir.set_current_folder(self._user_preferences['icondir'])
        self.btnLogDir.set_current_folder(self._user_preferences['logdir'])
        self.btnProgramDir.set_current_folder(
            self._user_preferences['progdir'])

        _color = Gdk.color_parse(
            self._user_preferences['colors']['revisionbg'])
        self.btnRevisionBGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['revisionfg'])
        self.btnRevisionFGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['functionbg'])
        self.btnFunctionBGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['functionfg'])
        self.btnFunctionFGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['requirementbg'])
        self.btnRequirementsBGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['requirementfg'])
        self.btnRequirementsFGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['hardwarebg'])
        self.btnHardwareBGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['hardwarefg'])
        self.btnHardwareFGColor.set_color(_color)
        # self.btnSoftwareBGColor.set_color(_color)
        # self.btnSoftwareFGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['validationbg'])
        self.btnValidationBGColor.set_color(_color)
        _color = Gdk.color_parse(
            self._user_preferences['colors']['validationfg'])
        self.btnValidationFGColor.set_color(_color)
        # self.btnIncidentBGColor.set_color(_color)
        # self.btnIncidentFGColor.set_color(_color)
        # self.btnTestingBGColor.set_color(_color)
        # self.btnTestingFGColor.set_color(_color)

    def _do_quit(self, __button: Gtk.Button) -> None:
        """
        Quit the preferences Gtk.Assistant().

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        self.destroy()

    def _do_request_list_add(self, __button: Gtk.Button) -> None:
        """
        Add a new item to the global list.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton()`
        :return: None
        :rtype: None
        """
        _model = self.cmbLists.get_model()
        _row = self.cmbLists.get_active_iter()
        _list = _model.get_value(_row, 1)

        _id = len(self._site_preferences[_list])
        _data = [_id, '', '', '', '']

        _model = self.tvwListEditor.get_model()
        _model.append(_data)

        if _list == 'damaging_conditions':
            _entity = RAMSTKCondition()
            _entity.description = 'New Damaging Operating Condition'
            _entity.cond_type = 'operating'
        elif _list == 'load_history':
            _entity = RAMSTKLoadHistory()
            _entity.description = 'New Load History'
        elif _list == 'measureable_parameters':
            _entity = RAMSTKMeasurement()
            _entity.code = 'NMP'
            _entity.description = 'New Measureable Parameter'
            _entity.measurement_type = 'damage'
        elif _list == 'rpn_detection':
            _entity = RAMSTKRPN()
            _entity.name = 'New RPN Name'
            _entity.description = 'New RPN Description'
            _entity.rpn_type = 'detection'
        elif _list == 'rpn_occurrence':
            _entity = RAMSTKRPN()
            _entity.name = 'New RPN Name'
            _entity.description = 'New RPN Description'
            _entity.rpn_type = 'occurrence'
        elif _list == 'rpn_severity':
            _entity = RAMSTKRPN()
            _entity.name = 'New RPN Name'
            _entity.description = 'New RPN Description'
            _entity.rpn_type = 'severity'
        elif _list == 'workgroups':
            _entity = RAMSTKGroup()
            _entity.description = 'New RAMSTK Workgroup'
            _entity.group_type = 'workgroup'
        elif _list == 'users':
            _entity = RAMSTKUser()
            _entity.user_lname = 'New RAMSTK User Last Name'
            _entity.user_fname = 'New RAMSTK User First Name'
            _entity.user_email = 'new@user'
            _entity.user_phane = '867.5309'

        self._site_preferences[_list].append(_entity)

    def _do_request_list_remove(self, __button: Gtk.Button) -> None:
        """
        Remove the seleced item from the global list.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton()`
        :return: None
        :rtype: None
        """
        _model = self.cmbLists.get_model()
        _row = self.cmbLists.get_active_iter()
        _list = _model.get_value(_row, 1)

        (_model, _row) = self.tvwListEditor.get_selection().get_selected()
        _id = _model.get_value(_row, 0)

        _record = self._site_preferences[_list].pop(_id)
        if self._dtc_data_controller.request_do_delete(_record):
            _prompt = _("There was an error removing an item from the {0:s} "
                        "RAMSTK global list.").format(_list)
            _dialog = RAMSTKMessageDialog(parent=self)
            _dialog.do_set_message(_prompt)
            _dialog.do_set_message_type('error')

            if _dialog.run() == Gtk.ResponseType.OK:
                _dialog.destroy()
        else:
            self._do_load_list(self.cmbLists)

    def _do_request_update(self, button: Gtk.Button) -> None:
        """
        Request to update the user and program preferences.

        :param button: the Gtk.Button() that called this method.
        :type button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        from shutil import copyfile

        # Make a backup of the original configuration files.
        _conf_file = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/Site.conf'
        copyfile(_conf_file, _conf_file + '_bak')
        _conf_file = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + '/RAMSTK.conf'
        copyfile(_conf_file, _conf_file + '_bak')

        if button.get_property('name') == 'format':
            copyfile(self._fmt_file, self._fmt_file + '_bak')
            self._do_save_tree_layout()
        elif button.get_property('name') == 'globallists':
            self._dtc_data_controller.request_set_preferences(
                self._site_preferences, site=True, user=False)
        else:
            self._dtc_data_controller.request_set_preferences(
                self._user_preferences, site=False, user=True)

        if self._dtc_data_controller.request_do_update():
            _prompt = _("There was an error saving user and program "
                        "preferences.")
            _dialog = RAMSTKMessageDialog(parent=self)
            _dialog.do_set_message(_prompt)
            _dialog.do_set_message_type('error')

            if _dialog.run() == Gtk.ResponseType.OK:
                _dialog.destroy()

    def _do_request_update_all(self) -> None:
        """
        Wrapper method for _do_request_update().

        :return: None
        :rtype: None
        """
        self._do_request_update(None)

    def _do_save_tree_layout(self) -> None:
        """
        Save the Module View RAMSTKTreeView() layout file.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Get the format file for the Gtk.TreeView to be edited.  Strip the
        # last four (.xml) characters to variable _name.
        _basename = basename(self._fmt_file)
        _name = _basename[:-4]

        # Open the format file for writing.
        _file = open(self._fmt_file, 'w')

        # Create the new format file.
        _file.write("<!--\n")
        _file.write("-*- coding: utf-8 -*-\n\n")
        _file.write(
            "{0:s} is part of the RAMSTK Project\n\n".format(_basename))
        _file.write('Copyright 2011-2018 Doyle "weibullguy" Rowland '
                    '<doyle DOT rowland AT reliaqual DOT com>\n\n')
        _file.write("All rights reserved.-->\n\n")
        _file.write("<!-- This file contains information used by the RAMSTK "
                    "application to draw\n")
        _file.write("various widgets.  These values can be changed by the "
                    "user to personalize\n")
        _file.write("their experience. -->\n\n")

        _file.write("<root>\n")
        _file.write('<tree name="{0:s}">\n'.format(_name))

        _model = self.tvwFormatFile.get_model()
        _row = _model.get_iter_first()
        while _row is not None:
            _file.write("<column>\n")
            _file.write("<defaulttitle>{0:s}</defaulttitle>\n".format(
                _model.get_value(_row, 0)))
            _file.write("<usertitle>{0:s}</usertitle>\n".format(
                _model.get_value(_row, 1)))
            _file.write("<datatype>{0:s}</datatype>\n".format(
                _model.get_value(_row, 5)))
            _file.write("<position>{0:d}</position>\n".format(
                _model.get_value(_row, 2)))
            _file.write("<widget>{0:s}</widget>\n".format(
                _model.get_value(_row, 6)))
            _file.write("<editable>{0:d}</editable>\n".format(
                _model.get_value(_row, 3)))
            _file.write("<visible>{0:d}</visible>\n".format(
                _model.get_value(_row, 4)))
            _file.write("<key>{0:s}</key>\n".format(_model.get_value(_row, 7)))
            _file.write("</column>\n")

            _row = _model.iter_next(_row)

        _file.write("</tree>\n")
        _file.write("</root>")
        _file.close()

    def _do_select_path(self, button, index) -> None:
        """
        Select the path from the file chooser.

        :param button: the Gtk.FileChooserButton() that called this method.
        :type button: :class:`Gtk.FileChooserButton`
        :param int index: the index of the Gtk.FileChooserButton() that called
                          this method.
        :return: None
        :rtyp: None
        """
        if index == 0:
            self._preferences['sitedir'] = button.get_current_folder()
        elif index == 1:
            self._preferences['datadir'] = button.get_current_folder()
        elif index == 2:
            self._preferences['icondir'] = button.get_current_folder()
        elif index == 3:
            self._preferences['logdir'] = button.get_current_folder()
        elif index == 4:
            self._preferences['progdir'] = button.get_current_folder()

    def _do_set_color(self, colorbutton, ramstk_colors) -> None:
        """
        Set the selected color.

        :param Gtk.ColorButton colorbutton: the Gtk.ColorButton() that called
                                            this method.
        :param int ramstk_colors: the position in the RAMSTK_COLORS global variable.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Retrieve the six digit hexidecimal version of the selected color.
        _color = colorbutton.get_color()
        try:
            _red = "{0:#0{1}}".format('%X' % int(_color.red / 255), 2)
        except ValueError:
            _red = '%X' % int(_color.red / 255)
        try:
            _green = "{0:#0{1}}".format('%X' % int(_color.green / 255), 2)
        except ValueError:
            _green = '%X' % int(_color.green / 255)
        try:
            _blue = "{0:#0{1}}".format('%X' % int(_color.blue / 255), 2)
        except ValueError:
            _blue = '%X' % int(_color.blue / 255)
        _color = '#%s%s%s' % (_red, _green, _blue)

        # Set the color variable.
        self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_COLORS[
            ramstk_colors] = _color

    @staticmethod
    def _do_toggle_cell(cell, path, position, model) -> None:
        """
        Handle Gtk.CellRendererToggle() edits.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the Gtk.TreeView() path of the Gtk.CellRenderer() that
                     was edited.
        :param position: the column position of the edited Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        model[path][position] = not cell.get_active()

    def _on_combo_changed(self, combo, index) -> None:
        """
        Edit RAMSTKTreeView() layouts.

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`gui.gtk.RAMSTKCombo`
        :param int index: the index in the signal handler list associated with
                          the RAMSTKCombo() calling this method.
        :return: None
        :rtype: None
        """
        combo.handler_block(self._lst_handler_id[index])

        if index == 0:
            self._do_load_format(combo)
        elif index == 1:
            self._do_load_list(combo)
        elif index == 2:
            self._user_preferences['tabpos'][
                'modulebook'] = combo.get_active_text()
        elif index == 3:
            self._user_preferences['tabpos'][
                'workbook'] = combo.get_active_text()
        elif index == 4:
            self._user_preferences['tabpos'][
                'listbook'] = combo.get_active_text()
        elif index == 5:
            self._user_preferences['report_size'] = combo.get_active_text()

        combo.handler_unblock(self._lst_handler_id[index])
