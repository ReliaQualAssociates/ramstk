# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.workviews.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Validation Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
import pandas as pd
import treelib
# noinspection PyPackageValidations,PyPackageRequirements
from matplotlib.patches import Ellipse
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
from pandas.plotting import register_matplotlib_converters
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton, RAMSTKComboBox, RAMSTKDateSelect, RAMSTKEntry, RAMSTKFrame,
    RAMSTKPanel, RAMSTKPlot, RAMSTKSpinButton, RAMSTKTextView, RAMSTKWorkView
)

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS

register_matplotlib_converters()


class TaskDescriptionPanel(RAMSTKPanel):
    """Panel to display general data about the selected Validation task."""
    def __init__(self) -> None:
        """Initialize an instance of the Validation Task Description panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS
        self._dic_task_types: Dict[int, List[str]] = {}
        self._dic_units: Dict[int, str] = {}

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Task ID:"),
            _("Task Code:"),
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
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Task Description")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.fmt: str = ''

        self.btnEndDate: RAMSTKButton = RAMSTKButton()
        self.btnStartDate: RAMSTKButton = RAMSTKButton()

        self.cmbTaskType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbMeasurementUnit: RAMSTKComboBox = RAMSTKComboBox()

        self.spnStatus: RAMSTKSpinButton = RAMSTKSpinButton()

        self.txtTaskID: RAMSTKEntry = RAMSTKEntry()
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtMaxAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtMinAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtVarAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()
        self.txtTask: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtEndDate: RAMSTKEntry = RAMSTKEntry()
        self.txtStartDate: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'description': [self.txtTask.do_update, 'changed', 0],
            'task_type': [self.cmbTaskType.do_update, 'changed', 1],
            'task_specification':
            [self.txtSpecification.do_update, 'changed', 2],
            'measurement_unit':
            [self.cmbMeasurementUnit.do_update, 'changed', 3],
            'acceptable_minimum': [self.txtMinAcceptable, 'changed', 4],
            'acceptable_mean': [self.txtMeanAcceptable, 'changed', 5],
            'acceptable_maximum': [self.txtMaxAcceptable, 'changed', 6],
            'acceptable_variance':
            [self.txtVarAcceptable.do_update, 'changed', 7],
            'date_start': [self.txtStartDate.do_update, 'changed', 8],
            'date_end': [self.txtEndDate.do_update, 'changed', 9],
            'status': [self.spnStatus.do_update, 'changed', 10],
        }

        self._lst_widgets = [
            self.txtTaskID,
            self.txtCode,
            self.txtTask,
            self.cmbTaskType,
            self.txtSpecification,
            self.cmbMeasurementUnit,
            self.txtMinAcceptable,
            self.txtMaxAcceptable,
            self.txtMeanAcceptable,
            self.txtVarAcceptable,
            self.txtStartDate,
            self.txtEndDate,
            self.spnStatus,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_validation')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_validation')

    def do_load_measurement_units(
            self, measurement_unit: Dict[int, Tuple[str, str]]) -> None:
        """Load the measurement units RAMSTKComboBox().

        :param measurement_unit: the list of measurement units to load.  The
            key is an integer representing the ID field in the database.  The
            value is a tuple with a unit abbreviation, unit name, and generic
            unit type.  For example:

            ('lbf', 'Pounds Force', 'unit')

        :return: None
        :rtype: None
        """
        _model = self.cmbMeasurementUnit.get_model()
        _model.clear()

        _units = []
        for _index, _key in enumerate(measurement_unit):
            self._dic_units[_index + 1] = measurement_unit[_key][1]
            _units.append([measurement_unit[_key][1]])
        self.cmbMeasurementUnit.do_load_combo(entries=_units)

    def do_load_validation_types(
            self, validation_type: Dict[int, Tuple[str, str]]) -> None:
        """Load the validation task types RAMSTKComboBox().

        :param validation_type: a dict of validation task types.  The key is an
            integer representing the ID field in the database.  The value is a
            tuple with a task code, task name, and generic task type.  For
            example:

            ('RAA', 'Reliability, Assessment', 'validation')

        :return: None
        :rtype: None
        """
        _model = self.cmbTaskType.get_model()
        _model.clear()

        _task_types = []
        for _index, _key in enumerate(validation_type):
            self._dic_task_types[_index + 1] = [
                validation_type[_key][0], validation_type[_key][1]
            ]
            _task_types.append([validation_type[_key][1]])
        self.cmbTaskType.do_load_combo(entries=_task_types)

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        self.cmbMeasurementUnit.do_update(0, signal='changed')
        self.cmbTaskType.do_update(0, signal='changed')

        self.txtCode.do_update('', signal='changed')
        self.txtTask.do_update('', signal='changed')
        self.txtSpecification.do_update('', signal='changed')
        self.txtMinAcceptable.do_update('', signal='changed')
        self.txtMeanAcceptable.do_update('', signal='changed')
        self.txtMaxAcceptable.do_update('', signal='changed')
        self.txtVarAcceptable.do_update('', signal='changed')
        self.txtStartDate.do_update('', signal='changed')
        self.txtEndDate.do_update('', signal='changed')

        self.spnStatus.do_update(0, signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Validation General Data page widgets.

        :param attributes: the Validation attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['validation_id']

        self.cmbTaskType.do_update(0, signal='changed')
        for _key, _type in self._dic_task_types.items():
            if _type[1] == attributes['task_type']:
                self.cmbTaskType.do_update(_key, signal='changed')

        self.cmbMeasurementUnit.do_update(0, signal='changed')
        for _key, _unit in self._dic_units.items():
            if _unit == attributes['measurement_unit']:
                self.cmbMeasurementUnit.do_update(_key, signal='changed')

        self.txtTaskID.do_update(attributes['validation_id'], signal='changed')
        self.txtCode.do_update(attributes['name'], signal='changed')
        self.txtTask.do_update(attributes['description'], signal='changed')
        self.txtSpecification.do_update(str(attributes['task_specification']),
                                        signal='changed')
        self.txtMinAcceptable.do_update(str(
            self.fmt.format(attributes['acceptable_minimum'])),
                                        signal='changed')  # noqa
        self.txtMeanAcceptable.do_update(str(
            self.fmt.format(attributes['acceptable_mean'])),
                                         signal='changed')  # noqa
        self.txtMaxAcceptable.do_update(str(
            self.fmt.format(attributes['acceptable_maximum'])),
                                        signal='changed')  # noqa
        self.txtVarAcceptable.do_update(str(
            self.fmt.format(attributes['acceptable_variance'])),
                                        signal='changed')  # noqa

        self.txtStartDate.do_update(attributes['date_start'], signal='changed')
        self.txtEndDate.do_update(attributes['date_end'], signal='changed')

        self.spnStatus.do_update(attributes['status'], signal='changed')

    def _do_make_task_code(self, combo: RAMSTKComboBox) -> None:
        """Create the validation task code.

        This method builds the task code based on the task type and the task
        ID.  The code created has the form:

            task type 3-letter abbreviation-task ID

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        :rtype: None
        """
        try:
            _index = combo.get_active()

            _task_type = self._dic_task_types[_index][0]
            _task_code = '{0:s}-{1:04d}'.format(_task_type,
                                                int(self._record_id))

            self.txtCode.do_update(str(_task_code), signal='changed')

            pub.sendMessage('wvw_editing_validation',
                            node_id=[self._record_id, -1, ''],
                            package={'name': _task_code})
        except (AttributeError, KeyError):
            pass

    @staticmethod
    def _do_select_date(__button: RAMSTKButton, __event: Gdk.Event,
                        entry: RAMSTKEntry) -> str:
        """Request to launch a date selection dialog.

        This method is used to select the validation date for the Validation.

        :param __button: the ramstk.RAMSTKButton() that called this method.
        :type __button: :class:`ramstk.gui.gtk.ramstk.RAMSTKButton`
        :param __event: the Gdk.Event() that called this method.
        :type __event: :class:`Gdk.Event`
        :param entry: the Gtk.Entry() that the new date should be displayed in.
        :type entry: :class:`Gtk.Entry`
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _dialog: RAMSTKDateSelect = RAMSTKDateSelect()

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.set_text(str(_date))

        return _date

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnEndDate.connect('button-release-event', self._do_select_date,
                                self.txtEndDate)
        self.btnStartDate.connect('button-release-event', self._do_select_date,
                                  self.txtStartDate)

        # ----- COMBOBOXES
        self.cmbMeasurementUnit.dic_handler_id[
            'changed'] = self.cmbMeasurementUnit.connect(
                'changed',
                super().on_changed_combo, 17, 'wvw_editing_validation')
        self.cmbTaskType.dic_handler_id['changed'] = self.cmbTaskType.connect(
            'changed',
            super().on_changed_combo, 21, 'wvw_editing_validation')
        self.cmbTaskType.connect('changed', self._do_make_task_code)

        # ----- ENTRIES
        _buffer: Gtk.TextBuffer = self.txtTask.do_get_buffer()
        self.txtTask.dic_handler_id['changed'] = _buffer.connect(
            'changed',
            super().on_changed_textview, 16, 'wvw_editing_validation',
            self.txtTask)
        self.txtSpecification.dic_handler_id[
            'changed'] = self.txtSpecification.connect(
                'changed',
                super().on_changed_entry, 20, 'wvw_editing_validation')
        self.txtMinAcceptable.dic_handler_id[
            'changed'] = self.txtMinAcceptable.connect(
                'changed',
                super().on_changed_entry, 4, 'wvw_editing_validation')
        self.txtMaxAcceptable.dic_handler_id[
            'changed'] = self.txtMaxAcceptable.connect(
                'changed',
                super().on_changed_entry, 2, 'wvw_editing_validation')
        self.txtMeanAcceptable.dic_handler_id[
            'changed'] = self.txtMeanAcceptable.connect(
                'changed',
                super().on_changed_entry, 3, 'wvw_editing_validation')
        self.txtVarAcceptable.dic_handler_id[
            'changed'] = self.txtVarAcceptable.connect(
                'changed',
                super().on_changed_entry, 5, 'wvw_editing_validation')
        self.txtStartDate.dic_handler_id[
            'changed'] = self.txtStartDate.connect('changed',
                                                   super().on_changed_entry,
                                                   15,
                                                   'wvw_editing_validation')
        self.txtEndDate.dic_handler_id['changed'] = self.txtEndDate.connect(
            'changed',
            super().on_changed_entry, 14, 'wvw_editing_validation')
        self.txtCode.dic_handler_id['changed'] = self.txtCode.connect(
            'changed',
            super().on_changed_entry, 18, 'wvw_editing_validation')

        # ----- SPINBUTTONS
        self.spnStatus.dic_handler_id['changed'] = self.spnStatus.connect(
            'value-changed',
            super().on_changed_entry, 19, 'wvw_editing_validation')

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

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

        # ----- SPINBUTTONS
        self.spnStatus.do_set_properties(
            limits=[0, 0, 100, 1, 0.1],
            numeric=True,
            ticks=True,
            tooltip=_("Displays % complete of the selected V&amp;V activity."))


class TaskEffortPanel(RAMSTKPanel):
    """Panel to display effort data about the selected Validation task."""
    def __init__(self) -> None:
        """Initialize an instance of the Validation Task Effort panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = ATTRIBUTE_KEYS

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Min. Task Time:"),
            _("Most Likely Task Time:"),
            _("Max. Task Time:"),
            _("Task Time (95% Confidence):"),
            _("Min. Task Cost:"),
            _("Most Likely Task Cost:"),
            _("Max. Task Cost:"),
            _("Task Cost (95% Confidence):"),
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Task Effort")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.fmt: str = ''

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

        self._dic_switch: Dict[str, Union[object, str]] = {
            'time_minimum': [self.txtMinTime.do_update, 'changed'],
            'time_average': [self.txtExpTime.do_update, 'changed'],
            'time_maximum': [self.txtMaxTime.do_update, 'changed'],
            'cost_minimum': [self.txtMinCost.do_update, 'changed'],
            'cost_average': [self.txtExpCost.do_update, 'changed'],
            'cost_maximum': [self.txtMaxCost.do_update, 'changed'],
        }

        self._lst_widgets = [
            self.txtMinTime,
            self.txtExpTime,
            self.txtMaxTime,
            self.txtMeanTimeLL,
            self.txtMinCost,
            self.txtExpCost,
            self.txtMaxCost,
            self.txtMeanCostLL,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_adjust_widgets()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.on_edit, 'mvw_editing_validation')

        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel, 'selected_validation')
        pub.subscribe(self._on_calculate_task,
                      'succeed_calculate_validation_task')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        self.txtMinTime.do_update('', signal='changed')
        self.txtExpTime.do_update('', signal='changed')
        self.txtMaxTime.do_update('', signal='changed')
        self.txtMinCost.do_update('', signal='changed')
        self.txtExpCost.do_update('', signal='changed')
        self.txtMaxCost.do_update('', signal='changed')

    def _do_load_code(self, task_code: int) -> None:
        """Load the Validation code RAMSTKEntry().

        :param task_code: the Validation code to load.
        :return: None
        :rtype: None
        """
        self.txtCode.do_update(str(task_code), signal='changed')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Validation General Data page widgets.

        :param attributes: the Validation attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['validation_id']

        self.txtMinTime.do_update(str('{0:0.2F}'.format(
            attributes['time_minimum'])),
                                  signal='changed')  # noqa
        self.txtExpTime.do_update(str('{0:0.2F}'.format(
            attributes['time_average'])),
                                  signal='changed')  # noqa
        self.txtMaxTime.do_update(str('{0:0.2F}'.format(
            attributes['time_maximum'])),
                                  signal='changed')  # noqa
        self.txtMinCost.do_update(str('${0:0.2F}'.format(
            attributes['cost_minimum'])),
                                  signal='changed')  # noqa
        self.txtExpCost.do_update(str('${0:0.2F}'.format(
            attributes['cost_average'])),
                                  signal='changed')  # noqa
        self.txtMaxCost.do_update(str('${0:0.2F}'.format(
            attributes['cost_maximum'])),
                                  signal='changed')  # noqa
        self.txtMeanTimeLL.do_update(
            str('{0:0.2F}'.format(attributes['time_ll'])))
        self.txtMeanTime.do_update(
            str('{0:0.2F}'.format(attributes['time_mean'])))
        self.txtMeanTimeUL.do_update(
            str('{0:0.2F}'.format(attributes['time_ul'])))
        self.txtMeanCostLL.do_update(
            str('${0:0.2F}'.format(attributes['cost_ll'])))
        self.txtMeanCost.do_update(
            str('${0:0.2F}'.format(attributes['cost_mean'])))
        self.txtMeanCostUL.do_update(
            str('${0:0.2F}'.format(attributes['cost_ul'])))

    def _do_make_task_code(self, task_type: str) -> str:
        """Create the validation task code.

        This method builds the task code based on the task type and the task
        ID.  The code created has the form:

            task type 3-letter abbreviation-task ID

        :param task_type: the three letter abbreviation for the task type.
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

    @staticmethod
    def _do_select_date(__button: RAMSTKButton, __event: Gdk.Event,
                        entry: RAMSTKEntry) -> str:
        """Request to launch a date selection dialog.

        This method is used to select the validation date for the Validation.

        :param __button: the ramstk.RAMSTKButton() that called this method.
        :type __button: :class:`ramstk.gui.gtk.ramstk.RAMSTKButton`
        :param __event: the Gdk.Event() that called this method.
        :type __event: :class:`Gdk.Event`
        :param entry: the Gtk.Entry() that the new date should be displayed in.
        :type entry: :class:`Gtk.Entry`
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _dialog: RAMSTKDateSelect = RAMSTKDateSelect()

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.set_text(str(_date))

        return _date

    def _on_calculate_task(self, tree: treelib.Tree) -> None:
        """Wrap _do_load_panel() on successful task calculation.

        :param tree: the validation treelib.Tree().
        :return: None
        :rtype: None
        """
        _attributes = tree.get_node(
            self._record_id).data['validation'].get_attributes()
        self._do_load_panel(_attributes)

    def __do_adjust_widgets(self) -> None:
        """Adjust position of some widgets.

        :return: None
        :rtype: None
        """
        _fixed: Gtk.Fixed = self.get_children()[0].get_children(
        )[0].get_children()[0]

        _time_entry: RAMSTKEntry = _fixed.get_children()[7]
        _cost_entry: RAMSTKEntry = _fixed.get_children()[-1]

        # We add the mean time and mean time UL to the same y position as
        # the mean time LL widget.
        _x_pos: int = _fixed.child_get_property(_time_entry, 'x')
        _y_pos: int = _fixed.child_get_property(_time_entry, 'y')
        _fixed.put(self.txtMeanTimeLL, _x_pos, _y_pos)
        _fixed.put(self.txtMeanTime, _x_pos + 175, _y_pos)
        _fixed.put(self.txtMeanTimeUL, _x_pos + 350, _y_pos)

        # We add the mean cost and mean cost UL to the same y position as
        # the mean cost LL widget.
        _x_pos = _fixed.child_get_property(_cost_entry, 'x')
        _y_pos = _fixed.child_get_property(_cost_entry, 'y')
        _fixed.put(self.txtMeanCostLL, _x_pos, _y_pos)
        _fixed.put(self.txtMeanCost, _x_pos + 195, _y_pos)
        _fixed.put(self.txtMeanCostUL, _x_pos + 390, _y_pos)

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the panel widgets.

        :return: None
        :rtype: None
        """
        self.txtMinTime.dic_handler_id['changed'] = self.txtMinTime.connect(
            'changed', self.on_changed_entry, 26, 'wvw_editing_validation')
        self.txtExpTime.dic_handler_id['changed'] = self.txtExpTime.connect(
            'changed', self.on_changed_entry, 22, 'wvw_editing_validation')
        self.txtMaxTime.dic_handler_id['changed'] = self.txtMaxTime.connect(
            'changed', self.on_changed_entry, 24, 'wvw_editing_validation')
        self.txtMinCost.dic_handler_id['changed'] = self.txtMinCost.connect(
            'changed', self.on_changed_entry, 11, 'wvw_editing_validation')
        self.txtExpCost.dic_handler_id['changed'] = self.txtExpCost.connect(
            'changed', self.on_changed_entry, 7, 'wvw_editing_validation')
        self.txtMaxCost.dic_handler_id['changed'] = self.txtMaxCost.connect(
            'changed', self.on_changed_entry, 9, 'wvw_editing_validation')

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

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


class ProgramEffortPanel(RAMSTKPanel):
    """Panel to display data about the selected Program (Revision) effort."""
    def __init__(self) -> None:
        """Initialize an instance of the Program Effort panel."""
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = [
            _("Program Time (95% Confidence):"),
            _("Program Cost (95% Confidence):"),
            "",
            "",
            "",
            "",
        ]

        # Initialize private scalar instance attributes.
        self._title: str = _("Verification Program Effort")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.fmt: str = ''

        self.txtProjectTimeLL: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectTime: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectTimeUL: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectCostLL: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectCost: RAMSTKEntry = RAMSTKEntry()
        self.txtProjectCostUL: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.txtProjectTime,
            self.txtProjectCost,
            self.txtProjectTimeLL,
            self.txtProjectTimeUL,
            self.txtProjectCostLL,
            self.txtProjectCostUL,
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_adjust_widgets()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel,
                      'succeed_get_program_status_attributes')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        self.txtProjectTimeLL.do_update('')
        self.txtProjectTime.do_update('')
        self.txtProjectTimeUL.do_update('')
        self.txtProjectCostLL.do_update('')
        self.txtProjectCost.do_update('')
        self.txtProjectCostUL.do_update('')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load data into the Validation General Data page widgets.

        :param attributes: the Validation attributes to load into the
            Work View widgets.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['validation_id']

        self.txtProjectTimeLL.do_update(str('{0:0.2F}'.format(
            attributes['time_ll'])),
                                        signal='changed')  # noqa
        self.txtProjectTime.do_update(str('{0:0.2F}'.format(
            attributes['time_mean'])),
                                      signal='changed')  # noqa
        self.txtProjectTimeUL.do_update(str('{0:0.2F}'.format(
            attributes['time_ul'])),
                                        signal='changed')  # noqa
        self.txtProjectCostLL.do_update(str('{0:0.2F}'.format(
            attributes['cost_ll'])),
                                        signal='changed')  # noqa
        self.txtProjectCost.do_update(str('{0:0.2F}'.format(
            attributes['cost_mean'])),
                                      signal='changed')  # noqa
        self.txtProjectCostUL.do_update(str('{0:0.2F}'.format(
            attributes['cost_ul'])),
                                        signal='changed')  # noqa

    def __do_adjust_widgets(self) -> None:
        """Adjust the position of some widgets.

        :return: None
        :rtype: None
        """
        _fixed: Gtk.Fixed = self.get_children()[0].get_children(
        )[0].get_children()[0]

        _time_entry: RAMSTKEntry = _fixed.get_children()[1]
        _cost_entry: RAMSTKEntry = _fixed.get_children()[3]

        # We add the project time and project time UL to the same y position
        # as the project time LL widget.
        _x_pos: int = _fixed.child_get_property(_time_entry, 'x')
        _y_pos: int = _fixed.child_get_property(_time_entry, 'y')
        _fixed.move(self.txtProjectTimeLL, _x_pos, _y_pos)
        _fixed.move(self.txtProjectTime, _x_pos + 175, _y_pos)
        _fixed.move(self.txtProjectTimeUL, _x_pos + 350, _y_pos)

        # We add the project cost and project cost UL to the same y position
        # as the project cost LL widget.
        _x_pos = _fixed.child_get_property(_cost_entry, 'x')
        _y_pos = _fixed.child_get_property(_cost_entry, 'y')
        _fixed.move(self.txtProjectCostLL, _x_pos, _y_pos)
        _fixed.move(self.txtProjectCost, _x_pos + 175, _y_pos)
        _fixed.move(self.txtProjectCostUL, _x_pos + 350, _y_pos)

    def __do_set_properties(self) -> None:
        """Set the properties of the panel widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(**{'bold': True, 'title': self._title})

        self.txtProjectTimeLL.do_set_properties(width=100, editable=False)
        self.txtProjectTime.do_set_properties(width=100, editable=False)
        self.txtProjectTimeUL.do_set_properties(width=100, editable=False)
        self.txtProjectCostLL.do_set_properties(width=100, editable=False)
        self.txtProjectCost.do_set_properties(width=100, editable=False)
        self.txtProjectCostUL.do_set_properties(width=100, editable=False)


class BurndownCurvePanel(RAMSTKPanel):
    """Panel to display the Verification plan efforts."""
    def __init__(self) -> None:
        """Initialize an instance of the Burndown Curve panel."""
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._title: str = _("Verification Plan Effort")

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a plot type panel.
        super().do_make_panel_plot()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'closed_program')
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel,
                      'succeed_calculate_verification_plan')

    def _do_clear_panel(self) -> None:
        """Clear the contents of the panel widgets.

        :return: None
        :rtype: None
        """
        self.pltPlot.axis.cla()
        self.pltPlot.figure.clf()
        self.pltPlot.plot.draw()

    def _do_load_panel(self, attributes: Dict[str, pd.DataFrame]) -> None:
        """Load the burndown curve with the planned and actual status.

        :param attributes: a dict containing a pandas DataFrames() for each of
            planned burndown, assessment dates/targets, and the actual
            progress.
        :return: None
        """
        self.__do_load_plan(attributes['plan'])
        self.__do_load_assessment_milestones(
            attributes['assessed'], attributes['plan'].loc[:, 'upper'].max())

        self.pltPlot.do_add_line(x_values=list(attributes['actual'].index),
                                 y_values=list(
                                     attributes['actual'].loc[:, 'time']),
                                 marker='o')

        self.pltPlot.do_make_title(_("Total Verification Effort"))
        self.pltPlot.do_make_labels(_("Total Time [hours]"),
                                    x_pos=-0.5,
                                    y_pos=0,
                                    set_x=False)
        # noinspection PyTypeChecker
        self.pltPlot.do_make_legend(
            (_("Minimum Expected Time"), _("Mean Expected Time"),
             _("Maximum Expected Time"), _("Actual Remaining Time")))
        self.pltPlot.figure.canvas.draw()

    def __do_load_assessment_milestones(self, assessed: pd.DataFrame,
                                        y_max: float) -> None:
        """Add the reliability assessment milestones to the plot.

        This method will add a vertical line at all the dates identified as
        dates when a reliability assessment is due.  Annotated along side
        these markers are the reliability targets (lower, mean, upper) for that
        assessment date.

        :return: None
        :rtype: None
        """
        _y_max = max(1.0, y_max)

        for _date in list(assessed.index):
            self.pltPlot.axis.axvline(x=_date,
                                      ymin=0,
                                      ymax=1.05 * _y_max,
                                      color='k',
                                      linewidth=1.0,
                                      linestyle='-.')
            self.pltPlot.axis.annotate(
                str(
                    self.fmt.format(assessed.loc[pd.to_datetime(_date),
                                                 'upper'])) + "\n"
                + str(
                    self.fmt.format(assessed.loc[pd.to_datetime(_date),
                                                 'mean'])) + "\n"
                + str(
                    self.fmt.format(assessed.loc[pd.to_datetime(_date),
                                                 'lower'])),
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
        """Load the verification plan burndown curve.

        :param plan: the pandas DataFrame() containing the planned task end
            dates and remaining hours of work (lower, mean, upper).
        :return: None
        :rtype: None
        """
        self.pltPlot.axis.cla()
        self.pltPlot.axis.grid(True, which='both')

        self.pltPlot.do_load_plot(
            **{
                'x_values': list(plan.index),
                'y_values': list(plan.loc[:, 'lower']),
                'plot_type': 'date',
                'marker': 'g--'
            })
        self.pltPlot.do_load_plot(
            **{
                'x_values': list(plan.index),
                'y_values': list(plan.loc[:, 'mean']),
                'plot_type': 'date',
                'marker': 'b-'
            })
        self.pltPlot.do_load_plot(
            **{
                'x_values': list(plan.index),
                'y_values': list(plan.loc[:, 'upper']),
                'plot_type': 'date',
                'marker': 'r--'
            })


class GeneralData(RAMSTKWorkView):
    """Display general Validation attribute data in the RAMSTK Work Book.

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
    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'validation'
    _tablabel: str = _("General\nData")
    _tabtooltip: str = _(
        "Displays general information for the selected Verification task.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Validation Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate,
            self._do_request_calculate_all,
            super().do_request_update,
            super().do_request_update_all,
        ]
        self._lst_icons = ['calculate', 'calculate_all', 'save', 'save-all']
        self._lst_mnu_labels = [
            _("Calculate Task"),
            _("Calculate Program"),
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _("Calculate the expected cost and time of the selected "
              "Validation task."),
            _("Calculate the cost and time of the program (i.e., all "
              "Validation tasks)."),
            _("Save changes to the selected Validation task."),
            _("Save changes to all Validation tasks."),
        ]

        # Initialize private scalar attributes.
        self._pnlTaskDescription: RAMSTKPanel = TaskDescriptionPanel()
        self._pnlTaskEffort: RAMSTKPanel = TaskEffortPanel()
        self._pnlProgramEffort: RAMSTKPanel = ProgramEffortPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_cursor_active,
                      'succeed_calculate_validation_task')
        pub.subscribe(super().do_set_cursor_active_on_fail,
                      'fail_calculate_validation_task')

        pub.subscribe(self._do_set_record_id, 'selected_validation')

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate the selected validation task.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            'request_calculate_validation_task',
            node_id=self._record_id,
        )

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_validation_tasks', )

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Verification task record ID.

        :param attributes: the attributes dict for the selected Validation
            task.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['validation_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Validation General Data tab.

        :return: None
        :rtype: None
        """
        _hpaned, _vpaned_right = super().do_make_layout_lrr()

        self._pnlTaskDescription.fmt = self.fmt
        self._pnlTaskDescription.do_load_measurement_units(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS)
        self._pnlTaskDescription.do_load_validation_types(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE)
        _hpaned.pack1(self._pnlTaskDescription, True, True)

        self._pnlTaskEffort.fmt = self.fmt
        self._pnlProgramEffort.fmt = self.fmt
        _vpaned_right.pack1(self._pnlTaskEffort, True, True)
        _vpaned_right.pack2(self._pnlProgramEffort, True, True)

        self.show_all()


class BurndownCurve(RAMSTKWorkView):
    """Display Verification task burn down curve in the RAMSTK Work Book.

    The Verification burn down Curve displays the planned burn down curve (
    solid line) for all tasks in the V&V plan as well as the actual progress
    (points).  The attributes of a Verification burn down curve view are:

    :cvar _module: the name of the module.

    :ivar _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """
    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module = 'validation'
    _tablabel = "<span weight='bold'>" + _(
        "Program\nVerification\nProgress") + "</span>"
    _tabtooltip = _(
        "Shows a plot of the total expected time to complete all verification "
        "tasks and the current progress on those tasks.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Work View for the Verification package.

        :param configuration: the RAMSTK configuration instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate_all,
        ]
        self._lst_icons = [
            'chart',
        ]
        self._lst_mnu_labels = [_("Plot Verification Effort")]
        self._lst_tooltips = [
            _("Plot the overall Verification program plan (i.e., "
              "all Verification tasks) and current status."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = BurndownCurvePanel()

        self._title: str = _("Program Verification Effort")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pltPlot: RAMSTKPlot = RAMSTKPlot()

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, 'selected_validation')

        pub.subscribe(self._do_set_cursor_active,
                      'succeed_calculate_verification_plan')

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_calculate_plan', )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _do_set_cursor_active(self, attributes: Dict[str, Any]) -> None:
        """Wrap do_set_cursor_active() of the meta-class.

        This method is called whenever the verification plan is calculated
        successfully.  That PyPubSub MDS includes an attributes data package
        (which is a dict containing the data to plot).  This method is
        needed since the meta-class do_set_cursor_active() method is
        expecting a treelib.Tree() in the MDS.

        :param attributes: the attributes dict for the selected Validation
            task.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_active()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Verification task record ID.

        :param attributes: the attributes dict for the selected Validation
            task.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['validation_id']

    def __make_ui(self) -> None:
        """Build the user interface for the Verification Status tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        _frame: RAMSTKFrame = RAMSTKFrame()
        _frame.do_set_properties(**{'title': _("Program Verification Effort")})
        _frame.add(self._pnlPanel)

        self.pack_end(_frame, True, True, 0)
        self.show_all()
