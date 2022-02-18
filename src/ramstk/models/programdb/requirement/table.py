# -*- coding: utf-8 -*-
#
#       ramstk.models.requirement.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Requirement Table Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable, RAMSTKRequirementRecord


class RAMSTKRequirementTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Requirement data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_requirement_id"
    _db_tablename = "ramstk_requirement"
    _select_msg = "selected_revision"
    _tag = "requirement"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Requirement data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "requirement_id",
            "parent_id",
            "record_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKRequirementRecord] = RAMSTKRequirementRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "requirement_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().do_create_all_codes, "request_create_all_requirement_codes"
        )

        pub.subscribe(self.do_create_code, "request_create_requirement_code")

    def do_create_code(self, node_id: int, prefix: str) -> None:
        """Request to create the requirement code.

        :param node_id: the Requirement ID to create the code for.
        :param prefix: the code prefix to use for the requested code.
        :return: None
        :rtype: None
        """
        try:
            _requirement = self.tree.get_node(node_id).data["requirement"]
            _requirement.create_code(prefix=prefix)

            pub.sendMessage("succeed_create_code")
            pub.sendMessage(
                "succeed_create_requirement_code",
                requirement_code=_requirement.get_attributes()["requirement_code"],
            )
        except (TypeError, AttributeError):
            if node_id != 0:
                _method_name: str = (
                    inspect.currentframe().f_code.co_name  # type: ignore
                )
                pub.sendMessage(
                    "fail_create_requirement_code",
                    error_message=(
                        f"{_method_name}: No data package found for requirement "
                        f"ID {node_id}."
                    ),
                )

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes[  # pylint: disable=attribute-defined-outside-init
            "parent_id"
        ]

        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.requirement_id = self.last_id + 1
        _new_record.parent_id = attributes.get("parent_id", 0)

        return _new_record
