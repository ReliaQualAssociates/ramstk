#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMission.py is part of The RTK Project
#
# All rights reserved.

"""
===============================================================================
The RTKMission Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
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
__copyright__ = 'Copyright 2017 Andrew "weibullguy" Rowland'


class RTKMission(RTK_BASE):
    """
    Class to represent the rtk_mission table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relationship with rtk_mission_phase.
    """

    __tablename__ = 'rtk_mission'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    mission_id = Column('fld_mission_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    description = Column('fld_description', BLOB, default='Description')
    mission_time = Column('fld_mission_time', Float, default=0.0)
    time_units = Column('fld_time_units', String(256), default='hours')

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='mission')
    phase = relationship('RTKMissionPhase', back_populates='mission')

    is_mission = True
    is_phase = False
    is_env = False

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKMission data model
        attributes.

        :return: (revision_id, mission_id, description, mission_time,
                  time_units)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.mission_id, self.description,
                       self.mission_time, self.time_units)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKMission data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return:
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMission {0:d} attributes.". \
            format(self.mission_id)

        try:
            self.description = str(attributes[0])
            self.mission_time = float(attributes[1])
            self.time_units = str(attributes[2])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMission.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMission attributes."

        return _error_code, _msg
