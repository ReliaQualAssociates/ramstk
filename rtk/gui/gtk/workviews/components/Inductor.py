# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Inductor.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Hardware Work View."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611


class AssessmentInputs(gtk.Fixed):
    """
    Display Hardware assessment input attribute data in the RTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Hardware assessment input view are:

    :cvar dict _dic_specifications: dictionary of inductor MIL-SPECs.  Key is
                                    inductor subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of inductor styles defined in the
                            MIL-SPECs.  Key is inductor subcategory ID; values
                            are lists of styles.

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the inductor
                               currently being displayed.

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

    +----------+------------------------------+
    | Position | Widget - Signal              |
    +==========+==============================+
    |     0    | cmbInsulation - `changed`    |
    +----------+------------------------------+
    |     1    | cmbSpecification - `changed` |
    +----------+------------------------------+
    |     2    | cmbFamily - `changed`        |
    +----------+------------------------------+
    |     3    | cmbConstruction - `changed`  |
    +----------+------------------------------+
    |     4    | txtArea - `changed`          |
    +----------+------------------------------+
    |     5    | txtWeight - `changed`        |
    +----------+------------------------------+
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

    # Define private list attributes.
    _lst_labels = [
        _(u"Quality:"),
        _(u"Specification:"),
        _(u"Insulation Class:"),
        _(u"Area:"),
        _(u"Weight:"),
        _(u"Family:"),
        _(u"Construction:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Inductor assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                inductor.
        :param int subcategory_id: the ID of the inductor subcategory.
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
            tooltip=_(u"The quality level of the inductive device."))
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
        Load the specification RKTComboBox().

        This method is used to load the specification RTKComboBox() whenever
        the inductor subcategory is changed.

        :param int subcategory_id: the newly selected inductor subcategory ID.
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
            _data = [[_(u"Established Reliability")], ["MIL-SPEC"],
                     [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []

        self.cmbQuality.do_load_combo(_data)

        # Load the specification RTKComboBox().
        _model = self.cmbSpecification.get_model()
        _model.clear()

        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        # Load the insulation class RTKComboBox().
        _model = self.cmbInsulation.get_model()
        _model.clear()

        try:
            _data = self._dic_insulation[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbInsulation.do_load_combo(_data)

        # Load the transformer family RTKComboBox().
        _model = self.cmbFamily.get_model()
        _model.clear()

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
        _model = self.cmbConstruction.get_model()
        _model.clear()

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

        # Build the container for inductors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])
        self.put(self.cmbSpecification, _x_pos, _y_pos[1])
        self.put(self.cmbInsulation, _x_pos, _y_pos[2])
        self.put(self.txtArea, _x_pos, _y_pos[3])
        self.put(self.txtWeight, _x_pos, _y_pos[4])
        self.put(self.cmbFamily, _x_pos, _y_pos[5])
        self.put(self.cmbConstruction, _x_pos, _y_pos[6])

        self._do_set_sensitive()

        self.show_all()

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
            |    0    | cmbQuality       |    3    | cmbFamily        |
            +---------+------------------+---------+------------------+
            |    1    | cmbSpecification |    4    | cmbConstruction  |
            +---------+------------------+---------+------------------+
            |    2    | cmbInsulation    |         |                  |
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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(_attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        self.cmbFamily.handler_block(self._lst_handler_id[3])
        self.cmbFamily.set_active(_attributes['family_id'])
        self.cmbFamily.handler_unblock(self._lst_handler_id[3])

        self._do_set_sensitive()

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

        return _return


class StressInputs(gtk.Fixed):
    """
    Display Inductor stress input attribute data in the RTK Work Book.

    The Inductor stress input view displays all the assessment inputs for
    the selected inductor.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a inductor stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the inductor
                               currently being displayed.

    :ivar txtTemperatureRated: enter and display the maximum rated temperature
                               of the inductive device.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           inductive device.
    :ivar txtVoltageAC: enter and display the operating ac voltage of the
                        inductive device.
    :ivar txtVoltageDC: enter and display the operating DC voltage of the
                        inductive device.
    :ivar txtPowerOperating: enter and display the operating power of the
                             inductive device.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTemperatureRated - `changed`           |
    +----------+-------------------------------------------+
    |     1    | txtVoltageRated - `changed`               |
    +----------+-------------------------------------------+
    |     2    | txtVoltageAC - `changed`                  |
    +----------+-------------------------------------------+
    |     3    | txtVoltageDC - `changed`                  |
    +----------+-------------------------------------------+
    |     4    | txtPowerOperating - `changed`             |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Minimum Rated Temperature (\u00B0C):"),
        _(u"Knee Temperature (\u00B0C):"),
        _(u"Maximum Rated Temperature (\u00B0C):"),
        _(u"Rated Voltage (V):"),
        _(u"Operating ac Voltage (V):"),
        _(u"Operating DC Voltage (V):"),
        _(u"Operating Power (W):")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Inductor stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                inductor.
        :param int subcategory_id: the ID of the inductor subcategory.
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
                u"The break temperature (in \u00B0C) of the inductor beyond "
                u"which it must be derated."))
        self.txtTemperatureRatedMin = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The minimum rated temperature (in \u00B0C) of the inductive "
                u"device."))
        self.txtTemperatureRatedMax = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The maximum rated temperature (in \u00B0C) of the inductive "
                u"device."))
        self.txtVoltageRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated voltage (in V) of the inductive device."))
        self.txtVoltageAC = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating ac voltage (in V) of the inductive "
                      u"device."))
        self.txtVoltageDC = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating DC voltage (in V) of the inductive "
                      u"device."))
        self.txtPowerOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating power (in W) of the inductive device."))

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
            self.txtVoltageAC.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtVoltageDC.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtPowerOperating.connect('changed', self._on_focus_out, 6))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the inductor module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for inductors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[2])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[3])
        self.put(self.txtVoltageAC, _x_pos, _y_pos[4])
        self.put(self.txtVoltageDC, _x_pos, _y_pos[5])
        self.put(self.txtPowerOperating, _x_pos, _y_pos[6])

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

            +---------+------------------------+---------+-------------------+
            |  Index  | Widget                 |  Index  | Widget            |
            +=========+========================+=========+===================+
            |    0    | txtTemperatureRatedMin |    4    | txtVoltageAC      |
            +---------+------------------------+---------+-------------------+
            |    1    | txtTemperatureKnee     |    5    | txtVoltageDC      |
            +---------+------------------------+---------+-------------------+
            |    2    | txtTemperatureRatedMax |    6    | txtPowerOperating |
            +---------+------------------------+---------+-------------------+
            |    3    | txtVoltageRated        |         |                   |
            +---------+------------------------+---------+-------------------+

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
                _attributes['voltage_ac_operating'] = _text
            elif index == 5:
                _attributes['voltage_dc_operating'] = _text
            elif index == 6:
                _attributes['power_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the inductor stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              inductor.
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

        self.txtVoltageAC.handler_block(self._lst_handler_id[4])
        self.txtVoltageAC.set_text(
            str(self.fmt.format(_attributes['voltage_ac_operating'])))
        self.txtVoltageAC.handler_unblock(self._lst_handler_id[4])

        self.txtVoltageDC.handler_block(self._lst_handler_id[5])
        self.txtVoltageDC.set_text(
            str(self.fmt.format(_attributes['voltage_dc_operating'])))
        self.txtVoltageDC.handler_unblock(self._lst_handler_id[5])

        self.txtPowerOperating.handler_block(self._lst_handler_id[6])
        self.txtPowerOperating.set_text(
            str(self.fmt.format(_attributes['power_operating'])))
        self.txtPowerOperating.handler_unblock(self._lst_handler_id[6])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display inductor assessment results attribute data in the RTK Work Book.

    The inductor assessment result view displays all the assessment results
    for the selected inductor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a inductor assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the inductor
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the inductor.
    :ivar txtPiC: displays the construction factor for the inductor.
    :ivar txtPiQ: displays the quality factor for the inductor.
    :ivar txtPiE: displays the environment factor for the inductor.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private list attributes.
    _lst_labels = [
        u"\u03BB<sub>b</sub>:", u"\u03C0<sub>C</sub>:", u"\u03C0<sub>Q</sub>:",
        u"\u03C0<sub>E</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Inductor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                inductor.
        :param int subcategory_id: the ID of the inductor subcategory.
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
            tooltip=_(u"The assessment model used to calculate the inductive "
                      u"device's failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the inductive device."))
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The construction factor for the coil."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the inductive device."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the inductive device."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self.on_select, 'calculatedHardware')

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected inductor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

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

        # Build the container for inductors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiC, _x_pos, _y_pos[1])
        self.put(self.txtPiQ, _x_pos, _y_pos[2])
        self.put(self.txtPiE, _x_pos, _y_pos[3])

        self.show_all()

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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self._do_set_sensitive()

        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))

        return _return


class StressResults(gtk.HPaned):
    """
    Display inductor stress results attribute data in the RTK Work Book.

    The inductor stress result view displays all the stress results for the
    selected inductor.  This includes, currently, results for MIL-HDBK-217FN2
    parts count and MIL-HDBK-217FN2 part stress methods.  The attributes of a
    inductor stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the inductor
                               currently being displayed.

    :ivar txtTemperareRise: enter and display the temperature rise of the
                            inductive device.
    :ivar txtTemperatureHotSpot: enter and display the inductive device's hot
                                 spot temperature.
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Voltage Ratio:"),
        _(u"Temperature Rise (C):"),
        _("Hot Spot Temperature (C):"), "",
        _(u"Overstress Reason:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Inductor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                inductor.
        :param int subcategory_id: the ID of the inductor subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.5, 0.6, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.pltDerate = rtk.RTKPlot()

        self.chkOverstress = rtk.RTKCheckButton(
            label=_(u"Overstressed"),
            tooltip=_(u"Indicates whether or not the selected inductor "
                      u"is overstressed."))
        self.txtReason = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=250,
            tooltip=_(u"The reason(s) the selected hardware item is "
                      u"overstressed."))
        self.txtVoltageRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating voltage to rated voltage for "
                      u"the inductor."))
        self.txtTemperatureRise = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The average temperature rise (in C) over ambient of "
                      u"the inductive device."))
        self.txtTemperatureHotSpot = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The hot spot temperature (in C) of the inductive "
                      u"device."))

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

        pub.subscribe(self.on_select, 'calculatedHardware')

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
            y_values=[_attributes['voltage_ratio']],
            plot_type='scatter',
            marker='go')

        self.pltDerate.do_load_plot(
            x_values=[_attributes['temperature_active']],
            y_values=[_attributes['current_ratio']],
            plot_type='scatter',
            marker='mo')

        self.pltDerate.do_make_title(
            _(u"Voltage and Current Derating Curve for {0:s} at {1:s}").format(
                _attributes['part_number'], _attributes['ref_des']),
            fontsize=12)
        self.pltDerate.do_make_legend([
            _(u"Harsh Environment"),
            _(u"Mild Environment"),
            _(u"Voltage Operating Point")
        ])

        self.pltDerate.do_make_labels(
            _(u"Temperature (\u2070C)"), 0, -0.2, fontsize=10)
        self.pltDerate.do_make_labels(
            _(u"Voltage/Current Ratio"), -1, 0, set_x=False, fontsize=10)

        self.pltDerate.figure.canvas.draw()

        return _return

    def _make_stress_results_page(self):
        """
        Make the inductor gtk.Notebook() assessment results page.

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
        _fixed.put(self.txtTemperatureRise, _x_pos, _y_pos[1])
        _fixed.put(self.txtTemperatureHotSpot, _x_pos, _y_pos[2])
        _fixed.put(self.chkOverstress, _x_pos, _y_pos[3])
        _fixed.put(self.txtReason.scrollwindow, _x_pos, _y_pos[4])

        _fixed.show_all()

        # Create the derating plot.
        _frame = rtk.RTKFrame(label=_(u"Derating Curve and Operating Point"))
        _frame.add(self.pltDerate.plot)
        _frame.show_all()

        self.pack2(_frame, True, True)

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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtVoltageRatio.set_text(
            str(self.fmt.format(_attributes['voltage_ratio'])))
        self.txtTemperatureRise.set_text(
            str(self.fmt.format(_attributes['temperature_rise'])))
        self.txtTemperatureHotSpot.set_text(
            str(self.fmt.format(_attributes['temperature_hot_spot'])))
        self.chkOverstress.set_active(_attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(_attributes['reason'])

        self._do_load_derating_curve()

        return _return
