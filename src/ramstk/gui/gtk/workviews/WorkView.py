# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.WorkView.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTKWorkView Meta-Class Module."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk.ramstk.Widget import _, GObject, Gtk
from ramstk.gui.gtk import ramstk


class RAMSTKWorkView(Gtk.HBox, ramstk.RAMSTKBaseView):
    """
    Class to display data in the RAMSTK Work Book.

    This is the meta class for all RAMSTK Work View classes.  Attributes of the
    RAMSTKWorkView are:

    :ivar list _lst_gendata_labels: the labels to use on the General Data page.
    :ivar list _lst_assess_labels: the labels to use on the Assessment Results
                                   page.
    :ivar str _module: the RAMSTK module the RAMSTKWorkView is associated with.
    :ivar txtCode: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to display
                   the RAMSTK module code.
    :ivar txtName: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to display
                   the RAMSTK module name or description.
    :ivar txtRemarks: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to display
                      any remarks associated with the RAMSTK module.
    :ivar txtActiveHt: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                       display the active hazard rate.
    :ivar txtDormantHt: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the dormant hazard rate.
    :ivar txtSoftwareHt: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                         display the software hazard rate.
    :ivar txtPredictedHt: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                          display the predicted (logistics) hazard rate.
    :ivar txtMissionHt: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the mission hazard rate.
    :ivar txtMTBF: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to display
                   the predicted (logistics) MTBF>
    :ivar txtMissionMTBF: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                          display the mission MTBF.
    :ivar txtReliability: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                          display the predicted (logistics) reliability.
    :ivar txtMissionRt: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the mission reliability.
    :ivar txtMPMT: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to display
                   the mean preventive maintenance time (MPMT).
    :ivar txtMCMT: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to display
                   the mean corrective maintenance time (MCMT).
    :ivar txtMTTR: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to display
                   the men time to repair (MTTR).
    :ivar txtMMT: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to display the
                  the mean maintenance time (MMT).
    :ivar txtAvailability: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                           display the predicted (logistics) availability.
    :ivar txtMissionAt: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the mission availability.
    :ivar txtPartCount: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the total part count for the RAMSTK module.
    :ivar txtTotalCost: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                        display the total cost of the RAMSTK module.
    :ivar txtCostFailure: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                          display the cost/failure of the RAMSTK module.
    :ivar txtCostHour: the :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` to
                       display the cost/operating hour for the RAMSTK module.
    """

    def __init__(self, controller, **kwargs):
        """
        Initialize the RAMSTKWorkView meta-class.

        :param controller: the RAMSTK master data controller instance.
        :type controller: :class:`ramstk.RAMSTK.RAMSTK`
        """
        _module = kwargs['module']
        GObject.GObject.__init__(self)
        ramstk.RAMSTKBaseView.__init__(self, controller, module=_module)

        self._module = None
        for __, char in enumerate(_module):
            if char.isalpha():
                self._module = _module.capitalize()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_gendata_labels = [
            _("{0:s} Code:").format(self._module),
            _("{0:s} Name:").format(self._module),
            _("Remarks:")
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
        self._lst_assess_labels = [
            [
                _("Active Failure Intensity [\u039B(t)]:"),
                _("Dormant \u039B(t):"),
                _("Software \u039B(t):"),
                _("Predicted h(t):"),
                _("Mission h(t):"),
                _("MTBF:"),
                _("Mission MTBF:"),
                _("Reliability [R(t)]:"),
                _("Mission R(t):"),
                _("Total Parts:")
            ],
            [
                _("Mean Preventive Maintenance Time [MPMT]:"),
                _("Mean Corrective Maintenance Time [MCMT]:"),
                _("Mean Time to Repair [MTTR]:"),
                _("Mean Maintenance Time [MMT]:"),
                _("Availability [A(t)]:"),
                _("Mission A(t):"),
                _("Total Cost:"),
                _("Cost/Failure:"),
                _("Cost/Hour:")
            ]
        ]
        """
        There are 10 labels that will appear in the left half and nine labels
        that will appear in the right half of all Assessment Results pages.
        Append additional, WorkView specific labels onto this list.  In the
        __init__() method for the WorkView requiring specific labels, do
        something like the following:

            self._lst_assess_labels[0].append(_(u"Specific Label:"))
        """

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtCode = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_("A unique code for the "
                      "selected {0:s}.").format(self._module))
        self.txtName = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_("The name of the selected "
                      "{0:s}.").format(self._module))
        self.txtRemarks = ramstk.RAMSTKTextView(
            Gtk.TextBuffer(),
            width=400,
            tooltip=_("Enter any remarks "
                      "associated with the "
                      "selected {0:s}.").format(self._module))

        self.txtActiveHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the active "
                      "failure intensity for the "
                      "selected {0:s}.").format(self._module))
        self.txtDormantHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the dormant "
                      "failure intensity for "
                      "the selected {0:s}.").format(self._module))
        self.txtSoftwareHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the software "
                      "failure intensity for "
                      "the selected {0:s}.").format(self._module))
        self.txtPredictedHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the logistics "
                      "failure intensity for "
                      "the selected {0:s}.  "
                      "This is the sum of the "
                      "active, dormant, and "
                      "software hazard "
                      "rates.").format(self._module))
        self.txtMissionHt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the mission "
                      "failure intensity for "
                      "the selected {0:s}.").format(self._module))
        self.txtMTBF = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the logistics mean "
                      "time between failure (MTBF) "
                      "for the selected {0:s}.").format(self._module))
        self.txtMissionMTBF = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the mission "
                      "mean time between "
                      "failure (MTBF) for the "
                      "selected {0:s}.").format(self._module))
        self.txtReliability = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the logistics "
                      "reliability for the "
                      "selected {0:s}.").format(self._module))
        self.txtMissionRt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the mission "
                      "reliability for the "
                      "selected {0:s}.").format(self._module))

        self.txtMPMT = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the mean preventive "
                      "maintenance time (MPMT) for "
                      "the selected {0:s}.").format(self._module))
        self.txtMCMT = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the mean corrective "
                      "maintenance time (MCMT) for "
                      "the selected {0:s}.").format(self._module))
        self.txtMTTR = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the mean time to "
                      "repair (MTTR) for the "
                      "selected {0:s}.").format(self._module))
        self.txtMMT = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the mean maintenance "
                      "time (MMT) for the selected "
                      "{0:s}.  This includes "
                      "preventive and corrective "
                      "maintenance.").format(self._module))
        self.txtAvailability = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the "
                      "logistics "
                      "availability for the "
                      "selected {0:s}.").format(self._module))
        self.txtMissionAt = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("Displays the mission "
                      "availability for the "
                      "selected {0:s}.").format(self._module))
        self.txtPartCount = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_("Displays the total part "
                      "count for the selected "
                      "{0:s}.").format(self._module))
        self.txtTotalCost = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_("Displays the total cost "
                      "of the selected "
                      "{0:s}.").format(self._module))
        self.txtCostFailure = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_("Displays the cost per "
                      "failure of the "
                      "selected {0:s}.").format(self._module))
        self.txtCostHour = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            tooltip=_("Displays the failure cost "
                      "per operating hour for "
                      "the selected {0:s}.").format(self._module))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_select_revision, 'selectedRevision')

    def _make_assessment_results_page(self):
        """
        Create the Gtk.Notebook() page for displaying assessment results.

        :return: (_hbox, _fxd_left, _fxd_right, _x_pos_l, _x_pos_r, _y_pos_l,
                  _y_pos_r)
        :rtype: tuple
        """
        _hbox = Gtk.HBox()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the left half of the page.                                    #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fxd_left = Gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fxd_left)
        _frame = ramstk.RAMSTKFrame(label=_("Reliability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame, True, True, 0)

        _x_pos_l, _y_pos_l = ramstk.make_label_group(
            self._lst_assess_labels[0], _fxd_left, 5, 5)
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
        _fxd_right = Gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fxd_right)
        _frame = ramstk.RAMSTKFrame(label=_("Maintainability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True, 0)

        _x_pos_r, _y_pos_r = ramstk.make_label_group(
            self._lst_assess_labels[1], _fxd_right, 5, 5)
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

        _label = ramstk.RAMSTKLabel(
            _("Assessment\nResults"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays reliability, "
                      "maintainability, and availability "
                      "assessment results for the selected "
                      "{0:s}.").format(self._module))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        return (_hbox, _fxd_left, _fxd_right, _x_pos_l, _x_pos_r, _y_pos_l,
                _y_pos_r)

    def make_general_data_page(self):
        """
        Create the Gtk.Notebook() page for displaying general data.

        :return: (_frame, _fixed, _x_pos, _y_pos); the :class:`Gtk.Frame` and
                 :class:`Gtk.Fixed` used to make the General Data page.
        :rtype: tuple
        """
        _fixed = Gtk.Fixed()

        _scrollwindow = ramstk.RAMSTKScrolledWindow(_fixed)
        _frame = ramstk.RAMSTKFrame(label=_("General Information"))
        _frame.add(_scrollwindow)

        _x_pos, _y_pos = ramstk.make_label_group(self._lst_gendata_labels,
                                                 _fixed, 5, 5)
        _x_pos += 50

        _fixed.put(self.txtCode, _x_pos, _y_pos[0])
        _fixed.put(self.txtName, _x_pos, _y_pos[1])
        _fixed.put(self.txtRemarks.scrollwindow, _x_pos, _y_pos[2])

        _fixed.show_all()

        _label = ramstk.RAMSTKLabel(
            _("General\nData"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays general information for the selected  "
                      "{0:s}.").format(self._module))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        return (_frame, _fixed, _x_pos, _y_pos)

    def _on_select_revision(self, **kwargs):
        """
        Respond to the `selectedRevision` signal from pypubsub.

        :return: None
        :rtype: None
        """
        self._revision_id = kwargs['module_id']

        return None
