# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_environment_table.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKEnvironment Table Model."""

# Standard Library Imports
from datetime import date
from typing import Dict, Type, Union

# RAMSTK Local Imports
from ..dbrecords import RAMSTKEnvironmentRecord
from .basetable import RAMSTKBaseTable


class RAMSTKEnvironmentTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Environment table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_environment_id"
    _db_tablename = "ramstk_environment"
    _select_msg = "selected_revision"
    _tag = "environment"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize an RAMSTKEnvironment table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "mission_id",
            "mission_phase_id",
            "environment_id",
            "parent_id",
            "record_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKEnvironmentRecord] = RAMSTKEnvironmentRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "environment_id"

        # Subscribe to PyPubSub messages.

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKEnvironmentRecord:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.mission_id = attributes["mission_id"]
        _new_record.mission_phase_id = attributes["mission_phase_id"]
        _new_record.environment_id = self.last_id + 1

        return _new_record
