# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKModuleView as RAMSTKModuleView
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import FunctionGeneralDataPanel as FunctionGeneralDataPanel
from . import FunctionTreePanel as FunctionTreePanel

class FunctionModuleView(RAMSTKModuleView):
    _module: str
    _tablabel: str
    _tabtooltip: str
    _lst_mnu_labels: Any
    _lst_tooltips: Any
    _pnlPanel: Any
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...

class FunctionWorkView(RAMSTKWorkView):
    _module: str
    _tablabel: Any
    _tabtooltip: Any
    _lst_mnu_labels: Any
    _lst_tooltips: Any
    _pnlGeneralData: Any
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...
