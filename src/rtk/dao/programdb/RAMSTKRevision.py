# -*- coding: utf-8 -*-
#
#       rtk.dao.RAMSTKRevision.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RAMSTKRevision Table Module."""

from sqlalchemy import BLOB, Column, Float, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from rtk.Utilities import none_to_default
from rtk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKRevision(RAMSTK_BASE):
    """
    Class to represent the rtk_revision table in the RAMSTK Program database.

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
        * One-to-Many relationship with rtk_hazard_analysis.
        * One-to-Many relationship with rtk_program_status.
    """

    __tablename__ = 'rtk_revision'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)
    availability_logistics = Column(
        'fld_availability_logistics', Float, nullable=False, default=1.0)
    availability_mission = Column(
        'fld_availability_mission', Float, nullable=False, default=1.0)
    cost = Column('fld_cost', Float, nullable=False, default=0.0)
    cost_failure = Column(
        'fld_cost_failure', Float, nullable=False, default=0.0)
    cost_hour = Column('fld_cost_hour', Float, nullable=False, default=0.0)
    hazard_rate_active = Column(
        'fld_hazard_rate_active', Float, nullable=False, default=0.0)
    hazard_rate_dormant = Column(
        'fld_hazard_rate_dormant', Float, nullable=False, default=0.0)
    hazard_rate_logistics = Column(
        'fld_hazard_rate_logistics', Float, nullable=False, default=0.0)
    hazard_rate_mission = Column(
        'fld_hazard_rate_mission', Float, nullable=False, default=0.0)
    hazard_rate_software = Column(
        'fld_hazard_rate_software', Float, nullable=False, default=0.0)
    mmt = Column('fld_mmt', Float, nullable=False, default=0.0)
    mcmt = Column('fld_mcmt', Float, nullable=False, default=0.0)
    mpmt = Column('fld_mpmt', Float, nullable=False, default=0.0)
    mtbf_logistics = Column(
        'fld_mtbf_logistics', Float, nullable=False, default=0.0)
    mtbf_mission = Column(
        'fld_mtbf_mission', Float, nullable=False, default=0.0)
    mttr = Column('fld_mttr', Float, nullable=False, default=0.0)
    name = Column('fld_name', String(128), nullable=False, default='')
    reliability_logistics = Column(
        'fld_reliability_logistics', Float, nullable=False, default=1.0)
    reliability_mission = Column(
        'fld_reliability_mission', Float, nullable=False, default=1.0)
    remarks = Column('fld_remarks', BLOB, nullable=False, default='')
    total_part_count = Column(
        'fld_total_part_count', Integer, nullable=False, default=1)
    revision_code = Column(
        'fld_revision_code', String(8), nullable=False, default='')
    program_time = Column(
        'fld_program_time', Float, nullable=False, default=0.0)
    program_time_sd = Column(
        'fld_program_time_sd', Float, nullable=False, default=0.0)
    program_cost = Column(
        'fld_program_cost', Float, nullable=False, default=0.0)
    program_cost_sd = Column(
        'fld_program_cost_sd', Float, nullable=False, default=0.0)

    # Define the relationships to other tables in the RAMSTK Program database.
    mission = relationship(
        'RAMSTKMission', back_populates='revision', cascade='delete')
    failures = relationship('RAMSTKFailureDefinition', back_populates='revision')
    function = relationship('RAMSTKFunction', back_populates='revision')
    requirement = relationship('RAMSTKRequirement', back_populates='revision')
    stakeholder = relationship('RAMSTKStakeholder', back_populates='revision')
    hardware = relationship('RAMSTKHardware', back_populates='revision')
    software = relationship('RAMSTKSoftware', back_populates='revision')
    validation = relationship('RAMSTKValidation', back_populates='revision')
    incident = relationship('RAMSTKIncident', back_populates='revision')
    test = relationship('RAMSTKTest', back_populates='revision')
    survival = relationship('RAMSTKSurvival', back_populates='revision')
    matrix = relationship('RAMSTKMatrix', back_populates='revision')
    hazard = relationship('RAMSTKHazardAnalysis', back_populates='revision')
    program_status = relationship(
        'RAMSTKProgramStatus', back_populates='revision')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKRevision data model attributes.

        :return: {revision_id, availability, mission_availability, cost,
                  cost_per_failure, cost_per_hour, active_hazard_rate,
                  dormant_hazard_rate, mission_hazard_rate, hazard_rate,
                  software_hazard_rate, mmt, mcmt, mpmt, mission_mtbf, mtbf,
                  mttr, name, mission_reliability, reliability, remarks,
                  n_parts, code, program_time, program_time_se, program_cost,
                  program_cost_se} pairs.
        :rtype: dict
        """
        _attributes = {
            'revision_id': self.revision_id,
            'availability_logistics': self.availability_logistics,
            'availability_mission': self.availability_mission,
            'cost': self.cost,
            'cost_per_failure': self.cost_failure,
            'cost_per_hour': self.cost_hour,
            'hazard_rate_active': self.hazard_rate_active,
            'hazard_rate_dormant': self.hazard_rate_dormant,
            'hazard_rate_logistics': self.hazard_rate_logistics,
            'hazard_rate_mission': self.hazard_rate_mission,
            'hazard_rate_software': self.hazard_rate_software,
            'mmt': self.mmt,
            'mcmt': self.mcmt,
            'mpmt': self.mpmt,
            'mtbf_logistics': self.mtbf_logistics,
            'mtbf_mission': self.mtbf_mission,
            'mttr': self.mttr,
            'name': self.name,
            'reliability_logistics': self.reliability_logistics,
            'reliability_mission': self.reliability_mission,
            'remarks': self.remarks,
            'n_parts': self.total_part_count,
            'revision_code': self.revision_code,
            'program_time': self.program_time,
            'program_time_sd': self.program_time_sd,
            'program_cost': self.program_cost,
            'program_cost_sd': self.program_cost_sd
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKRevision data model attributes.

        :param dict attributes: dict containing {attr name:attr value} pairs
                                of the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKRevision {0:d} attributes.".\
            format(self.revision_id)

        try:
            self.availability_logistics = float(
                none_to_default(attributes['availability_logistics'], 1.0))
            self.availability_mission = float(
                none_to_default(attributes['availability_mission'], 1.0))
            self.cost = float(none_to_default(attributes['cost'], 0.0))
            self.cost_failure = float(
                none_to_default(attributes['cost_per_failure'], 0.0))
            self.cost_hour = float(
                none_to_default(attributes['cost_per_hour'], 0.0))
            self.hazard_rate_active = float(
                none_to_default(attributes['hazard_rate_active'], 0.0))
            self.hazard_rate_dormant = float(
                none_to_default(attributes['hazard_rate_dormant'], 0.0))
            self.hazard_rate_logistics = float(
                none_to_default(attributes['hazard_rate_logistics'], 0.0))
            self.hazard_rate_mission = float(
                none_to_default(attributes['hazard_rate_mission'], 0.0))
            self.hazard_rate_software = float(
                none_to_default(attributes['hazard_rate_software'], 0.0))
            self.mmt = float(none_to_default(attributes['mmt'], 0.0))
            self.mcmt = float(none_to_default(attributes['mcmt'], 0.0))
            self.mpmt = float(none_to_default(attributes['mpmt'], 0.0))
            self.mtbf_logistics = float(
                none_to_default(attributes['mtbf_logistics'], 0.0))
            self.mtbf_mission = float(
                none_to_default(attributes['mtbf_mission'], 0.0))
            self.mttr = float(none_to_default(attributes['mttr'], 0.0))
            self.name = str(none_to_default(attributes['name'], ''))
            self.reliability_logistics = float(
                none_to_default(attributes['reliability_logistics'], 1.0))
            self.reliability_mission = float(
                none_to_default(attributes['reliability_mission'], 1.0))
            self.remarks = str(none_to_default(attributes['remarks'], ''))
            self.total_part_count = int(
                none_to_default(attributes['n_parts'], 0))
            self.revision_code = str(
                none_to_default(attributes['revision_code'], ''))
            self.program_time = float(
                none_to_default(attributes['program_time'], 0.0))
            self.program_time_sd = float(
                none_to_default(attributes['program_time_sd'], 0.0))
            self.program_cost = float(
                none_to_default(attributes['program_cost'], 0.0))
            self.program_cost_sd = float(
                none_to_default(attributes['program_cost_sd'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKRevision.set_attributes().".format(_err)

        return _error_code, _msg
