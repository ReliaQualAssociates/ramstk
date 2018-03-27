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
from rtk.hardware import dtmHardwareBoM
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
        self._dtm_hardware_bom = dtmHardwareBoM(dao)

        # Initialize public dictionary attributes.

        # Initialize public list attributes.
        self.lst_availability = []
        self.lst_hazard_rates = []
        self.lst_mtbf = []
        self.lst_name = []
        self.lst_reliability = []

        # Initialize public scalar attributes.
        self.system_hazard_rate = 0.0

    def request_select(self, node_id):
        """
        Request the RTK Program database record associated with Node ID.

        :param int node_id: the Hardware ID to retrieve from the Tree.
        :return: the RTK Program database record requested.
        """
        return RTKDataController.request_select(self, node_id)

    def request_select_all(self, parent_id, **kwargs):
        """
        Retrieve the treelib Tree() from the Data Model.

        :param int parent_id: the Revision ID to select the entities for.
        :return: tree; the treelib Tree() of RTKRequirement models in the
                 Requirement tree.
        :rtype: dict
        """
        self.lst_availability = []
        self.lst_hazard_rates = []
        self.lst_mtbf = []
        self.lst_name = []
        self.lst_reliability = []

        # Select the Hardware BoM tree and retrieve the system hazard rate.
        _tree = self._dtm_hardware_bom.select_all(parent_id, **kwargs)
        self.system_hazard_rate = _tree.children(
            _tree.root)[0].data['hazard_rate_logistics']

        # Grab the reliability attributes for the selected Hardware item and
        # add it's reliability attributes to the various lists used in the
        # calculation of allocations.
        _reliability = self._dtm_hardware_bom.select(parent_id, 'reliability')
        self.lst_availability.append(_reliability.availability_logistics)
        self.lst_hazard_rates.append(_reliability.hazard_rate_logistics)
        self.lst_mtbf.append(_reliability.mtbf_logistics)
        self.lst_reliability.append(_reliability.reliability_logistics)

        # Add the reliability metrics of each child assembly of the selected
        # Hardware item.
        for _node in self._dtm_hardware_bom.tree.children(parent_id):
            self.lst_name.append(_node.data['name'])
            self.lst_availability.append(_node.data['availability_logistics'])
            self.lst_hazard_rates.append(_node.data['hazard_rate_logistics'])
            self.lst_mtbf.append(_node.data['mtbf_logistics'])
            self.lst_reliability.append(_node.data['reliability_logistics'])

        # Select and return the Allocation treelib Tree().
        return RTKDataController.request_select_all(self, parent_id, **kwargs)

    def request_children(self, hardware_id):
        """
        Request the children (child tree) of the passed Hardware ID.

        :param int hardware_id: the Hardware ID to select the children for.
        :return: a treelib Tree() structure of the children (child tree).
        :rtype: :class:`treelib.Tree`
        """
        return self._dtm_data_model.tree.subtree(hardware_id)

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
            revision_id=revision_id,
            hardware_id=_hardware_id,
            parent_id=_parent_id)

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

    def request_calculate(self, node_id):
        """
        Request the allocation calculations be performed.

        :param int node_id: the Node (Hardware) ID of the hardware item whose
                            goal is to be allocated.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        _return = self._dtm_data_model.calculate(node_id,
                                                 self.lst_hazard_rates)

        if not _return:
            _return = RTKDataController.do_handle_results(
                self, 0, '', 'calculatedAllocation')

        return _return
