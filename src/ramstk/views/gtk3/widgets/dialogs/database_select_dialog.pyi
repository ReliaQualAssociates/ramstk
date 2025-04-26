# Standard Library Imports
from typing import Any, Tuple

# RAMSTK Package Imports
from ramstk.models.db import BaseDatabase as BaseDatabase
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import Pango as Pango
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from ..buttons import RAMSTKButton as RAMSTKButton
from ..buttons import RAMSTKCheckButton as RAMSTKCheckButton
from ..combo import RAMSTKComboBox as RAMSTKComboBox
from ..entry import RAMSTKEntry as RAMSTKEntry
from ..panels import RAMSTKFixedPanel as RAMSTKFixedPanel
from ..panels import RAMSTKTreePanel as RAMSTKTreePanel
from ..treeviews import RAMSTKCellRendererText as RAMSTKCellRendererText
from ..widget import WidgetConfig as WidgetConfig
from . import RAMSTKBaseDialog as RAMSTKBaseDialog

class RAMSTKDatabaseSelectDialog(RAMSTKBaseDialog):
    database: dict[str, str]
    exists: bool
    def __init__(
        self,
        title: str,
        parent: object,
        buttons: tuple[Any, Any, Any, Any] | None = None,
    ) -> None: ...
    def do_set_widget_callbacks(self) -> None: ...
    def do_run(self) -> Tuple[Gtk.ResponseType, bool]: ...
    def do_load_database_parameters(self) -> None: ...
    def do_load_databases(self) -> None: ...
    def do_set_icons(self, icons: dict[str, str]) -> None: ...

class RAMSTKDatabaseSelectPanel(RAMSTKFixedPanel):
    btnRefresh: RAMSTKButton
    btnSave: RAMSTKCheckButton
    cmbDialect: RAMSTKComboBox
    txtHost: RAMSTKEntry
    txtPort: RAMSTKEntry
    txtDatabase: RAMSTKEntry
    txtUser: RAMSTKEntry
    txtPassword: RAMSTKEntry
    def __init__(self) -> None: ...
    def do_load_panel(self, attributes) -> None: ...

class RAMSTKDatabaseSelectTreePanel(RAMSTKTreePanel):
    def __init__(self) -> None: ...
    def on_row_change(self, selection) -> str: ...
