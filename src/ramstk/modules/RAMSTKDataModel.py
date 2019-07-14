# -*- coding: utf-8 -*-
#
#       ramstk.modules.RAMSTKDataModel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Datamodels Package RAMSTKDataModel."""

# Third Party Imports
from treelib import Tree, tree  # pylint: disable=E0401


class RAMSTKDataModel():
    """
    This is the meta-class for all RAMSTK Data Models.

    :ivar tree: the :class:`treelib.Tree` that will contain the
                structure of the RAMSTK module being modeled..
    :ivar dao: the :class:`ramstk.dao.DAO` object used to communicate
               with the RAMSTK Program database.
    """

    def __init__(self, dao):
        """
        Initialize an RAMSTK data model instance.

        :param dao: the data access object for communicating with the
                    RAMSTK Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._last_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = dao
        self.tree = Tree()
        self.last_id = None

        # Add the root to the Tree().  This is neccessary to allow multiple
        # entries at the top level as there can only be one root in a treelib
        # Tree().  Manipulation and viewing of a RAMSTK module tree needs to
        # ignore the root of the tree.
        try:
            self.tree.create_node(
                tag=self._tag, identifier=self._root,
                parent=None,
            )
        except (
                tree.MultipleRootError, tree.NodeIDAbsentError,
                tree.DuplicatedNodeIdError,
        ):
            pass

    def do_calculate_all(self, **kwargs):
        """
        Calculate metrics for all RAMSTK<MODULE>s.

        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes()[1:]:
            if int(_node.identifier) != 0:
                self.do_calculate(_node.identifier, **kwargs)

    def do_select(self, node_id, **kwargs):  # pylint: disable=unused-argument
        """
        Retrieve instance of the RAMSTK<MODULE> model for the Node ID passed.

        :param int node_id: the Node ID of the data package to retrieve.
        :return: the instance of the RAMSTK<MODULE> class that was requested
            or None if the requested Node ID does not exist.
        """
        try:
            _entity = self.tree.get_node(node_id).data
        except AttributeError:
            _entity = None
        except tree.NodeIDAbsentError:
            _entity = None

        return _entity

    def do_select_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Retrieve and build the RAMSTK Module tree.

        :return: an SQLAlchemy session instance.
        :rtype:
        """
        _root = self.tree.root
        for _node in self.tree.children(_root):
            self.tree.remove_node(_node.identifier)

        return self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

    def do_insert(self, **kwargs):
        """
        Add the list of RAMSTK<MODULE> instance to the RAMSTK Program database.

        :param list entities: the list of RAMSTK<MODULE> entities to add to the
            RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _entities = kwargs['entities']
        return self.dao.db_add(_entities, None)

    def do_delete(self, node_id):
        """
        Delete the instance of RAMSTK<MODULE> from the RAMSTK Program database.

        :param int node_id entity: the ID of the RAMSTK<MODULE> record to be
                                   removed from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _msg = ''

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False,
        )

        try:
            _entity = self.tree.get_node(node_id).data
            _error_code, _msg = self.dao.db_delete(_entity, _session)

            if _error_code == 0:
                self.tree.remove_node(node_id)

        except AttributeError:
            _error_code = 2005

        _session.close()

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the RAMSTK<MODULE> instance in the RAMSTK Program database.

        :param entity: the RAMSTK<MODULE> instance to update in the RAMSTK
                       Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )

        try:
            _entity = self.tree.get_node(node_id).data
            if _entity is not None:
                _session.add(_entity)
                _error_code, _msg = self.dao.db_update(_session)
        except AttributeError:
            _error_code = 1
            _msg = (
                'RAMSTK ERROR: Attempted to save non-existent '
                'entity with Node ID {0:s}.'
            ).format(str(node_id))

        _session.close()

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTK<MODULE> table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)
            except AttributeError:
                _error_code = 1
                _debug_msg = (
                    'RAMSTK ERROR: Attempted to save non-existent '
                    'entity with Node ID {0:s}.'
                ).format(str(_node.identifier))

            _msg = _msg + _debug_msg + '\n'

        return _error_code, _msg
