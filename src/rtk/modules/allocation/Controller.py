# -*- coding: utf-8 -*-
#
#       rtk.modules.allocation.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Allocation Package Data Controller Module."""

from pubsub import pub

# Import other RAMSTK modules.
from rtk.modules import RAMSTKDataController
from rtk.modules.hardware import dtmHardwareBoM
from . import dtmAllocation


class AllocationDataController(RAMSTKDataController):
    """
    Provide an interface between Allocation data models and RAMSTK views.

    A single Allocation data controller can manage one or more Allocation data
    models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Allocation data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RAMSTK Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        :param configuration: the RAMSTK configuration instance.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
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
        self.dic_hardware_data = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.system_hazard_rate = 0.0

        pub.subscribe(self.insert_hardware_listener, 'insertedHardware')
        pub.subscribe(self.request_do_delete, 'deletedHardware')

    def insert_hardware_listener(self, revision_id, hardware_id, parent_id):
        """
        Listen for 'insertedHardware' message and call request_do_insert.

        This method is needed because PyPubSub can not pass **kwargs.
        """
        return self.request_do_insert(
            revision_id=revision_id,
            hardware_id=hardware_id,
            parent_id=parent_id)

    def request_do_calculate(self, node_id, **kwargs):
        """
        Request the allocation calculations be performed.

        :param int node_id: the PyPubSub Tree() ID of the Hardware item whose
                            goal is to be allocated.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        _lst_hazard_rates = [self.system_hazard_rate]
        for _child in self._dtm_hardware_bom.tree.children(node_id):
            _lst_hazard_rates.append(_child.data['hazard_rate_logistics'])

        _return = self._dtm_data_model.do_calculate(
            node_id, hazard_rates=_lst_hazard_rates, **kwargs)

        if not _return:
            _return = RAMSTKDataController.do_handle_results(
                self, 0, '', 'calculatedAllocation')

        return _return

    def request_do_calculate_all(self, **kwargs):
        """
        Request to calculate all Allocations.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_calculate_all(**kwargs)

    def request_do_delete(self, node_id):
        """
        Request to delete an RAMSTKAllocation table record.

        :param int node_id: the PyPubSub Tree() ID of the Allocation to be
                            deleted.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedAllocation')

    def request_do_insert(self, **kwargs):
        """
        Request to add an RAMSTKAllocation table record.

        :param int revision_id: the Revision ID this Allocation will be
                                associated with.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _revision_id = kwargs['revision_id']
        _hardware_id = kwargs['hardware_id']
        _parent_id = kwargs['parent_id']
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=_revision_id,
            hardware_id=_hardware_id,
            parent_id=_parent_id)

        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('insertedAllocation')
        else:
            _msg = _msg + ('  Failed to add a new Allocation to the RAMSTK '
                           'Program database.')
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_select_all(self, **kwargs):
        """
        Retrieve the treelib Tree() from the Data Model.

        :return: tree; the treelib Tree() of RAMSTKAllocation models in the
                 Allocation tree.
        :rtype: dict
        """
        _revision_id = kwargs['revision_id']

        # Select the Hardware BoM tree and retrieve the system hazard rate.
        _tree = self._dtm_hardware_bom.do_select_all(**kwargs)
        self.system_hazard_rate = _tree.children(
            _tree.root)[0].data['hazard_rate_logistics']

        for _node in _tree.all_nodes()[1:]:
            self.dic_hardware_data[_node.identifier] = [
                _node.data['name'], _node.data['availability_logistics'],
                _node.data['hazard_rate_logistics'],
                _node.data['mtbf_logistics'],
                _node.data['reliability_logistics']
            ]

        # Select and return the Allocation treelib Tree().
        return RAMSTKDataController.request_do_select_all(self, **kwargs)

    def request_do_select_children(self, node_id):
        """
        Request the children (child tree) of the passed Hardware ID.

        :param str node_id: the PyPubSub Tree() ID of the Hardware item to
                            select the children for.
        :return: a treelib Tree() structure of the children (child tree).
        :rtype: :class:`treelib.Tree`
        """
        return self._dtm_data_model.do_select_children(node_id)

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTKAllocation table record.

        :param str node_id: the PyPubSub Tree() ID of the Allocation to update.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedAllocation')

    def request_do_update_all(self, **kwargs):
        """
        Request to update all records in the RAMSTKAllocation table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_all(**kwargs)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)
