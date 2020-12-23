# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.MatrixManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package matrix manager."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKMatrixManager
from ramstk.models.programdb import (
    RAMSTKHardware, RAMSTKRequirement, RAMSTKValidation
)


class MatrixManager(RAMSTKMatrixManager):
    """Contain the attributes and methods of the Hardware matrix manager.

    This class manages the hardware matrices for Requirements and Validation.
    Attributes of the hardware Matrix Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    """

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize an instance of the hardware matrix manager."""
        RAMSTKMatrixManager.__init__(
            self,
            column_tables={
                'hrdwr_rqrmnt':
                [RAMSTKRequirement, 'requirement_id', 'requirement_code'],
                'hrdwr_vldtn': [RAMSTKValidation, 'validation_id', 'name']
            },
            row_table=RAMSTKHardware)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        # pub.subscribe(self.do_create_rows, 'succeed_retrieve_hardware')
        # pub.subscribe(self._do_create_hardware_matrix_columns,
        #               'succeed_retrieve_requirements')
        # pub.subscribe(self._do_create_hardware_matrix_columns,
        #               'succeed_retrieve_validations')
        # pub.subscribe(self._on_delete_hardware, 'succeed_delete_hardware')
        # pub.subscribe(self._on_delete_requirement,
        #               'succeed_delete_requirement')
        # pub.subscribe(self._on_delete_validation, 'succeed_delete_validation')
        # pub.subscribe(self._on_insert_hardware, 'succeed_insert_hardware')
        # pub.subscribe(self._on_insert_requirement,
        #               'succeed_insert_requirement')
        # pub.subscribe(self._on_insert_validation, 'succeed_insert_validation')

    def _do_create_hardware_matrix_columns(self, tree: treelib.Tree) -> None:
        """Create the Hardware data matrix columns.

        :param tree: the treelib Tree() containing the correlated workflow
            module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        # If the row tree has already been loaded, we can build the matrix.
        # Otherwise the matrix will be built when the row tree is loaded.
        if tree.get_node(0).tag == 'requirement':
            self._col_tree['hrdwr_rqrmnt'] = tree
            if self._row_tree.all_nodes():
                super().do_create_columns('hrdwr_rqrmnt')
                pub.sendMessage('request_select_matrix',
                                matrix_type='hrdwr_rqrmnt')
        elif tree.get_node(0).tag == 'validation':
            self._col_tree['hrdwr_vldtn'] = tree
            if self._row_tree.all_nodes():
                super().do_create_columns('hrdwr_vldtn')
                pub.sendMessage('request_select_matrix',
                                matrix_type='hrdwr_vldtn')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_hardware(self, node_id: int, tree: treelib.Tree) -> None:
        """Delete the matrix row associated with the deleted hardware.

        :param node_id: the treelib Tree() node ID associated with the
            deleted hardware.
        :param tree: the treelib Tree() containing the remaining hardware data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_delete_row(node_id)

    def _on_delete_requirement(self, tree: treelib.Tree) -> Any:
        """Delete the node ID column from the Hardware::Requirement matrix.

        :param node_id: the requirement treelib Node ID that was deleted.
            Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['hrdwr_rqrmnt'].get_node(node_id).tag
        return super().do_delete_column(_tag, 'hrdwr_rqrmnt')

    def _on_delete_validation(self, node_id: int, tree: treelib.Tree) -> Any:
        """Delete the node ID column from the Hardware::Validation matrix.

        :param node_id: the validation treelib Node ID that was deleted.
            Note that node ID = validation ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['hrdwr_vldtn'].get_node(node_id).tag
        return super().do_delete_column(_tag, 'hrdwr_vldtn')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert_hardware(self, node_id: int, tree: treelib.Tree) -> None:
        """Insert a matrix row associated with the inserted hardware.

        :param node_id: the treelib Tree() node ID associated with the
            inserted hardware.
        :param tree: the treelib Tree() containing the remaining hardware data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_insert_row(node_id)

    def _on_insert_requirement(self, node_id: int, tree: treelib.Tree) -> Any:
        """Insert the node ID column to the Hardware::Requirement matrix.

        :param node_id: the requirement treelib Node ID that is to be
            inserted.  Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['hrdwr_rqrmnt'].get_node(node_id).tag
        return super().do_insert_column(_tag, 'hrdwr_rqrmnt')

    def _on_insert_validation(self, node_id: int, tree: treelib.Tree) -> Any:
        """Insert the node ID column to the Hardware::Validation matrix.

        :param node_id: the validation treelib Node ID that is to be
            inserted.  Note that node ID = validation ID = matrix row ID.
        :return: None
        :rtype: None
        """
        _tag = self._col_tree['hrdwr_vldtn'].get_node(node_id).tag
        return super().do_insert_column(_tag, 'hrdwr_vldtn')
