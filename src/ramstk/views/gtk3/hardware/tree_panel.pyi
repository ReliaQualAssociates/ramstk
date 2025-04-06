# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererCombo as RAMSTKCellRendererCombo
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererToggle as RAMSTKCellRendererToggle,
)
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class HardwareTreePanel(RAMSTKTreePanel):
    dic_icons: Incomplete
    dic_subcategories: dict[int, list[str]]
    lst_categories: list[str]
    lst_manufacturers: list[str]
    part: int
    def __init__(self) -> None: ...
    def do_load_categories(
        self,
        categories: dict[int, tuple[str]],
        subcategories: dict[int, dict[int, tuple[str]]],
    ) -> None: ...
    def do_load_cost_types(self) -> None: ...
    def do_load_manufacturers(
        self, manufacturers: dict[int, tuple[str, str, str]]
    ) -> None: ...
    def do_load_subcategories(
        self, category: int, subcategories: dict[int, dict[int, tuple[str]]]
    ) -> None: ...
