# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKOpStress.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKOpStress Table
===============================================================================
"""

from sqlalchemy import BLOB, Column, ForeignKey, \
                       Integer, String              # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKOpStress(RTK_BASE):
    """
    Class to represent the table rtk_op_stress in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_op_load.
    """

    __tablename__ = 'rtk_op_stress'
    __table_args__ = {'extend_existing': True}

    load_id = Column('fld_load_id', Integer,
                     ForeignKey('rtk_op_load.fld_load_id'), nullable=False)
    stress_id = Column('fld_stress_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    load_history = Column('fld_load_history', Integer, default=0)
    measurable_parameter = Column('fld_measurable_parameter', Integer,
                                  default=0)
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    op_load = relationship('RTKOpLoad', back_populates='op_stress')
    test_method = relationship('RTKTestMethod', back_populates='op_stress')

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mode data model
        attributes.

        :return: (load_id, stress_id, description, load_history,
                  measurable_parameter, remarks)
        :rtype: tuple
        """

        _attributes = (self.load_id, self.stress_id, self.description,
                       self.load_history, self.measurable_parameter,
                       self.remarks)

        return _attributes

    def set_attributes(self, values):
        """
        Method to set the Stress data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKOpStress {0:d} attributes.". \
               format(self.stress_id)

        try:
            self.description = str(none_to_default(values[0], ''))
            self.load_history = int(none_to_default(values[1], 0))
            self.measurable_parameter = int(none_to_default(values[2], 0))
            self.remarks = str(none_to_default(values[3], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKOpStress.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKOpStress attributes."

        return _error_code, _msg
