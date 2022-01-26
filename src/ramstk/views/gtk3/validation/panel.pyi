# Standard Library Imports
from typing import Any, Dict, Tuple

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKButton as RAMSTKButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKDateSelect as RAMSTKDateSelect
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKSpinButton as RAMSTKSpinButton
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class ValidationTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: str
    _dic_row_loader: Any
    _lst_measurement_units: Any
    _lst_verification_types: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def do_load_measurement_units(
        self, measurement_unit: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def do_load_verification_types(
        self, verification_type: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: Any
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...

class ValidationTaskDescriptionPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Any
    btnEndDate: Any
    btnStartDate: Any
    cmbTaskType: Any
    cmbMeasurementUnit: Any
    spnStatus: Any
    txtTaskID: Any
    txtCode: Any
    txtMaxAcceptable: Any
    txtMeanAcceptable: Any
    txtMinAcceptable: Any
    txtVarAcceptable: Any
    txtSpecification: Any
    txtTask: Any
    txtEndDate: Any
    txtStartDate: Any
    _dic_task_types: Any
    _dic_units: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def do_load_measurement_units(
        self, measurement_unit: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def do_load_validation_types(
        self, validation_type: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def _do_make_task_code(self, combo: RAMSTKComboBox) -> None: ...
    @staticmethod
    def _do_select_date(
        __button: RAMSTKButton, __event: Gdk.Event, entry: RAMSTKEntry
    ) -> str: ...

class ValidationTaskEffortPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Any
    txtMinTime: Any
    txtExpTime: Any
    txtMaxTime: Any
    txtMinCost: Any
    txtExpCost: Any
    txtMaxCost: Any
    txtMeanTimeLL: Any
    txtMeanTime: Any
    txtMeanTimeUL: Any
    txtMeanCostLL: Any
    txtMeanCost: Any
    txtMeanCostUL: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def _do_load_code(self, task_code: int) -> None: ...
    def _do_make_task_code(self, task_type: str) -> str: ...
    @staticmethod
    def _do_select_date(
        __button: RAMSTKButton, __event: Gdk.Event, entry: RAMSTKEntry
    ) -> str: ...
    def _on_calculate_task(self, tree: treelib.Tree) -> None: ...
    def __do_adjust_widgets(self) -> None: ...
