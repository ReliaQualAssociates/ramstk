# -*- coding: utf-8 -*-
#
#       rtk.function.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Function Package Data Controller."""

from pubsub import pub

# Import other RTK modules.
from rtk.modules import RTKDataController
from rtk.modules import RTKDataMatrix
from rtk.dao import RTKFunction, RTKHardware, RTKSoftware
from . import dtmFunction


class FunctionDataController(RTKDataController):
    """
    Provide an interface between the Function data model and an RTK view model.

    A single Function controller can manage one or more Function data models.
    The attributes of a Function data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Function data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Function Data
                    Model.
        :type dao: :class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmFunction(dao),
            rtk_module='function',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_fctn_hw_matrix = RTKDataMatrix(dao, RTKFunction, RTKHardware)
        self._dmx_fctn_sw_matrix = RTKDataMatrix(dao, RTKFunction, RTKSoftware)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_select_all_matrix(self, revision_id, matrix_type):
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
            self._dmx_fctn_hw_matrix.select_all(
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

    def request_insert(self, revision_id=0, parent_id=0):
        """
        Request to add an RTKFunction table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.insert(
            revision_id=revision_id, parent_id=parent_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage(
                    'insertedFunction', function_id=self.dtm_function.last_id)
        else:
            _msg = _msg + '  Failed to add a new Function to the RTK ' \
                'Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_insert_matrix(self, matrix_type, item_id, heading, row=True):
        """
        Request the to add a new row or column to the Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
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
        if matrix_type == 'fnctn_hrdwr':
            _error_code, _msg = self._dmx_fctn_hw_matrix.insert(
                item_id, heading, row=row)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedMatrix',
                matrix_type=matrix_type,
                item_id=item_id,
                row=row)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, function_id):
        """
        Request to delete an RTKFunction table record.

        :param int function_id: the Function ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.delete(function_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedFunction')

    def request_delete_matrix(self, matrix_type, item_id, row=True):
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
        if matrix_type == 'fnctn_hrdwr':
            _error_code, _msg = self._dmx_fctn_hw_matrix.delete(
                item_id, row=row)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedMatrix')

    def request_update(self, function_id):
        """
        Request to update an RTKFunction table record.

        :param int function_id: the ID of the function to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update(function_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedFunction')

    def request_update_matrix(self, revision_id, matrix_type):
        """
        Request to update the selected Data Matrix.

        :param int revision_id: the ID of the Revision is the matrix to update
                                is associated with.
        :param int matrix_type: the type of the Matrix to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'fnctn_hrdwr':
            _error_code, _msg = self._dmx_fctn_hw_matrix.update(
                revision_id, matrix_type)
        else:
            _error_code = 6
            _msg = 'RTK ERROR: Attempted to update non-existent matrix ' \
                   '{0:s}.'.format(matrix_type)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedMatrix')

    def request_update_all(self):
        """
        Request to update all records in the RTKFunction table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)
