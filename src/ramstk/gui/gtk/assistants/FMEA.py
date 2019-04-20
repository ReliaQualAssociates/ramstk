# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.assistants.FMEA.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""(D)FME(C)A Assistants Module"""

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, gtk


class AddControlAction(ramstk.RAMSTKDialog):
    """
    This is the assistant that walks the user through the process of adding
    a new design control or action to the selected failure cause.
    """

    def __init__(self):
        """Initialize on instance of the Add Control or Action Assistant."""
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
        Destroy the assistant when the 'Cancel' button is pressed.

        :param __button: the gtk.Button() that called this method.
        :type __button: :class:`gtk.Button`
        """
        self.destroy()
