# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKValidation.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKValidation Table."""

from datetime import date, timedelta

from sqlalchemy import BLOB, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.statistics import calculate_beta_bounds
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKValidation(RTK_BASE):
    """
    Class to represent the table rtk_validation in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_validation'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('rtk_revision.fld_revision_id'),
        nullable=False)
    validation_id = Column(
        'fld_validation_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    acceptable_maximum = Column('fld_acceptable_maximum', Float, default=0.0)
    acceptable_mean = Column('fld_acceptable_mean', Float, default=0.0)
    acceptable_minimum = Column('fld_acceptable_minimum', Float, default=0.0)
    acceptable_variance = Column('fld_acceptable_variance', Float, default=0.0)
    confidence = Column('fld_confidence', Float, default=95.0)
    cost_average = Column('fld_cost_average', Float, default=0.0)
    cost_ll = Column('fld_cost_ll', Float, default=0.0)
    cost_maximum = Column('fld_cost_maximum', Float, default=0.0)
    cost_mean = Column('fld_cost_mean', Float, default=0.0)
    cost_minimum = Column('fld_cost_minimum', Float, default=0.0)
    cost_ul = Column('fld_cost_ul', Float, default=0.0)
    cost_variance = Column('fld_cost_variance', Float, default=0.0)
    date_end = Column(
        'fld_date_end', Date, default=date.today() + timedelta(days=30))
    date_start = Column('fld_date_start', Date, default=date.today())
    description = Column('fld_description', BLOB, default='')
    measurement_unit = Column('fld_measurement_unit', String(256), default='')
    name = Column('fld_name', String(256), default='')
    status = Column('fld_status', Float, default=0.0)
    task_type = Column('fld_type', String(256), default='')
    task_specification = Column(
        'fld_task_specification', String(512), default='')
    time_average = Column('fld_time_average', Float, default=0.0)
    time_ll = Column('fld_time_ll', Float, default=0.0)
    time_maximum = Column('fld_time_maximum', Float, default=0.0)
    time_mean = Column('fld_time_mean', Float, default=0.0)
    time_minimum = Column('fld_time_minimum', Float, default=0.0)
    time_ul = Column('fld_time_ul', Float, default=0.0)
    time_variance = Column('fld_time_variance', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='validation')

    def get_attributes(self):
        """
        Retrieve the current values of the RTKValidation data model attributes.

        :return: {revision_id, validation_id, acceptable_maximum,
                  acceptable_mean, acceptable_minimum, acceptable_variance,
                  confidence, cost_average, cost_ll. cost_maximum, cost_mean,
                  cost_minimum, cost_l, cost_variance, date_end, date_start,
                  description, measurement_unit_id, status_id, task_type_id,
                  task_specification, time_average, time_ll, time_maximum,
                  time_mean, time_minimum, time_ul, time_variance} pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'validation_id': self.validation_id,
            'acceptable_maximum': self.acceptable_maximum,
            'acceptable_mean': self.acceptable_mean,
            'acceptable_minimum': self.acceptable_minimum,
            'acceptable_variance': self.acceptable_variance,
            'confidence': self.confidence,
            'cost_average': self.cost_average,
            'cost_ll': self.cost_ll,
            'cost_maximum': self.cost_maximum,
            'cost_mean': self.cost_mean,
            'cost_minimum': self.cost_minimum,
            'cost_ul': self.cost_ul,
            'cost_variance': self.cost_variance,
            'date_end': self.date_end,
            'date_start': self.date_start,
            'description': self.description,
            'measurement_unit': self.measurement_unit,
            'name': self.name,
            'status': self.status,
            'task_type': self.task_type,
            'task_specification': self.task_specification,
            'time_average': self.time_average,
            'time_ll': self.time_ll,
            'time_maximum': self.time_maximum,
            'time_mean': self.time_mean,
            'time_minimum': self.time_minimum,
            'time_ul': self.time_ul,
            'time_variance': self.time_variance
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current value of the RTKValidation data model attributes.

        :param tuple attributes: dicte of values to assign to the instance
                                 attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKValidation {0:d} attributes.". \
               format(self.validation_id)

        try:
            self.acceptable_maximum = float(
                none_to_default(attributes['acceptable_maximum'], 0.0))
            self.acceptable_mean = float(
                none_to_default(attributes['acceptable_mean'], 0.0))
            self.acceptable_minimum = float(
                none_to_default(attributes['acceptable_minimum'], 0.0))
            self.acceptable_variance = float(
                none_to_default(attributes['acceptable_variance'], 0.0))
            self.confidence = float(
                none_to_default(attributes['confidence'], 95.0))
            self.cost_average = float(
                none_to_default(attributes['cost_average'], 0.0))
            self.cost_ll = float(none_to_default(attributes['cost_ll'], 0.0))
            self.cost_maximum = float(
                none_to_default(attributes['cost_maximum'], 0.0))
            self.cost_mean = float(
                none_to_default(attributes['cost_mean'], 0.0))
            self.cost_minimum = float(
                none_to_default(attributes['cost_minimum'], 0.0))
            self.cost_ul = float(none_to_default(attributes['cost_ul'], 0.0))
            self.cost_variance = float(
                none_to_default(attributes['cost_variance'], 0.0))
            self.date_end = none_to_default(
                attributes['date_end'], date.today() + timedelta(days=30))
            self.date_start = none_to_default(attributes['date_start'],
                                              date.today())
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.measurement_unit = str(
                none_to_default(attributes['measurement_unit'], ''))
            self.name = str(none_to_default(attributes['name'], ''))
            self.status = float(none_to_default(attributes['status'], 0.0))
            self.task_type = str(none_to_default(attributes['task_type'], ''))
            self.task_specification = str(
                none_to_default(attributes['task_specification'], ''))
            self.time_average = float(
                none_to_default(attributes['time_average'], 0.0))
            self.time_ll = float(none_to_default(attributes['time_ll'], 0.0))
            self.time_maximum = float(
                none_to_default(attributes['time_maximum'], 0.0))
            self.time_mean = float(
                none_to_default(attributes['time_mean'], 0.0))
            self.time_minimum = float(
                none_to_default(attributes['time_minimum'], 0.0))
            self.time_ul = float(none_to_default(attributes['time_ul'], 0.0))
            self.time_variance = float(
                none_to_default(attributes['time_variance'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKValidation.set_attributes().".format(_err)

        return _error_code, _msg

    def calculate_task_time(self):
        """
        Calculate the mean, standard error, and bounds on the task time.

        These values are calculated assuming a beta distribution (typical
        project management assumption).

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        (self.time_ll, self.time_mean, self.time_ul,
         _sd) = calculate_beta_bounds(self.time_minimum, self.time_average,
                                      self.time_maximum, self.confidence)

        self.time_variance = _sd**2.0

        return _return

    def calculate_task_cost(self):
        """
        Calculate the mean, standard error, and bounds on the task cost.

        These values are calculated assuming a beta distribution (typical
        project management assumption).

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        (self.cost_ll, self.cost_mean, self.cost_ul,
         _sd) = calculate_beta_bounds(self.cost_minimum, self.cost_average,
                                      self.cost_maximum, self.confidence)

        self.cost_variance = _sd**2.0

        return _return
