# -*- coding: utf-8 -*-
#
#       ramstk.controllers.RAMSTKMatrixManager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Controllers package RAMSTKMatrixManager meta-class."""

# Third Party Imports
import pandas as pd
from pubsub import pub
from treelib import Tree


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

    def __init__(self, column_tables=None, row_table=None):
        """
        Initialize a Matrix data model instance.

        :param list column_tables: a list of RAMSTK data table objects that
            comprise the columns.  One table per matrix managed by this
            manager.
        :param row_table: the RAMSTK data table object that comprises the rows
            of the matrix(ces) managed by this manager.
        """
        # Initialize private dictionary attributes.
        self._column_tables = column_tables

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._col_tree = Tree()
        self._row_table = row_table
        self._row_tree = Tree()

        # Initialize public dictionary attributes.
        self.dic_matrices = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.n_row = 1
        self.n_col = 1

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load, 'succeed_retrieve_matrix')

    def do_create(self, matrix_type):
        """
        Create the data matrices for MODULE and add to the matrix frame.

        :param str matrix_type: the type of the Matrix to add.
        :return: None
        :rtype: None
        """
        _dic_columns = {}

        # Retrieve the row information from the row tree.
        _lst_row_ids = [_node for _node in self._row_tree.nodes]
        _dic_columns['rows'] = [
            self._row_tree.get_node(_node).tag
            for _node in self._row_tree.nodes
        ]

        _lst_values = [
            0,
        ] * len(_lst_row_ids)
        _dic_columns['rows'][0] = self._column_tables[matrix_type][1]

        # Retrieve the column information from the column tree.
        _dic_col_ids = {
            _node: self._col_tree.get_node(_node).tag
            for _node in self._col_tree.nodes
        }
        _dic_col_ids.pop(0)
        _lst_col_ids = _dic_col_ids.keys()

        for _col_id in _dic_col_ids:
            _lst_values[0] = _dic_col_ids[_col_id]
            _dic_columns[_col_id] = pd.Series(
                _lst_values,
                index=_lst_row_ids,
            )

        # Put it together into a dict of pandas data frames (each matrix is a
        # data frame).  For now only the n_row attribute has meaning as each
        # matrix will have the same number of rows for a MODULE.
        self.dic_matrices[matrix_type] = pd.DataFrame(_dic_columns)
        (self.n_row, self.n_col) = self.dic_matrices[matrix_type].shape

        pub.sendMessage('request_select_matrix', matrix_type=matrix_type)

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
        for _col in matrix:
            self.dic_matrices[matrix_type][_col[0]][_col[1]] = _col[2]

    def do_select(self, matrix_type, col, row):
        """
        Select the value from the cell identified by col and row.

        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :param str col: the column of the cell.  This is the first index of the
            Pandas DataFrame.
        :param str row: the row of the cell.  This is the second index of the
            Pandas DataFrame.
        :return: the value in the cell at (col, row).
        :rtype: int
        :raise: KeyError if passed a matrix type, column, or row that doesn't
            exist.
        """
        return self.dic_matrices[matrix_type][col][row]

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
