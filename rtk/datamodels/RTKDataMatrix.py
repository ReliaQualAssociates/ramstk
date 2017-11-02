# -*- coding: utf-8 -*-
#
#       rtk.datamodels.matrix.Matrix.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
RTKDataMatrix Module
###############################################################################
"""

# Import modules for localization support.
import gettext

import pandas as pd
from sqlalchemy import and_

# Import other RTK modules.
from dao import RTKMatrix                       # pylint: disable=E0401

_ = gettext.gettext


class RTKDataMatrix(object):
    """
    The Matrix data model is an aggregate model of N x M cell data models.  The
    attributes of a Matrix are:

    :ivar dict dicRows: Dictionary of the Rows associated with the Matrix.  Key
                        is the Row ID; value is a list as follows:
                        [parent_id, row item id, row item code, row item name,
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

    _tag = 'matrix'

    def __init__(self, dao, row_table, column_table):
        """
        Method to initialize a Matrix data model instance.
        """

        # Initialize private dictionary attributes.
        self._dic_row_hdrs = {}
        self._dic_column_hdrs = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._column_table = column_table
        self._row_table = row_table
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dtf_matrix = None

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = dao
        self.n_row = 1
        self.n_col = 1

    def select(self, col, row):
        """
        Method to select the value from the cell identified by col and row.

        :param str col: the column of the cell.  This is the first index of the
                        Pandas DataFrame.
        :param str row: the row of the cell.  This is the second index of the
                        Pandas DataFrame.
        :return: the value in the cell at (col, row).
        :rtype: float
        """

        return self.dtf_matrix[col][row]

    def select_all(self, revision_id, matrix_id, rindex, cindex, rheader,
                   cheader):
        """
        Method to select the row heaidngs, the column headings, and the cell
        values for the matrix then build the matrix as a Pandas DataFrame.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param int matrix_id: the ID of the Matrix to select all rows and all
                              columns for.
        :param int rindex: the index in the row table attributes containing the
                           module ID.
        :param int cindex: the index in the column table attributes containing
                           the module ID.
        :param int rheader: the index in the row table attributes containing
                            the text to use for the Matrix row headings.
        :param int cheader: the index in the column table attributes containing
                            the text to use for the Matrix column headings.
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        _return = False

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        _column_id = 0
        _lst_row_id = []
        _lst_value = []
        _dic_column = {}

        self.n_col = 0
        self.n_row = 0

        # Retrieve the dictionary of row headings.  The key is the row table's
        # module ID.  The value is the row table field with string data
        # (typically the code, description, or name field).
        for _row in _session.query(self._row_table).filter(
                self._row_table.revision_id == revision_id).all():
            _attributes = _row.get_attributes()
            self._dic_row_hdrs[_attributes[rindex]] = _attributes[rheader]

            self.n_row += 1

        # Retrieve the dictionary of column headings.  The key is the column
        # table's module ID.  The value is the column table field with string
        # data (typically the code, description, or name field).
        for _column in _session.query(self._column_table).filter(
                self._column_table.revision_id == revision_id).all():
            _attributes = _column.get_attributes()
            self._dic_column_hdrs[_attributes[cindex]] = _attributes[cheader]

            self.n_col += 1

        # Retrieve the matrix values for the desired Matrix ID.
        for _matrix in _session.query(RTKMatrix).filter(
                RTKMatrix.matrix_id == matrix_id).all():
            if _matrix.column_item_id == _column_id:
                _lst_row_id.append(_matrix.row_item_id)
                _lst_value.append(_matrix.value)
            else:
                _lst_row_id = [_matrix.row_item_id]
                _lst_value = [_matrix.value]
                _column_id = _matrix.column_item_id

            _dic_column[_column_id] = pd.Series(_lst_value, index=_lst_row_id)

        self.dtf_matrix = pd.DataFrame(_dic_column)

        _session.close()

        return _return

    def insert(self, item_id, heading, row=True):
        """
        Method to insert a row or a column into the matrix.

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix.
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        if row:
            self._dic_row_hdrs[item_id] = heading
            _values = [0] * self.n_col

            _tmp_matrix = self.dtf_matrix.transpose()
            _tmp_matrix.insert(self.n_row, item_id, _values)

            self.dtf_matrix = _tmp_matrix.transpose()
            self.n_row += 1

        else:
            self._dic_column_hdrs[item_id] = heading
            _values = [0] * self.n_row
            self.dtf_matrix.insert(self.n_col, item_id, _values)
            self.n_col += 1

        _session.close()

        return _return

    def delete(self, item_id, row=True):
        """
        Method to delete a column or row from the Matrix.

        :param int item_id: the ID of the row or column item to delete from the
                            Matrix.
        :param bool row: indicates whether to delete a row (default) or a
                         column identified by identifier.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _session = self.dao.RTK_SESSION(bind=self.dao.engine, autoflush=False,
                                        expire_on_commit=False)

        if row:
            _tmp_matrix = self.dtf_matrix.transpose()
            try:
                _tmp_matrix.pop(item_id)
                self._dic_row_hdrs.pop(item_id)
                self.dtf_matrix = _tmp_matrix.transpose()
                self.n_row -= 1
            except KeyError:
                _return = True

        else:
            try:
                self.dtf_matrix.pop(item_id)
                self._dic_column_hdrs.pop(item_id)
                self.n_col -= 1
            except KeyError:
                _return = True

        _session.close()

        return _return

    def update(self, matrix_id):
        """
        Method to update the Matrix associated with Matrix ID to the RTK
        Program database.

        :param int matrix_id: the ID of the Matrix to update.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Updating Matrix {0:s}.'.format(str(matrix_id))

        _session = self.dao.RTK_SESSION(bind=self.dao.engine,
                                        autoflush=True,
                                        autocommit=False,
                                        expire_on_commit=False)

        for _column_item_id in list(self.dtf_matrix.columns):
            for _row_item_id in list(self.dtf_matrix.index):
                _entity = _session.query(RTKMatrix).filter(
                    and_(RTKMatrix.matrix_id == matrix_id,
                         RTKMatrix.column_item_id == int(_column_item_id),
                         RTKMatrix.row_item_id == int(_row_item_id))).first()

                try:
                    if _entity is not None:
                        _entity.value = int(self.dtf_matrix[_column_item_id]
                                            [_row_item_id])
                        _session.add(_entity)
                        _error_code, _msg = self.dao.db_update(_session)
                except AttributeError:
                    _error_code = 6
                    _msg = 'RTK ERROR: Attempted to save non-existent ' \
                           'entity with Column ID {0:s} and Row ID {1:s} to ' \
                           'Matrix {2:s}.'.format(
                               str(_column_item_id), str(_row_item_id),
                               str(matrix_id))

        _session.close()

        return _error_code, _msg
