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


class RTKWorkView(gtk.VBox, rtk.RTKBaseView):
    """
    This is the meta class for all RTK Work View classes.  Attributes of the
    RTKWorkView are:
    """

    def __init__(self, controller):
        """
        Method to initialize the Work View.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.VBox.__init__(self)
        rtk.RTKBaseView.__init__(self, controller)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.hbx_tab_label = gtk.HBox()

    @staticmethod
    def _make_assessment_results_page():
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

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the right half of the page.                                   #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fxd_right = gtk.Fixed()

        _scrollwindow = rtk.RTKScrolledWindow(_fxd_right)
        _frame = rtk.RTKFrame(label=_(u"Maintainability Results"))
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame)

        return _hbox, _fxd_left, _fxd_right

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
