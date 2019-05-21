# -*- coding: utf-8 -*-
#
#       ramstk.modules.function.Controller.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Controller."""

# Import third party modules.
from pubsub import pub

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
from ramstk.modules import RAMSTKDataMatrix
from ramstk.dao import RAMSTKFunction, RAMSTKHardware, RAMSTKSoftware
from . import dtmFunction


class FunctionDataController(RAMSTKDataController):
    """
    Provide interface between Function data model and RAMSTK view model.

    A single Function controller can manage one or more Function data
    models.  The attributes of a Function data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Function data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the
                    Function Data Model.
        :type dao: :class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with
                              the current instance of the RAMSTK
                              application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmFunction(dao, **kwargs),
            ramstk_module='function',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_fctn_hw_matrix = RAMSTKDataMatrix(dao, RAMSTKFunction,
                                                    RAMSTKHardware)
        self._dmx_fctn_sw_matrix = RAMSTKDataMatrix(dao, RAMSTKFunction,
                                                    RAMSTKSoftware)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._request_do_create_matrix,
                      'request_create_function_matrix')
        pub.subscribe(self.request_do_delete, 'request_delete_function')
        pub.subscribe(self._request_do_delete_matrix,
                      'request_delete_function_matrix')
        pub.subscribe(self.request_do_insert, 'request_insert_function')
        pub.subscribe(self._request_do_insert_matrix,
                      'request_insert_function_matrix')
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(self._request_do_select_all_matrix,
                      'request_select_function_matrix')
        pub.subscribe(self.request_do_update, 'request_update_function')
        pub.subscribe(self.request_do_update_all,
                      'request_update_all_functions')
        pub.subscribe(self._request_do_update_matrix,
                      'request_update_function_matrix')
        pub.subscribe(self.request_set_attributes, 'mvw_editing_function')
        pub.subscribe(self.request_set_attributes, 'wvw_editing_function')

    def _request_do_create_matrix(self, revision_id, matrix_type):
        """
        Request to create or refresh a Function matrix.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param str matrix_type: the type of the Matrix to select all rows and
                                columns.
        :return: None
        :rtype: None
        """
        _dic_creates = {
            'fnctn_hrdwr':
            [self._dmx_fctn_hw_matrix.do_create, 'hardware_id'],
            'fnctn_sftwr':
            [self._dmx_fctn_sw_matrix.do_create, 'software_id']
        }

        try:
            _create_method = _dic_creates[matrix_type][0]
            _col_id = _dic_creates[matrix_type][1]
        except KeyError:
            _create_method = None

        try:
            _create_method(
                revision_id, matrix_type, rkey='function_id', ckey=_col_id)
        except TypeError:
            _error_code = 6
            _msg = 'RAMSTK ERROR: Failed to create matrix ' \
                   '{0:s}.'.format(matrix_type)

            RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def _request_do_delete_matrix(self, matrix_type, item_id, row=True):
        """
        Request to remove a row or column from the selected Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
                                Function matrix types are:

                                fnctn_hrdwr = Function:Hardware
                                fnctn_sftwr = Function:Software
                                fnctn_vldtn = Function:Validation

        :param int item_id: the ID of the row or column item to remove from the
                            Matrix.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_deletes = {
            'fnctn_hrdwr': self._dmx_fctn_hw_matrix.do_delete,
            'fnctn_sftwr': self._dmx_fctn_sw_matrix.do_delete
        }

        try:
            self._matrix_delete_method = _dic_deletes[matrix_type]
        except KeyError:
            self._matrix_delete_method = None

        return RAMSTKDataController.request_do_delete_matrix(
            self, matrix_type, item_id, row=row)

    def _request_do_insert_matrix(self,
                                  matrix_type,
                                  item_id,
                                  heading,
                                  row=True):
        """
        Request the to add a new row or column to the Data Matrix.

        :param str matrix_type: the type of the Matrix to insert into.  Current
                                Function matrix types are:

                                fnctn_hrdwr = Function:Hardware
                                fnctn_sftwr = Function:Software
                                fnctn_vldtn = Function:Validation

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix.
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_inserts = {
            'fnctn_hrdwr': self._dmx_fctn_hw_matrix.do_insert,
            'fnctn_sftwr': self._dmx_fctn_sw_matrix.do_insert
        }

        try:
            self._matrix_insert_method = _dic_inserts[matrix_type]
        except KeyError:
            self._matrix_insert_method = None

        return RAMSTKDataController.request_do_insert_matrix(
            self, matrix_type, item_id, heading, row=row)

    def _request_do_select_all_matrix(self, revision_id, matrix_type):
        """
        Retrieve all the Matrices associated with the Function.

        :param int revision_id: the Revision ID to select the matrices for.
        :param int matrix_type: the type of the Matrix to retrieve.  Current
                                Function matrix types are:

                                fnctn_hrdwr = Function:Hardware
                                fnctn_sftwr = Function:Software
                                fnctn_vldtn = Function:Validation

        :return: (_matrix, _column_hdrs, _row_hdrs); the Pandas Dataframe,
                 noun names to use for column headings, noun names to use for
                 row headings.
        :rtype: (:class:`pandas.DataFrame`, dict, dict)
        """
        _matrix = None
        _column_hdrs = []
        _row_hdrs = []

        if matrix_type == 'fnctn_hrdwr':
            self._dmx_fctn_hw_matrix.do_select_all(
                revision_id,
                matrix_type,
                rkey='function_id',
                ckey='hardware_id',
                rheader='function_code',
                cheader='comp_ref_des')
            _matrix = self._dmx_fctn_hw_matrix.dtf_matrix
            _column_hdrs = self._dmx_fctn_hw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_fctn_hw_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def _request_do_update_matrix(self, revision_id, matrix_type):
        """
        Request to update the selected Data Matrix.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_type: the type of the Matrix to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _dic_updates = {
            'fnctn_hrdwr': self._dmx_fctn_hw_matrix.do_update,
            'fnctn_sftwr': self._dmx_fctn_sw_matrix.do_update
        }

        try:
            self._matrix_update_method = _dic_updates[matrix_type]
        except KeyError:
            self._matrix_update_method = None

        return RAMSTKDataController.request_do_update_matrix(
            self, revision_id, matrix_type)
