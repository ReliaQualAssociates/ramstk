# -*- coding: utf-8 -*-
#
#       ramstk.modules.hazops.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""HazardAnalysis Package Data Controller Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.modules import RAMSTKDataController

# RAMSTK Local Imports
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
        :type dao: :py:class:`ramstk.dao.DAO.DAO`
        :param configuration: the RAMSTK configuration instance.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmHazardAnalysis(dao, **kwargs),
            ramstk_module='hazard_analysis',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.request_do_calculate, 'request_calculate_hazop')
        pub.subscribe(
            self.request_do_calculate_all,
            'request_calculcate_all_hazops',
        )
        pub.subscribe(self.request_do_delete, 'request_delete_hazop')
        pub.subscribe(self._request_do_insert, 'request_insert_hazop')
        pub.subscribe(self.request_do_select_all, 'selected_hardware')
        pub.subscribe(self.request_do_update, 'request_update_hazop')
        pub.subscribe(self.request_do_update_all, 'request_update_all_hazops')
        pub.subscribe(self.request_set_attributes, 'wvw_editing_hazop')

    def _request_do_insert(self, revision_id, parent_id):
        """
        Request to add an RAMSTKHazardAnalysis table record.

        :param int revision_id: the Revision ID the HazOp is associated with.
        :param int parent_id: the Hardware ID the HazOp belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=revision_id, hardware_id=parent_id,
        )

        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage('inserted_hazop', module_id=parent_id)
        else:
            _msg = _msg + '  Failed to add a new Hazard Analysis to the ' \
                          'RAMSTK Program database.'
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)

        return RAMSTKDataController.do_handle_results(
            self, _error_code, _msg,
            None,
        )

    def request_do_select_children(self, node_id):
        """
        Request the child nodes of the selected Hardware ID.

        :param int node_id: the PyPubSub Tree() ID of the Hardware item to
                            select the HazOps for.
        :return: a list of the immediate child nodes of the passed Hardware ID.
        :rtype: list
        """
        return self._dtm_data_model.do_select_children(node_id)
