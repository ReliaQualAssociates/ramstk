# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKEnvironment.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKEnvironment Table Module."""

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKEnvironment(RTK_BASE):
    """
    Class to represent the rtk_environment table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_mission_phase.
    """

    __tablename__ = 'rtk_environment'
    __table_args__ = {'extend_existing': True}

    phase_id = Column(
        'fld_phase_id',
        Integer,
        ForeignKey('rtk_mission_phase.fld_phase_id'),
        nullable=False)
    # test_id = Column('fld_test_id', Integer,
    #                  ForeignKey('rtk_test.fld_test_id'),
    #                  nullable=False)
    environment_id = Column(
        'fld_environment_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

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
        Retrieve current values of the RTKEnvironment data model attributes.

        :return: {phase_id, environment_id, name, units, minimum,
                  maximum, mean, variance, ramp_rate, low_dwell_time,
                  high_dwell_time} pairs.
        :rtype: dict
        """
        _attributes = {
            'phase_id': self.phase_id,
            'environment_id': self.environment_id,
            'name': self.name,
            'units': self.units,
            'minimum': self.minimum,
            'maximum': self.maximum,
            'mean': self.mean,
            'variance': self.variance,
            'ramp_rate': self.ramp_rate,
            'low_dwell_time': self.low_dwell_time,
            'high_dwell_time': self.high_dwell_time
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKEnvironment data model attributes.

        :param dict attributes: dict containing {attr name:attr value} pairs
                                of the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKEnvironment {0:d} attributes.". \
            format(self.environment_id)

        try:
            self.name = str(
                none_to_default(attributes['name'], 'Condition Name'))
            self.units = str(none_to_default(attributes['units'], 'Units'))
            self.minimum = float(none_to_default(attributes['minimum'], 0.0))
            self.maximum = float(none_to_default(attributes['maximum'], 0.0))
            self.mean = float(none_to_default(attributes['mean'], 0.0))
            self.variance = float(none_to_default(attributes['variance'], 0.0))
            self.ramp_rate = float(
                none_to_default(attributes['ramp_rate'], 0.0))
            self.low_dwell_time = float(
                none_to_default(attributes['low_dwell_time'], 0.0))
            self.high_dwell_time = float(
                none_to_default(attributes['high_dwell_time'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKEnvironment.set_attributes().".format(_err)

        return _error_code, _msg
