# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.miscellaneous.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Miscellaneous Parts Work View."""

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
    """Display Miscellaneous assessment input attribute data.

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
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize instance of the Miscellaneous assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['quality_id', 'integer'],
            1: ['application_id', 'integer'],
            2: ['type_id', 'integer'],
            3: ['frequency_operating', 'float'],
            4: ['duty_cycle', 'float'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _("Quality Level:"),
            _("Application:"),
            _("Type:"),
            _("Operating Frequency:"),
            _("Utilization:"),
        ]
        self._lst_tooltips: List[str] = [
            _('The quality level.'),
            _("The application of the lamp."),
            _("The type of electronic filter."),
            _("The operating frequency of the crystal."),
            _("The utilization factor (illuminate hours / equipment operate "
              "hours) of the lamp.")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()

        self.txtFrequency: RAMSTKEntry = RAMSTKEntry()
        self.txtUtilization: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'quality_id': [self.cmbQuality.do_update, 'changed', 0],
            'application_id': [self.cmbApplication.do_update, 'changed', 1],
            'type_id': [self.cmbType.do_update, 'changed', 2],
            'frequency_operating': [self.txtFrequency.do_update, 'changed', 3],
            'duty_cycle': [self.txtUtilization.do_update, 'changed', 4],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.cmbApplication,
            self.cmbType,
            self.txtFrequency,
            self.txtUtilization,
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
        """Load the miscellaneous assessment input RKTComboBox()s.

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
        self.cmbApplication.do_load_combo(
            [[_("Incandescent, AC")], [_("Incandescent, DC")]],
            signal='changed')

        # Load the type RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            self.cmbType.do_load_combo(
                [[_("Ceramic-Ferrite")], [_("Discrete LC Components")],
                 [_("Discrete LC and Crystal Components")]],
                signal='changed')
        elif self._hazard_rate_method_id == 2:
            self.cmbType.do_load_combo(
                [[_("MIL-F-15733 Ceramic-Ferrite")],
                 [_("MIL-F-15733 Discrete LC Components")],
                 [_("MIL-F-18327 Discrete LC Components")],
                 [_("MIL-F-18327 Discrete LC and Crystal Components")]],
                signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Miscellaneous assessment input widgets.

        :param attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        _dic_method = {
            1: self.__do_load_crystal,
            2: self.__do_load_filter,
            4: self.__do_load_lamp
        }
        try:
            # noinspection PyArgumentList
            _dic_method[self._subcategory_id](attributes)
        except KeyError:
            pass

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity for the selected Miscellaneous item.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(False)
        self.cmbQuality.set_sensitive(True)
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

    def __do_load_crystal(self, attributes: Dict[str, Any]) -> None:
        """Load the Crystal assessment input widgets.

        :param attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:
            self.txtFrequency.do_update(str(
                self.fmt.format(attributes['frequency_operating'])),
                                        signal='changed')  # noqa

    def __do_load_filter(self, attributes: Dict[str, Any]) -> None:
        """Load the Filter assessment input widgets.

        :param attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        self.cmbType.do_update(attributes['type_id'], signal='changed')

    def __do_load_lamp(self, attributes: Dict[str, Any]) -> None:
        """Load the Lamp assessment input widgets.

        :param attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        self.cmbApplication.do_update(attributes['application_id'],
                                      signal='changed')

        if self._hazard_rate_method_id == 2:
            self.txtUtilization.do_update(str(
                self.fmt.format(attributes['duty_cycle'])),
                                          signal='changed')  # noqa

    def __do_set_crystal_sensitive(self) -> None:
        """Set the widget sensitivity as needed for a Crystal.

        :return: None
        :rtype: None
        """
        self.cmbType.set_sensitive(True)
        self.cmbQuality.set_sensitive(True)

        if self._hazard_rate_method_id == 2:
            self.txtFrequency.set_sensitive(True)

    def __do_set_filter_sensitive(self) -> None:
        """Set the widget sensitivity as needed for a Filter.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)

    def __do_set_lamp_sensitive(self) -> None:
        """Set the widget sensitivity as needed for a Lamp.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(True)

        if self._hazard_rate_method_id == 2:
            self.txtUtilization.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """Set callback methods for Misc hardware assessment input widgets.

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
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed', self.on_changed_combo, 2, 'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtFrequency.dic_handler_id[
            'changed'] = self.txtFrequency.connect('changed',
                                                   self.on_changed_entry, 3,
                                                   'wvw_editing_hardware')
        self.txtUtilization.dic_handler_id[
            'changed'] = self.txtUtilization.connect('changed',
                                                     self.on_changed_entry, 4,
                                                     'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for Misc hardware assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties()

        # ----- ENTRIES
        self.txtFrequency.do_set_properties(tooltip=self._lst_tooltips[3],
                                            width=125)
        self.txtUtilization.do_set_properties(tooltip=self._lst_tooltips[4],
                                              width=125)


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    """Display Misc assessment results attribute data in the RAMSTK Work Book.

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

    # Define private dict class attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>U</sub>\u03C0<sub>A</sub>\u03C0<sub>E"
        "</sub></span> "
    }

    # Define private class list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize instance of the Miscellaneous assessment result view."""
        super().__init__()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            '\u03C0<sub>U</sub>:',
            '\u03C0<sub>A</sub>:',
        ]
        self._lst_tooltips: List[str] = [
            _("The assessment model used to calculate the hazard rate."),
            _('The base hazard rate.'),
            _('The quality factor.'),
            _('The environment factor.'),
            _('The utilization factor.'),
            _('The application factor.'),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiU: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtPiA,
            self.txtPiU,
        ]

        super().do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the miscellaneous devices assessment results page.

        :param attributes: the attributes dictionary for the selected
            Miscellaneous item.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.txtPiU.do_update(str(self.fmt.format(attributes['piU'])))
        self.txtPiA.do_update(str(self.fmt.format(attributes['piA'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected Misc hardware.

        :return: None
        :rtype: None
        """
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

    def __do_set_crystal_sensitive(self) -> None:
        """Set sensitive the widgets for displaying Crystal assessment results.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

    def __do_set_filter_sensitive(self) -> None:
        """Set sensitive the widgets for displaying Filter assessment results.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

    def __do_set_lamp_sensitive(self) -> None:
        """Set sensitive the widgets for displaying Filter assessment results.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:
            self.txtPiU.set_sensitive(True)
            self.txtPiA.set_sensitive(True)
