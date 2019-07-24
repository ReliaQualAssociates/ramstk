# -*- coding: utf-8 -*-
#
#       ramstk.revision.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Controller Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.programdb import (
    RAMSTKHardware, RAMSTKRequirement, RAMSTKValidation
)
from ramstk.modules import RAMSTKDataController, RAMSTKDataMatrix

# RAMSTK Local Imports
from . import dtmValidation


class ValidationDataController(RAMSTKDataController):
    """
    Provide an interface between Validation data models and RAMSTK views.

    A single Validation data controller can manage one or more Failure
    Validation data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Validation data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RAMSTK Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        :param configuration: the RAMSTK configuration instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmValidation(dao, **kwargs),
            ramstk_module='validation',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_vldtn_rqrmnt_matrix = RAMSTKDataMatrix(
            dao,
            row_table=RAMSTKValidation,
            column_table=RAMSTKRequirement,
            **kwargs,
        )
        self._dmx_vldtn_hw_matrix = RAMSTKDataMatrix(
            dao,
            row_table=RAMSTKValidation,
            column_table=RAMSTKHardware,
            **kwargs,
        )
        self._dic_inserts = {
            'vldtn_rqrmnt': self._dmx_vldtn_rqrmnt_matrix.do_insert,
            'vldtn_hrdwr': self._dmx_vldtn_hw_matrix.do_insert,
        }

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self.request_do_calculate,
            'request_calculate_validation',
        )
        pub.subscribe(
            self._request_do_create_matrix,
            'request_create_validation_matrix',
        )
        pub.subscribe(
            self.request_do_calculate_all,
            'request_calculate_all_validations',
        )
        pub.subscribe(self.request_do_delete, 'request_delete_validation')
        pub.subscribe(
            self._request_do_delete_matrix,
            'request_delete_validation_matrix',
        )
        pub.subscribe(self.request_do_insert, 'request_insert_validation')
        pub.subscribe(
            self.request_do_insert_matrix,
            'request_insert_validation_matrix',
        )
        pub.subscribe(self.request_do_update, 'request_update_validation')
        pub.subscribe(
            self.request_do_update_all,
            'request_update_all_validations',
        )
        pub.subscribe(
            self._request_do_update_matrix,
            'request_update_validation_matrix',
        )
        pub.subscribe(self.request_do_update_status, 'request_update_status')
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(
            self._request_do_select_all_matrix,
            'request_select_validation_matrix',
        )
        pub.subscribe(self.request_set_attributes, 'mvw_editing_validation')
        pub.subscribe(self.request_set_attributes, 'wvw_editing_validation')

    def _request_do_create_matrix(self, revision_id, matrix_type):
        """
        Request to create or refresh a Validation matrix.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param str matrix_type: the type of the Matrix to select all rows and
                                all columns for.
        """
        _dic_creates = {
            'vldtn_rqrmnt':
            [self._dmx_vldtn_rqrmnt_matrix.do_create, 'requirement_id'],
            'vldtn_hrdwr':
            [self._dmx_vldtn_hw_matrix.do_create, 'hardware_id'],
        }

        try:
            _create_method = _dic_creates[matrix_type][0]
            _col_id = _dic_creates[matrix_type][1]
        except KeyError:
            _create_method = None

        try:
            _create_method(
                revision_id, matrix_type, rkey='validation_id', ckey=_col_id,
            )
        except TypeError:
            _error_code = 6
            _msg = 'RAMSTK ERROR: Failed to create matrix ' \
                   '{0:s}.'.format(matrix_type)

            RAMSTKDataController.do_handle_results(
                self, _error_code, _msg,
                None,
            )

    def _request_do_delete_matrix(self, matrix_type, item_id, row=True):
        """
        Request to remove a row or column from the selected Data Matrix.

        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Validation matrix types are:

                                rqrmnt_hrdwr = Validation:Hardware

        :param int item_id: the ID of the row or column item to remove from the
                            Matrix.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_deletes = {
            'vldtn_rqrmnt': self._dmx_vldtn_rqrmnt_matrix.do_delete,
            'vldtn_hrdwr': self._dmx_vldtn_hw_matrix.do_delete,
        }

        try:
            self._matrix_delete_method = _dic_deletes[matrix_type]
        except KeyError:
            self._matrix_delete_method = None

        return RAMSTKDataController.request_do_delete_matrix(
            self, matrix_type, item_id, row=row,
        )

    def _request_do_select_all_matrix(self, revision_id, matrix_type):
        """
        Retrieve all the Matrices associated with the Requirement module.

        :param int revision_id: the Revision ID to select the matrices for.
        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Validation matrix types are:

                                vldtn_hrdwr = Requirement:Hardware

        :return: (_matrix, _column_hdrs, _row_hdrs); the Pandas Dataframe,
                 noun names to use for column headings, noun names to use for
                 row headings.
        :rtype: (:class:`pandas.DataFrame`, dict, dict)
        """
        _matrix = None
        _column_hdrs = []
        _row_hdrs = []

        if matrix_type == 'vldtn_rqrmnt':
            self._dmx_vldtn_rqrmnt_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='validation_id',
                ckey='requirement_id',
                rheader='description',
                cheader='requirement_code',
            )
            _matrix = self._dmx_vldtn_rqrmnt_matrix.dtf_matrix
            _column_hdrs = self._dmx_vldtn_rqrmnt_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_vldtn_rqrmnt_matrix.dic_row_hdrs
        elif matrix_type == 'vldtn_hrdwr':
            self._dmx_vldtn_hw_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='validation_id',
                ckey='hardware_id',
                rheader='description',
                cheader='comp_ref_des',
            )
            _matrix = self._dmx_vldtn_hw_matrix.dtf_matrix
            _column_hdrs = self._dmx_vldtn_hw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_vldtn_hw_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def _request_do_update_matrix(self, revision_id, matrix_type):
        """
        Request to update the selected Data Matrix.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_type: the type of the Matrix to save.  Current
                                Validation matrix types are:

                                vldtn_hrdwr = Requirement:Hardware

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_updates = {
            'vldtn_rqrmnt': self._dmx_vldtn_rqrmnt_matrix.do_update,
            'vldtn_hrdwr': self._dmx_vldtn_hw_matrix.do_update,
        }

        try:
            self._matrix_update_method = _dic_updates[matrix_type]
        except KeyError:
            self._matrix_update_method = None

        return RAMSTKDataController.request_do_update_matrix(
            self, revision_id, matrix_type,
        )

    def request_do_update_status(self):
        """
        Request to update program Validation task status.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_status()

        return RAMSTKDataController.do_handle_results(
            self, _error_code, _msg,
            None,
        )
