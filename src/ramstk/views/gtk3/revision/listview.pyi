# Stubs for ramstk.views.gtk3.revision.listview (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3.widgets import RAMSTKListView

class FailureDefinition(RAMSTKListView):
    def __init__(self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager) -> None:
        self._do_request_delete = None
        self.__do_load_tree = None
        self._do_load_tree = None
        ...

    def __make_ui(self):
        pass

    def pack_start(self, param, param1, param2, param3):
        pass

    def __make_buttonbox(self):
        pass


class UsageProfile(RAMSTKListView):
    def __init__(self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager) -> None:

    def _do_load_tree(self, param: object, row: object) -> object:
        pass

    def __make_ui(self):
        pass

    def __do_load_tree(self, param):
        pass

    def pack_start(self, param, param1, param2, param3):
        pass

    def __make_buttonbox(self):
        pass

    def _do_load_phase(self, _entity, identifier, row):
        pass

    def _do_load_mission(self, _entity, identifier, row):
        pass

    def _do_load_environment(self, _entity, identifier, row):
        pass
