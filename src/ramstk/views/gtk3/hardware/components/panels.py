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
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKComboBox, RAMSTKEntry, RAMSTKLabel,
    RAMSTKPanel, RAMSTKScrolledWindow, RAMSTKTextView
)


class RAMSTKAssessmentInputPanel(RAMSTKPanel):
    """Display Hardware assessment input attribute data.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analyses.  The attributes of a
    Hardware assessment input view are:

    :ivar _hazard_rate_method_id: the ID of the method to use for estimating
        the Hardware item's hazard rate.
    :ivar _subcategory_id: the ID of the Hardware item's subcategory.
    :ivar _title: the text to put on the RAMSTKFrame() holding the
        assessment input widgets.
    :ivar cmbQuality: select and display the quality level of the hardware
        item.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {}

        # Initialize private list attributes.
        self._lst_labels: List[str] = []
        self._lst_tooltips: List[str] = []

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = -1
        self._subcategory_id: int = -1
        self._title: str = _("Design Ratings")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()

    def do_load_common(self, attributes: Dict[str, Any]) -> None:
        """Load the component common widgets.

        :param attributes: the attributes dictionary for the selected
            Component.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']
        self._subcategory_id = attributes['subcategory_id']

        self.do_load_comboboxes(attributes['subcategory_id'])
        self._do_set_sensitive()

        self.cmbQuality.do_update(attributes['quality_id'], signal='changed')

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        """Set properties for Hardware assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

        _idx = 0
        for _widget in self._lst_widgets:
            _widget.do_set_properties(tooltip=self._lst_tooltips[_idx])
            _idx += 1


class RAMSTKStressInputPanel(RAMSTKPanel):
    """Display hardware item stress input attribute data.

    The hardware item stress input view displays all the assessment inputs for
    the selected hardware item.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a hardware item stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
        labels.

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
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware stress input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['temperature_rated_min', 'float'],
            1: ['temperature_knee', 'float'],
            2: ['temperature_rated_max', 'float'],
            3: ['current_rated', 'float'],
            4: ['current_operating', 'float'],
            5: ['power_rated', 'float'],
            6: ['power_operating', 'float'],
            7: ['voltage_rated', 'float'],
            8: ['voltage_ac_operating', 'float'],
            9: ['voltage_dc_operating', 'float'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
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
        self._lst_tooltips: List[str] = [
            _("The minimum rated temperature (in \u00B0C) of the hardware "
              "item."),
            _("The break temperature (in \u00B0C) of the hardware item beyond "
              "which it must be derated."),
            _("The maximum rated temperature (in \u00B0C) of the hardware "
              "item."),
            _("The rated current (in A) of the hardware item."),
            _("The operating current (in A) of the hardware item."),
            _("The rated power (in W) of the hardware item."),
            _("The operating power (in W) of the hardware item."),
            _("The rated voltage (in V) of the hardware item."),
            _("The operating ac voltage (in V) of the hardware item."),
            _("The operating DC voltage (in V) of the hardware item."),
        ]

        # Initialize private scalar attributes.
        self._record_id: int = -1
        self._subcategory_id: int = -1
        self._title: str = _("Operating Stresses")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
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
            self.txtTemperatureRatedMin,
            self.txtTemperatureKnee,
            self.txtTemperatureRatedMax,
            self.txtCurrentRated,
            self.txtCurrentOperating,
            self.txtPowerRated,
            self.txtPowerOperating,
            self.txtVoltageRated,
            self.txtVoltageAC,
            self.txtVoltageDC,
        ]

        super().do_make_panel_fixed()
        self.__set_properties()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Component stress input widgets.

        :param attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']

        self.txtTemperatureRatedMin.do_update(str(
            self.fmt.format(attributes['temperature_rated_min'])),
                                              signal='changed')  # noqa
        self.txtTemperatureKnee.do_update(str(
            self.fmt.format(attributes['temperature_knee'])),
                                          signal='changed')  # noqa
        self.txtTemperatureRatedMax.do_update(str(
            self.fmt.format(attributes['temperature_rated_max'])),
                                              signal='changed')  # noqa
        self.txtCurrentRated.do_update(str(
            self.fmt.format(attributes['current_rated'])),
                                       signal='changed')  # noqa
        self.txtCurrentOperating.do_update(str(
            self.fmt.format(attributes['current_operating'])),
                                           signal='changed')  # noqa
        self.txtPowerRated.do_update(str(
            self.fmt.format(attributes['power_rated'])),
                                     signal='changed')  # noqa
        self.txtPowerOperating.do_update(str(
            self.fmt.format(attributes['power_operating'])),
                                         signal='changed')  # noqa
        self.txtVoltageRated.do_update(str(
            self.fmt.format(attributes['voltage_rated'])),
                                       signal='changed')  # noqa
        self.txtVoltageAC.do_update(str(
            self.fmt.format(attributes['voltage_ac_operating'])),
                                    signal='changed')  # noqa
        self.txtVoltageDC.do_update(str(
            self.fmt.format(attributes['voltage_dc_operating'])),
                                    signal='changed')  # noqa

    def __set_callbacks(self) -> None:
        """Set common callback methods for the ModuleView and widgets.

        :return: None
        :rtype: None
        """
        self.txtTemperatureRatedMin.dic_handler_id[
            'changed'] = self.txtTemperatureRatedMin.connect(
                'changed',
                super().on_changed_entry, 0, 'wvw_editing_hardware')
        self.txtTemperatureKnee.dic_handler_id[
            'changed'] = self.txtTemperatureKnee.connect(
                'changed',
                super().on_changed_entry, 1, 'wvw_editing_hardware')
        self.txtTemperatureRatedMax.dic_handler_id[
            'changed'] = self.txtTemperatureRatedMax.connect(
                'changed',
                super().on_changed_entry, 2, 'wvw_editing_hardware')
        self.txtCurrentRated.dic_handler_id[
            'changed'] = self.txtCurrentRated.connect('changed',
                                                      super().on_changed_entry,
                                                      3,
                                                      'wvw_editing_hardware')
        self.txtCurrentOperating.dic_handler_id[
            'changed'] = self.txtCurrentOperating.connect(
                'changed',
                super().on_changed_entry, 4, 'wvw_editing_hardware')
        self.txtPowerRated.dic_handler_id[
            'changed'] = self.txtPowerRated.connect('changed',
                                                    super().on_changed_entry,
                                                    5, 'wvw_editing_hardware')
        self.txtPowerOperating.dic_handler_id[
            'changed'] = self.txtPowerOperating.connect(
                'changed',
                super().on_changed_entry, 6, 'wvw_editing_hardware')
        self.txtVoltageRated.dic_handler_id[
            'changed'] = self.txtVoltageRated.connect('changed',
                                                      super().on_changed_entry,
                                                      7,
                                                      'wvw_editing_hardware')
        self.txtVoltageAC.dic_handler_id[
            'changed'] = self.txtVoltageAC.connect('changed',
                                                   super().on_changed_entry, 8,
                                                   'wvw_editing_hardware')
        self.txtVoltageDC.dic_handler_id[
            'changed'] = self.txtVoltageDC.connect('changed',
                                                   super().on_changed_entry, 9,
                                                   'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for the stress input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

        _idx = 0
        for _widget in self._lst_widgets:
            _widget.do_set_properties(tooltip=self._lst_tooltips[_idx],
                                      width=125)
            _idx += 1


class RAMSTKAssessmentResultPanel(RAMSTKPanel):
    """Display Hardware assessment results attribute data.

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

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware assessment result view."""
        super().__init__()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels: List[str] = []
        self._lst_tooltips: List[str] = []

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = -1
        self._subcategory_id: int = -1
        self._title: str = _("Model Details")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lblModel: RAMSTKLabel = RAMSTKLabel('')

        self.txtLambdaB: RAMSTKEntry = RAMSTKEntry()
        self.txtPiQ: RAMSTKEntry = RAMSTKEntry()
        self.txtPiE: RAMSTKEntry = RAMSTKEntry()

        # Subscribe to PyPubSub messages.

    def do_load_common(self, attributes: Dict[str, Any]) -> None:
        """Load the Hardware assessment results page.

        :param attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        # Display the correct calculation model.
        self.__do_set_model_label()

        self.txtLambdaB.do_update(str(self.fmt.format(attributes['lambda_b'])))
        self.txtPiQ.do_update(str(self.fmt.format(attributes['piQ'])))
        self.txtPiE.do_update(str(self.fmt.format(attributes['piE'])))

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        """Set properties for Meter assessment result widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

        self.lblModel.set_tooltip_markup(self._lst_tooltips[0])

        _idx = 1
        for _widget in self._lst_widgets[1:]:
            _widget.do_set_properties(width=125,
                                      editable=False,
                                      bold=True,
                                      tooltip=self._lst_tooltips[_idx])
            _idx += 1

    def __do_set_model_label(self) -> None:
        """Set the text displayed in the hazard rate model RAMSTKLabel().

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:
            self.lblModel.set_markup(
                "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
                "\u03BB<sub>b</sub>\u03C0<sub>Q</sub></span> ")
        elif self._hazard_rate_method_id == 2:
            try:
                self.lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id])
            except KeyError:
                self.lblModel.set_markup("No Model")
        else:
            self.lblModel.set_markup("No Model")


class RAMSTKStressResultPanel(RAMSTKPanel):
    """Display Hardware stress results attribute data in the RAMSTK Work Book.

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

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware stress result view."""
        super().__init__()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria: List[List[float]] = [[0.6, 0.6, 0.0],
                                                        [0.9, 0.9, 0.0]]
        self._lst_labels: List[str] = [
            _("Current Ratio:"),
            _("Power Ratio:"),
            _("Voltage Ratio:"),
            "",
            _("Overstress Reason:"),
        ]
        self._lst_tooltips: List[str] = [
            _("Indicates whether or not the selected hardware item is "
              "overstressed."),
            _("The ratio of operating current to rated current for the "
              "hardware item."),
            _("The ratio of operating power to rated power for the hardware "
              "item."),
            _("The ratio of operating voltage to rated voltage for the "
              "hardware item."),
            _("The reason(s) the selected hardware item is overstressed."),
        ]

        # Initialize private scalar attributes.
        self._record_id: int = -1
        self._subcategory_id: int = 0
        self._title: str = _("Stress Summary")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkOverstress: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Overstressed"))
        self.txtCurrentRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtPowerRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtVoltageRatio: RAMSTKEntry = RAMSTKEntry()
        self.txtReason: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        self._lst_widgets = [
            self.txtCurrentRatio,
            self.txtPowerRatio,
            self.txtVoltageRatio,
            self.chkOverstress,
            self.txtReason,
        ]

        super().do_make_panel_fixed()
        self.__make_ui()
        self.__set_properties()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_derating_curve(self,
                                attributes: Dict[str, Any],
                                stress: str = 'voltage') -> None:
        """Load the benign and harsh environment derating curves.

        :return: None
        :rtype: None
        """
        # Plot the derating curves.
        _x = [
            float(attributes['temperature_rated_min']),
            float(attributes['temperature_knee']),
            float(attributes['temperature_rated_max'])
        ]

        self.pltPlot.axis.grid(True, which='both')

        self.pltPlot.do_load_plot(x_values=_x,
                                  y_values=self._lst_derate_criteria[0],
                                  marker='r.-')

        self.pltPlot.do_load_plot(x_values=_x,
                                  y_values=self._lst_derate_criteria[1],
                                  marker='b.-')

        self.pltPlot.do_load_plot(
            x_values=[attributes['temperature_active']],
            y_values=[attributes['{}_ratio'.format(stress)]],
            marker='go')

        self.pltPlot.do_make_title(
            _("{2} Derating Curve for {0} at {1}").format(
                attributes['part_number'], attributes['ref_des'],
                stress.title()),
            fontsize=12)

        self.pltPlot.do_make_legend(
            (_("Harsh Environment"), _("Mild Environment"),
             _("{} Operating Point").format(stress.title())))

        self.pltPlot.do_make_labels(_("Temperature (\u2070C)"),
                                    x_pos=0,
                                    y_pos=-0.2,
                                    fontsize=10)
        self.pltPlot.do_make_labels(_("{} Ratio").format(stress.title()),
                                    x_pos=-1,
                                    y_pos=0,
                                    set_x=False,
                                    fontsize=10)

        self.pltPlot.figure.canvas.draw()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Hardware stress results page common widgets.

        :param attributes: the attributes dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']

        self.txtCurrentRatio.do_update(
            str(self.fmt.format(attributes['current_ratio'])))
        self.txtPowerRatio.do_update(
            str(self.fmt.format(attributes['power_ratio'])))
        self.txtVoltageRatio.do_update(
            str(self.fmt.format(attributes['voltage_ratio'])))
        self.chkOverstress.set_active(attributes['overstress'])
        self.txtReason.do_update(attributes['reason'])

        self.pltPlot.axis.cla()
        if attributes['category_id'] in [2, 4]:
            self._do_load_derating_curve(attributes, stress='voltage')
        elif attributes['category_id'] == 3:
            self._do_load_derating_curve(attributes, stress='power')
        elif attributes['category_id'] in [6, 7]:
            self._do_load_derating_curve(attributes, stress='current')

    def __make_ui(self) -> None:
        """Make the Hardware stress results page.

        :return: None
        :rtype: None
        """
        _scrollwindow: RAMSTKScrolledWindow = self.get_child()
        self.remove(self.get_child())

        _hpaned: Gtk.HPaned = Gtk.HPaned()
        self.add(_hpaned)

        _hpaned.pack1(_scrollwindow, False, False)

        _scrollwindow = RAMSTKScrolledWindow(self.pltPlot.canvas)
        _hpaned.pack2(_scrollwindow, False, False)

        self.show_all()

    def __set_properties(self) -> None:
        """Set properties for the stress result widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

        self.chkOverstress.do_set_properties(tooltip=self._lst_tooltips[0])
        self.txtCurrentRatio.do_set_properties(width=125,
                                               editable=False,
                                               bold=True,
                                               tooltip=self._lst_tooltips[1])
        self.txtPowerRatio.do_set_properties(width=125,
                                             editable=False,
                                             bold=True,
                                             tooltip=self._lst_tooltips[2])
        self.txtVoltageRatio.do_set_properties(width=125,
                                               editable=False,
                                               bold=True,
                                               tooltip=self._lst_tooltips[3])
        self.txtReason.do_set_properties(height=100,
                                         width=350,
                                         tooltip=self._lst_tooltips[4])

        self.chkOverstress.set_sensitive(False)
        self.txtReason.set_editable(False)
