# Standard Library Imports
from typing import Any, Callable, Dict, List, Tuple

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
    _title: str
    _dic_row_loader: Dict[str, Callable]
    dic_attribute_widget_map: Dict[str, Any]
    def __init__(self) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: int
    _parent_id: int
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def _on_workview_edit(
        self, node_id: int, package: Dict[str, List[Any]]
    ) -> None: ...
    def __do_load_requirement(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...

class RequirementGeneralDataPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    btnValidateDate: RAMSTKButton
    chkDerived: RAMSTKCheckButton
    chkValidated: RAMSTKCheckButton
    cmbOwner: RAMSTKComboBox
    cmbRequirementType: RAMSTKComboBox
    cmbPriority: RAMSTKComboBox
    txtCode: RAMSTKEntry
    txtFigNum: RAMSTKEntry
    txtName: RAMSTKEntry
    txtPageNum: RAMSTKEntry
    txtSpecification: RAMSTKEntry
    txtValidatedDate: RAMSTKEntry
    dic_attribute_widget_map: Dict[str, List[Any]]
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
    _title: str
    chkClarityQ0: RAMSTKCheckButton
    chkClarityQ1: RAMSTKCheckButton
    chkClarityQ2: RAMSTKCheckButton
    chkClarityQ3: RAMSTKCheckButton
    chkClarityQ4: RAMSTKCheckButton
    chkClarityQ5: RAMSTKCheckButton
    chkClarityQ6: RAMSTKCheckButton
    chkClarityQ7: RAMSTKCheckButton
    chkClarityQ8: RAMSTKCheckButton
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...

class RequirementCompletenessPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    chkCompleteQ0: RAMSTKCheckButton
    chkCompleteQ1: RAMSTKCheckButton
    chkCompleteQ2: RAMSTKCheckButton
    chkCompleteQ3: RAMSTKCheckButton
    chkCompleteQ4: RAMSTKCheckButton
    chkCompleteQ5: RAMSTKCheckButton
    chkCompleteQ6: RAMSTKCheckButton
    chkCompleteQ7: RAMSTKCheckButton
    chkCompleteQ8: RAMSTKCheckButton
    chkCompleteQ9: RAMSTKCheckButton
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...

class RequirementConsistencyPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    chkConsistentQ0: RAMSTKCheckButton
    chkConsistentQ1: RAMSTKCheckButton
    chkConsistentQ2: RAMSTKCheckButton
    chkConsistentQ3: RAMSTKCheckButton
    chkConsistentQ4: RAMSTKCheckButton
    chkConsistentQ5: RAMSTKCheckButton
    chkConsistentQ6: RAMSTKCheckButton
    chkConsistentQ7: RAMSTKCheckButton
    chkConsistentQ8: RAMSTKCheckButton
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...

class RequirementVerifiabilityPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    chkVerifiableQ0: RAMSTKCheckButton
    chkVerifiableQ1: RAMSTKCheckButton
    chkVerifiableQ2: RAMSTKCheckButton
    chkVerifiableQ3: RAMSTKCheckButton
    chkVerifiableQ4: RAMSTKCheckButton
    chkVerifiableQ5: RAMSTKCheckButton
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
