# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog as RAMSTKMessageDialog
from ramstk.views.gtk3.widgets import RAMSTKModuleView as RAMSTKModuleView
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import RequirementClarityPanel as RequirementClarityPanel
from . import RequirementCompletenessPanel as RequirementCompletenessPanel
from . import RequirementConsistencyPanel as RequirementConsistencyPanel
from . import RequirementGeneralDataPanel as RequirementGeneralDataPanel
from . import RequirementTreePanel as RequirementTreePanel
from . import RequirementVerifiabilityPanel as RequirementVerifiabilityPanel

class RequirementModuleView(RAMSTKModuleView):
    _module: str
    _tablabel: str
    _tabtooltip: str
    _lst_mnu_labels: Any
    _lst_tooltips: Any
    _pnlPanel: Any
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def do_request_delete(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...

class RequirementGeneralDataView(RAMSTKWorkView):
    _module: str
    _tablabel: str
    _tabtooltip: str
    _lst_mnu_labels: Any
    _lst_tooltips: Any
    _pnlGeneralData: Any
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_create_code(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...

class RequirementAnalysisView(RAMSTKWorkView):
    _module: str
    _tablabel: str
    _tabtooltip: str
    _pnlClarity: Any
    _pnlCompleteness: Any
    _pnlConsistency: Any
    _pnlVerifiability: Any
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...
