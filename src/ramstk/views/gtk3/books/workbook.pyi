# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3.function import FunctionWorkView as FunctionWorkView
from ramstk.views.gtk3.revision import RevisionWorkView as RevisionWorkView
from ramstk.views.gtk3.widgets import RAMSTKBaseBook as RAMSTKBaseBook
from ramstk.views.gtk3.widgets import RAMSTKBaseView as RAMSTKBaseView

class RAMSTKWorkBook(RAMSTKBaseBook):
    dic_work_views: Any
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _on_module_change(self, module: str = ...) -> None: ...
