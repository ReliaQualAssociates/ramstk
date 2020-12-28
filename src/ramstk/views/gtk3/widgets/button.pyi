# Standard Library Imports
from typing import Any, Union

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from .widget import RAMSTKWidget as RAMSTKWidget

def do_make_buttonbox(view: Any,
                      **kwargs: Any) -> Union[Gtk.HButtonBox, Gtk.VButtonBox]:
    ...


class RAMSTKButton(Gtk.Button, RAMSTKWidget):
    _default_height: int = ...
    _default_width: int = ...

    def __init__(self, label: str = ...) -> None:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...


class RAMSTKCheckButton(Gtk.CheckButton, RAMSTKWidget):
    _default_height: int = ...
    _default_width: int = ...

    def __init__(self, label: str = ...) -> None:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...

    def do_update(self, value: int, signal: str = ...) -> None:
        ...


class RAMSTKOptionButton(Gtk.RadioButton, RAMSTKWidget):
    def __init__(self, group: Gtk.RadioButton = ..., label: str = ...) -> None:
        ...


class RAMSTKSpinButton(Gtk.SpinButton, RAMSTKWidget):
    _default_height: int = ...
    _default_width: int = ...

    def __init__(self) -> None:
        ...

    def do_get_text(self) -> float:
        ...

    def do_set_properties(self, **kwargs: Any) -> None:
        ...

    def do_update(self, value: int, signal: str = ...) -> None:
        ...
