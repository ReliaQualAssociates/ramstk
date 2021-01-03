# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.connection.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
# noinspection PyPackageRequirements
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry

# RAMSTK Local Imports
from .panels import RAMSTKAssessmentInputPanel, RAMSTKAssessmentResultPanel


class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
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
    :ivar _subcategory_id: the ID of the Hardware item's subcategory.
    :ivar _title: the text to put on the RAMSTKFrame() holding the
        assessment input widgets.

    :ivar fmt: the formatting to use when displaying float values.
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

    # Quality levels; key is the subcategory ID.
    _dic_quality: Dict[int, List[Any]] = {
        1: [["MIL-SPEC"], [_("Lower")]],
        2: [["MIL-SPEC"], [_("Lower")]],
        4: [[_("MIL-SPEC or comparable IPC standards")], [_("Lower")]],
        5: [[_("Automated")], [_("Manual, Upper")], [_("Manual, Standard")],
            [_("Manual, Lower")]]
    }

    # Connector types; key is the subcategory ID.
    _dic_type: Dict[int, List[Any]] = {
        1: [[_("Rack and Panel")], [_("Circular")], [_("Power")],
            [_("Coaxial")], [_("Triaxial")]],
        4: [[_("PWA/PCB with PTHs")],
            [
                _("Discrete Wiring with Electroless Deposited PTH (<3 Levels "
                  "of Circuitry)")
            ]],  # noqa
        5: [[_("Hand Solder w/o Wrapping")], [_("Hand Solder w/ Wrapping")],
            [_("Crimp")], [_("Weld")], [_("Solderless Wrap")],
            [_("Clip Termination")], [_("Reflow Solder")]]
    }

    # Specifications; key is the type ID.
    _dic_specification: Dict[int, List[Any]] = {
        1: [[_("MIL-C-24308")], [_("MIL-C-28748")], [_("MIL-C-28804")],
            [_("MIL-C-83513")], [_("MIL-C-83733")]],
        2: [[_("MIL-C-5015")], [_("MIL-C-26482")], [_("MIL-C-28840")],
            [_("MIL-C-38999")], [_("MIL-C-81511")], [_("MIL-C-83723")]],
        3: [[_("MIL-C-3767")], [_("MIL-C-22992")]],
        4: [[_("MIL-C-3607")], [_("MIL-C-3643")], [_("MIL-C-3650")],
            [_("MIL-C-3655")], [_("MIL-C-25516")], [_("MIL-C-39012")],
            [_("MIL-C-55235")], [_("MIL-C-55339")]],
        5: [[_("MIL-C-49142")]]
    }

    _lst_insert_A: List[Any] = [[_("Vitreous Glass")], [_("Alumina Ceramic")],
                                [_("Polyimide")]]
    _lst_insert_B = [[_("Diallylphtalate")], [_("Melamine")],
                     [_("Flourosilicone")], [_("Silicone Rubber")],
                     [_("Polysulfone")], [_("Epoxy Resin")]]
    _lst_insert_C = [[_("Polytetraflourethylene (Teflon)")],
                     [_("Chlorotriflourethylene (Kel-f)")]]
    _lst_insert_D = [[_("Polyamide (Nylon)")],
                     [_("Polychloroprene (Neoprene)")], [_("Polyethylene")]]
    # Connector insert material; first key is the type ID, second key is the
    # specification ID.
    _dic_insert: Dict[int, Dict[int, List[Any]]] = {
        1: {
            1: _lst_insert_B,
            2: _lst_insert_B,
            3: _lst_insert_A + _lst_insert_B,
            4: _lst_insert_A + _lst_insert_B,
            5: _lst_insert_A + _lst_insert_B
        },
        2: {
            1: _lst_insert_B + _lst_insert_D,
            2: _lst_insert_A + _lst_insert_B + _lst_insert_D,
            3: _lst_insert_A + _lst_insert_B,
            4: _lst_insert_A + _lst_insert_B,
            5: _lst_insert_B,
            6: _lst_insert_B
        },
        3: {
            1: _lst_insert_B + _lst_insert_D,
            2: _lst_insert_B + _lst_insert_D
        },
        4: {
            1: _lst_insert_C,
            2: _lst_insert_C,
            3: _lst_insert_C,
            4: _lst_insert_C,
            5: _lst_insert_C,
            6: _lst_insert_C,
            7: _lst_insert_C,
            8: _lst_insert_B + _lst_insert_C
        },
        5: {
            1: _lst_insert_B + _lst_insert_C
        }
    }

    # Define private list attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Connection assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys = {
            0: ['quality_id', 'integer'],
            1: ['type_id', 'integer'],
            2: ['specification_id', 'integer'],
            3: ['insert_id', 'integer'],
            4: ['contact_gauge', 'integer'],
            5: ['n_active_pins', 'integer'],
            6: ['current_operating', 'float'],
            7: ['n_cycles', 'integer'],
            8: ['n_wave_soldered', 'integer'],
            9: ['n_hand_soldered', 'integer'],
            10: ['n_circuit_planes', 'integer'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _("Quality Level:"),
            _("Connector Type:"),
            _("Specification:"),
            _("Insert Material:"),
            _("Contact Gauge:"),
            _("Active Pins:"),
            _("Amperes/Contact:"),
            _("Mating/Unmating Cycles (per 1000 hours):"),
            _("Number of Wave Soldered PTH:"),
            _("Number of Hand Soldered PTH:"),
            _("Number of Circuit Planes:"),
        ]
        self._lst_tooltips: List[str] = [
            _("The quality level of the connector/connection."),
            _("The type of connector/connection."),
            _("The governing specification for the connection."),
            _("The connector insert material."),
            _("The gauge of the contacts in the connector."),
            _("The number of active pins in the connector."),
            _("The amperes per active contact."),
            _("The number of connector mate and unmate cycles per 1000 hours "
              "of operation."),
            _("The number of wave soldered PTH connections."),
            _("The number of hand soldered PTH connections."),
            _("The number of circuit planes for wave soldered connections."),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
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

        self._dic_attribute_updater = {
            'quality_id': [self.cmbQuality.do_update, 'changed', 0],
            'specification_id':
            [self.cmbSpecification.do_update, 'changed', 1],
            'type_id': [self.cmbType.do_update, 'changed', 2],
            'insert_id': [self.cmbInsert.do_update, 'changed', 3],
            'contact_gauge': [self.txtContactGauge.do_update, 'changed', 4],
            'n_active_pins': [self.txtActivePins.do_update, 'changed', 5],
            'current_operating': [self.txtAmpsContact, 'changed', 6],
            'n_cycles': [self.txtMating, 'changed', 7],
            'n_wave_soldered': [self.txtNWave, 'changed', 8],
            'n_hand_soldered': [self.txtNHand, 'changed', 9],
            'n_circuit_planes': [self.txtNPlanes, 'changed', 10],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.cmbType,
            self.cmbSpecification,
            self.cmbInsert,
            self.txtContactGauge,
            self.txtActivePins,
            self.txtAmpsContact,
            self.txtMating,
            self.txtNWave,
            self.txtNHand,
            self.txtNPlanes,
        ]

        self.__set_properties()
        super().do_make_panel_fixed()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    # pylint: disable=unused-argument
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the connection RKTComboBox()s.

        :param subcategory_id: the subcategory ID of the selected capacitor.
            This is unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F parts count.
            _data = [["MIL-SPEC"], [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data, signal='changed')

        # Load the connector type RAMSTKComboBox().
        try:
            _data = self._dic_type[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data, signal='changed')

        # Clear the remaining ComboBox()s.  These are loaded dynamically
        # based on the selection made in other ComboBox()s.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        _model = self.cmbInsert.get_model()
        _model.clear()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Connection assessment input widgets.

        :param attributes: the attributes dictionary for the selected
            Connection.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        # We don't block the callback signal otherwise the specification
        # RAMSTKComboBox() will not be loaded and set.
        self.cmbType.set_active(attributes['type_id'])

        if self._hazard_rate_method_id == 2:
            # We don't block the callback signal otherwise the insert
            # RAMSTKComboBox() will not be loaded and set.
            self.cmbSpecification.set_active(attributes['specification_id'])
            self.cmbInsert.do_update(attributes['insert_id'], signal='changed')

            self.txtContactGauge.do_update(str(attributes['contact_gauge']),
                                           signal='changed')
            self.txtActivePins.do_update(str(attributes['n_active_pins']),
                                         signal='changed')
            self.txtAmpsContact.do_update(str(
                self.fmt.format(attributes['current_operating'])),
                                          signal='changed')  # noqa
            self.txtMating.do_update(str(attributes['n_cycles']),
                                     signal='changed')

            if self._subcategory_id == 4:
                self.txtNWave.do_update(str(attributes['n_wave_soldered']),
                                        signal='changed')
                self.txtNHand.do_update(str(attributes['n_hand_soldered']),
                                        signal='changed')
                self.txtNPlanes.do_update(str(attributes['n_circuit_planes']),
                                          signal='changed')

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected connection.

        :return: None
        :rtype: None
        """
        self.cmbInsert.set_sensitive(False)
        self.cmbSpecification.set_sensitive(False)
        self.cmbType.set_sensitive(False)

        self.txtActivePins.set_sensitive(False)
        self.txtAmpsContact.set_sensitive(False)
        self.txtContactGauge.set_sensitive(False)
        self.txtMating.set_sensitive(False)
        self.txtNHand.set_sensitive(False)
        self.txtNPlanes.set_sensitive(False)
        self.txtNWave.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            self.cmbType.set_sensitive(True)
        else:
            self.__do_set_circular_sensitive()
            self.__do_set_ic_socket_sensitive()
            self.__do_set_pwa_edge_sensitive()
            self.__do_set_pth_sensitive()

    def _do_load_insert(self, combo: RAMSTKComboBox) -> None:
        """Load the insert RAMSTKComboBox() when the specification changes.

        :param combo: the specification RAMSTKCombo() that called this method.
        :return: None
        :rtype: None
        """
        try:
            _type_id = int(self.cmbType.get_active())
            _spec_id = int(combo.get_active())
            _inserts = self._dic_insert[_type_id][_spec_id]
        except KeyError:
            _inserts = []
        self.cmbInsert.do_load_combo(entries=_inserts, signal='changed')

    def _do_load_specification(self, combo: RAMSTKComboBox) -> None:
        """Retrieve RAMSTKCombo() changes and assign to Connection attribute.

        :param combo: the connection type RAMSTKCombo() that called this
            method.
        :return: None
        :rtype: None
        """
        try:
            _type_id = int(combo.get_active())
            _specifications = self._dic_specification[_type_id]
        except KeyError:
            _specifications = []
        self.cmbSpecification.do_load_combo(entries=_specifications,
                                            signal='changed')

    def __do_set_circular_sensitive(self) -> None:
        """Set the widgets for circular connectors sensitive or not.

        :return: None
        :rtype: None
        """
        if self._subcategory_id == 1:
            self.cmbInsert.set_sensitive(True)
            self.cmbSpecification.set_sensitive(True)
            self.cmbType.set_sensitive(True)

            self.txtActivePins.set_sensitive(True)
            self.txtAmpsContact.set_sensitive(True)
            self.txtContactGauge.set_sensitive(True)
            self.txtMating.set_sensitive(True)

    def __do_set_ic_socket_sensitive(self) -> None:
        """Set the widgets for IC socket connectors sensitive or not.

        :return: None
        :rtype: None
        """
        if self._subcategory_id == 3:
            self.cmbQuality.set_sensitive(False)
            self.txtActivePins.set_sensitive(True)

    def __do_set_pwa_edge_sensitive(self) -> None:
        """Set the widgets for PCB/PWA edge connectors sensitive or not.

        :return: None
        :rtype: None
        """
        if self._subcategory_id == 2:
            self.txtAmpsContact.set_sensitive(True)
            self.txtContactGauge.set_sensitive(True)
            self.txtMating.set_sensitive(True)
            self.txtActivePins.set_sensitive(True)

    def __do_set_pth_sensitive(self) -> None:
        """Set the widgets for PTH connections sensitive or not.

        :return: None
        :rtype: None
        """
        if self._subcategory_id == 4:
            self.txtNWave.set_sensitive(True)
            self.txtNHand.set_sensitive(True)
            self.txtNPlanes.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """Set callback methods for Connection assessment input widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed',
            super().on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed',
            super().on_changed_combo, 1, 'wvw_editing_hardware')
        self.cmbType.connect('changed', self._do_load_specification)
        self.cmbSpecification.dic_handler_id[
            'changed'] = self.cmbSpecification.connect(
                'changed',
                super().on_changed_combo, 2, 'wvw_editing_hardware')
        self.cmbSpecification.connect('changed', self._do_load_insert)
        self.cmbInsert.dic_handler_id['changed'] = self.cmbInsert.connect(
            'changed',
            super().on_changed_combo, 3, 'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtContactGauge.dic_handler_id[
            'changed'] = self.txtContactGauge.connect('changed',
                                                      super().on_changed_entry,
                                                      4,
                                                      'wvw_editing_hardware')
        self.txtActivePins.dic_handler_id[
            'changed'] = self.txtActivePins.connect('changed',
                                                    super().on_changed_entry,
                                                    5, 'wvw_editing_hardware')
        self.txtAmpsContact.dic_handler_id[
            'changed'] = self.txtAmpsContact.connect('changed',
                                                     super().on_changed_entry,
                                                     6, 'wvw_editing_hardware')
        self.txtMating.dic_handler_id['changed'] = self.txtMating.connect(
            'changed',
            super().on_changed_entry, 7, 'wvw_editing_hardware')
        self.txtNWave.dic_handler_id['changed'] = self.txtNWave.connect(
            'changed',
            super().on_changed_entry, 8, 'wvw_editing_hardware')
        self.txtNHand.dic_handler_id['changed'] = self.txtNHand.connect(
            'changed',
            super().on_changed_entry, 9, 'wvw_editing_hardware')
        self.txtNPlanes.dic_handler_id['changed'] = self.txtNPlanes.connect(
            'changed',
            super().on_changed_entry, 10, 'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for Connection assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties()

        # ----- ENTRIES
        self.txtContactGauge.do_set_properties(tooltip=self._lst_tooltips[4],
                                               width=125)
        self.txtActivePins.do_set_properties(tooltip=self._lst_tooltips[5],
                                             width=125)
        self.txtAmpsContact.do_set_properties(tooltip=self._lst_tooltips[6],
                                              width=125)
        self.txtMating.do_set_properties(tooltip=self._lst_tooltips[7],
                                         width=125)
        self.txtNWave.do_set_properties(tooltip=self._lst_tooltips[8],
                                        width=125)
        self.txtNHand.do_set_properties(tooltip=self._lst_tooltips[9],
                                        width=125)
        self.txtNPlanes.do_set_properties(tooltip=self._lst_tooltips[10],
                                          width=125)


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    """Displays connection assessment results attribute data.

    The connection assessment result view displays all the assessment results
    for the selected connection.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a connection assessment result view are:

    :cvar dict _dic_part_stress: dictionary of MIL-HDBK-217F part stress
        models.  The key is the subcategory ID attribute of the component.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.

    :ivar _hazard_rate_method_id: the ID of the method to use for estimating
        the Hardware item's hazard rate.
    :ivar _subcategory_id: the ID of the Hardware item's subcategory.

    :ivar fmt: the formatting to use when displaying float values.
    :ivar lblModel: displays the hazard rate model use to estimate the
        Hardware item's hazard rate.
    :ivar self.txtLambdaB: displays the base hazard rate for the Hardware
        item.
    :ivar txtPiC: displays the construction factor for the connection.
        :ivar txtPiE: displays the environment factor for the Hardware item.
    :ivar txtPiK: displays the capacitance factor for the connection.
    :ivar txtPiP: displays the configuration factor for the connection.
    :ivar txtPiQ: displays the quality factor for the Hardware item.
    """
    # Define private dict class attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub>\u03C0"
        "<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub>\u03C0"
        "<sub>E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>[N<sub>1</sub>\u03C0<sub>C</sub> + "
        "N<sub>2</sub>(\u03C0<sub>C</sub> + "
        "13)]\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Connection assessment result view."""
        super().__init__()

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            '\u03C0<sub>K</sub>:',
            '\u03C0<sub>P</sub>:',
            '\u03C0<sub>C</sub>:',
        ]
        self._lst_tooltips: List[str] = [
            _("The assessment model used to calculate the connection hazard "
              "rate."),
            _('The base hazard rate for the connection.'),
            _('The quality factor for the connection.'),
            _('The environment factor for the connection.'),
            _("The mating/unmating factor for the connection."),
            _("The active pins factor for the connection."),
            _("The complexity factor for the connection."),
        ]

        # Initialize private scalar attributes.

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiK: RAMSTKEntry = RAMSTKEntry()
        self.txtPiP: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtPiK,
            self.txtPiP,
            self.txtPiC,
        ]

        super().do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the connection assessment results page.

        :param attributes: the attributes dictionary for the selected
                                Connection.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.txtPiC.do_update(str(self.fmt.format(attributes['piC'])))
        self.txtPiK.do_update(str(self.fmt.format(attributes['piK'])))
        self.txtPiP.do_update(str(self.fmt.format(attributes['piP'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected connection.

        :return: None
        :rtype: None
        """
        self.txtPiK.set_sensitive(False)
        self.txtPiP.set_sensitive(False)
        self.txtPiC.set_sensitive(False)

        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
            self.__do_set_circular_pwa_sensitive()
            self.__do_set_ic_socket_sensitive()
            self.__do_set_pth_sensitive()
            self.__do_set_non_pth_sensitive()

    def __do_set_circular_pwa_sensitive(self) -> None:
        """Set widgets for circular and PWS connectors sensitive or not.

        :return: None
        :rtype: None
        """
        if self._subcategory_id in [1, 2]:
            self.txtPiK.set_sensitive(True)
            self.txtPiQ.set_sensitive(False)
            self.txtPiP.set_sensitive(True)

    def __do_set_ic_socket_sensitive(self) -> None:
        """Set widgets for IC socket connections sensitive or not.

        :return: None
        :rtype: None
        """
        if self._subcategory_id == 3:
            self.txtPiP.set_sensitive(True)
            self.txtPiQ.set_sensitive(False)

    def __do_set_pth_sensitive(self) -> None:
        """Set widgets for PTH connections sensitive or not.

        :return: None
        :rtype: None
        """
        if self._subcategory_id == 4:
            self.txtPiC.set_sensitive(True)
            self.txtPiQ.set_sensitive(True)

    def __do_set_non_pth_sensitive(self) -> None:
        """Set widgets for non-PTH connections sensitive or not.

        :return: None
        :rtype: None
        """
        if self._subcategory_id == 5:
            self.txtPiQ.set_sensitive(True)
