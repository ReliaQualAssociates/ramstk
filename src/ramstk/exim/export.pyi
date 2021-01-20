# Standard Library Imports
from typing import Any

# Third Party Imports
from treelib import Tree as Tree

class Export:
    _dic_output_data: Any = ...
    _df_output_data: Any = ...

    def __init__(self) -> None:
        ...

    def _do_export(self, file_type: str, file_name: str) -> None:
        ...

    def _do_export_to_delimited_text(self, file_name: str,
                                     separator: str) -> Any:
        ...

    def _do_export_to_excel(self, file_name: str) -> None:
        ...

    def _do_load_data(self, tree: Tree) -> None:
        ...
