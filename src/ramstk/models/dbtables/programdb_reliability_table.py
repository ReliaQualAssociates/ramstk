# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_reliability_table.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKReliability Table Model."""

# Standard Library Imports
from datetime import date
from typing import Dict, Type, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Local Imports
from ..dbrecords import RAMSTKReliabilityRecord
from .basetable import RAMSTKBaseTable


class RAMSTKReliabilityTable(RAMSTKBaseTable):
    """Contain attributes and methods of the Reliability table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_reliability"
    _select_msg = "selected_revision"
    _tag = "reliability"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKReliability table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
            "parent_id",
            "record_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKReliabilityRecord] = RAMSTKReliabilityRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._on_insert_hardware,
            "succeed_insert_hardware",
        )

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKReliabilityRecord:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.hardware_id = attributes["hardware_id"]

        return _new_record

    def _on_insert_hardware(self, tree: treelib.Tree) -> None:
        """Add new node to the Reliability tree for the newly added Hardware.

        Reliability records are added by triggers in the database when a new Hardware
        item is added.  This method simply adds a new node to the Reliability tree with
        a blank record.

        :param tree: the Hardware tree with the new node.
        :return: None
        :rtype: None
        """
        for _node in tree.all_nodes()[1:]:
            if not self.tree.contains(_node.identifier):
                _attributes = {
                    "revision_id": _node.data["hardware"].revision_id,
                    "hardware_id": _node.data["hardware"].hardware_id,
                }
                _record = self.do_get_new_record(_attributes)
                self.tree.create_node(
                    tag=self._tag,
                    identifier=_node.data["hardware"].hardware_id,
                    parent=0,
                    data={self._tag: _record},
                )

                pub.sendMessage(
                    f"succeed_insert_{self._tag}",
                    tree=self.tree,
                )
