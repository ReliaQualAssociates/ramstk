# Standard Library Imports
import gettext
from typing import Any, List

_ = gettext.gettext


def date_to_ordinal(date: str) -> int:
    ...


def dir_exists(directory: str) -> bool:
    ...


def file_exists(_file: str) -> bool:
    ...


def none_to_default(field: Any, default: Any) -> Any:
    ...


def none_to_string(string: None) -> str:
    ...


def ordinal_to_date(ordinal: int) -> str:
    ...


def split_string(string: str) -> List[str]:
    ...


def boolean_to_integer(boolean: bool) -> int:
    ...


def integer_to_boolean(integer: int) -> bool:
    ...


def string_to_boolean(string: str) -> bool:
    ...


def get_install_prefix() -> str:
    ...
