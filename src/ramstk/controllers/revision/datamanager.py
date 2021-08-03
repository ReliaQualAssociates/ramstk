# -*- coding: utf-8 -*-
#
#       ramstk.controllers.revision.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKRevision


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Revision data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_revision_id"
    _db_tablename = "ramstk_revision"
    _tag = "revision"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Revision data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {"revision": ["revision_id"]}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKRevision] = RAMSTKRevision

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_revision_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_revision_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_revision")
        pub.subscribe(super().do_update, "request_update_revision")

        pub.subscribe(self.do_select_all, "request_retrieve_revisions")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self._db_id_colname.replace("fld_", ""))

        _new_record.set_attributes(attributes)

        return _new_record

    def do_select_all(self) -> None:
        """Retrieve all the Revision data from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _revision in self.dao.do_select_all(
            RAMSTKRevision, key=None, value=None, order=RAMSTKRevision.revision_id
        ):

            self.tree.create_node(
                tag=_revision.name,
                identifier=_revision.revision_id,
                parent=self._parent_id,
                data={self._tag: _revision},
            )

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            "succeed_retrieve_revisions",
            tree=self.tree,
        )
