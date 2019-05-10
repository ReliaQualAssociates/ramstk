# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Inductor.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                           AssessmentResults)


class InductorAssessmentInputs(AssessmentInputs):
    """
    Display Inductor assessment input attribute data in the RAMSTK Work Book.

    The Inductor assessment input view displays all the assessment inputs for
    the selected inductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analysis.  The attributes of an
    Inductor assessment input view are:

    :cvar dict _dic_specifications: dictionary of inductor MIL-SPECs.  Key is
                                    inductor subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of inductor styles defined in the
                            MIL-SPECs.  Key is inductor subcategory ID; values
                            are lists of styles.

    :ivar cmbInsulation: select and display the insulation class of the
                         inductor.
    :ivar cmbSpecification: select and display the governing specification for
                            the inductor.
    :ivar cmbConstruction: select and display the method of construction of the
                           inductor.
    :ivar cmbFamily: select and display the family of the transformer.

    :ivar txtArea: enter and display the heat dissipating area of the inductor.
    :ivar txtWeight: enter and display the weight of the inductor.

    Callbacks signals in _lst_handler_id:

    +-------+------------------------------+
    | Index | Widget - Signal              |
    +=======+==============================+
    |   1   | cmbInsulation - `changed`    |
    +-------+------------------------------+
    |   2   | cmbSpecification - `changed` |
    +-------+------------------------------+
    |   3   | cmbFamily - `changed`        |
    +-------+------------------------------+
    |   4   | cmbConstruction - `changed`  |
    +-------+------------------------------+
    |   5   | txtArea - `changed`          |
    +-------+------------------------------+
    |   6   | txtWeight - `changed`        |
    +-------+------------------------------+
    """

    # Define private dict attributes.
    _dic_quality = {
        1: [["MIL-SPEC"], [_("Lower")]],
        2: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_("Lower")]]
    }

    _dic_specifications = {
        1: [["MIL-T-27"], ["MIL-T-21038"], ["MIL-T-55631"]],
        2: [["MIL-T-15305"], ["MIL-T-39010"]]
    }

    _dic_insulation = {
        1: [[_("Insulation Class A")], [_("Insulation Class B")],
            [_("Insulation Class C")], [_("Insulation Class O")],
            [_("Insulation Class Q")], [_("Insulation Class R")],
            [_("Insulation Class S")], [_("Insulation Class T")],
            [_("Insulation Class U")], [_("Insulation Class V")]],
        2: [[_("Insulation Class A")], [_("Insulation Class B")],
            [_("Insulation Class C")], [_("Insulation Class F")],
            [_("Insulation Class O")]]
    }

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Specification:"),
        _("Insulation Class:"),
        _("Area:"),
        _("Weight:"),
        _("Family:"),
        _("Construction:")
    ]

    def __init__(self, **kwargs):
        """Initialize an instance of the Inductor assessment input view."""
        AssessmentInputs.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbInsulation = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The insulation class of the inductive device."))
        self.cmbSpecification = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The governing specification for the inductive "
                      "device."))
        self.cmbFamily = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The application family of the transformer."))
        self.cmbConstruction = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_("The method of construction of the coil."))

        self.txtArea = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_("The case radiating surface (in square inches) of the "
                      "inductive device."))
        self.txtWeight = ramstk.RAMSTKEntry(
            width=125, tooltip=_("The transformer weight (in lbf)."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed', self._on_combo_changed,
                                          1))
        self._lst_handler_id.append(
            self.cmbInsulation.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbFamily.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtArea.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtWeight.connect('changed', self._on_focus_out, 6))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the Inductor RKTComboBox()s.

        :param int subcategory_id: the newly selected inductor subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            _data = [[_("Established Reliability")], ["MIL-SPEC"],
                     [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the specification RAMSTKComboBox().
        try:
            _data = self._dic_specifications[subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        # Load the insulation class RAMSTKComboBox().
        try:
            _data = self._dic_insulation[subcategory_id]
        except KeyError:
            _data = []
        self.cmbInsulation.do_load_combo(_data)

        # Load the transformer family RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            if self._subcategory_id == 1:
                _data = [
                    [_("Low Power Pulse Transformer")],
                    [_("Audio Transformer")],
                    [_("High Power Pulse and Power Transformer, Filter")],
                    [_("RF Transformer")]
                ]
            else:
                _data = [[_("RF Coils, Fixed or Molded")],
                         [_("RF Coils, Variable")]]
        else:
            _data = [[_("Pulse Transformer")], [_("Audio Transformer")],
                     [_("Power Transformer or Filter")],
                     [_("RF Transformer")]]
        self.cmbFamily.do_load_combo(_data)

        # load the coil construction RAMSTKComboBox().
        self.cmbConstruction.do_load_combo([[_("Fixed")], [_("Variable")]])

        return None

    def _do_load_page(self, attributes):
        """
        Load the Inductor assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Inductor.
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

        self.cmbFamily.handler_block(self._lst_handler_id[3])
        self.cmbFamily.set_active(attributes['family_id'])
        self.cmbFamily.handler_unblock(self._lst_handler_id[3])

        if self._hazard_rate_method_id == 2:
            self.cmbSpecification.handler_block(self._lst_handler_id[1])
            self.cmbSpecification.set_active(attributes['specification_id'])
            self.cmbSpecification.handler_unblock(self._lst_handler_id[1])

            self.cmbInsulation.handler_block(self._lst_handler_id[2])
            self.cmbInsulation.set_active(attributes['insulation_id'])
            self.cmbInsulation.handler_unblock(self._lst_handler_id[2])

            self.cmbConstruction.handler_block(self._lst_handler_id[4])
            self.cmbConstruction.set_active(attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[4])

            self.txtArea.handler_block(self._lst_handler_id[5])
            self.txtArea.set_text(str(self.fmt.format(attributes['area'])))
            self.txtArea.handler_unblock(self._lst_handler_id[5])

            self.txtWeight.handler_block(self._lst_handler_id[6])
            self.txtWeight.set_text(str(self.fmt.format(attributes['weight'])))
            self.txtWeight.handler_unblock(self._lst_handler_id[6])

        self._do_set_sensitive()

        return None

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
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

        return None

    def _make_page(self):
        """
        Make the Inductor Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.cmbSpecification, _x_pos, _y_pos[1])
        self.put(self.cmbInsulation, _x_pos, _y_pos[2])
        self.put(self.txtArea, _x_pos, _y_pos[3])
        self.put(self.txtWeight, _x_pos, _y_pos[4])
        self.put(self.cmbFamily, _x_pos, _y_pos[5])
        self.put(self.cmbConstruction, _x_pos, _y_pos[6])

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Inductor attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    1    | cmbSpecification |    3    | cmbFamily        |
            +---------+------------------+---------+------------------+
            |    2    | cmbInsulation    |    4    | cmbConstruction  |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        _dic_keys = {
            0: 'quality_id',
            1: 'specification_id',
            2: 'insulation_id',
            3: 'family_id',
            4: 'construction_id',
        }
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

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
                      method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Widget().  Indices are:

            +---------+---------+---------+-----------+
            |  Index  | Widget  |  Index  | Widget    |
            +=========+=========+=========+===========+
            |    5    | txtArea |    6    | txtWeight |
            +---------+---------+---------+-----------+

        :return: None
        :rtype: None
        """
        _dic_keys = {5: 'area', 6: 'weight'}
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = float(entry.get_text())
        except ValueError:
            _new_text = 0.0

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None


class InductorAssessmentResults(AssessmentResults):
    """
    Display Inductor assessment results attribute data in the RAMSTK Work Book.

    The Inductor assessment result view displays all the assessment results
    for the selected inductor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of an
    Inductor assessment result view are:

    :ivar txtPiC: displays the construction factor for the inductor.
    """

    def __init__(self, **kwargs):
        """Initialize an instance of the Inductor assessment result view."""
        AssessmentResults.__init__(self, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_part_stress = {
            1:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            2:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
        }

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>C</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _("The assessment model used to calculate the inductive device's "
              "failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The construction factor for the coil."))

        self._make_page()
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def _do_load_page(self, attributes):
        """
        Load the inductive device assessment results widgets.

        :param dict attributes: the attributes dictionary for the selected
                                Inductor.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

        return None

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected inductor.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        self.txtPiC.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            self.txtPiC.set_sensitive(False)
            self.txtPiE.set_sensitive(False)
        else:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 2:
                self.txtPiC.set_sensitive(True)

        return None

    def _make_page(self):
        """
        Make the inductor Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiC, _x_pos, _y_pos[3])

        return None
