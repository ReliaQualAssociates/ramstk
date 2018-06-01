# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Validation.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Validation Work View."""

from datetime import datetime

import numpy as np
from pubsub import pub
from matplotlib.patches import Ellipse

# Import other RTK modules.
from rtk.Utilities import ordinal_to_date
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from .WorkView import RTKWorkView


class GeneralData(RTKWorkView):
    """
    Display Validation attribute data in the RTK Work Book.

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

    def __init__(self, controller):
        """
        Initialize the Work View for the Validation package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Validation')

        # Initialize private dictionary attributes.
        self._dic_icons['calculate-all'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/calculate-all.png'

        # Initialize private list attributes.
        self._lst_gendata_labels = [[
            _(u"Task ID:"),
            _(u"Task Description:"),
            _(u"Task Type:"),
            _(u"Specification:"),
            _(u"Measurement Unit:"),
            _(u"Minimum Acceptable:"),
            _(u"Maximum Acceptable:"),
            _(u"Mean Acceptable:"),
            _(u"Variance:")
        ], [
            _(u"Start Date:"),
            _(u"End Date:"),
            _(u"% Complete:"),
            _(u"Minimum Task Time:"),
            _(u"Most Likely Task Time:"),
            _(u"Maximum Task Time:"),
            _(u"Task Time (95% Confidence):"),
            _(u"Minimum Task Cost:"),
            _(u"Most Likely Task Cost:"),
            _(u"Maximum Task Cost:"),
            _(u"Task Cost (95% Confidence):")
        ], [
            _(u"Project Time (95% Confidence):"),
            _(u"Project Cost (95% Confidence):")
        ]]

        # Initialize private scalar attributes.
        self._revision_id = None
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # General data page widgets.
        self.btnEndDate = rtk.RTKButton(height=25, width=25, label="...")
        self.btnStartDate = rtk.RTKButton(height=25, width=25, label="...")
        self.btnEndDate.set_tooltip_text(
            _(u"Launches the calendar to select the date the task was "
              u"completed."))
        self.btnStartDate.set_tooltip_text(
            _(u"Launches the calendar to select the date the task was started."
              ))

        self.cmbTaskType = rtk.RTKComboBox(
            tooltip=
            _(u"Selects and displays the type of task for the selected V&amp;V "
              u"activity."))
        self.cmbMeasurementUnit = rtk.RTKComboBox(
            tooltip=_(
                u"Selects and displays the measurement unit for the selected "
                u"V&amp;V activity acceptance parameter."))

        self.spnStatus = gtk.SpinButton()
        self.spnStatus.set_tooltip_text(
            _(u"Displays % complete of the selected V&amp;V activity."))

        self.txtID = rtk.RTKEntry(
            width=50,
            editable=False,
            tooltip=_(u"Displays the ID of the selected V&amp;V activity."))
        self.txtMaxAcceptable = rtk.RTKEntry(
            width=100,
            tooltip=_(
                u"Displays the maximum acceptable value for the selected "
                u"V&amp;V activity."))
        self.txtMeanAcceptable = rtk.RTKEntry(
            width=100,
            tooltip=_(
                u"Displays the mean acceptable value for the selected V&amp;V "
                u"activity."))
        self.txtMinAcceptable = rtk.RTKEntry(
            width=100,
            tooltip=_(
                u"Displays the minimum acceptable value for the selected "
                u"V&amp;V activity."))
        self.txtVarAcceptable = rtk.RTKEntry(
            width=100,
            tooltip=_(u"Displays the acceptable variance for the selected "
                      u"V&amp;V activity."))
        self.txtSpecification = rtk.RTKEntry(
            tooltip=_(
                u"Displays the internal or industry specification or procedure "
                u"governing the selected V&amp;V activity."))
        self.txtTask = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=600,
            tooltip=_(
                u"Displays the description of the selected V&amp;V activity."))
        self.txtEndDate = rtk.RTKEntry(
            width=100,
            tooltip=_(u"Displays the date the selected V&amp;V activity is "
                      u"scheduled to end."))
        self.txtStartDate = rtk.RTKEntry(
            width=100,
            tooltip=_(u"Displays the date the selected V&amp;V activity is "
                      u"scheduled to start."))
        self.txtMinTime = rtk.RTKEntry(
            width=100,
            tooltip=_(
                u"Minimum person-time needed to complete the selected task."))
        self.txtExpTime = rtk.RTKEntry(
            width=100,
            tooltip=_(
                u"Most likely person-time needed to complete the selected "
                u"task."))
        self.txtMaxTime = rtk.RTKEntry(
            width=100,
            tooltip=_(
                u"Maximum person-time needed to complete the selected task."))
        self.txtMinCost = rtk.RTKEntry(
            width=100, tooltip=_(u"Minimim cost of the selected task."))
        self.txtExpCost = rtk.RTKEntry(
            width=100, tooltip=_(u"Most likely cost of the selected task."))
        self.txtMaxCost = rtk.RTKEntry(
            width=100, tooltip=_(u"Maximum cost of the selected task."))
        self.txtMeanTimeLL = rtk.RTKEntry(width=100, editable=False)
        self.txtMeanTime = rtk.RTKEntry(width=100, editable=False)
        self.txtMeanTimeUL = rtk.RTKEntry(width=100, editable=False)
        self.txtMeanCostLL = rtk.RTKEntry(width=100, editable=False)
        self.txtMeanCost = rtk.RTKEntry(width=100, editable=False)
        self.txtMeanCostUL = rtk.RTKEntry(width=100, editable=False)
        self.txtProjectTimeLL = rtk.RTKEntry(width=100, editable=False)
        self.txtProjectTime = rtk.RTKEntry(width=100, editable=False)
        self.txtProjectTimeUL = rtk.RTKEntry(width=100, editable=False)
        self.txtProjectCostLL = rtk.RTKEntry(width=100, editable=False)
        self.txtProjectCost = rtk.RTKEntry(width=100, editable=False)
        self.txtProjectCostUL = rtk.RTKEntry(width=100, editable=False)

        # Connect to callback methods for editable widgets.
        self.btnEndDate.connect('button-release-event', self._do_select_date,
                                self.txtEndDate)
        self.btnStartDate.connect('button-release-event', self._do_select_date,
                                  self.txtStartDate)

        self._lst_handler_id.append(self.txtTask.do_get_buffer().connect(
            'changed', self._on_focus_out, None, 0))
        self._lst_handler_id.append(
            self.cmbTaskType.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.txtSpecification.connect('focus-out-event',
                                          self._on_focus_out, 2))
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
        self.txtStartDate.connect('changed', self._on_focus_out, None, 8)
        self._lst_handler_id.append(
            self.txtStartDate.connect('focus-out-event', self._on_focus_out,
                                      8))
        self.txtEndDate.connect('changed', self._on_focus_out, None, 9)
        self._lst_handler_id.append(
            self.txtEndDate.connect('focus-out-event', self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.spnStatus.connect('value-changed', self._on_value_changed,
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

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(self._make_general_data_page(), expand=True, fill=True)
        self.show_all()

        self.txtCode.hide()
        self.txtName.hide()
        self.txtRemarks.scrollwindow.hide()

        pub.subscribe(self._do_set_revision, 'selectedRevision')
        pub.subscribe(self._on_select, 'selectedValidation')
        pub.subscribe(self._on_select, 'calculatedValidation')
        pub.subscribe(self._on_edit, 'mvwEditedValidation')

    def _do_request_calculate(self, __button):
        """
        Request to calculate the selected Validation task.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _error_code = 0
        _msg = ''

        if self._dtc_data_controller.request_calculate(self._validation_id):
            _error_code = 1
            _msg = 'Error calculating Validation activity cost and time.'

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to calculate "
                        u"Validation {0:d}. \n\n\t" + _msg + "\n\n").format(
                            self._validation_id)
            _error_dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True
        else:
            pub.sendMessage(
                'calculatedValidation', module_id=self._validation_id)

        return _return

    def _do_request_calculate_program(self, __button):
        """
        Request to calculate program cost and time.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        (_cost_ll, _cost_mean, _cost_ul, _time_ll, _time_mean,
         _time_ul) = self._dtc_data_controller.request_calculate_program()

        self.txtProjectCostLL.set_text(str(self.fmt.format(_cost_ll)))
        self.txtProjectCost.set_text(str(self.fmt.format(_cost_mean)))
        self.txtProjectCostUL.set_text(str(self.fmt.format(_cost_ul)))
        self.txtProjectTimeLL.set_text(str(self.fmt.format(_time_ll)))
        self.txtProjectTime.set_text(str(self.fmt.format(_time_mean)))
        self.txtProjectTimeUL.set_text(str(self.fmt.format(_time_ul)))

        return _return

    def _do_request_update(self, __button):
        """
        Request to save the currently selected Validation.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update(self._validation_id)

    def _do_request_update_all(self, __button):
        """
        Request to save all Validation tasks and program results.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = self._dtc_data_controller.request_update_all()

        if not _return:
            _return = self._dtc_data_controller.request_update_status()

        return _return

    @staticmethod
    def _do_select_date(__button, __event, entry):
        """
        Select a date from a Calendar widget.

        This method launches a Calendar widget to allow the user to select a
        date.  The selected date (in ISO-8601 format) is set in the RTKEntry()
        passed as an argument.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`rtk.gui.gtk.Button.RTKButton`
        :param __event: the button event that called this method.
        :type __event: :class:`gtk.gdk.Event`
        :param entry: the RTKEntry() to place the date in.
        :type entry: :class:`rtk.gui.gtk.rtk.Entry.RTKEntry`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _calendar = rtk.RTKDateSelect()

        _date = _calendar.do_run()

        entry.set_text(_date)

        _calendar.do_destroy()

        return _return

    def _do_set_revision(self, module_id):
        """
        Set the revision ID attribute when a Revision is selected.

        :param int module_id: the ID of the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = module_id

        return None

    def _make_general_data_page(self):
        """
        Make the Validation class gtk.Notebook() general data page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbTaskType.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_VALIDATION_TYPE:
            _data.append(
                [self._mdcRTK.RTK_CONFIGURATION.RTK_VALIDATION_TYPE[_key][1]])
        self.cmbTaskType.do_load_combo(_data)

        _model = self.cmbMeasurementUnit.get_model()
        _model.clear()

        _data = []
        for _key in self._mdcRTK.RTK_CONFIGURATION.RTK_MEASUREMENT_UNITS:
            _data.append([
                self._mdcRTK.RTK_CONFIGURATION.RTK_MEASUREMENT_UNITS[_key][1]
            ])
        self.cmbMeasurementUnit.do_load_combo(_data)

        # Build the General Data page starting with the left half.
        _hbox = gtk.HBox()

        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Task Description"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[0][:2],
                                              _fixed, 5, 5)
        _x_pos += 50

        _hbox.pack_start(_frame, expand=True, fill=True)

        _fixed.put(self.txtID, _x_pos, _y_pos[0])
        _fixed.put(self.txtTask.scrollwindow, _x_pos, _y_pos[1])

        _x_pos, _y_pos = rtk.make_label_group(
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
        _vpaned = gtk.VPaned()
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Task Effort"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[1],
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
        self.spnStatus.set_adjustment(gtk.Adjustment(0, 0, 100, 1, 0.1))
        self.spnStatus.set_update_policy(gtk.UPDATE_IF_VALID)
        self.spnStatus.set_numeric(True)
        self.spnStatus.set_snap_to_ticks(True)

        # Now add the bottom pane to the right side.
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"Project Effort"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels[2],
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

        _hbox.pack_end(_vpaned, expand=True, fill=True)

        _label = rtk.RTKLabel(
            _(u"General\nData"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays general information for the selected "
                      u"validation."))
        self.hbx_tab_label.pack_start(_label)

        return _hbox

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the Validation class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Validation class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Calculate the cost and time of the currently selected "
              u"Validation task only."),
            _(u"Calculate the cost and time of the program (i.e., all "
              u"Validation tasks)."),
            _(u"Saves the currently selected Validation to the open "
              u"RTK Program database."),
            _(u"Saves all the Validation tasks and Program results to the "
              u"open RTK Program database.")
        ]
        _callbacks = [
            self._do_request_calculate, self._do_request_calculate_program,
            self._do_request_update, self._do_request_update_all
        ]
        _icons = ['calculate', 'calculate-all', 'save', 'save-all']

        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _on_combo_changed(self, combo, index):
        """
        Handle changs made in gtk.ComboBox() widgets.

        This method is called by:

            * RTKComboBox() 'changed' signal

        This method sends the 'wvwEditedValidation' message.

        :param combo: the RTKComboBox() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.Combo.RTKComboBox`
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        combo.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _validation = self._dtc_data_controller.request_select(
                self._validation_id)

            if index == 1:
                _index = 3
                _new_text = combo.get_active_text()
                _validation.task_type = _new_text
            elif index == 3:
                _index = 5
                _new_text = combo.get_active_text()
                _validation.measurement_unit = _new_text

            pub.sendMessage(
                'wvwEditedValidation', position=_index, new_text=_new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_edit(self, index, new_text):
        """
        Update the Work View gtk.Widgets() when Validation attributes change.

        This method is called whenever an attribute is edited in a different
        view.

        :param int index: the index in the Validation attributes list of the
                          attribute that was edited.
        :param str new_text: the new text to update the gtk.Widget() with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _validation = self._dtc_data_controller.request_select(
            self._validation_id)

        if index == 2:
            _buffer = self.txtTask.do_get_buffer()
            _buffer.handler_block(self._lst_handler_id[0])
            _buffer.set_text(str(new_text))
            _buffer.handler_unblock(self._lst_handler_id[0])
        elif index == 3:
            self.cmbTaskType.handler_block(self._lst_handler_id[1])
            _types = self._mdcRTK.RTK_CONFIGURATION.RTK_VALIDATION_TYPE
            self.cmbTaskType.set_active(0)
            for _key, _type in _types.iteritems():
                if _type[1] == _validation.task_type:
                    self.cmbTaskType.set_active(int(_key))
            self.cmbTaskType.handler_unblock(self._lst_handler_id[1])
        elif index == 4:
            self.txtSpecification.handler_block(self._lst_handler_id[2])
            self.txtSpecification.set_text(new_text)
            self.txtSpecification.handler_unblock(self._lst_handler_id[2])
        elif index == 5:
            self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
            _units = self._mdcRTK.RTK_CONFIGURATION.RTK_MEASUREMENT_UNITS
            self.cmbMeasurementUnit.set_active(0)
            for _key, _unit in _units.iteritems():
                if _unit[1] == _validation.measurement_unit:
                    self.cmbMeasurementUnit.set_active(int(_key))
            self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])
        elif index == 6:
            self.txtMinAcceptable.handler_block(self._lst_handler_id[4])
            self.txtMinAcceptable.set_text(str(new_text))
            self.txtMinAcceptable.handler_unblock(self._lst_handler_id[4])
        elif index == 7:
            self.txtMeanAcceptable.handler_block(self._lst_handler_id[5])
            self.txtMeanAcceptable.set_text(str(new_text))
            self.txtMeanAcceptable.handler_unblock(self._lst_handler_id[5])
        elif index == 8:
            self.txtMaxAcceptable.handler_block(self._lst_handler_id[6])
            self.txtMaxAcceptable.set_text(str(new_text))
            self.txtMaxAcceptable.handler_unblock(self._lst_handler_id[6])
        elif index == 9:
            self.txtVarAcceptable.handler_block(self._lst_handler_id[7])
            self.txtVarAcceptable.set_text(str(new_text))
            self.txtVarAcceptable.handler_unblock(self._lst_handler_id[7])
        elif index == 10:
            self.txtStartDate.handler_block(self._lst_handler_id[8])
            self.txtStartDate.set_text(str(ordinal_to_date(new_text)))
            self.txtStartDate.handler_unblock(self._lst_handler_id[8])
        elif index == 11:
            self.txtEndDate.handler_block(self._lst_handler_id[9])
            self.txtEndDate.set_text(str(ordinal_to_date(new_text)))
            self.txtEndDate.handler_unblock(self._lst_handler_id[9])
        elif index == 12:
            self.spnStatus.handler_block(self._lst_handler_id[10])
            self.spnStatus.set_value(new_text)
            self.spnStatus.handler_unblock(self._lst_handler_id[10])
        elif index == 13:
            self.txtMinTime.handler_block(self._lst_handler_id[11])
            self.txtMinTime.set_text(str(new_text))
            self.txtMinTime.handler_unblock(self._lst_handler_id[11])
        elif index == 14:
            self.txtExpTime.handler_block(self._lst_handler_id[12])
            self.txtExpTime.set_text(str(new_text))
            self.txtExpTime.handler_unblock(self._lst_handler_id[12])
        elif index == 15:
            self.txtMaxTime.handler_block(self._lst_handler_id[13])
            self.txtMaxTime.set_text(str(new_text))
            self.txtMaxTime.handler_unblock(self._lst_handler_id[13])
        elif index == 16:
            self.txtMinCost.handler_block(self._lst_handler_id[14])
            self.txtMinCost.set_text(str(new_text))
            self.txtMinCost.handler_unblock(self._lst_handler_id[14])
        elif index == 17:
            self.txtExpCost.handler_block(self._lst_handler_id[15])
            self.txtExpCost.set_text(str(new_text))
            self.txtExpCost.handler_unblock(self._lst_handler_id[15])
        elif index == 18:
            self.txtMaxCost.handler_block(self._lst_handler_id[16])
            self.txtMaxCost.set_text(str(new_text))
            self.txtMaxCost.handler_unblock(self._lst_handler_id[16])

        return _return

    def _on_focus_out(self, entry, __event, index):
        """
        Handle changes made in RTKEntry() and RTKTextView() widgets.

        This method is called by:

            * RTKEntry() 'changed' signal
            * RTKTextView() 'changed' signal

        This method sends the 'wvwEditedValidation' message.

        :param entry: the RTKEntry() or RTKTextView() that called this method.
        :type entry: :class:`rtk.gui.gtk.rtk.Entry`
        :param __event: the gtk.gdk.Event() that called this method.
        :type __event: :class:`gtk.gdk.Event`
        :param int index: the position in the Validation class gtk.TreeModel()
                          associated with the data from the calling
                          RTK widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _index = -1
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _validation = self._dtc_data_controller.request_select(
                self._validation_id)

            if index == 0:
                _index = 2
                _text = self.txtTask.do_get_text()
                _validation.description = _text
            elif index == 2:
                _index = 4
                _text = str(entry.get_text())
                _validation.task_specification = _text
            elif index == 4:
                _index = 6
                _text = float(entry.get_text())
                _validation.acceptable_minimum = _text
            elif index == 5:
                _index = 7
                _text = float(entry.get_text())
                _validation.acceptable_mean = _text
            elif index == 6:
                _index = 8
                _text = float(entry.get_text())
                _validation.acceptable_maximum = _text
            elif index == 7:
                _index = 9
                _text = float(entry.get_text())
                _validation.acceptable_variance = _text
            elif index == 8:
                _index = 10
                _text = str(entry.get_text())
                _validation.date_start = datetime.strptime(_text, '%Y-%m-%d')
            elif index == 9:
                _index = 11
                _text = str(entry.get_text())
                _validation.date_end = datetime.strptime(_text, '%Y-%m-%d')
            elif index == 11:
                _index = 13
                _text = float(entry.get_text())
                _validation.time_minimum = _text
            elif index == 12:
                _index = 14
                _text = float(entry.get_text())
                _validation.time_average = _text
            elif index == 13:
                _index = 15
                _text = float(entry.get_text())
                _validation.time_maximum = _text
            elif index == 14:
                _index = 18
                _text = float(entry.get_text())
                _validation.cost_minimum = _text
            elif index == 15:
                _index = 19
                _text = float(entry.get_text())
                _validation.cost_average = _text
            elif index == 16:
                _index = 20
                _text = float(entry.get_text())
                _validation.cost_maximum = _text

            pub.sendMessage(
                'wvwEditedValidation', position=_index, new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_select(self, module_id, **kwargs):
        """
        Load the Validation Work View class gtk.Notebook() widgets.

        :param int validation_id: the Validation ID of the selected/edited
                                  Validation.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._validation_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['validation']
        _validation = self._dtc_data_controller.request_select(
            self._validation_id)

        self.txtID.set_text(str(_validation.validation_id))

        _buffer = self.txtTask.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[0])
        _buffer.set_text(_validation.description)
        _buffer.handler_unblock(self._lst_handler_id[0])

        self.cmbTaskType.handler_block(self._lst_handler_id[1])
        _types = self._mdcRTK.RTK_CONFIGURATION.RTK_VALIDATION_TYPE
        _index = 1
        self.cmbTaskType.set_active(0)
        for _key, _type in _types.iteritems():
            if _type[1] == _validation.task_type:
                self.cmbTaskType.set_active(_index)
            else:
                _index += 1
        self.cmbTaskType.handler_unblock(self._lst_handler_id[1])

        self.txtSpecification.handler_block(self._lst_handler_id[2])
        self.txtSpecification.set_text(str(_validation.task_specification))
        self.txtSpecification.handler_unblock(self._lst_handler_id[2])

        self.cmbMeasurementUnit.handler_block(self._lst_handler_id[3])
        _units = self._mdcRTK.RTK_CONFIGURATION.RTK_MEASUREMENT_UNITS
        self.cmbMeasurementUnit.set_active(0)
        for _key, _unit in _units.iteritems():
            if _unit[1] == _validation.measurement_unit:
                self.cmbMeasurementUnit.set_active(int(_key))
        self.cmbMeasurementUnit.handler_unblock(self._lst_handler_id[3])

        self.txtMinAcceptable.handler_block(self._lst_handler_id[4])
        self.txtMinAcceptable.set_text(
            str(self.fmt.format(_validation.acceptable_minimum)))
        self.txtMinAcceptable.handler_unblock(self._lst_handler_id[4])

        self.txtMeanAcceptable.handler_block(self._lst_handler_id[5])
        self.txtMeanAcceptable.set_text(
            str(self.fmt.format(_validation.acceptable_mean)))
        self.txtMeanAcceptable.handler_unblock(self._lst_handler_id[5])

        self.txtMaxAcceptable.handler_block(self._lst_handler_id[6])
        self.txtMaxAcceptable.set_text(
            str(self.fmt.format(_validation.acceptable_maximum)))
        self.txtMaxAcceptable.handler_unblock(self._lst_handler_id[6])

        self.txtVarAcceptable.handler_block(self._lst_handler_id[7])
        self.txtVarAcceptable.set_text(
            str(self.fmt.format(_validation.acceptable_variance)))
        self.txtVarAcceptable.handler_unblock(self._lst_handler_id[7])

        self.txtStartDate.handler_block(self._lst_handler_id[8])
        _date_start = datetime.strftime(_validation.date_start, '%Y-%m-%d')
        self.txtStartDate.set_text(_date_start)
        self.txtStartDate.handler_unblock(self._lst_handler_id[8])

        self.txtEndDate.handler_block(self._lst_handler_id[9])
        _date_end = datetime.strftime(_validation.date_end, '%Y-%m-%d')
        self.txtEndDate.set_text(_date_end)
        self.txtEndDate.handler_unblock(self._lst_handler_id[9])

        self.spnStatus.handler_block(self._lst_handler_id[10])
        self.spnStatus.set_value(_validation.status)
        self.spnStatus.handler_unblock(self._lst_handler_id[10])

        self.txtMinTime.handler_block(self._lst_handler_id[11])
        self.txtMinTime.set_text(
            str(self.fmt.format(_validation.time_minimum)))
        self.txtMinTime.handler_unblock(self._lst_handler_id[11])

        self.txtExpTime.handler_block(self._lst_handler_id[12])
        self.txtExpTime.set_text(
            str(self.fmt.format(_validation.time_average)))
        self.txtExpTime.handler_unblock(self._lst_handler_id[12])

        self.txtMaxTime.handler_block(self._lst_handler_id[13])
        self.txtMaxTime.set_text(
            str(self.fmt.format(_validation.time_maximum)))
        self.txtMaxTime.handler_unblock(self._lst_handler_id[13])

        self.txtMinCost.handler_block(self._lst_handler_id[14])
        self.txtMinCost.set_text(
            str(self.fmt.format(_validation.cost_minimum)))
        self.txtMinCost.handler_unblock(self._lst_handler_id[14])

        self.txtExpCost.handler_block(self._lst_handler_id[15])
        self.txtExpCost.set_text(
            str(self.fmt.format(_validation.cost_average)))
        self.txtExpCost.handler_unblock(self._lst_handler_id[15])

        self.txtMaxCost.handler_block(self._lst_handler_id[16])
        self.txtMaxCost.set_text(
            str(self.fmt.format(_validation.cost_maximum)))
        self.txtMaxCost.handler_unblock(self._lst_handler_id[16])

        self.txtMeanTimeLL.set_text(str(self.fmt.format(_validation.time_ll)))
        self.txtMeanTime.set_text(str(self.fmt.format(_validation.time_mean)))
        self.txtMeanTimeUL.set_text(str(self.fmt.format(_validation.time_ul)))
        self.txtMeanCostLL.set_text(str(self.fmt.format(_validation.cost_ll)))
        self.txtMeanCost.set_text(str(self.fmt.format(_validation.cost_mean)))
        self.txtMeanCostUL.set_text(str(self.fmt.format(_validation.cost_ul)))

        return _return

    def _on_value_changed(self, spinbutton, index):
        """
        Handle changes made in gtk.SpinButton() widgets.

        This method is called by:

            * gtk.SpinButton() 'changed' signal

        This method sends the 'wvwEditedValidation' message.

        :param spinbutton: the gtk.SpinButton() that called this method.
        :type spinbutton: :class:`gtk.SpinButton`
        :param int index: the position in the Validation class attribute list
                          associated with the data from the calling
                          spinbutton.
        """
        spinbutton.handler_block(self._lst_handler_id[index])

        _validation = self._dtc_data_controller.request_select(
            self._validation_id)

        if index == 10:
            _index = 12
            _text = spinbutton.get_value()
            _validation.status = float(_text)

        pub.sendMessage('wvwEditedValidation', position=_index, new_text=_text)

        spinbutton.handler_unblock(self._lst_handler_id[index])

        return False


class BurndownCurve(RTKWorkView):
    """
    Display Validation task burndown curve in the RTK Work Book.

    The Validation Burndown Curve displays the planned burndown curve (solid
    line) for all tasks in the V&V plan as well as the actual progress
    (points).  The attributes of a Validation Burndown Curve View are:

    :ivar int _validation_id: the ID of the Validation task currently being
                              displayed.
    :ivar burndown: the RTKPlot() widget to display the burndown curve of
                    program V&V task effort.
    """

    def __init__(self, controller):
        """
        Initialize the Work View for the Validation package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Validation')

        # Initialize private dictionary attributes.
        self._dic_icons['calculate-all'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/calculate-all.png'
        self._dic_icons['plot'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/charts.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._validation_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.burndown = rtk.RTKPlot()

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(
            self._make_burndown_curve_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._do_request_plot, 'calculatedProgram')

    # pylint: disable=unused-argument
    def _do_load_burndown_status(self, module_id=None):
        """
        Load the actual burndown progress.

        :param int module_id: unused; needed for compatibility with pubsub
                              message.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _y_actual = self._dtc_data_controller.request_actual_burndown()

        if _y_actual:
            self.burndown.do_add_line(
                x_values=_y_actual.keys(),
                y_values=_y_actual.values(),
                marker='o')

        else:
            _prompt = _(u"Actual program status information is not "
                        u"available.  You must calculate the program to make "
                        u"this information available for plotting.")
            _dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['important'], 'warning')
            _response = _dialog.do_run()

            if _response == gtk.RESPONSE_OK:
                _dialog.do_destroy()

            _return = True

        return _return

    def _do_load_planned_burndown(self, module_id=None):
        """
        Load the Validation class effort progress plot.

        :param int module_id: unused; needed for compatibility with pubsub
                              message.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['validation']

        (_y_minimum, _y_average,
         _y_maximum) = self._dtc_data_controller.request_planned_burndown()

        self.burndown.axis.cla()
        self.burndown.axis.grid(True, which='both')

        _time_minimum = list(reversed(np.cumsum(_y_minimum.values())))
        _time_average = list(reversed(np.cumsum(_y_average.values())))
        _time_maximum = list(reversed(np.cumsum(_y_maximum.values())))

        # Plot the maximum, mean, and minimum expected burndown curves.
        if _y_maximum:
            self.burndown.do_load_plot(
                x_values=_y_maximum.keys(),
                y_values=_time_maximum,
                plot_type='date',
                marker='r--')
        if _y_average:
            self.burndown.do_load_plot(
                x_values=_y_average.keys(),
                y_values=_time_average,
                plot_type='date',
                marker='b-')
            self._x_pos = int(
                (max(_y_average.keys()) - min(_y_average.keys())) / 2)
        if _y_minimum:
            self.burndown.do_load_plot(
                x_values=_y_minimum.keys(),
                y_values=_time_minimum,
                plot_type='date',
                marker='g--')

        (_assessment_dates,
         _targets) = self._dtc_data_controller.request_assessments()

        # Add a vertical line at the scheduled end-date for each task
        # identified as a Reliability Assessment.  Add an annotation box
        # showing the minimum and maximum goal values for each milestone.
        if _assessment_dates:
            for __, _dates in enumerate(_assessment_dates):
                self.burndown.axis.axvline(
                    x=_dates,
                    ymin=0,
                    ymax=1.05 * _y_maximum.values()[0],
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

        return _return

    def _do_request_calculate_program(self, __button):
        """
        Request to calculate program cost and time.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        (_cost_ll, _cost_mean, _cost_ul, _time_ll, _time_mean,
         _time_ul) = self._dtc_data_controller.request_calculate_program()

        return _return

    def _do_request_plot(self, __button=None):
        """
        Request to load planned and actual burndown curves.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._do_load_planned_burndown()
        self._do_load_burndown_status()

        self.burndown.do_make_title(_(u"Total Validation Effort"))
        self.burndown.do_make_labels(
            _(u"Total Time [hours]"), -0.5, 0, set_x=False)
        _text = (_(u"Maximum Expected Time"), _(u"Mean Expected Time"),
                 _(u"Minimum Expected Time"), _(u"Actual Remaining Time"))
        self.burndown.do_make_legend(_text)
        self.burndown.figure.canvas.draw()

        return _return

    def _do_request_update_all(self, __button):
        """
        Request to save all Validation tasks and program results.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = self._dtc_data_controller.request_update_all()

        if not _return:
            _return = self._dtc_data_controller.request_update_status()

        return _return

    def _make_burndown_curve_page(self):
        """
        Make the Validation class gtk.Notebook() burndown curve page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _frame = rtk.RTKFrame(label=_(u"Program Validation Effort"))
        _frame.add(self.burndown.plot)
        _frame.show_all()

        # Insert the tab.
        self.hbx_tab_label = gtk.Label()
        self.hbx_tab_label.set_markup("<span weight='bold'>" +
                                      _(u"Program\nValidation\nProgress") +
                                      "</span>")
        self.hbx_tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.hbx_tab_label.set_justify(gtk.JUSTIFY_CENTER)
        self.hbx_tab_label.show_all()
        self.hbx_tab_label.set_tooltip_text(
            _(u"Shows a plot of the total expected time "
              u"to complete all V&amp;V tasks and the "
              u"current progress."))

        return _frame

    def _make_buttonbox(self):
        """
        Make the gtk.ButtonBox() for the Validation class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Validation class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Calculate the cost and time of the program (i.e., all "
              u"Validation tasks)."),
            _(u"Load the planned and actual burndown curves."),
            _(u"Saves all the Validation tasks and Program results to the "
              u"open RTK Program database.")
        ]
        _callbacks = [
            self._do_request_calculate_program, self._do_request_plot,
            self._do_request_update_all
        ]
        _icons = ['calculate-all', 'plot', 'save-all']

        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox
