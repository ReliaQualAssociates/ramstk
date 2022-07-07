# Standard Library Imports
from typing import Callable, Dict, List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog as RAMSTKMessageDialog
from ramstk.views.gtk3.widgets import RAMSTKModuleView as RAMSTKModuleView
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import RAMSTKValidationRequirementPanel as RAMSTKValidationRequirementPanel
from . import (
    RAMSTKValidationTaskDescriptionPanel as RAMSTKValidationTaskDescriptionPanel,
)
from . import RAMSTKValidationTaskEffortPanel as RAMSTKValidationTaskEffortPanel
from . import RAMSTKValidationTreePanel as RAMSTKValidationTreePanel

class RAMSTKValidationModuleView(RAMSTKModuleView):
    _tag: str
    _tablabel: str
    _tabtooltip: str
    _lst_mnu_labels: List[str]
    _lst_tooltips: List[str]
    _pnlPanel: RAMSTKValidationTreePanel

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def do_request_delete(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: int

    def _do_set_record_id(
        self,
        attributes: Dict[str, Union[bool, int, float, str]],
    ) -> None: ...
    def __make_ui(self) -> None: ...

class RAMSTKValidationGeneralDataView(RAMSTKWorkView):
    _tag: str
    _tablabel: str
    _tabtooltip: str
    _lst_callbacks: List[Callable]
    _lst_icons: List[str]
    _lst_mnu_labels: List[str]
    _lst_tooltips: List[str]
    _pnlTaskDescription: RAMSTKValidationTaskDescriptionPanel
    _pnlTaskEffort: RAMSTKValidationTaskEffortPanel

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: int

    def _do_set_record_id(
        self,
        attributes: Dict[str, Union[bool, float, int, str]],
    ) -> None: ...
    def __make_ui(self) -> None: ...

class RAMSTKValidationMatrixView(RAMSTKWorkView):
    _tag: str
    _tablabel: str
    _tabtooltip: str
    _record_id: int
    _lst_callbacks: List[Callable]
    _lst_icons: List[str]
    _lst_mnu_labels: List[str]
    _lst_tooltips: List[str]
    _pnlRequirementMatrix: RAMSTKValidationRequirementPanel

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_set_record_id(
        self,
        attributes: Dict[str, Union[bool, float, int, str]],
    ) -> None: ...
    def __do_load_lists(self) -> None: ...
    def __make_ui(self) -> None: ...
