# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.__mocks__.MockDAO.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mock class for mocking DAO objects and accessing mock database tables."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError


class MockDAO:
    """Class to mock the DAO for unit testing."""

    def __init__(self):
        """Initialize an instance of the Mock DAO."""
        self.table: List[object] = []
        self.last_id = 0

    def do_select_all(self, record, **kwargs: Dict[str, Any]) -> List[object]:
        """Mock the do_select_all() method."""
        _keys: List[str] = kwargs.get("key", None)
        _values: List[Any] = kwargs.get("value", None)
        _order: Any = kwargs.get("order", None)
        _all: bool = kwargs.get("_all", True)

        self.last_id = len(self.table)

        return self.table

    def do_select(self, node_id: int) -> object:
        """Mock the do_select() method.

        :param node_id:
        """
        return self.table[node_id]

    def do_insert(self, record: object) -> None:
        """Mock the do_insert() method.

        :param record: the record to add to the "database" table.
        """
        self.table.append(record)
        self.last_id += 1

    def do_delete(self, record: object) -> None:
        """Mock the do_delete() method.

        :param record: the record to remove from the "database" table.
        """
        try:
            self.table.pop(self.table.index(record))
            self.last_id = self.last_id - 1
        except ValueError:
            raise DataAccessError("Mock DAO do_delete() error.")

    def do_update(self, record=None) -> None:
        """Mock the do_update() method.

        :param record: the record to update in the "database" table.
        """
        pass

    def get_last_id(self, table: str, field: str):
        """Mock the get_last_id() method.

        :param table: the name of the table to get the last used ID for.
        :param field: the name of the field containing the last ID.
        """
        return self.last_id
