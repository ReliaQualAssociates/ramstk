# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets.dialog import (
    RAMSTKDatabaseSelect as RAMSTKDatabaseSelect
)
from ramstk.views.gtk3.widgets.dialog import RAMSTKDialog as RAMSTKDialog
from ramstk.views.gtk3.widgets.dialog import (
    RAMSTKMessageDialog as RAMSTKMessageDialog
)
from ramstk.views.gtk3.widgets.label import RAMSTKLabel as RAMSTKLabel

class CreateProject:
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = ...
    _parent: Any = ...

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration,
                 parent: object) -> None:
        ...

    def _do_confirm_overwrite(self, database: str) -> None:
        ...

    def _do_request_create_project(self) -> None:
        ...


class OpenProject:
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = ...
    _parent: Any = ...

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration,
                 parent: object) -> None:
        ...

    def _do_request_open_project(self) -> None:
        ...

    def __project_is_open(self) -> None:
        ...
