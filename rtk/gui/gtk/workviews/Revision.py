# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.Revision.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Revision Package Work View Class
###############################################################################
"""

import locale

# Import other RTK modules.
from .WorkView import RTKWorkView, pub, gtk, rtk, _
# from Assistants import AddRevision


class WorkView(gtk.VBox, RTKWorkView):
    """
    The Work Book view displays all the attributes for the selected Revision.
    The attributes of a Work Book view are:

    :ivar _dtc_revision: the :py:class:`rtk.revision.Revision.Revision` data
                         controller to use with this Work Book.
    :ivar int revision_id: the ID of the Revision currently being displayed.
    :ivar gtk.Entry txtCode: the gtk.Entry() to display/edit the Revision code.
    :ivar gtk.Entry txtName: the gtk.Entry() to display/edit the Revision name.
    :ivar gtk.Entry txtTotalCost: the gtk.Entry() to display the Revision cost.
    :ivar gtk.Entry txtCostFailure: the gtk.Entry() to display the Revision
                                    cost per failure.
    :ivar gtk.Entry txtCostHour: the gtk.Entry() to display the Revision cost
                                 per operating hour.
    :ivar gtk.Entry txtPartCount: the gtk.Entry() to display the numebr of
                                  hardware components comprising the Revision.
    :ivar gtk.Entry txtRemarks: the gtk.Entry() display/edit the Revision
                                remarks.
    :ivar gtk.Entry txtActiveHt: the gtk.Entry() to display the Revision active
                                 hazard rate.
    :ivar gtk.Entry txtDormantHt: the gtk.Entry() to display the Revision
                                  dormant hazard rate.
    :ivar gtk.Entry txtSoftwareHt: the gtk.Entry() to display the Revision
                                   software hazard rate.
    :ivar gtk.Entry txtPredictedHt: the gtk.Entry() to display the Revision
                                    logistics hazard rate.
    :ivar gtk.Entry txtMissionHt: the gtk.Entry() to display the Revision
                                  mission hazard rate.
    :ivar gtk.Entry txtMTBF: the gtk.Entry() display the Revision logistics
                             MTBF.
    :ivar gtk.Entry txtMissionMTBF: the gtk.Entry() display the Revision
                                    mission MTBF.
    :ivar gtk.Entry txtReliability: the gtk.Entry() display the Revision
                                    logistics reliability.
    :ivar gtk.Entry txtMissionRt: the gtk.Entry() display the Revision mission
                                  reliability.
    :ivar gtk.Entry txtMPMT: the gtk.Entry() to display the Revision mean
                             preventive maintenance time.
    :ivar gtk.Entry txtMCMT: the gtk.Entry() display the Revision mean
                             corrective maintenance time.
    :ivar gtk.Entry txtMTTR: the gtk.Entry() to display the Revision mean time
                             to repair.
    :ivar gtk.Entry txtMMT: the gtk.Entry() display the Revision mean
                            maintenance time.
    :ivar gtk.Entry txtAvailability: the gtk.Entry() to display the Revision
                                     logistics availability.
    :ivar gtk.Entry txtMissionAt: the gtk.Entry() to display the Revision
                                  mission availability.
    """

    def __init__(self, controller):
        """
        Method to initialize the Work Book view for the Revision package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.VBox.__init__(self)
        RTKWorkView.__init__(self, controller)

        # Initialize private dictionary attributes.
        self._dic_icons['tab'] = controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/revision.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_revision = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.revision_id = None

        # General data tab widgets.
        self.txtCode = rtk.RTKEntry(tooltip=_(u"A unique code for the "
                                              u"selected Revision."))
        self.txtName = rtk.RTKEntry(tooltip=_(u"The name of the selected "
                                              u"Revision."))
        self.txtTotalCost = rtk.RTKEntry(width=75, editable=False,
                                         tooltip=_(u"Displays the total cost "
                                                   u"of the selected "
                                                   u"Revision."))
        self.txtCostFailure = rtk.RTKEntry(width=75, editable=False,
                                           tooltip=_(u"Displays the cost per "
                                                     u"failure of the "
                                                     u"selected Revision."))
        self.txtCostHour = rtk.RTKEntry(width=75, editable=False,
                                        tooltip=_(u"Displays the failure cost "
                                                  u"per operating hour for "
                                                  u"the selected Revision."))
        self.txtPartCount = rtk.RTKEntry(width=75, editable=False,
                                         tooltip=_(u"Displays the total part "
                                                   u"count for the selected "
                                                   u"Revision."))
        self.txtRemarks = rtk.RTKTextView(gtk.TextBuffer(), width=400,
                                          tooltip=_(u"Enter any remarks "
                                                    u"associated with the "
                                                    u"selected Revision."))

        # Assessment results tab widgets.
        self.txtActiveHt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                        tooltip=_(u"Displays the active "
                                                  u"failure intensity for the "
                                                  u"selected Revision."))
        self.txtDormantHt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the dormant "
                                                   u"failure intensity for "
                                                   u"the selected Revision."))
        self.txtSoftwareHt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                          tooltip=_(u"Displays the software "
                                                    u"failure intensity for "
                                                    u"the selected Revision."))
        self.txtPredictedHt = rtk.RTKEntry(width=125, editable=False,
                                           bold=True,
                                           tooltip=_(u"Displays the predicted "
                                                     u"failure intensity for "
                                                     u"the selected "
                                                     u"Revision.  This is the "
                                                     u"sum of the active, "
                                                     u"dormant, and software "
                                                     u"hazard rates."))
        self.txtMissionHt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the mission "
                                                   u"failure intensity for "
                                                   u"the selected Revision."))
        self.txtMTBF = rtk.RTKEntry(width=125, editable=False, bold=True,
                                    tooltip=_(u"Displays the limiting mean "
                                              u"time between failure (MTBF) "
                                              u"for the selected Revision."))
        self.txtMissionMTBF = rtk.RTKEntry(width=125, editable=False,
                                           bold=True,
                                           tooltip=_(u"Displays the mission "
                                                     u"mean time between "
                                                     u"failure (MTBF) for the "
                                                     u"selected Revision."))
        self.txtReliability = rtk.RTKEntry(width=125, editable=False,
                                           bold=True,
                                           tooltip=_(u"Displays the logistics "
                                                     u"reliability for the "
                                                     u"selected Revision."))
        self.txtMissionRt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the mission "
                                                   u"reliability for the "
                                                   u"selected revision."))
        self.txtMPMT = rtk.RTKEntry(width=125, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean preventive "
                                              u"maintenance time (MPMT) for "
                                              u"the selected Revision."))
        self.txtMCMT = rtk.RTKEntry(width=125, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean corrective "
                                              u"maintenance time (MCMT) for "
                                              u"the selected Revision."))
        self.txtMTTR = rtk.RTKEntry(width=125, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean time to "
                                              u"repair (MTTR) for the "
                                              u"selected Revision."))
        self.txtMMT = rtk.RTKEntry(width=125, editable=False, bold=True,
                                   tooltip=_(u"Displays the mean maintenance "
                                             u"time (MMT) for the selected "
                                             u"revision.  This includes "
                                             u"preventive and corrective "
                                             u"maintenance."))
        self.txtAvailability = rtk.RTKEntry(width=125, editable=False,
                                            bold=True,
                                            tooltip=_(u"Displays the "
                                                      u"logistics "
                                                      u"availability for the "
                                                      u"selected Revision."))
        self.txtMissionAt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the mission "
                                                   u"availability for the "
                                                   u"selected Revision."))

        self._make_general_data_page()
        self._make_assessment_results_page()

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.txtName.connect('focus-out-event',
                                 self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtRemarks.do_get_buffer().connect('changed',
                                                    self._on_focus_out,
                                                    None, 1))
        self._lst_handler_id.append(
            self.txtCode.connect('focus-out-event',
                                 self._on_focus_out, 2))

        self.pack_start(self._make_toolbar(), expand=False)
        self.pack_start(self._notebook)
        self.show_all()

        pub.subscribe(self._on_select, 'selectedRevision')
        pub.subscribe(self._on_select, 'mvw_editedRevision')

    def _make_toolbar(self, hierarchical=False):
        """
        Method to create the gtk.ToolBar() for the Revision class Work View.

        :return: _toolbar
        :rtype: :py:class:`gtk.ToolBar`
        """

        _position = 6

        _toolbar = RTKWorkView._make_toolbar(self, hierarchical)

        _button = _toolbar.get_nth_item(0)
        _button.set_tooltip_text(_(u"Adds a new Revision to the open RTK "
                                   u"Program database."))
        _button.connect('clicked', self._request_insert)

        _button = _toolbar.get_nth_item(1)
        _button.set_tooltip_text(_(u"Removes the currently selected Revision "
                                   u"from the open RTK Project database."))
        _button.connect('clicked', self._request_delete)

        _button = _toolbar.get_nth_item(3)
        _button.set_tooltip_text(_(u"Calculate the currently selected "
                                   u"Revision."))
        _button.connect('clicked', self._request_calculate)

        _button = _toolbar.get_nth_item(5)
        _button.set_tooltip_text(_(u"Saves the currently selected Revision "
                                   u"to the open RTK Project database."))
        _button.connect('clicked', self._request_save)

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Create report button.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(_(u"Create Revision reports."))
        _image = gtk.Image()
        _image.set_from_file(self._dic_icons['reports'])
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Mission and Environmental "
                                          u"Profile"))
        _menu_item.set_tooltip_text(_(u"Creates the mission and environmental "
                                      u"profile report for the currently "
                                      u"selected revision."))
        # _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Failure Definition"))
        _menu_item.set_tooltip_text(_(u"Creates the failure definition report "
                                      u"for the currently selected revision."))
        # _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _make_assessment_results_page(self):
        """
        Method to create the Revision Work View page for displaying assessment
        results for the selected Revision.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_hbx_page,
         _fxd_left,
         _fxd_right) = RTKWorkView._make_assessment_results_page()

        _labels = [_(u"Active Failure Intensity [\u039B(t)]:"),
                   _(u"Dormant \u039B(t):"), _(u"Software \u039B(t):"),
                   _(u"Predicted \u039B(t):"), _(u"Mission \u039B(t):"),
                   _(u"Mean Time Between Failure [MTBF]:"),
                   _(u"Mission MTBF:"), _(u"Reliability [R(t)]:"),
                   _(u"Mission R(t):")]
        _x_pos, _y_pos = rtk.make_label_group(_labels, _fxd_left, 5, 5)
        _x_pos += 55

        _fxd_left.put(self.txtActiveHt, _x_pos, _y_pos[0])
        _fxd_left.put(self.txtDormantHt, _x_pos, _y_pos[1])
        _fxd_left.put(self.txtSoftwareHt, _x_pos, _y_pos[2])
        _fxd_left.put(self.txtPredictedHt, _x_pos, _y_pos[3])
        _fxd_left.put(self.txtMissionHt, _x_pos, _y_pos[4])
        _fxd_left.put(self.txtMTBF, _x_pos, _y_pos[5])
        _fxd_left.put(self.txtMissionMTBF, _x_pos, _y_pos[6])
        _fxd_left.put(self.txtReliability, _x_pos, _y_pos[7])
        _fxd_left.put(self.txtMissionRt, _x_pos, _y_pos[8])

        _fxd_left.show_all()

        _labels = [_(u"Mean Preventive Maintenance Time [MPMT]:"),
                   _(u"Mean Corrective Maintenance Time [MCMT]:"),
                   _(u"Mean Time to Repair [MTTR]:"),
                   _(u"Mean Maintenance Time [MMT]:"),
                   _(u"Availability [A(t)]:"), _(u"Mission A(t):")]
        _x_pos, _y_pos = rtk.make_label_group(_labels, _fxd_right, 5, 5)
        _x_pos += 55

        _fxd_right.put(self.txtMPMT, _x_pos, _y_pos[0])
        _fxd_right.put(self.txtMCMT, _x_pos, _y_pos[1])
        _fxd_right.put(self.txtMTTR, _x_pos, _y_pos[2])
        _fxd_right.put(self.txtMMT, _x_pos, _y_pos[3])
        _fxd_right.put(self.txtAvailability, _x_pos, _y_pos[4])
        _fxd_right.put(self.txtMissionAt, _x_pos, _y_pos[5])

        _fxd_right.show_all()

        _label = rtk.RTKLabel(_(u"Assessment\nResults"), width=-1, height=-1,
                              justify=gtk.JUSTIFY_CENTER,
                              tooltip=_(u"Displays reliability, "
                                        u"maintainability, and availability "
                                        u"assessment results for the selected "
                                        u"Revision."))
        self._notebook.insert_page(_hbx_page, tab_label=_label, position=-1)

        return False

    def _make_general_data_page(self):
        """
        Method to create the Revision Work Book page for displaying general
        data about the selected Revision.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _frame, _fixed = RTKWorkView._make_general_data_page()

        _labels = [_(u"Revision Code:"), _(u"Revision Name:"),
                   _(u"Total Cost:"), _(u"Cost/Failure:"),
                   _(u"Cost/Hour:"), _(u"Total Part Count:"),
                   _(u"Remarks:")]
        _x_pos, _y_pos = rtk.make_label_group(_labels, _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtTotalCost, _x_pos, _y_pos[2])
        _fixed.put(self.txtCostFailure, _x_pos, _y_pos[3])
        _fixed.put(self.txtCostHour, _x_pos, _y_pos[4])
        _fixed.put(self.txtPartCount, _x_pos, _y_pos[5])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[6])

        _fixed.show_all()

        _label = rtk.RTKLabel(_(u"General\nData"), width=-1,
                              justify=gtk.JUSTIFY_CENTER,
                              tooltip=_(u"Displays general information for "
                                        u"the selected Revision."))
        self._notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _on_select(self, revision_id):
        """
        Method to load the Revision class gtk.Notebook() widgets.

        :param int revision_id: the Revision ID of the selected/edited
                                Revision.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._dtc_revision = self._mdcRTK.dic_controllers['revision']
        _revision = self._dtc_revision.request_select(revision_id)

        self.revision_id = _revision.revision_id

        # Load the General Data page.
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

        # Load the Assessment Results page.
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
        _workview = self.get_parent()
        _workview.set_title(_title)

        return False

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
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        self._dtc_revision = self._mdcRTK.dic_controllers['revision']
        if self._dtc_revision is not None:
            _revision = self._dtc_revision.request_select(self.revision_id)

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

            pub.sendMessage('wvw_editedRevision', position=_index,
                            new_text=_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _request_calculate(self, __button):
        """
        Method to send request to calculate the selected revision to the
        Revision data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code = 0
        _msg = ['', '', '']

        if self._dtc_revision.request_calculate_reliability(
                self.revision_id, self._mission_time):
            _error_code = 1
            _msg[0] = 'Error calculating reliability attributes.'

        if self._dtc_revision.request_calculate_availability(self.revision_id):
            _error_code = 1
            _msg[1] = 'Error calculating availability attributes.'

        if self._dtc_revision.request_calculate_costs(
                self.revision_id, self._mission_time):
            _error_code = 1
            _msg[2] = 'Error calculating cost attributes.'

        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to calculate "
                        u"Revision {0:d}. \n\n\t" +
                        _msg[0] + "\n\t" +
                        _msg[1] + "\n\t" +
                        _msg[2] + "\n\n").format(self.revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _request_delete(self, __button):
        """
        Method to send request to delete the selected revision from the
        Revision data controller.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _prompt = _(u"You are about to delete Revision {0:d} and all data "
                    u"associated with it.  Is this really what you want "
                    u"to do?").format(self.revision_id)
        _dialog = rtk.RTKMessageDialog(_prompt, self._dic_icons['question'],
                                       'question')
        _response = _dialog.do_run()

        if _response == gtk.RESPONSE_YES:
            _dialog.do_destroy()
            if self._dtc_revision.request_delete(self.revision_id):
                _prompt = _(u"An error occurred when attempting to delete "
                            u"Revision {0:d}.").format(self.revision_id)
                _dialog = rtk.RTKMessageDialog(_prompt,
                                               self._dic_icons['error'],
                                               'error')
                _dialog.do_run()
                _dialog.do_destroy()
                _return = True
        else:
            _dialog.do_destroy()

        return _return

    def _request_insert(self, __button):
        """
        Method to send request to insert a new Revision into the RTK Program
        database.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False
        # TODO: This method should launch a wizard to assist the user in adding a new Revision.
        if self._dtc_revision.request_insert():
            _prompt = _(u"An error occurred while attempting to add a new "
                        u"Revision.")
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _request_save(self, __button):
        """
        Method to send request to save the selected revision to the Revision
        data controller.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if self._dtc_revision.request_update(self.revision_id):
            _prompt = _(u"An error occurred while attempting to save "
                        u"Revision {0:d}.").format(self.revision_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return
