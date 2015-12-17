#!/usr/bin/env python
"""
#############
Matrix Module
#############
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.datamodels.matrix.Matrix.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    from datamodels.cell.Cell import Model as Cell
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    from rtk.datamodels.cell.Cell import Model as Cell


try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ParentError(Exception): pass          # pylint: disable=C0111, C0321


class NoMatrixError(Exception): pass        # pylint: disable=C0111, C0321


def _add_cell(matrix, row_id, col_id):
    """
    Adds a new cell to the selected Matrix.

    :param rtk.datamodels.matrix.Model matrix: the Matrix to add the cell.
    :param int row_id: the row ID of the new cell.
    :param int col_id: the column ID of the new cell.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    matrix.dicCells[row_id, col_id] = Cell()

    return False

def _delete_cell(matrix, row_id, col_id):
    """
    Delete the cell at row_id, col_id from the selected Matrix.

    :param rtk.datamodels.matrix.Model matrix: the Matrix to delete the
                                               cell from.
    :param int row_id: the row ID of the cell to delete.
    :param int col_id: the column ID of the cell to delete.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    matrix.dicCells.pop((row_id, col_id))

    return False


class Model(object):
    """
    The Matrix data model is an aggregate model of N x M cell data models.  The
    attributes of a Matrix are:

    :ivar dicCells: Dictionary of the Cells associated with the Matrix.  Key is the Cell ID; value is a pointer to the instance of the Cell data model.

    :ivar matrix_id: the Matrix ID this model represents.
    :ivar n_row: the number of rows in the Matrix.
    :ivar n_col: the number of columns in the Matrix.
    :ivar matrix_type: the type of Matrix this model represents.  Matrix types
                       are one of the following:

    +------+------------+-------------+
    | Type |    Rows    |   Columns   |
    +======+============+=============+
    |   0  | Hardware   | Function    |
    +------+------------+-------------+
    |   1  | Software   | Function    |
    +------+------------+-------------+
    |   2  | Testing    | Function    |
    +------+------------+-------------+
    |   3  | Validation | Requirement |
    +------+------------+-------------+
    |   4  | Testing    | Hardware    |
    +------+------------+-------------+
    |   5  | Testing    | Software    |
    +------+------------+-------------+
    """

    def __init__(self, matrix_id, matrix_type):
        """
        Method to initialize a Matrix data model instance.

        :param int matrix_id: the Matrix ID that the model will represent.
        :param int matrix_type: the type of Matrix the model will represent.
        """

        # Set public dict attribute default values.
        self.dicCells = {}

        # Set public scalar attribute default values.
        self.matrix_id = matrix_id
        self.matrix_type = matrix_type
        self.n_row = 0
        self.n_col = 0


class Matrix(object):
    """
    The Matrix data controller provides an interface between the Matrix data
    model and an RTK view model.  A single Matrix data controller can manage
    one or more Matrix data models.

    :ivar _dao: default value: None

    :ivar dicMatrices: Dictionary of the Matrix data models managed.  Key is the Revision ID; value is a dictionary of Matrix data models for the revision.  The internal matrix key is the Matrix ID the value is a pointer to the instance of the Matrix data model.
    """

    def __init__(self):
        """
        Initialize a Matrix data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None

        # Initialize public dictionary attributes.
        self.dicMatrices = {}

    def request_matrix(self, revision_id, query, matrix_type):
        """
        Loads the entire set of Matrices for the Revision ID.

        :param `rtk.DAO` dao: the Data Access object to use for communicating
                              with the RTK Project database.
        :param int revision_id: the Revision ID to retrieve the Matrices for.
        :param str query: the SQL query to use for retrieving the data to fill
                          the Matrix.
        :param int matrix_type: the type of Matrix being requested.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Controller must be associated with a Revision.
        if revision_id is None:
            raise ParentError

        # Select all the unique matrix ID for the Revision ID.
        _query = "SELECT DISTINCT fld_matrix_id \
                  FROM rtk_matrices \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_mats, _error_code, __) = self._dao.execute(_query)
        try:
            _n_matrices = len(_mats)
        except TypeError:
            _n_matrices = 0

        # Now select all the cell information using the passed query.
        (_cells, _error_code, __) = self._dao.execute(query)
        try:
            _n_cells = len(_cells)
        except TypeError:
            _n_cells = 0

        # Create the inner dictionary of Matrix ID --> Matrix relationships.
        _matrices = {}
        for i in range(_n_matrices):
            _matrix = Model(_mats[i][0], matrix_type)
            _matrices[_mats[i][0]] = _matrix
            _mat_cells = [x for x in _cells if x[0] == _mats[i][0]]
            for j in range(len(_mat_cells)):
                _cell = Cell()
                _cell.set_attributes(_mat_cells[j][1:])
                _matrix.dicCells[_cell.row_id, _cell.col_id] = _cell

        # Create the outer dictionary of Revision ID --> {}.
        self.dicMatrices[revision_id] = _matrices

        return False

    def request_rows(self, revision_id, matrix_id):
        """
        Create a dictionary of row values.  The key is the row number and the
        value is a list of values for each column.

        :param int revision_id: the Revision ID to look for the Matrix.
        :param int matrix_id: the Matrix ID to the rows for.
        :return: _rows
        :rtype: dict
        """

        from operator import itemgetter

        try:
            _matrix = self.dicMatrices[revision_id][matrix_id]
        except KeyError:
            return {}

        _cells = _matrix.dicCells.values()

        _matrix.n_row = 0
        _matrix.n_col = 0

        _n_row = 0
        _n_col = set()
        _temp = {}
        _rows = {}
        for _cell in _cells:
            try:
                _temp[_cell.row_id].append([_cell.col_id, _cell.value])
            except KeyError:
                _temp[_cell.row_id] = [[_cell.col_id, _cell.value]]
            _values = sorted(_temp[_cell.row_id], key=itemgetter(0))
            _rows[_cell.row_id] = [x[1] for x in _values]
            _n_row += 1
            _n_col.add(_cell.col_id)

        # Set the Matrix row and column count.
        _matrix.n_row = _n_row
        _matrix.n_col = len(_n_col)

        return _rows

    def add_row(self, revision_id, matrix_type, matrix_id, row_id):
        """
        Adds a new row to the selected Matrix.

        :param int revision_id: the Revision ID to add the cell to.
        :param int matrix_type: the type of Matrix this row is being added to.
        :param int matrix_id: the Matrix ID to add the cell to.
        :param int row_id: the ID of the new row.
        :return: (True, 0)
        :rtype: tuple
        """

        _matrix = self.dicMatrices[revision_id][matrix_id]

        _query = "INSERT INTO rtk_matrices \
                  (fld_revision_id, fld_matrix_type, fld_matrix_id, \
                   fld_row_id, fld_col_id) \
                  VALUES "

        for _col_id in range(_matrix.n_col):
            _add_cell(_matrix, row_id, _col_id)
            _query = _query + "({0:d}, {1:d}, {2:d}, {3:d}, {4:d}),".format(
                revision_id, matrix_type, matrix_id, row_id, _col_id)

        # Remove the trailing comma from the query.
        _query = _query[:-1]

        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)

    def delete_row(self, revision_id, matrix_id, row_id):
        """
        Adds a new row to the selected Matrix.

        :param int revision_id: the Revision ID to add the cell to.
        :param int matrix_id: the Matrix ID to add the cell to.
        :param int row_id: the ID of the new row.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _matrix = self.dicMatrices[revision_id][matrix_id]

        _query = "DELETE FROM rtk_matrices \
                  WHERE fld_revision_id={0:d} \
                  AND fld_matrix_id={1:d} \
                  AND fld_row_id={2:d}".format(revision_id, matrix_id, row_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        if _results:
            for _col_id in range(_matrix.n_col):
                _delete_cell(_matrix, row_id, _col_id)

        return(_results, _error_code)

    def save_matrix(self, matrix):
        """
        Saves the matrix information to the open RTK Project database.

        :param rtk.datamodels.matrix.Model matrix: the Matrix to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        for _cell in matrix.dicCells.values():
            _attributes = _cell.get_attributes()
            _query = "UPDATE rtk_matrices \
                      SET fld_value={0:d} \
                      WHERE fld_matrix_id={1:d} \
                      AND fld_row_id={2:d} \
                      AND fld_col_id={3:d}".format(_attributes[2],
                                                   matrix.matrix_id,
                                                   _attributes[0],
                                                   _attributes[1])
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

        return(_results, _error_code)
