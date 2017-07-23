#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKOpStress.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKOpStress Table
==============================
"""

# Import the database models.
from sqlalchemy import BLOB, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKOpStress(Base):
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
            self.description = str(values[0])
            self.load_history = int(values[1])
            self.measurable_parameter = int(values[2])
            self.remarks = str(values[3])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKOpStress.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKOpStress attributes."

        return _error_code, _msg
