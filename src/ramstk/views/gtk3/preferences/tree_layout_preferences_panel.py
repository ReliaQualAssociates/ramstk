# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.preferences.tree_layout_preferences_panel.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The tree layout preferences panel module."""

# Standard Library Imports
from typing import List

# Third Party Imports
import toml

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.utilities import do_subscribe_to_messages, string_to_boolean
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererText,
    RAMSTKCellRendererToggle,
    RAMSTKComboBox,
    RAMSTKLabel,
    RAMSTKTreePanel,
    RAMSTKTreeView,
    WidgetConfig,
    make_widget_config,
)


class TreeLayoutPreferencesPanel(RAMSTKTreePanel):
    """The panel to display options to be edited."""

    # Define private class attributes.
    _select_msg = None
    _tag = "preferences"
    _title = _("Tree View Layout")

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKTreeView Layout panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbFormatFiles: RAMSTKComboBox = RAMSTKComboBox(simple=False)
        self.tvwTreeView: RAMSTKTreeView = RAMSTKTreeView()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "default_title",
                    "index": 0,
                    "label_text": _("Default\nTitle"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "editable": False,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_title",
                    "index": 1,
                    "label_text": _("User\nTitle"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": "",
                    "field": "column_position",
                    "index": 2,
                    "label_text": _("Column\nPosition"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gint",
                    "default": "",
                    "field": "can_edit",
                    "index": 3,
                    "label_text": _("Can\nEdit?"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gint",
                    "default": "",
                    "field": "is_visible",
                    "index": 4,
                    "label_text": _("Is\nVisible?"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
        ]
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration()

        # Initialize public instance attributes.
        self.fmt_file: str = ""

        # Make a fixed type panel.
        super().do_set_widget_attributes()
        self._do_set_widget_properties()
        self._do_make_tree_panel()
        self._do_set_widget_callbacks()
        self._do_load_format_files()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "request_load_preferences": self._do_load_panel,
            }
        )

    def _do_load_format_files(self) -> None:
        """Load the format files RAMSTKComboBox with its entries."""
        self.cmbFormatFiles.do_load_combo(
            [
                [
                    _("Allocation"),
                    "allocation",
                ],
                [
                    _("Failure Definition"),
                    "failure_definition",
                ],
                [
                    _("(D)FME(C)A"),
                    "fmea",
                ],
                [
                    _("Function"),
                    "function",
                ],
                [
                    _("Hardware"),
                    "hardware",
                ],
                [
                    _("Hazards Analysis"),
                    "hazard",
                ],
                [
                    _("Physics of Failure Analysis"),
                    "pof",
                ],
                [
                    _("Requirements"),
                    "requirement",
                ],
                [
                    _("Revisions"),
                    "revision",
                ],
                [
                    _("Similar Item Analysis"),
                    "similar_item",
                ],
                [
                    _("Stakeholder Inputs"),
                    "stakeholder",
                ],
                [
                    _("Usage Profile"),
                    "usage_profile",
                ],
                [
                    _("Validation"),
                    "validation",
                ],
            ],
            simple=False,
        )

    def _do_load_format(self, module: str) -> None:
        """Load the selected Module View format file for editing.

        :param module: the name of the RAMSTK work stream module whose Module View
            layout is to be edited.
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
        """Load the current preference values."""
        self._configuration = configuration

    def _do_make_tree_panel(self) -> None:
        """Build the UI for the Preferences assistant."""
        super().do_make_tree_panel()

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

    def _do_set_widget_callbacks(self) -> None:
        """Set the RAMSTKTreeView widget callbacks."""
        super().do_set_widget_callbacks()

        self.cmbFormatFiles.dic_handler_id["changed"] = self.cmbFormatFiles.connect(
            "changed", self._on_combo_changed
        )

    def _do_set_widget_properties(self) -> None:
        """Set the RAMSTKTreeView widget properties."""
        super().do_set_widget_properties()

        self.cmbFormatFiles.do_set_properties(
            {"tooltip": _("Select the Tree View layout to edit.")}
        )
        self.tvwTreeView.do_set_properties(
            {
                "can_focus": True,
                "editable": True,
                "height_request": 300,
                "sensitive": True,
                "tooltip": _("Edit the RAMSTK Module View layout."),
                "visible": True,
                "width_request": 600,
            }
        )

    def _on_combo_changed(self, combo: RAMSTKComboBox) -> None:
        """Edit RAMSTKTreeView layouts.

        :param combo: the RAMSTKComboBox that called this method.
        """
        combo.handler_block(combo.dic_handler_id["changed"])

        _model = combo.get_model()
        _row = combo.get_active_iter()
        _module = _model.get_value(_row, 1)
        self._do_load_format(_module)

        combo.handler_unblock(combo.dic_handler_id["changed"])
