# Standard Library Imports
from typing import Any

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from ..widget import RAMSTKBaseWidget as RAMSTKBaseWidget
from ..widget import WidgetProperties as WidgetProperties

class RAMSTKBaseDialog(Gtk.Dialog, RAMSTKBaseWidget):
    def __init__(
        self,
        title: str,
        parent: object,
        buttons: tuple[Any, Any, Any, Any] | None = None,
    ) -> None: ...
    def do_set_properties(self, properties: WidgetProperties) -> None: ...
    def do_destroy(self) -> None: ...
    def do_run(self) -> Any: ...
    def do_set_widget_attributes(self) -> None: ...
    handler_id: Incomplete
    def do_set_widget_callbacks(self) -> None: ...
    def do_set_widget_properties(self) -> None: ...
