# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKColorButton as RAMSTKColorButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig
from ramstk.views.gtk3.widgets import make_widget_config as make_widget_config

class LookFeelPreferencesPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: Incomplete
    btnRevisionBGColor: RAMSTKColorButton
    btnRevisionFGColor: RAMSTKColorButton
    btnFunctionBGColor: RAMSTKColorButton
    btnFunctionFGColor: RAMSTKColorButton
    btnRequirementsBGColor: RAMSTKColorButton
    btnRequirementsFGColor: RAMSTKColorButton
    btnHardwareBGColor: RAMSTKColorButton
    btnHardwareFGColor: RAMSTKColorButton
    btnValidationBGColor: RAMSTKColorButton
    btnValidationFGColor: RAMSTKColorButton
    _lst_widget_configuration: list[WidgetConfig]
    _configuration: RAMSTKUserConfiguration
    def __init__(self) -> None: ...
    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None: ...
    def _do_set_color(
        self, colorbutton: Gtk.ColorButton, ramstk_color: int
    ) -> None: ...
    def _do_set_widget_callbacks(self) -> None: ...
