# -*- coding: utf-8 -*-
#
#       ramstk.modules.stakeholder.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Controller."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
from . import dtmStakeholder


class StakeholderDataController(RAMSTKDataController):
    """
    Provide an interface between the Stakeholder data model and an RAMSTK View.

    A single Stakeholder controller can manage one or more Stakeholder data
    models.  The attributes of a Stakeholder data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a Stakeholder data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the Stakeholder
                    Data Model.
        :type dao: :class:`ramstk.dao.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmStakeholder(dao, **kwargs),
            ramstk_module='stakeholder',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.request_do_select_all, 'selected_revision')
        pub.subscribe(self.request_do_calculate,
                      'request_calculate_stakeholder')
        pub.subscribe(self.request_do_calculate_all,
                      'request_calculate_all_stakeholders')
        pub.subscribe(self.request_do_delete, 'request_delete_stakeholder')
        pub.subscribe(self.request_do_insert, 'request_insert_stakeholder')
        pub.subscribe(self.request_do_update, 'request_update_stakeholder')
        pub.subscribe(self.request_do_update_all,
                      'request_update_all_stakeholders')
        pub.subscribe(self.request_set_attributes, 'editing_stakeholder')

    def request_do_calculate(self, node_id, **kwargs):
        """
        Request to calculate the Stakeholder input.

        :param int node_id: the PyPubSub Tree() ID of the Stakeholder to
                            calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_calculate(node_id, **kwargs)

    def request_do_calculate_all(self, **kwargs):
        """
        Request to calculate all Stakeholder inputs.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtm_data_model.do_calculate_all(**kwargs)

    def request_do_delete(self, node_id):
        """
        Request to delete an RAMSTKStakeholder table record.

        :param int stakeholder_id: the Stakeholder ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_insert(self, revision_id):
        """
        Request to add an RAMSTKStakeholder table record.

        :param int revision_id: the ID of the Revision to add the new
                                Stakeholder input to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=revision_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTKStakeholder table record.

        :param int node_id: the ID of the Stakeholder to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_update_all(self):
        """
        Request to update all records in the RAMSTKStakeholder table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update_all()

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)
