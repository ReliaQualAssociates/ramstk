# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.assistants import AddStressTestMethod as AddStressTestMethod
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog as RAMSTKMessageDialog
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import PoFTreePanel as PoFTreePanel

class PoFWorkView(RAMSTKWorkView):
    _tag: str
    _pixbuf: bool
    _tablabel: str
    _tabtooltip: str
    _lst_tooltips: List[str]
    _pnlPanel: RAMSTKPanel
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: int
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __do_load_test_method_lists(self) -> None: ...
    def __make_ui(self) -> None: ...
    def __on_request_insert_opstress_method(self) -> str: ...
