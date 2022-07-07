# Standard Library Imports
from typing import Dict, List, Tuple, Union

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
from ramstk.views.gtk3.widgets import RAMSTKMatrixPanel as RAMSTKMatrixPanel
from ramstk.views.gtk3.widgets import RAMSTKSpinButton as RAMSTKSpinButton
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel
from ramstk.views.gtk3.widgets import RAMSTKWidget as RAMSTKWidget

class RAMSTKValidationTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: str
    _measurement_units: List[str]
    _verification_types: List[str]
    dic_attribute_widget_map: Dict[str, List[Union[bool, float, int, object, str]]]
    def __init__(self) -> None: ...
    def do_load_measurement_units(
        self, measurement_unit_dic: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def do_load_verification_types(
        self, verification_type_dic: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: int
    def _on_row_change(self, selection_obj: Gtk.TreeSelection) -> None: ...
    def _on_workview_edit(
        self, node_id: int, package: Dict[str, Union[bool, float, int, str]]
    ) -> None: ...
    def __do_load_validation(
        self, node_obj: treelib.Node, row_obj: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...

class RAMSTKValidationTaskDescriptionPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
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
    txtTask: RAMSTKEntry
    txtEndDate: RAMSTKEntry
    txtStartDate: RAMSTKEntry
    _dic_task_types: Dict[int, List[str]]
    _dic_units: Dict[int, str]
    dic_attribute_widget_map: Dict[str, List[Union[bool, float, int, object, str]]]
    def __init__(self) -> None: ...
    def do_load_measurement_units(
        self, measurement_unit_dic: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def do_load_validation_types(
        self, validation_type_dic: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def _do_make_task_code(self, combo_obj: RAMSTKComboBox) -> None: ...
    @staticmethod
    def _do_select_date(
        __button_obj: RAMSTKButton, __event_obj: Gdk.Event, entry_obj: RAMSTKEntry
    ) -> str: ...

class RAMSTKValidationTaskEffortPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    txtMinTime: RAMSTKEntry
    txtExpTime: RAMSTKEntry
    txtMaxTime: RAMSTKEntry
    txtMinCost: RAMSTKEntry
    txtExpCost: RAMSTKEntry
    txtMaxCost: RAMSTKEntry
    txtMeanTimeLL: RAMSTKEntry
    txtMeanTime: RAMSTKEntry
    txtMeanTimeUL: RAMSTKEntry
    txtMeanCostLL: RAMSTKEntry
    txtMeanCost: RAMSTKEntry
    txtMeanCostUL: RAMSTKEntry
    _dic_task_types: Dict[int, List[str]]
    dic_attribute_widget_map: Dict[str, List[Union[bool, float, int, object, str]]]
    def __init__(self) -> None: ...
    def do_load_validation_types(
        self, validation_type_dic: Dict[int, Tuple[str, str]]
    ) -> None: ...
    def _do_load_code(self, task_code_int: int) -> None: ...
    def _do_make_task_code(self, task_type_str: str) -> str: ...
    @staticmethod
    def _do_select_date(
        __button_obj: RAMSTKButton, __event_obj: Gdk.Event, entry_obj: RAMSTKEntry
    ) -> str: ...
    def _on_calculate_task(
        self, attributes: Dict[str, Union[float, int, str]]
    ) -> None: ...
    def __do_adjust_widgets(self) -> None: ...

class RAMSTKValidationRequirementPanel(RAMSTKMatrixPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    def __init__(self) -> None: ...
    def _do_set_column_headers(self, tree_obj: treelib.Tree) -> None: ...
    def _do_set_row_headers(self, tree_obj: treelib.Tree) -> None: ...
