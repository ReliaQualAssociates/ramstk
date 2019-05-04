# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.assistants.PoF.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RASMTK Physics of Failure Assistants Module."""

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _, Gtk


class AddStressMethod(ramstk.RAMSTKDialog):
    """Assistant to walk user through process of adding stress or test method."""

    def __init__(self):
        """Initialize instance of the Add Stress or Test Method Assistant."""
        ramstk.RAMSTKDialog.__init__(
            self,
            _(u"RAMSTK Physics of Failure Analysis Operating Stress and "
              u"Test Method Addition Assistant"))

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.rdoStress = ramstk.RAMSTKOptionButton(None, _(u"Add stress"))
        self.rdoMethod = ramstk.RAMSTKOptionButton(self.rdoStress,
                                                   _(u"Add test method"))

        self.__make_ui()

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        _fixed = Gtk.Fixed()
        self.vbox.pack_start(_fixed, True, True, 0)

        _label = ramstk.RAMSTKLabel(
            _(u"This is the RAMSTK Operating Stress and Test Method "
              u"Addition Assistant.  Enter the information "
              u"requested below and then press 'OK' to add "
              u"a new design control or action to the RAMSTK "
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

        return None

    def _cancel(self, __button):
        """
        Destroy the assistant when the 'Cancel' button is pressed.

        :param Gtk.Button __button: the Gtk.Button() that called this method.
        """
        self.destroy()
