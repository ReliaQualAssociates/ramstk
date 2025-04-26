# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.relay.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.constants.relay import (
    RELAY_APPLICATION_DICT,
    RELAY_CONSTRUCTION_DICT,
    RELAY_CONTACT_FORM_LIST,
    RELAY_CONTACT_RATING_LIST,
    RELAY_QUALITY_DICT,
    RELAY_TECHNOLOGY_LIST,
    RELAY_TYPE_DICT,
)
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class RelayDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Relay assessment input attribute data in the RAMSTK Work Book.

    The Relay assessment input view displays all the assessment inputs for the selected
    relay.  This includes, currently, inputs for MIL-HDBK-217FN2.  The attributes of a
    Relay assessment input view are:

    :ivar cmbType: select and display the type of relay.
    :ivar cmbLoadType: select and display the type of load the relay is switching.
    :ivar cmbContactForm: select and display the form of the relay contacts.
    :ivar cmbContactRating: select and display the rating of the relay contacts.
    :ivar cmbApplication: select and display the relay application.
    :ivar cmbConstruction: select and display the relay's method of construction.
    :ivar txtCycles: enter and display the number of relay cycles per hour.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Relay Design Inputs")

    def __init__(self) -> None:
        """Initialize an instance of the Relay assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactForm: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactRating: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbLoadType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtCycles: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.cmbQuality,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "quality_id",
                    "index": 32,
                    "label_text": _("Quality Level:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                {
                    "editable": True,
                    "tooltip": _("The quality level."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbType,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "type_id",
                    "index": 48,
                    "label_text": _("Type:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The relay type."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbLoadType,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "technology_id",
                    "index": 37,
                    "label_text": _("Load Type:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The type of load the relay is switching."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbContactForm,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "contact_form_id",
                    "index": 7,
                    "label_text": _("Contact Form:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The contact form of the relay."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbContactRating,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "contact_rating_id",
                    "index": 9,
                    "label_text": _("Contact Rating:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The rating of the relay contacts."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbApplication,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "application_id",
                    "index": 2,
                    "label_text": _("Application:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The type of relay application."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbConstruction,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "construction_id",
                    "index": 6,
                    "label_text": _("Construction:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The method of construction of the relay."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtCycles,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "n_cycles",
                    "index": 2,
                    "label_text": _("Number of Cycles/Hour:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The number of relay on/off cycles per hour."),
                    "visible": True,
                },
            ),
        ]
        self._hazard_rate_method_id: int = 0
        self._quality_id: int = 0

        # Initialize public instance attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        self._do_set_widget_callbacks()
        self._do_load_contact_form()
        self._do_load_contact_rating()
        self._do_load_technology()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.on_subcategory_change,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def on_subcategory_change(self, subcategory_id: int) -> None:
        """Load the relay RAMSTKComboBoxes with subcategory specific entries.

        :param subcategory_id: the subcategory ID of the selected relay.
        """
        self.subcategory_id = subcategory_id

        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
        )
        self.cmbType.do_load_combo(
            RELAY_TYPE_DICT.get(self.subcategory_id, [[""]]),
        )

        self._set_sensitive()

    def _do_load_application(self) -> None:
        """Load the relay application RAMSTKComboBox."""
        self.cmbApplication.do_load_combo(
            self._get_application_list(),
        )

    def _do_load_construction(self) -> None:
        """Load the relay construction RAMSTKComboBox."""
        self.cmbConstruction.do_load_combo(
            self._get_construction_list(),
        )

    def _do_load_contact_form(self) -> None:
        """Load the relay contact form RAMSTKComboBox."""
        self.cmbContactForm.do_load_combo(
            RELAY_CONTACT_FORM_LIST,
        )

    def _do_load_contact_rating(self) -> None:
        """Load the relay contact rating RAMSTKComboBox."""
        self.cmbContactRating.do_load_combo(
            RELAY_CONTACT_RATING_LIST,
        )

    def _do_load_technology(self) -> None:
        """Load the relay technology RAMSTKComboBox."""
        self.cmbLoadType.do_load_combo(
            RELAY_TECHNOLOGY_LIST,
        )

    def _do_set_widget_callbacks(self) -> None:
        """Set the RAMSTKComboBox() callbacks."""
        super().do_set_widget_callbacks()

        self.cmbContactRating.connect("changed", self._do_load_application)
        self.cmbApplication.connect("changed", self._do_load_construction)

    def _get_application_list(self) -> List[List[str]]:
        """Return the list of relay applications.

        :return: list of relay applications.
        :rtype: list
        """
        _contact_rating_id = int(self.cmbContactRating.get_active())
        return RELAY_APPLICATION_DICT.get(_contact_rating_id, [])

    def _get_construction_list(self) -> List[List[str]]:
        """Return the list of relay construction methods.

        :return: list of relay construction methods.
        :rtype: list
        """
        _application_id = int(self.cmbApplication.get_active())
        _contact_rating_id = int(self.cmbContactRating.get_active())
        return RELAY_CONSTRUCTION_DICT.get(_contact_rating_id, {}).get(
            _application_id, []
        )

    def _get_quality_list(self) -> List[List[str]]:
        """Return the list of relay qualities.

        :return: list of relay qualities.
        :rtype: list
        """
        _default_quality_list = [
            [_("Established Reliability")],
            ["MIL-SPEC"],
            [_("Lower")],
        ]
        return (
            _default_quality_list
            if self._hazard_rate_method_id == 1
            else RELAY_QUALITY_DICT.get(self.subcategory_id, [[""]])
        )

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self._set_sensitive()
        super().do_set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            {"quality_id": self._quality_id},
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected relay."""
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbApplication,
            self.cmbConstruction,
            self.cmbContactForm,
            self.cmbContactRating,
            self.cmbLoadType,
            self.cmbType,
            self.txtCycles,
        ]

        # Reset all widgets to be insensitive.
        super().do_set_widget_sensitivity(
            _all_widgets,
            False,
        )

        super().do_set_widget_sensitivity([self.cmbType])

        if self.subcategory_id == 1 and self._hazard_rate_method_id != 1:
            _additional_widgets = [
                self.cmbApplication,
                self.cmbConstruction,
                self.cmbContactForm,
                self.cmbContactRating,
                self.cmbLoadType,
                self.txtCycles,
            ]
            super().do_set_widget_sensitivity(_additional_widgets)

            self.cmbApplication.do_load_combo(
                self._get_application_list,
            )
            self.cmbConstruction.do_load_combo(
                self._get_construction_list,
            )
