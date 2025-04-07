# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererToggle as RAMSTKCellRendererToggle,
)
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class AllocationTreePanel(RAMSTKTreePanel):
    def __init__(self) -> None: ...
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool: ...
