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
from rtk.gui.gtk.rtk.Widget import _, gtk


class AssessmentInputs(gtk.Fixed):
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

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the switch
                               currently being displayed.

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

    # Define private list attributes.
    _lst_labels = [
        _(u"Quality Level:"),
        _(u"Application:"),
        _(u"Construction:"),
        _(u"Contact Form:"),
        _(u"Number of Cycles/Hour:"),
        _(u"Number of Active Contacts:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Switch assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                switch.
        :param int subcategory_id: the ID of the switch subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.cmbQuality = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The quality level of the switch."))
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

        self._make_assessment_input_page()
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

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the switch RKTComboBox().

        This method is used to load the specification RTKComboBox() whenever
        the switch subcategory is changed.

        :param int subcategory_id: the newly selected switch subcategory ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._subcategory_id = subcategory_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

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

    def _do_set_sensitive(self):
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

    def _make_assessment_input_page(self):
        """
        Make the Switch class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for switchs.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])
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

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    2    | cmbConstruction  |
            +---------+------------------+---------+------------------+
            |    1    | cmbApplication   |    3    | cmbContactForm   |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 0:
                _attributes['quality_id'] = int(combo.get_active())
            elif index == 1:
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

    def on_select(self, module_id=None):
        """
        Load the switch assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              switch.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(_attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        self._do_set_sensitive()

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


class StressInputs(gtk.Fixed):
    """
    Display Switch stress input attribute data in the RTK Work Book.

    The Switch stress input view displays all the assessment inputs for
    the selected switch.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a switch stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the switch
                               currently being displayed.

    :ivar txtTemperatureRated: enter and display the maximum rated temperature
                               of the switch.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           switch.
    :ivar txtVoltageAC: enter and display the operating ac voltage of the
                        switch.
    :ivar txtVoltageDC: enter and display the operating DC voltage of the
                        switch.

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | txtTemperatureRatedMin - `changed`        |
    +-------+-------------------------------------------+
    |   1   | txtTemperatureKnee - `changed`            |
    +-------+-------------------------------------------+
    |   2   | txtTemperatureRatedMax - `changed`        |
    +-------+-------------------------------------------+
    |   3   | txtCurrentRated - `changed`               |
    +-------+-------------------------------------------+
    |   4   | txtCurrentOperating - `changed`           |
    +-------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Minimum Rated Temperature (\u00B0C):"),
        _(u"Knee Temperature (\u00B0C):"),
        _(u"Maximum Rated Temperature (\u00B0C):"),
        _(u"Rated Current (A):"),
        _(u"Operating Current (A):")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Switch stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                switch.
        :param int subcategory_id: the ID of the switch subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtTemperatureRatedMin = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The minimum rated temperature (in \u00B0C) of the switch."))
        self.txtTemperatureKnee = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The break temperature (in \u00B0C) of the switch beyond "
                u"which it must be derated."))
        self.txtTemperatureRatedMax = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The maximum rated temperature (in \u00B0C) of the switch."))
        self.txtCurrentRated = rtk.RTKEntry(
            width=125, tooltip=_(u"The rated current (in A) of the switch."))
        self.txtCurrentOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating current (in A) of the switch."))

        self._lst_handler_id.append(
            self.txtTemperatureRatedMin.connect('changed', self._on_focus_out,
                                                0))
        self._lst_handler_id.append(
            self.txtTemperatureKnee.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect('changed', self._on_focus_out,
                                                2))
        self._lst_handler_id.append(
            self.txtCurrentRated.connect('changed', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.txtCurrentOperating.connect('changed', self._on_focus_out, 4))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the switch module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for switchs.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[2])
        self.put(self.txtCurrentRated, _x_pos, _y_pos[3])
        self.put(self.txtCurrentOperating, _x_pos, _y_pos[4])

        self.show_all()

        return None

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

            +-------+------------------------+-------+---------------------+
            | Index | Widget                 | Index | Widget              |
            +=======+========================+=======+=====================+
            |   0   | txtTemperatureRatedMin |   3   | txtCurrentRated     |
            +-------+------------------------+-------+---------------------+
            |   1   | txtTemperatureKnee     |   4   | txtCurrentOperating |
            +-------+------------------------+-------+---------------------+
            |   2   | txtTemperatureRatedMax |       |                     |
            +-------+------------------------+-------+---------------------+

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

            if index == 0:
                _attributes['temperature_rated_min'] = _text
            elif index == 1:
                _attributes['temperature_knee'] = _text
            elif index == 2:
                _attributes['temperature_rated_max'] = _text
            elif index == 3:
                _attributes['current_rated'] = _text
            elif index == 4:
                _attributes['current_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the switch stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              switch.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # We don't block the callback signal otherwise the style RTKComboBox()
        # will not be loaded and set.
        self.txtTemperatureRatedMin.handler_block(self._lst_handler_id[0])
        self.txtTemperatureRatedMin.set_text(
            str(self.fmt.format(_attributes['temperature_rated_min'])))
        self.txtTemperatureRatedMin.handler_unblock(self._lst_handler_id[0])

        self.txtTemperatureKnee.handler_block(self._lst_handler_id[1])
        self.txtTemperatureKnee.set_text(
            str(self.fmt.format(_attributes['temperature_knee'])))
        self.txtTemperatureKnee.handler_unblock(self._lst_handler_id[1])

        self.txtTemperatureRatedMax.handler_block(self._lst_handler_id[2])
        self.txtTemperatureRatedMax.set_text(
            str(self.fmt.format(_attributes['temperature_rated_max'])))
        self.txtTemperatureRatedMax.handler_unblock(self._lst_handler_id[2])

        self.txtCurrentRated.handler_block(self._lst_handler_id[3])
        self.txtCurrentRated.set_text(
            str(self.fmt.format(_attributes['current_rated'])))
        self.txtCurrentRated.handler_unblock(self._lst_handler_id[3])

        self.txtCurrentOperating.handler_block(self._lst_handler_id[4])
        self.txtCurrentOperating.set_text(
            str(self.fmt.format(_attributes['current_operating'])))
        self.txtCurrentOperating.handler_unblock(self._lst_handler_id[4])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display switch assessment results attribute data in the RTK Work Book.

    The switch assessment result view displays all the assessment results
    for the selected switch.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a switch assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the switch
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the switch.
    :ivar txtPiQ: displays the quality factor for the switch.
    :ivar txtPiE: displays the environment factor for the switch.
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

    # Define private list attributes.
    _lst_labels = [
        u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:",
        u"\u03C0<sub>CYC</sub>:", u"\u03C0<sub>L</sub>:",
        u"\u03C0<sub>C</sub>:", u"\u03C0<sub>N</sub>:", u"\u03C0<sub>U</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Switch assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                switch.
        :param int subcategory_id: the ID of the switch subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        self._lblModel = rtk.RTKLabel(
            '',
            tooltip=_(u"The assessment model used to calculate the switch "
                      u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the switch."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the switch."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the switch."))
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

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the switch assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))
        self.txtPiCYC.set_text(str(self.fmt.format(_attributes['piCYC'])))
        self.txtPiL.set_text(str(self.fmt.format(_attributes['piL'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiN.set_text(str(self.fmt.format(_attributes['piN'])))
        self.txtPiU.set_text(str(self.fmt.format(_attributes['piU'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected switch.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self._subcategory_id = _attributes['subcategory_id']

        self.txtPiQ.set_sensitive(False)
        self.txtPiE.set_sensitive(False)
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

    def _make_assessment_results_page(self):
        """
        Make the switch gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        if _attributes['hazard_rate_method_id'] == 1:
            self._lblModel.set_markup(
                u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = "
                u"\u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>")
            self._lst_labels[0] = u"\u03BB<sub>g</sub>:"
        else:
            try:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id])
            except KeyError:
                self._lblModel.set_markup(_(u"Missing Model"))
            self._lst_labels[0] = u"\u03BB<sub>b</sub>:"

        self._do_set_sensitive()

        # Build the container for switchs.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiQ, _x_pos, _y_pos[1])
        self.put(self.txtPiE, _x_pos, _y_pos[2])
        self.put(self.txtPiCYC, _x_pos, _y_pos[3])
        self.put(self.txtPiL, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])
        self.put(self.txtPiN, _x_pos, _y_pos[6])
        self.put(self.txtPiU, _x_pos, _y_pos[7])

        self.show_all()

        return None

    def on_select(self, module_id=None):
        """
        Load the switch assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              switch.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_set_sensitive()
        self._do_load_page()

        return _return


class StressResults(gtk.HPaned):
    """
    Display switch stress results attribute data in the RTK Work Book.

    The switch stress result view displays all the stress results for the
    selected switch.  This includes, currently, results for MIL-HDBK-217FN2
    parts count and MIL-HDBK-217FN2 part stress methods.  The attributes of a
    switch stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the switch
                               currently being displayed.

    :ivar txtCurrentRatio: display the current ratio for the switch.
    """

    # Define private list attributes.
    _lst_labels = [_(u"Current Ratio:"), "", _(u"Overstress Reason:")]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Switch assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                switch.
        :param int subcategory_id: the ID of the switch subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.75, 0.75, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.pltDerate = rtk.RTKPlot()

        self.txtCurrentRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating current to rated current for "
                      u"the switch."))
        self.chkOverstress = rtk.RTKCheckButton(
            label=_(u"Overstressed"),
            tooltip=_(u"Indicates whether or not the selected switch "
                      u"is overstressed."))
        self.txtReason = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=250,
            tooltip=_(u"The reason(s) the selected hardware item is "
                      u"overstressed."))

        self.chkOverstress.set_sensitive(False)
        self.txtReason.set_editable(False)
        _bg_color = gtk.gdk.Color('#ADD8E6')
        self.txtReason.modify_base(gtk.STATE_NORMAL, _bg_color)
        self.txtReason.modify_base(gtk.STATE_ACTIVE, _bg_color)
        self.txtReason.modify_base(gtk.STATE_PRELIGHT, _bg_color)
        self.txtReason.modify_base(gtk.STATE_SELECTED, _bg_color)
        self.txtReason.modify_base(gtk.STATE_INSENSITIVE, _bg_color)

        self._make_stress_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_derating_curve(self):
        """
        Load the benign and harsh environment derating curves.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # Plot the derating curve.
        _x = [
            float(_attributes['temperature_rated_min']),
            float(_attributes['temperature_knee']),
            float(_attributes['temperature_rated_max'])
        ]

        self.pltDerate.axis.cla()
        self.pltDerate.axis.grid(True, which='both')

        self.pltDerate.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[0],
            plot_type='scatter',
            marker='r.-')

        self.pltDerate.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[1],
            plot_type='scatter',
            marker='b.-')

        self.pltDerate.do_load_plot(
            x_values=[_attributes['temperature_active']],
            y_values=[_attributes['current_ratio']],
            plot_type='scatter',
            marker='go')

        self.pltDerate.do_make_title(
            _(u"Current Derating Curve for {0:s} at {1:s}").format(
                _attributes['part_number'], _attributes['ref_des']),
            fontsize=12)
        self.pltDerate.do_make_legend([
            _(u"Harsh Environment"),
            _(u"Mild Environment"),
            _(u"Current Operating Point")
        ])

        self.pltDerate.do_make_labels(
            _(u"Temperature (\u2070C)"), 0, -0.2, fontsize=10)
        self.pltDerate.do_make_labels(
            _(u"Current Ratio"), -1, 0, set_x=False, fontsize=10)

        self.pltDerate.figure.canvas.draw()

        return _return

    def _do_load_page(self):
        """
        Load the switch assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtCurrentRatio.set_text(
            str(self.fmt.format(_attributes['current_ratio'])))
        self.chkOverstress.set_active(_attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(_attributes['reason'])

        self._do_load_derating_curve()

        return _return

    def _make_stress_results_page(self):
        """
        Make the switch gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Create the left side.
        _fixed = gtk.Fixed()
        self.pack1(_fixed, True, True)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, _fixed, 5, 35)
        _x_pos += 50

        _fixed.put(self.txtCurrentRatio, _x_pos, _y_pos[0])
        _fixed.put(self.chkOverstress, _x_pos, _y_pos[1])
        _fixed.put(self.txtReason.scrollwindow, _x_pos, _y_pos[2])

        _fixed.show_all()

        # Create the derating plot.
        _frame = rtk.RTKFrame(label=_(u"Derating Curve and Operating Point"))
        _frame.add(self.pltDerate.plot)
        _frame.show_all()

        self.pack2(_frame, True, True)

        return _return

    def on_select(self, module_id=None):
        """
        Load the switch assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited switch.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_load_page()

        return _return
