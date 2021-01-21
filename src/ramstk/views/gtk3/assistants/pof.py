# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.fmea.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK (D)FME(C)A Assistants Module."""

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKDialog, RAMSTKLabel


class AddStressTestMethod(RAMSTKDialog):
    """Assistant to walk user through process of adding stress or test."""
    def __init__(self, parent=None):
        """Initialize on instance of the Add Stress or Method Assistant."""
        super().__init__(_("RAMSTK Physics of Failure Analysis Operating "
                           "Stress and Test Method Addition Assistant"),
                         dlgparent=parent)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.rdoOpStress = Gtk.RadioButton.new_with_label_from_widget(
            None, _("Add stress"))
        self.rdoTestMethod = Gtk.RadioButton.new_from_widget(self.rdoOpStress)
        self.rdoTestMethod.set_label(_("Add test method"))

        self.__make_ui()

    def _cancel(self, __button: Gtk.Button) -> None:
        """Destroy the assistant when the 'Cancel' button is pressed.

        :param __button: the Gtk.Button() that called this method.
        """
        self.destroy()

    def __make_ui(self) -> None:
        """Build the user interface.

        :return: None
        :rtype: None
        """
        _fixed = Gtk.Fixed()
        self.vbox.pack_start(_fixed, True, True, 0)

        _label = RAMSTKLabel(
            _("This is the RAMSTK Operating Stress and Test Method "
              "Addition Assistant.  Enter the information "
              "requested below and then press 'OK' to add "
              "a new design control or action to the RAMSTK "
              "Program database."))
        _label.do_set_properties(width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 10)

        _y_pos: int = _label.get_preferred_size()[0].height + 50

        self.rdoOpStress.set_tooltip_text(
            _("Select to add an operating stress to the selected operating "
              "load."))
        self.rdoTestMethod.set_tooltip_text(
            _("Select to add a test method to the selected operating load."))

        _fixed.put(self.rdoOpStress, 10, _y_pos)
        _fixed.put(self.rdoTestMethod, 10, _y_pos + 35)

        _fixed.show_all()

        self.set_default_size(250, -1)
