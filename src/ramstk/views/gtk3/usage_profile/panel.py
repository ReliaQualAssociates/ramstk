# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.usage_profile.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Usage Profile tree panel module."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererText,
    RAMSTKTreePanel,
    WidgetConfig,
    make_widget_config,
)


class UsageProfileTreePanel(RAMSTKTreePanel):
    """Panel to display hierarchical list of usage profiles."""

    # Define private class attributes.
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
    _select_msg = "succeed_retrieve_usage_profile"
    _tag = "usage_profile"
    _title = _("Usage Profile")

    def __init__(self) -> None:
        """Initialize an instance of the usage profile panel."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_units: List[str] = []
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "mission_id",
                    "index": 1,
                    "label_text": _("Mission ID"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "mission_phase_id",
                    "index": 2,
                    "label_text": _("Phase ID"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "environment_id",
                    "index": 3,
                    "label_text": _("Environment ID"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "name",
                    "index": 4,
                    "label_text": _("Mission Phase Name"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 5,
                    "label_text": _("Description"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "mission_time",
                    "index": 6,
                    "label_text": _("Mission Time"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "units",
                    "index": 7,
                    "label_text": _("Units"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "phase_start",
                    "index": 8,
                    "label_text": _("Phase Start"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "phase_end",
                    "index": 9,
                    "label_text": _("Phase End"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "minimum",
                    "index": 10,
                    "label_text": _("Minimum"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "maximum",
                    "index": 11,
                    "label_text": _("Maximum"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "mean",
                    "index": 12,
                    "label_text": _("Mean"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "variance",
                    "index": 13,
                    "label_text": _("Variance"),
                    "send_topic": "wvw_editing_usage_profile",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
        ]
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        # Initialize public instance attributes.
        self.dic_icons: Dict[str, Any] = {
            "mission": None,
            "mission_phase": None,
            "environment": None,
        }
        self.dic_units: Dict[str, Tuple[str, str, str]] = {}
        self.level: str = ""

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_tree_panel()
        super().do_set_widget_callbacks()

        # FIXME: Is this line necessary?
        self.tvwTreeView.dic_row_loader = {
            "mission": self.__do_load_mission,
            "mission_phase": self.__do_load_phase,
            "environment": self.__do_load_environment,
        }
        self.tvwTreeView.set_tooltip_text(
            _("Displays the usage profiles for the selected revision.")
        )

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle row changes for the Usage Profile tree panel's RAMSTKTreeView.

        This method is called whenever a Usage Profile List View RAMSTKTreeView row is
        activated or changed.

        :param selection: the Usage Profile class Gtk.TreeSelection.
        """
        _attributes = super().on_row_change(selection)
        _model, _row = selection.get_selected()

        if _row is None:
            return

        self.do_get_usage_profile_level(_model, _row)
        super().do_set_visible_columns()
        self._record_id = _attributes[f"{self.level}_id"]

    # ----- ----- UsageProfileTreePanel specific methods. ----- ----- #
    def do_get_usage_profile_level(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter
    ) -> None:
        """Determine the Usage Profile level of the selected Usage Profile row.

        :param model: the Usage Profile Gtk.TreeModel().
        :param row: the selected Gtk.TreeIter() in the Usage Profile.
        """
        # FIXME: There needs to be a better way of doing this.  Even adding a column
        #  to the tree to contain "mission", "mission_phase", or "environment" would
        #  be better than this.
        _cid = ""

        for _col in [1, 2, 3]:
            _cid = f"{_cid}{int(bool(model.get_value(row, _col)))}"

        self.level = {
            "100": "mission",
            "110": "mission_phase",
            "111": "environment",
        }[_cid]

    def do_load_units(self, measurement_units: Dict[int, Tuple[str, str]]) -> None:
        """Load the units list.

        :param measurement_units: the dict containing the measurement units to load.
        """
        for _unit in measurement_units:
            self._lst_units.append(measurement_units[_unit][1])

        self.tvwTreeView.do_load_cellrenderercombo("units", self._lst_units)

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
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer() that was
            edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param key: the column key of the edited Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        """
        super().on_cell_edit(
            cell,
            path,
            new_text,
            key,
            f"wvw_editing_{self.level}",
        )

    def __do_load_environment(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load an environmental condition into the RAMSTK TreeView.

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        # FIXME: This method needs to accept a treelib.Tree object with all the
        #  requirements and then pass that tree to the treeview method do_load_tree.
        #  This method should handle all exceptions and return None.  Maybe this
        #  should be combined with the __do_load_mission and __do_load_phase methods.
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
            _new_row = self.tvwTreeView.unfiltered_model.append(row, _attributes)
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
        # FIXME: This method needs to accept a treelib.Tree object with all the
        #  requirements and then pass that tree to the treeview method do_load_tree.
        #  This method should handle all exceptions and return None.
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
            _new_row = self.tvwTreeView.unfiltered_model.append(row, _attributes)
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
        # FIXME: This method needs to accept a treelib.Tree object with all the
        #  requirements and then pass that tree to the treeview method do_load_tree.
        #  This method should handle all exceptions and return None.
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
            _new_row = self.tvwTreeView.unfiltered_model.append(row, _attributes)
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
