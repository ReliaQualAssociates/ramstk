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

    :ivar dict dic_row_hdrs: dictionary of the row heading text to use in
                              views.  Key is the <MODULE> ID; values are the
                              noun name to use in the row heading.
    :ivar dict dic_column_hdrs: dictionary of the column heading text to use
                                 in views.  Key is the <MODULE> ID; values are
                                 the noun name to use in the column heading.
    :ivar object _column_table: the RTK Progam database table to use for the
                                matrix columns.  This is an SQLAlchemy object.
    :ivar object _row_table: the RTK Progam database table to use for the
                             matrix rows.  This is an SQLAlchemy object.
    :ivar dtf_matrix: the :py:class:`pd.DataFrame` storing the Matrix.
    :ivar dao: the :py:class:`rtk.dao.DAO` object used to communicate with the
               RTK Program database.
    :ivar int n_row: the number of rows in the Matrix.
    :ivar int n_col: the number of columns in the Matrix.

    There are currently 10 matrices as defined by their matrix ID.  These are:

        +-----------+-------------+--------------+
        | Matrix ID |  Row Table  | Column Table |
        +-----------+-------------+--------------+
        |     1     | Function    | Hardware     |
        +-----------+-------------+--------------+
        |     2     | Function    | Software     |
        +-----------+-------------+--------------+
        |     3     | Function    | Validation   |
        +-----------+-------------+--------------+
        |    11     | Requirement | Hardware     |
        +-----------+-------------+--------------+
        |    12     | Requirement | Software     |
        +-----------+-------------+--------------+
        |    13     | Requirement | Validation   |
        +-----------+-------------+--------------+
        |    21     | Hardware    | Testing      |
        +-----------+-------------+--------------+
        |    22     | Hardware    | Validation   |
        +-----------+-------------+--------------+
        |    31     | Software    | Risk         |
        +-----------+-------------+--------------+
        |    32     | Software    | Validation   |
        +-----------+-------------+--------------+
    """

    _tag = 'matrix'

    def __init__(self, dao, row_table, column_table):
        """
        Method to initialize a Matrix data model instance.
        """

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._column_table = column_table
        self._row_table = row_table

        # Initialize public dictionary attributes.
        self.dtf_matrix = None
        self.dic_row_hdrs = {}
        self.dic_column_hdrs = {}

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

    def select_all(self, revision_id, matrix_id, rindex=0, cindex=0, rheader=0,
                   cheader=0):
        """
        Method to select the row heaidngs, the column headings, and the cell
        values for the matrix then build the matrix as a Pandas DataFrame.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param int matrix_id: the ID of the Matrix to select all rows and all
                              columns for.
        :keyword int rindex: the index in the row table attributes containing
                             the module ID.
        :keyword int cindex: the index in the column table attributes
                             containing the module ID.
        :keyword int rheader: the index in the row table attributes containing
                              the text to use for the Matrix row headings.
        :keyword int cheader: the index in the column table attributes
                              containing the text to use for the Matrix column
                              headings.
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
            self.dic_row_hdrs[_attributes[rindex]] = _attributes[rheader]

            self.n_row += 1

        # Retrieve the dictionary of column headings.  The key is the column
        # table's module ID.  The value is the column table field with string
        # data (typically the code, description, or name field).
        for _column in _session.query(self._column_table).filter(
                self._column_table.revision_id == revision_id).all():
            _attributes = _column.get_attributes()
            self.dic_column_hdrs[_attributes[cindex]] = _attributes[cheader]

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
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Inserting a row or column into the matrix.'

        if row:
            if (self.dtf_matrix.index == item_id).any():
                _error_code = 6
                _msg = 'RTK ERROR: Attempting to insert row {0:d} into a ' \
                       'matrix already containing a row {0:d}.'.format(item_id)
            else:
                self.dic_row_hdrs[item_id] = heading
                _values = [0] * len(self.dtf_matrix.columns)

                try:
                    self.dtf_matrix.loc[item_id] = _values
                    self.n_row = len(self.dtf_matrix.index)
                except ValueError:
                    _error_code = 6
                    _msg = 'RTK ERROR: Inserting row into matrix.  Row ' \
                           '{0:d} already exists or adjacent row {1:d} does ' \
                           'NOT exist.'.format(item_id, self.n_row - 1)
        else:
            self.dic_column_hdrs[item_id] = heading
            _values = [0] * len(self.dtf_matrix.index)

            try:
                self.dtf_matrix.insert(self.n_col, item_id, _values)
                self.n_col = len(self.dtf_matrix.columns)
            except ValueError:
                _error_code = 6
                _msg = 'RTK ERROR: Inserting column into matrix.  Column ' \
                       '{0:d} already exists or adjacent column {1:d} does ' \
                       'NOT exist.'.format(item_id, self.n_col)

        return _error_code, _msg

    def delete(self, item_id, row=True):
        """
        Method to delete a column or row from the Matrix.

        :param int item_id: the ID of the row or column item to delete from the
                            Matrix.
        :param bool row: indicates whether to delete a row (default) or a
                         column identified by identifier.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = 'RTK SUCCESS: Removing a row or column from the matrix.'

        if row:
            try:
                self.dtf_matrix = self.dtf_matrix.drop(item_id)
                self.dic_row_hdrs.pop(item_id)
                self.n_row = len(self.dtf_matrix.index)
            except(KeyError, ValueError):
                _error_code = 6
                _msg = 'RTK ERROR: Attempted to drop non-existent row {0:d} ' \
                       'from the matrix.'.format(item_id)

        else:
            try:
                self.dtf_matrix.pop(item_id)
                self.dic_column_hdrs.pop(item_id)
                self.n_col = len(self.dtf_matrix.columns)
            except KeyError:
                _error_code = 6
                _msg = 'RTK ERROR: Attempted to drop non-existent column ' \
                       '{0:d} from the matrix.'.format(item_id)

        return _error_code, _msg

    def update(self, revision_id, matrix_id):
        """
        Method to update the Matrix associated with Matrix ID to the RTK
        Program database.

        :param int revision_id: the Revision ID the matrix is associated with.
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
