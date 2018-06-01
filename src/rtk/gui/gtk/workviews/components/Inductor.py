# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Inductor.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Inductor Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _
from rtk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class InductorAssessmentInputs(AssessmentInputs):
    """
    Display Inductor assessment input attribute data in the RTK Work Book.

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
        1: [["MIL-SPEC"], [_(u"Lower")]],
        2: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_(u"Lower")]]
    }

    _dic_specifications = {
        1: [["MIL-T-27"], ["MIL-T-21038"], ["MIL-T-55631"]],
        2: [["MIL-T-15305"], ["MIL-T-39010"]]
    }

    _dic_insulation = {
        1: [[_(u"Insulation Class A")], [_(u"Insulation Class B")], [
            _(u"Insulation Class C")
        ], [_(u"Insulation Class O")], [_(u"Insulation Class Q")], [
            _(u"Insulation Class R")
        ], [_(u"Insulation Class S")], [_(u"Insulation Class T")],
            [_(u"Insulation Class U")], [_(u"Insulation Class V")]],
        2: [[_(u"Insulation Class A")], [_(u"Insulation Class B")],
            [_(u"Insulation Class C")], [_(u"Insulation Class F")],
            [_(u"Insulation Class O")]]
    }

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Inductor assessment input view.

        :param controller: the Hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                inductor.
        :param int subcategory_id: the ID of the inductor subcategory.
        """
        AssessmentInputs.__init__(self, controller, hardware_id,
                                  subcategory_id)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Specification:"))
        self._lst_labels.append(_(u"Insulation Class:"))
        self._lst_labels.append(_(u"Area:"))
        self._lst_labels.append(_(u"Weight:"))
        self._lst_labels.append(_(u"Family:"))
        self._lst_labels.append(_(u"Construction:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbInsulation = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The insulation class of the inductive device."))
        self.cmbSpecification = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The governing specification for the inductive "
                      u"device."))
        self.cmbFamily = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The application family of the transformer."))
        self.cmbConstruction = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the coil."))

        self.txtArea = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The case radiating surface (in square inches) of the "
                      u"inductive device."))
        self.txtWeight = rtk.RTKEntry(
            width=125, tooltip=_(u"The transformer weight (in lbf)."))

        self._make_assessment_input_page()
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

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the Inductor RKTComboBox()s.

        :param int subcategory_id: the newly selected inductor subcategory ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_comboboxes(self, subcategory_id)

        # Load the quality level RTKComboBox().
        if _attributes['hazard_rate_method_id'] == 1:
            _data = [[_(u"Established Reliability")], ["MIL-SPEC"],
                     [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the specification RTKComboBox().
        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        # Load the insulation class RTKComboBox().
        try:
            _data = self._dic_insulation[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbInsulation.do_load_combo(_data)

        # Load the transformer family RTKComboBox().
        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id == 1:
                _data = [[_(u"Low Power Pulse Transformer")], [
                    _(u"Audio Transformer")
                ], [_(u"High Power Pulse and Power Transformer, Filter")],
                         [_(u"RF Transformer")]]
            else:
                _data = [[_(u"RF Coils, Fixed or Molded")],
                         [_(u"RF Coils, Variable")]]
        else:
            _data = [[_(u"Pulse Transformer")], [_("Audio Transformer")],
                     [_(u"Power Transformer or Filter")],
                     [_(u"RF Transformer")]]
        self.cmbFamily.do_load_combo(_data)

        # load the coil construction RTKComboBox().
        self.cmbConstruction.do_load_combo([[_(u"Fixed")], [_(u"Variable")]])

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected inductor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbSpecification.set_sensitive(False)
        self.cmbInsulation.set_sensitive(False)
        self.cmbFamily.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtArea.set_sensitive(False)
        self.txtWeight.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 1:
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

        return _return

    def _make_assessment_input_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_assessment_input_page(self)

        self.put(self.cmbSpecification, _x_pos, _y_pos[1])
        self.put(self.cmbInsulation, _x_pos, _y_pos[2])
        self.put(self.txtArea, _x_pos, _y_pos[3])
        self.put(self.txtWeight, _x_pos, _y_pos[4])
        self.put(self.cmbFamily, _x_pos, _y_pos[5])
        self.put(self.cmbConstruction, _x_pos, _y_pos[6])

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Inductor attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    1    | cmbSpecification |    3    | cmbFamily        |
            +---------+------------------+---------+------------------+
            |    2    | cmbInsulation    |    4    | cmbConstruction  |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _attributes = AssessmentInputs.on_combo_changed(self, combo, index)

        if _attributes:
            if index == 1:
                _attributes['specification_id'] = int(combo.get_active())
            elif index == 2:
                _attributes['insulation_id'] = int(combo.get_active())
            elif index == 3:
                _attributes['family_id'] = int(combo.get_active())
            elif index == 4:
                _attributes['construction_id'] = int(combo.get_active())

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RTKEntry() widgets..

        This method is called by:

            * RTKEntry() 'changed' signal
            * RTKTextView() 'changed' signal

        :param entry: the RTKEntry() or RTKTextView() that called the method.
        :type entry: :class:`rtk.gui.gtk.rtk.RTKEntry` or
                     :class:`rtk.gui.gtk.rtk.RTKTextView`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

            +---------+---------+---------+-----------+
            |  Index  | Widget  |  Index  | Widget    |
            +=========+=========+=========+===========+
            |    5    | txtArea |    6    | txtWeight |
            +---------+---------+---------+-----------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            try:
                _text = float(entry.get_text())
            except ValueError:
                _text = 0.0

            if index == 5:
                _attributes['area'] = _text
            elif index == 6:
                _attributes['weight'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the inductor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              inductor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = AssessmentInputs.on_select(self, module_id)

        self.cmbFamily.handler_block(self._lst_handler_id[3])
        self.cmbFamily.set_active(_attributes['family_id'])
        self.cmbFamily.handler_unblock(self._lst_handler_id[3])

        if _attributes['hazard_rate_method_id'] == 2:
            self.cmbSpecification.handler_block(self._lst_handler_id[1])
            self.cmbSpecification.set_active(_attributes['specification_id'])
            self.cmbSpecification.handler_unblock(self._lst_handler_id[1])

            self.cmbInsulation.handler_block(self._lst_handler_id[2])
            self.cmbInsulation.set_active(_attributes['insulation_id'])
            self.cmbInsulation.handler_unblock(self._lst_handler_id[2])

            self.cmbConstruction.handler_block(self._lst_handler_id[4])
            self.cmbConstruction.set_active(_attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[4])

            self.txtArea.handler_block(self._lst_handler_id[5])
            self.txtArea.set_text(str(self.fmt.format(_attributes['area'])))
            self.txtArea.handler_unblock(self._lst_handler_id[5])

            self.txtWeight.handler_block(self._lst_handler_id[6])
            self.txtWeight.set_text(
                str(self.fmt.format(_attributes['weight'])))
            self.txtWeight.handler_unblock(self._lst_handler_id[6])

        self._do_set_sensitive()

        return _return


class InductorAssessmentResults(AssessmentResults):
    """
    Display Inductor assessment results attribute data in the RTK Work Book.

    The Inductor assessment result view displays all the assessment results
    for the selected inductor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of an
    Inductor assessment result view are:

    :ivar txtPiC: displays the construction factor for the inductor.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Inductor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                inductor.
        :param int subcategory_id: the ID of the inductor subcategory.
        """
        AssessmentResults.__init__(self, controller, hardware_id,
                                   subcategory_id)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>C</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the inductive device's "
              u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The construction factor for the coil."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the inductive device assessment results wodgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentResults.do_load_page(self)

        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected inductor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = AssessmentResults.do_set_sensitive(self)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiC.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 1:
            self.txtPiC.set_sensitive(False)
            self.txtPiE.set_sensitive(False)
        else:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 2:
                self.txtPiC.set_sensitive(True)

        return _return

    def _make_assessment_results_page(self):
        """
        Make the inductor gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_assessment_results_page(self)

        self.put(self.txtPiC, _x_pos, _y_pos[3])

        return None

    def on_select(self, module_id=None):
        """
        Load the inductor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              inductor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_set_sensitive()
        self._do_load_page()

        return _return
