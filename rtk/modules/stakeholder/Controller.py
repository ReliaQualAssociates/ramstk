# -*- coding: utf-8 -*-
#
#       rtk.stakeholder.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Controller."""

from pubsub import pub

# Import other RTK modules.
from rtk.datamodels import RTKDataController
from . import dtmStakeholder


class StakeholderDataController(RTKDataController):
    """
    Provide an interface between the Stakeholder data model and an RTK View.

    A single Stakeholder controller can manage one or more Stakeholder data
    models.  The attributes of a Stakeholder data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Stakeholder data controller instance.

        :param dao: the RTK Program DAO instance to pass to the Stakeholder
                    Data Model.
        :type dao: :class:`rtk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self,
            configuration,
            model=dtmStakeholder(dao),
            rtk_module='stakeholder',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_insert(self, revision_id):
        """
        Request to add an RTKStakeholder table record.

        :param int revision_id: the ID of the Revision to add the new
                                Stakeholder to.
        :param int parent_id: the ID of the parent Stakeholder to add the new
                              Stakeholder to.
        :keyword bool sibling: indicates whether or not to insert a sibling
                               (default) or child (derived) Stakeholder.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.insert(
            revision_id=revision_id)

        if _error_code == 0:
            self._configuration.RTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage(
                    'insertedStakeholder',
                    stakeholder_id=self._dtm_data_model.last_id)
        else:
            _msg = _msg + '  Failed to add a new Stakeholder to the RTK ' \
                'Program database.'

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_delete(self, stakeholder_id):
        """
        Request to delete an RTKStakeholder table record.

        :param int stakeholder_id: the Stakeholder ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.delete(stakeholder_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'deletedStakeholder')

    def request_update(self, stakeholder_id):
        """
        Request to update an RTKStakeholder table record.

        :param int stakeholder_id: the ID of the stakeholder to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.update(stakeholder_id)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   'savedStakeholder')

    def request_update_all(self):
        """
        Request to update all records in the RTKStakeholder table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_calculate_weight(self, stakeholder_id):
        """
        Request to calculate the Stakeholder input.

        :param int stakeholder_id: the Stakholder ID to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.calculate_weight(stakeholder_id)
