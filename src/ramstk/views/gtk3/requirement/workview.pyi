# Standard Library Imports
from typing import Any, Dict, Tuple

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKButton as RAMSTKButton
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKDateSelect as RAMSTKDateSelect
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import ATTRIBUTE_KEYS as ATTRIBUTE_KEYS

class GeneralDataPanel(RAMSTKPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _title: Any = ...
    btnValidateDate: Any = ...
    chkDerived: Any = ...
    chkValidated: Any = ...
    cmbOwner: Any = ...
    cmbRequirementType: Any = ...
    cmbPriority: Any = ...
    txtCode: Any = ...
    txtFigNum: Any = ...
    txtName: Any = ...
    txtPageNum: Any = ...
    txtSpecification: Any = ...
    txtValidatedDate: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_priorities(self) -> None:
        ...

    def do_load_requirement_types(
            self, requirement_types: Dict[int, Tuple[str]]) -> None:
        ...

    def do_load_workgroups(self, workgroups: Dict[int, Tuple[str]]) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...

    def _do_load_code(self, requirement_code: int) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...

    @staticmethod
    def _do_select_date(__button: RAMSTKButton, __event: Gdk.Event,
                        entry: RAMSTKEntry) -> str:
        ...

    def __do_set_callbacks(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...


class AnalysisPanel(RAMSTKPanel):
    def __init__(self) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...


class ClarityPanel(AnalysisPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _title: Any = ...
    chkClarityQ0: Any = ...
    chkClarityQ1: Any = ...
    chkClarityQ2: Any = ...
    chkClarityQ3: Any = ...
    chkClarityQ4: Any = ...
    chkClarityQ5: Any = ...
    chkClarityQ6: Any = ...
    chkClarityQ7: Any = ...
    chkClarityQ8: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...


class CompletenessPanel(AnalysisPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _title: Any = ...
    chkCompleteQ0: Any = ...
    chkCompleteQ1: Any = ...
    chkCompleteQ2: Any = ...
    chkCompleteQ3: Any = ...
    chkCompleteQ4: Any = ...
    chkCompleteQ5: Any = ...
    chkCompleteQ6: Any = ...
    chkCompleteQ7: Any = ...
    chkCompleteQ8: Any = ...
    chkCompleteQ9: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...


class ConsistencyPanel(AnalysisPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _title: Any = ...
    chkConsistentQ0: Any = ...
    chkConsistentQ1: Any = ...
    chkConsistentQ2: Any = ...
    chkConsistentQ3: Any = ...
    chkConsistentQ4: Any = ...
    chkConsistentQ5: Any = ...
    chkConsistentQ6: Any = ...
    chkConsistentQ7: Any = ...
    chkConsistentQ8: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...


class VerifiabilityPanel(AnalysisPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    _title: Any = ...
    chkVerifiableQ0: Any = ...
    chkVerifiableQ1: Any = ...
    chkVerifiableQ2: Any = ...
    chkVerifiableQ3: Any = ...
    chkVerifiableQ4: Any = ...
    chkVerifiableQ5: Any = ...
    _dic_attribute_updater: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    _record_id: Any = ...

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        ...


class GeneralData(RAMSTKWorkView):
    _module: str = ...
    _tablabel: str = ...
    _tabtooltip: str = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _pnlGeneralData: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _do_request_create_code(self, __button: Gtk.ToolButton) -> None:
        ...

    _record_id: Any = ...
    _parent_id: Any = ...

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        ...

    def __make_ui(self) -> None:
        ...


class RequirementAnalysis(RAMSTKWorkView):
    _module: str = ...
    _tablabel: str = ...
    _tabtooltip: str = ...
    _pnlClarity: Any = ...
    _pnlCompleteness: Any = ...
    _pnlConsistency: Any = ...
    _pnlVerifiability: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    _record_id: Any = ...
    _parent_id: Any = ...

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        ...

    def __make_ui(self) -> None:
        ...
