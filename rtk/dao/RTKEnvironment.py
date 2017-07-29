#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKEnvironment.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKEnvironment Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer, String
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
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKEnvironment(RTK_BASE):
    """
    Class to represent the rtk_environment table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_mission_phase.
    """

    __tablename__ = 'rtk_environment'
    __table_args__ = {'extend_existing': True}

    phase_id = Column('fld_phase_id', Integer,
                      ForeignKey('rtk_mission_phase.fld_phase_id'),
                      nullable=False)
    # test_id = Column('fld_test_id', Integer,
    #                  ForeignKey('rtk_test.fld_test_id'),
    #                  nullable=False)
    environment_id = Column('fld_environment_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)

    name = Column('fld_name', String(256), default='Condition Name')
    units = Column('fld_units', String(128), default='Units')
    minimum = Column('fld_minimum', Float, default=0.0)
    maximum = Column('fld_maximum', Float, default=0.0)
    mean = Column('fld_mean', Float, default=0.0)
    variance = Column('fld_variance', Float, default=0.0)
    ramp_rate = Column('fld_ramp_rate', Float, default=0.0)
    low_dwell_time = Column('fld_low_dwell_time', Float, default=0.0)
    high_dwell_time = Column('fld_high_dwell_time', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    phase = relationship('RTKMissionPhase', back_populates='environment')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKEnvironment data model
        attributes.

        :return: (phase_id, environment_id, name, units, minimum,
                  maximum, mean, variance, ramp_rate, low_dwell_time,
                  high_dwell_time)
        :rtype: tuple
        """

        _attributes = (self.phase_id, self.environment_id, self.name,
                       self.units, self.minimum, self.maximum, self.mean,
                       self.variance, self.ramp_rate, self.low_dwell_time,
                       self.high_dwell_time)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKEnvironment data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return:
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKEnvironment {0:d} attributes.". \
            format(self.environment_id)

        try:
            self.name = str(attributes[0])
            self.units = str(attributes[1])
            self.minimum = float(attributes[2])
            self.maximum = float(attributes[3])
            self.mean = float(attributes[4])
            self.variance = float(attributes[5])
            self.ramp_rate = float(attributes[6])
            self.low_dwell_time = float(attributes[7])
            self.high_dwell_time = float(attributes[8])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKEnvironment.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKEnvironment attributes."

        return _error_code, _msg

