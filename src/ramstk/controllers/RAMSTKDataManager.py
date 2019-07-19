# -*- coding: utf-8 -*-
#
#       ramstk.controllers.RAMSTKDataManager.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Controllers Package RAMSTKDataManager meta-class."""

# Third Party Imports
from pubsub import pub
from sqlalchemy import and_
from treelib import Tree, tree

# RAMSTK Package Imports
from ramstk.models.programdb import RAMSTKMatrix


class RAMSTKDataManager():
    """
    This is the meta-class for all RAMSTK Data Managers.

    :ivar tree: the treelib Tree()that will contain the structure of the RAMSTK
        module being modeled.
    :type tree: :class:`treelib.Tree`
    :ivar dao: the data access object used to communicate with the RAMSTK
        Program database.
    :type dao: :class:`ramstk.dao.DAO`
    """

    def __init__(self, dao, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an RAMSTK data model instance.

        :param dao: the data access object for communicating with the RAMSTK
            Program database.
        :type dao: :class:`ramstk.dao.DAO.DAO`
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = 0

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
                tag=self._tag,
                identifier=self._root,
                parent=None,
            )
        except (
                tree.MultipleRootError,
                tree.NodeIDAbsentError,
                tree.DuplicatedNodeIdError,
        ):
            pass

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_select_matrix, 'request_select_matrix')
        pub.subscribe(self.do_update_matrix, 'request_update_matrix')

    @staticmethod
    def do_build_dict(records, id_field):
        """
        Convert a list of RAMSTK database records into a dict of records.

        This is a helper method to use when an entry in a data manager's data
        package will consist of multiple records.  SQLAlchemy will return a
        list of records for any one-to-many relationships.  However, there is
        no simple way to select the exact record from the many returned in a
        list.  This method creates a dict using the passed ID field name as the
        key and the associated RAMSTK data table instance (record) as the
        value.

        For example, the Revision data manager needs to manage all the failure
        definitions associated with each revision.  This method will convert
        the list return by SQLAlchemy to a dict so each definition can be
        accessed by it's definition ID (key).

        :param list records: the list of RAMSTK<MODULE> data table records.
        :param str id_field: the name of the field in the RAMSTK<MODULE> data
            table records to use as the key in the resulting dict.
        :return: _dic_records; the dict version of the records.
        :rtype: dict
        """
        _dic_records = {}
        for _record in records:
            _id = _record.get_attributes()[id_field]
            _dic_records[_id] = _record

        return _dic_records

    def do_delete(self, node_id, table):
        """
        Remove a RAMSTK data table record.

        :param int node_id: the node ID to be removed from the RAMSTK Program
            database.
        :param str table: the key in the module's treelib Tree() data package
            for the RAMSTK data table to remove the record from.
        :return: (_error_code, _error_msg); the error code and associated
            message from the DAO.
        :rtype: (int, str)
        """
        return self.dao.db_delete(self.do_select(node_id, table))

    def do_select(self, node_id, table):
        """
        Retrieve the RAMSTK data table record for the Node ID passed.

        :param int node_id: the Node ID of the data package to retrieve.
        :param str table: the name of the RAMSTK data table to retrieve the
            attributes from.
        :return: the instance of the RAMSTK<MODULE> data table that was
            requested or None if the requested Node ID does not exist.
        :raise: KeyError if passed the name of a table that isn't managed by
            this manager.
        """
        try:
            _entity = self.tree.get_node(node_id).data[table]
        except AttributeError:
            _entity = None
        except tree.NodeIDAbsentError:
            _entity = None

        return _entity

    def do_select_matrix(self, matrix_type):
        """
        Retrieve all the values for the matrix.

        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :return: None
        :rtype: None
        """
        _lst_matrix = []

        # Retrieve the matrix values for the desired Matrix ID.
        for _matrix in self.dao.session.query(RAMSTKMatrix).filter(
                and_(
                    RAMSTKMatrix.revision_id == self._revision_id,
                    RAMSTKMatrix.matrix_type == matrix_type,
                ), ).all():
            _lst_matrix.append(
                (_matrix.column_item_id, _matrix.row_item_id, _matrix.value))

        pub.sendMessage('succeed_retrieve_matrix',
                        matrix_type=matrix_type,
                        matrix=_lst_matrix)

    def do_set_tree(self, module_tree):
        """
        Set the MODULE treelib Tree().

        This method is generally used to respond to events such as successful
        calculations of the entire system.

        :param module_tree: the treelib Tree() to assign to the tree attribute.
        :type module_tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.tree = module_tree

    def do_update_all(self):
        """
        Update all MODULE data table records in the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            self.do_update(_node.identifier)

    def do_update_matrix(self, revision_id, matrix_type, matrix):
        """
        Update the matrix values in the RAMSTK Program database.

        :param int revision_id: the revisiond ID associated with the matrix to
            update.
        :param str matrix_type: the type (name) of the matrix to update.
        :param matrix: the actual matrix whose values are being updated in the
            database.
        :type matrix: :class:`pandas.DataFrame`
        :return: None
        :rtype: None
        """
        _row_ids = list(matrix.index[1:])
        _column_ids = list(matrix.columns[1:])
        for _row_id in _row_ids:
            for _col_id in _column_ids:
                _entity = self.dao.session.query(RAMSTKMatrix).filter(
                    and_(RAMSTKMatrix.revision_id == revision_id,
                         RAMSTKMatrix.matrix_type == matrix_type,
                         RAMSTKMatrix.column_item_id == int(_col_id),
                         RAMSTKMatrix.row_item_id == int(_row_id))).first()

                # If there is no corresponding record in RAMSTKMatrix, then
                # create a new RAMSTKMatrix record and add it.
                if _entity is None:
                    _entity = RAMSTKMatrix()
                    _entity.revision_id = revision_id
                    _entity.matrix_type = matrix_type
                    _entity.column_item_id = int(_col_id)
                    _entity.row_item_id = int(_row_id)

                _entity.value = int(matrix[_col_id][_row_id])

                self.dao.session.add(_entity)

        (_error_code, _error_msg) = self.dao.db_update()

        if _error_code == 0:
            pub.sendMessage('succeed_update_matrix')
        else:
            pub.sendMessage('fail_update_matrix', error_msg=_error_msg)
