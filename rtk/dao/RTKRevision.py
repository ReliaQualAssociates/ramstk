#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKRevision.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKRevision Package.
"""

# Import the database models.
from sqlalchemy import BLOB, Column, Float, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities
try:
    from dao.RTKCommonDB import Base
except ImportError:
    from rtk.dao.RTKCommonDB import Base

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKRevision(Base):
    """
    Class to represent the rtk_revision table in the RTK Program database.

    This table shares a One-to-Many relationship with rtk_mission.
    This table shares a One-to-Many relationship with rtk_failure_definition.
    This table shares a One-to-Many relationship with rtk_function.
    This table shares a One-to-Many relationship with rtk_requirement.
    This table shares a One-to-Many relationship with rtk_hardware.
    This table shares a One-to-Many relationship with rtk_software.
    This table shares a One-to-Many relationship with rtk_validation.
    This table shares a One-to-Many relationship with rtk_incident.
    This table shares a One-to-Many relationship with rtk_survival.
    This table shares a One-to-Many relationship with rtk_matrix.
    """

    __tablename__ = 'rtk_revision'

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

    def calculate_reliability(self, mission_time):
        """
        Method to calculate the active hazard rate, dormant hazard rate,
        software hazard rate, inherent hazard rate, mission hazard rate,
        MTBF, mission MTBF, inherent reliability, and mission reliability.

        :param float mission_time: the time to use in the reliability
                                   calculations.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import exp

        _return = False

        # Calculate the logistics h(t).
        self.hazard_rate_logistics = self.hazard_rate_active + \
            self.hazard_rate_dormant + self.hazard_rate_software

        # Calculate the logistics MTBF.
        try:
            self.mtbf_logistics = 1.0 / self.hazard_rate_logistics
        except(ZeroDivisionError, OverflowError):
            self.mtbf_logistics = 0.0
            _msg = "RTK ERROR: Zero Division or Overflow Error when " \
                   "calculating the logistics MTBF in RTKRevision.  " \
                   "Logistics hazard rate: {0:f}.".\
                   format(self.hazard_rate_logistics)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        # Calculate the mission MTBF.
        try:
            self.mtbf_mission = 1.0 / self.hazard_rate_mission
        except(ZeroDivisionError, OverflowError):
            self.mtbf_mission = 0.0
            _msg = "RTK ERROR: Zero Division or Overflow Error when " \
                   "calculating the mission MTBF in RTKRevision.  Mission " \
                   "hazard rate: {0:f}.".format(self.hazard_rate_logistics)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        # Calculate reliabilities.
        self.reliability_logistics = exp(-1.0 * self.hazard_rate_logistics *
                                         mission_time / \
                                         Configuration.RTK_HR_MULTIPLIER)
        self.reliability_mission = exp(-1.0 * self.hazard_rate_mission *
                                       mission_time / \
                                       Configuration.RTK_HR_MULTIPLIER)

        return _return

    def calculate_availability(self):
        """
        Method to calculate the logistics availability and mission
        availability.

        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # Calculate logistics availability.
        try:
            self.availability_logistics = self.mtbf_logistics / \
                                          (self.mtbf_logistics + self.mttr)
        except(ZeroDivisionError, OverflowError):
            self.availability_logistics = 1.0
            _msg = "RTK ERROR: Zero Division or Overflow Error when  " \
                   "calculating the logistics availability in RTKRevision.  " \
                   "Logistics MTBF: {0:f} and MTTR: {1:f}.".\
                   format(self.mtbf_logistics, self.mttr)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        # Calculate mission availability.
        try:
            self.availability_mission = self.mtbf_mission / \
                (self.mtbf_mission + self.mttr)
        except(ZeroDivisionError, OverflowError):
            self.availability_mission = 1.0
            _msg = "RTK ERROR: Zero Division or Overflow Error when " \
                   "calculating the mission availability in RTKRevision.  " \
                   "Mission MTBF: {0:f} and MTTR: {1:f}.".\
                   format(self.mtbf_mission, self.mttr)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

    def calculate_costs(self, mission_time):
        """
        Method to calculate the total cost, cost per failure, and cost per
        operating hour.

        :param float mission_time: the time over which to calculate costs.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _return = False

        # Calculate costs.
        self.cost_per_failure = self.cost * self.hazard_rate_logistics
        try:
            self.cost_per_hour = self.cost / mission_time
        except ZeroDivisionError:
            self.cost_per_hour = 0.0
            _msg = "RTK ERROR: Zero Division Error when calculating the " \
                   "cost per mission hour in RTKRevision.  Mission time: " \
                   "{0:f}.".format(mission_time)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return

