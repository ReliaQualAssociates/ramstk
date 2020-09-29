# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.Inductor.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor Work View."""

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
    """Displays Inductor assessment input attribute data.

    The Inductor assessment input view displays all the assessment inputs for
    the selected inductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analysis.  The attributes of an
    Inductor assessment input view are:

    :cvar _dic_insulation: dictionary of insulation classes.  Key is
        inductor subcategory ID; values are lists of insulation classes.
    :cvar dict _dic_specifications: dictionary of inductor MIL-SPECs.  Key is
        inductor subcategory ID; values are lists of specifications.

    :ivar _dic_attribute_keys: dictionary to provide a "Rosetta Stone" for
        the widget index (key) and the attribute name and data type (value).
    :ivar _dic_attribute_updater: dictionary to provide a "Rosetta Stone"
        for the attribute name (key) and the method and signal name (value)
        that updates the widget on this view.  This dictionary is used to
        have the widgets on this panel updated when changes are made in the
        module view.
    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.
    :ivar _lst_widgets: the list of widgets to display in the panel.  These
        are listed in the order they should appear on the panel.

    :ivar _hazard_rate_method_id: the ID of the method to use for estimating
        the Hardware item's hazard rate.
    :ivar _subcategory_id: the ID of the Hardware item's subcategory.
    :ivar _title: the text to put on the RAMSTKFrame() holding the
        assessment input widgets.

    :ivar fmt: the formatting to use when displaying float values.
    :ivar cmbInsulation: select and display the insulation class of the
        inductor.
    :ivar cmbSpecification: select and display the governing specification for
        the inductor.
    :ivar cmbConstruction: select and display the method of construction of the
        inductor.
    :ivar cmbFamily: select and display the family of the transformer.
    :ivar txtArea: enter and display the heat dissipating area of the inductor.
    :ivar txtWeight: enter and display the weight of the inductor.
    """

    # Define private dict class attributes.
    _dic_insulation: Dict[int, List[Any]] = {
        1: [[_("Insulation Class A")], [_("Insulation Class B")],
            [_("Insulation Class C")], [_("Insulation Class O")],
            [_("Insulation Class Q")], [_("Insulation Class R")],
            [_("Insulation Class S")], [_("Insulation Class T")],
            [_("Insulation Class U")], [_("Insulation Class V")]],
        2: [[_("Insulation Class A")], [_("Insulation Class B")],
            [_("Insulation Class C")], [_("Insulation Class F")],
            [_("Insulation Class O")]],
    }

    _dic_quality: Dict[int, List[Any]] = {
        1: [["MIL-SPEC"], [_("Lower")]],
        2: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_("Lower")]]
    }

    _dic_specifications: Dict[int, List[Any]] = {
        1: [["MIL-T-27"], ["MIL-T-21038"], ["MIL-T-55631"]],
        2: [["MIL-T-15305"], ["MIL-T-39010"]]
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Inductor assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['quality_id', 'integer'],
            1: ['specification_id', 'integer'],
            2: ['insulation_id', 'integer'],
            3: ['family_id', 'integer'],
            4: ['construction_id', 'integer'],
            5: ['area', 'float'],
            6: ['weight', 'float'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _("Quality Level:"),
            _("Specification:"),
            _("Insulation Class:"),
            _("Area:"),
            _("Weight:"),
            _("Family:"),
            _("Construction:"),
        ]

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = -1
        self._subcategory_id: int = -1
        self._title: str = _("Design Ratings")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbFamily: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbInsulation: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.txtArea: RAMSTKEntry = RAMSTKEntry()
        self.txtWeight: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater: Dict[str, Union[object, str]] = {
            'quality_id': [self.cmbQuality.do_update, 'changed'],
            'construction_id': [self.cmbConstruction.do_update, 'changed'],
            'family_id': [self.cmbFamily.do_update, 'changed'],
            'insulation_id': [self.cmbInsulation.do_update, 'changed'],
            'specification_id': [self.cmbSpecification.do_update, 'changed'],
            'area': [self.txtArea.do_update, 'changed'],
            'weight': [self.txtWeight.do_update, 'changed'],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.cmbSpecification,
            self.cmbInsulation,
            self.txtArea,
            self.txtWeight,
            self.cmbFamily,
            self.cmbConstruction,
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
        """Load the capacitor assessment input RAMSTKComboBox().

        :param subcategory_id: the subcategory ID of the selected capacitor.
            This is unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        self.__do_load_family_combobox()
        self.__do_load_insulation_combobox()
        self.__do_load_quality_combobox()
        self.__do_load_specification_combobox()

        self.cmbConstruction.do_load_combo([[_("Fixed")], [_("Variable")]],
                                           signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Inductor assessment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Inductor.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']
        self._subcategory_id = attributes['subcategory_id']

        self.do_load_comboboxes(attributes['subcategory_id'])
        self._do_set_sensitive()

        self.cmbQuality.do_update(attributes['quality_id'], signal='changed')

        self.cmbFamily.do_update(attributes['family_id'], signal='changed')

        if self._hazard_rate_method_id == 2:
            self.cmbSpecification.do_update(attributes['specification_id'],
                                            signal='changed')
            self.cmbInsulation.do_update(attributes['insulation_id'],
                                         signal='changed')
            self.cmbConstruction.do_update(attributes['construction_id'],
                                           signal='changed')
            self.txtArea.do_update(str(self.fmt.format(attributes['area'])),
                                   signal='changed')
            self.txtWeight.do_update(str(self.fmt.format(
                attributes['weight'])),
                                     signal='changed')  # noqa

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected inductor.

        :return: None
        :rtype: None
        """
        self.cmbSpecification.set_sensitive(False)
        self.cmbInsulation.set_sensitive(False)
        self.cmbFamily.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtArea.set_sensitive(False)
        self.txtWeight.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            self.cmbFamily.set_sensitive(True)
        else:
            self.cmbSpecification.set_sensitive(True)
            self.cmbInsulation.set_sensitive(True)
            self.txtArea.set_sensitive(True)
            self.txtWeight.set_sensitive(True)

            if self._subcategory_id == 1:
                self.cmbFamily.set_sensitive(True)

            if self._subcategory_id == 2:
                self.cmbConstruction.set_sensitive(True)

    def __do_load_family_combobox(self) -> None:
        """Load the family RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:
            if self._subcategory_id == 1:
                _data = [[_("Low Power Pulse Transformer")],
                         [_("Audio Transformer")],
                         [_("High Power Pulse and Power Transformer, Filter")],
                         [_("RF Transformer")]]
            else:
                _data = [[_("RF Coils, Fixed or Molded")],
                         [_("RF Coils, Variable")]]
        else:
            _data = [[_("Pulse Transformer")], [_("Audio Transformer")],
                     [_("Power Transformer or Filter")], [_("RF Transformer")]]
        self.cmbFamily.do_load_combo(_data, signal='changed')

    def __do_load_insulation_combobox(self) -> None:
        """Load the insulation RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_insulation[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbInsulation.do_load_combo(_data, signal='changed')

    def __do_load_quality_combobox(self) -> None:
        """Load the quality RAMSTKComboBox().

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
        self.cmbQuality.do_load_combo(_data, signal='changed')

    def __do_load_specification_combobox(self) -> None:
        """Load the specification RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data, signal='changed')

    def __set_callbacks(self) -> None:
        """Set callback methods for Inductor assessment input widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self.on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbSpecification.dic_handler_id[
            'changed'] = self.cmbSpecification.connect('changed',
                                                       self.on_changed_combo,
                                                       1,
                                                       'wvw_editing_hardware')
        self.cmbInsulation.dic_handler_id[
            'changed'] = self.cmbInsulation.connect('changed',
                                                    self.on_changed_combo, 2,
                                                    'wvw_editing_hardware')
        self.cmbFamily.dic_handler_id['changed'] = self.cmbFamily.connect(
            'changed', self.on_changed_combo, 3, 'wvw_editing_hardware')
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      self.on_changed_combo, 4,
                                                      'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtArea.dic_handler_id['changed'] = self.txtArea.connect(
            'changed', self.on_changed_text, 5, 'wvw_editing_hardware')
        self.txtWeight.dic_handler_id['changed'] = self.txtWeight.connect(
            'changed', self.on_changed_text, 6, 'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for Inductor assessment input widgets.

        :return: None
        :rtype: None
        """
        self.do_set_properties(bold=True, title=self._title)

        # ----- COMBOBOXES
        self.cmbInsulation.do_set_properties(
            tooltip=_("The insulation class of the inductive device."))
        self.cmbSpecification.do_set_properties(
            tooltip=_("The governing specification for the inductive "
                      "device."))
        self.cmbFamily.do_set_properties(
            tooltip=_("The application family of the transformer."))
        self.cmbConstruction.do_set_properties(
            tooltip=_("The method of construction of the coil."))

        # ----- ENTRIES
        self.txtArea.do_set_properties(tooltip=_(
            "The case radiating surface (in square inches) of the "
            "inductive device."),
                                       width=125)  # noqa
        self.txtWeight.do_set_properties(
            tooltip=_("The transformer weight (in lbf)."), width=125)


class AssessmentResultPanel(RAMSTKPanel):
    """Displays Inductor assessment results attribute data.

    The Inductor assessment result view displays all the assessment results
    for the selected inductor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of an
    Inductor assessment result view are:

    :cvar dict _dic_part_stress: dictionary of MIL-HDBK-217F part stress
        models.  The key is the subcategory ID attribute of the component.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.

    :ivar _hazard_rate_method_id: the ID of the method to use for estimating
        the Hardware item's hazard rate.
    :ivar _subcategory_id: the ID of the Hardware item's subcategory.

    :ivar fmt: the formatting to use when displaying float values.
    :ivar lblModel: displays the hazard rate model use to estimate the
        Hardware item's hazard rate.
    :ivar self.txtLambdaB: displays the base hazard rate for the Hardware
        item.
    :ivar txtPiC: displays the construction factor for the Hardware item.
    :ivar txtPiE: displays the environment factor for the Hardware item.
    :ivar txtPiQ: displays the quality factor for the Hardware item.
    """

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0"
        "<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private list attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Inductor assessment result view."""
        super().__init__()

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            '\u03C0<sub>C</sub>:',
        ]

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = -1
        self._subcategory_id: int = -1

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lblModel: RAMSTKLabel = RAMSTKLabel('')

        self.txtLambdaB: RAMSTKEntry = RAMSTKEntry()
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiE: RAMSTKEntry = RAMSTKEntry()
        self.txtPiQ: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtPiC,
        ]

        self.do_make_panel_fixed()
        self.__set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')
        pub.subscribe(self._do_load_panel, 'succeed_calculate_hardware')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the inductive device assessment results widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Inductor.
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

        self.txtPiC.do_update(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected inductor.

        :return: None
        :rtype: None
        """
        self.txtPiC.set_sensitive(False)
        self.txtPiQ.set_sensitive(True)

        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtPiC.set_sensitive(False)
            self.txtPiE.set_sensitive(False)
        else:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 2:
                self.txtPiC.set_sensitive(True)

    def __set_properties(self) -> None:
        """Set properties for Inductor assessment result widgets.

        :return: None
        :rtype: None
        """
        self.lblModel.set_tooltip_markup(
            _("The assessment model used to calculate the inductive device's "
              "failure rate."))

        self.txtPiC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The construction factor for the inductive device."))
        self.txtPiE.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The environment factor for the inductive device.'))
        self.txtLambdaB.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The base hazard rate for the inductive device.'))
        self.txtPiQ.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_('The quality factor for the inductive device.'))
