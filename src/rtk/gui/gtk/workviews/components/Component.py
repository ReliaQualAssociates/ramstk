# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Component.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Component Base Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk


class AssessmentInputs(gtk.Fixed):
    """
    Display Hardware assessment input attribute data in the RAMSTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analyses.  The attributes of a
    Hardware assessment input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the hardware item
                               currently being displayed.

    :ivar cmbQuality: select and display the quality level of the hardware
                      item.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | cmbQuality - `changed`                    |
    +----------+-------------------------------------------+
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Hardware assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                hardware item.
        :param int subcategory_id: the ID of the hardware item subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []
        self._lst_labels = [
            _(u"Quality Level:"),
        ]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = kwargs['hardware_id']
        self._subcategory_id = kwargs['subcategory_id']

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.cmbQuality = rtk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The quality level of the hardware item."))

    def do_load_comboboxes(self, **kwargs):
        """
        Load the assessment input RKTComboBox()s.

        :param int subcategory_id: the newly selected hardware item
                                   subcategory ID.
        :return: _attributes
        :rtype: dict
        """
        self._subcategory_id = kwargs['subcategory_id']

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        return _attributes

    def do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Component assessment input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(_attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        return _attributes

    def do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected hardware item.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)

        return None

    def make_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: _x_pos, _y_pos
        :rtype: tuple
        """
        self.do_load_comboboxes(subcategory_id=self._subcategory_id)
        self.do_set_sensitive()

        # Build the assessment input container for hardware items.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])

        return _x_pos, _y_pos

    def on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to hardware item attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |         |                  |
            +---------+------------------+---------+------------------+

        :return: _attributes
        :rtype: dict
        """
        _attributes = {}

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 0:
                _attributes['quality_id'] = int(combo.get_active())

        return _attributes

    def on_select(self, module_id, **kwargs):
        """
        Load the hardware item assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              hardware item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        return self._do_load_page(**kwargs)


class StressInputs(gtk.Fixed):
    """
    Display hardware item stress input attribute data in the RAMSTK Work Book.

    The hardware item stress input view displays all the assessment inputs for
    the selected hardware item.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a hardware item stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the hardware item
                               currently being displayed.

    :ivar txtTemperatureRatedMin: enter and display the minimum rated
                                  temperature of the hardware item.
    :ivar txtTemperatureKnee: enter and display the temperature above which the
                              hardware item must be derated.
    :ivar txtTemperatureRatedMax: enter and display the maximum rated
                                  temperature of the hardware item.
    :ivar txtCurrentRated:
    :ivar txtCurrentOperating:
    :ivar txtPowerRated:
    :ivar txtPowerOperating:
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           hardware item.
    :ivar txtVoltageAC: enter and display the operating ac voltage of the
                        hardware item.
    :ivar txtVoltageDC: enter and display the operating DC voltage of the
                        hardware item.

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
    |   5   | txtPowerRated - `changed`                 |
    +-------+-------------------------------------------+
    |   6   | txtPowerOperating - `changed`             |
    +-------+-------------------------------------------+
    |   7   | txtVoltageRated - `changed`               |
    +-------+-------------------------------------------+
    |   8   | txtVoltageAC - `changed`                  |
    +-------+-------------------------------------------+
    |   9   | txtVoltageDC - `changed`                  |
    +-------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Minimum Rated Temperature (\u00B0C):"),
        _(u"Knee Temperature (\u00B0C):"),
        _(u"Maximum Rated Temperature (\u00B0C):"),
        _(u"Rated Current (A):"),
        _(u"Operating Current (A):"),
        _(u"Rated Power (W):"),
        _(u"Operating Power (W):"),
        _(u"Rated Voltage (V):"),
        _(u"Operating ac Voltage (V):"),
        _(u"Operating DC Voltage (V):")
    ]

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Hardware stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                hardware item.
        :param int subcategory_id: the ID of the hardware item subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = kwargs['hardware_id']
        self._subcategory_id = kwargs['subcategory_id']

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtTemperatureRatedMin = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The minimum rated temperature (in \u00B0C) of the "
                      u"hardware item."))
        self.txtTemperatureKnee = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"The break temperature (in \u00B0C) of the hardware item "
                u"beyond which it must be derated."))
        self.txtTemperatureRatedMax = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(
                u"The maximum rated temperature (in \u00B0C) of the hardware "
                u"item."))
        self.txtCurrentRated = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The rated current (in A) of the hardware item."))
        self.txtCurrentOperating = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The operating current (in A) of the hardware item."))
        self.txtPowerRated = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The rated power (in W) of the hardware item."))
        self.txtPowerOperating = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The operating power (in W) of the hardware item."))
        self.txtVoltageRated = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The rated voltage (in V) of the hardware item."))
        self.txtVoltageAC = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The operating ac voltage (in V) of the hardware "
                      u"item."))
        self.txtVoltageDC = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The operating DC voltage (in V) of the hardware "
                      u"item."))

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
        self._lst_handler_id.append(
            self.txtPowerRated.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtPowerOperating.connect('changed', self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('changed', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtVoltageAC.connect('changed', self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtVoltageDC.connect('changed', self._on_focus_out, 9))

        self._make_page()
        self.show_all()

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Component stress input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # We don't block the callback signal otherwise the style RAMSTKComboBox()
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

        self.txtPowerRated.handler_block(self._lst_handler_id[5])
        self.txtPowerRated.set_text(
            str(self.fmt.format(_attributes['power_rated'])))
        self.txtPowerRated.handler_unblock(self._lst_handler_id[5])

        self.txtPowerOperating.handler_block(self._lst_handler_id[6])
        self.txtPowerOperating.set_text(
            str(self.fmt.format(_attributes['power_operating'])))
        self.txtPowerOperating.handler_unblock(self._lst_handler_id[6])

        self.txtVoltageRated.handler_block(self._lst_handler_id[7])
        self.txtVoltageRated.set_text(
            str(self.fmt.format(_attributes['voltage_rated'])))
        self.txtVoltageRated.handler_unblock(self._lst_handler_id[7])

        self.txtVoltageAC.handler_block(self._lst_handler_id[8])
        self.txtVoltageAC.set_text(
            str(self.fmt.format(_attributes['voltage_ac_operating'])))
        self.txtVoltageAC.handler_unblock(self._lst_handler_id[8])

        self.txtVoltageDC.handler_block(self._lst_handler_id[9])
        self.txtVoltageDC.set_text(
            str(self.fmt.format(_attributes['voltage_dc_operating'])))
        self.txtVoltageDC.handler_unblock(self._lst_handler_id[9])

        return _return

    def _make_page(self):
        """
        Make the Hardware module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[2])
        self.put(self.txtCurrentRated, _x_pos, _y_pos[3])
        self.put(self.txtCurrentOperating, _x_pos, _y_pos[4])
        self.put(self.txtPowerRated, _x_pos, _y_pos[5])
        self.put(self.txtPowerOperating, _x_pos, _y_pos[6])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[7])
        self.put(self.txtVoltageAC, _x_pos, _y_pos[8])
        self.put(self.txtVoltageDC, _x_pos, _y_pos[9])

        self.show_all()

        return None

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the method.
        :type entry: :class:`rtk.gui.gtk.rtk.RAMSTKEntry` or
                     :class:`rtk.gui.gtk.rtk.RAMSTKTextView`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

            +-------+------------------------+-------+-------------------+
            | Index | Widget                 | Index | Widget            |
            +=======+========================+=======+===================+
            |   0   | txtTemperatureRatedMin |   5   | txtPowerRated     |
            +-------+------------------------+-------+-------------------+
            |   1   | txtTemperatureKnee     |   6   | txtPowerOperating |
            +-------+------------------------+-------+-------------------+
            |   2   | txtTemperatureRatedMax |   7   | txtVoltageRated   |
            +-------+------------------------+-------+-------------------+
            |   3   | txtCurrentRated        |   8   | txtVoltageAC      |
            +-------+------------------------+-------+-------------------+
            |   4   | txtCurrentOperating    |   9   | txtVoltageDC      |
            +-------+------------------------+-------+-------------------+

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
            elif index == 5:
                _attributes['power_rated'] = _text
            elif index == 6:
                _attributes['power_operating'] = _text
            elif index == 7:
                _attributes['voltage_rated'] = _text
            elif index == 8:
                _attributes['voltage_ac_operating'] = _text
            elif index == 9:
                _attributes['voltage_dc_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id, **kwargs):
        """
        Load the hardware item stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              hardware item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        return self._do_load_page(**kwargs)


class AssessmentResults(gtk.Fixed):
    """
    Display Hardware assessment results attribute data in the RAMSTK Work Book.

    The Hardware assessment result view displays all the assessment results
    for the selected hardware item.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a Hardware assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the hardware item
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RAMSTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the hardware item.
    :ivar txtPiQ: displays the quality factor for the hardware item.
    :ivar txtPiE: displays the environment factor for the hardware item.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Hardware assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                hardware item.
        :param int subcategory_id: the ID of the hardware item subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
            u"\u03C0<sub>E</sub>:"
        ]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = kwargs['hardware_id']
        self._subcategory_id = kwargs['subcategory_id']

        self._lblModel = rtk.RAMSTKLabel(
            '',
            tooltip=_(u"The assessment model used to calculate the hardware "
                      u"item failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the hardware item."))
        self.txtPiQ = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the hardware item."))
        self.txtPiE = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the hardware item."))

    def do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Hardware assessment results page.

        :return: _attributes
        :rtype: dict
        """
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))

        return _attributes

    def do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected hardware item.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self.txtPiQ.set_sensitive(True)
        self.txtPiE.set_sensitive(False)

        return _return

    def make_page(self):
        """
        Make the Hardware gtk.Notebook() assessment results page.

        :return: _x_pos, _y_pos
        :rtype: tuple
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

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiQ, _x_pos, _y_pos[1])
        self.put(self.txtPiE, _x_pos, _y_pos[2])

        return _x_pos, _y_pos


class StressResults(gtk.HPaned):
    """
    Display Hardware stress results attribute data in the RAMSTK Work Book.

    The Hardware stress result view displays all the stress results for the
    selected hardware item.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of a
    Hardware stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the hardware item
                               currently being displayed.

    :ivar chkOverstressed: display whether or not the selected hardware item is
                           overstressed.
    :ivar txtCurrentRatio: display the ratio of operating current to rated
                           current.
    :ivar txtPowerRatio: display the ratio of operating power to rated power.
    :ivar txtVoltageRatio: display the ratio of operating voltage (ac + DC) to
                           rated voltage.
    :ivar txtReason: display the reason(s) the hardware item is overstressed.
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Current Ratio:"),
        _(u"Power Ratio:"),
        _(u"Voltage Ratio:"), "",
        _(u"Overstress Reason:")
    ]

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Hardware assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                hardware item.
        :param int subcategory_id: the ID of the hardware item subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = kwargs['hardware_id']
        self._subcategory_id = kwargs['subcategory_id']

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.pltDerate = rtk.RAMSTKPlot()

        self.chkOverstress = rtk.RAMSTKCheckButton(
            label=_(u"Overstressed"),
            tooltip=_(u"Indicates whether or not the selected hardware item "
                      u"is overstressed."))
        self.txtCurrentRatio = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating current to rated current for "
                      u"the hardware item."))
        self.txtPowerRatio = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating power to rated power for "
                      u"the hardware item."))
        self.txtVoltageRatio = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating voltage to rated voltage for "
                      u"the hardware item."))
        self.txtReason = rtk.RAMSTKTextView(
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

        self._make_page()
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
            y_values=[_attributes['voltage_ratio']],
            plot_type='scatter',
            marker='go')

        self.pltDerate.do_make_title(
            _(u"Voltage Derating Curve for {0:s} at {1:s}").format(
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
            _(u"Voltage Ratio"), -1, 0, set_x=False, fontsize=10)

        self.pltDerate.figure.canvas.draw()

        return _return

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Hardware assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtCurrentRatio.set_text(
            str(self.fmt.format(_attributes['current_ratio'])))
        self.txtPowerRatio.set_text(
            str(self.fmt.format(_attributes['power_ratio'])))
        self.txtVoltageRatio.set_text(
            str(self.fmt.format(_attributes['voltage_ratio'])))
        self.chkOverstress.set_active(_attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(_attributes['reason'])

        self._do_load_derating_curve()

        return _return

    def _make_page(self):
        """
        Make the Hardware gtk.Notebook() assessment results page.

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
        _fixed.put(self.txtPowerRatio, _x_pos, _y_pos[1])
        _fixed.put(self.txtVoltageRatio, _x_pos, _y_pos[2])
        _fixed.put(self.chkOverstress, _x_pos, _y_pos[3])
        _fixed.put(self.txtReason.scrollwindow, _x_pos, _y_pos[4])

        _fixed.show_all()

        # Create the derating plot.
        _frame = rtk.RAMSTKFrame(
            label=_(u"Derating Curve and Operating Point"))
        _frame.add(self.pltDerate.plot)
        _frame.show_all()

        self.pack2(_frame, True, True)

        return _return

    def on_select(self, module_id, **kwargs):
        """
        Load the Hardware assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              hardware item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        return self._do_load_page(**kwargs)
