# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

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

    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        """Initialize a Function data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._last_id = [0, 0]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self._do_delete, 'request_delete_function')
        pub.subscribe(self._do_delete_hazard, 'request_delete_hazard')
        pub.subscribe(self.do_insert, 'request_insert_function')
        pub.subscribe(self.do_insert_hazard, 'request_insert_hazard')
        pub.subscribe(self.do_update, 'request_update_function')
        pub.subscribe(self.do_update, 'request_update_hazard')
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
        pub.subscribe(self.do_set_attributes, 'wvw_editing_function')
        pub.subscribe(self.do_set_attributes, 'wvw_editing_hazard')

    def _do_delete(self, node_id: int) -> None:
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

            pub.sendMessage('succeed_delete_function',
                            node_id=node_id,
                            tree=self.tree)
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _error_message = ("Attempted to delete non-existent function ID "
                              "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_function',
                            error_message=_error_message)

    def _do_delete_hazard(self, function_id: int, node_id: int) -> None:
        """
        Remove a hazard from function ID.

        :param int function_id: the function ID to remove the hazard from.
        :param int node_id: the node (hazard) ID to remove.
        :return: None
        :rtype: None
        """
        _hazards = super().do_select(function_id, 'hazards')
        try:
            self.dao.do_delete(_hazards[node_id])

            _hazards.pop(node_id)
            self.tree.get_node(function_id).data['hazards'] = _hazards

            pub.sendMessage('succeed_delete_hazard', node_id=node_id)
        except (DataAccessError, KeyError):
            pub.sendMessage('fail_delete_hazard',
                            error_message=("Attempted to delete non-existent "
                                           "hazard ID {0:s} from function ID "
                                           "{1:s}.").format(
                                               str(node_id), str(function_id)))

    def _do_get_attributes(self, node_id: int, table: str) -> None:
        """
        Retrieve the RAMSTK data table attributes for the function.

        .. important:: the failure definition will return a dict of all the
            failure definitions associated with the node (function) ID.  This
            dict uses the definition ID as the key and the instance of the
            RAMSTKFailureDefinition as the value.  The subscribing methods and
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

    def _do_set_hazard(self, node_id: List, package: Dict) -> None:
        """
        Set the attributes of the record associated with hazard ID.

        This is a helper method to set the desired hazard analysis attribute
        since the hazard analyses are carried in a dict and we need to
        select the correct record to update.

        :param list node_id: a list of the ID's of the record in the RAMSTK
            Program database table whose attributes are to be set.  The list
            is:

                0 - Function ID
                1 - Hazard ID
                2 - FMEA ID

        :param dict package: the key:value for the attribute being updated.
        :return: None
        :rtype: None
        """
        try:
            _attributes = self.do_select(
                node_id[0], table='hazards')[node_id[1]].get_attributes()
            _attributes.pop('revision_id')
            _attributes.pop('function_id')
            _attributes.pop('hazard_id')
        except KeyError:
            _attributes = {}

        for _key in list(package.keys()):
            if _key in _attributes:
                _attributes[_key] = package[_key]
                self.do_select(
                    node_id[0],
                    table='hazards')[node_id[1]].set_attributes(_attributes)

    def do_get_all_attributes(self, node_id: int) -> None:
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

    def do_get_tree(self) -> None:
        """
        Retrieve the function treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_function_tree', dmtree=self.tree)

    # pylint: disable=arguments-differ
    def do_insert(self, parent_id: int = 0) -> None:
        """
        Add a new function as child of the parent ID function.

        :param int parent_id: the parent (function) ID of the function to
            insert the child.  Default is to add a top-level function.
        :return: None
        :rtype: None
        """
        if self.tree.get_node(parent_id) is not None:
            _last_id = self.dao.get_last_id('ramstk_function', 'function_id')
            try:
                _function = RAMSTKFunction(revision_id=self._revision_id,
                                           function_id=_last_id + 1,
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
                                node_id=self.last_id,
                                tree=self.tree)
            except DataAccessError as _error:
                print(_error)
                pub.sendMessage("fail_insert_function", error_message=_error)
        else:
            pub.sendMessage("fail_insert_function",
                            error_message=("Attempting to add a function as a "
                                           "child of non-existent parent node "
                                           "{0:s}.".format(str(parent_id))))

    def do_insert_hazard(self, function_id: int) -> None:
        """
        Add a new hazard to function ID.

        :param int function_id: the function ID to associate the new hazard
            with.
        :return: None
        :rtype: None
        """
        _node = self.tree.get_node(function_id)

        if _node is not None:
            _last_id = self.dao.get_last_id('ramstk_hazard_analysis',
                                            'hazard_id')
            try:
                _hazard = RAMSTKHazardAnalysis(revision_id=self._revision_id,
                                               function_id=function_id,
                                               hazard_id=_last_id + 1)
                self.dao.do_insert(_hazard)

                self._last_id[1] = _hazard.hazard_id

                _node.data['hazards'][_hazard.hazard_id] = _hazard

                pub.sendMessage('succeed_insert_hazard',
                                node_id=_hazard.hazard_id)
            except DataAccessError as _error:
                print(_error)
                pub.sendMessage("fail_insert_hazard", error_message=_error)
        else:
            pub.sendMessage("fail_insert_hazard",
                            error_message=("Attempting to add a hazard to a "
                                           "non-existent function ID "
                                           "{0:s}.".format(str(function_id))))

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """
        Retrieve all the Function data from the RAMSTK Program database.

        :param dict attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _function in self.dao.do_select_all(
                RAMSTKFunction,
                key=RAMSTKFunction.revision_id,
                value=self._revision_id,
                order=RAMSTKFunction.function_id):

            _hazards = self.dao.do_select_all(
                RAMSTKHazardAnalysis,
                key=RAMSTKHazardAnalysis.function_id,
                value=_function.function_id,
                order=RAMSTKHazardAnalysis.hazard_id)
            _hazards = self.do_build_dict(_hazards, 'hazard_id')

            try:
                self._last_id[1] = max(self._last_id[1], max(_hazards.keys()))
            except ValueError:
                self._last_id[1] = self._last_id[1]

            _data_package = {'function': _function, 'hazards': _hazards}

            self.tree.create_node(tag=_function.name,
                                  identifier=_function.function_id,
                                  parent=_function.parent_id,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_functions', tree=self.tree)

    def do_set_all_attributes(self,
                              attributes: Dict[str, Any],
                              hazard_id: int = None) -> None:
        """
        Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param dict attributes: the aggregate attributes dict for the function.
        :param int hazard_id: the hazard ID if the attribute being set is a
            hazard analysis attribute.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(
                node_id=[attributes['function_id'], hazard_id, ''],
                package={_key: attributes[_key]})

    def do_set_attributes(self, node_id: List, package: Dict) -> None:
        """
        Set the attributes of the record associated with the Module ID.

        :param list node_id: a list of the ID's of the record in the RAMSTK
            Program database table whose attributes are to be set.  The list
            is:

                0 - Function ID
                1 - Hazard ID
                2 - FMEA ID

        :param dict package: the key:value for the attribute being updated.
        :return: None
        :rtype: None
        """
        [[_key, _value]] = package.items()

        for _table in ['function', 'hazards']:
            if _table == 'hazards':
                self._do_set_hazard(node_id, package)
            else:
                _attributes = self.do_select(node_id[0],
                                             table=_table).get_attributes()
                if _key in _attributes:
                    _attributes[_key] = _value

                    try:
                        _attributes.pop('revision_id')
                        _attributes.pop('function_id')
                        _attributes.pop('hazard_id')
                    except KeyError:
                        pass

                    self.do_select(node_id[0],
                                   table=_table).set_attributes(_attributes)

    def do_update(self, node_id: int) -> None:
        """
        Update the record associated with node ID in RAMSTK Program database.

        .. note:: This will also update all the hazards associated with the
            function.

        :param int node_id: the node (function) ID of the function to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['function'])
            for _key in self.tree.get_node(node_id).data['hazards']:
                self.dao.do_update(
                    self.tree.get_node(node_id).data['hazards'][_key])

            pub.sendMessage('succeed_update_function', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_function',
                            error_message=('Attempted to save non-existent '
                                           'function with function ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            pub.sendMessage('fail_update_function',
                            error_message=('No data package found for '
                                           'function ID {0:s}.').format(
                                               str(node_id)))
