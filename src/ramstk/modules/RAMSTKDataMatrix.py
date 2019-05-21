# -*- coding: utf-8 -*-
#
#       ramstk.modules.Matrix.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Datamodels Package RAMSTKDataMatrix."""

import pandas as pd
from sqlalchemy import and_, func

# Import other RAMSTK modules.
from ramstk.dao import RAMSTKMatrix


class RAMSTKDataMatrix():
    """
    The RAMSTK Data Matrix model.

    The Matrix data model is an aggregate model of N x M cell data models.  The
    attributes of a Matrix are:

    :ivar dict dic_row_hdrs: dictionary of the row heading text to use in
                             views.  Key is the <MODULE> ID; values are the
                             noun name to use in the row heading.
    :ivar dict dic_column_hdrs: dictionary of the column heading text to use
                                in views.  Key is the <MODULE> ID; values are
                                the noun name to use in the column heading.
    :ivar object _column_table: the RAMSTK Progam database table to use for the
                                matrix columns.  This is an SQLAlchemy object.
    :ivar object _row_table: the RAMSTK Progam database table to use for the
                             matrix rows.  This is an SQLAlchemy object.
    :ivar dtf_matrix: the :class:`pd.DataFrame` storing the Matrix.
    :ivar dao: the :class:`ramstk.dao.DAO` object used to communicate with the
               RAMSTK Program database.
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

    def __init__(self, dao, row_table, column_table):
        """Initialize a Matrix data model instance."""
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

    def do_create(self, revision_id, matrix_type, rkey='rkey', ckey='ckey'):
        """
        Create or refresh a data matrix.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param str matrix_type: the type of the Matrix to select all rows and
                                all columns for.
        :keyword int rkey: the key in the row table attributes containing the
                           module ID.
        :keyword int ckey: the key in the column table attributes containing
                           the module ID.
        """
        _return = False

        _lst_row_id = []
        _lst_value = []
        _dic_column = {}

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

        # Iterate over the rows (records from the "row" table) and then the
        # columns (records from the "column" table) to create, ultimately, a
        # pandas dataframe representation of the matrix.  Update the RAMSTK
        # Program database with the contents of this dataframe.
        for _row in _session.query(self._row_table).filter(
                self._row_table.revision_id == revision_id).all():
            _attributes = _row.get_attributes()
            _lst_row_id.append(_attributes[rkey])
            _lst_value.append(0)

            for _column in _session.query(self._column_table).filter(
                    self._column_table.revision_id == revision_id).all():
                _attributes = _column.get_attributes()
                _column_id = _attributes[ckey]
                _dic_column[_column_id] = pd.Series(
                    _lst_value, index=_lst_row_id)

        self.dtf_matrix = pd.DataFrame(_dic_column)

        self.do_update(revision_id, matrix_type)

        return _return

    def do_select(self, col, row):
        """
        Select the value from the cell identified by col and row.

        :param str col: the column of the cell.  This is the first index of the
                        Pandas DataFrame.
        :param str row: the row of the cell.  This is the second index of the
                        Pandas DataFrame.
        :return: the value in the cell at (col, row).
        :rtype: float
        """
        return self.dtf_matrix[col][row]

    def do_select_all(self, revision_id, matrix_type, **kwargs):
        r"""
        Select everything needed to build the matrix.

        This method selects the row headngs, the column headings, and the cell
        values for the matrix then build the matrix as a Pandas DataFrame.

        :param int revision_id: the ID of the Revision the desired Matrix is
                                associated with.
        :param str matrix_type: the type of the Matrix to select all rows and
                                all columns for.
        :param \**kwargs: See below

        :Keyword Arguments:
            * *rkey* (int) -- the key in the row table attributes containing
                              the module ID.
            * *ckey* (int) -- the key in the column table attributes containing
                              the module ID.
            * *rheader* (int) -- the index in the row table attributes
                                 containing the text to use for the Matrix row
                                 headings.
            * *cheader* (int) -- the index in the column table attributes
                                 containing the text to use for the Matrix
                                 column headings.
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """
        try:
            _rkey = kwargs['rkey']
        except KeyError:
            _rkey = 'rkey'
        try:
            _ckey = kwargs['ckey']
        except KeyError:
            _ckey = 'ckey'
        try:
            _rheader = kwargs['rheader']
        except KeyError:
            _rheader = 0
        try:
            _cheader = kwargs['cheader']
        except KeyError:
            _cheader = 0

        _return = False

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine, autoflush=False, expire_on_commit=False)

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
            self.dic_row_hdrs[_attributes[_rkey]] = _attributes[_rheader]

            self.n_row += 1

        # Retrieve the dictionary of column headings.  The key is the column
        # table's module ID.  The value is the column table field with string
        # data (typically the code, description, or name field).
        for _column in _session.query(self._column_table).filter(
                self._column_table.revision_id == revision_id).all():
            _attributes = _column.get_attributes()
            try:
                self.dic_column_hdrs[
                    _attributes[_ckey]] = _attributes[_cheader]
            except TypeError:
                print('FIXME: Handle TypeError in ' \
                      'RAMSTKDataMatrix.do_select_all().  Tuple indices must ' \
                      'be integers, not str.  This will be fixed when all ' \
                      'the RAMSTK database tables are converted to return ' \
                      'dicts from the get_attributes() method.  Matrix {0:s} ' \
                      'is not working.  See issue #59'.format(matrix_type))

            self.n_col += 1

        # Retrieve the matrix values for the desired Matrix ID.
        for _matrix in _session.query(RAMSTKMatrix).filter(
                and_(RAMSTKMatrix.revision_id == revision_id,
                     RAMSTKMatrix.matrix_type == matrix_type)).all():
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

    def do_insert(self, item_id, heading, row=True):
        """
        Insert a row or a column into the matrix.

        :param int item_id: the ID of the row or column item to insert into the
                            Matrix (this is the module ID associated with the
                            row or column to be inserted).
        :param str heading: the heading for the new row or column.
        :keyword bool row: indicates whether to insert a row (default) or a
                           column.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Inserting a row or column into the matrix.'

        if row:
            if (self.dtf_matrix.index == item_id).any():
                _error_code = 6
                _msg = 'RAMSTK ERROR: Attempting to insert row {0:d} into a ' \
                       'matrix already containing a row {0:d}.'.format(item_id)
            else:
                self.dic_row_hdrs[item_id] = heading
                _values = [0] * len(self.dtf_matrix.columns)
                try:
                    self.dtf_matrix.loc[item_id] = _values
                    self.n_row = len(self.dtf_matrix.index)
                except ValueError:
                    _error_code = 6
                    _msg = 'RAMSTK ERROR: Inserting row into matrix.  Row ' \
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
                _msg = 'RAMSTK ERROR: Inserting column into matrix.  Column ' \
                       '{0:d} already exists or adjacent column {1:d} does ' \
                       'NOT exist.'.format(item_id, self.n_col)

        return _error_code, _msg

    def do_delete(self, item_id, row=True):
        """
        Delete a column or row from the Matrix.

        :param int item_id: the ID of the row or column item to delete from the
                            Matrix.
        :param bool row: indicates whether to delete a row (default) or a
                         column identified by identifier.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Removing a row or column from the matrix.'

        if row:
            try:
                self.dtf_matrix = self.dtf_matrix.drop(item_id)
                self.dic_row_hdrs.pop(item_id)
                self.n_row = len(self.dtf_matrix.index)
            except (KeyError, ValueError):
                _error_code = 6
                _msg = 'RAMSTK ERROR: Attempted to drop non-existent row {0:d} ' \
                       'from the matrix.'.format(item_id)

        else:
            try:
                self.dtf_matrix.pop(item_id)
                self.dic_column_hdrs.pop(item_id)
                self.n_col = len(self.dtf_matrix.columns)
            except KeyError:
                _error_code = 6
                _msg = 'RAMSTK ERROR: Attempted to drop non-existent column ' \
                       '{0:d} from the matrix.'.format(item_id)

        return _error_code, _msg

    def do_update(self, revision_id, matrix_type):
        """
        Update the Matrix associated with Matrix type.

        :param int revision_id: the Revision ID the matrix is associated with.
        :param str matrix_type: the type of the Matrix to update.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RAMSTK SUCCESS: Updating Matrix {0:s}.'.format(matrix_type)

        _session = self.dao.RAMSTK_SESSION(
            bind=self.dao.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        try:
            _matrix_id = _session.query(RAMSTKMatrix).filter(
                RAMSTKMatrix.matrix_type == matrix_type).first().matrix_id
        except AttributeError:
            _matrix_id = _session.query(
                func.max(RAMSTKMatrix.matrix_id).label("last_id")).one()
            try:
                _matrix_id = int(_matrix_id.last_id) + 1
            except TypeError:
                _matrix_id = 1

        for _column_item_id in list(self.dtf_matrix.columns):
            for _row_item_id in list(self.dtf_matrix.index):
                _entity = _session.query(RAMSTKMatrix).filter(
                    and_(RAMSTKMatrix.revision_id == revision_id,
                         RAMSTKMatrix.matrix_type == matrix_type,
                         RAMSTKMatrix.column_item_id == int(_column_item_id),
                         RAMSTKMatrix.row_item_id == int(
                             _row_item_id))).first()

                try:
                    # If there is no corresponding record in RAMSTKMatrix, then
                    # create a new RAMSTKMatrix record and add it.
                    if _entity is None:
                        _entity = RAMSTKMatrix()
                        _entity.revision_id = revision_id
                        _entity.matrix_id = _matrix_id
                        _entity.matrix_type = matrix_type
                        _entity.column_item_id = int(_column_item_id)
                        _entity.row_item_id = int(_row_item_id)

                    _entity.value = int(
                        self.dtf_matrix[_column_item_id][_row_item_id])
                    _session.add(_entity)
                    _error_code, _msg = self.dao.db_update(_session)

                except AttributeError:
                    _error_code = 6
                    _msg = 'RAMSTK ERROR: Attempted to save non-existent ' \
                           'entity with Column ID {0:s} and Row ID {1:s} to ' \
                           'Matrix {2:s}.'.format(
                               str(_column_item_id), str(_row_item_id),
                               matrix_type)

        _session.close()

        return _error_code, _msg
