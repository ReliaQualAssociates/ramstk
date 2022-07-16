# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_matrix_table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMatrix Table Model."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Type, Union

# Third Party Imports
import pandas as pd

# RAMSTK Local Imports
from ..dbrecords import RAMSTKMatrixRecord
from .basetable import RAMSTKBaseTable


class RAMSTKMatrixTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Matrix table model."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_matrix_id"
    _db_tablename = "ramstk_matrix"
    _select_msg = "selected_revision"
    _tag = "matrix"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKMatrix table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "description",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKMatrixRecord] = RAMSTKMatrixRecord

        # Initialize public dictionary attributes.
        self.matrix_df = pd.DataFrame()

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "matrix_id"

        # Subscribe to PyPubSub messages.

    def do_build_matrix(self, column_lst: List[str], row_lst: List[str]) -> None:
        """Build the matrix from the columns and rows provided.

        :param column_lst: the list of column header strings.
        :param row_lst: the list of row header strings.
        :return: None
        :rtype: None
        """
        _column_dic = {_column_str: [0] * len(row_lst) for _column_str in column_lst}
        self.matrix_df = pd.DataFrame(_column_dic, index=row_lst)

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attribute_dic: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKMatrixRecord:
        """Get a new record instance with attributes set.

        :param attribute_dic: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record_obj = self._record()
        _new_record_obj.revision_id = attribute_dic["revision_id"]
        _new_record_obj.matrix_id = self.last_id + 1
        _new_record_obj.description = attribute_dic["description"]

        return _new_record_obj
