# Standard Library Imports
from typing import Any, Callable, Dict, List, Tuple, Union

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.models.dbrecords import RAMSTKCauseRecord as RAMSTKCauseRecord
from ramstk.models.dbrecords import RAMSTKMechanismRecord as RAMSTKMechanismRecord
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class FMEAMethodPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    chkCriticality: RAMSTKCheckButton
    chkRPN: RAMSTKCheckButton
    txtItemCriticality: RAMSTKTextView
    _on_edit_message: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    def __init__(self) -> None: ...
    def _do_load_item_criticality(self, item_criticality: Dict[str, float]) -> None: ...

class FMEATreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: str
    _dic_mission_phases: Dict[str, List[str]]
    _dic_row_loader: Dict[str, Callable]
    _dic_visible_mask: Dict[str, List[str]]
    _lst_missions: List[str]
    _on_edit_message: str
    dic_attribute_widget_map: Dict[str, List[Any]]
    dic_icons: Dict[str, str]
    lst_action_category: List[str]
    lst_action_status: List[str]
    lst_control_types: List[str]
    lst_rpn_detection: List[str]
    lst_rpn_occurrence: List[str]
    lst_rpn_severity: List[str]
    lst_mode_probability: List[str]
    lst_severity_class: List[str]
    lst_users: List[str]
    def __init__(self) -> None: ...
    def do_load_comboboxes(self) -> None: ...
    def _on_mission_change(
        self, __combo: Gtk.CellRendererCombo, path: str, new_text: str
    ) -> None: ...
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...
    def __do_get_rpn_names(
        self, entity: Union[RAMSTKCauseRecord, RAMSTKMechanismRecord]
    ) -> Tuple[str, str, str, str]: ...
    def __do_load_action(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_action_category(self) -> None: ...
    def __do_load_action_status(self) -> None: ...
    def __do_load_cause(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_control(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_control_type(self) -> None: ...
    def __do_load_mechanism(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter: ...
    def __do_load_missions(
        self,
        tree: treelib.Tree = ...,
        node_id: Any = ...,
        row: Gtk.TreeIter = ...,
    ) -> None: ...
    def __do_load_mission_phases(self, mission: str) -> None: ...
    def __do_load_mode(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter: ...
    def __do_load_mode_probability(self) -> None: ...
    def __do_load_rpn_detection(self) -> None: ...
    def __do_load_rpn_occurrence(self) -> None: ...
    def __do_load_rpn_severity(self) -> None: ...
    def __do_load_severity_class(self) -> None: ...
    def __do_load_users(self) -> None: ...
