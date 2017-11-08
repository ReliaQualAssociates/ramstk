# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Revision.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Revision Work View Module
-------------------------------------------------------------------------------
"""

import locale

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611
from .WorkView import RTKWorkView

# from Assistants import AddRevision


class GeneralData(RTKWorkView):
    """
    The Revision Work View displays all the general data attributes for the
    selected Revision. The attributes of a Revision General Data Work View are:

    :ivar int _revision_id: the ID of the Revision currently being displayed.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtCode `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     1    | txtName `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     2    | txtRemarks `changed`                      |
    +----------+-------------------------------------------+
    """

    def __init__(self, controller):
        """
        Method to initialize the Work Book view for the Revision package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKWorkView.__init__(self, controller, module='revision')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtName.props.width_request = 800

        self._lst_handler_id.append(
            self.txtName.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(self.txtRemarks.do_get_buffer().connect(
            'changed', self._on_focus_out, None, 1))
        self._lst_handler_id.append(
            self.txtCode.connect('focus-out-event', self._on_focus_out, 2))

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_end(self._make_general_data_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedRevision')
        pub.subscribe(self._on_edit, 'mvwEditedRevision')

    def _do_request_calculate(self, __button):
        """
        Method to send request to calculate the selected revision to the
        Revision data controller.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code = 0
        _msg = ['', '', '']

        if self._dtc_data_controller.request_calculate_reliability(
                self._revision_id, self._mission_time):
            _error_code = 1
            _msg[0] = 'Error calculating reliability attributes.'

        if self._dtc_data_controller.request_calculate_availability(
                self._revision_id):
            _error_code = 1
            _msg[1] = 'Error calculating availability attributes.'

        if self._dtc_data_controller.request_calculate_costs(
                self._revision_id, self._mission_time):
            _error_code = 1
            _msg[2] = 'Error calculating cost attributes.'

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to calculate "
                        u"Revision {0:d}. \n\n\t" + _msg[0] + "\n\t" +
                        _msg[1] + "\n\t" + _msg[2] + "\n\n").\
                        format(self._revision_id)
            _error_dialog = rtk.RTKMessageDialog(
                _prompt, self._dic_icons['error'], 'error')
            if _error_dialog.do_run() == gtk.RESPONSE_OK:
                _error_dialog.do_destroy()

            _return = True

        return _return

    def _do_request_update(self, __button):
        """
        Method to save all the Functions.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_data_controller.request_update(self._revision_id)

    def _make_general_data_page(self):
        """
        Method to create the Revision Work Book page for displaying general
        data about the selected Revision.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_frame, _fixed, _x_pos,
         _y_pos) = RTKWorkView._make_general_data_page(self)

        return _frame

    def _make_buttonbox(self):
        """
        Method to create the gtk.ButtonBox() for the Revision class Work View.

        :return: _buttonbox; the gtk.ButtonBox() for the Revision class Work
                 View.
        :rtype: :py:class:`gtk.ButtonBox`
        """

        _tooltips = [
            _(u"Calculate the currently selected Revision."),
            _(u"Saves the currently selected Revision to the open "
              u"RTK Project database.")
        ]
        _callbacks = [self._do_request_calculate, self._do_request_update]

        _icons = ['calculate', 'save']
        _buttonbox = RTKWorkView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _on_edit(self, index, new_text):
        """
        Method to update the Work View gtk.Widgets() with changes to the
        Revision data model attributes.  This method is called whenever an
        attribute is edited in a different view.

        :param int index: the index in the Revision attributes list of the
                          attribute that was edited.
        :param str new_text: the new text to update the gtk.Widget() with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if index == 17:
            self.txtName.handler_block(self._lst_handler_id[0])
            self.txtName.set_text(new_text)
            self.txtName.handler_unblock(self._lst_handler_id[0])
        elif index == 20:
            _textbuffer = self.txtRemarks.do_get_buffer()
            _textbuffer.handler_block(self._lst_handler_id[1])
            _textbuffer.set_text(new_text)
            _textbuffer.handler_unblock(self._lst_handler_id[1])
        elif index == 22:
            self.txtCode.handler_block(self._lst_handler_id[2])
            self.txtCode.set_text(str(new_text))
            self.txtCode.handler_unblock(self._lst_handler_id[2])

        return _return

    def _on_focus_out(self, entry, __event, index):
        """
        Method to retrieve gtk.Entry() changes and assign the new data to the
        appropriate Revision data model attribute.

        :param gtk.Entry entry: the gtk.Entry() that called the method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the position in the Revision class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _index = -1
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _revision = self._dtc_data_controller.request_select(
                self._revision_id)

            if index == 0:
                _index = 17
                _text = entry.get_text()
                _revision.name = _text
            elif index == 1:
                _index = 20
                _text = self.txtRemarks.do_get_text()
                _revision.remarks = _text
            elif index == 2:
                _index = 22
                _text = entry.get_text()
                _revision.revision_code = _text

            pub.sendMessage(
                'wvwEditedRevision', position=_index, new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_select(self, module_id, **kwargs):
        """
        Method to load the Revision class gtk.Notebook() General Data page
        widgets.

        :param int revision_id: the ID of the newly selected Revision.
        :param str title: the title to display on the Work Book titlebar.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['revision']
        _revision = self._dtc_data_controller.request_select(self._revision_id)

        self.txtTotalCost.set_text(str(locale.currency(_revision.cost)))
        self.txtCostFailure.set_text(
            str(locale.currency(_revision.cost_failure)))
        self.txtCostHour.set_text(str(locale.currency(_revision.cost_hour)))
        self.txtName.set_text(_revision.name)
        _buffer = self.txtRemarks.do_get_buffer()
        _buffer.set_text(_revision.remarks)
        self.txtPartCount.set_text(
            str('{0:0.0f}'.format(_revision.total_part_count)))
        self.txtCode.set_text(str(_revision.revision_code))

        return _return


class AssessmentResults(RTKWorkView):
    """
    The Revision Assessment Results view displays all the assessment results
    for the selected Revision.  The attributes of a Revision Assessment Results
    View are:

    :ivar int _revision_id: the ID of the Revision currently being displayed.
    """

    def __init__(self, controller):
        """
        Method to initialize the Work Book view for the Revision package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKWorkView.__init__(self, controller, module='Revision')

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.pack_end(
            self._make_assessment_results_page(), expand=True, fill=True)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedRevision')

    def _make_assessment_results_page(self):
        """
        Method to create the Revision Work View page for displaying assessment
        results for the selected Revision.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_hbx_page, __, __, __, __, __,
         __) = RTKWorkView._make_assessment_results_page(self)

        return _hbx_page

    def _on_select(self, module_id, **kwargs):
        """
        Method to load the Revision class gtk.Notebook() widgets.

        :param int revision_id: the ID of the newly selected Revision.
        :param str title: the title to display on the Work Book titlebar.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['revision']
        _revision = self._dtc_data_controller.request_select(self._revision_id)

        self.txtAvailability.set_text(
            str(self.fmt.format(_revision.availability_logistics)))
        self.txtMissionAt.set_text(
            str(self.fmt.format(_revision.availability_mission)))
        self.txtActiveHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_active)))
        self.txtDormantHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_dormant)))
        self.txtMissionHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_mission)))
        self.txtPredictedHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_logistics)))
        self.txtSoftwareHt.set_text(
            str(self.fmt.format(_revision.hazard_rate_software)))
        self.txtMMT.set_text(str(self.fmt.format(_revision.mmt)))
        self.txtMCMT.set_text(str(self.fmt.format(_revision.mcmt)))
        self.txtMPMT.set_text(str(self.fmt.format(_revision.mpmt)))
        self.txtMissionMTBF.set_text(
            str(self.fmt.format(_revision.mtbf_mission)))
        self.txtMTBF.set_text(str(self.fmt.format(_revision.mtbf_logistics)))
        self.txtMTTR.set_text(str(self.fmt.format(_revision.mttr)))
        self.txtMissionRt.set_text(
            str(self.fmt.format(_revision.reliability_mission)))
        self.txtReliability.set_text(
            str(self.fmt.format(_revision.reliability_logistics)))

        _title = _(u"RTK Work Book: Revision "
                   u"(Analyzing {0:s})").format(_revision.name)
        RTKWorkView._on_select(self, self._revision_id, title=_title)

        return _return
