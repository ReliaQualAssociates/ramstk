# -*- coding: utf-8 -*-
#
#       rtk.modules.revision.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Import other RTK modules.
from rtk.modules import RTKDataModel
from rtk.dao import RTKRevision


class RevisionDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Revision.

    An RTK Project will consist of one or more Revisions.  The attributes of a
    Revision are:
    """

    _tag = 'Revisions'

    def __init__(self, dao):
        """
        Initialize a Revision data model instance.

        :param dao: the data access object for communicating with the RTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Retrieve all the Revisions from the RTK Program database.

        This method retrieves all the records from the RTKRevision table in the
        connected RTK Program database.  It then add each to the Revision data
        model treelib.Tree().

        :return: tree; the Tree() of RTKRevision data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.do_select_all(self)

        for _revision in _session.query(RTKRevision).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _revision.get_attributes()
            _revision.set_attributes(_attributes)
            self.tree.create_node(
                _revision.name,
                _revision.revision_id,
                parent=0,
                data=_revision)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _revision.revision_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RTKRevision table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision = RTKRevision()
        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _revision,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _revision.name,
                _revision.revision_id,
                parent=0,
                data=_revision)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _revision.revision_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RTKRevision table.

        :param int node_id entity: the ID of the RTKRevision record to be
                                   removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Revision ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the Revision ID of the Revision to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Revision ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RTKRevision table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''
        print self.tree.all_nodes()
        for _node in self.tree.all_nodes():
            print _node
            try:
                _error_code, _debug_msg = self.do_update(
                    _node.data.revision_id)
                _msg = _msg + _debug_msg + '\n'
            except AttributeError:
                _error_code = 1
                _msg = ("RTK ERROR: One or more Revisions did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all Revisions.")

        return _error_code, _msg
