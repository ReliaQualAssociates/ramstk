# -*- coding: utf-8 -*-
#
#       ramstk.revision.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Controller Module."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
from ramstk.modules import RAMSTKDataMatrix
from ramstk.dao import RAMSTKHardware, RAMSTKRequirement, RAMSTKValidation
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
            model=dtmValidation(dao),
            ramstk_module='validation',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dmx_vldtn_rqrmnt_matrix = RAMSTKDataMatrix(
            dao, RAMSTKValidation, RAMSTKRequirement)
        self._dmx_vldtn_hw_matrix = RAMSTKDataMatrix(dao, RAMSTKValidation,
                                                     RAMSTKHardware)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_create(self, revision_id, matrix_type):
        """
        Request to create or refresh a Validation matrix.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param str matrix_type: the type of the Matrix to select all rows and
                                all columns for.
        """
        if matrix_type == 'vldtn_rqrmnt':
            self._dmx_vldtn_rqrmnt_matrix.do_create(
                revision_id,
                matrix_type,
                rkey='validation_id',
                ckey='requirement_id')
        elif matrix_type == 'vldtn_hrdwr':
            self._dmx_vldtn_hw_matrix.do_create(
                revision_id,
                matrix_type,
                rkey='validation_id',
                ckey='hardware_id')

        return

    def request_do_select_all_matrix(self, revision_id, matrix_type):
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
                cheader='requirement_code')
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
                cheader='comp_ref_des')
            _matrix = self._dmx_vldtn_hw_matrix.dtf_matrix
            _column_hdrs = self._dmx_vldtn_hw_matrix.dic_column_hdrs
            _row_hdrs = self._dmx_vldtn_hw_matrix.dic_row_hdrs

        return (_matrix, _column_hdrs, _row_hdrs)

    def request_do_insert(self, **kwargs):
        """
        Request to add an RAMSTKValidation table record.

        :param int revision_id: the Revision ID this Validation will be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _revision_id = kwargs['revision_id']
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=_revision_id)

        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('insertedValidation')
        else:
            _msg = _msg + '  Failed to add a new Validation to the ' \
                          'RAMSTK Program database.'
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_insert_matrix(self, matrix_type, item_id, heading,
                                 row=True):
        """
        Request the to add a new row or column to the Data Matrix.

        :param str matrix_type: the type of the Matrix to retrieve.  Current
                                Validation matrix types are:

                                vldtn_hrdwr = Validation:Hardware

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix.
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        if matrix_type == 'vldtn_rqrmnt':
            _error_code, _msg = self._dmx_vldtn_rqrmnt_matrix.do_insert(
                item_id, heading, row=row)
        elif matrix_type == 'vldtn_hrdwr':
            _error_code, _msg = self._dmx_vldtn_hw_matrix.do_insert(
                item_id, heading, row=row)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedMatrix',
                matrix_type=matrix_type,
                item_id=item_id,
                row=row)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_delete(self, node_id):
        """
        Request to delete an RAMSTKValidation table record.

        :param int node_id: the PyPubSub Tree() ID of the Validation task to
                            delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'deletedValidation')

    def request_do_delete_matrix(self, matrix_type, item_id, row=True):
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
        if matrix_type == 'vldtn_rqrmnt':
            _error_code, _msg = self._dmx_vldtn_rqrmnt_matrix.do_delete(
                item_id, row=row)
        elif matrix_type == 'vldtn_hrdwr':
            _error_code, _msg = self._dmx_vldtn_hw_matrix.do_delete(
                item_id, row=row)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'deletedMatrix')

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTKValidation table record.

        :param int node_id: the PyPubSub Tree() ID of the Validation task to
                            delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'savedValidation')

    def request_do_update_matrix(self, revision_id, matrix_type):
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
        if matrix_type == 'vldtn_rqrmnt':
            _error_code, _msg = self._dmx_vldtn_rqrmnt_matrix.do_update(
                revision_id, matrix_type)
        elif matrix_type == 'vldtn_hrdwr':
            _error_code, _msg = self._dmx_vldtn_hw_matrix.do_update(
                revision_id, matrix_type)
        else:
            _error_code = 6
            _msg = 'RAMSTK ERROR: Attempted to update non-existent matrix ' \
                   '{0:s}.'.format(matrix_type)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'savedMatrix')

    def request_do_update_all(self, **kwargs):
        """
        Request to update all records in the RAMSTKValidation table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_all(**kwargs)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_update_status(self):
        """
        Request to update program Validation task status.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_status()

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_calculate(self, node_id, **kwargs):  # pylint: disable=unused-argument
        """
        Request to calculate the Validation task metrics.

        This method calls the data model methods to calculate task cost and
        task time.

        :param int node_id: the PyPubSub Tree() ID of the Validation task
                            to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _msg = 'RAMSTK SUCCESS: Calculating Validation Task {0:d} cost and ' \
               'time metrics.'.format(node_id)

        _costs = self._dtm_data_model.do_calculate(node_id, metric='cost')
        _time = self._dtm_data_model.do_calculate(node_id, metric='time')

        if not _costs and not _time:
            self._configuration.RAMSTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('calculatedValidation', module_id=node_id)

        elif _costs:
            _msg = 'RAMSTK ERROR: Calculating Validation Task {0:d} cost ' \
                   'metrics.'.format(node_id)
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)
            _return = True

        elif _time:
            _msg = 'RAMSTK ERROR: Calculating Validation Task {0:d} time ' \
                   'metrics.'.format(node_id)
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def request_do_calculate_all(self):
        """
        Request to calculate program cost and time.

        :return: (_cost_ll, _cost_mean, _cost_ul,
                  _time_ll, _time_mean, _time_ul); the lower bound, mean,
                 and upper bound for program cost and time.
        :rtype: tuple
        """
        (_cost_ll, _cost_mean, _cost_ul, _time_ll, _time_mean,
         _time_ul) = self._dtm_data_model.do_calculate_all()

        if not self._test:
            pub.sendMessage('calculatedProgram')

        return (_cost_ll, _cost_mean, _cost_ul, _time_ll, _time_mean, _time_ul)

    def request_get_planned_burndown(self):
        """
        Request the planned burndown curve.

        :return: (_y_minimum, _y_average, _y_maximum)
        :rtype: tuple
        """
        return self._dtm_data_model.get_planned_burndown()

    def request_get_assessment_points(self):
        """
        Request the assessment dates, minimum, and maximum values.

        :return: (_assessed_dates, _targets)
        :rtype: tuple
        """
        return self._dtm_data_model.get_assessment_points()

    def request_get_actual_burndown(self):
        """
        Request the actual burndown curve.

        :return: dictionary of actual remaining times for each date the value
                 has been calculated.  Key is the date, value is the remaining
                 time.
        :rtype: dict
        """
        return self._dtm_data_model.get_actual_burndown()
