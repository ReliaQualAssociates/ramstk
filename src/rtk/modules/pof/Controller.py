# -*- coding: utf-8 -*-
#
#       rtk.modules.pof.Controller.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Physics of Failure Package Data Controller."""

# Import other RTK modules.
from rtk.modules import RTKDataController
from . import dtmPoF


class PhysicsOfFailureDataController(RTKDataController):
    """
    Provide an interface between the PoF data model and an RTK view model.

    A single PoF controller can manage one or more PoF data models.
    The attributes of a PoF data controller are:
    """

    def __init__(self, dao, configuration, **kwargs):
        """
        Initialize a PoF data controller instance.

        :param dao: the RTK Program DAO instance to pass to the PoF Data
                    Model.
        :type dao: :class:`rtk.dao.DAO.DAO`
        :param configuration: the Configuration instance associated with the
                              current instance of the RTK application.
        :type configuration: :class:`rtk.Configuration.Configuration`
        """
        RTKDataController.__init__(
            self, configuration, model=dtmPoF(dao), rtk_module='PoF', **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def request_do_select_all(self, parent_id, **kwargs):  # pylint: disable=unused-argument
        """
        Load the entire PoF for a failure Mechanism.

        :param int parent_id: the Mechanism ID to retrieve the PoF and build
                              trees for.
        :return: tree; the PoF treelib Tree().
        :rtype: :class:`treelib.Tree`
        """
        return self._dtm_data_model.do_select_all(parent_id=parent_id)

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
            self._configuration.RTK_USER_LOG.info(_msg)
        else:
            _msg = _msg + '  Failed to add a new PoF item to the RTK ' \
                'Program database.'
            self._configuration.RTK_DEBUG_LOG.error(_msg)

        return RTKDataController.do_handle_results(self, _error_code, _msg,
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

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)

    def request_do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Request all (D)FME(C)A entities be saved to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _error_code, _msg = self._dtm_data_model.do_update_all()

        return RTKDataController.do_handle_results(self, _error_code, _msg,
                                                   None)
