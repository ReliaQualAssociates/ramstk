# -*- coding: utf-8 -*-
#
#       rtk.modules.function.Model.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Function Package Data Model."""

# Import other RTK modules.
from rtk.modules import RTKDataModel
from rtk.dao import RTKFunction


class FunctionDataModel(RTKDataModel):
    """
    Contain the attributes and methods of a Function.

    An RTK Project will consist of one or more Functions.  The attributes of a
    Function are:
    """

    _tag = 'Functions'

    def __init__(self, dao):
        """
        Initialize a Function data model instance.

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

    def do_select_all(self, **kwargs):
        """
        Retrieve all the Functions from the RTK Program database.

        This method retrieves all the records from the RTKFunction table in the
        connected RTK Program database.  It then add each to the Function data
        model treelib.Tree().

        :param int revision_id: the Revision ID to select the Functions for.
        :return: tree; the Tree() of RTKFunction data models.
        :rtype: :class:`treelib.Tree`
        """
        _revision_id = kwargs['revision_id']
        _session = RTKDataModel.do_select_all(self)

        for _function in _session.query(RTKFunction).filter(
                RTKFunction.revision_id == _revision_id).all():
            # We get and then set the attributes to replace any None values
            # (NULL fields in the database) with their default value.
            _attributes = _function.get_attributes()
            _function.set_attributes(_attributes)
            self.tree.create_node(
                _function.name,
                _function.function_id,
                parent=_function.parent_id,
                data=_function)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = max(self.last_id, _function.function_id)

        _session.close()

        return self.tree

    def do_insert(self, **kwargs):
        """
        Add a record to the RTKFunction table.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _function = RTKFunction()
        _function.revision_id = kwargs['revision_id']
        _function.parent_id = kwargs['parent_id']
        _error_code, _msg = RTKDataModel.do_insert(
            self, entities=[
                _function,
            ])

        if _error_code == 0:
            self.tree.create_node(
                _function.name,
                _function.function_id,
                parent=_function.parent_id,
                data=_function)

            # pylint: disable=attribute-defined-outside-init
            # It is defined in RTKDataModel.__init__
            self.last_id = _function.function_id

        return _error_code, _msg

    def do_delete(self, node_id):
        """
        Remove a record from the RTKFunction table.

        :param int node_id: the ID of the RTKFunction record to be removed from
                            the RTK Program database.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_delete(self, node_id)

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKDataModel.__init__
        if _error_code != 0:
            _error_code = 2005
            _msg = _msg + '  RTK ERROR: Attempted to delete non-existent ' \
                          'Function ID {0:s}.'.format(str(node_id))
        else:
            self.last_id = max(self.tree.nodes.keys())

        return _error_code, _msg

    def do_update(self, node_id):
        """
        Update the record associated with Node ID to the RTK Program database.

        :param int node_id: the Function ID of the Function to save.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code, _msg = RTKDataModel.do_update(self, node_id)

        if _error_code != 0:
            _error_code = 2006
            _msg = 'RTK ERROR: Attempted to save non-existent Function ID ' \
                   '{0:d}.'.format(node_id)

        return _error_code, _msg

    def do_update_all(self, **kwargs):  # pylint: disable=unused-argument
        """
        Update all RTKFunction table records in the RTK Program database.

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
                _msg = ("RTK ERROR: One or more records in the function "
                        "table did not update.")

        if _error_code == 0:
            _msg = ("RTK SUCCESS: Updating all records in the function "
                    "table.")

        return _error_code, _msg
