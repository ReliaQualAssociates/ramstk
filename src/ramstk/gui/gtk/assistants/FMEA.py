# -*- coding: utf-8 -*-
#
#       gui.gtk.assistants.FMEA.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK (D)FME(C)A Assistants Module."""

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKDialog, RAMSTKLabel, RAMSTKOptionButton
from ramstk.gui.gtk.ramstk.Widget import Gtk, _


class AddControlAction(RAMSTKDialog):
    """Assistant to walk user through process of adding control or action."""

    def __init__(self):
        """Initialize on instance of the Add Control or Action Assistant."""
        RAMSTKDialog.__init__(
            self,
            _(
                "RAMSTK FMEA/FMECA Design Control and "
                "Action Addition Assistant",
            ),
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.rdoControl = RAMSTKOptionButton(None, _("Add control"))
        self.rdoAction = RAMSTKOptionButton(
            self.rdoControl,
            _("Add action"),
        )

        self.__make_ui()

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        _fixed = Gtk.Fixed()
        self.vbox.pack_start(_fixed, True, True, 0)

        _label = RAMSTKLabel(
            _(
                "This is the RAMSTK Design Control and Action "
                "Addition Assistant.  Enter the information "
                "requested below and then press 'OK' to add "
                "a new design control or action to the RAMSTK "
                "Program database.",
            ),
            width=600,
            height=-1,
            wrap=True,
        )
        _fixed.put(_label, 5, 10)
        _y_pos = _label.size_request()[1] + 50

        self.rdoControl.set_tooltip_text(
            _(
                "Select to add a design control to the selected failure "
                "cause.",
            ),
        )
        self.rdoAction.set_tooltip_text(
            _("Select to add an Action to the selected failure cause."),
        )

        _fixed.put(self.rdoControl, 10, _y_pos)
        _fixed.put(self.rdoAction, 10, _y_pos + 35)

        _fixed.show_all()

    def _cancel(self, __button):
        """
        Destroy the assistant when the 'Cancel' button is pressed.

        :param __button: the Gtk.Button() that called this method.
        :type __button: :class:`Gtk.Button`
        """
        self.destroy()
