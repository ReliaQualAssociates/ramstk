# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import Pango as Pango

# RAMSTK Local Imports
from .widget import RAMSTKWidget as RAMSTKWidget

class RAMSTKEntry(Gtk.Entry, RAMSTKWidget):
    def __init__(self) -> None:
        ...

    def do_get_text(self):
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...

    def do_update(self, value: Any, signal: str = ...) -> None:
        ...


class RAMSTKTextView(Gtk.TextView, RAMSTKWidget):
    scrollwindow: Any = ...
    tag_bold: Any = ...

    def __init__(self, txvbuffer: Gtk.TextBuffer) -> None:
        ...

    def do_get_buffer(self) -> Gtk.TextBuffer:
        ...

    def do_get_text(self) -> Any:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...

    def do_update(self, value: str, signal: str = ...) -> None:
        ...
