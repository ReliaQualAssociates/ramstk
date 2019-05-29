# -*- coding: utf-8 -*-
#
#       ramstk.modules.failure_definition.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Definition Package Data Model Module."""

# Import other RAMSTK modules.
from ramstk.modules import RAMSTKDataModel
from ramstk.dao import RAMSTKFailureDefinition


class FailureDefinitionDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of Failure Definition.

    The Failure Definition data model contains the attributes and methods of a
    failure definition.  A Revision will contain zero or more definitions.  The
    attributes of a Failure Definition are:
    """

    _tag = 'Failure Definitions'

    def __init__(self, dao):
        """
        Initialize a Failure Definition data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
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
        Retrieve all the Failure Definitions from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKFailureDefinition
        table in the connected RAMSTK Program database.  It then add each to the
        Failure Definition data model treelib.Tree().

        :return: tree; the treelib Tree() of RAMSTKFailureDefinition data models.
        :rtype: :py:class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _definition in _session.query(RAMSTKFailureDefinition).filter(
                RAMSTKFailureDefinition.revision_id == _revision_id).all():
            self.tree.create_node(
                _definition.definition,
                _definition.definition_id,
                parent=0,
                data=_definition)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = max(self.last_id, _definition.definition_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKFailureDefinition table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _revision_id = kwargs['revision_id']
        _definition = RAMSTKFailureDefinition()
        _definition.revision_id = _revision_id
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _definition,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _definition.definition,
                _definition.definition_id,
                parent=0,
                data=_definition)
            self.last_id = _definition.definition_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKFailureDefinition table.

        :param int node_id: the ID of the Failure Definition to be
                                  removed.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RAMSTK ERROR: Attempted to delete non-existent ' \
                          'Failure Definition ID {0:d}.'.format(node_id)
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record in the RAMSTKFailureDefinition table.

        :param int node_id: the Failure Definition ID to save to the RAMSTK
                                  Program database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2207
            _msg = 'RAMSTK ERROR: Attempted to save non-existent Failure ' \
                   'Definition ID {0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Upsate all RAMSTKFailureDefinition records.

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
                _msg = ("RAMSTK ERROR: One or more records in the failure "
                        "definition table did not update.")

        if _error_code == 0:
            _msg = ("RAMSTK SUCCESS: Updating all records in the failure "
                    "definition table.")

        return _error_code, _msg
