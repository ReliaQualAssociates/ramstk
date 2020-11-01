# Standard Library Imports
from typing import Any, Dict, Tuple

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKListView as RAMSTKListView
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel

class StakeholderPanel(RAMSTKPanel):
    _dic_attribute_updater: Any = ...
    _title: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_affinity_groups(
            self, affinities: Dict[int, Tuple[str, str]]) -> None:
        ...

    def do_load_stakeholders(self, stakeholders: Dict[int, str]) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def _do_load_requirements(self, tree: treelib.Tree) -> None:
        ...

    def _on_module_switch(self, module: str = ...) -> None:
        ...

    _record_id: Any = ...
    _parent_id: Any = ...

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        ...


class Stakeholders(RAMSTKListView):
    _module: str = ...
    _tablabel: Any = ...
    _tabtooltip: Any = ...
    _view_type: str = ...
    _lst_callbacks: Any = ...
    _lst_icons: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _pnlPanel: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _do_add_to_affinity_group(self, new_text: str) -> None:
        ...

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        ...

    def _on_insert_stakeholder(self, node_id: int, tree: treelib.Tree) -> None:
        ...

    def __make_ui(self) -> None:
        ...
