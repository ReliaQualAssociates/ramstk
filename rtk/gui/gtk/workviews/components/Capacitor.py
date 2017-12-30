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
    _dic_quality = {
        1: [["MIL-SPEC"], [_(u"Lower")]],
        2: [["M"], [_(u"Non-Established Reliability")], [_(u"Lower")]],
        3: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-19978 Non-Established Reliability")], [_(u"Lower")]
        ],
        4: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-18312 Non-Established Reliability")], [_(u"Lower")]
        ],
        5: ["S", "R", "P", "M", [_(u"Lower")]],
        6: ["S", "R", "P", "M", [_(u"Lower")]],
        7: [
            "T", "S", "R", "P", "M", "L",
            [_(u"MIL-C-5 Non-Established Reliability, Dipped")],
            [_(u"MIL-C-5 Non-Established Reliability, Molded")], [_(u"Lower")]
        ],
        8: [["MIL-C-10950"], [_(u"Lower")]],
        9: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-11272 Non-Established Reliability")], [_(u"Lower")]
        ],
        10: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-11015 Non-Established Reliability")], [_(u"Lower")]
        ],
        11: [
            "S", "R", "P", "M", [_(u"Non-Established Reliability")],
            [_(u"Lower")]
        ],
        12: ["D", "C", "S", "B", "R", "P", "M", "L", [_(u"Lower")]],
        13: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-3965 Non-Established Reliability")], [_(u"Lower")]
        ],
        14: [
            "S", "R", "P", "M", [_(u"Non-Established Reliability")],
            [_(u"Lower")]
        ],
        15: [["MIL-SPEC"], [_(u"Lower")]],
        16: [["MIL-SPEC"], [_(u"Lower")]],
        17: [["MIL-SPEC"], [_(u"Lower")]],
        18: [["MIL-SPEC"], [_(u"Lower")]],
        19: [["MIL-SPEC"], [_(u"Lower")]]
    }

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
        _(u"Quality Level:"),
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
        :param int hardware_id: the hardware ID of the currently selected
                                capacitor.
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

        self.cmbQuality = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The quality level of the capacitor."))
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
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed', self._on_combo_changed,
                                          1))
        self._lst_handler_id.append(
            self.cmbStyle.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbConfiguration.connect('changed', self._on_combo_changed,
                                          3))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtCapacitance.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtESR.connect('changed', self._on_focus_out, 6))

        pub.subscribe(self._do_load_comboboxes, 'changedSubcategory')

    def _do_load_comboboxes(self, subcategory_id):
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

        # Load the specification RTKComboBox().
        _model = self.cmbSpecification.get_model()
        _model.clear()

        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        # Load the quality level RTKComboBox().
        _model = self.cmbQuality.get_model()
        _model.clear()

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)
        if _attributes['hazard_rate_method_id'] == 1:
            _data = ["S", "R", "P", "M", "L", ["MIL-SPEC"], [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected capacitor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id == 1:
                self.cmbSpecification.set_sensitive(True)
            else:
                self.cmbSpecification.set_sensitive(False)
            self.cmbStyle.set_sensitive(False)
            self.cmbConfiguration.set_sensitive(False)
            self.cmbConstruction.set_sensitive(False)
            self.txtCapacitance.set_sensitive(False)
            self.txtESR.set_sensitive(False)
        else:
            self.cmbSpecification.set_sensitive(True)
            self.cmbStyle.set_sensitive(True)
            self.txtCapacitance.set_sensitive(True)

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

        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtCapacitance, _x_pos, _y_pos[0])
        self.put(self.cmbQuality, _x_pos, _y_pos[1])
        self.put(self.cmbSpecification, _x_pos, _y_pos[2])
        self.put(self.cmbStyle, _x_pos, _y_pos[3])
        self.put(self.cmbConfiguration, _x_pos, _y_pos[4])
        self.put(self.cmbConstruction, _x_pos, _y_pos[5])
        self.put(self.txtESR, _x_pos, _y_pos[6])

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
            |    0    | cmbQuality       |    3    | cmbConfiguration |
            +---------+------------------+---------+------------------+
            |    1    | cmbSpecification |    4    | cmbConstruction  |
            +---------+------------------+---------+------------------+
            |    2    | cmbStyle         |         |                  |
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

                _model = self.cmbStyle.get_model()
                _model.clear()

                # Load the capacitor style RTKComboBox().
                _index = _attributes['specification_id'] - 1
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

            elif index == 2:
                _attributes['type_id'] = int(combo.get_active())
            elif index == 3:
                _attributes['configuration_id'] = int(combo.get_active())
            elif index == 4:
                _attributes['consruction_id'] = int(combo.get_active())

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
            |    5    | txtCapacitance      |    6    | txtESR              |
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
                _attributes['capacitance'] = _text
            elif index == 6:
                _attributes['resistance'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(_attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        # We don't block the callback signal otherwise the style
        # RTKComboBox()will not be loaded and set.
        self.cmbSpecification.set_active(_attributes['specification_id'])

        self._do_set_sensitive()

        if (_attributes['hazard_rate_method_id'] != 1
                and self._subcategory_id == 1):
            self.cmbStyle.handler_block(self._lst_handler_id[2])
            self.cmbStyle.set_active(_attributes['type_id'])
            self.cmbStyle.handler_unblock(self._lst_handler_id[2])

            self.cmbConfiguration.handler_block(self._lst_handler_id[3])
            self.cmbConfiguration.set_active(_attributes['configuration_id'])
            self.cmbConfiguration.handler_unblock(self._lst_handler_id[3])

            self.cmbConstruction.handler_block(self._lst_handler_id[4])
            self.cmbConstruction.set_active(_attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[4])

            self.txtCapacitance.handler_block(self._lst_handler_id[5])
            self.txtCapacitance.set_text(
                str(self.fmt.format(_attributes['capacitance'])))
            self.txtCapacitance.handler_unblock(self._lst_handler_id[5])

            self.txtESR.handler_block(self._lst_handler_id[6])
            self.txtESR.set_text(
                str(self.fmt.format(_attributes['resistance'])))
            self.txtESR.handler_unblock(self._lst_handler_id[6])

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
        _(u"Minimum Rated Temperature (\u00B0C):"),
        _(u"Knee Temperature (\u00B0C):"),
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
        :param int hardware_id: the hardware ID of the currently selected
                                capacitor.
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

        self.txtTemperatureKnee = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The break temperature (in \u00B0C) of the capacitor beyond "
                u"which it must be derated."))
        self.txtTemperatureRatedMin = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The minimum rated temperature (in \u00B0C) of the capacitor."
            ))
        self.txtTemperatureRatedMax = rtk.RTKEntry(
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

        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[2])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[3])
        self.put(self.txtVoltageAC, _x_pos, _y_pos[4])
        self.put(self.txtVoltageDC, _x_pos, _y_pos[5])

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
            |    0    | txtTemperatureRatedMin |    3    | VoltageRated      |
            +---------+------------------------+---------+-------------------+
            |    1    | txtTemperatureKnee     |    4    | txtVoltageAC      |
            +---------+------------------------+---------+-------------------+
            |    2    | txtTemperatureRatedMax |    5    | txtVoltageDC      |
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

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

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

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display capacitor assessment results attribute data in the RTK Work Book.

    The capacitor assessment result view displays all the assessment results
    for the selected capacitor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a capacitor assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the capacitor
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the capacitor.
    :ivar txtPiCV: displays the capacitance factor for the capacitor.
    :ivar txtPiCF: displays the configuration factor for the capacitor.
    :ivar txtPiC: displays the construction factor for the capacitor.
    :ivar txtPiQ: displays the quality factor for the capacitor.
    :ivar txtPiE: displays the environment factor for the capacitor.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        6:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        10:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        12:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        13:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        14:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        15:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        16:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        17:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        18:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        19:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
    }

    # Define private list attributes.
    _lst_labels = [
        u"\u03BB<sub>b</sub>:", u"\u03C0<sub>CV</sub>:",
        u"\u03C0<sub>CF</sub>:", u"\u03C0<sub>C</sub>:",
        u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Capacitor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                capacitor.
        :param int subcategory_id: the ID of the capacitor subcategory.
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
            tooltip=_(u"The assessment model used to calculate the capacitor "
                      u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the capacitor."))
        self.txtPiCV = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The capacitance factor for the capacitor."))
        self.txtPiCF = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The configuration factor for the capacitor."))
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The construction factor for the capacitor."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the capacitor."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the capacitor."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self.on_select, 'calculatedHardware')

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected capacitor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        if _attributes['hazard_rate_method_id'] == 1:
            self.txtPiCV.set_sensitive(False)
            self.txtPiCF.set_sensitive(False)
            self.txtPiC.set_sensitive(False)
            self.txtPiE.set_sensitive(False)
        else:
            self.txtPiCV.set_sensitive(True)
            self.txtPiCF.set_sensitive(True)
            self.txtPiC.set_sensitive(True)
            self.txtPiE.set_sensitive(True)

        return _return

    def _make_assessment_results_page(self):
        """
        Make the capacitor gtk.Notebook() assessment results page.

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
            self._lblModel.set_markup(
                self._dic_part_stress[self._subcategory_id])
            self._lst_labels[0] = u"\u03BB<sub>b</sub>:"

        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiCV, _x_pos, _y_pos[1])
        self.put(self.txtPiCF, _x_pos, _y_pos[2])
        self.put(self.txtPiC, _x_pos, _y_pos[3])
        self.put(self.txtPiQ, _x_pos, _y_pos[4])
        self.put(self.txtPiE, _x_pos, _y_pos[5])

        self.show_all()

        return None

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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self._do_set_sensitive()

        self.txtPiCV.set_text(str(self.fmt.format(_attributes['piCV'])))
        self.txtPiCF.set_text(str(self.fmt.format(_attributes['piCF'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))

        return _return


class StressResults(gtk.HPaned):
    """
    Display capacitor stress results attribute data in the RTK Work Book.

    The capacitor stress result view displays all the stress results for the
    selected capacitor.  This includes, currently, results for MIL-HDBK-217FN2
    parts count and MIL-HDBK-217FN2 part stress methods.  The attributes of a
    capacitor stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

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
    """

    # Define private list attributes.
    _lst_labels = [_(u"Voltage Ratio:"), "", _(u"Overstress Reason:")]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Capacitor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                capacitor.
        :param int subcategory_id: the ID of the capacitor subcategory.
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
            tooltip=_(u"Indicates whether or not the selected capacitor "
                      u"is overstressed."))
        self.txtReason = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=200,
            tooltip=_(u"The reason(s) the selected hardware item is "
                      u"overstressed."))
        self.txtVoltageRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating voltage to rated voltage for "
                      u"the capacitor."))

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

    def _make_stress_results_page(self):
        """
        Make the capacitor gtk.Notebook() assessment results page.

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
        _fixed.put(self.chkOverstress, _x_pos, _y_pos[1])
        _fixed.put(self.txtReason.scrollwindow, _x_pos, _y_pos[2])

        _fixed.show_all()

        # Create the derating plot.
        _frame = rtk.RTKFrame(label=_(u"Derating Curve and Operating Point"))
        _frame.add(self.pltDerate.plot)
        _frame.show_all()

        self.pack2(_frame, True, True)

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

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtVoltageRatio.set_text(
            str(self.fmt.format(_attributes['voltage_ratio'])))
        self.chkOverstress.set_active(_attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(_attributes['reason'])

        self._do_load_derating_curve()

        return _return
