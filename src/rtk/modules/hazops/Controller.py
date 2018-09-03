# -*- coding: utf-8 -*-
#
#       rtk.modules.hazops.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""HazardAnalysis Package Data Controller Module."""

from pubsub import pub

# Import other RAMSTK modules.
from rtk.modules import RAMSTKDataController
from . import dtmHazardAnalysis


class HazardAnalysisDataController(RAMSTKDataController):
    """
    Provide an interface between HazardAnalysis data models and RAMSTK views.

    A single HazardAnalysis data controller can manage one or more HazardAnalysis
    data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a HazardAnalysis data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RAMSTK Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        :param configuration: the RAMSTK configuration instance.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
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

    def request_do_insert(self, **kwargs):
        """
        Request to add an RAMSTKHazardAnalysis table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _revision_id = kwargs['revision_id']
        _hardware_id = kwargs['hardware_id']
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=_revision_id, hardware_id=_hardware_id)

        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('insertedHazardAnalysis')
        else:
            _msg = _msg + '  Failed to add a new Hazard Analysis to the ' \
                          'RAMSTK Program database.'
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_delete(self, node_id):
        """
        Request to delete an RAMSTKHazardAnalysis table record.

        :param str node_id: the node (Hazard) ID whose hazard_analysis is to be
                            deleted.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedHazardAnalysis')

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTKHazardAnalysis table record.

        :param str node_id: the node ID to update.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedHazardAnalysis')

    def request_do_update_all(self, **kwargs):
        """
        Request to update all records in the RAMSTKHazardAnalysis table.

        :param int node_id: the ID of the Hardware item to update the HazOps
                            for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_all(**kwargs)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_select_children(self, node_id):
        """
        Request the child nodes of the selected Hardware ID.

        :param int node_id: the PyPubSub Tree() ID of the Hardware item to
                            select the HazOps for.
        :return: a list of the immediate child nodes of the passed Hardware ID.
        :rtype: list
        """
        return self._dtm_data_model.do_select_children(node_id)

    def request_do_calculate(self, node_id, **kwargs):
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
        return self._dtm_data_model.do_calculate(node_id, **kwargs)

    def request_do_calculate_all(self, **kwargs):
        """
        Request to calculate all HazOps.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_calculate_all(**kwargs)
