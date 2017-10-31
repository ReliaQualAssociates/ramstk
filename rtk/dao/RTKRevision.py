# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKRevision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKRevision Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import BLOB, Column, Float, Integer, String
from sqlalchemy.orm import relationship               # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


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
            self.availability_logistics = float(
                none_to_default(attributes[0], 1.0))
            self.availability_mission = float(
                none_to_default(attributes[1], 1.0))
            self.cost = float(none_to_default(attributes[2], 0.0))
            self.cost_failure = float(none_to_default(attributes[3], 0.0))
            self.cost_hour = float(none_to_default(attributes[4], 0.0))
            self.hazard_rate_active = float(
                none_to_default(attributes[5], 0.0))
            self.hazard_rate_dormant = float(
                none_to_default(attributes[6], 0.0))
            self.hazard_rate_logistics = float(
                none_to_default(attributes[7], 0.0))
            self.hazard_rate_mission = float(
                none_to_default(attributes[8], 0.0))
            self.hazard_rate_software = float(
                none_to_default(attributes[9], 0.0))
            self.mmt = float(none_to_default(attributes[10], 0.0))
            self.mcmt = float(none_to_default(attributes[11], 0.0))
            self.mpmt = float(none_to_default(attributes[12], 0.0))
            self.mtbf_logistics = float(none_to_default(attributes[13], 0.0))
            self.mtbf_mission = float(none_to_default(attributes[14], 0.0))
            self.mttr = float(none_to_default(attributes[15], 0.0))
            self.name = str(none_to_default(attributes[16], ''))
            self.reliability_logistics = float(
                none_to_default(attributes[17], 1.0))
            self.reliability_mission = float(
                none_to_default(attributes[18], 1.0))
            self.remarks = str(none_to_default(attributes[19], ''))
            self.total_part_count = int(none_to_default(attributes[20], 0))
            self.revision_code = str(none_to_default(attributes[21], ''))
            self.program_time = float(none_to_default(attributes[22], 0.0))
            self.program_time_sd = float(none_to_default(attributes[23], 0.0))
            self.program_cost = float(none_to_default(attributes[24], 0.0))
            self.program_cost_sd = float(none_to_default(attributes[25], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKRevision.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKRevision attributes."

        return _error_code, _msg
