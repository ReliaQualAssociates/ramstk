# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.Switch.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Switch Work View."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
# noinspection PyPackageRequirements
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry

# RAMSTK Local Imports
from .workview import RAMSTKAssessmentInputs, RAMSTKAssessmentResults


class AssessmentInputs(RAMSTKAssessmentInputs):
    """
    Display Switch assessment input attribute data in the RAMSTK Work Book.

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
    _dic_keys = {
        0: 'quality_id',
        1: 'application_id',
        2: 'construction_id',
        3: 'contact_form_id',
        4: 'n_cycles',
        5: 'n_elements'
    }

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
    _lst_labels = [
        _("Quality Level:"),
        _("Application:"),
        _("Construction:"),
        _("Contact Form:"),
        _("Number of Cycles/Hour:"),
        _("Number of Active Contacts:")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'switch') -> None:
        """
        Initialize an instance of the Switch assessment input view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactForm: RAMSTKComboBox = RAMSTKComboBox()
        self.txtNCycles: RAMSTKEntry = RAMSTKEntry()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.cmbQuality, self.cmbApplication, self.cmbConstruction,
            self.cmbContactForm, self.txtNCycles, self.txtNElements
        ]

        self.__set_properties()
        self.__set_callbacks()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __do_set_breaker_sensitive(self) -> None:
        """
        Set the widgets to display circuit breaker switch inputs sensitive.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(True)
        self.cmbContactForm.set_sensitive(True)

    def __do_set_rotary_sensitive(self) -> None:
        """
        Set the widgets to display rotary switch assessment inputs sensitive.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(True)
        self.txtNCycles.set_sensitive(True)
        self.txtNElements.set_sensitive(True)

    def __do_set_sensitive_sensitive(self) -> None:
        """
        Set the widgets to display sensitive switch inputs sensitive.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(True)
        self.txtNElements.set_sensitive(True)
        self.txtNCycles.set_sensitive(True)

    def __do_set_thumbwheel_sensitive(self) -> None:
        """
        Set the widgets to display thumbwheel switch inputs sensitive.

        :return: None
        :rtype: None
        """
        self.txtNCycles.set_sensitive(True)
        self.txtNElements.set_sensitive(True)

    def __do_set_toggle_sensitive(self) -> None:
        """
        Set the widgets to display toggle switch assessment inputs sensitive.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.set_sensitive(True)
        self.cmbContactForm.set_sensitive(True)
        self.txtNCycles.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """
        Set callback methods for Switch assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self._on_combo_changed, 0)
        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     self._on_combo_changed, 1)
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      self._on_combo_changed,
                                                      2)
        self.cmbContactForm.dic_handler_id[
            'changed'] = self.cmbContactForm.connect('changed',
                                                     self._on_combo_changed, 3)
        self.txtNCycles.dic_handler_id['changed'] = self.txtNCycles.connect(
            'focus-out-event', self._on_focus_out, 4)
        self.txtNElements.dic_handler_id[
            'changed'] = self.txtNElements.connect('focus-out-event',
                                                   self._on_focus_out, 5)

    def __set_properties(self) -> None:
        """
        Set properties for Switch assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the switch."))
        self.cmbConstruction.do_set_properties(
            tooltip=_("The construction method for the switch."))
        self.cmbContactForm.do_set_properties(
            tooltip=_("The contact form and quantity of the switch."))
        self.txtNCycles.do_set_properties(
            width=125,
            tooltip=_("The number of cycles per hour of the switch."))
        self.txtNElements.do_set_properties(
            width=125,
            tooltip=_("The number of active contacts in the switch."))

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Switch assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Switch.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        if self._hazard_rate_method_id == 2:
            self.cmbApplication.do_update(attributes['application_id'],
                                          signal='changed')
            self.cmbConstruction.do_update(attributes['construction_id'],
                                           signal='changed')
            self.cmbContactForm.do_update(attributes['contact_form_id'],
                                          signal='changed')
            self.txtNCycles.do_update(str(
                self.fmt.format(attributes['n_cycles'])),
                                      signal='changed')
            self.txtNElements.do_update(str(
                self.fmt.format(attributes['n_elements'])),
                                        signal='changed')

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
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

        if self._hazard_rate_method_id == 1 and self._subcategory_id == 5:
            self.cmbConstruction.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:
            self.cmbApplication.set_sensitive(True)

            self.__do_set_breaker_sensitive()
            self.__do_set_rotary_sensitive()
            self.__do_set_sensitive_sensitive()
            self.__do_set_thumbwheel_sensitive()
            self.__do_set_toggle_sensitive()

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Retrieve RAMSTKCombo() changes and assign to Switch attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
            with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    2    | cmbConstruction  |
            +---------+------------------+---------+------------------+
            |    1    | cmbApplication   |    3    | cmbContactForm   |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        super().on_combo_changed(combo, index, 'wvw_editing_component')

    # pylint: disable=unused-argument
    def _on_focus_out(self, entry: object, __event: Gdk.EventFocus,
                      index: int) -> None:
        """
        Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'on-focus-out' signal
            * RAMSTKTextView() 'changed' signal

        :param object entry: the RAMSTKEntry() or RAMSTKTextView() that
            called this method.
        :param __event: the Gdk.EventFocus that triggered the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Hardware class Gtk.TreeModel()
            associated with the data from the calling Gtk.Widget().  Indices
            are:

            +-------+----------------------+-------+----------------------+
            | Index | Widget               | Index | Widget               |
            +=======+======================+=======+======================+
            |   4   | txtNCycles           |   5   | txtNElements         |
            +-------+----------------------+-------+----------------------+

        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_component')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """
        Load the switch RKTComboBox().

        This method is used to load the specification RAMSTKComboBox() whenever
        the switch subcategory is changed.

        :param int subcategory_id: the newly selected switch subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_("Lower")]],
                                      signal='changed')

        # Load the application RAMSTKCOmboBOx().
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


class AssessmentResults(RAMSTKAssessmentResults):
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

    # Define private dict class attributes.
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

    # Define private list class attributes.
    _lst_tooltips = [
        _("The assessment model used to calculate the switch failure rate."),
        _("The base hazard rate of the switch."),
        _("The quality factor for the switch."),
        _("The environment factor for the switch."),
        _("The cycling factor for the switch."),
        _("The load stress factor for the switch."),
        _("The contact form and quantity factor for the switch."),
        _("The number of active contacts factor for the switch."),
        _("The use factor for the circuit breaker.")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'switch') -> None:
        """
        Initialize an instance of the Switch assessment result view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module=module)

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
        self.txtPiCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiN: RAMSTKEntry = RAMSTKEntry()
        self.txtPiU: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets.append(self.txtPiCYC)
        self._lst_widgets.append(self.txtPiL)
        self._lst_widgets.append(self.txtPiN)
        self._lst_widgets.append(self.txtPiC)
        self._lst_widgets.append(self.txtPiU)

        self.set_properties()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')
        pub.subscribe(self._do_load_page, 'succeed_calculate_hardware')

    def __do_set_breaker_sensitive(self) -> None:
        """
        Set the widgets to display circuit breaker switch assessment results
        sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)
        self.txtPiU.set_sensitive(True)
        self.txtPiC.set_sensitive(True)

    def __do_set_rotary_sensitive(self) -> None:
        """
        Set the widgets to display rotary switch assessment results
        sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiCYC.set_sensitive(True)
        self.txtPiL.set_sensitive(True)

    def __do_set_sensitive_sensitive(self) -> None:
        """
        Set the widgets to display sensitive switch assessment results
        sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiCYC.set_sensitive(True)
        self.txtPiL.set_sensitive(True)
        self.txtPiN.set_sensitive(True)

    def __do_set_thumbwheel_sensitive(self) -> None:
        """
        Set the widgets to display thumbwheel switch assessment results
        sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiCYC.set_sensitive(True)
        self.txtPiL.set_sensitive(True)

    def __do_set_toggle_sensitive(self) -> None:
        """
        Set the widgets to display toggle switch assessment results sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiCYC.set_sensitive(True)
        self.txtPiL.set_sensitive(True)
        self.txtPiC.set_sensitive(True)

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the switch assessment results page.

        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        self.txtPiCYC.do_update(str(self.fmt.format(attributes['piCYC'])))
        self.txtPiL.do_update(str(self.fmt.format(attributes['piL'])))
        self.txtPiC.do_update(str(self.fmt.format(attributes['piC'])))
        self.txtPiN.do_update(str(self.fmt.format(attributes['piN'])))
        self.txtPiU.do_update(str(self.fmt.format(attributes['piU'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected switch.

        :return: None
        :rtype: None
        """
        super().do_set_sensitive()

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
