# -*- coding: utf-8 -*-
#
#       rtk.revision.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
Revision Package
===============================================================================
"""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from datamodels import RTKDataController  # pylint: disable=E0401
from . import dtmRevision


class RevisionDataController(RTKDataController):
    """
    The Revision data controller provides an interface between the Revision
    data model and an RTK view model.  A single Revision controller can manage
    one or more Revision data models.  The attributes of a Revision data
    controller are:

    :ivar _dtm_revision: the :py:class:`rtk.revision.Revision.Model` associated
                         with the Revision Data Controller.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Method to initialize a Revision data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Revision Data
                    Model.
        :type dao: :py:class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        RTKDataController.__init__(
            self, configuration, module=dtmRevision(dao), **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_insert(self):
        """
        Method to request the Revision Data Model to add a new Revision to the
        RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _error_code, _msg = self._dtm_data_model.insert(None)

        if _error_code == 0 and not self._test:
            pub.sendMessage(
                'insertedRevision', revision_id=self.dtm_revision.last_id)
        else:
            _msg = _msg + '  Failed to add a new Revision to the RTK ' \
                'Program database.'

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, revision_id):
        """
        Method to request the Revision Data Model to delete a Revision from the
        RTK Program database.

        :param int revision_id: the Revision ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_data_model.delete(revision_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedRevision')

    def request_update(self, revision_id):
        """
        Method to request the Revision Data Model save the RTKRevision
        attributes to the RTK Program database.

        :param int revision_id: the ID of the revision to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_data_model.update(revision_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedRevision')

    def request_update_all(self):
        """
        Method to request the Revision Data Model to save all RTKRevision
        model attributes to the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)
