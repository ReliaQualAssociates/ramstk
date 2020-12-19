# -*- coding: utf-8 -*-
#
#       ramstk.controllers.requirement.MatrixManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007-2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Requirement Controller Package matrix manager."""

# Standard Library Imports
from typing import Any

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKMatrixManager
from ramstk.models.programdb import RAMSTKHardware, RAMSTKRequirement


class MatrixManager(RAMSTKMatrixManager):
    """Contain the attributes and methods of the Requirement matrix manager.

    This class manages the requirement matrices for Hardware and
    Validation. Attributes of the requirement Matrix Manager are:
    """
    def __init__(self) -> None:
        """Initialize an instance of the requirement matrix manager."""
        super().__init__(column_tables={
            'rqrmnt_hrdwr': [RAMSTKHardware, 'hardware_id', 'comp_ref_des']
        },
                         row_table=RAMSTKRequirement)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        # // TODO: Update Requirement matrixmanager to respond to hardware.
        # //
        # // The Requirement module matrixmanager is currently only responding
        # // to Requirement module pubsub messages.  Ensure the Requirement
        # // module matrix manager is updated to respond to Hardware module
        # // pubsub messages when the Hardware module is refactored.
        pub.subscribe(self.do_create_rows, 'succeed_retrieve_requirements')
        pub.subscribe(self._do_create_requirement_matrix_columns,
                      'succeed_retrieve_hardware')
        pub.subscribe(self._on_delete_requirement,
                      'succeed_delete_requirement')
        pub.subscribe(self._on_delete_hardware, 'succeed_delete_hardware')
        pub.subscribe(self._on_insert_requirement,
                      'succeed_insert_requirement')
        pub.subscribe(self._on_insert_hardware, 'succeed_insert_hardware')

    def _do_create_requirement_matrix_columns(self,
                                              tree: treelib.Tree) -> None:
        """Create the Requirement data matrix columns.

        :param tree: the treelib Tree() containing the correlated workflow
            module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        # If the row tree has already been loaded, we can build the matrix.
        # Otherwise the matrix will be built when the row tree is loaded.
        if tree.get_node(0).tag == 'hardware':
            self._col_tree['rqrmnt_hrdwr'] = tree
            if self._row_tree.all_nodes():
                super().do_create_columns('rqrmnt_hrdwr')
                pub.sendMessage('request_select_matrix',
                                matrix_type='rqrmnt_hrdwr')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_requirement(self, node_id: int, tree: treelib.Tree) -> None:
        """Delete the matrix row associated with the deleted requirement.

        :param node_id: the treelib Tree() node ID associated with the
            deleted requirement.
        :param tree: the treelib Tree() containing the remaining requirement
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_delete_row(node_id)

    def _on_delete_hardware(self, node_id: int, tree: treelib.Tree) -> Any:
        """Delete the node ID column from the Validation::Hardware matrix.

        :param node_id: the hardware treelib Node ID that was deleted.
            Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['rqrmnt_hrdwr'].get_node(node_id).tag
        return super().do_delete_column(_tag, 'rqrmnt_hrdwr')

    def _on_insert_hardware(self, node_id: int, tree: treelib.Tree) -> Any:
        """Insert the node ID column to the Validation::Hardware matrix.

        :param node_id: the hardware treelib Node ID that is to be
            inserted.  Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['rqrmnt_hrdwr'].get_node(node_id).tag
        return super().do_insert_column(_tag, 'rqrmnt_hrdwr')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert_requirement(self, node_id: int, tree: treelib.Tree) -> None:
        """Insert row into matrix when new requirement is added.

        :param node_id: the treelib Tree() node ID associated with the
            inserted requirement.
        :param tree: the treelib Tree() containing the remaining requirement
            data.
        :return: None
        :rtype: None
        """
        self.do_insert_row(node_id)
