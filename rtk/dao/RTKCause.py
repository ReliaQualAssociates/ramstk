#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKCause.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKCause Package.
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


class RTKCause(Base):
    """
    Class to represent the table rtk_cause in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_mechanism.
    This table shared a One-to-Many relationship with rtk_control.
    This table shared a One-to-Many relationship with rtk_action.
    """

    __tablename__ = 'rtk_cause'
    __table_args__ = {'extend_existing': True}

    mechanism_id = Column('fld_mechanism_id', Integer,
                          ForeignKey('rtk_mechanism.fld_mechanism_id'),
                          nullable=False)
    cause_id = Column('fld_cause_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    rpn = Column('fld_rpn', Integer, default=0)
    rpn_detection = Column('fld_rpn_detection', Integer, default=0)
    rpn_detection_new = Column('fld_rpn_detection_new', Integer, default=0)
    rpn_new = Column('fld_rpn_new', Integer, default=0)
    rpn_occurrence = Column('fld_rpn_occurrence', Integer, default=0)
    rpn_occurrence_new = Column('fld_rpn_occurrence_new', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    mechanism = relationship('RTKMechanism', back_populates='cause')
    control = relationship('RTKControl', back_populates='cause')
    action = relationship('RTKAction', back_populates='cause')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKCause data model
        attributes.

        :return: (mode_id, mechanism_id, cause_id, description, rpn_occurrence,
                  rpn_detection, rpn, rpn_occurrence_new, rpn_detection_new,
                  rpn_new)
        :rtype: tuple
        """

        _attributes = (self.mechanism_id, self.cause_id, self.description,
                       self.rpn, self.rpn_detection, self.rpn_detection_new,
                       self.rpn_new, self.rpn_occurrence,
                       self.rpn_occurrence_new)

        return _attributes

    def set_attributes(self, values):
        """
        Method to set the RTKCause data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKCause {0:d} attributes.". \
               format(self.cause_id)

        try:
            self.description = str(values[0])
            self.rpn = int(values[1])
            self.rpn_detection = int(values[2])
            self.rpn_detection_new = int(values[3])
            self.rpn_new = int(values[4])
            self.rpn_occurrence = int(values[5])
            self.rpn_occurrence_new = int(values[6])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKCause.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKCause attributes."

        return _error_code, _msg

