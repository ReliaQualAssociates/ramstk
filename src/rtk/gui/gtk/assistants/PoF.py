# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.assistants.PoF.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Physics of Failue Assistants Module"""

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
from rtk.gui.gtk import rtk

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2018 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class AddStressMethod(rtk.RTKDialog):
    """
    This is the assistant that walks the user through the process of adding
    a new operating stress or test method to the selected operating load.
    """

    def __init__(self):
        """
        Method to initialize on instance of the Add Stress or Test Method
        Assistant.
        """

        rtk.RTKDialog.__init__(
            self,
            _(u"RTK Physics of Failure Analysis Operating Stress and "
              u"Test Method Addition Assistant"))

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.rdoStress = rtk.RTKOptionButton(None, _(u"Add stress"))
        self.rdoMethod = rtk.RTKOptionButton(self.rdoStress,
                                             _(u"Add test method"))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()
        self.vbox.pack_start(_fixed)

        _label = rtk.RTKLabel(
            _(u"This is the RTK Operating Stress and Test Method "
              u"Addition Assistant.  Enter the information "
              u"requested below and then press 'OK' to add "
              u"a new design control or action to the RTK "
              u"Program database."),
            width=600,
            height=-1,
            wrap=True)
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        self.rdoStress.set_tooltip_text(
            _(u"Select to add an operating stress to the selected operating "
              u"load."))
        self.rdoMethod.set_tooltip_text(
            _(u"Select to add a test method to the selected operating load."))

        _fixed.put(self.rdoStress, 10, _y_pos)
        _fixed.put(self.rdoMethod, 10, _y_pos + 35)

        _fixed.show_all()

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()
