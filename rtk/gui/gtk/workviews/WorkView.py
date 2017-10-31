# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.WorkView.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
RTK Work View Package Meta Class
###############################################################################
"""

# Import other RTK modules.
from gui.gtk.rtk.Widget import _, gtk           # pylint: disable=E0401,W0611
from gui.gtk import rtk                         # pylint: disable=E0401,W0611


class RTKWorkView(gtk.HBox, rtk.RTKBaseView):
    """
    This is the meta class for all RTK Work View classes.  Attributes of the
    RTKWorkView are:
    """

    def __init__(self, controller, **kwargs):
        """
        Method to initialize the Work View.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.HBox.__init__(self)
        rtk.RTKBaseView.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._module = kwargs['module']

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()

        self.txtActiveHt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                        tooltip=_(u"Displays the active "
                                                  u"failure intensity for the "
                                                  u"selected {0:s}.").
                                        format(self._module))
        self.txtDormantHt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the dormant "
                                                   u"failure intensity for "
                                                   u"the selected {0:s}.").
                                         format(self._module))
        self.txtSoftwareHt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                          tooltip=_(u"Displays the software "
                                                    u"failure intensity for "
                                                    u"the selected {0:s}.").
                                          format(self._module))
        self.txtPredictedHt = rtk.RTKEntry(width=125, editable=False,
                                           bold=True,
                                           tooltip=_(u"Displays the logistics "
                                                     u"failure intensity for "
                                                     u"the selected {0:s}.  "
                                                     u"This is the sum of the "
                                                     u"active, dormant, and "
                                                     u"software hazard "
                                                     u"rates.").
                                           format(self._module))
        self.txtMissionHt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the mission "
                                                   u"failure intensity for "
                                                   u"the selected {0:s}.").
                                         format(self._module))
        self.txtMTBF = rtk.RTKEntry(width=125, editable=False, bold=True,
                                    tooltip=_(u"Displays the logistics mean "
                                              u"time between failure (MTBF) "
                                              u"for the selected {0:s}.").
                                    format(self._module))
        self.txtMissionMTBF = rtk.RTKEntry(width=125, editable=False,
                                           bold=True,
                                           tooltip=_(u"Displays the mission "
                                                     u"mean time between "
                                                     u"failure (MTBF) for the "
                                                     u"selected {0:s}.").
                                           format(self._module))
        self.txtReliability = rtk.RTKEntry(width=125, editable=False,
                                           bold=True,
                                           tooltip=_(u"Displays the logistics "
                                                     u"reliability for the "
                                                     u"selected {0:s}.").
                                           format(self._module))
        self.txtMissionRt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the mission "
                                                   u"reliability for the "
                                                   u"selected {0:s}.").
                                         format(self._module))

        self.txtMPMT = rtk.RTKEntry(width=125, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean preventive "
                                              u"maintenance time (MPMT) for "
                                              u"the selected {0:s}.").
                                    format(self._module))
        self.txtMCMT = rtk.RTKEntry(width=125, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean corrective "
                                              u"maintenance time (MCMT) for "
                                              u"the selected {0:s}.").
                                    format(self._module))
        self.txtMTTR = rtk.RTKEntry(width=125, editable=False, bold=True,
                                    tooltip=_(u"Displays the mean time to "
                                              u"repair (MTTR) for the "
                                              u"selected {0:s}.").
                                    format(self._module))
        self.txtMMT = rtk.RTKEntry(width=125, editable=False, bold=True,
                                   tooltip=_(u"Displays the mean maintenance "
                                             u"time (MMT) for the selected "
                                             u"{0:s}.  This includes "
                                             u"preventive and corrective "
                                             u"maintenance.").
                                   format(self._module))
        self.txtAvailability = rtk.RTKEntry(width=125, editable=False,
                                            bold=True,
                                            tooltip=_(u"Displays the "
                                                      u"logistics "
                                                      u"availability for the "
                                                      u"selected {0:s}.").
                                            format(self._module))
        self.txtMissionAt = rtk.RTKEntry(width=125, editable=False, bold=True,
                                         tooltip=_(u"Displays the mission "
                                                   u"availability for the "
                                                   u"selected {0:s}.").
                                         format(self._module))

    def _make_assessment_results_page(self):
        """
        Method to create the gtk.Notebook() page for displaying assessment
        results.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _hbox = gtk.HBox()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the left half of the page.                                    #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fxd_left = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fxd_left)
        _frame = rtk.RTKFrame(label=_(u"Reliability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        _labels = [_(u"Active Failure Intensity [\u039B(t)]:"),
                   _(u"Dormant \u039B(t):"), _(u"Software \u039B(t):"),
                   _(u"Predicted h(t):"), _(u"Mission h(t):"), _(u"MTBF:"),
                   _(u"Mission MTBF:"), _(u"Reliability [R(t)]:"),
                   _(u"Mission R(t):")]
        _x_pos_l, _y_pos = rtk.make_label_group(_labels, _fxd_left, 5, 5)
        _x_pos_l += 50

        _fxd_left.put(self.txtActiveHt, _x_pos_l, _y_pos[0])
        _fxd_left.put(self.txtDormantHt, _x_pos_l, _y_pos[1])
        _fxd_left.put(self.txtSoftwareHt, _x_pos_l, _y_pos[2])
        _fxd_left.put(self.txtPredictedHt, _x_pos_l, _y_pos[3])
        _fxd_left.put(self.txtMissionHt, _x_pos_l, _y_pos[4])
        _fxd_left.put(self.txtMTBF, _x_pos_l, _y_pos[5])
        _fxd_left.put(self.txtMissionMTBF, _x_pos_l, _y_pos[6])
        _fxd_left.put(self.txtReliability, _x_pos_l, _y_pos[7])
        _fxd_left.put(self.txtMissionRt, _x_pos_l, _y_pos[8])

        _fxd_left.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the right half of the page.                                   #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fxd_right = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fxd_right)
        _frame = rtk.RTKFrame(label=_(u"Maintainability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame)

        _labels = [_(u"Mean Preventive Maintenance Time [MPMT]:"),
                   _(u"Mean Corrective Maintenance Time [MCMT]:"),
                   _(u"Mean Time to Repair [MTTR]:"),
                   _(u"Mean Maintenance Time [MMT]:"),
                   _(u"Availability [A(t)]:"), _(u"Mission A(t):")]
        _x_pos_r, _y_pos = rtk.make_label_group(_labels, _fxd_right, 5, 5)
        _x_pos_r += 55

        _fxd_right.put(self.txtMPMT, _x_pos_r, _y_pos[0])
        _fxd_right.put(self.txtMCMT, _x_pos_r, _y_pos[1])
        _fxd_right.put(self.txtMTTR, _x_pos_r, _y_pos[2])
        _fxd_right.put(self.txtMMT, _x_pos_r, _y_pos[3])
        _fxd_right.put(self.txtAvailability, _x_pos_r, _y_pos[4])
        _fxd_right.put(self.txtMissionAt, _x_pos_r, _y_pos[5])

        _fxd_right.show_all()

        _label = rtk.RTKLabel(_(u"Assessment\nResults"), height=30, width=-1,
                              justify=gtk.JUSTIFY_CENTER,
                              tooltip=_(u"Displays reliability, "
                                        u"maintainability, and availability "
                                        u"assessment results for the selected "
                                        u"{0:s}.").format(self._module))
        self.hbx_tab_label.pack_start(_label)

        return _hbox, _fxd_left, _fxd_right, _x_pos_l, _x_pos_r

    @staticmethod
    def _make_general_data_page():
        """
        Method to create the gtk.Notebook() page for displaying general data.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _frame = rtk.RTKFrame(label=_(u"General Information"))

        _fixed = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fixed)
        _frame.add(_scrollwindow)

        return _frame, _fixed

    def _on_select(self, module_id, **kwargs):  # pylint: disable=W0613
        """
        Method to respond load the Work View gtk.Notebook() widgets.

        :param int revision_id: the ID of the newly selected Revision.
        :param str title: the title to display on the Work Book titlebar.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _title = kwargs['title']

        _workbook = self.get_parent().get_parent()
        _workbook.set_title(_title)

        return _return
