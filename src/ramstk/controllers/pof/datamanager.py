# -*- coding: utf-8 -*-
#
#       ramstk.controllers.pof.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""PoF Package Data Model."""

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
    RAMSTKMechanism, RAMSTKMode, RAMSTKOpLoad,
    RAMSTKOpStress, RAMSTKTestMethod
)


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the PoF data manager.

    This class manages the PoF data from the RAMSTKMode,
    RAMSTKMechanism, RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod
    data models.
    """

    _tag = 'pofs'
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a PoF data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            'opload': [
                'revision_id', 'hardware_id', 'mode_id', 'mechanism_id',
                'load_id'
            ],
            'opstress': [
                'revision_id', 'hardware_id', 'mode_id', 'mechanism_id',
                'load_id', 'stress_id'
            ],
            'testmethod': [
                'revision_id', 'hardware_id', 'mode_id', 'mechanism_id',
                'load_id', 'test_id'
            ]
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.
        self.last_id: Dict[str, int] = {
            'opload': 0,
            'opstress': 0,
            'testmethod': 0,
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, 'request_get_mode_attributes')
        pub.subscribe(super().do_get_attributes,
                      'request_get_mechanism_attributes')
        pub.subscribe(super().do_get_attributes,
                      'request_get_opload_attributes')
        pub.subscribe(super().do_get_attributes,
                      'request_get_opstress_attributes')
        pub.subscribe(super().do_get_attributes,
                      'request_get_test_method_attributes')
        pub.subscribe(super().do_set_attributes, 'request_set_pof_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_pof')
        pub.subscribe(super().do_update_all, 'request_update_all_pofs')

        pub.subscribe(self.do_select_all, 'selected_hardware')
        pub.subscribe(self.do_update, 'request_update_pof')
        pub.subscribe(self.do_get_tree, 'request_get_pof_tree')

        pub.subscribe(self._do_delete, 'request_delete_pof')
        pub.subscribe(self._do_insert_opload, 'request_insert_pof_opload')
        pub.subscribe(self._do_insert_opstress, 'request_insert_pof_opstress')
        pub.subscribe(self._do_insert_testmethod,
                      'request_insert_pof_testmethod')

    def do_get_tree(self) -> None:
        """Retrieve the PoF treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            'succeed_get_pof_tree',
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the PoF data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            function or hardware item.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._revision_id = attributes['revision_id']
        self._parent_id = attributes['hardware_id']

        for _mode in self.dao.session.query(RAMSTKMode).filter(
                RAMSTKMode.revision_id == self._revision_id,
                RAMSTKMode.hardware_id == self._parent_id).all():

            self.tree.create_node(tag='mode',
                                  identifier=str(_mode.mode_id),
                                  parent=self._root,
                                  data={'mode': _mode})

            self._do_select_all_mechanism(_mode.mode_id)

        pub.sendMessage(
            'succeed_retrieve_pof',
            tree=self.tree,
        )

    def do_update(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node ID of the PoF item to save.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            self.dao.session.add(self.tree.get_node(node_id).data[_table])

            self.dao.do_update()
            pub.sendMessage(
                'succeed_update_pof',
                tree=self.tree,
            )
        except AttributeError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: Attempted to save non-existent PoF '
                          'record ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_pof',
                error_message=_error_msg,
            )
        except IndexError:
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: No data package found for PoF record '
                          'ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_pof',
                error_message=_error_msg,
            )
        except (TypeError, DataAccessError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg = ('{1}: The value for one or more attributes for PoF '
                          'record ID {0} was the wrong type.').format(
                              str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_update_pof',
                error_message=_error_msg,
            )

    def _do_delete(self, node_id: int) -> None:
        """Remove a PoF element.

        :param node_id: the node (PoF element) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            super().do_delete(node_id, _table)

            self.tree.remove_node(node_id)
            pub.sendMessage(
                'succeed_delete_pof_2',
                node_id=node_id,
            )
            pub.sendMessage(
                'succeed_delete_pof',
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe(  # type: ignore
            ).f_code.co_name
            _error_msg: str = (
                '{1}: Attempted to delete non-existent PoF record '
                'with ID {0}.').format(str(node_id), _method_name)
            pub.sendMessage(
                'do_log_debug',
                logger_name='DEBUG',
                message=_error_msg,
            )
            pub.sendMessage(
                'fail_delete_pof',
                error_message=_error_msg,
            )

    def _do_insert_opload(self, parent_id: str) -> None:
        """Add a new operating to PoF mechanism ID.

        :param parent_id: the parent node ID the operating load is
            associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id) = parent_id.split('.')
        try:
            _opload = RAMSTKOpLoad()
            _opload.revision_id = self._revision_id
            _opload.hardware_id = self._parent_id
            _opload.mode_id = int(_mode_id)
            _opload.mechanism_id = int(_mechanism_id)
            _opload.load_id = self.last_id['opload'] + 1
            _opload.description = 'New Operating Load'

            self.dao.do_insert(_opload)

            _identifier = '{0:s}.{1:d}'.format(parent_id, _opload.load_id)

            self.tree.create_node(tag='opload',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'opload': _opload})

            self.last_id['opload'] = max(self.last_id['opload'],
                                         _opload.load_id)

            pub.sendMessage('succeed_insert_pof',
                            node_id=self.last_id['opload'],
                            tree=self.tree)
            pub.sendMessage('succeed_insert_opload',
                            node_id=_identifier,
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = (
                'An error occurred when attempting to add an operating load '
                'to failure mechanism ID {0:s}.'.format(_mechanism_id))
            pub.sendMessage("fail_insert_opload", error_message=_error_msg)

    def _do_insert_opstress(self, parent_id: str) -> None:
        """Add a new operating stress to PoF load ID.

        :param str parent_id: the parent node ID the operating stress is
            associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _load_id) = parent_id.split('.')
        try:
            _opstress = RAMSTKOpStress()
            _opstress.revision_id = self._revision_id
            _opstress.hardware_id = self._parent_id
            _opstress.mode_id = int(_mode_id)
            _opstress.mechanism_id = int(_mechanism_id)
            _opstress.load_id = int(_load_id)
            _opstress.stress_id = self.last_id['opstress'] + 1
            _opstress.description = 'New Operating Stress'

            self.dao.do_insert(_opstress)

            _identifier = '{0:s}.{1:d}.s'.format(parent_id,
                                                 _opstress.stress_id)

            self.tree.create_node(tag='opstress',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'opstress': _opstress})

            self.last_id['opstress'] = max(self.last_id['opstress'],
                                           _opstress.stress_id)

            pub.sendMessage('succeed_insert_pof',
                            node_id=self.last_id['opstress'],
                            tree=self.tree)
            pub.sendMessage('succeed_insert_opstress',
                            node_id=_identifier,
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ('An error occurred when attempting to add an '
                          'operating stress to operating load '
                          'ID {0:s}.'.format(_load_id))
            pub.sendMessage("fail_insert_opstress", error_message=_error_msg)

    def _do_insert_testmethod(self, parent_id: str) -> None:
        """Add a new test method to PoF load ID.

        :param str parent_id: the parent node ID the test method is associated
            with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _load_id) = parent_id.split('.')
        try:
            _method = RAMSTKTestMethod()
            _method.revision_id = self._revision_id
            _method.hardware_id = self._parent_id
            _method.mode_id = int(_mode_id)
            _method.mechanism_id = int(_mechanism_id)
            _method.load_id = int(_load_id)
            _method.test_id = self.last_id['testmethod'] + 1
            _method.description = 'New Test Method'

            self.dao.do_insert(_method)

            _identifier = '{0:s}.{1:d}.t'.format(parent_id, _method.test_id)
            self.tree.create_node(tag='method',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'testmethod': _method})

            self.last_id['testmethod'] = max(self.last_id['testmethod'],
                                             _method.test_id)

            pub.sendMessage('succeed_insert_pof',
                            node_id=self.last_id['testmethod'],
                            tree=self.tree)
            pub.sendMessage('succeed_insert_test_method',
                            node_id=_identifier,
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ('An error occurred when attempting to add a test '
                          'method to operating load '
                          'ID {0:s}.'.format(_load_id))
            pub.sendMessage("fail_insert_test_method",
                            error_message=_error_msg)

    def _do_select_all_mechanism(self, mode_id: int) -> None:
        """Retrieve all the failure mechanisms for the mode ID.

        :param mode_id: the mode ID to select the mechanisms for.
        :return: None
        :rtype: None
        """
        for _mechanism in self.dao.session.query(RAMSTKMechanism).filter(
                RAMSTKMode.revision_id == self._revision_id,
                RAMSTKMode.hardware_id == self._parent_id,
                RAMSTKMechanism.mode_id == mode_id).all():

            _identifier = '{0:d}.{1:d}'.format(mode_id,
                                               _mechanism.mechanism_id)

            self.tree.create_node(tag='mechanism',
                                  identifier=_identifier,
                                  parent=str(mode_id),
                                  data={'mechanism': _mechanism})

            self._do_select_all_opload(_identifier)

    def _do_select_all_opload(self, parent_id: str) -> None:
        """Retrieve all the operating loads for the mechanism ID.

        :param str parent_id: the parent node ID the operating loads are
            associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id) = parent_id.split('.')
        for _opload in self.dao.session.query(RAMSTKOpLoad).filter(
                RAMSTKOpLoad.revision_id == self._revision_id,
                RAMSTKOpLoad.hardware_id == self._parent_id,
                RAMSTKOpLoad.mode_id == int(_mode_id),
                RAMSTKOpLoad.mechanism_id == int(_mechanism_id)).all():

            _identifier = '{0:s}.{1:d}'.format(parent_id, _opload.load_id)

            self.tree.create_node(tag='opload',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'opload': _opload})

            self.last_id['opload'] = max(self.last_id['opload'],
                                         _opload.load_id)

            self._do_select_all_opstress(_identifier)
            self._do_select_all_testmethod(_identifier)

    def _do_select_all_opstress(self, parent_id: str) -> None:
        """Retrieve all the operating stresses for the load ID.

        :param str parent_id: the parent node ID the operating stresses are
            associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _load_id) = parent_id.split('.')
        for _opstress in self.dao.session.query(RAMSTKOpStress).filter(
                RAMSTKOpStress.revision_id == self._revision_id,
                RAMSTKOpStress.hardware_id == self._parent_id,
                RAMSTKOpStress.mode_id == int(_mode_id),
                RAMSTKOpStress.mechanism_id == int(_mechanism_id),
                RAMSTKOpStress.load_id == int(_load_id)).all():

            _identifier = '{0:s}.{1:d}.s'.format(parent_id,
                                                 _opstress.stress_id)

            self.tree.create_node(tag='opstress',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'opstress': _opstress})

            self.last_id['opstress'] = max(self.last_id['opstress'],
                                           _opstress.stress_id)

    def _do_select_all_testmethod(self, parent_id: str) -> None:
        """Retrieve all the test methods for the load ID.

        :param str parent_id: the parent node ID the test methods are
            associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _load_id) = parent_id.split('.')
        for _method in self.dao.session.query(RAMSTKTestMethod).filter(
                RAMSTKTestMethod.revision_id == self._revision_id,
                RAMSTKTestMethod.hardware_id == self._parent_id,
                RAMSTKTestMethod.mode_id == int(_mode_id),
                RAMSTKTestMethod.mechanism_id == int(_mechanism_id),
                RAMSTKTestMethod.load_id == int(_load_id)).all():

            _identifier = '{0:s}.{1:d}.t'.format(parent_id, _method.test_id)

            self.tree.create_node(tag='method',
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'testmethod': _method})

            self.last_id['testmethod'] = max(self.last_id['testmethod'],
                                             _method.test_id)
