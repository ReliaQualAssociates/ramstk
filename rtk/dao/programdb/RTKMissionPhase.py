# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMissionPhase.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKMissionPhase Table Module."""

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RTKCommonDB import RTK_BASE


class RTKMissionPhase(RTK_BASE):
    """
    Class to represent the rtk_mission_phase table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_mission.
    This table shares a One-to-Many relationship with rtk_environment.
    """

    __tablename__ = 'rtk_mission_phase'
    __table_args__ = {'extend_existing': True}

    mission_id = Column(
        'fld_mission_id',
        Integer,
        ForeignKey('rtk_mission.fld_mission_id'),
        nullable=False)
    phase_id = Column(
        'fld_phase_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', BLOB, default='')
    name = Column('fld_name', String(256), default='')
    phase_start = Column('fld_phase_start', Float, default=0.0)
    phase_end = Column('fld_phase_end', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    mission = relationship('RTKMission', back_populates='phase')
    environment = relationship(
        'RTKEnvironment', back_populates='phase', cascade='delete')

    is_mission = False
    is_phase = True
    is_env = False

    def get_attributes(self):
        """
        Retrieve the current values of the Mission Phase data model attributes.

        :return: value of instance attributes
        :rtype: tuple
        """
        _values = {
            'mission_id': self.mission_id,
            'phase_id': self.phase_id,
            'description': self.description,
            'name': self.name,
            'phase_start': self.phase_start,
            'phase_end': self.phase_end
        }

        return _values

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKMissionPhase data model attributes.

        :param tuple attributes: tuple containing the values to set.
        :return:
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMissionPhase {0:d} attributes.". \
            format(self.phase_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], ''))
            self.name = str(none_to_default(attributes['name'], ''))
            self.phase_start = float(
                none_to_default(attributes['phase_start'], 0.0))
            self.phase_end = float(
                none_to_default(attributes['phase_end'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKMissionPhase.set_attributes().".format(_err)

        return _error_code, _msg
