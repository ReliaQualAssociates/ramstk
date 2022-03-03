# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_cause_table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKCause Table Model."""

# Standard Library Imports
from datetime import date
from typing import Dict, Type, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import criticality

# RAMSTK Local Imports
from ..dbrecords import RAMSTKCauseRecord
from .basetable import RAMSTKBaseTable


class RAMSTKCauseTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Cause table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_cause_id"
    _db_tablename = "ramstk_cause"
    _select_msg = "selected_revision"
    _tag = "cause"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKCause table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
            "mode_id",
            "mechanism_id",
            "cause_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKCauseRecord] = RAMSTKCauseRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "cause_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_calculate_rpn, "request_calculate_cause_rpn")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKCauseRecord:
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
        _new_record.cause_id = self.last_id + 1
        _new_record.parent_id = attributes["mechanism_id"]

        return _new_record

    def do_calculate_rpn(self, severity: int) -> None:
        """Calculate the risk priority number (RPN) of a hardware item's modes.

            .. note:: the severity (S) value will always be associated with a
                failure mode.

            .. note:: the occurrence (O) and detection (D) values may be
                associated with a failure mechanism or a failure cause.  Typically,
                hardware FMEA use mechanisms and functional FMEA use causes.

        :param severity: the RPN severity value.
        :return: None
        :rtype: None
        """
        _sod = {
            "rpn_severity": severity,
            "rpn_occurrence": 10,
            "rpn_detection": 10,
        }

        for _node in self.tree.all_nodes()[1:]:
            _sod["rpn_occurrence"] = _node.data[self._tag].rpn_occurrence
            _sod["rpn_detection"] = _node.data[self._tag].rpn_detection
            _node.data[self._tag].rpn = criticality.calculate_rpn(_sod)

            _sod["rpn_occurrence"] = _node.data[self._tag].rpn_occurrence_new
            _sod["rpn_detection"] = _node.data[self._tag].rpn_detection_new
            _node.data[self._tag].rpn_new = criticality.calculate_rpn(_sod)

        pub.sendMessage(
            "succeed_calculate_cause_rpn",
            tree=self.tree,
        )
