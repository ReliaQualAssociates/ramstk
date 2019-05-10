# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKMatrix.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMatrix Table Module."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKMatrix(RAMSTK_BASE):
    """Class to represent ramstk_matrix table in the RAMSTK Program database.

    Matrix types are one of the following:

        +-------------+--------------+--------------+
        |  Row Table  | Column Table |  Matrix Type |
        +-------------+--------------+--------------+
        | Function    | Hardware     | fnctn_hrdwr  |
        +-------------+--------------+--------------+
        | Function    | Software     | fnctn_sftwr  |
        +-------------+--------------+--------------+
        | Function    | Validation   | fnctn_vldtn  |
        +-------------+--------------+--------------+
        | Requirement | Hardware     | rqrmnt_hrdwr |
        +-------------+--------------+--------------+
        | Requirement | Software     | rqrmnt_sftwr |
        +-------------+--------------+--------------+
        | Requirement | Validation   | rqrmnt_vldtn |
        +-------------+--------------+--------------+
        | Hardware    | Testing      | hrdwr_tstng  |
        +-------------+--------------+--------------+
        | Hardware    | Validation   | hrdwr_vldtn  |
        +-------------+--------------+--------------+
        | Software    | Risk         |  sftwr_rsk   |
        +-------------+--------------+--------------+
        | Software    | Validation   | sftwr_vldtn  |
        +-------------+--------------+--------------+

    The primary key for this table consists of the revision_id, matrix_id,
    column_item_id, and row_item_id.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __tablename__ = 'ramstk_matrix'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        primary_key=True,
        nullable=False)
    matrix_id = Column('fld_matrix_id', Integer, primary_key=True, default=0)

    column_id = Column('fld_column_id', Integer, default=0)
    column_item_id = Column(
        'fld_column_item_id', Integer, primary_key=True, default=0)
    matrix_type = Column('fld_matrix_type', String(128), default='')
    parent_id = Column('fld_parent_id', Integer, default=0)
    row_id = Column('fld_row_id', Integer, default=0)
    row_item_id = Column(
        'fld_row_item_id', Integer, primary_key=True, default=0)
    value = Column('fld_value', Integer, default=0)

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='matrix')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKMatrix data model attributes.

        :return: {revision_id, matrix_id, column_id, column_item_id, parent_id,
                  row_id, row_item_id, type_id, value} pairs.
        :rtype: tuple
        """
        _attributes = {
            'revision_id': self.revision_id,
            'matrix_id': self.matrix_id,
            'column_id': self.column_id,
            'column_item_id': self.column_item_id,
            'matrix_type': self.matrix_type,
            'parent_id': self.parent_id,
            'row_id': self.row_id,
            'row_item_id': self.row_item_id,
            'value': self.value
        }

        return _attributes

    def set_attributes(self, values):
        """
        Set the RAMSTKMatrix data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKMatrix {0:d} attributes.". \
               format(self.matrix_id)

        try:
            self.column_id = int(none_to_default(values['column_id'], 0))
            self.column_item_id = int(
                none_to_default(values['column_item_id'], 0))
            self.matrix_type = str(none_to_default(values['matrix_type'], ''))
            self.parent_id = int(none_to_default(values['parent_id'], 0))
            self.row_id = int(none_to_default(values['row_id'], 0))
            self.row_item_id = int(none_to_default(values['row_item_id'], 0))
            self.value = float(none_to_default(values['value'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKMatrix.set_attributes().".format(str(_err))

        return _error_code, _msg
