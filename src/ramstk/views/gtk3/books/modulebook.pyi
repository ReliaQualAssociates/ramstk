# Standard Library Imports
from typing import Dict

# Third Party Imports
from treelib import Tree as Tree

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.function import FunctionModuleView as FunctionModuleView
from ramstk.views.gtk3.revision import RevisionModuleView as RevisionModuleView
from ramstk.views.gtk3.widgets import RAMSTKBaseBook as RAMSTKBaseBook

class RAMSTKModuleBook(RAMSTKBaseBook):
    _dic_module_views: Dict[str, object]
    icoStatus: Gtk.StatusIcon
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def __make_ui(self) -> None: ...
    def __set_callbacks(self) -> None: ...
    def _on_close(self) -> None: ...
    def _on_open(self, tree: Tree) -> None: ...
    def _on_switch_page(
        self, __notebook: Gtk.Notebook, __page: Gtk.Widget, page_num: int
    ) -> None: ...
