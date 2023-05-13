# Standard Library Imports
from typing import Dict

# Third Party Imports
from _typeshed import Incomplete

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError as DataAccessError

# RAMSTK Local Imports
from .basedatabase import BaseDatabase as BaseDatabase

class RAMSTKProgramDB(BaseDatabase):
    tables: Incomplete
    dic_views: Incomplete
    def __init__(self) -> None: ...
    def _do_create_database(self, database: Dict[str, str], sql_file: str) -> None: ...
    def do_open_program(self, database: Dict[str, str]) -> None: ...
    def do_close_program(self) -> None: ...
    @staticmethod
    def do_save_program() -> None: ...
