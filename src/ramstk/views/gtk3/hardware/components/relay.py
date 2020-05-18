# -*- coding: utf-8 -*-
#
#       views.gtk3.hardware.components.relay.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay Work View."""

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
    Display Relay assessment input attribute data in the RAMSTK Work Book.

    The Relay assessment input view displays all the assessment inputs for
    the selected relay.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Relay assessment input view are:

    :cvar dict _dic_specifications: dictionary of relay MIL-SPECs.  Key is
        relay subcategory ID; values are lists of specifications.
    :cvar dict _dic_styles: dictionary of relay styles defined in the
        MIL-SPECs.  Key is relay subcategory ID; values are lists of styles.

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

    # Define private class dict attributes.
    _dic_keys = {
        0: 'quality_id',
        1: 'type_id',
        2: 'technology_id',
        3: 'contact_form_id',
        4: 'contact_rating_id',
        5: 'application_id',
        6: 'construction_id',
        7: 'n_cycles'
    }

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
        2: [[_("Solid State")], [_("Solid State Time Delay")], [_("Hybrid")]]
    }
    # Key is contact rating ID.  Index is application ID.
    _dic_application = {
        1: [[_("Dry Circuit")]],
        2:
        [[_("General Purpose")], [_("Sensitve (0 - 100mW)")], [_("Polarized")],
         [_("Vibrating Reed")], [_("High Speed")], [_("Thermal Time Delay")],
         [_("Electronic Time Delay, Non-Thermal")], [_("Latching, Magnetic")]],
        3: [[_("High Voltage")], [_("Medium Power")]],
        4: [[_("Contactors, High Current")]],
    }
    # First key is contact rating ID, second key is application ID.  Index is
    # construction ID.
    _dic_construction = {
        1: {
            1: [[_("Armature (Long)")], [_("Dry Reed")], [_("Mercury Wetted")],
                [_("Magnetic Latching")], [_("Balanced Armature")],
                [_("Solenoid")]]
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
            8: [
                [_("Dry Reed")],
                [_("Mercury Wetted")],
                [_("Balanced Armature")],
            ]
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

    # Define private class list attributes.

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

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'relay') -> None:
        """
        Initialize an instance of the Relay assessment input view.

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
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbLoadType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactForm: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbContactRating: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()

        self.txtCycles: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.cmbQuality, self.cmbType, self.cmbLoadType,
            self.cmbContactForm, self.cmbContactRating, self.cmbApplication,
            self.cmbConstruction, self.txtCycles
        ]

        self.__set_properties()
        self.__set_callbacks()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __do_load_application_combo(self) -> None:
        """
        Load the selections in the Relay application RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _contact_rating_id = int(self.cmbContactRating.get_active())
        try:
            _data = self._dic_application[_contact_rating_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data)

    def __do_load_construction_combo(self) -> None:
        """
        Load the selections in the Relay construction RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _application_id = int(self.cmbApplication.get_active())
        _contact_rating_id = int(self.cmbContactRating.get_active())
        try:
            _data = self._dic_construction[_contact_rating_id][_application_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data)

    def __do_load_quality_combo(self) -> None:
        """
        Load the selections in the Relay quality RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:
            _data = [[_("Established Reliability")], ["MIL-SPEC"],
                     [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

    def __do_load_type_combo(self) -> None:
        """
        Load the selections in the Relay type RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_types[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

    def __set_callbacks(self) -> None:
        """
        Set callback methods for Relay assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self._on_combo_changed, 0)
        # TODO: See issue #310.  The _lst_handler_id attribute will be
        #  retired once issue #310 is implemented completely.
        self._lst_handler_id.append(self.cmbQuality.dic_handler_id['changed'])

        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed', self._on_combo_changed, 1)
        self.cmbLoadType.dic_handler_id['changed'] = self.cmbLoadType.connect(
            'changed', self._on_combo_changed, 2)
        self.cmbContactForm.dic_handler_id[
            'changed'] = self.cmbContactForm.connect('changed',
                                                     self._on_combo_changed, 3)
        self.cmbContactRating.dic_handler_id[
            'changed'] = self.cmbContactRating.connect('changed',
                                                       self._on_combo_changed,
                                                       4)
        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     self._on_combo_changed, 5)
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      self._on_combo_changed,
                                                      6)

        self.txtCycles.dic_handler_id['changed'] = self.txtCycles.connect(
            'focus-out-event', self._on_focus_out, 7)

    def __set_properties(self) -> None:
        """
        Set properties for Relay assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbType.do_set_properties(tooltip=_("The relay type."))
        self.cmbLoadType.do_set_properties(
            tooltip=_("The type of load the relay is switching."))
        self.cmbContactForm.do_set_properties(
            tooltip=_("The contact form of the relay."))
        self.cmbContactRating.do_set_properties(
            tooltip=_("The rating of the relay contacts."))
        self.cmbApplication.do_set_properties(
            tooltip=_("The type of relay appliction."))
        self.cmbConstruction.do_set_properties(
            tooltip=_("The method of construction of the relay."))
        self.txtCycles.do_set_properties(
            width=125,
            tooltip=_("The number of relay on/off cycles per hour."))

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Relay assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Relay.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        self.cmbType.do_update(attributes['type_id'])

        if self._hazard_rate_method_id == 2:
            self.cmbLoadType.do_update(attributes['technology_id'])
            self.cmbContactForm.do_update(attributes['contact_form_id'])
            self.cmbContactRating.do_update(attributes['contact_rating_id'])

            self.__do_load_application_combo()
            self.cmbApplication.do_update(attributes['application_id'])

            self.__do_load_construction_combo()
            self.cmbConstruction.do_update(attributes['construction_id'])

            self.txtCycles.do_update(
                str(self.fmt.format(attributes['n_cycles'])), )

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
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

        if self._hazard_rate_method_id == 2 and self._subcategory_id == 1:
            self.cmbLoadType.set_sensitive(True)
            self.cmbContactForm.set_sensitive(True)
            self.cmbContactRating.set_sensitive(True)
            self.cmbApplication.set_sensitive(True)
            self.cmbConstruction.set_sensitive(True)
            self.txtCycles.set_sensitive(True)

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Retrieve RAMSTKCombo() changes and assign to Relay attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`gui.gtk.RAMSTKCombo`
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
        super().on_combo_changed(combo, index, 'wvw_editing_component')

        if index == 4:
            self.__do_load_application_combo()
        elif index == 5:
            self.__do_load_construction_combo()

    def _on_focus_out(
            self,
            entry: object,
            __event: Gdk.EventFocus,  # pylint: disable=unused-argument
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
            |   7   | txtCycles            |       |                      |
            +-------+----------------------+-------+----------------------+

        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_component')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """
        Load the Relay RAMSTKComboBox()s.

        :param int subcategory_id: the newly selected miscellaneous hardware
            item subcategory ID.
        :return: None
        :rtype: None
        """
        self.__do_load_quality_combo()
        self.__do_load_type_combo()

        self.cmbLoadType.do_load_combo(self._lst_technology)
        self.cmbContactForm.do_load_combo(self._lst_contact_form)
        self.cmbContactRating.do_load_combo(self._lst_contact_rating)


class AssessmentResults(RAMSTKAssessmentResults):
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

    # Define private class dict attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>CYC</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private class list attributes.
    _lst_tooltips = [
        _("The assessment model used to calculate the relay's failure rate."),
        _("The base hazard rate of the relay."),
        _("The quality factor for the relay."),
        _("The environment factor for the relay."),
        _("The contact form factor for the relay."),
        _("The cycling factor for the relay."),
        _("The application and construction factor for the relay."),
        _("The load stress factor for the relay.")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'relay') -> None:
        """
        Initialize an instance of the Relay assessment result view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>C</sub>:")
        self._lst_labels.append("\u03C0<sub>CYC</sub>:")
        self._lst_labels.append("\u03C0<sub>F</sub>:")
        self._lst_labels.append("\u03C0<sub>L</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCYC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiF: RAMSTKEntry = RAMSTKEntry()
        self.txtPiL: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets.append(self.txtPiC)
        self._lst_widgets.append(self.txtPiCYC)
        self._lst_widgets.append(self.txtPiF)
        self._lst_widgets.append(self.txtPiL)

        self.set_properties()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')
        pub.subscribe(self._do_load_page, 'succeed_calculate_hardware')

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Relay assessment results wodgets.

        :param dict attributes: the attributes dictionary for the selected
        Relay.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        # TODO: See issue #305.
        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))
        self.txtPiCYC.set_text(str(self.fmt.format(attributes['piCYC'])))
        self.txtPiF.set_text(str(self.fmt.format(attributes['piF'])))
        self.txtPiL.set_text(str(self.fmt.format(attributes['piL'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected relay.

        :return: None
        :rtype: None
        """
        super().do_set_sensitive()

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
