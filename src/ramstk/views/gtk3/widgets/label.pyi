# Standard Library Imports
from typing import Any, Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk

# RAMSTK Local Imports
from .widget import RAMSTKWidget as RAMSTKWidget

class RAMSTKLabel(Gtk.Label, RAMSTKWidget):
    _default_height: int = ...
    _default_width: int = ...

    def __init__(self, text: str) -> None:
        ...

    def get_attribute(self, attribute: str) -> Any:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...


def do_make_label_group(
        text: List[str], **kwargs: Dict[str,
                                        Any]) -> Tuple[int, List[RAMSTKLabel]]:
    ...
