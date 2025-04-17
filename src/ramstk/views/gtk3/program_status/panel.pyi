# Third Party Imports
import pandas as pd
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages as do_subscribe_to_messages
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKPlotPanel as RAMSTKPlotPanel

class ProgramStatusPlotPanel(RAMSTKPlotPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Incomplete
    lst_axis_labels: Incomplete
    lst_legend: Incomplete
    plot_title: Incomplete
    def __init__(self) -> None: ...
    def _do_load_panel(self, attributes: dict[str, pd.DataFrame]) -> None: ...
    def _do_load_actuals(self, status: pd.DataFrame) -> None: ...
    def _do_load_assessment_milestones(
        self, assessed: pd.DataFrame, y_max: float
    ) -> None: ...
    def _do_load_plan(self, plan: pd.DataFrame) -> None: ...
