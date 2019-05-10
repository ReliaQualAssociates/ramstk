# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKMissionPhase.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMissionPhase Table Module."""

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKMissionPhase(RAMSTK_BASE):
    """
    Class to represent the ramstk_mission_phase table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mission.
    This table shares a One-to-Many relationship with ramstk_environment.
    """

    __tablename__ = 'ramstk_mission_phase'
    __table_args__ = {'extend_existing': True}

    mission_id = Column(
        'fld_mission_id',
        Integer,
        ForeignKey('ramstk_mission.fld_mission_id'),
        nullable=False)
    phase_id = Column(
        'fld_phase_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    description = Column('fld_description', BLOB, default=b'')
    name = Column('fld_name', String(256), default='')
    phase_start = Column('fld_phase_start', Float, default=0.0)
    phase_end = Column('fld_phase_end', Float, default=0.0)

    # Define the relationships to other tables in the RAMSTK Program database.
    mission = relationship('RAMSTKMission', back_populates='phase')
    environment = relationship(
        'RAMSTKEnvironment', back_populates='phase', cascade='delete')

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
        Set the current values of the RAMSTKMissionPhase data model attributes.

        :param tuple attributes: tuple containing the values to set.
        :return:
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKMissionPhase {0:d} attributes.". \
            format(self.phase_id)

        try:
            self.description = none_to_default(attributes['description'], b'')
            self.name = str(none_to_default(attributes['name'], ''))
            self.phase_start = float(
                none_to_default(attributes['phase_start'], 0.0))
            self.phase_end = float(
                none_to_default(attributes['phase_end'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKMissionPhase.set_attributes().".format(str(_err))

        return _error_code, _msg
