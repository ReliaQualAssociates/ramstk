# -*- coding: utf-8 -*-
#
#       ramstk.controllers.revision.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKRevision


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Revision data manager.

    This class manages the revision data from the RAMSTKRevision,
    RAMSTKFailureDefinition, RAMSTKMission, RAMSTKMissionPhase, and
    RAMSKTEnvironment data models.
    """

    _tag = 'revision'

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Revision data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {'revision': ['revision_id']}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_all, 'request_retrieve_revisions')
        pub.subscribe(self._do_delete, 'request_delete_revision')
        pub.subscribe(self.do_insert, 'request_insert_revision')
        pub.subscribe(self.do_update, 'request_update_revision')
        pub.subscribe(self.do_update_all, 'request_update_all_revisions')
        pub.subscribe(self._do_get_attributes,
                      'request_get_revision_attributes')
        pub.subscribe(self.do_get_all_attributes,
                      'request_get_all_revision_attributes')
        pub.subscribe(self.do_get_tree, 'request_get_revision_tree')
        pub.subscribe(super().do_set_attributes,
                      'request_set_revision_attributes')
        pub.subscribe(super().do_set_attributes, 'wvw_editing_revision')
        pub.subscribe(self.do_set_all_attributes,
                      'request_set_all_revision_attributes')

    def do_get_all_attributes(self, node_id: int) -> None:
        """Retrieve all RAMSTK data tables' attributes for the revision.

        This is a helper method to be able to retrieve all the revision's
        attributes in a single call.  It's used primarily by the
        AnalysisManager.

        :param int node_id: the node (revision) ID of the revision item to
            get the attributes for.
        :return: None
        :rtype: None
        """
        _attributes = self.do_select(node_id,
                                     table='revision').get_attributes()

        pub.sendMessage('succeed_get_all_revision_attributes',
                        attributes=_attributes)

    def do_get_tree(self) -> None:
        """Retrieve the revision treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_revision_tree', dmtree=self.tree)

    # pylint: disable=arguments-differ
    def do_insert(self) -> None:
        """Add a new revision.

        :return: None
        :rtype: None
        :raise: AttributeError if not connected to a RAMSTK program database.
        """
        try:
            _last_id = self.dao.get_last_id('ramstk_revision', 'revision_id')
            _revision = RAMSTKRevision()
            _revision.revision_id = _last_id + 1
            _revision.name = 'New Revision'

            self.dao.do_insert(_revision)

            self.tree.create_node(tag=_revision.name,
                                  identifier=_revision.revision_id,
                                  parent=self._root,
                                  data={'revision': _revision})
            self.last_id = _revision.revision_id
            pub.sendMessage('succeed_insert_revision',
                            node_id=self.last_id,
                            tree=self.tree)
        except DataAccessError:
            pub.sendMessage("fail_insert_revision",
                            error_message=("Failed to insert revision into "
                                           "program database."))

    def do_select_all(self) -> None:
        """Retrieve all the Revision data from the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _revision in self.dao.do_select_all(
                RAMSTKRevision,
                key=None,
                value=None,
                order=RAMSTKRevision.revision_id):

            self.tree.create_node(tag=_revision.name,
                                  identifier=_revision.revision_id,
                                  parent=self._root,
                                  data={'revision': _revision})

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage('succeed_retrieve_revisions', tree=self.tree)

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the revision.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            super().do_set_attributes(node_id=[
                attributes['revision_id'],
            ],
                                      package={_key: attributes[_key]})

    def do_update(self, node_id: int) -> None:
        """Update record associated with node ID in RAMSTK Program database.

        :param int node_id: the node (revision) ID of the revision to save.
        :return: None
        :rtype: None
        """
        try:
            self.dao.do_update(self.tree.get_node(node_id).data['revision'])
            pub.sendMessage('succeed_update_revision', node_id=node_id)
        except AttributeError:
            pub.sendMessage('fail_update_revision',
                            error_message=('Attempted to save non-existent '
                                           'revision with revision ID '
                                           '{0:s}.').format(str(node_id)))
        except (KeyError, TypeError):
            if node_id != 0:
                pub.sendMessage('fail_update_revision',
                                error_message=('No data package found for '
                                               'revision ID {0:s}.').format(
                                                   str(node_id)))

    def _do_delete(self, node_id: int) -> None:
        """Remove a revision.

        :param int node_id: the node (revision) ID to be removed from the
            RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            super().do_delete(node_id, 'revision')

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage('succeed_delete_revision',
                            node_id=node_id,
                            tree=self.tree)
        except (DataAccessError, NodeIDAbsentError):
            _error_msg = ("Attempted to delete non-existent revision ID "
                          "{0:s}.").format(str(node_id))
            pub.sendMessage('fail_delete_revision', error_message=_error_msg)

    def _do_get_attributes(self, node_id: int) -> None:
        """Retrieve the RAMSTK data table attributes for the revision.

        :param node_id: the node (revision) ID of the revision to get the
            attributes for.
        :return: None
        :rtype: None
        """
        _attributes = self.do_select(node_id,
                                     table='revision').get_attributes()

        pub.sendMessage('succeed_get_revision_attributes',
                        attributes=_attributes)
