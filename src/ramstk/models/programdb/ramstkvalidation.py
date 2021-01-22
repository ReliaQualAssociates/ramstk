# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKValidation.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKValidation Table."""

# Standard Library Imports
from datetime import date, timedelta

# Third Party Imports
# noinspection PyPackageRequirements
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.analyses.statistics import do_calculate_beta_bounds
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKValidation(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent table ramstk_validation in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    """

    __defaults__ = {
        'acceptable_maximum': 0.0,
        'acceptable_mean': 0.0,
        'acceptable_minimum': 0.0,
        'acceptable_variance': 0.0,
        'confidence': 95.0,
        'cost_average': 0.0,
        'cost_ll': 0.0,
        'cost_maximum': 0.0,
        'cost_mean': 0.0,
        'cost_minimum': 0.0,
        'cost_ul': 0.0,
        'cost_variance': 0.0,
        'date_end': date.today() + timedelta(days=30),
        'date_start': date.today(),
        'description': '',
        'measurement_unit': '',
        'name': '',
        'status': 0.0,
        'task_type': '',
        'task_specification': '',
        'time_average': 0.0,
        'time_ll': 0.0,
        'time_maximum': 0.0,
        'time_mean': 0.0,
        'time_minimum': 0.0,
        'time_ul': 0.0,
        'time_variance': 0.0
    }
    __tablename__ = 'ramstk_validation'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    validation_id = Column(
        'fld_validation_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    acceptable_maximum = Column('fld_acceptable_maximum',
                                Float,
                                default=__defaults__['acceptable_maximum'])
    acceptable_mean = Column('fld_acceptable_mean',
                             Float,
                             default=__defaults__['acceptable_mean'])
    acceptable_minimum = Column('fld_acceptable_minimum',
                                Float,
                                default=__defaults__['acceptable_minimum'])
    acceptable_variance = Column('fld_acceptable_variance',
                                 Float,
                                 default=__defaults__['acceptable_variance'])
    confidence = Column('fld_confidence',
                        Float,
                        default=__defaults__['confidence'])
    cost_average = Column('fld_cost_average',
                          Float,
                          default=__defaults__['cost_average'])
    cost_ll = Column('fld_cost_ll', Float, default=__defaults__['cost_ll'])
    cost_maximum = Column('fld_cost_maximum',
                          Float,
                          default=__defaults__['cost_maximum'])
    cost_mean = Column('fld_cost_mean',
                       Float,
                       default=__defaults__['cost_mean'])
    cost_minimum = Column('fld_cost_minimum',
                          Float,
                          default=__defaults__['cost_minimum'])
    cost_ul = Column('fld_cost_ul', Float, default=__defaults__['cost_ul'])
    cost_variance = Column('fld_cost_variance',
                           Float,
                           default=__defaults__['cost_variance'])
    date_end = Column('fld_date_end', Date, default=__defaults__['date_end'])
    date_start = Column('fld_date_start',
                        Date,
                        default=__defaults__['date_start'])
    description = Column('fld_description',
                         String,
                         default=__defaults__['description'])
    measurement_unit = Column('fld_measurement_unit',
                              String(256),
                              default=__defaults__['measurement_unit'])
    name = Column('fld_name', String(256), default=__defaults__['name'])
    status = Column('fld_status', Float, default=__defaults__['status'])
    task_specification = Column('fld_task_specification',
                                String(512),
                                default=__defaults__['task_specification'])
    task_type = Column('fld_type',
                       String(256),
                       default=__defaults__['task_type'])
    time_average = Column('fld_time_average',
                          Float,
                          default=__defaults__['time_average'])
    time_ll = Column('fld_time_ll', Float, default=__defaults__['time_ll'])
    time_maximum = Column('fld_time_maximum',
                          Float,
                          default=__defaults__['time_maximum'])
    time_mean = Column('fld_time_mean',
                       Float,
                       default=__defaults__['time_mean'])
    time_minimum = Column('fld_time_minimum',
                          Float,
                          default=__defaults__['time_minimum'])
    time_ul = Column('fld_time_ul', Float, default=__defaults__['time_ul'])
    time_variance = Column('fld_time_variance',
                           Float,
                           default=__defaults__['time_variance'])

    # Define the relationships to other tables in the RAMSTK Program database.
    revision: relationship = relationship(
        'RAMSTKRevision',
        back_populates='validation',
    )

    def get_attributes(self):
        """Retrieve current values of RAMSTKValidation data model attributes.

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
            'task_specification': self.task_specification,
            'task_type': self.task_type,
            'time_average': self.time_average,
            'time_ll': self.time_ll,
            'time_maximum': self.time_maximum,
            'time_mean': self.time_mean,
            'time_minimum': self.time_minimum,
            'time_ul': self.time_ul,
            'time_variance': self.time_variance
        }

        return _attributes

    def calculate_task_time(self):
        """Calculate the mean, standard error, and bounds on the task time.

        These values are calculated assuming a beta distribution (typical
        project management assumption).

        :return: None
        :rtype: None
        """
        (self.time_ll, self.time_mean, self.time_ul,
         _sd) = do_calculate_beta_bounds(self.time_minimum, self.time_average,
                                         self.time_maximum, self.confidence)

        self.time_variance = _sd**2.0

    def calculate_task_cost(self):
        """Calculate the mean, standard error, and bounds on the task cost.

        These values are calculated assuming a beta distribution (typical
        project management assumption).

        :return: None
        :rtype: None
        """
        (self.cost_ll, self.cost_mean, self.cost_ul,
         _sd) = do_calculate_beta_bounds(self.cost_minimum, self.cost_average,
                                         self.cost_maximum, self.confidence)

        self.cost_variance = _sd**2.0
