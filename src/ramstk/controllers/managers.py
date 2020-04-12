# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.AnalysisManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package analysis manager."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
import pandas as pd
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMatrix


class RAMSTKAnalysisManager():
    """
    Contain the attributes and methods of an analysis manager.

    This class manages the analyses for RAMSTK modules.  Attributes of the
    analysis manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    :ivar tree: the treelib Tree() used to hold a copy of the data manager's
        tree.  This do not remain in-sync automatically.
    :type tree: :class:`treelib.Tree`
    :ivar RAMSTK_CONFIGURATION: the instance of the Configuration class
        associated with this analysis manager.
    :type RAMSTK_CONFIGURATION: :class:`ramstk.configuration.Configuration`
    """
    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an instance of the hardware analysis manager.

        :param configuration: the Configuration instance associated with the
            current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        # Initialize private dictionary attributes.
        self._attributes = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._tree = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_CONFIGURATION = configuration

    def on_get_all_attributes(self, attributes):
        """
        Set all the attributes for the analysis manager.

        :param dict attributes: the data manager's attributes dict.
        :return: None
        :rtype: None
        """
        self._attributes = attributes

    def on_get_tree(self, dmtree):
        """
        Set the analysis manager's treelib Tree().

        :param tree: the data manager's treelib Tree().
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._tree = dmtree


class RAMSTKDataManager():
    """
    This is the meta-class for all RAMSTK Data Managers.

    :ivar tree: the treelib Tree()that will contain the structure of the RAMSTK
        module being modeled.
    :type tree: :class:`treelib.Tree`
    """
    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize an RAMSTK data model instance.
        """
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._revision_id = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None
        self.last_id = None
        self.tree = treelib.Tree()

        # Add the root to the Tree().  This is neccessary to allow multiple
        # entries at the top level as there can only be one root in a treelib
        # Tree().  Manipulation and viewing of a RAMSTK module tree needs to
        # ignore the root of the tree.
        try:
            self.tree.create_node(tag=self._tag,
                                  identifier=self._root,
                                  parent=None)
        except (treelib.tree.MultipleRootError, treelib.tree.NodeIDAbsentError,
                treelib.tree.DuplicatedNodeIdError):
            pass

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_select_revision, 'selected_revision')
        pub.subscribe(self.do_select_matrix, 'request_select_matrix')
        pub.subscribe(self.do_update_matrix, 'request_update_matrix')
        pub.subscribe(self.do_connect, 'succeed_connect_program_database')

    def _do_set_attributes(self, node_id: int, key: str, value: Any,
                           table: str, poppers: Dict) -> None:
        """
        Set the attributes of the record associated with the Module ID.

        :param int node_id: the ID of the record in the RAMSTK Program
            database table whose attributes are to be set.
        :param str key: the key in the attributes dict.
        :param value: the new value of the attribute to set.
        :param str table: the name of the table whose attributes are being set.
        :param dict poppers: the key:value pair containing the attribute and
            its value to set.
        :return: None
        :rtype: None
        """
        _attributes = self.do_select(node_id, table=table).get_attributes()

        for _field in poppers[table]:
            _attributes.pop(_field)

        if key in _attributes:
            _attributes[key] = value

            self.do_select(node_id, table=table).set_attributes(_attributes)

    def _on_select_revision(self, attributes: Dict[str, Any]) -> None:
        """
        Set the revision ID for the data manager.
        """
        self._revision_id = attributes['revision_id']

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

    def do_connect(self, dao: BaseDatabase) -> None:
        """
        Connect data manager to a database.

        :param dao: the BaseDatabase() instance (data access object)
            representing the connected RAMSTK Program database.
        :type dao: :class:`ramstk.db.base.BaseDatabase`
        """
        self.dao = dao

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
        return self.dao.do_delete(self.do_select(node_id, table))

    def do_get_attributes(self, node_id, table):
        """
        Retrieve the RAMSTK data table attributes for node ID.

        :param str node_id: the node ID in the treelib Tree to get the
            attributes for.
        :param str table: the RAMSTK data table to retrieve the attributes
            from.
        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_{0:s}_attributes'.format(table),
                        attributes=self.do_select(
                            node_id, table=table).get_attributes())

    def do_get_last_id(self, module: str) -> None:
        """
        Broadcast the last used ID as the payload of a message.

        :param str module: the name of the workflow module to retrieve the
            last ID.
        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_last_{0:s}_id'.format(module),
                        last_id=self.last_id)

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
        except (AttributeError, treelib.tree.NodeIDAbsentError):
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
        try:
            for _matrix in self.dao.do_select_all(
                    RAMSTKMatrix,
                    key=[RAMSTKMatrix.revision_id, RAMSTKMatrix.matrix_type],
                    value=[self._revision_id, matrix_type],
                    order=RAMSTKMatrix.row_id):
                _lst_matrix.append(
                    (_matrix.column_item_id,
                     _matrix.row_item_id,
                     _matrix.value))

            pub.sendMessage('succeed_retrieve_matrix',
                            matrix_type=matrix_type,
                            matrix=_lst_matrix)
        except TypeError:
            pub.sendMessage('fail_retrieve_matrix',
                            error_message=("No matrix returned for {0:s} "
                                           "matrix.".format(str(matrix_type))))

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
                _entity = self.dao.do_select_all(
                    table=RAMSTKMatrix,
                    key=[
                        RAMSTKMatrix.revision_id, RAMSTKMatrix.matrix_type,
                        RAMSTKMatrix.column_item_id, RAMSTKMatrix.row_item_id
                    ],
                    value=[
                        revision_id, matrix_type,
                        int(_col_id),
                        int(_row_id)
                    ],
                    order=None,
                    _all=False)

                # If there is no corresponding record in RAMSTKMatrix, then
                # create a new RAMSTKMatrix record and add it.
                if _entity is None:
                    _entity = RAMSTKMatrix()
                    _entity.revision_id = revision_id
                    _entity.matrix_type = matrix_type
                    _entity.column_item_id = int(_col_id)
                    _entity.row_item_id = int(_row_id)

                _entity.value = int(matrix[_col_id][_row_id])

                self.dao.do_update(_entity)

        pub.sendMessage('succeed_update_matrix')


class RAMSTKMatrixManager():
    """
    This is the meta-class for all RAMSTK Matrix Managers.

    The Matrix data model is an aggregate model of N x M cell data models.  The
    attributes of a Matrix are:

    :ivar object _row_table: the RAMSTK Progam database table to use for the
        matrix rows.  This is an SQLAlchemy object.
    :ivar list column_tables: a list of RAMSTK data table objects that
        comprise the columns.  One table per matrix managed by an instance of
        the matrix manager.
    :ivar dict dic_matrices: the dictionary containing all the matrices managed
        by an instance of the matrix manager.
    :ivar int n_row: the number of rows in the Matrix.
    :ivar int n_col: the number of columns in the Matrix.

    There are currently 10 matrices as defined by their matrix type.  These
    are:

        +-----------+-------------+--------------+--------------+
        | Matrix ID |  Row Table  | Column Table |  Matrix Type |
        +-----------+-------------+--------------+--------------+
        |     1     | Function    | Hardware     | fnctn_hrdwr  |
        +-----------+-------------+--------------+--------------+
        |     2     | Function    | Validation   | fnctn_vldtn  |
        +-----------+-------------+--------------+--------------+
        |     3     | Requirement | Hardware     | rqrmnt_hrdwr |
        +-----------+-------------+--------------+--------------+
        |     4     | Requirement | Validation   | rqrmnt_vldtn |
        +-----------+-------------+--------------+--------------+
        |     5     | Hardware    | Requirement  | hrdwr_rqrmnt |
        +-----------+-------------+--------------+--------------+
        |     6     | Hardware    | Validation   | hrdwr_vldtn  |
        +-----------+-------------+--------------+--------------+
        |     7     | Validation  | Requirement  | vldtn_rqrmnt |
        +-----------+-------------+--------------+--------------+
        |     8     | Validation  | Hardware     | vldtn_hrdwr  |
        +-----------+-------------+--------------+--------------+
    """

    _tag = 'matrix'

    def __init__(self, column_tables: Dict = None, row_table: Any = None):
        """
        Initialize a Matrix data model instance.

        :param dict column_tables: a dict of RAMSTK data table objects that
            comprise the columns.
        :param row_table: the RAMSTK data table object that comprises the rows
            of the matrix(ces) managed by this manager.
        """
        # Initialize private dictionary attributes.
        self._column_tables = column_tables
        self._dic_columns = {}
        self._dic_matrix = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._col_tree = treelib.Tree()
        self._row_table = row_table
        self._row_tree = treelib.Tree()

        # Initialize public dictionary attributes.
        self.dic_matrices = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.n_row = 1
        self.n_col = 1

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load, 'succeed_retrieve_matrix')

    def do_create_columns(self, matrix_type: str) -> None:
        """
        Create the matrix columns.

        This will effectively create the requested matrix since the row
        headings column was already created.  All values in the resulting
        matrix will be zero.  Call do_load() to load the actual values into
        the matrix.

        :param str matrix_type: the type (name) of the matrix to create the
            columns for.
        :return: None
        :rtype: None
        """
        _lst_values = [0] * self.n_row

        _dic_col_ids = {
            _node: self._col_tree.get_node(_node).tag
            for _node in self._col_tree.nodes
        }
        _dic_col_ids.pop(0)
        _lst_col_ids = _dic_col_ids.keys()

        for _col_id in _dic_col_ids:
            _lst_values[0] = _dic_col_ids[_col_id]
            self._dic_matrix[_col_id] = pd.Series(
                _lst_values,
                index=list(self._row_tree.nodes)
            )

        self.dic_matrices[matrix_type] = pd.DataFrame(self._dic_matrix)
        (self.n_row, self.n_col) = self.dic_matrices[matrix_type].shape

    def do_create_rows(self, tree: treelib.Tree) -> None:
        """
        Create the matrix rows.

        All matrices for a given workflow module will have the same row
        headings.  This method will create a matrix with only one column
        containing the row headings.

        :param tree: the treelib Tree() containing the workflow module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._row_tree = tree
        self._dic_matrix = {}

        self._dic_matrix['rows'] = [
            self._row_tree.get_node(_node).tag
            for _node in self._row_tree.nodes
        ]

        for _matrix_type in self._column_tables.keys():
            self._dic_matrix['rows'][0] = self._column_tables[_matrix_type][1]
            self.dic_matrices[_matrix_type] = pd.DataFrame(self._dic_matrix)
            (self.n_row, self.n_col) = self.dic_matrices[_matrix_type].shape

    def do_delete_column(self, node_id, matrix_type):
        """
        Delete a column from the requested matrix.

        :param int node_id: the MODULE treelib Node ID that was deleted.
            Note that node ID = MODULE ID = matrix row ID.
        :param str matrix_type: the type of the Matrix to delete the column.
        :return: None
        :rtype: None
        :raise: KeyError if passed a node ID or matrix type that doesn't exist.
        """
        self.dic_matrices[matrix_type] = self.dic_matrices[matrix_type].drop(
            [node_id], axis=1)

    def do_delete_row(self, node_id):
        """
        Delete a row from all the matrices.

        :param int node_id: the MODULE treelib Node ID that was deleted.
            Note that node ID = MODULE ID = matrix row ID.
        :return: None
        :rtype: None
        :raise: KeyError if passed a node ID that doesn't exist.
        """
        for _matrix in self.dic_matrices:
            self.dic_matrices[_matrix] = self.dic_matrices[_matrix].drop(
                [node_id])

    def do_insert_column(self, node_id, matrix_type):
        """
        Insert a column into the requested matrix.

        :param int node_id: the MODULE treelib Node ID that was inserted.
            Note that node ID = MODULE ID = matrix row ID.
        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :return: None
        :rtype: None
        :raise: KeyError if passed a node ID or matrix type that doesn't exist.
        """
        _lst_values = [0] * self.n_row
        _lst_values[0] = ''

        self.dic_matrices[matrix_type][node_id] = _lst_values

    def do_insert_row(self, node_id):
        """
        Insert a row into each matrix managed by this matrix manager.

        :param int node_id: the MODULE treelib Node ID that was inserted.
            Note that node ID = MODULE ID = matrix row ID.
        :return: None
        :rtype: None
        """
        for _matrix in self.dic_matrices:
            __, _n_col = self.dic_matrices[_matrix].shape
            _lst_values = [0] * _n_col

            _new_row = pd.DataFrame([_lst_values],
                                    columns=list(
                                        self.dic_matrices[_matrix].columns),
                                    index=[node_id])
            self.dic_matrices[_matrix] = self.dic_matrices[_matrix].append(
                _new_row)

    def do_load(self, matrix_type, matrix):
        """
        Load the matrix values.

        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :param list matrix: a list of tuples (column ID, row ID, value) for the
            selected matrix.
        :return: None
        :rtype: None
        """
        if matrix_type in self.dic_matrices:
            for _col in matrix:
                self.dic_matrices[matrix_type].loc[_col[1], _col[0]] = _col[2]

            pub.sendMessage('succeed_load_matrix', matrix_type=matrix_type,
                            matrix=self.dic_matrices[matrix_type])

    def do_select(self, matrix_type, row, col):
        """
        Select the value from the cell identified by col and row.

        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :param str row: the row of the cell.  This is the second index of the
            Pandas DataFrame.
        :param str col: the column of the cell.  This is the first index of the
            Pandas DataFrame.
        :return: the value in the cell at (col, row).
        :rtype: int
        :raise: KeyError if passed a matrix type, column, or row that doesn't
            exist.
        """
        return self.dic_matrices[matrix_type].at[row, col]

    def do_update(self, revision_id, matrix_type):
        """
        Update the requested matrix in the RAMSTK program database.

        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_update_matrix',
                        revision_id=revision_id,
                        matrix_type=matrix_type,
                        matrix=self.dic_matrices[matrix_type])
