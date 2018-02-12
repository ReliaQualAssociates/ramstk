# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Miscellaneous.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hardware Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk


class AssessmentInputs(gtk.Fixed):
    """
    Display Hardware assessment input attribute data in the RTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Miscellaneous assessment input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.

    :ivar cmbApplication: select and display the application of the
                          miscellaneous item (lamps only).
    :ivar cmbType: the type of miscellaneous item (filters only).
    :ivar txtFrequency: enter and display the operating frequency of the
                        miscellaneous item (crystals only).
    :ivar txtUtilization: enter and display the utilization factor of the
                          miscellaneous item (lamps only).

    Callbacks signals in _lst_handler_id:

    +----------+----------------------------+
    | Position | Widget - Signal            |
    +==========+============================+
    |     0    | cmbQuality - `changed`     |
    +----------+----------------------------+
    |     1    | cmbApplication - `changed` |
    +----------+----------------------------+
    |     2    | cmbType - `changed`        |
    +----------+----------------------------+
    |     3    | txtFrequency - `changed`   |
    +----------+----------------------------+
    |     4    | txtUtilization - `changed` |
    +----------+----------------------------+
    """

    # Define private dict attributes.

    # Define private list attributes.
    _lst_labels = [
        _(u"Quality Level:"),
        _(u"Application:"),
        _(u"Type:"),
        _(u"Operating Frequency:"),
        _(u"Utilization:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Miscellaneous assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                miscellaneous.
        :param int subcategory_id: the ID of the miscellaneous subcategory.
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
            tooltip=_(u"The quality level of the hardware item."))
        self.cmbApplication = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The application of the lamp."))
        self.cmbType = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The type of electronic filter."))

        self.txtFrequency = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating frequency of the crystal."))
        self.txtUtilization = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The utilization factor (illuminate hours / equipment "
                      u"operate hours) of the lamp."))

        self._make_assessment_input_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.txtFrequency.connect('changed', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.txtUtilization.connect('changed', self._on_focus_out, 4))

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the miscellaneous RKTComboBox()s.

        This method is used to load the specification RTKComboBox() whenever
        the miscellaneous subcategory is changed.

        :param int subcategory_id: the newly selected miscellaneous hardware
                                   item subcategory ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._subcategory_id = subcategory_id

        # Load the quality level RTKComboBox().
        _model = self.cmbQuality.get_model()
        _model.clear()

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_(u"Lower")]])
        self.cmbApplication.do_load_combo([[_(u"Incandescent, AC")], [_(u"Incandescent, DC")]])
        if _attributes['hazard_rate_method_id'] == 1:
            self.cmbType.do_load_combo([[_(u"Ceramic-Ferrite")], [_(u"Discrete LC Components")], [_(u"Discrete LC and Crystal Components")]])
        elif _attributes['hazard_rate_method_id'] == 2:
            self.cmbType.do_load_combo([[_(u"MIL-F-15733 Ceramic-Ferrite")], [_(u"MIL-F-15733 Discrete LC Components")], [_(u"MIL-F-18327 Discrete LC Components")], [_(u"MIL-F-18327 Discrete LC and Crystal Components")]])

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected miscellaneous.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.set_sensitive(False)
        self.cmbApplication.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtFrequency.set_sensitive(False)
        self.txtUtilization.set_sensitive(False)

        if self._subcategory_id == 2:
            self.cmbApplication.set_sensitive(True)
        elif self._subcategory_id == 4:
            self.cmbType.set_sensitive(True)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id in [1, 4]:
                self.cmbQuality.set_sensitive(True)
        elif _attributes['hazard_rate_method_id'] == 2:
            if self._subcategory_id == 1:
                self.cmbQuality.set_sensitive(True)
                self.txtFrequency.set_sensitive(True)
            elif self._subcategory_id == 2:
                self.txtUtilization.set_sensitive(True)
            elif self._subcategory_id == 4:
                self.cmbQuality.set_sensitive(True)

        return _return

    def _make_assessment_input_page(self):
        """
        Make the Miscellaneous hardware class gtk.Notebook() assessment input
        page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for miscellaneouss.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])
        self.put(self.cmbApplication, _x_pos, _y_pos[1])
        self.put(self.cmbType, _x_pos, _y_pos[2])
        self.put(self.txtFrequency, _x_pos, _y_pos[3])
        self.put(self.txtUtilization, _x_pos, _y_pos[4])

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Miscellaneous attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +---------+------------------+
            |  Index  | Widget           |
            +=========+==================+
            |    0    | cmbQuality       |
            +---------+------------------+
            |    1    | cmbApplication   |
            +---------+------------------+
            |    2    | cmbType          |
            +---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 0:
                _attributes['quality_id'] = int(combo.get_active())
            elif index == 1:
                _attributes['application_id'] = int(combo.get_active())
            elif index == 2:
                _attributes['type_id'] = int(combo.get_active())

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

            +---------+---------------------+
            |  Index  | Widget              |
            +=========+=====================+
            |    3    | txtFrequency        |
            +---------+---------------------+
            |    4    | txtUtilization      |
            +---------+---------------------+

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

            if index == 3:
                _attributes['frequency_operating'] = _text
            elif index == 4:
                _attributes['duty_cycle'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the miscellaneous assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              miscellaneous.
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

        if self._subcategory_id == 2:
            self.cmbApplication.handler_block(self._lst_handler_id[1])
            self.cmbApplication.set_active(_attributes['application_id'])
            self.cmbApplication.handler_unblock(self._lst_handler_id[1])
        elif self._subcategory_id == 4:
            self.cmbType.handler_block(self._lst_handler_id[2])
            self.cmbType.set_active(_attributes['type_id'])
            self.cmbType.handler_unblock(self._lst_handler_id[2])

        if _attributes['hazard_rate_method_id'] == 2:
            if self._subcategory_id == 1:
                self.txtFrequency.handler_block(self._lst_handler_id[3])
                self.txtFrequency.set_text(
                    str(self.fmt.format(_attributes['frequency_operating'])))
                self.txtFrequency.handler_unblock(self._lst_handler_id[3])
            elif self._subcategory_id == 2:
                self.txtUtilization.handler_block(self._lst_handler_id[4])
                self.txtUtilization.set_text(str(self.fmt.format(_attributes['duty_cycle'])))
                self.txtUtilization.handler_unblock(self._lst_handler_id[4])

        self._do_set_sensitive()

        return _return


class StressInputs(gtk.Fixed):
    """
    Display Miscellaneous stress input attribute data in the RTK Work Book.

    The Miscellaneous stress input view displays all the assessment inputs for
    the selected miscellaneous.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a miscellaneous stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the miscellaneous
                               currently being displayed.

    :ivar txtTemperatureRated: enter and display the maximum rated temperature
                               of the miscellaneous.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           miscellaneous.
    :ivar txtVoltageOperating: enter and display the operating voltage of the
                               miscellaneous.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTemperatureRated - `changed`           |
    +----------+-------------------------------------------+
    |     1    | txtVoltageRated - `changed`               |
    +----------+-------------------------------------------+
    |     2    | txtVoltageOperating - `changed`           |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Minimum Rated Temperature (\u00B0C):"),
        _(u"Knee Temperature (\u00B0C):"),
        _(u"Maximum Rated Temperature (\u00B0C):"),
        _(u"Rated Voltage (V):"),
        _(u"Operating Voltage (V):")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Miscellaneous stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                miscellaneous.
        :param int subcategory_id: the ID of the miscellaneous subcategory.
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

        self.txtTemperatureKnee = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The break temperature (in \u00B0C) of the hardware item "
                u"beyond which it must be derated."))
        self.txtTemperatureRatedMin = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The minimum rated temperature (in \u00B0C) of the "
                u"hardware item."
            ))
        self.txtTemperatureRatedMax = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The maximum rated temperature (in \u00B0C) of the "
                u"hardware item."
            ))
        self.txtVoltageRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated voltage (in V) of the miscellaneous."))
        self.txtVoltageOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating voltage (in V) of the miscellaneous."))

        self._lst_handler_id.append(
            self.txtTemperatureRatedMin.connect('changed', self._on_focus_out,
                                                0))
        self._lst_handler_id.append(
            self.txtTemperatureKnee.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect('changed', self._on_focus_out,
                                                2))
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('changed', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.txtVoltageOperating.connect('changed', self._on_focus_out, 4))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the miscellaneous module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for miscellaneouss.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[2])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[3])
        self.put(self.txtVoltageOperating, _x_pos, _y_pos[4])

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

        +---------+------------------------+---------+---------------------+
        |  Index  | Widget                 |  Index  | Widget              |
        +=========+========================+=========+=====================+
        |    0    | txtTemperatureRatedMin |    3    | txtVoltageRated     |
        +---------+------------------------+---------+---------------------+
        |    1    | txtTemperatureKnee     |    4    | txtVoltageOperating |
        +---------+------------------------+---------+---------------------+
        |    2    | txtTemperatureRatedMax |         |                     |
        +---------+------------------------+---------+---------------------+

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
                _attributes['voltage_rated'] = _text
            elif index == 4:
                _attributes['voltage_dc_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the miscellaneous hardware item stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              miscellaneous.
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

        self.txtVoltageRated.handler_block(self._lst_handler_id[3])
        self.txtVoltageRated.set_text(
            str(self.fmt.format(_attributes['voltage_rated'])))
        self.txtVoltageRated.handler_unblock(self._lst_handler_id[3])

        self.txtVoltageOperating.handler_block(self._lst_handler_id[4])
        self.txtVoltageOperating.set_text(
            str(self.fmt.format(_attributes['voltage_dc_operating'])))
        self.txtVoltageOperating.handler_unblock(self._lst_handler_id[4])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display miscellaneous assessment results attribute data in the RTK Work Book.

    The miscellaneous hardware item assessment result view displays all the
    assessment results for the selected miscellaneous hardware item.  This
    includes, currently, results for MIL-HDBK-217FN2 parts count and
    MIL-HDBK-217FN2 part stress methods.  The attributes of a miscellaneous
    hardware item assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the miscellaneous
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the miscellaneous.
    :ivar txtPiQ: displays the quality factor for the miscellaneous.
    :ivar txtPiE: displays the environment factor for the miscellaneous.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1: u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2: u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3: u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub></span>",
        4: u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>U</sub>\u03C0<sub>A</sub>\u03C0<sub>E</sub></span>"}

    # Define private list attributes.
    _lst_labels = [
        u"", u"\u03C0<sub>U</sub>:", u"\u03C0<sub>A</sub>:", u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Miscellaneous assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                miscellaneous.
        :param int subcategory_id: the ID of the miscellaneous subcategory.
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
            width=-1,
            tooltip=_(u"The assessment model used to calculate the hardware "
                      u"item failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the hardware item."))
        self.txtPiU = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The utilization factor for the lamp."))
        self.txtPiA = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The application factor for the lamp."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the hardware item."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the hardware item."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the miscellaneous devices assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self.txtPiU.set_text(str(self.fmt.format(_attributes['piU'])))
        self.txtPiA.set_text(str(self.fmt.format(_attributes['piA'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected miscellaneous.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiU.set_sensitive(False)
        self.txtPiA.set_sensitive(False)
        self.txtPiQ.set_sensitive(False)
        self.txtPiE.set_sensitive(True)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id in [1, 4]:
                self.txtPiQ.set_sensitive(True)
            self.txtPiE.set_sensitive(False)
        elif _attributes['hazard_rate_method_id'] == 2:
            if self._subcategory_id in [1, 4]:
                self.txtPiQ.set_sensitive(True)
            elif self._subcategory_id == 2:
                self.txtPiU.set_sensitive(True)
                self.txtPiA.set_sensitive(True)

        return _return

    def _make_assessment_results_page(self):
        """
        Make the miscellaneous hardware item gtk.Notebook() assessment results
        page.

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
                self._lblModel.set_markup(self._dic_part_stress[self._subcategory_id])
            except KeyError:
                self._lblModel.set_markup(_(u"Missing Model"))
            self._lst_labels[0] = u"\u03BB<sub>b</sub>:"

        self._do_set_sensitive()

        # Build the container for miscellaneouss.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiU, _x_pos, _y_pos[1])
        self.put(self.txtPiA, _x_pos, _y_pos[2])
        self.put(self.txtPiQ, _x_pos, _y_pos[3])
        self.put(self.txtPiE, _x_pos, _y_pos[4])

        self.show_all()

        return None

    def on_select(self, module_id=None):
        """
        Load the miscellaneous assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              miscellaneous.
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
    Display miscellaneous stress results attribute data in the RTK Work Book.

    The miscellaneous stress result view displays all the stress results for the
    selected miscellaneous.  This includes, currently, results for MIL-HDBK-217FN2
    parts count and MIL-HDBK-217FN2 part stress methods.  The attributes of a
    miscellaneous stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.
    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the miscellaneous
                               currently being displayed.

    :ivar txtVoltageRatio: the :class:`rtk.gui.gtk.rtk.RTKEntry` displaying
                           the operating to rated voltage ratio for the
                           miscellaneous.
    :ivar txtCurrentRatio: the :class:`rtk.gui.gtk.rtk.RTKEntry` displaying
                           the operating to rated current ratio for the
                           miscellaneous.
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Voltage Ratio:"),
        _(u"Current Ratio:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Miscellaneous hardware item assessment
        result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                miscellaneous.
        :param int subcategory_id: the ID of the miscellaneous subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtVoltageRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating voltage to rated voltage for "
                      u"the miscellaneous."))
        self.txtCurrentRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating current to rated current for "
                      u"the miscellaneous."))

        self._make_stress_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the miscellaneous devices stress results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtVoltageRatio.set_text(
            str(self.fmt.format(_attributes['voltage_ratio'])))
        self.txtCurrentRatio.set_text(
            str(self.fmt.format(_attributes['current_ratio'])))

        return _return

    def _make_stress_results_page(self):
        """
        Make the miscellaneous gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Create the left side.
        _fixed = gtk.Fixed()
        self.pack1(_fixed, True, True)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, _fixed, 5, 35)
        _x_pos += 50

        _fixed.put(self.txtVoltageRatio, _x_pos, _y_pos[0])
        _fixed.put(self.txtCurrentRatio, _x_pos, _y_pos[1])

        _fixed.show_all()

        return _return

    def on_select(self, module_id=None):
        """
        Load the miscellaneous item assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              miscellaneous item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_load_page()

        return _return
