# -*- coding: utf-8 -*-
#
#       rtk.modules.hazard_analysis.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""HazardAnalysis Package Data Controller Module."""

from pubsub import pub

# Import other RTK modules.
from rtk.datamodels import RTKDataController
from . import dtmHazardAnalysis


class HazardAnalysisDataController(RTKDataController):
    """
    Provide an interface between HazardAnalysis data models and RTK views.

    A single HazardAnalysis data controller can manage one or more HazardAnalysis
    data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a HazardAnalysis data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RTK Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        :param configuration: the RTK configuration instance.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmHazardAnalysis(dao),
            rtk_module='hazard_analysis',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_insert(self, revision_id, **kwargs):
        """
        Request to add an RTKHazardAnalysis table record.

        :param int revision_id: the Revision ID this HazardAnalysis will be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _hardware_id = kwargs['hardware_id']
        _error_code, _msg = self._dtm_data_model.insert(
            revision_id=revision_id,
            hardware_id=_hardware_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('insertedHazardAnalysis')
        else:
            _msg = _msg + '  Failed to add a new Hazard Analysis to the ' \
                          'RTK Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, node_id):
        """
        Request to delete an RTKHazardAnalysis table record.

        :param str node_id: the node (Hazard) ID whose hazard_analysis is to be
                            deleted.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.delete(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedHazardAnalysis')

    def request_update(self, node_id):
        """
        Request to update an RTKHazardAnalysis table record.

        :param str node_id: the node ID to update.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update(node_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedHazardAnalysis')

    def request_update_all(self):
        """
        Request to update all records in the RTKHazardAnalysis table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_calculate(self, node_id):
        """
        Request the hazard_analysis calculations be performed.

        :param int node_id: the Node (Hazard) ID of the hardware item whose
                            goal is to be allocated.
        :param list hazard_rates: the hazard rates of the parent hardware item
                                  to be allocated and each of the child items
                                  (only needed for ARINC apportionment).  Index
                                  0 is the parent hazard rate.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.calculate(node_id)
