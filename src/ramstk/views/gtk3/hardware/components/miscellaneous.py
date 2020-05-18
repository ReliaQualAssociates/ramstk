# -*- coding: utf-8 -*-
#
#       views.gtk3.hardware.components.miscellaneous.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Miscellaneous Parts Work View."""

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
    Display Miscellaneous assessment input attribute data in RAMSTK WorkBook.

    The Miscellaneous hardware assessment input view displays all the
    assessment inputs for the selected miscellaneous hardware item.  This
    includes, currently, inputs for MIL-HDBK-217FN2.  The attributes of a
    Miscellaneous hardware assessment input view are:

    :ivar cmbApplication: select and display the application of the
        miscellaneous item (lamps only).
    :ivar cmbType: the type of miscellaneous item (filters only).
    :ivar txtFrequency: enter and display the operating frequency of the
        miscellaneous item (crystals only).
    :ivar txtUtilization: enter and display the utilization factor of the
        miscellaneous item (lamps only).

    Callbacks signals in _lst_handler_id:

    +-------+----------------------------+
    | Index | Widget - Signal            |
    +=======+============================+
    |   0   | cmbQuality - `changed`     |
    +-------+----------------------------+
    |   1   | cmbApplication - `changed` |
    +-------+----------------------------+
    |   2   | cmbType - `changed`        |
    +-------+----------------------------+
    |   3   | txtFrequency - `changed`   |
    +-------+----------------------------+
    |   4   | txtUtilization - `changed` |
    +-------+----------------------------+
    """

    # Define private dictionary attributes.
    _dic_keys = {
        0: 'quality_id',
        1: 'application_id',
        2: 'type_id',
        3: 'frequency_operating',
        4: 'duty_cycle'
    }

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Application:"),
        _("Type:"),
        _("Operating Frequency:"),
        _("Utilization:")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'miscellaneous') -> None:
        """
        Initialize an instance of the Miscellaneous assessment input view.

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
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()

        self.txtFrequency: RAMSTKEntry = RAMSTKEntry()
        self.txtUtilization: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.cmbQuality, self.cmbApplication, self.cmbType,
            self.txtFrequency, self.txtUtilization
        ]

        self.__set_properties()
        self.__set_callbacks()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __do_load_crystal(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Crystal assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """

        if self._hazard_rate_method_id == 2:
            self.txtFrequency.do_update(
                str(self.fmt.format(attributes['frequency_operating'])))

    def __do_load_filter(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Filter assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        self.cmbType.do_update(attributes['type_id'])

    def __do_load_lamp(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Lamp assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        self.cmbApplication.do_update(attributes['application_id'])

        if self._hazard_rate_method_id == 2:
            self.txtUtilization.do_update(
                str(self.fmt.format(attributes['duty_cycle'])))

    def __do_set_crystal_sensitive(self) -> None:
        """
        Set the widget sensitivity as needed for a Crystal.

        :return: None
        :rtype: None
        """
        self.cmbType.set_sensitive(True)
        self.cmbQuality.set_sensitive(True)

        if self._hazard_rate_method_id == 2:
            self.txtFrequency.set_sensitive(True)

    def __do_set_filter_sensitive(self) -> None:
        """
        Set the widget sensitivity as needed for a Filter.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)

    def __do_set_lamp_sensitive(self) -> None:
        """
        Set the widget sensitivity as needed for a Lamp.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(True)

        if self._hazard_rate_method_id == 2:
            self.txtUtilization.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """
        Set callback methods for Misc hardware assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self._on_combo_changed, 0)
        # TODO: See issue #310.  The _lst_handler_id attribute will be
        #  retired once issue #310 is implemented completely.
        self._lst_handler_id.append(self.cmbQuality.dic_handler_id['changed'])

        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     self._on_combo_changed, 1)
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed', self._on_combo_changed, 2)
        self.txtFrequency.dic_handler_id[
            'changed'] = self.txtFrequency.connect('focus-out-event',
                                                   self._on_focus_out, 3)
        self.txtUtilization.dic_handler_id[
            'changed'] = self.txtUtilization.connect('focus-out-event',
                                                     self._on_focus_out, 4)

    def __set_properties(self) -> None:
        """
        Set properties for Misc hardware assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the lamp."))
        self.cmbType.do_set_properties(
            tooltip=_("The type of electronic filter."))

        self.txtFrequency.do_set_properties(
            width=125, tooltip=_("The operating frequency of the crystal."))
        self.txtUtilization.do_set_properties(
            width=125,
            tooltip=_("The utilization factor (illuminate hours / equipment "
                      "operate hours) of the lamp."))

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Miscellaneous assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        _dic_method = {
            1: self.__do_load_crystal,
            2: self.__do_load_filter,
            4: self.__do_load_lamp
        }
        try:
            _dic_method[self._subcategory_id](attributes)
        except KeyError:
            pass

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected Miscellaneous item.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtFrequency.set_sensitive(False)
        self.txtUtilization.set_sensitive(False)

        _dic_method = {
            1: self.__do_set_crystal_sensitive,
            2: self.__do_set_filter_sensitive,
            4: self.__do_set_lamp_sensitive
        }
        try:
            _dic_method[self._subcategory_id]
        except KeyError:
            pass

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Retrieve RAMSTKCombo() changes and assign to Miscellaneous attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
            with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    2    | cmbType          |
            +---------+------------------+---------+------------------+
            |    1    | cmbApplication   |         |                  |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        super().on_combo_changed(combo, index, 'wvw_editing_component')

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
            |   3   | txtFrequency         |   4   | txtUtilization       |
            +-------+----------------------+-------+----------------------+

        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_component')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """
        Load the miscellaneous RKTComboBox()s.

        This method is used to load the specification RAMSTKComboBox() whenever
        the miscellaneous subcategory is changed.

        :param int subcategory_id: the newly selected miscellaneous hardware
            item subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_("Lower")]])

        # Load the application RAMSTKComboBox().
        self.cmbApplication.do_load_combo([[_("Incandescent, AC")],
                                           [_("Incandescent, DC")]])

        # Load the type RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            self.cmbType.do_load_combo(
                [[_("Ceramic-Ferrite")], [_("Discrete LC Components")],
                 [_("Discrete LC and Crystal Components")]])
        elif self._hazard_rate_method_id == 2:
            self.cmbType.do_load_combo(
                [[_("MIL-F-15733 Ceramic-Ferrite")],
                 [_("MIL-F-15733 Discrete LC Components")],
                 [_("MIL-F-18327 Discrete LC Components")],
                 [_("MIL-F-18327 Discrete LC and Crystal Components")]])


class AssessmentResults(RAMSTKAssessmentResults):
    """
    Display Misc assessment results attribute data in the RAMSTK Work Book.

    The Miscellaneous hardware item assessment result view displays all the
    assessment results for the selected miscellaneous hardware item.  This
    includes, currently, results for MIL-HDBK-217FN2 parts count and
    MIL-HDBK-217FN2 part stress methods.  The attributes of a miscellaneous
    hardware item assessment result view are:

    :ivar txtPiA: displays the application factor for the miscellaneous
        hardware item.
    :ivar txtPiU: displays the utilization factor for the miscellaneous
        hardware item.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>U</sub>\u03C0<sub>A</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private class list attributes.
    _lst_tooltips = [
        _("The assessment model used to calculate the miscellaneous item "
          "failure rate."),
        _("The base hazard rate of the miscellaneous item."),
        _("The quality factor for the miscellaneous item."),
        _("The environment factor for the miscellaneous item."),
        _("The utilization factor for the lamp."),
        _("The application factor for the lamp.")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'miscellaneous') -> None:
        """
        Initialize an instance of the Miscellaneous assessment result view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the RAMSTK workflow module.
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>U</sub>:")
        self._lst_labels.append("\u03C0<sub>A</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiU: RAMSTKEntry = RAMSTKEntry()
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets.append(self.txtPiU)
        self._lst_widgets.append(self.txtPiA)

        self.set_properties()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')
        pub.subscribe(self._do_load_page, 'succeed_calculate_hardware')

    def __do_set_crystal_sensitive(self) -> None:
        """
        Set sensitive the widgets for displaying Crystal assessment results.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

    def __do_set_filter_sensitive(self) -> None:
        """
        Set sensitive the widgets for displaying Filter assessment results.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

    def __do_set_lamp_sensitive(self) -> None:
        """
        Set sensitive the widgets for displaying Filter assessment results.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:
            self.txtPiU.set_sensitive(True)
            self.txtPiA.set_sensitive(True)

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the miscellaneous devices assessment results page.

        :param dict attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        # TODO: See issue #305.
        self.txtPiU.set_text(str(self.fmt.format(attributes['piU'])))
        self.txtPiA.set_text(str(self.fmt.format(attributes['piA'])))

        if (self._hazard_rate_method_id == 1
                and self._subcategory_id in [3, 4]):
            self._lblModel.set_markup(
                "<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = "
                "\u03BB<sub>g</sub></span>")

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected Misc hardware.

        :return: None
        :rtype: None
        """
        super().do_set_sensitive()

        self.txtPiU.set_sensitive(False)
        self.txtPiA.set_sensitive(False)
        self.txtPiQ.set_sensitive(False)
        self.txtPiE.set_sensitive(True)

        if self._hazard_rate_method_id == 1:
            self.txtPiE.set_sensitive(False)

        _dic_method = {
            1: self.__do_set_crystal_sensitive,
            2: self.__do_set_filter_sensitive,
            4: self.__do_set_lamp_sensitive
        }

        try:
            _dic_method[self._subcategory_id]
        except KeyError:
            pass
