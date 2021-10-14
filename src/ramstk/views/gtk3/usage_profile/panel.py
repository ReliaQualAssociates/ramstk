# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.usage_profile.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Usage Profile Panels."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel


class UsageProfileTreePanel(RAMSTKTreePanel):
    """Panel to display hierarchical list of usage profiles."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_usage_profile"
    _tag = "usage_profile"
    _title = _("Usage Profile")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the usage profile panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self.tvwTreeView.dic_row_loader = {
            "mission": self.__do_load_mission,
            "mission_phase": self.__do_load_phase,
            "environment": self.__do_load_environment,
        }
        self._dic_visible_mask: Dict[str, Dict[str, bool]] = {
            "mission": {
                "revision_id": False,
                "mission_id": True,
                "phase_id": False,
                "environment_id": False,
                "name": False,
                "description": True,
                "mission_time": True,
                "units": True,
                "phase_start": False,
                "phase_end": False,
                "minimum": False,
                "maximum": False,
                "mean": False,
                "variance": False,
            },
            "phase": {
                "revision_id": False,
                "mission_id": False,
                "phase_id": True,
                "environment_id": False,
                "name": True,
                "description": True,
                "mission_time": False,
                "units": False,
                "phase_start": True,
                "phase_end": True,
                "minimum": False,
                "maximum": False,
                "mean": False,
                "variance": False,
            },
            "environment": {
                "revision_id": False,
                "mission_id": False,
                "phase_id": False,
                "environment_id": True,
                "name": True,
                "description": False,
                "mission_time": False,
                "units": True,
                "phase_start": False,
                "phase_end": False,
                "minimum": True,
                "maximum": True,
                "mean": True,
                "variance": True,
            },
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._on_edit_message: str = f"lvw_editing_{self._tag}"

        # Initialize public dictionary class attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Revision ID"),
                "gint",
            ],
            "mission_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Mission ID"),
                "gint",
            ],
            "phase_id": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Phase ID"),
                "gint",
            ],
            "environment_id": [
                3,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Environment ID"),
                "gint",
            ],
            "name": [
                4,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mission Phase Name"),
                "gchararray",
            ],
            "description": [
                5,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Description"),
                "gchararray",
            ],
            "mission_time": [
                6,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mission Time"),
                "gfloat",
            ],
            "units": [
                7,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Units"),
                "gchararray",
            ],
            "phase_start": [
                8,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Phase Start"),
                "gfloat",
            ],
            "phase_end": [
                9,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Phase End"),
                "gfloat",
            ],
            "minimum": [
                10,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Minimum"),
                "gfloat",
            ],
            "maximum": [
                11,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Maximum"),
                "gfloat",
            ],
            "mean": [
                12,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mean"),
                "gfloat",
            ],
            "variance": [
                13,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Variance"),
                "gfloat",
            ],
        }

        self.dic_icons: Dict[str, Any] = {
            "mission": None,
            "phase": None,
            "environment": None,
        }
        self.dic_units: Dict[str, Tuple[str, str, str]] = {}

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the usage profiles for the selected revision.")
        )

        # Subscribe to PyPubSub messages.

    def do_load_comboboxes(self) -> None:
        """Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self.tvwTreeView.position["units"])
        for __, _unit in self.dic_units.items():  # pylint: disable=unused-variable
            _model.append([_unit[1]])

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle row changes for the Usage Profile package List View.

        This method is called whenever a Usage Profile List View
        RAMSTKTreeView() row is activated or changed.

        :param selection: the Usage Profile class Gtk.TreeSelection().
        :return: None
        """
        _model, _row = selection.get_selected()

        if _row is not None:
            if _model.get_value(_row, 2) == 0:
                _level = "mission"
            elif _model.get_value(_row, 3) == 0:
                _level = "phase"
            else:
                _level = "environment"

            self.tvwTreeView.visible = self._dic_visible_mask[_level]
            self.tvwTreeView.do_set_visible_columns()

    def __do_load_environment(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load an environmental condition into the RAMSTK TreeView.

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _pixbuf = GdkPixbuf.Pixbuf()
        _icon = _pixbuf.new_from_file_at_size(self.dic_icons["environment"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.mission_id,
            _entity.phase_id,
            _entity.environment_id,
            _entity.name,
            "",
            0.0,
            _entity.units,
            0.0,
            0.0,
            _entity.minimum,
            _entity.maximum,
            _entity.mean,
            _entity.variance,
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading environment {0:s} in the "
                "usage profile.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_mission(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a mission into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # pylint: disable=unused-variable
        [[__, _entity]] = node.data.items()

        _model = self.tvwTreeView.get_model()

        _pixbuf = GdkPixbuf.Pixbuf()
        _icon = _pixbuf.new_from_file_at_size(self.dic_icons["mission"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.mission_id,
            0,
            0,
            "",
            _entity.description,
            _entity.mission_time,
            _entity.time_units,
            0.0,
            _entity.mission_time,
            0.0,
            0.0,
            0.0,
            0.0,
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading mission {0:s} in the usage "
                "profile.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_phase(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a mission phase into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _pixbuf = GdkPixbuf.Pixbuf()
        _icon = _pixbuf.new_from_file_at_size(self.dic_icons["phase"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.mission_id,
            _entity.phase_id,
            0,
            _entity.name,
            _entity.description,
            0.0,
            "",
            _entity.phase_start,
            _entity.phase_end,
            0.0,
            0.0,
            0.0,
            0.0,
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading mission phase {0:s} in the "
                "usage profile.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row
