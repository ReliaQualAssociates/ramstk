# -*- coding: utf-8 -*-
#
#       rtk.modules.allocation.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Allocation Package Data Controller Module."""

from pubsub import pub

# Import other RTK modules.
from rtk.datamodels import RTKDataController
from . import dtmAllocation


class AllocationDataController(RTKDataController):
    """
    Provide an interface between Allocation data models and RTK views.

    A single Allocation data controller can manage one or more Allocation data
    models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Allocation data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RTK Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        :param configuration: the RTK configuration instance.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmAllocation(dao),
            rtk_module='allocation',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_insert(self, revision_id, **kwargs):
        """
        Request to add an RTKAllocation table record.

        :param int revision_id: the Revision ID this Allocation will be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _hardware_id = kwargs['hardware_id']
        _parent_id = kwargs['parent_id']
        _error_code, _msg = self._dtm_data_model.insert(
            revision_id=revision_id, hardware_id=_hardware_id, parent_id=_parent_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('insertedAllocation')
        else:
            _msg = _msg + '  Failed to add a new Allocation to the ' \
                          'RTK Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, hardware_id):
        """
        Request to delete an RTKAllocation table record.

        :param int hardware_id: the Hardware ID whose allocation is to be
                                deleted.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.delete(hardware_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedAllocation')

    def request_update(self, definition_id):
        """
        Request to update an RTKAllocation table record.

        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update(definition_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedAllocation')

    def request_update_all(self):
        """
        Request to update all records in the RTKAllocation table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_calculate(self, node_id, hazard_rates=None):
        """
        Request the allocation calculations be performed.

        :param int node_id: the Node (Hardware) ID of the hardware item whose
                            goal is to be allocated.
        :param list hazard_rates: the hazard rates of the parent hardware item
                                  to be allocated and each of the child items
                                  (only needed for ARINC apportionment).  Index
                                  0 is the parent hazard rate.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.calculate(node_id, hazard_rates)
