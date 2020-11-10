# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKFunction


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Function data manager.

    This class manages the function data from the RAMSTKFunction and
    RAMSTKHazardAnalysis data models.
    """

    _tag = 'function'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Function data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'function': ['revision_id', 'function_id']}

        # Initialize private list attributes.
        self._last_id = [0, 0]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_function_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_function_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_function')
        pub.subscribe(super().do_update_all, 'request_update_all_functions')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_update, 'request_update_function')
        pub.subscribe(self.do_get_tree, 'request_get_function_tree')

        pub.subscribe(self._do_delete, 'request_delete_function')
        pub.subscribe(self._do_insert_function, 'request_insert_function')

    def do_get_tree(self) -> None:
        """Retrieve the function treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_function_tree', dmtree=self.tree)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Function data from the RAMSTK Program database.

        :param dict attributes: the attributes for the selected Function.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _function in self.dao.do_select_all(
                RAMSTKFunction,
                key=RAMSTKFunction.revision_id,
                value=self._revision_id,
                order=RAMSTKFunction.function_id):

            self.tree.create_node(tag=_function.name,
                                  identifier=_function.function_id,
                                  parent=_function.parent_id,
                                  data={'function': _function})

        self._last_id[0] = max(self.tree.nodes.keys())
        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_functions', tree=self.tree)

    def do_update(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node (function) ID of the function to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['function'])
            pub.sendMessage('succeed_update_function', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_function',
                            error_message=('Attempted to save non-existent '
                                           'function with function ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_function',
                                error_message=('No data package found for '
                                               'function ID {0:s}.').format(
                                                   str(node_id)))

    def _do_delete(self, node_id: int) -> None:
        """Remove a function.

        :param int node_id: the node (function) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'function')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_function',
                            node_id=node_id,
                            tree=self.tree)
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _error_message = ("Attempted to delete non-existent function ID "
                              "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_function',
                            error_message=_error_message)

    def _do_insert_function(self, parent_id: int = 0) -> None:
        """Add a new function as child of the parent ID function.

        :param int parent_id: the parent (function) ID of the function to
            insert the child.  Default is to add a top-level function.
        :return: None
        :rtype: None
        """
        if self.tree.get_node(parent_id) is not None:
            _last_id = self.dao.get_last_id('ramstk_function', 'function_id')
            try:
                _function = RAMSTKFunction()
                _function.revision_id = self._revision_id
                _function.function_id = _last_id + 1
                _function.name = 'New Function'
                _function.parent_id = parent_id

                self.dao.do_insert(_function)

                self.tree.create_node(tag=_function.name,
                                      identifier=_function.function_id,
                                      parent=_function.parent_id,
                                      data={'function': _function})

                self._last_id[0] = _function.function_id
                self.last_id = _function.function_id

                pub.sendMessage('succeed_insert_function',
                                node_id=self.last_id,
                                tree=self.tree)
            except DataAccessError as _error:
                pub.sendMessage("fail_insert_function", error_message=_error)
        else:
            pub.sendMessage("fail_insert_function",
                            error_message=("Attempting to add a function as a "
                                           "child of non-existent parent node "
                                           "{0:s}.".format(str(parent_id))))
