# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.utilities import string_to_boolean as string_to_boolean
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCellRendererText as RAMSTKCellRendererText
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererToggle as RAMSTKCellRendererToggle,
)
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import RAMSTKTreeView as RAMSTKTreeView
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class TreeLayoutPreferencesPanel(RAMSTKTreePanel):
    _select_msg: Incomplete
    _tag: str
    _title: Incomplete
    cmbFormatFiles: RAMSTKComboBox
    tvwTreeView: RAMSTKTreeView
    _lst_widget_configuration: list[WidgetConfig]
    _configuration: RAMSTKUserConfiguration
    fmt_file: str
    def __init__(self) -> None: ...
    def _do_load_format_files(self) -> None: ...
    def _do_load_format(self, module: str) -> None: ...
    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None: ...
    def _do_make_panel(self) -> None: ...
    def _do_set_widget_callbacks(self) -> None: ...
    def _do_set_widget_properties(self) -> None: ...
    def _on_combo_changed(self, combo: RAMSTKComboBox) -> None: ...
