# Stubs for ramstk.views.gtk3.widgets.dialog (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from ramstk.views.gtk3 import Gtk
from typing import Any, Optional, Tuple

class RAMSTKDialog(Gtk.Dialog):
    def __init__(self, dlgtitle: str, **kwargs: Any) -> None:
        self.vbox = None
        ...
    def do_destroy(self) -> None: ...
    def do_run(self) -> Any: ...

    def run(self):
        pass

    def destroy(self):
        pass

    def add_buttons(self, param):
        pass

    def set_destroy_with_parent(self, param):
        pass

    def set_modal(self, param):
        pass

    def set_property(self, param, _dlgparent):
        pass

    def set_title(self, dlgtitle):
        pass


class RAMSTKMessageDialog(Gtk.MessageDialog):
    def __init__(self, prompt: str, icon: str, criticality: str, parent: Gtk.Window=...) -> None: ...
    def do_run(self) -> Any: ...
    def do_destroy(self) -> None: ...

    def add_buttons(self, param, OK):
        pass

    def set_parent(self, parent):
        pass

    def set_destroy_with_parent(self, param):
        pass

    def set_modal(self, param):
        pass

    def set_image(self, _image):
        pass

    def set_markup(self, prompt):
        pass

    def set_property(self, param, _criticality):
        pass

    def show_all(self):
        pass

    def run(self):
        pass

    def destroy(self):
        pass


class RAMSTKDateSelect(Gtk.Dialog):
    def __init__(self) -> None:
        self._calendar = None
        self.vbox = None
        ...
    def do_destroy(self) -> None: ...
    def do_run(self) -> Any: ...

    def add_buttons(self, STOCK_OK, ACCEPT):
        pass

    def set_title(self, param):
        pass

    def destroy(self):
        pass

    def run(self):
        pass


class RAMSTKFileChooser(Gtk.FileChooserDialog):
    def __init__(self, title: str, **kwargs: Any) -> None: ...
    def do_run(self) -> Tuple[Optional[Any], Optional[Any]]: ...
    def do_destroy(self) -> None: ...

    def add_buttons(self, STOCK_OK, ACCEPT, STOCK_CANCEL, REJECT):
        pass

    def set_destroy_with_parent(self, param):
        pass

    def set_modal(self, param):
        pass

    def set_property(self, param, _dlgparent):
        pass

    def set_title(self, title):
        pass

    def set_action(self, SAVE):
        pass
