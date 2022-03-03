# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_revision_table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKRevision Table Model."""

# Standard Library Imports
from datetime import date
from typing import Dict, Type, Union

# RAMSTK Local Imports
from ..dbrecords import RAMSTKRevisionRecord
from .basetable import RAMSTKBaseTable


class RAMSTKRevisionTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Revision table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_revision_id"
    _db_tablename = "ramstk_revision"
    _select_msg = "request_retrieve_revisions"
    _tag = "revision"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKRevision table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKRevisionRecord] = RAMSTKRevisionRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "revision_id"

        # Subscribe to PyPubSub messages.

    # pylint: disable=unused-argument, disable=method-hidden
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKRevisionRecord:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = self.last_id + 1
        _new_record.name = "New Revision"

        return _new_record
