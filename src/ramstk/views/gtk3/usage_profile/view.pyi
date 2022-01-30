# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import UsageProfileTreePanel as UsageProfileTreePanel

class UsageProfileWorkView(RAMSTKWorkView):
    _tag: str
    _tablabel: str
    _tabtooltip: str
    _lst_col_order: List[int]
    _lst_mnu_labels: List[str]
    _lst_tooltips: List[str]
    _pnlPanel: RAMSTKPanel
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None: ...
    def __make_ui(self) -> None: ...
