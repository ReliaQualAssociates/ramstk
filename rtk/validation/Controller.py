# -*- coding: utf-8 -*-
#
#       rtk.revision.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Controller Module."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataController  # pylint: disable=E0401
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

    def request_insert(self, revision_id):
        """
        Request to add an RTKValidation table record.

        :param int revision_id: the Revision ID this Validation will be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.insert(
            revision_id=revision_id)

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

    def request_delete(self, definition_id):
        """
        Request to delete an RTKValidation table record.

        :param int definition_id: the Validation ID to delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.delete(definition_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedValidation')

    def request_update(self, definition_id):
        """
        Request to update an RTKValidation table record.

        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update(definition_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedValidation')

    def request_update_all(self):
        """
        Request to update all records in the RTKValidation table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_calculate(self, validation_id):
        """
        Request to calculate the Validation task metrics.

        This method calls the data model methods to calculate task cost and
        task time.

        :param int validation_id: the ID of the Validation task to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _msg = 'RTK SUCCESS: Calculating Validation Task {0:d} cost and ' \
               'time metrics.'.format(validation_id)

        _costs = self._dtm_data_model.calculate_costs(validation_id)
        _time = self._dtm_data_model.calculate_time(validation_id)

        if not _costs and not _time:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('calculatedValidation')

        elif _costs:
            _msg = 'RTK ERROR: Calculating Validation Task {0:d} cost ' \
                   'metrics.'.format(validation_id)
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        elif _time:
            _msg = 'RTK ERROR: Calculating Validation Task {0:d} time ' \
                   'metrics.'.format(validation_id)
            self._configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return
