# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import StakeholderTreePanel as StakeholderTreePanel

class StakeholderWorkView(RAMSTKWorkView):
    _tag: str
    _tablabel: str
    _tabtooltip: str
    _view_type: str
    _pnlPanel: RAMSTKPanel
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_add_to_affinity_group(self, new_text: str) -> None: ...
    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: int
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...
