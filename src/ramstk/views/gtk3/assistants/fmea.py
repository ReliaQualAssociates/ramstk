# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.assistants.fmea.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK (D)FME(C)A Assistants Module."""

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKDialog, RAMSTKLabel


class AddControlAction(RAMSTKDialog):
    """Assistant to walk user through process of adding control or action."""
    def __init__(self, parent=None):
        """Initialize on instance of the Add Control or Action Assistant."""
        super().__init__(_("RAMSTK FMEA/FMECA Design Control and "
                           "Action Addition Assistant"),
                         dlgparent=parent)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.rdoControl = Gtk.RadioButton.new_with_label_from_widget(
            None, _("Add control"))
        self.rdoAction = Gtk.RadioButton.new_from_widget(self.rdoControl)
        self.rdoAction.set_label(_("Add action"))

        self.__make_ui()

    def __make_ui(self):
        """Build the user interface.

        :return: None
        :rtype: None
        """
        self.set_default_size(250, -1)

        _fixed = Gtk.Fixed()
        self.vbox.pack_start(_fixed, True, True, 0)

        _label = RAMSTKLabel(
            _("This is the RAMSTK Design Control and Action "
              "Addition Assistant.  Enter the information "
              "requested below and then press 'OK' to add "
              "a new design control or action to the RAMSTK "
              "Program database."))
        _label.do_set_properties(width=600, height=-1, wrap=True)
        _fixed.put(_label, 5, 10)

        _y_pos: int = _label.get_preferred_size()[0].height + 50

        self.rdoControl.set_tooltip_text(
            _(u"Select to add a design control "
              u"to the selected failure cause."))
        self.rdoAction.set_tooltip_text(
            _("Select to add an action to the selected failure cause."))

        _fixed.put(self.rdoControl, 10, _y_pos)
        _fixed.put(self.rdoAction, 10, _y_pos + 35)

        _fixed.show_all()

    def _cancel(self, __button):
        """Destroy the assistant when the 'Cancel' button is pressed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        """
        self.destroy()
