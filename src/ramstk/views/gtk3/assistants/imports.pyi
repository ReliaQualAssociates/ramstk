# Standard Library Imports
from typing import Any, List

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel

class ImportProject(Gtk.Assistant):
    RAMSTK_USER_CONFIGURATION: Any = ...
    cmbSelectModule: Any = ...
    _filechooser: Any = ...
    _module: str = ...
    tvwFieldMap: Any = ...

    def __init__(self, __button: Gtk.ToolButton,
                 configuration: RAMSTKUserConfiguration,
                 parent: object) -> None:
        ...

    def _do_edit_cell(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      model: Gtk.TreeModel) -> None:
        ...

    def _do_load_db_fields(self, db_fields: List[str]) -> None:
        ...

    def _do_load_import_fields(self, import_fields: List[str]) -> None:
        ...

    def _do_quit(self, __widget: Gtk.Widget) -> None:
        ...

    def _do_request_import(self, __assistant: Gtk.Assistant) -> None:
        ...

    def _do_select_file(self, filechooser: Gtk.FileChooser) -> None:
        ...

    def _on_combo_changed(self, combo: RAMSTKComboBox) -> None:
        ...

    def __do_load_combobox(self) -> None:
        ...

    def __do_set_callbacks(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...

    def __make_confirm_page(self) -> None:
        ...

    def __make_input_file_select_page(self) -> None:
        ...

    def __make_introduction_page(self) -> None:
        ...

    def __make_map_field_page(self) -> None:
        ...

    def __make_ui(self) -> None:
        ...
