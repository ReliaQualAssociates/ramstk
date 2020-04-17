# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Validation.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RASMTK Validation Work View."""

# Standard Library Imports
from datetime import datetime

# Third Party Imports
import numpy as np
from matplotlib.patches import Ellipse
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import (
    RAMSTKButton, RAMSTKComboBox, RAMSTKDateSelect, RAMSTKEntry,
    RAMSTKFrame, RAMSTKLabel, RAMSTKMessageDialog, RAMSTKPlot,
    RAMSTKScrolledWindow, RAMSTKTextView, do_make_label_group
)
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _

# RAMSTK Local Imports
from .WorkView import RAMSTKWorkView


class GeneralData(RAMSTKWorkView):
    """
    Display Validation attribute data in the RAMSTK Work Book.

    The Work View displays all the general data attributes for the selected
    Validation. The attributes of a Validation General Data Work View are:

    :ivar int _validation_id: the ID of the Validation task currently being
                              displayed.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTask - `changed`                       |
    +----------+-------------------------------------------+
    |     1    | cmbTaskType - `changed`                   |
    +----------+-------------------------------------------+
    |     2    | txtSpecification - `focus-out-event`      |
    +----------+-------------------------------------------+
    |     3    | cmbMeasurementUnit - `changed`            |
    +----------+-------------------------------------------+
    |     4    | txtMinAcceptable - `focus-out-event`      |
    +----------+-------------------------------------------+
    |     5    | txtMeanAcceptable - `focus-out-event`     |
    +----------+-------------------------------------------+
    |     6    | txtMaxAcceptable - `focus-out-event`      |
    +----------+-------------------------------------------+
    |     7    | txtVarAcceptable - `focus-out-event`      |
    +----------+-------------------------------------------+
    |     8    | txtStartDate - `changed`                  |
    +          +-------------------------------------------+
    |          | txtStartDate - `focus-out-event`          |
    +----------+-------------------------------------------+
    |     9    | txtEndDate - `changed`                    |
    +          +-------------------------------------------+
    |          | txtEndDate - `focus-out-event`            |
    +----------+-------------------------------------------+
    |    10    | spnStatus - `value-changed`               |
    +----------+-------------------------------------------+
    |    11    | txtMinTime - `focus-out-event`            |
    +----------+-------------------------------------------+
    |    12    | txtExpTime - `focus-out-event`            |
    +----------+-------------------------------------------+
    |    13    | txtMaxTime - `focus-out-event`            |
    +----------+-------------------------------------------+
    |    14    | txtMinCost - `focus-out-event`            |
    +----------+-------------------------------------------+
    |    15    | txtExpCost - `focus-out-event`            |
    +----------+-------------------------------------------+
    |    16    | txtMaxCost - `focus-out-event`            |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        [
            _("Task ID:"),
            _("Task Description:"),
            _("Task Type:"),
            _("Specification:"),
            _("Measurement Unit:"),
            _("Minimum Acceptable:"),
            _("Maximum Acceptable:"),
            _("Mean Acceptable:"),
            _("Variance:"),
        ],
        [
            _("Start Date:"),
            _("End Date:"),
            _("% Complete:"),
            _("Minimum Task Time:"),
            _("Most Likely Task Time:"),
            _("Maximum Task Time:"),
            _("Task Time (95% Confidence):"),
            _("Minimum Task Cost:"),
            _("Most Likely Task Cost:"),
            _("Maximum Task Cost:"),
            _("Task Cost (95% Confidence):"),
        ],
        [
            _("Project Time (95% Confidence):"),
            _("Project Cost (95% Confidence):"),
        ],
    ]

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Validation package.

        :param configuration: the RAMSTK configuration instance.
        :type configuration: :class:`ramstk.RAMSTK.Configuration`
        """
        RAMSTKWorkView.__init__(self, configuration, module='Validation')

        # Initialize private dictionary attributes.
        self._dic_icons['calculate-all'] = \
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/calculate-all.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnEndDate = RAMSTKButton(label="...")
        self.btnStartDate = RAMSTKButton(label="...")

        self.cmbTaskType = RAMSTKComboBox(simple=True)
        self.cmbMeasurementUnit = RAMSTKComboBox(simple=True)

        self.spnStatus = Gtk.SpinButton()

        self.txtID = RAMSTKEntry()
        self.txtMaxAcceptable = RAMSTKEntry()
        self.txtMeanAcceptable = RAMSTKEntry()
        self.txtMinAcceptable = RAMSTKEntry()
        self.txtVarAcceptable = RAMSTKEntry()
        self.txtSpecification = RAMSTKEntry()
        self.txtTask = RAMSTKTextView(Gtk.TextBuffer())
        self.txtEndDate = RAMSTKEntry()
        self.txtStartDate = RAMSTKEntry()
        self.txtMinTime = RAMSTKEntry()
        self.txtExpTime = RAMSTKEntry()
        self.txtMaxTime = RAMSTKEntry()
        self.txtMinCost = RAMSTKEntry()
        self.txtExpCost = RAMSTKEntry()
        self.txtMaxCost = RAMSTKEntry()
        self.txtMeanTimeLL = RAMSTKEntry()
        self.txtMeanTime = RAMSTKEntry()
        self.txtMeanTimeUL = RAMSTKEntry()
        self.txtMeanCostLL = RAMSTKEntry()
        self.txtMeanCost = RAMSTKEntry()
        self.txtMeanCostUL = RAMSTKEntry()
        self.txtProjectTimeLL = RAMSTKEntry()
        self.txtProjectTime = RAMSTKEntry()
        self.txtProjectTimeUL = RAMSTKEntry()
        self.txtProjectCostLL = RAMSTKEntry()
        self.txtProjectCost = RAMSTKEntry()
        self.txtProjectCostUL = RAMSTKEntry()

        self.__set_properties()
        self.__load_combobox()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._on_edit, 'mvw_editing_validation')
        pub.subscribe(self._do_load_page, 'selected_validation')

    def __load_combobox(self):
        """
        Load the RAMSTK ComboBox widgets with lists of information.

        :return: None
        :rtype: None
        """
        _model = self.cmbTaskType.get_model()
        _model.clear()

        _data = []
        for _key in self.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE:
            _data.append(
                [self.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE[_key][1]],
            )
        self.cmbTaskType.do_load_combo(_data)

        _model = self.cmbMeasurementUnit.get_model()
        _model.clear()

        _data = []
        for _key in self.RAMSTK_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS:
            _data.append(
                [self.RAMSTK_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS[_key][1]],
            )
        self.cmbMeasurementUnit.do_load_combo(_data)

    def __make_ui(self):
        """
        Make the Validation class Gtk.Notebook() general data page.

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrolledwindow.add_with_viewport(
            RAMSTKWorkView._make_buttonbox(
                self,
                icons=['calculate-all'],
                tooltips=[
                    _(
                        "Calculate the cost and time of the program (i.e., all "
                        "Validation tasks).",
                    ),
                ],
                callbacks=[self._do_request_calculate_all],
            ),
        )
        self.pack_start(_scrolledwindow, False, False, 0)

        _hbox = Gtk.HBox()

        _fixed = Gtk.Fixed()

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame(label=_("Task Description"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = do_make_label_group(
            self._lst_labels[0][:2],
            _fixed, 5, 5,
        )
        _x_pos += 50

        _hbox.pack_start(_frame, True, True, 0)

        _fixed.put(self.txtID, _x_pos, _y_pos[0])
        _fixed.put(self.txtTask.scrollwindow, _x_pos, _y_pos[1])

        _x_pos, _y_pos = do_make_label_group(
            self._lst_labels[0][2:],
            _fixed,
            5,
            _y_pos[1] + 110,
            y_inc=30,
        )
        _x_pos += 35

        _fixed.put(self.cmbTaskType, _x_pos, _y_pos[0])
        _fixed.put(self.txtSpecification, _x_pos, _y_pos[1])
        _fixed.put(self.cmbMeasurementUnit, _x_pos, _y_pos[2])
        _fixed.put(self.txtMinAcceptable, _x_pos, _y_pos[3])
        _fixed.put(self.txtMaxAcceptable, _x_pos, _y_pos[4])
        _fixed.put(self.txtMeanAcceptable, _x_pos, _y_pos[5])
        _fixed.put(self.txtVarAcceptable, _x_pos, _y_pos[6])

        _fixed.show_all()

        # Now add the right hand side starting with the top pane.
        _vpaned = Gtk.VPaned()
        _fixed = Gtk.Fixed()

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame(label=_("Task Effort"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = do_make_label_group(
            self._lst_labels[1],
            _fixed, 5, 5,
        )
        _x_pos += 50

        _vpaned.pack1(_frame, True, True)

        _fixed.put(self.btnEndDate, _x_pos + 105, _y_pos[1])
        _fixed.put(self.btnStartDate, _x_pos + 105, _y_pos[0])
        _fixed.put(self.txtStartDate, _x_pos, _y_pos[0])
        _fixed.put(self.txtEndDate, _x_pos, _y_pos[1])
        _fixed.put(self.spnStatus, _x_pos, _y_pos[2])
        _fixed.put(self.txtMinTime, _x_pos, _y_pos[3])
        _fixed.put(self.txtExpTime, _x_pos, _y_pos[4])
        _fixed.put(self.txtMaxTime, _x_pos, _y_pos[5])
        _fixed.put(self.txtMeanTimeLL, _x_pos, _y_pos[6])
        _fixed.put(self.txtMeanTime, _x_pos + 105, _y_pos[6])
        _fixed.put(self.txtMeanTimeUL, _x_pos + 210, _y_pos[6])
        _fixed.put(self.txtMinCost, _x_pos, _y_pos[7])
        _fixed.put(self.txtExpCost, _x_pos, _y_pos[8])
        _fixed.put(self.txtMaxCost, _x_pos, _y_pos[9])
        _fixed.put(self.txtMeanCostLL, _x_pos, _y_pos[10])
        _fixed.put(self.txtMeanCost, _x_pos + 105, _y_pos[10])
        _fixed.put(self.txtMeanCostUL, _x_pos + 210, _y_pos[10])

        _fixed.show_all()

        # Set the spin button to be a 0-100 in steps of 0.1 spinner.  Only
        # update if value is numeric and within range.
        self.spnStatus.set_adjustment(Gtk.Adjustment(0, 0, 100, 1, 0.1))
        self.spnStatus.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.spnStatus.set_numeric(True)
        self.spnStatus.set_snap_to_ticks(True)

        # Now add the bottom pane to the right side.
        _fixed = Gtk.Fixed()

        _scrollwindow = RAMSTKScrolledWindow(_fixed)
        _frame = RAMSTKFrame(label=_("Project Effort"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = do_make_label_group(
            self._lst_labels[2],
            _fixed, 5, 5,
        )
        _x_pos += 50

        _vpaned.pack2(_frame, True, True)

        _fixed.put(self.txtProjectTimeLL, _x_pos, _y_pos[0])
        _fixed.put(self.txtProjectTime, _x_pos + 105, _y_pos[0])
        _fixed.put(self.txtProjectTimeUL, _x_pos + 210, _y_pos[0])
        _fixed.put(self.txtProjectCostLL, _x_pos, _y_pos[1])
        _fixed.put(self.txtProjectCost, _x_pos + 105, _y_pos[1])
        _fixed.put(self.txtProjectCostUL, _x_pos + 210, _y_pos[1])

        _fixed.show_all()

        _hbox.pack_end(_vpaned, True, True, 0)

        self.pack_start(_hbox, True, True, 0)

        _label = RAMSTKLabel(
            _("General\nData"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays general information for the selected "
                "validation.",
            ),
        )
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback functions/methods for Validation widgets.

        :return: None
        :rtype: None
        """
        self.btnEndDate.connect(
            'button-release-event', self._do_select_date,
            self.txtEndDate,
        )
        self.btnStartDate.connect(
            'button-release-event', self._do_select_date,
            self.txtStartDate,
        )

        self._lst_handler_id.append(
            self.txtTask.do_get_buffer().connect(
                'changed', self._on_focus_out, 0,
            ),
        )
        self._lst_handler_id.append(
            self.cmbTaskType.connect('changed', self._on_combo_changed, 1),
        )
        self._lst_handler_id.append(
            self.txtSpecification.connect('changed', self._on_focus_out, 2),
        )
        self._lst_handler_id.append(
            self.cmbMeasurementUnit.connect(
                'changed', self._on_combo_changed,
                3,
            ),
        )
        self._lst_handler_id.append(
            self.txtMinAcceptable.connect(
                'focus-out-event',
                self._on_focus_out, 4,
            ),
        )
        self._lst_handler_id.append(
            self.txtMeanAcceptable.connect(
                'focus-out-event',
                self._on_focus_out, 5,
            ),
        )
        self._lst_handler_id.append(
            self.txtMaxAcceptable.connect(
                'focus-out-event',
                self._on_focus_out, 6,
            ),
        )
        self._lst_handler_id.append(
            self.txtVarAcceptable.connect(
                'focus-out-event',
                self._on_focus_out, 7,
            ),
        )
        self._lst_handler_id.append(
            self.txtStartDate.connect(
                'focus-out-event', self._on_focus_out,
                8,
            ),
        )
        self._lst_handler_id.append(
            self.txtEndDate.connect('focus-out-event', self._on_focus_out, 9),
        )
        self._lst_handler_id.append(
            self.spnStatus.connect(
                'focus-out-event', self._on_value_changed,
                10,
            ),
        )
        self._lst_handler_id.append(
            self.txtMinTime.connect('focus-out-event', self._on_focus_out, 11),
        )
        self._lst_handler_id.append(
            self.txtExpTime.connect('focus-out-event', self._on_focus_out, 12),
        )
        self._lst_handler_id.append(
            self.txtMaxTime.connect('focus-out-event', self._on_focus_out, 13),
        )
        self._lst_handler_id.append(
            self.txtMinCost.connect('focus-out-event', self._on_focus_out, 14),
        )
        self._lst_handler_id.append(
            self.txtExpCost.connect('focus-out-event', self._on_focus_out, 15),
        )
        self._lst_handler_id.append(
            self.txtMaxCost.connect('focus-out-event', self._on_focus_out, 16),
        )

    def __set_properties(self):
        """
        Set the properties of the Validation General Data RAMSTK widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        self.btnEndDate.do_set_properties(
            height=25,
            width=25,
            tooltip=_(
                "Launches the calendar to select the date the task was "
                "completed.",
            ),
        )
        self.btnStartDate.do_set_properties(
            height=25,
            width=25,
            tooltip=_(
                "Launches the calendar to select the date the task was "
                "started.",
            ),
        )

        # ----- COMBOBOXES
        self.cmbTaskType.do_set_properties(
            tooltip=_(
                "Selects and displays the type of task for the "
                "selected V&amp;V activity.",
            ),
        )
        self.cmbMeasurementUnit.do_set_properties(
            tooltip=_(
                "Selects and displays the measurement unit for the selected "
                "V&amp;V activity acceptance parameter.",
            ),
        )

        # ----- ENTRIES
        self.txtTask.do_set_properties(
            height=100,
            width=800,
            tooltip=_(
                "Displays the description of the selected V&amp;V activity.",
            ),
        )
        self.txtID.do_set_properties(
            width=50,
            editable=False,
            tooltip=_("Displays the ID of the selected V&amp;V activity."),
        )
        self.txtMaxAcceptable.do_set_properties(
            width=100,
            tooltip=_(
                "Displays the maximum acceptable value for the selected "
                "V&amp;V activity.",
            ),
        )
        self.txtMeanAcceptable.do_set_properties(
            width=100,
            tooltip=_(
                "Displays the mean acceptable value for the selected V&amp;V "
                "activity.",
            ),
        )
        self.txtMinAcceptable.do_set_properties(
            width=100,
            tooltip=_(
                "Displays the minimum acceptable value for the selected "
                "V&amp;V activity.",
            ),
        )
        self.txtVarAcceptable.do_set_properties(
            width=100,
            tooltip=_(
                "Displays the acceptable variance for the selected "
                "V&amp;V activity.",
            ),
        )
        self.txtSpecification.do_set_properties(
            tooltip=_(
                "Displays the internal or industry specification or procedure "
                "governing the selected V&amp;V activity.",
            ),
        )
        self.txtEndDate.do_set_properties(
            width=100,
            tooltip=_(
                "Displays the date the selected V&amp;V activity is "
                "scheduled to end.",
            ),
        )
        self.txtStartDate.do_set_properties(
            width=100,
            tooltip=_(
                "Displays the date the selected V&amp;V activity is "
                "scheduled to start.",
            ),
        )
        self.txtMinTime.do_set_properties(
            width=100,
            tooltip=_(
                "Minimum person-time needed to complete the selected task.",
            ),
        )
        self.txtExpTime.do_set_properties(
            width=100,
            tooltip=_(
                "Most likely person-time needed to complete the selected "
                "task.",
            ),
        )
        self.txtMaxTime.do_set_properties(
            width=100,
            tooltip=_(
                "Maximum person-time needed to complete the selected task.",
            ),
        )
        self.txtMinCost.do_set_properties(
            width=100, tooltip=_("Minimim cost of the selected task."),
        )
        self.txtExpCost.do_set_properties(
            width=100, tooltip=_("Most likely cost of the selected task."),
        )
        self.txtMaxCost.do_set_properties(
            width=100, tooltip=_("Maximum cost of the selected task."),
        )
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
        self.spnStatus.set_tooltip_text(
            _("Displays % complete of the selected V&amp;V activity."),
        )

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtID.set_text('')
        self.txtTask.do_update('', self._lst_handler_id[0])

        self.cmbTaskType.handler_block(self._lst_handler_id[1])
        self.cmbTaskType.set_active(0)
        self.cmbTaskType.handler_unblock(self._lst_handler_id[1])

        self.txtSpecification.do_update('', self._lst_handler_id[2])

        self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
        self.cmbMeasurementUnit.set_active(0)
        self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])

        self.txtMinAcceptable.do_update('', self._lst_handler_id[4])
        self.txtMeanAcceptable.do_update('', self._lst_handler_id[5])
        self.txtMaxAcceptable.do_update('', self._lst_handler_id[6])
        self.txtVarAcceptable.do_update('', self._lst_handler_id[7])
        self.txtStartDate.do_update('', self._lst_handler_id[8])
        self.txtEndDate.do_update('', self._lst_handler_id[9])

        self.spnStatus.handler_block(self._lst_handler_id[10])
        self.spnStatus.set_value(0.0)
        self.spnStatus.handler_unblock(self._lst_handler_id[10])

        self.txtMinTime.do_update('', self._lst_handler_id[11])
        self.txtExpTime.do_update('', self._lst_handler_id[12])
        self.txtMaxTime.do_update('', self._lst_handler_id[13])
        self.txtMinCost.do_update('', self._lst_handler_id[14])
        self.txtExpCost.do_update('', self._lst_handler_id[15])
        self.txtMaxCost.do_update('', self._lst_handler_id[16])

        self.txtMeanTimeLL.set_text('')
        self.txtMeanTime.set_text('')
        self.txtMeanTimeUL.set_text('')
        self.txtMeanCostLL.set_text('')
        self.txtMeanCost.set_text('')
        self.txtMeanCostUL.set_text('')

    def _do_load_page(self, attributes):
        """
        Load the Validation General Data page.

        :param dict attributes: a dict of attribute key:value pairs for the selected
                                Validation.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._validation_id = attributes['validation_id']

        _types = self.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        for _key, _type in _types.items():
            if _type[1] == attributes['task_type']:
                _name = '{0:s}-{1:04d}'.format(
                    _type[0],
                    int(self._validation_id),
                )
        RAMSTKWorkView.on_select(
            self,
            title=_("Analyzing Validation Task {0:s}").format(str(_name)),
        )

        self.txtID.set_text(str(attributes['validation_id']))

        self.txtTask.do_update(
            attributes['description'],
            self._lst_handler_id[0],
        )

        self.cmbTaskType.handler_block(self._lst_handler_id[1])
        _types = self.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        _index = 1
        self.cmbTaskType.set_active(0)
        for _key, _type in _types.items():
            if _type[1] == attributes['task_type']:
                self.cmbTaskType.set_active(_index)
            else:
                _index += 1
        self.cmbTaskType.handler_unblock(self._lst_handler_id[1])

        self.txtSpecification.do_update(
            str(attributes['task_specification']), self._lst_handler_id[2],
        )

        self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
        _units = self.RAMSTK_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS
        self.cmbMeasurementUnit.set_active(0)
        for _key, _unit in _units.items():
            if _unit[1] == attributes['measurement_unit']:
                self.cmbMeasurementUnit.set_active(int(_key))
        self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])

        self.txtMinAcceptable.do_update(
            str(self.fmt.format(attributes['acceptable_minimum'])),
            self._lst_handler_id[4],
        )
        self.txtMeanAcceptable.do_update(
            str(self.fmt.format(attributes['acceptable_mean'])),
            self._lst_handler_id[5],
        )
        self.txtMaxAcceptable.do_update(
            str(self.fmt.format(attributes['acceptable_maximum'])),
            self._lst_handler_id[6],
        )
        self.txtVarAcceptable.do_update(
            str(self.fmt.format(attributes['acceptable_variance'])),
            self._lst_handler_id[7],
        )
        try:
            _date_start = datetime.strftime(
                attributes['date_start'],
                '%Y-%m-%d',
            )
        except TypeError:
            _date_start = attributes['date_start']
        self.txtStartDate.do_update(_date_start, self._lst_handler_id[8])
        try:
            _date_end = datetime.strftime(attributes['date_end'], '%Y-%m-%d')
        except TypeError:
            _date_end = attributes['date_end']
        self.txtEndDate.do_update(_date_end, self._lst_handler_id[9])

        self.spnStatus.handler_block(self._lst_handler_id[10])
        self.spnStatus.set_value(attributes['status'])
        self.spnStatus.handler_unblock(self._lst_handler_id[10])

        self.txtMinTime.do_update(
            str(self.fmt.format(attributes['time_minimum'])),
            self._lst_handler_id[11],
        )
        self.txtExpTime.do_update(
            str(self.fmt.format(attributes['time_average'])),
            self._lst_handler_id[12],
        )
        self.txtMaxTime.do_update(
            str(self.fmt.format(attributes['time_maximum'])),
            self._lst_handler_id[13],
        )
        self.txtMinCost.do_update(
            str(self.fmt.format(attributes['cost_minimum'])),
            self._lst_handler_id[14],
        )
        self.txtExpCost.do_update(
            str(self.fmt.format(attributes['cost_average'])),
            self._lst_handler_id[15],
        )
        self.txtMaxCost.do_update(
            str(self.fmt.format(attributes['cost_maximum'])),
            self._lst_handler_id[16],
        )
        self.txtMeanTimeLL.set_text(
            str(self.fmt.format(attributes['time_ll'])),
        )
        self.txtMeanTime.set_text(
            str(self.fmt.format(attributes['time_mean'])),
        )
        self.txtMeanTimeUL.set_text(
            str(self.fmt.format(attributes['time_ul'])),
        )
        self.txtMeanCostLL.set_text(
            str(self.fmt.format(attributes['cost_ll'])),
        )
        self.txtMeanCost.set_text(
            str(self.fmt.format(attributes['cost_mean'])),
        )
        self.txtMeanCostUL.set_text(
            str(self.fmt.format(attributes['cost_ul'])),
        )

    def _do_request_calculate_all(self, __button):
        """
        Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_calculate_all_validations')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Validation.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_validation', node_id=self._validation_id,
        )
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Request to save all Validation tasks and program results.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_validations')
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    @staticmethod
    def _do_select_date(__button, __event, entry):
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

    def _on_combo_changed(self, combo, index):
        """
        Handle changs made in Gtk.ComboBox() widgets.

        This method is called by:

            * RAMSTKComboBox() 'changed' signal

        This method sends the 'wvw_edited_validation' message.

        :param combo: the RAMSTKComboBox() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.Combo.RAMSTKComboBox`
        :param int index: the index in the handler ID list of the callback
                          signal associated with the Gtk.ComboBox() that
                          called this method.
        :return: None
        :rtype: None
        """
        _dic_keys = {1: 'task_type', 3: 'measurement_unit'}
        try:
            _key = _dic_keys[self._lst_col_order[index]]
        except KeyError:
            _key = None

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if _key == 'task_type':
            _new_text = _model.get_value(_row, 0)

            # Update the Validation task name for the selected Validation task.
            _types = self.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE
            for _key, _type in _types.items():
                if _type[1] == _new_text:
                    _name = '{0:s}-{1:04d}'.format(
                        _type[0],
                        int(self._validation_id),
                    )

            # pub.sendMessage(
            #     'wvw_editing_requirement',
            #     module_id=self._validation_id,
            #     key='name',
            #     value=_name,
            # )

        elif _key == 'measurement_unit':
            _new_text = _model.get_value(_row, 0)
        else:
            _new_text = ''

        pub.sendMessage(
            'wvw_editing_validation',
            module_id=self._validation_id,
            key=_key,
            value=_new_text,
        )

        combo.handler_unblock(self._lst_handler_id[index])

    def _on_edit(self, module_id, key, value):  # pylint: disable=unused-argument
        """
        Update the Work View Gtk.Widgets() when Validation attributes change.

        This method updates the function Work View Gtk.Widgets() with changes
        to the Validation data model attributes.  This method is called
        whenever an attribute is edited in a different RAMSTK View.

        :param int module_id: the ID of the Validation being edited.  This
                              parameter is required to allow the PyPubSub
                              signals to call this method and the
                              request_set_attributes() method in the
                              RAMSTKDataController.
        :param str key: the key in the Validation attributes list of the
                        attribute that was edited.
        :param str value: the new text to update the Gtk.Widget() with.
        :return: None
        :rtype: None
        """
        _dic_switch = {
            'description': [self.txtTask.do_update, 0],
            'task_type': [self.cmbTaskType.do_update, 1],
            'task_specification': [self.txtSpecification.do_update, 2],
            'measurement_unit': [self.cmbMeasurementUnit.do_update, 3],
            'acceptable_minimum': [self.txtMinAcceptable, 4],
            'acceptable_mean': [self.txtMeanAcceptable, 5],
            'acceptable_maximum': [self.txtMaxAcceptable, 6],
            'acceptable_variance': [self.txtVarAcceptable.do_update, 7],
            'date_start': [self.txtStartDate.do_update, 8],
            'date_end': [self.txtEndDate.do_update, 9],
            'time_minimum': [self.txtMinTime.do_update, 11],
            'time_average': [self.txtExpTime.do_update, 12],
            'time_maximum': [self.txtMaxTime.do_update, 13],
            'cost_minimum': [self.txtMinCost.do_update, 14],
            'cost_average': [self.txtExpCost.do_update, 15],
            'cost_maximum': [self.txtMaxCost.do_update, 16],
        }

        if key == 'status':
            self.spnStatus.handler_block(self._lst_handler_id[10])
            self.spnStatus.set_value(value)
            self.spnStatus.handler_unblock(self._lst_handler_id[10])
        else:
            (_function, _id) = _dic_switch.get(key)
            _function(value, self._lst_handler_id[_id])

    def _on_focus_out(self, entry, index):
        """
        Handle changes made in RAMSTKEntry() and RAMSTKTextView() widgets.

        This method is called by:

            * RAMSTKEntry() 'focus-out-event' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvw_editing_validation' message.

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called this
                      method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.Entry`
        :param __event: the Gdk.EventFocus that triggerd the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Validation class Gtk.TreeModel()
                          associated with the data from the calling
                          RAMSTK widget.
        :return: None
        :rtype: None
        """
        _dic_keys = {
            0: 'description',
            2: 'specification',
            4: 'acceptable_minimum',
            5: 'acceptable_mean',
            6: 'acceptable_maximum',
            7: 'acceptable_variance',
            8: 'date_start',
            9: 'date_end',
            11: 'time_minimum',
            12: 'time_average',
            13: 'time_maximum',
            14: 'cost_minimum',
            15: 'cost_average',
            16: 'cost_maximum',
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        if index in [0, 2, 8, 9]:
            try:
                _new_text = str(entry.get_text())
            except ValueError:
                _new_text = ''
        else:
            try:
                _new_text = float(entry.get_text())
            except ValueError:
                _new_text = 0.0

        pub.sendMessage(
            'wvw_editing_validation',
            module_id=self._validation_id,
            key=_key,
            value=_new_text,
        )

        entry.handler_unblock(self._lst_handler_id[index])

    def _on_value_changed(self, spinbutton, __event, index):
        """
        Handle changes made in Gtk.SpinButton() widgets.

        This method is called by:

            * Gtk.SpinButton() 'changed' signal

        This method sends the 'wvwEditedValidation' message.

        :param spinbutton: the Gtk.SpinButton() that called this method.
        :type spinbutton: :class:`Gtk.SpinButton`
        :param __event: the Gdk.EventFocus that triggerd the signal.
        :type __event: :class:`Gdk.EventFocus`
        :param int index: the position in the Validation class attribute list
                          associated with the data from the calling
                          spinbutton.
        :return: None
        :rtype: None
        """
        spinbutton.handler_block(self._lst_handler_id[index])

        pub.sendMessage(
            'wvw_editing_validation',
            module_id=self._validation_id,
            key='status',
            value=float(spinbutton.get_value()),
        )

        spinbutton.handler_unblock(self._lst_handler_id[index])


class BurndownCurve(RAMSTKWorkView):
    """
    Display Validation task burndown curve in the RAMSTK Work Book.

    The Validation Burndown Curve displays the planned burndown curve (solid
    line) for all tasks in the V&V plan as well as the actual progress
    (points).  The attributes of a Validation Burndown Curve View are:

    :ivar int _validation_id: the ID of the Validation task currently being
                              displayed.
    :ivar burndown: the RAMSTKPlot() widget to display the burndown curve of
                    program V&V task effort.
    """

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Validation package.

        :param configuration: the RAMSTK configuration instance.
        :type configuration: :class:`ramstk.RAMSTK.Configuration`
        """
        RAMSTKWorkView.__init__(self, configuration, module='Validation')

        # Initialize private dictionary attributes.
        self._dic_icons['calculate-all'] = \
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/calculate-all.png'
        self._dic_icons['plot'] = \
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/charts.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.burndown = RAMSTKPlot()

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        #pub.subscribe(self._do_load_page, 'selected_validation')
        pub.subscribe(self._do_load_page, 'calculated_validation')

    def __make_ui(self):
        """
        Make the Validation class Gtk.Notebook() burndown curve page.

        :return: None
        :rtype: None
        """
        _scrolledwindow = Gtk.ScrolledWindow()
        _scrolledwindow.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrolledwindow.add_with_viewport(
            RAMSTKWorkView._make_buttonbox(
                self,
                icons=['calculate-all'],
                tooltips=[
                    _(
                        "Calculate the cost and time of the program (i.e., all "
                        "Validation tasks).",
                    ),
                ],
                callbacks=[self._do_request_calculate_all],
            ),
        )
        self.pack_start(_scrolledwindow, False, False, 0)

        _frame = RAMSTKFrame(label=_("Program Validation Effort"))
        _frame.add(self.burndown.plot)
        _frame.show_all()

        self.pack_start(_frame, True, True, 0)

        # Insert the tab.
        _label = RAMSTKLabel(
            _(
                "<span weight='bold'>" + _("Program\nValidation\nProgress") +
                "</span>",
            ),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Shows a plot of the total expected time to complete "
                "all V&amp;V tasks and the current progress.",
            ),
        )
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.burndown.axis.cla()
        self.burndown.figure.clf()
        self.burndown.plot.draw()

    def _do_load_page(self, attributes):
        """
        Load the actual burndown progress.

        :param dict attributes: a dict of attribute key:value pairs for the
                                Validation program status.
        :return: None
        :rtype: None
        """
        _y_minimum = attributes['y_minimum']
        _y_average = attributes['y_average']
        _y_maximum = attributes['y_maximum']
        _assessment_dates = attributes['assessment_dates']
        _targets = attributes['targets']
        _y_actual = attributes['y_actual']
        _y_actual = {
            _key: _value
            for _key, _value in _y_actual.items() if _value != 0
        }

        self.burndown.axis.cla()
        self.burndown.axis.grid(True, which='both')

        self._do_load_planned(attributes)

        # Add a vertical line at the scheduled end-date for each task
        # identified as a Reliability Assessment.  Add an annotation box
        # showing the minimum and maximum goal values for each milestone.
        if _assessment_dates:
            for __, _dates in enumerate(_assessment_dates):
                self.burndown.axis.axvline(
                    x=_dates,
                    ymin=0,
                    ymax=1.05 * list(_y_maximum.values())[0],
                    color='m',
                    linewidth=2.5,
                    linestyle=':',
                )

            for _index, _target in enumerate(_targets):
                self.burndown.axis.annotate(
                    str(self.fmt.format(_target[1])) + "\n" + str(
                        self.fmt.format(_target[0]),
                    ),
                    xy=(
                        _assessment_dates[_index],
                        0.95 * max(_y_maximum.values()),
                    ),
                    xycoords='data',
                    xytext=(-55, 0),
                    textcoords='offset points',
                    size=12,
                    va="center",
                    bbox=dict(
                        boxstyle="round", fc='#E5E5E5', ec='None', alpha=0.5,
                    ),
                    arrowprops=dict(
                        arrowstyle="wedge,tail_width=1.",
                        fc='#E5E5E5',
                        ec='None',
                        alpha=0.5,
                        patchA=None,
                        patchB=Ellipse((2, -1), 0.5, 0.5),
                        relpos=(0.2, 0.5),
                    ),
                )

        if _y_actual:
            self.burndown.do_add_line(
                x_values=list(_y_actual.keys()),
                y_values=list(_y_actual.values()),
                marker='o',
            )

        else:
            _prompt = _(
                "Actual program status information is not "
                "available.  You must calculate the program to make "
                "this information available for plotting.",
            )
            _dialog = RAMSTKMessageDialog(
                _prompt, self._dic_icons['important'], 'warning',
            )
            _response = _dialog.do_run()

            if _response == Gtk.ResponseType.OK:
                _dialog.do_destroy()

        self.burndown.do_make_title(_("Total Validation Effort"))
        self.burndown.do_make_labels(
            _("Total Time [hours]"), -0.5, 0, set_x=False,
        )
        _text = (
            _("Maximum Expected Time"), _("Mean Expected Time"),
            _("Minimum Expected Time"), _("Actual Remaining Time"),
        )
        self.burndown.do_make_legend(_text)
        self.burndown.figure.canvas.draw()

    def _do_load_planned(self, attributes):
        """
        Load the LCL, expected, and UCL planned burndown curves.

        :param dict attributes: a dict of attribute key:value pairs for the
                                Validation program status.
        :return: None
        :rtype: None
        """
        _y_minimum = attributes['y_minimum']
        _y_average = attributes['y_average']
        _y_maximum = attributes['y_maximum']

        _time_minimum = list(reversed(np.cumsum(list(_y_minimum.values()))))
        _time_average = list(reversed(np.cumsum(list(_y_average.values()))))
        _time_maximum = list(reversed(np.cumsum(list(_y_maximum.values()))))

        if _y_maximum:
            self.burndown.do_load_plot(
                x_values=list(_y_maximum.keys()),
                y_values=_time_maximum,
                plot_type='date',
                marker='r--',
            )
        if _y_average:
            self.burndown.do_load_plot(
                x_values=list(_y_average.keys()),
                y_values=_time_average,
                plot_type='date',
                marker='b-',
            )
        if _y_minimum:
            self.burndown.do_load_plot(
                x_values=list(_y_minimum.keys()),
                y_values=_time_minimum,
                plot_type='date',
                marker='g--',
            )

    def _do_request_calculate_all(self, __button):
        """
        Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_calculate_all_validations')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Request to save all Validation tasks and program results.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_validations')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)
