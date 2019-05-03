# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Meter.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                           AssessmentResults)


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
    # Quality levels; key is the subcategory ID.
    _dic_quality = {
        2: [["MIL-SPEC"], [_(u"Lower")]],
        1: [["MIL-SPEC"], [_(u"Lower")]],
    }
    # Meter types; key is the subcategory ID.
    _dic_types = {
        1: [[_(u"AC")], [_(u"Inverter Driver")], [_(u"Commutator DC")]],
        2: [[_(u"Direct Current")], [_(u"Alternating Current")]]
    }

    # Define private list attributes.
    _lst_labels = [
        _(u"Quality Level:"),
        _(u"Meter Type:"),
        _(u"Meter Function:")
    ]

    def __init__(self, **kwargs):
        """Initialize an instance of the Meter assessment input view."""
        AssessmentInputs.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The appliction of the panel meter."))
        self.cmbType = ramstk.RAMSTKComboBox(
            index=0, simple=False, tooltip=_(u"The type of meter."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 2))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

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
            _data = [["MIL-SPEC"], [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the meter appliction RAMSTKComboBox().
        self.cmbApplication.do_load_combo([[_(u"Ammeter")], [_(u"Voltmeter")],
                                           [_(u"Other")]])

        # Load the meter type RAMSTKComboBox().
        try:
            _data = self._dic_types[subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

        return None

    def _do_load_page(self, attributes):
        """
        Load the Meter assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Meter.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self._do_load_comboboxes(self._subcategory_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        self.cmbApplication.handler_block(self._lst_handler_id[1])
        self.cmbApplication.set_active(attributes['application_id'])
        self.cmbApplication.handler_unblock(self._lst_handler_id[1])

        self.cmbType.handler_block(self._lst_handler_id[2])
        self.cmbType.set_active(attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[2])

        self._do_set_sensitive()

        return None

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

        return None

    def _make_page(self):
        """
        Make the Meter class Gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.cmbType, _x_pos, _y_pos[1])
        self.put(self.cmbApplication, _x_pos, _y_pos[2])

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Meter attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   1   | cmbApplication   |   2   | cmbType          |
            +-------+------------------+-------+------------------+

        :return: None
        :rtype: None
        """
        _dic_keys = {0: 'quality_id', 1: 'application_id', 2: 'type_id'}
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        combo.handler_block(self._lst_handler_id[index])

        try:
            _new_text = int(combo.get_active())
        except ValueError:
            _new_text = 0

        # Only publish the message if something is selected in the ComboBox.
        if _new_text != -1:
            pub.sendMessage(
                'wvw_editing_hardware',
                module_id=self._hardware_id,
                key=_key,
                value=_new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return None


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
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, **kwargs):
        """Initialize an instance of the Meter assessment result view."""
        AssessmentResults.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>A</sub>:")
        self._lst_labels.append(u"\u03C0<sub>F</sub>:")
        self._lst_labels.append(u"\u03C0<sub>T</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the meter failure "
              u"rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiA = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The application factor for the meter."))
        self.txtPiF = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The function factor for the meter."))
        self.txtPiT = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The temperature stress factor for the meter."))

        self._make_page()
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

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

        return None

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

        return None

    def _make_page(self):
        """
        Make the meter Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiA, _x_pos, _y_pos[3])
        self.put(self.txtPiF, _x_pos, _y_pos[4])
        self.put(self.txtPiT, _x_pos, _y_pos[5])

        return None
