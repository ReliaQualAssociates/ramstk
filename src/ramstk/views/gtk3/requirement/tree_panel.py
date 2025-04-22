# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.tree_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Requirements tree panel module."""

# Standard Library Imports
from typing import Dict, List, Tuple, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererText,
    RAMSTKCellRendererToggle,
    RAMSTKTreePanel,
    WidgetConfig,
    make_widget_config,
)


class RequirementTreePanel(RAMSTKTreePanel):
    """Panel to display the hierarchy of requirements."""

    # Define private class attributes.
    _select_msg = "succeed_retrieve_all_requirement"
    _tag = "requirement"
    _title = _("Requirement Tree")

    def __init__(self) -> None:
        """Initialize an instance of the RequirementTreePanel widget."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "field": "requirement_id",
                    "index": 1,
                    "label_text": _("Requirement ID"),
                    "listen_topic": "wvw_editing_requirement",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "derived",
                    "index": 2,
                    "label_text": _("Derived?"),
                    "listen_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 3,
                    "label_text": _("Description"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "field": "figure_number",
                    "index": 4,
                    "label_text": _("Figure Number"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "field": "owner",
                    "index": 5,
                    "label_text": _("Owner"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "field": "page_number",
                    "index": 6,
                    "label_text": _("Page Number"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "default": 0,
                    "field": "parent_id",
                    "index": 7,
                    "label_text": _("Parent ID"),
                    "listen_topic": "wvw_editing_requirement",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "priority",
                    "index": 8,
                    "label_text": _("Priority"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "default": 0,
                    "field": "requirement_code",
                    "index": 9,
                    "label_text": _("Code"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "field": "specification",
                    "index": 10,
                    "label_text": _("Specification"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "field": "requirement_type",
                    "index": 11,
                    "label_text": _("Type"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "default": 0,
                    "field": "validated",
                    "index": 12,
                    "label_text": _("Validated?"),
                    "listen_topic": "wvw_editing_requirement",
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
                    "field": "validated_date",
                    "index": 13,
                    "label_text": _("Validated Date"),
                    "listen_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
        ]

        # Initialize public instance attributes.
        self.lst_owner: List[str] = [""]
        self.lst_type: List[str] = [""]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_tree_panel()
        super().do_set_widget_callbacks()

        # FIXME: Is this line necessary?
        self.tvwTreeView.dic_row_loader = {
            "requirement": self.__do_load_requirement,
        }
        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of requirements.")
        )

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_module_switch(self, module: str = "") -> None:
        """Respond to change in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        """
        # FIXME: This method needs to use something other than the position dict of
        #  the RAMSTKTreeView class to get the column numbers.
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(
                _row, self.tvwTreeView.position["requirement_code"]
            )
            _name = _model.get_value(_row, self.tvwTreeView.position["description"])
            _title = _(f"Analyzing Requirement {_code}: {_name}")
            super().do_set_title(_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Requirement ModuleView RAMSTKTreeView.

        This method is called whenever a Requirement Module View RAMSTKTreeView row is
        activated/changed.

        :param selection: the Requirement class Gtk.TreeSelection().
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            # FIXME: Can we move setting the record ID and parent ID to the super class?
            self._record_id = _attributes["requirement_id"]
            self._parent_id = _attributes["parent_id"]
            _attributes["owner"] = self.lst_owner.index(_attributes["owner"])
            _attributes["requirement_type"] = self.lst_type.index(
                _attributes["requirement_type"]
            )

            _title = _(
                f"Analyzing Requirement {str(_attributes["requirement_code"])}: "
                f"{str(_attributes["description"])}"
            )

            super().do_set_title(_title)

    # ----- -- RequirementTreePanel specific methods. --- ----- #
    def do_load_owners(self, owners: Dict[int, Tuple[str]]) -> None:
        """Load the owners list.

        :param owners: the dict with the owners to load.
        """
        for _owner in owners:
            self.lst_owner.append(owners[_owner][0])

        self.tvwTreeView.do_load_cellrenderercombo("owner", self.lst_owner)

    def do_load_priorities(self) -> None:
        """Load the requirement priorities list."""
        self.tvwTreeView.do_load_cellrenderercombo(
            "priority", ["", "1", "2", "3", "4", "5"]
        )

    def do_load_types(self, types: Dict[int, Tuple[str, str]]) -> None:
        """Load the requirement types list.

        :param types: the dict with the requirement types to load.
        """
        for _type in types:
            self.lst_type.append(types[_type][1])

        self.tvwTreeView.do_load_cellrenderercombo("requirement_type", self.lst_type)

    def _on_workview_edit(
        self, node_id: int, package: Dict[str, Union[bool, float, int, str]]
    ) -> None:
        """Update the module view RAMSTKTreeView with attribute changes.

        This is a wrapper for the metaclass method do_refresh_tree.  It is necessary to
        handle RAMSTKComboBox changes because the package value will be an integer and
        the RAMSTKCellRendererCombo needs a string input to update.

        :param node_id: the ID of the requirement being edited.
        :param package: the key:value for the data being updated.
        """
        for _key, _value in package.items():
            _column = self.tvwTreeView.get_column(self.tvwTreeView.position[_key])
            _cell = _column.get_cells()[-1]

            if isinstance(_cell, Gtk.CellRendererCombo) and isinstance(_value, int):
                if _key == "owner":
                    package[_key] = str(self.lst_owner[_value])
                elif _key == "priority":
                    package[_key] = str(package[_key])
                elif _key == "requirement_type":
                    package[_key] = str(self.lst_type[_value])

            super().do_refresh_tree(node_id, package)

    def __do_load_requirement(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a requirement into the RAMSTKTreeView.

        :param node: the treelib Node with the mode data to load.
        :param row: the parent row of the mode to load into the requirement
            tree.
        :return: _new_row; the row that was just populated with requirement
            data.
        :rtype: :class:`Gtk.TreeIter`
        """
        # FIXME: This method needs to accept a treelib.Tree object with all the
        #  requirements and then pass that tree to the treeview method do_load_tree.
        #  This method should handle all exceptions and return None.
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _attributes = [
            _entity.revision_id,
            _entity.requirement_id,
            _entity.derived,
            _entity.description,
            _entity.figure_number,
            self.lst_owner[_entity.owner],
            _entity.page_number,
            _entity.parent_id,
            _entity.priority,
            _entity.requirement_code,
            _entity.specification,
            self.lst_type[_entity.requirement_type],
            _entity.validated,
            str(_entity.validated_date),
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading requirement {0} in the "
                "requirement tree.  This might indicate it was missing it's "
                "data package, some of the data in the package was missing, "
                "or some of the data was the wrong type.  Row data was: "
                "{1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row
