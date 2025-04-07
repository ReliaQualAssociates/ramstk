# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKButton as RAMSTKButton
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKDateSelectDialog as RAMSTKDateSelectDialog
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class RequirementGeneralDataPanel(RAMSTKFixedPanel):
    btnValidateDate: RAMSTKButton
    chkDerived: RAMSTKCheckButton
    chkValidated: RAMSTKCheckButton
    cmbOwner: RAMSTKComboBox
    cmbRequirementType: RAMSTKComboBox
    cmbPriority: RAMSTKComboBox
    txtCode: RAMSTKEntry
    txtFigNum: RAMSTKEntry
    txtName: RAMSTKTextView
    txtPageNum: RAMSTKEntry
    txtSpecification: RAMSTKEntry
    txtValidatedDate: RAMSTKEntry
    def __init__(self) -> None: ...
    def do_load_priorities(self) -> None: ...
    def do_load_requirement_types(
        self, requirement_types: dict[int, tuple[str]]
    ) -> None: ...
    def do_load_workgroups(self, workgroups: dict[int, tuple[str]]) -> None: ...
