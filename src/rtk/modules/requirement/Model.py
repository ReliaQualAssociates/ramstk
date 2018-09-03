# -*- coding: utf-8 -*-
#
#       rtk.requirement.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Requirement Package Data Model."""

# Import other RAMSTK modules.
from rtk.modules import RAMSTKDataModel
from rtk.dao import RAMSTKRequirement


class RequirementDataModel(RAMSTKDataModel):
    """
    Contains the attributes and methods of a Requirement.

    An RAMSTK Project will consist of one or more Requirements.  The attributes of
    a Requirement are:
    """

    _tag = 'Requirements'

    def __init__(self, dao):
        """
        Initialize a Requirement data model instance.

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

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Requirements from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKRequirement table in
        the connected RAMSTK Program database.  It then adds each to the
        Requirement data model treelib.Tree().

        :return: tree; the Tree() of RAMSTKRequirement data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _requirement in _session.query(RAMSTKRequirement).filter(
                RAMSTKRequirement.revision_id == _revision_id).all():
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
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _requirement.requirement_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKRequirement table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _requirement = RAMSTKRequirement()
        _requirement.revision_id = kwargs['revision_id']
        _requirement.parent_id = kwargs['parent_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
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
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = _requirement.requirement_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKRequirement table.

        :param int node_id entity: the PyPubSub Tree() ID of the Requirement to
                                   delete.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Requirement ID {0:s}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RAMSTK Program database.

        :param str node_id: the PyPubSub Tree() ID of the Requirement to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = ('RAMSTK ERROR: Attempted to save non-existent Requirement ID '
                    '{0:s}.'.format(str(node_id)))

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKRequirement table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ''

        for _node in self.tree.all_nodes():
            try:
                _error_code, _debug_msg = self.do_update(_node.identifier)

                _msg = _msg + _debug_msg + '\n'

            except AttributeError:
                _error_code = 1
                _msg = ("RAMSTK ERROR: One or more records in the requirement "
                        "table did not update.")

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all records in the requirement "
                    "table.")

        return _error_code, _msg
