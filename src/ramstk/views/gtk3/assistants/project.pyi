# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.models.db import BaseDatabase as BaseDatabase
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKBaseDialog as RAMSTKBaseDialog
from ramstk.views.gtk3.widgets import (
    RAMSTKDatabaseSelectDialog as RAMSTKDatabaseSelectDialog,
)
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog as RAMSTKMessageDialog

class CreateProject:
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration
    def __init__(
        self,
        /,
        __button: Gtk.ToolButton,
        configuration: RAMSTKUserConfiguration,
        parent: object,
    ) -> None: ...

class OpenProject:
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration
    def __init__(
        self,
        /,
        __button: Gtk.ToolButton,
        configuration: RAMSTKUserConfiguration,
        parent: object,
    ) -> None: ...
