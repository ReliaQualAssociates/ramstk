# -*- coding: utf-8 -*-
#
#       ramstk.models.failure_definition.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Definition Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable
from ramstk.models.programdb import RAMSTKFailureDefinition


class DataManager(RAMSTKBaseTable):
    """Contains attributes and methods of the Failure Definition data manager.

    This class manages the failure definition data from the
    RAMSTKFailureDefinition data models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_definition_id"
    _db_tablename = "ramstk_failure_definition"
    _select_msg = "selected_revision"
    _tag = "failure_definition"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Failure Definition data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "definition_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKFailureDefinition] = RAMSTKFailureDefinition

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "definition_id"

        # Subscribe to PyPubSub messages.

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.definition_id = self.last_id + 1

        return _new_record
