# -*- coding: utf-8 -*-
#
#       ramstk.controllers.fmea.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Package Data Model."""

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKAction, RAMSTKCause, RAMSTKControl, RAMSTKMechanism, RAMSTKMode
)


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the FMEA data manager.

    This class manages the fmea data from the RAMSTKFMEA and
    RAMSTKHazardAnalysis data models.
    """

    _tag = 'fmea'
    _root = 0

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize a FMEA data manager instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataManager.__init__(self, dao, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        try:
            self._is_functional = kwargs['functional']
        except KeyError:
            self._is_functional = False
        self._parent_id = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'succeed_select_hardware')
        pub.subscribe(self._do_delete, 'request_delete_fmea')
        pub.subscribe(self._do_insert_action, 'request_insert_fmea_action')
        pub.subscribe(self._do_insert_cause, 'request_insert_fmea_cause')
        pub.subscribe(self._do_insert_control, 'request_insert_fmea_control')
        pub.subscribe(self._do_insert_mechanism,
                      'request_insert_fmea_mechanism')
        pub.subscribe(self._do_insert_mode, 'request_insert_fmea_mode')
        pub.subscribe(self.do_update, 'request_update_fmea')
        pub.subscribe(self.do_get_attributes, 'request_get_mode_attributes')
        pub.subscribe(self.do_get_attributes,
                      'request_get_mechanism_attributes')
        pub.subscribe(self.do_get_attributes, 'request_get_cause_attributes')
        pub.subscribe(self.do_get_attributes, 'request_get_control_attributes')
        pub.subscribe(self.do_get_attributes, 'request_get_action_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_fmea_tree')
        pub.subscribe(self.do_set_attributes, 'request_set_fmea_attributes')

    def _add_cause_node(self, cause, parent_id):
        """
        Add a node to the treelib Tree() to hold a failure cause.

        This is a helper method to allow causes to be children of either a
        failure mode (functional FMEA) or a failure mechanism (hardware FMEA).

        :param cause: an instance of RAMSTKCause.
        :type cause: :class:`ramstk.models.programdb.RAMSTKCause`
        :parem str parent_id: the parent node ID the causes are associated
            with.
        :return: None
        :rtype: None
        """
        _data_package = {'cause': cause}

        _identifier = '{0:s}.{1:d}'.format(parent_id, cause.cause_id)

        self.tree.create_node(tag=_identifier,
                              identifier=_identifier,
                              parent=parent_id,
                              data=_data_package)

        self._do_select_all_control(cause.cause_id, _identifier)
        self._do_select_all_action(cause.cause_id, _identifier)

    def _add_mode_node(self, mode):
        """
        Add a node to the treelib Tree() to hold a failure mode.

        This is a helper method to allow modes to be children of either a
        function (functional FMEA) or a hardware item (hardware FMEA).

        :param mode: an instance of RAMSTKMode.
        :type cause: :class:`ramstk.models.programdb.RAMSTKMode`
        :parem str parent_id: the parent node ID the causes are associated
            with.
        :return: None
        :rtype: None
        """
        _data_package = {'mode': mode}

        self.tree.create_node(tag=str(mode.mode_id),
                              identifier=str(mode.mode_id),
                              parent=self._root,
                              data=_data_package)

    def _do_delete(self, node_id):
        """
        Remove a FMEA element.

        :param int node_id: the node (FMEA action) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            (_error_code,
             _error_msg) = RAMSTKDataManager.do_delete(self, node_id, _table)

            if _error_code == 0:
                self.tree.remove_node(node_id)

                pub.sendMessage('succeed_delete_fmea', node_id=node_id)
            else:
                print(_error_code, _error_msg)
        except AttributeError:
            _error_msg = ("Attempted to delete non-existent FMEA element ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_fmea', error_msg=_error_msg)

    def _do_insert_action(self, cause_id, parent_id):
        """
        Add a new action to FMEA cause ID.

        :param int fmea_id: the FMEA cause ID to associate the new action with.
        :parem str parent_id: the parent node ID the control is associated
            with.
        :return: None
        :rtype: None
        """
        try:
            _action = RAMSTKAction(cause_id=cause_id,
                                   action_recommended=b'Recommended Action')
            _error_code, _msg = self.dao.db_add([_action])

            _data_package = {'action': _action}

            _identifier = '{0:s}.{1:d}.a'.format(parent_id, _action.action_id)
            self.tree.create_node(tag=_action.action_recommended,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_action', node_id=_identifier)
        except (DataAccessError, NodeIDAbsentError) as _error:
            _error_msg = ('Attempting to add an action to unknown failure '
                          'cause ID {0:d}.'.format(cause_id))
            pub.sendMessage("fail_insert_action", error_msg=_error_msg)

    def _do_insert_cause(self, mode_id, mechanism_id, parent_id):
        """
        Add a new failure cause to FMEA mechanism ID.

        :param int mode_id: the FMEA mode ID to associate the new cause with.
        :param int mechanism_id: the FMEA mechanism ID to associate the new
            cause with.
        :parem str parent_id: the parent node ID the cause is associated with.
        :return: None
        :rtype: None
        """
        try:
            _cause = RAMSTKCause(mode_id=mode_id,
                                 mechanism_id=mechanism_id,
                                 description='New Failure Cause')
            _error_code, _msg = self.dao.db_add([_cause])

            _identifier = '{0:s}.{1:d}'.format(parent_id, _cause.cause_id)

            _data_package = {'cause': _cause}
            self.tree.create_node(tag=_cause.description,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_cause', node_id=_identifier)
        except (DataAccessError, NodeIDAbsentError) as _error:
            _error_msg = (
                'Attempting to add a failure cause to unknown '
                'failure mode ID {0:d} or mechanism ID {1:d}.'.format(
                    mode_id, mechanism_id))
            pub.sendMessage("fail_insert_cause", error_msg=_error_msg)

    def _do_insert_control(self, cause_id, parent_id):
        """
        Add a new control to FMEA cause ID.

        :param int cause_id: the FMEA cause ID to associate the new control
            with.
        :parem str parent_id: the parent node ID the control is associated
            with.
        :return: None
        :rtype: None
        """
        try:
            _control = RAMSTKControl(cause_id=cause_id,
                                     description='New Control')
            _error_code, _msg = self.dao.db_add([_control])

            _data_package = {'control': _control}

            _identifier = '{0:s}.{1:d}.c'.format(parent_id,
                                                 _control.control_id)
            self.tree.create_node(tag=_control.description,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_control', node_id=_identifier)
        except (DataAccessError, NodeIDAbsentError) as _error:
            _error_msg = ('Attempting to add a control to unknown failure '
                          'cause ID {0:d}.'.format(cause_id))
            pub.sendMessage("fail_insert_control", error_msg=_error_msg)

    def _do_insert_mechanism(self, mode_id):
        """
        Add a new failure mechanism to FMEA mode ID.

        :param str mode_id: the FMEA mode ID to associate the new mechanism
            with.
        :return: None
        :rtype: None
        """
        try:
            _mechanism = RAMSTKMechanism(mode_id=mode_id,
                                         description='New Failure Mechanism')
            _error_code, _msg = self.dao.db_add([_mechanism])

            _identifier = '{0:s}.{1:d}'.format(mode_id,
                                               _mechanism.mechanism_id)

            _data_package = {'mechanism': _mechanism}
            self.tree.create_node(tag=_mechanism.description,
                                  identifier=_identifier,
                                  parent=mode_id,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_mechanism', node_id=_identifier)
        except (DataAccessError, NodeIDAbsentError) as _error:
            _error_msg = ('Attempting to add a failure mechanism to unknown '
                          'failure mode ID {0:s}.'.format(mode_id))
            pub.sendMessage("fail_insert_mechanism", error_msg=_error_msg)

    def _do_insert_mode(self):
        """
        Add a new failure mode.

        :return: None
        :rtype: None
        """
        try:
            _mode = RAMSTKMode(function_id=-1,
                               hardware_id=self._parent_id,
                               description='New Failure Mode')
            _error_code, _msg = self.dao.db_add([_mode])

            _data_package = {'mode': _mode}
            self.tree.create_node(tag=_mode.description,
                                  identifier=str(_mode.mode_id),
                                  parent=self._root,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_mode', node_id=str(_mode.mode_id))
        except (DataAccessError, NodeIDAbsentError) as _error:
            pub.sendMessage("fail_insert_mode", error_msg=_error)

    def _do_select_all_action(self, cause_id, parent_id):
        """
        Retrieve all the actions for the cause ID.

        :param int cause_id: the cause ID to select the actions for.
        :parem str parent_id: the parent node ID the actions are associated
            with.
        :return: None
        :rtype: None
        """
        for _action in self.dao.session.query(RAMSTKAction).filter(
                RAMSTKAction.cause_id == cause_id).all():

            _data_package = {'action': _action}

            _identifier = '{0:s}.{1:d}.a'.format(parent_id, _action.action_id)

            self.tree.create_node(tag=_identifier,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

    def _do_select_all_cause(self, mechanism_id, parent_id):
        """
        Retrieve all the failure causes for the mechanism ID.

        :param int mechanism_id: the mechanism ID to select the causes for.
        :parem str parent_id: the parent node ID the causes are associated
            with.
        :return: None
        :rtype: None
        """
        if not self._is_functional:
            for _cause in self.dao.session.query(RAMSTKCause).filter(
                    RAMSTKCause.mechanism_id == mechanism_id).all():

                self._add_cause_node(_cause, parent_id)
        elif self._is_functional:
            for _cause in self.dao.session.query(RAMSTKCause).filter(
                    RAMSTKCause.mode_id == mechanism_id).all():

                self._add_cause_node(_cause, parent_id)

    def _do_select_all_control(self, cause_id, parent_id):
        """
        Retrieve all the controls for the cause ID.

        :param int cause_id: the cause ID to select the controls for.
        :parem str parent_id: the parent node ID the controls are associated
            with.
        :return: None
        :rtype: None
        """
        for _control in self.dao.session.query(RAMSTKControl).filter(
                RAMSTKControl.cause_id == cause_id).all():

            _data_package = {'control': _control}

            _identifier = '{0:s}.{1:d}.c'.format(parent_id,
                                                 _control.control_id)

            self.tree.create_node(tag=_identifier,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

    def _do_select_all_mechanism(self, mode_id):
        """
        Retrieve all the failure mechanisms for the mode ID.

        :param int mode_id: the mode ID to select the mechanisms for.
        :return: None
        :rtype: None
        """
        for _mechanism in self.dao.session.query(RAMSTKMechanism).filter(
                RAMSTKMechanism.mode_id == mode_id).all():

            _data_package = {'mechanism': _mechanism}

            _identifier = '{0:d}.{1:d}'.format(mode_id,
                                               _mechanism.mechanism_id)

            self.tree.create_node(tag=_identifier,
                                  identifier=_identifier,
                                  parent=str(mode_id),
                                  data=_data_package)

            self._do_select_all_cause(_mechanism.mechanism_id, _identifier)

    def do_get_tree(self):
        """
        Retrieve the FMEA treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_fmea_tree', dmtree=self.tree)

    def do_select_all(self, parent_id):  # pylint: disable=arguments-differ
        """
        Retrieve all the FMEA data from the RAMSTK Program database.

        :param int parent_id: the parent (function or hardware) ID to select
            the FMEA for.
        :return: None
        :rtype: None
        """
        self._parent_id = parent_id

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        if not self._is_functional:
            for _mode in self.dao.session.query(RAMSTKMode).filter(
                    RAMSTKMode.hardware_id == self._parent_id).all():

                self._add_mode_node(_mode)
                self._do_select_all_mechanism(_mode.mode_id)

            pub.sendMessage('succeed_retrieve_hardware_fmea', tree=self.tree)

        elif self._is_functional:
            for _mode in self.dao.session.query(RAMSTKMode).filter(
                    RAMSTKMode.function_id == self._parent_id).all():

                self._add_mode_node(_mode)
                self._do_select_all_cause(_mode.mode_id, str(parent_id))

            pub.sendMessage('succeed_retrieve_functional_fmea', tree=self.tree)

    def do_set_attributes(self, node_id, key, value, table):
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :param str table: the name of the table whose attributes are being set.
        :return: None
        :rtype: None
        """
        _poppers = {
            'mode': ['function_id', 'hardware_id', 'mode_id'],
            'mechanism': ['mode_id', 'mechanism_id'],
            'cause': ['mode_id', 'mechanism_id', 'cause_id'],
            'control': ['cause_id', 'control_id'],
            'action': ['cause_id', 'action_id']
        }

        _attributes = self.do_select(node_id, table=table).get_attributes()

        for _field in _poppers[table]:
            _attributes.pop(_field)

        if key in _attributes:
            _attributes[key] = value

            self.do_select(node_id, table=table).set_attributes(_attributes)

    def do_update(self, node_id):
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the node ID of the FMEA item to save.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]
            self.dao.session.add(self.tree.get_node(node_id).data[_table])

            _error_code, _error_msg = self.dao.db_update()

            if _error_code == 0:
                pub.sendMessage('succeed_update_fmea', node_id=node_id)
            else:
                pub.sendMessage('fail_update_fmea', error_msg=_error_msg)
        except AttributeError:
            pub.sendMessage('fail_update_fmea',
                            error_msg=('Attempted to save non-existent '
                                       'FMEA element with FMEA ID '
                                       '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_fmea',
                                error_msg=('No data package found for '
                                           'FMEA ID {0:s}.').format(
                                               str(node_id)))
