# Standard Library Imports
from typing import Any, List, TypeVar

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
from ramstk.views.gtk3 import _ as _
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
    RAMSTK_SITE_CONFIGURATION: RAMSTKSiteConfiguration = ...
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = ...
    _logger: Any = ...
    _height: Any = ...
    _n_screens: Any = ...
    _width: Any = ...
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

    def _do_request_options_assistant(self,
                                      __widget: Gtk.ImageMenuItem) -> None:
        ...

    def _do_request_preferences_assistant(self,
                                          __widget: Gtk.ImageMenuItem) -> None:
        ...

    def __make_menu(self) -> None:
        ...

    def __make_menu_edit(self) -> Gtk.MenuItem:
        ...

    def __make_menu_file(self) -> Gtk.MenuItem:
        ...

    def __make_menu_items(self, icons: List[str],
                          labels: List[str]) -> List[Gtk.ImageMenuItem]:
        ...

    def __make_menu_tools(self) -> Gtk.MenuItem:
        ...

    def __make_toolbuttons(self, icons: List[str],
                           tooltips: List[str]) -> List[Gtk.ToolButton]:
        ...

    def __make_toolbar(self) -> None:
        ...

    def __make_ui(self) -> None:
        ...

    def __set_callbacks(self) -> None:
        ...

    def __set_properties(self) -> None:
        ...

    @staticmethod
    def _do_request_close_project(__widget: Gtk.Widget) -> None:
        ...

    def _do_request_save_project(self,
                                 widget: Gtk.Widget,
                                 end: bool = ...) -> None:
        ...

    def _do_set_status(self, status: str) -> None:
        ...

    def _do_set_status_icon(self, connected: bool = ...) -> None:
        ...

    def _on_button_press(self, __book: object, event: Gdk.EventButton) -> None:
        ...

    def _on_request_open(self) -> None:
        ...

    def _on_select(self, title: str) -> None:
        ...

    @staticmethod
    def _on_window_state_event(window: Gtk.Window,
                               event: Gdk.EventWindowState) -> None:
        ...
