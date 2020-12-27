# Standard Library Imports
from typing import Any, Dict, Optional, Tuple

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import Pango as Pango
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets.entry import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets.label import RAMSTKLabel as RAMSTKLabel

class RAMSTKDialog(Gtk.Dialog):
    def __init__(self, dlgtitle: str, **kwargs: Any) -> None:
        ...

    def do_destroy(self) -> None:
        ...

    def do_run(self) -> Any:
        ...


class RAMSTKDatabaseSelect(RAMSTKDialog):
    _dao: Any = ...
    _lst_databases: Any = ...
    _entry: Any = ...
    _treeview: Any = ...

    def __init__(self, dlgtitle: str, **kwargs: Any) -> None:
        ...

    def __do_load_databases(self, database: Dict[str, str]) -> None:
        ...

    def __make_ui(self) -> None:
        ...

    def _get_database(self) -> str:
        ...

    def do_destroy(self) -> None:
        ...

    def do_run(self) -> Tuple[str, bool]:
        ...


class RAMSTKDateSelect(Gtk.Dialog):
    _calendar: Any = ...

    def __init__(self, **kwargs: Any) -> None:
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
