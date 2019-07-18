# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKEnvironment.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKEnvironment Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKEnvironment(RAMSTK_BASE):
    """
    Class to represent the ramstk_environment table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mission_phase.
    """

    __defaults__ = {
        'name': 'Condition Name',
        'units': 'Units',
        'minimum': 0.0,
        'maximum': 0.0,
        'mean': 0.0,
        'variance': 0.0,
        'ramp_rate': 0.0,
        'low_dwell_time': 0.0,
        'high_dwell_time': 0.0
    }
    __tablename__ = 'ramstk_environment'
    __table_args__ = {'extend_existing': True}

    phase_id = Column(
        'fld_phase_id',
        Integer,
        ForeignKey('ramstk_mission_phase.fld_phase_id'),
        nullable=False,
    )
    # test_id = Column('fld_test_id', Integer,
    #                  ForeignKey('ramstk_test.fld_test_id'),
    #                  nullable=False)
    environment_id = Column(
        'fld_environment_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    name = Column('fld_name', String(256), default=__defaults__['name'])
    units = Column('fld_units', String(128), default=__defaults__['units'])
    minimum = Column('fld_minimum', Float, default=__defaults__['minimum'])
    maximum = Column('fld_maximum', Float, default=__defaults__['maximum'])
    mean = Column('fld_mean', Float, default=__defaults__['mean'])
    variance = Column('fld_variance', Float, default=__defaults__['variance'])
    ramp_rate = Column('fld_ramp_rate',
                       Float,
                       default=__defaults__['ramp_rate'])
    low_dwell_time = Column('fld_low_dwell_time',
                            Float,
                            default=__defaults__['low_dwell_time'])
    high_dwell_time = Column('fld_high_dwell_time',
                             Float,
                             default=__defaults__['high_dwell_time'])

    # Define the relationships to other tables in the RAMSTK Program database.
    phase = relationship('RAMSTKMissionPhase', back_populates='environment')

    is_mission = False
    is_phase = False
    is_env = True

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKEnvironment data model attributes.

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
            'high_dwell_time': self.high_dwell_time,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of RAMSTKEnvironment data model attributes.

        .. note:: you should pop the phase ID and environment ID entries from
        the attributes dict before passing it to this method.

        :param dict attributes: dict of values to assign to the instance
            attributes.
        :return: None
        :rtype: None
        :raise: AttributeError if passed an attribute key that doesn't exist as
            a table field.
        """
        for _key in attributes:
            getattr(self, _key)
            setattr(self, _key,
                    none_to_default(attributes[_key], self.__defaults__[_key]))
