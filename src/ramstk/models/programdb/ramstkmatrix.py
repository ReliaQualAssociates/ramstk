# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKMatrix.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMatrix Data Table Module."""

# Third Party Imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKMatrix(RAMSTK_BASE, RAMSTKBaseTable):
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

    __defaults__ = {
        'matrix_id': 0,
        'column_id': 0,
        'column_item_id': 0,
        'matrix_type': '',
        'parent_id': 0,
        'row_id': 0,
        'row_item_id': 0,
        'value': 0
    }

    __tablename__ = 'ramstk_matrix'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        primary_key=True,
        nullable=False,
    )
    matrix_id = Column('fld_matrix_id',
                       Integer,
                       primary_key=True,
                       default=__defaults__['matrix_id'])

    column_id = Column('fld_column_id',
                       Integer,
                       default=__defaults__['column_id'])
    column_item_id = Column('fld_column_item_id',
                            Integer,
                            primary_key=True,
                            default=__defaults__['column_item_id'])
    matrix_type = Column('fld_matrix_type',
                         String(128),
                         default=__defaults__['matrix_type'])
    parent_id = Column('fld_parent_id',
                       Integer,
                       default=__defaults__['parent_id'])
    row_id = Column('fld_row_id', Integer, default=__defaults__['row_id'])
    row_item_id = Column('fld_row_item_id',
                         Integer,
                         primary_key=True,
                         default=__defaults__['row_item_id'])
    value = Column('fld_value', Integer, default=__defaults__['value'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship(  # type: ignore
        'RAMSTKRevision',
        back_populates='matrix',
    )

    def get_attributes(self):
        """Retrieve current values of the RAMSTKMatrix data model attributes.

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
            'value': self.value,
        }

        return _attributes
