# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.workview.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Component Base Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKComboBox, RAMSTKEntry, RAMSTKLabel,
    RAMSTKPlot, RAMSTKScrolledWindow, RAMSTKTextView, RAMSTKWorkView
)


class RAMSTKAssessmentInputs(RAMSTKWorkView):
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

    # Define private list attributes.
    _lst_labels: List[str] = []

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'component') -> None:
        """
        Initialize an instance of the Hardware assessment input view.

        :param configuration: the RAMSTK User Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.RAMSTKUserConfiguration`
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.
        self._dic_switch: Dict[str, Union[object, int]] = {}

        # Initialize private list attributes.
        self._lst_handler_id: List[int] = []
        self._lst_widgets: List[object] = []

        # Initialize private scalar attributes.
        self._record_id: int = -1
        self._subcategory_id: int = 0
        self._hazard_rate_method_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt: str = (
            '{0:0.' + str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_DEC_PLACES) +
            'G}')

        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()

        self.__set_properties()

        # Subscribe to PyPubSub messages.

    def __set_properties(self) -> None:
        """
        Set properties for assessment input widgets common to all components.

        :return: None
        :rtype: None
        """
        self.cmbQuality.do_set_properties(
            tooltip=_("The quality level of the hardware item."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        This method is only required to satisfy the RAMSTKWorkView base
        class message listener requirement.  When we close a RAMSTK program
        database, any component-specific workviews will be removed from
        their containers which effectively clears their contents.

        :return: None
        :rtype: None
        """
    def do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the component common widgets.

        :param dict attributes: the attributes dictionary for the selected
            Component.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.do_load_comboboxes(attributes['subcategory_id'])

        self.cmbQuality.do_update(attributes['quality_id'],
                                  self._lst_handler_id[0])

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def make_ui(self, **kwargs: Any) -> None:
        """
        Make the Hardware class component Assessment Input container.

        This method lays out the Assessment Input Gtk.Fixed() with labels and
        input widgets for components.  Label text (_lst_labels) and widgets
        (_lst_widgets) are defined in each child class.

        :return: None
        :rtype: None
        """
        # This hardware WorkView assessment input page has the following
        # layout.  This meta-class is placed in the lower left quadrant.
        # +-----+-------------------+-------------------+
        # |  B  |      L. TOP       |      R. TOP       |
        # |  U  |                   |                   |
        # |  T  |                   |                   |
        # |  T  +-------------------+-------------------+
        # |  O  |     L. BOTTOM     |     R. BOTTOM     |
        # |  N  |                   |                   |
        # |  S  |                   |                   |
        # +-----+-------------------+-------------------+
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        (__, __, _fixed) = super().make_ui(start=0)
        self.pack_start(_fixed, True, True, 0)

        self.show_all()


class RAMSTKStressInputs(RAMSTKWorkView):
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

    RAMSTK_USER_CONFIGURATION = None

    # Define private dict class attributes.
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
        9: 'voltage_dc_operating'
    }

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
        _("Operating DC Voltage (V):")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'component') -> None:
        """
        Initialize an instance of the Hardware stress input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id: List[int] = []

        # Initialize private scalar attributes.
        self._record_id: int = -1
        self._subcategory_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt: str = (
            '{0:0.' + str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_DEC_PLACES) +
            'G}')

        self.txtTemperatureRatedMin: RAMSTKEntry = RAMSTKEntry()
        self.txtTemperatureKnee: RAMSTKEntry = RAMSTKEntry()
        self.txtTemperatureRatedMax: RAMSTKEntry = RAMSTKEntry()
        self.txtCurrentRated: RAMSTKEntry = RAMSTKEntry()
        self.txtCurrentOperating: RAMSTKEntry = RAMSTKEntry()
        self.txtPowerRated: RAMSTKEntry = RAMSTKEntry()
        self.txtPowerOperating: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageRated: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageAC: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageDC: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.txtTemperatureRatedMin, self.txtTemperatureKnee,
            self.txtTemperatureRatedMax, self.txtCurrentRated,
            self.txtCurrentOperating, self.txtPowerRated,
            self.txtPowerOperating, self.txtVoltageRated, self.txtVoltageAC,
            self.txtVoltageDC
        ]

        self.__set_properties()
        self.__set_callbacks()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __make_ui(self) -> None:
        """
        Make the Hardware module stress input container.

        :return: None
        :rtype: None
        """
        # The hardware WorkView assessment input page has the following
        # layout.  This meta-class is placed in the lower right quadrant.
        # +-----+-------------------+-------------------+
        # |  B  |      L. TOP       |      R. TOP       |
        # |  U  |                   |                   |
        # |  T  |                   |                   |
        # |  T  +-------------------+-------------------+
        # |  O  |     L. BOTTOM     |     R. BOTTOM     |
        # |  N  |                   |                   |
        # |  S  |                   |                   |
        # +-----+-------------------+-------------------+
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        (__, __, _fixed) = super().make_ui(start=0)
        self.pack_start(_fixed, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set common callback methods for the ModuleView and widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.txtTemperatureRatedMin.connect('focus-out-event',
                                                self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtTemperatureKnee.connect('focus-out-event',
                                            self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect('focus-out-event',
                                                self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.txtCurrentRated.connect('focus-out-event', self._on_focus_out,
                                         3))
        self._lst_handler_id.append(
            self.txtCurrentOperating.connect('focus-out-event',
                                             self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtPowerRated.connect('focus-out-event', self._on_focus_out,
                                       5))
        self._lst_handler_id.append(
            self.txtPowerOperating.connect('focus-out-event',
                                           self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('focus-out-event', self._on_focus_out,
                                         7))
        self._lst_handler_id.append(
            self.txtVoltageAC.connect('focus-out-event', self._on_focus_out,
                                      8))
        self._lst_handler_id.append(
            self.txtVoltageDC.connect('focus-out-event', self._on_focus_out,
                                      9))

    def __set_properties(self) -> None:
        """
        Set properties for the stress input widgets common to all components.

        :return: None
        :rtype: None
        """
        self.txtTemperatureRatedMin.do_set_properties(
            width=125,
            tooltip=_("The minimum rated temperature (in \u00B0C) of the "
                      "hardware item."))
        self.txtTemperatureKnee.do_set_properties(
            width=125,
            tooltip=_(
                "The break temperature (in \u00B0C) of the hardware item "
                "beyond which it must be derated."))
        self.txtTemperatureRatedMax.do_set_properties(
            width=125,
            tooltip=_(
                "The maximum rated temperature (in \u00B0C) of the hardware "
                "item."))
        self.txtCurrentRated.do_set_properties(
            width=125,
            tooltip=_("The rated current (in A) of the hardware item."))
        self.txtCurrentOperating.do_set_properties(
            width=125,
            tooltip=_("The operating current (in A) of the hardware item."))
        self.txtPowerRated.do_set_properties(
            width=125,
            tooltip=_("The rated power (in W) of the hardware item."))
        self.txtPowerOperating.do_set_properties(
            width=125,
            tooltip=_("The operating power (in W) of the hardware item."))
        self.txtVoltageRated.do_set_properties(
            width=125,
            tooltip=_("The rated voltage (in V) of the hardware item."))
        self.txtVoltageAC.do_set_properties(
            width=125,
            tooltip=_("The operating ac voltage (in V) of the hardware item."))
        self.txtVoltageDC.do_set_properties(
            width=125,
            tooltip=_("The operating DC voltage (in V) of the hardware "
                      "item."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        This method is only required to satisfy the RAMSTKWorkView base
        class message listener requirement.  When we close a RAMSTK program
        database, any component-specific workviews will be removed from
        their containers which effectively clears their contents.

        :return: None
        :rtype: None
        """
    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Component stress input widgets.

        :param dict attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']

        self.txtTemperatureRatedMin.do_update(
            str(self.fmt.format(attributes['temperature_rated_min'])),
            self._lst_handler_id[0])
        self.txtTemperatureKnee.do_update(
            str(self.fmt.format(attributes['temperature_knee'])),
            self._lst_handler_id[1])
        self.txtTemperatureRatedMax.do_update(
            str(self.fmt.format(attributes['temperature_rated_max'])),
            self._lst_handler_id[2])
        self.txtCurrentRated.do_update(
            str(self.fmt.format(attributes['current_rated'])),
            self._lst_handler_id[3])
        self.txtCurrentOperating.do_update(
            str(self.fmt.format(attributes['current_operating'])),
            self._lst_handler_id[4])
        self.txtPowerRated.do_update(
            str(self.fmt.format(attributes['power_rated'])),
            self._lst_handler_id[5])
        self.txtPowerOperating.do_update(
            str(self.fmt.format(attributes['power_operating'])),
            self._lst_handler_id[6])
        self.txtVoltageRated.do_update(
            str(self.fmt.format(attributes['voltage_rated'])),
            self._lst_handler_id[7])
        self.txtVoltageAC.do_update(
            str(self.fmt.format(attributes['voltage_ac_operating'])),
            self._lst_handler_id[8])
        self.txtVoltageDC.do_update(
            str(self.fmt.format(attributes['voltage_dc_operating'])),
            self._lst_handler_id[9])

    def _on_focus_out(
            self,
            entry: Gtk.Entry,
            __event: Gdk.EventFocus,  # pylint: disable=unused-argument
            index: int) -> None:
        """
        Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
            method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
            :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param __event: the Gdk.EventFocus that triggered the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Hardware class Gtk.TreeModel()
            associated with the data from the calling Gtk.Widget().  Indices
            are:

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
        super().on_focus_out(entry, index, 'wvw_editing_component')


class RAMSTKAssessmentResults(RAMSTKWorkView):
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
    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'component') -> None:
        """
        Initialize an instance of the Hardware assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            "", "\u03BB<sub>b</sub>:", "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:"
        ]

        # Initialize private scalar attributes.
        self._record_id: int = -1
        self._subcategory_id: int = 0
        self._hazard_rate_method_id: int = 0

        self._lblModel: RAMSTKLabel = RAMSTKLabel('')

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt: str = (
            '{0:0.' + str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_DEC_PLACES) +
            'G}')

        self.txtLambdaB: RAMSTKEntry = RAMSTKEntry()
        self.txtPiQ: RAMSTKEntry = RAMSTKEntry()
        self.txtPiE: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self._lblModel, self.txtLambdaB, self.txtPiQ, self.txtPiE
        ]

        self.__set_properties()

        # Subscribe to PyPubSub messages.

    def __set_properties(self) -> None:
        """
        Set properties for assessment result widgets common to all components.

        :return: None
        :rtype: None
        """
        self._lblModel.do_set_properties(tooltip=_(
            "The assessment model used to calculate the hardware item "
            "hazard rate."))

        self.txtLambdaB.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The base hazard rate of the hardware item."))
        self.txtPiQ.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The quality factor for the hardware item."))
        self.txtPiE.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The environment factor for the hardware item."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        This method is only required to satisfy the RAMSTKWorkView base
        class message listener requirement.  When we close a RAMSTK program
        database, any component-specific workviews will be removed from
        their containers which effectively clears their contents.

        :return: None
        :rtype: None
        """
    def _do_set_model_label(self) -> None:
        """
        Sets the text displayed in the hazard rate model RAMSTKLabel().

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:
            self._lblModel.set_markup(
                "<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = "
                "\u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>")
            self._lst_labels[0] = "\u03BB<sub>g</sub>:"
        else:
            try:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id])
            except KeyError:
                self._lblModel.set_markup(_("Missing Model"))

    def do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Hardware assessment results page.

        :param dict attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        # Display the correct calculation model.
        if self._hazard_rate_method_id == 1:
            self._lblModel.set_markup(
                "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub></span>"
            )
        elif self._hazard_rate_method_id == 2:
            try:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id], )
            except KeyError:
                self._lblModel.set_markup("No Model")
        else:
            self._lblModel.set_markup("No Model")

        self.txtLambdaB.set_text(str(self.fmt.format(attributes['lambda_b'])))
        self.txtPiQ.set_text(str(self.fmt.format(attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(attributes['piE'])))

    def do_set_sensitive(self) -> None:
        """
        Set widget sensitivity as needed for the selected hardware item.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)
        self.txtPiE.set_sensitive(False)

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def make_ui(self, **kwargs: Any) -> None:
        """
        Make the Hardware class component Assessment Results container.

        This method lays out the Assessment Results Gtk.Fixed() with labels and
        input widgets for components.  Label text (_lst_labels) and widgets
        (_lst_widgets) are defined in each child class.

        :return: None
        :rtype: None
        """
        # The hardware WorkView assessment input page has the following
        # layout.  This meta-class is placed in the lower left quadrant.
        # +-----+-------------------+-------------------+
        # |  B  |      L. TOP       |      R. TOP       |
        # |  U  |                   |                   |
        # |  T  |                   |                   |
        # |  T  +-------------------+-------------------+
        # |  O  |     L. BOTTOM     |     R. BOTTOM     |
        # |  N  |                   |                   |
        # |  S  |                   |                   |
        # +-----+-------------------+-------------------+
        # TODO: See issue #304.  Only _fixed will be returned in the future.
        (__, __, _fixed) = super().make_ui(start=0)
        self.pack_start(_fixed, True, True, 0)

        self.show_all()


class RAMSTKStressResults(RAMSTKWorkView):
    """
    Display Hardware stress results attribute data in the RAMSTK Work Book.

    The Hardware stress result view displays all the stress results for the
    selected hardware item.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of a
    Hardware stress result view are:

    :cvar list _lst_labels: the text to use for the stress results widget
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

    RAMSTK_USER_CONFIGURATION = None

    # Define private list class attributes.
    _lst_labels = [
        _("Current Ratio:"),
        _("Power Ratio:"),
        _("Voltage Ratio:"), "",
        _("Overstress Reason:")
    ]

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'component') -> None:
        """
        Initialize an instance of the Hardware stress result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        super().__init__(configuration, logger, module=module)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria: List[List[float]] = [[0.6, 0.6, 0.0],
                                                        [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._record_id: int = -1
        self._subcategory_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt: str = (
            '{0:0.' + str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_DEC_PLACES) +
            'G}')

        self.pltDerate: RAMSTKPlot = RAMSTKPlot()

        self.chkOverstress: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Overstressed"))
        self.txtCurrentRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtPowerRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtReason: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        self._lst_widgets = [
            self.txtCurrentRatio, self.txtPowerRatio, self.txtVoltageRatio,
            self.chkOverstress, self.txtReason
        ]

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')
        pub.subscribe(self._do_load_page, 'succeed_calculate_hardware')

    def __make_ui(self) -> None:
        """
        Make the Hardware Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # The hardware WorkView assessment input page has the following
        # layout.  This meta-class is placed in the lower right quadrant.
        # +-----+-------------------+-------------------+
        # |  B  |      L. TOP       |      R. TOP       |
        # |  U  |                   |                   |
        # |  T  |                   |                   |
        # |  T  +-------------------+-------------------+
        # |  O  |     L. BOTTOM     |     R. BOTTOM     |
        # |  N  |                   |                   |
        # |  S  |                   |                   |
        # +-----+-------------------+-------------------+
        _hpaned = Gtk.HPaned()
        self.pack_start(_hpaned, True, True, 0)

        # TODO: See issue #304.  Only _fixed will be returned in the future.
        (__, __, _fixed) = super().make_ui(start=0)
        _hpaned.pack1(_fixed, False, False)

        # Create the derating plot.
        _scrollwindow = RAMSTKScrolledWindow(self.pltDerate.plot)
        _hpaned.pack2(_scrollwindow, False, False)

        self.show_all()

    def __set_properties(self) -> None:
        """
        Set properties for the stress result widgets common to all components.

        :return: None
        :rtype: None
        """
        self.chkOverstress.do_set_properties(
            tooltip=_("Indicates whether or not the selected hardware item "
                      "is overstressed."))
        self.txtCurrentRatio.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The ratio of operating current to rated current for "
                      "the hardware item."))
        self.txtPowerRatio.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The ratio of operating power to rated power for "
                      "the hardware item."))
        self.txtVoltageRatio.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The ratio of operating voltage to rated voltage for "
                      "the hardware item."))
        self.txtReason.do_set_properties(
            height=100,
            width=350,
            tooltip=_("The reason(s) the selected hardware item is "
                      "overstressed."))

        self.chkOverstress.set_sensitive(False)
        self.txtReason.set_editable(False)

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        This method is only required to satisfy the RAMSTKWorkView base
        class message listener requirement.  When we close a RAMSTK program
        database, any component-specific workviews will be removed from
        their containers which effectively clears their contents.

        :return: None
        :rtype: None
        """
    def _do_load_derating_curve(self, attributes: Dict[str, Any]) -> None:
        """
        Load the benign and harsh environment derating curves.

        :return: None
        :rtype: None
        """
        # Plot the derating curve.
        _x = [
            float(attributes['temperature_rated_min']),
            float(attributes['temperature_knee']),
            float(attributes['temperature_rated_max'])
        ]

        self.pltDerate.axis.cla()
        self.pltDerate.axis.grid(True, which='both')

        self.pltDerate.do_load_plot(x_values=_x,
                                    y_values=self._lst_derate_criteria[0],
                                    marker='r.-')

        self.pltDerate.do_load_plot(x_values=_x,
                                    y_values=self._lst_derate_criteria[1],
                                    marker='b.-')

        self.pltDerate.do_load_plot(
            x_values=[attributes['temperature_active']],
            y_values=[attributes['voltage_ratio']],
            marker='go')

        self.pltDerate.do_make_title(
            _("Voltage Derating Curve for {0:s} at {1:s}").format(
                attributes['part_number'], attributes['ref_des']),
            fontsize=12)

        self.pltDerate.do_make_legend(
            (_("Harsh Environment"), _("Mild Environment"),
             _("Voltage Operating Point")))

        self.pltDerate.do_make_labels(_("Temperature (\u2070C)"),
                                      0,
                                      -0.2,
                                      fontsize=10)
        self.pltDerate.do_make_labels(_("Voltage Ratio"),
                                      -1,
                                      0,
                                      set_x=False,
                                      fontsize=10)

        self.pltDerate.figure.canvas.draw()

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Hardware stress results page common widgets.

        :param dict attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """

        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']

        self.txtCurrentRatio.set_text(
            str(self.fmt.format(attributes['current_ratio'])))
        self.txtPowerRatio.set_text(
            str(self.fmt.format(attributes['power_ratio'])))
        self.txtVoltageRatio.set_text(
            str(self.fmt.format(attributes['voltage_ratio'])))
        self.chkOverstress.set_active(attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(attributes['reason'])

        self._do_load_derating_curve(attributes)
