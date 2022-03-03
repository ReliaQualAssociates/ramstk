# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Requirement Panels."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton,
    RAMSTKCheckButton,
    RAMSTKComboBox,
    RAMSTKDateSelect,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    RAMSTKTreePanel,
)


class RequirementTreePanel(RAMSTKTreePanel):
    """Panel to display hierarchy of requirements."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_all_requirement"
    _tag = "requirement"
    _title = _("Requirement Tree")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Requirement panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self.tvwTreeView.dic_row_loader = {
            "requirement": self.__do_load_requirement,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.

        # Initialize public dictionary class attributes.
        self.dic_attribute_widget_map = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_requirement",
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
            "requirement_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Requirement ID"),
                "gint",
            ],
            "derived": [
                2,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Derived?"),
                "gint",
            ],
            "description": [
                3,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_requirement",
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
            "figure_number": [
                4,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_requirement",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Figure Number"),
                "gchararray",
            ],
            "owner": [
                5,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                "mvw_editing_requirement",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Owner"),
                "gchararray",
            ],
            "page_number": [
                6,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_requirement",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Page Number"),
                "gchararray",
            ],
            "parent_id": [
                7,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Parent ID"),
                "gint",
            ],
            "priority": [
                8,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Priority"),
                "gint",
            ],
            "requirement_code": [
                9,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_requirement",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Code"),
                "gchararray",
            ],
            "specification": [
                10,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_requirement",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Specification"),
                "gchararray",
            ],
            "requirement_type": [
                11,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Type"),
                "gchararray",
            ],
            "validated": [
                12,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Validated?"),
                "gint",
            ],
            "validated_date": [
                13,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_requirement",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Validated Date"),
                "gchararray",
            ],
            "q_clarity_0": [
                14,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q1"),
                "gint",
            ],
            "q_clarity_1": [
                15,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q2"),
                "gint",
            ],
            "q_clarity_2": [
                16,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q3"),
                "gint",
            ],
            "q_clarity_3": [
                17,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q4"),
                "gint",
            ],
            "q_clarity_4": [
                18,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q5"),
                "gint",
            ],
            "q_clarity_5": [
                19,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q6"),
                "gint",
            ],
            "q_clarity_6": [
                20,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q7"),
                "gint",
            ],
            "q_clarity_7": [
                21,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q8"),
                "gint",
            ],
            "q_clarity_8": [
                22,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Clarity Q9"),
                "gint",
            ],
            "q_complete_0": [
                23,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q1"),
                "gint",
            ],
            "q_complete_1": [
                24,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q2"),
                "gint",
            ],
            "q_complete_2": [
                25,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q3"),
                "gint",
            ],
            "q_complete_3": [
                26,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q4"),
                "gint",
            ],
            "q_complete_4": [
                27,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q5"),
                "gint",
            ],
            "q_complete_5": [
                28,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q6"),
                "gint",
            ],
            "q_complete_6": [
                29,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q7"),
                "gint",
            ],
            "q_complete_7": [
                30,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q8"),
                "gint",
            ],
            "q_complete_8": [
                31,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q9"),
                "gint",
            ],
            "q_complete_9": [
                32,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Complete Q10"),
                "gint",
            ],
            "q_consistent_0": [
                33,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q1"),
                "gint",
            ],
            "q_consistent_1": [
                34,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q2"),
                "gint",
            ],
            "q_consistent_2": [
                35,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q3"),
                "gint",
            ],
            "q_consistent_3": [
                36,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q4"),
                "gint",
            ],
            "q_consistent_4": [
                37,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q5"),
                "gint",
            ],
            "q_consistent_5": [
                38,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q6"),
                "gint",
            ],
            "q_consistent_6": [
                39,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q7"),
                "gint",
            ],
            "q_consistent_7": [
                40,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q8"),
                "gint",
            ],
            "q_consistent_8": [
                41,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Consistent Q9"),
                "gint",
            ],
            "q_verifiable_0": [
                42,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Verifiable Q1"),
                "gint",
            ],
            "q_verifiable_1": [
                43,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Verifiable Q2"),
                "gint",
            ],
            "q_verifiable_2": [
                44,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Verifiable Q3"),
                "gint",
            ],
            "q_verifiable_3": [
                45,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Verifiable Q4"),
                "gint",
            ],
            "q_verifiable_4": [
                46,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Verifiable Q5"),
                "gint",
            ],
            "q_verifiable_5": [
                47,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_requirement",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Verifiable Q6"),
                "gint",
            ],
        }

        # Initialize public list class attributes.
        self.lst_owner: List[str] = [""]
        self.lst_type: List[str] = [""]

        # Initialize public scalar class attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of requirements.")
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._on_module_switch,
            "mvwSwitchedPage",
        )
        pub.subscribe(
            self._on_workview_edit,
            f"wvw_editing_{self._tag}",
        )

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to change in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(
                _row, self.tvwTreeView.position["requirement_code"]
            )
            _name = _model.get_value(_row, self.tvwTreeView.position["description"])
            _title = _(f"Analyzing Requirement {_code}: {_name}")

            pub.sendMessage("request_set_title", title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Requirement ModuleView RAMSTKTreeView().

        This method is called whenever a Requirement Module View
        RAMSTKTreeView() row is activated/changed.

        :param selection: the Requirement class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["requirement_id"]
            self._parent_id = _attributes["parent_id"]
            _attributes["owner"] = self.lst_owner.index(_attributes["owner"])
            _attributes["requirement_type"] = self.lst_type.index(
                _attributes["requirement_type"]
            )

            _title = _("Analyzing Requirement {0:s}: {1:s}").format(
                str(_attributes["requirement_code"]),
                str(_attributes["description"]),
            )

            pub.sendMessage("selected_requirement", attributes=_attributes)
            pub.sendMessage("request_set_title", title=_title)

    def _on_workview_edit(self, node_id: int, package: Dict[str, Any]) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

        This is a wrapper for the metaclass method do_refresh_tree().  It is
        necessary to handle RAMSTKComboBox() changes because the package value will
        be an integer and the Gtk.CellRendererCombo() needs a string input to update.

        :param node_id: the ID of the requirement being edited.
        :param package: the key:value for the data being updated.
        :return: None
        """
        [[_key, _value]] = package.items()

        _column = self.tvwTreeView.get_column(self.tvwTreeView.position[_key])
        _cell = _column.get_cells()[-1]

        if isinstance(_cell, Gtk.CellRendererCombo):
            if _key == "owner":
                package[_key] = self.lst_owner[_value]
            elif _key == "priority":
                package[_key] = str(package[_key])
            elif _key == "requirement_type":
                package[_key] = self.lst_type[_value]

            super().do_refresh_tree(node_id, package)

    def __do_load_requirement(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a requirement into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the requirement
            tree.
        :return: _new_row; the row that was just populated with requirement
            data.
        :rtype: :class:`Gtk.TreeIter`
        """
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
            _entity.q_clarity_0,
            _entity.q_clarity_1,
            _entity.q_clarity_2,
            _entity.q_clarity_3,
            _entity.q_clarity_4,
            _entity.q_clarity_5,
            _entity.q_clarity_6,
            _entity.q_clarity_7,
            _entity.q_clarity_8,
            _entity.q_complete_0,
            _entity.q_complete_1,
            _entity.q_complete_2,
            _entity.q_complete_3,
            _entity.q_complete_4,
            _entity.q_complete_5,
            _entity.q_complete_6,
            _entity.q_complete_7,
            _entity.q_complete_8,
            _entity.q_complete_9,
            _entity.q_consistent_0,
            _entity.q_consistent_1,
            _entity.q_consistent_2,
            _entity.q_consistent_3,
            _entity.q_consistent_4,
            _entity.q_consistent_5,
            _entity.q_consistent_6,
            _entity.q_consistent_7,
            _entity.q_consistent_8,
            _entity.q_verifiable_0,
            _entity.q_verifiable_1,
            _entity.q_verifiable_2,
            _entity.q_verifiable_3,
            _entity.q_verifiable_4,
            _entity.q_verifiable_5,
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


class RequirementGeneralDataPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Requirement."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("General Requirement Information")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Requirement General Data panel."""
        super().__init__()

        # Initialize widgets.
        self.btnValidateDate: RAMSTKButton = RAMSTKButton()

        self.chkDerived: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirement is derived.")
        )
        self.chkValidated: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirement is validated.")
        )

        self.cmbOwner: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbRequirementType: RAMSTKComboBox = RAMSTKComboBox(index=1, simple=False)
        self.cmbPriority: RAMSTKComboBox = RAMSTKComboBox()

        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtFigNum: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtPageNum: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()
        self.txtValidatedDate: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "requirement_code": [
                9,
                self.txtCode,
                "changed",
                super().on_changed_entry,
                "wvw_editing_requirement",
                "",
                {
                    "width": 125,
                    "tooltip": _("A unique code for the selected requirement."),
                },
                _("Requirement Code:"),
                "gchararray",
            ],
            "description": [
                3,
                self.txtName,
                "changed",
                super().on_changed_textview,
                "wvw_editing_requirement",
                "",
                {
                    "height": 100,
                    "width": 800,
                    "tooltip": _("The description of the selected requirement."),
                },
                _("Requirement Description:"),
                "gchararray",
            ],
            "requirement_type": [
                11,
                self.cmbRequirementType,
                "changed",
                super().on_changed_combo,
                "wvw_editing_requirement",
                0,
                {
                    "tooltip": _("The type of requirement."),
                },
                _("Requirement Type:"),
                "gint",
            ],
            "derived": [
                2,
                self.chkDerived,
                "toggled",
                super().on_toggled,
                "mvw_editing_requirement",
                0,
                {
                    "tooltip": _(
                        "Indicates whether or not the selected requirement is derived."
                    ),
                    "width": 400,
                },
                "",
                "gint",
            ],
            "specification": [
                10,
                self.txtSpecification,
                "changed",
                super().on_changed_entry,
                "wvw_editing_requirement",
                "",
                {
                    "tooltip": _(
                        "The governing specification, if any, for the requirement."
                    )
                },
                _("Specification:"),
                "gchararray",
            ],
            "page_number": [
                6,
                self.txtSpecification,
                "changed",
                super().on_changed_entry,
                "wvw_editing_requirement",
                "",
                {
                    "tooltip": _(
                        "The applicable page number in the governing specification."
                    )
                },
                _("Page Number:"),
                "gchararray",
            ],
            "figure_number": [
                4,
                self.txtFigNum,
                "changed",
                super().on_changed_entry,
                "wvw_editing_requirement",
                "",
                {
                    "toolip": _(
                        "The applicable figure number in the governing specification."
                    )
                },
                _("Figure Number:"),
                "gchararray",
            ],
            "priority": [
                8,
                self.cmbPriority,
                "changed",
                super().on_changed_combo,
                "wvw_editing_requirement",
                0,
                {
                    "width": 50,
                },
                _("Priority:"),
                "gint",
            ],
            "owner": [
                5,
                self.cmbOwner,
                "changed",
                super().on_changed_combo,
                "wvw_editing_requirement",
                0,
                {
                    "tooltip": _("The organization responsible for the requirement."),
                },
                _("Owner:"),
                "gint",
            ],
            "validated": [
                12,
                self.chkValidated,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "tooltip": _(
                        "Indicates whether or not the selected requirement is "
                        "validated."
                    ),
                    "width": 400,
                },
                "",
                "gint",
            ],
            "validated_date": [
                13,
                self.txtValidatedDate,
                "changed",
                super().on_changed_entry,
                "wvw_editing_requirement",
                date.today(),
                {
                    "tooltip": _("The date the selected requirement was validated."),
                },
                _("Validated Date:"),
                "gchararray",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.btnValidateDate.do_set_properties(
            height=25,
            width=25,
        )
        self.btnValidateDate.dic_handler_id["released"] = self.btnValidateDate.connect(
            "button-release-event",
            self._do_select_date,
            self.txtValidatedDate,
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_code, "succeed_create_requirement_code")

    def do_load_priorities(self) -> None:
        """Load the priority RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _priorities: List[List[str]] = [["1"], ["2"], ["3"], ["4"], ["5"]]
        self.cmbPriority.do_load_combo(_priorities)

    def do_load_requirement_types(
        self, requirement_types: Dict[int, Tuple[str]]
    ) -> None:
        """Load the requirement types RAMSTKComboBox().

        :param requirement_types:
        :return: None
        :rtype: None
        """
        _requirement_types: List[Tuple[str]] = list(requirement_types.values())

        self.cmbRequirementType.do_load_combo(entries=_requirement_types, simple=False)

    def do_load_workgroups(self, workgroups: Dict[int, Tuple[str]]) -> None:
        """Load the workgroups RAMSTKComboBox().

        :param workgroups:
        :return: None
        :rtype: None
        """
        _owners = list(workgroups.values())

        self.cmbOwner.do_load_combo(_owners)

    def _do_load_code(self, requirement_code: int) -> None:
        """Load the Requirement code RAMSTKEntry().

        :param requirement_code: the Requirement code to load.
        :return: None
        :rtype: None
        """
        self.txtCode.do_update(str(requirement_code), signal="changed")

    @staticmethod
    def _do_select_date(
        __button: RAMSTKButton, __event: Gdk.Event, entry: RAMSTKEntry
    ) -> str:
        """Request to launch a date selection dialog.

        This method is used to select the validation date for the Requirement.

        :param __button: the ramstk.RAMSTKButton() that called this method.
        :param __event: the Gdk.Event() that called this method.
        :param entry: the Gtk.Entry() that the new date should be displayed in.
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _parent = (
            entry.get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
        )

        _dialog: RAMSTKDateSelect = RAMSTKDateSelect(dlgparent=_parent)

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.do_update(_date)
        super().on_changed_entry(entry, "validated_date", "wvw_editing_requirement")

        return _date


class RequirementClarityPanel(RAMSTKFixedPanel):
    """Panel to display clarity questions about the selected Requirement."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("Clarity of Requirement")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Requirement clarity panel."""
        super().__init__()

        # Initialize widgets.
        self.chkClarityQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ8: RAMSTKCheckButton = RAMSTKCheckButton()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "q_clarity_0": [
                14,
                self.chkClarityQ0,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("1. The requirement clearly states what is needed or desired."),
                "gint",
            ],
            "q_clarity_1": [
                15,
                self.chkClarityQ1,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("2. The requirement is unambiguous and not open to interpretation."),
                "gint",
            ],
            "q_clarity_2": [
                16,
                self.chkClarityQ2,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "3. All terms that can have more than one meaning are qualified so "
                    "that the desired meaning is readily apparent."
                ),
                "gint",
            ],
            "q_clarity_3": [
                17,
                self.chkClarityQ3,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "4. Diagrams, drawings, etc. are used to increase understanding of "
                    "the requirement."
                ),
                "gint",
            ],
            "q_clarity_4": [
                18,
                self.chkClarityQ4,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("5. The requirement is free from spelling and grammatical errors."),
                "gint",
            ],
            "q_clarity_5": [
                19,
                self.chkClarityQ5,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "6. The requirement is written in non-technical language using the "
                    "vocabulary of the stakeholder."
                ),
                "gint",
            ],
            "q_clarity_6": [
                20,
                self.chkClarityQ6,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("7. Stakeholders understand the requirement as written."),
                "gint",
            ],
            "q_clarity_7": [
                21,
                self.chkClarityQ7,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "8. The requirement is clear enough to be turned over to an "
                    "independent group and still be understood."
                ),
                "gint",
            ],
            "q_clarity_8": [
                22,
                self.chkClarityQ8,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "9. The requirement avoids stating how the problem is "
                    "to be solved or what techniques are to be used."
                ),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel(justify=Gtk.Justification.LEFT)
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.


class RequirementCompletenessPanel(RAMSTKFixedPanel):
    """Panel to display completeness questions about selected Requirement."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("Completeness of Requirement")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Requirement completeness panel."""
        super().__init__()

        # Initialize widgets.
        self.chkCompleteQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ8: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ9: RAMSTKCheckButton = RAMSTKCheckButton()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "q_complete_0": [
                23,
                self.chkCompleteQ0,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "1. Performance objectives are properly documented from the "
                    "user's point of view."
                ),
                "gint",
            ],
            "q_complete_1": [
                24,
                self.chkCompleteQ1,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("2. No necessary information is missing from the requirement."),
                "gint",
            ],
            "q_complete_2": [
                25,
                self.chkCompleteQ2,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("3. The requirement has been assigned a priority."),
                "gint",
            ],
            "q_complete_3": [
                26,
                self.chkCompleteQ3,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "4. The requirement is realistic given the technology that will "
                    "be used to implement the system."
                ),
                "gint",
            ],
            "q_complete_4": [
                27,
                self.chkCompleteQ4,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "5. The requirement is feasible to implement given the defined "
                    "project time frame, scope, structure and budget."
                ),
                "gint",
            ],
            "q_complete_5": [
                28,
                self.chkCompleteQ5,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "6. If the requirement describes something as a 'standard' the "
                    "specific source is cited."
                ),
                "gint",
            ],
            "q_complete_6": [
                29,
                self.chkCompleteQ6,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("7. The requirement is relevant to the problem and its solution."),
                "gint",
            ],
            "q_complete_7": [
                30,
                self.chkCompleteQ7,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("8. The requirement contains no implied design details."),
                "gint",
            ],
            "q_complete_8": [
                31,
                self.chkCompleteQ8,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "9. The requirement contains no implied implementation "
                    "constraints."
                ),
                "gint",
            ],
            "q_complete_9": [
                32,
                self.chkCompleteQ9,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "10. The requirement contains no implied project management "
                    "constraints."
                ),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel(justify=Gtk.Justification.LEFT)
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.


class RequirementConsistencyPanel(RAMSTKFixedPanel):
    """Panel to display consistency questions about selected Requirement."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("Consistency of Requirement")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Requirement consistency panel."""
        super().__init__()

        # Initialize widgets.
        self.chkConsistentQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ8: RAMSTKCheckButton = RAMSTKCheckButton()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "q_consistent_0": [
                33,
                self.chkConsistentQ0,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "1. The requirement describes a single need or want; it could not "
                    "be broken into several different requirements."
                ),
                "gint",
            ],
            "q_consistent_1": [
                34,
                self.chkConsistentQ1,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "2. The requirement requires non-standard hardware or must use "
                    "software to implement."
                ),
                "gint",
            ],
            "q_consistent_2": [
                35,
                self.chkConsistentQ2,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("3. The requirement can be implemented within known constraints."),
                "gint",
            ],
            "q_consistent_3": [
                36,
                self.chkConsistentQ3,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "4. The requirement provides an adequate basis for design and "
                    "testing."
                ),
                "gint",
            ],
            "q_consistent_4": [
                37,
                self.chkConsistentQ4,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "5. The requirement adequately supports the business goal of the "
                    "project."
                ),
                "gint",
            ],
            "q_consistent_5": [
                38,
                self.chkConsistentQ5,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "6. The requirement does not conflict with some constraint, policy "
                    "or regulation."
                ),
                "gint",
            ],
            "q_consistent_6": [
                39,
                self.chkConsistentQ6,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("7. The requirement does not conflict with another requirement."),
                "gint",
            ],
            "q_consistent_7": [
                40,
                self.chkConsistentQ7,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("8. The requirement is not a duplicate of another requirement."),
                "gint",
            ],
            "q_consistent_8": [
                41,
                self.chkConsistentQ8,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _("9. The requirement is in scope for the project."),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel(justify=Gtk.Justification.LEFT)
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.


class RequirementVerifiabilityPanel(RAMSTKFixedPanel):
    """Panel to display verifiability questions about selected Requirement."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("Verifiability of Requirement")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Requirement verifiability panel."""
        super().__init__()

        # Initialize widgets.
        self.chkVerifiableQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ5: RAMSTKCheckButton = RAMSTKCheckButton()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "q_verifiable_0": [
                42,
                self.chkVerifiableQ0,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "1. The requirement is verifiable by testing, demonstration, "
                    "review, or analysis."
                ),
                "gint",
            ],
            "q_verifiable_1": [
                43,
                self.chkVerifiableQ1,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "2. The requirement lacks 'weasel words' (e.g. various, mostly, "
                    "suitable, integrate, maybe, consistent, robust, modular, "
                    "user-friendly, superb, good)."
                ),
                "gint",
            ],
            "q_verifiable_2": [
                44,
                self.chkVerifiableQ2,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "3. Any performance criteria are quantified such that they are "
                    "testable."
                ),
                "gint",
            ],
            "q_verifiable_3": [
                45,
                self.chkVerifiableQ3,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "4. Independent testing would be able to determine whether the "
                    "requirement has been satisfied."
                ),
                "gint",
            ],
            "q_verifiable_4": [
                46,
                self.chkVerifiableQ4,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "5. The task(s) that will validate and verify the final design "
                    "satisfies the requirement have been identified."
                ),
                "gint",
            ],
            "q_verifiable_5": [
                47,
                self.chkVerifiableQ5,
                "toggled",
                super().on_toggled,
                "wvw_editing_requirement",
                0,
                {
                    "height": 30,
                },
                _(
                    "6. The identified V&amp;V task(s) have been added to the "
                    "validation plan (e.g., DVP)"
                ),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel(justify=Gtk.Justification.LEFT)
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
