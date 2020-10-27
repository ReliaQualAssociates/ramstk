# -*- coding: utf-8 -*-
#
#       ramstk.controllers.failure_definition.datamanager.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKFailureDefinition


class DataManager(RAMSTKDataManager):
    """Contains attributes and methods of the Failure Definition data manager.

    This class manages the failure definition data from the
    RAMSTKFailureDefinition data models.
    """

    _tag = 'failure_definition'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Failure Definition data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_insert_failure_definition,
                      'request_insert_failure_definition')
        pub.subscribe(self.do_update, 'request_update_failure_definition')
        pub.subscribe(self.do_update_all,
                      'request_update_all_failure_definitions')
        pub.subscribe(self.do_get_tree, 'request_get_failure_definition_tree')
        pub.subscribe(self.do_set_attributes,
                      'request_set_failure_definition_attributes')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_failure_definition_attributes')
        pub.subscribe(self.do_set_attributes, 'lvw_editing_failure_definition')

        pub.subscribe(self._do_delete_failure_definition,
                      'request_delete_failure_definition')
        pub.subscribe(self._do_get_attributes,
                      'request_get_failure_definition_attributes')

    def do_get_tree(self) -> None:
        """Retrieve the failure definition treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_failure_definition_tree',
                        dmtree=self.tree)

    def do_insert_failure_definition(self) -> None:
        """Add a new failure definition for the selected revision.

        :return: None
        :rtype: None
        """
        try:
            _failure_definition = RAMSTKFailureDefinition()
            _failure_definition.revision_id = self._revision_id
            _failure_definition.definition_id = self.last_id + 1

            self.dao.do_insert(_failure_definition)

            self.last_id = _failure_definition.definition_id

            self.tree.create_node(
                tag=_failure_definition.definition,
                identifier=self.last_id,
                parent=self._root,
                data={'failure_definition': _failure_definition})

            pub.sendMessage("succeed_insert_failure_definition",
                            node_id=self.last_id,
                            tree=self.tree)
        except DataAccessError as _error:
            pub.sendMessage("fail_insert_failure_definition",
                            error_message=("Attempting to add failure "
                                           "definition to non-existent "
                                           "revision {0:d}.").format(
                                               self._revision_id))

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all Failure Definitions from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _failure_definition in self.dao.do_select_all(
                RAMSTKFailureDefinition,
                key=RAMSTKFailureDefinition.revision_id,
                value=self._revision_id,
                order=RAMSTKFailureDefinition.definition_id):

            self.tree.create_node(
                tag=_failure_definition.definition,
                identifier=_failure_definition.definition_id,
                parent=self._root,
                data={'failure_definition': _failure_definition})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_failure_definitions', tree=self.tree)

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the revision.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(node_id=[attributes['definition_id'], -1],
                                   package={_key: attributes[_key]})

    def do_set_attributes(self, node_id: List, package: Dict[str,
                                                             Any]) -> None:
        """Set the attributes of the record associated with definition ID.

        This is a helper method to set the desired failure definition attribute
        since the failure definitions are carried in a dict and we need to
        select the correct record to update.

        :param node_id: the ID of the revision and the failure definition in
            the RAMSTK Program database table whose attributes are to be set.
        :param package: the key:value pair of the attribute to set.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        for _table in ['failure_definition']:
            _attributes = self.do_select(node_id[0],
                                         table=_table).get_attributes()
            if _key in _attributes:
                _attributes[_key] = _value

                _attributes.pop('revision_id')
                _attributes.pop('definition_id')

                self.do_select(node_id[0],
                               table=_table).set_attributes(_attributes)

    def do_update(self, node_id: int) -> None:
        """Update the failure definition associated with node ID in database.

        :param node_id: the node (failure definition) ID of the failure
            definition to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(
                self.tree.get_node(node_id).data['failure_definition'])

            pub.sendMessage('succeed_update_failure_definition',
                            node_id=node_id)
        except (AttributeError, KeyError, TypeError):
            if node_id != 0:
                pub.sendMessage('fail_update_failure_definition',
                                error_message=('No data package found for '
                                               'failure definition ID '
                                               '{0:s}.').format(str(node_id)))

    def _do_delete_failure_definition(self, node_id: int) -> None:
        """Remove a failure definition.

        :param node_id: the failure definition ID to remove.
        :return: None
        """
        try:
            super().do_delete(node_id, 'failure_definition')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_failure_definition',
                            node_id=node_id,
                            tree=self.tree)
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _error_msg = ("Attempted to delete non-existent failure "
                          "definition ID {0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_failure_definition',
                            error_message=_error_msg)

    def _do_get_attributes(self, node_id: int, table: str) -> None:
        """Retrieve RAMSTK data table attributes for the failure definition.

        :param node_id: the node (failure definition) ID of the failure
            definition to get the attributes for.
        :param table: the RAMSTK data table to retrieve the attributes from.
        :return: None
        :rtype: None
        """
        _attributes = self.do_select(node_id, table=table).get_attributes()

        pub.sendMessage('succeed_get_failure_definition_attributes',
                        attributes=_attributes)
