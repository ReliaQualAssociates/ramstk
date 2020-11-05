# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hazards.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hazards Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKHazardAnalysis


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Hazard data manager.

    This class manages the hazard data from the RAMSTKHazardAnalysis and
    RAMSTKHazardAnalysis data models.
    """

    _tag = 'hazards'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Hazard data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'hazard': ['revision_id', 'function_id', 'hazard_id']}

        # Initialize private list attributes.
        self._last_id = [0, 0]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_insert_hazard, 'request_insert_hazard')
        pub.subscribe(self.do_update, 'request_update_hazard')
        pub.subscribe(self.do_update_all, 'request_update_all_hazards')
        pub.subscribe(super().do_get_attributes,
                      'request_get_hazard_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_hazard_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_hazard_tree')
        pub.subscribe(super().do_set_attributes,
                      'request_set_hazard_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_hazard')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_hazard_attributes')

        pub.subscribe(self._do_delete_hazard, 'request_delete_hazard')

    def _do_delete_hazard(self, node_id: int) -> None:
        """Remove a hazard.

        :param int node_id: the node (hazard) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'hazard')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_hazard',
                            node_id=node_id,
                            tree=self.tree)
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _error_message = ("Attempted to delete non-existent hazard ID "
                              "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_hazard', error_message=_error_message)

    def _do_set_hazard(self, node_id: List, package: Dict) -> None:
        """Set the attributes of the record associated with hazard ID.

        This is a helper method to set the desired hazard analysis attribute
        since the hazard analyses are carried in a dict and we need to
        select the correct record to update.

        :param list node_id: a list of the ID's of the record in the RAMSTK
            Program database table whose attributes are to be set.  The list
            is:

                0 - Hazard ID
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
            _attributes.pop('hazard_id')
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
        """Retrieve all RAMSTK data tables' attributes for the hazard.

        This is a helper method to be able to retrieve all the hazard's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param node_id: the node (hazard) ID of the hazard item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes = self.do_select(node_id, table='hazard').get_attributes()

        pub.sendMessage('succeed_get_all_hazard_attributes',
                        attributes=_attributes)

    def do_get_tree(self) -> None:
        """Retrieve the hazard treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_hazard_tree', dmtree=self.tree)

    def do_insert_hazard(self, parent_id: int = 0) -> None:
        """Add a new hazard to parent (function) ID.

        :param parent_id: the parent (function) ID to associate the new hazard
        with.
        :return: None
        :rtype: None
        """
        _last_id = self.dao.get_last_id('ramstk_hazard_analysis', 'hazard_id')
        try:
            _hazard = RAMSTKHazardAnalysis()
            _hazard.revision_id = self._revision_id
            _hazard.function_id = parent_id
            _hazard.hazard_id = _last_id + 1

            self.dao.do_insert(_hazard)

            self.tree.create_node(tag=_hazard.potential_hazard,
                                  identifier=_hazard.hazard_id,
                                  parent=self._root,
                                  data={'hazard': _hazard})

            self._last_id[0] = _hazard.hazard_id
            self.last_id = _hazard.hazard_id

            pub.sendMessage('succeed_insert_hazard',
                            node_id=self.last_id,
                            tree=self.tree)
        except DataAccessError as _error:
            print(_error)
            pub.sendMessage("fail_insert_hazard", error_message=_error)

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Hazard data from the RAMSTK Program database.

        :param dict attributes: the attributes for the selected Hazard.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _hazard in self.dao.do_select_all(
                RAMSTKHazardAnalysis,
                key=RAMSTKHazardAnalysis.revision_id,
                value=self._revision_id,
                order=RAMSTKHazardAnalysis.hazard_id):

            _hazards = self.dao.do_select_all(
                RAMSTKHazardAnalysis,
                key=RAMSTKHazardAnalysis.hazard_id,
                value=_hazard.hazard_id,
                order=RAMSTKHazardAnalysis.hazard_id)
            _hazards = self.do_build_dict(_hazards, 'hazard_id')

            self.tree.create_node(tag=_hazard.potential_hazard,
                                  identifier=_hazard.hazard_id,
                                  parent=self._root,
                                  data={'hazard': _hazard})

            try:
                self._last_id[0] = max(self._last_id[0], max(_hazards.keys()))
            except ValueError:
                self._last_id[0] = self._last_id[0]

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_hazards', tree=self.tree)

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the record associated with the Module ID.

        This is a helper hazard to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the hazard.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            self.do_set_attributes(node_id=[
                attributes['hazard_id'],
            ],
                                   package={_key: attributes[_key]})

    def do_update(self, node_id: int) -> None:
        """Update the record associated with node ID in RAMSTK Program
        database.

        :param node_id: the node (hazard) ID of the hazard to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['hazard'])
            for _key in self.tree.get_node(node_id).data['hazard']:
                self.dao.do_update(
                    self.tree.get_node(node_id).data['hazard'][_key])

            pub.sendMessage('succeed_update_hazard', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_hazard',
                            error_message=('Attempted to save non-existent '
                                           'hazard with hazard ID '
                                           '{0:s}.').format(str(node_id)))
        except TypeError:
            if node_id != 0:
                pub.sendMessage('fail_update_hazard',
                                error_message=('No data package found for '
                                               'hazard ID {0:s}.').format(
                                                   str(node_id)))
