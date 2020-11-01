# Standard Library Imports
from typing import Any

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import (
    RAMSTKMessageDialog as RAMSTKMessageDialog
)
from ramstk.views.gtk3.widgets import RAMSTKModuleView as RAMSTKModuleView
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS as ATTRIBUTE_KEYS

class FunctionPanel(RAMSTKPanel):
    _dic_attribute_keys: Any = ...
    _dic_attribute_updater: Any = ...
    _title: Any = ...

    def __init__(self) -> None:
        ...

    def _on_module_switch(self, module: str = ...) -> None:
        ...

    _record_id: Any = ...
    _parent_id: Any = ...

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...


class ModuleView(RAMSTKModuleView):
    _module: str = ...
    _tablabel: str = ...
    _tabtooltip: str = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _pnlPanel: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        ...

    def _on_insert_function(self, node_id: int, tree: treelib.Tree) -> None:
        ...
