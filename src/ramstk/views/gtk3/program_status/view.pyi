# Standard Library Imports
from typing import Any, Callable, Dict, List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKFrame as RAMSTKFrame
from ramstk.views.gtk3.widgets import RAMSTKPlot as RAMSTKPlot
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import ProgramStatusPlotPanel as ProgramStatusPlotPanel

class ProgramStatusWorkView(RAMSTKWorkView):
    _tag: str
    _tablabel: str
    _tabtooltip: str
    _lst_callbacks: List[Callable]
    _lst_icons: List[str]
    _lst_mnu_labels: List[str]
    _lst_tooltips: List[str]
    _pnlPanel: ProgramStatusPlotPanel
    _title: str
    pltPlot: RAMSTKPlot
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None: ...
    def _do_set_cursor_active(self, attributes: Dict[str, Any]) -> None: ...
    _record_id: int
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...
