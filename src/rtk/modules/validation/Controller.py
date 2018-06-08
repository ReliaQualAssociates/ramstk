# -*- coding: utf-8 -*-
#
#       rtk.revision.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Controller Module."""

from pubsub import pub

# Import other RTK modules.
from rtk.modules import RTKDataController
from . import dtmValidation


class ValidationDataController(RTKDataController):
    """
    Provide an interface between Validation data models and RTK views.

    A single Validation data controller can manage one or more Failure
    Validation data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Validation data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RTK Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        :param configuration: the RTK configuration instance.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmValidation(dao),
            rtk_module='validation',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_insert(self, **kwargs):
        """
        Request to add an RTKValidation table record.

        :param int revision_id: the Revision ID this Validation will be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _revision_id = kwargs['revision_id']
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=_revision_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('insertedValidation')
        else:
            _msg = _msg + '  Failed to add a new Validation to the ' \
                          'RTK Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_delete(self, node_id):
        """
        Request to delete an RTKValidation table record.

        :param int node_id: the PyPubSub Tree() ID of the Validation task to
                            delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedValidation')

    def request_do_update(self, node_id):
        """
        Request to update an RTKValidation table record.

        :param int node_id: the PyPubSub Tree() ID of the Validation task to
                            delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedValidation')

    def request_do_update_all(self, **kwargs):
        """
        Request to update all records in the RTKValidation table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_all(**kwargs)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_update_status(self):
        """
        Request to update program Validation task status.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_status()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_calculate(self, node_id, **kwargs):
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
        _msg = 'RTK SUCCESS: Calculating Validation Task {0:d} cost and ' \
               'time metrics.'.format(node_id)

        _costs = self._dtm_data_model.do_calculate(
            node_id, metric='cost')
        _time = self._dtm_data_model.do_calculate(
            node_id, metric='time')

        if not _costs and not _time:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('calculatedValidation', module_id=node_id)

        elif _costs:
            _msg = 'RTK ERROR: Calculating Validation Task {0:d} cost ' \
                   'metrics.'.format(node_id)
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        elif _time:
            _msg = 'RTK ERROR: Calculating Validation Task {0:d} time ' \
                   'metrics.'.format(node_id)
            self._configuration.RTK_DEBUG_LOG.error(_msg)
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
