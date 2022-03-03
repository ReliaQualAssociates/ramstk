# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_test_method_table.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKTestMethod Table Model."""

# Standard Library Imports
from datetime import date
from typing import Dict, Type, Union

# RAMSTK Local Imports
from ..dbrecords import RAMSTKTestMethodRecord
from .basetable import RAMSTKBaseTable


class RAMSTKTestMethodTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Test Method table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_test_method_id"
    _db_tablename = "ramstk_test_method"
    _select_msg = "selected_revision"
    _tag = "test_method"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKTestMethod table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
            "mode_id",
            "mechanism_id",
            "opload_id",
            "test_method_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKTestMethodRecord] = RAMSTKTestMethodRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "test_method_id"

        # Subscribe to PyPubSub messages.

    # pylint: disable=method-hidden
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKTestMethodRecord:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.hardware_id = attributes["hardware_id"]
        _new_record.mode_id = attributes["mode_id"]
        _new_record.mechanism_id = attributes["mechanism_id"]
        _new_record.opload_id = attributes["opload_id"]
        _new_record.test_method_id = self.last_id + 1

        return _new_record
