# -*- coding: utf-8 -*-
#
#       rtk.datamodels.RTKDataController.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
RTKDataController Module
###############################################################################
"""

from pubsub import pub                              # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKDataController(object):
    """
    This is the meta-class for all RTK data controllers.

    :ivar _configuration: the :py:class:`rtk.Configuration.Configuration`
                          instance associated with the current RTK instance.
    """

    def __init__(self, configuration, **kwargs):
        """
        Base method to initialize a RTK data controller instance.

        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._test = kwargs['test']
        self._configuration = configuration

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_insert(self, error_code, error_msg, entity='entity'):
        """
        Method to request the Data Model to add a new Entity to the RTK
        Program database.

        :param int error_code: the error code returned by the Data Model when
                               requested to insert.
        :param str error_msg: the error message returned by the Data Model when
                              requested to insert.
        :param str pub_msg: the message to be published by pypubsub.
        :param str entity: the type of entity that is being inserted.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if error_code == 0:
            self._configuration.RTK_USER_LOG.info(error_msg)
        else:
            error_msg = error_msg + '  Failed to add a new {0:s} to the ' \
                'RTK Program database.'.format(entity)
            self._configuration.RTK_DEBUG_LOG.error(error_msg)
            _return = True

        return _return

    def request_delete(self, error_code, error_msg, pub_msg):
        """
        Method to request the Data Model to delete an Entity from the RTK
        Program database.

        :param int error_code: the error code returned by the Data Model when
                               requested to insert.
        :param str error_msg: the error message returned by the Data Model when
                              requested to insert.
        :param str pub_msg: the message to be published by pypubsub.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # If the delete was successful log the success message to the user log.
        # Otherwise, update the error message and log it to the debug log.
        if error_code == 0:
            self._configuration.RTK_USER_LOG.info(error_msg)

            if not self._test:
                pub.sendMessage(pub_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(error_msg)
            _return = True

        return _return

    def request_update(self, error_code, error_msg, pub_msg):
        """
        Method to request the Data Model save the RTK<ENTITY> attributes to the
        RTK Program database.

        :param int error_code: the error code returned by the Data Model when
                               requested to insert.
        :param str error_msg: the error message returned by the Data Model when
                              requested to insert.
        :param str pub_msg: the message to be published by pypubsub.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if error_code == 0:
            self._configuration.RTK_USER_LOG.info(error_msg)

            if not self._test:
                pub.sendMessage(pub_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(error_msg)
            _return = True

        return _return

    def request_calculate(self, error_code, error_msg, pub_msg):
        """
        Method to request criticality attributes be calculated for the
        Mode ID passed.

        :param int error_code: the error code returned by the Data Model when
                               requested to insert.
        :param str error_msg: the error message returned by the Data Model when
                              requested to insert.
        :param str pub_msg: the message to be published by pypubsub.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if error_code == 0:
            self._configuration.RTK_USER_LOG.info(error_msg)

            if not self._test:
                pub.sendMessage(pub_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(error_msg)
            _return = True

        return _return
