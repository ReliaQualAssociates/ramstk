# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.Revision.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Revision Package List Book View
###############################################################################
"""

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)

# Import other RTK modules.
# pylint: disable=E0401
from gui.gtk.listviews.UsageProfile import ListView as lvwUsageProfile
# pylint: disable=E0401
from gui.gtk.listviews.FailureDefinition \
    import ListView as lvwFailureDefinition

_ = gettext.gettext


class ListView(gtk.Notebook):
    """
    The List View displays all the matrices and lists associated with the
    Revision Class.  The attributes of a List View are:
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Revision package.

        :param controller: the RTK Master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.Notebook.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lvw_usage_profile = lvwUsageProfile(controller)
        self.lvw_failure_definition = lvwFailureDefinition(controller)

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Set the user's preferred gtk.Notebook tab position.
        if controller.RTK_CONFIGURATION.RTK_TABPOS['listbook'] == 'left':
            self.set_tab_pos(gtk.POS_LEFT)
        elif controller.RTK_CONFIGURATION.RTK_TABPOS['listbook'] == 'right':
            self.set_tab_pos(gtk.POS_RIGHT)
        elif controller.RTK_CONFIGURATION.RTK_TABPOS['listbook'] == 'top':
            self.set_tab_pos(gtk.POS_TOP)
        else:
            self.set_tab_pos(gtk.POS_BOTTOM)

        self.insert_page(self.lvw_usage_profile,
                         tab_label=self.lvw_usage_profile.hbx_tab_label,
                         position=-1)
        self.insert_page(self.lvw_failure_definition,
                         tab_label=self.lvw_failure_definition.hbx_tab_label,
                         position=-1)

        self.show_all()
