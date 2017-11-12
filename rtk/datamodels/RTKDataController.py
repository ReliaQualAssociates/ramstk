# -*- coding: utf-8 -*-
#
#       rtk.datamodels.RTKDataController.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
RTKDataController Module
===============================================================================
"""

from pubsub import pub  # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKDataController(object):
    """
    This is the meta-class for all RTK data controllers.

    :ivar _configuration: the :py:class:`rtk.Configuration.Configuration`
                          instance associated with the current RTK instance.
    :ivar _dtm_data_model:
    :ivar bool _test:
    """

    def __init__(self, configuration, module=None, rtk_module=None, **kwargs):
        """
        Base method to initialize a RTK data controller instance.

        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._configuration = configuration
        self._dtm_data_model = module
        self._test = kwargs['test']

        self._module = None
        for __, char in enumerate(rtk_module):
            if char.isalpha():
                self._module = rtk_module.capitalize()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_handle_results(self, error_code, error_msg, pub_msg=None):
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

    def handle_results(self, error_code, error_msg, pub_msg=None):

        return self.do_handle_results(
            error_code, error_msg, pub_msg=None)

    def request_select(self, node_id):
        """
        Method to request the Requirement Data Model to retrieve the
        RTKRequirement model associated with the Requirement ID.

        :param int requirement_id: the Requirement ID to retrieve.
        :return: the RTKRequirement model requested.
        :rtype: `:class:rtk.dao.DAO.RTKRequirement` model
        """

        return self._dtm_data_model.select(node_id)

    def request_select_all(self, node_id):
        """
        Method to retrieve the Requirement tree from the Requirement Data
        Model.

        :param int revision_id: the Revision ID to select the Requirements for.
        :return: tree; the treelib Tree() of RTKRequirement models in the
                 Requirement tree.
        :rtype: dict
        """

        return self._dtm_data_model.select_all(node_id)

    def request_get_attributes(self, node_id):
        """
        Method to request the attributes from the record in the RTK Program
        database table associated with node_id.

        :param int node_id: the ID of the record in the RTK Program database
                            whose attributes are being requested.
        :return: _attributes
        :rtype: dict
        """

        _entity = self.request_select(node_id)

        return _entity.get_attributes()

    def request_set_attributes(self, node_id, attributes):
        """
        Method to set the attributes of the RTK Program database table record
        data model associated with node_id.

        :param int node_id: the ID of the record in the RTK Program database
                            table whose attributes are to be set.
        :param dict attributes: the dictionary of attributes and values.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _entity = self.request_select(node_id)

        return _entity.set_attributes(attributes)

    def request_last_id(self):
        """
        Method to request the last Requirement ID used in the RTK Program
        database.

        :return: the last Requirement ID used.
        :rtype: int
        """

        return self._dtm_data_model.last_id

    def request_calculate_reliability(self,
                                      node_id,
                                      mission_time,
                                      multiplier=1.0):
        """
        Request reliability attributes be calculated for the Node ID passed.

        :param int node_id: the ID of the entity in the treelib.Tree() to
                            calculate.
        :param float mission_time: the time to use in the calculations.
        :keyword float multiplier: the hazard rate multiplier.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, \
            _msg = self._dtm_data_model.calculate_reliability(node_id,
                                                              mission_time,
                                                              multiplier)

        return self.handle_results(_error_code, _msg,
                                   'calculated' + self._module)

    def request_calculate_availability(self, revision_id):
        """
        Method to request availability attributes be calculated for the
        Revision ID passed.

        :param int revision_id: the Revision ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, \
            _msg = self._dtm_data_model.calculate_availability(revision_id)

        return self.handle_results(_error_code, _msg,
                                   'calculatedRevision')

    def request_calculate_costs(self, revision_id, mission_time):
        """
        Method to request cost attributes be calculated for the Revision ID
        passed.

        :param int revision_id: the Revision ID to calculate.
        :param float mission_time: the time to use in the calculations.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _error_code, _msg = self._dtm_data_model.calculate_costs(
            revision_id, float(mission_time))

        return self.handle_results(_error_code, _msg,
                                   'calculatedRevision')
