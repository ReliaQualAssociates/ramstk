#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.Function.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
###############################################################################
Function Package List Book View
###############################################################################
"""

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
try:
    # noinspection PyUnresolvedReferences
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

_ = gettext.gettext


class ListView(gtk.Notebook):
    """
    The List View displays all the matrices and lists associated with the
    Function Class.  The attributes of a List View are:
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Function package.

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
        #self.lvw_usage_profile = lvwUsageProfile(controller)
        #self.lvw_failure_definition = lvwFailureDefinition(controller)

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

        #self.insert_page(self.lvw_usage_profile,
        #                 tab_label=self.lvw_usage_profile.hbx_tab_label,
        #                 position=-1)
        #self.insert_page(self.lvw_failure_definition,
        #                 tab_label=self.lvw_failure_definition.hbx_tab_label,
        #                 position=-1)

        self.show_all()
