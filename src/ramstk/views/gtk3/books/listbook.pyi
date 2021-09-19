# Standard Library Imports
from typing import Dict, List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3.failure_definition import (
    FailureDefinitionListView as FailureDefinitionListView,
)
from ramstk.views.gtk3.widgets import RAMSTKBaseBook as RAMSTKBaseBook

class RAMSTKListBook(RAMSTKBaseBook):
    _dic_list_views: Dict[str, List[object]]
    _module: str
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _on_close(self) -> None: ...
    def _on_module_change(self, module: str = ...) -> None: ...
