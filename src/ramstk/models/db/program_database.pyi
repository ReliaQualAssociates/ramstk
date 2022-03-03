# Standard Library Imports
from typing import Dict

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.db import BaseDatabase as BaseDatabase
from ramstk.db import do_create_program_db as do_create_program_db
from ramstk.exceptions import DataAccessError as DataAccessError

class RAMSTKProgramDB:
    dic_tables: Dict[str, object]
    dic_views: Dict[str, object]
    user_configuration: RAMSTKUserConfiguration
    program_dao: BaseDatabase
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
