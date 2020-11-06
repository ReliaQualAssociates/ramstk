# -*- coding: utf-8 -*-
#
#       ramstk.controllers.stakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKStakeholder


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Stakeholder data manager.

    This class manages the stakeholder data from the RAMSTKStakeholder
    and RAMSTKStakeholder data models.
    """

    _tag = 'stakeholder'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Stakeholder data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'stakeholder': ['revision_id', 'stakeholder_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes,
                      'request_get_stakeholder_attributes')
        pub.subscribe(super().do_set_attributes,
                      'request_set_stakeholder_attributes')
        pub.subscribe(super().do_set_attributes, 'lvw_editing_stakeholder')
        pub.subscribe(super().do_update_all, 'request_update_all_stakeholders')

        pub.subscribe(self.do_select_all, 'selected_revision')
        pub.subscribe(self.do_update_stakeholder, 'request_update_stakeholder')
        pub.subscribe(self.do_get_tree, 'request_get_stakeholder_tree')

        pub.subscribe(self._do_delete_stakeholder,
                      'request_delete_stakeholder')
        pub.subscribe(self._do_insert_stakeholder,
                      'request_insert_stakeholder')

    def _do_delete_stakeholder(self, node_id: int) -> None:
        """Remove a stakeholder.

        :param int node_id: the node (stakeholder) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'stakeholder')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_stakeholder_', node_id=node_id)
            pub.sendMessage('succeed_delete_stakeholder',
                            node_id=node_id,
                            tree=self.tree)
        except DataAccessError:
            _error_msg = ("Attempted to delete non-existent stakeholder ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_stakeholder',
                            error_message=_error_msg)

    def do_get_tree(self) -> None:
        """Retrieve the stakeholder treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_stakeholder_tree', dmtree=self.tree)


    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Stakeholder data from the RAMSTK Program database.

        :param dict attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes['revision_id']

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _stakeholder in self.dao.do_select_all(
                RAMSTKStakeholder,
                key=RAMSTKStakeholder.revision_id,
                value=self._revision_id,
                order=RAMSTKStakeholder.stakeholder_id):
            _data_package = {'stakeholder': _stakeholder}

            self.tree.create_node(tag=_stakeholder.description,
                                  identifier=_stakeholder.stakeholder_id,
                                  parent=self._root,
                                  data=_data_package)

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_stakeholders', tree=self.tree)

    def do_update_stakeholder(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param node_id: the node (stakeholder) ID of the stakeholder to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['stakeholder'])

            pub.sendMessage('succeed_update_stakeholder', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_stakeholder',
                            error_message=('Attempted to save non-existent '
                                           'stakeholder with stakeholder ID '
                                           '{0:s}.').format(str(node_id)))
        except (KeyError, TypeError):
            if node_id != 0:
                pub.sendMessage('fail_update_stakeholder',
                                error_message=('No data package found for '
                                               'stakeholder ID {0:s}.').format(
                                                   str(node_id)))
    def _do_insert_stakeholder(self) -> None:
        """Add a new stakeholder.

        :return: None
        :rtype: None
        """
        try:
            _stakeholder = RAMSTKStakeholder()
            _stakeholder.revision_id = self._revision_id
            _stakeholder.stakeholder_id = self.last_id + 1
            _stakeholder.description = 'New Stakeholder Input'

            self.dao.do_insert(_stakeholder)

            self.last_id = _stakeholder.stakeholder_id
            self.tree.create_node(tag=_stakeholder.description,
                                  identifier=self.last_id,
                                  parent=0,
                                  data={'stakeholder': _stakeholder})
            pub.sendMessage('succeed_insert_stakeholder_2',
                            node_id=self.last_id)
            pub.sendMessage('succeed_insert_stakeholder',
                            node_id=self.last_id,
                            tree=self.tree)
        except DataAccessError as _error:
            pub.sendMessage("fail_insert_stakeholder",
                            error_message=_error.msg)
