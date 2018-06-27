# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Relay.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Relay Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _
from rtk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class RelayAssessmentInputs(AssessmentInputs):
    """
    Display Relay assessment input attribute data in the RTK Work Book.

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
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_(u"Lower")]],
        2: [["MIL-SPEC"], [_(u"Lower")]]
    }
    # Key is subcategory ID.  Index is type ID.
    _dic_pc_types = {
        1: [[_(u"General Purpose")], [_(u"Contactor, High Current")],
            [_(u"Latching")], [_(u"Reed")], [_(u"Thermal, Bi-Metal")],
            [_(u"Meter Movement")]],
        2: [[_(u"Solid State")], [_(u"Hybrid and Solid State Time Delay")]]
    }
    # Key is subcategory ID, index is type ID.
    _dic_types = {
        1: [[_("85C Rated")], [_("125C Rated")]],
        2: [[_(u"Solid State")], [_(u"Solid State Time Delay")],
            [_(u"Hybrid")]]
    }
    # Key is contact rating ID.  Index is application ID.
    _dic_application = {
        1: [[_(u"Dry Circuit")]],
        2: [[_(u"General Purpose")], [_(u"Sensitve (0 - 100mW)")],
            [_(u"Polarized")], [_(u"Vibrating Reed")], [_(u"High Speed")], [
                _(u"Thermal Time Delay")
            ], [_(u"Electronic Time Delay, Non-Thermal")],
            [_(u"Latching, Magnetic")]],
        3: [[_(u"High Voltage")], [_(u"Medium Power")]],
        4: [[_(u"Contactors, High Current")]]
    }
    # First key is contact rating ID, second key is application ID.  Index is
    # construction ID.
    _dic_construction = {
        1: {
            1: [[_(u"Armature (Long)")], [_(u"Dry Reed")],
                [_(u"Mercury Wetted")], [_(u"Magnetic Latching")],
                [_(u"Balanced Armature")], [_(u"Solenoid")]]
        },
        2: {
            1: [[_(u"Armature (Long)")], [_(u"Balanced Armature")],
                [_(u"Solenoid")]],
            2: [[_(u"Armature (LOng and Short)")], [_(u"Mercury Wetted")],
                [_(u"Magnetic Latching")], [_(u"Meter Movement")],
                [_(u"Balanced Armature")]],
            3: [[_(u"Armature (Short)")], [_(u"Meter Movement")]],
            4: [[_(u"Dry Reed")], [_(u"Mercury Wetted")]],
            5: [[_(u"Armature (Balanced and Short)")], [_(u"Dry Reed")]],
            6: [[_(u"Bimetal")]],
            8: [[_(u"Dry Reed")], [_(u"Mercury Wetted")],
                [_(u"Balanced Armature")]]
        },
        3: {
            1: [[_(u"Vacuum (Glass)")], [_(u"Vacuum (Ceramic)")]],
            2: [[_(u"Armature (Long and Short)")], [_(u"Mercury Wetted")],
                [_(u"Magnetic Latching")], [_(u"Mechanical Latching")],
                [_(u"Balanced Armature")], [_(u"Solenoid")]]
        },
        4: {
            1: [[_(u"Armature (Short)")], [_(u"Mechanical Latching")],
                [_(u"Balanced Armature")], [_(u"Solenoid")]]
        }
    }

    # Define private list attributes.
    # Index is the technology ID (load type).
    _lst_technology = [[_(u"Resistive")], [_(u"Inductive")], [_(u"Lamp")]]
    # Index is the contact form ID.
    _lst_contact_form = [["SPST"], ["DPST"], ["SPDT"], ["3PST"], ["4PST"],
                         ["DPDT"], ["3PDT"], ["4PDT"], ["6PDT"]]
    # Index is contact rating ID.
    _lst_contact_rating = [[_(u"Signal Current (low mV and mA)")],
                           [_(u"0 - 5 Amp")], [_(u"5 - 20 Amp")],
                           [_(u"20 - 600 Amp")]]

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Relay assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentInputs.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Type:"))
        self._lst_labels.append(_(u"Load Type"))
        self._lst_labels.append(_(u"Contact Form:"))
        self._lst_labels.append(_(u"Contact Rating:"))
        self._lst_labels.append(_(u"Application:"))
        self._lst_labels.append(_(u"Construction:"))
        self._lst_labels.append(_(u"Number of Cycles/Hour:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbType = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The relay type."))
        self.cmbLoadType = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The type of load the relay is switching."))
        self.cmbContactForm = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The contact form of the relay."))
        self.cmbContactRating = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The rating of the relay contacts."))
        self.cmbApplication = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The type of relay appliction."))
        self.cmbConstruction = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the relay."))
        self.txtCycles = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of relay on/off cycles per hour."))

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

    def _do_load_comboboxes(self, **kwargs):
        """
        Load the relay RKTComboBox()s.

        This method is used to load the specification RTKComboBox() whenever
        the relay subcategory is changed.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_comboboxes(self, **kwargs)

        # Load the quality level RTKComboBox().
        if _attributes['hazard_rate_method_id'] == 1:
            _data = [[_(u"Established Reliability")], ["MIL-SPEC"],
                     [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the relay type RTKComboBox().
        if _attributes['hazard_rate_method_id'] == 1:
            _data = self._dic_pc_types[self._subcategory_id]
        else:
            try:
                _data = self._dic_types[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbType.do_load_combo(_data)

        # Load the load type RTKComboBox().
        self.cmbLoadType.do_load_combo(self._lst_technology)

        # Load the contact form RTKComboBox().
        self.cmbContactForm.do_load_combo(self._lst_contact_form)

        # Load the contact rating RTKComboBox().
        self.cmbContactRating.do_load_combo(self._lst_contact_rating)

        return _return

    def _do_load_page(self, **kwargs):
        """
        Load the Relay assesment input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_page(self, **kwargs)

        self.cmbType.handler_block(self._lst_handler_id[1])
        self.cmbType.set_active(_attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[1])

        if _attributes['hazard_rate_method_id'] == 2:
            self.cmbLoadType.handler_block(self._lst_handler_id[2])
            self.cmbLoadType.set_active(_attributes['technology_id'])
            self.cmbLoadType.handler_unblock(self._lst_handler_id[2])

            self.cmbContactForm.handler_block(self._lst_handler_id[3])
            self.cmbContactForm.set_active(_attributes['contact_form_id'])
            self.cmbContactForm.handler_unblock(self._lst_handler_id[3])

            self.cmbContactRating.handler_block(self._lst_handler_id[4])
            self.cmbContactRating.set_active(_attributes['contact_rating_id'])
            # Load the application RTKComboBox().
            try:
                _data = self._dic_application[_attributes['contact_rating_id']]
            except KeyError:
                _data = []
            self.cmbApplication.do_load_combo(_data)
            self.cmbContactRating.handler_unblock(self._lst_handler_id[4])

            self.cmbApplication.handler_block(self._lst_handler_id[5])
            self.cmbApplication.set_active(_attributes['application_id'])
            # Load the construction RTKComboBox().
            try:
                _data = self._dic_construction[_attributes[
                    'contact_rating_id']][_attributes['application_id']]
            except KeyError:
                _data = []
            self.cmbConstruction.do_load_combo(_data)
            self.cmbApplication.handler_unblock(self._lst_handler_id[5])

            self.cmbConstruction.handler_block(self._lst_handler_id[6])
            self.cmbConstruction.set_active(_attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[6])

            self.txtCycles.handler_block(self._lst_handler_id[7])
            self.txtCycles.set_text(
                str(self.fmt.format(_attributes['n_cycles'])))
            self.txtCycles.handler_unblock(self._lst_handler_id[7])

        return _return

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected relay.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbType.set_sensitive(True)
        self.cmbLoadType.set_sensitive(False)
        self.cmbContactForm.set_sensitive(False)
        self.cmbContactRating.set_sensitive(False)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtCycles.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            if self._subcategory_id == 1:
                self.cmbLoadType.set_sensitive(True)
                self.cmbContactForm.set_sensitive(True)
                self.cmbContactRating.set_sensitive(True)
                self.cmbApplication.set_sensitive(True)
                self.cmbConstruction.set_sensitive(True)
                self.txtCycles.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_load_comboboxes(subcategory_id=self._subcategory_id)

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
        Retrieve RTKCombo() changes and assign to Relay attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   1   | cmbType          |   4   | cmbContactRating |
            +-------+------------------+-------+------------------+
            |   2   | cmbLoadType      |   5   | cmbApplication   |
            +-------+------------------+-------+------------------+
            |   3   | cmbContactForm   |   6   | cmbConstruction  |
            +-------+------------------+-------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _attributes = AssessmentInputs.on_combo_changed(self, combo, index)

        if _attributes:
            if index == 1:
                _attributes['type_id'] = int(combo.get_active())
            elif index == 2:
                _attributes['technology_id'] = int(combo.get_active())
            elif index == 3:
                _attributes['contact_form_id'] = int(combo.get_active())
            elif index == 4:
                _attributes['contact_rating_id'] = int(combo.get_active())
                # Load the application RTKComboBox().
                try:
                    _data = self._dic_application[_attributes[
                        'contact_rating_id']]
                except KeyError:
                    _data = []
                self.cmbApplication.do_load_combo(_data)
            elif index == 5:
                _attributes['application_id'] = int(combo.get_active())
                # Load the construction RTKComboBox().
                try:
                    _data = self._dic_construction[_attributes[
                        'contact_rating_id']][_attributes['application_id']]
                except KeyError:
                    _data = []
                self.cmbConstruction.do_load_combo(_data)
            elif index == 6:
                _attributes['construction_id'] = int(combo.get_active())

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

            +---------+-----------+---------+-----------+
            |  Index  | Widget    |  Index  | Widget    |
            +=========+===========+=========+===========+
            |    7    | txtcycles |         |           |
            +---------+-----------+---------+-----------+

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

            if index == 7:
                _attributes['n_cycles'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id, **kwargs):
        """
        Load the relay assessment input work view widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)


class RelayAssessmentResults(AssessmentResults):
    """
    Display Relay assessment results attribute data in the RTK Work Book.

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
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>CYC</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Relay assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentResults.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>C</sub>:")
        self._lst_labels.append(u"\u03C0<sub>CYC</sub>:")
        self._lst_labels.append(u"\u03C0<sub>F</sub>:")
        self._lst_labels.append(u"\u03C0<sub>L</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the relay's failure "
              u"rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The contact form factor for the relay."))
        self.txtPiCYC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The cycling factor for the relay."))
        self.txtPiF = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The application and construction factor for the "
                      u"relay."))
        self.txtPiL = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The load stress factor for the relay."))

        self._make_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self, **kwargs):
        """
        Load the Relay assessment results wodgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentResults.do_load_page(self, **kwargs)

        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiCYC.set_text(str(self.fmt.format(_attributes['piCYC'])))
        self.txtPiF.set_text(str(self.fmt.format(_attributes['piF'])))
        self.txtPiL.set_text(str(self.fmt.format(_attributes['piL'])))

        return _return

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected relay.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = AssessmentResults.do_set_sensitive(self, **kwargs)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiC.set_sensitive(False)
        self.txtPiCYC.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiL.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 1:
                self.txtPiC.set_sensitive(True)
                self.txtPiCYC.set_sensitive(True)
                self.txtPiF.set_sensitive(True)
                self.txtPiL.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the relay gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiC, _x_pos, _y_pos[3])
        self.put(self.txtPiCYC, _x_pos, _y_pos[4])
        self.put(self.txtPiF, _x_pos, _y_pos[5])
        self.put(self.txtPiL, _x_pos, _y_pos[6])

        return None

    def on_select(self, module_id, **kwargs):
        """
        Load the Relay assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              relay.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)
