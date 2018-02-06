# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Connection.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hardware Work View."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611


class AssessmentInputs(gtk.Fixed):
    """
    Display Hardware assessment input attribute data in the RTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Hardware assessment input view are:

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

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the connection
                               currently being displayed.

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

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | cmbQuality - `changed`                    |
    +----------+-------------------------------------------+
    |     1    | cmbType - `changed`                       |
    +----------+-------------------------------------------+
    |     2    | cmbSpecification - `changed`              |
    +----------+-------------------------------------------+
    |     3    | cmbInsert - `changed`                     |
    +----------+-------------------------------------------+
    |     4    | txtContactGauge - `changed`               |
    +----------+-------------------------------------------+
    |     5    | txtActivePins - `changed`                 |
    +----------+-------------------------------------------+
    |     6    | txtAmpsContact - `changed`                |
    +----------+-------------------------------------------+
    |     7    | txtMating - `changed`                     |
    +----------+-------------------------------------------+
    |     8    | txtNWave - `changed`                      |
    +----------+-------------------------------------------+
    |     9    | txtNHand - `changed`                      |
    +----------+-------------------------------------------+
    |    10    | txtNPlanes - `changed`                    |
    +----------+-------------------------------------------+
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
        4: [[_(u"PWA/PCB with PTHs")], [
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

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Connection assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                connection.
        :param int subcategory_id: the ID of the connection subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.cmbQuality = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The quality level of the connection."))
        self.cmbType = rtk.RTKComboBox(
            index=0,
            simple=False,
            tooltip=_(u"The type of connector/connection."))
        self.cmbSpecification = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The governing specification for the connection."))
        self.cmbInsert = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The connector insert material."))

        self.txtContactGauge = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The gauge of the contacts in the connector."))
        self.txtActivePins = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of active pins in the connector."))
        self.txtAmpsContact = rtk.RTKEntry(
            width=125, tooltip=_(u"The amperes per active contact."))
        self.txtMating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of connector mate and unmate cycles per "
                      u"1000 hours of operation."))
        self.txtNWave = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of wave soldered PTH connections."))
        self.txtNHand = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of hand soldered PTH connections."))
        self.txtNPlanes = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of circuit planes for wave soldered "
                      u"connections."))

        self._make_assessment_input_page()
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

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the connection RKTComboBox()s.

        This method is used to load the specification RTKComboBox() whenever
        the connection subcategory is changed.

        :param int subcategory_id: the newly selected connection subcategory ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._subcategory_id = subcategory_id

        # Load the quality level RTKComboBox().
        _model = self.cmbQuality.get_model()
        _model.clear()

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)
        if _attributes['hazard_rate_method_id'] == 1:
            _data = [["MIL-SPEC"], [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the connector type RTKComboBox().
        _model = self.cmbType.get_model()
        _model.clear()

        try:
            _data = self._dic_type[self._subcategory_id]
        except KeyError:
            _data = []

        self.cmbType.do_load_combo(_data)

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected connection.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.set_sensitive(True)
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

        if _attributes['hazard_rate_method_id'] == 1:
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

        return _return

    def _make_assessment_input_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        _model = self.cmbType.get_model()
        _model.clear()

        _model = self.cmbInsert.get_model()
        _model.clear()

        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for connections.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])
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

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Connection attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    2    | cmbSpecification |
            +---------+------------------+---------+------------------+
            |    1    | cmbType          |    3    | cmbInsert        |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 0:
                _attributes['quality_id'] = int(combo.get_active())
            elif index == 1:
                _attributes['type_id'] = int(combo.get_active())

                # Load the specification RTKComboBox().
                _model = self.cmbSpecification.get_model()
                _model.clear()

                try:
                    _data = self._dic_specification[_attributes['type_id']]
                except KeyError:
                    _data = []
                self.cmbSpecification.do_load_combo(_data)

            elif index == 2:
                _attributes['specification_id'] = int(combo.get_active())

                # Load the connector insert material RTKComboBox().
                _model = self.cmbInsert.get_model()
                _model.clear()

                try:
                    _data = self._dic_insert[_attributes['type_id']][
                        _attributes['specification_id']]
                except KeyError:
                    _data = []
                self.cmbInsert.do_load_combo(_data)

            elif index == 3:
                _attributes['insert_id'] = int(combo.get_active())

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RTKEntry() widgets..

        This method is called by:

            * RTKEntry() 'changed' signal
            * RTKTextView() 'changed' signal

        :param entry: the RTKEntry() or RTKTextView() that called the method.
        :type entry: :class:`rtk.gui.gtk.rtk.RTKEntry` or
                     :class:`rtk.gui.gtk.rtk.RTKTextView`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

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

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            try:
                _text = float(entry.get_text())
            except ValueError:
                _text = 0.0

            if index == 4:
                _attributes['contact_gauge'] = int(_text)
            elif index == 5:
                _attributes['n_active_pins'] = int(_text)
            elif index == 6:
                _attributes['current_operating'] = _text
            elif index == 7:
                _attributes['n_cycles'] = _text
            elif index == 8:
                _attributes['n_wave_soldered'] = int(_text)
            elif index == 9:
                _attributes['n_hand_soldered'] = int(_text)
            elif index == 10:
                _attributes['n_circuit_planes'] = int(_text)

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the connection assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              connection.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # Load the subcategory RTKComboBox.  We need to block the quality and
        # connector type RTKComboBoxes otherwise loading them causes the
        # respective attributes to be set to -1.
        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbType.handler_block(self._lst_handler_id[1])
        self._do_load_comboboxes(_attributes['subcategory_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])
        self.cmbType.handler_unblock(self._lst_handler_id[1])

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(_attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        # We don't block the callback signal otherwise the specification
        # RTKComboBox() will not be loaded and set.
        self.cmbType.set_active(_attributes['type_id'])

        if _attributes['hazard_rate_method_id'] == 2:
            # We don't block the callback signal otherwise the insert
            # RTKComboBox() will not be loaded and set.
            self.cmbSpecification.set_active(_attributes['specification_id'])

            self.cmbInsert.handler_block(self._lst_handler_id[3])
            self.cmbInsert.set_active(_attributes['insert_id'])
            self.cmbInsert.handler_unblock(self._lst_handler_id[3])

            self.txtContactGauge.handler_block(self._lst_handler_id[4])
            self.txtContactGauge.set_text(
                str(self.fmt.format(_attributes['contact_gauge'])))
            self.txtContactGauge.handler_unblock(self._lst_handler_id[4])

            self.txtActivePins.handler_block(self._lst_handler_id[5])
            self.txtActivePins.set_text(
                str(self.fmt.format(_attributes['n_active_pins'])))
            self.txtActivePins.handler_unblock(self._lst_handler_id[5])

            self.txtAmpsContact.handler_block(self._lst_handler_id[6])
            self.txtAmpsContact.set_text(
                str(self.fmt.format(_attributes['current_operating'])))
            self.txtAmpsContact.handler_unblock(self._lst_handler_id[6])

            self.txtMating.handler_block(self._lst_handler_id[7])
            self.txtMating.set_text(
                str(self.fmt.format(_attributes['n_cycles'])))
            self.txtMating.handler_unblock(self._lst_handler_id[7])

            if self._subcategory_id == 4:
                self.txtNWave.handler_block(self._lst_handler_id[8])
                self.txtNWave.set_text(
                    str(self.fmt.format(_attributes['n_wave_soldered'])))
                self.txtNWave.handler_unblock(self._lst_handler_id[8])

                self.txtNHand.handler_block(self._lst_handler_id[9])
                self.txtNHand.set_text(
                    str(self.fmt.format(_attributes['n_hand_soldered'])))
                self.txtNHand.handler_unblock(self._lst_handler_id[9])

                self.txtNPlanes.handler_block(self._lst_handler_id[10])
                self.txtNPlanes.set_text(
                    str(self.fmt.format(_attributes['n_circuit_planes'])))
                self.txtNPlanes.handler_unblock(self._lst_handler_id[10])

        self._do_set_sensitive()

        return _return


class StressInputs(gtk.Fixed):
    """
    Display Connection stress input attribute data in the RTK Work Book.

    The Connection stress input view displays all the assessment inputs for
    the selected connection.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a connection stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the connection
                               currently being displayed.

    :ivar txtTemperatureRated: enter and display the maximum rated temperature
                               of the connection.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           connection.
    :ivar txtVoltageOperating: enter and display the operating voltage of the
                               connector.
    :ivar txtCurrentRated: enter and display the rated current of the
                           connector.
    :ivar txtCurrentOperating: enter and display the operating current of the
                               connector.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTemperatureRated - `changed`           |
    +----------+-------------------------------------------+
    |     1    | txtVoltageRated - `changed`               |
    +----------+-------------------------------------------+
    |     2    | txtVoltageOperating - `changed`           |
    +----------+-------------------------------------------+
    |     3    | txtCurrentRated - `changed`               |
    +----------+-------------------------------------------+
    |     4    | txtCurrentOperating - `changed`           |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Minimum Rated Temperature (\u00B0C):"),
        _(u"Knee Temperature (\u00B0C):"),
        _(u"Maximum Rated Temperature (\u00B0C):"),
        _(u"Rated Voltage (V):"),
        _(u"Operating Voltage (V):"),
        _(u"Rated Current (A):"),
        _(u"Operating Current (A):")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Connection stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                connection.
        :param int subcategory_id: the ID of the connection subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtTemperatureKnee = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The break temperature (in \u00B0C) of the connector beyond "
                u"which it must be derated."))
        self.txtTemperatureRatedMin = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The minimum rated temperature (in \u00B0C) of the connector."
            ))
        self.txtTemperatureRatedMax = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The maximum rated temperature (in \u00B0C) of the connector."
            ))
        self.txtVoltageRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated voltage (in V) of the connector."))
        self.txtVoltageOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating voltage (in V) of the connector."))
        self.txtCurrentRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated current (in A) of the connector pins."))
        self.txtCurrentOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating current (in A) of the connector pins."))

        self._lst_handler_id.append(
            self.txtTemperatureRatedMin.connect('changed', self._on_focus_out,
                                                0))
        self._lst_handler_id.append(
            self.txtTemperatureKnee.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect('changed', self._on_focus_out,
                                                2))
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('changed', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.txtVoltageOperating.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtCurrentRated.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtCurrentOperating.connect('changed', self._on_focus_out, 6))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the connection module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for connections.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[2])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[3])
        self.put(self.txtVoltageOperating, _x_pos, _y_pos[4])
        self.put(self.txtCurrentRated, _x_pos, _y_pos[5])
        self.put(self.txtCurrentOperating, _x_pos, _y_pos[6])

        self.show_all()

        return None

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RTKEntry() widgets..

        This method is called by:

            * RTKEntry() 'changed' signal
            * RTKTextView() 'changed' signal

        :param entry: the RTKEntry() or RTKTextView() that called the method.
        :type entry: :class:`rtk.gui.gtk.rtk.RTKEntry` or
                     :class:`rtk.gui.gtk.rtk.RTKTextView`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

        +---------+------------------------+---------+---------------------+
        |  Index  | Widget                 |  Index  | Widget              |
        +=========+========================+=========+=====================+
        |    0    | txtTemperatureRatedMin |    4    | txtVoltageOperating |
        +---------+------------------------+---------+---------------------+
        |    1    | txtTemperatureKnee     |    5    | txtCurrentRated     |
        +---------+------------------------+---------+---------------------+
        |    2    | txtTemperatureRatedMax |    6    | txtCurrentOperating |
        +---------+------------------------+---------+---------------------+
        |    3    | txtVoltageRated        |         |                     |
        +---------+------------------------+---------+---------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            try:
                _text = float(entry.get_text())
            except ValueError:
                _text = 0.0

            if index == 0:
                _attributes['temperature_rated_min'] = _text
            elif index == 1:
                _attributes['temperature_knee'] = _text
            elif index == 2:
                _attributes['temperature_rated_max'] = _text
            elif index == 3:
                _attributes['voltage_rated'] = _text
            elif index == 4:
                _attributes['voltage_dc_operating'] = _text
            elif index == 5:
                _attributes['current_rated'] = _text
            elif index == 6:
                _attributes['current_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the connection stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              connection.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # We don't block the callback signal otherwise the style RTKComboBox()
        # will not be loaded and set.
        self.txtTemperatureRatedMin.handler_block(self._lst_handler_id[0])
        self.txtTemperatureRatedMin.set_text(
            str(self.fmt.format(_attributes['temperature_rated_min'])))
        self.txtTemperatureRatedMin.handler_unblock(self._lst_handler_id[0])

        self.txtTemperatureKnee.handler_block(self._lst_handler_id[1])
        self.txtTemperatureKnee.set_text(
            str(self.fmt.format(_attributes['temperature_knee'])))
        self.txtTemperatureKnee.handler_unblock(self._lst_handler_id[1])

        self.txtTemperatureRatedMax.handler_block(self._lst_handler_id[2])
        self.txtTemperatureRatedMax.set_text(
            str(self.fmt.format(_attributes['temperature_rated_max'])))
        self.txtTemperatureRatedMax.handler_unblock(self._lst_handler_id[2])

        self.txtVoltageRated.handler_block(self._lst_handler_id[3])
        self.txtVoltageRated.set_text(
            str(self.fmt.format(_attributes['voltage_rated'])))
        self.txtVoltageRated.handler_unblock(self._lst_handler_id[3])

        self.txtVoltageOperating.handler_block(self._lst_handler_id[4])
        self.txtVoltageOperating.set_text(
            str(self.fmt.format(_attributes['voltage_dc_operating'])))
        self.txtVoltageOperating.handler_unblock(self._lst_handler_id[4])

        self.txtCurrentRated.handler_block(self._lst_handler_id[5])
        self.txtCurrentRated.set_text(
            str(self.fmt.format(_attributes['current_rated'])))
        self.txtCurrentRated.handler_unblock(self._lst_handler_id[5])

        self.txtCurrentOperating.handler_block(self._lst_handler_id[6])
        self.txtCurrentOperating.set_text(
            str(self.fmt.format(_attributes['current_operating'])))
        self.txtCurrentOperating.handler_unblock(self._lst_handler_id[6])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display connection assessment results attribute data in the RTK Work Book.

    The connection assessment result view displays all the assessment results
    for the selected connection.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a connection assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the connection
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the connection.
    :ivar txtPiK: displays the capacitance factor for the connection.
    :ivar txtPiP: displays the configuration factor for the connection.
    :ivar txtPiC: displays the construction factor for the connection.
    :ivar txtPiQ: displays the quality factor for the connection.
    :ivar txtPiE: displays the environment factor for the connection.
    """

    # Define private dict attributes.
    _dic_part_stress = {
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

    # Define private list attributes.
    _lst_labels = [
        u"\u03BB<sub>b</sub>:", u"\u03C0<sub>K</sub>:", u"\u03C0<sub>P</sub>:",
        u"\u03C0<sub>C</sub>:", u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Connection assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                connection.
        :param int subcategory_id: the ID of the connection subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        self._lblModel = rtk.RTKLabel(
            '',
            width=-1,
            tooltip=_(u"The assessment model used to calculate the connection "
                      u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the connection."))
        self.txtPiK = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The mating/unmating factor for the connection."))
        self.txtPiP = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The active pins factor for the connection."))
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The complexity factor for the connection."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the connection."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the connection."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the connection assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self.txtPiK.set_text(str(self.fmt.format(_attributes['piK'])))
        self.txtPiP.set_text(str(self.fmt.format(_attributes['piP'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected connection.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiK.set_sensitive(False)
        self.txtPiP.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiQ.set_sensitive(False)
        self.txtPiE.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id in [1, 2]:
                self.txtPiK.set_sensitive(True)
                self.txtPiP.set_sensitive(True)
            elif self._subcategory_id == 3:
                self.txtPiP.set_sensitive(True)
            elif self._subcategory_id == 4:
                self.txtPiC.set_sensitive(True)
                self.txtPiQ.set_sensitive(True)
            elif self._subcategory_id == 5:
                self.txtPiQ.set_sensitive(True)

        return _return

    def _make_assessment_results_page(self):
        """
        Make the connection gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        if _attributes['hazard_rate_method_id'] == 1:
            self._lblModel.set_markup(
                u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = "
                u"\u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>")
            self._lst_labels[0] = u"\u03BB<sub>g</sub>:"
        else:
            try:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id])
            except KeyError:
                self._lblModel.set_markup(_(u"Missing Model"))
            self._lst_labels[0] = u"\u03BB<sub>b</sub>:"

        self._do_set_sensitive()

        # Build the container for connections.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiK, _x_pos, _y_pos[1])
        self.put(self.txtPiP, _x_pos, _y_pos[2])
        self.put(self.txtPiC, _x_pos, _y_pos[3])
        self.put(self.txtPiQ, _x_pos, _y_pos[4])
        self.put(self.txtPiE, _x_pos, _y_pos[5])

        self.show_all()

        return None

    def on_select(self, module_id=None):
        """
        Load the connection assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              connection.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_set_sensitive()
        self._do_load_page()

        return _return


class StressResults(gtk.HPaned):
    """
    Display connection stress results attribute data in the RTK Work Book.

    The connection stress result view displays all the stress results for the
    selected connection.  This includes, currently, results for MIL-HDBK-217FN2
    parts count and MIL-HDBK-217FN2 part stress methods.  The attributes of a
    connection stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.
    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the connection
                               currently being displayed.

    :ivar pltDerate: matplotlib plot showing the design limits and operating
                     point for the connector.
    :ivar chkOverstress: the :py:class:`gtk.CheckButton` indicating whether or
                         not the connector is overstressed.
    :ivar txtReason: the :py:class:`rtk.gui.gtk.rtk.RTKTextView` displaying the
                     reason or reasons the connector is overstressed.
    :ivar txtVoltageRatio: the :py:class:`rtk.gui.gtk.rtk.RTKEntry` displaying
                           the operating to rated voltage ratio for the
                           connector.
    :ivar txtCurrentRatio: the :py:class:`rtk.gui.gtk.rtk.RTKEntry` displaying
                           the operating to rated current ratio for the
                           connector.
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Voltage Ratio:"),
        _(u"Current Ratio:"),
        _(u"Temperature Rise:"), "",
        _(u"Overstress Reason:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Connection assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                connection.
        :param int subcategory_id: the ID of the connection subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.7, 0.7, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.pltDerate = rtk.RTKPlot()

        self.chkOverstress = rtk.RTKCheckButton(
            label=_(u"Overstressed"),
            tooltip=_(u"Indicates whether or not the selected connection "
                      u"is overstressed."))
        self.txtReason = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=250,
            tooltip=_(u"The reason(s) the selected hardware item is "
                      u"overstressed."))
        self.txtVoltageRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating voltage to rated voltage for "
                      u"the connection."))
        self.txtCurrentRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating current to rated current for "
                      u"the connection."))
        self.txtTemperatureRise = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The temperature rise of the connector insert "
                      u"(multi-pin connectors) or contacts (PCB connectors)."))

        self.chkOverstress.set_sensitive(False)
        self.txtReason.set_editable(False)
        _bg_color = gtk.gdk.Color('#ADD8E6')
        self.txtReason.modify_base(gtk.STATE_NORMAL, _bg_color)
        self.txtReason.modify_base(gtk.STATE_ACTIVE, _bg_color)
        self.txtReason.modify_base(gtk.STATE_PRELIGHT, _bg_color)
        self.txtReason.modify_base(gtk.STATE_SELECTED, _bg_color)
        self.txtReason.modify_base(gtk.STATE_INSENSITIVE, _bg_color)

        self._make_stress_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_derating_curve(self):
        """
        Load the benign and harsh environment derating curves.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # Plot the derating curve.
        _x = [
            float(_attributes['temperature_rated_min']),
            float(_attributes['temperature_rated_max']),
            float(_attributes['temperature_rated_max'])
        ]

        self.pltDerate.axis.cla()
        self.pltDerate.axis.grid(True, which='both')

        self.pltDerate.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[0],
            plot_type='scatter',
            marker='r.-')

        self.pltDerate.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[1],
            plot_type='scatter',
            marker='b.-')

        self.pltDerate.do_load_plot(
            x_values=[_attributes['temperature_active']],
            y_values=[_attributes['voltage_ratio']],
            plot_type='scatter',
            marker='go')

        self.pltDerate.do_load_plot(
            x_values=[_attributes['temperature_active']],
            y_values=[_attributes['current_ratio']],
            plot_type='scatter',
            marker='mo')

        self.pltDerate.do_make_title(
            _(u"Voltage and Current Derating Curve for {0:s} at {1:s}").format(
                _attributes['part_number'], _attributes['ref_des']),
            fontsize=12)
        self.pltDerate.do_make_legend([
            _(u"Harsh Environment"),
            _(u"Mild Environment"),
            _(u"Voltage Operating Point"),
            _(u"Current Operating Point")
        ])

        self.pltDerate.do_make_labels(
            _(u"Temperature (\u2070C)"), 0, -0.2, fontsize=10)
        self.pltDerate.do_make_labels(
            _(u"Voltage Ratio"), -1, 0, set_x=False, fontsize=10)

        self.pltDerate.figure.canvas.draw()

        return _return

    def _do_load_page(self):
        """
        Load the connection assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtVoltageRatio.set_text(
            str(self.fmt.format(_attributes['voltage_ratio'])))
        self.txtCurrentRatio.set_text(
            str(self.fmt.format(_attributes['current_ratio'])))
        self.txtTemperatureRise.set_text(
            str(self.fmt.format(_attributes['temperature_rise'])))
        self.chkOverstress.set_active(_attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(_attributes['reason'])

        self._do_load_derating_curve()

        return _return

    def _make_stress_results_page(self):
        """
        Make the connection gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Create the left side.
        _fixed = gtk.Fixed()
        self.pack1(_fixed, True, True)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, _fixed, 5, 35)
        _x_pos += 50

        _fixed.put(self.txtVoltageRatio, _x_pos, _y_pos[0])
        _fixed.put(self.txtCurrentRatio, _x_pos, _y_pos[1])
        _fixed.put(self.txtTemperatureRise, _x_pos, _y_pos[2])
        _fixed.put(self.chkOverstress, _x_pos, _y_pos[3])
        _fixed.put(self.txtReason.scrollwindow, _x_pos, _y_pos[4])

        _fixed.show_all()

        # Create the derating plot.
        _frame = rtk.RTKFrame(label=_(u"Derating Curve and Operating Point"))
        _frame.add(self.pltDerate.plot)
        _frame.show_all()

        self.pack2(_frame, True, True)

        return _return

    def on_select(self, module_id=None):
        """
        Load the connection assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              connection.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_load_page()

        return _return
