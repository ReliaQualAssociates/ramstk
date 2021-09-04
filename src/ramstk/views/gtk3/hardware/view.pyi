# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTK_ACTIVE_ENVIRONMENTS as RAMSTK_ACTIVE_ENVIRONMENTS,
)
from ramstk.configuration import (
    RAMSTK_DORMANT_ENVIRONMENTS as RAMSTK_DORMANT_ENVIRONMENTS,
)
from ramstk.configuration import RAMSTK_HR_DISTRIBUTIONS as RAMSTK_HR_DISTRIBUTIONS
from ramstk.configuration import RAMSTK_HR_MODELS as RAMSTK_HR_MODELS
from ramstk.configuration import RAMSTK_HR_TYPES as RAMSTK_HR_TYPES
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.design_electric import (
    DesignElectricEnvironmentalInputPanel as DesignElectricEnvironmentalInputPanel,
)
from ramstk.views.gtk3.design_electric import (
    DesignElectricStressInputPanel as DesignElectricStressInputPanel,
)
from ramstk.views.gtk3.design_electric import (
    ICDesignElectricInputPanel as ICDesignElectricInputPanel,
)
from ramstk.views.gtk3.reliability import ReliabilityInputPanel as ReliabilityInputPanel
from ramstk.views.gtk3.widgets import RAMSTKModuleView as RAMSTKModuleView
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import HardwareGeneralDataPanel as HardwareGeneralDataPanel
from . import HardwareLogisticsPanel as HardwareLogisticsPanel
from . import HardwareMiscellaneousPanel as HardwareMiscellaneousPanel
from . import HardwareTreePanel as HardwareTreePanel

class HardwareModuleView(RAMSTKModuleView):
    _module: str
    _tablabel: str
    _tabtooltip: str
    _lst_mnu_labels: Any
    _lst_tooltips: Any
    _pnlPanel: Any
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_calculate_hardware(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_calculate_all_hardware(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> Any: ...
    def _do_request_insert_part(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> Any: ...
    _record_id: Any
    _parent_id: Any
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...

class HardwareGeneralDataView(RAMSTKWorkView):
    _module: str
    _tablabel: str
    _tabtooltip: str
    _pnlGeneralData: Any
    _pnlLogistics: Any
    _pnlMiscellaneous: Any
    _lst_callbacks: Any
    _lst_icons: Any
    _lst_mnu_labels: Any
    _lst_tooltips: Any
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_make_comp_ref_des(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...

class HardwareAssessmentInputView(RAMSTKWorkView):
    _lst_title: List[str]
    _module: str
    _tablabel: str
    _tabtooltip: str
    _dic_component_panels: Any
    _lst_callbacks: Any
    _lst_icons: Any
    _lst_tooltips: Any
    _pnlReliabilityInput: Any
    _pnlEnvironmentalInput: Any
    _pnlStressInput: Any
    _vpnLeft: Any
    _vpnRight: Any
    _hazard_rate_method_id: int
    _subcategory_id: int
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_pack_component_panel(self, attributes: Dict[str, Any]) -> None: ...
    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_update(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...
