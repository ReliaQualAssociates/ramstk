# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
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
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def do_request_delete(self, /, __button: Gtk.ToolButton) -> None: ...

class RequirementGeneralDataView(RAMSTKWorkView):
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...

class RequirementAnalysisView(RAMSTKWorkView):
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
