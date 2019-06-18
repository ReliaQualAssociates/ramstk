# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.Switch.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKComboBox, RAMSTKEntry
from ramstk.gui.gtk.ramstk.Widget import _

# RAMSTK Local Imports
from .Component import AssessmentInputs, AssessmentResults


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
    _dic_keys = {
        0: 'quality_id',
        1: 'application_id',
        2: 'construction_id',
        3: 'contact_form_id',
        4: 'n_cycles',
        5: 'n_elements',
    }

    # Key is subcategory ID; index is application ID.
    _dic_applications = {
        1: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        2: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        3: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        4: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        5: [
            [_("Not Used as a Power On/Off Switch")],
            [_("Also Used as a Power On/Off Switch")],
        ],
    }
    # Key is subcategory ID; index is construction ID.
    _dic_constructions = {
        1: [[_("Snap Action")], [_("Non-Snap Action")]],
        2: [
            [_("Actuation Differential > 0.002 inches")],
            [_("Actuation Differential < 0.002 inches")],
        ],
        3: [[_("Ceramic RF Wafers")], [_("Medium Power Wafers")]],
        5: [[_("Magnetic")], [_("Thermal")], [_("Thermal-Magnetic")]],
    }
    # Key is subcategory ID; index is contact form ID.
    _dic_contact_forms = {
        1: [
            ["SPST"], ["DPST"], ["SPDT"], ["3PST"], ["4PST"], ["DPDT"],
            ["3PDT"], ["4PDT"], ["6PDT"],
        ],
        5: [["SPST"], ["DPST"], ["3PST"], ["4PST"]],
    }

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Application:"),
        _("Construction:"),
        _("Contact Form:"),
        _("Number of Cycles/Hour:"),
        _("Number of Active Contacts:"),
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Switch assessment input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentInputs.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication = RAMSTKComboBox(
            index=0, simple=True,
        )
        self.cmbConstruction = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbContactForm = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.txtNCycles = RAMSTKEntry()
        self.txtNElements = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __make_ui(self):
        """
        Make the Switch class Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_ui(self)

        self.put(self.cmbApplication, _x_pos, _y_pos[1])
        self.put(self.cmbConstruction, _x_pos, _y_pos[2])
        self.put(self.cmbContactForm, _x_pos, _y_pos[3])
        self.put(self.txtNCycles, _x_pos, _y_pos[4])
        self.put(self.txtNElements, _x_pos, _y_pos[5])

        self.show_all()

    def __set_callbacks(self):
        """
        Set callback methods for Switch assessment input widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self.on_combo_changed, 0),
        )
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self.on_combo_changed, 1),
        )
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self.on_combo_changed, 2),
        )
        self._lst_handler_id.append(
            self.cmbContactForm.connect('changed', self.on_combo_changed, 3),
        )
        self._lst_handler_id.append(
            self.txtNCycles.connect('changed', self.on_focus_out, 4),
        )
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self.on_focus_out, 5),
        )

    def __set_properties(self):
        """
        Set properties for Switch assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the switch."),
        )
        self.cmbConstruction.do_set_properties(
            tooltip=_(
                "The construction method for the switch.",
            ),
        )
        self.cmbContactForm.do_set_properties(
            tooltip=_("The contact form and quantity of the switch."),
        )
        self.txtNCycles.do_set_properties(
            width=125,
            tooltip=_("The number of cycles per hour of the switch."),
        )
        self.txtNElements.do_set_properties(
            width=125,
            tooltip=_("The number of active contacts in the switch."),
        )

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

    def _do_load_page(self, attributes):
        """
        Load the Switch assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Switch.
        :return: None
        :rtype: None
        """
        AssessmentInputs.do_load_page(self, attributes)

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
                str(self.fmt.format(attributes['n_cycles'])),
            )
            self.txtNCycles.handler_unblock(self._lst_handler_id[4])

            self.txtNElements.handler_block(self._lst_handler_id[5])
            self.txtNElements.set_text(
                str(self.fmt.format(attributes['n_elements'])),
            )
            self.txtNElements.handler_unblock(self._lst_handler_id[5])

        self._do_set_sensitive()

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
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
    }

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Switch assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentResults.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>CYC</sub>:")
        self._lst_labels.append("\u03C0<sub>L</sub>:")
        self._lst_labels.append("\u03C0<sub>C</sub>:")
        self._lst_labels.append("\u03C0<sub>N</sub>:")
        self._lst_labels.append("\u03C0<sub>U</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiCYC = RAMSTKEntry()
        self.txtPiL = RAMSTKEntry()
        self.txtPiC = RAMSTKEntry()
        self.txtPiN = RAMSTKEntry()
        self.txtPiU = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __make_ui(self):
        """
        Make the switch Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_ui(self)

        self.put(self.txtPiCYC, _x_pos, _y_pos[3])
        self.put(self.txtPiL, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])
        self.put(self.txtPiN, _x_pos, _y_pos[6])
        self.put(self.txtPiU, _x_pos, _y_pos[7])

        self.show_all()

    def __set_properties(self):
        """
        Set properties for Switch assessment result widgets.

        :return: None
        :rtype: None
        """
        self._lblModel.set_tooltip_markup(
            _(
                "The assessment model used to calculate the switch failure "
                "rate.",
            ),
        )

        self.txtPiCYC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The cycling factor for the switch."),
        )
        self.txtPiL.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The load stress factor for the switch."),
        )
        self.txtPiC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The contact form and quantity factor for the switch."),
        )
        self.txtPiN.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The number of active contacts factor for the switch."),
        )
        self.txtPiU.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The use factor for the breaker."),
        )

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
