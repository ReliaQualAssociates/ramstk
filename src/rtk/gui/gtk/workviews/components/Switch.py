# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Switch.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Switch Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _
from rtk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class SwitchAssessmentInputs(AssessmentInputs):
    """
    Display Switch assessment input attribute data in the RTK Work Book.

    The Switch assessment input view displays all the assessment inputs for
    the selected switch.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a switch assessment input view are:

    :cvar dict _dic_applications: dictionary of switch applications.  Key is
                                  switch subcategory ID; values are lists
                                  of applications.
    :cvar dict _dic_construction: dictionary of switch construction methods.
                                  Key is switch subcategory ID; values are
                                  lists of construction methods.
    :cvar dict _dic_contact_forms: dictionary of switch contact forms.  Key is
                                   switch subcategory ID; values are lists of
                                   contact forms.

    :ivar cmbApplication: select and display the switch application.
    :ivar cmbConstruction: select and display the switch construction method.
    :ivar cmbContactForm: select and display the switch contact form.
    :ivar txtNCycles: enter and display the number of switch cycles/hour.
    :ivar txtNElements: enter and display the number of switch wafers.

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | cmbQuality - `changed`                    |
    +-------+-------------------------------------------+
    |   1   | cmbApplication - `changed`                |
    +-------+-------------------------------------------+
    |   2   | cmbConstruction - `changed`               |
    +-------+-------------------------------------------+
    |   3   | cmbContactForm - `changed`                |
    +-------+-------------------------------------------+
    |   4   | txtNCycles - `changed`                    |
    +-------+-------------------------------------------+
    |   5   | txtNElements - `changed`                  |
    +-------+-------------------------------------------+
    """

    # Define private dict attributes.
    # Key is subcategory ID; index is application ID.
    _dic_applications = {
        1: [[_(u"Resistive")], [_(u"Inductive")], [_(u"Lamp")]],
        2: [[_(u"Resistive")], [_(u"Inductive")], [_(u"Lamp")]],
        3: [[_(u"Resistive")], [_(u"Inductive")], [_(u"Lamp")]],
        4: [[_(u"Resistive")], [_(u"Inductive")], [_(u"Lamp")]],
        5: [[_(u"Not Used as a Power On/Off Switch")],
            [_(u"Also Used as a Power On/Off Switch")]]
    }
    # Key is subcategory ID; index is construction ID.
    _dic_constructions = {
        1: [[_(u"Snap Action")], [_(u"Non-Snap Action")]],
        2: [[_(u"Actuation Differential > 0.002 inches")],
            [_(u"Actuation Differential < 0.002 inches")]],
        3: [[_(u"Ceramic RF Wafers")], [_(u"Medium Power Wafers")]],
        5: [[_(u"Magnetic")], [_(u"Thermal")], [_(u"Thermal-Magnetic")]]
    }
    # Key is subcategory ID; index is contact form ID.
    _dic_contact_forms = {
        1: [["SPST"], ["DPST"], ["SPDT"], ["3PST"], ["4PST"], ["DPDT"],
            ["3PDT"], ["4PDT"], ["6PDT"]],
        5: [[u"SPST"], [u"DPST"], [u"3PST"], [u"4PST"]]
    }

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Switch assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentInputs.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Application:"))
        self._lst_labels.append(_(u"Construction:"))
        self._lst_labels.append(_(u"Contact Form:"))
        self._lst_labels.append(_(u"Number of Cycles/Hour:"))
        self._lst_labels.append(_(u"Number of Active Contacts:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The application of the switch."))
        self.cmbConstruction = rtk.RTKComboBox(
            index=0,
            simple=False,
            tooltip=_(u"The construction method for "
                      u"the switch."))
        self.cmbContactForm = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The contact form and quantity of the switch."))
        self.txtNCycles = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of cycles per hour of the switch."))
        self.txtNElements = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of active contacts in the switch."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbContactForm.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.txtNCycles.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self._on_focus_out, 5))

    def _do_load_comboboxes(self, **kwargs):
        """
        Load the switch RKTComboBox().

        This method is used to load the specification RTKComboBox() whenever
        the switch subcategory is changed.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_comboboxes(self, **kwargs)

        # Load the quality level RTKComboBox().
        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_(u"Lower")]])

        # Load the application RTKCOmboBOx().
        try:
            _data = self._dic_applications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data)

        # Load the construction RTKComboBox().
        try:
            if _attributes['hazard_rate_method_id'] == 1:
                _data = [[_(u"Thermal")], [_(u"Magnetic")]]
            else:
                _data = self._dic_constructions[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data)

        # Load the contact form RTKComboBox().
        try:
            _data = self._dic_contact_forms[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbContactForm.do_load_combo(_data)

        return _return

    def _do_load_page(self, **kwargs):
        """
        Load the Switch assesment input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_page(self, **kwargs)

        if _attributes['hazard_rate_method_id'] == 2:
            self.cmbApplication.handler_block(self._lst_handler_id[1])
            self.cmbApplication.set_active(_attributes['application_id'])
            self.cmbApplication.handler_unblock(self._lst_handler_id[1])

            self.cmbConstruction.handler_block(self._lst_handler_id[2])
            self.cmbConstruction.set_active(_attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[2])

            self.cmbContactForm.handler_block(self._lst_handler_id[3])
            self.cmbContactForm.set_active(_attributes['contact_form_id'])
            self.cmbContactForm.handler_unblock(self._lst_handler_id[3])

            self.txtNCycles.handler_block(self._lst_handler_id[4])
            self.txtNCycles.set_text(
                str(self.fmt.format(_attributes['n_cycles'])))
            self.txtNCycles.handler_unblock(self._lst_handler_id[4])

            self.txtNElements.handler_block(self._lst_handler_id[5])
            self.txtNElements.set_text(
                str(self.fmt.format(_attributes['n_elements'])))
            self.txtNElements.handler_unblock(self._lst_handler_id[5])

        return _return

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected switch.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.cmbContactForm.set_sensitive(False)
        self.txtNCycles.set_sensitive(False)
        self.txtNElements.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id == 5:
                self.cmbConstruction.set_sensitive(True)
        elif _attributes['hazard_rate_method_id'] == 2:
            self.cmbApplication.set_sensitive(True)
            if self._subcategory_id in [1, 2, 3, 5]:
                self.cmbConstruction.set_sensitive(True)
            if self._subcategory_id in [1, 5]:
                self.cmbContactForm.set_sensitive(True)
            if self._subcategory_id != 5:
                self.txtNCycles.set_sensitive(True)
            if self._subcategory_id in [2, 3, 4]:
                self.txtNElements.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the Switch class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_load_comboboxes(subcategory_id=self._subcategory_id)

        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.cmbApplication, _x_pos, _y_pos[1])
        self.put(self.cmbConstruction, _x_pos, _y_pos[2])
        self.put(self.cmbContactForm, _x_pos, _y_pos[3])
        self.put(self.txtNCycles, _x_pos, _y_pos[4])
        self.put(self.txtNElements, _x_pos, _y_pos[5])

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Switch attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   1   | cmbApplication   |   3   | cmbContactForm   |
            +-------+------------------+-------+------------------+
            |   2   | cmbConstruction  |       |                  |
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
                _attributes['construction_id'] = int(combo.get_active())
            elif index == 3:
                _attributes['contact_form_id'] = int(combo.get_active())

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

            +---------+---------------------+---------+---------------------+
            |  Index  | Widget              |  Index  | Widget              |
            +=========+=====================+=========+=====================+
            |    4    | txtNCycles          |    5    | txtNElements        |
            +---------+---------------------+---------+---------------------+

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

            if index == 4:
                _attributes['n_cycles'] = _text
            elif index == 5:
                _attributes['n_elements'] = int(_text)

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id, **kwargs):
        """
        Load the switch assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              switch.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)


class SwitchAssessmentResults(AssessmentResults):
    """
    Display Switch assessment results attribute data in the RTK Work Book.

    The Switch assessment result view displays all the assessment results
    for the selected switch.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a switch assessment result view are:

    :ivar txtPiC: displays the contact form and quantity factor for the switch.
    :ivar txtPiCYC: displays the cycling factor for the switch.
    :ivar txtPiL: displays the load stress factor for the switch.
    :ivar txtPiN: displays the number of active contacts factor for the switch.
    :ivar txtPiU: displays the use factor for the breaker.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>",
        3:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>",
        4:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (\u03BB<sub>b1</sub> + \u03C0<sub>N</sub>\u03BB<sub>b2</sub>)\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>",
        5:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Switch assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentResults.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>CYC</sub>:")
        self._lst_labels.append(u"\u03C0<sub>L</sub>:")
        self._lst_labels.append(u"\u03C0<sub>C</sub>:")
        self._lst_labels.append(u"\u03C0<sub>N</sub>:")
        self._lst_labels.append(u"\u03C0<sub>U</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the switch failure "
              u"rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiCYC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The cycling factor for the switch."))
        self.txtPiL = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The load stress factor for the switch."))
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The contact form and quantity factor for the switch."))
        self.txtPiN = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The number of active contacts factor for the switch."))
        self.txtPiU = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The use factor for the breaker."))

        self._make_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self, **kwargs):
        """
        Load the switch assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentResults.do_load_page(self, **kwargs)

        self.txtPiCYC.set_text(str(self.fmt.format(_attributes['piCYC'])))
        self.txtPiL.set_text(str(self.fmt.format(_attributes['piL'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiN.set_text(str(self.fmt.format(_attributes['piN'])))
        self.txtPiU.set_text(str(self.fmt.format(_attributes['piU'])))

        return _return

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected switch.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = AssessmentResults.do_set_sensitive(self, **kwargs)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiCYC.set_sensitive(False)
        self.txtPiL.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiN.set_sensitive(False)
        self.txtPiU.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 1:
            self.txtPiQ.set_sensitive(True)
        else:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id != 5:
                self.txtPiCYC.set_sensitive(True)
                self.txtPiL.set_sensitive(True)
            if self._subcategory_id == 2:
                self.txtPiN.set_sensitive(True)
            if self._subcategory_id == 5:
                self.txtPiQ.set_sensitive(True)
                self.txtPiU.set_sensitive(True)
            if self._subcategory_id in [1, 5]:
                self.txtPiC.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the switch gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiCYC, _x_pos, _y_pos[3])
        self.put(self.txtPiL, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])
        self.put(self.txtPiN, _x_pos, _y_pos[6])
        self.put(self.txtPiU, _x_pos, _y_pos[7])

        return None

    def on_select(self, module_id, **kwargs):
        """
        Load the switch assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              switch.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)
