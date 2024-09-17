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
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel

INSERT_A_LIST: List[List[str]] = [
    [_("Vitreous Glass")],
    [_("Alumina Ceramic")],
    [_("Polyimide")],
]
INSERT_B_LIST: List[List[str]] = [
    [_("Diallylphtalate")],
    [_("Melamine")],
    [_("Flourosilicone")],
    [_("Silicone Rubber")],
    [_("Polysulfone")],
    [_("Epoxy Resin")],
]
INSERT_C_LIST: List[List[str]] = [
    [_("Polytetraflourethylene (Teflon)")],
    [_("Chlorotriflourethylene (Kel-f)")],
]
INSERT_D_LIST: List[List[str]] = [
    [_("Polyamide (Nylon)")],
    [_("Polychloroprene (Neoprene)")],
    [_("Polyethylene")],
]
# CONNECTION_INSERT_DICT: Nested dictionary structure
# Key 1: Connection type
# Key 2: Insert type
# Value: List of insert materials
CONNECTION_INSERT_DICT = {
    1: {
        1: INSERT_B_LIST,
        2: INSERT_B_LIST,
        3: INSERT_A_LIST + INSERT_B_LIST,
        4: INSERT_A_LIST + INSERT_B_LIST,
        5: INSERT_A_LIST + INSERT_B_LIST,
    },
    2: {
        1: INSERT_B_LIST + INSERT_D_LIST,
        2: INSERT_A_LIST + INSERT_B_LIST + INSERT_D_LIST,
        3: INSERT_A_LIST + INSERT_B_LIST,
        4: INSERT_A_LIST + INSERT_B_LIST,
        5: INSERT_B_LIST,
        6: INSERT_B_LIST,
    },
    3: {
        1: INSERT_B_LIST + INSERT_D_LIST,
        2: INSERT_B_LIST + INSERT_D_LIST,
    },
    4: {
        1: INSERT_C_LIST,
        2: INSERT_C_LIST,
        3: INSERT_C_LIST,
        4: INSERT_C_LIST,
        5: INSERT_C_LIST,
        6: INSERT_C_LIST,
        7: INSERT_C_LIST,
        8: INSERT_B_LIST + INSERT_C_LIST,
    },
    5: {
        1: INSERT_B_LIST + INSERT_C_LIST,
    },
}
CONNECTION_QUALITY_DICT = {
    1: [["MIL-SPEC"], [_("Lower")]],
    2: [["MIL-SPEC"], [_("Lower")]],
    4: [[_("MIL-SPEC or comparable IPC standards")], [_("Lower")]],
    5: [
        [_("Automated")],
        [_("Manual, Upper")],
        [_("Manual, Standard")],
        [_("Manual, Lower")],
    ],
}
CONNECTION_SPECIFICATION_DICT = {
    1: [
        [_("MIL-C-24308")],
        [_("MIL-C-28748")],
        [_("MIL-C-28804")],
        [_("MIL-C-83513")],
        [_("MIL-C-83733")],
    ],
    2: [
        [_("MIL-C-5015")],
        [_("MIL-C-26482")],
        [_("MIL-C-28840")],
        [_("MIL-C-38999")],
        [_("MIL-C-81511")],
        [_("MIL-C-83723")],
    ],
    3: [[_("MIL-C-3767")], [_("MIL-C-22992")]],
    4: [
        [_("MIL-C-3607")],
        [_("MIL-C-3643")],
        [_("MIL-C-3650")],
        [_("MIL-C-3655")],
        [_("MIL-C-25516")],
        [_("MIL-C-39012")],
        [_("MIL-C-55235")],
        [_("MIL-C-55339")],
    ],
    5: [[_("MIL-C-49142")]],
}
CONNECTION_TYPE_DICT = {
    1: [
        [_("Rack and Panel")],
        [_("Circular")],
        [_("Power")],
        [_("Coaxial")],
        [_("Triaxial")],
    ],
    4: [
        [_("PWA/PCB with PTHs")],
        [
            _(
                "Discrete Wiring with Electroless Deposited PTH (<3 Levels "
                "of Circuitry)"
            )
        ],
    ],  # noqa
    5: [
        [_("Hand Solder w/o Wrapping")],
        [_("Hand Solder w/ Wrapping")],
        [_("Crimp")],
        [_("Weld")],
        [_("Solderless Wrap")],
        [_("Clip Termination")],
        [_("Reflow Solder")],
    ],
}


class ConnectionDesignElectricInputPanel(RAMSTKFixedPanel):
    """Displays connection assessment input attribute data.

    The Connection assessment input view displays all the assessment inputs for
    the selected connection.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analysis.  The attributes of a
    Connection assessment input view are:

    :cvar dict _dic_quality: dictionary of MIL-HDBK-217 capacitor quality
        levels.  Key is capacitor subcategory ID; values are lists of quality
        levels.
    :cvar dict _dic_insert: dictionary of connector insert materials.  First
        key is connector type ID, second key is connector specification ID;
        values are lists of insert materials.
     :cvar dict _dic_insert: dictionary of connector insert materials.  First
        key is connector type ID, second key is connector specification ID;
        values are lists of insert materials.
    :cvar dict _dic_type: dictionary of connector types.  Key is connector
        subcategory ID; values are lists of types.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.
    :ivar _lst_widgets: the list of widgets to display in the panel.  These
        are listed in the order they should appear on the panel.

    :ivar _hazard_rate_method_id: the ID of the method to use for estimating
        the Hardware item's hazard rate.
    :ivar _title: the text to put on the RAMSTKFrame() holding the
        assessment input widgets.

    :ivar fmt: the formatting to use when displaying float values.
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

    # Define private dict class attributes.
    _dic_insert: Dict[int, Dict[int, List[List[str]]]] = CONNECTION_INSERT_DICT
    _dic_quality: Dict[int, List[List[str]]] = CONNECTION_QUALITY_DICT
    _dic_specification: Dict[int, List[List[str]]] = CONNECTION_SPECIFICATION_DICT
    _dic_type: Dict[int, List[List[str]]] = CONNECTION_TYPE_DICT

    # Define private list attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Connection Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

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

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = 0
        self._quality_id: int = 0

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map = self._do_initialize_attribute_widget_map()

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.cmbSpecification.connect("changed", self._do_load_insert)
        self.cmbType.connect("changed", self._do_load_specification)

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.do_load_comboboxes,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the connection RKTComboBox()s.

        :param subcategory_id: the subcategory ID of the selected connection.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
            signal="changed",
        )
        self.cmbType.do_load_combo(
            self._dic_type.get(self.subcategory_id, [[""]]),
            signal="changed",
        )

        # Clear the remaining ComboBox()s.  These are loaded dynamically
        # based on the selection made in other ComboBox()s.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        _model = self.cmbInsert.get_model()
        _model.clear()

        self._do_set_sensitive()

    def _do_initialize_attribute_widget_map(self) -> Dict[str, Any]:
        """Initialize the attribute widget map."""
        return {
            "quality_id": [
                32,
                self.cmbQuality,
                "changed",
                super().on_changed_combo,
                "wvw_editing_reliability",
                0,
                {
                    "tooltip": _("The quality level of the connector/connection."),
                },
                _("Quality Level:"),
                "gint",
            ],
            "type_id": [
                48,
                self.cmbType,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The type of connector/connection."),
                },
                _("Connector Type:"),
                "gint",
            ],
            "specification_id": [
                36,
                self.cmbSpecification,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The governing specification for the connection."),
                },
                _("Specification:"),
                "gint",
            ],
            "insert_id": [
                18,
                self.cmbInsert,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The connector insert material."),
                },
                _("Insert Material:"),
                "gint",
            ],
            "contact_gauge": [
                8,
                self.txtContactGauge,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                22,
                {
                    "tooltip": _("The gauge of the contacts in the connector."),
                },
                _("Contact Gauge:"),
                "gint",
            ],
            "n_active_pins": [
                22,
                self.txtActivePins,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The number of active pins in the connector."),
                },
                _("Active Pins:"),
                "gint",
            ],
            "current_operating": [
                10,
                self.txtAmpsContact,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The amperes per active contact."),
                },
                _("Amperes/Contact:"),
                "gfloat",
            ],
            "n_cycles": [
                24,
                self.txtMating,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The number of connector mate and unmate cycles per 1000 hours "
                        "of operation."
                    ),
                },
                _("Mating/Unmating Cycles (per 1000 hours):"),
                "gfloat",
            ],
            "n_wave_soldered": [
                27,
                self.txtNWave,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The number of wave soldered PTH connections."),
                },
                _("Number of Wave Soldered PTH:"),
                "gint",
            ],
            "n_hand_soldered": [
                26,
                self.txtNHand,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The number of hand soldered PTH connections."),
                },
                _("Number of Hand Soldered PTH:"),
                "gint",
            ],
            "n_circuit_planes": [
                23,
                self.txtNPlanes,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The number of circuit planes for wave soldered connections."
                    ),
                },
                _("Number of Circuit Planes:"),
                "gint",
            ],
        }

    def _do_load_insert(self, combo: RAMSTKComboBox) -> None:
        """Load the insert RAMSTKComboBox() when the specification changes.

        :param combo: the specification RAMSTKCombo() that called this method.
        :return: None
        :rtype: None
        """
        _type_id = int(self.cmbType.get_active())
        _spec_id = int(combo.get_active())
        _inserts = self._dic_insert.get(_type_id, {}).get(_spec_id, [])
        self.cmbInsert.do_load_combo(entries=_inserts, signal="changed")

    def _do_load_specification(self, combo: RAMSTKComboBox) -> None:
        """Retrieve RAMSTKCombo() changes and assign to Connection attribute.

        :param combo: the connection type RAMSTKCombo() that called this
            method.
        :return: None
        :rtype: None
        """
        _type_id = int(combo.get_active())
        _specifications = self._dic_specificationget(_type_id, [])
        self.cmbSpecification.do_load_combo(entries=_specifications, signal="changed")

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
            else self._dic_quality.get(self.subcategory_id, [[""]])
        )

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self._set_sensitive()
        super.set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            self._quality_id,
            signal="changed",
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected connection.

        :return: None
        :rtype: None
        """
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
        super.set_widget_sensitivity(
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
            super().set_widget_sensitivity([self.cmbType])
        else:
            super.set_widget_sensitivity(_sensitivity_map.get(self.subcategory_id, []))
