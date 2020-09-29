# -*- coding: utf-8 -*-
#
#       views.gtk3.hardware.components.meter.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
# noinspection PyPackageRequirements
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox, RAMSTKEntry, RAMSTKLabel, RAMSTKPanel
)


class AssessmentInputPanel(RAMSTKPanel):
    """Display Meter assessment input attribute data in the RAMSTK Work Book.

    The Meter assessment input view displays all the assessment inputs for
    the selected Meter item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Meter assessment input view are:

    :cvar dict _dic_quality: dictionary of meter quality levels.  Key is
        meter subcategory ID; values are lists of quality levels.
    :cvar dict _dic_type: dictionary of meter types.  Key is meter
        subcategory ID; values are lists of types.
    :cvar dict _dic_specification: dictionary of meter MIL-SPECs.  Key is
        meter tye ID; values are lists of specifications.
    :cvar dict _dic_insert: dictionary of meter insert materials.  First
        key is meter type ID, second key is meter specification ID; values are
        lists of insert materials.

    :ivar cmbApplication: select and display the application of the meter.
    :ivar cmbType: select and display the type of meter.
    """

    # Define private dict class attributes.

    # Quality levels; key is the subcategory ID.
    _dic_quality = {
        2: [["MIL-SPEC"], [_("Lower")]],
        1: [["MIL-SPEC"], [_("Lower")]]
    }
    # Meter types; key is the subcategory ID.
    _dic_types = {
        1: [[_("AC")], [_("Inverter Driver")], [_("Commutator DC")]],
        2: [[_("Direct Current")], [_("Alternating Current")]]
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Meter assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys = {
            0: ['quality_id', 'integer'],
            1: ['application_id', 'integer'],
            2: ['type_id', 'integer'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _('Quality Level:'),
            _("Meter Type:"),
            _("Meter Function:"),
        ]

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = -1
        self._subcategory_id: int = -1
        self._title: str = _("Design Ratings")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()

        self._dic_attribute_updater: Dict[str, Union[object, str]] = {
            'quality_id': [self.cmbQuality.do_update, 'changed'],
            'application_id': [self.cmbApplication.do_update, 'changed'],
            'type_id': [self.cmbType.do_update, 'changed'],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.cmbType,
            self.cmbApplication,
        ]

        self.__set_properties()
        self.do_make_panel_fixed()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    # pylint: disable=unused-argument
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the meter assessment input RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected capacitor.
            This is unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            _data = [["MIL-SPEC"], [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data, signal='changed')

        # Load the meter application RAMSTKComboBox().
        self.cmbApplication.do_load_combo(
            [[_("Ammeter")], [_("Voltmeter")], [_("Other")]], signal='changed')

        # Load the meter type RAMSTKComboBox().
        try:
            _data = self._dic_types[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data, signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Meter assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
            Meter.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']
        self._subcategory_id = attributes['subcategory_id']

        self.do_load_comboboxes(attributes['subcategory_id'])
        self._do_set_sensitive()

        self.cmbQuality.do_update(attributes['quality_id'], signal='changed')

        self.cmbApplication.do_update(attributes['application_id'],
                                      signal='changed')
        self.cmbType.do_update(attributes['type_id'], signal='changed')

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected meter.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(False)
        self.cmbQuality.set_sensitive(True)
        self.cmbType.set_sensitive(True)

        if self._hazard_rate_method_id == 2 and self._subcategory_id == 2:
            self.cmbApplication.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """Set callback methods for Meter assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self.on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     self.on_changed_combo, 1,
                                                     'wvw_editing_hardware')
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed', self.on_changed_combo, 2, 'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for Meter assessment input widgets.

        :return: None
        :rtype: None
        """
        self.do_set_properties(bold=True, title=self._title)

        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the panel meter."))
        self.cmbType.do_set_properties(tooltip=_("The type of meter."))


class AssessmentResultPanel(RAMSTKPanel):
    """Display Meter assessment results attribute data in the RAMSTK Work Book.

    The Meter assessment result view displays all the assessment results
    for the selected meter.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a meter assessment result view are:

    :ivar txtPiA: displays the application factor for the panel meter.
    :ivar txtPiF: displays the function factor for the panel meter.
    :ivar txtPiT: displays the temperature stress factor for the elapsed time
        meter.
    """

    # Define private class dict class attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span> "
    }

    # Define private class list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Meter assessment result view."""
        super().__init__()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        # Initialize private list attributes.
        self._lst_labels = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            '\u03C0<sub>A</sub>:',
            '\u03C0<sub>F</sub>:',
            '\u03C0<sub>T</sub>:',
        ]

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = -1
        self._subcategory_id: int = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lblModel: RAMSTKLabel = RAMSTKLabel('')

        self.txtLambdaB: RAMSTKEntry = RAMSTKEntry()
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiE: RAMSTKEntry = RAMSTKEntry()
        self.txtPiF: RAMSTKEntry = RAMSTKEntry()
        self.txtPiQ: RAMSTKEntry = RAMSTKEntry()
        self.txtPiT: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtPiA,
            self.txtPiF,
            self.txtPiT,
        ]

        self.do_make_panel_fixed()
        self.__set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')
        pub.subscribe(self._do_load_panel, 'succeed_calculate_hardware')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the meter assessment results page.

        :param dict attributes: the attributes dictionary for the selected
            Meter.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        # Display the correct calculation model.
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.lblModel.set_markup(
                "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
                "\u03BB<sub>b</sub>\u03C0<sub>Q</sub></span>")
        elif self._hazard_rate_method_id == 2:  # MIL-HDBK-217F, Part Stress
            try:
                self.lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id])
            except KeyError:
                self.lblModel.set_markup("No Model")
        else:
            self.lblModel.set_markup("No Model")

        self.txtLambdaB.do_update(str(self.fmt.format(attributes['lambda_b'])))
        self.txtPiQ.do_update(str(self.fmt.format(attributes['piQ'])))
        self.txtPiE.do_update(str(self.fmt.format(attributes['piE'])))

        self.txtPiA.do_update(str(self.fmt.format(attributes['piA'])))
        self.txtPiF.do_update(str(self.fmt.format(attributes['piF'])))
        self.txtPiT.do_update(str(self.fmt.format(attributes['piT'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected meter.

        :return: None
        :rtype: None
        """
        self.txtPiA.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiT.set_sensitive(False)

        self.__do_set_part_stress_sensitive()

    def __do_set_part_stress_sensitive(self) -> None:
        """Set the widgets needed to display assessment results sensitive.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 1:
                self.txtPiT.set_sensitive(True)
                self.txtPiQ.set_sensitive(False)
            elif self._subcategory_id == 2:
                self.txtPiA.set_sensitive(True)
                self.txtPiF.set_sensitive(True)

    def __set_properties(self) -> None:
        """Set properties for Capacitor assessment result widgets.

        :return: None
        :rtype: None
        """
        self.lblModel.set_tooltip_markup(
            _("The assessment model used to calculate the meter failure "
              "rate."))

        self.txtLambdaB.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The base hazard rate for the meter.'))
        self.txtPiA.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The application factor for the meter.'))
        self.txtPiE.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The environment factor for the meter.'))
        self.txtPiF.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The function factor for the meter.'))
        self.txtPiQ.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The quality factor for the meter.'))
        self.txtPiT.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The temperature stress factor for the elapsed time '
                      'meter.'))
