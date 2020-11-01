# Stubs for ramstk.views.gtk3.books.modulebook (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3.widgets import RAMSTKBaseBook

class RAMSTKModuleBook(RAMSTKBaseBook):
    icoStatus: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        self._on_switch_page = None
        self._lst_handler_id = None
        self._dic_module_views = None
        self._on_close = None
        self._on_open = None
        ...

    def insert_page(self, param, tab_label, position):
        pass

    def __make_ui(self):
        pass

    def __set_callbacks(self):
        pass

    def show_all(self):
        pass

    def set_current_page(self, param):
        pass

    def connect(self, param, _on_switch_page):
        pass

    def get_n_pages(self):
        pass

    def remove_page(self, param):
        pass
