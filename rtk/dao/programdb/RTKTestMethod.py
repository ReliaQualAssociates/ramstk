# -*- coding: utf-8 -*-
#
#       rtk.dao.programdb.RTKTestMethod.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKTestMethod Table."""

from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKTestMethod(RTK_BASE):
    """
    Class to represent the table rtk_test_method in the RTK Program database.

    This table shared a Many-to-One relationship with rtk_op_stress.
    """

    __tablename__ = 'rtk_test_method'
    __table_args__ = {'extend_existing': True}

    stress_id = Column(
        'fld_stress_id',
        Integer,
        ForeignKey('rtk_op_stress.fld_stress_id'),
        nullable=False)
    test_id = Column(
        'fld_test_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', String(512), default='')
    boundary_conditions = Column(
        'fld_boundary_conditions', String(512), default='')
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    op_stress = relationship('RTKOpStress', back_populates='test_method')

    def get_attributes(self):
        """
        Retrieve the current values of the RTKTestMethod data model attributes.

        :return: {stress_id, test_id, description, boundary_conditions,
                  remarks} pairs
        :rtype: dict
        """
        _attributes = {
            'stress_id': self.stress_id,
            'test_id': self.test_id,
            'description': self.description,
            'boundary_conditions': self.boundary_conditions,
            'remarks': self.remarks
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the RTKTestMethod data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKTestMethod {0:d} attributes.". \
               format(self.test_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.boundary_conditions = str(
                none_to_default(attributes['boundary_conditions'], ''))
            self.remarks = str(none_to_default(attributes['remarks'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKTestMethod.set_attributes().".format(_err)

        return _error_code, _msg
