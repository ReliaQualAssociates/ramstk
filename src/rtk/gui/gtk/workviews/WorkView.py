# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.WorkView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RAMSTKWorkView Meta-Class Module."""

from pubsub import pub

# Import other RAMSTK modules.
from rtk.gui.gtk.rtk.Widget import _, gtk
from rtk.gui.gtk import rtk


class RAMSTKWorkView(gtk.HBox, rtk.RAMSTKBaseView):
    """
    class to display data in the RAMSTK Work Book.

    This is the meta class for all RAMSTK Work View classes.  Attributes of the
    RAMSTKWorkView are:

    :ivar list _lst_gendata_labels: the labels to use on the General Data page.
    :ivar list _lst_assess_labels: the labels to use on the Assessment Results
                                   page.
    :ivar str _module: the RAMSTK module the RAMSTKWorkView is associated with.
    :ivar txtCode: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                   RAMSTK module code.
    :ivar txtName: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the RAMSTK
                   module name or description.
    :ivar txtRemarks: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display any
                      remarks associated with the RAMSTK module.
    :ivar txtActiveHt: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                       active hazard rate.
    :ivar txtDormantHt: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                        dormant hazard rate.
    :ivar txtSoftwareHt: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display
                         the software hazard rate.
    :ivar txtPredictedHt: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display
                          the predicted (logistics) hazard rate.
    :ivar txtMissionHt: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                        mission hazard rate.
    :ivar txtMTBF: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                   predicted (logistics) MTBF>
    :ivar txtMissionMTBF: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display
                          the mission MTBF.
    :ivar txtReliability: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display
                          the predicted (logistics) reliability.
    :ivar txtMissionRt: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                        mission reliability.
    :ivar txtMPMT: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                   mean preventive maintenance time (MPMT).
    :ivar txtMCMT: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                   mean corrective maintenance time (MCMT).
    :ivar txtMTTR: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                   men time to repair (MTTR).
    :ivar txtMMT: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                  the mean maintenance time (MMT).
    :ivar txtAvailability: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display
                           the predicted (logistics) availability.
    :ivar txtMissionAt: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                        mission availability.
    :ivar txtPartCount: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                        total part count for the RAMSTK module.
    :ivar txtTotalCost: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                        total cost of the RAMSTK module.
    :ivar txtCostFailure: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display
                          the cost/failure of the RAMSTK module.
    :ivar txtCostHour: the :class:`rtk.gui.gtk.rtk.RAMSTKEntry` to display the
                       cost/operating hour for the RAMSTK module.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the RAMSTKWorkView meta-class.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`rtk.RAMSTK.RAMSTK`
        :keyword str module: the RAMSTK Module this RAMSTKWorkView is the bassis for.
        """
        _module = kwargs['module']
        gtk.HBox.__init__(self)
        rtk.RAMSTKBaseView.__init__(self, controller, module=_module)

        self._module = None
        for __, char in enumerate(_module):
            if char.isalpha():
                self._module = _module.capitalize()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_gendata_labels = [
            _(u"{0:s} Code:").format(self._module),
            _(u"{0:s} Name:").format(self._module),
            _(u"Remarks:")
        ]
        """
        There are three labels that will appear on all General Data pages.
        Insert additional, WorkView specific labels into this list starting at
        position 2.  In the __init__() method for the WorkView requiring
        specific labels, do something like the following:

            self._lst_gendata_labels.insert(1, _(u"Specific Label:"))

        This will ensure the Remarks widget is always at the bottom of the row
        of General Data page widgets.  This, then, ensures WorkView specific
        widgets don't overlap the Remarks widget.
        """

        self._lst_assess_labels = [[
            _(u"Active Failure Intensity [\u039B(t)]:"),
            _(u"Dormant \u039B(t):"),
            _(u"Software \u039B(t):"),
            _(u"Predicted h(t):"),
            _(u"Mission h(t):"),
            _(u"MTBF:"),
            _(u"Mission MTBF:"),
            _(u"Reliability [R(t)]:"),
            _(u"Mission R(t):"),
            _(u"Total Parts:")
        ], [
            _(u"Mean Preventive Maintenance Time [MPMT]:"),
            _(u"Mean Corrective Maintenance Time [MCMT]:"),
            _(u"Mean Time to Repair [MTTR]:"),
            _(u"Mean Maintenance Time [MMT]:"),
            _(u"Availability [A(t)]:"),
            _(u"Mission A(t):"),
            _(u"Total Cost:"),
            _(u"Cost/Failure:"),
            _(u"Cost/Hour:")
        ]]
        """
        There are 10 labels that will appear in the left half and nine labels
        that will appear in the right half of all Assessment Results pages.
        Append additional, WorkView specific labels onto this list.  In the
        __init__() method for the WorkView requiring specific labels, do
        something like the following:

            self._lst_assess_labels[0].append(_(u"Specific Label:"))
        """

        # Initialize private scalar attributes.
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtCode = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"A unique code for the "
                      u"selected {0:s}.").format(self._module))
        self.txtName = rtk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The name of the selected "
                      u"{0:s}.").format(self._module))
        self.txtRemarks = rtk.RAMSTKTextView(
            gtk.TextBuffer(),
            width=400,
            tooltip=_(u"Enter any remarks "
                      u"associated with the "
                      u"selected {0:s}.").format(self._module))

        self.txtActiveHt = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the active "
                      u"failure intensity for the "
                      u"selected {0:s}.").format(self._module))
        self.txtDormantHt = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the dormant "
                      u"failure intensity for "
                      u"the selected {0:s}.").format(self._module))
        self.txtSoftwareHt = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the software "
                      u"failure intensity for "
                      u"the selected {0:s}.").format(self._module))
        self.txtPredictedHt = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics "
                      u"failure intensity for "
                      u"the selected {0:s}.  "
                      u"This is the sum of the "
                      u"active, dormant, and "
                      u"software hazard "
                      u"rates.").format(self._module))
        self.txtMissionHt = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission "
                      u"failure intensity for "
                      u"the selected {0:s}.").format(self._module))
        self.txtMTBF = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics mean "
                      u"time between failure (MTBF) "
                      u"for the selected {0:s}.").format(self._module))
        self.txtMissionMTBF = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission "
                      u"mean time between "
                      u"failure (MTBF) for the "
                      u"selected {0:s}.").format(self._module))
        self.txtReliability = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the logistics "
                      u"reliability for the "
                      u"selected {0:s}.").format(self._module))
        self.txtMissionRt = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission "
                      u"reliability for the "
                      u"selected {0:s}.").format(self._module))

        self.txtMPMT = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean preventive "
                      u"maintenance time (MPMT) for "
                      u"the selected {0:s}.").format(self._module))
        self.txtMCMT = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean corrective "
                      u"maintenance time (MCMT) for "
                      u"the selected {0:s}.").format(self._module))
        self.txtMTTR = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean time to "
                      u"repair (MTTR) for the "
                      u"selected {0:s}.").format(self._module))
        self.txtMMT = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mean maintenance "
                      u"time (MMT) for the selected "
                      u"{0:s}.  This includes "
                      u"preventive and corrective "
                      u"maintenance.").format(self._module))
        self.txtAvailability = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the "
                      u"logistics "
                      u"availability for the "
                      u"selected {0:s}.").format(self._module))
        self.txtMissionAt = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"Displays the mission "
                      u"availability for the "
                      u"selected {0:s}.").format(self._module))
        self.txtPartCount = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the total part "
                      u"count for the selected "
                      u"{0:s}.").format(self._module))
        self.txtTotalCost = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the total cost "
                      u"of the selected "
                      u"{0:s}.").format(self._module))
        self.txtCostFailure = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the cost per "
                      u"failure of the "
                      u"selected {0:s}.").format(self._module))
        self.txtCostHour = rtk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_(u"Displays the failure cost "
                      u"per operating hour for "
                      u"the selected {0:s}.").format(self._module))

        pub.subscribe(self._on_select_revision, 'selectedRevision')

    def _make_assessment_results_page(self):
        """
        Create the gtk.Notebook() page for displaying assessment results.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
        _hbox = gtk.HBox()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the left half of the page.                                    #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fxd_left = gtk.Fixed()

        _scrollwindow = rtk.RAMSTKScrolledWindow(_fxd_left)
        _frame = rtk.RAMSTKFrame(label=_(u"Reliability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame)

        _x_pos_l, _y_pos_l = rtk.make_label_group(self._lst_assess_labels[0],
                                                  _fxd_left, 5, 5)
        _x_pos_l += 50

        _fxd_left.put(self.txtActiveHt, _x_pos_l, _y_pos_l[0])
        _fxd_left.put(self.txtDormantHt, _x_pos_l, _y_pos_l[1])
        _fxd_left.put(self.txtSoftwareHt, _x_pos_l, _y_pos_l[2])
        _fxd_left.put(self.txtPredictedHt, _x_pos_l, _y_pos_l[3])
        _fxd_left.put(self.txtMissionHt, _x_pos_l, _y_pos_l[4])
        _fxd_left.put(self.txtMTBF, _x_pos_l, _y_pos_l[5])
        _fxd_left.put(self.txtMissionMTBF, _x_pos_l, _y_pos_l[6])
        _fxd_left.put(self.txtReliability, _x_pos_l, _y_pos_l[7])
        _fxd_left.put(self.txtMissionRt, _x_pos_l, _y_pos_l[8])
        _fxd_left.put(self.txtPartCount, _x_pos_l, _y_pos_l[9])

        _fxd_left.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the right half of the page.                                   #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fxd_right = gtk.Fixed()

        _scrollwindow = rtk.RAMSTKScrolledWindow(_fxd_right)
        _frame = rtk.RAMSTKFrame(label=_(u"Maintainability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame)

        _x_pos_r, _y_pos_r = rtk.make_label_group(self._lst_assess_labels[1],
                                                  _fxd_right, 5, 5)
        _x_pos_r += 55

        _fxd_right.put(self.txtMPMT, _x_pos_r, _y_pos_r[0])
        _fxd_right.put(self.txtMCMT, _x_pos_r, _y_pos_r[1])
        _fxd_right.put(self.txtMTTR, _x_pos_r, _y_pos_r[2])
        _fxd_right.put(self.txtMMT, _x_pos_r, _y_pos_r[3])
        _fxd_right.put(self.txtAvailability, _x_pos_r, _y_pos_r[4])
        _fxd_right.put(self.txtMissionAt, _x_pos_r, _y_pos_r[5])
        _fxd_right.put(self.txtTotalCost, _x_pos_r, _y_pos_r[6])
        _fxd_right.put(self.txtCostFailure, _x_pos_r, _y_pos_r[7])
        _fxd_right.put(self.txtCostHour, _x_pos_r, _y_pos_r[8])

        _fxd_right.show_all()

        _label = rtk.RAMSTKLabel(
            _(u"Assessment\nResults"),
            height=30,
            width=-1,
            justify=gtk.JUSTIFY_CENTER,
            tooltip=_(u"Displays reliability, "
                      u"maintainability, and availability "
                      u"assessment results for the selected "
                      u"{0:s}.").format(self._module))
        self.hbx_tab_label.pack_start(_label)

        return (_hbox, _fxd_left, _fxd_right, _x_pos_l, _x_pos_r, _y_pos_l,
                _y_pos_r)

    def on_select(self, **kwargs):
        """
        Respond to load the Work View gtk.Notebook() widgets.

        This method handles the results of the an individual module's
        _on_select() method.  It sets the title of the RAMSTK Work Book and
        raises an error dialog if needed.

        :return: None
        :rtype: None
        """
        _title = kwargs['title']
        _error_code = kwargs['error_code']
        _user_msg = kwargs['user_msg']
        _debug_msg = kwargs['debug_msg']

        try:
            _workbook = self.get_parent().get_parent()
            _workbook.set_title(_title)
        except AttributeError:
            pass

        if _error_code != 0:
            self._mdcRAMSTK.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                _debug_msg)
            _dialog = rtk.RAMSTKMessageDialog(
                _user_msg, self._dic_icons['error'], 'error')
            if _dialog.do_run() == gtk.RESPONSE_OK:
                _dialog.destroy()

        return None

    def _on_select_revision(self, **kwargs):
        """
        Respond to the `selectedRevision` signal from pypubsub.

        :return: None
        :rtype: None
        """
        self._revision_id = kwargs['module_id']

        return None
