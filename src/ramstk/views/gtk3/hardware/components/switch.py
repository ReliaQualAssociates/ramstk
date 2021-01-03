# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.switch.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Work View."""

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
    """Display Switch assessment input attribute data in the RAMSTK Work Book.

    The Switch assessment input view displays all the assessment inputs for
    the selected switch.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a switch assessment input view are:

    :cvar dict _dic_applications: dictionary of switch applications.  Key is
        switch subcategory ID; values are lists of applications.
    :cvar dict _dic_construction: dictionary of switch construction methods.
        Key is switch subcategory ID; values are lists of construction methods.
    :cvar dict _dic_contact_forms: dictionary of switch contact forms.  Key is
        switch subcategory ID; values are lists of contact forms.

    :ivar cmbApplication: select and display the switch application.
    :ivar cmbConstruction: select and display the switch construction method.
    :ivar cmbContactForm: select and display the switch contact form.
    :ivar txtNCycles: enter and display the number of switch cycles/hour.
    :ivar txtNElements: enter and display the number of switch wafers.
    """

    # Define private dict class attributes.
    # Key is subcategory ID; index is application ID.
    _dic_applications = {
        1: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        2: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        3: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        4: [[_("Resistive")], [_("Inductive")], [_("Lamp")]],
        5: [[_("Not Used as a Power On/Off Switch")],
            [_("Also Used as a Power On/Off Switch")]],
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

    # Define private list class attributes.

    _lst_title: List[str] = ["", ""]

    # Define private scalar class attributes.
    _module: str = 'switch'
    _tablabel: str = ""
    _tabtooltip: str = ""

    def __init__(self) -> None:
        """Initialize an instance of the Switch assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['quality_id', 'integer'],
            1: ['application_id', 'integer'],
            2: ['construction_id', 'integer'],
            3: ['contact_form_id', 'integer'],
            4: ['n_cycles', 'integer'],
            5: ['n_elements', 'integer'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _("Quality Level:"),
            _("Application:"),
            _("Construction:"),
            _("Contact Form:"),
            _("Number of Cycles/Hour:"),
            _("Number of Active Contacts:")
        ]
        self._lst_tooltips: List[str] = [
            _("The quality level of the switch."),
            _("The application of the switch."),
            _("The construction method for the switch."),
            _("The contact form and quantity of the switch."),
            _("The number of cycles per hour of the switch."),
            _("The number of active contacts in the switch."),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactForm: RAMSTKComboBox = RAMSTKComboBox()

        self.txtNCycles: RAMSTKEntry = RAMSTKEntry()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'quality_id': [self.cmbQuality.do_update, 'changed', 0],
            'application_id': [self.cmbApplication.do_update, 'changed', 1],
            'construction_id': [self.cmbConstruction.do_update, 'changed', 2],
            'contact_form_id': [self.cmbContactForm.do_update, 'changed', 3],
            'n_cycles': [self.txtNCycles.do_update, 'changed', 4],
            'n_elements': [self.txtNElements.do_update, 'changed', 5],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.cmbApplication,
            self.cmbConstruction,
            self.cmbContactForm,
            self.txtNCycles,
            self.txtNElements,
        ]

        self.__set_properties()
        super().do_make_panel_fixed()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the switch RKTComboBox().

        :param subcategory_id: the subcategory ID of the selected capacitor.
            This is unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_("Lower")]],
                                      signal='changed')

        # Load the application RAMSTKComboBox().
        try:
            _data = self._dic_applications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data, signal='changed')

        # Load the construction RAMSTKComboBox().
        try:
            if self._hazard_rate_method_id == 1:
                _data = [[_("Thermal")], [_("Magnetic")]]
            else:
                _data = self._dic_constructions[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data, signal='changed')

        # Load the contact form RAMSTKComboBox().
        try:
            _data = self._dic_contact_forms[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbContactForm.do_load_combo(_data, signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Switch assessment input widgets.

        :param attributes: the attributes dictionary for the selected
        Switch.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        if self._hazard_rate_method_id == 2:
            self.cmbApplication.do_update(attributes['application_id'],
                                          signal='changed')
            self.cmbConstruction.do_update(attributes['construction_id'],
                                           signal='changed')
            self.cmbContactForm.do_update(attributes['contact_form_id'],
                                          signal='changed')
            self.txtNCycles.do_update(str(attributes['n_cycles']),
                                      signal='changed')
            self.txtNElements.do_update(str(attributes['n_elements']),
                                        signal='changed')

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected switch.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.cmbContactForm.set_sensitive(False)
        self.txtNCycles.set_sensitive(False)
        self.txtNElements.set_sensitive(False)

        if self._hazard_rate_method_id == 1 and self._subcategory_id == 5:
            self.cmbConstruction.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:
            self.cmbApplication.set_sensitive(True)

            self.__do_set_breaker_sensitive()
            self.__do_set_rotary_sensitive()
            self.__do_set_sensitive_sensitive()
            self.__do_set_thumbwheel_sensitive()
            self.__do_set_toggle_sensitive()

    def __do_set_breaker_sensitive(self) -> None:
        """Set the widgets to display circuit breaker switch inputs sensitive.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(True)
        self.cmbContactForm.set_sensitive(True)

    def __do_set_rotary_sensitive(self) -> None:
        """Set widgets for rotary switch assessment inputs sensitive.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(True)
        self.txtNCycles.set_sensitive(True)
        self.txtNElements.set_sensitive(True)

    def __do_set_sensitive_sensitive(self) -> None:
        """Set the widgets to display sensitive switch inputs sensitive.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(True)
        self.txtNElements.set_sensitive(True)
        self.txtNCycles.set_sensitive(True)

    def __do_set_thumbwheel_sensitive(self) -> None:
        """Set the widgets to display thumbwheel switch inputs sensitive.

        :return: None
        :rtype: None
        """
        self.txtNCycles.set_sensitive(True)
        self.txtNElements.set_sensitive(True)

    def __do_set_toggle_sensitive(self) -> None:
        """Set widgets for toggle switch assessment inputs sensitive.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(True)
        self.cmbContactForm.set_sensitive(True)
        self.txtNCycles.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """Set callback methods for Switch assessment input widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self.on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     self.on_changed_combo, 1,
                                                     'wvw_editing_hardware')
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      self.on_changed_combo, 2,
                                                      'wvw_editing_hardware')
        self.cmbContactForm.dic_handler_id[
            'changed'] = self.cmbContactForm.connect('changed',
                                                     self.on_changed_combo, 3,
                                                     'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtNCycles.dic_handler_id['changed'] = self.txtNCycles.connect(
            'changed', self.on_changed_entry, 4, 'wvw_editing_hardware')
        self.txtNElements.dic_handler_id[
            'changed'] = self.txtNElements.connect('changed',
                                                   self.on_changed_entry, 5,
                                                   'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for Switch assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties()

        # ----- ENTRIES
        self.txtNCycles.do_set_properties(tooltip=self._lst_tooltips[4],
                                          width=125)
        self.txtNElements.do_set_properties(tooltip=self._lst_tooltips[5],
                                            width=125)


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    """Display Switch assessment results attribute data.

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

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub"
        ">C</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub"
        ">E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub"
        ">E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (\u03BB<sub>b1</sub> "
        "+ \u03C0<sub>N</sub>\u03BB<sub>b2</sub>)\u03C0<sub>CYC</sub>\u03C0"
        "<sub>L</sub>\u03C0<sub>E</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span> "
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Switch assessment result view."""
        super().__init__()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            '\u03C0<sub>CYC</sub>:',
            '\u03C0<sub>L</sub>:',
            '\u03C0<sub>C</sub>:',
            '\u03C0<sub>N</sub>:',
            '\u03C0<sub>U</sub>:',
        ]
        self._lst_tooltips: List[str] = [
            _("The assessment model used to calculate the switch hazard "
              "rate."),
            _('The base hazard rate for the switch.'),
            _('The quality factor for the switch.'),
            _('The environment factor for the switch.'),
            _('The cycling factor for the switch.'),
            _('The load stress factor for the switch.'),
            _('The number of active contacts factor for the switch.'),
            _('The contact form and quantity factor for the switch.  This is '
              'the configuration factor for a circuit breaker.'),
            _('The use factor for the switch.'),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()
        self.txtPiN: RAMSTKEntry = RAMSTKEntry()
        self.txtPiU: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtPiCYC,
            self.txtPiL,
            self.txtPiN,
            self.txtPiC,
            self.txtPiU,
        ]

        super().do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the switch assessment results page.

        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.txtPiCYC.do_update(str(self.fmt.format(attributes['piCYC'])))
        self.txtPiL.do_update(str(self.fmt.format(attributes['piL'])))
        self.txtPiC.do_update(str(self.fmt.format(attributes['piC'])))
        self.txtPiN.do_update(str(self.fmt.format(attributes['piN'])))
        self.txtPiU.do_update(str(self.fmt.format(attributes['piU'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected switch.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

        self.txtPiCYC.set_sensitive(False)
        self.txtPiL.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiN.set_sensitive(False)
        self.txtPiU.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            self.txtPiQ.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)

            self.__do_set_breaker_sensitive()
            self.__do_set_rotary_sensitive()
            self.__do_set_sensitive_sensitive()
            self.__do_set_thumbwheel_sensitive()
            self.__do_set_toggle_sensitive()

    def __do_set_breaker_sensitive(self) -> None:
        """Set widgets for circuit breaker assessment results sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)
        self.txtPiU.set_sensitive(True)
        self.txtPiC.set_sensitive(True)

    def __do_set_rotary_sensitive(self) -> None:
        """Set widgets for rotary switch assessment results sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiCYC.set_sensitive(True)
        self.txtPiL.set_sensitive(True)

    def __do_set_sensitive_sensitive(self) -> None:
        """Set widgets for sensitive switch assessment results sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiCYC.set_sensitive(True)
        self.txtPiL.set_sensitive(True)
        self.txtPiN.set_sensitive(True)

    def __do_set_thumbwheel_sensitive(self) -> None:
        """Set widgets for thumbwheel switch assessment results sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiCYC.set_sensitive(True)
        self.txtPiL.set_sensitive(True)

    def __do_set_toggle_sensitive(self) -> None:
        """Set widgets for toggle switch assessment results sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiCYC.set_sensitive(True)
        self.txtPiL.set_sensitive(True)
        self.txtPiC.set_sensitive(True)
