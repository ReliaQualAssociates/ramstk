# Standard Library Imports
from typing import Any

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererCombo as RAMSTKCellRendererCombo
from ramstk.views.gtk3.widgets import RAMSTKCellRendererSpin as RAMSTKCellRendererSpin
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class PoFTreePanel(RAMSTKTreePanel):
    dic_icons: dict[str, str]
    lst_damage_models: list[str]
    lst_load_history: list[str]
    lst_measurable_parameters: list[str]
    def __init__(self) -> None: ...
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool: ...
    level: Incomplete
    def do_get_pof_level(self, model: Gtk.TreeModel, row: Gtk.TreeIter) -> None: ...
    def do_load_damage_models(self, models: dict[int, tuple[str]]) -> None: ...
    def do_load_load_history(self, histories: dict[int, tuple[str]]) -> None: ...
    def do_load_measurable_parameters(
        self, parameters: dict[int, tuple[str, str]]
    ) -> None: ...
