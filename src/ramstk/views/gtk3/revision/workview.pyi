# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS as ATTRIBUTE_KEYS

class GeneralDataPanel(RAMSTKPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _title: Any = ...
    txtCode: Any = ...
    txtName: Any = ...
    txtRemarks: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    def __do_set_callbacks(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...


class GeneralData(RAMSTKWorkView):
    _module: str = ...
    _tablabel: Any = ...
    _tabtooltip: Any = ...
    _lst_callbacks: Any = ...
    _lst_icons: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _pnlGeneralData: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def __make_ui(self) -> None:
        ...
