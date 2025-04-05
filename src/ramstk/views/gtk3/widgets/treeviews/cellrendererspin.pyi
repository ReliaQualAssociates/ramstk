# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from ..widget import WidgetProperties as WidgetProperties
from . import RAMSTKCellRendererText as RAMSTKCellRendererText

class RAMSTKCellRendererSpin(Gtk.CellRendererSpin, RAMSTKCellRendererText):
    tree_model: Gtk.TreeStore | None
    tree_row: Gtk.TreeIter | None
    def __init__(self) -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
