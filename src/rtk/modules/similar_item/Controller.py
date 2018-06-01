# -*- coding: utf-8 -*-
#
#       rtk.modules.similar_item.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""SimilarItem Package Data Controller Module."""

from pubsub import pub

# Import other RTK modules.
from rtk.datamodels import RTKDataController
from . import dtmSimilarItem


class SimilarItemDataController(RTKDataController):
    """
    Provide an interface between SimilarItem data models and RTK views.

    A single SimilarItem data controller can manage one or more SimilarItem
    data models.
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a SimilarItem data controller instance.

        :param dao: the data access object used to communicate with the
                    connected RTK Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
        :param configuration: the RTK configuration instance.
        :type configuration: :py:class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmSimilarItem(dao),
            rtk_module='similar_item',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_insert(self, revision_id, **kwargs):
        """
        Request to add an RTKSimilarItem table record.

        :param int revision_id: the Revision ID this SimilarItem will be
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
                pub.sendMessage('insertedSimilarItem')
        else:
            _msg = _msg + '  Failed to add a new SimilarItem to the ' \
                          'RTK Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, hardware_id):
        """
        Request to delete an RTKSimilarItem table record.

        :param int hardware_id: the Hardware ID whose similar_item is to be
                                deleted.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.delete(hardware_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedSimilarItem')

    def request_update(self, hardware_id):
        """
        Request to update an RTKSimilarItem table record.

        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update(hardware_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedSimilarItem')

    def request_update_all(self):
        """
        Request to update all records in the RTKSimilarItem table.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_select_children(self, hardware_id):
        """
        Request the child nodes of the selected Hardware ID.

        :param int hardware_id: the ID of the Hardware item to select the
                                child nodes for.
        :return: a list of the immediate child nodes of the passed Hardware ID.
        :rtype: list
        """
        return self._dtm_data_model.select_children(hardware_id)

    def request_calculate(self, node_id, hazard_rate=0.0):
        """
        Request the similar_item calculations be performed.

        :param int node_id: the Node (Hardware) ID of the hardware item whose
                            goal is to be allocated.
        :param float hazard_rate: the current hazard rate of the hardware item
                                  to be calculated.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.calculate(node_id, hazard_rate)
