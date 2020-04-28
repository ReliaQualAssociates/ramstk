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
    """
    Contain the attributes and methods of the Hardware matrix manager.

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
        pub.subscribe(self.do_create_rows, 'succeed_retrieve_hardware')
        pub.subscribe(self._on_delete_hardware, 'succeed_delete_hardware')
        pub.subscribe(self._on_insert_hardware, 'succeed_insert_hardware')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_delete_hardware(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Delete the matrix row associated with the deleted hardware.

        :param int node_id: the treelib Tree() node ID associated with the
            deleted hardware.
        :param tree: the treelib Tree() containing the remaining hardware data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_delete_row(node_id)

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def _on_insert_hardware(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Insert a matrix row associated with the inserted hardware.

        :param int node_id: the treelib Tree() node ID associated with the
            inserted hardware.
        :param tree: the treelib Tree() containing the remaining hardware data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.do_insert_row(node_id)
