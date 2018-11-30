# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKMission.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMission Table Module."""

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKMission(RAMSTK_BASE):
    """
    Class to represent the ramstk_mission table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a One-to-Many relationship with ramstk_mission_phase.
    """

    __tablename__ = 'ramstk_mission'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    mission_id = Column(
        'fld_mission_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    description = Column('fld_description', BLOB, default='Description')
    mission_time = Column('fld_mission_time', Float, default=0.0)
    time_units = Column('fld_time_units', String(256), default='hours')

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='mission')
    phase = relationship('RAMSTKMissionPhase', back_populates='mission')

    is_mission = True
    is_phase = False
    is_env = False

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKMission data model attributes.

        :return: (revision_id, mission_id, description, mission_time,
                  time_units)
        :rtype: tuple
        """
        _attributes = {
            'revision_id': self.revision_id,
            'mission_id': self.mission_id,
            'description': self.description,
            'mission_time': self.mission_time,
            'time_units': self.time_units
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKMission data model attributes.

        :param tuple attributes: tuple containing the values to set.
        :return:
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKMission {0:d} attributes.". \
            format(self.mission_id)

        try:
            self.description = str(
                none_to_default(attributes['description'], 'Description'))
            self.mission_time = float(
                none_to_default(attributes['mission_time'], 0.0))
            self.time_units = str(
                none_to_default(attributes['time_units'], 'hours'))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKMission.set_attributes().".format(str(_err))

        return _error_code, _msg
