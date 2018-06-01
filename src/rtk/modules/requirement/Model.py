# -*- coding: utf-8 -*-
#
#       rtk.requirement.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Requirement Package Data Model."""

# Import other RTK modules.
from rtk.datamodels import RTKDataModel
from rtk.dao import RTKRequirement


class RequirementDataModel(RTKDataModel):
    """
    Contains the attributes and methods of a Requirement.

    An RTK Project will consist of one or more Requirements.  The attributes of
    a Requirement are:
    """

    _tag = 'Requirements'

    def __init__(self, dao):
        """
        Initialize a Requirement data model instance.

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

    def select_all(self, revision_id):  # pylint: disable=unused-argument
        """
        Retrieve all the Requirements from the RTK Program database.

        This method retrieves all the records from the RTKRequirement table in
        the connected RTK Program database.  It then adds each to the
        Requirement data model treelib.Tree().

        :param int revision_id: the Revision ID to select the Requirements for.
        :return: tree; the Tree() of RTKRequirement data models.
        :rtype: :class:`treelib.Tree`
        """
        _session = RTKDataModel.select_all(self)

        for _requirement in _session.query(RTKRequirement).filter(
                RTKRequirement.revision_id == revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _requirement.get_attributes()
            _requirement.set_attributes(_attributes)
            self.tree.create_node(
                _requirement.requirement_code,
                _requirement.requirement_id,
                parent=_requirement.parent_id,
                data=_requirement)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _requirement.requirement_id)

        _session.close()

        return self.tree

    def insert(self, **kwargs):  # pylint: disable=unused-argument
        """
        Add a record to the RTKRequirement table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _requirement = RTKRequirement()
        _requirement.revision_id = kwargs['revision_id']
        _requirement.parent_id = kwargs['parent_id']
        _error_code, _msg = RTKDataModel.insert(
            self, entities=[
                _requirement,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _requirement.requirement_code,
                _requirement.requirement_id,
                parent=_requirement.parent_id,
                data=_requirement)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _requirement.requirement_id

        return _error_code, _msg

    def delete(self, node_id):
        """
        Remove a record from the RTKRequirement table.

        :param int node_id entity: the ID of the RTKRequirement record to be
                                   removed from the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Requirement ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the Requirement ID of the Requirement to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Requirement ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def update_all(self):
        """
        Update all RTKRequirement table records in the RTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _msg = self.update(_node.data.requirement_id)

                # Break if something goes wrong and return.
                if _error_code != 0:
                    print 'FIXME: Handle non-zero error codes in ' \
                          'rtk.requirement.Model.update_all().'

            except AttributeError:
                print 'FIXME: Handle AttributeError in ' \
                      'rtk.requirement.Model.update_all().'

        return _error_code, _msg
