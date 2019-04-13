# -*- coding: utf-8 -*-
#
#       ramstk.modules.pof.Controller.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Physics of Failure Package Data Controller."""

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataController
from . import dtmPoF


class PhysicsOfFailureDataController(RAMSTKDataController):
    """
    Provide an interface between the PoF data model and an RAMSTK view model.

    A single PoF controller can manage one or more PoF data models.
    The attributes of a PoF data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a PoF data controller instance.

        :param dao: the RAMSTK Program DAO instance to pass to the PoF Data
                    Model.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        RAMSTKDataController.__init__(
            self,
            configuration,
            model=dtmPoF(dao, **kwargs),
            ramstk_module='PoF',
            **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_select_all(self, attributes):
        """
        Retrieve the treelib Tree() from the Requirement Data Model.

        :return: tree; the treelib Tree() of RAMSTKRequirement models in the
                 Requirement tree.
        :rtype: :class:`treelib.Tree`
        """
        return self._dtm_data_model.do_select_all(
            hardware_id=attributes['hardware_id'])

    def request_do_insert(self, **kwargs):
        """
        Request to add a PoF table record.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _entity_id = kwargs['entity_id']
        _parent_id = kwargs['parent_id']
        _level = kwargs['level']

        _error_code, _msg = self._dtm_data_model.do_insert(
            entity_id=_entity_id, parent_id=_parent_id, level=_level)

        if _error_code == 0:
            self._configuration.RAMSTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + '  Failed to add a new PoF item to the RAMSTK ' \
                'Program database.'
            self._configuration.RAMSTK_DEBUG_LOG.error(_msg)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_delete(self, node_id):
        """
        Request entity and it's children be deleted from the PoF.

        :param str node_id: the Mode, Mechanism, Cause, Controle, or Action ID
                            to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_delete(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_update(self, node_id):
        """
        Request to update an RAMSTKOpLoad, RAMSTKOpStress, or RAMSTKTestMethod.

        :param int node_id: the PyPubSub Tree() ID of the entity to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update(node_id)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)

    def request_do_update_all(self, **kwargs):
        """
        Request all PoF entities be saved to the RAMSTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = self._dtm_data_model.do_update_all(**kwargs)

        return RAMSTKDataController.do_handle_results(self, _error_code, _msg,
                                                      None)
