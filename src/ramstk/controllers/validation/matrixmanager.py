# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.matrixmanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007-2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Controller Package matrix manager."""

# Standard Library Imports
from typing import Any

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKMatrixManager
from ramstk.models.programdb import (
    RAMSTKHardware, RAMSTKRequirement, RAMSTKValidation
)


class MatrixManager(RAMSTKMatrixManager):
    """Contain the attributes and methods of the Validation matrix manager.

    This class manages the validation matrices for Requirements and Validation.
    Attributes of the validation Matrix Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the validation item being analyzed.
    """
    def __init__(self) -> None:
        """Initialize an instance of the validation matrix manager."""
        super().__init__(column_tables={
            'vldtn_rqrmnt':
            [RAMSTKRequirement, 'requirement_id', 'requirement_code'],
            'vldtn_hrdwr': [RAMSTKHardware, 'hardware_id', 'comp_ref_des']
        },
                         row_table=RAMSTKValidation)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_create_rows, 'succeed_retrieve_validations')
        pub.subscribe(self._do_create_validation_matrix_columns,
                      'succeed_retrieve_hardware')
        pub.subscribe(self._do_create_validation_matrix_columns,
                      'succeed_retrieve_requirements')
        pub.subscribe(self._on_delete_validation, 'succeed_delete_validation')
        pub.subscribe(self._on_delete_hardware, 'succeed_delete_hardware')
        pub.subscribe(self._on_delete_requirement,
                      'succeed_delete_requirement')
        pub.subscribe(self._on_insert_validation, 'succeed_insert_validation')
        pub.subscribe(self._on_insert_hardware, 'succeed_insert_hardware')
        pub.subscribe(self._on_insert_requirement,
                      'succeed_insert_requirement')

    def _do_create_validation_matrix_columns(self, tree: treelib.Tree) -> None:
        """Create the Validation data matrix columns.

        :param tree: the treelib Tree() containing the correlated workflow
            module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        # If the row tree has already been loaded, we can build the matrix.
        # Otherwise the matrix will be built when the row tree is loaded.
        if tree.get_node(0).tag == 'hardware':
            self._col_tree['vldtn_hrdwr'] = tree
            if self._row_tree.all_nodes():
                super().do_create_columns('vldtn_hrdwr')
                pub.sendMessage('request_select_matrix',
                                matrix_type='vldtn_hrdwr')
        elif tree.get_node(0).tag == 'requirement':
            self._col_tree['vldtn_rqrmnt'] = tree
            if self._row_tree.all_nodes():
                super().do_create_columns('vldtn_rqrmnt')
                pub.sendMessage('request_select_matrix',
                                matrix_type='vldtn_rqrmnt')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_hardware(self, node_id: int, tree: treelib.Tree) -> Any:
        """Delete the node ID column from the Validation::Hardware matrix.

        :param node_id: the hardware treelib Node ID that was deleted.
            Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['vldtn_hrdwr'].get_node(node_id).tag
        return super().do_delete_column(_tag, 'vldtn_hrdwr')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_requirement(self, node_id: int, tree: treelib.Tree) -> Any:
        """Delete the node ID column from the Validation::Requirements matrix.

        :param node_id: the requirement treelib Node ID that was deleted.
            Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['vldtn_rqrmnt'].get_node(node_id).tag
        return super().do_delete_column(_tag, 'vldtn_rqrmnt')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_validation(self, node_id: int, tree: treelib.Tree) -> Any:
        """Delete the matrix row associated with the deleted validation.

        :param node_id: the treelib Tree() node ID associated with the
            deleted validation.
        :param tree: the treelib Tree() containing the remaining validation
            data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_delete_row(node_id)

    def _on_insert_hardware(self, node_id: int, tree: treelib.Tree) -> Any:
        """Insert the node ID column to the Validation::Hardware matrix.

        :param node_id: the hardware treelib Node ID that is to be
            inserted.  Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['vldtn_hrdwr'].get_node(node_id).tag
        return super().do_insert_column(_tag, 'vldtn_hrdwr')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert_requirement(self, node_id: int, tree: treelib.Tree) -> Any:
        """Insert the node ID column to the Hardware::Requirements matrix.

        :param node_id: the requirement treelib Node ID that is to be
            inserted.  Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['vldtn_rqrmnt'].get_node(node_id).tag
        return super().do_insert_column(_tag, 'vldtn_rqrmnt')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert_validation(self, node_id: int, tree: treelib.Tree) -> None:
        """Insert row into matrix when new validation task is added.

        :param node_id: the treelib Tree() node ID associated with the
            inserted validation.
        :param tree: the treelib Tree() containing the remaining validation
            data.
        :return: None
        :rtype: None
        """
        self.do_insert_row(node_id)
