# -*- coding: utf-8 -*-
#
#       ramstk.controllers.fmea.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

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
    """Contain the attributes and methods of the FMEA data manager.

    This class manages the fmea data from the RAMSTKFMEA and
    RAMSTKHazardAnalysis data models.
    """

    _tag = 'fmeas'
    _root = 0

    # pylint: disable=unused-argument
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a FMEA data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
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

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        try:
            # noinspection PyTypeChecker
            self._is_functional: bool = kwargs['functional']  # type: ignore
        except KeyError:
            self._is_functional = False
        self._parent_id: int = 0

        # Initialize public dictionary attributes.
        self.last_id: Dict[str, int] = {
            'mode': 0,
            'mechanism': 0,
            'cause': 0,
            'control': 0,
            'action': 0,
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, 'request_get_mode_attributes')
        pub.subscribe(super().do_get_attributes,
                      'request_get_mechanism_attributes')
        pub.subscribe(super().do_get_attributes,
                      'request_get_cause_attributes')
        pub.subscribe(super().do_get_attributes,
                      'request_get_control_attributes')
        pub.subscribe(super().do_get_attributes,
                      'request_get_action_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_fmea')
        pub.subscribe(super().do_set_attributes, 'request_set_fmea_attributes')
        pub.subscribe(super().do_update_all, 'request_update_all_fmeas')

        pub.subscribe(self.do_select_all, 'selected_function')
        pub.subscribe(self.do_select_all, 'selected_hardware')
        pub.subscribe(self.do_update, 'request_update_fmea')
        pub.subscribe(self.do_get_tree, 'request_get_fmea_tree')

        pub.subscribe(self._do_delete, 'request_delete_fmea')
        pub.subscribe(self._do_insert_action, 'request_insert_fmea_action')
        pub.subscribe(self._do_insert_cause, 'request_insert_fmea_cause')
        pub.subscribe(self._do_insert_control, 'request_insert_fmea_control')
        pub.subscribe(self._do_insert_mechanism,
                      'request_insert_fmea_mechanism')
        pub.subscribe(self._do_insert_mode, 'request_insert_fmea_mode')

    def do_get_tree(self) -> None:
        """Retrieve the FMEA treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_fmea_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all FMEA data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            function or hardware item.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._revision_id = attributes['revision_id']

        try:
            self._is_functional = False
            self._parent_id = attributes['hardware_id']
            self._do_select_all_hardware_fmea()
        except KeyError:
            self._is_functional = True
            self._parent_id = attributes['function_id']

    def do_update(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node ID of the FMEA item to save.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            self.dao.session.add(self.tree.get_node(node_id).data[_table])

            self.dao.do_update()
            pub.sendMessage(
                'succeed_update_fmea',
                tree=self.tree,
            )
        except AttributeError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: Attempted to save non-existent FMEA '
                          'record ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_fmea',
                error_message=_error_msg,
            )
        except IndexError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: No data package found for FMEA record '
                          'ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_fmea',
                error_message=_error_msg,
            )
        except (TypeError, DataAccessError):
            if node_id != 0:
                _method_name: str = inspect.currentframe(  # type: ignore
                ).f_code.co_name
                _error_msg = ('{1}: The value for one or more attributes for '
                              'FMEA record ID {0} was the wrong '
                              'type.').format(str(node_id), _method_name)
                pub.sendMessage(
                    'do_log_debug',
                    logger_name='DEBUG',
                    message=_error_msg,
                )
                pub.sendMessage(
                    'fail_update_fmea',
                    error_message=_error_msg,
                )

    def _add_cause_node(self, cause: RAMSTKCause, parent_id: str) -> None:
        """Add a node to the treelib Tree() to hold a failure cause.

        This is a helper method to allow causes to be children of either a
        failure mode (functional FMEA) or a failure mechanism (hardware FMEA).

        :param cause: an instance of RAMSTKCause.
        :param parent_id: the parent node ID the causes are associated
            with.
        :return: None
        :rtype: None
        """
        _identifier = '{0:s}.{1:d}'.format(parent_id,
                                           cause.cause_id)  # type: ignore

        self.tree.create_node(tag='cause',
                              identifier=_identifier,
                              parent=parent_id,
                              data={'cause': cause})

        self.last_id['cause'] = max(self.last_id['cause'],
                                    cause.cause_id)  # type: ignore

        self._do_select_all_control(_identifier)
        self._do_select_all_action(_identifier)

    def _add_mode_node(self, mode: RAMSTKMode) -> None:
        """Add a node to the treelib Tree() to hold a failure mode.

        This is a helper method to allow modes to be children of either a
        function (functional FMEA) or a hardware item (hardware FMEA).

        :param mode: an instance of RAMSTKMode.
        :type mode: :class:`ramstk.models.programdb.RAMSTKMode`
        :return: None
        :rtype: None
        """
        self.tree.create_node(
            tag='mode',
            identifier=str(mode.mode_id),  # type: ignore
            parent=self._root,
            data={'mode': mode})

        self.last_id['mode'] = max(self.last_id['mode'], mode.mode_id)

    def _do_delete(self, node_id: int) -> None:
        """Remove a FMEA element.

        :param node_id: the node (FMEA action) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """

        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            super().do_delete(node_id, _table)

            self.tree.remove_node(node_id)

            pub.sendMessage(
                'succeed_delete_fmea',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent FMEA record '
                'with hardware ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_fmea',
                error_message=_error_msg,
            )

    def _do_insert_action(self, parent_id: str) -> None:
        """Add a new action to FMEA cause ID.

        :param parent_id: the parent node ID the control is associated
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
            _action.action_id = self.last_id['action'] + 1
            _action.action_recommended = 'Recommended Action'

            self.dao.do_insert(_action)

            self.last_id['action'] = _action.action_id

            _identifier = '{0:s}.{1:d}.a'.format(parent_id, _action.action_id)
            self.tree.create_node(tag='action',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'action': _action})

            pub.sendMessage(
                'succeed_insert_fmea',
                node_id=self.last_id['action'],
                tree=self.tree,
            )
            pub.sendMessage(
                'succeed_insert_action',
                node_id=_identifier,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_action",
                error_message=_error.msg,
            )

    def _do_insert_cause(self, parent_id: str) -> None:
        """Add a new failure cause to FMEA mechanism ID.

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
            _cause.cause_id = self.last_id['cause'] + 1
            _cause.description = 'New Failure Cause'

            self.dao.do_insert(_cause)

            self.last_id['cause'] = _cause.cause_id

            _identifier = '{0:s}.{1:d}'.format(parent_id, _cause.cause_id)

            self.tree.create_node(tag='cause',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'cause': _cause})

            pub.sendMessage(
                'succeed_insert_fmea',
                node_id=self.last_id['cause'],
                tree=self.tree,
            )
            pub.sendMessage(
                'succeed_insert_cause',
                node_id=_identifier,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_cause",
                error_message=_error.msg,
            )

    def _do_insert_control(self, parent_id: str) -> None:
        """Add a new control to FMEA cause ID.

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
            _control.control_id = self.last_id['control'] + 1
            _control.description = 'New Control'

            self.dao.do_insert(_control)

            self.last_id['control'] = _control.control_id

            _identifier = '{0:s}.{1:d}.c'.format(parent_id,
                                                 _control.control_id)
            self.tree.create_node(tag='control',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'control': _control})

            pub.sendMessage(
                'succeed_insert_fmea',
                node_id=self.last_id['control'],
                tree=self.tree,
            )
            pub.sendMessage(
                'succeed_insert_control',
                node_id=_identifier,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_control",
                error_message=_error.msg,
            )

    def _do_insert_mechanism(self, mode_id: str) -> None:
        """Add a new failure mechanism to FMEA mode ID.

        :param mode_id: the FMEA mode ID to associate the new mechanism
            with.
        :return: None
        :rtype: None
        """
        try:
            _mechanism = RAMSTKMechanism()
            _mechanism.revision_id = self._revision_id
            _mechanism.hardware_id = self._parent_id
            _mechanism.mode_id = int(mode_id)
            _mechanism.mechanism_id = self.last_id['mechanism'] + 1
            _mechanism.description = 'New Failure Mechanism'

            self.dao.do_insert(_mechanism)

            self.last_id['mechanism'] = _mechanism.mechanism_id

            _identifier = '{0:s}.{1:d}'.format(mode_id,
                                               _mechanism.mechanism_id)

            self.tree.create_node(tag='mechanism',
                                  identifier=_identifier,
                                  parent=mode_id,
                                  data={'mechanism': _mechanism})

            pub.sendMessage(
                'succeed_insert_fmea',
                node_id=self.last_id['mechanism'],
                tree=self.tree,
            )
            pub.sendMessage(
                'succeed_insert_mechanism',
                node_id=_identifier,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_mechanism",
                error_message=_error.msg,
            )

    def _do_insert_mode(self) -> None:
        """Add a new failure mode.

        :return: None
        :rtype: None
        """
        try:
            _mode = RAMSTKMode()
            _mode.revision_id = self._revision_id
            _mode.hardware_id = self._parent_id
            _mode.mode_id = self.last_id['mode'] + 1
            _mode.description = 'New Failure Mode'

            self.dao.do_insert(_mode)

            self.last_id['mode'] = _mode.mode_id

            self.tree.create_node(tag='mode',
                                  identifier=str(_mode.mode_id),
                                  parent=self._root,
                                  data={'mode': _mode})

            pub.sendMessage(
                'succeed_insert_fmea',
                node_id=self.last_id['mode'],
                tree=self.tree,
            )
            pub.sendMessage(
                'succeed_insert_mode',
                node_id=str(_mode.mode_id),
                tree=self.tree,
            )
        except NodeIDAbsentError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to add a mode to non-existent parent FMEA '
                'record with hardware ID {0}.').format(str(self._root),
                                                       _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_insert_mode",
                error_message=_error_msg,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_mode",
                error_message=_error.msg,
            )

    def _do_select_all_action(self, parent_id: str) -> None:
        """Retrieve all the actions for the cause ID.

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

            _identifier = '{0:s}.{1:d}.a'.format(parent_id, _action.action_id)

            self.tree.create_node(tag='action',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'action': _action})

            self.last_id['action'] = max(self.last_id['action'],
                                         _action.action_id)

    def _do_select_all_cause(self, parent_id: str) -> None:
        """Retrieve all the failure causes for the mechanism ID.

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
        """Retrieve all the controls for the cause ID.

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

            self.last_id['control'] = max(self.last_id['control'],
                                          _control.control_id)

    def _do_select_all_functional_fmea(self) -> None:
        """Retrieve all functional FMEA data from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _mode in self.dao.session.query(RAMSTKMode).filter(
                RAMSTKMode.function_id == self._parent_id).all():

            self._add_mode_node(_mode)
            self._do_select_all_cause(str(self._parent_id))

        pub.sendMessage(
            'succeed_retrieve_functional_fmea',
            tree=self.tree,
        )

    def _do_select_all_hardware_fmea(self) -> None:
        """Retrieve all hardware FMEA data from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _mode in self.dao.session.query(RAMSTKMode).filter(
                RAMSTKMode.revision_id == self._revision_id,
                RAMSTKMode.hardware_id == self._parent_id).all():

            self._add_mode_node(_mode)
            self._do_select_all_mechanism(_mode.mode_id)

        pub.sendMessage(
            'succeed_retrieve_hardware_fmea',
            tree=self.tree,
        )

    def _do_select_all_mechanism(self, mode_id: int) -> None:
        """Retrieve all the failure mechanisms for the mode ID.

        :param mode_id: the mode ID to select the mechanisms for.
        :return: None
        :rtype: None
        """
        for _mechanism in self.dao.session.query(RAMSTKMechanism).filter(
                RAMSTKMechanism.mode_id == mode_id).all():

            _identifier = '{0:d}.{1:d}'.format(mode_id,
                                               _mechanism.mechanism_id)

            self.tree.create_node(tag='mechanism',
                                  identifier=_identifier,
                                  parent=str(mode_id),
                                  data={'mechanism': _mechanism})

            self.last_id['mechanism'] = max(self.last_id['mechanism'],
                                            _mechanism.mechanism_id)

            self._do_select_all_cause(_identifier)
