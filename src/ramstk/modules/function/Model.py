# -*- coding: utf-8 -*-
#
#       ramstk.modules.function.Model.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Model."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKFunction
from ramstk.modules import RAMSTKDataModel


class FunctionDataModel(RAMSTKDataModel):
    """
    Contain the attributes and methods of a Function.

    An RAMSTK Project will consist of one or more Functions.  The attributes
    of a Function are:
    """

    _tag = 'Functions'
    _root = 0

    def __init__(self, dao, **kwargs):
        """
        Initialize a Function data model instance.

        :param dao: the data access object for communicating with the RAMSTK
                    Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        RAMSTKDataModel.__init__(self, dao)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._test = kwargs['test']

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_delete(self, node_id):
        """
        Remove a record from the RAMSTKFunction table.

        :param int node_id: the ID of the RAMSTKFunction record to be removed
                            from the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RAMSTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = (
                "RAMSTK ERROR: Attempted to delete non-existent Function "
                "ID {0:s}."
            ).format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

            # If we're not running a test, let anyone who cares know a Function
            # was deleted.
            if not self._test:
                pub.sendMessage('deleted_function', tree=self.tree)

        return _error_code, _msg

    def do_insert(self, **kwargs):
        """
        Add a record to the RAMSTKFunction table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _function = RAMSTKFunction()
        _function.revision_id = kwargs['revision_id']
        _function.parent_id = kwargs['parent_id']
        _error_code, _msg = RAMSTKDataModel.do_insert(
            self, entities=[
                _function,
            ],
        )

        if _error_code == 0:
            self.tree.create_node(
                _function.name,
                _function.function_id,
                parent=_function.parent_id,
                data=_function,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            self.last_id = _function.function_id

            # If we're not running a test, let anyone who cares know a new
            # Function was inserted.
            if not self._test:
                pub.sendMessage('inserted_function', tree=self.tree)

        return _error_code, _msg

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Functions from the RAMSTK Program database.

        This method retrieves all the records from the RAMSTKFunction table in
        the connected RAMSTK Program database.  It then add each to the
        Function data model treelib.Tree().

        :return: None
        :rtype: None
        """
        _revision_id = kwargs['revision_id']
        _session = RAMSTKDataModel.do_select_all(self)

        for _function in _session.query(RAMSTKFunction).filter(
                RAMSTKFunction.revision_id == _revision_id,
        ).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _function.get_attributes()
            _function.set_attributes(_attributes)
            self.tree.create_node(
                tag=_function.name,
                identifier=_function.function_id,
                parent=_function.parent_id,
                data=_function,
            )

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RAMSTKDataModel.__init__
            try:
                self.last_id = max(self.last_id, _function.function_id)
            except TypeError:
                self.last_id = _function.function_id

        _session.close()

        # If we're not running a test and there were functions returned,
        # let anyone who cares know the Functions have been selected.
        if not self._test and self.tree.size() > 1:
            pub.sendMessage('retrieved_functions', tree=self.tree)

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to RAMSTK Program database.

        :param int node_id: the Function ID of the Function to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update(self, node_id)

        # If there was no error and we're not running a test, let anyone
        # who cares know a Function was updated.
        if _error_code == 0:
            if not self._test:
                _attributes = self.do_select(node_id).get_attributes()
                pub.sendMessage('updated_function', attributes=_attributes)
        else:
            _error_code = 2005
            _msg = (
                "RAMSTK ERROR: Attempted to save non-existent "
                "Function ID {0:d}."
            ).format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RAMSTKFunction table records in the RAMSTK Program database.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RAMSTKDataModel.do_update_all(self, **kwargs)

        if _error_code == 0:
            _msg = (
                "RAMSTK SUCCESS: Updating all records in the function "
                "table."
            )
        elif _error_code == 1:
            _msg = (
                "RAMSTK ERROR: One or more records in the function "
                "table did not update."
            )

        return _error_code, _msg
