# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
import pandas as pd
import treelib

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.db.base import BaseDatabase as BaseDatabase
from ramstk.models.programdb import RAMSTKMatrix as RAMSTKMatrix

class RAMSTKAnalysisManager:
    RAMSTK_USER_CONFIGURATION: Any = ...
    _attributes: Any = ...
    _tree: Any = ...
    RAMSTK_CONFIGURATION: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        ...

    def on_get_all_attributes(self, attributes: Dict[str, Any]) -> None:
        ...

    def on_get_tree(self, dmtree: treelib.Tree) -> None:
        ...


class RAMSTKDataManager:
    _root: int = ...
    _tag: str = ...
    _pkey: Any = ...
    _parent_id: int = ...
    _revision_id: int = ...
    dao: Any = ...
    last_id: int = ...
    tree: Any = ...
    _mtx_prefix: Any = ...

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def _on_select_revision(self, attributes: Dict[str, Any]) -> None:
        ...

    @staticmethod
    def do_build_dict(records: List[object],
                      id_field: str) -> Dict[int, object]:
        ...

    def do_connect(self, dao: BaseDatabase) -> None:
        ...

    def do_create_all_codes(self, prefix: str) -> None:
        ...

    def do_delete(self, node_id: int, table: str) -> None:
        ...

    def do_get_attributes(self, node_id: int, table: str) -> None:
        ...

    def do_get_last_id(self, module: str) -> None:
        ...

    def do_select(self, node_id: Any, table: str) -> Any:
        ...

    def do_select_matrix(self, matrix_type: str) -> None:
        ...

    def do_set_attributes(self, node_id: List, package: Dict[str,
                                                             Any]) -> None:
        ...

    def do_set_tree(self, module_tree: treelib.Tree) -> None:
        ...

    def do_update_all(self) -> None:
        ...

    def do_update_matrix(self, revision_id: int, matrix_type: str,
                         matrix: pd.DataFrame) -> None:
        ...


class RAMSTKMatrixManager:
    _tag: str = ...
    _col_tree: Any = ...
    _column_tables: Any = ...
    _dic_columns: Any = ...
    _dic_matrix: Any = ...
    _row_table: Any = ...
    _row_tree: Any = ...
    dic_matrices: Any = ...
    n_row: int = ...
    n_col: int = ...

    def __init__(self, column_tables: Dict[str, List[Any]],
                 row_table: object) -> None:
        ...

    def do_create_columns(self, matrix_type: str) -> None:
        ...

    def do_create_rows(self, tree: treelib.Tree) -> None:
        ...

    def do_delete_column(self, node_id: int, matrix_type: str) -> Any:
        ...

    def do_delete_row(self, node_id: int) -> Any:
        ...

    def do_insert_column(self, node_id: str, matrix_type: str) -> Any:
        ...

    def do_insert_row(self, node_id: int) -> Any:
        ...

    def do_load(self, matrix_type: str, matrix: List[Tuple[int]]) -> None:
        ...

    def do_request_update(self, revision_id: int, matrix_type: str) -> None:
        ...

    def do_select(self, matrix_type: str, row: int, col: str) -> Any:
        ...
