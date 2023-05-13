# Standard Library Imports
from typing import Any, Dict, List, TextIO, Tuple

# Third Party Imports
from _typeshed import Incomplete
from sqlalchemy import Select as Select
from sqlalchemy.engine import Engine as Engine
from sqlalchemy.orm import query as query
from sqlalchemy.orm import scoped_session

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError as DataAccessError

def do_create_postgres_db(database: Dict[str, str], sql_file: TextIO) -> None: ...
def do_create_sqlite3_db(database: Dict[str, str], sql_file: TextIO) -> None: ...
def do_open_session(database: str) -> Tuple[Engine, scoped_session]: ...

class BaseDatabase:
    sqlstatements: Dict[str, str]
    cxnargs: Incomplete
    engine: Incomplete
    session: Incomplete
    database: str
    def __init__(self) -> None: ...
    def do_connect(self, database: Dict) -> None: ...
    def do_create_database(self, database: Dict[str, str], sql_file: str) -> None: ...
    def do_delete(self, item: object) -> None: ...
    def do_disconnect(self) -> None: ...
    def do_execute_query(self, query_: Select) -> List[object]: ...
    def do_insert(self, record: object) -> None: ...
    def do_insert_many(self, records: List[object]) -> None: ...
    def do_select_all(self, table, **kwargs) -> query.Query: ...
    def do_update(self, record: object = ...) -> None: ...
    def get_database_list(self, database: Dict[str, str]) -> List: ...
    def get_last_id(self, table: str, id_column: str) -> Any: ...
