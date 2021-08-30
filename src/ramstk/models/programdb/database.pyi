# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.db import BaseDatabase

class RAMSTKProgramDB:
    dic_tables: Any
    dic_views: Any
    user_configuration: Any
    program_dao: Any
    def __init__(self) -> None: ...
    def do_create_program(
        self, program_db: BaseDatabase, database: Dict[str, str]
    ) -> None: ...
    def do_open_program(
        self, program_db: BaseDatabase, database: Dict[str, str]
    ) -> None: ...
    def do_close_program(self) -> None: ...
    @staticmethod
    def do_save_program() -> None: ...
