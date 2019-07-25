# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.MatrixManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package matrix manager."""

# Third Party Imports
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

    def __init__(self, **kwargs):  # pylint: disable=unused-argument
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
        pub.subscribe(self._do_create, 'succeed_select_revision')
        pub.subscribe(self._do_delete_requirement,
                      'succeed_delete_requirement')
        pub.subscribe(self._do_delete_validation, 'succeed_delete_validation')
        pub.subscribe(self.do_delete_row, 'succeed_delete_hardware')
        pub.subscribe(self.do_insert_row, 'succeed_insert_hardware')
        pub.subscribe(self._do_insert_requirement,
                      'succeed_insert_requirement')
        pub.subscribe(self._do_insert_validation, 'succeed_insert_validation')
        pub.subscribe(self.do_update, 'request_update_hardware_matrix')
        pub.subscribe(self._on_get_tree, 'succeed_get_hardware_tree')
        pub.subscribe(self._on_get_tree, 'succeed_get_requirement_tree')
        pub.subscribe(self._on_get_tree, 'succeed_get_validation_tree')

    def _do_create(self, revision_id):  # pylint: disable=unused-argument
        """
        Create the Hardware data matrices.

        :param int revision_id: the revision ID to gather the data that will be
            used to create the matrices.
        :return:
        :rtype:
        """
        self.dic_matrices = {}

        pub.sendMessage('request_get_hardware_tree')

        # See ISSUE at https://github.com/ReliaQualAssociates/ramstk/issues/251
        # pub.sendMessage('request_get_requirements_tree')
        RAMSTKMatrixManager.do_create(self, 'hrdwr_rqrmnt')

        # See ISSUE at https://github.com/ReliaQualAssociates/ramstk/issues/250
        # pub.sendMessage('request_get_validation_tree')
        # RAMSTKMatrixManager.do_create(self, 'hrdwr_vldtn')

    def _do_delete_requirement(self, node_id):
        """
        Delete the node ID column from the Hardware::Requirements matrix.

        :param int node_id: the requirement treelib Node ID that was deleted.
            Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_delete_column(self, node_id,
                                                    'hrdwr_rqrmnt')

    def _do_delete_validation(self, node_id):
        """
        Delete the node ID column from the Hardware::Validation matrix.

        :param int node_id: the validation treelib Node ID that was deleted.
            Note that node ID = validation ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_delete_column(self, node_id,
                                                    'hrdwr_vldtn')

    def _do_insert_requirement(self, node_id):
        """
        Insert the node ID column to the Hardware::Requirements matrix.

        :param int node_id: the requirement treelib Node ID that is to be
            inserted.  Note that node ID = requirement ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_insert_column(self, node_id,
                                                    'hrdwr_rqrmnt')

    def _do_insert_validation(self, node_id):
        """
        Insert the node ID column to the Hardware::Validation matrix.

        :param int node_id: the validation treelib Node ID that is to be
            inserted.  Note that node ID = validation ID = matrix row ID.
        :return: None
        :rtype: None
        """
        return RAMSTKMatrixManager.do_insert_column(self, node_id,
                                                    'hrdwr_vldtn')

    def _on_get_tree(self, dmtree):
        """
        Request the hardware treelib Tree().

        :param dmtree: the hardware treelib Tree().
        :type dmtree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        if dmtree.get_node(0).tag == 'hardware':
            self._row_tree = dmtree
        else:
            self._col_tree = dmtree
