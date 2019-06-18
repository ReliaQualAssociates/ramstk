# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.Meter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKComboBox, RAMSTKEntry
from ramstk.gui.gtk.ramstk.Widget import _

# RAMSTK Local Imports
from .Component import AssessmentInputs, AssessmentResults


class MeterAssessmentInputs(AssessmentInputs):
    """
    Display Meter assessment input attribute data in the RAMSTK Work Book.

    The Meter assessment input view displays all the assessment inputs for
    the selected Meter item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Meter assessment input view are:

    :cvar dict _dic_quality: dictionary of meter quality levels.  Key is
                             meter subcategory ID; values are lists of
                             quality levels.
    :cvar dict _dic_type: dictionary of meter types.  Key is meter
                          subcategory ID; values are lists of types.
    :cvar dict _dic_specification: dictionary of meter MIL-SPECs.  Key is
                                   meter tye ID; values are lists
                                   of specifications.
    :cvar dict _dic_insert: dictionary of meter insert materials.  First
                            key is meter type ID, second key is meter
                            specification ID; values are lists of insert
                            materials.

    :ivar cmbApplication: select and display the application of the meter.
    :ivar cmbType: select and display the type of meter.

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | cmbQuality - `changed`                    |
    +-------+-------------------------------------------+
    |   1   | cmbApplication - `changed`                |
    +-------+-------------------------------------------+
    |   2   | cmbType - `changed`                       |
    +-------+-------------------------------------------+
    """

    # Define private dict attributes.
    _dic_keys = {0: 'quality_id', 1: 'application_id', 2: 'type_id'}

    # Quality levels; key is the subcategory ID.
    _dic_quality = {
        2: [["MIL-SPEC"], [_("Lower")]],
        1: [["MIL-SPEC"], [_("Lower")]],
    }
    # Meter types; key is the subcategory ID.
    _dic_types = {
        1: [[_("AC")], [_("Inverter Driver")], [_("Commutator DC")]],
        2: [[_("Direct Current")], [_("Alternating Current")]],
    }

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Meter Type:"),
        _("Meter Function:"),
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Meter assessment input view.

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
            index=0,
            simple=True,
        )
        self.cmbType = RAMSTKComboBox(
            index=0, simple=True,
        )

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __make_ui(self):
        """
        Make the Meter class Gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_ui(self)

        self.put(self.cmbType, _x_pos, _y_pos[1])
        self.put(self.cmbApplication, _x_pos, _y_pos[2])

        self.show_all()

    def __set_callbacks(self):
        """
        Set callback methods for Meter assessment input widgets.

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
            self.cmbType.connect('changed', self.on_combo_changed, 2),
        )

    def __set_properties(self):
        """
        Set properties for Meter assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbApplication.do_set_properties(
            tooltip=_("The appliction of the panel meter."),
        )
        self.cmbType.do_set_properties(
            tooltip=_("The type of meter."),
        )

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the meter RKTComboBox()s.

        This method is used to load the specification RAMSTKComboBox() whenever
        the meter subcategory is changed.

        :param int subcategory_id: the newly selected meter subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            _data = [["MIL-SPEC"], [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the meter appliction RAMSTKComboBox().
        self.cmbApplication.do_load_combo([
            [_("Ammeter")], [_("Voltmeter")],
            [_("Other")],
        ])

        # Load the meter type RAMSTKComboBox().
        try:
            _data = self._dic_types[subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

    def _do_load_page(self, attributes):
        """
        Load the Meter assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Meter.
        :return: None
        :rtype: None
        """
        AssessmentInputs.do_load_page(self, attributes)

        self.cmbApplication.handler_block(self._lst_handler_id[1])
        self.cmbApplication.set_active(attributes['application_id'])
        self.cmbApplication.handler_unblock(self._lst_handler_id[1])

        self.cmbType.handler_block(self._lst_handler_id[2])
        self.cmbType.set_active(attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[2])

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected meter.

        :return: None
        :rtype: None
        """
        self.cmbType.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)

        if (self._hazard_rate_method_id == 2 and self._subcategory_id == 2):
            self.cmbApplication.set_sensitive(True)


class MeterAssessmentResults(AssessmentResults):
    """
    Display Meter assessment results attribute data in the RAMSTK Work Book.

    The Meter assessment result view displays all the assessment results
    for the selected meter.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a meter assessment result view are:

    :ivar txtPiA: displays the application factor for the panel meter.
    :ivar txtPiF: displays the function factor for the panel meter.
    :ivar txtPiT: displays the temperature stress factor for the elapsed time
                  meter.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span>",
    }

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Meter assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentResults.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>A</sub>:")
        self._lst_labels.append("\u03C0<sub>F</sub>:")
        self._lst_labels.append("\u03C0<sub>T</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiA = RAMSTKEntry()
        self.txtPiF = RAMSTKEntry()
        self.txtPiT = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __make_ui(self):
        """
        Make the meter Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_ui(self)

        self.put(self.txtPiA, _x_pos, _y_pos[3])
        self.put(self.txtPiF, _x_pos, _y_pos[4])
        self.put(self.txtPiT, _x_pos, _y_pos[5])

        self.show_all()

    def __set_properties(self):
        """
        Set properties for Meter assessment result widgets.

        :return: None
        :rtype: None
        """
        self._lblModel.set_tooltip_markup(
            _(
                "The assessment model used to calculate the meter failure "
                "rate.",
            ),
        )
        self.txtPiA.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The application factor for the meter."),
        )
        self.txtPiF.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The function factor for the meter."),
        )
        self.txtPiT.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The temperature stress factor for the meter."),
        )

    def _do_load_page(self, attributes):
        """
        Load the meter assessment results page.

        :param dict attributes: the attributes dictionary for the selected
                                Meter.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiA.set_text(str(self.fmt.format(attributes['piA'])))
        self.txtPiF.set_text(str(self.fmt.format(attributes['piF'])))
        self.txtPiT.set_text(str(self.fmt.format(attributes['piT'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected meter.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, *kwargs)

        self.txtPiA.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiT.set_sensitive(False)

        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 1:
                self.txtPiT.set_sensitive(True)
                self.txtPiQ.set_sensitive(False)
            elif self._subcategory_id == 2:
                self.txtPiA.set_sensitive(True)
                self.txtPiF.set_sensitive(True)
