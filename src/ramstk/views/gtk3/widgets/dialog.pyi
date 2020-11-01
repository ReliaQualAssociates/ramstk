# Standard Library Imports
from typing import Any, Optional, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import Pango as Pango

class RAMSTKDialog(Gtk.Dialog):
    def __init__(self, dlgtitle: str, **kwargs: Any) -> None:
        ...

    def do_destroy(self) -> None:
        ...

    def do_run(self) -> Any:
        ...


class RAMSTKDatabaseSelect(RAMSTKDialog):
    def __init__(self, dlgtitle: str, **kwargs: Any) -> None:
        ...

    def do_destroy(self) -> None:
        ...

    def do_run(self) -> str:
        ...


class RAMSTKDateSelect(Gtk.Dialog):
    def __init__(self) -> None:
        ...

    def do_destroy(self) -> None:
        ...

    def do_run(self) -> Any:
        ...


class RAMSTKFileChooser(Gtk.FileChooserDialog):
    def __init__(self, title: str, parent: object) -> None:
        ...

    def do_destroy(self) -> None:
        ...

    def do_run(self) -> Tuple[Optional[Any], Optional[Any]]:
        ...


class RAMSTKMessageDialog(Gtk.MessageDialog):
    def __init__(self, parent: Gtk.Window = ...) -> None:
        ...

    def do_set_message(self, message: str) -> None:
        ...

    def do_set_message_type(self, message_type: str = ...) -> None:
        ...

    def do_run(self) -> Any:
        ...

    def do_destroy(self) -> None:
        ...
