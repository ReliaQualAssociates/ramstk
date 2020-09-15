# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.Inductor.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor Work View."""

# Standard Library Imports
from typing import Any, Dict, List

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
    Display Inductor assessment input attribute data in the RAMSTK Work Book.

    The Inductor assessment input view displays all the assessment inputs for
    the selected inductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analysis.  The attributes of an
    Inductor assessment input view are:

    :cvar dict _dic_specifications: dictionary of inductor MIL-SPECs.  Key is
        inductor subcategory ID; values are lists of specifications.
    :cvar dict _dic_styles: dictionary of inductor styles defined in the
        MIL-SPECs.  Key is inductor subcategory ID; values are lists of styles.

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
    _dic_keys = {
        0: 'quality_id',
        1: 'specification_id',
        2: 'insulation_id',
        3: 'family_id',
        4: 'construction_id',
        5: 'area',
        6: 'weight'
    }

    _dic_insulation = {
        1: [[_("Insulation Class A")], [_("Insulation Class B")],
            [_("Insulation Class C")], [_("Insulation Class O")],
            [_("Insulation Class Q")], [_("Insulation Class R")],
            [_("Insulation Class S")], [_("Insulation Class T")],
            [_("Insulation Class U")], [_("Insulation Class V")]],
        2: [[_("Insulation Class A")], [_("Insulation Class B")],
            [_("Insulation Class C")], [_("Insulation Class F")],
            [_("Insulation Class O")]],
    }

    _dic_quality = {
        1: [["MIL-SPEC"], [_("Lower")]],
        2: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_("Lower")]]
    }

    _dic_specifications = {
        1: [["MIL-T-27"], ["MIL-T-21038"], ["MIL-T-55631"]],
        2: [["MIL-T-15305"], ["MIL-T-39010"]]
    }

    # Define private list class attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Specification:"),
        _("Insulation Class:"),
        _("Area:"),
        _("Weight:"),
        _("Family:"),
        _("Construction:")
    ]
    _lst_title: List[str] = ["", ""]

    # Define private scalar class attributes.
    _module: str = 'inductor'
    _tablabel: str = ""
    _tabtooltip: str = ""

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize an instance of the Inductor assessment input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbInsulation: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbFamily: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.txtArea: RAMSTKEntry = RAMSTKEntry()
        self.txtWeight: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.cmbQuality, self.cmbSpecification, self.cmbInsulation,
            self.txtArea, self.txtWeight, self.cmbFamily, self.cmbConstruction
        ]

        self.__set_properties()
        self.__set_callbacks()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __set_callbacks(self) -> None:
        """
        Set callback methods for Inductor assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self._on_combo_changed, 0)
        self.cmbSpecification.dic_handler_id[
            'changed'] = self.cmbSpecification.connect('changed',
                                                       self._on_combo_changed,
                                                       1)
        self.cmbInsulation.dic_handler_id[
            'changed'] = self.cmbInsulation.connect('changed',
                                                    self._on_combo_changed, 2)
        self.cmbFamily.dic_handler_id['changed'] = self.cmbFamily.connect(
            'changed', self._on_combo_changed, 3)
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      self._on_combo_changed,
                                                      4)
        self.txtArea.dic_handler_id['changed'] = self.txtArea.connect(
            'focus-out-event', self._on_focus_out, 5)
        self.txtWeight.dic_handler_id['changed'] = self.txtWeight.connect(
            'focus-out-event', self._on_focus_out, 6)

    def __set_properties(self) -> None:
        """
        Set properties for Inductor assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbInsulation.do_set_properties(
            tooltip=_("The insulation class of the inductive device."))
        self.cmbSpecification.do_set_properties(
            tooltip=_("The governing specification for the inductive "
                      "device."))
        self.cmbFamily.do_set_properties(
            tooltip=_("The application family of the transformer."))
        self.cmbConstruction.do_set_properties(
            tooltip=_("The method of construction of the coil."))

        self.txtArea.do_set_properties(
            width=125,
            tooltip=_("The case radiating surface (in square inches) of the "
                      "inductive device."))
        self.txtWeight.do_set_properties(
            width=125, tooltip=_("The transformer weight (in lbf)."))

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Inductor assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Inductor.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

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
                                     signal='changed')

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected inductor.

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

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Retrieve RAMSTKCombo() changes and assign to Capacitor attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
            with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    3    | cmbFamily        |
            +---------+------------------+---------+------------------+
            |    1    | cmbSpecification |    4    | cmbConstruction  |
            +---------+------------------+---------+------------------+
            |    2    | cmbInsulation    |         |                  |
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

            +-------+------------------------+-------+-------------------+
            | Index | Widget                 | Index | Widget            |
            +=======+========================+=======+===================+
            |   5   | txtArea                |   6   | txtWeight         |
            +-------+------------------------+-------+-------------------+

        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_component')

    def __do_load_family_combobox(self) -> None:
        """
        Load the family RAMSTKComboBox()

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
        """
        Load the insulation RAMSTKComboBox()

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_insulation[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbInsulation.do_load_combo(_data, signal='changed')

    def __do_load_quality_combobox(self) -> None:
        """
        Load the quality RAMSTKComboBox()

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
        """
        Load the specification RAMSTKComboBox()

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data, signal='changed')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """
        Load the Inductor RAMSTKComboBox()s.

        :param int subcategory_id: the newly selected inductor subcategory ID.
        :return: None
        :rtype: None
        """
        self.__do_load_family_combobox()
        self.__do_load_insulation_combobox()
        self.__do_load_quality_combobox()
        self.__do_load_specification_combobox()

        self.cmbConstruction.do_load_combo([[_("Fixed")], [_("Variable")]],
                                           signal='changed')


class AssessmentResults(RAMSTKAssessmentResults):
    """
    Display Inductor assessment results attribute data in the RAMSTK Work Book.

    The Inductor assessment result view displays all the assessment results
    for the selected inductor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of an
    Inductor assessment result view are:

    :ivar txtPiC: displays the construction factor for the inductor.
    """

    # Define private list attributes.
    _lst_title: List[str] = ["", ""]

    # Define private scalar class attributes.
    _module: str = 'inductor'
    _tablabel: str = ""
    _tabtooltip: str = ""

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize an instance of the Inductor assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        super().__init__(configuration, logger)

        # Initialize private dict attributes.
        self._dic_part_stress = {
            1:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            2:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        }

        # Initialize private list attributes.
        self._lst_callbacks: List[str] = []
        self._lst_icons: List[str] = []
        self._lst_tooltips: List[str] = []

        self._lst_labels.append("\u03C0<sub>C</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dict attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets.append(self.txtPiC)

        self.__set_properties()
        self.make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __set_properties(self) -> None:
        """
        Set properties for Inductor assessment result widgets.

        :return: None
        :rtype: None
        """
        self._lblModel.set_tooltip_markup(
            _("The assessment model used to calculate the inductive device's "
              "hazard rate."))

        self.txtPiC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The construction factor for the coil."))

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the inductive device assessment results widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Inductor.
        :return: None
        :rtype: None
        """
        super().do_load_page(attributes)

        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiC.do_update(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected inductor.

        :return: None
        :rtype: None
        """
        super().do_set_sensitive()

        self.txtPiC.set_sensitive(False)

        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtPiC.set_sensitive(False)
            self.txtPiE.set_sensitive(False)
        else:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 2:
                self.txtPiC.set_sensitive(True)
