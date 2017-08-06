#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMissionPhase.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
===============================================================================
The RTKMissionPhase Table
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
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKMissionPhase(RTK_BASE):
    """
    Class to represent the rtk_mission_phase table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_mission.
    This table shares a One-to-Many relationship with rtk_environment.
    """

    __tablename__ = 'rtk_mission_phase'
    __table_args__ = {'extend_existing': True}

    mission_id = Column('fld_mission_id', Integer,
                        ForeignKey('rtk_mission.fld_mission_id'),
                        nullable=False)
    phase_id = Column('fld_phase_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)

    description = Column('fld_description', BLOB, default='')
    name = Column('fld_name', String(256), default='')
    phase_start = Column('fld_phase_start', Float, default=0.0)
    phase_end = Column('fld_phase_end', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    mission = relationship('RTKMission', back_populates='phase')
    environment = relationship('RTKEnvironment', back_populates='phase',
                               cascade='delete')

    def get_attributes(self):
        """
        Method to retrieve the current values of the Phase data model
        attributes.

        :return: value of instance attributes
        :rtype: tuple
        """

        _values = (self.mission_id, self.phase_id, self.description, self.name,
                   self.phase_start, self.phase_end)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the current values of the RTKMissionPhase data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return:
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMissionPhase {0:d} attributes.". \
            format(self.phase_id)

        try:
            self.description = str(attributes[0])
            self.name = str(attributes[1])
            self.phase_start = float(attributes[2])
            self.phase_end = float(attributes[3])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMissionPhase.set_attributes()."
        except TypeError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMissionPhase attributes."

        return _error_code, _msg
