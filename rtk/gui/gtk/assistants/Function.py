# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.assistants.Function.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Function Package Assistants Module
###############################################################################
"""

import gettext
import sys

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
from gui.gtk import rtk                     # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class AddFunction(gtk.Assistant):
    """
    This is the assistant that walks the user through the process of adding
    a new Function to the open RTK Project database.
    """

    def __init__(self, workview, level='sibling'):
        """
        Method to initialize on instance of the Add Function Assistant.
        """

        gtk.Assistant.__init__(self)

        self.set_title(_(u"RTK Add Function Assistant"))
        self.set_transient_for(workview.get_parent())
        self.set_position(gtk.WIN_POS_CENTER_ON_PARENT)

        # Initialize private dictionary attributes.
        self._level = level

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._workview = workview

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtQuantity = rtk.RTKEntry(width=50)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the introduction page.
        _fixed = gtk.Fixed()
        _text = _(u"This is the RTK Function Addition Assistant.  It will "
                  u"help you add new {0:s} Functions to the RTK Program "
                  u"database.  Press 'Forward' to continue or 'Cancel' to "
                  u"quit the assistant.").format(level)
        _label = rtk.RTKLabel(_text, width=500, height=-1, wrap=True)
        _fixed.put(_label, 5, 5)
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_INTRO)
        self.set_page_title(_fixed, _(u"Introduction"))
        self.set_page_complete(_fixed, True)

        # Create the page for selecting whether to add a sibling or child
        # Function and how many.
        _fixed = gtk.Fixed()

        self.txtQuantity.set_tooltip_text(_(u"Enter the number of functions "
                                            u"to add."))

        _label = rtk.RTKLabel(_(u"Select the number of {0:s} functions to "
                                u"add...".format(level)),
                              width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        _labels = [_(u"Number of {0:s} functions to add:").format(level)]
        (_x_pos, _y_pos) = rtk.make_label_group(_labels, _fixed, 5, _y_pos)
        _x_pos += 50
        _fixed.put(self.txtQuantity, _x_pos, _y_pos[0])
        self.txtQuantity.set_text("1")

        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONTENT)
        self.set_page_title(_fixed, _(u"Select Number of New {0:s} Functions "
                                      u"to Add").format(level))
        self.set_page_complete(_fixed, True)

        # Create the confirmation page.
        _fixed = gtk.Fixed()
        self.append_page(_fixed)
        self.set_page_type(_fixed, gtk.ASSISTANT_PAGE_CONFIRM)
        self.set_page_title(_fixed, _(u"Function: Confirm Addition"))
        self.set_page_complete(_fixed, True)

        # Connect to callback methods.
        self.connect('apply', self._add_function)
        self.connect('cancel', self._cancel)
        self.connect('close', self._cancel)

        self.show_all()

    def _add_function(self, __assistant):
        """
        Method to add the new Function to the open RTK Project database.

        :param gtk.Assistant __assistant: the current instance of the
                                          assistant.
        :return: None
        :rtype: None
        """

        # Find out how many Functions to add.  Defaults to one Function if the
        # user hasn't entered a value.
        try:
            _n_functions = int(self.txtQuantity.get_text())
        except ValueError:
            _n_functions = 1

        for i in range(_n_functions):               # pylint: disable=W0612
            self._workview.do_add_function(self._level)

        return None

    def _cancel(self, __assistant):
        """
        Method to destroy the assistant when the 'Cancel' button is pressed.

        :param gtk.Assistant __assistant: the current instance of the
                                          assistant.
        """

        self.destroy()
