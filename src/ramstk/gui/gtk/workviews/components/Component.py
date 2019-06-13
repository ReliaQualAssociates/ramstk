# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Component.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Component Base Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import (
    RAMSTKCheckButton, RAMSTKComboBox, RAMSTKEntry, RAMSTKFrame,
    RAMSTKLabel, RAMSTKPlot, RAMSTKTextView, do_make_label_group,
)
from ramstk.gui.gtk.ramstk.Widget import Gdk, GObject, Gtk, _


class AssessmentInputs(Gtk.Fixed):
    """
    Display Hardware assessment input attribute data in the RAMSTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analyses.  The attributes of a
    Hardware assessment input view are:

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the hardware item
                               currently being displayed.

    :ivar cmbQuality: select and display the quality level of the hardware
                      item.
    """

    RAMSTK_CONFIGURATION = None

    # Define private list attributes.
    _lst_labels = []

    def __init__(self, configuration, **kwargs):    # pylint: disable=unused-argument
        """
        Initialize an instance of the Hardware assessment input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        GObject.GObject.__init__(self)
        self.RAMSTK_CONFIGURATION = configuration

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._subcategory_id = None
        self._hazard_rate_method_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = '{0:0.' + \
                   str(self.RAMSTK_CONFIGURATION.RAMSTK_DEC_PLACES) + \
                   'G}'

        self.cmbQuality = RAMSTKComboBox(
            index=0,
            simple=True,
        )

        self.__set_properties()

        # Subscribe to PyPubSub messages.

    def __set_properties(self):
        """
        Set properties for assessment input widgets common to all components.

        :return: None
        :rtype: None
        """
        self.cmbQuality.do_set_properties(tooltip=_("The quality level of the hardware item."),)

    def do_load_page(self, attributes):
        """
        Load the component common widgets.

        :param dict attributes: the attributes dictionary for the selected
        Component.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self._do_load_comboboxes(self._subcategory_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

    def make_ui(self):
        """
        Make the Hardware class Gtk.Notebook() assessment input page.

        :return: _x_pos, _y_pos
        :rtype: tuple
        """
        _x_pos, _y_pos = do_make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])

        return _x_pos, _y_pos

    def on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Component attribute.

        This method is called by:

            * RAMSTKComboBox() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
        with the calling RAMSTKComboBox().
        :return: None
        :rtype: None
        """
        try:
            _key = self._dic_keys[index]
        except KeyError:
            _key = ''

        combo.handler_block(self._lst_handler_id[index])

        try:
            _new_text = int(combo.get_active())
        except ValueError:
            _new_text = 0

        # Only publish the message if something is selected in the ComboBox.
        if _new_text != -1:
            pub.sendMessage(
                'wvw_editing_hardware',
                module_id=self._hardware_id,
                key=_key,
                value=_new_text,
            )

        combo.handler_unblock(self._lst_handler_id[index])

    def on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
        method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class Gtk.TreeModel()
        associated with the data from the calling Gtk.Widget().
        :return: None
        :rtype: None
        """
        try:
            _key = self._dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = int(entry.get_text())
        except ValueError:
            try:
                _new_text = float(entry.get_text())
            except ValueError:
                try:
                    _new_text = str(entry.get_text())
                except ValueError:
                    _new_text = None

        entry.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text,
        )


class StressInputs(Gtk.Fixed):
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
    :ivar txtCurrentRated: enter and display the current rating of the hardware
                           item.
    :ivar txtCurrentOperating: enter and display the operating current of the
                               hardware item.
    :ivar txtPowerRated: enter and display the rated power of the hardware
                         item.
    :ivar txtPowerOperating: enter and display the operating power of the
                             hardware item.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           hardware item.
    :ivar txtVoltageAC: enter and display the operating ac voltage of the
                        hardware item.
    :ivar txtVoltageDC: enter and display the operating DC voltage of the
                        hardware item.

    Callbacks signals in RAMSTKBaseView._lst_handler_id:

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

    RAMSTK_CONFIGURATION = None

    # Define private list attributes.
    _lst_labels = [
        _("Minimum Rated Temperature (\u00B0C):"),
        _("Knee Temperature (\u00B0C):"),
        _("Maximum Rated Temperature (\u00B0C):"),
        _("Rated Current (A):"),
        _("Operating Current (A):"),
        _("Rated Power (W):"),
        _("Operating Power (W):"),
        _("Rated Voltage (V):"),
        _("Operating ac Voltage (V):"),
        _("Operating DC Voltage (V):"),
    ]

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the Hardware stress input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        GObject.GObject.__init__(self)
        self.RAMSTK_CONFIGURATION = configuration

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._subcategory_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = '{0:0.' + \
                   str(self.RAMSTK_CONFIGURATION.RAMSTK_DEC_PLACES) + \
                   'G}'

        self.txtTemperatureRatedMin = RAMSTKEntry()
        self.txtTemperatureKnee = RAMSTKEntry()
        self.txtTemperatureRatedMax = RAMSTKEntry()
        self.txtCurrentRated = RAMSTKEntry()
        self.txtCurrentOperating = RAMSTKEntry()
        self.txtPowerRated = RAMSTKEntry()
        self.txtPowerOperating = RAMSTKEntry()
        self.txtVoltageRated = RAMSTKEntry()
        self.txtVoltageAC = RAMSTKEntry()
        self.txtVoltageDC = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.

    def __make_ui(self):
        """
        Make the Hardware module stress input container.

        :return: None
        :rtype: None
        """
        _x_pos, _y_pos = do_make_label_group(self._lst_labels, self, 5, 5)
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

    def __set_callbacks(self):
        """
        Set common callback methods for the ModuleView and widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.txtTemperatureRatedMin.connect(
                'changed', self._on_focus_out,
                0,
            ),
        )
        self._lst_handler_id.append(
            self.txtTemperatureKnee.connect('changed', self.on_focus_out, 1),
        )
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect(
                'changed', self._on_focus_out,
                2,
            ),
        )
        self._lst_handler_id.append(
            self.txtCurrentRated.connect('changed', self._on_focus_out, 3),
        )
        self._lst_handler_id.append(
            self.txtCurrentOperating.connect('changed', self._on_focus_out, 4),
        )
        self._lst_handler_id.append(
            self.txtPowerRated.connect('changed', self._on_focus_out, 5),
        )
        self._lst_handler_id.append(
            self.txtPowerOperating.connect('changed', self._on_focus_out, 6),
        )
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('changed', self._on_focus_out, 7),
        )
        self._lst_handler_id.append(
            self.txtVoltageAC.connect('changed', self._on_focus_out, 8),
        )
        self._lst_handler_id.append(
            self.txtVoltageDC.connect('changed', self._on_focus_out, 9),
        )

    def __set_properties(self):
        """
        Set properties for the stress input widgets common to all components.

        :return: None
        :rtype: None
        """
        self.txtTemperatureRatedMin.do_set_properties(
            width=125,
            tooltip=_(
                "The minimum rated temperature (in \u00B0C) of the "
                "hardware item.",
            ),
        )
        self.txtTemperatureKnee.do_set_properties(
            width=125,
            tooltip=_(
                "The break temperature (in \u00B0C) of the hardware item "
                "beyond which it must be derated.",
            ),
        )
        self.txtTemperatureRatedMax.do_set_properties(
            width=125,
            tooltip=_(
                "The maximum rated temperature (in \u00B0C) of the hardware "
                "item.",
            ),
        )
        self.txtCurrentRated.do_set_properties(
            width=125,
            tooltip=_("The rated current (in A) of the hardware item."),
        )
        self.txtCurrentOperating.do_set_properties(
            width=125,
            tooltip=_("The operating current (in A) of the hardware item."),
        )
        self.txtPowerRated.do_set_properties(
            width=125,
            tooltip=_("The rated power (in W) of the hardware item."),
        )
        self.txtPowerOperating.do_set_properties(
            width=125,
            tooltip=_("The operating power (in W) of the hardware item."),
        )
        self.txtVoltageRated.do_set_properties(
            width=125,
            tooltip=_("The rated voltage (in V) of the hardware item."),
        )
        self.txtVoltageAC.do_set_properties(
            width=125,
            tooltip=_(
                "The operating ac voltage (in V) of the hardware item.",
            ),
        )
        self.txtVoltageDC.do_set_properties(
            width=125,
            tooltip=_(
                "The operating DC voltage (in V) of the hardware "
                "item.",
            ),
        )

    def do_load_page(self, attributes):
        """
        Load the Component stress input widgets.

        :param dict attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']

        self.txtTemperatureRatedMin.handler_block(self._lst_handler_id[0])
        self.txtTemperatureRatedMin.set_text(
            str(self.fmt.format(attributes['temperature_rated_min'])),
        )
        self.txtTemperatureRatedMin.handler_unblock(self._lst_handler_id[0])

        self.txtTemperatureKnee.handler_block(self._lst_handler_id[1])
        self.txtTemperatureKnee.set_text(
            str(self.fmt.format(attributes['temperature_knee'])),
        )
        self.txtTemperatureKnee.handler_unblock(self._lst_handler_id[1])

        self.txtTemperatureRatedMax.handler_block(self._lst_handler_id[2])
        self.txtTemperatureRatedMax.set_text(
            str(self.fmt.format(attributes['temperature_rated_max'])),
        )
        self.txtTemperatureRatedMax.handler_unblock(self._lst_handler_id[2])

        self.txtCurrentRated.handler_block(self._lst_handler_id[3])
        self.txtCurrentRated.set_text(
            str(self.fmt.format(attributes['current_rated'])),
        )
        self.txtCurrentRated.handler_unblock(self._lst_handler_id[3])

        self.txtCurrentOperating.handler_block(self._lst_handler_id[4])
        self.txtCurrentOperating.set_text(
            str(self.fmt.format(attributes['current_operating'])),
        )
        self.txtCurrentOperating.handler_unblock(self._lst_handler_id[4])

        self.txtPowerRated.handler_block(self._lst_handler_id[5])
        self.txtPowerRated.set_text(
            str(self.fmt.format(attributes['power_rated'])),
        )
        self.txtPowerRated.handler_unblock(self._lst_handler_id[5])

        self.txtPowerOperating.handler_block(self._lst_handler_id[6])
        self.txtPowerOperating.set_text(
            str(self.fmt.format(attributes['power_operating'])),
        )
        self.txtPowerOperating.handler_unblock(self._lst_handler_id[6])

        self.txtVoltageRated.handler_block(self._lst_handler_id[7])
        self.txtVoltageRated.set_text(
            str(self.fmt.format(attributes['voltage_rated'])),
        )
        self.txtVoltageRated.handler_unblock(self._lst_handler_id[7])

        self.txtVoltageAC.handler_block(self._lst_handler_id[8])
        self.txtVoltageAC.set_text(
            str(self.fmt.format(attributes['voltage_ac_operating'])),
        )
        self.txtVoltageAC.handler_unblock(self._lst_handler_id[8])

        self.txtVoltageDC.handler_block(self._lst_handler_id[9])
        self.txtVoltageDC.set_text(
            str(self.fmt.format(attributes['voltage_dc_operating'])),
        )
        self.txtVoltageDC.handler_unblock(self._lst_handler_id[9])

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
                      method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class Gtk.TreeModel()
                          associated with the data from the calling
                          Gtk.Widget().  Indices are:

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

        :return: None
        :rtype: None
        """
        _dic_keys = {
            0: 'temperature_rated_min',
            1: 'temperature_knee',
            2: 'temperature_rated_max',
            3: 'current_rated',
            4: 'current_operating',
            5: 'power_rated',
            6: 'power_operating',
            7: 'voltage_rated',
            8: 'voltage_ac_operating',
            9: 'voltage_dc_operating',
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = float(entry.get_text())
        except ValueError:
            _new_text = 0.0

        entry.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text,
        )


class AssessmentResults(Gtk.Fixed):
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
    :ivar _lblModel: the :class:`ramstk.gui.gtk.ramstk.Label.RAMSTKLabel` to
                     display the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the hardware item.
    :ivar txtPiQ: displays the quality factor for the hardware item.
    :ivar txtPiE: displays the environment factor for the hardware item.
    """

    RAMSTK_CONFIGURATION = None

    def __init__(self, configuration, **kwargs):    # pylint: disable=unused-argument
        """
        Initialize an instance of the Hardware assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        GObject.GObject.__init__(self)
        self.RAMSTK_CONFIGURATION = configuration

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            "\u03BB<sub>b</sub>:", "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
        ]

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._subcategory_id = None
        self._hazard_rate_method_id = None

        self._lblModel = RAMSTKLabel(
            '',
            tooltip=_(
                "The assessment model used to calculate the hardware item "
                "hazard rate.",
            ),
        )

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = '{0:0.' + \
                   str(self.RAMSTK_CONFIGURATION.RAMSTK_DEC_PLACES) + \
                   'G}'

        self.txtLambdaB = RAMSTKEntry()
        self.txtPiQ = RAMSTKEntry()
        self.txtPiE = RAMSTKEntry()

        # Subscribe to PyPubSub messages.

    def __set_properties(self):
        """
        Set properties for assessment result widgets common to all components.

        :return: None
        :rtype: None
        """
        self.txtLambdaB.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The base hazard rate of the hardware item."),
        )
        self.txtPiQ.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The quality factor for the hardware item."),
        )
        self.txtPiE.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The environment factor for the hardware item."),
        )

    def do_load_page(self, attributes):
        """
        Load the Hardware assessment results page.

        :param dict attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        # Display the correct calculation model.
        if self._hazard_rate_method_id == 1:
            self._lblModel.set_markup(
                "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub></span>",
            )
        elif self._hazard_rate_method_id == 2:
            try:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id],
                )
            except KeyError:
                self._lblModel.set_markup("No Model")
        else:
            self._lblModel.set_markup("No Model")

        self.txtLambdaB.set_text(str(self.fmt.format(attributes['lambda_b'])))
        self.txtPiQ.set_text(str(self.fmt.format(attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(attributes['piE'])))

    def do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected hardware item.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)
        self.txtPiE.set_sensitive(False)

    def make_ui(self):
        """
        Make the Hardware Gtk.Notebook() assessment results page.

        :return: _x_pos, _y_pos
        :rtype: tuple
        """
        if self._hazard_rate_method_id == 1:
            self._lblModel.set_markup(
                "<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = "
                "\u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>",
            )
            self._lst_labels[0] = "\u03BB<sub>g</sub>:"
        else:
            try:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id],
                )
            except KeyError:
                self._lblModel.set_markup(_("Missing Model"))
            self._lst_labels[0] = "\u03BB<sub>b</sub>:"

        _x_pos, _y_pos = do_make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiQ, _x_pos, _y_pos[1])
        self.put(self.txtPiE, _x_pos, _y_pos[2])

        return _x_pos, _y_pos


class StressResults(Gtk.HPaned):
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

    :ivar str fmt: the format string for displaying numbers.

    :ivar chkOverstressed: display whether or not the selected hardware item is
                           overstressed.
    :ivar pltDerate: displays the derating curves and the design operating
                     point relative to those curves.
    :ivar txtCurrentRatio: display the ratio of operating current to rated
                           current.
    :ivar txtPowerRatio: display the ratio of operating power to rated power.
    :ivar txtVoltageRatio: display the ratio of operating voltage (ac + DC) to
                           rated voltage.
    :ivar txtReason: display the reason(s) the hardware item is overstressed.
    """

    RAMSTK_CONFIGURATION = None

    # Define private list attributes.
    _lst_labels = [
        _("Current Ratio:"),
        _("Power Ratio:"),
        _("Voltage Ratio:"), "",
        _("Overstress Reason:"),
    ]

    def __init__(self, configuration, **kwargs):    # pylint: disable=unused-argument
        """
        Initialize an instance of the Hardware stress result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        GObject.GObject.__init__(self)
        self.RAMSTK_CONFIGURATION = configuration

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._hardware_id = None
        self._subcategory_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = '{0:0.' + \
                   str(self.RAMSTK_CONFIGURATION.RAMSTK_DEC_PLACES) + \
                   'G}'

        self.pltDerate = RAMSTKPlot()

        self.chkOverstress = RAMSTKCheckButton(
            label=_("Overstressed"),
        )
        self.txtCurrentRatio = RAMSTKEntry()
        self.txtPowerRatio = RAMSTKEntry()
        self.txtVoltageRatio = RAMSTKEntry()
        self.txtReason = RAMSTKTextView(Gtk.TextBuffer(),)

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __make_ui(self):
        """
        Make the Hardware Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        _fixed = Gtk.Fixed()
        self.pack1(_fixed, True, True)

        _x_pos, _y_pos = do_make_label_group(
            self._lst_labels, _fixed, 5,
            35,
        )
        _x_pos += 50

        _fixed.put(self.txtCurrentRatio, _x_pos, _y_pos[0])
        _fixed.put(self.txtPowerRatio, _x_pos, _y_pos[1])
        _fixed.put(self.txtVoltageRatio, _x_pos, _y_pos[2])
        _fixed.put(self.chkOverstress, _x_pos, _y_pos[3])
        _fixed.put(self.txtReason.scrollwindow, _x_pos, _y_pos[4])

        _fixed.show_all()

        # Create the derating plot.
        _frame = RAMSTKFrame(
            label=_("Derating Curve and Operating Point"),
        )
        _frame.add(self.pltDerate.plot)
        _frame.show_all()

        self.pack2(_frame, True, True)

    def __set_properties(self):
        """
        Set properties for the stress result widgets common to all components.

        :return: None
        :rtype: None
        """
        self.chkOverstress.do_set_properties(
            tooltip=_(
                "Indicates whether or not the selected hardware item "
                "is overstressed.",
            ),
        )
        self.txtCurrentRatio.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The ratio of operating current to rated current for "
                "the hardware item.",
            ),
        )
        self.txtPowerRatio.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The ratio of operating power to rated power for "
                "the hardware item.",
            ),
        )
        self.txtVoltageRatio.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The ratio of operating voltage to rated voltage for "
                "the hardware item.",
            ),
        )
        self.txtReason.do_set_properties(
            width=250,
            tooltip=_(
                "The reason(s) the selected hardware item is "
                "overstressed.",
            ),
        )

        self.chkOverstress.set_sensitive(False)
        self.txtReason.set_editable(False)
        _bg_color = Gdk.RGBA(red=173.0, green=216.0, blue=230.0, alpha=1.0)
        self.txtReason.override_background_color(
            Gtk.StateFlags.NORMAL, _bg_color,
        )
        self.txtReason.override_background_color(
            Gtk.StateFlags.ACTIVE, _bg_color,
        )
        self.txtReason.override_background_color(
            Gtk.StateFlags.PRELIGHT, _bg_color,
        )
        self.txtReason.override_background_color(
            Gtk.StateFlags.SELECTED, _bg_color,
        )
        self.txtReason.override_background_color(
            Gtk.StateFlags.INSENSITIVE, _bg_color,
        )

    def _do_load_derating_curve(self, attributes):
        """
        Load the benign and harsh environment derating curves.

        :return: None
        :rtype: None
        """
        # Plot the derating curve.
        _x = [
            float(attributes['temperature_rated_min']),
            float(attributes['temperature_knee']),
            float(attributes['temperature_rated_max']),
        ]

        self.pltDerate.axis.cla()
        self.pltDerate.axis.grid(True, which='both')

        self.pltDerate.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[0],
            plot_type='scatter',
            marker='r.-',
        )

        self.pltDerate.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[1],
            plot_type='scatter',
            marker='b.-',
        )

        self.pltDerate.do_load_plot(
            x_values=[attributes['temperature_active']],
            y_values=[attributes['voltage_ratio']],
            plot_type='scatter',
            marker='go',
        )

        self.pltDerate.do_make_title(
            _("Voltage Derating Curve for {0:s} at {1:s}").format(
                attributes['part_number'], attributes['ref_des'],
            ),
            fontsize=12,
        )
        self.pltDerate.do_make_legend([
            _("Harsh Environment"),
            _("Mild Environment"),
            _("Voltage Operating Point"),
        ])

        self.pltDerate.do_make_labels(
            _("Temperature (\u2070C)"), 0, -0.2, fontsize=10,
        )
        self.pltDerate.do_make_labels(
            _("Voltage Ratio"), -1, 0, set_x=False, fontsize=10,
        )

        self.pltDerate.figure.canvas.draw()

    def _do_load_page(self, attributes):
        """
        Load the Hardware stress results page common widgets.

        :param dict attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']

        self.txtCurrentRatio.set_text(
            str(self.fmt.format(attributes['current_ratio'])),
        )
        self.txtPowerRatio.set_text(
            str(self.fmt.format(attributes['power_ratio'])),
        )
        self.txtVoltageRatio.set_text(
            str(self.fmt.format(attributes['voltage_ratio'])),
        )
        self.chkOverstress.set_active(attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(attributes['reason'])

        self._do_load_derating_curve(attributes)
