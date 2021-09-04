# Standard Library Imports
from typing import Any, Dict, Tuple

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class HardwareTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: Any
    _dic_row_loader: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    dic_icons: Any
    def __init__(self) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def __do_load_hardware(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...

class HardwareGeneralDataPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: Any
    chkRepairable: Any
    cmbCategory: Any
    cmbSubcategory: Any
    txtAltPartNum: Any
    txtCompRefDes: Any
    txtDescription: Any
    txtFigureNumber: Any
    txtLCN: Any
    txtName: Any
    txtPageNumber: Any
    txtPartNumber: Any
    txtRefDes: Any
    txtSpecification: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    dicSubcategories: Any
    def __init__(self) -> None: ...
    def do_load_categories(self, category: Dict[int, str]) -> None: ...
    def _do_load_subcategories(self, category_id: int) -> None: ...
    def _request_load_component(self, combo: RAMSTKComboBox) -> None: ...
    def _request_load_subcategories(self, combo: RAMSTKComboBox) -> None: ...

class HardwareLogisticsPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: Any
    cmbCostType: Any
    cmbManufacturer: Any
    txtCAGECode: Any
    txtCost: Any
    txtNSN: Any
    txtQuantity: Any
    txtYearMade: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def do_load_cost_types(self) -> None: ...
    def do_load_manufacturers(
        self, manufacturers: Dict[int, Tuple[str, str, str]]
    ) -> None: ...
    def _do_load_cage_code(self, combo: RAMSTKComboBox) -> None: ...

class HardwareMiscellaneousPanel(RAMSTKFixedPanel):
    _select_msg: str
    _tag: str
    _title: Any
    chkTagged: Any
    txtAttachments: Any
    txtRemarks: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
