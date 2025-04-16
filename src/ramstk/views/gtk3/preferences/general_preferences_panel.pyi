# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFileChooserButton as RAMSTKFileChooserButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class GeneralPreferencesPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: Incomplete
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
    _lst_widget_configuration: list[WidgetConfig]
    _configuration: RAMSTKUserConfiguration
    def __init__(self) -> None: ...
    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None: ...
    def _do_load_paper_sizes(self) -> None: ...
    def _do_load_tab_positions(self) -> None: ...
    def _do_select_path(self, button: Gtk.FileChooserButton, index: int) -> None: ...
    def _do_set_widget_callbacks(self) -> None: ...
    def _on_combo_changed(self, combo: RAMSTKComboBox, index: int) -> None: ...
