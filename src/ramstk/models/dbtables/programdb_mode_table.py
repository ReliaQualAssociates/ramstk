# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_mode_table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMode Table Model."""

# Standard Library Imports
from collections import defaultdict
from datetime import date
from typing import Dict, Type, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses.criticality import (
    calculate_mode_criticality,
    calculate_mode_hazard_rate,
)

# RAMSTK Local Imports
from ..dbrecords import RAMSTKModeRecord
from .basetable import RAMSTKBaseTable


class RAMSTKModeTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Mode table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_mode_id"
    _db_tablename = "ramstk_mode"
    _select_msg = "selected_revision"
    _tag = "mode"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKMode table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
            "mode_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKModeRecord] = RAMSTKModeRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "mode_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_calculate_criticality, "request_calculate_criticality")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKModeRecord:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.hardware_id = attributes["hardware_id"]
        _new_record.mode_id = self.last_id + 1

        return _new_record

    def do_calculate_criticality(self, item_hr: float) -> None:
        """Calculate MIL-STD-1629A, Task 102 criticality of a hardware item.

        :param item_hr: the hazard rate of the hardware item the criticality is
            being calculated for.
        :return: None
        :rtype: None
        """
        _item_criticality: Dict[str, float] = defaultdict(float)
        for _mode in self.tree.children(0):
            _mode.data["mode"].mode_hazard_rate = calculate_mode_hazard_rate(
                item_hr, _mode.data["mode"].mode_ratio
            )
            _mode.data["mode"].mode_criticality = calculate_mode_criticality(
                _mode.data["mode"].mode_hazard_rate,
                _mode.data["mode"].mode_op_time,
                _mode.data["mode"].effect_probability,
            )
            _item_criticality[_mode.data["mode"].severity_class] += _mode.data[
                "mode"
            ].mode_criticality

        pub.sendMessage(
            "succeed_calculate_mode_criticality",
            item_criticality=_item_criticality,
        )
