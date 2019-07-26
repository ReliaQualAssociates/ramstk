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
from ramstk.models.programdb import RAMSTKRequirement, RAMSTKValidation


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
                'hrdwr_rqrmnt':
                [RAMSTKRequirement, 'requirement_id', 'requirement_code'],
                'hrdwr_vldtn': [RAMSTKValidation, 'validation_id', 'name']
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
        pub.subscribe(self._do_delete_validation, 'succeed_delete_validation')
        pub.subscribe(self.do_delete_row, 'succeed_delete_validation')
        pub.subscribe(self.do_insert_row, 'succeed_insert_validation')
        pub.subscribe(self._do_insert_requirement,
                      'succeed_insert_requirement')
        pub.subscribe(self._do_insert_validation, 'succeed_insert_validation')
        pub.subscribe(self.do_update, 'request_update_validation_matrix')
        pub.subscribe(self._on_get_tree, 'succeed_get_validation_tree')
        pub.subscribe(self._on_get_tree, 'succeed_get_requirement_tree')
        pub.subscribe(self._on_get_tree, 'succeed_get_validation_tree')
