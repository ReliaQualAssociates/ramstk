# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.assistants.FMEA.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
FMEA Package Assistants Module
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

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Doyle "weibullguy" Rowland'

_ = gettext.gettext


class AddControlAction(ramstk.RAMSTKDialog):
    """
    This is the assistant that walks the user through the process of adding
    a new design control or action to the selected failure cause.
    """

    def __init__(self):
        """
        Method to initialize on instance of the Add Control or Action
        Assistant.
        """

        ramstk.RAMSTKDialog.__init__(
            self,
            _(u"RAMSTK FMEA/FMECA Design Control and "
              u"Action Addition Assistant"))

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.rdoControl = ramstk.RAMSTKOptionButton(None, _(u"Add control"))
        self.rdoAction = ramstk.RAMSTKOptionButton(self.rdoControl,
                                                _(u"Add action"))

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the dialog.                       #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()
        self.vbox.pack_start(_fixed)

        _label = ramstk.RAMSTKLabel(
            _(u"This is the RAMSTK Design Control and Action "
              u"Addition Assistant.  Enter the information "
              u"requested below and then press 'OK' to add "
              u"a new design control or action to the RAMSTK "
              u"Program database."),
            width=600,
            height=-1,
            wrap=True)
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        self.rdoControl.set_tooltip_text(
            _(u"Select to add a design control "
              u"to the selected failure cause."))
        self.rdoAction.set_tooltip_text(
            _(u"Select to add an Action to the "
              u"selected failure cause."))

        _fixed.put(self.rdoControl, 10, _y_pos)
        _fixed.put(self.rdoAction, 10, _y_pos + 35)

        _fixed.show_all()

    def _cancel(self, __button):
        """
        Method to destroy the assistant when the 'Cancel' button is
        pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """

        self.destroy()
