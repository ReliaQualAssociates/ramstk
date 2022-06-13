# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
import pandas as pd
from treelib import Tree as Tree

class Export:
    _dic_output_data: Dict[
        str, Dict[int, Dict[str, Union[bool, float, int, str]]]
    ] = ...
    _df_output_data: pd.DataFrame = ...
    def __init__(self) -> None: ...
    def _do_export(self, modules: Dict[str, bool], file_name: str) -> None: ...
    def _do_export_to_delimited_text(self, file_name: str, separator: str) -> None: ...
    def _do_export_to_excel_legacy(self, module: str, file_name: str) -> None: ...
    def _do_export_to_excel(self, modules: Dict[str, bool], file_name: str) -> None: ...
    def _do_load_data(self, tree: Tree) -> None: ...
    def _do_request_data_trees(
        self, modules: Dict[str, bool], file_name: str
    ) -> None: ...
