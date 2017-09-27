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

    def handle_results(self, error_code, error_msg, pub_msg=None):
        """
        Method to handle the error code and error message from the insert,
        delete, update, and calculate methods.

        :param int error_code: the error code returned by the Data Model when
                               requested to insert.
        :param str error_msg: the error message returned by the Data Model when
                              requested to insert.
        :param str pub_msg: the message to be published by pypubsub.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # If the insert, delete, update, or calculation was successful log the
        # error message to the user log.  Otherwise, log it to the debug log.
        if error_code == 0:
            self._configuration.RTK_USER_LOG.info(error_msg)

            if pub_msg is not None and not self._test:
                pub.sendMessage(pub_msg)
        else:
            self._configuration.RTK_DEBUG_LOG.error(error_msg)
            _return = True

        return _return
