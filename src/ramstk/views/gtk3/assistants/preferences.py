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
from shutil import copyfile

# Third Party Imports
# noinspection PyPackageRequirements
import toml

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.utilities import string_to_boolean
from ramstk.views.gtk3 import Gdk, GObject, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKBaseView, RAMSTKComboBox, RAMSTKEntry, RAMSTKFrame, RAMSTKLabel,
    RAMSTKScrolledWindow, do_make_buttonbox, do_make_column,
    do_make_label_group, do_make_text_cell, do_make_toggle_cell,
    do_set_cell_properties)


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
        _("Validation Tree Foreground Color:")
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
        self._lst_callbacks = [self._do_quit, self._do_request_update]
        self._lst_icons = ['cancel']
        self._lst_tooltips = [
            _("Quit the RAMSTK preferences assistant without saving.")
        ]

        # Initialize private scalar attributes.
        self._fmt_file: str = ''
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

        self._lst_widgets = [
            self.cmbModuleBookTabPosition, self.cmbWorkBookTabPosition,
            self.cmbListBookTabPosition, self.cmbReportSize,
            self.txtFRMultiplier, self.txtDecimalPlaces, self.txtMissionTime,
            self.btnConfDir, self.btnDataDir, self.btnLogDir,
            self.cmbFormatFiles, self.btnRevisionBGColor,
            self.btnRevisionFGColor, self.btnFunctionBGColor,
            self.btnFunctionFGColor, self.btnRequirementsBGColor,
            self.btnRequirementsFGColor, self.btnHardwareBGColor,
            self.btnHardwareFGColor, self.btnValidationBGColor,
            self.btnValidationFGColor
        ]

        self.__set_properties()
        self.__make_ui()
        self.__load_comboboxes()
        self.__set_callbacks()

        self._do_load_page()

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
        self.cmbFormatFiles.do_load_combo(
            [[_("Allocation"), 'allocation', ''], [
                _("(D)FME(C)A"), 'fmea', ''
            ], [_("Failure Definition"), 'failure_definition', ''],
             [_("Function"), 'function', ''], [_("Hardware"), 'hardware', ''],
             [_("Hazards Analysis"), 'hazard', ''],
             [_("Physics of Failure Analysis"), 'pof', ''],
             [_("Requirement"), 'requirement', ''],
             [_("Revision"), 'revision', ''],
             [_("Similar Item Analysis"), 'similar_item', ''],
             [_("Stakeholder Input"), 'stakeholder', ''],
             [_("Validation"), 'validation', '']],
            simple=False)

    def __make_format_treeview(self) -> None:
        """
        Make the format file editing Gtk.Treeview().

        :return: None
        :rtype: None
        """
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
                _cell = do_make_text_cell(False)
                do_set_cell_properties(_cell,
                                       bg_color='light gray',
                                       editable=False,
                                       fg_color='#000000',
                                       weight=700,
                                       weight_set=True)
                _column = do_make_column([_cell], heading=_text)
                _column.set_attributes(_cell, text=_idx)
            elif _idx in [1, 2]:
                _cell = do_make_text_cell(False)
                do_set_cell_properties(_cell,
                                       bg_color='#FFFFFF',
                                       editable=True,
                                       fg_color='#000000')
                _cell.connect('edited', self._do_edit_cell, _idx, _model)
                _column = do_make_column([_cell], heading=_text)
                _column.set_attributes(_cell, text=_idx)
            elif _idx > 4:
                _cell = do_make_text_cell(False)
                do_set_cell_properties(_cell,
                                       bg_color='light gray',
                                       editable=False,
                                       fg_color='#000000')
                _column = do_make_column([_cell], heading=_text, visible=False)
            else:
                _cell = do_make_toggle_cell()
                do_set_cell_properties(_cell, editable=True)
                _cell.connect('toggled', self._do_toggle_cell, _idx, _model)
                _column = do_make_column([_cell], heading=_text)
                _column.set_attributes(_cell, active=_idx)

            self.tvwFormatFile.append_column(_column)

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

        self.__make_format_treeview()

        _scrollwindow: RAMSTKScrolledWindow = RAMSTKScrolledWindow(
            self.tvwFormatFile)
        _frame: RAMSTKFrame = RAMSTKFrame()
        _frame.do_set_properties(title="Module View Column Layout")
        _frame.add(_scrollwindow)
        _hpaned.pack2(_frame, True, True)

        _label: RAMSTKLabel = RAMSTKLabel(_("Look &amp; Feel"))
        _label.do_set_properties(
            height=30,
            width=-1,
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

        self.show_all()

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
        self.cmbModuleBookTabPosition.dic_handler_id[
            'changed'] = self.cmbModuleBookTabPosition.connect(
                'changed', self._on_combo_changed, 1)
        self.cmbWorkBookTabPosition.dic_handler_id[
            'changed'] = self.cmbWorkBookTabPosition.connect(
                'changed', self._on_combo_changed, 2)
        self.cmbListBookTabPosition.dic_handler_id[
            'changed'] = self.cmbListBookTabPosition.connect(
                'changed', self._on_combo_changed, 3)
        self.cmbReportSize.dic_handler_id[
            'changed'] = self.cmbReportSize.connect('changed',
                                                    self._on_combo_changed, 4)

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

        # ----- ENTRIES
        self.txtFRMultiplier.do_set_properties(width=75)
        self.txtDecimalPlaces.do_set_properties(width=75)

    @staticmethod
    def _do_edit_cell(__cell, path, new_text, position, model) -> None:
        """
        Handle Gtk.CellRenderer() edits.

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :type model: :class:`Gtk.TreeModel`
        """
        _type = GObject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

    def _do_load_format(self, module: str) -> None:
        """
        Load the selected Module View format file for editing.

        :param str module: the name of the RAMSTK workstream module whose
            Module View layout is to be edited.
        :return: None
        :rtype: None
        """
        self._fmt_file = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + '/layouts/'
            + self.RAMSTK_USER_CONFIGURATION.RAMSTK_FORMAT_FILE[module])

        _format = toml.load(self._fmt_file)

        _datatypes = _format['datatype']
        _default = _format['defaulttitle']
        _editable = _format['editable']
        _user = _format['usertitle']
        _keys = _format['key']
        _position = _format['position']
        _visible = _format['visible']
        _widgets = _format['widget']

        _model = self.tvwFormatFile.get_model()
        _model.clear()
        # pylint: disable=unused-variable
        for _key in _default:
            _data = [
                _default[_key], _user[_key],
                int(_position[_key]), string_to_boolean(_editable[_key]),
                string_to_boolean(_visible[_key]),
                _datatypes[_key], _widgets[_key], _key
            ]
            _model.append(_data)

    def _do_load_page(self) -> None:
        """
        Load the current preference values.

        :return: (_error_code, _user_msg, _debug_msg); the error code, message
                 to be displayed to the user, and the message to be written to
                 the debug log.
        :rtype: (int, str, str)
        """
        _positions = {"bottom": 1, "left": 2, "right": 3, "top": 4}
        _papersize = {'a4': 1, 'letter': 2}

        self.cmbModuleBookTabPosition.set_active(
            _positions[self.RAMSTK_USER_CONFIGURATION.
                       RAMSTK_TABPOS['modulebook'].lower()])
        self.cmbWorkBookTabPosition.set_active(_positions[
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_TABPOS['workbook'].lower()])
        self.cmbListBookTabPosition.set_active(_positions[
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_TABPOS['listbook'].lower()])
        self.cmbReportSize.set_active(_papersize[
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_REPORT_SIZE.lower()])

        self.txtFRMultiplier.set_text(
            str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_HR_MULTIPLIER))
        self.txtDecimalPlaces.set_text(
            str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_DEC_PLACES))
        self.txtMissionTime.set_text(
            str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_MTIME))

        self.btnConfDir.set_current_folder(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR)
        self.btnDataDir.set_current_folder(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_DATA_DIR)
        self.btnIconDir.set_current_folder(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR)
        self.btnLogDir.set_current_folder(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOG_DIR)

        self.btnRevisionBGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['revisionbg']))
        self.btnRevisionFGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['revisionfg']))
        self.btnFunctionBGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['functionbg']))
        self.btnFunctionFGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['functionfg']))
        self.btnRequirementsBGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['requirementbg']))
        self.btnRequirementsFGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['requirementfg']))
        self.btnHardwareBGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['hardwarebg']))
        self.btnHardwareFGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['hardwarefg']))
        self.btnValidationBGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['validationbg']))
        self.btnValidationFGColor.set_color(
            Gdk.color_parse(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS['validationfg']))

    def _do_quit(self, __button: Gtk.Button) -> None:
        """
        Quit the preferences Gtk.Assistant().

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        self.destroy()

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """
        Request to update the user and program preferences.

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        _conf_file = self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + \
            '/RAMSTK.toml'
        copyfile(_conf_file, _conf_file + '_bak')
        self.RAMSTK_USER_CONFIGURATION.set_user_configuration()

        try:
            copyfile(self._fmt_file, self._fmt_file + '_bak')
            self._do_save_tree_layout()
        # This happens when no format file was edited.
        except FileNotFoundError:
            pass

    def _do_request_update_all(self, button: Gtk.Button) -> None:
        """
        Wrapper method for _do_request_update().

        :param button: the Gtk.Button() that called this method.
        :type button: :class:`Gtk.Button`
        :return: None
        :rtype: None
        """
        self._do_request_update(button)

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
        _file.write('Copyright 2011-2020 Doyle "weibullguy" Rowland '
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

    def _do_select_path(self, button: Gtk.FileChooserButton,
                        index: int) -> None:
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
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR = \
                button.get_current_folder()
        elif index == 1:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_DATA_DIR = \
                button.get_current_folder()
        elif index == 2:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR = \
                button.get_current_folder()
        elif index == 3:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOG_DIR = \
                button.get_current_folder()

    def _do_set_color(self, colorbutton: Gtk.ColorButton,
                      ramstk_color: int) -> None:
        """
        Set the selected color.

        :param colorbutton: the Gtk.ColorButton() that called this method.
        :type colorbutton: :class:`Gtk.ColorButton`
        :param str ramstk_color: the name of the color to set.
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
        self.RAMSTK_USER_CONFIGURATION.RAMSTK_COLORS[ramstk_color] = _color

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

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Edit RAMSTKTreeView() layouts.

        :param combo: the RAMSTKComboBox() that called this method.
        :type combo: :class:`gui.gtk.RAMSTKComboBox`
        :param int index: the index in the signal handler list associated with
            the RAMSTKComboBox() calling this method.
        :return: None
        :rtype: None
        """
        combo.handler_block(combo.dic_handler_id['changed'])

        if index == 0:
            _model = combo.get_model()
            _row = combo.get_active_iter()
            _module = _model.get_value(_row, 1)
            self._do_load_format(_module)
        elif index == 1:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_TABPOS[
                'modulebook'] = combo.get_value()
        elif index == 2:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_TABPOS[
                'workbook'] = combo.get_value()
        elif index == 3:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_TABPOS[
                'listbook'] = combo.get_value()
        elif index == 4:
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_REPORT_SIZE = \
                combo.get_value()

        combo.handler_unblock(combo.dic_handler_id['changed'])
