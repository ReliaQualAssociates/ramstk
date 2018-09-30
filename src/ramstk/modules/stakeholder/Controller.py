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
            model=dtmStakeholder(dao),
            ramstk_module='stakeholder',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_insert(self, **kwargs):
        """
        Request to add an RAMSTKStakeholder table record.

        :param int revision_id: the ID of the Revision to add the new
                                Stakeholder to.
        :param int parent_id: the ID of the parent Stakeholder to add the new
                              Stakeholder to.
        :keyword bool sibling: indicates whether or not to insert a sibling
                               (default) or child (derived) Stakeholder.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _revision_id = kwargs['revision_id']
        _error_code, _msg = self._dtm_data_model.do_insert(
            revision_id=_revision_id)

        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)

            if not self._test:
                pub.sendMessage(
                    'insertedStakeholder',
                    stakeholder_id=self._dtm_data_model.last_id)
        else:
            _msg = _msg + '  Failed to add a new Stakeholder to the RAMSTK ' \
                'Program database.'

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_delete(self, node_id):
        """
        Request to delete an RAMSTKStakeholder table record.

        :param int stakeholder_id: the Stakeholder ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'deletedStakeholder')

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTKStakeholder table record.

        :param int stakeholder_id: the ID of the stakeholder to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      'savedStakeholder')

    def request_do_update_all(self):
        """
        Request to update all records in the RAMSTKStakeholder table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = self._dtm_data_model.do_update_all()

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

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
