# -*- coding: utf-8 -*-
#
#       rtk.modules.revision.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Revision Package Data Model."""

# Import other RAMSTK modules.
from rtk.modules import RAMSTKDataModel
from rtk.dao import RAMSTKRevision


class RevisionDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a Revision.

    An RAMSTK Project will consist of one or more Revisions.  The attributes of a
    Revision are:
    """

    _tag = 'Revisions'

    def __init__(self, dao):
        """
        Initialize a Revision data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`rtk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_select_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Retrieve all the Revisions from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKRevision table in the
        connected RAMSTK Program database.  It then add each to the Revision data
        model treelib.Tree().

        :return: tree; the Tree() of RAMSTKRevision data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RAMSTKDataModel.do_select_all(self)

        for _revision in _session.query(RAMSTKRevision).all():
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
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _revision.revision_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RAMSTKRevision table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision = RAMSTKRevision()
        _error_code, _msg = RAMSTKDataModel.do_insert(
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
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = _revision.revision_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKRevision table.

        :param int node_id entity: the ID of the RAMSTKRevision record to be
                                   removed from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Revision ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param int node_id: the Revision ID of the Revision to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Revision ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKRevision table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(
                    _node.data.revision_id)
                _msg = _msg + _debug_msg + '\n'
            except AttributeError:
                _error_code = 1
                _msg = ("RAMSTK ERROR: One or more Revisions did not update.")

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all Revisions.")

        return _error_code, _msg
