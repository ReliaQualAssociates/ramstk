# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.general_data_panel.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RequirementGeneralDataPanel module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton,
    RAMSTKCheckButton,
    RAMSTKComboBox,
    RAMSTKDateSelectDialog,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    WidgetConfig,
    make_widget_config,
)


class RequirementGeneralDataPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Requirement."""

    # Define private class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("General Requirement Information")

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

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.txtCode,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "requirement_code",
                    "index": 9,
                    "label_text": _("Requirement Code:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "width_request": 125,
                    "tooltip": _("A unique code for the selected requirement."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtName,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 3,
                    "label_text": _("Requirement Description:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 100,
                    "width_request": 800,
                    "tooltip": _("The description of the selected requirement."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbRequirementType,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "requirement_type",
                    "index": 11,
                    "label_text": _("Requirement Type:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "tooltip": _("The type of requirement."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkDerived,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "derived",
                    "index": 2,
                    "label_text": "",
                    "listen_topic": "mvw_editing_requirement",
                    "send_topic": "mvw_editing_requirement",
                },
                {
                    "editable": True,
                    "width_request": 400,
                    "tooltip": _(
                        "Indicates whether or not the selected requirement is derived."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtSpecification,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "specification",
                    "index": 10,
                    "label_text": _("Specification:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The governing specification, if any, for the requirement."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtSpecification,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "page_number",
                    "index": 6,
                    "label_text": _("Page Number:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The applicable page number in the governing specification."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtFigNum,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "figure_number",
                    "index": 4,
                    "label_text": _("Figure Number:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The applicable figure number in the governing specification."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbPriority,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "priority",
                    "index": 8,
                    "label_text": _("Priority:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "width_request": 50,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbOwner,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "owner",
                    "index": 5,
                    "label_text": _("Owner:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "tooltip": _("The organization responsible for the requirement."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkValidated,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "validated",
                    "index": 12,
                    "label_text": "",
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "width_request": 400,
                    "tooltip": _(
                        "Indicates whether or not the selected requirement is "
                        "validated."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtValidatedDate,
                {
                    "datatype": "gchararray",
                    "default": date.today(),
                    "field": "validated_date",
                    "index": 13,
                    "label_text": _("Validated Date:"),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "tooltip": _("The date the selected requirement was validated."),
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

        self.btnValidateDate.do_set_properties(
            {
                "height_request": 25,
                "width_request": 25,
            }
        )
        self.btnValidateDate.dic_handler_id["released"] = self.btnValidateDate.connect(
            "button-release-event",
            self._do_select_date,
            self.txtValidatedDate,
        )

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "succeed_create_requirement_code": self._do_load_code,
            }
        )

    def do_load_priorities(self) -> None:
        """Load the priority RAMSTKComboBox."""
        _priorities: List[List[str]] = [["1"], ["2"], ["3"], ["4"], ["5"]]
        self.cmbPriority.do_load_combo(_priorities)

    def do_load_requirement_types(
        self, requirement_types: Dict[int, Tuple[str]]
    ) -> None:
        """Load the requirement types RAMSTKComboBox.

        :param requirement_types:
        """
        _requirement_types: List[Tuple[str]] = list(requirement_types.values())

        self.cmbRequirementType.do_load_combo(entries=_requirement_types, simple=False)

    def do_load_workgroups(self, workgroups: Dict[int, Tuple[str]]) -> None:
        """Load the workgroups RAMSTKComboBox.

        :param workgroups:
        """
        _owners = list(workgroups.values())

        self.cmbOwner.do_load_combo(_owners)

    def _do_load_code(self, requirement_code: int) -> None:
        """Load the Requirement code RAMSTKEntry.

        :param requirement_code: the Requirement code to load.
        """
        self.txtCode.do_update({"requirement_code": str(requirement_code)})

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

        _dialog: RAMSTKDateSelectDialog = RAMSTKDateSelectDialog(
            _("Select Date"),
            _parent,
        )

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.do_update(_date)
        super().on_changed_entry(entry, "validated_date", "wvw_editing_requirement")

        return _date
