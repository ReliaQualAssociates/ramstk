# -*- coding: utf-8 -*-
#
#       rtk.dao.RTValidation.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTValidation Table
===============================================================================
"""

from datetime import date, timedelta

from sqlalchemy import BLOB, Column, Date, Float, \
                       ForeignKey, Integer, String  # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


class RTKValidation(RTK_BASE):
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
            self.acceptable_maximum = float(
                none_to_default(attributes[0], 0.0))
            self.acceptable_mean = float(none_to_default(attributes[1], 0.0))
            self.acceptable_minimum = float(
                none_to_default(attributes[2], 0.0))
            self.acceptable_variance = float(
                none_to_default(attributes[3], 0.0))
            self.confidence = float(none_to_default(attributes[4], 95.0))
            self.cost_average = float(none_to_default(attributes[5], 0.0))
            self.cost_maximum = float(none_to_default(attributes[6], 0.0))
            self.cost_mean = float(none_to_default(attributes[7], 0.0))
            self.cost_minimum = float(none_to_default(attributes[8], 0.0))
            self.cost_variance = float(none_to_default(attributes[9], 0.0))
            self.date_end = none_to_default(attributes[10],
                                            date.today() + timedelta(days=30))
            self.date_start = none_to_default(attributes[11], date.today())
            self.description = str(none_to_default(attributes[12], ''))
            self.measurement_unit_id = int(none_to_default(attributes[13], 0))
            self.status_id = int(none_to_default(attributes[14], 0))
            self.task_type_id = int(none_to_default(attributes[15], 0))
            self.task_specification = str(none_to_default(attributes[16], ''))
            self.time_average = float(none_to_default(attributes[17], 0.0))
            self.time_maximum = float(none_to_default(attributes[18], 0.0))
            self.time_mean = float(none_to_default(attributes[19], 0.0))
            self.time_minimum = float(none_to_default(attributes[20], 0.0))
            self.time_variance = float(none_to_default(attributes[21], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKValidation.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKValidation attributes."

        return _error_code, _msg
