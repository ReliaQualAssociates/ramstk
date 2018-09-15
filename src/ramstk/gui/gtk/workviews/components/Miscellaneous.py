# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Miscellaneous.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class MiscAssessmentInputs(AssessmentInputs):
    """
    Display Miscellaneous assessment input attribute data in the RAMSTK Work Book.

    The Miscellaneous hardware assessment input view displays all the
    assessment inputs for the selected miscellaneous hardware item.  This
    includes, currently, inputs for MIL-HDBK-217FN2.  The attributes of a
    Miscellaneous hardware assessment input view are:

    :ivar cmbApplication: select and display the application of the
                          miscellaneous item (lamps only).
    :ivar cmbType: the type of miscellaneous item (filters only).
    :ivar txtFrequency: enter and display the operating frequency of the
                        miscellaneous item (crystals only).
    :ivar txtUtilization: enter and display the utilization factor of the
                          miscellaneous item (lamps only).

    Callbacks signals in _lst_handler_id:

    +-------+----------------------------+
    | Index | Widget - Signal            |
    +=======+============================+
    |   0   | cmbQuality - `changed`     |
    +-------+----------------------------+
    |   1   | cmbApplication - `changed` |
    +-------+----------------------------+
    |   2   | cmbType - `changed`        |
    +-------+----------------------------+
    |   3   | txtFrequency - `changed`   |
    +-------+----------------------------+
    |   4   | txtUtilization - `changed` |
    +-------+----------------------------+
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Miscellaneous assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`ramstk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentInputs.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Application:"))
        self._lst_labels.append(_(u"Type:"))
        self._lst_labels.append(_(u"Operating Frequency:"))
        self._lst_labels.append(_(u"Utilization:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication = ramstk.RAMSTKComboBox(
            index=0, simple=True, tooltip=_(u"The application of the lamp."))
        self.cmbType = ramstk.RAMSTKComboBox(
            index=0, simple=True, tooltip=_(u"The type of electronic filter."))

        self.txtFrequency = ramstk.RAMSTKEntry(
            width=125, tooltip=_(u"The operating frequency of the crystal."))
        self.txtUtilization = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The utilization factor (illuminate hours / equipment "
                      u"operate hours) of the lamp."))

        self._make_page()
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

    def _do_load_comboboxes(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the miscellaneous RKTComboBox()s.

        This method is used to load the specification RAMSTKComboBox() whenever
        the miscellaneous subcategory is changed.

        :param int subcategory_id: the newly selected miscellaneous hardware
                                   item subcategory ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_comboboxes(self, **kwargs)

        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_(u"Lower")]])

        # Load the application RAMSTKComboBox().
        self.cmbApplication.do_load_combo([[_(u"Incandescent, AC")],
                                           [_(u"Incandescent, DC")]])

        # Load the type RAMSTKComboBox().
        if _attributes['hazard_rate_method_id'] == 1:
            self.cmbType.do_load_combo(
                [[_(u"Ceramic-Ferrite")], [_(u"Discrete LC Components")],
                 [_(u"Discrete LC and Crystal Components")]])
        elif _attributes['hazard_rate_method_id'] == 2:
            self.cmbType.do_load_combo(
                [[_(u"MIL-F-15733 Ceramic-Ferrite")], [
                    _(u"MIL-F-15733 Discrete LC Components")
                ], [_(u"MIL-F-18327 Discrete LC Components")],
                 [_(u"MIL-F-18327 Discrete LC and Crystal Components")]])

        return _return

    def _do_load_page(self, **kwargs):
        """
        Load the Miscellaneous assesment input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_page(self, **kwargs)

        if self._subcategory_id == 4:  # Lamp
            self.cmbApplication.handler_block(self._lst_handler_id[1])
            self.cmbApplication.set_active(_attributes['application_id'])
            self.cmbApplication.handler_unblock(self._lst_handler_id[1])
        elif self._subcategory_id == 2:  # Filter
            self.cmbType.handler_block(self._lst_handler_id[2])
            self.cmbType.set_active(_attributes['type_id'])
            self.cmbType.handler_unblock(self._lst_handler_id[2])

        if _attributes['hazard_rate_method_id'] == 2:
            if self._subcategory_id == 1:  # Crystal
                self.txtFrequency.handler_block(self._lst_handler_id[3])
                self.txtFrequency.set_text(
                    str(self.fmt.format(_attributes['frequency_operating'])))
                self.txtFrequency.handler_unblock(self._lst_handler_id[3])
            elif self._subcategory_id == 4:  # Lamp
                self.txtUtilization.handler_block(self._lst_handler_id[4])
                self.txtUtilization.set_text(
                    str(self.fmt.format(_attributes['duty_cycle'])))
                self.txtUtilization.handler_unblock(self._lst_handler_id[4])

        return _return

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected miscellaneous.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbApplication.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtFrequency.set_sensitive(False)
        self.txtUtilization.set_sensitive(False)

        if self._subcategory_id == 4:  # Lamp
            self.cmbApplication.set_sensitive(True)
        elif self._subcategory_id == 2:  # Filter
            self.cmbType.set_sensitive(True)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id in [1, 2]:  # Crystal or filter
                self.cmbQuality.set_sensitive(True)
        elif _attributes['hazard_rate_method_id'] == 2:
            if self._subcategory_id == 1:  # Crystal
                self.cmbQuality.set_sensitive(True)
                self.txtFrequency.set_sensitive(True)
            elif self._subcategory_id == 4:  # Lamp
                self.txtUtilization.set_sensitive(True)
            elif self._subcategory_id == 2:  # Filter
                self.cmbQuality.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the Misc hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_load_comboboxes(subcategory_id=self._subcategory_id)

        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.cmbApplication, _x_pos, _y_pos[1])
        self.put(self.cmbType, _x_pos, _y_pos[2])
        self.put(self.txtFrequency, _x_pos, _y_pos[3])
        self.put(self.txtUtilization, _x_pos, _y_pos[4])

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Miscellaneous attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+
            |  Index  | Widget           |
            +=========+==================+
            |    1    | cmbApplication   |
            +---------+------------------+
            |    2    | cmbType          |
            +---------+------------------+

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
                _attributes['type_id'] = int(combo.get_active())

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
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

    def on_select(self, module_id, **kwargs):
        """
        Load the miscellaneous assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              miscellaneous.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)


class MiscAssessmentResults(AssessmentResults):
    """
    Display Misc assessment results attribute data in the RAMSTK Work Book.

    The Miscellaneous hardware item assessment result view displays all the
    assessment results for the selected miscellaneous hardware item.  This
    includes, currently, results for MIL-HDBK-217FN2 parts count and
    MIL-HDBK-217FN2 part stress methods.  The attributes of a miscellaneous
    hardware item assessment result view are:

    :ivar txtPiA: displays the application factor for the miscellaneous
                  hardware item.
    :ivar txtPiU: displays the utilization factor for the miscellaneous
                  hardware item.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub></span>",
        4:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>U</sub>\u03C0<sub>A</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Miscellaneous assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`ramstk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentResults.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>U</sub>:")
        self._lst_labels.append(u"\u03C0<sub>A</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the hardware item "
              u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiU = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The utilization factor for the lamp."))
        self.txtPiA = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The application factor for the lamp."))

        self._make_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self, **kwargs):
        """
        Load the miscellaneous devices assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentResults.do_load_page(self, **kwargs)

        self.txtPiU.set_text(str(self.fmt.format(_attributes['piU'])))
        self.txtPiA.set_text(str(self.fmt.format(_attributes['piA'])))

        if (_attributes['hazard_rate_method_id'] == 1
                and _attributes['subcategory_id'] in [3, 4]):
            self._lblModel.set_markup(
                u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = "
                u"\u03BB<sub>g</sub></span>")

        return _return

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected Misc hardware.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = AssessmentResults.do_set_sensitive(self, **kwargs)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiU.set_sensitive(False)
        self.txtPiA.set_sensitive(False)
        self.txtPiQ.set_sensitive(False)
        self.txtPiE.set_sensitive(True)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id in [1, 2]:
                self.txtPiQ.set_sensitive(True)
            self.txtPiE.set_sensitive(False)
        elif _attributes['hazard_rate_method_id'] == 2:
            if self._subcategory_id in [1, 2]:
                self.txtPiQ.set_sensitive(True)
            elif self._subcategory_id == 4:
                self.txtPiU.set_sensitive(True)
                self.txtPiA.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the Misc hardware item gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiU, _x_pos, _y_pos[3])
        self.put(self.txtPiA, _x_pos, _y_pos[4])

        return None

    def on_select(self, module_id, **kwargs):
        """
        Load the miscellaneous assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              miscellaneous.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)
