# Standard Library Imports
from datetime import date

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererCombo as RAMSTKCellRendererCombo
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class HazardsTreePanel(RAMSTKTreePanel):
    lst_hazards: list[str]
    lst_probability: list[str]
    lst_severity: list[str]
    def __init__(self) -> None: ...
    def do_filter_tree(
        self,
        model: Gtk.TreeModel,
        row: Gtk.TreeIter,
        data: bool | date | float | int | str,
    ) -> bool: ...
    def do_load_hazards(self, hazards: dict[int, tuple[str, str]]) -> None: ...
    def do_load_probabilities(self, probabilities: list[list[str]]) -> None: ...
    def do_load_severities(
        self, severities: dict[int, tuple[str, str, int]]
    ) -> None: ...
    def do_refresh_functions(self, row: Gtk.TreeIter, function: list[str]) -> None: ...
