# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.capacitor.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor Work View Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry

# RAMSTK Local Imports
from .panels import RAMSTKAssessmentInputPanel, RAMSTKAssessmentResultPanel


class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
    """Display Capacitor assessment input attribute data.

    The Capacitor assessment input view displays all the assessment inputs for
    the selected capacitor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analyses.  The attributes of a
    Capacitor assessment input view are:

    :cvar dict _dic_quality: dictionary of MIL-HDBK-217 capacitor quality
        levels.  Key is capacitor subcategory ID; values are lists of quality
        levels.
    :cvar dict _dic_specifications: dictionary of capacitor MIL-SPECs.  Key is
        capacitor subcategory ID; values are lists of specifications.
    :cvar dict _dic_styles: dictionary of capacitor styles defined in the
        MIL-SPECs.  Key is capacitor subcategory ID; values are lists of
        styles.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.
    :ivar _lst_widgets: the list of widgets to display in the panel.  These
        are listed in the order they should appear on the panel.

    :ivar cmbConfiguration: select and display the configuration of the
        capacitor.
    :ivar cmbConstruction: select and display the method of construction of the
        capacitor.
    :ivar cmbSpecification: select and display the governing specification of
        the capacitor.
    :ivar cmbStyle: select and display the style of the capacitor.
    :ivar txtCapacitance: enter and display the capacitance rating of the
        capacitor.
    :ivar txtESR: enter and display the equivalent series resistance.
    """

    # Define private dictionary class attributes.
    _dic_quality: Dict[int, List[Any]] = {
        1: [['MIL-SPEC'], [_('Lower')]],
        2: [['M'], [_('Non-Established Reliability')], [_('Lower')]],
        3: [
            'S', 'R', 'P', 'M', 'L',
            [_('MIL-C-19978 Non-Established Reliability')], [_('Lower')]
        ],
        4: [
            'S', 'R', 'P', 'M', 'L',
            [_('MIL-C-18312 Non-Established Reliability')], [_('Lower')]
        ],
        5: ['S', 'R', 'P', 'M', [_('Lower')]],
        6: ['S', 'R', 'P', 'M', [_('Lower')]],
        7: [
            'T', 'S', 'R', 'P', 'M', 'L',
            [_('MIL-C-5 Non-Established Reliability, Dipped')],
            [_('MIL-C-5 Non-Established Reliability, Molded')], [_('Lower')]
        ],
        8: [['MIL-C-10950'], [_('Lower')]],
        9: [
            'S', 'R', 'P', 'M', 'L',
            [_('MIL-C-11272 Non-Established Reliability')], [_('Lower')]
        ],
        10: [
            'S', 'R', 'P', 'M', 'L',
            [_('MIL-C-11015 Non-Established Reliability')], [_('Lower')]
        ],
        11:
        ['S', 'R', 'P', 'M', [_('Non-Established Reliability')], [_('Lower')]],
        12: ['D', 'C', 'S', 'B', 'R', 'P', 'M', 'L', [_('Lower')]],
        13: [
            'S', 'R', 'P', 'M', 'L',
            [_('MIL-C-3965 Non-Established Reliability')], [_('Lower')]
        ],
        14:
        ['S', 'R', 'P', 'M', [_('Non-Established Reliability')], [_('Lower')]],
        15: [['MIL-SPEC'], [_('Lower')]],
        16: [['MIL-SPEC'], [_('Lower')]],
        17: [['MIL-SPEC'], [_('Lower')]],
        18: [['MIL-SPEC'], [_('Lower')]],
        19: [['MIL-SPEC'], [_('Lower')]]
    }

    _dic_specifications: Dict[int, List[Any]] = {
        1: [['MIL-C-25'], ['MIL-C-12889']],
        2: [['MIL-C-11693']],
        3: [['MIL-C-14157'], ['MIL-C-19978']],
        4: [['MIL-C-18312'], ['MIL-C-39022']],
        5: [['MIL-C-55514']],
        6: [['MIL-C-83421']],
        7: [['MIL-C-5'], ['MIL-C-39001']],
        8: [['MIL-C-10950']],
        9: [['MIL-C-11272'], ['MIL-C-23269']],
        10: [['MIL-C-11015'], ['MIL-C-39014']],
        11: [['MIL-C-20'], ['MIL-C-55681']],
        12: [['MIL-C-39003']],
        13: [['MIL-C-3965'], ['MIL-C-39006']],
        14: [['MIL-C-39018']],
        15: [['MIL-C-62']],
        16: [['MIL-C-81']],
        17: [['MIL-C-14409']],
        18: [['MIL-C-92']],
        19: [['MIL-C-23183']]
    }

    _dic_styles: Dict[int, List[Any]] = {
        1: [[['CP4'], ['CP5'], ['CP8'], ['CP9'], ['CP10'], ['CP11'], ['CP12'],
             ['CP13'], ['CP25'], ['CP26'], ['CP27'], ['CP28'], ['CP29'],
             ['CP40'], ['CP41'], ['CP67'], ['CP69'], ['CP70'], ['CP72'],
             ['CP75'], ['CP76'], ['CP77'], ['CP78'], ['CP80'], ['CP81'],
             ['CP82']], [['CA']]],
        2: [[_('Characteristic E')], [_('Characteristic K')],
            [_('Characteristic P')], [_('Characteristic W')]],
        3: [[['CPV07'], ['CPV09'], ['CPV17']],
            [[_('Characteristic E')], [_('Characteristic F')],
             [_('Characteristic G')], [_('Characteristic K')],
             [_('Characteristic L')], [_('Characteristic M')],
             [_('Characteristic P')], [_('Characteristic Q')],
             [_('Characteristic S')], [_('Characteristic T')]]],
        4: [[[_('Characteristic N')], [_('Characteristic R')]],
            [[_('Characteristic 1')], [_('Characteristic 9')],
             [_('Characteristic 10')], [_('Characteristic 12')],
             [_('Characteristic 19')], [_('Characteristic 29')],
             [_('Characteristic 49')], [_('Characteristic 59')]]],
        5: [[_('Characteristic M')], [_('Characteristic N')],
            [_('Characteristic Q')], [_('Characteristic R')],
            [_('Characteristic S')]],
        6: [['CRH']],
        7: [
            [[_('Temperature Range M')], [_('Temperature Range N')],
             [_('Temperature Range O')], [_('Temperature Range P')]],
            [[_('Temperature Range O')], [_('Temperature Range P')]],
        ],
        8: [['CB50'], [_('Other')]],
        9: [
            [[_('Temperature Range C')], [_('Temperature Range D')]],
            [[_('All')]],
        ],
        10: [[[_('Type A Rated Temperature')], [_('Type B Rated Temperature')],
              [_('Type C Rated Temperature')]],
             [['CKR05'], ['CKR06'], ['CKR07'], ['CKR08'], ['CKR09'], ['CKR10'],
              ['CKR11'], ['CKR12'], ['CKR13'], ['CKR14'], ['CKR15'], ['CKR16'],
              ['CKR17'], ['CKR18'], ['CKR19'], ['CKR48'], ['CKR64'], ['CKR72'],
              ['CKR73'], ['CKR74']]],
        11: [[['CC5'], ['CC6'], ['CC7'], ['CC8'], ['CC9'], ['CC13'], ['CC14'],
              ['CC15'], ['CC16'], ['CC17'], ['CC18'], ['CC19'], ['CC20'],
              ['CC21'], ['CC22'], ['CC25'], ['CC26'], ['CC27'], ['CC30'],
              ['CC31'], ['CC32'], ['CC33'], ['CC35'], ['CC36'], ['CC37'],
              ['CC45'], ['CC47'], ['CC50'], ['CC51'], ['CC52'], ['CC53'],
              ['CC54'], ['CC55'], ['CC56'], ['CC57'], ['CC75'], ['CC76'],
              ['CC77'], ['CC78'], ['CC79'], ['CC81'], ['CC82'], ['CC83'],
              ['CC85'], ['CC95'], ['CC96'], ['CC97'], ['CCR05'], ['CCR06'],
              ['CCR07'], ['CCR08'], ['CCR09'], ['CCR13'], ['CCR14'], ['CCR15'],
              ['CCR16'], ['CCR17'], ['CCR18'], ['CCR19'], ['CCR54'], ['CCR55'],
              ['CCR56'], ['CCR57'], ['CCR75'], ['CCR76'], ['CCR77'], ['CCR78'],
              ['CCR79'], ['CCR81'], ['CCR82'], ['CCR83'], ['CCR90']],
             [['CDR']]],
        12: [['CSR']],
        13: [[['CL10'], ['CL13'], ['CL14'], ['CL16'], ['CL17'], ['CL18'],
              ['CL24'], ['CL25'], ['CL26'], ['CL27'], ['CL30'], ['CL31'],
              ['CL32'], ['CL33'], ['CL34'], ['CL35'], ['CL36'], ['CL37'],
              ['CL40'], ['CL41'], ['CL42'], ['CL43'], ['CL46'], ['CL47'],
              ['CL48'], ['CL49'], ['CL50'], ['CL51'], ['CL52'], ['CL53'],
              ['CL54'], ['CL55'], ['CL56'], ['CL64'], ['CL65'], ['CL66'],
              ['CL67'], ['CL70'], ['CL71'], ['CL72'], ['CL73']], [['CLR']]],
        14: [[_('Style 16')], [_('Style 17')], [_('Style 71')],
             [_('All Others')]],
        15: [['CE']],
        16: [['CV11'], ['CV14'], ['CV21'], ['CV31'], ['CV32'], ['CV34'],
             ['CV35'], ['CV36'], ['CV40'], ['CV41']],
        17: [[_('Style G')], [_('Style H')], [_('Style J')], [_('Style L')],
             [_('Style Q')], [_('Style T')]],
        18: [['CT']],
        19: [['CG20'], ['CG21'], ['CG30'], ['CG31'], ['CG32'], ['CG40'],
             ['CG41'], ['CG42'], ['CG43'], ['CG44'], ['CG50'], ['CG51'],
             ['CG60'], ['CG61'], ['CG62'], ['CG63'], ['CG64'], ['CG65'],
             ['CG66'], ['CG67']]
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Capacitor assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['quality_id', 'integer'],
            1: ['specification_id', 'integer'],
            2: ['type_id', 'integer'],
            3: ['configuration_id', 'integer'],
            4: ['construction_id', 'integer'],
            5: ['capacitance', 'float'],
            6: ['resistance', 'float'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _('Quality Level:'),
            _('Capacitance (F):'),
            _('Specification:'),
            _('Style:'),
            _('Configuration:'),
            _('Construction:'),
            _('Equivalent Series Resistance (\u03A9):'),
        ]
        self._lst_tooltips: List[str] = [
            _('The quality level of the capacitor.'),
            _('The capacitance rating (in farads) of the capacitor.'),
            _('The governing specification for the capacitor.'),
            _('The style of the capacitor.'),
            _('The configuration of the capacitor.'),
            _('The method of construction of the capacitor.'),
            _('The equivalent series resistance of the capacitor.'),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbConfiguration: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbStyle: RAMSTKComboBox = RAMSTKComboBox()

        self.txtCapacitance: RAMSTKEntry = RAMSTKEntry()
        self.txtESR: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'quality_id': [self.cmbQuality.do_update, 'changed', 0],
            'specification_id':
            [self.cmbSpecification.do_update, 'changed', 1],
            'type_id': [self.cmbStyle.do_update, 'changed', 2],
            'configuration_id':
            [self.cmbConfiguration.do_update, 'changed', 3],
            'construction_id': [self.cmbConstruction.do_update, 'changed', 4],
            'capacitance': [self.txtCapacitance.do_update, 'changed', 5],
            'resistance': [self.txtESR.do_update, 'changed', 6],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.txtCapacitance,
            self.cmbSpecification,
            self.cmbStyle,
            self.cmbConfiguration,
            self.cmbConstruction,
            self.txtESR,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the capacitor assessment input RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected capacitor.
            This is unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F parts count.
            _quality: List[Any] = [
                'S', 'R', 'P', 'M', 'L', ['MIL-SPEC'], [_('Lower')]
            ]
        else:
            try:
                _quality = self._dic_quality[self._subcategory_id]
            except KeyError:
                _quality = []

        self.cmbQuality.do_load_combo(_quality, signal='changed')

        try:
            _specification: List[Any] = self._dic_specifications[
                self._subcategory_id]
        except KeyError:
            _specification = []

        self.cmbSpecification.do_load_combo(_specification, signal='changed')

        self.cmbStyle.do_load_combo([], signal='changed')

        self.cmbConfiguration.do_load_combo([[_('Fixed')], [_('Variable')]],
                                            signal='changed')

        _construction: List[Any] = [[_('Slug, All Tantalum')],
                                    [_('Foil, Hermetic')],
                                    [_('Slug, Hermetic')],
                                    [_('Foil, Non-Hermetic')],
                                    [_('Slug, Non-Hermetic')]]
        self.cmbConstruction.do_load_combo(_construction, signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Capacitor Assessment Inputs page.

        :param attributes: the attributes dictionary for the selected
            Capacitor.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        # We don't block the callback signal otherwise the style
        # RAMSTKComboBox() will not be loaded and set.
        self.cmbSpecification.set_active(attributes['specification_id'])

        if self._hazard_rate_method_id != 1:
            self.cmbStyle.do_update(attributes['type_id'], signal='changed')
            self.cmbConfiguration.do_update(attributes['configuration_id'],
                                            signal='changed')
            self.cmbConstruction.do_update(attributes['construction_id'],
                                           signal='changed')

            self.txtCapacitance.do_update(str(
                self.fmt.format(attributes['capacitance'])),
                                          signal='changed')  # noqa
            self.txtESR.do_update(str(self.fmt.format(
                attributes['resistance'])),
                                  signal='changed')  # noqa

    def _do_load_styles(self, combo: RAMSTKComboBox) -> None:
        """Load the style RAMSTKComboBox() when the specification changes.

        :param combo: the specification RAMSTKCombo() that called this method.
        :return: None
        :rtype: None
        """
        # If the capacitor specification changed, load the capacitor style
        # RAMSTKComboBox().
        try:
            if self._subcategory_id in [1, 3, 4, 7, 9, 10, 11, 13]:
                _idx = int(combo.get_active()) - 1
                _styles = self._dic_styles[self._subcategory_id][_idx]
            else:
                _styles = self._dic_styles[self._subcategory_id]
        except KeyError:
            _styles = []
        self.cmbStyle.do_load_combo(entries=_styles, signal='changed')

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected capacitor type.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)

        if self._hazard_rate_method_id == 1:
            self.__do_set_parts_count_sensitive()
        else:
            self.__do_set_part_stress_sensitive()

    def __do_set_callbacks(self) -> None:
        """Set callback methods for Capacitor assessment input widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed',
            super().on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbSpecification.dic_handler_id[
            'changed'] = self.cmbSpecification.connect(
                'changed',
                super().on_changed_combo, 1, 'wvw_editing_hardware')
        self.cmbSpecification.connect('changed', self._do_load_styles)
        self.cmbStyle.dic_handler_id['changed'] = self.cmbStyle.connect(
            'changed',
            super().on_changed_combo, 2, 'wvw_editing_hardware')
        self.cmbConfiguration.dic_handler_id[
            'changed'] = self.cmbConfiguration.connect(
                'changed',
                super().on_changed_combo, 3, 'wvw_editing_hardware')
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      super().on_changed_combo,
                                                      4,
                                                      'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtCapacitance.dic_handler_id[
            'changed'] = self.txtCapacitance.connect('changed',
                                                     super().on_changed_entry,
                                                     5, 'wvw_editing_hardware')
        self.txtESR.dic_handler_id['changed'] = self.txtESR.connect(
            'changed',
            super().on_changed_entry, 6, 'wvw_editing_hardware')

    def __do_set_parts_count_sensitive(self) -> None:
        """Set widget sensitivity as needed for MIL-HDBK-217F, Parts Count.

        :return: None
        :rtype: None
        """
        if self._subcategory_id == 1:
            self.cmbSpecification.set_sensitive(True)
        else:
            self.cmbSpecification.set_sensitive(False)
            self.cmbStyle.set_sensitive(False)
            self.cmbConfiguration.set_sensitive(False)
            self.cmbConstruction.set_sensitive(False)
            self.txtCapacitance.set_sensitive(False)
            self.txtESR.set_sensitive(False)

    def __do_set_part_stress_sensitive(self) -> None:
        """Set widget sensitivity as needed for MIL-HDBK-217F, Part Stress.

        :return: None
        :rtype: None
        """
        self.cmbSpecification.set_sensitive(True)
        self.cmbStyle.set_sensitive(True)
        self.txtCapacitance.set_sensitive(True)

        if self._subcategory_id == 12:
            self.txtESR.set_sensitive(True)
        else:
            self.txtESR.set_sensitive(False)

        if self._subcategory_id == 13:
            self.cmbConstruction.set_sensitive(True)
        else:
            self.cmbConstruction.set_sensitive(False)

        if self._subcategory_id == 19:
            self.cmbConfiguration.set_sensitive(True)
        else:
            self.cmbConfiguration.set_sensitive(False)

    def __do_set_properties(self) -> None:
        """Set properties for Capacitor assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties()

        # ----- ENTRIES
        self.txtCapacitance.do_set_properties(tooltip=self._lst_tooltips[1],
                                              width=125)
        self.txtESR.do_set_properties(tooltip=self._lst_tooltips[6], width=125)


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    """Displays capacitor assessment results attribute data.

    The capacitor assessment result view displays all the assessment results
    for the selected capacitor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a capacitor assessment result view are:

    :cvar dict _dic_part_stress: dictionary of MIL-HDBK-217F part stress
        models.  The key is the subcategory ID attribute of the component.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.

    :ivar self.txtLambdaB: displays the base hazard rate for the Hardware
        item.
    :ivar txtPiCV: displays the capacitance factor for the capacitor.
    :ivar txtPiCF: displays the configuration factor for the capacitor.
    :ivar txtPiC: displays the construction factor for the capacitor.
    """

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        6:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        7:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        8:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        9:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        10:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        11:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        12:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>SR</sub>\u03C0<sub"
        ">Q</sub>\u03C0<sub>E</sub></span>",
        13:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>C</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        14:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        15:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        16:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        17:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        18:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        19:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>CF</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Capacitor assessment result view."""
        super().__init__()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            '\u03C0<sub>CV</sub>:',
            '\u03C0<sub>CF</sub>:',
            '\u03C0<sub>C</sub>:',
        ]
        self._lst_tooltips: List[str] = [
            _("The assessment model used to calculate the capacitor hazard "
              "rate."),
            _('The base hazard rate for the capacitor.'),
            _('The quality factor for the capacitor.'),
            _('The environment factor for the capacitor.'),
            _('The capacitance factor for the capacitor.'),
            _('The configuration factor for the capacitor.'),
            _('The construction factor for the capacitor.'),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiCV: RAMSTKEntry = RAMSTKEntry()
        self.txtPiCF: RAMSTKEntry = RAMSTKEntry()
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtPiCV,
            self.txtPiCF,
            self.txtPiC,
        ]

        super().do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the capacitor assessment results page.

        :param attributes: the attributes dictionary for the selected
            Capacitor.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.txtPiCV.do_update(str(self.fmt.format(attributes['piCV'])))
        self.txtPiCF.do_update(str(self.fmt.format(attributes['piCF'])))
        self.txtPiC.do_update(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected capacitor.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F, Parts Count
            self.txtPiCV.set_sensitive(False)
            self.txtPiCF.set_sensitive(False)
            self.txtPiC.set_sensitive(False)
            self.txtPiE.set_sensitive(False)
        else:
            self.txtPiCV.set_sensitive(True)
            self.txtPiCF.set_sensitive(True)
            self.txtPiC.set_sensitive(True)
            self.txtPiE.set_sensitive(True)
