# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.workviews.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Validation Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageRequirements
import pandas as pd
# noinspection PyPackageRequirements
from matplotlib.patches import Ellipse
# pylint: disable=ungrouped-imports
# noinspection PyPackageRequirements
from pandas.plotting import register_matplotlib_converters
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton, RAMSTKComboBox, RAMSTKDateSelect, RAMSTKEntry, RAMSTKFrame,
    RAMSTKLabel, RAMSTKPlot, RAMSTKSpinButton, RAMSTKTextView, RAMSTKWorkView,
    do_make_buttonbox)

register_matplotlib_converters()


class GeneralData(RAMSTKWorkView):
    """
    Display general Validation attribute data in the RAMSTK Work Book.

    The Validation Work View displays all the general data attributes for the
    selected Validation. The attributes of a Validation General Data Work View
    are:

    :cvar dict _dic_keys:
    :cvar list _lst_labels: the list of label text.
    :cvar str _module: the name of the module.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """
    # Define private dict class attributes.
    _dic_keys = {
        0: ['description', 'string'],
        1: 'task_type',
        2: ['task_specification', 'string'],
        3: 'measurement_unit',
        4: ['acceptable_minimum', 'float'],
        5: ['acceptable_maximum', 'float'],
        6: ['acceptable_mean', 'float'],
        7: ['acceptable_variance', 'float'],
        8: ['date_start', 'string'],
        9: ['date_end', 'string'],
        11: ['time_minimum', 'float'],
        12: ['time_average', 'float'],
        13: ['time_maximum', 'float'],
        14: ['cost_minimum', 'float'],
        15: ['cost_average', 'float'],
        16: ['cost_maximum', 'float'],
        32: ['name', 'string']
    }

    # Define private list class attributes.
    _lst_labels = [
        _("Task ID:"),
        _("Task Name:"),
        _("Task Description:"),
        _("Task Type:"),
        _("Specification:"),
        _("Measurement Unit:"),
        _("Min. Acceptable:"),
        _("Max. Acceptable:"),
        _("Mean Acceptable:"),
        _("Variance:"),
        _("Start Date:"),
        _("End Date:"),
        _("% Complete:"),
        _("Min. Task Time:"),
        _("Most Likely Task Time:"),
        _("Max. Task Time:"),
        _("Task Time (95% Confidence):"),
        _("Min. Task Cost:"),
        _("Most Likely Task Cost:"),
        _("Max. Task Cost:"),
        _("Task Cost (95% Confidence):"),
        _("Project Time (95% Confidence):"),
        _("Project Cost (95% Confidence):")
    ]
    _lst_title: List[str] = [_("Task Description"), ""]

    # Define private scalar class attributes.
    _module: str = 'validation'
    _tablabel: str = _("General\nData")
    _tabtooltip: str = _(
        "Displays general information for the selected Verification task.")

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Validation Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate, self._do_request_calculate_all
        ]
        self._lst_icons = ['calculate', 'calculate_all']
        self._lst_tooltips = [
            _("Calculate the expected cost and "
              "time of the selected Validation "
              "task."),
            _("Calculate the cost and time "
              "of the program (i.e., all "
              "Validation tasks).")
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnEndDate: RAMSTKButton = RAMSTKButton()
        self.btnStartDate: RAMSTKButton = RAMSTKButton()

        self.cmbTaskType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbMeasurementUnit: RAMSTKComboBox = RAMSTKComboBox()

        self.spnStatus: RAMSTKSpinButton = RAMSTKSpinButton()

        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtMaxAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtMinAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtVarAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()
        self.txtTask: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtEndDate: RAMSTKEntry = RAMSTKEntry()
        self.txtStartDate: RAMSTKEntry = RAMSTKEntry()
        self.txtMinTime: RAMSTKEntry = RAMSTKEntry()
        self.txtExpTime: RAMSTKEntry = RAMSTKEntry()
        self.txtMaxTime: RAMSTKEntry = RAMSTKEntry()
        self.txtMinCost: RAMSTKEntry = RAMSTKEntry()
        self.txtExpCost: RAMSTKEntry = RAMSTKEntry()
        self.txtMaxCost: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanTimeLL: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanTime: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanTimeUL: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanCostLL: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanCost: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanCostUL: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectTimeLL: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectTime: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectTimeUL: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectCostLL: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectCost: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectCostUL: RAMSTKEntry = RAMSTKEntry()

        self._dic_switch: Dict[str, Union[object, str]] = {
            'description': [self.txtTask.do_update, 'changed'],
            'task_type': [self.cmbTaskType.do_update, 'changed'],
            'task_specification': [self.txtSpecification.do_update, 'changed'],
            'measurement_unit': [self.cmbMeasurementUnit.do_update, 'changed'],
            'acceptable_minimum': [self.txtMinAcceptable, 'changed'],
            'acceptable_mean': [self.txtMeanAcceptable, 'changed'],
            'acceptable_maximum': [self.txtMaxAcceptable, 'changed'],
            'acceptable_variance':
            [self.txtVarAcceptable.do_update, 'changed'],
            'date_start': [self.txtStartDate.do_update, 'changed'],
            'date_end': [self.txtEndDate.do_update, 'changed'],
            'status': [self.spnStatus.do_update, 'changed'],
            'time_minimum': [self.txtMinTime.do_update, 'changed'],
            'time_average': [self.txtExpTime.do_update, 'changed'],
            'time_maximum': [self.txtMaxTime.do_update, 'changed'],
            'cost_minimum': [self.txtMinCost.do_update, 'changed'],
            'cost_average': [self.txtExpCost.do_update, 'changed'],
            'cost_maximum': [self.txtMaxCost.do_update, 'changed']
        }

        self._lst_widgets = [
            self.txtCode, self.txtName, self.txtTask, self.cmbTaskType,
            self.txtSpecification, self.cmbMeasurementUnit,
            self.txtMinAcceptable, self.txtMaxAcceptable,
            self.txtMeanAcceptable, self.txtVarAcceptable, self.txtStartDate,
            self.txtEndDate, self.spnStatus, self.txtMinTime, self.txtExpTime,
            self.txtMaxTime, self.txtMeanTimeLL, self.txtMinCost,
            self.txtExpCost, self.txtMaxCost, self.txtMeanCostLL,
            self.txtProjectTimeLL, self.txtProjectCostLL
        ]

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()
        self.__load_combobox()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'selected_validation')

        pub.subscribe(self.do_set_cursor_active,
                      'succeed_calculate_validation_task')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_validation')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_calculate_validation_task')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_validation')

    def __do_make_task_code(self, task_type: str) -> str:
        """
        Create the validation task code.

        This method builds the task code based on the task type and the task
        ID.  The code created has the form:

            task type 3-letter abbreviation-task ID

        :param str task_type: the three letter abbreviation for the task type.
        :return: _code
        :rtype: str
        """
        _code = ''

        # Update the Validation task name for the selected Validation task.
        _types = self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        # pylint: disable=unused-variable
        for __, _type in _types.items():
            if _type[1] == task_type:
                _code = '{0:s}-{1:04d}'.format(_type[0], int(self._record_id))

        pub.sendMessage('wvw_editing_validation',
                        node_id=[self._record_id, -1, ''],
                        package={'name': _code})

        return _code

    def __load_combobox(self) -> None:
        """
        Load the RAMSTK ComboBox widgets with lists of information.

        :return: None
        :rtype: None
        """
        _model = self.cmbTaskType.get_model()
        _model.clear()

        _data = []
        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE:
            _data.append([
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE[_key][1]
            ], )
        self.cmbTaskType.do_load_combo(_data)

        _model = self.cmbMeasurementUnit.get_model()
        _model.clear()

        _data = []
        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS:
            _data.append([
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS[_key]
                [1]
            ], )
        self.cmbMeasurementUnit.do_load_combo(_data)

    def __make_ui(self) -> None:
        """
        Create the Validation Work View general data page.

        :return: None
        :rtype: None
        """
        # This page has the following layout:
        # +-----+-------------------+-------------------+
        # |  B  |      L. SIDE      |      R. TOP       |
        # |  U  |                   |                   |
        # |  T  |                   |                   |
        # |  T  |                   +-------------------+
        # |  O  |                   |     R. BOTTOM     |
        # |  N  |                   |                   |
        # |  S  |                   |                   |
        # +-----+-------------------+-------------------+
        #                                                     buttons -+-> self
        #                                                              |
        #                  Gtk.Fixed --> RAMSTKFrame -+-> Gtk.HPaned --+
        #                                             |
        #  Gtk.Fixed --> RAMSTKFrame -+-> Gtk.VPaned -+
        #                             |
        #  Gtk.Fixed --> RAMSTKFrame -+
        # Build out the containers for the page.
        _hpaned: Gtk.HPaned = Gtk.HPaned()
        self.pack_start(_hpaned, True, True, 0)

        # Place the LEFT side widgets.
        _frame: RAMSTKFrame = super().make_ui(end=13)
        _hpaned.pack1(_frame, True, True)

        # Place the RIGHT side widgets.
        _vpaned: Gtk.VPaned = Gtk.VPaned()
        _hpaned.pack2(_vpaned, True, True)
        _vpaned.pack1(self.__make_ui_top_right(), True, True)
        _vpaned.pack2(self.__make_ui_bottom_right(), True, True)

        self.show_all()

    def __make_ui_bottom_right(self) -> RAMSTKFrame:
        """
        Make the bottom right frame of the UI.

        :return: _frame; the frame containing the Gtk.Fixed() with widgets
            loaded.
        :rtype: :class:`ramstk.views.gtk3.widgets.RAMSTKFrame`
        """
        _frame = super().make_ui(start=21, title=[_("Project Effort"), ""])

        # We add the project time and project time UL to the same y position
        # as the project time LL widget.
        _fixed = _frame.get_children()[0].get_children()[0].get_children()[0]
        _time_entry = _fixed.get_children()[1]
        _cost_entry = _fixed.get_children()[-1]
        _x_pos: int = _fixed.child_get_property(_time_entry, 'x')
        _y_pos: int = _fixed.child_get_property(_time_entry, 'y')
        _fixed.put(self.txtProjectTime, _x_pos + 175, _y_pos)
        _fixed.put(self.txtProjectTimeUL, _x_pos + 350, _y_pos)

        # We add the project cost and project cost UL to the same y position
        # as the project cost LL widget.
        _x_pos: int = _fixed.child_get_property(_cost_entry, 'x')
        _y_pos: int = _fixed.child_get_property(_cost_entry, 'y')
        _fixed.put(self.txtProjectCost, _x_pos + 175, _y_pos)
        _fixed.put(self.txtProjectCostUL, _x_pos + 350, _y_pos)

        return _frame

    def __make_ui_top_right(self) -> RAMSTKFrame:
        """
        Make the top right frame of the UI.

        :return: _frame; the frame containing the Gtk.Fixed() with widgets
            loaded.
        :rtype: :class:`ramstk.views.gtk3.widgets.RAMSTKFrame`
        """
        _frame = super().make_ui(start=13,
                                 end=21,
                                 title=[_("Task Effort"), ""])

        # We add the mean time and mean time UL to the same y position as
        # the mean time LL widget.
        _fixed = _frame.get_children()[0].get_children()[0].get_children()[0]
        _time_entry = _fixed.get_children()[7]
        _cost_entry = _fixed.get_children()[-1]
        _x_pos = _fixed.child_get_property(_time_entry, 'x')
        _y_pos = _fixed.child_get_property(_time_entry, 'y')
        _fixed.put(self.txtMeanTime, _x_pos + 175, _y_pos)
        _fixed.put(self.txtMeanTimeUL, _x_pos + 350, _y_pos)

        # We add the mean cost and mean cost UL to the same y position as
        # the mean cost LL widget.
        _x_pos = _fixed.child_get_property(_cost_entry, 'x')
        _y_pos = _fixed.child_get_property(_cost_entry, 'y')
        _fixed.put(self.txtMeanCost, _x_pos + 195, _y_pos)
        _fixed.put(self.txtMeanCostUL, _x_pos + 390, _y_pos)

        return _frame

    # noinspection PyArgumentList
    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions.

        :return: None
        :rtype: None
        """
        self.btnEndDate.connect('button-release-event', self._do_select_date,
                                self.txtEndDate)
        self.btnStartDate.connect('button-release-event', self._do_select_date,
                                  self.txtStartDate)
        self.spnStatus.dic_handler_id['changed'] = self.spnStatus.connect(
            'focus-out-event', self._on_value_changed)

        # noinspection PyArgumentList
        self.txtTask.dic_handler_id['changed'] = self.txtTask.do_get_buffer(
        ).connect('changed', self._on_focus_out, None, 0)
        self.cmbTaskType.dic_handler_id['changed'] = self.cmbTaskType.connect(
            'changed', self._on_combo_changed, 1)
        self.txtSpecification.dic_handler_id[
            'changed'] = self.txtSpecification.connect('focus-out-event',
                                                       self._on_focus_out, 2)
        self.cmbMeasurementUnit.dic_handler_id[
            'changed'] = self.cmbMeasurementUnit.connect(
                'changed', self._on_combo_changed, 3)
        self.txtMinAcceptable.dic_handler_id[
            'changed'] = self.txtMinAcceptable.connect('focus-out-event',
                                                       self._on_focus_out, 4)
        self.txtMaxAcceptable.dic_handler_id[
            'changed'] = self.txtMaxAcceptable.connect('focus-out-event',
                                                       self._on_focus_out, 5)
        self.txtMeanAcceptable.dic_handler_id[
            'changed'] = self.txtMeanAcceptable.connect(
                'focus-out-event', self._on_focus_out, 6)
        self.txtVarAcceptable.dic_handler_id[
            'changed'] = self.txtVarAcceptable.connect('focus-out-event',
                                                       self._on_focus_out, 7)
        self.txtStartDate.dic_handler_id[
            'changed'] = self.txtStartDate.connect('changed',
                                                   self._on_focus_out, None, 8)
        self.txtEndDate.dic_handler_id['changed'] = self.txtEndDate.connect(
            'changed', self._on_focus_out, None, 9)

        self.txtMinTime.dic_handler_id['changed'] = self.txtMinTime.connect(
            'focus-out-event', self._on_focus_out, 11)
        self.txtExpTime.dic_handler_id['changed'] = self.txtExpTime.connect(
            'focus-out-event', self._on_focus_out, 12)
        self.txtMaxTime.dic_handler_id['changed'] = self.txtMaxTime.connect(
            'focus-out-event', self._on_focus_out, 13)
        self.txtMinCost.dic_handler_id['changed'] = self.txtMinCost.connect(
            'focus-out-event', self._on_focus_out, 14)
        self.txtExpCost.dic_handler_id['changed'] = self.txtExpCost.connect(
            'focus-out-event', self._on_focus_out, 15)
        self.txtMaxCost.dic_handler_id['changed'] = self.txtMaxCost.connect(
            'focus-out-event', self._on_focus_out, 16)

    def __set_properties(self) -> None:
        """
        Set the properties of the General Data Work View and widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnEndDate.do_set_properties(
            height=25,
            width=25,
            tooltip=_("Launches the calendar to select the date the task was "
                      "completed."))
        self.btnStartDate.do_set_properties(
            height=25,
            width=25,
            tooltip=_("Launches the calendar to select the date the task was "
                      "started."))

        # ----- COMBOBOXES
        self.cmbTaskType.do_set_properties(
            tooltip=_("Selects and displays the type of task for the "
                      "selected V&amp;V activity."))
        self.cmbMeasurementUnit.do_set_properties(tooltip=_(
            "Selects and displays the measurement unit for the selected "
            "V&amp;V activity acceptance parameter."))

        # ----- ENTRIES
        self.txtTask.do_set_properties(
            height=100,
            width=500,
            tooltip=_(
                "Displays the description of the selected V&amp;V activity."))
        self.txtCode.do_set_properties(
            width=50,
            editable=False,
            tooltip=_("Displays the ID of the selected V&amp;V activity."))
        self.txtMaxAcceptable.do_set_properties(
            width=100,
            tooltip=_("Displays the maximum acceptable value for the selected "
                      "V&amp;V activity."))
        self.txtMeanAcceptable.do_set_properties(
            width=100,
            tooltip=_(
                "Displays the mean acceptable value for the selected V&amp;V "
                "activity."))
        self.txtMinAcceptable.do_set_properties(
            width=100,
            tooltip=_("Displays the minimum acceptable value for the selected "
                      "V&amp;V activity."))
        self.txtVarAcceptable.do_set_properties(
            width=100,
            tooltip=_("Displays the acceptable variance for the selected "
                      "V&amp;V activity."))
        self.txtSpecification.do_set_properties(tooltip=_(
            "Displays the internal or industry specification or procedure "
            "governing the selected V&amp;V activity."))
        self.txtEndDate.do_set_properties(
            width=100,
            tooltip=_("Displays the date the selected V&amp;V activity is "
                      "scheduled to end."))
        self.txtStartDate.do_set_properties(
            width=100,
            tooltip=_("Displays the date the selected V&amp;V activity is "
                      "scheduled to start."))
        self.txtMinTime.do_set_properties(
            width=100,
            tooltip=_(
                "Minimum person-time needed to complete the selected task."))
        self.txtExpTime.do_set_properties(
            width=100,
            tooltip=_(
                "Most likely person-time needed to complete the selected "
                "task."))
        self.txtMaxTime.do_set_properties(
            width=100,
            tooltip=_(
                "Maximum person-time needed to complete the selected task."))
        self.txtMinCost.do_set_properties(
            width=100, tooltip=_("Minimim cost of the selected task."))
        self.txtExpCost.do_set_properties(
            width=100, tooltip=_("Most likely cost of the selected task."))
        self.txtMaxCost.do_set_properties(
            width=100, tooltip=_("Maximum cost of the selected task."))
        self.txtMeanTimeLL.do_set_properties(width=100, editable=False)
        self.txtMeanTime.do_set_properties(width=100, editable=False)
        self.txtMeanTimeUL.do_set_properties(width=100, editable=False)
        self.txtMeanCostLL.do_set_properties(width=100, editable=False)
        self.txtMeanCost.do_set_properties(width=100, editable=False)
        self.txtMeanCostUL.do_set_properties(width=100, editable=False)
        self.txtProjectTimeLL.do_set_properties(width=100, editable=False)
        self.txtProjectTime.do_set_properties(width=100, editable=False)
        self.txtProjectTimeUL.do_set_properties(width=100, editable=False)
        self.txtProjectCostLL.do_set_properties(width=100, editable=False)
        self.txtProjectCost.do_set_properties(width=100, editable=False)
        self.txtProjectCostUL.do_set_properties(width=100, editable=False)

        # ----- SPINBUTTONS
        self.spnStatus.do_set_properties(
            limits=[0, 0, 100, 1, 0.1],
            numeric=True,
            ticks=True,
            tooltip=_("Displays % complete of the selected V&amp;V activity."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtCode.do_update('', signal='changed')
        self.txtTask.do_update('', signal='changed')
        self.cmbTaskType.do_update(0, signal='changed')
        self.txtSpecification.do_update('', signal='changed')
        self.cmbMeasurementUnit.do_update(0, signal='changed')
        self.txtMinAcceptable.do_update('', signal='changed')
        self.txtMeanAcceptable.do_update('', signal='changed')
        self.txtMaxAcceptable.do_update('', signal='changed')
        self.txtVarAcceptable.do_update('', signal='changed')
        self.txtStartDate.do_update('', signal='changed')
        self.txtEndDate.do_update('', signal='changed')

        self.spnStatus.do_update(0.0, signal='changed')

        self.txtMinTime.do_update('', signal='changed')
        self.txtExpTime.do_update('', signal='changed')
        self.txtMaxTime.do_update('', signal='changed')
        self.txtMinCost.do_update('', signal='changed')
        self.txtExpCost.do_update('', signal='changed')
        self.txtMaxCost.do_update('', signal='changed')

        self.txtMeanTimeLL.do_update('', signal='changed')
        self.txtMeanTime.do_update('', signal='changed')
        self.txtMeanTimeUL.do_update('', signal='changed')
        self.txtMeanCostLL.do_update('', signal='changed')
        self.txtMeanCost.do_update('', signal='changed')
        self.txtMeanCostUL.do_update('', signal='changed')

    def _do_load_page(self, attributes: Dict[str, Any]) -> None:
        """
        Load the Validation General Data page.

        :param dict attributes: the Validation attributes to load into the Work
            View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['validation_id']

        _code = self.__do_make_task_code(attributes['task_type'])
        self.txtCode.do_update(_code)
        self.txtTask.do_update(attributes['description'], signal='changed')

        self.cmbTaskType.handler_block(
            self.cmbTaskType.dic_handler_id['changed'])
        _types = self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        _index = 1
        self.cmbTaskType.do_update(0, signal='changed')
        for _key, _type in _types.items():
            if _type[1] == attributes['task_type']:
                self.cmbTaskType.set_active(_index)
            else:
                _index += 1
        self.cmbTaskType.handler_unblock(
            self.cmbTaskType.dic_handler_id['changed'])

        self.txtSpecification.do_update(str(attributes['task_specification']),
                                        signal='changed')

        self.cmbMeasurementUnit.handler_block(
            self.cmbMeasurementUnit.dic_handler_id['changed'])
        _units = self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS
        self.cmbMeasurementUnit.do_update(0, signal='changed')
        for _key, _unit in _units.items():
            if _unit[1] == attributes['measurement_unit']:
                self.cmbMeasurementUnit.set_active(int(_key))
        self.cmbMeasurementUnit.handler_unblock(
            self.cmbMeasurementUnit.dic_handler_id['changed'])

        self.txtMinAcceptable.do_update(str(
            self.fmt.format(attributes['acceptable_minimum'])),
                                        signal='changed')
        self.txtMeanAcceptable.do_update(str(
            self.fmt.format(attributes['acceptable_mean'])),
                                         signal='changed')
        self.txtMaxAcceptable.do_update(str(
            self.fmt.format(attributes['acceptable_maximum'])),
                                        signal='changed')
        self.txtVarAcceptable.do_update(str(
            self.fmt.format(attributes['acceptable_variance'])),
                                        signal='changed')

        self.txtStartDate.do_update(attributes['date_start'], signal='changed')
        self.txtEndDate.do_update(attributes['date_end'], signal='changed')

        self.spnStatus.do_update(attributes['status'], signal='changed')

        self.txtMinTime.do_update(str(
            self.fmt.format(attributes['time_minimum'])),
                                  signal='changed')
        self.txtExpTime.do_update(str(
            self.fmt.format(attributes['time_average'])),
                                  signal='changed')
        self.txtMaxTime.do_update(str(
            self.fmt.format(attributes['time_maximum'])),
                                  signal='changed')
        self.txtMinCost.do_update(str(
            self.fmt.format(attributes['cost_minimum'])),
                                  signal='changed')
        self.txtExpCost.do_update(str(
            self.fmt.format(attributes['cost_average'])),
                                  signal='changed')
        self.txtMaxCost.do_update(str(
            self.fmt.format(attributes['cost_maximum'])),
                                  signal='changed')
        self.txtMeanTimeLL.do_update(
            str(self.fmt.format(attributes['time_ll'])))
        self.txtMeanTime.do_update(
            str(self.fmt.format(attributes['time_mean'])))
        self.txtMeanTimeUL.do_update(
            str(self.fmt.format(attributes['time_ul'])))
        self.txtMeanCostLL.do_update(
            str(self.fmt.format(attributes['cost_ll'])))
        self.txtMeanCost.do_update(
            str(self.fmt.format(attributes['cost_mean'])))
        self.txtMeanCostUL.do_update(
            str(self.fmt.format(attributes['cost_ul'])))

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """
        Request to calculate the selected validation task.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_validation_task',
                        task_id=self._record_id)

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_validation_tasks')

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected Validation.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_validation', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the Validations.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_validations')

    @staticmethod
    def _do_select_date(__button: Gtk.ToolButton, __event: Gdk.Event,
                        entry: RAMSTKEntry) -> None:
        """
        Select a date from a Calendar widget.

        This method launches a Calendar widget to allow the user to select a
        date.  The selected date (in ISO-8601 format) is set in the
        RAMSTKEntry() passed as an argument.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`ramstk.gui.gtk.Button.RAMSTKButton`
        :param __event: the button event that called this method.
        :type __event: :class:`Gdk.Event`
        :param entry: the RAMSTKEntry() to place the date in.
        :type entry: :class:`ramstk.gui.gtk.ramstk.Entry.RAMSTKEntry`
        :return: None
        :rtype: None
        """
        _calendar = RAMSTKDateSelect()

        _date = _calendar.do_run()
        entry.set_text(_date)

        _calendar.do_destroy()

    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None:
        """
        Handle changs made in Gtk.ComboBox() widgets.

        This method is called by:

            * RAMSTKComboBox() 'changed' signal

        This method sends the 'wvw_edited_validation' message.

        :param combo: the RAMSTKComboBox() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.Combo.RAMSTKComboBox`
        :param int index: the index in the handler ID list of the callback
            signal associated with the Gtk.ComboBox() that called this method.
        :return: None
        :rtype: None
        """
        #// TODO: Store Validation task type as integer not string
        #//
        #// This will make this field consistent with others that hold
        #// similar information.  Additionally, it will allow the use of the
        #// RAMSTKBaseView.on_combo_changed() method in the Validation
        #// workview.
        #//
        #// labels: type:enhancement, status:globalbacklog, module:validation
        _new_text = ''
        try:
            _key = self._dic_keys[self._lst_col_order[index]]
        except KeyError:
            _key = None

        combo.handler_block(combo.dic_handler_id['changed'])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if _key == 'task_type':
            _new_text = _model.get_value(_row, 0)
            _code = self.__do_make_task_code(_model.get_value(_row, 0))
            self.txtCode.set_text(_code)
        elif _key == 'measurement_unit':
            _new_text = _model.get_value(_row, 0)
        else:
            _new_text = ''

        pub.sendMessage('wvw_editing_validation',
                        node_id=[self._record_id, -1],
                        package={_key: _new_text})

        combo.handler_unblock(combo.dic_handler_id['changed'])

    # pylint: disable=unused-argument
    def _on_focus_out(self, entry: RAMSTKEntry, __event: Gdk.EventFocus,
                      index: int) -> None:
        """
        Handle changes made in RAMSTKEntry() and RAMSTKTextView() widgets.

        This method is called by:

            * RAMSTKEntry() 'focus-out-event' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvw_editing_validation' message.

        :param entry: the RAMSTKEntry() that called the method.
        :type entry: :class:`ramstk.views.gtk3.widgets.RAMSTKEntry`
        :param __event: the Gdk.EventFocus that triggered the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Validation class Gtk.TreeModel()
            associated with the data from the calling Gtk.Entry().
        :return: None
        :rtype: None
        """
        super().on_focus_out(entry, index, 'wvw_editing_validation')

    def _on_value_changed(self, spinbutton: Gtk.SpinButton,
                          __event: Gdk.EventFocus) -> None:
        """
        Handle changes made in Gtk.SpinButton() widgets.

        This method is called by:

            * Gtk.SpinButton() 'changed' signal

        This method sends the 'wvwEditedValidation' message.

        :param spinbutton: the Gtk.SpinButton() that called this method.
        :type spinbutton: :class:`Gtk.SpinButton`
        :param __event: the Gdk.EventFocus that triggered the signal.
        :type __event: :class:`Gdk.EventFocus`
        :return: None
        :rtype: None
        """
        spinbutton.handler_block(spinbutton.dic_handler_id['changed'])

        pub.sendMessage('wvw_editing_validation',
                        node_id=[self._record_id, -1],
                        package={'status': float(spinbutton.get_value())})

        spinbutton.handler_unblock(spinbutton.dic_handler_id['changed'])


class BurndownCurve(RAMSTKWorkView):
    """
    Display Validation task burndown curve in the RAMSTK Work Book.

    The Validation Burndown Curve displays the planned burndown curve (solid
    line) for all tasks in the V&V plan as well as the actual progress
    (points).  The attributes of a Validation Burndown Curve View are:

    :cvar str _module: the name of the module.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    :ivar int _record_id: the ID of the Validation task currently being
                              displayed.
    :ivar burndown: the RAMSTKPlot() widget to display the burndown curve of
                    program V&V task effort.
    """

    # Define private scalar class attributes.
    _module: str = 'validation'

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """
        Initialize the Work View for the Validation package.

        :param configuration: the RAMSTK configuration instance.
        :type configuration: :class:`ramstk.RAMSTK.Configuration`
        """
        super().__init__(configuration, logger)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.burndown: RAMSTKPlot = RAMSTKPlot()

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._do_load_page, 'succeed_calculate_plan')

        pub.subscribe(self.do_set_cursor_active,
                      'succeed_calculate_validation_plan')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_validation')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_validation')

    def __make_ui(self) -> None:
        """
        Make the Validation class Gtk.Notebook() burndown curve page.

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(Gtk.PolicyType.NEVER,
                                   Gtk.PolicyType.AUTOMATIC)
        _scrolledwindow.add_with_viewport(
            do_make_buttonbox(self,
                              icons=['chart'],
                              tooltips=[
                                  _("Plot the overall Validation program plan "
                                    "(i.e., all Validation tasks) and current "
                                    "status.")
                              ],
                              callbacks=[self._do_request_calculate_all]))
        self.pack_start(_scrolledwindow, False, False, 0)

        _frame = RAMSTKFrame()
        _frame.do_set_properties(title=_("Program Validation Effort"))
        _frame.add(self.burndown.plot)
        _frame.show_all()

        self.pack_start(_frame, True, True, 0)

        # Insert the tab.
        _label = RAMSTKLabel(
            _("<span weight='bold'>" + _("Program\nValidation\nProgress")
              + "</span>"))
        _label.do_set_properties(height=30,
                                 width=-1,
                                 justify=Gtk.Justification.CENTER,
                                 tooltip=_("Shows a plot of the total "
                                           "expected time to complete all "
                                           "V&amp;V tasks and the current "
                                           "progress."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __do_load_assessment_milestones(self, assessed: pd.DataFrame,
                                        y_max: float) -> None:
        """
        Adds the reliability assessment milestones to the plot.

        This method will add a vertical line at all the dates identified as
        dates when a reliability assessment is due.  Annotated along side
        these markers are the reliability targets (lower, mean, upper) for that
        assessment date.

        :return: None
        :rtype: None
        """
        _y_max = max(1.0, y_max)

        for _date in list(assessed.index):
            self.burndown.axis.axvline(x=_date,
                                       ymin=0,
                                       ymax=1.05 * _y_max,
                                       color='k',
                                       linewidth=1.0,
                                       linestyle='-.')
            self.burndown.axis.annotate(
                str(
                    self.fmt.format(
                        assessed.loc[pd.to_datetime(_date), 'upper'])) + "\n"
                + str(
                    self.fmt.format(
                        assessed.loc[pd.to_datetime(_date), 'mean'])) + "\n"
                + str(
                    self.fmt.format(
                        assessed.loc[pd.to_datetime(_date), 'lower'])),
                xy=(_date, 0.9 * _y_max),
                xycoords='data',
                xytext=(-55, 0),
                textcoords='offset points',
                size=12,
                va="center",
                bbox=dict(boxstyle="round", fc='#E5E5E5', ec='None',
                          alpha=0.5),
                arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                fc='#E5E5E5',
                                ec='None',
                                alpha=0.5,
                                patchA=None,
                                patchB=Ellipse((2, -1), 0.5, 0.5),
                                relpos=(0.2, 0.5)))

    def __do_load_plan(self, plan: pd.DataFrame) -> None:
        """
        Load the burndown plan.

        :param plan: the pandas DataFrame() containing the planned task end
            dates and remaining hours of work (lower, mean, upper).
        :return: None
        :rtype: None
        """
        self.burndown.axis.cla()
        self.burndown.axis.grid(True, which='both')

        self.burndown.do_load_plot(x_values=list(plan.index),
                                   y_values=list(plan.loc[:, 'lower']),
                                   plot_type='date',
                                   marker='g--')
        self.burndown.do_load_plot(x_values=list(plan.index),
                                   y_values=list(plan.loc[:, 'mean']),
                                   plot_type='date',
                                   marker='b-')
        self.burndown.do_load_plot(x_values=list(plan.index),
                                   y_values=list(plan.loc[:, 'upper']),
                                   plot_type='date',
                                   marker='r--')

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.burndown.axis.cla()
        self.burndown.figure.clf()
        self.burndown.plot.draw()

    def _do_load_page(self, plan: Dict[str, pd.DataFrame]) -> None:
        """
        Load the burndown curve with the planned and actual status.

        :param plan: a dict containing a pandas DataFrames() for each of
            planned burndown, assessment dates/targets, and the actual
            progress.
        :return: None
        """
        self.__do_load_plan(plan['plan'])
        self.__do_load_assessment_milestones(
            plan['assessed'], plan['plan'].loc[:, 'upper'].max())

        self.burndown.do_add_line(x_values=list(plan['actual'].index),
                                  y_values=list(plan['actual'].loc[:, 'time']),
                                  marker='o')

        self.burndown.do_make_title(_("Total Validation Effort"))
        self.burndown.do_make_labels(_("Total Time [hours]"),
                                     -0.5,
                                     0,
                                     set_x=False)
        # noinspection PyTypeChecker
        self.burndown.do_make_legend(
            (_("Maximum Expected Time"), _("Mean Expected Time"),
             _("Minimum Expected Time"), _("Actual Remaining Time")))
        self.burndown.figure.canvas.draw()

    @staticmethod
    def _do_request_calculate_all(__button: Gtk.ToolButton) -> None:
        """
        Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_plan')

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all Validation tasks and program results.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_validation', node_id=self._record_id)

    @staticmethod
    def _do_request_update_all(__button: Gtk.ToolButton) -> None:
        """
        Request to save all Validation tasks and program results.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_validations')
