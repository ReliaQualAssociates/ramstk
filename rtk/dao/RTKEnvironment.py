# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKEnvironment.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKEnvironment Table
===============================================================================
"""

from sqlalchemy import Column, Float, ForeignKey, \
                       Integer, String              # pylint: disable=E0401
from sqlalchemy.orm import relationship             # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, \
                      none_to_default               # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                # pylint: disable=E0401


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

    is_mission = False
    is_phase = False
    is_env = True

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
            self.name = str(none_to_default(attributes[0], 'Condition Name'))
            self.units = str(none_to_default(attributes[1], 'Units'))
            self.minimum = float(none_to_default(attributes[2], 0.0))
            self.maximum = float(none_to_default(attributes[3], 0.0))
            self.mean = float(none_to_default(attributes[4], 0.0))
            self.variance = float(none_to_default(attributes[5], 0.0))
            self.ramp_rate = float(none_to_default(attributes[6], 0.0))
            self.low_dwell_time = float(none_to_default(attributes[7], 0.0))
            self.high_dwell_time = float(none_to_default(attributes[8], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKEnvironment.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKEnvironment attributes."

        return _error_code, _msg
