# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKButton as RAMSTKButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKDateSelectDialog as RAMSTKDateSelectDialog
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKSpinButton as RAMSTKSpinButton
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import WidgetConfig as WidgetConfig

class ValidationTaskDescriptionPanel(RAMSTKFixedPanel):
    btnEndDate: RAMSTKButton
    btnStartDate: RAMSTKButton
    cmbTaskType: RAMSTKComboBox
    cmbMeasurementUnit: RAMSTKComboBox
    spnStatus: RAMSTKSpinButton
    txtTaskID: RAMSTKEntry
    txtCode: RAMSTKEntry
    txtMaxAcceptable: RAMSTKEntry
    txtMeanAcceptable: RAMSTKEntry
    txtMinAcceptable: RAMSTKEntry
    txtVarAcceptable: RAMSTKEntry
    txtSpecification: RAMSTKEntry
    txtTask: RAMSTKTextView
    txtEndDate: RAMSTKEntry
    txtStartDate: RAMSTKEntry
    def __init__(self) -> None: ...
    def do_load_measurement_units(
        self, measurement_unit: dict[int, tuple[str, str]]
    ) -> None: ...
    def do_load_validation_types(
        self, validation_type: dict[int, tuple[str, str]]
    ) -> None: ...
