# -*- coding: utf-8 -*-
#
#       ramstk.modules.similar_item.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""SimilarItem Package Data Controller Module."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
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
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

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
        Request the Similar Item calculations be performed.

        :param int node_id: the PyPubSub Tree()  ID of the Similar Item to be
                            calculated.
        :param float hazard_rate: the current hazard rate of the hardware item
                                  to be calculated.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        _hazard_rate = kwargs['hazard_rate']

        return self._dtm_data_model.do_calculate(
            node_id, hazard_rate=_hazard_rate)

    def request_do_calculate_all(self, **kwargs):
        """
        Request to calculate all Similar Items.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_calculate_all(**kwargs)

    def request_do_delete(self, node_id):
        """
        Request to delete an RAMSTKSimilarItem table record.

        :param int node_id: the PyPubSub Tree() ID of the Similar Item to be
                            deleted.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'deletedSimilarItem')

    def request_do_insert(self, **kwargs):
        """
        Request to add an RAMSTKSimilarItem table record.

        :param int revision_id: the Revision ID this SimilarItem will be
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
                pub.sendMessage('insertedSimilarItem')
        else:
            _msg = _msg + ('  Failed to add a new Similar Item to the RAMSTK '
                           'Program database.')
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_roll_up(self, node_id):
        """
        Request to roll-up change descriptions of child nodes.

        :param int node_id: the Node ID of the parent to roll-up descriptions
                            to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_roll_up(node_id)

    def request_do_select_children(self, node_id):
        """
        Request the child nodes of the selected Hardware ID.

        :param int node_id: the PyPubSub Tree() ID of the Similar Item to
                            select the child nodes for.
        :return: a list of the immediate child nodes of the passed Hardware ID.
        :rtype: list
        """
        return self._dtm_data_model.do_select_children(node_id)

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTKSimilarItem table record.

        :param int node_id: the PyPubSub Tree() ID of the Similar Item to be
                            saved.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'savedSimilarItem')

    def request_do_update_all(self, **kwargs):
        """
        Request to update all records in the RAMSTKSimilarItem table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_all(**kwargs)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)
