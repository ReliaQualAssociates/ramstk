# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Resistor.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Resistor Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk


class AssessmentInputs(gtk.Fixed):
    """
    Display Hardware assessment input attribute data in the RTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Hardware assessment input view are:

    :cvar dict _dic_specifications: dictionary of resistor MIL-SPECs.  Key is
                                    resistor subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of resistor styles defined in the
                            MIL-SPECs.  Key is resistor subcategory ID; values
                            are lists of styles.

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the resistor
                               currently being displayed.

    :ivar cmbSpecification: select and display the governing specification of
                            the resistor.
    :ivar cmbType: select and display the type of thermistor.
    :ivar cmbConstruction: select and display the method of construction of the
                           resistor.
    :ivar txtResistance: enter and display the resistance of the resistor.
    :ivar txtNElements: enter and display the number of active resistors in a
                        resistor network or the number of potentiometers taps.

    Callbacks signals in _lst_handler_id:

    +----------+------------------------------+
    | Position | Widget - Signal              |
    +==========+==============================+
    |     0    | cmbQuality - `changed`       |
    +----------+------------------------------+
    |     1    | cmbSpecification - `changed` |
    +----------+------------------------------+
    |     2    | cmbType - `changed`          |
    +----------+------------------------------+
    |     3    | cmbStyle - `changed`         |
    +----------+------------------------------+
    |     4    | cmbConstruction - `changed`  |
    +----------+------------------------------+
    |     5    | txtResistance - `changed`    |
    +----------+------------------------------+
    |     6    | txtNElements - `changed`     |
    +----------+------------------------------+
    """

    # Define private dict attributes.
    _dic_quality = {
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-R-11"], [_(u"Lower")]],
        2: [["S"], ["R"], ["P"], ["M"], ["MIL-R-10509"], ["MIL-R-22684"],
            [_(u"Lower")]],
        3: [["MIL-SPEC"], [_(u"Lower")]],
        4: [["MIL-SPEC"], [_(u"Lower")]],
        5: [["S"], ["R"], ["P"], ["M"], ["MIL-R-93"], [_(u"Lower")]],
        6: [["S"], ["R"], ["P"], ["M"], ["MIL-R-26"], [_(u"Lower")]],
        7: [["S"], ["R"], ["P"], ["M"], ["MIL-R-18546"], [_(u"Lower")]],
        8: [["MIL-SPEC"], [_(u"Lower")]],
        9: [["S"], ["R"], ["P"], ["M"], ["MIL-R-27208"], [_(u"Lower")]],
        10: [["MIL-SPEC"], [_(u"Lower")]],
        11: [["MIL-SPEC"], [_(u"Lower")]],
        12: [["MIL-SPEC"], [_(u"Lower")]],
        13: [["S"], ["R"], ["P"], ["M"], ["MIL-R-22097"], [_(u"Lower")]],
        14: [["MIL-SPEC"], [_(u"Lower")]],
        15: [["MIL-SPEC"], [_(u"Lower")]]
    }
    # Key is subcategory ID; index is specification ID.
    _dic_specifications = {
        2: [["MIL-R-10509"], ["MIL-R-22684"], ["MIL-R-39017"],
            ["MIL-R-55182"]],
        6: [["MIL-R-26"], ["MIL-R-39007"]],
        7: [["MIL-R-18546"], ["MIL-R-39009"]],
        15: [["MIL-R-23285"], ["MIL-R-39023"]]
    }
    # Key is subcategory ID, index is type ID.
    _dic_types = {
        1: [["RCR"], ["RC"]],
        2: [["RLR"], ["RL"], ["RNR"], ["RN"]],
        5: [["RBR"], ["RB"]],
        6: [["RWR"], ["RW"]],
        7: [["RER"], ["RE"]],
        9: [["RTR"], ["RT"]],
        11: [["RA"], ["RK"]],
        13: [["RJR"], ["RJ"]],
        15: [["RO"], ["RVC"]]
    }
    # First key is subcategory ID; second key is specification ID.
    # Index is style ID.
    _dic_styles = {
        6: {
            1: [["RWR 71"], ["RWR 74"], ["RWR 78"], ["RWR 80"], ["RWR 81"],
                ["RWR 82"], ["RWR 84"], ["RWR 89"]],
            2:
            [["RW 10"], ["RW 11"], ["RW 12"], ["RW 13"], ["RW 14"], ["RW 15"],
             ["RW 16"], ["RW 20"], ["RW 21 "], ["RW 22"], ["RW 23"], ["RW 24"],
             ["RW 29"], ["RW 30"], ["RW 31"], ["RW 32"], ["RW 33"], ["RW 34"],
             ["RW 35"], ["RW 36"], ["RW 37"], ["RW 38"], ["RW 39"], ["RW 47"],
             ["RW 55"], ["RW 56"], ["RW 67"], ["RW 68"], ["RW 69"], ["RW 70"],
             ["RW 74"], ["RW 78"], ["RW 79"], ["RW 80"], ["RW 81"]]
        },
        7: {
            1: [["RE 60/RER 60"], ["RE 65/RER 65"], ["RE 70/RER 70"],
                ["RE 75/RER 75"], ["RE 77"], ["RE 80"]],
            2: [["RE 60/RER40"], ["RE 65/RER 45"], ["RE 70/ RER 50"],
                ["RE 75/RER 55"], ["RE 77"], ["RE 80"]]
        }
    }
    # Key is subcategory ID; index is construction ID.
    _dic_construction = {
        10: ["2", "3", "4", "5"],
        12: [[_(u"Enclosed")], [_(u"Unenclosed")]]
    }

    # Define private list attributes.
    _lst_labels = [
        _(u"Resistance (\u03A9):"),
        _(u"Quality Level:"),
        _(u"Specification:"),
        _(u"Type:"),
        _(u"Style:"),
        _(u"Construction:"),
        _(u"Number of Elements:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Resistor assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                resistor.
        :param int subcategory_id: the ID of the resistor subcategory.
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
            tooltip=_(u"The quality level of the resistor."))
        self.cmbSpecification = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The governing specification for the resistor."))
        self.cmbType = rtk.RTKComboBox(
            index=0, simple=False, tooltip=_(u"The type of thermistor."))
        self.cmbStyle = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The style of resistor."))
        self.cmbConstruction = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the resistor."))

        self.txtResistance = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The resistance (in \u03A9) of the resistor."))
        self.txtNElements = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of active resistors in a resistor network "
                      u"or the number of potentiometer taps."))

        self._make_assessment_input_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed', self._on_combo_changed,
                                          1))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbStyle.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtResistance.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self._on_focus_out, 6))

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the specification RKTComboBox().

        This method is used to load the specification RTKComboBox() whenever
        the resistor subcategory is changed.

        :param int subcategory_id: the newly selected resistor subcategory ID.
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
            _data = ["S", "R", "P", "M", ["MIL-SPEC"], [_(u"Lower")]]
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

        # Load the type RTKComboBox().
        _model = self.cmbType.get_model()
        _model.clear()

        if _attributes['hazard_rate_method_id'] == 1:
            try:
                _data = self._dic_types[self._subcategory_id]
            except KeyError:
                _data = []
        else:
            _data = [[_(u"Bead")], [_(u"Disk")], [_(u"Rod")]]
        self.cmbType.do_load_combo(_data)

        # Load the style RTKComboBox().
        _model = self.cmbStyle.get_model()
        _model.clear()

        try:
            _data = self._dic_styles[_attributes['subcategory_id']][_attributes['specification_id']]
        except (KeyError, IndexError):
            _data = []
        self.cmbStyle.do_load_combo(_data)

        # Load the construction RTKComboBox().
        _model = self.cmbConstruction.get_model()
        _model.clear()

        try:
            _data = self._dic_construction[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data)

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected resistor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.set_sensitive(True)
        self.cmbSpecification.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.cmbStyle.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtResistance.set_sensitive(False)
        self.txtNElements.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id in [1, 2, 5, 6, 7, 9, 11, 13, 15]:
                self.cmbType.set_sensitive(True)
        elif _attributes['hazard_rate_method_id'] == 2:
            self.txtResistance.set_sensitive(True)
            if self._subcategory_id in [2, 6, 7, 15]:
                self.cmbSpecification.set_sensitive(True)
            if self._subcategory_id in [6, 7]:
                self.cmbStyle.set_sensitive(True)
            if self._subcategory_id == 8:
                self.cmbType.set_sensitive(True)
            if self._subcategory_id in [10, 12]:
                self.cmbConstruction.set_sensitive(True)
            else:
                self.cmbConstruction.set_sensitive(False)
            if self._subcategory_id in [4, 9, 10, 11, 12, 13, 14, 15]:
                self.txtNElements.set_sensitive(True)
            else:
                self.txtNElements.set_sensitive(False)

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

        # Build the container for resistors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtResistance, _x_pos, _y_pos[0])
        self.put(self.cmbQuality, _x_pos, _y_pos[1])
        self.put(self.cmbSpecification, _x_pos, _y_pos[2])
        self.put(self.cmbType, _x_pos, _y_pos[3])
        self.put(self.cmbStyle, _x_pos, _y_pos[4])
        self.put(self.cmbConstruction, _x_pos, _y_pos[5])
        self.put(self.txtNElements, _x_pos, _y_pos[6])

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Resistor attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    4    | cmbStyle         |
            +---------+------------------+---------+------------------+
            |    1    | cmbSpecification |    5    | cmbConstruction  |
            +---------+------------------+---------+------------------+
            |    2    | cmbType          |         |                  |
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
                _attributes['type_id'] = int(combo.get_active())
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

            +---------+---------------------+---------+---------------------+
            |  Index  | Widget              |  Index  | Widget              |
            +=========+=====================+=========+=====================+
            |    5    | txtResistance       |    6    | txtNElements        |
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

            if index == 5:
                _attributes['resistance'] = _text
            elif index == 6:
                _attributes['n_elements'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the resistor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              resistor.
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

        self.cmbType.handler_block(self._lst_handler_id[2])
        self.cmbType.set_active(_attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[2])

        self._do_set_sensitive()

        if _attributes['hazard_rate_method_id'] == 2:
            self.cmbSpecification.handler_block(self._lst_handler_id[1])
            self.cmbSpecification.set_active(_attributes['specification_id'])
            self.cmbSpecification.handler_unblock(self._lst_handler_id[1])

            self.cmbStyle.handler_block(self._lst_handler_id[3])
            self.cmbStyle.set_active(_attributes['family_id'])
            self.cmbStyle.handler_unblock(self._lst_handler_id[3])

            self.cmbConstruction.handler_block(self._lst_handler_id[4])
            self.cmbConstruction.set_active(_attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[4])

            self.txtResistance.handler_block(self._lst_handler_id[5])
            self.txtResistance.set_text(
                str(self.fmt.format(_attributes['resistance'])))
            self.txtResistance.handler_unblock(self._lst_handler_id[5])

            self.txtNElements.handler_block(self._lst_handler_id[6])
            self.txtNElements.set_text(
                str(self.fmt.format(_attributes['n_elements'])))
            self.txtNElements.handler_unblock(self._lst_handler_id[6])

        return _return


class StressInputs(gtk.Fixed):
    """
    Display Resistor stress input attribute data in the RTK Work Book.

    The Resistor stress input view displays all the assessment inputs for
    the selected resistor.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a resistor stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the resistor
                               currently being displayed.

    :ivar txtTemperatureRatedMin: enter and display the minimum rated
                                  temperature of the resistor.
    :ivar txtTemperatureKnee: enter and display the temperature above which
                              the resistor must be derated.
    :ivar txtTemperatureRatedMax: enter and display the maximum rated
                                  temperature of the resistor.
    :ivar txtPowerRated: enter and display the rated power of the resistor.
    :ivar txtPowerOperating; enter and display the operating power of the
                             resistor.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           resistor.
    :ivar txtVoltageOperating: enter and display the operating voltage of the
                               resistor.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTemperatureRatedMin - `changed`        |
    +----------+-------------------------------------------+
    |     1    | txtTemperatureKnee - `changed`            |
    +----------+-------------------------------------------+
    |     2    | txtTemperatureRatedMax - `changed`        |
    +----------+-------------------------------------------+
    |     3    | txtPowerRated - `changed`                 |
    +----------+-------------------------------------------+
    |     4    | txtPowerOperating - `changed`             |
    +----------+-------------------------------------------+
    |     5    | txtVoltageRated - `changed`               |
    +----------+-------------------------------------------+
    |     6    | txtVoltageOperating - `changed`           |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Minimum Rated Temperature (\u00B0C):"),
        _(u"Knee Temperature (\u00B0C):"),
        _(u"Maximum Rated Temperature (\u00B0C):"),
        _(u"Rated Power (W):"),
        _(u"Operating Power (W):"),
        _(u"Rated Voltage (V):"),
        _(u"Operating Voltage (V):")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Resistor stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                resistor.
        :param int subcategory_id: the ID of the resistor subcategory.
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
                u"The minimum rated temperature (in \u00B0C) of the resistor.")
        )
        self.txtTemperatureKnee = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The break temperature (in \u00B0C) of the resistor beyond "
                u"which it must be derated."))
        self.txtTemperatureRatedMax = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The maximum rated temperature (in \u00B0C) of the resistor.")
        )
        self.txtPowerRated = rtk.RTKEntry(
            width=125, tooltip=_(u"The rated power (in W) of the resistor."))
        self.txtPowerOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating power (in W) of the resistor."))
        self.txtVoltageRated = rtk.RTKEntry(
            width=125, tooltip=_(u"The rated voltage (in V) of the resistor."))
        self.txtVoltageOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating voltage (in V) of the resistor."))

        self._lst_handler_id.append(
            self.txtTemperatureRatedMin.connect('changed', self._on_focus_out,
                                                0))
        self._lst_handler_id.append(
            self.txtTemperatureKnee.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect('changed', self._on_focus_out,
                                                2))
        self._lst_handler_id.append(
            self.txtPowerRated.connect('changed', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.txtPowerOperating.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtVoltageOperating.connect('changed', self._on_focus_out, 6))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the resistor module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for resistors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[2])
        self.put(self.txtPowerRated, _x_pos, _y_pos[3])
        self.put(self.txtPowerOperating, _x_pos, _y_pos[4])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[5])
        self.put(self.txtVoltageOperating, _x_pos, _y_pos[6])

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
            |   0   | txtTemperatureRatedMin |   4   | txtPowerOperating   |
            +-------+------------------------+-------+---------------------+
            |   1   | txtTemperatureKnee     |   5   | txtVoltageRated     |
            +-------+------------------------+-------+---------------------+
            |   2   | txtTemperatureRatedMax |   6   | txtVoltageOperating |
            +-------+------------------------+-------+---------------------+
            |   3   | txtPowerRated          |       |                     |
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
                _attributes['power_rated'] = _text
            elif index == 4:
                _attributes['power_operating'] = _text
            elif index == 5:
                _attributes['voltage_rated'] = _text
            elif index == 6:
                _attributes['voltage_dc_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the resistor stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              resistor.
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

        self.txtPowerRated.handler_block(self._lst_handler_id[3])
        self.txtPowerRated.set_text(
            str(self.fmt.format(_attributes['power_rated'])))
        self.txtPowerRated.handler_unblock(self._lst_handler_id[3])

        self.txtPowerOperating.handler_block(self._lst_handler_id[4])
        self.txtPowerOperating.set_text(
            str(self.fmt.format(_attributes['power_operating'])))
        self.txtPowerOperating.handler_unblock(self._lst_handler_id[4])

        self.txtVoltageRated.handler_block(self._lst_handler_id[5])
        self.txtVoltageRated.set_text(
            str(self.fmt.format(_attributes['voltage_rated'])))
        self.txtVoltageRated.handler_unblock(self._lst_handler_id[5])

        self.txtVoltageOperating.handler_block(self._lst_handler_id[6])
        self.txtVoltageOperating.set_text(
            str(self.fmt.format(_attributes['voltage_dc_operating'])))
        self.txtVoltageOperating.handler_unblock(self._lst_handler_id[6])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display resistor assessment results attribute data in the RTK Work Book.

    The resistor assessment result view displays all the assessment results
    for the selected resistor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a resistor assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the resistor
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the resistor.
    :ivar txtPiR: displays the resistance factor for the resistor.
    :ivar txtPiT: displays the temperature factor for the resistor.
    :ivar txtPiNR: displays the number of resistors factor for the resistor.
    :ivar txtPiTAPS: displays the potentiometer taps factor for the resistor.
    :ivar txtPiV: displays the voltage factor for the resistor.
    :ivar txtPiC: displays the construction class factor for the resistor.
    :ivar txtPiQ: displays the quality factor for the resistor.
    :ivar txtPiE: displays the environment factor for the resistor.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        6:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        10:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        12:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        13:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        14:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        15:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private list attributes.
    _lst_labels = [
        u"\u03BB<sub>b</sub>:", u"\u03C0<sub>R</sub>:", u"\u03C0<sub>T</sub>:",
        u"\u03C0<sub>NR</sub>:", u"\u03C0<sub>TAPS</sub>",
        u"\u03C0<sub>V</sub>", u"\u03C0<sub>C</sub>", u"\u03C0<sub>Q</sub>:",
        u"\u03C0<sub>E</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Resistor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                resistor.
        :param int subcategory_id: the ID of the resistor subcategory.
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
            tooltip=_(u"The assessment model used to calculate the resistor "
                      u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the resistor."))
        self.txtPiR = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The resistance factor for the resistor."))
        self.txtPiT = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The temperature factor for the resistor."))
        self.txtPiNR = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The number of resistors factor for the resistor."))
        self.txtPiTAPS = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The potentiometer taps factor for the resistor."))
        self.txtPiV = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The voltage factor for the resistor."))
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The construction class factor for the resistor."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the resistor."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the resistor."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the resistor assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self.txtPiR.set_text(str(self.fmt.format(_attributes['piR'])))
        self.txtPiT.set_text(str(self.fmt.format(_attributes['piT'])))
        self.txtPiNR.set_text(str(self.fmt.format(_attributes['piNR'])))
        self.txtPiTAPS.set_text(str(self.fmt.format(_attributes['piTAPS'])))
        self.txtPiV.set_text(str(self.fmt.format(_attributes['piV'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected resistor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiQ.set_sensitive(True)
        self.txtPiR.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtPiNR.set_sensitive(False)
        self.txtPiTAPS.set_sensitive(False)
        self.txtPiV.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiE.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            self.txtPiE.set_sensitive(True)
            if _attributes['subcategory_id'] != 8:
                self.txtPiR.set_sensitive(True)
            if _attributes['subcategory_id'] == 4:
                self.txtPiT.set_sensitive(True)
                self.txtPiNR.set_sensitive(True)
            if _attributes['subcategory_id'] in [9, 10, 11, 12, 13, 14, 15]:
                self.txtPiTAPS.set_sensitive(True)
                self.txtPiV.set_sensitive(True)
            if _attributes['subcategory_id'] in [10, 12]:
                self.txtPiC.set_sensitive(True)

        return _return

    def _make_assessment_results_page(self):
        """
        Make the resistor gtk.Notebook() assessment results page.

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

        # Build the container for resistors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiR, _x_pos, _y_pos[1])
        self.put(self.txtPiT, _x_pos, _y_pos[2])
        self.put(self.txtPiNR, _x_pos, _y_pos[3])
        self.put(self.txtPiTAPS, _x_pos, _y_pos[4])
        self.put(self.txtPiV, _x_pos, _y_pos[5])
        self.put(self.txtPiC, _x_pos, _y_pos[6])
        self.put(self.txtPiQ, _x_pos, _y_pos[7])
        self.put(self.txtPiE, _x_pos, _y_pos[8])

        self.show_all()

        return None

    def on_select(self, module_id=None):
        """
        Load the resistor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              resistor.
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
    Display resistor stress results attribute data in the RTK Work Book.

    The resistor stress result view displays all the stress results for the
    selected resistor.  This includes, currently, results for MIL-HDBK-217FN2
    parts count and MIL-HDBK-217FN2 part stress methods.  The attributes of a
    resistor stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the resistor
                               currently being displayed.

    :ivar chkOverstress: indicates whether or not the resistor is overstresed.
    :ivar txtPowerRatio: display the power ratio of the resistor.
    :ivar txtReason: display the reason(s) a resistor is overstressed.
    """

    # Define private list attributes.
    _lst_labels = [_(u"Voltage Ratio:"), "", _(u"Overstress Reason:")]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Resistor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                resistor.
        :param int subcategory_id: the ID of the resistor subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

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
            tooltip=_(u"Indicates whether or not the selected resistor "
                      u"is overstressed."))
        self.txtReason = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=250,
            tooltip=_(u"The reason(s) the selected hardware item is "
                      u"overstressed."))
        self.txtPowerRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating power to rated power for "
                      u"the resistor."))

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
            y_values=[_attributes['power_ratio']],
            plot_type='scatter',
            marker='go')

        self.pltDerate.do_make_title(
            _(u"Voltage Derating Curve for {0:s} at {1:s}").format(
                _attributes['part_number'], _attributes['ref_des']),
            fontsize=12)
        self.pltDerate.do_make_legend([
            _(u"Harsh Environment"),
            _(u"Mild Environment"),
            _(u"Power Operating Point")
        ])

        self.pltDerate.do_make_labels(
            _(u"Temperature (\u2070C)"), 0, -0.2, fontsize=10)
        self.pltDerate.do_make_labels(
            _(u"Power Ratio"), -1, 0, set_x=False, fontsize=10)

        self.pltDerate.figure.canvas.draw()

        return _return

    def _do_load_page(self):
        """
        Load the resistor assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPowerRatio.set_text(
            str(self.fmt.format(_attributes['power_ratio'])))
        self.chkOverstress.set_active(_attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(_attributes['reason'])

        self._do_load_derating_curve()

        return _return

    def _make_stress_results_page(self):
        """
        Make the resistor gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Create the left side.
        _fixed = gtk.Fixed()
        self.pack1(_fixed, True, True)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, _fixed, 5, 35)
        _x_pos += 50

        _fixed.put(self.txtPowerRatio, _x_pos, _y_pos[0])
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
        Load the resistor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              resistor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_load_page()

        return _return
