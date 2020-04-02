# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.MatrixManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Controller Package matrix manager."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKMatrixManager
from ramstk.models.programdb import RAMSTKFunction, RAMSTKHardware


class MatrixManager(RAMSTKMatrixManager):
    """
    Contain the attributes and methods of the Function matrix manager.

    This class manages the function matrices for Hardware and Validation.
    Attributes of the function Matrix Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the function item being analyzed.
    """

    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        """Initialize an instance of the function matrix manager."""
        RAMSTKMatrixManager.__init__(
            self,
            column_tables={
                'fnctn_hrdwr':
                [RAMSTKHardware, 'hardware_id', 'comp_ref_des']
            },
            row_table=RAMSTKFunction)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_create, 'succeed_select_revision')
        #pub.subscribe(self._do_delete_hardware, 'succeed_delete_hardware')
        #pub.subscribe(self._do_insert_hardware,
        #              'succeed_insert_hardware')
        #pub.subscribe(self._do_insert_validation, 'succeed_insert_validation')
        pub.subscribe(self.do_update, 'request_update_function_matrix')
        pub.subscribe(self._on_delete_function, 'succeed_delete_function')
        pub.subscribe(self._on_get_tree, 'succeed_get_function_tree')
        pub.subscribe(self._on_get_tree, 'succeed_get_hardware_tree')
        #pub.subscribe(self._on_get_tree, 'succeed_get_validation_tree')
        pub.subscribe(self._on_insert_function, 'succeed_insert_function')

    def _do_create(self, revision_id: int) -> None: # pylint: disable=unused-argument
        """
        Create the Function data matrices.

        :param int revision_id: the revision ID to gather the data that will be
            used to create the matrices.
        :return:
        :rtype:
        """
        self.dic_matrices = {}

        pub.sendMessage('request_get_function_tree')
        # pub.sendMessage('request_get_hardware_tree')

        RAMSTKMatrixManager.do_create(self, 'fnctn_hrdwr')

    def _on_delete_function(self, tree) -> None:
        """
        Delete the node ID column from the Function::Hardware matrix.

        :param tree: the function treelib Tree() after deleting a function.
        :type tree: :class:`treelib.Tree`:
        :return: None
        :rtype: None
        """
        self._row_tree = tree
        self._do_create(0)

    def _on_insert_function(self, node_id: int, tree) -> None:  # pylint: disable=unused-argument
        """
        Insert the node ID column to the Function::Hardware matrix.

        :param int node_id: the function treelib Node ID that is to be
            inserted.  Note that node ID = function ID = matrix row ID.
        :param tree: the function treelib Tree() after inserting a function.
        :type tree: :class:`treelib.Tree`:
        :return: None
        :rtype: None
        """
        self._row_tree = tree
        self._do_create(0)

    def _on_get_tree(self, dmtree) -> None:
        """
        Request the function treelib Tree().

        :param dmtree: the function treelib Tree().
        :type dmtree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        if dmtree.get_node(0).tag == 'function':
            self._row_tree = dmtree
        else:
            self._col_tree = dmtree
