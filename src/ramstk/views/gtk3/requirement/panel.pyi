# Standard Library Imports
from typing import Any, Dict, Tuple

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKButton as RAMSTKButton
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKDateSelect as RAMSTKDateSelect
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class RequirementTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: Any
    _dic_row_loader: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def __do_load_requirement(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...

class RequirementGeneralDataPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Any
    btnValidateDate: Any
    chkDerived: Any
    chkValidated: Any
    cmbOwner: Any
    cmbRequirementType: Any
    cmbPriority: Any
    txtCode: Any
    txtFigNum: Any
    txtName: Any
    txtPageNum: Any
    txtSpecification: Any
    txtValidatedDate: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def do_load_priorities(self) -> None: ...
    def do_load_requirement_types(
        self, requirement_types: Dict[int, Tuple[str]]
    ) -> None: ...
    def do_load_workgroups(self, workgroups: Dict[int, Tuple[str]]) -> None: ...
    def _do_load_code(self, requirement_code: int) -> None: ...
    @staticmethod
    def _do_select_date(
        __button: RAMSTKButton, __event: Gdk.Event, entry: RAMSTKEntry
    ) -> str: ...

class RequirementClarityPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Any
    chkClarityQ0: Any
    chkClarityQ1: Any
    chkClarityQ2: Any
    chkClarityQ3: Any
    chkClarityQ4: Any
    chkClarityQ5: Any
    chkClarityQ6: Any
    chkClarityQ7: Any
    chkClarityQ8: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...

class RequirementCompletenessPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Any
    chkCompleteQ0: Any
    chkCompleteQ1: Any
    chkCompleteQ2: Any
    chkCompleteQ3: Any
    chkCompleteQ4: Any
    chkCompleteQ5: Any
    chkCompleteQ6: Any
    chkCompleteQ7: Any
    chkCompleteQ8: Any
    chkCompleteQ9: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...

class RequirementConsistencyPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Any
    chkConsistentQ0: Any
    chkConsistentQ1: Any
    chkConsistentQ2: Any
    chkConsistentQ3: Any
    chkConsistentQ4: Any
    chkConsistentQ5: Any
    chkConsistentQ6: Any
    chkConsistentQ7: Any
    chkConsistentQ8: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...

class RequirementVerifiabilityPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Any
    chkVerifiableQ0: Any
    chkVerifiableQ1: Any
    chkVerifiableQ2: Any
    chkVerifiableQ3: Any
    chkVerifiableQ4: Any
    chkVerifiableQ5: Any
    dic_attribute_index_map: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
