# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKRevision.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKRevision Table Module."""

# pylint: disable=E0401
from sqlalchemy import BLOB, Column, Float, Integer, String
from sqlalchemy.orm import relationship  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


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

    # Define the relationships to other tables in the RTK Program database.
    mission = relationship(
        'RTKMission', back_populates='revision', cascade='delete')
    failures = relationship('RTKFailureDefinition', back_populates='revision')
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
        Retrieve the current values of the RTKRevision data model attributes.

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
        Set the current values of the RTKRevision data model attributes.

        :param dict attributes: dict containing {attr name:attr value} pairs
                                of the values to set.
        :return: (_error_code, _msg)
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKRevision {0:d} attributes.".\
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
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKRevision.set_attributes().".format(_err)

        return _error_code, _msg

    def calculate_hazard_rate(self):
        """
        Calculate hazard rates for the RTKRevision database record model.

        This method calculates the logistics and mission hazard rates.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating hazard rates for Revision ' \
               'ID {0:d}.'.format(self.revision_id)

        # Calculate the logistics h(t).
        self.hazard_rate_logistics = (
            self.hazard_rate_active + self.hazard_rate_dormant +
            self.hazard_rate_software)

        return _error_code, _msg

    def calculate_mtbf(self):
        """
        Calculate MTBFs for the RTKRevision database record model.

        This method calculates the logistics and mission mean time between
        failure (MTBF).

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating MTBFs for Revision ID ' \
               '{0:d}.'.format(self.revision_id)

        # Calculate the logistics MTBF.
        try:
            self.mtbf_logistics = 1.0 / self.hazard_rate_logistics
        except OverflowError:
            self.mtbf_logistics = 0.0
            _error_code = 101
            _msg = 'RTK ERROR: Overflow Error when calculating the ' \
                   'logistics MTBF for Revision ID {0:d}.  Logistics hazard ' \
                   'rate: {1:f}.'.format(self.revision_id,
                                         self.hazard_rate_logistics)
        except ZeroDivisionError:
            self.mtbf_logistics = 0.0
            _error_code = 102
            _msg = 'RTK ERROR: Zero Division Error when calculating the ' \
                   'logistics MTBF for Revision ID {0:d}.  Logistics hazard ' \
                   'rate: {1:f}.'.format(self.revision_id,
                                         self.hazard_rate_logistics)

        # Calculate the mission MTBF.
        try:
            self.mtbf_mission = 1.0 / self.hazard_rate_mission
        except OverflowError:
            self.mtbf_mission = 0.0
            _error_code = 101
            _msg = 'RTK ERROR: Overflow Error when calculating the mission ' \
                   'MTBF for Revision ID {0:d}.  Mission hazard rate: ' \
                   '{1:f}.'.format(self.revision_id, self.hazard_rate_mission)
        except ZeroDivisionError:
            self.mtbf_mission = 0.0
            _error_code = 102
            _msg = 'RTK ERROR: Zero Division Error when calculating the ' \
                   'mission MTBF for Revision ID {0:d}.  Mission hazard ' \
                   'rate: {1:f}.'.format(self.revision_id,
                                         self.hazard_rate_mission)

        return _error_code, _msg

    def calculate_reliability(self, mission_time, multiplier):
        """
        Calculate reliability for the RTKRevision database record model.

        This method calculate the logistics and mission reliability.

        :param float mission_time: the time to use in the reliability
                                   calculations.
        :param float multiplier: the hazard rate multiplier.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        from math import exp

        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating reliabilities for Revision ID ' \
               '{0:d}.'.format(self.revision_id)

        # Calculate reliabilities.
        try:
            self.reliability_logistics = exp(
                -1.0 * self.hazard_rate_logistics * mission_time / multiplier)
        except ZeroDivisionError:
            self.reliability_logistics = 0.0
            _error_code = 102
            _msg = 'RTK ERROR: Zero Division Error when calculating the ' \
                   'logistics reliability for Revision ID {0:d}.  Hazard ' \
                   'rate multiplier: {1:f}.'.format(self.revision_id,
                                                    multiplier)
        try:
            self.reliability_mission = exp(
                -1.0 * self.hazard_rate_mission * mission_time / multiplier)
        except ZeroDivisionError:
            self.reliability_logistics = 0.0
            _error_code = 102
            _msg = 'RTK ERROR: Zero Division Error when calculating the ' \
                   'mission reliability for Revision ID {0:d}.  Hazard ' \
                   'rate multiplier: {1:f}.'.format(self.revision_id,
                                                    multiplier)

        return _error_code, _msg

    def calculate_availability(self):
        """
        Calculate availabilities for the RTKRevision database record model.

        This method calculate the logistics availability and mission
        availability.

        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating availability metrics for Revision ' \
               'ID {0:d}.'.format(self.revision_id)

        try:
            self.availability_logistics = (self.mtbf_logistics /
                                           (self.mtbf_logistics + self.mttr))
        except OverflowError:
            self.reliability_logistics = 0.0
            _error_code = 101
            _msg = 'RTK ERROR: Overflow Error when calculating the ' \
                   'logistics availability for Revision ID {0:d}.  ' \
                   'Logistics MTBF: {1:f} MTTR: {2:f}.'.\
                   format(self.revision_id, self.mtbf_logistics, self.mttr)
        except ZeroDivisionError:
            self.reliability_logistics = 0.0
            _error_code = 102
            _msg = 'RTK ERROR: Zero Division Error when calculating the ' \
                   'logistics availability for Revision ID {0:d}.  ' \
                   'Logistics MTBF: {1:f} MTTR: {2:f}.'.\
                   format(self.revision_id, self.mtbf_logistics, self.mttr)

        try:
            self.availability_mission = (self.mtbf_mission /
                                         (self.mtbf_mission + self.mttr))
        except OverflowError:
            self.reliability_logistics = 0.0
            _error_code = 101
            _msg = 'RTK ERROR: Overflow Error when calculating the ' \
                   'mission availability for Revision ID {0:d}.  ' \
                   'Mission MTBF: {1:f} MTTR: {2:f}.'.format(self.revision_id,
                                                             self.mtbf_mission,
                                                             self.mttr)
        except ZeroDivisionError:
            self.reliability_logistics = 0.0
            _error_code = 102
            _msg = 'RTK ERROR: Zero Division Error when calculating the ' \
                   'mission availability for Revision ID {0:d}.  ' \
                   'Mission MTBF: {1:f} MTTR: {2:f}.'.format(self.revision_id,
                                                             self.mtbf_mission,
                                                             self.mttr)

        return _error_code, _msg

    def calculate_costs(self, mission_time):
        """
        Calculate costs for the RTKRevision database record model.

        This method calculates the total cost, cost per failure, and cost per
        operating hour.

        :param float mission_time: the time over which to calculate costs.
        :return: (_error_code, _msg); the error code and associated message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = 'RTK SUCCESS: Calculating cost metrics for Revision ID ' \
               '{0:d}.'.format(self.revision_id)

        self.cost_failure = (self.cost * self.hazard_rate_logistics)
        try:
            self.cost_hour = self.cost / mission_time
        except OverflowError:
            self.cost_hour = 0.0
            _error_code = 101
            _msg = 'RTK ERROR: Overflow Error when calculating the cost per ' \
                   'mission hour for Revision ID {0:d}.  Mission ' \
                   'time: {1:f}.'.format(self.revision_id, mission_time)
        except ZeroDivisionError:
            self.cost_hour = 0.0
            _error_code = 102
            _msg = 'RTK ERROR: Zero Division Error when calculating the ' \
                   'cost per mission hour for Revision ID {0:d}.  Mission ' \
                   'time: {1:f}.'.format(self.revision_id, mission_time)

        return _error_code, _msg
