# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Validation.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RASMTK Validation Work View."""

from datetime import datetime

import numpy as np
from pubsub import pub
from matplotlib.patches import Ellipse

# Import other RAMSTK modules.
from ramstk.Utilities import ordinal_to_date
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, Gdk, Gtk
from .WorkView import RAMSTKWorkView


class GeneralData(RAMSTKWorkView):
    """
    Display Validation attribute data in the RAMSTK Work Book.

    The Work View displays all the general data attributes for the selected
    Validation. The attributes of a Validation General Data Work View are:

    :ivar int _validation_id: the ID of the Validation currently being
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

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Validation package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Validation')

        # Initialize private dictionary attributes.
        self._dic_icons['calculate-all'] = \
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/calculate-all.png'

        # Initialize private list attributes.
        self._lst_gendata_labels = [[
            _("Task ID:"),
            _("Task Description:"),
            _("Task Type:"),
            _("Specification:"),
            _("Measurement Unit:"),
            _("Minimum Acceptable:"),
            _("Maximum Acceptable:"),
            _("Mean Acceptable:"),
            _("Variance:")
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
                                        _("Task Cost (95% Confidence):")
                                    ],
                                    [
                                        _("Project Time (95% Confidence):"),
                                        _("Project Cost (95% Confidence):")
                                    ]]

        # Initialize private scalar attributes.
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnEndDate = ramstk.RAMSTKButton(height=25, width=25, label="...")
        self.btnStartDate = ramstk.RAMSTKButton(
            height=25, width=25, label="...")
        self.btnEndDate.set_tooltip_text(
            _("Launches the calendar to select the date the task was "
              "completed."))
        self.btnStartDate.set_tooltip_text(
            _("Launches the calendar to select the date the task was started.")
        )

        self.cmbTaskType = ramstk.RAMSTKComboBox(
            tooltip=_("Selects and displays the type of task for the "
                      "selected V&amp;V activity."))
        self.cmbMeasurementUnit = ramstk.RAMSTKComboBox(
            tooltip=_(
                "Selects and displays the measurement unit for the selected "
                "V&amp;V activity acceptance parameter."))

        self.spnStatus = Gtk.SpinButton()
        self.spnStatus.set_tooltip_text(
            _("Displays % complete of the selected V&amp;V activity."))

        self.txtID = ramstk.RAMSTKEntry(
            width=50,
            editable=False,
            tooltip=_("Displays the ID of the selected V&amp;V activity."))
        self.txtMaxAcceptable = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_("Displays the maximum acceptable value for the selected "
                      "V&amp;V activity."))
        self.txtMeanAcceptable = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_(
                "Displays the mean acceptable value for the selected V&amp;V "
                "activity."))
        self.txtMinAcceptable = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_("Displays the minimum acceptable value for the selected "
                      "V&amp;V activity."))
        self.txtVarAcceptable = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_("Displays the acceptable variance for the selected "
                      "V&amp;V activity."))
        self.txtSpecification = ramstk.RAMSTKEntry(
            tooltip=_(
                "Displays the internal or industry specification or procedure "
                "governing the selected V&amp;V activity."))
        self.txtTask = ramstk.RAMSTKTextView(
            Gtk.TextBuffer(),
            width=600,
            tooltip=_(
                "Displays the description of the selected V&amp;V activity."))
        self.txtEndDate = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_("Displays the date the selected V&amp;V activity is "
                      "scheduled to end."))
        self.txtStartDate = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_("Displays the date the selected V&amp;V activity is "
                      "scheduled to start."))
        self.txtMinTime = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_(
                "Minimum person-time needed to complete the selected task."))
        self.txtExpTime = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_(
                "Most likely person-time needed to complete the selected "
                "task."))
        self.txtMaxTime = ramstk.RAMSTKEntry(
            width=100,
            tooltip=_(
                "Maximum person-time needed to complete the selected task."))
        self.txtMinCost = ramstk.RAMSTKEntry(
            width=100, tooltip=_("Minimim cost of the selected task."))
        self.txtExpCost = ramstk.RAMSTKEntry(
            width=100, tooltip=_("Most likely cost of the selected task."))
        self.txtMaxCost = ramstk.RAMSTKEntry(
            width=100, tooltip=_("Maximum cost of the selected task."))
        self.txtMeanTimeLL = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtMeanTime = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtMeanTimeUL = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtMeanCostLL = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtMeanCost = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtMeanCostUL = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtProjectTimeLL = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtProjectTime = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtProjectTimeUL = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtProjectCostLL = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtProjectCost = ramstk.RAMSTKEntry(width=100, editable=False)
        self.txtProjectCostUL = ramstk.RAMSTKEntry(width=100, editable=False)

        # Connect to callback methods for editable widgets.
        self.btnEndDate.connect('button-release-event', self._do_select_date,
                                self.txtEndDate)
        self.btnStartDate.connect('button-release-event', self._do_select_date,
                                  self.txtStartDate)

        self._lst_handler_id.append(self.txtTask.do_get_buffer().connect(
            'changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.cmbTaskType.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.txtSpecification.connect('changed', self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.cmbMeasurementUnit.connect('changed', self._on_combo_changed,
                                            3))
        self._lst_handler_id.append(
            self.txtMinAcceptable.connect('focus-out-event',
                                          self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtMeanAcceptable.connect('focus-out-event',
                                           self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtMaxAcceptable.connect('focus-out-event',
                                          self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtVarAcceptable.connect('focus-out-event',
                                          self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtStartDate.connect('focus-out-event', self._on_focus_out,
                                      8))
        self._lst_handler_id.append(
            self.txtEndDate.connect('focus-out-event', self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.spnStatus.connect('focus-out-event', self._on_value_changed,
                                   10))
        self._lst_handler_id.append(
            self.txtMinTime.connect('focus-out-event', self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtExpTime.connect('focus-out-event', self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtMaxTime.connect('focus-out-event', self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtMinCost.connect('focus-out-event', self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtExpCost.connect('focus-out-event', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtMaxCost.connect('focus-out-event', self._on_focus_out, 16))

        self.__make_ui()

        self.txtCode.hide()
        self.txtName.hide()
        self.txtRemarks.scrollwindow.hide()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        pub.subscribe(self._on_edit, 'mvw_editing_validation')
        pub.subscribe(self._do_load_page, 'selected_validation')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the Gtk.ButtonBox() for the Validation class Work View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Validation class Work
                 View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _("Calculate the cost and time of the program (i.e., all "
              "Validation tasks).")
        ]
        _callbacks = [self._do_request_calculate_all]
        _icons = ['calculate-all']

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def __make_ui(self):
        """
        Make the Validation class Gtk.Notebook() general data page.

        :return: None
        :rtype: None
        """
        # Load the Gtk.ComboBox() widgets.
        _model = self.cmbTaskType.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE:
            _data.append([
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.
                RAMSTK_VALIDATION_TYPE[_key][1]
            ])
        self.cmbTaskType.do_load_combo(_data)

        _model = self.cmbMeasurementUnit.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS:
            _data.append([
                self._mdcRAMSTK.RAMSTK_CONFIGURATION.
                RAMSTK_MEASUREMENT_UNITS[_key][1]
            ])
        self.cmbMeasurementUnit.do_load_combo(_data)

        # Build the General Data page starting with the left half.
        _hbox = Gtk.HBox()

        _fixed = Gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_("Task Description"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(
            self._lst_gendata_labels[0][:2], _fixed, 5, 5)
        _x_pos += 50

        _hbox.pack_start(_frame, True, True, 0)

        _fixed.put(self.txtID, _x_pos, _y_pos[0])
        _fixed.put(self.txtTask.scrollwindow, _x_pos, _y_pos[1])

        _x_pos, _y_pos = ramstk.make_label_group(
            self._lst_gendata_labels[0][2:],
            _fixed,
            5,
            _y_pos[1] + 110,
            y_inc=30)
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

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_("Task Effort"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_gendata_labels[1],
                                                 _fixed, 5, 5)
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

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_("Project Effort"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_gendata_labels[2],
                                                 _fixed, 5, 5)
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

        _label = ramstk.RAMSTKLabel(
            _("General\nData"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays general information for the selected "
                      "validation."))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.pack_start(self.__make_buttonbox(), False, False, 0)
        self.pack_start(_hbox, True, True, 0)
        self.show_all()

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtID.set_text('')

        _buffer = self.txtTask.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[0])
        _buffer.set_text('')
        _buffer.handler_unblock(self._lst_handler_id[0])

        self.cmbTaskType.handler_block(self._lst_handler_id[1])
        self.cmbTaskType.set_active(0)
        self.cmbTaskType.handler_unblock(self._lst_handler_id[1])

        self.txtSpecification.handler_block(self._lst_handler_id[2])
        self.txtSpecification.set_text('')
        self.txtSpecification.handler_unblock(self._lst_handler_id[2])

        self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
        self.cmbMeasurementUnit.set_active(0)
        self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])

        self.txtMinAcceptable.handler_block(self._lst_handler_id[4])
        self.txtMinAcceptable.set_text('')
        self.txtMinAcceptable.handler_unblock(self._lst_handler_id[4])

        self.txtMeanAcceptable.handler_block(self._lst_handler_id[5])
        self.txtMeanAcceptable.set_text('')
        self.txtMeanAcceptable.handler_unblock(self._lst_handler_id[5])

        self.txtMaxAcceptable.handler_block(self._lst_handler_id[6])
        self.txtMaxAcceptable.set_text('')
        self.txtMaxAcceptable.handler_unblock(self._lst_handler_id[6])

        self.txtVarAcceptable.handler_block(self._lst_handler_id[7])
        self.txtVarAcceptable.set_text('')
        self.txtVarAcceptable.handler_unblock(self._lst_handler_id[7])

        self.txtStartDate.handler_block(self._lst_handler_id[8])
        self.txtStartDate.set_text('')
        self.txtStartDate.handler_unblock(self._lst_handler_id[8])

        self.txtEndDate.handler_block(self._lst_handler_id[9])
        self.txtEndDate.set_text('')
        self.txtEndDate.handler_unblock(self._lst_handler_id[9])

        self.spnStatus.handler_block(self._lst_handler_id[10])
        self.spnStatus.set_value(0.0)
        self.spnStatus.handler_unblock(self._lst_handler_id[10])

        self.txtMinTime.handler_block(self._lst_handler_id[11])
        self.txtMinTime.set_text('')
        self.txtMinTime.handler_unblock(self._lst_handler_id[11])

        self.txtExpTime.handler_block(self._lst_handler_id[12])
        self.txtExpTime.set_text('')
        self.txtExpTime.handler_unblock(self._lst_handler_id[12])

        self.txtMaxTime.handler_block(self._lst_handler_id[13])
        self.txtMaxTime.set_text('')
        self.txtMaxTime.handler_unblock(self._lst_handler_id[13])

        self.txtMinCost.handler_block(self._lst_handler_id[14])
        self.txtMinCost.set_text('')
        self.txtMinCost.handler_unblock(self._lst_handler_id[14])

        self.txtExpCost.handler_block(self._lst_handler_id[15])
        self.txtExpCost.set_text('')
        self.txtExpCost.handler_unblock(self._lst_handler_id[15])

        self.txtMaxCost.handler_block(self._lst_handler_id[16])
        self.txtMaxCost.set_text('')
        self.txtMaxCost.handler_unblock(self._lst_handler_id[16])

        self.txtMeanTimeLL.set_text('')
        self.txtMeanTime.set_text('')
        self.txtMeanTimeUL.set_text('')
        self.txtMeanCostLL.set_text('')
        self.txtMeanCost.set_text('')
        self.txtMeanCostUL.set_text('')

    def _do_load_page(self, attributes):
        """
        Load the Validation General Data page.

        :param tuple attributes: a dict of attribute key:value pairs for
                                 the selected Validation.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']
        self._validation_id = attributes['validation_id']

        _types = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        for _key, _type in _types.items():
            if _type[1] == attributes['task_type']:
                _name = '{0:s}-{1:04d}'.format(_type[0],
                                               int(self._validation_id))
        RAMSTKWorkView.on_select(
            self,
            title=_("Analyzing Validation Task {0:s}").format(str(_name)))

        self.txtID.set_text(str(attributes['validation_id']))

        _buffer = self.txtTask.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[0])
        _buffer.set_text(attributes['description'])
        _buffer.handler_unblock(self._lst_handler_id[0])

        self.cmbTaskType.handler_block(self._lst_handler_id[1])
        _types = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        _index = 1
        self.cmbTaskType.set_active(0)
        for _key, _type in _types.items():
            if _type[1] == attributes['task_type']:
                self.cmbTaskType.set_active(_index)
            else:
                _index += 1
        self.cmbTaskType.handler_unblock(self._lst_handler_id[1])

        self.txtSpecification.handler_block(self._lst_handler_id[2])
        self.txtSpecification.set_text(str(attributes['task_specification']))
        self.txtSpecification.handler_unblock(self._lst_handler_id[2])

        self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
        _units = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS
        self.cmbMeasurementUnit.set_active(0)
        for _key, _unit in _units.items():
            if _unit[1] == attributes['measurement_unit']:
                self.cmbMeasurementUnit.set_active(int(_key))
        self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])

        self.txtMinAcceptable.handler_block(self._lst_handler_id[4])
        self.txtMinAcceptable.set_text(
            str(self.fmt.format(attributes['acceptable_minimum'])))
        self.txtMinAcceptable.handler_unblock(self._lst_handler_id[4])

        self.txtMeanAcceptable.handler_block(self._lst_handler_id[5])
        self.txtMeanAcceptable.set_text(
            str(self.fmt.format(attributes['acceptable_mean'])))
        self.txtMeanAcceptable.handler_unblock(self._lst_handler_id[5])

        self.txtMaxAcceptable.handler_block(self._lst_handler_id[6])
        self.txtMaxAcceptable.set_text(
            str(self.fmt.format(attributes['acceptable_maximum'])))
        self.txtMaxAcceptable.handler_unblock(self._lst_handler_id[6])

        self.txtVarAcceptable.handler_block(self._lst_handler_id[7])
        self.txtVarAcceptable.set_text(
            str(self.fmt.format(attributes['acceptable_variance'])))
        self.txtVarAcceptable.handler_unblock(self._lst_handler_id[7])

        self.txtStartDate.handler_block(self._lst_handler_id[8])
        try:
            _date_start = datetime.strftime(attributes['date_start'],
                                            '%Y-%m-%d')
        except TypeError:
            _date_start = attributes['date_start']
        self.txtStartDate.set_text(_date_start)
        self.txtStartDate.handler_unblock(self._lst_handler_id[8])

        self.txtEndDate.handler_block(self._lst_handler_id[9])
        try:
            _date_end = datetime.strftime(attributes['date_end'], '%Y-%m-%d')
        except TypeError:
            _date_end = attributes['date_end']
        self.txtEndDate.set_text(_date_end)
        self.txtEndDate.handler_unblock(self._lst_handler_id[9])

        self.spnStatus.handler_block(self._lst_handler_id[10])
        self.spnStatus.set_value(attributes['status'])
        self.spnStatus.handler_unblock(self._lst_handler_id[10])

        self.txtMinTime.handler_block(self._lst_handler_id[11])
        self.txtMinTime.set_text(
            str(self.fmt.format(attributes['time_minimum'])))
        self.txtMinTime.handler_unblock(self._lst_handler_id[11])

        self.txtExpTime.handler_block(self._lst_handler_id[12])
        self.txtExpTime.set_text(
            str(self.fmt.format(attributes['time_average'])))
        self.txtExpTime.handler_unblock(self._lst_handler_id[12])

        self.txtMaxTime.handler_block(self._lst_handler_id[13])
        self.txtMaxTime.set_text(
            str(self.fmt.format(attributes['time_maximum'])))
        self.txtMaxTime.handler_unblock(self._lst_handler_id[13])

        self.txtMinCost.handler_block(self._lst_handler_id[14])
        self.txtMinCost.set_text(
            str(self.fmt.format(attributes['cost_minimum'])))
        self.txtMinCost.handler_unblock(self._lst_handler_id[14])

        self.txtExpCost.handler_block(self._lst_handler_id[15])
        self.txtExpCost.set_text(
            str(self.fmt.format(attributes['cost_average'])))
        self.txtExpCost.handler_unblock(self._lst_handler_id[15])

        self.txtMaxCost.handler_block(self._lst_handler_id[16])
        self.txtMaxCost.set_text(
            str(self.fmt.format(attributes['cost_maximum'])))
        self.txtMaxCost.handler_unblock(self._lst_handler_id[16])

        self.txtMeanTimeLL.set_text(
            str(self.fmt.format(attributes['time_ll'])))
        self.txtMeanTime.set_text(
            str(self.fmt.format(attributes['time_mean'])))
        self.txtMeanTimeUL.set_text(
            str(self.fmt.format(attributes['time_ul'])))
        self.txtMeanCostLL.set_text(
            str(self.fmt.format(attributes['cost_ll'])))
        self.txtMeanCost.set_text(
            str(self.fmt.format(attributes['cost_mean'])))
        self.txtMeanCostUL.set_text(
            str(self.fmt.format(attributes['cost_ul'])))

    def _do_request_calculate_all(self, __button):
        """
        Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_calculate_all_validations')
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Validation.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage(
            'request_update_validation', node_id=self._validation_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

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
        date.  The selected date (in ISO-8601 format) is set in the RAMSTKEntry()
        passed as an argument.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`ramstk.gui.gtk.Button.RAMSTKButton`
        :param __event: the button event that called this method.
        :type __event: :class:`Gdk.Event`
        :param entry: the RAMSTKEntry() to place the date in.
        :type entry: :class:`ramstk.gui.gtk.ramstk.Entry.RAMSTKEntry`
        :return: None
        :rtype: None
        """
        _calendar = ramstk.RAMSTKDateSelect()

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
            _types = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE
            for _key, _type in _types.items():
                if _type[1] == _new_text:
                    _name = '{0:s}-{1:04d}'.format(_type[0],
                                                   int(self._validation_id))

            pub.sendMessage(
                'wvw_editing_requirement',
                module_id=self._validation_id,
                key='name',
                value=_name)

        elif _key == 'measurement_unit':
            _new_text = _model.get_value(_row, 0)
        else:
            _new_text = ''

        pub.sendMessage(
            'wvw_editing_validation',
            module_id=self._validation_id,
            key=_key,
            value=_new_text)

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
        if key == 'description':
            _buffer = self.txtTask.do_get_buffer()
            _buffer.handler_block(self._lst_handler_id[0])
            _buffer.set_text(str(value))
            _buffer.handler_unblock(self._lst_handler_id[0])
        elif key == 'task_type':
            self.cmbTaskType.handler_block(self._lst_handler_id[1])
            _types = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_VALIDATION_TYPE
            self.cmbTaskType.set_active(0)
            for _key, _type in _types.items():
                if _type[1] == value:
                    self.cmbTaskType.set_active(int(_key))
            self.cmbTaskType.handler_unblock(self._lst_handler_id[1])
        elif key == 'specification':
            self.txtSpecification.handler_block(self._lst_handler_id[2])
            self.txtSpecification.set_text(str(value))
            self.txtSpecification.handler_unblock(self._lst_handler_id[2])
        elif key == 'measurement_unit':
            self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
            _units = self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS
            self.cmbMeasurementUnit.set_active(0)
            for _key, _unit in _units.items():
                if _unit[1] == value:
                    self.cmbMeasurementUnit.set_active(int(_key))
            self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])
        elif key == 'acceptable_minimum':
            self.txtMinAcceptable.handler_block(self._lst_handler_id[4])
            self.txtMinAcceptable.set_text(str(value))
            self.txtMinAcceptable.handler_unblock(self._lst_handler_id[4])
        elif key == 'acceptable_mean':
            self.txtMeanAcceptable.handler_block(self._lst_handler_id[5])
            self.txtMeanAcceptable.set_text(str(value))
            self.txtMeanAcceptable.handler_unblock(self._lst_handler_id[5])
        elif key == 'acceptable_maximum':
            self.txtMaxAcceptable.handler_block(self._lst_handler_id[6])
            self.txtMaxAcceptable.set_text(str(value))
            self.txtMaxAcceptable.handler_unblock(self._lst_handler_id[6])
        elif key == 'acceptable_variance':
            self.txtVarAcceptable.handler_block(self._lst_handler_id[7])
            self.txtVarAcceptable.set_text(str(value))
            self.txtVarAcceptable.handler_unblock(self._lst_handler_id[7])
        elif key == 'date_start':
            self.txtStartDate.handler_block(self._lst_handler_id[8])
            self.txtStartDate.set_text(str(ordinal_to_date(value)))
            self.txtStartDate.handler_unblock(self._lst_handler_id[8])
        elif key == 'date_end':
            self.txtEndDate.handler_block(self._lst_handler_id[9])
            self.txtEndDate.set_text(str(ordinal_to_date(value)))
            self.txtEndDate.handler_unblock(self._lst_handler_id[9])
        elif key == 'status':
            self.spnStatus.handler_block(self._lst_handler_id[10])
            self.spnStatus.set_value(value)
            self.spnStatus.handler_unblock(self._lst_handler_id[10])
        elif key == 'time_minimum':
            self.txtMinTime.handler_block(self._lst_handler_id[11])
            self.txtMinTime.set_text(str(value))
            self.txtMinTime.handler_unblock(self._lst_handler_id[11])
        elif key == 'time_average':
            self.txtExpTime.handler_block(self._lst_handler_id[12])
            self.txtExpTime.set_text(str(value))
            self.txtExpTime.handler_unblock(self._lst_handler_id[12])
        elif key == 'time_maximum':
            self.txtMaxTime.handler_block(self._lst_handler_id[13])
            self.txtMaxTime.set_text(str(value))
            self.txtMaxTime.handler_unblock(self._lst_handler_id[13])
        elif key == 'cost_minimum':
            self.txtMinCost.handler_block(self._lst_handler_id[14])
            self.txtMinCost.set_text(str(value))
            self.txtMinCost.handler_unblock(self._lst_handler_id[14])
        elif key == 'time_average':
            self.txtExpCost.handler_block(self._lst_handler_id[15])
            self.txtExpCost.set_text(str(value))
            self.txtExpCost.handler_unblock(self._lst_handler_id[15])
        elif key == 'time_maximum':
            self.txtMaxCost.handler_block(self._lst_handler_id[16])
            self.txtMaxCost.set_text(str(value))
            self.txtMaxCost.handler_unblock(self._lst_handler_id[16])

    def _on_focus_out(self, entry, __event, index):
        """
        Handle changes made in RAMSTKEntry() and RAMSTKTextView() widgets.

        This method is called by:

            * RAMSTKEntry() 'focus-out' signal
            * RAMSTKTextView() 'changed' signal

        This method sends the 'wvw_edited_validation' message.

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
            16: 'cost_maximum'
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
            value=_new_text)

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
            value=float(spinbutton.get_value()))

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

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Validation package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Validation')

        # Initialize private dictionary attributes.
        self._dic_icons['calculate-all'] = \
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/calculate-all.png'
        self._dic_icons['plot'] = \
            controller.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/charts.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.burndown = ramstk.RAMSTKPlot()

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, 'closed_program')
        #pub.subscribe(self._do_load_page, 'selected_validation')
        pub.subscribe(self._do_load_page, 'calculated_validation')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the Gtk.ButtonBox() for the Validation class Work View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Validation class Work
                 View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _("Calculate the cost and time of the program (i.e., all "
              "Validation tasks).")
        ]
        _callbacks = [self._do_request_calculate_all]
        _icons = ['calculate-all']

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def __make_ui(self):
        """
        Make the Validation class Gtk.Notebook() burndown curve page.

        :return: None
        :rtype: None
        """
        _frame = ramstk.RAMSTKFrame(label=_("Program Validation Effort"))
        _frame.add(self.burndown.plot)
        _frame.show_all()

        # Insert the tab.
        self.hbx_tab_label = Gtk.Label()
        self.hbx_tab_label.set_markup("<span weight='bold'>" +
                                      _("Program\nValidation\nProgress") +
                                      "</span>")
        self.hbx_tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.hbx_tab_label.set_justify(Gtk.Justification.CENTER)
        self.hbx_tab_label.show_all()
        self.hbx_tab_label.set_tooltip_text(
            _("Shows a plot of the total expected time "
              "to complete all V&amp;V tasks and the "
              "current progress."))

        self.pack_start(self.__make_buttonbox(), False, False, 0)
        self.pack_start(_frame, True, True, 0)
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

        _time_minimum = list(reversed(np.cumsum(list(_y_minimum.values()))))
        _time_average = list(reversed(np.cumsum(list(_y_average.values()))))
        _time_maximum = list(reversed(np.cumsum(list(_y_maximum.values()))))

        # Plot the maximum, mean, and minimum expected burndown curves.
        if _y_maximum:
            self.burndown.do_load_plot(
                x_values=list(_y_maximum.keys()),
                y_values=_time_maximum,
                plot_type='date',
                marker='r--')
        if _y_average:
            self.burndown.do_load_plot(
                x_values=list(_y_average.keys()),
                y_values=_time_average,
                plot_type='date',
                marker='b-')
        if _y_minimum:
            self.burndown.do_load_plot(
                x_values=list(_y_minimum.keys()),
                y_values=_time_minimum,
                plot_type='date',
                marker='g--')

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
                    linestyle=':')

            for _index, _target in enumerate(_targets):
                self.burndown.axis.annotate(
                    str(self.fmt.format(_target[1])) + "\n" + str(
                        self.fmt.format(_target[0])),
                    xy=(_assessment_dates[_index],
                        0.95 * max(_y_maximum.values())),
                    xycoords='data',
                    xytext=(-55, 0),
                    textcoords='offset points',
                    size=12,
                    va="center",
                    bbox=dict(
                        boxstyle="round", fc='#E5E5E5', ec='None', alpha=0.5),
                    arrowprops=dict(
                        arrowstyle="wedge,tail_width=1.",
                        fc='#E5E5E5',
                        ec='None',
                        alpha=0.5,
                        patchA=None,
                        patchB=Ellipse((2, -1), 0.5, 0.5),
                        relpos=(0.2, 0.5)))

        if _y_actual:
            self.burndown.do_add_line(
                x_values=list(_y_actual.keys()),
                y_values=list(_y_actual.values()),
                marker='o')

        else:
            _prompt = _("Actual program status information is not "
                        "available.  You must calculate the program to make "
                        "this information available for plotting.")
            _dialog = ramstk.RAMSTKMessageDialog(
                _prompt, self._dic_icons['important'], 'warning')
            _response = _dialog.do_run()

            if _response == Gtk.ResponseType.OK:
                _dialog.do_destroy()

        self.burndown.do_make_title(_("Total Validation Effort"))
        self.burndown.do_make_labels(
            _("Total Time [hours]"), -0.5, 0, set_x=False)
        _text = (_("Maximum Expected Time"), _("Mean Expected Time"),
                 _("Minimum Expected Time"), _("Actual Remaining Time"))
        self.burndown.do_make_legend(_text)
        self.burndown.figure.canvas.draw()

    def _do_request_calculate_all(self, __button):
        """
        Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_calculate_all_validations')
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

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
