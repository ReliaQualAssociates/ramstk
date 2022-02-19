# Standard Library Imports
from typing import Callable, List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.utilities import integer_to_boolean as integer_to_boolean
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKBaseView as RAMSTKBaseView
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel

# RAMSTK Local Imports
from . import GeneralPreferencesPanel as GeneralPreferencesPanel
from . import LookFeelPreferencesPanel as LookFeelPreferencesPanel
from . import TreeLayoutPreferencesPanel as TreeLayoutPreferencesPanel

class PreferencesDialog(RAMSTKBaseView):
    _tag: str
    _pixbuf: bool
    _tablabel: str
    _tabtooltip: str
    _lst_callbacks: List[Callable]
    _lst_icons: List[str]
    _lst_tooltips: List[str]
    _pnlGeneralPreferences: GeneralPreferencesPanel
    _pnlLookFeel: LookFeelPreferencesPanel
    _pnlTreeViewLayout: TreeLayoutPreferencesPanel
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _cancel(self, __button: Gtk.Button) -> None: ...
    def _do_request_update(self, __button: Gtk.Button) -> None: ...
    def _do_save_tree_layout(self) -> None: ...
    def __make_ui(self) -> None: ...
