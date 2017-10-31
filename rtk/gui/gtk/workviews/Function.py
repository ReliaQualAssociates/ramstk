# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Function.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Function Package Work View
###############################################################################
"""

import locale

from pubsub import pub                          # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk                         # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk           # pylint: disable=E0401,W0611
from .WorkView import RTKWorkView


class GeneralData(RTKWorkView):
    """
    The Work View displays all the attributes for the selected Function. The
    attributes of a Work View are:

    :ivar _lst_handler_id: list containing the ID's of the callback signals for
                           each gtk.Widget() associated with an editable
                           Function attribute.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |      0   | txtCode `focus_out_event`                 |
    +----------+-------------------------------------------+
    |      1   | txtName `focus_out_event`                 |
    +----------+-------------------------------------------+
    |      2   | txtRemarks `focus_out_event`              |
    +----------+-------------------------------------------+
    |      3   | Mission gtk.CellRendererCombo() `edited`  |
    +----------+-------------------------------------------+
    |      4   | Phase gtk.CellRendererCombo() `edited`    |
    +----------+-------------------------------------------+
    |      5   | btnAddMode `clicked`                      |
    +----------+-------------------------------------------+
    |      6   | btnRemoveMode `clicked`                   |
    +----------+-------------------------------------------+
    |      7   | btnSaveFMEA `clicked`                     |
    +----------+-------------------------------------------+

    :ivar _dtc_function: the :class:`rtk.function.Function.Function` data
                         controller to use with this Work Book.

    :ivar chkSafetyCritical: the :class:`gtk.CheckButton` to display/edit the
                             Function's safety criticality.

    :ivar txtCode: the :class:`gtk.Entry` to display/edit the Function code.
    :ivar txtName: the :class:`gtk.Entry` to display/edit the Function name.
    :ivar txtTotalCost: the :class:`gtk.Entry` to display the Function cost.
    :ivar txtModeCount: the :class:`gtk.Entry` to display the number of
                        hardware failure modes the Function is susceptible to.
    :ivar txtPartCount: the :class:`gtk.Entry` to display the number of
                        hardware components comprising the Function.
    :ivar txtRemarks: the :class:`gtk.Entry` to display/edit the Function
                      remarks.
    """

    def __init__(self, controller):
        """
        Method to initialize the Work View for the Function package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKWorkView.__init__(self, controller, module='Function')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_function = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self._function_id = None

        # General data page widgets.
        self.chkSafetyCritical = rtk.RTKCheckButton(
            label=_(u"Function is safety critical."),
            tooltip=_(u"Indicates whether or not the selected function is "
                      u"safety critical."))

        self.txtCode = rtk.RTKEntry(width=125,
                                    tooltip=_(u"Enter a unique code for the "
                                              u"selected Function."))
        self.txtTotalCost = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the total cost "
                                                   u"of the selected "
                                                   u"Function."))
        self.txtName = rtk.RTKEntry(width=400, tooltip=_(u"Enter the name of "
                                                         u"the selected "
                                                         u"Function."))
        self.txtModeCount = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the total "
                                                   u"number of failure modes "
                                                   u"associated with the "
                                                   u"selected Function."))
        self.txtPartCount = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the total "
                                                   u"number of components "
                                                   u"associated with the "
                                                   u"selected Function."))
        self.txtRemarks = rtk.RTKTextView(txvbuffer=gtk.TextBuffer(),
                                          width=400,
                                          tooltip=_(u"Enter any remarks "
                                                    u"related to the selected "
                                                    u"Function."))

        # Connect to callback functions for editable gtk.Widgets().
        self._lst_handler_id.append(
            self.txtCode.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtName.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtRemarks.do_get_buffer().connect(
                'changed', self._on_focus_out, 2))

        # FIXME: The general data page should be the page shown after launching.
        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(self._make_general_data_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedFunction')
        pub.subscribe(self._on_edit, 'mvwEditedFunction')
        pub.subscribe(self._on_edit, 'calculatedFunction')

    def _do_request_calculate(self, __button):
        """
        Method to send request to calculate the selected function to the
        Function data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code = 0
        _msg = ['', '']

        if self._dtc_function.request_calculate_reliability(self._function_id):
            _error_code = 1
            _msg[0] = 'Error calculating reliability attributes.'

        if self._dtc_function.request_calculate_availability(
                self._function_id):
            _error_code = 1
            _msg[1] = 'Error calculating availability attributes.'

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to calculate "
                        u"Function {0:d}. \n\n\t" + _msg[0] + "\n\t" +
                        _msg[1] + "\n\n").format(self._function_id)
            _error_dialog = rtk.RTKMessageDialog(_prompt,
                                                 self._dic_icons['error'],
                                                 'error')
            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_update(self, __button):
        """
        Method to save the currently selected Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_function.request_update(self._function_id)

    def _make_general_data_page(self):
        """
        Method to create the Function class gtk.Notebook() page for
        displaying general data about the selected Function.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _frame, _fixed = RTKWorkView._make_general_data_page()

        _labels = [_(u"Function Code:"), _(u"Function Name:"),
                   _(u"Total Cost:"), _(u"Total Mode Count:"),
                   _(u"Total Part Count:"), _(u"Remarks:")]
        _x_pos, _y_pos = rtk.make_label_group(_labels, _fixed, 5, 5)
        _x_pos = _x_pos + 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtTotalCost, _x_pos, _y_pos[2])
        _fixed.put(self.txtModeCount, _x_pos, _y_pos[3])
        _fixed.put(self.txtPartCount, _x_pos, _y_pos[4])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[5])
        _fixed.put(self.chkSafetyCritical, 5, _y_pos[5] + 110)

        _fixed.show_all()

        _label = rtk.RTKLabel(_(u"General\nData"), height=30, width=-1,
                              justify=gtk.JUSTIFY_CENTER,
                              tooltip=_(u"Displays general information for "
                                        u"the selected Function."))
        self.hbx_tab_label.pack_start(_label)

        return _frame

    def _make_buttonbox(self):
        """
        Method to create the gtk.ButtonBox() for the Function class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Function class Work
                 View.
        :rtype: :py:class:`gtk.ButtonBox`
        """

        _tooltips = [_(u"Calculate the currently selected Function."),
                     _(u"Saves the currently selected Function to the open "
                       u"RTK Project database.")]
        _callbacks = [self._do_request_calculate, self._do_request_update]

        _icons = ['calculate', 'save']
        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _on_edit(self, index, new_text):
        """
        Method to update the Work View gtk.Widgets() with changes to the
        Function data model attributes.  This method is called whenever an
        attribute is edited in a different view.

        :param int index: the index in the Function attributes list of the
                          attribute that was edited.
        :param str new_text: the new text to update the gtk.Widget() with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if index == 5:
            self.txtCode.handler_block(self._lst_handler_id[0])
            self.txtCode.set_text(str(new_text))
            self.txtCode.handler_unblock(self._lst_handler_id[0])
        elif index == 15:
            self.txtName.handler_block(self._lst_handler_id[1])
            self.txtName.set_text(new_text)
            self.txtName.handler_unblock(self._lst_handler_id[1])
        elif index == 17:
            _textbuffer = self.txtRemarks.do_get_buffer()
            _textbuffer.handler_block(self._lst_handler_id[2])
            _textbuffer.set_text(new_text)
            _textbuffer.handler_unblock(self._lst_handler_id[2])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Method to retrieve changes made to Function attributes through the
        various gtk.Widgets() and assign the new data to the appropriate
        Function data model attribute.  This method is called by:

            * gtk.Entry() 'changed' signal
            * gtk.TextView() 'changed' signal

        This method sends the 'wvwEditedFunction' message.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param int index: the position in the Function class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _index = -1
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_function is not None:
            _function = self._dtc_function.request_select(self._function_id)

            if index == 0:
                _index = 5
                _text = str(entry.get_text())
                _function.function_code = _text
            elif index == 1:
                _index = 15
                _text = str(entry.get_text())
                _function.name = _text
            elif index == 2:
                _index = 17
                _text = self.txtRemarks.do_get_text()
                _function.remarks = _text

            pub.sendMessage('wvwEditedFunction', position=_index,
                            new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_select(self, module_id, **kwargs):
        """
        Method to load the Function Work View class gtk.Notebook() widgets.

        :param int function_id: the Function ID of the selected/edited
                                Function.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._function_id = module_id

        self._dtc_function = self._mdcRTK.dic_controllers['function']
        _function = self._dtc_function.request_select(self._function_id)

        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(_function.function_code))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text(_function.name)
        self.txtName.handler_unblock(self._lst_handler_id[1])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[2])
        _textbuffer.set_text(_function.remarks)
        _textbuffer.handler_unblock(self._lst_handler_id[2])

        self.txtTotalCost.set_text(
            str(locale.currency(_function.cost)))
        self.txtModeCount.set_text(
            str('{0:d}'.format(_function.total_mode_count)))
        self.txtPartCount.set_text(
            str('{0:d}'.format(_function.total_part_count)))

        return _return


class AssessmentResults(RTKWorkView):
    """
    The Work View displays all the attributes for the selected Function. The
    attributes of a Work View are:

    :ivar _dtc_function: the :class:`rtk.function.Function.Function` data
                         controller to use with this Work Book.
    :ivar txtPredictedHt: the :class:`gtk.Entry` to display the Function
                          logistics hazard rate.
    :ivar txtMissionHt: the :class:`gtk.Entry` to display the Function mission
                        hazard rate.
    :ivar txtMTBF: the :class:`gtk.Entry` to display the Function logistics
                   MTBF.
    :ivar txtMissionMTBF: the :class:`gtk.Entry` to display the Function
                          mission MTBF.
    :ivar txtMPMT: the :class:`gtk.Entry` to display the Function mean
                   preventive maintenance time.
    :ivar txtMCMT: the :class:`gtk.Entry` to display the Function mean
                   corrective maintenance time.
    :ivar txtMTTR: the :class:`gtk.Entry` to display the Function mean time to
                   repair.
    :ivar txtMMT: the :class:`gtk.Entry` to display the Function mean
                  maintenance time.
    :ivar txtAvailability: the :class:`gtk.Entry` to display the Function
                           logistics availability.
    :ivar txtMissionAt: the :class:`gtk.Entry` to display the Function mission
                        availability.
    """

    def __init__(self, controller):
        """
        Method to initialize the Work View for the Function package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKWorkView.__init__(self, controller, module='Function')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_function = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self._function_id = None

        self.pack_start(self._make_assessment_results_page(), expand=True,
                        fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedFunction')

    def _make_assessment_results_page(self):
        """
        Method to create the Function class gtk.Notebook() page for
        displaying assessment results for the selected Function.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_hbx_page,
         __, __, __, __) = RTKWorkView._make_assessment_results_page(self)

        self.txtActiveHt.set_sensitive(False)
        self.txtDormantHt.set_sensitive(False)
        self.txtSoftwareHt.set_sensitive(False)
        self.txtReliability.set_sensitive(False)
        self.txtMissionRt.set_sensitive(False)

        return _hbx_page

    def _on_select(self, module_id, **kwargs):
        """
        Method to load the Function Work View class gtk.Notebook() widgets.

        :param int function_id: the Function ID of the selected/edited
                                Function.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._function_id = module_id

        self._dtc_function = self._mdcRTK.dic_controllers['function']
        _function = self._dtc_function.request_select(self._function_id)

        self.txtAvailability.set_text(
            str(self.fmt.format(_function.availability_logistics)))
        self.txtMissionAt.set_text(
            str(self.fmt.format(_function.availability_mission)))
        self.txtMissionHt.set_text(
            str(self.fmt.format(_function.hazard_rate_mission)))
        self.txtPredictedHt.set_text(
            str(self.fmt.format(_function.hazard_rate_logistics)))

        self.txtMMT.set_text(str(self.fmt.format(_function.mmt)))
        self.txtMCMT.set_text(str(self.fmt.format(_function.mcmt)))
        self.txtMPMT.set_text(str(self.fmt.format(_function.mpmt)))

        self.txtMissionMTBF.set_text(
            str(self.fmt.format(_function.mtbf_mission)))
        self.txtMTBF.set_text(
            str(self.fmt.format(_function.mtbf_logistics)))
        self.txtMTTR.set_text(str(self.fmt.format(_function.mttr)))

        return _return
