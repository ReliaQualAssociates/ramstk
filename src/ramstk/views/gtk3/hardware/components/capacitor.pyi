# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry

# RAMSTK Local Imports
from .panels import RAMSTKAssessmentInputPanel as RAMSTKAssessmentInputPanel
from .panels import RAMSTKAssessmentResultPanel as RAMSTKAssessmentResultPanel

class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
    cmbConfiguration: Any = ...
    cmbConstruction: Any = ...
    cmbSpecification: Any = ...
    cmbStyle: Any = ...
    txtCapacitance: Any = ...
    txtESR: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        ...


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    txtPiCV: Any = ...
    txtPiCF: Any = ...
    txtPiC: Any = ...

    def __init__(self) -> None:
        ...
