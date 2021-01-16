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
from datetime import datetime
from shutil import copyfile
from typing import Any, Dict, List

# Third Party Imports
# noinspection PyPackageRequirements
import toml
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.utilities import integer_to_boolean, string_to_boolean
from ramstk.views.gtk3 import Gdk, GObject, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKBaseView, RAMSTKComboBox, RAMSTKEntry, RAMSTKLabel,
    RAMSTKPanel, do_make_column, do_make_text_cell,
    do_make_toggle_cell, do_set_cell_properties
)


class GeneralPreferencesPanel(RAMSTKPanel):
    """The panel to display options to be edited."""
    def __init__(self) -> None:
        """Initialize an instance of the Preferences panel."""
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
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
        ]

        # Initialize private scalar instance attributes.
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration(
        )
        self._title: str = _("General Preferences")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
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

        self._lst_widgets = [
            self.cmbModuleBookTabPosition, self.cmbWorkBookTabPosition,
            self.cmbListBookTabPosition, self.cmbReportSize,
            self.txtFRMultiplier, self.txtDecimalPlaces, self.txtMissionTime,
            self.btnConfDir, self.btnDataDir, self.btnLogDir
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_load_comboboxes()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel, 'request_load_preferences')

    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None:
        """Load the current preference values.

        :return: None
        :rtype: None
        """
        _positions = {"bottom": 1, "left": 2, "right": 3, "top": 4}
        _papersize = {'a4': 1, 'letter': 2}

        self._configuration = configuration

        self.cmbModuleBookTabPosition.do_update(_positions[
            self._configuration.RAMSTK_TABPOS['modulebook'].lower()],
                                                signal='changed')
        self.cmbWorkBookTabPosition.do_update(
            _positions[self._configuration.RAMSTK_TABPOS['workbook'].lower()],
            signal='changed')
        self.cmbListBookTabPosition.do_update(
            _positions[self._configuration.RAMSTK_TABPOS['listbook'].lower()],
            signal='changed')
        self.cmbReportSize.do_update(
            _papersize[self._configuration.RAMSTK_REPORT_SIZE.lower()],
            signal='changed')

        self.txtFRMultiplier.do_update(str(
            self._configuration.RAMSTK_HR_MULTIPLIER),
                                       signal='changed')
        self.txtDecimalPlaces.do_update(str(
            self._configuration.RAMSTK_DEC_PLACES),
                                        signal='changed')
        self.txtMissionTime.do_update(str(self._configuration.RAMSTK_MTIME),
                                      signal='changed')

        self.btnConfDir.set_current_folder(self._configuration.RAMSTK_CONF_DIR)
        self.btnDataDir.set_current_folder(self._configuration.RAMSTK_DATA_DIR)
        self.btnIconDir.set_current_folder(self._configuration.RAMSTK_ICON_DIR)
        self.btnLogDir.set_current_folder(self._configuration.RAMSTK_LOG_DIR)

    def __do_load_comboboxes(self) -> None:
        """Load the RAMSTKComboBoxes() with their data.

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

    def __do_select_path(self, button: Gtk.FileChooserButton,
                         index: int) -> None:
        """Select the path from the file chooser.

        :param button: the Gtk.FileChooserButton() that called this method.
        :param index: the index of the Gtk.FileChooserButton() that called
            this method.
        :return: None
        :rtyp: None
        """
        if index == 0:
            self._configuration.RAMSTK_CONF_DIR = button.get_current_folder()
        elif index == 1:
            self._configuration.RAMSTK_DATA_DIR = button.get_current_folder()
        elif index == 2:
            self._configuration.RAMSTK_ICON_DIR = button.get_current_folder()
        elif index == 3:
            self._configuration.RAMSTK_LOG_DIR = button.get_current_folder()

    def __do_set_callbacks(self) -> None:
        """Set the callback functions/methods for each of the widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnConfDir.connect('file-set', self.__do_select_path, 0)
        self.btnDataDir.connect('file-set', self.__do_select_path, 1)
        self.btnIconDir.connect('file-set', self.__do_select_path, 2)
        self.btnLogDir.connect('file-set', self.__do_select_path, 3)

        # ----- COMBOBOXES
        self.cmbModuleBookTabPosition.dic_handler_id[
            'changed'] = self.cmbModuleBookTabPosition.connect(
                'changed', self.__on_change_combo, 1)
        self.cmbWorkBookTabPosition.dic_handler_id[
            'changed'] = self.cmbWorkBookTabPosition.connect(
                'changed', self.__on_change_combo, 2)
        self.cmbListBookTabPosition.dic_handler_id[
            'changed'] = self.cmbListBookTabPosition.connect(
                'changed', self.__on_change_combo, 3)
        self.cmbReportSize.dic_handler_id[
            'changed'] = self.cmbReportSize.connect('changed',
                                                    self.__on_change_combo, 4)

    def __do_set_properties(self) -> None:
        """Set the properties of the Preferences assistance widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnConfDir.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.btnDataDir.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.btnIconDir.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.btnLogDir.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        self.btnConfDir.height = 30
        self.btnDataDir.height = 30
        self.btnIconDir.height = 30
        self.btnLogDir.height = 30

        # ----- ENTRIES
        self.txtFRMultiplier.do_set_properties(width=75)
        self.txtDecimalPlaces.do_set_properties(width=75)

    def __on_change_combo(self, combo: RAMSTKComboBox, index: int) -> \
            None:
        """Edit RAMSTKTreeView() layouts.

        :param combo: the RAMSTKComboBox() that called this method.
        :type combo: :class:`gui.gtk.RAMSTKComboBox`
        :param index: the index in the signal handler list associated with
            the RAMSTKComboBox() calling this method.
        :return: None
        :rtype: None
        """
        combo.handler_block(combo.dic_handler_id['changed'])

        if index == 1:
            self._configuration.RAMSTK_TABPOS['modulebook'] = combo.get_value()
        elif index == 2:
            self._configuration.RAMSTK_TABPOS['workbook'] = combo.get_value()
        elif index == 3:
            self._configuration.RAMSTK_TABPOS['listbook'] = combo.get_value()
        elif index == 4:
            self._configuration.RAMSTK_REPORT_SIZE = combo.get_value()

        combo.handler_unblock(combo.dic_handler_id['changed'])


class LookFeelPanel(RAMSTKPanel):
    """The panel to display options to be edited."""
    def __init__(self) -> None:
        """Initialize an instance of the Look and Feel panel."""
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Revision Tree Background Color:"),
            _("Revision Tree Foreground Color:"),
            _("Function Tree Background Color:"),
            _("Function Tree Foreground Color:"),
            _("Requirements Tree Background Color:"),
            _("Requirements Tree Foreground Color:"),
            _("Hardware Tree Background Color:"),
            _("Hardware Tree Foreground Color:"),
            _("Validation Tree Background Color:"),
            _("Validation Tree Foreground Color:"),
        ]

        # Initialize private scalar instance attributes.
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration(
        )
        self._title: str = _("Look &amp; Feel")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
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

        self.cmbFormatFiles = RAMSTKComboBox(simple=False)
        self.tvwTreeView = Gtk.TreeView()

        self._lst_widgets = [
            self.btnRevisionBGColor, self.btnRevisionFGColor,
            self.btnFunctionBGColor, self.btnFunctionFGColor,
            self.btnRequirementsBGColor, self.btnRequirementsFGColor,
            self.btnHardwareBGColor, self.btnHardwareFGColor,
            self.btnValidationBGColor, self.btnValidationFGColor
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel, 'request_load_preferences')

    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None:
        """Load the current preference values.

        :return: None
        :rtype: None
        """
        self._configuration = configuration

        self.btnRevisionBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS['revisionbg']))
        self.btnRevisionFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS['revisionfg']))
        self.btnFunctionBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS['functionbg']))
        self.btnFunctionFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS['functionfg']))
        self.btnRequirementsBGColor.set_color(
            Gdk.color_parse(
                self._configuration.RAMSTK_COLORS['requirementbg']))
        self.btnRequirementsFGColor.set_color(
            Gdk.color_parse(
                self._configuration.RAMSTK_COLORS['requirementfg']))
        self.btnHardwareBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS['hardwarebg']))
        self.btnHardwareFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS['hardwarefg']))
        self.btnValidationBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS['validationbg']))
        self.btnValidationFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS['validationfg']))

    def _do_set_color(self, colorbutton: Gtk.ColorButton,
                      ramstk_color: int) -> None:
        """Set the selected color.

        :param colorbutton: the Gtk.ColorButton() that called this method.
        :param ramstk_color: the name of the color to set.
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
        self._configuration.RAMSTK_COLORS[ramstk_color] = _color

    def __do_set_callbacks(self) -> None:
        """Set the callback functions/methods for each of the widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
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

    def __do_set_properties(self) -> None:
        """Set the properties of the Preferences assistance widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnRevisionBGColor.height = 30
        self.btnRevisionFGColor.height = 30
        self.btnFunctionBGColor.height = 30
        self.btnFunctionFGColor.height = 30
        self.btnRequirementsBGColor.height = 30
        self.btnRequirementsFGColor.height = 30
        self.btnHardwareBGColor.height = 30
        self.btnHardwareFGColor.height = 30
        self.btnSoftwareBGColor.height = 30
        self.btnSoftwareFGColor.height = 30
        self.btnValidationBGColor.height = 30
        self.btnValidationFGColor.height = 30
        self.btnIncidentBGColor.height = 30
        self.btnIncidentFGColor.height = 30
        self.btnTestingBGColor.height = 30
        self.btnTestingFGColor.height = 30


class TreeLayoutPanel(RAMSTKPanel):
    """The panel to display options to be edited."""
    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKTreeView Layout panel."""
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [_("Select format file to edit:")]

        # Initialize private scalar instance attributes.
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration(
        )
        self._title: str = _("Tree View Layout")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.cmbFormatFiles = RAMSTKComboBox(simple=False)
        self.fmt_file: str = ''

        self._lst_widgets = [self.cmbFormatFiles]

        # Make a fixed type panel.
        self.__do_set_properties()
        self.__do_make_treeview()
        self.__make_ui()
        self.__do_load_comboboxes()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel, 'request_load_preferences')

    @staticmethod
    def _do_edit_cell(__cell, path, new_text, position, model) -> None:
        """Handle Gtk.CellRenderer() edits.

        :param __cell: the Gtk.CellRenderer() that was edited.
        :param path: the Gtk.TreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param position: the column position of the edited
            Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        """
        _type = GObject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

    def _do_load_format(self, module: str) -> None:
        """Load the selected Module View format file for editing.

        :param module: the name of the RAMSTK workstream module whose
            Module View layout is to be edited.
        :return: None
        :rtype: None
        """
        self.fmt_file = (self._configuration.RAMSTK_CONF_DIR + '/layouts/'
                         + self._configuration.RAMSTK_FORMAT_FILE[module])

        _format = toml.load(self.fmt_file)

        _datatypes = _format['datatype']
        _default = _format['defaulttitle']
        _editable = _format['editable']
        _user = _format['usertitle']
        _keys = _format['key']
        _position = _format['position']
        _visible = _format['visible']
        _widgets = _format['widget']

        _model = self.tvwTreeView.get_model()
        _model.clear()
        # pylint: disable=unused-variable
        for _key in _default:
            _data = [
                _default[_key], _user[_key],
                int(_position[_key]),
                string_to_boolean(_editable[_key]),
                string_to_boolean(_visible[_key]), _datatypes[_key],
                _widgets[_key], _keys[_key], _key
            ]
            _model.append(_data)

    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None:
        """Load the current preference values.

        :return: None
        :rtype: None
        """
        self._configuration = configuration

    @staticmethod
    def _do_toggle_cell(cell, path, position, model) -> None:
        """Handle Gtk.CellRendererToggle() edits.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the Gtk.TreeView() path of the Gtk.CellRenderer() that
                     was edited.
        :param position: the column position of the edited Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        model[path][position] = not cell.get_active()

    def __do_load_comboboxes(self) -> None:
        """Load the RAMSTKComboBoxes() with their data.

        :return: None
        :rtype: None
        """
        self.cmbFormatFiles.do_load_combo([
            [_("Allocation"), 'allocation', ''],
            [_("Failure Definition"), 'failure_definition', ''],
            [_("(D)FME(C)A"), 'fmea', ''],
            [_("Function"), 'function', ''],
            [_("Hardware"), 'hardware', ''],
            [_("Hazards Analysis"), 'hazard', ''],
            [_("Physics of Failure Analysis"), 'pof', ''],
            [_("Requirements"), 'requirement', ''],
            [_("Revisions"), 'revision', ''],
            [_("Similar Item Analysis"), 'similar_item', ''],
            [_("Stakeholder Inputs"), 'stakeholder', ''],
            [_("Usage Profile"), 'usage_profile', ''],
            [_("Validation"), 'validation', ''],
        ],
                                          simple=False)  # noqa

    def __do_make_treeview(self) -> None:
        """Make the format file editing Gtk.Treeview().

        :return: None
        :rtype: None
        """
        _bg_color = [
            'light gray', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF',
            'light gray', 'light gray', 'light gray', 'light gray'
        ]
        _editable = [False, True, True, True, True, False, False, False, False]
        _visible = [True, True, True, True, True, False, False, False, False]
        _model = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING,
                               GObject.TYPE_INT, GObject.TYPE_INT,
                               GObject.TYPE_INT, GObject.TYPE_STRING,
                               GObject.TYPE_STRING, GObject.TYPE_STRING,
                               GObject.TYPE_STRING)
        self.tvwTreeView.set_model(_model)

        for _idx, _text in enumerate([
                _("Default\nTitle"),
                _("User\nTitle"),
                _("Column\nPosition"),
                _("Can\nEdit?"),
                _("Is\nVisible?")
        ]):
            if _idx in [3, 4]:
                _cell = do_make_toggle_cell()
                _cell.connect('toggled', self._do_toggle_cell, _idx, _model)
                _column = do_make_column([_cell],
                                         heading=_text,
                                         visible=_visible[_idx])
                _column.set_attributes(_cell, active=_idx)
            else:
                _cell = do_make_text_cell(False)
                _cell.connect('edited', self._do_edit_cell, _idx, _model)
                _column = do_make_column([_cell],
                                         heading=_text,
                                         visible=_visible[_idx])
                _column.set_attributes(_cell, text=_idx)

            do_set_cell_properties(_cell,
                                   bg_color=_bg_color[_idx],
                                   editable=_editable[_idx],
                                   fg_color='#000000')

            self.tvwTreeView.append_column(_column)

    def __do_set_callbacks(self) -> None:
        """Set the callback functions/methods for each of the widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbFormatFiles.dic_handler_id[
            'changed'] = self.cmbFormatFiles.connect('changed',
                                                     self.__on_change_combo)

    def __do_set_properties(self) -> None:
        """Set the properties of the Preferences assistance widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbFormatFiles.do_set_properties(
            tooltip=_("Select the Tree View layout to edit."))

    def __make_ui(self) -> None:
        """Build the UI for the Preferences assistant."""
        super().do_make_panel_treeview()

        _scrollwindow = self.get_child()
        self.remove(_scrollwindow)

        _label = RAMSTKLabel(self._lst_labels[0])
        _x_pos = _label.get_attribute('width')

        _fixed: Gtk.Fixed = Gtk.Fixed()
        _fixed.put(_label, 5, 5)
        _fixed.put(self.cmbFormatFiles, _x_pos + 10, 5)

        _vbox = Gtk.VBox()
        _vbox.pack_start(_fixed, False, False, 0)
        _vbox.pack_end(_scrollwindow, True, True, 0)

        self.add(_vbox)

    def __on_change_combo(self, combo: RAMSTKComboBox) -> None:
        """Edit RAMSTKTreeView() layouts.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        :rtype: None
        """
        combo.handler_block(combo.dic_handler_id['changed'])

        _model = combo.get_model()
        _row = combo.get_active_iter()
        _module = _model.get_value(_row, 1)
        self._do_load_format(_module)

        combo.handler_unblock(combo.dic_handler_id['changed'])


class EditPreferences(RAMSTKBaseView):
    """Assistant to provide a GUI to set various RAMSTK config preferences.

    RAMSTK preferences are stored in the RAMSTK Site database and the
    user's Site configuration file and Program configuration file.
    Configurations preferences are stored in Site.conf or RAMSTK.conf in
    each user's $HOME/.config/RAMSTK directory and are applicable only
    to that specific user.  Configuration preferences are edited with
    the Preferences assistant.
    """
    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module = 'preferences'
    _pixbuf: bool = True
    _tablabel: str = _("")
    _tabtooltip: str = _("")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize an instance of the Preferences assistant.

        :param __widget: the Gtk.ImageMenuItem() that called this assistant.
        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [self._do_request_update, self._cancel]
        self._lst_icons = ['save', 'cancel']
        self._lst_tooltips = [
            _("Save changes to RAMSTK program configuration file "
              "{0}/RAMSTK.toml.".format(configuration.RAMSTK_CONF_DIR)),
            _("Quit the RAMSTK preferences assistant without saving.")
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralPreferences = GeneralPreferencesPanel()
        self._pnlLookFeel = LookFeelPanel()
        self._pnlTreeViewLayout = TreeLayoutPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        pub.sendMessage(
            'request_load_preferences',
            configuration=self.RAMSTK_USER_CONFIGURATION,
        )

    def _cancel(self, __button: Gtk.Button) -> None:
        """Quit the preferences Gtk.Assistant().

        :param __button: the Gtk.Button() that called this method.
        :return: None
        """
        _parent = self.get_parent()
        _parent.destroy()

    def _do_request_update(self, __button: Gtk.Button) -> None:
        """Request to update the user and program preferences.

        :param __button: the Gtk.Button() that called this method.
        :return: None
        """
        _conf_file = self.RAMSTK_USER_CONFIGURATION.RAMSTK_CONF_DIR + \
            '/RAMSTK.toml'
        copyfile(_conf_file, _conf_file + '_bak')
        self.RAMSTK_USER_CONFIGURATION.set_user_configuration()

        try:
            self._do_save_tree_layout()
        # This happens when no format file was edited.
        except FileNotFoundError:
            pass

    def _do_save_tree_layout(self) -> None:
        """Save the Module View RAMSTKTreeView() layout file.

        :return: None
        """
        _layout: Dict[str, Any] = {
            'pixbuf': 'False',
            'defaulttitle': {},
            'usertitle': {},
            'datatype': {},
            'position': {},
            'widget': {},
            'editable': {},
            'visible': {},
            'key': {},
        }

        copyfile(self._pnlTreeViewLayout.fmt_file,
                 self._pnlTreeViewLayout.fmt_file + '_bak')

        # Get the format file for the Gtk.TreeView to be edited.  Make a
        # backup copy by appending the current date.
        _now = datetime.today().strftime('%Y%m%d')
        _bak_file = '{0:s}_bak_{1:s}.toml'.format(
            self._pnlTreeViewLayout.fmt_file[:-5], _now)
        copyfile(self._pnlTreeViewLayout.fmt_file, _bak_file)

        # Open the format file for writing.
        _file = open(self._pnlTreeViewLayout.fmt_file, 'w')

        _model = self._pnlTreeViewLayout.tvwTreeView.get_model()
        _row = _model.get_iter_first()
        while _row is not None:
            _key = _model.get_value(_row, 8)
            _layout['defaulttitle'][_key] = _model.get_value(_row, 0)
            _layout['usertitle'][_key] = _model.get_value(_row, 1)
            _layout['position'][_key] = _model.get_value(_row, 2)
            _layout['editable'][_key] = integer_to_boolean(
                _model.get_value(_row, 3))
            _layout['visible'][_key] = integer_to_boolean(
                _model.get_value(_row, 4))
            _layout['datatype'][_key] = _model.get_value(_row, 5)
            _layout['widget'][_key] = _model.get_value(_row, 6)
            _layout['key'][_key] = _model.get_value(_row, 7)

            _row = _model.iter_next(_row)

        toml.dump(_layout, _file)

    def __make_ui(self) -> None:
        """Build the user interface.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        _label = RAMSTKLabel(_("General &amp; Directories"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Allows setting general preferences for the "
                      "open RAMSTK program."))
        self._notebook.insert_page(self._pnlGeneralPreferences,
                                   tab_label=_label,
                                   position=-1)

        _label = RAMSTKLabel(_("Look &amp; Feel"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Allows setting color and other preferences."))
        self._notebook.insert_page(self._pnlLookFeel,
                                   tab_label=_label,
                                   position=-1)

        _label = RAMSTKLabel(_("Tree View Layout"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Allows setting tree view layout preferences."))
        self._notebook.insert_page(self._pnlTreeViewLayout,
                                   tab_label=_label,
                                   position=-1)

        self.pack_end(self._notebook, True, True, 0)

        self.show_all()
