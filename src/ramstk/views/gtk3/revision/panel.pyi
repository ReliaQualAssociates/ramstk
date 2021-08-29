# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel

class RevisionTreePanel(RAMSTKPanel):
    _select_msg: str
    _tag: str
    _title: str
    _type: str
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: Any
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
