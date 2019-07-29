# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKMission.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMission Table Module."""

# Third Party Imports
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKMission(RAMSTK_BASE):
    """
    Class to represent the ramstk_mission table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a One-to-Many relationship with ramstk_mission_phase.
    """

    __defaults__ = {
        'description': b'',
        'mission_time': 0.0,
        'time_units': 'hours'
    }
    __tablename__ = 'ramstk_mission'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False,
    )
    mission_id = Column(
        'fld_mission_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column('fld_description',
                         BLOB,
                         default=__defaults__['description'])
    mission_time = Column('fld_mission_time',
                          Float,
                          default=__defaults__['mission_time'])
    time_units = Column('fld_time_units',
                        String(256),
                        default=__defaults__['time_units'])

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
            'time_units': self.time_units,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of RAMSTKMission data model attributes.

        .. note:: you should pop the revision ID and mission ID entries from
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
