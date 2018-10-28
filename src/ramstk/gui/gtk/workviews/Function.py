# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.Function.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Work View."""

import locale

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.Utilities import boolean_to_integer
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk
from .WorkView import RAMSTKWorkView


class GeneralData(RAMSTKWorkView):
    """
    Display Function attribute data in the RAMSTK Work Book.

    The Work View displays all the general data attributes for the selected
    Function. The attributes of a Function General Data Work View are:

    :ivar int _function_id: the ID of the Function currently being displayed.
    :ivar chkSafetyCritical: the
                             :class:`ramstk.gui.gtk.ramstk.RAMSTKCheckButton`
                             to display/edit the Function's safety criticality.
    :ivar txtTotalCost: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the Function cost.
    :ivar txtModeCount: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the number of failure modes the function is
                        susceptible to.

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

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Function')

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
        self.chkSafetyCritical = ramstk.RAMSTKCheckButton(
            label=_(u"Function is safety critical."),
            tooltip=_(u"Indicates whether or not the selected function is "
                      u"safety critical."))

        self.txtCode = ramstk.RAMSTKEntry(
            width=125, tooltip=_(u"A unique code for the selected function."))
        self.txtName = ramstk.RAMSTKEntry(
            width=800, tooltip=_(u"The name of the selected function."))
        self.txtRemarks = ramstk.RAMSTKTextView(
            gtk.TextBuffer(),
            width=800,
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

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_start(self._make_page(), expand=True, fill=True)
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'selected_function')
        pub.subscribe(self._do_clear_page, 'closed_program')

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

    def _do_load_page(self, attributes):
        """
        Load the Function General Data page.

        :param tuple attributes: a dict of attribute key:value pairs for
                                 the selected Function.
        :return: None
        :rtype: None
        """
        self._function_id = attributes['function_id']

        self.txtCode.handler_block(self._lst_handler_id[0])
        self.txtCode.set_text(str(attributes['function_code']))
        self.txtCode.handler_unblock(self._lst_handler_id[0])

        self.txtName.handler_block(self._lst_handler_id[1])
        self.txtName.set_text(str(attributes['name']))
        self.txtName.handler_unblock(self._lst_handler_id[1])

        _textbuffer = self.txtRemarks.do_get_buffer()
        _textbuffer.handler_block(self._lst_handler_id[2])
        _textbuffer.set_text(str(attributes['remarks']))
        _textbuffer.handler_unblock(self._lst_handler_id[2])

        self.chkSafetyCritical.handler_block(self._lst_handler_id[3])
        self.chkSafetyCritical.set_active(int(attributes['safety_critical']))
        self.chkSafetyCritical.handler_unblock(self._lst_handler_id[3])

        return None

    def _do_request_update(self, __button):
        """
        Send request to save the currently selected Function.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_function', node_id=self._function_id)
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _do_request_update_all(self, __button):
        """
        Request to save all the Functions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`.
        :return: None
        :rtype: None
        """
        self.set_cursor(gtk.gdk.WATCH)
        pub.sendMessage('request_update_all_functions')
        self.set_cursor(gtk.gdk.LEFT_PTR)

        return None

    def _make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the gtk.ButtonBox() for the Function class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Function class Work
                 View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Saves the currently selected Function to the open "
              u"RAMSTK Program database."),
            _(u"Saves all Functions to the open RAMSTK Program database."),
        ]
        _callbacks = [self._do_request_update, self._do_request_update_all]
        _icons = ['save', 'save-all']

        _buttonbox = ramstk.do_make_buttonbox(
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

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_(u"General Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_gendata_labels,
                                                 _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[2])
        _fixed.put(self.chkSafetyCritical, 5, _y_pos[2] + 110)

        _fixed.show_all()

        _label = ramstk.RAMSTKLabel(
            _(u"General\nData"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays general information for the selected "
                      u"function."))
        self.hbx_tab_label.pack_start(_label)

        return _frame

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * gtk.Entry() 'changed' signal
            * gtk.TextView() 'changed' signal

        This method sends the 'wvwEditedFunction' message.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param int index: the position in the Function class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().
        :return: None
        :rtype: None
        """
        _key = ''
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if index == 0:
            _key = 'function_code'
            _text = str(entry.get_text())
        elif index == 1:
            _key = 'name'
            _text = str(entry.get_text())
        elif index == 2:
            _key = 'remarks'
            _text = self.txtRemarks.do_get_text()

        pub.sendMessage(
            'editing_function',
            module_id=self._function_id,
            key=_key,
            value=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_toggled(self, togglebutton, index):
        """
        Handle RAMSTKCheckButton() 'toggle' signals.

        :param togglebutton: the RAMSTKToggleButton() that called this method.
        :type: :class:`ramstk.gui.gtk.ramstk.Button.RAMSTKToggleButton`
        :param int index: the index in the signal handler ID list.
        :return: None
        :rtype: None
        """
        togglebutton.handler_block(self._lst_handler_id[index])

        _key = 'safety_critical'
        _text = boolean_to_integer(self.chkSafetyCritical.get_active())

        togglebutton.handler_unblock(self._lst_handler_id[index])

        pub.sendMessage(
            'editing_function',
            module_id=self._function_id,
            key=_key,
            value=_text)

        return None


class AssessmentResults(RAMSTKWorkView):
    """
    Display Function attribute data in the RAMSTK Work Book.

    The Function Assessment Results view displays all the assessment results
    for the selected Function.  The attributes of a Function Assessment Results
    View are:

    :ivar int _function_id: the ID of the Function currently being displayed.
    """

    def __init__(self, controller, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Function package.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        RAMSTKWorkView.__init__(self, controller, module='Function')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_assess_labels[1].append(_(u"Total Mode Count:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self._function_id = None

        self.txtModeCount = ramstk.RAMSTKEntry(
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
         _y_pos_r) = RAMSTKWorkView._make_assessment_results_page(self)

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
        # It is defined in RAMSTKBaseView.__init__
        if self._dtc_data_controller is None:
            self._dtc_data_controller = self._mdcRAMSTK.dic_controllers[
                'function']
        self._do_load_page()

        return _return
