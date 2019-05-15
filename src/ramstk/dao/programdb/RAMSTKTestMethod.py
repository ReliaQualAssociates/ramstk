# -*- coding: utf-8 -*-
#
#       ramstk.dao.programdb.RAMSTKTestMethod.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKTestMethod Table."""

from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKTestMethod(RAMSTK_BASE):
    """
    Class to represent table ramstk_test_method in the RAMSTK Program database.

    This table shared a Many-to-One relationship with ramstk_op_stress.
    """

    __tablename__ = 'ramstk_test_method'
    __table_args__ = {'extend_existing': True}

    load_id = Column(
        'fld_load_id',
        Integer,
        ForeignKey('ramstk_op_load.fld_load_id'),
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
    remarks = Column('fld_remarks', BLOB, default=b'')

    # Define the relationships to other tables in the RAMSTK Program database.
    op_load = relationship('RAMSTKOpLoad', back_populates='test_method')

    is_mode = False
    is_mechanism = False
    is_opload = False
    is_opstress = False
    is_testmethod = True

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKTestMethod data model attributes.

        :return: {stress_id, test_id, description, boundary_conditions,
                  remarks} pairs
        :rtype: dict
        """
        _attributes = {
            'load_id': self.load_id,
            'test_id': self.test_id,
            'description': self.description,
            'boundary_conditions': self.boundary_conditions,
            'remarks': self.remarks
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the RAMSTKTestMethod data model attributes.

        :param dict attributes: values to assign to instance attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKTestMethod {0:d} attributes.". \
               format(self.test_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.boundary_conditions = str(
                none_to_default(attributes['boundary_conditions'], ''))
            self.remarks = none_to_default(attributes['remarks'], b'')
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKTestMethod.set_attributes().".format(str(_err))

        return _error_code, _msg
