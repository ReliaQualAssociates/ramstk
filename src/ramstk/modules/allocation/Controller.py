# -*- coding: utf-8 -*-
#
#       ramstk.modules.allocation.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Allocation Package Data Controller Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.modules import RAMSTKDataController
from ramstk.modules.hardware import dtmHardwareBoM

# RAMSTK Local Imports
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
        :type dao: :py:class:`ramstk.dao.DAO.DAO`
        :param configuration: the RAMSTK configuration instance.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmAllocation(dao, **kwargs),
            ramstk_module='allocation',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtm_hardware_bom = dtmHardwareBoM(dao, **kwargs)

        # Initialize public dictionary attributes.
        self.dic_hardware_data = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.system_hazard_rate = 0.0

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._request_do_calculate,
            "request_calculate_allocation",
        )
        pub.subscribe(
            self.request_do_calculate_all,
            "request_calculate_all_allocations",
        )
        pub.subscribe(self.request_do_delete, "request_delete_allocation")
        pub.subscribe(self.request_do_delete, 'deleted_hardware')
        pub.subscribe(self.request_do_insert, "request_insert_allocation")
        pub.subscribe(self.request_do_insert, 'inserted_hardware')
        pub.subscribe(self._request_do_select_all, "selected_hardware")
        pub.subscribe(self.request_do_update, "request_update_allocation")
        pub.subscribe(
            self.request_do_update_all,
            "request_update_all_allocations",
        )

    def _request_do_calculate(self, node_id, **kwargs):
        """
        Request the allocation calculations be performed.

        :param int node_id: the treelib Tree() ID of the Hardware item whose
                            goal is to be allocated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _lst_hazard_rates = [self.system_hazard_rate]
        for _child in self._dtm_hardware_bom.tree.children(node_id):
            _lst_hazard_rates.append(_child.data['hazard_rate_logistics'])

        return self._dtm_data_model.do_calculate(
            node_id,
            hazard_rates=_lst_hazard_rates,
            **kwargs,
        )

    def _request_do_select_all(self, attributes):
        """
        Retrieve the treelib Tree() from the Allocation Data Model.

        :return: None
        :rtype: None
        """
        # Select the Hardware BoM tree and retrieve the system hazard rate.
        self._dtm_hardware_bom.do_select_all(
            revision_id=attributes['revision_id'], )
        self.system_hazard_rate = self._dtm_hardware_bom.tree.children(
            self._dtm_hardware_bom.tree.root,
        )[0].data['hazard_rate_logistics']

        for _node in self._dtm_hardware_bom.tree.all_nodes()[1:]:
            self.dic_hardware_data[_node.identifier] = [
                _node.data['name'],
                _node.data['availability_logistics'],
                _node.data['hazard_rate_logistics'],
                _node.data['mtbf_logistics'],
                _node.data['reliability_logistics'],
            ]

        return RAMSTKDataController.request_do_select_all(self, attributes)

    def request_do_select_children(self, node_id):
        """
        Request the children (child tree) of the passed Hardware ID.

        :param str node_id: the PyPubSub Tree() ID of the Hardware item to
                            select the children for.
        :return: a treelib Tree() structure of the children (child tree).
        :rtype: :class:`treelib.Tree`
        """
        return self._dtm_data_model.do_select_children(node_id)
