# -*- coding: utf-8 -*-
#
#       rtk.datamodels.RTKDataModel.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
RTKDataModel Module
###############################################################################
"""

from treelib import tree, Tree

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKDataModel(object):
    """
    This is the meta-class for all RTK Data Models.

    :ivar tree: the :py:class:`treelib.Tree` that will contain the structure
                of the RTK module being modeled..
    :ivar dao: the :py:class:`rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    """

    def __init__(self, dao):
        """
        Method to initialize an RTK data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :py:class:`rtk.dao.DAO.DAO`
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

        # Add the root to the Tree().  This is neccessary to allow multiple
        # entries at the top level as there can only be one root in a treelib
        # Tree().  Manipulation and viewing of a RTK module tree needs to
        # ignore the root of the tree.
        try:
            self.tree.create_node(tag=self._tag, identifier=0,
                                  parent=None)
        except(tree.MultipleRootError, tree.NodeIDAbsentError,
               tree.DuplicatedNodeIdError):
            pass

    def select(self, node_id):
        """
        Base method to retrieve the instance of the RTK<Module> model for the
        Node ID passed.

        :param int node_id: the Node ID Of the data package to retrieve.
        :return: the instance of the RTK<Module> class that was requested
                 or None if the requested Node ID does not exist.
        """

        try:
            _entity = self.tree.get_node(node_id).data
        except AttributeError:
            _entity = None
        except tree.NodeIDAbsentError:
            _entity = None

        return _entity

    def select_all(self, **kwargs):
        """
        Base method to retrieve and build the RTK Module tree.

        :return: an SQLAlchemy session instance.
        :rtype:
        """

        _root = self.tree.root
        for _node in self.tree.children(_root):
            self.tree.remove_node(_node.identifier)

        return self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                    expire_on_commit=False)

    def insert(self, entities):
        """
        Base method to add the list of RTK<Module> instance to the RTK Program
        database.

        :param list entities: the list of RTK<Module> entities to add to the
                              RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        _error_code, _msg = self.dao.db_add(entities, _session)

        _session.close()

        return _error_code, _msg

    def delete(self, entity):
        """
        Base method to remove the instance of RTK<Module> from the RTK Program
        database.

        :param entity: the instance of the RTK<Module> to be removed from the
                       RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        _error_code, _msg = self.dao.db_delete(entity, _session)

        _session.close()

        return _error_code, _msg

    def update(self, entity):
        """
        Base method to update the RTK<Module> instance in the RTK Program
        database.

        :param entity: the RTK<Module> instance to update in the RTK Program
                       database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        # TODO: Refactor rtk.datamodels.RTKDataModel.update().

        # Update RTKDataModel.update().  Convert to commented code which will
        # require updating every class that sources RTKDataModel.  Change
        # paramater from entity to node_id.

        # _error_code = 0

        # _session = self.dao.RTK_SESSION(bind=self.dao.engine,
        #                                 autoflush=True,
        #                                 autocommit=False,
        #                                 expire_on_commit=False)

        # try:
        #     _entity = self.tree.get_node(node_id).data
        # except AttributeError:
        #    _error_code = 6

        # if _error_code == 0:
        #     _session.add(_entity)
        #     _error_code, _msg = self.dao.db_update(_session)

        # _session.close()

        # return _error_code
        # Delete the following code.
        _session = self.dao.RTK_SESSION(bind=self.dao.engine,
                                        autoflush=True,
                                        autocommit=False,
                                        expire_on_commit=False)
        _session.add(entity)
        _error_code, _msg = self.dao.db_update(_session)

        _session.close()

        return _error_code, _msg
