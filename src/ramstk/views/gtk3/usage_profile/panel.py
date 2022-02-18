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
    _dic_visible_mask: Dict[str, List[bool]] = {
        "mission": [
            False,
            True,
            False,
            False,
            False,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
        "mission_phase": [
            False,
            False,
            True,
            False,
            True,
            True,
            False,
            False,
            True,
            True,
            False,
            False,
            False,
            False,
        ],
        "environment": [
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
        ],
    }

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

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

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
            "mission_phase_id": [
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
                self._on_cell_edit,
                "wvw_editing_usage_profile",
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
                self._on_cell_edit,
                "wvw_editing_usage_profile",
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
                "wvw_editing_mission",
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
                self._on_cell_edit,
                "wvw_editing_usage_profile",
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
                "wvw_editing_mission_phase",
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
                "wvw_editing_mission_phase",
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
                "wvw_editing_environment",
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
                "wvw_editing_environment",
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
                "wvw_editing_environment",
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
                "wvw_editing_environment",
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
            "mission_phase": None,
            "environment": None,
        }
        self.dic_units: Dict[str, Tuple[str, str, str]] = {}

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.
        self.level: str = ""

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the usage profiles for the selected revision.")
        )

        # Subscribe to PyPubSub messages.

    def do_get_usage_profile_level(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter
    ) -> None:
        """Determine the Usage Profile level of the selected Usage Profile row.

        :param model: the Usage Profile Gtk.TreeModel().
        :param row: the selected Gtk.TreeIter() in the Usage Profile.
        :return: None
        :rtype: None
        """
        _cid = ""

        for _col in [1, 2, 3]:
            _cid = f"{_cid}{int(bool(model.get_value(row, _col)))}"

        self.level = {
            "100": "mission",
            "110": "mission_phase",
            "111": "environment",
        }[_cid]

    def do_load_comboboxes(self) -> None:
        """Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self.tvwTreeView.position["units"])
        for (
            __,  # pylint: disable=unused-variable
            _unit,
        ) in self.dic_units.items():
            _model.append([_unit[1]])

    # noinspection PyUnusedLocal
    def _on_cell_edit(
        self,
        cell: Gtk.CellRenderer,
        path: str,
        new_text: str,
        key: str,
        message: str,  # pylint: disable=unused-argument
    ) -> None:
        """Handle edits of description column to ensure proper level is updated.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param key: the column key of the edited Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        """
        super().on_cell_edit(
            cell,
            path,
            new_text,
            key,
            f"wvw_editing_{self.level}",
        )

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle row changes for the Usage Profile package List View.

        This method is called whenever a Usage Profile List View
        RAMSTKTreeView() row is activated or changed.

        :param selection: the Usage Profile class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)
        _model, _row = selection.get_selected()

        if _row is None:
            return

        self.do_get_usage_profile_level(_model, _row)
        super().do_set_visible_columns(_attributes)
        self._record_id = _attributes[f"{self.level}_id"]

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

        _pixbuf = GdkPixbuf.Pixbuf()
        _icon = _pixbuf.new_from_file_at_size(self.dic_icons["environment"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.mission_id,
            _entity.mission_phase_id,
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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
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

        _pixbuf = GdkPixbuf.Pixbuf()
        _icon = _pixbuf.new_from_file_at_size(self.dic_icons["mission_phase"], 22, 22)

        _attributes = [
            _entity.revision_id,
            _entity.mission_id,
            _entity.mission_phase_id,
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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
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
