# Standard Library Imports
import gettext
from typing import Callable, List, Union

_ = gettext.gettext

def date_to_ordinal(date: str) -> int: ...
def deprecated(func: Callable) -> Callable: ...
def dir_exists(directory: str) -> bool: ...
def file_exists(_file: str) -> bool: ...
def none_to_default(
    field: None, default: Union[bool, float, int, str]
) -> Union[bool, float, int, str]: ...
def none_to_string(string: Union[None, str]) -> str: ...
def ordinal_to_date(ordinal: int) -> str: ...
def split_string(string: str) -> List[str]: ...
def boolean_to_integer(boolean: bool) -> int: ...
def integer_to_boolean(integer: int) -> bool: ...
def string_to_boolean(string: Union[bool, str]) -> bool: ...
def get_install_prefix() -> str: ...
