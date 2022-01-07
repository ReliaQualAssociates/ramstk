# Standard Library Imports
from typing import Any, Callable, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class FunctionTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: str
    _type: str
    _dic_row_loader: Dict[str, Callable]
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: int
    _parent_id: int
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...

class FunctionGeneralDataPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    _type: str
    chkSafetyCritical: RAMSTKCheckButton
    txtCode: RAMSTKEntry
    txtName: RAMSTKEntry
    txtRemarks: RAMSTKEntry
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
