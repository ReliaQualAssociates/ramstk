# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Relay.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Relay Work View."""

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

    :cvar dict _dic_specifications: dictionary of relay MIL-SPECs.  Key is
                                    relay subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of relay styles defined in the
                            MIL-SPECs.  Key is relay subcategory ID; values
                            are lists of styles.

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the relay
                               currently being displayed.

    :ivar cmbType: select and display the type of relay.
    :ivar cmbLoadType: select and display the type of load the relay is
                       switching.
    :ivar cmbContactForm: select and display the form of the relay contacts.
    :ivar cmbContactRating: select and display the rating of the relay
                            contacts.
    :ivar cmbApplication: select and display the relay application.
    :ivar cmbConstruction: select and display the relay's method of
                           construction.

    :ivar txtCycles: enter and display the number of relay cycles per hour.

    Callbacks signals in _lst_handler_id:

    +----------+------------------------------+
    | Position | Widget - Signal              |
    +==========+==============================+
    |     0    | cmbQuality - `changed`       |
    +----------+------------------------------+
    |     1    | cmbType - `changed`          |
    +----------+------------------------------+
    |     2    | cmbLoadType - `changed`      |
    +----------+------------------------------+
    |     3    | cmbContactForm - `changed`   |
    +----------+------------------------------+
    |     4    | cmbContactRating - `changed` |
    +----------+------------------------------+
    |     5    | cmbApplication - `changed`   |
    +----------+------------------------------+
    |     6    | cmbConstruction - `changed`  |
    +----------+------------------------------+
    |     7    | txtCycles - `changed`        |
    +----------+------------------------------+
    """

    # Define private dict attributes.
    _dic_quality = {
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_(u"Lower")]],
        2: [["MIL-SPEC"], [_(u"Lower")]]
    }
    # Key is subcategory ID.  Index is type ID.
    _dic_pc_types = {
        1: [[_(u"General Purpose")], [_(u"Contactor, High Current")],
            [_(u"Latching")], [_(u"Reed")], [_(u"Thermal, Bi-Metal")],
            [_(u"Meter Movement")]],
        2: [[_(u"Solid State")], [_(u"Hybrid and Solid State Time Delay")]]
    }
    # Key is subcategory ID, index is type ID.
    _dic_types = {
        1: [[_("85C Rated")], [_("125C Rated")]],
        2: [[_(u"Solid State")], [_(u"Solid State Time Delay")],
            [_(u"Hybrid")]]
    }
    # Key is contact rating ID.  Index is application ID.
    _dic_application = {
        1: [[_(u"Dry Circuit")]],
        2: [[_(u"General Purpose")], [_(u"Sensitve (0 - 100mW)")],
            [_(u"Polarized")], [_(u"Vibrating Reed")], [_(u"High Speed")], [
                _(u"Thermal Time Delay")
            ], [_(u"Electronic Time Delay, Non-Thermal")],
            [_(u"Latching, Magnetic")]],
        3: [[_(u"High Voltage")], [_(u"Medium Power")]],
        4: [[_(u"Contactors, High Current")]]
    }
    # First key is contact rating ID, second key is application ID.  Index is
    # construction ID.
    _dic_construction = {
        1: {
            1: [[_(u"Armature (Long)")], [_(u"Dry Reed")],
                [_(u"Mercury Wetted")], [_(u"Magnetic Latching")],
                [_(u"Balanced Armature")], [_(u"Solenoid")]]
        },
        2: {
            1: [[_(u"Armature (Long)")], [_(u"Balanced Armature")],
                [_(u"Solenoid")]],
            2: [[_(u"Armature (LOng and Short)")], [_(u"Mercury Wetted")],
                [_(u"Magnetic Latching")], [_(u"Meter Movement")],
                [_(u"Balanced Armature")]],
            3: [[_(u"Armature (Short)")], [_(u"Meter Movement")]],
            4: [[_(u"Dry Reed")], [_(u"Mercury Wetted")]],
            5: [[_(u"Armature (Balanced and Short)")], [_(u"Dry Reed")]],
            6: [[_(u"Bimetal")]],
            8: [[_(u"Dry Reed")], [_(u"Mercury Wetted")],
                [_(u"Balanced Armature")]]
        },
        3: {
            1: [[_(u"Vacuum (Glass)")], [_(u"Vacuum (Ceramic)")]],
            2: [[_(u"Armature (Long and Short)")], [_(u"Mercury Wetted")],
                [_(u"Magnetic Latching")], [_(u"Mechanical Latching")],
                [_(u"Balanced Armature")], [_(u"Solenoid")]]
        },
        4: {
            1: [[_(u"Armature (Short)")], [_(u"Mechanical Latching")],
                [_(u"Balanced Armature")], [_(u"Solenoid")]]
        }
    }

    # Define private list attributes.
    # Index is the technology ID (load type).
    _lst_technology = [[_(u"Resistive")], [_(u"Inductive")], [_(u"Lamp")]]
    # Index is the contact form ID.
    _lst_contact_form = [["SPST"], ["DPST"], ["SPDT"], ["3PST"], ["4PST"],
                         ["DPDT"], ["3PDT"], ["4PDT"], ["6PDT"]]
    # Index is contact rating ID.
    _lst_contact_rating = [[_(u"Signal Current (low mV and mA)")],
                           [_(u"0 - 5 Amp")], [_(u"5 - 20 Amp")],
                           [_(u"20 - 600 Amp")]]

    _lst_labels = [
        _(u"Quality:"),
        _(u"Type:"),
        _(u"Load Type"),
        _(u"Contact Form:"),
        _(u"Contact Rating:"),
        _(u"Application:"),
        _(u"Construction:"),
        _(u"Number of Cycles/Hour:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Relay assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                relay.
        :param int subcategory_id: the ID of the relay subcategory.
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
            tooltip=_(u"The quality level of the relay."))
        self.cmbType = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The relay type."))
        self.cmbLoadType = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The type of load the relay is switching."))
        self.cmbContactForm = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The contact form of the relay."))
        self.cmbContactRating = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The rating of the relay contacts."))
        self.cmbApplication = rtk.RTKComboBox(
            index=0, simple=True, tooltip=_(u"The type of relay appliction."))
        self.cmbConstruction = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the relay."))

        self.txtCycles = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of relay on/off cycles per hour."))

        self._make_assessment_input_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbLoadType.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbContactForm.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbContactRating.connect('changed', self._on_combo_changed,
                                          4))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 6))

        self._lst_handler_id.append(
            self.txtCycles.connect('changed', self._on_focus_out, 7))

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the relay RKTComboBox()s.

        This method is used to load the specification RTKComboBox() whenever
        the relay subcategory is changed.

        :param int subcategory_id: the newly selected relay subcategory ID.
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

        # Load the relay type RTKComboBox().
        _model = self.cmbType.get_model()
        _model.clear()

        if _attributes['hazard_rate_method_id'] == 1:
            _data = self._dic_pc_types[self._subcategory_id]
        else:
            try:
                _data = self._dic_types[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbType.do_load_combo(_data)

        # Load the load type RTKComboBox().
        _model = self.cmbLoadType.get_model()
        _model.clear()
        self.cmbLoadType.do_load_combo(self._lst_technology)

        # Load the contact form RTKComboBox().
        _model = self.cmbContactForm.get_model()
        _model.clear()
        self.cmbContactForm.do_load_combo(self._lst_contact_form)

        # Load the contact rating RTKComboBox().
        _model = self.cmbContactRating.get_model()
        _model.clear()
        self.cmbContactRating.do_load_combo(self._lst_contact_rating)

        # Load the application RTKComboBox().
        self._do_load_application_combo(_attributes['contact_rating_id'])

        # Load the construction RTKComboBox().
        self._do_load_construction_combo(_attributes['contact_rating_id'],
                                         _attributes['application_id'])

        return _return

    def _do_load_application_combo(self, contact_rating_id):
        """
        Load the relay application RTKComboBox().

        :param int contact_rating_id: the contact rating ID used to select the
                                      correct list of relay applications.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _model = self.cmbApplication.get_model()
        _model.clear()

        try:
            _data = self._dic_application[contact_rating_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data)

        return False

    def _do_load_construction_combo(self, contact_rating_id, application_id):
        """
        Load the relay application RTKComboBox().

        :param int contact_rating_id: the contact rating ID used to select the
                                      correct list of relay construction
                                      methods.
        :param int application_id: the relay application ID used to select the
                                   correct list of relay construction methods.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _model = self.cmbConstruction.get_model()
        _model.clear()

        try:
            _data = self._dic_construction[contact_rating_id][application_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data)

        return False

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected relay.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbType.set_sensitive(True)
        self.cmbLoadType.set_sensitive(False)
        self.cmbContactForm.set_sensitive(False)
        self.cmbContactRating.set_sensitive(False)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtCycles.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            if self._subcategory_id == 1:
                self.cmbLoadType.set_sensitive(True)
                self.cmbContactForm.set_sensitive(True)
                self.cmbContactRating.set_sensitive(True)
                self.cmbApplication.set_sensitive(True)
                self.cmbConstruction.set_sensitive(True)
                self.txtCycles.set_sensitive(True)

        return _return

    def _make_assessment_input_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        self._do_load_comboboxes(self._subcategory_id)

        # Build the container for relays.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])
        self.put(self.cmbType, _x_pos, _y_pos[1])
        self.put(self.cmbLoadType, _x_pos, _y_pos[2])
        self.put(self.cmbContactForm, _x_pos, _y_pos[3])
        self.put(self.cmbContactRating, _x_pos, _y_pos[4])
        self.put(self.cmbApplication, _x_pos, _y_pos[5])
        self.put(self.cmbConstruction, _x_pos, _y_pos[6])
        self.put(self.txtCycles, _x_pos, _y_pos[7])

        self._do_set_sensitive()

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Relay attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    4    | cmbContactRating |
            +---------+------------------+---------+------------------+
            |    1    | cmbType          |    5    | cmbApplication   |
            +---------+------------------+---------+------------------+
            |    2    | cmbLoadType      |    6    | cmbConstruction  |
            +---------+------------------+---------+------------------+
            |    3    | cmbContactForm   |         |                  |
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
                _attributes['type_id'] = int(combo.get_active())
            elif index == 2:
                _attributes['technology_id'] = int(combo.get_active())
            elif index == 3:
                _attributes['contact_form_id'] = int(combo.get_active())
            elif index == 4:
                _attributes['contact_rating_id'] = int(combo.get_active())
                self._do_load_application_combo(
                    _attributes['contact_rating_id'])
            elif index == 5:
                _attributes['application_id'] = int(combo.get_active())
                self._do_load_construction_combo(
                    _attributes['contact_rating_id'],
                    _attributes['application_id'])
            elif index == 6:
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

            +---------+-----------+---------+-----------+
            |  Index  | Widget    |  Index  | Widget    |
            +=========+===========+=========+===========+
            |    7    | txtcycles |         |           |
            +---------+-----------+---------+-----------+

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

            if index == 7:
                _attributes['n_cycles'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the relay assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              relay.
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

        self.cmbType.handler_block(self._lst_handler_id[1])
        self.cmbType.set_active(_attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[1])

        self._do_set_sensitive()

        if _attributes['hazard_rate_method_id'] == 2:
            self.cmbLoadType.handler_block(self._lst_handler_id[2])
            self.cmbLoadType.set_active(_attributes['technology_id'])
            self.cmbLoadType.handler_unblock(self._lst_handler_id[2])

            self.cmbContactForm.handler_block(self._lst_handler_id[3])
            self.cmbContactForm.set_active(_attributes['contact_form_id'])
            self.cmbContactForm.handler_unblock(self._lst_handler_id[3])

            self.cmbContactRating.handler_block(self._lst_handler_id[4])
            self.cmbContactRating.set_active(_attributes['contact_rating_id'])
            self._do_load_application_combo(_attributes['contact_rating_id'])
            self.cmbContactRating.handler_unblock(self._lst_handler_id[4])

            self.cmbApplication.handler_block(self._lst_handler_id[5])
            self.cmbApplication.set_active(_attributes['application_id'])
            self._do_load_construction_combo(_attributes['contact_rating_id'],
                                             _attributes['application_id'])
            self.cmbApplication.handler_unblock(self._lst_handler_id[5])

            self.cmbConstruction.handler_block(self._lst_handler_id[6])
            self.cmbConstruction.set_active(_attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[6])

            self.txtCycles.handler_block(self._lst_handler_id[7])
            self.txtCycles.set_text(
                str(self.fmt.format(_attributes['n_cycles'])))
            self.txtCycles.handler_unblock(self._lst_handler_id[7])

        return _return


class StressInputs(gtk.Fixed):
    """
    Display Relay stress input attribute data in the RTK Work Book.

    The Relay stress input view displays all the assessment inputs for
    the selected relay.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a relay stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the relay
                               currently being displayed.

    :ivar txtCurrentRated: enter and display the rated current of the relay.
    :ivar txtCurrentOperating: enter and display the operating current of the
                               relay.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtCurrentRated - `changed`               |
    +----------+-------------------------------------------+
    |     1    | txtCurrentOperating - `changed`           |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [_(u"Rated Current (A):"), _(u"Operating Current (A):")]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Relay stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                relay.
        :param int subcategory_id: the ID of the relay subcategory.
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

        self.txtCurrentRated = rtk.RTKEntry(
            width=125, tooltip=_(u"The rated current (in A) of the relay."))
        self.txtCurrentOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating current (in A) of the relay."))

        self._lst_handler_id.append(
            self.txtCurrentRated.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtCurrentOperating.connect('changed', self._on_focus_out, 1))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the relay module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for relays.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtCurrentRated, _x_pos, _y_pos[0])
        self.put(self.txtCurrentOperating, _x_pos, _y_pos[1])

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

            +---------+--------------------+---------+-----------------------+
            |  Index  | Widget             |  Index  | Widget                |
            +=========+====================+=========+=======================+
            |    0    | txtCurrentRated    |    1    | txtCurrentOperating   |
            +---------+--------------------+---------+-----------------------+

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
                _attributes['current_rated'] = _text
            elif index == 1:
                _attributes['current_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the relay stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              relay.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # We don't block the callback signal otherwise the style RTKComboBox()
        # will not be loaded and set.
        self.txtCurrentRated.handler_block(self._lst_handler_id[0])
        self.txtCurrentRated.set_text(
            str(self.fmt.format(_attributes['current_rated'])))
        self.txtCurrentRated.handler_unblock(self._lst_handler_id[0])

        self.txtCurrentOperating.handler_block(self._lst_handler_id[1])
        self.txtCurrentOperating.set_text(
            str(self.fmt.format(_attributes['current_operating'])))
        self.txtCurrentOperating.handler_unblock(self._lst_handler_id[1])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display relay assessment results attribute data in the RTK Work Book.

    The relay assessment result view displays all the assessment results
    for the selected relay.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a relay assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the relay
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the relay.
    :ivar txtPiE: displays the environment factor for the relay.
    :ivar txtPiQ: displays the quality factor for the relay.
    :ivar txtPiC: displays the contact form factor for the relay.
    :ivar txtPiCYC: displays the cycling factor for the relay.
    :ivar txtPiL: displays the load stress factor for the relay.
    :ivar txtPiF: displays the application and construction factor for the
                  relay.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>CYC</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    # Define private list attributes.
    _lst_labels = [
        u"\u03BB<sub>b</sub>:", u"\u03C0<sub>E</sub>:", u"\u03C0<sub>Q</sub>:",
        u"\u03C0<sub>C</sub>:", u"\u03C0<sub>CYC</sub>:",
        u"\u03C0<sub>F</sub>:", u"\u03C0<sub>L</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Relay assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                relay.
        :param int subcategory_id: the ID of the relay subcategory.
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
            tooltip=_(u"The assessment model used to calculate the relay's "
                      u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the relay."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the relay."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the relay."))
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The contact form factor for the relay."))
        self.txtPiCYC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The cycling factor for the relay."))
        self.txtPiF = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The application and construction factor for the "
                      u"relay."))
        self.txtPiL = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The load stress factor for the relay."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the relay assessment results wodgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiCYC.set_text(str(self.fmt.format(_attributes['piCYC'])))
        self.txtPiF.set_text(str(self.fmt.format(_attributes['piF'])))
        self.txtPiL.set_text(str(self.fmt.format(_attributes['piL'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected relay.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiE.set_sensitive(False)
        self.txtPiQ.set_sensitive(True)
        self.txtPiC.set_sensitive(False)
        self.txtPiCYC.set_sensitive(False)
        self.txtPiF.set_sensitive(False)
        self.txtPiL.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            self.txtPiE.set_sensitive(True)
            if self._subcategory_id == 1:
                self.txtPiC.set_sensitive(True)
                self.txtPiCYC.set_sensitive(True)
                self.txtPiF.set_sensitive(True)
                self.txtPiL.set_sensitive(True)

        return _return

    def _make_assessment_results_page(self):
        """
        Make the relay gtk.Notebook() assessment results page.

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

        # Build the container for relays.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiE, _x_pos, _y_pos[1])
        self.put(self.txtPiQ, _x_pos, _y_pos[2])
        self.put(self.txtPiC, _x_pos, _y_pos[3])
        self.put(self.txtPiCYC, _x_pos, _y_pos[4])
        self.put(self.txtPiF, _x_pos, _y_pos[5])
        self.put(self.txtPiL, _x_pos, _y_pos[6])

        self.show_all()

        return None

    def on_select(self, module_id=None):
        """
        Load the relay assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              relay.
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
    Display relay stress results attribute data in the RTK Work Book.

    The relay stress result view displays all the stress results for the
    selected relay.  This includes, currently, results for MIL-HDBK-217FN2
    parts count and MIL-HDBK-217FN2 part stress methods.  The attributes of a
    relay stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the relay
                               currently being displayed.

    :ivar txtCurrentRatio: enter and display the current ratio of the relay.
    """

    # Define private list attributes.
    _lst_labels = [_(u"Current Ratio:"), "", _(u"Overstress Reason:")]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Relay assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                relay.
        :param int subcategory_id: the ID of the relay subcategory.
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

        self.chkOverstress = rtk.RTKCheckButton(
            label=_(u"Overstressed"),
            tooltip=_(u"Indicates whether or not the selected relay "
                      u"is overstressed."))
        self.txtReason = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=250,
            tooltip=_(u"The reason(s) the selected hardware item is "
                      u"overstressed."))
        self.txtCurrentRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating current to rated current for "
                      u"the relay."))

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
            float(_attributes['current_rated']),
            float(0.9 * _attributes['current_rated']),
            float(0.75 * _attributes['current_rated'])
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
        Load the relay stress results widgets.

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
        Make the relay gtk.Notebook() assessment results page.

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
        Load the relay assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              relay.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_load_page()

        return _return
