# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.rtk.Frame.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Frame Module
-------------------------------------------------------------------------------

This module contains RTK frame classes.  These classes are derived from the
applicable pyGTK frame, but are provided with RTK specific property values
and methods.  This ensures a consistent look and feel to widgets in the RTK
application.
"""

# Import other RTK Widget classes.
from .Widget import _, gtk                          # pylint: disable=E0401
from .Label import RTKLabel                         # pylint: disable=E0401


class RTKFrame(gtk.Frame):
    """
    This is the RTK Frame class.
    """

    def __init__(self, label=_("")):
        """
        Method to create an RTK Frame widget.

        :keyword str label: the text to display in the RTK Frame label.
                            Default is an empty string.
        """

        gtk.Frame.__init__(self)

        _label = RTKLabel(label, width=-1)
        _label.show_all()

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        self.set_label_widget(_label)
