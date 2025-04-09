# Third Party Imports
import treelib
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererCombo as RAMSTKCellRendererCombo
from ramstk.views.gtk3.widgets import RAMSTKCellRendererSpin as RAMSTKCellRendererSpin
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class StakeholderTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: Incomplete
    _lst_widget_configuration: list[WidgetConfig]
    _on_edit_message: str
    def __init__(self) -> None: ...
    def do_load_affinity_groups(
        self, affinities: dict[int, tuple[str, str]]
    ) -> None: ...
    def do_load_stakeholders(self, stakeholders: dict[int, str]) -> None: ...
    def _do_load_requirements(self, tree: treelib.Tree) -> None: ...
    def _on_insert(self, tree: treelib.Tree) -> None: ...
    def _on_module_switch(self, module: str = "") -> None: ...
    _record_id: Incomplete
    _parent_id: Incomplete
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
