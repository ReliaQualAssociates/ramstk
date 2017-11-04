# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMatrix.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKMatrix Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship               # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKMatrix(RTK_BASE):
    """
    Class to represent the rtk_matrix table in the RTK Program database.
    Matrix types are one of the following:

    +-----------+------------+-------------+
    | Matrix ID |    Rows    |   Columns   |
    +===========+============+=============+
    |     1     | Function   | Hardware    |
    +-----------+------------+-------------+
    |     2     | Function   | Software    |
    +-----------+------------+-------------+
    |     3     | Function   | Testing     |
    +-----------+------------+-------------+
    |    11     | Requirement| Hardware    |
    +-----------+------------+-------------+
    |    12     | Requirement| Software    |
    +-----------+------------+-------------+
    |    13     | Requirement| Validation  |
    +-----------+------------+-------------+
    |    21     | Hardware   | Testing     |
    +-----------+------------+-------------+
    |    22     | Hardware   | Validation  |
    +-----------+------------+-------------+

    The primary key for this table consists of the revision_id, matrix_id,
    column_item_id, and row_item_id.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_matrix'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         primary_key=True, nullable=False)
    matrix_id = Column('fld_matrix_id', Integer, primary_key=True,
                       default=0)

    column_id = Column('fld_column_id', Integer, default=0)
    column_item_id = Column('fld_column_item_id', Integer, primary_key=True,
                            default=0)
    parent_id = Column('fld_parent_id', Integer, default=0)
    row_id = Column('fld_row_id', Integer, default=0)
    row_item_id = Column('fld_row_item_id', Integer, primary_key=True,
                         default=0)
    type_id = Column('fld_type_id', Integer, default=0)
    value = Column('fld_value', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='matrix')

    def get_attributes(self):
        """
        Method to retrieve the current values of the TKMatrix data model
        attributes.

        :return: (revision_id, matrix_id, column_id, column_item_id, parent_id,
                  row_id, row_item_id, type_id, value)
        :rtype: tuple
        """

        _values = (self.revision_id, self.matrix_id, self.column_id,
                   self.column_item_id, self.parent_id, self.row_id,
                   self.row_item_id, self.type_id, self.value)

        return _values

    def set_attributes(self, values):
        """
        Method to set the RTKMatrix data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMatrix {0:d} attributes.". \
               format(self.matrix_id)

        try:
            self.column_id = int(none_to_default(values[0], 0))
            self.column_item_id = int(none_to_default(values[1], 0))
            self.parent_id = int(none_to_default(values[2], 0))
            self.row_id = int(none_to_default(values[3], 0))
            self.row_item_id = int(none_to_default(values[4], 0))
            self.type_id = int(none_to_default(values[5], 0))
            self.value = float(none_to_default(values[6], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMatrix.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMatrix attributes."

        return _error_code, _msg
