# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hardware.AnalysisManager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hardware Controller Package analysis manager."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
# noinspection PyPackageRequirements
import pandas as pd
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.db.base import BaseDatabase
from ramstk.models.programdb import RAMSTKMatrix


class RAMSTKAnalysisManager():
    """Contain the attributes and methods of an analysis manager.

    This class manages the analyses for RAMSTK modules.  Attributes of the
    analysis manager are:

    :ivar dict _attributes: the dict used to hold the aggregate attributes for
        the hardware item being analyzed.
    :ivar tree: the treelib Tree() used to hold a copy of the data manager's
        tree.  This do not remain in-sync automatically.
    :type tree: :class:`treelib.Tree`
    :ivar RAMSTK_CONFIGURATION: the instance of the RAMSTKUserConfiguration
        class associated with this analysis manager.
    :type RAMSTK_CONFIGURATION: :class:`ramstk.RAMSTKUserConfiguration`
    """

    RAMSTK_USER_CONFIGURATION = None

    # pylint: disable=unused-argument
    def __init__(self, configuration: RAMSTKUserConfiguration,
                 **kwargs: Dict[str, Any]) -> None:
        """Initialize an instance of the hardware analysis manager.

        :param configuration: the RAMSTKUserConfiguration instance associated
            with the current instance of the RAMSTK application.
        :type configuration: :class:`ramstk.RAMSTKUserConfiguration`
        """
        # Initialize private dictionary attributes.
        self._attributes: Dict[str, Any] = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._tree: treelib.Tree = treelib.Tree()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.RAMSTK_USER_CONFIGURATION = configuration
        # TODO: Remove the following statement when all the controllers are
        #  updated to use RAMSTK
        self.RAMSTK_CONFIGURATION = self.RAMSTK_USER_CONFIGURATION

    def on_get_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes for the analysis manager.

        :param dict attributes: the data manager's attributes dict.
        :return: None
        :rtype: None
        """
        self._attributes = attributes

    def on_get_tree(self, dmtree: treelib.Tree) -> None:
        """Set the analysis manager's treelib Tree().

        :param dmtree: the data manager's treelib Tree().
        :type dmtree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._tree = dmtree


class RAMSTKDataManager():
    """This is the meta-class for all RAMSTK Data Managers.

    :ivar tree: the treelib Tree()that will contain the structure of the RAMSTK
        module being modeled.
    :type tree: :class:`treelib.Tree`
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _root = 0
    _tag = ''

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    # pylint: disable=unused-argument
    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize an RAMSTK data model instance."""
        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._parent_id: int = 0
        self._revision_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao: BaseDatabase = BaseDatabase()
        self.last_id: int = 0
        self.tree: treelib.Tree = treelib.Tree()

        # Add the root to the Tree().  This is neccessary to allow multiple
        # entries at the top level as there can only be one root in a treelib
        # Tree().  Manipulation and viewing of a RAMSTK module tree needs to
        # ignore the root of the tree.
        try:
            self.tree.create_node(tag=self._tag, identifier=self._root)
        except (treelib.tree.MultipleRootError, treelib.tree.NodeIDAbsentError,
                treelib.tree.DuplicatedNodeIdError):
            pass

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_select_revision, 'selected_revision')
        pub.subscribe(self.do_select_matrix, 'request_select_matrix')
        pub.subscribe(self.do_update_matrix, 'request_update_matrix')
        pub.subscribe(self.do_connect, 'succeed_connect_program_database')
        pub.subscribe(self.do_update_all, 'request_save_project')

        self._mtx_prefix = self._tag
        for _letter in self._tag.lower():
            if _letter in ('a', 'e', 'i', 'o', 'u'):
                self._mtx_prefix = self._mtx_prefix.replace(_letter, "")
        self._mtx_prefix = self._mtx_prefix + '_'

    def _on_select_revision(self, attributes: Dict[str, Any]) -> None:
        """Set the revision ID for the data manager."""
        self._revision_id = attributes['revision_id']

    @staticmethod
    def do_build_dict(records: List[object],
                      id_field: str) -> Dict[int, object]:
        """Convert a list of RAMSTK database records into a dict of records.

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
            _id = _record.get_attributes()[id_field]  # type: ignore
            _dic_records[_id] = _record

        return _dic_records

    def do_connect(self, dao: BaseDatabase) -> None:
        """Connect data manager to a database.

        :param dao: the BaseDatabase() instance (data access object)
            representing the connected RAMSTK Program database.
        :type dao: :class:`ramstk.db.base.BaseDatabase`
        """
        self.dao = dao

    def do_create_all_codes(self, prefix: str) -> None:
        """Create codes for all MODULE data table records.

        :param str prefix: the string to use as a prefix for each code.
        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            self.do_create_code(_node.identifier, prefix)  # type: ignore

    def do_delete(self, node_id: int, table: str) -> None:
        """Remove a RAMSTK data table record.

        :param int node_id: the node ID to be removed from the RAMSTK Program
            database.
        :param str table: the key in the module's treelib Tree() data package
            for the RAMSTK data table to remove the record from.
        :return: None
        :rtype: None
        """
        return self.dao.do_delete(self.do_select(node_id, table))

    def do_get_attributes(self, node_id: int, table: str) -> None:
        """Retrieve the RAMSTK data table attributes for node ID.

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
        """Broadcast the last used ID as the payload of a message.

        :param str module: the name of the workflow module to retrieve the
            last ID.
        :return: None
        :rtype: None
        """
        pub.sendMessage('succeed_get_last_{0:s}_id'.format(module),
                        last_id=self.last_id)

    def do_select(self, node_id: Any, table: str) -> Any:
        """Retrieve the RAMSTK data table record for the Node ID passed.

        :param node_id: the Node ID of the data package to retrieve.
        :param table: the name of the RAMSTK data table to retrieve the
            attributes from.
        :return: the instance of the RAMSTK<MODULE> data table that was
            requested or None if the requested Node ID does not exist.
        :raise: KeyError if passed the name of a table that isn't managed by
            this manager.
        """
        try:
            _entity = self.tree.get_node(node_id).data[table]
        except (AttributeError, treelib.tree.NodeIDAbsentError, TypeError):
            _entity = None

        return _entity

    def do_select_matrix(self, matrix_type: str) -> None:
        """Retrieve all the values for the matrix.

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
                _lst_matrix.append((_matrix.column_item_id,
                                    _matrix.row_item_id, _matrix.value))

            if self._mtx_prefix in matrix_type:
                pub.sendMessage('succeed_retrieve_matrix',
                                matrix_type=matrix_type,
                                matrix=_lst_matrix)
        except TypeError:
            pub.sendMessage('fail_retrieve_matrix',
                            error_message=("No matrix returned for {0:s} "
                                           "matrix.".format(str(matrix_type))))

    def do_set_tree(self, module_tree: treelib.Tree) -> None:
        """Set the MODULE treelib Tree().

        This method is generally used to respond to events such as successful
        calculations of the entire system.

        :param module_tree: the treelib Tree() to assign to the tree attribute.
        :type module_tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self.tree = module_tree

    # noinspection PyUnresolvedReferences
    def do_update_all(self) -> None:
        """Update all MODULE data table records in the RAMSTK Program database.

        :return: None
        :rtype: None
        """
        for _node in self.tree.all_nodes():
            self.do_update(_node.identifier)  # type: ignore

    def do_update_matrix(self, revision_id: int, matrix_type: str,
                         matrix: pd.DataFrame) -> None:
        """Update the matrix values in the RAMSTK Program database.

        :param int revision_id: the revisiond ID associated with the matrix to
            update.
        :param str matrix_type: the type (name) of the matrix to update.
        :param matrix: the actual matrix whose values are being updated in the
            database.
        :type matrix: :class:`pandas.DataFrame`
        :return: None
        :rtype: None
        """
        _row_ids = list(matrix.index)[1:]
        _column_ids = list(matrix.loc[0, :])[2:]

        _next_id = self.dao.get_last_id('ramstk_matrix', 'matrix_id') + 1
        for _row_id in _row_ids:
            for _col_id in _column_ids:
                _entity: List[object] = self.dao.do_select_all(
                    table=RAMSTKMatrix,
                    key=[
                        RAMSTKMatrix.revision_id, RAMSTKMatrix.matrix_type,
                        RAMSTKMatrix.column_item_id, RAMSTKMatrix.row_item_id
                    ],
                    value=[
                        revision_id, matrix_type,
                        int(_col_id) + 2,
                        int(_row_id)
                    ],
                    order=None,
                    _all=False)

                # If there is no corresponding record in RAMSTKMatrix, then
                # create a new RAMSTKMatrix record and add it.
                if _entity is None:
                    _entity = RAMSTKMatrix()
                    _entity.revision_id = revision_id
                    _entity.matrix_id = _next_id
                    _entity.matrix_type = matrix_type
                    _entity.column_item_id = int(_col_id) + 2
                    _entity.row_item_id = int(_row_id)
                _entity.value = int(matrix.iloc[_row_id, _col_id + 2])

                self.dao.do_update(_entity)

        pub.sendMessage('succeed_update_matrix')


class RAMSTKMatrixManager():
    """This is the meta-class for all RAMSTK Matrix Managers.

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

    def __init__(self, column_tables: Dict[str, List[Any]],
                 row_table: object) -> None:
        """Initialize a Matrix data model instance.

        :param dict column_tables: a dict of RAMSTK data table objects that
            comprise the columns.
        :param row_table: the RAMSTK data table object that comprises the rows
            of the matrix(ces) managed by this manager.
        """
        # Initialize private dictionary attributes.
        self._col_tree: Dict[str, treelib.Tree] = {}
        self._column_tables: Dict = column_tables
        self._dic_columns: Dict = {}
        self._dic_matrix: Dict = {}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._row_table: Any = row_table
        self._row_tree: treelib.Tree = treelib.Tree()

        # Initialize public dictionary attributes.
        self.dic_matrices: Dict[str, Any] = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.n_row: int = 1
        self.n_col: int = 1

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load, 'succeed_retrieve_matrix')
        pub.subscribe(self.do_request_update, 'do_request_update_matrix')

    def do_create_columns(self, matrix_type: str) -> None:
        """Create the matrix columns.

        This will effectively create the requested matrix since the row
        headings column was already created.  All values in the resulting
        matrix will be zero.  Call do_load() to load the actual values into
        the matrix.

        :param str matrix_type: the type (name) of the matrix to create the
            columns for.
        :return: None
        :rtype: None
        """
        self._dic_matrix = {
            'id': self._dic_matrix['id'],
            'display_name': self._dic_matrix['display_name']
        }

        try:
            _lst_columns = [
                self._col_tree[matrix_type].get_node(_node).tag
                for _node in self._col_tree[matrix_type].nodes
            ][1:]
        except KeyError:
            _lst_columns = []

        for _idx, _column in enumerate(_lst_columns):
            _values = [0] * (self.n_row - 1)
            _values.insert(0, _idx)
            self._dic_matrix[_column] = _values

        self.dic_matrices[matrix_type] = pd.DataFrame(self._dic_matrix)
        # pylint: disable=unused-variable
        (__, self.n_col) = self.dic_matrices[matrix_type].shape

    def do_create_rows(self, tree: treelib.Tree) -> None:
        """Create the matrix rows.

        All matrices for a given workflow module will have the same row
        headings.  This method will create a matrix with only one column
        containing the row headings.

        :param tree: the treelib Tree() containing the workflow module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._row_tree = tree

        # Build a dict containing the record ID's of the row module items
        # and the name to display in the RAMSTKMatrixView() for the rows.
        # We do not want the ID/tag of the root node in the tree as this is
        # simply the name of the work flow module.
        _row_ids = [
            self._row_tree.get_node(_node).identifier
            for _node in self._row_tree.nodes
        ][1:]
        _row_ids.insert(0, -1)
        _display_names = [
            self._row_tree.get_node(_node).tag
            for _node in self._row_tree.nodes
        ][1:]
        _display_names.insert(0, 'column_id')
        self._dic_matrix = {'id': _row_ids, 'display_name': _display_names}

        for _matrix_type in self._column_tables.keys():
            self.dic_matrices[_matrix_type] = pd.DataFrame(self._dic_matrix)
            # pylint: disable=unused-variable
            (self.n_row, __) = self.dic_matrices[_matrix_type].shape

            # If the column tree has already been loaded, we can build the
            # matrix.  Otherwise the matrix will be built when the column
            # tree is loaded.
            if self._col_tree:
                self.do_create_columns(_matrix_type)
                pub.sendMessage('request_select_matrix',
                                matrix_type=_matrix_type)

    def do_delete_column(self, node_id: int, matrix_type: str) -> Any:
        """Delete a column from the requested matrix.

        :param int node_id: the MODULE treelib Node ID that was deleted.
            Note that node ID = MODULE ID = matrix row ID.
        :param str matrix_type: the type of the Matrix to delete the column.
        :return: None
        :rtype: None
        :raise: KeyError if passed a node ID or matrix type that doesn't exist.
        """
        self.dic_matrices[matrix_type] = self.dic_matrices[matrix_type].drop(
            [node_id], axis=1)

    def do_delete_row(self, node_id: int) -> Any:
        """Delete a row from all the matrices.

        :param int node_id: the MODULE treelib Node ID that was deleted.
            Note that node ID = MODULE ID = matrix row ID.
        :return: None
        :rtype: None
        :raise: KeyError if passed a node ID that doesn't exist.
        """
        for _matrix in self.dic_matrices:
            self.dic_matrices[_matrix] = self.dic_matrices[_matrix].drop(
                [node_id])

    def do_insert_column(self, node_id: str, matrix_type: str) -> Any:
        """Insert a column into the requested matrix.

        :param int node_id: the MODULE treelib Node ID that was inserted.
            Note that node ID = MODULE ID = matrix row ID.
        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :return: None
        :rtype: None
        :raise: KeyError if passed a node ID or matrix type that doesn't exist.
        """
        _lst_values: List[Any] = [0] * self.n_row
        _lst_values[0] = ''

        self.dic_matrices[matrix_type] = pd.concat([
            self.dic_matrices[matrix_type],
            pd.DataFrame({node_id: _lst_values})
        ],
                                                   axis=1)

    def do_insert_row(self, node_id: int) -> Any:
        """Insert a row into each matrix managed by this matrix manager.

        :param int node_id: the MODULE treelib Node ID that was inserted.
            Note that node ID = MODULE ID = matrix row ID.
        :return: None
        :rtype: None
        """
        for _matrix in self.dic_matrices:
            # pylint: disable=unused-variable
            (__, _n_col) = self.dic_matrices[_matrix].shape
            _lst_values = [0] * _n_col

            _new_row = pd.DataFrame([_lst_values],
                                    columns=list(
                                        self.dic_matrices[_matrix].columns),
                                    index=[node_id])
            self.dic_matrices[_matrix] = self.dic_matrices[_matrix].append(
                _new_row)

    def do_load(self, matrix_type: str, matrix: List[Tuple[int]]) -> None:
        """Load the matrix values.

        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :param list matrix: a list of tuples (column ID, row ID, value) for the
            selected matrix.
        :return: None
        :rtype: None
        """
        # If the matrix type exists in the dict of matrices, then build it.
        # Otherwise just keep going.
        try:
            _n_columns = len(self.dic_matrices[matrix_type].columns)
            if _n_columns > 2:
                for _col in matrix:
                    self.dic_matrices[matrix_type].iloc[_col[1],
                                                        _col[0]] = _col[2]
                pub.sendMessage('succeed_load_matrix',
                                matrix_type=matrix_type,
                                matrix=self.dic_matrices[matrix_type])
        except KeyError:
            pass

    def do_request_update(self, revision_id: int, matrix_type: str) -> None:
        """Update the requested matrix in the RAMSTK program database.

        :param int revision_id: the Revision ID the associated matrix
            belongs to.
        :param str matrix_type: the type of the Matrix to select from.  This
            selects the correct matrix from the dict of matrices managed by
            this matrix manager.
        :return: None
        :rtype: None
        """
        if matrix_type in self.dic_matrices:
            pub.sendMessage('request_update_matrix',
                            revision_id=revision_id,
                            matrix_type=matrix_type,
                            matrix=self.dic_matrices[matrix_type])

    def do_select(self, matrix_type: str, row: int, col: str) -> Any:
        """Select the value from the cell identified by col and row.

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
        return self.dic_matrices[matrix_type].loc[row, col]
