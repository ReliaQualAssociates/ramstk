# -*- coding: utf-8 -*-
#
#       ramstk.controllers.RAMSTKDataManager.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Controllers Package RAMSTKDataManager."""

# Third Party Imports
from treelib import Tree, tree


class RAMSTKDataManager():
    """
    This is the meta-class for all RAMSTK Data Managers.

    :ivar tree: the treelib Tree()that will contain the structure of the RAMSTK
        module being modeled.
    :type tree: :class:`treelib.Tree`
    :ivar dao: the data access object used to communicate with the RAMSTK
        Program database.
    :type dao: :class:`ramstk.dao.DAO`
    """

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an RAMSTK data model instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = dao
        self.tree = Tree()
        self.last_id = None

        # Add the root to the Tree().  This is neccessary to allow multiple
        # entries at the top level as there can only be one root in a treelib
        # Tree().  Manipulation and viewing of a RAMSTK module tree needs to
        # ignore the root of the tree.
        try:
            self.tree.create_node(
                tag=self._tag,
                identifier=self._root,
                parent=None,
            )
        except (
                tree.MultipleRootError,
                tree.NodeIDAbsentError,
                tree.DuplicatedNodeIdError,
        ):
            pass

    def do_delete(self, node_id, table):
        """
        Remove a RAMSTK data table record.

        :param int node_id: the node ID to be removed from the RAMSTK Program
            database.
        :param str table: the key in the module's treelib Tree() data package
            for the RAMSTK data table to remove the record from.
        :return: (_error_code, _error_msg); the error code and associated
            message from the DAO.
        :rtype: (int, str)
        """
        return self.dao.db_delete(self.do_select(node_id, table))

    def do_select(self, node_id, table):
        """
        Retrieve the RAMSTK data table record for the Node ID passed.

        :param int node_id: the Node ID of the data package to retrieve.
        :param str table: the name of the RAMSTK data table to retrieve the
            attributes from.
        :return: the instance of the RAMSTK<MODULE> data table that was
            requested or None if the requested Node ID does not exist.
        :raise: KeyError if passed the name of a table that isn't managed by
            this manager.
        """
        try:
            _entity = self.tree.get_node(node_id).data[table]
        except AttributeError:
            _entity = None
        except tree.NodeIDAbsentError:
            _entity = None

        return _entity

    def do_set_tree(self, module_tree):
        """
        Set the MODULE treelib Tree().

        This method is generally used to respond to events such as successful
        calculations of the entire system.

        :param module_tree: the treelib Tree() to assign to the tree attribute.
        :type module_tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.tree = module_tree

    def do_update_all(self):
        """
        Update all MODULE data table records in the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            self.do_update(_node.identifier)
