# -*- coding: utf-8 -*-
#
#       rtk.revision.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Controller."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from rtk.modules import RTKDataController  # pylint: disable=E0401
from . import dtmRevision


class RevisionDataController(RTKDataController):
    """
    Provide an interface between the Revision data model and an RTK view model.

    A single Revision controller can manage one or more Revision data models.
    The attributes of a Revision data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Revision data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Revision Data
                    Model.
        :type dao: :py:class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmRevision(dao),
            rtk_module='revision',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Request to add an RTKRevision table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert()

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage(
                    'insertedRevision', revision_id=self.dtm_revision.last_id)
        else:
            _msg = _msg + '  Failed to add a new Revision to the RTK ' \
                'Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_delete(self, node_id):
        """
        Request to delete an RTKRevision table record.

        :param int node_id: the PyPubSub Tree() ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedRevision')

    def request_do_update(self, node_id):
        """
        Request to update an RTKRevision table record.

        :param int node_id: the PyPubSub Tree() ID of the Revision to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedRevision')

    def request_do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Request to update all records in the RTKRevision table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)
