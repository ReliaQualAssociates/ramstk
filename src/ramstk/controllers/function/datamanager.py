# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Model."""

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKFunction, RAMSTKHazardAnalysis


class DataManager(RAMSTKDataManager):
    """
    Contain the attributes and methods of the Function data manager.

    This class manages the function data from the RAMSTKFunction and
    RAMSTKHazardAnalysis data models.
    """

    _tag = 'function'
    _root = 0

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize a Function data manager instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataManager.__init__(self, dao, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'succeed_select_revision')
        pub.subscribe(self._do_delete, 'request_delete_function')
        pub.subscribe(self._do_delete_hazard, 'request_delete_hazard')
        pub.subscribe(self.do_insert, 'request_insert_function')
        pub.subscribe(self.do_insert_hazard, 'request_insert_hazard')
        pub.subscribe(self.do_update, 'request_update_function')
        pub.subscribe(self.do_update_all, 'request_update_all_functions')
        pub.subscribe(self._do_get_attributes,
                      'request_get_function_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_function_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_function_tree')
        pub.subscribe(self.do_set_attributes,
                      'request_set_function_attributes')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_function_attributes')

    def _do_delete(self, node_id):
        """
        Remove a function.

        :param int node_id: the node (function) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            RAMSTKDataManager.do_delete(self, node_id, 'function')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_function', node_id=node_id)
        except(AttributeError, DataAccessError):
            _error_msg = ("Attempted to delete non-existent function ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_function', error_msg=_error_msg)

    def _do_delete_hazard(self, function_id, node_id):
        """
        Remove a hazard from function ID.

        :param int function_id: the function ID to remove the hazard from.
        :param int node_id: the node (hazard) ID to remove.
        :return: None
        :rtype: None
        """
        _hazards = RAMSTKDataManager.do_select(self, function_id, 'hazards')
        try:
            self.dao.do_delete(_hazards[node_id])

            _hazards.pop(node_id)
            self.tree.get_node(function_id).data['hazards'] = _hazards

            pub.sendMessage('succeed_delete_hazard', node_id=node_id)
        except(DataAccessError, KeyError):
            pub.sendMessage('fail_delete_hazard',
                            error_msg=("Attempted to delete non-existent "
                                       "hazard ID {0:s} from function ID "
                                       "{1:s}.").format(
                                           str(node_id), str(function_id)))

    def _do_get_attributes(self, node_id, table):
        """
        Retrieve the RAMSTK data table attributes for the function.

        .. important:: the failure definition will return a dict of all the
            failure definitions associated with the node (function) ID.  This
            dict uses the definition ID as the key and the instance of the
            RAMSTKFailureDefinition as the value.  The subscibing methods and
            functions will need to unpack this dict.

        .. important:: the usage profile will return a treelib Tree() of all
            the usage profiles associated with the node (function) ID.  The
            subscribing methods and functions will need to parse this Tree().

        :param int node_id: the node (function) ID of the function to get the
            attributes for.
        :param str table: the RAMSTK data table to retrieve the attributes
            from.
        :return: None
        :rtype: None
        """
        if table in ['hazards']:
            _attributes = self.do_select(node_id, table=table)
        else:
            _attributes = self.do_select(node_id, table=table).get_attributes()

        pub.sendMessage('succeed_get_{0:s}_attributes'.format(table),
                        attributes=_attributes)

    def _do_set_hazard(self, node_id, key, value, hazard_id):
        """
        Set the attributes of the record associated with hazard ID.

        This is a helper method to set the desired hazard analysis attribute
        since the hazard analyses are carried in a dict and we need to
        select the correct record to update.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :param int hazard_id: the hazard ID if the attribute being set is a
            hazard analysis attribute.
        :return: None
        :rtype: None
        """
        try:
            _attributes = self.do_select(
                node_id, table='hazards')[hazard_id].get_attributes()
            _attributes.pop('revision_id')
            _attributes.pop('function_id')
            _attributes.pop('hazard_id')
        except KeyError:
            _attributes = {}

        if key in _attributes:
            _attributes[key] = value
            self.do_select(
                node_id,
                table='hazards')[hazard_id].set_attributes(_attributes)

    def do_get_all_attributes(self, node_id):
        """
        Retrieve all RAMSTK data tables' attributes for the function.

        This is a helper method to be able to retrieve all the function's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param int node_id: the node (function) ID of the function item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes = {'hazards': {}}
        for _table in ['function', 'hazards']:
            if _table == 'hazards':
                _attributes['hazards'].update(
                    self.do_select(node_id, table=_table))
            else:
                _attributes.update(
                    self.do_select(node_id, table=_table).get_attributes())

        pub.sendMessage('succeed_get_all_function_attributes',
                        attributes=_attributes)

    def do_get_tree(self):
        """
        Retrieve the function treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_function_tree', dmtree=self.tree)

    def do_insert(self, parent_id=0):  # pylint: disable=arguments-differ
        """
        Add a new function as child of the parent ID function.

        :param int parent_id: the parent (function) ID of the function to
            insert the child.  Default is to add a top-level function.
        :return: None
        :rtype: None
        """
        _tree = Tree()

        if self.tree.get_node(parent_id) is not None:
            try:
                _function = RAMSTKFunction(revision_id=self._revision_id,
                                           name='New Function',
                                           parent_id=parent_id)
                self.dao.do_insert(_function)

                self.last_id = _function.function_id

                _data_package = {'function': _function, 'hazards': {}}
                self.tree.create_node(tag=_function.name,
                                      identifier=_function.function_id,
                                      parent=_function.parent_id,
                                      data=_data_package)

                pub.sendMessage('succeed_insert_function',
                                node_id=self.last_id)
            except DataAccessError as _error:
                print(_error)
                pub.sendMessage("fail_insert_function", error_msg=_error)
        else:
            pub.sendMessage("fail_insert_function",
                            error_msg=("Attempting to add a function as a "
                                       "child of non-existent parent node "
                                       "{0:s}.".format(str(parent_id))))

    def do_insert_hazard(self, function_id):
        """
        Add a new hazard to function ID.

        :param int function_id: the function ID to associate the new hazard
            with.
        :return: None
        :rtype: None
        """
        _node = self.tree.get_node(function_id)

        if _node is not None:
            try:
                _hazard = RAMSTKHazardAnalysis(revision_id=self._revision_id,
                                               function_id=function_id)
                self.dao.do_insert(_hazard)

                _node.data['hazards'][_hazard.hazard_id] = _hazard

                pub.sendMessage('succeed_insert_hazard',
                                node_id=_hazard.hazard_id)
            except DataAccessError as _error:
                print(_error)
                pub.sendMessage("fail_insert_hazard", error_msg=_error)
        else:
            pub.sendMessage("fail_insert_hazard",
                            error_msg=("Attempting to add a hazard to a "
                                       "non-existent function ID "
                                       "{0:s}.".format(str(function_id))))

    def do_select_all(self, revision_id):  # pylint: disable=arguments-differ
        """
        Retrieve all the Function data from the RAMSTK Program database.

        :param int revision_id: the Revision ID to select the Functions for.
        :return: None
        :rtype: None
        """
        self._revision_id = revision_id

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _function in self.dao.session.query(RAMSTKFunction).filter(
                RAMSTKFunction.revision_id == self._revision_id).all():

            _hazards = self.dao.session.query(RAMSTKHazardAnalysis).filter(
                RAMSTKHazardAnalysis.function_id ==
                _function.function_id).all()
            _hazards = self.do_build_dict(_hazards, 'hazard_id')

            _data_package = {
                'function': _function,
                'hazards': _hazards,
            }

            self.tree.create_node(tag=_function.name,
                                  identifier=_function.function_id,
                                  parent=_function.parent_id,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_functions', tree=self.tree)

    def do_set_all_attributes(self, attributes, hazard_id=None):
        """
        Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param dict attributes: the aggregate attributes dict for the function.
        :keyword int hazard_id: the hazard ID if the attribute being set is a
            hazard analysis attribute.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(attributes['function_id'], _key,
                                   attributes[_key], hazard_id)

    def do_set_attributes(self, node_id, key, value, hazard_id=None):
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :keyword int hazard_id: the hazard ID if the attribute being set is a
            hazard analysis attribute.
        :return: None
        :rtype: None
        """
        for _table in ['function', 'hazards']:
            if _table == 'hazards':
                self._do_set_hazard(node_id, key, value, hazard_id)
            else:
                _attributes = self.do_select(node_id,
                                             table=_table).get_attributes()
                if key in _attributes:
                    _attributes[key] = value

                    try:
                        _attributes.pop('revision_id')
                        _attributes.pop('function_id')
                    except KeyError:
                        pass

                    self.do_select(node_id,
                                   table=_table).set_attributes(_attributes)

    def do_update(self, node_id):
        """
        Update the record associated with node ID in RAMSTK Program database.

        .. note:: This will also update all the hazards associated with the
            function.

        :param int node_id: the node (function) ID of the function to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.session.add(self.tree.get_node(node_id).data['function'])
            for _key in self.tree.get_node(node_id).data['hazards']:
                self.dao.session.add(
                    self.tree.get_node(node_id).data['hazards'][_key])

            self.dao.do_update()
            pub.sendMessage('succeed_update_function', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_function',
                            error_msg=('Attempted to save non-existent '
                                       'function with function ID '
                                       '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_function',
                                error_msg=('No data package found for '
                                           'function ID {0:s}.').format(
                                               str(node_id)))
