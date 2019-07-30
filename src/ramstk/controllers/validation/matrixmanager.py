# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.matrixmanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Controller Package matrix manager."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKMatrixManager
from ramstk.models.programdb import (
    RAMSTKHardware, RAMSTKRequirement, RAMSTKValidation
)


class MatrixManager(RAMSTKMatrixManager):
    """
    Contain the attributes and methods of the Validation matrix manager.

    This class manages the validation matrices for Requirements and Validation.
    Attributes of the validation Matrix Manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the validation item being analyzed.
    """

    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        """Initialize an instance of the validation matrix manager."""
        RAMSTKMatrixManager.__init__(
            self,
            column_tables={
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
        pub.subscribe(self._do_create, 'succeed_select_revision')
        pub.subscribe(self._do_delete_requirement,
                      'succeed_delete_requirement')
        pub.subscribe(self._do_delete_hardware, 'succeed_delete_hardware')
        pub.subscribe(self.do_delete_row, 'succeed_delete_validation')
        pub.subscribe(self.do_insert_row, 'succeed_insert_validation')
        pub.subscribe(self._do_insert_hardware, 'succeed_insert_hardware')
        pub.subscribe(self._do_insert_requirement,
                      'succeed_insert_requirement')
        pub.subscribe(self.do_update, 'request_update_validation_matrix')
        pub.subscribe(self._on_get_tree, 'succeed_get_validation_tree')
        pub.subscribe(self._on_get_tree, 'succeed_get_requirement_tree')
        pub.subscribe(self._on_get_tree, 'succeed_get_hardware_tree')

    def _do_create(self, revision_id):  # pylint: disable=unused-argument
        """
        Create the Requirement data matrices.

        :param int revision_id: the revision ID to gather the data that will be
            used to create the matrices.
        :return:
        :rtype:
        """
        self.dic_matrices = {}

        pub.sendMessage('request_get_validation_tree')

        pub.sendMessage('request_get_requirement_tree')
        RAMSTKMatrixManager.do_create(self, 'vldtn_rqrmnt')

        pub.sendMessage('request_get_hardware_tree')
        RAMSTKMatrixManager.do_create(self, 'vldtn_hrdwr')

    def _do_delete_hardware(self, node_id):
        """
        Delete the node ID column from the Validation::Hardware matrix.

        :param int node_id: the hardware treelib Node ID that was deleted.
            Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_delete_column(self, node_id,
                                                    'vldtn_hrdwr')

    def _do_delete_requirement(self, node_id):
        """
        Delete the node ID column from the Validation::Requirements matrix.

        :param int node_id: the requirement treelib Node ID that was deleted.
            Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_delete_column(self, node_id,
                                                    'vldtn_rqrmnt')

    def _do_insert_hardware(self, node_id):
        """
        Insert the node ID column to the Validation::Hardware matrix.

        :param int node_id: the hardware treelib Node ID that is to be
            inserted.  Note that node ID = hardware ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_insert_column(self, node_id,
                                                    'vldtn_hrdwr')

    def _do_insert_requirement(self, node_id):
        """
        Insert the node ID column to the Hardware::Requirements matrix.

        :param int node_id: the requirement treelib Node ID that is to be
            inserted.  Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_insert_column(self, node_id,
                                                    'vldtn_rqrmnt')

    def _on_get_tree(self, dmtree):
        """
        Request the validation treelib Tree().

        :param dmtree: the validation treelib Tree().
        :type dmtree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        if dmtree.get_node(0).tag == 'validation':
            self._row_tree = dmtree
        else:
            self._col_tree = dmtree
