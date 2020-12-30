# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry

# RAMSTK Local Imports
from .panels import RAMSTKAssessmentInputPanel as RAMSTKAssessmentInputPanel
from .panels import RAMSTKAssessmentResultPanel as RAMSTKAssessmentResultPanel

class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
    cmbApplication: Any = ...
    cmbConstruction: Any = ...
    cmbMatching: Any = ...
    cmbPackage: Any = ...
    cmbType: Any = ...
    txtFrequencyOperating: Any = ...
    txtNElements: Any = ...
    txtThetaJC: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        ...


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    txtPiA: Any = ...
    txtPiC: Any = ...
    txtPiI: Any = ...
    txtPiM: Any = ...
    txtPiP: Any = ...
    txtPiR: Any = ...
    txtPiS: Any = ...
    txtPiT: Any = ...

    def __init__(self) -> None:
        ...
