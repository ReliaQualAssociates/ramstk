# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.utilities import string_to_boolean as string_to_boolean
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFileChooserButton as RAMSTKFileChooserButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import RAMSTKTreeView as RAMSTKTreeView

class GeneralPreferencesPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: str
    btnConfDir: RAMSTKFileChooserButton
    btnDataDir: RAMSTKFileChooserButton
    btnIconDir: RAMSTKFileChooserButton
    btnLogDir: RAMSTKFileChooserButton
    cmbModuleBookTabPosition: RAMSTKComboBox
    cmbWorkBookTabPosition: RAMSTKComboBox
    cmbListBookTabPosition: RAMSTKComboBox
    cmbReportSize: RAMSTKComboBox
    txtFRMultiplier: RAMSTKEntry
    txtDecimalPlaces: RAMSTKEntry
    txtMissionTime: RAMSTKEntry
    _configuration: RAMSTKUserConfiguration
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None: ...
    def _do_load_comboboxes(self) -> None: ...
    def _do_select_path(self, button: Gtk.FileChooserButton, index: int) -> None: ...
    def _on_changed_combo(self, combo: RAMSTKComboBox, index: int) -> None: ...

class LookFeelPreferencesPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: str
    btnRevisionBGColor: Gtk.ColorButton
    btnRevisionFGColor: Gtk.ColorButton
    btnFunctionBGColor: Gtk.ColorButton
    btnFunctionFGColor: Gtk.ColorButton
    btnRequirementsBGColor: Gtk.ColorButton
    btnRequirementsFGColor: Gtk.ColorButton
    btnHardwareBGColor: Gtk.ColorButton
    btnHardwareFGColor: Gtk.ColorButton
    btnValidationBGColor: Gtk.ColorButton
    btnValidationFGColor: Gtk.ColorButton
    _configuration: RAMSTKUserConfiguration
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None: ...
    def _do_set_color(
        self, colorbutton: Gtk.ColorButton, ramstk_color: int
    ) -> None: ...
    def _do_set_callbacks(self) -> None: ...
    def _do_set_properties(self) -> None: ...

class TreeLayoutPreferencesPanel(RAMSTKTreePanel):
    _select_msg: Any
    _tag: str
    _title: str
    cmbFormatFiles: RAMSTKComboBox
    tvwTreeView: RAMSTKTreeView
    _lst_labels: List[str]
    _configuration: RAMSTKUserConfiguration
    fmt_file: str
    def __init__(self) -> None: ...
    def _do_load_comboboxes(self) -> None: ...
    def _do_load_format(self, module: str) -> None: ...
    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None: ...
    def _on_combo_changed(self, combo: RAMSTKComboBox) -> None: ...
    def __do_make_treeview(self) -> None: ...
    def __make_ui(self) -> None: ...
