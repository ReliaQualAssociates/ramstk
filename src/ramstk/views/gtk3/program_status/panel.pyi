# Standard Library Imports
from typing import Dict, List

# Third Party Imports
import pandas as pd

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKPlotPanel as RAMSTKPlotPanel

class ProgramStatusPlotPanel(RAMSTKPlotPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    lst_axis_labels: List[str]
    lst_legend: List[str]
    plot_title: str
    def __init__(self) -> None: ...
    def _do_load_panel(self, attributes: Dict[str, pd.DataFrame]) -> None: ...
    def _do_load_assessment_milestones(
        self, assessed: pd.DataFrame, y_max: float
    ) -> None: ...
    def _do_load_plan(self, plan: pd.DataFrame) -> None: ...
