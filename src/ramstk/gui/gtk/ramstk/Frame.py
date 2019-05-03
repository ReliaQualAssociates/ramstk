# pylint: disable=non-parent-init-called
# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.ramstk.Frame.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Frame Module."""

# Import other RAMSTK Widget classes.
from .Widget import _, GObject, Gtk
from .Label import RAMSTKLabel


class RAMSTKFrame(Gtk.Frame):
    """This is the RAMSTK Frame class."""

    def __init__(self, label=_("")):
        """
        Initialize an instance of the RAMSTK Frame.

        :keyword str label: the text to display in the RAMSTK Frame label.
                            Default is an empty string.
        """
        GObject.GObject.__init__(self)

        _label = RAMSTKLabel(label, width=-1)
        _label.show_all()

        self.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        self.set_label_widget(_label)
