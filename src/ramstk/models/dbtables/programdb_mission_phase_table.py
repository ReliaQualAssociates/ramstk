# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_mission_phase_table.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMissionPhase Table Model."""

# Standard Library Imports
from datetime import date
from typing import Dict, Type, Union

# RAMSTK Local Imports
from ..dbrecords import RAMSTKMissionPhaseRecord
from .basetable import RAMSTKBaseTable


class RAMSTKMissionPhaseTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Mission Phase table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_mission_phase_id"
    _db_tablename = "ramstk_mission_phase"
    _select_msg = "selected_revision"
    _tag = "mission_phase"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKMissionPhase table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "mission_id",
            "mission_phase_id",
            "parent_id",
            "record_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKMissionPhaseRecord] = RAMSTKMissionPhaseRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "mission_phase_id"

        # Subscribe to PyPubSub messages.

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKMissionPhaseRecord:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.mission_id = attributes["mission_id"]
        _new_record.mission_phase_id = self.last_id + 1

        return _new_record
