# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.preferences.general_preferences_panel.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The general preferences panel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFileChooserButton,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class GeneralPreferencesPanel(RAMSTKFixedPanel):
    """The panel to display options to be edited."""

    # Define private class attributes.
    _select_msg = "succeed_get_preferences_attributes"
    _tag = "preferences"
    _title = _("General Preferences")

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
        self.cmbModuleBookTabPosition: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbWorkBookTabPosition: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbListBookTabPosition: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbReportSize: RAMSTKComboBox = RAMSTKComboBox()
        self.txtFRMultiplier: RAMSTKEntry = RAMSTKEntry()
        self.txtDecimalPlaces: RAMSTKEntry = RAMSTKEntry()
        self.txtMissionTime: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.cmbModuleBookTabPosition,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "module_book_tab_pos",
                    "index": 0,
                    "label_text": _("Module Book Tab Position:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbWorkBookTabPosition,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "work_book_tab_pos",
                    "index": 1,
                    "label_text": _("Work Book Tab Position:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbListBookTabPosition,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "list_book_tab_pos",
                    "index": 2,
                    "label_text": _("List Book Tab Position:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbReportSize,
                {
                    "datatype": "gchararray",
                    "default": "Letter",
                    "field": "report_size",
                    "index": 3,
                    "label_text": _("Report Paper Size:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtFRMultiplier,
                {
                    "datatype": "gfloat",
                    "default": 6,
                    "field": "fr_multiplier",
                    "index": 4,
                    "label_text": _("Failure Rate Multiplier:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                    "width_request": 75,
                },
            ),
            make_widget_config(
                self.txtDecimalPlaces,
                {
                    "datatype": "gint",
                    "default": 3,
                    "field": "decimals",
                    "index": 5,
                    "label_text": _("Decimal Places:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                    "width_request": 75,
                },
            ),
            make_widget_config(
                self.txtMissionTime,
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "mission_time",
                    "index": 6,
                    "label_text": _("Reliability Mission Time:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnConfDir,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "config_file_path",
                    "index": 7,
                    "label_text": _("Path to RAMSTK Configuration Files:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "height_request": 30,
                    "fg_color": "#000000",
                    "action": Gtk.FileChooserAction.SELECT_FOLDER,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnDataDir,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "data_file_path",
                    "index": 8,
                    "label_text": _("Path to RAMSTK Data Files:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "height_request": 30,
                    "fg_color": "#000000",
                    "action": Gtk.FileChooserAction.SELECT_FOLDER,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnIconDir,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "icon_file_path",
                    "index": 9,
                    "label_text": _("Path to RAMSTK Icon Files:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "height_request": 30,
                    "fg_color": "#000000",
                    "action": Gtk.FileChooserAction.SELECT_FOLDER,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnLogDir,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "log_file_path",
                    "index": 10,
                    "label_text": _("Path to RAMSTK Log Files:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "height_request": 30,
                    "fg_color": "#000000",
                    "action": Gtk.FileChooserAction.SELECT_FOLDER,
                    "visible": True,
                },
            ),
        ]
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration()

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        self._do_set_widget_callbacks()
        self._do_load_paper_sizes()
        self._do_load_tab_positions()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "request_load_preferences": self._do_load_panel,
            }
        )

    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None:
        """Load the current preference values.

        :param configuration: the RAMSTKUserConfiguration object containing the current
            preferences.
        """
        _positions = {"bottom": 1, "left": 2, "right": 3, "top": 4}
        _papersize = {"a4": 1, "letter": 2}

        self._configuration = configuration

        self.cmbModuleBookTabPosition.do_update(
            {
                "module_book_tab_pos": _positions[
                    self._configuration.RAMSTK_TABPOS["modulebook"].lower()
                ]
            },
        )
        self.cmbWorkBookTabPosition.do_update(
            {
                "work_book_tab_pos": _positions[
                    self._configuration.RAMSTK_TABPOS["workbook"].lower()
                ]
            },
        )
        self.cmbListBookTabPosition.do_update(
            {
                "list_book_tab_pos": _positions[
                    self._configuration.RAMSTK_TABPOS["listbook"].lower()
                ]
            },
        )
        self.cmbReportSize.do_update(
            {"report_size": _papersize[self._configuration.RAMSTK_REPORT_SIZE.lower()]},
        )

        self.txtFRMultiplier.do_update(
            {"fr_multiplier": str(self._configuration.RAMSTK_HR_MULTIPLIER)},
        )
        self.txtDecimalPlaces.do_update(
            {"decimals": str(self._configuration.RAMSTK_DEC_PLACES)},
        )
        self.txtMissionTime.do_update(
            {"mission_time": str(self._configuration.RAMSTK_MTIME)},
        )

        self.btnConfDir.set_current_folder(self._configuration.RAMSTK_CONF_DIR)
        self.btnDataDir.set_current_folder(self._configuration.RAMSTK_DATA_DIR)
        self.btnIconDir.set_current_folder(self._configuration.RAMSTK_ICON_DIR)
        self.btnLogDir.set_current_folder(self._configuration.RAMSTK_LOG_DIR)

    def _do_load_paper_sizes(self) -> None:
        """Load the paper size RAMSTKComboBox with its entries."""
        self.cmbReportSize.do_load_combo([["A4"], ["Letter"]])

    def _do_load_tab_positions(self) -> None:
        """Load the tab position RAMSTKComboBoxes with their entries."""
        self.cmbModuleBookTabPosition.do_load_combo(
            [["Bottom"], ["Left"], ["Right"], ["Top"]]
        )
        self.cmbWorkBookTabPosition.do_load_combo(
            [["Bottom"], ["Left"], ["Right"], ["Top"]]
        )
        self.cmbListBookTabPosition.do_load_combo(
            [["Bottom"], ["Left"], ["Right"], ["Top"]]
        )

    def _do_select_path(self, button: Gtk.FileChooserButton, index: int) -> None:
        """Select the path from the file chooser.

        :param button: the Gtk.FileChooserButton() that called this method.
        :param index: the index of the Gtk.FileChooserButton() that called this method.
        """
        if index == 0:
            self._configuration.RAMSTK_CONF_DIR = button.get_current_folder()
        elif index == 1:
            self._configuration.RAMSTK_DATA_DIR = button.get_current_folder()
        elif index == 2:
            self._configuration.RAMSTK_ICON_DIR = button.get_current_folder()
        elif index == 3:
            self._configuration.RAMSTK_LOG_DIR = button.get_current_folder()

    def _do_set_widget_callbacks(self) -> None:
        """Set the callback methods for the widgets."""
        self.btnConfDir.dic_handler_id["file-set"] = self.btnConfDir.connect(
            "file-set", self._do_select_path, 0
        )
        self.btnDataDir.dic_handler_id["file-set"] = self.btnDataDir.connect(
            "file-set", self._do_select_path, 1
        )
        self.btnIconDir.dic_handler_id["file-set"] = self.btnIconDir.connect(
            "file-set", self._do_select_path, 2
        )
        self.btnLogDir.dic_handler_id["file-set"] = self.btnLogDir.connect(
            "file-set", self._do_select_path, 3
        )

        self.cmbModuleBookTabPosition.dic_handler_id["changed"] = (
            self.cmbModuleBookTabPosition.connect("changed", self._on_combo_changed, 0)
        )
        self.cmbWorkBookTabPosition.dic_handler_id["changed"] = (
            self.cmbWorkBookTabPosition.connect("changed", self._on_combo_changed, 1)
        )
        self.cmbListBookTabPosition.dic_handler_id["changed"] = (
            self.cmbListBookTabPosition.connect("changed", self._on_combo_changed, 2)
        )
        self.cmbReportSize.dic_handler_id["changed"] = self.cmbReportSize.connect(
            "changed", self._on_combo_changed, 3
        )

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """Edit RAMSTKTreeView() layouts.

        :param combo: the RAMSTKComboBox() that called this method.
        :type combo: :class:`gui.gtk.RAMSTKComboBox`
        :param index: the index in the signal handler list associated with
            the RAMSTKComboBox() calling this method.
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
