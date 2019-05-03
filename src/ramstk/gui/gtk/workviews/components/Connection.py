# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Connection.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                           AssessmentResults)


class ConnectionAssessmentInputs(AssessmentInputs):
    """
    Display Connection assessment input attribute data in the RAMSTK Work Book.

    The Connection assessment input view displays all the assessment inputs for
    the selected connection.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analysis.  The attributes of a
    Connection assessment input view are:

    :cvar dict _dic_quality: dictionary of connector quality levels.  Key is
                             connector subcategory ID; values are lists of
                             quality levels.
    :cvar dict _dic_type: dictionary of connector types.  Key is connector
                          subcategory ID; values are lists of types.
    :cvar dict _dic_specification: dictionary of connector MIL-SPECs.  Key is
                                   connector tye ID; values are lists
                                   of specifications.
    :cvar dict _dic_insert: dictionary of connector insert materials.  First
                            key is connector type ID, second key is connector
                            specification ID; values are lists of insert
                            materials.

    :ivar cmbType: select and display the type of the connection.
    :ivar cmbSpecification: select and display the governing specification of
                            the connection.
    :ivar cmbInsert: select and display the available insert materials for the
                     connector.
    :ivar txtContactGauge: enter and display the contact gauge of the
                           connector.
    :ivar txtActivePins: enter and display the number of active pins in the
                         connector.
    :ivar txtAmpsContact: enter and display the amps carried by the pins in the
                          connector.
    :ivar txtMating: enter and display the number of mate/demate cycles the
                     connector undergoes per 1000 hours.
    :ivar txtNWave: enter and display the number of wave soldered PTH
                    connections.
    :ivar txtNHand: enter and display the number of hand soldered PTH
                    connections.
    :ivar txtPlanes: enter and display the number of layers in the circuit
                     board the PTH needs to penetrate.

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   1   | cmbType - `changed`                       |
    +-------+-------------------------------------------+
    |   2   | cmbSpecification - `changed`              |
    +-------+-------------------------------------------+
    |   3   | cmbInsert - `changed`                     |
    +-------+-------------------------------------------+
    |   4   | txtContactGauge - `changed`               |
    +-------+-------------------------------------------+
    |   5   | txtActivePins - `changed`                 |
    +-------+-------------------------------------------+
    |   6   | txtAmpsContact - `changed`                |
    +-------+-------------------------------------------+
    |   7   | txtMating - `changed`                     |
    +-------+-------------------------------------------+
    |   8   | txtNWave - `changed`                      |
    +-------+-------------------------------------------+
    |   9   | txtNHand - `changed`                      |
    +-------+-------------------------------------------+
    |  10   | txtNPlanes - `changed`                    |
    +-------+-------------------------------------------+
    """

    # Define private dict attributes.
    # Quality levels; key is the subcategory ID.
    _dic_quality = {
        1: [["MIL-SPEC"], [_(u"Lower")]],
        2: [["MIL-SPEC"], [_(u"Lower")]],
        4: [[_(u"MIL-SPEC or comparable IPC standards")], [_(u"Lower")]],
        5: [[_(u"Automated")], [_(u"Manual, Upper")], [_(u"Manual, Standard")],
            [_(u"Manual, Lower")]]
    }
    # Connector types; key is the subcategory ID.
    _dic_type = {
        1: [[_("Rack and Panel")], [_(u"Circular")], [_(u"Power")],
            [_(u"Coaxial")], [_(u"Triaxial")]],
        4:
        [[_(u"PWA/PCB with PTHs")],
         [
             _(u"Discrete Wiring with Electroless Deposited PTH (<3 Levels of "
               u"Circuitry)")
         ]],
        5: [[_(u"Hand Solder w/o Wrapping")], [_(u"Hand Solder w/ Wrapping")],
            [_(u"Crimp")], [_(u"Weld")], [_(u"Solderless Wrap")],
            [_(u"Clip Termination")], [_(u"Reflow Solder")]]
    }
    # Specifications; key is the type ID.
    _dic_specification = {
        1: [[_(u"MIL-C-24308")], [_(u"MIL-C-28748")], [_(u"MIL-C-28804")],
            [_(u"MIL-C-83513")], [_(u"MIL-C-83733")]],
        2: [[_(u"MIL-C-5015")], [_(u"MIL-C-26482")], [_(u"MIL-C-28840")],
            [_(u"MIL-C-38999")], [_(u"MIL-C-81511")], [_(u"MIL-C-83723")]],
        3: [[_(u"MIL-C-3767")], [_(u"MIL-C-22992")]],
        4: [[_(u"MIL-C-3607")], [_(u"MIL-C-3643")], [_(u"MIL-C-3650")],
            [_(u"MIL-C-3655")], [_(u"MIL-C-25516")], [_(u"MIL-C-39012")],
            [_(u"MIL-C-55235")], [_(u"MIL-C-55339")]],
        5: [[_(u"MIL-C-49142")]]
    }
    _lst_insert_A = [[_(u"Vitreous Glass")], [_(u"Alumina Ceramic")],
                     [_(u"Polyimide")]]
    _lst_insert_B = [[_(u"Diallylphtalate")], [_(u"Melamine")],
                     [_(u"Flourosilicone")], [_(u"Silicone Rubber")],
                     [_(u"Polysulfone")], [_(u"Epoxy Resin")]]
    _lst_insert_C = [[_(u"Polytetraflourethylene (Teflon)")],
                     [_(u"Chlorotriflourethylene (Kel-f)")]]
    _lst_insert_D = [[_(u"Polyamide (Nylon)")],
                     [_(u"Polychloroprene (Neoprene)")], [_(u"Polyethylene")]]
    # Connector insert material; first key is the type ID, second key is the
    # specification ID.
    _dic_insert = {
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
    _lst_labels = [
        _(u"Quality Level:"),
        _(u"Connector Type:"),
        _(u"Specification:"),
        _(u"Insert Material:"),
        _(u"Contact Gauge:"),
        _(u"Active Pins:"),
        _(u"Amperes/Contact:"),
        _(u"Mating/Unmating Cycles (per 1000 hours):"),
        _(u"Number of Wave Soldered PTH:"),
        _(u"Number of Hand Soldered PTH:"),
        _(u"Number of Circuit Planes:")
    ]

    def __init__(self, **kwargs):
        """Initialize an instance of the Connection assessment input view."""
        AssessmentInputs.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbType = ramstk.RAMSTKComboBox(
            index=0,
            simple=False,
            tooltip=_(u"The type of connector/connection."))
        self.cmbSpecification = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The governing specification for the connection."))
        self.cmbInsert = ramstk.RAMSTKComboBox(
            index=0, simple=True, tooltip=_(u"The connector insert material."))

        self.txtContactGauge = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The gauge of the contacts in the connector."))
        self.txtActivePins = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The number of active pins in the connector."))
        self.txtAmpsContact = ramstk.RAMSTKEntry(
            width=125, tooltip=_(u"The amperes per active contact."))
        self.txtMating = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The number of connector mate and unmate cycles per "
                      u"1000 hours of operation."))
        self.txtNWave = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The number of wave soldered PTH connections."))
        self.txtNHand = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The number of hand soldered PTH connections."))
        self.txtNPlanes = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The number of circuit planes for wave soldered "
                      u"connections."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed', self._on_combo_changed,
                                          2))
        self._lst_handler_id.append(
            self.cmbInsert.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.txtContactGauge.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtActivePins.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtAmpsContact.connect('changed', self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtMating.connect('changed', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtNWave.connect('changed', self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtNHand.connect('changed', self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.txtNPlanes.connect('changed', self._on_focus_out, 10))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the connection RKTComboBox()s.

        :param int subcategory_id: the newly selected connection subcategory
                                   ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F parts count.
            _data = [["MIL-SPEC"], [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the connector type RAMSTKComboBox().
        try:
            _data = self._dic_type[subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

        # Clear the remaining ramstk.ComboBox()s.  These are loaded dynamically
        # based on the selection made in other ramstk.ComboBox()s.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        _model = self.cmbInsert.get_model()
        _model.clear()

        return None

    def _do_load_page(self, attributes):
        """
        Load the Connection assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Connection.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self._do_load_comboboxes(self._subcategory_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        # We don't block the callback signal otherwise the specification
        # RAMSTKComboBox() will not be loaded and set.
        self.cmbType.set_active(attributes['type_id'])

        if self._hazard_rate_method_id == 2:
            # We don't block the callback signal otherwise the insert
            # RAMSTKComboBox() will not be loaded and set.
            self.cmbSpecification.set_active(attributes['specification_id'])

            self.cmbInsert.handler_block(self._lst_handler_id[3])
            self.cmbInsert.set_active(attributes['insert_id'])
            self.cmbInsert.handler_unblock(self._lst_handler_id[3])

            self.txtContactGauge.handler_block(self._lst_handler_id[4])
            self.txtContactGauge.set_text(
                str(self.fmt.format(attributes['contact_gauge'])))
            self.txtContactGauge.handler_unblock(self._lst_handler_id[4])

            self.txtActivePins.handler_block(self._lst_handler_id[5])
            self.txtActivePins.set_text(
                str(self.fmt.format(attributes['n_active_pins'])))
            self.txtActivePins.handler_unblock(self._lst_handler_id[5])

            self.txtAmpsContact.handler_block(self._lst_handler_id[6])
            self.txtAmpsContact.set_text(
                str(self.fmt.format(attributes['current_operating'])))
            self.txtAmpsContact.handler_unblock(self._lst_handler_id[6])

            self.txtMating.handler_block(self._lst_handler_id[7])
            self.txtMating.set_text(
                str(self.fmt.format(attributes['n_cycles'])))
            self.txtMating.handler_unblock(self._lst_handler_id[7])

            if self._subcategory_id == 4:
                self.txtNWave.handler_block(self._lst_handler_id[8])
                self.txtNWave.set_text(
                    str(self.fmt.format(attributes['n_wave_soldered'])))
                self.txtNWave.handler_unblock(self._lst_handler_id[8])

                self.txtNHand.handler_block(self._lst_handler_id[9])
                self.txtNHand.set_text(
                    str(self.fmt.format(attributes['n_hand_soldered'])))
                self.txtNHand.handler_unblock(self._lst_handler_id[9])

                self.txtNPlanes.handler_block(self._lst_handler_id[10])
                self.txtNPlanes.set_text(
                    str(self.fmt.format(attributes['n_circuit_planes'])))
                self.txtNPlanes.handler_unblock(self._lst_handler_id[10])

        self._do_set_sensitive()

        return None

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected connection.

        :return: None
        :rtype: None
        """
        self.cmbSpecification.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.cmbInsert.set_sensitive(False)

        self.txtContactGauge.set_sensitive(False)
        self.txtActivePins.set_sensitive(False)
        self.txtAmpsContact.set_sensitive(False)
        self.txtMating.set_sensitive(False)
        self.txtNWave.set_sensitive(False)
        self.txtNHand.set_sensitive(False)
        self.txtNPlanes.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            self.cmbType.set_sensitive(True)
        else:
            if self._subcategory_id == 1:
                self.cmbSpecification.set_sensitive(True)
                self.cmbType.set_sensitive(True)
                self.cmbInsert.set_sensitive(True)

                self.txtAmpsContact.set_sensitive(True)
                self.txtContactGauge.set_sensitive(True)
                self.txtMating.set_sensitive(True)
                self.txtActivePins.set_sensitive(True)

            elif self._subcategory_id == 2:
                self.txtAmpsContact.set_sensitive(True)
                self.txtContactGauge.set_sensitive(True)
                self.txtMating.set_sensitive(True)
                self.txtActivePins.set_sensitive(True)

            elif self._subcategory_id == 3:
                self.cmbQuality.set_sensitive(False)
                self.txtActivePins.set_sensitive(True)

            elif self._subcategory_id == 4:
                self.cmbType.set_sensitive(True)

                self.txtNWave.set_sensitive(True)
                self.txtNHand.set_sensitive(True)
                self.txtNPlanes.set_sensitive(True)

            elif self._subcategory_id == 5:
                self.cmbType.set_sensitive(True)

        return None

    def _make_page(self):
        """
        Make the Connection class Gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for connections.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.cmbType, _x_pos, _y_pos[1])
        self.put(self.cmbSpecification, _x_pos, _y_pos[2])
        self.put(self.cmbInsert, _x_pos, _y_pos[3])
        self.put(self.txtContactGauge, _x_pos, _y_pos[4])
        self.put(self.txtActivePins, _x_pos, _y_pos[5])
        self.put(self.txtAmpsContact, _x_pos, _y_pos[6])
        self.put(self.txtMating, _x_pos, _y_pos[7])
        self.put(self.txtNWave, _x_pos, _y_pos[8])
        self.put(self.txtNHand, _x_pos, _y_pos[9])
        self.put(self.txtNPlanes, _x_pos, _y_pos[10])

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Connection attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    1    | cmbType          |    3    | cmbInsert        |
            +---------+------------------+---------+------------------+
            |    2    | cmbSpecification |         |                  |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        _dic_keys = {
            0: 'quality_id',
            1: 'type_id',
            2: 'specification_id',
            3: 'insert_id',
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        combo.handler_block(self._lst_handler_id[index])

        try:
            _new_text = int(combo.get_active())
        except ValueError:
            _new_text = 0

        # If the connection type changed, load the specification
        # RAMSTKComboBox().
        if index == 1:
            try:
                _type_id = int(combo.get_active())
                _data = self._dic_specification[_type_id]
            except KeyError:
                _data = []
            self.cmbSpecification.do_load_combo(_data)

        # If the connection specification changed, load the insert material
        # RAMSTKComboBox().
        elif index == 2:
            try:
                _type_id = int(self.cmbType.get_active())
                _spec_id = int(combo.get_active())
                _data = self._dic_insert[_type_id][_spec_id]
            except KeyError:
                _data = []
            self.cmbInsert.do_load_combo(_data)

        # Only publish the message if something is selected in the ComboBox.
        if _new_text != -1:
            pub.sendMessage(
                'wvw_editing_hardware',
                module_id=self._hardware_id,
                key=_key,
                value=_new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
                      method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Widget().  Indices are:

            +---------+---------------------+---------+---------------------+
            |  Index  | Widget              |  Index  | Widget              |
            +=========+=====================+=========+=====================+
            |    4    | txtContactGauge     |    8    | txtNWave            |
            +---------+---------------------+---------+---------------------+
            |    5    | txtActivePins       |    9    | txtNHand            |
            +---------+---------------------+---------+---------------------+
            |    6    | txtAmpsContact      |   10    | txtNPlanes          |
            +---------+---------------------+---------+---------------------+
            |    7    | txtMating           |         |                     |
            +---------+---------------------+---------+---------------------+

        :return: None
        :rtype: None
        """
        _dic_keys = {
            4: 'contact_gauge',
            5: 'n_active_pins',
            6: 'current_operating',
            7: 'n_cycles',
            8: 'n_wave_soldered',
            9: 'n_hand_soldered',
            10: 'n_circuit_planes'
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            if index in [4, 5, 8, 9, 10]:
                _new_text = int(entry.get_text())
            elif index in [6, 7]:
                _new_text = str(entry.get_text())
        except ValueError:
            _new_text = 0.0

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None


class ConnectionAssessmentResults(AssessmentResults):
    """
    Display Connection assessment results attribute data in the RAMSTK Work Book.

    The connection assessment result view displays all the assessment results
    for the selected connection.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a connection assessment result view are:

    :ivar txtPiK: displays the capacitance factor for the connection.
    :ivar txtPiP: displays the configuration factor for the connection.
    :ivar txtPiC: displays the construction factor for the connection.
    """

    def __init__(self, **kwargs):
        """Initialize an instance of the Connection assessment result view."""
        AssessmentResults.__init__(self, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_part_stress = {
            1:
            u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>",
            2:
            u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>",
            3:
            u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>",
            4:
            u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>[N<sub>1</sub>\u03C0<sub>C</sub> + N<sub>2</sub>(\u03C0<sub>C</sub> + 13)]\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            5:
            u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        }

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>K</sub>:")
        self._lst_labels.append(u"\u03C0<sub>P</sub>:")
        self._lst_labels.append(u"\u03C0<sub>C</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the connection failure "
              u"rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiK = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The mating/unmating factor for the connection."))
        self.txtPiP = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The active pins factor for the connection."))
        self.txtPiC = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The complexity factor for the connection."))

        self._make_page()
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def _do_load_page(self, attributes):
        """
        Load the connection assessment results page.

        :param dict attributes: the attributes dictionary for the selected
                                Connection.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiK.set_text(str(self.fmt.format(attributes['piK'])))
        self.txtPiP.set_text(str(self.fmt.format(attributes['piP'])))
        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

        return None

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected connection.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        self.txtPiK.set_sensitive(False)
        self.txtPiP.set_sensitive(False)
        self.txtPiC.set_sensitive(False)

        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id in [1, 2]:
                self.txtPiK.set_sensitive(True)
                self.txtPiQ.set_sensitive(False)
                self.txtPiP.set_sensitive(True)
            elif self._subcategory_id == 3:
                self.txtPiP.set_sensitive(True)
                self.txtPiQ.set_sensitive(False)
            elif self._subcategory_id == 4:
                self.txtPiC.set_sensitive(True)
                self.txtPiQ.set_sensitive(True)
            elif self._subcategory_id == 5:
                self.txtPiQ.set_sensitive(True)

        return None

    def _make_page(self):
        """
        Make the connection Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiK, _x_pos, _y_pos[3])
        self.put(self.txtPiP, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])

        return None
