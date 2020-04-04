# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.MatrixManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Controller Package matrix manager."""

# Third Party Imports
import treelib
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
        pub.subscribe(self._do_create, 'request_create_matrix')
        pub.subscribe(self._on_delete_function, 'succeed_delete_function')
        #pub.subscribe(self._do_delete_hardware, 'succeed_delete_hardware')
        pub.subscribe(self._on_insert_function, 'succeed_insert_function')
        #pub.subscribe(self._do_insert_hardware,
        #              'succeed_insert_hardware')
        pub.subscribe(self.do_update, 'request_update_function_matrix')
        pub.subscribe(self._on_get_tree, 'succeed_get_function_tree')
        pub.subscribe(self._on_get_tree, 'succeed_get_hardware_tree')
        #pub.subscribe(self._on_get_tree, 'succeed_get_validation_tree')

    def _do_create(self, tree: treelib.Tree) -> None:
        """
        Create the Function data matrices.

        :param tree: the treelib Tree() containing the work stream module's
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._row_tree = tree
        self.dic_matrices = {}

        # pub.sendMessage('request_get_hardware_tree')

        RAMSTKMatrixManager.do_create(self, 'fnctn_hrdwr')

    def _on_delete_function(self, node_id: int, tree: treelib.Tree) -> None: # pylint: disable=unused-argument
        """
        Delete the matrix row associated with the deleted function.

        :param int node_id: the treelib Tree() node ID associated with the
            deleted function.
        :param tree: the treelib Tree() containing the remaining function data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_delete_row(node_id)

    def _on_get_tree(self, dmtree: treelib.Tree) -> None:
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

    def _on_insert_function(self, node_id: int, tree: treelib.Tree) -> None:    # pylint: disable=unused-argument
        """

        :param int node_id: the treelib Tree() node ID associated with the
            inserted function.
        :param tree: the treelib Tree() containing the remaining function data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_insert_row(node_id)
