# -*- coding: utf-8 -*-
#
#       rtk.revision.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Failure Defintion Package Data Controller Module."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataController  # pylint: disable=E0401
from . import dtmFailureDefinition


class FailureDefinitionDataController(RTKDataController):
    """
    Provide an interface between Failure Definition data models and RTK views.

    A single Failure Definition data controller can manage one or more Failure
    Definition data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Failure Definition data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RTK Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        :param configuration: the RTK configuration instance.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmFailureDefinition(dao),
            rtk_module='failure_definition',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_insert(self, revision_id):
        """
        Request to add an RTKFailureDefinition table record.

        :param int revision_id: the Revision ID this Failure Definition will be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.insert(
            revision_id=revision_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('insertedDefinition')
        else:
            _msg = _msg + '  Failed to add a new Failure Definition to the ' \
                          'RTK Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, definition_id):
        """
        Request to delete an RTKFailureDefinition table record.

        :param int definition_id: the Failure Definition ID to delete.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.delete(definition_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedDefinition')

    def request_update(self, definition_id):
        """
        Request to update an RTKFailureDefinition table record.

        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update(definition_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedDefinition')

    def request_update_all(self):
        """
        Request to update all records in the RTKFailureDefinition table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)
