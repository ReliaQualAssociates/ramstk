# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Capacitor.py is part of the RTK Project
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

    :cvar dict _dic_specifications: dictionary of capacitor MIL-SPECs.  Key is
                                    capacitor subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of capacitor styles defined in the
                            MIL-SPECs.  Key is capacitor subcategory ID; values
                            are lists of styles.

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the capacitor
                               currently being displayed.

    :ivar cmbSpecification: select and display the governing specification of
                            the capacitor.
    :ivar cmbStyle: select and display the style of the capacitor.
    :ivar cmbConfiguration: select and display the configuration of the
                            capacitor.
    :ivar cmbConstruction: select and display the method of construction of the
                           capacitor.
    :ivar txtCapacitance: enter and display the capacitance rating of the
                          capacitor.
    :ivar txtESR: enter and display the equivalent series resistance.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | cmbSpecification - `changed`              |
    +----------+-------------------------------------------+
    |     1    | cmbStyle - `changed`                      |
    +----------+-------------------------------------------+
    |     2    | cmbConfiguration - `changed`              |
    +----------+-------------------------------------------+
    |     3    | cmbConstruction - `changed`               |
    +----------+-------------------------------------------+
    |     4    | txtCapacitance - `changed`                |
    +----------+-------------------------------------------+
    |     5    | txtESR - `changed`                        |
    +----------+-------------------------------------------+
    """

    # Define private dict attributes.
    _dic_specifications = {
        1: [["MIL-C-25"], ["MIL-C-12889"]],
        2: [["MIL-C-11693"]],
        3: [["MIL-C-14157"], ["MIL-C-19978"]],
        4: [["MIL-C-18312"], ["MIL-C-39022"]],
        5: [["MIL-C-55514"]],
        6: [["MIL-C-83421"]],
        7: [["MIL-C-5"], ["MIL-C-39001"]],
        8: [["MIL-C-10950"]],
        9: [["MIL-C-11272"], ["MIL-C-23269"]],
        10: [["MIL-C-11015"], ["MIL-C-39014"]],
        11: [["MIL-C-20"], ["MIL-C-55681"]],
        12: [["MIL-C-39003"]],
        13: [["MIL-C-3965"], ["MIL-C-39006"]],
        14: [["MIL-C-39018"]],
        15: [["MIL-C-62"]],
        16: [["MIL-C-81"]],
        17: [["MIL-C-14409"]],
        18: [["MIL-C-92"]],
        19: [["MIL-C-23183"]]
    }

    _dic_styles = {
        1:
        [[["CP4"], ["CP5"], ["CP8"], ["CP9"], ["CP10"], ["CP11"], ["CP12"],
          ["CP13"], ["CP25"], ["CP26"], ["CP27"], ["CP28"], ["CP29"], ["CP40"],
          ["CP41"], ["CP67"], ["CP69"], ["CP70"], ["CP72"], ["CP75"], ["CP76"],
          ["CP77"], ["CP78"], ["CP80"], ["CP81"], ["CP82"]], [["CA"]]],
        2: [[_(u"Characteristic E")], [_(u"Characteristic K")],
            [_(u"Characteristic P")], [_(u"Characteristic W")]],
        3: [[["CPV07"], ["CPV09"], ["CPV17"]],
            [[_(u"Characteristic E")], [_(u"Characteristic F")], [
                _(u"Characteristic G")
            ], [_(u"Characteristic K")], [_(u"Characteristic L")], [
                _(u"Characteristic M")
            ], [_(u"Characteristic P")], [_(u"Characteristic Q")],
             [_(u"Characteristic S")], [_(u"Characteristic T")]]],
        4: [[[_(u"Characteristic N")], [_(u"Characteristic R")]],
            [[_(u"Characteristic 1")], [_(u"Characteristic 9")],
             [_(u"Characteristic 10")], [_(u"Characteristic 12")],
             [_(u"Characteristic 19")], [_(u"Characteristic 29")],
             [_(u"Characteristic 49")], [_(u"Characteristic 59")]]],
        5: [[_(u"Characteristic M")], [_(u"Characteristic N")],
            [_(u"Characteristic Q")], [_(u"Characteristic R")],
            [_(u"Characteristic S")]],
        6: [["CRH"]],
        7: [[[_(u"Temperature Range M")], [_(u"Temperature Range N")],
             [_(u"Temperature Range O")], [_(u"Temperature Range P")]],
            [[_(u"Temperature Range O")], [_(u"Temperature Range P")]]],
        8: [["CB50"], [_(u"Other")]],
        9: [[[_(u"Temperature Range C")], [_(u"Temperature Range D")]],
            [[_(u"All")]]],
        10: [[[_(u"Type A Rated Temperature")],
              [_(u"Type B Rated Temperature")],
              [_(u"Type C Rated Temperature")]],
             [["CKR05"], ["CKR06"], ["CKR07"], ["CKR08"], ["CKR09"], ["CKR10"],
              ["CKR11"], ["CKR12"], ["CKR13"], ["CKR14"], ["CKR15"], ["CKR16"],
              ["CKR17"], ["CKR18"], ["CKR19"], ["CKR48"], ["CKR64"], ["CKR72"],
              ["CKR73"], ["CKR74"]]],
        11:
        [[["CC5"], ["CC6"], ["CC7"], ["CC8"], ["CC9"], ["CC13"], ["CC14"], [
            "CC15"
        ], ["CC16"], ["CC17"], ["CC18"], ["CC19"], ["CC20"], ["CC21"], [
            "CC22"
        ], ["CC25"], ["CC26"], ["CC27"], ["CC30"], ["CC31"], ["CC32"], [
            "CC33"
        ], ["CC35"], ["CC36"], ["CC37"], ["CC45"], ["CC47"], ["CC50"], [
            "CC51"
        ], ["CC52"], ["CC53"], ["CC54"], ["CC55"], ["CC56"], ["CC57"], [
            "CC75"
        ], ["CC76"], ["CC77"], ["CC78"], ["CC79"], ["CC81"], ["CC82"], [
            "CC83"
        ], ["CC85"], ["CC95"], ["CC96"], ["CC97"], ["CCR05"], ["CCR06"], [
            "CCR07"
        ], ["CCR08"], ["CCR09"], ["CCR13"], ["CCR14"], ["CCR15"], ["CCR16"],
          ["CCR17"], ["CCR18"], ["CCR19"], ["CCR54"], ["CCR55"], ["CCR56"],
          ["CCR57"], ["CCR75"], ["CCR76"], ["CCR77"], ["CCR78"], ["CCR79"],
          ["CCR81"], ["CCR82"], ["CCR83"], ["CCR90"]], [["CDR"]]],
        12: [["CSR"]],
        13: [[["CL10"], ["CL13"], ["CL14"], ["CL16"], ["CL17"], ["CL18"], [
            "CL24"
        ], ["CL25"], ["CL26"], ["CL27"], ["CL30"], ["CL31"], ["CL32"], [
            "CL33"
        ], ["CL34"], ["CL35"], ["CL36"], ["CL37"], ["CL40"], ["CL41"], [
            "CL42"
        ], ["CL43"], ["CL46"], ["CL47"], ["CL48"], ["CL49"], ["CL50"],
              ["CL51"], ["CL52"], ["CL53"], ["CL54"], ["CL55"], ["CL56"],
              ["CL64"], ["CL65"], ["CL66"], ["CL67"], ["CL70"], ["CL71"],
              ["CL72"], ["CL73"]], [["CLR"]]],
        14: [[_(u"Style 16")], [_(u"Style 17")], [_(u"Style 71")],
             [_(u"All Others")]],
        15: [["CE"]],
        16: [["CV11"], ["CV14"], ["CV21"], ["CV31"], ["CV32"], ["CV34"],
             ["CV35"], ["CV36"], ["CV40"], ["CV41"]],
        17: [[_(u"Style G")], [_(u"Style H")], [_(u"Style J")],
             [_(u"Style L")], [_(u"Style Q")], [_(u"Style T")]],
        18: [["CT"]],
        19: [["CG20"], ["CG21"], ["CG30"], ["CG31"], ["CG32"], ["CG40"],
             ["CG41"], ["CG42"], ["CG43"], ["CG44"], ["CG50"], ["CG51"],
             ["CG60"], ["CG61"], ["CG62"], ["CG63"], ["CG64"], ["CG65"],
             ["CG66"], ["CG67"]]
    }

    # Define private list attributes.
    _lst_labels = [
        _(u"Capacitance (F):"),
        _(u"Specification:"),
        _(u"Style:"),
        _(u"Configuration:"),
        _(u"Construction:"),
        _(u"Equivalent Series Resistance (\u03A9):")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Capacitor assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int subcategory_id: the ID of the capacitor subcategory.
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

        self.cmbSpecification = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The governing specification for the capacitor."))
        self.cmbStyle = rtk.RTKComboBox(
            index=0, simple=False, tooltip=_(u"The style of the capacitor."))
        self.cmbConfiguration = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The configuration of the capacitor."))
        self.cmbConstruction = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the capacitor."))

        self.txtCapacitance = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The capacitance rating (in farads) of the capacitor."))
        self.txtESR = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The equivalent series resistance of the capcaitor."))

        self._make_assessment_input_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed', self._on_combo_changed,
                                          0))
        self._lst_handler_id.append(
            self.cmbStyle.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbConfiguration.connect('changed', self._on_combo_changed,
                                          2))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.txtCapacitance.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtESR.connect('changed', self._on_focus_out, 5))

        pub.subscribe(self._do_load_specification, 'changedSubcategory')

    def _do_load_specification(self, subcategory_id):
        """
        Load the specification RKTComboBox().

        This method is used to load the specification RTKComboBox() whenever
        the capacitor subcategory is changed.

        :param int subcategory_id: the newly selected capacitor subcategory ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._subcategory_id = subcategory_id

        # Load the gtk.ComboBox() widgets.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        return _return

    def _make_assessment_input_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        _model = self.cmbStyle.get_model()
        _model.clear()

        _model = self.cmbConstruction.get_model()
        _model.clear()

        _data = [[_(u"Slug, All Tantalum")], [_(u"Foil, Hermetic")],
                 [_(u"Slug, Hermetic")], [_(u"Foil, Non-Hermetic")],
                 [_(u"Slug, Non-Hermetic")]]
        self.cmbConstruction.do_load_combo(_data)

        _model = self.cmbConfiguration.get_model()
        _model.clear()

        _data = [[_(u"Fixed")], [_(u"Variable")]]
        self.cmbConfiguration.do_load_combo(_data)

        if self._subcategory_id == 12:
            self.txtESR.set_sensitive(True)
        else:
            self.txtESR.set_sensitive(False)

        if self._subcategory_id == 13:
            self.cmbConstruction.set_sensitive(True)
        else:
            self.cmbConstruction.set_sensitive(False)

        if self._subcategory_id == 19:
            self.cmbConfiguration.set_sensitive(True)
        else:
            self.cmbConfiguration.set_sensitive(False)

        # Build the container for capacitors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtCapacitance, _x_pos, _y_pos[0])
        self.put(self.cmbSpecification, _x_pos, _y_pos[1])
        self.put(self.cmbStyle, _x_pos, _y_pos[2])
        self.put(self.cmbConfiguration, _x_pos, _y_pos[3])
        self.put(self.cmbConstruction, _x_pos, _y_pos[4])
        self.put(self.txtESR, _x_pos, _y_pos[5])

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Capacitor attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbSpecification |    2    | cmbConfiguration |
            +---------+------------------+---------+------------------+
            |    1    | cmbStyle         |    3    | cmbConstruction  |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if self._dtc_data_controller is not None:
            _hardware = self._dtc_data_controller.request_select(
                self._hardware_id, 'electrical_design')

            if index == 0:
                _hardware.specification_id = int(combo.get_active())

                _model = self.cmbStyle.get_model()
                _model.clear()

                # Load the capacitor style RTKComboBox().
                _index = _hardware.specification_id - 1
                if self._subcategory_id in [1, 3, 4, 7, 9, 10, 11, 13]:
                    try:
                        _data = self._dic_styles[self._subcategory_id][_index]
                    except KeyError:
                        _data = []
                else:
                    try:
                        _data = self._dic_styles[self._subcategory_id]
                    except KeyError:
                        _data = []

                self.cmbStyle.do_load_combo(_data)

            elif index == 1:
                _hardware.type_id = int(combo.get_active())
            elif index == 2:
                _hardware.configuration_id = int(combo.get_active())
            elif index == 3:
                _hardware.construction_id = int(combo.get_active())

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
            |    4    | txtCapacitance      |    5    | txtESR              |
            +---------+---------------------+---------+---------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _hardware = self._dtc_data_controller.request_select(
                self._hardware_id, 'electrical_design')

            try:
                _text = float(entry.get_text())
            except ValueError:
                _text = 0.0

            if index == 4:
                _hardware.capacitance = _text
            elif index == 5:
                _hardware.resistance = _text

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id):
        """
        Load the capacitor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              capacitor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _hardware = self._dtc_data_controller.request_select(
            self._hardware_id, 'electrical_design')

        # We don't block the callback signal otherwise the style RTKComboBox()
        # will not be loaded and set.
        self.cmbSpecification.set_active(_hardware.specification_id)

        self.cmbStyle.handler_block(self._lst_handler_id[1])
        self.cmbStyle.set_active(_hardware.type_id)
        self.cmbStyle.handler_unblock(self._lst_handler_id[1])

        self.cmbConfiguration.handler_block(self._lst_handler_id[2])
        self.cmbConfiguration.set_active(_hardware.configuration_id)
        self.cmbConfiguration.handler_unblock(self._lst_handler_id[2])

        self.cmbConstruction.handler_block(self._lst_handler_id[3])
        self.cmbConstruction.set_active(_hardware.construction_id)
        self.cmbConstruction.handler_unblock(self._lst_handler_id[3])

        self.txtCapacitance.handler_block(self._lst_handler_id[4])
        self.txtCapacitance.set_text(
            str(self.fmt.format(_hardware.capacitance)))
        self.txtCapacitance.handler_unblock(self._lst_handler_id[4])

        self.txtESR.handler_block(self._lst_handler_id[5])
        self.txtESR.set_text(str(self.fmt.format(_hardware.resistance)))
        self.txtESR.handler_unblock(self._lst_handler_id[5])

        return _return


class StressInputs(gtk.Fixed):
    """
    Display Capacitor stress input attribute data in the RTK Work Book.

    The Capacitor stress input view displays all the assessment inputs for
    the selected capacitor.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a capacitor stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the capacitor
                               currently being displayed.

    :ivar txtTemperatureRated: enter and display the maximum rated temperature
                               of the capacitor.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           capacitor.
    :ivar txtVoltageAC: enter and display the operating ac voltage of the
                        capacitor.
    :ivar txtVoltageDC: enter and display the operating DC voltage of the
                        capacitor.

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
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Maximum Rated Temperature (\u00B0C):"),
        _(u"Rated Voltage (V):"),
        _(u"Operating ac Voltage (V):"),
        _(u"Operating DC Voltage (V):")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Capacitor stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int subcategory_id: the ID of the capacitor subcategory.
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

        self.txtTemperatureRated = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The maximum rated temperature (in \u00B0C) of the capacitor."
            ))
        self.txtVoltageRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated voltage (in V) of the capacitor."))
        self.txtVoltageAC = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating ac voltage (in V) of the capacitor."))
        self.txtVoltageDC = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating DC voltage (in V) of the capacitor."))

        self._lst_handler_id.append(
            self.txtTemperatureRated.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtVoltageAC.connect('changed', self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.txtVoltageDC.connect('changed', self._on_focus_out, 3))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the capacitor module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRated, _x_pos, _y_pos[0])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[1])
        self.put(self.txtVoltageAC, _x_pos, _y_pos[2])
        self.put(self.txtVoltageDC, _x_pos, _y_pos[3])

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

            +---------+---------------------+---------+---------------------+
            |  Index  | Widget              |  Index  | Widget              |
            +=========+=====================+=========+=====================+
            |    0    | txtTemperatureRated |    2    | txtVoltageAC        |
            +---------+---------------------+---------+---------------------+
            |    1    | txtVoltageRated     |    3    | txtVoltageDC        |
            +---------+---------------------+---------+---------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _hardware = self._dtc_data_controller.request_select(
                self._hardware_id, 'electrical_design')

            try:
                _text = float(entry.get_text())
            except ValueError:
                _text = 0.0

            if index == 0:
                _hardware.temperature_rated_max = _text
            elif index == 1:
                _hardware.voltage_rated = _text
            elif index == 2:
                _hardware.voltage_ac_operating = _text
            elif index == 3:
                _hardware.voltage_dc_operating = _text

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id):
        """
        Load the capacitor stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              capacitor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _hardware = self._dtc_data_controller.request_select(
            self._hardware_id, 'electrical_design')

        # We don't block the callback signal otherwise the style RTKComboBox()
        # will not be loaded and set.
        self.txtTemperatureRated.handler_block(self._lst_handler_id[0])
        self.txtTemperatureRated.set_text(
            str(self.fmt.format(_hardware.temperature_rated_max)))
        self.txtTemperatureRated.handler_unblock(self._lst_handler_id[0])

        self.txtVoltageRated.handler_block(self._lst_handler_id[1])
        self.txtVoltageRated.set_text(
            str(self.fmt.format(_hardware.voltage_rated)))
        self.txtVoltageRated.handler_unblock(self._lst_handler_id[1])

        self.txtVoltageAC.handler_block(self._lst_handler_id[2])
        self.txtVoltageAC.set_text(
            str(self.fmt.format(_hardware.voltage_ac_operating)))
        self.txtVoltageAC.handler_unblock(self._lst_handler_id[2])

        self.txtVoltageDC.handler_block(self._lst_handler_id[3])
        self.txtVoltageDC.set_text(
            str(self.fmt.format(_hardware.voltage_dc_operating)))
        self.txtVoltageDC.handler_unblock(self._lst_handler_id[3])

        return _return
