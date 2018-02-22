# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Meter.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Meter Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _
from rtk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class MeterAssessmentInputs(AssessmentInputs):
    """
    Display Meter assessment input attribute data in the RTK Work Book.

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
        1: [["MIL-SPEC"], [_(u"Lower")]],
        2: [["MIL-SPEC"], [_(u"Lower")]],
    }
    # Meter types; key is the subcategory ID.
    _dic_types = {
        1: [[_(u"Direct Current")], [_(u"Alternating Current")]],
        2: [[_(u"AC")], [_(u"Inverter Driver")], [_(u"Commutator DC")]]
    }

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Meter assessment input view.

        :param controller: the meter data controller instance.
        :type controller: :class:`rtk.meter.Controller.MeterBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected meter.
        :param int subcategory_id: the ID of the meter subcategory.
        """
        AssessmentInputs.__init__(self, controller, hardware_id,
                                  subcategory_id)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Meter Type:"))
        self._lst_labels.append(_(u"Meter Function:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The appliction of the panel meter."))
        self.cmbType = rtk.RTKComboBox(
            index=0, simple=False, tooltip=_(u"The type of meter."))

        self._make_assessment_input_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 2))

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the meter RKTComboBox()s.

        This method is used to load the specification RTKComboBox() whenever
        the meter subcategory is changed.

        :param int subcategory_id: the newly selected meter subcategory ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_comboboxes(self, subcategory_id)

        # Load the quality level RTKComboBox().
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)
        if _attributes['hazard_rate_method_id'] == 1:
            _data = [["MIL-SPEC"], [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the meter appliction RTKComboBox().
        self.cmbApplication.do_load_combo([[_(u"Ammeter")], [_(u"Voltmeter")],
                                           [_(u"Other")]])

        # Load the meter type RTKComboBox().
        try:
            _data = self._dic_types[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected meter.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbType.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)

        if (_attributes['hazard_rate_method_id'] == 2
                and _attributes['subcategory_id'] == 1):
            self.cmbApplication.set_sensitive(True)

        return _return

    def _make_assessment_input_page(self):
        """
        Make the Meter class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_assessment_input_page(self)

        self.put(self.cmbType, _x_pos, _y_pos[1])
        self.put(self.cmbApplication, _x_pos, _y_pos[2])

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Meter attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   1   | cmbApplication   |   2   | cmbType          |
            +-------+------------------+-------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _attributes = AssessmentInputs.on_combo_changed(self, combo, index)

        if _attributes:
            if index == 1:
                _attributes['application_id'] = int(combo.get_active())
            elif index == 2:
                _attributes['type_id'] = int(combo.get_active())

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the meter assessment input work view widgets.

        :param int module_id: the Meter ID of the selected/edited
                              meter.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = AssessmentInputs.on_select(self, module_id)

        self.cmbApplication.handler_block(self._lst_handler_id[1])
        self.cmbApplication.set_active(_attributes['application_id'])
        self.cmbApplication.handler_unblock(self._lst_handler_id[1])

        self.cmbType.handler_block(self._lst_handler_id[2])
        self.cmbType.set_active(_attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[2])

        return _return


class MeterAssessmentResults(AssessmentResults):
    """
    Display Meter assessment results attribute data in the RTK Work Book.

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

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Meter assessment result view.

        :param controller: the meter data controller instance.
        :type controller: :class:`rtk.meter.Controller.MeterBoMDataController`
        :param int hardware_id: the meter ID of the currently selected
                                meter.
        :param int subcategory_id: the ID of the meter subcategory.
        """
        AssessmentResults.__init__(self, controller, hardware_id,
                                   subcategory_id)

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
        self.txtPiA = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The application factor for the meter."))
        self.txtPiF = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The function factor for the meter."))
        self.txtPiT = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The temperature stress factor for the meter."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the meter assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentResults.do_load_page(self)

        self.txtPiA.set_text(str(self.fmt.format(_attributes['piA'])))
        self.txtPiF.set_text(str(self.fmt.format(_attributes['piF'])))
        self.txtPiT.set_text(str(self.fmt.format(_attributes['piT'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected meter.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = AssessmentResults.do_set_sensitive(self)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiA.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiT.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 1:
                self.txtPiA.set_sensitive(True)
                self.txtPiF.set_sensitive(True)
            elif self._subcategory_id == 2:
                self.txtPiT.set_sensitive(True)
                self.txtPiQ.set_sensitive(False)

        return _return

    def _make_assessment_results_page(self):
        """
        Make the meter gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_assessment_results_page(self)

        self.put(self.txtPiA, _x_pos, _y_pos[3])
        self.put(self.txtPiF, _x_pos, _y_pos[4])
        self.put(self.txtPiT, _x_pos, _y_pos[5])

        return None

    def on_select(self, module_id=None):
        """
        Load the meter assessment input work view widgets.

        :param int module_id: the Meter ID of the selected/edited
                              meter.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_set_sensitive()
        self._do_load_page()

        return _return
