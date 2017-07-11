#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKControl.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKControl Package.
"""

# Import the database models.
from sqlalchemy import Column, ForeignKey, Integer, String
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


class RTKControl(Base):
    """
    Class to represent the table rtk_control in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_control'

    cause_id = Column('fld_cause_id', Integer,
                      ForeignKey('rtk_cause.fld_cause_id'), nullable=False)
    control_id = Column('fld_control_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    cause = relationship('RTKCause', back_populates='control')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKControl data model
        attributes.

        :return: (cause_id, control_id, description, type_id)
        :rtype: tuple
        """

        _attributes = (self.cause_id, self.control_id, self.description,
                       self.type_id)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKControl data model attributes.

        :param tuple attributes: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKControl {0:d} attributes.". \
               format(self.control_id)

        try:
            self.description = str(attributes[0])
            self.type_id = int(attributes[1])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKControl.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKControl attributes."

        return _error_code, _msg
