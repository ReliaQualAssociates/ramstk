# -*- coding: utf-8 -*-
#
#       ramstk.models.stakeholder.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Table Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import improvementfactor
from ramstk.models import RAMSTKBaseTable, RAMSTKStakeholderRecord


class RAMSTKStakeholderTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Stakeholder data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_stakeholder_id"
    _db_tablename = "ramstk_stakeholder"
    _select_msg = "selected_revision"
    _tag = "stakeholder"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Stakeholder data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "stakeholder_id",
            "parent_id",
            "record_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKStakeholderRecord] = RAMSTKStakeholderRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "stakeholder_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self.do_calculate_stakeholder, "request_calculate_stakeholder"
        )

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
        _new_record.stakeholder_id = self.last_id + 1
        _new_record.description = "New Stakeholder Input"

        return _new_record

    def do_calculate_stakeholder(self, node_id: int) -> None:
        """Calculate improvement factor and weight for currently selected item.

        :param node_id: the ID of the record to calculate.
        :return: None
        :rtype: None
        """
        self._do_calculate_improvement(node_id)

        pub.sendMessage(
            "succeed_calculate_stakeholder",
            tree=self.tree,
        )

    def _do_calculate_improvement(self, node_id: int) -> None:
        """Calculate improvement factor and weight for currently selected item.

        :param node_id: the ID of the record to calculate.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]
        _attributes = _record.get_attributes()

        (
            _improvement,
            _overall_weight,
        ) = improvementfactor.calculate_improvement(
            _attributes["planned_rank"],
            _attributes["customer_rank"],
            _attributes["priority"],
            user_float_1=_attributes["user_float_1"],
            user_float_2=_attributes["user_float_2"],
            user_float_3=_attributes["user_float_3"],
            user_float_4=_attributes["user_float_4"],
            user_float_5=_attributes["user_float_5"],
        )

        self.do_set_attributes(
            node_id=node_id,
            package={"improvement": _improvement},
        )
        self.do_set_attributes(
            node_id=node_id,
            package={"overall_weight": _overall_weight},
        )
