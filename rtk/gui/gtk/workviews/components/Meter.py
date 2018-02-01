# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Meter.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Meter Work View."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611


class AssessmentInputs(gtk.Fixed):
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

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Meter item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the meter
                               currently being displayed.

    :ivar cmbApplication: select and display the application of the meter.
    :ivar cmbType: select and display the type of meter.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | cmbQuality - `changed`                    |
    +----------+-------------------------------------------+
    |     1    | cmbApplication - `changed`                |
    +----------+-------------------------------------------+
    |     2    | cmbType - `changed`                       |
    +----------+-------------------------------------------+
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

    # Define private list attributes.
    _lst_labels = [
        _(u"Quality Level:"),
        _(u"Meter Type:"),
        _(u"Meter Function:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Meter assessment input view.

        :param controller: the meter data controller instance.
        :type controller: :class:`rtk.meter.Controller.MeterBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected meter.
        :param int subcategory_id: the ID of the meter subcategory.
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
            tooltip=_(u"The quality level of the meter."))
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

        self._subcategory_id = subcategory_id

        # Load the quality level RTKComboBox().
        _model = self.cmbQuality.get_model()
        _model.clear()

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
        _model = self.cmbApplication.get_model()
        _model.clear()

        self.cmbApplication.do_load_combo([[_(u"Ammeter")], [_(u"Voltmeter")],
                                           [_(u"Other")]])

        # Load the meter type RTKComboBox().
        _model = self.cmbType.get_model()
        _model.clear()

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

        self.cmbQuality.set_sensitive(True)
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
        # Load the gtk.ComboBox() widgets.
        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for meters.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])
        self.put(self.cmbType, _x_pos, _y_pos[1])
        self.put(self.cmbApplication, _x_pos, _y_pos[2])

        self.show_all()

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

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    2    | cmbType          |
            +---------+------------------+---------+------------------+
            |    1    | cmbApplication   |         |                  |
            +---------+------------------+---------+------------------+

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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(_attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        self.cmbApplication.handler_block(self._lst_handler_id[1])
        self.cmbApplication.set_active(_attributes['application_id'])
        self.cmbApplication.handler_unblock(self._lst_handler_id[1])

        self.cmbType.handler_block(self._lst_handler_id[2])
        self.cmbType.set_active(_attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[2])

        return _return


class StressInputs(gtk.Fixed):
    """
    Display Meter stress input attribute data in the RTK Work Book.

    The Meter stress input view displays all the assessment inputs for
    the selected meter.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a meter stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Meter BoM data controller instance.

    :ivar int _hardware_id: the ID of the Meter item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the meter
                               currently being displayed.

    :ivar txtTemperatureRated: enter and display the maximum rated temperature
                               of the elapsed time meter.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTemperatureRatedMAx - `changed`        |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [_(u"Maximum Rated Temperature (\u00B0C):")]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Meter stress input view.

        :param controller: the meter data controller instance.
        :type controller: :class:`rtk.meter.Controller.MeterBoMDataController`
        :param int hardware_id: the meter ID of the currently selected
                                meter.
        :param int subcategory_id: the ID of the meter subcategory.
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

        self.txtTemperatureRatedMax = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The maximum rated temperature (in \u00B0C) of the meter."))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect('changed', self._on_focus_out,
                                                0))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the meter module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for meters.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[0])

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
        :param int index: the position in the Meter class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

        +---------+------------------------+---------+---------------------+
        |  Index  | Widget                 |  Index  | Widget              |
        +=========+========================+=========+=====================+
        |    0    | txtTemperatureRatedMax |         |                     |
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
                _attributes['temperature_rated_max'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the meter stress input work view widgets.

        :param int module_id: the Meter ID of the selected/edited
                              meter.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # We don't block the callback signal otherwise the style RTKComboBox()
        # will not be loaded and set.
        self.txtTemperatureRatedMax.handler_block(self._lst_handler_id[0])
        self.txtTemperatureRatedMax.set_text(
            str(self.fmt.format(_attributes['temperature_rated_max'])))
        self.txtTemperatureRatedMax.handler_unblock(self._lst_handler_id[0])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display meter assessment results attribute data in the RTK Work Book.

    The meter assessment result view displays all the assessment results
    for the selected meter.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a meter assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Meter item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the meter
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the meter.
    :ivar txtPiA: displays the application factor for the panel meter.
    :ivar txtPiF: displays the function factor for the panel meter.
    :ivar txtPiT: displays the temperature stress factor for the elapsed time
                  meter.
    :ivar txtPiQ: displays the quality factor for the meter.
    :ivar txtPiE: displays the environment factor for the meter.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private list attributes.
    _lst_labels = [
        u"\u03BB<sub>b</sub>:", u"\u03C0<sub>A</sub>:", u"\u03C0<sub>F</sub>:",
        u"\u03C0<sub>T</sub>:", u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Meter assessment result view.

        :param controller: the meter data controller instance.
        :type controller: :class:`rtk.meter.Controller.MeterBoMDataController`
        :param int hardware_id: the meter ID of the currently selected
                                meter.
        :param int subcategory_id: the ID of the meter subcategory.
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
            tooltip=_(u"The assessment model used to calculate the meter "
                      u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the meter."))
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
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the meter."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the meter."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self.on_select, 'calculatedHardware')

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected meter.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiA.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtPiQ.set_sensitive(True)
        self.txtPiE.set_sensitive(False)

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

        # Build the container for meters.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiA, _x_pos, _y_pos[1])
        self.put(self.txtPiF, _x_pos, _y_pos[2])
        self.put(self.txtPiT, _x_pos, _y_pos[3])
        self.put(self.txtPiQ, _x_pos, _y_pos[4])
        self.put(self.txtPiE, _x_pos, _y_pos[5])

        self.show_all()

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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self.txtPiA.set_text(str(self.fmt.format(_attributes['piA'])))
        self.txtPiF.set_text(str(self.fmt.format(_attributes['piF'])))
        self.txtPiT.set_text(str(self.fmt.format(_attributes['piT'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))

        self._do_set_sensitive()

        return _return


class StressResults(gtk.HPaned):
    """
    Display meter stress results attribute data in the RTK Work Book.

    The meter stress result view displays all the stress results for the
    selected meter.  This includes, currently, results for MIL-HDBK-217FN2
    parts count and MIL-HDBK-217FN2 part stress methods.  The attributes of a
    meter stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar _dtc_data_controller: the Meter BoM data controller instance.
    :ivar int _hardware_id: the ID of the Meter item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the meter
                               currently being displayed.

    :ivar txtTemperatureRatio: the :class:`rtk.gui.gtk.rtk.RTKEntry` displaying
                               the operating to rated temperature ratio for the
                               meter.
    """

    # Define private list attributes.
    _lst_labels = [_(u"Temperature Ratio:")]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Meter assessment result view.

        :param controller: the meter data controller instance.
        :type controller: :class:`rtk.meter.Controller.MeterBoMDataController`
        :param int hardware_id: the meter ID of the currently selected
                                meter.
        :param int subcategory_id: the ID of the meter subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.7, 0.7, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtTemperatureRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating temperature to rated "
                      u"temperature for the meter."))

        self._make_stress_results_page()
        self.show_all()

        pub.subscribe(self.on_select, 'calculatedHardware')

    def _make_stress_results_page(self):
        """
        Make the meter gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Create the left side.
        _fixed = gtk.Fixed()
        self.pack1(_fixed, True, True)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, _fixed, 5, 35)
        _x_pos += 50

        _fixed.put(self.txtTemperatureRatio, _x_pos, _y_pos[0])

        _fixed.show_all()

        return _return

    def on_select(self, module_id=None):
        """
        Load the meter assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              meter.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        try:
            _ratio = (_attributes['temperature_active'] /
                      _attributes['temperature_rated_max'])
        except ZeroDivisionError:
            _ratio = 1.0

        self.txtTemperatureRatio.set_text(str(self.fmt.format(_ratio)))

        return _return
