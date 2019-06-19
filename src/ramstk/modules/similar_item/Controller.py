# -*- coding: utf-8 -*-
#
#       ramstk.modules.similar_item.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""SimilarItem Package Data Controller Module."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.modules import RAMSTKDataController

# RAMSTK Local Imports
from . import dtmSimilarItem


class SimilarItemDataController(RAMSTKDataController):
    """
    Provide an interface between SimilarItem data models and RAMSTK views.

    A single SimilarItem data controller can manage one or more SimilarItem
    data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a SimilarItem data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RAMSTK Program database.
        :type dao: :py:class:`ramstk.dao.DAO.DAO`
        :param configuration: the RAMSTK configuration instance.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmSimilarItem(dao, **kwargs),
            ramstk_module='similar_item',
            **kwargs,
        )

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._request_do_calculate,
            'request_calculate_similar_item',
        )
        pub.subscribe(self._request_do_insert, 'request_insert_similar_item')
        pub.subscribe(self.request_do_delete, 'request_delete_similar_item')
        pub.subscribe(self.request_do_roll_up, 'request_roll_up_similar_item')
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(self._request_do_select_children, 'selected_hardware')
        pub.subscribe(self.request_do_update, 'request_update_similar_item')
        pub.subscribe(
            self.request_do_update_all,
            'request_update_all_similar_items',
        )
        pub.subscribe(self.request_set_attributes, 'wvw_editing_similar_item')

    def _request_do_calculate(self, node_id, hazard_rate):
        """
        Request to calculate the record.

        :param int node_id: the PyPubSub Tree() ID of the Stakeholder to
                            calculate.
        :param int hazard_rate: the current hazard rate of the Similar Item
        node that is being calculated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_calculate(
            node_id=node_id,
            hazard_rate=hazard_rate,
        )

    def _request_do_insert(self, revision_id, hardware_id, parent_id):
        """
        Request to add an RAMSTKSimilarItem table record.

        :param int revision_id: the Revision ID this Similar Item record will
        be associated with.
        :param int hardware_id: the Hardware ID this Similar Item record will
        be associated with.
        :param int parent_id: the Hardware ID of the parent hardware item.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=revision_id,
            hardware_id=hardware_id,
            parent_id=parent_id,
        )

        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + (
                '  Failed to add a new Similar Item to the RAMSTK '
                'Program database.'
            )
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)

        return RAMSTKDataController.do_handle_results(
            self,
            _error_code,
            _msg,
            None,
        )

    def _request_do_select_children(self, attributes):
        """
        Load the children for the selected Hardware item.

        :param dict attributes: the key:value pairs of the Similar Item
            attributes.
        :return: children; a list of child nodes from the Similar Item tree.
        :rtype: list
        """
        return self._dtm_data_model.do_select_children(
            node_id=attributes['hardware_id'],
        )

    def request_do_roll_up(self, node_id):
        """
        Request to roll-up change descriptions of child nodes.

        :param int node_id: the Node ID of the parent to roll-up descriptions
        to.
        :return: None
        :rtype: None
        """
        return self._dtm_data_model.do_roll_up(node_id)
