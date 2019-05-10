# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Switch.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                           AssessmentResults)


class SwitchAssessmentInputs(AssessmentInputs):
    """
    Display Switch assessment input attribute data in the RAMSTK Work Book.

    The Switch assessment input view displays all the assessment inputs for
    the selected switch.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a switch assessment input view are:

    :cvar dict _dic_applications: dictionary of switch applications.  Key is
                                  switch subcategory ID; values are lists
                                  of applications.
    :cvar dict _dic_construction: dictionary of switch construction methods.
                                  Key is switch subcategory ID; values are
                                  lists of construction methods.
    :cvar dict _dic_contact_forms: dictionary of switch contact forms.  Key is
                                   switch subcategory ID; values are lists of
                                   contact forms.

    :ivar cmbApplication: select and display the switch application.
    :ivar cmbConstruction: select and display the switch construction method.
    :ivar cmbContactForm: select and display the switch contact form.
    :ivar txtNCycles: enter and display the number of switch cycles/hour.
    :ivar txtNElements: enter and display the number of switch wafers.

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | cmbQuality - `changed`                    |
    +-------+-------------------------------------------+
    |   1   | cmbApplication - `changed`                |
    +-------+-------------------------------------------+
    |   2   | cmbConstruction - `changed`               |
    +-------+-------------------------------------------+
    |   3   | cmbContactForm - `changed`                |
    +-------+-------------------------------------------+
    |   4   | txtNCycles - `changed`                    |
    +-------+-------------------------------------------+
    |   5   | txtNElements - `changed`                  |
    +-------+-------------------------------------------+
    """

    # Define private dict attributes.
    # Key is subcategory ID; index is application ID.
    _dic_applications = {
        1: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        2: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        3: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        4: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        5: [[_("Not Used as a Power On/Off Switch")],
            [_("Also Used as a Power On/Off Switch")]]
    }
    # Key is subcategory ID; index is construction ID.
    _dic_constructions = {
        1: [[_("Snap Action")], [_("Non-Snap Action")]],
        2: [[_("Actuation Differential > 0.002 inches")],
            [_("Actuation Differential < 0.002 inches")]],
        3: [[_("Ceramic RF Wafers")], [_("Medium Power Wafers")]],
        5: [[_("Magnetic")], [_("Thermal")], [_("Thermal-Magnetic")]]
    }
    # Key is subcategory ID; index is contact form ID.
    _dic_contact_forms = {
        1: [["SPST"], ["DPST"], ["SPDT"], ["3PST"], ["4PST"], ["DPDT"],
            ["3PDT"], ["4PDT"], ["6PDT"]],
        5: [["SPST"], ["DPST"], ["3PST"], ["4PST"]]
    }

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Application:"),
        _("Construction:"),
        _("Contact Form:"),
        _("Number of Cycles/Hour:"),
        _("Number of Active Contacts:")
    ]

    def __init__(self, **kwargs):
        """Initialize an instance of the Switch assessment input view."""
        AssessmentInputs.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication = ramstk.RAMSTKComboBox(
            index=0, simple=True, tooltip=_("The application of the switch."))
        self.cmbConstruction = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The construction method for "
                      "the switch."))
        self.cmbContactForm = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The contact form and quantity of the switch."))
        self.txtNCycles = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_("The number of cycles per hour of the switch."))
        self.txtNElements = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_("The number of active contacts in the switch."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbContactForm.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.txtNCycles.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self._on_focus_out, 5))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def _do_load_comboboxes(self, subcategory_id):  # pylint: disable=unused-argument
        """
        Load the switch RKTComboBox().

        This method is used to load the specification RAMSTKComboBox() whenever
        the switch subcategory is changed.

        :param int subcategory_id: the newly selected semiconductor subcategory
                                   ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_("Lower")]])

        # Load the application RAMSTKCOmboBOx().
        try:
            _data = self._dic_applications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data)

        # Load the construction RAMSTKComboBox().
        try:
            if self._hazard_rate_method_id == 1:
                _data = [[_("Thermal")], [_("Magnetic")]]
            else:
                _data = self._dic_constructions[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data)

        # Load the contact form RAMSTKComboBox().
        try:
            _data = self._dic_contact_forms[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbContactForm.do_load_combo(_data)

        return None

    def _do_load_page(self, attributes):
        """
        Load the Switch assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Switch.
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

        if self._hazard_rate_method_id == 2:
            self.cmbApplication.handler_block(self._lst_handler_id[1])
            self.cmbApplication.set_active(attributes['application_id'])
            self.cmbApplication.handler_unblock(self._lst_handler_id[1])

            self.cmbConstruction.handler_block(self._lst_handler_id[2])
            self.cmbConstruction.set_active(attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[2])

            self.cmbContactForm.handler_block(self._lst_handler_id[3])
            self.cmbContactForm.set_active(attributes['contact_form_id'])
            self.cmbContactForm.handler_unblock(self._lst_handler_id[3])

            self.txtNCycles.handler_block(self._lst_handler_id[4])
            self.txtNCycles.set_text(
                str(self.fmt.format(attributes['n_cycles'])))
            self.txtNCycles.handler_unblock(self._lst_handler_id[4])

            self.txtNElements.handler_block(self._lst_handler_id[5])
            self.txtNElements.set_text(
                str(self.fmt.format(attributes['n_elements'])))
            self.txtNElements.handler_unblock(self._lst_handler_id[5])

        self._do_set_sensitive()

        return None

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected switch.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.cmbContactForm.set_sensitive(False)
        self.txtNCycles.set_sensitive(False)
        self.txtNElements.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            if self._subcategory_id == 5:
                self.cmbConstruction.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:
            self.cmbApplication.set_sensitive(True)
            if self._subcategory_id in [1, 2, 3, 5]:
                self.cmbConstruction.set_sensitive(True)
            if self._subcategory_id in [1, 5]:
                self.cmbContactForm.set_sensitive(True)
            if self._subcategory_id != 5:
                self.txtNCycles.set_sensitive(True)
            if self._subcategory_id in [2, 3, 4]:
                self.txtNElements.set_sensitive(True)

        return None

    def _make_page(self):
        """
        Make the Switch class Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.cmbApplication, _x_pos, _y_pos[1])
        self.put(self.cmbConstruction, _x_pos, _y_pos[2])
        self.put(self.cmbContactForm, _x_pos, _y_pos[3])
        self.put(self.txtNCycles, _x_pos, _y_pos[4])
        self.put(self.txtNElements, _x_pos, _y_pos[5])

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Switch attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   1   | cmbApplication   |   3   | cmbContactForm   |
            +-------+------------------+-------+------------------+
            |   2   | cmbConstruction  |       |                  |
            +-------+------------------+-------+------------------+

        :return: None
        :rtype: None
        """
        _dic_keys = {
            0: 'quality_id',
            1: 'application_id',
            2: 'construction_id',
            3: 'contact_form_id'
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

            +---------+---------------------+---------+---------------------+
            |  Index  | Widget              |  Index  | Widget              |
            +=========+=====================+=========+=====================+
            |    4    | txtNCycles          |    5    | txtNElements        |
            +---------+---------------------+---------+---------------------+

        :return: None
        :rtype: None
        """
        _dic_keys = {4: 'n_cycles', 5: 'n_elements'}
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


class SwitchAssessmentResults(AssessmentResults):
    """
    Display Switch assessment results attribute data in the RAMSTK Work Book.

    The Switch assessment result view displays all the assessment results
    for the selected switch.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a switch assessment result view are:

    :ivar txtPiC: displays the contact form and quantity factor for the switch.
    :ivar txtPiCYC: displays the cycling factor for the switch.
    :ivar txtPiL: displays the load stress factor for the switch.
    :ivar txtPiN: displays the number of active contacts factor for the switch.
    :ivar txtPiU: displays the use factor for the breaker.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (\u03BB<sub>b1</sub> + \u03C0<sub>N</sub>\u03BB<sub>b2</sub>)\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, **kwargs):
        """Initialize an instance of the Switch assessment result view."""
        AssessmentResults.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>CYC</sub>:")
        self._lst_labels.append("\u03C0<sub>L</sub>:")
        self._lst_labels.append("\u03C0<sub>C</sub>:")
        self._lst_labels.append("\u03C0<sub>N</sub>:")
        self._lst_labels.append("\u03C0<sub>U</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _("The assessment model used to calculate the switch failure "
              "rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiCYC = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The cycling factor for the switch."))
        self.txtPiL = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The load stress factor for the switch."))
        self.txtPiC = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The contact form and quantity factor for the switch."))
        self.txtPiN = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The number of active contacts factor for the switch."))
        self.txtPiU = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The use factor for the breaker."))

        self._make_page()
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def _do_load_page(self, attributes):
        """
        Load the switch assessment results page.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self.txtPiCYC.set_text(str(self.fmt.format(attributes['piCYC'])))
        self.txtPiL.set_text(str(self.fmt.format(attributes['piL'])))
        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))
        self.txtPiN.set_text(str(self.fmt.format(attributes['piN'])))
        self.txtPiU.set_text(str(self.fmt.format(attributes['piU'])))

        self._do_set_sensitive()

        return None

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected switch.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        self.txtPiCYC.set_sensitive(False)
        self.txtPiL.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiN.set_sensitive(False)
        self.txtPiU.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            self.txtPiQ.set_sensitive(True)
        else:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id != 5:
                self.txtPiCYC.set_sensitive(True)
                self.txtPiL.set_sensitive(True)
            if self._subcategory_id == 2:
                self.txtPiN.set_sensitive(True)
            if self._subcategory_id == 5:
                self.txtPiQ.set_sensitive(True)
                self.txtPiU.set_sensitive(True)
            if self._subcategory_id in [1, 5]:
                self.txtPiC.set_sensitive(True)

        return None

    def _make_page(self):
        """
        Make the switch Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiCYC, _x_pos, _y_pos[3])
        self.put(self.txtPiL, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])
        self.put(self.txtPiN, _x_pos, _y_pos[6])
        self.put(self.txtPiU, _x_pos, _y_pos[7])

        return None
