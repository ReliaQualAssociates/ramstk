# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Function.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Function Work View."""

import locale

from pubsub import pub

# Import other RTK modules.
from rtk.Utilities import boolean_to_integer
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _, gtk
from .WorkView import RTKWorkView


class GeneralData(RTKWorkView):
    """
    Display Function attribute data in the RTK Work Book.

    The Work View displays all the general data attributes for the selected
    Function. The attributes of a Function General Data Work View are:

    :ivar int _function_id: the ID of the Function currently being displayed.
    :ivar chkSafetyCritical: the :class:`rtk.gui.gtk.rtk.RTKCheckButton` to
                             display/edit the Function's safety criticality.
    :ivar txtTotalCost: the :class:`rtk.gui.gtk.rtk.RTKEntry` to display the
                        Function cost.
    :ivar txtModeCount: the :class:`rtk.gui.gtk.rtk.RTKEntry` to display the
                        number of failure modes the function is susceptible to.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtCode `changed`                         |
    +----------+-------------------------------------------+
    |     1    | txtName `changed`                         |
    +----------+-------------------------------------------+
    |     2    | txtRemarks `changed`                      |
    +----------+-------------------------------------------+
    |     3    | chkSafetyCritical `toggled`               |
    +----------+-------------------------------------------+
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Function package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Function')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_gendata_labels = [
            _(u"Function Code:"),
            _(u"Function Description:"),
            _(u"Remarks:")
        ]

        # Initialize private scalar attributes.
        self._function_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # General data page widgets.
        self.chkSafetyCritical = rtk.RTKCheckButton(
            label=_(u"Function is safety critical."),
            tooltip=_(u"Indicates whether or not the selected function is "
                      u"safety critical."))

        self.txtCode = rtk.RTKEntry(
            width=125, tooltip=_(u"A unique code for the selected function."))
        self.txtName = rtk.RTKEntry(
            width=800, tooltip=_(u"The name of the selected function."))
        self.txtRemarks = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=400,
            tooltip=_(u"Enter any remarks associated with the "
                      u"selected function."))

        # Connect to callback functions for editable gtk.Widgets().
        self._lst_handler_id.append(
            self.txtCode.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtName.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.chkSafetyCritical.connect('toggled', self._on_toggled, 3))

        # FIXME: The general data page should be the page shown after launching.
        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(self._make_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedFunction')
        pub.subscribe(self._on_edit, 'mvwEditedFunction')
        pub.subscribe(self._do_clear_page, 'closedProgram')

    def _do_clear_page(self):
        """
        Clear the contents of the page.

        :return: None
        :rtype: None
        """
        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text('')
        self.txtCode.handler_unblock(self._lst_handler_id[0])
        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text('')
        self.txtName.handler_unblock(self._lst_handler_id[1])
        _buffer = self.txtRemarks.do_get_buffer()
        _buffer.handler_block(self._lst_handler_id[2])
        _buffer.set_text('')
        _buffer.handler_block(self._lst_handler_id[2])
        self.chkSafetyCritical.handler_block(self._lst_handler_id[3])
        self.chkSafetyCritical.set_active(False)
        self.chkSafetyCritical.handler_unblock(self._lst_handler_id[3])

        return None

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Function General Data page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _function = self._dtc_data_controller.request_do_select(
            self._function_id)

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

        self.chkSafetyCritical.handler_block(self._lst_handler_id[3])
        self.chkSafetyCritical.set_active(_function.safety_critical)
        self.chkSafetyCritical.handler_unblock(self._lst_handler_id[3])

        return _return

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update(
            self._function_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _do_request_update_all(self, __button):
        """
        Request to save all the Functions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(gtk.gdk.WATCH)
        _return = self._dtc_data_controller.request_do_update_all()
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return _return

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Function class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Function class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Saves the currently selected Function to the open "
              u"RTK Program database."),
            _(u"Saves all Functions to the open RTK Program database."),
        ]
        _callbacks = [self._do_request_update, self._do_request_update_all]
        _icons = ['save', 'save-all']

        _buttonbox = RTKWorkView._make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1)

        return _buttonbox

    def _make_page(self):
        """
        Make the Function class gtk.Notebook() general data page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame = rtk.RTKFrame(label=_(u"General Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_gendata_labels, _fixed,
                                              5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[2])
        _fixed.put(self.chkSafetyCritical, 5, _y_pos[2] + 110)

        _fixed.show_all()

        _label = rtk.RTKLabel(
            _(u"General\nData"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays general information for he selected "
                      u"function."))
        self.hbx_tab_label.pack_start(_label)

        return _frame

    def _on_edit(self, index, new_text):
        """
        Update the Work View gtk.Widgets() when Function attributes change.

        This method is called whenever an attribute is edited in a different
        view.

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
        Retrieve changes made in RTKEntry() widgets..

        This method is called by:

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

        if self._dtc_data_controller is not None:
            _function = self._dtc_data_controller.request_do_select(
                self._function_id)

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

            pub.sendMessage(
                'wvwEditedFunction', position=_index, new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_select(self, module_id, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Function Work View class gtk.Notebook() widgets.

        :param int module_id: the Function ID of the selected/edited Function.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._function_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        if self._dtc_data_controller is None:
            self._dtc_data_controller = self._mdcRTK.dic_controllers[
                'function']
        self._do_load_page()

        return _return

    def _on_toggled(self, togglebutton, index):
        """
        Handle RTKCheckButton() 'toggle' signals.

        :param togglebutton: the RTKToggleButton() that called this method.
        :type: :class:`rtk.gui.gtk.rtk.Button.RTKToggleButton`
        :param int index: the index in the signal handler ID list.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        togglebutton.handler_block(self._lst_handler_id[index])

        _function = self._dtc_data_controller.request_do_select(
            self._function_id)
        _function.safety_critical = boolean_to_integer(
            self.chkSafetyCritical.get_active())

        togglebutton.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage('wvwEditedFunction', position=index, new_text='')

        return _return


class AssessmentResults(RTKWorkView):
    """
    Display Function attribute data in the RTK Work Book.

    The Function Assessment Results view displays all the assessment results
    for the selected Function.  The attributes of a Function Assessment Results
    View are:

    :ivar int _function_id: the ID of the Function currently being displayed.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Function package.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKWorkView.__init__(self, controller, module='Function')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_assess_labels[1].append(_(u"Total Mode Count:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self._function_id = None

        self.txtModeCount = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the total "
                      u"number of failure modes "
                      u"associated with the "
                      u"selected Function."))

        self.pack_start(self._make_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedFunction')
        pub.subscribe(self._on_select, 'calculatedFunction')

    def _do_load_page(self, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Function Assessment Results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _function = self._dtc_data_controller.request_do_select(
            self._function_id)

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
        self.txtMTBF.set_text(str(self.fmt.format(_function.mtbf_logistics)))
        self.txtMTTR.set_text(str(self.fmt.format(_function.mttr)))

        self.txtTotalCost.set_text(str(locale.currency(_function.cost)))
        self.txtModeCount.set_text(
            str('{0:d}'.format(_function.total_mode_count)))
        self.txtPartCount.set_text(
            str('{0:d}'.format(_function.total_part_count)))

        return _return

    def _make_page(self):
        """
        Make the Function class gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        (_hbx_page, __, _fxd_right, ___, _x_pos_r, __,
         _y_pos_r) = RTKWorkView._make_assessment_results_page(self)

        _fxd_right.put(self.txtModeCount, _x_pos_r, _y_pos_r[8] + 30)
        _fxd_right.show_all()

        self.txtActiveHt.set_sensitive(False)
        self.txtDormantHt.set_sensitive(False)
        self.txtSoftwareHt.set_sensitive(False)
        self.txtReliability.set_sensitive(False)
        self.txtMissionRt.set_sensitive(False)

        return _hbx_page

    def _on_select(self, module_id, **kwargs):  # pylint: disable=unused-argument
        """
        Load the Function Work View class gtk.Notebook() widgets.

        :param int module_id: the Function ID of the selected/edited Function.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._function_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        if self._dtc_data_controller is None:
            self._dtc_data_controller = self._mdcRTK.dic_controllers[
                'function']
        self._do_load_page()

        return _return
