# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.models.hardware.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Package Table Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable
from ramstk.models.programdb import RAMSTKHardware


class RAMSTKHardwareTable(RAMSTKBaseTable):
    """Contain attributes and methods of the Hardware table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_hardware"
    _select_msg = "selected_revision"
    _tag = "hardware"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Hardware table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
        ]

        # Initialize private scalar attributes.
        # This is the record class associated with the table being modelled.
        self._record: Type[RAMSTKHardware] = RAMSTKHardware

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

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
        _new_record.hardware_id = attributes["hardware_id"]

        return _new_record

    def do_calculate_cost(self, node_id: int) -> float:
        """Calculate the cost related metrics.

        :param node_id: the record ID to calculate.
        :return: _total_cost; the total cost.
        :rtype: float
        """
        _node = self.tree.get_node(node_id)
        _record = _node.data[self._tag]
        _total_cost: float = 0.0

        if _record.cost_type_id == 2:
            if _record.part == 1:
                _total_cost = _record.cost * _record.quantity
            else:
                for _node_id in _node.successors(self.tree.identifier):
                    _total_cost += self.do_calculate_cost(_node_id)
                _total_cost = _total_cost * _record.quantity
        else:
            _total_cost = _record.total_cost

        _record.total_cost = _total_cost

        pub.sendMessage(
            "request_set_hardware_attributes",
            node_id=node_id,
            package={"total_cost": _total_cost},
        )

        return _total_cost

    def do_calculate_part_count(self, node_id: int) -> int:
        """Calculate the total part count of a hardware item.

        :param node_id: the record ID to calculate.
        :return: _part_count
        :rtype: int
        """
        _node = self.tree.get_node(node_id)
        _record = _node.data[self._tag]
        _part_count: int = 0

        if _record.part == 1:
            _part_count = _record.quantity
        else:
            for _node_id in _node.successors(self.tree.identifier):
                _part_count += self.do_calculate_part_count(_node_id)
            _part_count = _part_count * _record.quantity

        pub.sendMessage(
            "request_set_hardware_attributes",
            node_id=node_id,
            package={"total_part_count": _part_count},
        )

        return _part_count
