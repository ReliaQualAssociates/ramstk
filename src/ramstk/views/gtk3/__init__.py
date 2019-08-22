# pylint: disable=unused-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.__init__.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 GUI package."""

# Standard Library Imports
import gettext
import sys

# Third Party Imports
from gi.repository import (  # pylint: disable=unused-import
    Gdk, GdkPixbuf, GObject, Gtk, Pango
)

try:
    import gi
    gi.require_version('Gdk', '3.0')
    gi.require_version('Gtk', '3.0')
except ImportError:
    print("Failed to import package gi; exiting.")
    sys.exit(1)

_ = gettext.gettext


#from .Book import RAMSTKBook, destroy
#from .widgets.button import (RAMSTKButton, RAMSTKCheckButton, RAMSTKOptionButton,
#                     do_make_buttonbox)
#from .Combo import RAMSTKComboBox
#from .Dialog import (RAMSTKDateSelect, RAMSTKDialog, RAMSTKFileChooser,
#                     RAMSTKMessageDialog)
#from .Entry import RAMSTKEntry, RAMSTKTextView
#from .Frame import RAMSTKFrame
#from .Helpers import ramstk_file_select, ramstk_set_cursor
#from .Label import RAMSTKLabel, do_make_label_group
#from .Matrix import RAMSTKBaseMatrix
#from .Plot import RAMSTKPlot
#from .ScrolledWindow import RAMSTKScrolledWindow
#from .TreeView import RAMSTKTreeView
#from .View import RAMSTKBaseView
