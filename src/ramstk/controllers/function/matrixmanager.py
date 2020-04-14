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
        # // TODO: Update Function module matrixmanager to respond to hardware.
        # //
        # // The Function module matrixmanager is currently only responding to
        # // Function module pubsub messages.  Ensure the Function module
        # // matrix manager is updated to respond to Hardware module pubsub
        # // messages when the Hardware module is refactored.
        pub.subscribe(self.do_create_rows, 'succeed_retrieve_functions')
        pub.subscribe(self._do_create_function_matrix_columns,
                      'succeed_retrieve_hardware')
        pub.subscribe(self._on_delete_function, 'succeed_delete_function')
        # pub.subscribe(self._on_delete_hardware, 'succeed_delete_hardware')
        pub.subscribe(self._on_insert_function, 'succeed_insert_function')
        # pub.subscribe(self._on_insert_hardware,
        #              'succeed_insert_hardware')
        pub.subscribe(self.do_update, 'request_update_function_matrix')

    def _do_create_function_matrix_columns(self, tree: treelib.Tree) -> None:
        """
        Create the Function data matrix columns.

        :param tree: the treelib Tree() containing the correlated workflow
            module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._col_tree = tree

        if tree.get_node(0).tag == 'hardware':
            super().do_create_columns('fnctn_hrdwr')
            pub.sendMessage('request_select_matrix', matrix_type='fnctn_hrdwr')

    # pylint: disable=unused-argument
    def _on_delete_function(self, node_id: int, tree: treelib.Tree) -> None:
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

    # pylint: disable=unused-argument
    def _on_insert_function(self, node_id: int, tree: treelib.Tree) -> None:
        """

        :param int node_id: the treelib Tree() node ID associated with the
            inserted function.
        :param tree: the treelib Tree() containing the remaining function data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_insert_row(node_id)
