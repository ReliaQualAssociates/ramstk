# -*- coding: utf-8 -*-
#
#       ramstk.controllers.fmea.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (RAMSTKAction, RAMSTKCause, RAMSTKControl,
                                     RAMSTKMechanism, RAMSTKMode)


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the FMEA data manager.

    This class manages the fmea data from the RAMSTKFMEA and
    RAMSTKHazardAnalysis data models.
    """

    _tag = 'fmea'
    _root = 0

    # pylint: disable=unused-argument
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a FMEA data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._last_id = [0, 0, 0, 0, 0]

        # Initialize private scalar attributes.
        try:
            self._is_functional: bool = kwargs['functional']
        except KeyError:
            self._is_functional = False
        self._parent_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_select_all_functional_fmea, 'selected_function')
        pub.subscribe(self._do_select_all_hardware_fmea, 'selected_hardware')
        pub.subscribe(self._do_delete, 'request_delete_fmea')
        pub.subscribe(self._do_insert_action, 'request_insert_fmea_action')
        pub.subscribe(self._do_insert_cause, 'request_insert_fmea_cause')
        pub.subscribe(self._do_insert_control, 'request_insert_fmea_control')
        pub.subscribe(self._do_insert_mechanism,
                      'request_insert_fmea_mechanism')
        pub.subscribe(self._do_insert_mode, 'request_insert_fmea_mode')
        pub.subscribe(self._do_set_fmea_attributes, 'wvw_editing_fmea')
        pub.subscribe(self._do_set_fmea_attributes,
                      'request_set_fmea_attributes')

        pub.subscribe(self.do_update, 'request_update_fmea')
        pub.subscribe(self.do_update_all, 'request_update_all_fmea')
        pub.subscribe(self.do_get_attributes, 'request_get_mode_attributes')
        pub.subscribe(self.do_get_attributes,
                      'request_get_mechanism_attributes')
        pub.subscribe(self.do_get_attributes, 'request_get_cause_attributes')
        pub.subscribe(self.do_get_attributes, 'request_get_control_attributes')
        pub.subscribe(self.do_get_attributes, 'request_get_action_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_fmea_tree')

    def _add_cause_node(self, cause: object, parent_id: str) -> None:
        """
        Add a node to the treelib Tree() to hold a failure cause.

        This is a helper method to allow causes to be children of either a
        failure mode (functional FMEA) or a failure mechanism (hardware FMEA).

        :param cause: an instance of RAMSTKCause.
        :type cause: :class:`ramstk.models.programdb.RAMSTKCause`
        :param str parent_id: the parent node ID the causes are associated
            with.
        :return: None
        :rtype: None
        """
        _data_package = {'cause': cause}

        _identifier = '{0:s}.{1:d}'.format(parent_id, cause.cause_id)

        self.tree.create_node(tag='cause',
                              identifier=_identifier,
                              parent=parent_id,
                              data=_data_package)

        self._last_id[2] = max(self._last_id[2], cause.cause_id)

        self._do_select_all_control(_identifier)
        self._do_select_all_action(_identifier)

    def _add_mode_node(self, mode: object) -> None:
        """
        Add a node to the treelib Tree() to hold a failure mode.

        This is a helper method to allow modes to be children of either a
        function (functional FMEA) or a hardware item (hardware FMEA).

        :param mode: an instance of RAMSTKMode.
        :type mode: :class:`ramstk.models.programdb.RAMSTKMode`
        :return: None
        :rtype: None
        """
        _data_package = {'mode': mode}

        self.tree.create_node(tag='mode',
                              identifier=str(mode.mode_id),
                              parent=self._root,
                              data=_data_package)

        self._last_id[0] = max(self._last_id[0], mode.mode_id)

    def _do_delete(self, node_id: int) -> None:
        """
        Remove a FMEA element.

        :param int node_id: the node (FMEA action) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            RAMSTKDataManager.do_delete(self, node_id, _table)

            self.tree.remove_node(node_id)
            pub.sendMessage('succeed_delete_fmea', node_id=node_id)

        except (AttributeError, DataAccessError):
            _error_msg = ("Attempted to delete non-existent FMEA element ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_fmea', error_message=_error_msg)

    def _do_insert_action(self, parent_id: str) -> None:
        """
        Add a new action to FMEA cause ID.

        :param str parent_id: the parent node ID the control is associated
            with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _cause_id) = parent_id.split('.')
        try:
            _action = RAMSTKAction()
            _action.revision_id = self._revision_id
            _action.hardware_id = self._parent_id
            _action.mode_id = int(_mode_id)
            _action.mechanism_id = int(_mechanism_id)
            _action.cause_id = int(_cause_id)
            _action.action_id = self._last_id[4] + 1
            _action.action_recommended = 'Recommended Action'

            self.dao.do_insert(_action)

            self._last_id[4] = _action.action_id

            _data_package = {'action': _action}

            _identifier = '{0:s}.{1:d}.a'.format(parent_id, _action.action_id)
            self.tree.create_node(tag='action',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_action',
                            node_id=_identifier,
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ('Attempting to add an action to unknown failure '
                          'cause ID {0:d}.'.format(int(_cause_id)))
            pub.sendMessage("fail_insert_action", error_message=_error_msg)

    def _do_insert_cause(self, parent_id: str) -> None:
        """
        Add a new failure cause to FMEA mechanism ID.

        :parem str parent_id: the parent node ID the cause is associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id) = parent_id.split('.')
        try:
            _cause = RAMSTKCause()
            _cause.revision_id = self._revision_id
            _cause.hardware_id = self._parent_id
            _cause.mode_id = int(_mode_id)
            _cause.mechanism_id = int(_mechanism_id)
            _cause.cause_id = self._last_id[2] + 1
            _cause.description = 'New Failure Cause'

            self.dao.do_insert(_cause)

            self._last_id[2] = _cause.cause_id

            _identifier = '{0:s}.{1:d}'.format(parent_id, _cause.cause_id)

            _data_package = {'cause': _cause}
            self.tree.create_node(tag='cause',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_cause',
                            node_id=_identifier,
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = (
                'Attempting to add a failure cause to unknown '
                'failure mode ID {0:d} or mechanism ID {1:d}.'.format(
                    int(_mode_id), int(_mechanism_id)))
            pub.sendMessage("fail_insert_cause", error_message=_error_msg)

    def _do_insert_control(self, parent_id: str) -> None:
        """
        Add a new control to FMEA cause ID.

        :parem str parent_id: the parent node ID the control is associated
            with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _cause_id) = parent_id.split('.')
        try:
            _control = RAMSTKControl()
            _control.revision_id = self._revision_id
            _control.hardware_id = self._parent_id
            _control.mode_id = int(_mode_id)
            _control.mechanism_id = int(_mechanism_id)
            _control.cause_id = int(_cause_id)
            _control.control_id = self._last_id[3] + 1
            _control.description = 'New Control'

            self.dao.do_insert(_control)

            self._last_id[3] = _control.control_id

            _data_package = {'control': _control}

            _identifier = '{0:s}.{1:d}.c'.format(parent_id,
                                                 _control.control_id)
            self.tree.create_node(tag='control',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_control',
                            node_id=_identifier,
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ('Attempting to add a control to unknown failure '
                          'cause ID {0:d}.'.format(int(_cause_id)))
            pub.sendMessage("fail_insert_control", error_message=_error_msg)

    def _do_insert_mechanism(self, mode_id: str) -> None:
        """
        Add a new failure mechanism to FMEA mode ID.

        :param str mode_id: the FMEA mode ID to associate the new mechanism
            with.
        :return: None
        :rtype: None
        """
        try:
            _mechanism = RAMSTKMechanism()
            _mechanism.revision_id = self._revision_id
            _mechanism.hardware_id = self._parent_id
            _mechanism.mode_id = int(mode_id)
            _mechanism.mechanism_id = self._last_id[1] + 1
            _mechanism.description = 'New Failure Mechanism'

            self.dao.do_insert(_mechanism)

            self._last_id[1] = _mechanism.mechanism_id

            _identifier = '{0:s}.{1:d}'.format(mode_id,
                                               _mechanism.mechanism_id)

            _data_package = {'mechanism': _mechanism}
            self.tree.create_node(tag='mechanism',
                                  identifier=_identifier,
                                  parent=mode_id,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_mechanism',
                            node_id=_identifier,
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ('Attempting to add a failure mechanism to unknown '
                          'failure mode ID {0:s}.'.format(str(mode_id)))
            pub.sendMessage("fail_insert_mechanism", error_message=_error_msg)

    def _do_insert_mode(self) -> None:
        """
        Add a new failure mode.

        :return: None
        :rtype: None
        """
        try:
            _mode = RAMSTKMode()
            _mode.revision_id = self._revision_id
            _mode.hardware_id = self._parent_id
            _mode.mode_id = self._last_id[0] + 1
            _mode.description = 'New Failure Mode'

            self.dao.do_insert(_mode)

            self._last_id[0] = _mode.mode_id

            _data_package = {'mode': _mode}
            self.tree.create_node(tag='mode',
                                  identifier=str(_mode.mode_id),
                                  parent=self._root,
                                  data=_data_package)

            pub.sendMessage('succeed_insert_mode',
                            node_id=str(_mode.mode_id),
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ('Attempting to add a failure mode to unknown '
                          'hardware ID {0:s}.'.format(str(self._root)))
            pub.sendMessage("fail_insert_mode", error_message=_error_msg)

    def _do_select_all_action(self, parent_id: str) -> None:
        """
        Retrieve all the actions for the cause ID.

        :parem str parent_id: the parent node ID the actions are associated
            with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _cause_id) = parent_id.split('.')
        for _action in self.dao.session.query(RAMSTKAction).filter(
                RAMSTKAction.mode_id == int(_mode_id),
                RAMSTKAction.mechanism_id == int(_mechanism_id),
                RAMSTKAction.cause_id == int(_cause_id)).all():

            _data_package = {'action': _action}

            _identifier = '{0:s}.{1:d}.a'.format(parent_id, _action.action_id)

            self.tree.create_node(tag='action',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

            self._last_id[4] = max(self._last_id[4], _action.action_id)

    def _do_select_all_cause(self, parent_id: str) -> None:
        """
        Retrieve all the failure causes for the mechanism ID.

        :parem str parent_id: the parent node ID the causes are associated
            with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id) = parent_id.split('.')
        for _cause in self.dao.session.query(RAMSTKCause).filter(
                RAMSTKCause.mode_id == int(_mode_id),
                RAMSTKCause.mechanism_id == int(_mechanism_id)).all():

            self._add_cause_node(_cause, parent_id)

    def _do_select_all_control(self, parent_id: str) -> None:
        """
        Retrieve all the controls for the cause ID.

        :parem str parent_id: the parent node ID the controls are associated
            with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _cause_id) = parent_id.split('.')
        for _control in self.dao.session.query(RAMSTKControl).filter(
                RAMSTKControl.mode_id == int(_mode_id),
                RAMSTKControl.mechanism_id == int(_mechanism_id),
                RAMSTKControl.cause_id == int(_cause_id)).all():

            _data_package = {'control': _control}

            _identifier = '{0:s}.{1:d}.c'.format(parent_id,
                                                 _control.control_id)

            self.tree.create_node(tag='control',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data=_data_package)

            self._last_id[3] = max(self._last_id[3], _control.control_id)

    def _do_select_all_functional_fmea(self,
                                       attributes: Dict[str, Any]) -> None:
        """
        Retrieve all functional FMEA data from the RAMSTK Program database.

        :param dict attributes: the attributes dict for the selected
            function or hardware item.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._parent_id = attributes['function_id']
        for _mode in self.dao.session.query(RAMSTKMode).filter(
                RAMSTKMode.function_id == self._parent_id).all():

            self._add_mode_node(_mode)
            self._do_select_all_cause(str(self._parent_id))

        pub.sendMessage('succeed_retrieve_functional_fmea', tree=self.tree)

    def _do_select_all_hardware_fmea(self, attributes: Dict[str, Any]) -> None:
        """
        Retrieve all hardware FMEA data from the RAMSTK Program database.

        :param dict attributes: the attributes dict for the selected
            function or hardware item.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._last_id = [0, 0, 0, 0, 0]
        self._revision_id = attributes['revision_id']
        self._parent_id = attributes['hardware_id']
        for _mode in self.dao.session.query(RAMSTKMode).filter(
                RAMSTKMode.hardware_id == self._parent_id).all():

            self._add_mode_node(_mode)
            self._do_select_all_mechanism(_mode.mode_id)

        pub.sendMessage('succeed_retrieve_hardware_fmea', tree=self.tree)

    def _do_select_all_mechanism(self, mode_id: int) -> None:
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

            self.tree.create_node(tag='mechanism',
                                  identifier=_identifier,
                                  parent=str(mode_id),
                                  data=_data_package)

            self._last_id[1] = max(self._last_id[1], _mechanism.mechanism_id)

            self._do_select_all_cause(_identifier)

    def _do_set_fmea_attributes(self, node_id: List[int],
                                package: Dict[str, Any]) -> None:
        """
        Set the attributes of the record associated with the Module ID.

        :param list node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        _pkey = {
            'mode': ['revision_id', 'hardware_id', 'mode_id'],
            'mechanism':
            ['revision_id', 'hardware_id', 'mode_id', 'mechanism_id'],
            'cause': [
                'revision_id', 'hardware_id', 'mode_id', 'mechanism_id',
                'cause_id'
            ],
            'control': [
                'revision_id', 'hardware_id', 'mode_id', 'mechanism_id',
                'cause_id', 'control_id'
            ],
            'action': [
                'revision_id', 'hardware_id', 'mode_id', 'mechanism_id',
                'cause_id', 'action_id'
            ]
        }
        for _table in ['mode', 'mechanism', 'cause', 'control', 'action']:
            try:
                _attributes = self.do_select(node_id[0],
                                             table=_table).get_attributes()
            except (AttributeError, KeyError):
                _attributes = {}

            for _field in _pkey[_table]:
                try:
                    _attributes.pop(_field)
                except KeyError:
                    pass

            if _key in _attributes:
                _attributes[_key] = _value

                self.do_select(node_id[0],
                               table=_table).set_attributes(_attributes)

    def do_get_tree(self) -> None:
        """
        Retrieve the FMEA treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_fmea_tree', dmtree=self.tree)

    def do_update(self, node_id: int) -> None:
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the node ID of the FMEA item to save.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]
            self.dao.session.add(self.tree.get_node(node_id).data[_table])

            self.dao.do_update()
            pub.sendMessage('succeed_update_fmea', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_fmea',
                            error_message=('Attempted to save non-existent '
                                           'FMEA element with FMEA ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_fmea',
                                error_message=('No data package found for '
                                               'FMEA ID {0:s}.').format(
                                                   str(node_id)))
