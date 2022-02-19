# Standard Library Imports
from typing import Dict, List, Union

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.assistants import EditFunction as EditFunction
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

# RAMSTK Local Imports
from . import SimilarItemMethodPanel as SimilarItemMethodPanel
from . import SimilarItemTreePanel as SimilarItemTreePanel

class SimilarItemWorkView(RAMSTKWorkView):
    _tag: str
    _tablabel: str
    _tabtooltip: str
    _lst_mnu_labels: List[str]
    _lst_tooltips: List[str]
    _pnlMethod: RAMSTKPanel
    _pnlPanel: RAMSTKPanel
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    _record_id: int
    _parent_id: int
    def _do_set_record_id(
        self, attributes: Dict[str, Union[float, int, str]]
    ) -> None: ...
    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_edit_function(self, __button: Gtk.ToolButton) -> None: ...
    def _do_request_rollup(self, __button: Gtk.ToolButton) -> None: ...
    def __make_ui(self) -> None: ...
