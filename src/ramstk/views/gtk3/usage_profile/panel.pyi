# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererCombo as RAMSTKCellRendererCombo
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class UsageProfileTreePanel(RAMSTKTreePanel):
    dic_icons: dict[str, Any]
    dic_units: dict[str, tuple[str, str, str]]
    level: str
    def __init__(self) -> None: ...
    def do_get_usage_profile_level(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter
    ) -> None: ...
    def do_load_units(self, measurement_units: dict[int, tuple[str, str]]) -> None: ...
