# -*- coding: utf-8 -*-
#
#       rtk.datamodels.RTKDataModel.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Datamodels Package RTKDataModel."""

from treelib import tree, Tree  # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKDataModel(object):
    """
    This is the meta-class for all RTK Data Models.

    :ivar tree: the :class:`treelib.Tree` that will contain the structure
                of the RTK module being modeled..
    :ivar dao: the :class:`rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    def __init__(self, dao):
        """
        Method to initialize an RTK data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
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
        # Tree().  Manipulation and viewing of a RTK module tree needs to
        # ignore the root of the tree.
        try:
            self.tree.create_node(tag=self._tag, identifier=0, parent=None)
        except (tree.MultipleRootError, tree.NodeIDAbsentError,
                tree.DuplicatedNodeIdError):
            pass

    def select(self, node_id):
        """
        Base method to retrieve the instance of the RTK<MODULE> model for the
        Node ID passed.

        :param int node_id: the Node ID Of the data package to retrieve.
        :return: the instance of the RTK<MODULE> class that was requested
                 or None if the requested Node ID does not exist.
        """
        try:
            _entity = self.tree.get_node(node_id).data
        except AttributeError:
            _entity = None
        except tree.NodeIDAbsentError:
            _entity = None

        return _entity

    def select_all(self):
        """
        Retrieve and build the RTK Module tree.

        :return: an SQLAlchemy session instance.
        :rtype:
        """
        _root = self.tree.root
        for _node in self.tree.children(_root):
            self.tree.remove_node(_node.identifier)

        return self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

    def insert(self, **kwargs):
        """
        Add the list of RTK<MODULE> instance to the RTK Program database.

        :param list entities: the list of RTK<MODULE> entities to add to the
                              RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _entities = kwargs['entities']
        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        _error_code, _msg = self.dao.db_add(_entities, _session)

        _session.close()

        return _error_code, _msg

    def delete(self, node_id):
        """
        Base method to remove the instance of RTK<MODULE> from the RTK Program
        database.

        :param int node_id entity: the ID of the RTK<MODULE> record to be
                                   removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _msg = ''

        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        try:
            _entity = self.tree.get_node(node_id).data
            _error_code, _msg = self.dao.db_delete(_entity, _session)

            if _error_code == 0:
                self.tree.remove_node(node_id)

        except AttributeError:
            _error_code = 2005

        _session.close()

        return _error_code, _msg

    def update(self, node_id):
        """
        Base method to update the RTK<MODULE> instance in the RTK Program
        database.

        :param entity: the RTK<MODULE> instance to update in the RTK Program
                       database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = ''

        _session = self.dao.RTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        try:
            _entity = self.tree.get_node(node_id).data
            if _entity is not None:
                _session.add(_entity)
                _error_code, _msg = self.dao.db_update(_session)
        except AttributeError:
            _error_code = 6
            _msg = 'RTK ERROR: Attempted to save non-existent entity ' \
                   'with Node ID {0:s}.'.format(str(node_id))

        _session.close()

        return _error_code, _msg
