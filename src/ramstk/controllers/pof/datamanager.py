# -*- coding: utf-8 -*-
#
#       ramstk.controllers.pof.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""PoF Package Data Model."""

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (RAMSTKMechanism, RAMSTKMode, RAMSTKOpLoad,
                                     RAMSTKOpStress, RAMSTKTestMethod)


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the PoF data manager.

    This class manages the PoF data from the RAMSTKMode, RAMSTKMechains,
    RAMSTKOpLoad, RAMSTKOpStress, and RAMSTKTestMethod data models.
    """

    _tag = 'pof'
    _root = 0

    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        """Initialize a PoF data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent_id = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'succeed_select_hardware')
        pub.subscribe(self._do_delete, 'request_delete_pof')
        pub.subscribe(self._do_insert_opload, 'request_insert_opload')
        pub.subscribe(self._do_insert_opstress, 'request_insert_opstress')
        pub.subscribe(self._do_insert_testmethod,
                      'request_insert_pof_testmethod')
        pub.subscribe(self.do_update, 'request_update_pof')
        pub.subscribe(self.do_get_attributes, 'request_get_mode_attributes')
        pub.subscribe(self.do_get_attributes,
                      'request_get_mechanism_attributes')
        pub.subscribe(self.do_get_attributes, 'request_get_opload_attributes')
        pub.subscribe(self.do_get_attributes,
                      'request_get_opstress_attributes')
        pub.subscribe(self.do_get_attributes,
                      'request_get_test_method_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_pof_tree')
        pub.subscribe(self.do_set_attributes, 'request_set_pof_attributes')

    def _do_delete(self, node_id):
        """
        Remove a PoF element.

        :param int node_id: the node (PoF element) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            RAMSTKDataManager.do_delete(self, node_id, _table)

            self.tree.remove_node(node_id)
            pub.sendMessage('succeed_delete_pof', node_id=node_id)
        except AttributeError:
            _error_msg = ("Attempted to delete non-existent PoF element ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_pof', error_message=_error_msg)

    def _do_insert_opload(self, mechanism_id, parent_id):
        """
        Add a new operating to PoF mechanism ID.

        :param int mechanism_id: the PoF mechanism ID to associate the new
            operating load with.
        :parem str parent_id: the parent node ID the operating load is
            associated with.
        :return: None
        :rtype: None
        """
        try:
            _opload = RAMSTKOpLoad(mechanism_id=mechanism_id,
                                   description='New Operating Load')
            self.dao.do_insert(_opload)

            _identifier = '{0:s}.{1:d}'.format(parent_id, _opload.load_id)

            self.tree.create_node(tag=_opload.description,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'opload': _opload})

            pub.sendMessage('succeed_insert_opload', node_id=_identifier)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = (
                'Attempting to add an operating load to unknown failure '
                'mechanism ID {0:d}.'.format(mechanism_id))
            pub.sendMessage("fail_insert_opload", error_message=_error_msg)

    def _do_insert_opstress(self, load_id, parent_id):
        """
        Add a new operating stress to PoF load ID.

        :param int load_id: the PoF load ID to associate the new operating
            stress with.
        :parem str parent_id: the parent node ID the operating stress is
            associated with.
        :return: None
        :rtype: None
        """
        try:
            _opstress = RAMSTKOpStress(load_id=load_id,
                                       description='New Operating Stress')
            self.dao.do_insert(_opstress)

            _identifier = '{0:s}.{1:d}.s'.format(parent_id,
                                                 _opstress.stress_id)

            self.tree.create_node(tag=_identifier,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'opstress': _opstress})

            pub.sendMessage('succeed_insert_opstress', node_id=_identifier)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ('Attempting to add an operating stress to unknown '
                          'operating load ID {0:d}.'.format(load_id))
            pub.sendMessage("fail_insert_opstress", error_message=_error_msg)

    def _do_insert_testmethod(self, load_id, parent_id):
        """
        Add a new test method to PoF load ID.

        :param int load_id: the PoF load ID to associate the new test method
            with.
        :parem str parent_id: the parent node ID the test method is associated
            with.
        :return: None
        :rtype: None
        """
        try:
            _method = RAMSTKTestMethod(load_id=load_id,
                                       description='New Test Method')
            self.dao.do_insert(_method)

            _identifier = '{0:s}.{1:d}.t'.format(parent_id, _method.test_id)
            self.tree.create_node(tag=_method.description,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'testmethod': _method})

            pub.sendMessage('succeed_insert_test_method', node_id=_identifier)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ('Attempting to add a test method to unknown '
                          'operating load ID {0:d}.'.format(load_id))
            pub.sendMessage("fail_insert_test_method",
                            error_message=_error_msg)

    def _do_select_all_mechanism(self, mode_id):
        """
        Retrieve all the failure mechanisms for the mode ID.

        :param int mode_id: the mode ID to select the mechanisms for.
        :return: None
        :rtype: None
        """
        for _mechanism in self.dao.session.query(RAMSTKMechanism).filter(
                RAMSTKMechanism.mode_id == mode_id).all():

            _identifier = '{0:d}.{1:d}'.format(mode_id,
                                               _mechanism.mechanism_id)

            self.tree.create_node(tag=_identifier,
                                  identifier=_identifier,
                                  parent=str(mode_id),
                                  data={'mechanism': _mechanism})

            self._do_select_all_opload(_mechanism.mechanism_id, _identifier)

    def _do_select_all_opload(self, mechanism_id, parent_id):
        """
        Retrieve all the operating loads for the mechanism ID.

        :param int mechanism_id: the mechanism ID to select the operating loads
            for.
        :parem str parent_id: the parent node ID the coperating loads are
            associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id) = parent_id.split('.')
        for _opload in self.dao.session.query(RAMSTKOpLoad).filter(
                RAMSTKOpLoad.hardware_id == self._parent_id,
                RAMSTKOpLoad.mode_id == int(_mode_id),
                RAMSTKOpLoad.mechanism_id == int(_mechanism_id)).all():

            _identifier = '{0:s}.{1:d}'.format(parent_id, _opload.load_id)

            self.tree.create_node(tag=_identifier,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'opload': _opload})

            self._do_select_all_opstress(_opload.load_id, _identifier)
            self._do_select_all_testmethod(_opload.load_id, _identifier)

    def _do_select_all_opstress(self, load_id, parent_id):
        """
        Retrieve all the operating stresses for the load ID.

        :param int load_id: the operating load ID to select the stresses for.
        :parem str parent_id: the parent node ID the operating stresses are
            associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _load_id) = parent_id.split('.')
        for _opstress in self.dao.session.query(RAMSTKOpStress).filter(
                RAMSTKOpStress.hardware_id == self._parent_id,
                RAMSTKOpStress.mode_id == int(_mode_id),
                RAMSTKOpStress.mechanism_id == int(_mechanism_id),
                RAMSTKOpStress.load_id == int(_load_id)).all():

            _identifier = '{0:s}.{1:d}.s'.format(parent_id,
                                                 _opstress.stress_id)

            self.tree.create_node(tag=_identifier,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'opstress': _opstress})

    def _do_select_all_testmethod(self, load_id, parent_id):
        """
        Retrieve all the test methods for the load ID.

        :param int load_id: the operating load ID to select the test methods
            for.
        :parem str parent_id: the parent node ID the test methods are
            associated with.
        :return: None
        :rtype: None
        """
        (_mode_id, _mechanism_id, _load_id) = parent_id.split('.')
        for _method in self.dao.session.query(RAMSTKTestMethod).filter(
                RAMSTKTestMethod.hardware_id == self._parent_id,
                RAMSTKTestMethod.mode_id == int(_mode_id),
                RAMSTKTestMethod.mechanism_id == int(_mechanism_id),
                RAMSTKTestMethod.load_id == int(_load_id)).all():

            _identifier = '{0:s}.{1:d}.t'.format(parent_id, _method.test_id)

            self.tree.create_node(tag=_identifier,
                                  identifier=_identifier,
                                  parent=parent_id,
                                  data={'testmethod': _method})

    def do_get_tree(self):
        """
        Retrieve the PoF treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_pof_tree', dmtree=self.tree)

    def do_select_all(self, parent_id):  # pylint: disable=arguments-differ
        """
        Retrieve all the PoF data from the RAMSTK Program database.

        :param int parent_id: the parent (function or hardware) ID to select
            the PoF for.
        :return: None
        :rtype: None
        """
        self._parent_id = parent_id

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _mode in self.dao.session.query(RAMSTKMode).filter(
                RAMSTKMode.hardware_id == self._parent_id).all():

            self.tree.create_node(tag=str(_mode.mode_id),
                                  identifier=str(_mode.mode_id),
                                  parent=self._root,
                                  data={'mode': _mode})

            self._do_select_all_mechanism(_mode.mode_id)

        pub.sendMessage('succeed_retrieve_pof', tree=self.tree)

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
            'mode': ['revision_id', 'hardware_id', 'mode_id'],
            'mechanism':
            ['revision_id', 'hardware_id', 'mode_id', 'mechanism_id'],
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

        _attributes = self.do_select(node_id, table=table).get_attributes()

        for _field in _poppers[table]:
            try:
                _attributes.pop(_field)
            except KeyError:
                pass

        if key in _attributes:
            _attributes[key] = value

            self.do_select(node_id, table=table).set_attributes(_attributes)

    def do_update(self, node_id):
        """
        Update the record associated with node ID in RAMSTK Program database.

        :param int node_id: the node ID of the PoF item to save.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]
            self.dao.session.add(self.tree.get_node(node_id).data[_table])

            self.dao.do_update()

            pub.sendMessage('succeed_update_pof', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_pof',
                            error_message=('Attempted to save non-existent '
                                           'PoF element with PoF ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_pof',
                                error_message=('No data package found for '
                                               'PoF ID {0:s}.').format(
                                                   str(node_id)))
