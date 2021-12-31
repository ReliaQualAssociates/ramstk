# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTK_CONTROL_TYPES as RAMSTK_CONTROL_TYPES
from ramstk.configuration import RAMSTK_CRITICALITY as RAMSTK_CRITICALITY
from ramstk.configuration import (
    RAMSTK_FAILURE_PROBABILITY as RAMSTK_FAILURE_PROBABILITY,
)
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.assistants import AddControlAction as AddControlAction
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog as RAMSTKMessageDialog
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import FMEAMethodPanel as FMEAMethodPanel
from . import FMEATreePanel as FMEATreePanel

def do_request_insert(level: str, parent_id: str) -> None: ...

class FMEAWorkView(RAMSTKWorkView):
    _tag: str
    _pixbuf: bool
    _tablabel: str
    _tabtooltip: str
    _lst_tooltips: List[str]
    _item_hazard_rate: float
    _pnlMethods: RAMSTKPanel
    _pnlPanel: RAMSTKPanel
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: int
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def __do_load_action_combos(self) -> None: ...
    def __do_load_rpn_combos(self) -> None: ...
    def __do_load_severity_combos(self) -> None: ...
    def __make_ui(self) -> None: ...
    def __on_request_insert_control_action(self) -> str: ...
