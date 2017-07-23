#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTValidation.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTValidation Table
==============================
"""

from datetime import date, timedelta

# Import the database models.
from sqlalchemy import BLOB, Column, Date, Float, ForeignKey, Integer, String
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


class RTKValidation(Base):
    """
    Class to represent the table rtk_validation in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_validation'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    validation_id = Column('fld_validation_id', Integer, primary_key=True,
                           autoincrement=True, nullable=False)

    acceptable_maximum = Column('fld_acceptable_maximum', Float, default=0.0)
    acceptable_mean = Column('fld_acceptable_mean', Float, default=0.0)
    acceptable_minimum = Column('fld_acceptable_minimum', Float, default=0.0)
    acceptable_variance = Column('fld_acceptable_variance', Float, default=0.0)
    confidence = Column('fld_confidence', Float, default=95.0)
    cost_average = Column('fld_cost_average', Float, default=0.0)
    cost_maximum = Column('fld_cost_maximum', Float, default=0.0)
    cost_mean = Column('fld_cost_mean', Float, default=0.0)
    cost_minimum = Column('fld_cost_minimum', Float, default=0.0)
    cost_variance = Column('fld_cost_variance', Float, default=0.0)
    date_end = Column('fld_date_end', Date,
                      default=date.today() + timedelta(days=30))
    date_start = Column('fld_date_start', Date, default=date.today())
    description = Column('fld_description', BLOB, default='')
    measurement_unit_id = Column('fld_measurement_unit_id', Integer, default=0)
    status_id = Column('fld_status', Float, default=0.0)
    task_type_id = Column('fld_type_id', Integer, default=0)
    task_specification = Column('fld_task_specification', String(512),
                                default='')
    time_average = Column('fld_time_average', Float, default=0.0)
    time_maximum = Column('fld_time_maximum', Float, default=0.0)
    time_mean = Column('fld_time_mean', Float, default=0.0)
    time_minimum = Column('fld_time_minimum', Float, default=0.0)
    time_variance = Column('fld_time_variance', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='validation')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKValidation data model
        attributes.

        :return: (revision_id, validation_id, acceptable_maximum,
                  acceptable_mean, acceptable_minimum, acceptable_variance,
                  confidence, cost_average, cost_maximum, cost_mean,
                  cost_minimum, cost_variance, date_end, date_start,
                  description, measurement_unit_id, status_id, task_type_id,
                  task_specification, time_average, time_maximum, time_mean,
                  time_minimum, time_variance)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.validation_id, 
                       self.acceptable_maximum, self.acceptable_mean, 
                       self.acceptable_minimum, self.acceptable_variance, 
                       self.confidence, self.cost_average, self.cost_maximum, 
                       self.cost_mean, self.cost_minimum, self.cost_variance, 
                       self.date_end, self.date_start, self.description, 
                       self.measurement_unit_id, self.status_id, 
                       self.task_type_id, self.task_specification, 
                       self.time_average, self.time_maximum, self.time_mean, 
                       self.time_minimum, self.time_variance)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKValidation data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKValidation {0:d} attributes.". \
               format(self.validation_id)

        try:
            self.acceptable_maximum = float(attributes[0])
            self.acceptable_mean = float(attributes[1])
            self.acceptable_minimum = float(attributes[2])
            self.acceptable_variance = float(attributes[3])
            self.confidence = float(attributes[4])
            self.cost_average = float(attributes[5])
            self.cost_maximum = float(attributes[6])
            self.cost_mean = float(attributes[7])
            self.cost_minimum = float(attributes[8])
            self.cost_variance = float(attributes[9])
            self.date_end = attributes[10]
            self.date_start = attributes[11]
            self.description = str(attributes[12])
            self.measurement_unit_id = int(attributes[13])
            self.status_id = int(attributes[14])
            self.task_type_id = int(attributes[15])
            self.task_specification = str(attributes[16])
            self.time_average = float(attributes[17])
            self.time_maximum = float(attributes[18])
            self.time_mean = float(attributes[19])
            self.time_minimum = float(attributes[20])
            self.time_variance = float(attributes[21])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKValidation.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKValidation attributes."

        return _error_code, _msg
