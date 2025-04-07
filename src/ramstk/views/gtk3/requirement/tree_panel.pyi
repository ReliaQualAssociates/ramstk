# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets.treeviews.cellrenderercombo import (
    RAMSTKCellRendererCombo as RAMSTKCellRendererCombo,
)
from ramstk.views.gtk3.widgets.treeviews.cellrenderertext import (
    RAMSTKCellRendererText as RAMSTKCellRendererText,
)
from ramstk.views.gtk3.widgets.treeviews.cellrenderertoggle import (
    RAMSTKCellRendererToggle as RAMSTKCellRendererToggle,
)

class RequirementTreePanel(RAMSTKTreePanel):
    lst_owner: list[str]
    lst_type: list[str]
    def __init__(self) -> None: ...
    def do_load_owners(self, owners: dict[int, tuple[str]]) -> None: ...
    def do_load_priorities(self) -> None: ...
    def do_load_types(self, types: dict[int, tuple[str, str]]) -> None: ...
