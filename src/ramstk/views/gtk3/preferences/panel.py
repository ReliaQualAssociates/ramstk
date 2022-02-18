# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.preferences.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Preferences Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import toml
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.utilities import string_to_boolean
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFileChooserButton,
    RAMSTKFixedPanel,
    RAMSTKLabel,
    RAMSTKTreePanel,
    RAMSTKTreeView,
)


class GeneralPreferencesPanel(RAMSTKFixedPanel):
    """The panel to display options to be edited."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_get_preferences_attributes"
    _tag = "preferences"
    _title = _("General Preferences")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Preferences panel."""
        super().__init__()

        # Initialize widgets.
        self.btnConfDir: RAMSTKFileChooserButton = RAMSTKFileChooserButton(
            _("RAMSTK Configuration File Directory")
        )
        self.btnDataDir: RAMSTKFileChooserButton = RAMSTKFileChooserButton(
            _("RAMSTK Data Directory")
        )
        self.btnIconDir: RAMSTKFileChooserButton = RAMSTKFileChooserButton(
            _("RAMSTK Icon Directory")
        )
        self.btnLogDir: RAMSTKFileChooserButton = RAMSTKFileChooserButton(
            _("RAMSTK Log Directory")
        )

        self.cmbModuleBookTabPosition: RAMSTKComboBox = RAMSTKComboBox(simple=True)
        self.cmbWorkBookTabPosition: RAMSTKComboBox = RAMSTKComboBox(simple=True)
        self.cmbListBookTabPosition: RAMSTKComboBox = RAMSTKComboBox(simple=True)
        self.cmbReportSize: RAMSTKComboBox = RAMSTKComboBox(simple=True)

        self.txtFRMultiplier: RAMSTKEntry = RAMSTKEntry()
        self.txtDecimalPlaces: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionTime: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration()

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "module_book_tab_pos": [
                0,
                self.cmbModuleBookTabPosition,
                "changed",
                self._on_changed_combo,
                "",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Module Book Tab Position:"),
                "gchararray",
            ],
            "work_book_tab_pos": [
                1,
                self.cmbWorkBookTabPosition,
                "changed",
                self._on_changed_combo,
                "",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Work Book Tab Position:"),
                "gchararray",
            ],
            "list_book_tab_pos": [
                2,
                self.cmbListBookTabPosition,
                "changed",
                self._on_changed_combo,
                "",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("List Book Tab Position:"),
                "gchararray",
            ],
            "report_size": [
                3,
                self.cmbReportSize,
                "changed",
                super().on_changed_combo,
                "",
                "Letter",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Report Paper Size:"),
                "gchararray",
            ],
            "fr_multiplier": [
                4,
                self.txtFRMultiplier,
                "changed",
                super().on_changed_entry,
                "",
                6,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                    "width": 75,
                },
                _("Failure Rate Multiplier:"),
                "gfloat",
            ],
            "decimals": [
                5,
                self.txtDecimalPlaces,
                "changed",
                super().on_changed_entry,
                "",
                3,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                    "width": 75,
                },
                _("Decimal Places:"),
                "gint",
            ],
            "mission_time": [
                6,
                self.txtMissionTime,
                "changed",
                super().on_changed_entry,
                "",
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Reliability Mission Time:"),
                "gfloat",
            ],
            "config_file_path": [
                7,
                self.btnConfDir,
                "file-set",
                self._do_select_path,
                "",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "height": 30,
                    "fg_color": "#000000",
                    "select-action": Gtk.FileChooserAction.SELECT_FOLDER,
                    "visible": True,
                },
                _("Path to RAMSTK Configuration Files:"),
                "gchararray",
            ],
            "data_file_path": [
                8,
                self.btnDataDir,
                "file-set",
                self._do_select_path,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "height": 30,
                    "fg_color": "#000000",
                    "select-action": Gtk.FileChooserAction.SELECT_FOLDER,
                    "visible": True,
                },
                _("Path to RAMSTK Data Files:"),
                "gchararray",
            ],
            "icon_file_path": [
                9,
                self.btnIconDir,
                "file-set",
                self._do_select_path,
                "",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "height": 30,
                    "fg_color": "#000000",
                    "select-action": Gtk.FileChooserAction.SELECT_FOLDER,
                    "visible": True,
                },
                _("Path to RAMSTK Icon Files:"),
                "gchararray",
            ],
            "log_file_path": [
                10,
                self.btnLogDir,
                "file-set",
                self._do_select_path,
                "",
                2,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "height": 30,
                    "fg_color": "#000000",
                    "select-action": Gtk.FileChooserAction.SELECT_FOLDER,
                    "visible": True,
                },
                _("Path to RAMSTK Log Files:"),
                "gchararray",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        self._do_load_comboboxes()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel, "request_load_preferences")

    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None:
        """Load the current preference values.

        :return: None
        :rtype: None
        """
        _positions = {"bottom": 1, "left": 2, "right": 3, "top": 4}
        _papersize = {"a4": 1, "letter": 2}

        self._configuration = configuration

        self.cmbModuleBookTabPosition.do_update(
            _positions[self._configuration.RAMSTK_TABPOS["modulebook"].lower()],
            signal="changed",
        )
        self.cmbWorkBookTabPosition.do_update(
            _positions[self._configuration.RAMSTK_TABPOS["workbook"].lower()],
            signal="changed",
        )
        self.cmbListBookTabPosition.do_update(
            _positions[self._configuration.RAMSTK_TABPOS["listbook"].lower()],
            signal="changed",
        )
        self.cmbReportSize.do_update(
            _papersize[self._configuration.RAMSTK_REPORT_SIZE.lower()],
            signal="changed",
        )

        self.txtFRMultiplier.do_update(
            str(self._configuration.RAMSTK_HR_MULTIPLIER), signal="changed"
        )
        self.txtDecimalPlaces.do_update(
            str(self._configuration.RAMSTK_DEC_PLACES), signal="changed"
        )
        self.txtMissionTime.do_update(
            str(self._configuration.RAMSTK_MTIME), signal="changed"
        )

        self.btnConfDir.set_current_folder(self._configuration.RAMSTK_CONF_DIR)
        self.btnDataDir.set_current_folder(self._configuration.RAMSTK_DATA_DIR)
        self.btnIconDir.set_current_folder(self._configuration.RAMSTK_ICON_DIR)
        self.btnLogDir.set_current_folder(self._configuration.RAMSTK_LOG_DIR)

    def _do_load_comboboxes(self) -> None:
        """Load the RAMSTKComboBoxes() with their data.

        :return: None
        :rtype: None
        """
        self.cmbModuleBookTabPosition.do_load_combo(
            [["Bottom"], ["Left"], ["Right"], ["Top"]]
        )
        self.cmbWorkBookTabPosition.do_load_combo(
            [["Bottom"], ["Left"], ["Right"], ["Top"]]
        )
        self.cmbListBookTabPosition.do_load_combo(
            [["Bottom"], ["Left"], ["Right"], ["Top"]]
        )
        self.cmbReportSize.do_load_combo([["A4"], ["Letter"]])

    def _do_select_path(self, button: Gtk.FileChooserButton, index: int) -> None:
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

    def _on_changed_combo(self, combo: RAMSTKComboBox, index: int) -> None:
        """Edit RAMSTKTreeView() layouts.

        :param combo: the RAMSTKComboBox() that called this method.
        :type combo: :class:`gui.gtk.RAMSTKComboBox`
        :param index: the index in the signal handler list associated with
            the RAMSTKComboBox() calling this method.
        :return: None
        :rtype: None
        """
        combo.handler_block(combo.dic_handler_id["changed"])

        if index == 1:
            self._configuration.RAMSTK_TABPOS["modulebook"] = combo.get_value()
        elif index == 2:
            self._configuration.RAMSTK_TABPOS["workbook"] = combo.get_value()
        elif index == 3:
            self._configuration.RAMSTK_TABPOS["listbook"] = combo.get_value()
        elif index == 4:
            self._configuration.RAMSTK_REPORT_SIZE = combo.get_value()

        combo.handler_unblock(combo.dic_handler_id["changed"])


class LookFeelPreferencesPanel(RAMSTKFixedPanel):
    """The panel to display options to be edited."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_get_preferences_attributes"
    _tag = "preferences"
    _title = _("Look &amp; Feel")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Look and Feel panel."""
        super().__init__()

        # Initialize widgets.
        self.btnRevisionBGColor = Gtk.ColorButton()
        self.btnRevisionFGColor = Gtk.ColorButton()
        self.btnFunctionBGColor = Gtk.ColorButton()
        self.btnFunctionFGColor = Gtk.ColorButton()
        self.btnRequirementsBGColor = Gtk.ColorButton()
        self.btnRequirementsFGColor = Gtk.ColorButton()
        self.btnHardwareBGColor = Gtk.ColorButton()
        self.btnHardwareFGColor = Gtk.ColorButton()
        self.btnValidationBGColor = Gtk.ColorButton()
        self.btnValidationFGColor = Gtk.ColorButton()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration()

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "revisionbg": [
                0,
                self.btnRevisionBGColor,
                "color-set",
                self._do_set_color,
                "",
                "#FFFFFF",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                },
                _("Revision Tree Background Color:"),
            ],
            "revisionfg": [
                1,
                self.btnRevisionFGColor,
                "color-set",
                self._do_set_color,
                "",
                "#000000",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                },
                _("Revision Tree Foreground Color:"),
            ],
            "functionbg": [
                2,
                self.btnFunctionBGColor,
                "color-set",
                self._do_set_color,
                "",
                "#FFFFFF",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                },
                _("Function Tree Background Color:"),
            ],
            "functionfg": [
                3,
                self.btnFunctionFGColor,
                "color-set",
                self._do_set_color,
                "",
                "#000000",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                },
                _("Function Tree Foreground Color:"),
            ],
            "requirementbg": [
                4,
                self.btnRequirementsBGColor,
                "color-set",
                self._do_set_color,
                "",
                "#FFFFFF",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                    "width": 75,
                },
                _("Requirements Tree Background Color:"),
            ],
            "requirementfg": [
                5,
                self.btnRequirementsFGColor,
                "color-set",
                self._do_set_color,
                "",
                "#000000",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                    "width": 75,
                },
                _("Requirements Tree Foreground Color:"),
            ],
            "hardwarebg": [
                6,
                self.btnHardwareBGColor,
                "color-set",
                self._do_set_color,
                "",
                "#FFFFFF",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                },
                _("Hardware Tree Background Color:"),
            ],
            "hardwarefg": [
                7,
                self.btnHardwareFGColor,
                "color-set",
                self._do_set_color,
                "",
                "#000000",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                },
                _("Hardware Tree Foreground Color:"),
            ],
            "validationbg": [
                8,
                self.btnValidationBGColor,
                "color-set",
                self._do_set_color,
                "",
                "#FFFFFF",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                },
                _("Validation Tree Background Color:"),
            ],
            "validationfg": [
                9,
                self.btnValidationFGColor,
                "color-set",
                self._do_set_color,
                "",
                "#000000",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height": 30,
                    "visible": True,
                },
                _("Validation Tree Foreground Color:"),
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        self._do_set_properties()
        super().do_make_panel()
        self._do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel, "request_load_preferences")

    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None:
        """Load the current preference values.

        :return: None
        :rtype: None
        """
        self._configuration = configuration

        self.btnRevisionBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["revisionbg"])
        )
        self.btnRevisionFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["revisionfg"])
        )
        self.btnFunctionBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["functionbg"])
        )
        self.btnFunctionFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["functionfg"])
        )
        self.btnRequirementsBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["requirementbg"])
        )
        self.btnRequirementsFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["requirementfg"])
        )
        self.btnHardwareBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["hardwarebg"])
        )
        self.btnHardwareFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["hardwarefg"])
        )
        self.btnValidationBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["validationbg"])
        )
        self.btnValidationFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["validationfg"])
        )

    def _do_set_color(self, colorbutton: Gtk.ColorButton, ramstk_color: int) -> None:
        """Set the selected color.

        :param colorbutton: the Gtk.ColorButton() that called this method.
        :param ramstk_color: the name of the color to set.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Retrieve the six digit hexidecimal version of the selected color.
        _color = colorbutton.get_color()
        try:
            _red = f"{int(_color.red / 255)}:#02"
        except ValueError:
            _red = f"{int(_color.red / 255)}"
        try:
            _green = f"{int(_color.green / 255)}:#02"
        except ValueError:
            _green = f"{int(_color.green / 255)}"
        try:
            _blue = f"{int(_color.blue / 255)}:#02"
        except ValueError:
            _blue = f"{int(_color.blue / 255)}"
        _color = f"#{_red}{_green}{_blue}"

        # Set the color variable.
        self._configuration.RAMSTK_COLORS[ramstk_color] = _color

    def _do_set_callbacks(self) -> None:
        """Set the callback functions/methods for each of the widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnRevisionBGColor.connect("color-set", self._do_set_color, "revisionbg")
        self.btnRevisionFGColor.connect("color-set", self._do_set_color, "revisionfg")
        self.btnFunctionBGColor.connect("color-set", self._do_set_color, "functionbg")
        self.btnFunctionFGColor.connect("color-set", self._do_set_color, "functionfg")
        self.btnRequirementsBGColor.connect(
            "color-set", self._do_set_color, "requirementbg"
        )
        self.btnRequirementsFGColor.connect(
            "color-set", self._do_set_color, "requirementfg"
        )
        self.btnHardwareBGColor.connect("color-set", self._do_set_color, "hardwarebg")
        self.btnHardwareFGColor.connect("color-set", self._do_set_color, "hardwarefg")
        self.btnValidationBGColor.connect(
            "color-set", self._do_set_color, "validationbg"
        )
        self.btnValidationFGColor.connect(
            "color-set", self._do_set_color, "validationfg"
        )

    def _do_set_properties(self) -> None:
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
        self.btnValidationBGColor.height = 30
        self.btnValidationFGColor.height = 30


class TreeLayoutPreferencesPanel(RAMSTKTreePanel):
    """The panel to display options to be edited."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = None
    _tag = "preferences"
    _title = _("Tree View Layout")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKTreeView Layout panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbFormatFiles: RAMSTKComboBox = RAMSTKComboBox(simple=False)
        self.tvwTreeView: RAMSTKTreeView = RAMSTKTreeView()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration()

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.fmt_file: str = ""

        # Make a fixed type panel.
        self._do_load_comboboxes()
        self.__do_make_treeview()
        self.__make_ui()

        self.cmbFormatFiles.do_set_properties(
            tooltip=_("Select the Tree View layout to edit.")
        )
        self.cmbFormatFiles.dic_handler_id["changed"] = self.cmbFormatFiles.connect(
            "changed", self._on_combo_changed
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel, "request_load_preferences")

    def _do_load_comboboxes(self) -> None:
        """Load the RAMSTKComboBoxes() with their data.

        :return: None
        :rtype: None
        """
        self.cmbFormatFiles.do_load_combo(
            [
                [_("Allocation"), "allocation", ""],
                [_("Failure Definition"), "failure_definition", ""],
                [_("(D)FME(C)A"), "fmea", ""],
                [_("Function"), "function", ""],
                [_("Hardware"), "hardware", ""],
                [_("Hazards Analysis"), "hazard", ""],
                [_("Physics of Failure Analysis"), "pof", ""],
                [_("Requirements"), "requirement", ""],
                [_("Revisions"), "revision", ""],
                [_("Similar Item Analysis"), "similar_item", ""],
                [_("Stakeholder Inputs"), "stakeholder", ""],
                [_("Usage Profile"), "usage_profile", ""],
                [_("Validation"), "validation", ""],
            ],
            simple=False,
        )

    def _do_load_format(self, module: str) -> None:
        """Load the selected Module View format file for editing.

        :param module: the name of the RAMSTK workstream module whose
            Module View layout is to be edited.
        :return: None
        :rtype: None
        """
        self.fmt_file = (
            self._configuration.RAMSTK_CONF_DIR
            + "/layouts/"
            + self._configuration.RAMSTK_FORMAT_FILE[module]
        )

        _format = toml.load(self.fmt_file)

        _datatypes = _format["datatype"]
        _defaulttitle = _format["defaulttitle"]
        _editable = _format["editable"]
        _usertitle = _format["usertitle"]
        _keys = _format["key"]
        _position = _format["position"]
        _visible = _format["visible"]
        _widgets = _format["widget"]

        _model = self.tvwTreeView.get_model()
        _model.clear()
        for _key in _defaulttitle:
            _data = [
                _defaulttitle[_key],
                _usertitle[_key],
                int(_position[_key]),
                string_to_boolean(_editable[_key]),
                string_to_boolean(_visible[_key]),
                _datatypes[_key],
                _widgets[_key],
                _keys[_key],
                _key,
            ]
            _model.append(None, _data)

    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None:
        """Load the current preference values.

        :return: None
        :rtype: None
        """
        self._configuration = configuration

    def _on_combo_changed(self, combo: RAMSTKComboBox) -> None:
        """Edit RAMSTKTreeView() layouts.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        :rtype: None
        """
        combo.handler_block(combo.dic_handler_id["changed"])

        _model = combo.get_model()
        _row = combo.get_active_iter()
        _module = _model.get_value(_row, 1)
        self._do_load_format(_module)

        combo.handler_unblock(combo.dic_handler_id["changed"])

    def __do_make_treeview(self) -> None:
        """Make the format file editing Gtk.Treeview().

        :return: None
        :rtype: None
        """
        self.tvwTreeView.position = {
            "col0": 0,
            "col1": 1,
            "col2": 2,
            "col3": 3,
            "col4": 4,
            "col5": 5,
            "col6": 6,
            "col7": 7,
            "col8": 8,
        }
        self.tvwTreeView.headings = {
            "col0": _("Default\nTitle"),
            "col1": _("User\nTitle"),
            "col2": _("Column\nPosition"),
            "col3": _("Can\nEdit?"),
            "col4": _("Is\nVisible?"),
            "col5": "",
            "col6": "",
            "col7": "",
            "col8": "",
        }
        self.tvwTreeView.editable = {
            "col0": "False",
            "col1": "True",
            "col2": "True",
            "col3": "True",
            "col4": "True",
            "col5": "False",
            "col6": "False",
            "col7": "False",
            "col8": "False",
        }
        self.tvwTreeView.visible = {
            "col0": "True",
            "col1": "True",
            "col2": "True",
            "col3": "True",
            "col4": "True",
            "col5": "False",
            "col6": "False",
            "col7": "False",
            "col8": "False",
        }
        self.tvwTreeView.datatypes = {
            "col0": "gchararray",
            "col1": "gchararray",
            "col2": "gint",
            "col3": "gint",
            "col4": "gint",
            "col5": "gchararray",
            "col6": "gchararray",
            "col7": "gchararray",
            "col8": "gchararray",
        }
        self.tvwTreeView.korder = {
            "col0": "default_title",
            "col1": "user_title",
            "col2": "column_position",
            "col3": "can_edit",
            "col4": "is_visible",
            "col5": "unk1",
            "col6": "unk2",
            "col7": "unk3",
            "col8": "unk4",
        }
        self.tvwTreeView.widgets = {
            "default_title": Gtk.CellRendererText(),
            "user_title": Gtk.CellRendererText(),
            "column_position": Gtk.CellRendererText(),
            "can_edit": Gtk.CellRendererToggle(),
            "is_visible": Gtk.CellRendererToggle(),
            "unk1": Gtk.CellRendererText(),
            "unk2": Gtk.CellRendererText(),
            "unk3": Gtk.CellRendererText(),
            "unk4": Gtk.CellRendererText(),
        }
        self.tvwTreeView.do_make_model()
        self.tvwTreeView.do_make_columns()
        self.tvwTreeView.do_set_editable_columns(self.tvwTreeView.do_edit_cell)

    def __make_ui(self) -> None:
        """Build the UI for the Preferences assistant."""
        super().do_make_panel()

        _scrollwindow = self.get_child()
        self.remove(_scrollwindow)

        _label = RAMSTKLabel(_("Select format file to edit:"))
        _x_pos = _label.get_attribute("width")

        _fixed: Gtk.Fixed = Gtk.Fixed()
        _fixed.put(_label, 5, 5)
        _fixed.put(self.cmbFormatFiles, _x_pos + 10, 5)

        _vbox = Gtk.VBox()
        _vbox.pack_start(_fixed, False, False, 0)
        _vbox.pack_end(_scrollwindow, True, True, 0)

        self.add(_vbox)
