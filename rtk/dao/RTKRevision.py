#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKRevision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
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
The RTKRevision Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import BLOB, Column, Float, Integer, String
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


class RTKRevision(RTK_BASE):
    """
    Class to represent the rtk_revision table in the RTK Program database.

    This table shares a:
        * One-to-Many relationship with rtk_mission.
        * One-to-Many relationship with rtk_failure_definition.
        * One-to-Many relationship with rtk_function.
        * One-to-Many relationship with rtk_requirement.
        * One-to-Many relationship with rtk_hardware.
        * One-to-Many relationship with rtk_software.
        * One-to-Many relationship with rtk_validation.
        * One-to-Many relationship with rtk_incident.
        * One-to-Many relationship with rtk_survival.
        * One-to-Many relationship with rtk_matrix.
    """

    __tablename__ = 'rtk_revision'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    availability_logistics = Column('fld_availability_logistics', Float,
                                    nullable=False, default=1.0)
    availability_mission = Column('fld_availability_mission', Float,
                                  nullable=False, default=1.0)
    cost = Column('fld_cost', Float, nullable=False, default=0.0)
    cost_failure = Column('fld_cost_failure', Float, nullable=False,
                          default=0.0)
    cost_hour = Column('fld_cost_hour', Float, nullable=False, default=0.0)
    hazard_rate_active = Column('fld_hazard_rate_active', Float,
                                nullable=False, default=0.0)
    hazard_rate_dormant = Column('fld_hazard_rate_dormant', Float,
                                 nullable=False, default=0.0)
    hazard_rate_logistics = Column('fld_hazard_rate_logistics', Float,
                                   nullable=False, default=0.0)
    hazard_rate_mission = Column('fld_hazard_rate_mission', Float,
                                 nullable=False, default=0.0)
    hazard_rate_software = Column('fld_hazard_rate_software', Float,
                                  nullable=False, default=0.0)
    mmt = Column('fld_mmt', Float, nullable=False, default=0.0)
    mcmt = Column('fld_mcmt', Float, nullable=False, default=0.0)
    mpmt = Column('fld_mpmt', Float, nullable=False, default=0.0)
    mtbf_logistics = Column('fld_mtbf_logistics', Float, nullable=False,
                            default=0.0)
    mtbf_mission = Column('fld_mtbf_mission', Float, nullable=False,
                          default=0.0)
    mttr = Column('fld_mttr', Float, nullable=False, default=0.0)
    name = Column('fld_name', String(128), nullable=False, default='')
    reliability_logistics = Column('fld_reliability_logistics', Float,
                                   nullable=False, default=1.0)
    reliability_mission = Column('fld_reliability_mission', Float,
                                 nullable=False, default=1.0)
    remarks = Column('fld_remarks', BLOB, nullable=False, default='')
    total_part_count = Column('fld_total_part_count', Integer, nullable=False,
                              default=1)
    revision_code = Column('fld_revision_code', String(8), nullable=False,
                           default='')
    program_time = Column('fld_program_time', Float, nullable=False,
                          default=0.0)
    program_time_sd = Column('fld_program_time_sd', Float, nullable=False,
                             default=0.0)
    program_cost = Column('fld_program_cost', Float, nullable=False,
                          default=0.0)
    program_cost_sd = Column('fld_program_cost_sd', Float, nullable=False,
                             default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    mission = relationship('RTKMission', back_populates='revision',
                           cascade='delete')
    failures = relationship('RTKFailureDefinition',
                            back_populates='revision')
    function = relationship('RTKFunction', back_populates='revision')
    requirement = relationship('RTKRequirement', back_populates='revision')
    stakeholder = relationship('RTKStakeholder', back_populates='revision')
    hardware = relationship('RTKHardware', back_populates='revision')
    software = relationship('RTKSoftware', back_populates='revision')
    validation = relationship('RTKValidation', back_populates='revision')
    incident = relationship('RTKIncident', back_populates='revision')
    test = relationship('RTKTest', back_populates='revision')
    survival = relationship('RTKSurvival', back_populates='revision')
    matrix = relationship('RTKMatrix', back_populates='revision')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKRevision data model
        attributes.

        :return: (revision_id, availability, mission_availability, cost,
                  cost_per_failure, cost_per_hour, active_hazard_rate,
                  dormant_hazard_rate, mission_hazard_rate, hazard_rate,
                  software_hazard_rate, mmt, mcmt, mpmt, mission_mtbf, mtbf,
                  mttr, name, mission_reliability, reliability, remarks,
                  n_parts, code, program_time, program_time_se, program_cost,
                  program_cost_se)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.availability_logistics,
                       self.availability_mission, self.cost, self.cost_failure,
                       self.cost_hour, self.hazard_rate_active,
                       self.hazard_rate_dormant, self.hazard_rate_logistics,
                       self.hazard_rate_mission, self.hazard_rate_software,
                       self.mmt, self.mcmt, self.mpmt, self.mtbf_logistics,
                       self.mtbf_mission, self.mttr, self.name,
                       self.reliability_logistics, self.reliability_mission,
                       self.remarks, self.total_part_count, self.revision_code,
                       self.program_time, self.program_time_sd,
                       self.program_cost, self.program_cost_sd)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the current values of the Failure Definition data model
        attributes.

        :param tuple attributes: tuple containing the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKRevision {0:d} attributes.".\
            format(self.revision_id)

        try:
            self.availability_logistics = float(attributes[0])
            self.availability_mission = float(attributes[1])
            self.cost = float(attributes[2])
            self.cost_failure = float(attributes[3])
            self.cost_hour = float(attributes[4])
            self.hazard_rate_active = float(attributes[5])
            self.hazard_rate_dormant = float(attributes[6])
            self.hazard_rate_logistics = float(attributes[7])
            self.hazard_rate_mission = float(attributes[8])
            self.hazard_rate_software = float(attributes[9])
            self.mmt = float(attributes[10])
            self.mcmt = float(attributes[11])
            self.mpmt = float(attributes[12])
            self.mtbf_logistics = float(attributes[13])
            self.mtbf_mission = float(attributes[14])
            self.mttr = float(attributes[15])
            self.name = str(attributes[16])
            self.reliability_logistics = float(attributes[17])
            self.reliability_mission = float(attributes[18])
            self.remarks = str(attributes[19])
            self.total_part_count = int(attributes[20])
            self.revision_code = str(attributes[21])
            self.program_time = float(attributes[22])
            self.program_time_sd = float(attributes[23])
            self.program_cost = float(attributes[24])
            self.program_cost_sd = float(attributes[25])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKRevision.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKRevision attributes."

        return _error_code, _msg
