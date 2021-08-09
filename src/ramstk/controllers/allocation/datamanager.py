# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.models.allocation.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Allocation Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Tuple, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses import allocation
from ramstk.models import RAMSTKBaseTable
from ramstk.models.programdb import RAMSTKAllocation


class DataManager(RAMSTKBaseTable):
    """Contain the attributes and methods of the Allocation data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_allocation"
    _select_msg = "selected_revision"
    _tag = "allocation"

    _system_hazard_rate: float = 0.0

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Allocation data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
        ]

        # Initialize private scalar attributes.
        self._node_hazard_rate: float = 0.0
        self._record: Type[RAMSTKAllocation] = RAMSTKAllocation

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_calculate_allocation, "request_calculate_allocation")
        pub.subscribe(
            self.do_calculate_allocation_goals, "request_calculate_allocation_goals"
        )

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes["parent_id"]

        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.parent_id = attributes["parent_id"]
        _new_record.hardware_id = attributes["hardware_id"]

        return _new_record

    def do_calculate_allocation(self, node_id: int) -> None:
        """Allocate a parent reliability goal to it's children.

        :param node_id: the record ID whose goals are to be calculated.
        :return: None
        :rtype: None
        """
        _dic_method = {
            1: self._do_calculate_equal_allocation,
            2: self._do_calculate_agree_allocation,
            3: self._do_calculate_arinc_allocation,
            4: self._do_calculate_foo_allocation,
        }

        self.do_calculate_allocation_goals(node_id)

        _record = self.tree.get_node(node_id).data[self._tag]
        try:
            _method = _dic_method[_record.allocation_method_id]
            _method(node_id)

            pub.sendMessage(
                "succeed_calculate_allocation",
                tree=self.tree,
            )
        except KeyError:
            _error_msg: str = (
                "Failed to allocate reliability for hardware ID {0}.  "
                "Unknown allocation method ID {1} selected.".format(
                    node_id, _record.allocation_method_id
                )
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_calculate_allocation",
                error_message=_error_msg,
            )

    def do_calculate_allocation_goals(self, node_id: int) -> None:
        """Calculate the allocation goals.

        :param node_id: the record ID whose goals are to be calculated.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]
        _attributes = _record.get_attributes()

        _attributes = allocation.do_calculate_goals(**_attributes)

        self.do_set_attributes(
            node_id=[node_id],
            package={"hazard_rate_goal": _attributes["hazard_rate_goal"]},
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={"mtbf_goal": _attributes["mtbf_goal"]},
        )
        self.do_set_attributes(
            node_id=[node_id],
            package={"reliability_goal": _attributes["reliability_goal"]},
        )

    def _do_calculate_agree_allocation(self, node_id: int) -> None:
        """Allocate reliability using the AGREE method.

        :param node_id: the record ID whose allocation is to be calculated.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]
        _parent_goal = _record.reliability_goal
        _method_id = _record.allocation_method_id

        for _node in self.tree.children(node_id):
            _attributes: Dict[str, Any] = _node.data["allocation"].get_attributes()
            _attributes["allocation_method_id"] = _method_id

            (
                _attributes["n_sub_elements"],
                _attributes["n_sub_systems"],
            ) = self._do_calculate_agree_total_elements(node_id)

            _attributes = allocation.do_allocate_reliability(
                _parent_goal, 0, **_attributes
            )

            _node.data["allocation"].hazard_rate_alloc = _attributes[
                "hazard_rate_alloc"
            ]
            _node.data["allocation"].mtbf_alloc = _attributes["mtbf_alloc"]
            _node.data["allocation"].reliability_alloc = _attributes[
                "reliability_alloc"
            ]

            _parent_goal = _node.data["allocation"].reliability_goal

    def _do_calculate_agree_total_elements(self, node_id: int) -> Tuple[int, int]:
        """Calculate the total number of elements for the AGREE method.

        :param node_id: the record ID whose allocation is to be calculated.
        :return: _n_sub_elements, _n_sub_systems; the number of
            sub-elements and subsystems comprising the selected node.
        :rtype: tuple
        """
        _n_sub_elements = 0
        _n_sub_systems = 0

        for _node in self.tree.children(node_id):
            _n_sub_elements += _node.data["allocation"].n_sub_elements
            _n_sub_systems += _node.data["allocation"].n_sub_systems

        return _n_sub_elements, _n_sub_systems

    def _do_calculate_arinc_allocation(self, node_id: int) -> None:
        """Allocate reliability using the ARINC method.

        :param node_id: the record ID whose allocation is to be calculated.
        :return: None
        :rtype: None
        :raises: ZeroDivisionError if the system hazard rate is zero.
        """
        _record = self.tree.get_node(node_id).data[self._tag]

        _parent_goal = _record.hazard_rate_goal
        _method_id = _record.allocation_method_id

        for _node in self.tree.children(node_id):
            _attributes = _node.data["allocation"].get_attributes()
            _attributes["allocation_method_id"] = _method_id

            _attributes["weight_factor"] = (
                self._node_hazard_rate / self._system_hazard_rate
            )
            _attributes = allocation.do_allocate_reliability(
                _parent_goal, 0, **_attributes
            )

            _node.data["allocation"].mtbf_alloc = _attributes["mtbf_alloc"]
            _node.data["allocation"].hazard_rate_alloc = _attributes[
                "hazard_rate_alloc"
            ]
            _node.data["allocation"].reliability_alloc = _attributes[
                "reliability_alloc"
            ]

            _parent_goal = _node.data["allocation"].hazard_rate_goal

    def _do_calculate_equal_allocation(self, node_id: int) -> None:
        """Allocate reliability using equal apportionment.

        :param node_id: the record ID whose allocation is to be calculated.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]
        _attributes = _record.get_attributes()

        _parent_goal = _attributes["reliability_goal"]
        _method_id = _attributes["allocation_method_id"]

        for _node in self.tree.children(node_id):
            _attributes = _node.data["allocation"].get_attributes()
            _attributes["allocation_method_id"] = _method_id

            _attributes["weight_factor"] = 1.0 / _node.data["allocation"].n_sub_systems
            _attributes = allocation.do_allocate_reliability(
                _parent_goal, 0, **_attributes
            )

            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"allocation_method_id": _attributes["allocation_method_id"]},
            )
            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"weight_factor": _attributes["weight_factor"]},
            )
            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"mtbf_alloc": _attributes["mtbf_alloc"]},
            )
            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"hazard_rate_alloc": _attributes["hazard_rate_alloc"]},
            )
            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"reliability_alloc": _attributes["reliability_alloc"]},
            )

            _parent_goal = _node.data["allocation"].reliability_goal

    def _do_calculate_foo_allocation(self, node_id: int) -> None:
        """Allocate reliability using the FOO method.

        :param node_id: the record ID whose allocation is to be calculated.
        :return: None
        :rtype: None
        """
        _record = self.tree.get_node(node_id).data[self._tag]

        _parent_goal = _record.hazard_rate_goal
        _method_id = _record.allocation_method_id
        _cum_weight = self._do_calculate_foo_cumulative_weight(node_id)

        for _node in self.tree.children(node_id):
            _attributes = _node.data["allocation"].get_attributes()
            _attributes["allocation_method_id"] = _method_id

            _attributes = allocation.do_allocate_reliability(
                _parent_goal, _cum_weight, **_attributes
            )

            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"weight_factor": _attributes["weight_factor"]},
            )
            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"percent_weight_factor": _attributes["percent_weight_factor"]},
            )
            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"mtbf_alloc": _attributes["mtbf_alloc"]},
            )
            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"hazard_rate_alloc": _attributes["hazard_rate_alloc"]},
            )
            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"reliability_alloc": _attributes["reliability_alloc"]},
            )

    def _do_calculate_foo_cumulative_weight(self, node_id: int) -> int:
        """Calculate the cumulative weight for the FOO method.

        :param node_id: the node (allocation) ID of the allocation item whose
            goal is to be allocated.
        :return: _cum_weight; the cumulative weighting factor for the
            allocation item to be allocated.
        """
        _cum_weight = 0

        for _node in self.tree.children(node_id):
            _attributes = _node.data["allocation"].get_attributes()
            _attributes["weight_factor"] = (
                _attributes["int_factor"]
                * _attributes["soa_factor"]
                * _attributes["op_time_factor"]
                * _attributes["env_factor"]
            )
            _cum_weight += _attributes["weight_factor"]

            self.do_set_attributes(
                node_id=[_node.identifier],
                package={"weight_factor": _attributes["weight_factor"]},
            )

        return _cum_weight
