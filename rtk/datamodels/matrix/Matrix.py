#!/usr/bin/env python
"""
#############
Matrix Module
#############
"""

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
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ParentError(Exception):
    """
    Error to raise when no Revision ID is passed.
    """
    pass


class NoMatrixError(Exception):
    """
    Error to raise when no Matrices are returned.
    """
    pass


class Model(object):
    """
    The Matrix data model is an aggregate model of N x M cell data models.  The
    attributes of a Matrix are:

    :ivar dict dicRows: Dictionary of the Rows associated with the Matrix.  Key
                        is the Row ID; value is a list as follows:
                        [parent_id, function id, function code, function name,
                         value1, value2, ... valueN]
    :ivar int revision_id: the Revision ID the Matrix belongs to.
    :ivar int matrix_id: the Matrix ID this model represents.
    :ivar int matrix_type: the type of Matrix this model represents.  Matrix
                           types are one of the following:
    +------+------------+-------------+
    | Type |    Rows    |   Columns   |
    +======+============+=============+
    |   0  | Function   | Hardware    |
    +------+------------+-------------+
    |   1  | Function   | Software    |
    +------+------------+-------------+
    |   2  | Function   | Testing     |
    +------+------------+-------------+
    |   3  | Requirement| Hardware    |
    +------+------------+-------------+
    |   4  | Requirement| Software    |
    +------+------------+-------------+
    |   5  | Requirement| Validation  |
    +------+------------+-------------+
    |   6  | Hardware   | Testing     |
    +------+------------+-------------+
    |   7  | Hardware   | Validation  |
    +------+------------+-------------+
    :ivar int n_row: the number of rows in the Matrix.
    :ivar int n_col: the number of columns in the Matrix.
    """

    def __init__(self):
        """
        Method to initialize a Matrix data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicRows = {}

        # Define public list attributes.
        self.lstColumnHeaders = []

        # Define public scalar attributes.
        self.revision_id = None
        self.matrix_id = None
        self.matrix_type = None
        self.n_row = 1
        self.n_col = 1

    def set_attributes(self, values):
        """
        Method to set the Matrix data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.matrix_id = int(values[1])
            self.matrix_type = int(values[2])
            self.n_row = int(values[3])
            self.n_col = int(values[4])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Matrix Model - Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Matrix Model - Converting one or more inputs " \
                   "to the correct data type."
        except ValueError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Matrix Model - Converting one or more inputs " \
                   "to the correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Matrix data model
        attributes.

        :return: (revision_id, matrix_id, matrix_type, n_row, n_col)
        :rtype: tuple
        """

        _values = (self.revision_id, self.matrix_id, self.matrix_type,
                   self.n_row, self.n_col)

        return _values


class Matrix(object):
    """
    The Matrix data controller provides an interface between the Matrix data
    model and an RTK view model.  A single Matrix data controller can manage
    one or more Matrix data models.

    :ivar _dao: the :py:class:`rtk.dao.DAO` object for this controller to use
                when interfacing with the open RTK Project database.
    :ivar dict dicMatrices: Dictionary of the Matrix data models managed.  Key
                            is the Matrix type; value is a pointer to the
                            Matrix data model instance.
    """

    def __init__(self):
        """
        Initialize a Matrix data controller instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._dao = None

        # Define public dictionary attributes.
        self.dicMatrices = {}

        # Define public list attributes.

        # Define public scalar attributes.

    def request_matrix(self, dao, revision_id, matrix_types):
        """
        Method to load the entire set of Matrices for the Revision ID.

        :param dao: the :py:class:`rtk.dao.DAO` object to use for communicating
                    with the open RTK Project database.
        :param int revision_id: the ID of the Revision to request the Matrices
                                for.
        :param list matrix_types: a list of the types of Matrix to retrieve the
                                  data for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Controller must be associated with a Revision.
        if revision_id is None:
            raise ParentError

        self._dao = dao

        for __, _matrix_type in enumerate(matrix_types):
            _query = "SELECT t1.fld_matrix_id, t1.fld_matrix_type, \
                             t2.fld_code, t2.fld_name, t2.fld_function_id, \
                             t1.fld_parent_id, t1.fld_row_id, t1.fld_col_id, \
                             t1.fld_value, t1.fld_col_item_id \
                      FROM rtk_matrix AS t1 \
                      INNER JOIN tbl_functions AS t2 \
                      ON t2.fld_function_id=t1.fld_row_item_id \
                      WHERE t1.fld_revision_id={0:d} \
                      AND t1.fld_matrix_type={1:d} \
                      ORDER BY t1.fld_matrix_id, t1.fld_row_id, \
                               t1.fld_col_id".format(revision_id, _matrix_type)
            (_results, _error_code, __) = self._dao.execute(_query)

            if len(_results) > 0:
                self._create_matrix(revision_id, _results)

                _column_ids = list(set([_r[9] for _r in _results]))
                self._request_column_headers(_column_ids, _matrix_type)

        return(_results, _error_code)

    def _create_matrix(self, revision_id, results):
        """
        Method to create a Matrix data model, populate it's row dictionary, and
        add it to the Matrix data controller's matrix dictionary.

        :param int revision_id: the ID of the Revision this Matrix is
                                associated with.
        :param list results: the data returned from the open RTK Program
                             database for the Matrix to create.
        :return: False on success or True if an error is encountered.
        :rtype: bool
        """

        # _results = [matrix_id, matrix_type, function code, function name,
        #             function id, parent_id, row id, col id, value,
        #             col_item_id]
        _matrix_id = results[0][0]

        # Create a list of the row values for the Matrix.
        # _rows = [function code, function name, function id, parent_id,
        #          row id, col id, value, col_item_id]
        _rows = [_m[2:len(_m) - 1] for _m in results]

        # Create a new Matrix data model, set it's attributes, and add it to
        # the Matrix dictionary.
        _matrix = Model()
        _n_row = len(set([_m[4] for _m in _rows]))
        _n_col = len(set([_m[5] for _m in _rows]))
        _matrix.set_attributes([revision_id, results[0][1], _matrix_id, _n_row,
                                _n_col])
        self.dicMatrices[_matrix_id] = _matrix

        # Populate the row dictionary for the Matrix.
        for j in range(_n_row):
            _name = list(set([_r[0:4] for _r in _rows if _r[4] == j]))
            # _values = [parent_id, function id, function code, function name,
            #            value1, value2, ... valueN]
            _values = [_name[0][3], _name[0][2], _name[0][0], _name[0][1]]
            _values.extend([_r[6] for _r in _rows if _r[4] == j])
            _matrix.dicRows[j] = _values

        return False

    def _request_column_headers(self, column_ids, matrix_type):
        """
        Method to retrieve the Function/Hardware Matrix information from the
        open RTK Program database.

        :param list column_ids: list of the IDs for the items that represent
                                the columns in the Matrix.
        :param int matrix_type: the type of Matrix to retrieve the headers for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _matrix = self.dicMatrices[matrix_type]

        if len(column_ids) == 1:
            _column_ids = "({0:d})".format(column_ids[0])
        else:
            _column_ids = str(tuple(column_ids))

        _matrix.lstColumnHeaders = []
        if matrix_type in [0, 3]:
            _query = "SELECT fld_name \
                      FROM rtk_hardware \
                      WHERE fld_hardware_id IN " + _column_ids + \
                      " AND fld_part=0"
        elif matrix_type in [1, 4]:
            _query = "SELECT fld_description \
                      FROM rtk_software \
                      WHERE fld_software_id IN " + _column_ids + \
                      " AND fld_level_id<4"
        elif matrix_type in [2, 6]:
            _query = "SELECT fld_name \
                      FROM rtk_tests \
                      WHERE fld_test_id IN " + _column_ids
        elif matrix_type in [5, 7]:
            _query = "SELECT fld_task_desc \
                      FROM rtk_validation \
                      WHERE fld_validation_id IN " + _column_ids

        (_results, _error_code, __) = self._dao.execute(_query)

        try:
            _n_headers = len(_results)
        except TypeError:
            _n_headers = 0

        for i in range(_n_headers):
            _matrix.lstColumnHeaders.append(_results[i][0])

        return False

    def save_matrix(self, matrix_id):
        """
        Method to save the Matrix information to the open RTK Project database.

        :param int matrix_id: the ID of the Matrix to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _matrix = self.dicMatrices[matrix_id]

        for _row_id in _matrix.dicRows.keys():
            for _col_id in range(len(_matrix.dicRows[_row_id][4:])):
                (_results,
                 _error_code) = self.save_cell(matrix_id, _row_id, _col_id,
                                               _matrix.dicRows[_row_id][0],
                                               _matrix.dicRows[_row_id][_col_id + 4])

        return False

    def add_row(self, matrix_id, parent_id=-1, row_item_id=0, **kwargs):
        """
        Method to add a new row to the selected Matrix.

        :param int matrix_id: the Matrix ID to add the row to.
        :keyword int parent_id: the ID of the parent row, if any.
        :keyword int row_item_id: the ID for the item associated with the new
                                  row.  For each matrix this will be:
                                  #. Functional/Hardware -> Function ID
                                  #. Functional/Software -> Function ID
                                  #. Functional/Testing -> Function ID
                                  #. Requirement/Hardware -> Requirement ID
                                  #. Requirement/Software -> Requirement ID
                                  #. Requirement/Validation -> Requirement ID
                                  #. Hardware/Testing -> Hardware ID
                                  #. Hardware/Validation -> Hardware ID
        :keyword dict **kwargs: any additional inputs provided.  Typically used
                                to pass the new code and name.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _code = kwargs.get('val1', '')
        _name = kwargs.get('val2', '')

        # Define local list variables.
        _row = [parent_id, row_item_id, _code, _name]
        _cells = []

        # Retrieve the matrix to add the row to.
        _matrix = self.dicMatrices[matrix_id]

        # Retrieve the existing column IDs and column item IDs.
        _query = "SELECT DISTINCT fld_col_id, fld_col_item_id \
                  FROM rtk_matrix \
                  WHERE fld_matrix_id={0:d}".format(matrix_id)
        (_results, _error_code, __) = self._dao.execute(_query,
                                                        commit=False)

        try:
            _n_col = len(_results)
        except TypeError:
            _n_col = 0

        # Add one cell for each column in the matrix.
        for i in range(_n_col):
            _query = "INSERT INTO rtk_matrix \
                      (fld_revision_id, fld_matrix_id, fld_matrix_type, \
                       fld_row_id, fld_col_id, fld_parent_id, fld_value, \
                       fld_row_item_id, fld_col_item_id) \
                      VALUES ({0:d}, {1:d}, {2:d}, {3:d}, {4:d}, {5:d}, '', \
                              {6:d}, {7:d})".format(_matrix.revision_id,
                                                    matrix_id,
                                                    _matrix.matrix_type,
                                                    _matrix.n_row,
                                                    _results[i][0], parent_id,
                                                    row_item_id,
                                                    _results[i][1])
            (__, _error_code, __) = self._dao.execute(_query, commit=True)

            _cells.append('')

        # If the row was successfully added to the open RTK Project database
        # add a new row to the Matrix's row dictionary and update the count of
        # rows in the Matrix.
        if _results:
            _row.extend(_cells)
            _matrix.dicRows[_matrix.n_row] = _row
            _matrix.n_row += 1

        return(_results, _error_code)

    def delete_row(self, matrix_id, row_id):
        """
        Method to delete the selected Row from the selected Matrix.

        :param int matrix_id: the Matrix ID to delete the Row from.
        :param int row_id: the ID of the Row to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _matrix = self.dicMatrices[matrix_id]

        _query = "DELETE FROM rtk_matrix \
                  WHERE fld_revision_id={0:d} \
                  AND fld_matrix_id={1:d} \
                  AND fld_row_id={2:d}".format(_matrix.revision_id, matrix_id,
                                               row_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the row was successfully deleted, remove it from the Matrix's row
        # dictionary and decrement the count of rows by one.  Then update the
        # remaining row IDs in case the removed row wasn't the last one.
        if _results:
            _query = "UPDATE rtk_matrix \
                      SET fld_row_id=fld_row_id-1 \
                      WHERE fld_revision_id={0:d} \
                      AND fld_matrix_id={1:d} \
                      AND fld_row_id>{2:d}".format(_matrix.revision_id,
                                                   matrix_id, row_id)
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

            _matrix.dicRows.pop(row_id)
            _matrix.n_row -= 1

        return(_results, _error_code)

    def add_column(self, matrix_id, col_item_id=0):
        """
        Method to add a new column to the selected Matrix.

        :param int matrix_id: the Matrix ID to add the column to.
        :keyword int col_item_id: the ID for the item associated with the new
                                  column.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Retrieve the matrix to add the row to.
        _matrix = self.dicMatrices[matrix_id]

        # Retrieve the existing column IDs and column item IDs.
        _query = "SELECT DISTINCT fld_row_id, fld_row_item_id \
                  FROM rtk_matrix \
                  WHERE fld_matrix_id={0:d}".format(matrix_id)
        (_results, _error_code, __) = self._dao.execute(_query,
                                                        commit=False)

        try:
            _n_row = len(_results)
        except TypeError:
            _n_row = 0

        # Add one cell for each row in the matrix.
        for i in range(_n_row):
            _query = "INSERT INTO rtk_matrix \
                      (fld_revision_id, fld_matrix_id, fld_matrix_type, \
                       fld_row_id, fld_col_id, fld_parent_id, fld_value, \
                       fld_row_item_id, fld_col_item_id) \
                      VALUES ({0:d}, {1:d}, {2:d}, {3:d}, {4:d}, {5:d}, '0', \
                              {6:d}, {7:d})".format(_matrix.revision_id,
                                                    matrix_id,
                                                    _matrix.matrix_type,
                                                    _results[i][0],
                                                    _matrix.n_col,
                                                    _matrix.dicRows[i][0],
                                                    _results[i][1],
                                                    col_item_id)
            (__, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the column was successfully added to the open RTK Project database
        # add a new column to each of the Matrix's rows and update the count of
        # columns in the Matrix.
        if _results:
            for _row in _matrix.dicRows.values():
                _row.append('0')

            _matrix.n_col += 1

        return(_results, _error_code)

    def delete_column(self, matrix_id, col_id):
        """
        Method to delete the selected column from the selected Matrix.

        :param int matrix_id: the Matrix ID to delete the Row from.
        :param int int_id: the ID of the column to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _matrix = self.dicMatrices[matrix_id]

        _query = "DELETE FROM rtk_matrix \
                  WHERE fld_revision_id={0:d} \
                  AND fld_matrix_id={1:d} \
                  AND fld_col_id={2:d}".format(_matrix.revision_id, matrix_id,
                                               col_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # If the column was successfully deleted, remove it's values from the
        # Matrix's row dictionary and decrement the count of columns by one.
        # Then update the remaining column IDs in case the removed column
        # wasn't the last one.
        if _results:
            _query = "UPDATE rtk_matrix \
                      SET fld_col_id=fld_col_id-1 \
                      WHERE fld_revision_id={0:d} \
                      AND fld_matrix_id={1:d} \
                      AND fld_col_id>{2:d}".format(_matrix.revision_id,
                                                   matrix_id, col_id)
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

            for _row in _matrix.dicRows.values():
                print _row, col_id
                _row.pop(col_id + 3)

            _matrix.n_col -= 1

        return(_results, _error_code)

    def save_cell(self, matrix_id, row_id, col_id, parent_id, value):
        """
        Method to save the cell information to the open RTK Project database.

        :param int matrix_id: the ID of the Matrix the row is associated with.
        :param int row_id: the ID of the row the cell to save is in.
        :param int col_id: the ID of the column the cell to save is in.
        :param int parent_id: the ID of the parent row.
        :param value: the value of the cell to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "UPDATE rtk_matrix \
                  SET fld_parent_id={0:d}, fld_value='{1:s}' \
                  WHERE fld_matrix_id={2:d} \
                  AND fld_row_id={3:d} \
                  AND fld_col_id={4:d}".format(parent_id, str(value),
                                               matrix_id, row_id, col_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        return(_results, _error_code)
