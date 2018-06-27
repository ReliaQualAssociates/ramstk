# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Connection.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Connection Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _
from rtk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class ConnectionAssessmentInputs(AssessmentInputs):
    """
    Display Connection assessment input attribute data in the RTK Work Book.

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

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Connection assessment input view.

        :param controller: the Hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentInputs.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Connector Type:"))
        self._lst_labels.append(_(u"Specification:"))
        self._lst_labels.append(_(u"Insert Material:"))
        self._lst_labels.append(_(u"Contact Gauge:"))
        self._lst_labels.append(_(u"Active Pins:"))
        self._lst_labels.append(_(u"Amperes/Contact:"))
        self._lst_labels.append(_(u"Mating/Unmating Cycles (per 1000 hours):"))
        self._lst_labels.append(_(u"Number of Wave Soldered PTH:"))
        self._lst_labels.append(_(u"Number of Hand Soldered PTH:"))
        self._lst_labels.append(_(u"Number of Circuit Planes:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
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

    def _do_load_comboboxes(self, **kwargs):
        """
        Load the connection RKTComboBox()s.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_comboboxes(self, **kwargs)

        # Load the quality level RTKComboBox().
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
        try:
            _data = self._dic_type[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

        # Clear the remaining rtk.ComboBox()s.  These are loaded dynamically
        # based on the selection made in other rtk.ComboBox()s.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        _model = self.cmbInsert.get_model()
        _model.clear()

        return _return

    def _do_load_page(self, **kwargs):
        """
        Load the Connection assessment input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_page(self, **kwargs)

        # Load the subcategory RTKComboBox.  We need to block the quality and
        # connector type RTKComboBoxes otherwise loading them causes the
        # respective attributes to be set to -1.
        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbType.handler_block(self._lst_handler_id[1])
        self._do_load_comboboxes(subcategory_id=_attributes['subcategory_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])
        self.cmbType.handler_unblock(self._lst_handler_id[1])

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

        return _return

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected connection.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

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

    def _make_page(self):
        """
        Make the Connection class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        self._do_load_comboboxes(subcategory_id=self._subcategory_id)
        self._do_set_sensitive()

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
            |    1    | cmbType          |    3    | cmbInsert        |
            +---------+------------------+---------+------------------+
            |    2    | cmbSpecification |         |                  |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _attributes = AssessmentInputs.on_combo_changed(self, combo, index)

        if _attributes:
            if index == 1:
                _attributes['type_id'] = int(combo.get_active())

                # Load the specification RTKComboBox().
                try:
                    _data = self._dic_specification[_attributes['type_id']]
                except KeyError:
                    _data = []
                self.cmbSpecification.do_load_combo(_data)

            elif index == 2:
                _attributes['specification_id'] = int(combo.get_active())

                # Load the connector insert material RTKComboBox().
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

    def on_select(self, module_id, **kwargs):
        """
        Load the connection assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              connection.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)


class ConnectionAssessmentResults(AssessmentResults):
    """
    Display Connection assessment results attribute data in the RTK Work Book.

    The connection assessment result view displays all the assessment results
    for the selected connection.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a connection assessment result view are:

    :ivar txtPiK: displays the capacitance factor for the connection.
    :ivar txtPiP: displays the configuration factor for the connection.
    :ivar txtPiC: displays the construction factor for the connection.
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

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Connection assessment result view.

        :param controller: the Hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentResults.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

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

        self._make_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the connection assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentResults.do_load_page(self)

        self.txtPiK.set_text(str(self.fmt.format(_attributes['piK'])))
        self.txtPiP.set_text(str(self.fmt.format(_attributes['piP'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))

        return _return

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected connection.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = AssessmentResults.do_set_sensitive(self, **kwargs)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiK.set_sensitive(False)
        self.txtPiP.set_sensitive(False)
        self.txtPiC.set_sensitive(False)

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

    def _make_page(self):
        """
        Make the connection gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiK, _x_pos, _y_pos[3])
        self.put(self.txtPiP, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])

        return None

    def on_select(self, module_id, **kwargs):
        """
        Load the connection assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              connection.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)
