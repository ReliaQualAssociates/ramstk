# Standard Library Imports
from typing import Any, TypeVar

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKSiteConfiguration as RAMSTKSiteConfiguration
)
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3.assistants import CreateProject as CreateProject
from ramstk.views.gtk3.assistants import EditOptions as EditOptions
from ramstk.views.gtk3.assistants import EditPreferences as EditPreferences
from ramstk.views.gtk3.assistants import ExportProject as ExportProject
from ramstk.views.gtk3.assistants import ImportProject as ImportProject
from ramstk.views.gtk3.assistants import OpenProject as OpenProject
from ramstk.views.gtk3.books import RAMSTKListBook as RAMSTKListBook
from ramstk.views.gtk3.books import RAMSTKModuleBook as RAMSTKModuleBook
from ramstk.views.gtk3.books import RAMSTKWorkBook as RAMSTKWorkBook

Tconfiguration = TypeVar('Tconfiguration', RAMSTKUserConfiguration,
                         RAMSTKSiteConfiguration)


def destroy(__widget: Gtk.Widget, __event: Gdk.Event = ...) -> None:
    ...


class RAMSTKDesktop(Gtk.Window):
    RAMSTK_USER_CONFIGURATION: Any = ...
    menubar: Any = ...
    progressbar: Any = ...
    statusbar: Any = ...
    toolbar: Any = ...
    icoStatus: Any = ...
    nbkListBook: Any = ...
    nbkModuleBook: Any = ...
    nbkWorkBook: Any = ...

    def __init__(self, configuration: Tconfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...
