# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Relay.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                           AssessmentResults)


class RelayAssessmentInputs(AssessmentInputs):
    """
    Display Relay assessment input attribute data in the RAMSTK Work Book.

    The Relay assessment input view displays all the assessment inputs for
    the selected relay.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Relay assessment input view are:

    :cvar dict _dic_specifications: dictionary of relay MIL-SPECs.  Key is
                                    relay subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of relay styles defined in the
                            MIL-SPECs.  Key is relay subcategory ID; values
                            are lists of styles.

    :ivar cmbType: select and display the type of relay.
    :ivar cmbLoadType: select and display the type of load the relay is
                       switching.
    :ivar cmbContactForm: select and display the form of the relay contacts.
    :ivar cmbContactRating: select and display the rating of the relay
                            contacts.
    :ivar cmbApplication: select and display the relay application.
    :ivar cmbConstruction: select and display the relay's method of
                           construction.
    :ivar txtCycles: enter and display the number of relay cycles per hour.

    Callbacks signals in _lst_handler_id:

    +-------+------------------------------+
    | Index | Widget - Signal              |
    +=======+==============================+
    |   0   | cmbQuality - `changed`       |
    +-------+------------------------------+
    |   1   | cmbType - `changed`          |
    +-------+------------------------------+
    |   2   | cmbLoadType - `changed`      |
    +-------+------------------------------+
    |   3   | cmbContactForm - `changed`   |
    +-------+------------------------------+
    |   4   | cmbContactRating - `changed` |
    +-------+------------------------------+
    |   5   | cmbApplication - `changed`   |
    +-------+------------------------------+
    |   6   | cmbConstruction - `changed`  |
    +-------+------------------------------+
    |   7   | txtCycles - `changed`        |
    +-------+------------------------------+
    """

    # Define private dict attributes.
    _dic_quality = {
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_("Lower")]],
        2: [["MIL-SPEC"], [_("Lower")]]
    }
    # Key is subcategory ID.  Index is type ID.
    _dic_pc_types = {
        1: [[_("General Purpose")], [_("Contactor, High Current")],
            [_("Latching")], [_("Reed")], [_("Thermal, Bi-Metal")],
            [_("Meter Movement")]],
        2: [[_("Solid State")], [_("Hybrid and Solid State Time Delay")]]
    }
    # Key is subcategory ID, index is type ID.
    _dic_types = {
        1: [[_("85C Rated")], [_("125C Rated")]],
        2: [[_("Solid State")], [_("Solid State Time Delay")],
            [_("Hybrid")]]
    }
    # Key is contact rating ID.  Index is application ID.
    _dic_application = {
        1: [[_("Dry Circuit")]],
        2: [[_("General Purpose")], [_("Sensitve (0 - 100mW)")],
            [_("Polarized")], [_("Vibrating Reed")], [_("High Speed")],
            [_("Thermal Time Delay")],
            [_("Electronic Time Delay, Non-Thermal")],
            [_("Latching, Magnetic")]],
        3: [[_("High Voltage")], [_("Medium Power")]],
        4: [[_("Contactors, High Current")]]
    }
    # First key is contact rating ID, second key is application ID.  Index is
    # construction ID.
    _dic_construction = {
        1: {
            1: [[_("Armature (Long)")], [_("Dry Reed")],
                [_("Mercury Wetted")], [_("Magnetic Latching")],
                [_("Balanced Armature")], [_("Solenoid")]]
        },
        2: {
            1: [[_("Armature (Long)")], [_("Balanced Armature")],
                [_("Solenoid")]],
            2: [[_("Armature (LOng and Short)")], [_("Mercury Wetted")],
                [_("Magnetic Latching")], [_("Meter Movement")],
                [_("Balanced Armature")]],
            3: [[_("Armature (Short)")], [_("Meter Movement")]],
            4: [[_("Dry Reed")], [_("Mercury Wetted")]],
            5: [[_("Armature (Balanced and Short)")], [_("Dry Reed")]],
            6: [[_("Bimetal")]],
            8: [[_("Dry Reed")], [_("Mercury Wetted")],
                [_("Balanced Armature")]]
        },
        3: {
            1: [[_("Vacuum (Glass)")], [_("Vacuum (Ceramic)")]],
            2: [[_("Armature (Long and Short)")], [_("Mercury Wetted")],
                [_("Magnetic Latching")], [_("Mechanical Latching")],
                [_("Balanced Armature")], [_("Solenoid")]]
        },
        4: {
            1: [[_("Armature (Short)")], [_("Mechanical Latching")],
                [_("Balanced Armature")], [_("Solenoid")]]
        }
    }

    # Define private list attributes.
    # Index is the technology ID (load type).
    _lst_technology = [[_("Resistive")], [_("Inductive")], [_("Lamp")]]
    # Index is the contact form ID.
    _lst_contact_form = [["SPST"], ["DPST"], ["SPDT"], ["3PST"], ["4PST"],
                         ["DPDT"], ["3PDT"], ["4PDT"], ["6PDT"]]
    # Index is contact rating ID.
    _lst_contact_rating = [[_("Signal Current (low mV and mA)")],
                           [_("0 - 5 Amp")], [_("5 - 20 Amp")],
                           [_("20 - 600 Amp")]]
    _lst_labels = [
        _("Quality Level:"),
        _("Type:"),
        _("Load Type"),
        _("Contact Form:"),
        _("Contact Rating:"),
        _("Application:"),
        _("Construction:"),
        _("Number of Cycles/Hour:")
    ]

    def __init__(self, **kwargs):
        """Initialize an instance of the Relay assessment input view."""
        AssessmentInputs.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbType = ramstk.RAMSTKComboBox(
            index=0, simple=True, tooltip=_("The relay type."))
        self.cmbLoadType = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The type of load the relay is switching."))
        self.cmbContactForm = ramstk.RAMSTKComboBox(
            index=0, simple=True, tooltip=_("The contact form of the relay."))
        self.cmbContactRating = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The rating of the relay contacts."))
        self.cmbApplication = ramstk.RAMSTKComboBox(
            index=0, simple=True, tooltip=_("The type of relay appliction."))
        self.cmbConstruction = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The method of construction of the relay."))
        self.txtCycles = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_("The number of relay on/off cycles per hour."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbLoadType.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbContactForm.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbContactRating.connect('changed', self._on_combo_changed,
                                          4))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 6))

        self._lst_handler_id.append(
            self.txtCycles.connect('changed', self._on_focus_out, 7))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the relay RKTComboBox()s.

        This method is used to load the specification RAMSTKComboBox() whenever
        the relay subcategory is changed.

        :param int subcategory_id: the newly selected miscellaneous hardware
                                   item subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            _data = [[_("Established Reliability")], ["MIL-SPEC"],
                     [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the relay type RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            try:
                _data = self._dic_types[subcategory_id]
            except KeyError:
                _data = []
        else:
            try:
                _data = self._dic_types[subcategory_id]
            except KeyError:
                _data = []
        self.cmbType.do_load_combo(_data)

        # Load the load type RAMSTKComboBox().
        self.cmbLoadType.do_load_combo(self._lst_technology)

        # Load the contact form RAMSTKComboBox().
        self.cmbContactForm.do_load_combo(self._lst_contact_form)

        # Load the contact rating RAMSTKComboBox().
        self.cmbContactRating.do_load_combo(self._lst_contact_rating)

        return None

    def _do_load_page(self, attributes):
        """
        Load the Relay assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Relay.
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

        self.cmbType.handler_block(self._lst_handler_id[1])
        self.cmbType.set_active(attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[1])

        if self._hazard_rate_method_id == 2:
            self.cmbLoadType.handler_block(self._lst_handler_id[2])
            self.cmbLoadType.set_active(attributes['technology_id'])
            self.cmbLoadType.handler_unblock(self._lst_handler_id[2])

            self.cmbContactForm.handler_block(self._lst_handler_id[3])
            self.cmbContactForm.set_active(attributes['contact_form_id'])
            self.cmbContactForm.handler_unblock(self._lst_handler_id[3])

            self.cmbContactRating.handler_block(self._lst_handler_id[4])
            self.cmbContactRating.set_active(attributes['contact_rating_id'])
            # Load the application RAMSTKComboBox().
            try:
                _data = self._dic_application[attributes['contact_rating_id']]
            except KeyError:
                _data = []
            self.cmbApplication.do_load_combo(_data)
            self.cmbContactRating.handler_unblock(self._lst_handler_id[4])

            self.cmbApplication.handler_block(self._lst_handler_id[5])
            self.cmbApplication.set_active(attributes['application_id'])
            # Load the construction RAMSTKComboBox().
            try:
                _data = self._dic_construction[attributes[
                    'contact_rating_id']][attributes['application_id']]
            except KeyError:
                _data = []
            self.cmbConstruction.do_load_combo(_data)
            self.cmbApplication.handler_unblock(self._lst_handler_id[5])

            self.cmbConstruction.handler_block(self._lst_handler_id[6])
            self.cmbConstruction.set_active(attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[6])

            self.txtCycles.handler_block(self._lst_handler_id[7])
            self.txtCycles.set_text(
                str(self.fmt.format(attributes['n_cycles'])))
            self.txtCycles.handler_unblock(self._lst_handler_id[7])

        self._do_set_sensitive()

        return None

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected relay.

        :return: None
        :rtype: None
        """
        self.cmbType.set_sensitive(True)
        self.cmbLoadType.set_sensitive(False)
        self.cmbContactForm.set_sensitive(False)
        self.cmbContactRating.set_sensitive(False)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtCycles.set_sensitive(False)

        if self._hazard_rate_method_id == 2:
            if self._subcategory_id == 1:
                self.cmbLoadType.set_sensitive(True)
                self.cmbContactForm.set_sensitive(True)
                self.cmbContactRating.set_sensitive(True)
                self.cmbApplication.set_sensitive(True)
                self.cmbConstruction.set_sensitive(True)
                self.txtCycles.set_sensitive(True)

        return None

    def _make_page(self):
        """
        Make the Hardware class Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.cmbType, _x_pos, _y_pos[1])
        self.put(self.cmbLoadType, _x_pos, _y_pos[2])
        self.put(self.cmbContactForm, _x_pos, _y_pos[3])
        self.put(self.cmbContactRating, _x_pos, _y_pos[4])
        self.put(self.cmbApplication, _x_pos, _y_pos[5])
        self.put(self.cmbConstruction, _x_pos, _y_pos[6])
        self.put(self.txtCycles, _x_pos, _y_pos[7])

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Relay attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   1   | cmbType          |   4   | cmbContactRating |
            +-------+------------------+-------+------------------+
            |   2   | cmbLoadType      |   5   | cmbApplication   |
            +-------+------------------+-------+------------------+
            |   3   | cmbContactForm   |   6   | cmbConstruction  |
            +-------+------------------+-------+------------------+

        :return: None
        :rtype: None
        """
        _dic_keys = {
            0: 'quality_id',
            1: 'type_id',
            2: 'technology_id',
            3: 'contact_form_id',
            4: 'contact_rating_id',
            5: 'application_id',
            6: 'construction_id'
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

        if index == 4:
            # Load the application RAMSTKComboBox().
            _contact_rating_id = int(self.cmbContactRating.get_active())
            try:
                _data = self._dic_application[_contact_rating_id]
            except KeyError:
                _data = []
            self.cmbApplication.do_load_combo(_data)
        elif index == 5:
            # Load the construction RAMSTKComboBox().
            _application_id = int(self.cmbApplication.get_active())
            _contact_rating_id = int(self.cmbContactRating.get_active())
            try:
                _data = self._dic_construction[_contact_rating_id][
                    _application_id]
            except KeyError:
                _data = []
            self.cmbConstruction.do_load_combo(_data)

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

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Widget().  Indices are:

            +---------+-----------+---------+-----------+
            |  Index  | Widget    |  Index  | Widget    |
            +=========+===========+=========+===========+
            |    7    | txtcycles |         |           |
            +---------+-----------+---------+-----------+

        :return: None
        :rtype: None
        """
        _dic_keys = {7: 'n_cycles'}
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = float(entry.get_text())
        except ValueError:
            _new_text = 0.0

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None


class RelayAssessmentResults(AssessmentResults):
    """
    Display Relay assessment results attribute data in the RAMSTK Work Book.

    The Relay assessment result view displays all the assessment results
    for the selected relay.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a relay assessment result view are:

    :ivar txtPiC: displays the contact form factor for the relay.
    :ivar txtPiCYC: displays the cycling factor for the relay.
    :ivar txtPiL: displays the load stress factor for the relay.
    :ivar txtPiF: displays the application and construction factor for the
                  relay.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>CYC</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, **kwargs):
        """Initialize an instance of the Relay assessment result view."""
        AssessmentResults.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>C</sub>:")
        self._lst_labels.append("\u03C0<sub>CYC</sub>:")
        self._lst_labels.append("\u03C0<sub>F</sub>:")
        self._lst_labels.append("\u03C0<sub>L</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _("The assessment model used to calculate the relay's failure "
              "rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The contact form factor for the relay."))
        self.txtPiCYC = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The cycling factor for the relay."))
        self.txtPiF = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The application and construction factor for the "
                      "relay."))
        self.txtPiL = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The load stress factor for the relay."))

        self._make_page()
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def _do_load_page(self, attributes):
        """
        Load the Relay assessment results wodgets.

        :param dict attributes: the attributes dictionary for the selected
                                Relay.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))
        self.txtPiCYC.set_text(str(self.fmt.format(attributes['piCYC'])))
        self.txtPiF.set_text(str(self.fmt.format(attributes['piF'])))
        self.txtPiL.set_text(str(self.fmt.format(attributes['piL'])))

        self._do_set_sensitive()

        return None

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected relay.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        self.txtPiC.set_sensitive(False)
        self.txtPiCYC.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiL.set_sensitive(False)

        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 1:
                self.txtPiC.set_sensitive(True)
                self.txtPiCYC.set_sensitive(True)
                self.txtPiF.set_sensitive(True)
                self.txtPiL.set_sensitive(True)

        return None

    def _make_page(self):
        """
        Make the relay Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiC, _x_pos, _y_pos[3])
        self.put(self.txtPiCYC, _x_pos, _y_pos[4])
        self.put(self.txtPiF, _x_pos, _y_pos[5])
        self.put(self.txtPiL, _x_pos, _y_pos[6])

        return None
