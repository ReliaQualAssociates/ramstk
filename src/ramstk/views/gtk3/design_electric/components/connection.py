# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.connection.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.constants.connection import (
    CONNECTION_INSERT_DICT,
    CONNECTION_QUALITY_DICT,
    CONNECTION_SPECIFICATION_DICT,
    CONNECTION_TYPE_DICT,
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


class ConnectionDesignElectricInputPanel(RAMSTKFixedPanel):
    """Displays connection assessment input attribute data.

    The Connection assessment input view displays all the assessment inputs for
    the selected connection.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analysis.  The attributes of a
    Connection assessment input view are:

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.

    :ivar _hazard_rate_method_id: the ID of the method to use for estimating
        the Hardware item's hazard rate.
    :ivar _title: the text to put on the RAMSTKFrame() holding the
        assessment input widgets.

    :ivar subcategory_id: the ID of the Hardware item's subcategory.
    :ivar cmbInsert: select and display the available insert materials for the
        connector.
    :ivar cmbSpecification: select and display the governing specification of
        the connection.
    :ivar cmbType: select and display the type of the connection.

    :ivar txtActivePins: enter and display the number of active pins in the
        connector.
    :ivar txtAmpsContact: enter and display the amps carried by the pins in the
        connector.
    :ivar txtContactGauge: enter and display the contact gauge of the
        connector.
    :ivar txtMating: enter and display the number of mate/demate cycles the
        connector undergoes per 1000 hours.
    :ivar txtNHand: enter and display the number of hand soldered PTH
        connections.
    :ivar txtNPlanes: enter and display the number of layers in the circuit
        board the PTH needs to penetrate.
    :ivar txtNWave: enter and display the number of wave soldered PTH
        connections.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Connection Design Inputs")

    def __init__(self) -> None:
        """Initialize an instance of the Connection assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbInsert: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtContactGauge: RAMSTKEntry = RAMSTKEntry()
        self.txtActivePins: RAMSTKEntry = RAMSTKEntry()
        self.txtAmpsContact: RAMSTKEntry = RAMSTKEntry()
        self.txtMating: RAMSTKEntry = RAMSTKEntry()
        self.txtNWave: RAMSTKEntry = RAMSTKEntry()
        self.txtNHand: RAMSTKEntry = RAMSTKEntry()
        self.txtNPlanes: RAMSTKEntry = RAMSTKEntry()

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
                    "tooltip": _("The quality level of the connector/connection."),
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
                    "label_text": _("Connector Type:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The type of connector/connection."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbSpecification,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "specification_id",
                    "index": 36,
                    "label_text": _("Specification:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The governing specification for the connection."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbInsert,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "insert_id",
                    "index": 18,
                    "label_text": _("Insert Material:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The connector insert material."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtContactGauge,
                {
                    "datatype": "gint",
                    "default": 22,
                    "field": "contact_gauge",
                    "index": 8,
                    "label_text": _("Contact Gauge:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The gauge of the contacts in the connector."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtActivePins,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "n_active_pins",
                    "index": 22,
                    "label_text": _("Active Pins:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The number of active pins in the connector."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtAmpsContact,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "current_operating",
                    "index": 10,
                    "label_text": _("Amperes/Contact:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The amperes per active contact."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtMating,
                {
                    "datatype": "gfloat",
                    "default": 0,
                    "field": "n_cycles",
                    "index": 24,
                    "label_text": _("Mating/Unmating Cycles (per 1000 hours):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The number of connector mate and unmate cycles per 1000 "
                        "hours of operation."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtNWave,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "n_wave_soldered",
                    "index": 27,
                    "label_text": _("Number of Wave Soldered PTH:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The number of wave soldered PTH connections."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtNHand,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "n_hand_soldered",
                    "index": 26,
                    "label_text": _("Number of Hand Soldered PTH:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The number of hand soldered PTH connections."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtNPlanes,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "n_circuit_planes",
                    "index": 23,
                    "label_text": _("Number of Circuit Planes:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The number of circuit planes for wave soldered connections."
                    ),
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

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.on_subcategory_change,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def on_subcategory_change(self, subcategory_id: int) -> None:
        """Load the connection RAMSTKComboBoxes with subcategory specific entries.

        :param subcategory_id: the subcategory ID of the selected connection.
        """
        self.subcategory_id = subcategory_id

        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
        )
        self.cmbType.do_load_combo(
            CONNECTION_TYPE_DICT.get(self.subcategory_id, [[""]]),
        )

        # Clear the remaining ComboBox()s.  These are loaded dynamically
        # based on the selection made in other ComboBox()s.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        _model = self.cmbInsert.get_model()
        _model.clear()

        self._set_sensitive()

    def _do_load_insert(self, combo: RAMSTKComboBox) -> None:
        """Load the insert RAMSTKComboBox() when the specification changes.

        :param combo: the specification RAMSTKCombo() that called this method.
        """
        _type_id = int(self.cmbType.get_active())
        _spec_id = int(combo.get_active())
        _inserts = CONNECTION_INSERT_DICT.get(_type_id, {}).get(_spec_id, [])
        self.cmbInsert.do_load_combo(_inserts)

    def _do_load_specification(self, combo: RAMSTKComboBox) -> None:
        """Retrieve RAMSTKCombo() changes and assign to Connection attribute.

        :param combo: the connection type RAMSTKCombo() that called this method.
        """
        _type_id = int(combo.get_active())
        _specifications = CONNECTION_SPECIFICATION_DICT.get(_type_id, [])
        self.cmbSpecification.do_load_combo(_specifications)

    def _do_set_widget_callbacks(self) -> None:
        """Set the callbacks for the connection widgets."""
        super().do_set_widget_callbacks()

        self.cmbSpecification.connect("changed", self._do_load_insert)
        self.cmbType.connect("changed", self._do_load_specification)

    def _get_quality_list(self) -> List[List[str]]:
        """Return the list of quality levels based on subcategory.

        :return: list of connection quality levels.
        :rtype: list
        """
        _default_quality_list = [
            ["MIL-SPEC"],
            [_("Lower")],
        ]
        return (
            _default_quality_list
            if self._hazard_rate_method_id == 1
            else CONNECTION_QUALITY_DICT.get(self.subcategory_id, [[""]])
        )

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self._set_sensitive()
        super().do_set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update({"quality_id": self._quality_id})

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected connection."""
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbInsert,
            self.cmbSpecification,
            self.cmbType,
            self.txtActivePins,
            self.txtAmpsContact,
            self.txtContactGauge,
            self.txtMating,
            self.txtNHand,
            self.txtNPlanes,
            self.txtNWave,
        ]

        # Reset all widgets to be insensitive.
        super().do_set_widget_sensitivity(
            _all_widgets,
            False,
        )

        _sensitivity_map = {
            1: [
                self.cmbType,
                self.cmbSpecification,
                self.cmbInsert,
                self.txtActivePins,
                self.txtAmpsContact,
                self.txtContactGauge,
                self.txtMating,
            ],
            2: [
                self.txtAmpsContact,
                self.txtContactGauge,
                self.txtMating,
                self.txtActivePins,
            ],
            3: [
                self.cmbQuality,
                self.txtActivePins,
            ],
            4: [
                self.txtNWave,
                self.txtNHand,
                self.txtNPlanes,
            ],
        }

        if self._hazard_rate_method_id == 1:
            super().do_set_widget_sensitivity([self.cmbType])
        else:
            super().do_set_widget_sensitivity(
                _sensitivity_map.get(self.subcategory_id, [])
            )
