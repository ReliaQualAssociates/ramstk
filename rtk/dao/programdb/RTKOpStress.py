# -*- coding: utf-8 -*-
#
#       rtk.dao.programdb.RTKOpStress.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKOpStress Table."""

from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKOpStress(RTK_BASE):
    """
    Class to represent the table rtk_op_stress in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_op_load.
    This table shares a One-to-Many relationship with rtk_test_method.
    """

    __tablename__ = 'rtk_op_stress'
    __table_args__ = {'extend_existing': True}

    load_id = Column(
        'fld_load_id',
        Integer,
        ForeignKey('rtk_op_load.fld_load_id'),
        nullable=False)
    stress_id = Column(
        'fld_stress_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', String(512), default='')
    load_history = Column('fld_load_history', Integer, default=0)
    measurable_parameter = Column(
        'fld_measurable_parameter', Integer, default=0)
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    op_load = relationship('RTKOpLoad', back_populates='op_stress')
    test_method = relationship(
        'RTKTestMethod', back_populates='op_stress', cascade='all,delete')

    def get_attributes(self):
        """
        Retrieve the current values of the Op Stress data model attributes.

        :return: {load_id, stress_id, description, load_history,
                  measurable_parameter, remarks} pairs
        :rtype: tuple
        """
        _attributes = {
            'load_id': self.load_id,
            'stress_id': self.stress_id,
            'description': self.description,
            'load_history': self.load_history,
            'measurable_parameter': self.measurable_parameter,
            'remarks': self.remarks
        }

        return _attributes

    def set_attributes(self, values):
        """
        Set the Stress data model attributes.

        :param dict values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKOpStress {0:d} attributes.". \
               format(self.stress_id)

        try:
            self.description = str(none_to_default(values['description'], ''))
            self.load_history = int(none_to_default(values['load_history'], 0))
            self.measurable_parameter = int(
                none_to_default(values['measurable_parameter'], 0))
            self.remarks = str(none_to_default(values['remarks'], ''))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKOpStress.set_attributes().".format(_err)

        return _error_code, _msg
