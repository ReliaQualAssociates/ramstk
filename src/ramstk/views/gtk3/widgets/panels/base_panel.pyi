# RAMSTK Local Imports
from ..frame import RAMSTKFrame as RAMSTKFrame
from ..widget import RAMSTKBaseWidget as RAMSTKBaseWidget
from ..widget import WidgetConfig as WidgetConfig

def do_log_message(
    method_name: str, topic_name: str, logger_name: str, message: str
) -> None: ...

class RAMSTKBasePanel(RAMSTKFrame):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    _lst_widget_configuration: list[WidgetConfig]
    _parent_id: int
    _record_id: int
    def __init__(self) -> None: ...
    def do_set_widget_attributes(self) -> None: ...
    def do_set_widget_callbacks(self) -> None: ...
    def do_set_widget_properties(self) -> None: ...
    @staticmethod
    def do_set_widget_sensitivity(
        widgets: list[RAMSTKBaseWidget], sensitive: bool = True
    ) -> None: ...
