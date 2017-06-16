#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.DAO.py is part of The RTK Project
#
# All rights reserved.

"""
The Data Acces Object (DAO) Package.
"""

from datetime import date, timedelta

# Import the database models.
from SQLite3 import Model as SQLite3

from sqlalchemy import create_engine, BLOB, Column, Date, Float, ForeignKey, \
    Integer, MetaData, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.engine.url import URL

# Import other RTK modules.
try:
    import Configuration
except ImportError:
    import rtk.Configuration

Base = declarative_base()

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class DAO(object):
    """
    This is the data access controller class.

    :ivar model: an instance of the database class selected for data access.
    """

    # Define public class scalar attributes.
    engine = None
    metadata = None
    session = scoped_session(sessionmaker())

    def __init__(self, database, db_type=0):
        """
        Method to initialize an instance of the DAO controller.

        :param str database: the full path of the database to connect to.
        :keyword int db_type: the type of database to connect to.  Options are:
                              * SQLite3 = 0 (default)
                              * MySQL/MariaDB = 1
        """

        if db_type == 0:
            self.model = SQLite3()
        elif db_type == 1:
            pass

        self.model.connect(database)

    def execute(self, query, commit=False):
        """
        Method to execute the passed query.

        :param str query: the SQL query to execute.
        :param bool commit: indicates whether or not to commit query.
        :return: (_results, _error_code); the results of the query and the
                                          error code produced.
        :rtype: tuple
        """

        (_results, _error_code, _last_id) = self.model.execute(query, commit)

        return _results, _error_code, _last_id

    def get_last_id(self, table):
        """
        Retrieves the next value to be used in the autoincrement field for the
        passed table.

        :param str table: the name of the table to get the next value.
        :return: _next_id
        :rtype: int
        """

        _last_id = self.model.get_last_id(table)

        return _last_id

    def close(self):
        """
        Method to close the database connection.
        """

        self.model.connection.close()


    def db_connect(self, database):
        """
        Method to perform database connection using database settings from
        the configuration file.

        :param str database: the absolute path to the database to connect to.
        :return: False if successful, True if an error occurs.
        :rtype: bool
        """

        self.engine = create_engine(database, echo=False)

        self.session.remove()
        self.session.configure(bind=self.engine, autoflush=False,
                               expire_on_commit=False)
        self.metadata = MetaData(self.engine)

        if not database_exists(database):
            self.db_create(database)

        return False

    def db_create(self, database):
        """
        Method to create a new RTK Program database.

        :param str database: the absolute path to the database to create.
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        create_database(database)

        RTKRevision.__table__.create(bind=self.engine)
        RTKMission.__table__.create(bind=self.engine)
        RTKMissionPhase.__table__.create(bind=self.engine)
        RTKEnvironment.__table__.create(bind=self.engine)
        RTKFailureDefinition.__table__.create(bind=self.engine)
        RTKFunction.__table__.create(bind=self.engine)
        RTKRequirement.__table__.create(bind=self.engine)
        RTKStakeholderInput.__table__.create(bind=self.engine)
        RTKMatrix.__table__.create(bind=self.engine)
        RTKHardware.__table__.create(bind=self.engine)
        RTKAllocation.__table__.create(bind=self.engine)
        RTKHazard.__table__.create(bind=self.engine)
        RTKSimilarItem.__table__.create(bind=self.engine)
        RTKReliability.__table__.create(bind=self.engine)
        RTKMilHdbkF.__table__.create(bind=self.engine)
        RTKNSWC.__table__.create(bind=self.engine)
        RTKDesignElectric.__table__.create(bind=self.engine)
        RTKDesignMechanic.__table__.create(bind=self.engine)
        RTKMode.__table__.create(bind=self.engine)
        RTKMechanism.__table__.create(bind=self.engine)
        RTKCause.__table__.create(bind=self.engine)
        RTKControl.__table__.create(bind=self.engine)
        RTKAction.__table__.create(bind=self.engine)
        RTKOpLoad.__table__.create(bind=self.engine)
        RTKOpStress.__table__.create(bind=self.engine)
        RTKTestMethod.__table__.create(bind=self.engine)
        RTKSoftware.__table__.create(bind=self.engine)
        RTKSoftwareDevelopment.__table__.create(bind=self.engine)
        RTKSRRSSR.__table__.create(bind=self.engine)
        RTKPDR.__table__.create(bind=self.engine)
        RTKCDR.__table__.create(bind=self.engine)
        RTKTRR.__table__.create(bind=self.engine)
        RTKSoftwareTest.__table__.create(bind=self.engine)
        RTKValidation.__table__.create(bind=self.engine)
        RTKIncident.__table__.create(bind=self.engine)
        RTKIncidentDetail.__table__.create(bind=self.engine)
        RTKIncidentAction.__table__.create(bind=self.engine)
        RTKTest.__table__.create(bind=self.engine)
        RTKGrowthTest.__table__.create(bind=self.engine)
        RTKSurvival.__table__.create(bind=self.engine)
        RTKSurvivalData.__table__.create(bind=self.engine)

        return False

    def db_add(self, item):
        """
        Method to add a new item to the RTK Program database.

        :param item: the object to add to the RTK Program database.
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "SUCCESS: Adding an item to the RTK Program database."

        try:
            if isinstance(item, list):
                self.session.add_all(item)
            else:
                self.session.add(item)
            self.session.commit()
        except:
            self.session.rollback()
            _error_code = 1003
            _msg = "ERROR: Adding an item to the RTK Program database."

        return _error_code, _msg

    def db_update(self):
        """
        Method to update the RTK Program database with any pending changes.

        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "SUCCESS: Updating the RTK Program database."

        try:
            self.session.commit()
        except:
            self.session.rollback()
            _error_code = 1004
            _msg = "ERROR: Updating the RTK Program database."

        return _error_code, _msg

    def db_delete(self, item):
        """
        Method to delete a record from the RTK Program database.

        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "SUCCESS: Deleting an item from the RTK Program database."

        try:
            self.session.delete(item)
            self.session.commit()
        except:
            self.session.rollback()
            _error_code = 1005
            _msg = "ERROR: Deleting an item from the RTK Program database."

        return _error_code, _msg

    def db_last_id(self):
        """
        Method to retrieve the value of the last ID column from a table in the
        RTK Program database.

        :return: _last_id; the last value of the ID column.
        :rtype: int
        """

        _last_id = 0

        return _last_id


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
    stakeholder = relationship('RTKStakeholderInput',
                               back_populates='revision')
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

        _values = (self.revision_id, self.availability_logistics,
                   self.availability_mission, self.cost, self.cost_failure,
                   self.cost_hour, self.hazard_rate_active,
                   self.hazard_rate_dormant, self.hazard_rate_logistics,
                   self.hazard_rate_mission, self.hazard_rate_software,
                   self.mmt, self.mcmt, self.mpmt, self.mtbf_logistics,
                   self.mtbf_mission, self.mttr, self.name,
                   self.reliability_logistics, self.reliability_mission,
                   self.remarks, self.total_part_count, self.revision_code,
                   self.program_time, self.program_time_sd, self.program_cost,
                   self.program_cost_sd)

        return _values

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
            _msg = "ERROR: Zero Division or Overflow Error when calculating " \
                   "the logistics MTBF.  Logistics hazard rate: {0:f}.".\
                   format(self.hazard_rate_logistics)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        # Calculate the mission MTBF.
        try:
            self.mtbf_mission = 1.0 / self.hazard_rate_mission
        except(ZeroDivisionError, OverflowError):
            self.mtbf_mission = 0.0
            _msg = "ERROR: Zero Division or Overflow Error when calculating " \
                   "the mission MTBF.  Mission hazard rate: {0:f}.".\
                   format(self.hazard_rate_logistics)
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
            _msg = "ERROR: Zero Division or Overflow Error when calculating " \
                   "the logistics availability.  Logistics MTBF: {0:f} and " \
                   "MTTR: {1:f}.".\
                   format(self.mtbf_logistics, self.mttr)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        # Calculate mission availability.
        try:
            self.availability_mission = self.mtbf_mission / \
                (self.mtbf_mission + self.mttr)
        except(ZeroDivisionError, OverflowError):
            self.availability_mission = 1.0
            _msg = "ERROR: Zero Division or Overflow Error when calculating " \
                   "the logistics availability.  Mission MTBF: {0:f} and " \
                   "MTTR: {1:f}.".\
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
            _msg = "ERROR: Zero Division Error when calculating the cost " \
                   "mission hour.  Mission time: {0:f}.".\
                   format(mission_time)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

        return _return


class RTKMission(Base):
    """
    Class to represent the rtk_mission table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relationship with rtk_mission_phase.
    """

    __tablename__ = 'rtk_mission'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    mission_id = Column('fld_mission_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)
    description = Column('fld_description', BLOB, default='')
    mission_time = Column('fld_mission_time', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='mission')
    phase = relationship('RTKMissionPhase', back_populates='mission')


class RTKMissionPhase(Base):
    """
    Class to represent the rtk_mission_phase table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_mission.
    This table shares a One-to-Many relationship with rtk_environment.
    """

    __tablename__ = 'rtk_mission_phase'

    mission_id = Column('fld_mission_id', Integer,
                        ForeignKey('rtk_mission.fld_mission_id'),
                        nullable=False)
    phase_id = Column('fld_phase_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)

    description = Column('fld_description', BLOB, default='')
    name = Column('fld_name', String(256), default='Phase Name')
    phase_start = Column('fld_phase_start', Float, default=0.0)
    phase_end = Column('fld_phase_end', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    mission = relationship('RTKMission', back_populates='phase')
    environment = relationship('RTKEnvironment', back_populates='phase',
                               cascade='delete')


class RTKEnvironment(Base):
    """
    Class to represent the rtk_environment table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_mission_phase.
    """

    __tablename__ = 'rtk_environment'

    phase_id = Column('fld_phase_id', Integer,
                      ForeignKey('rtk_mission_phase.fld_phase_id'),
                      nullable=False)
    # test_id = Column('fld_test_id', Integer,
    #                   ForeignKey('rtk_test.fld_test_id'),
    #                   nullable=False)
    environment_id = Column('fld_environment_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)

    name = Column('fld_name', String(256), default='Condition Name')
    units = Column('fld_units', String(128), default='Units')
    minimum = Column('fld_minimum', Float, default=0.0)
    maximum = Column('fld_maximum', Float, default=0.0)
    mean = Column('fld_mean', Float, default=0.0)
    variance = Column('fld_variance', Float, default=0.0)
    ramp_rate = Column('fld_ramp_rate', Float, default=0.0)
    low_dwell_time = Column('fld_low_dwell_time', Float, default=0.0)
    high_dwell_time = Column('fld_high_dwell_time', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    phase = relationship('RTKMissionPhase', back_populates='environment')


class RTKFailureDefinition(Base):
    """
    Class to represent the rtk_failure_definition table in the RTK Program
    database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_failure_definition'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    definition_id = Column('fld_definition_id', Integer, primary_key=True,
                           autoincrement=True, nullable=False)

    definition = Column('fld_definition', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='failures')


class RTKFunction(Base):
    """
    Class to represent the rtk_function table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relationship with rtk_mode.
    """

    __tablename__ = 'rtk_function'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    function_id = Column('fld_function_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

    availability_logistics = Column('fld_availability_logistics', Float,
                                    default=0.0)
    availability_mission = Column('fld_availability_mission', Float,
                                  default=0.0)
    cost = Column('cost', Float, default=0.0)
    function_code = Column('fld_function_code', String(16),
                           default='Function Code')
    hazard_rate_logistics = Column('fld_hazard_rate_logistics', Float,
                                   default=0.0)
    hazard_rate_mission = Column('fld_hazard_rate_mission', Float, default=0.0)
    level = Column('fld_level', Integer, default=0)
    mmt = Column('fld_mmt', Float, default=0.0)
    mcmt = Column('fld_mcmt', Float, default=0.0)
    mpmt = Column('fld_mpmt', Float, default=0.0)
    mtbf_logistics = Column('fld_mtbf_logistics', Float, default=0.0)
    mtbf_mission = Column('fld_mtbf_mission', Float, default=0.0)
    mttr = Column('fld_mttr', Float, default=0.0)
    name = Column('fld_name', String(256), default='Name')
    parent_id = Column('fld_parent_id', Integer, default=0)
    remarks = Column('fld_remarks', BLOB, default='')
    safety_critical = Column('fld_safety_critical', Integer, default=0)
    total_mode_count = Column('fld_mode_count', Integer, default=0)
    total_part_count = Column('fld_part_count', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='function')
    mode = relationship('RTKMode', back_populates='function')


class RTKRequirement(Base):
    """
    Class to represent the rtk_requirement table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_requirement'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    requirement_id = Column('fld_requirement_id', Integer, primary_key=True,
                            autoincrement=True, nullable=False)

    requirement_code = Column('fld_requirement_code', String(256), default='')
    description = Column('fld_description', BLOB, default='')
    type_id = Column('fld_type_id', Integer, default=0)
    priority = Column('fld_priority', Integer, default=0)
    specification = Column('fld_specification', String(256), default='')
    page_number = Column('fld_page_number', String(256), default='')
    figure_number = Column('fld_figure_number', String(256), default='')
    derived = Column('fld_derived', Integer, default=0)
    owner_id = Column('fld_owner_id', Integer, default=0)
    validated = Column('fld_validated', Integer, default=0)
    validated_date = Column('fld_validated_date', Date,
                            default=date.today())

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='requirement')


class RTKStakeholderInput(Base):
    """
    Class to represent the rtk_stakeholder_input table in the RTK Program
    database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_stakeholder_input'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    input_id = Column('fld_input_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)

    customer_rank = Column('fld_customer_rank', Integer, default=1)
    description = Column('fld_description', BLOB, default='')
    group = Column('fld_group', String(128), default='')
    improvement = Column('fld_improvement', Float, default=0.0)
    overall_weight = Column('fld_overall_weight', Float, default=0.0)
    planned_rank = Column('fld_planned_rank', Integer, default=1)
    priority = Column('fld_priority', Integer, default=1)
    requirement_id = Column('fld_requirement_id', Integer, default=0)
    stakeholder = Column('fld_stakeholder', String(128), default='')
    user_Float_1 = Column('fld_user_Float_1', Float, default=0.0)
    user_Float_2 = Column('fld_user_Float_2', Float, default=0.0)
    user_Float_3 = Column('fld_user_Float_3', Float, default=0.0)
    user_Float_4 = Column('fld_user_Float_4', Float, default=0.0)
    user_Float_5 = Column('fld_user_Float_5', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='stakeholder')


class RTKMatrix(Base):
    """
    Class to represent the rtk_matrix table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_matrix'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    matrix_id = Column('fld_matrix_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    column_id = Column('fld_column_id', Integer, default=0)
    column_item_id = Column('fld_column_item_id', Integer, default=0)
    parent_id = Column('fld_parent_id', Integer, default=0)
    row_id = Column('fld_row_id', Integer, default=0)
    row_item_id = Column('fld_row_item_id', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)
    value = Column('fld_value', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='matrix')


class RTKHardware(Base):
    """
    Class to represent the rtk_hardware table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relationship with rtk_hazard.
    This table shares a One-to-Many relationship with rtk_similar_item.
    This table shares a One-to-One relationship with rtk_allocation.
    This table shares a One-to-One relationship with rtk_reliability.
    This table shares a One-to-One relationship with rtk_mil_hdbk_f.
    This table shares a One-to-One relationship with rtk_nswc.
    This table shares a One-to-One relationship with rtk_design_electric.
    This table shares a One-to-One relationship with rtk_design_mechanic.
    """

    __tablename__ = 'rtk_hardware'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    hardware_id = Column('fld_hardware_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

    alt_part_number = Column('fld_alt_part_number', String(256), default='')
    attachments = Column('fld_attachments', String(512), default='')
    cage_code = Column('fld_cage_code', String(256), default='')
    comp_ref_des = Column('fld_comp_ref_des', String(256), default='')
    category_id = Column('fld_category_id', Integer, default=0)
    cost = Column('fld_cost', Float, default=0.0)
    cost_failure = Column('fld_cost_failure', Float, default=0.0)
    cost_hour = Column('fld_cost_hour', Float, default=0.0)
    cost_type_id = Column('fld_cost_Type_id', Integer, default=0)
    description = Column('fld_description', String(512), default='')
    duty_cycle = Column('fld_duty_cycle', Float, default=100.0)
    figure_number = Column('fld_figure_number', String(256), default='')
    lcn = Column('fld_lcn', String(256), default='')
    level = Column('fld_level', Integer, default=0)
    manufacturer_id = Column('fld_manufacturer_id', Integer, default=0)
    mission_time = Column('fld_mission_time', Float, default=100.0)
    name = Column('fld_name', String(256), default='')
    nsn = Column('fld_nsn', String(256), default='')
    page_number = Column('fld_page_number', String(256), default='')
    parent_id = Column('fld_parent_id', Integer, default=0)
    part = Column('fld_part', Integer, default=0)
    part_number = Column('fld_part_number', String(256), default='')
    quantity = Column('fld_quantity', Integer, default=1)
    ref_des = Column('fld_ref_des', String(256), default='')
    remarks = Column('fld_remarks', BLOB, default='')
    repairable = Column('fld_repairable', Integer, default=0)
    specification_number = Column('fld_specification_number', String(256),
                                  default='')
    subcategory_id = Column('fld_subcategory_id', Integer, default=0)
    tagged_part = Column('fld_tagged_part', Integer, default=0)
    total_part_count = Column('fld_total_part_count', Integer, default=0)
    total_power_dissipation = Column('fld_total_power_dissipation', Float,
                                     default=0.0)
    year_of_manufacture = Column('fld_year_of_manufacture', Integer,
                                 default=date.today().year)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='hardware')

    # One-to-one relationships.
    allocation = relationship('RTKAllocation', back_populates='hardware')
    hazard = relationship('RTKHazard', back_populates='hardware')
    sia = relationship('RTKSimilarItem', back_populates='hardware')
    mode = relationship('RTKMode', back_populates='hardware')

    reliability = relationship('RTKReliability', uselist=False,
                               back_populates='hardware')
    milhdbkf = relationship('RTKMilHdbkF', uselist=False,
                            back_populates='hardware')
    nswc = relationship('RTKNSWC', uselist=False,
                        back_populates='hardware')
    design_electric = relationship('RTKDesignElectric', uselist=False,
                                   back_populates='hardware')
    design_mechanic = relationship('RTKDesignMechanic', uselist=False,
                                   back_populates='hardware')


class RTKAllocation(Base):
    """
    Class to represent the rtk_allocation table in the RTK Program database.
    
    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_allocation'

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    availability_alloc = Column('fld_availability_alloc', Float, default=0.0)
    env_factor = Column('fld_env_factor', Integer, default=1)
    goal_measure_id = Column('fld_goal_measure_id', Integer, default=1)
    hazard_rate_alloc = Column('fld_hazard_rate_alloc', Float, default=0.0)
    hazard_rate_goal = Column('fld_hazard_rate_goal', Float, default=0.0)
    included = Column('fld_included', Integer, default=1)
    int_factor = Column('fld_int_factor', Integer, default=1)
    method_id = Column('fld_method_id', Integer, default=1)
    mtbf_alloc = Column('fld_mtbf_alloc', Float, default=0.0)
    mtbf_goal = Column('fld_mtbf_goal', Float, default=0.0)
    n_sub_systems = Column('fld_n_sub_systems', Integer, default=1)
    n_sub_elements = Column('fld_n_sub_elements', Integer, default=1)
    parent_id = Column('fld_parent_id', Integer, default=1)
    percent_weight_factor = Column('fld_percent_weight_factor', Float,
                                   default=0.0)
    reliability_alloc = Column('fld_reliability_alloc', Float, default=0.0)
    reliability_goal = Column('fld_reliability_goal', Float, default=1.0)
    op_time_factor = Column('fld_op_time_factor', Integer, default=1)
    soa_factor = Column('fld_soa_factor', Integer, default=1)
    weight_factor = Column('fld_weight_factor', Integer, default=1)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='allocation')


class RTKHazard(Base):
    """
    Class to represent the rtk_hazard table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_hazard'

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         nullable=False)
    hazard_id = Column('fld_hazard_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    potential_hazard = Column('fld_potential_hazard', String(256), default='')
    potential_cause = Column('fld_potential_cause', String(512), default='')
    assembly_effect = Column('fld_assembly_effect', String(512), default='')
    assembly_severity_id = Column('fld_assembly_severity', Integer,
                                  default=4)
    assembly_probability_id = Column('fld_assembly_probability', Integer,
                                     default=5)
    assembly_hri = Column('fld_assembly_hri', Integer, default=20)
    assembly_mitigation = Column('fld_assembly_mitigation', BLOB, default='')
    assembly_severity_id_f = Column('fld_assembly_severity_f', Integer,
                                    default=4)
    assembly_probability_id_f = Column('fld_assembly_probability_f',
                                       Integer, default=5)
    assembly_hri_id_f = Column('fld_assembly_hri_f', Integer, default=4)
    system_effect = Column('fld_system_effect', String(512), default='')
    system_severity = Column('fld_system_severity', Integer, default=4)
    system_probability = Column('fld_system_probability', Integer, default=5)
    system_hri = Column('fld_system_hri', Integer, default=20)
    system_mitigation = Column('fld_system_mitigation', BLOB, default='')
    system_severity_f = Column('fld_system_severity_f', Integer, default=4)
    system_probability_f = Column('fld_system_probability_f', Integer,
                                  default=5)
    system_hri_f = Column('fld_system_hri_f', Integer, default=20)
    remarks = Column('fld_remarks', BLOB, default='')
    function_1 = Column('fld_function_1', String(128), default='')
    function_2 = Column('fld_function_2', String(128), default='')
    function_3 = Column('fld_function_3', String(128), default='')
    function_4 = Column('fld_function_4', String(128), default='')
    function_5 = Column('fld_function_5', String(128), default='')
    result_1 = Column('fld_result_1', Float, default=0.0)
    result_2 = Column('fld_result_2', Float, default=0.0)
    result_3 = Column('fld_result_3', Float, default=0.0)
    result_4 = Column('fld_result_4', Float, default=0.0)
    result_5 = Column('fld_result_5', Float, default=0.0)
    user_blob_1 = Column('fld_user_blob_1', BLOB, default='')
    user_blob_2 = Column('fld_user_blob_2', BLOB, default='')
    user_blob_3 = Column('fld_user_blob_3', BLOB, default='')
    user_Float_1 = Column('fld_user_Float_1', Float, default=0.0)
    user_Float_2 = Column('fld_user_Float_2', Float, default=0.0)
    user_Float_3 = Column('fld_user_Float_3', Float, default=0.0)
    user_int_1 = Column('fld_user_int_1', Integer, default=0)
    user_int_2 = Column('fld_user_int_2', Integer, default=0)
    user_int_3 = Column('fld_user_int_3', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='hazard')


class RTKSimilarItem(Base):
    """
    Class to represent the rtk_similar_item table in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_similar_item'

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    change_description_1 = Column('fld_change_description_1', BLOB, default='')
    change_description_2 = Column('fld_change_description_2', BLOB, default='')
    change_description_3 = Column('fld_change_description_3', BLOB, default='')
    change_description_4 = Column('fld_change_description_4', BLOB, default='')
    change_description_5 = Column('fld_change_description_5', BLOB, default='')
    change_description_6 = Column('fld_change_description_6', BLOB, default='')
    change_description_7 = Column('fld_change_description_7', BLOB, default='')
    change_description_8 = Column('fld_change_description_8', BLOB, default='')
    change_description_9 = Column('fld_change_description_9', BLOB, default='')
    change_description_10 = Column('fld_change_description_10', BLOB,
                                   default='')
    change_factor_1 = Column('fld_change_factor_1', Float, default=1.0)
    change_factor_2 = Column('fld_change_factor_2', Float, default=1.0)
    change_factor_3 = Column('fld_change_factor_3', Float, default=1.0)
    change_factor_4 = Column('fld_change_factor_4', Float, default=1.0)
    change_factor_5 = Column('fld_change_factor_5', Float, default=1.0)
    change_factor_6 = Column('fld_change_factor_6', Float, default=1.0)
    change_factor_7 = Column('fld_change_factor_7', Float, default=1.0)
    change_factor_8 = Column('fld_change_factor_8', Float, default=1.0)
    change_factor_9 = Column('fld_change_factor_9', Float, default=1.0)
    change_factor_10 = Column('fld_change_factor_10', Float, default=1.0)
    environment_from_id = Column('fld_environment_from_id', Integer, default=0)
    environment_to_id = Column('fld_environment_to_id', Integer, default=0)
    function_1 = Column('fld_function_1', String(128), default='')
    function_2 = Column('fld_function_2', String(128), default='')
    function_3 = Column('fld_function_3', String(128), default='')
    function_4 = Column('fld_function_4', String(128), default='')
    function_5 = Column('fld_function_5', String(128), default='')
    method_id = Column('fld_method_id', Integer, default=0)
    parent_id = Column('fld_parent_id', Integer, default=0)
    quality_from_id = Column('fld_quality_from_id', Integer, default=0)
    quality_to_id = Column('fld_quality_to_id', Integer, default=0)
    result_1 = Column('fld_result_1', Float, default=0.0)
    result_2 = Column('fld_result_2', Float, default=0.0)
    result_3 = Column('fld_result_3', Float, default=0.0)
    result_4 = Column('fld_result_4', Float, default=0.0)
    result_5 = Column('fld_result_5', Float, default=0.0)
    temperature_from = Column('fld_temperature_from', Float, default=30.0)
    temperature_to = Column('fld_temperature_to', Float, default=30.0)
    user_blob_1 = Column('fld_user_blob_1', BLOB, default='')
    user_blob_2 = Column('fld_user_blob_2', BLOB, default='')
    user_blob_3 = Column('fld_user_blob_3', BLOB, default='')
    user_blob_4 = Column('fld_user_blob_4', BLOB, default='')
    user_blob_5 = Column('fld_user_blob_5', BLOB, default='')
    user_float_1 = Column('fld_user_Float_1', Float, default=0.0)
    user_float_2 = Column('fld_user_Float_2', Float, default=0.0)
    user_float_3 = Column('fld_user_Float_3', Float, default=0.0)
    user_float_4 = Column('fld_user_Float_4', Float, default=0.0)
    user_float_5 = Column('fld_user_Float_5', Float, default=0.0)
    user_int_1 = Column('fld_user_int_1', Integer, default=0)
    user_int_2 = Column('fld_user_int_2', Integer, default=0)
    user_int_3 = Column('fld_user_int_3', Integer, default=0)
    user_int_4 = Column('fld_user_int_4', Integer, default=0)
    user_int_5 = Column('fld_user_int_5', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='sia')


class RTKReliability(Base):
    """
    Class to represent the rtk_reliability table in the RTK Program database.
    
    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_reliability'

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    add_adj_factor = Column('fld_add_adj_factor', Float, default=0.0)
    availability_logistics = Column('fld_availability_logistics', Float,
                                    default=1.0)
    availability_mission = Column('fld_availability_mission', Float,
                                  default=1.0)
    avail_log_variance = Column('fld_avail_log_variance', Float, default=0.0)
    avail_mis_variance = Column('fld_avail_mis_variance', Float, default=0.0)
    failure_distribution_id = Column('fld_failure_distribution_id', Integer,
                                     default=0)
    hazard_rate_active = Column('fld_hazard_rate_active', Float, default=0.0)
    hazard_rate_dormant = Column('fld_hazard_rate_dormant', Float, default=0.0)
    hazard_rate_logistics = Column('fld_hazard_rate_logistics', Float,
                                   default=0.0)
    hazard_rate_method_id = Column('fld_hazard_rate_method_id', Integer,
                                   default=0)
    hazard_rate_mission = Column('fld_hazard_rate_mission', Float, default=0.0)
    hazard_rate_model = Column('fld_hazard_rate_model', String(512),
                               default='')
    hazard_rate_percent = Column('fld_hazard_rate_percent', Float, default=0.0)
    hazard_rate_software = Column('fld_hazard_rate_software', Float,
                                  default=0.0)
    hazard_rate_specified = Column('fld_hazard_rate_specified', Float,
                                   default=0.0)
    hazard_rate_type_id = Column('fld_hazard_rate_type_id', Integer, default=0)
    hr_active_variance = Column('fld_hr_active_variance', Float, default=0.0)
    hr_dormant_variance = Column('fld_hr_dormant_variance', Float, default=0.0)
    hr_logistics_variance = Column('fld_hr_log_variance', Float, default=0.0)
    hr_mission_variance = Column('fld_hr_mis_variance', Float, default=0.0)
    hr_specified_variance = Column('fld_hr_spec_variance', Float, default=0.0)
    lambda_b = Column('fld_lambda_b', Float, default=0.0)
    location_parameter = Column('fld_location_parameter', Float, default=0.0)
    mtbf_logistics = Column('fld_mtbf_logistics', Float, default=0.0)
    mtbf_mission = Column('fld_mtbf_mission', Float, default=0.0)
    mtbf_specified = Column('fld_mtbf_specified', Float, default=0.0)
    mtbf_log_variance = Column('fld_mtbf_log_variance', Float, default=0.0)
    mtbf_mis_variance = Column('fld_mtbf_mis_variance', Float, default=0.0)
    mtbf_spec_variance = Column('fld_mtbf_spec_variance', Float, default=0.0)
    mult_adj_factor = Column('fld_mult_adj_factor', Float, default=0.0)
    quality_id = Column('fld_quality_id', Integer, default=0)
    reliability_goal = Column('fld_reliability_goal', Float, default=0.0)
    reliability_goal_meassure_id = Column('fld_reliability_goal_measure_id',
                                          Integer, default=0)
    reliability_logistics = Column('fld_reliability_logistics', Float,
                                   default=0.0)
    reliability_mission = Column('fld_reliability_mission', Float, default=0.0)
    reliability_log_variance = Column('fld_reliability_log_variance', Float,
                                      default=0.0)
    reliability_mis_variance = Column('fld_reliability_mis_variance', Float,
                                      default=0.0)
    scale_parameter = Column('fld_scale_parameter', Float, default=0.0)
    shape_parameter = Column('fld_shape_parameter', Float, default=0.0)
    survival_analysis_id = Column('fld_survival_analysis_id', Integer,
                                  default=0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='reliability')


class RTKMilHdbkF(Base):
    """
    Class to represent the rtk_mil_hdbk_f table in the RTK Program database.
    
    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_mil_hdbk_f'

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    A1 = Column('fld_a_one', Float, default=0.0)
    A2 = Column('fld_a_two', Float, default=0.0)
    B1 = Column('fld_b_one', Float, default=0.0)
    B2 = Column('fld_b_two', Float, default=0.0)
    C1 = Column('fld_c_one', Float, default=0.0)
    C2 = Column('fld_c_two', Float, default=0.0)
    lambdaDB = Column('fld_lambda_bd', Float, default=0.0)
    lambdaBP = Column('fld_lambda_bp', Float, default=0.0)
    lambdaCYC = Column('fld_lambda_cyc', Float, default=0.0)
    lambdaEOS = Column('fld_lambda_eos', Float, default=0.0)
    piA = Column('fld_pi_a', Float, default=0.0)
    piC = Column('fld_pi_c', Float, default=0.0)
    piCD = Column('fld_pi_cd', Float, default=0.0)
    piCF = Column('fld_pi_cf', Float, default=0.0)
    piCR = Column('fld_pi_cr', Float, default=0.0)
    piCV = Column('fld_pi_cv', Float, default=0.0)
    piCYC = Column('fld_pi_cyc', Float, default=0.0)
    piE = Column('fld_pi_e', Float, default=0.0)
    piF = Column('fld_pi_f', Float, default=0.0)
    piI = Column('fld_pi_i', Float, default=0.0)
    piK = Column('fld_pi_k', Float, default=0.0)
    piL = Column('fld_pi_l', Float, default=0.0)
    piM = Column('fld_pi_m', Float, default=0.0)
    piMFG = Column('fld_pi_mfg', Float, default=0.0)
    piN = Column('fld_pi_n', Float, default=0.0)
    piNR = Column('fld_pi_nr', Float, default=0.0)
    piP = Column('fld_pi_p', Float, default=0.0)
    piPT = Column('fld_pi_pt', Float, default=0.0)
    piQ = Column('fld_pi_q', Float, default=0.0)
    piR = Column('fld_pi_r', Float, default=0.0)
    piS = Column('fld_pi_s', Float, default=0.0)
    piT = Column('fld_pi_t', Float, default=0.0)
    piTAPS = Column('fld_pi_taps', Float, default=0.0)
    pi_u = Column('fld_pi_u', Float, default=0.0)
    pi_v = Column('fld_pi_v', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='milhdbkf')


class RTKNSWC(Base):
    """
    Class to represent the rtk_nswc table in the RTK Program database.
    
    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_nswc'

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    Cac = Column('fld_c_ac', Float, default=0.0)
    Calt = Column('fld_c_alt', Float, default=0.0)
    Cb = Column('fld_c_b', Float, default=0.0)
    Cbl = Column('fld_c_bl', Float, default=0.0)
    Cbt = Column('fld_c_bt', Float, default=0.0)
    Cbv = Column('fld_c_bv', Float, default=0.0)
    Cc = Column('fld_c_c', Float, default=0.0)
    Ccf = Column('fld_c_cf', Float, default=0.0)
    Ccp = Column('fld_c_cp', Float, default=0.0)
    Ccs = Column('fld_c_cs', Float, default=0.0)
    Ccv = Column('fld_c_cv', Float, default=0.0)
    Ccw = Column('fld_c_cw', Float, default=0.0)
    Cd = Column('fld_c_d', Float, default=0.0)
    Cdc = Column('fld_c_dc', Float, default=0.0)
    Cdl = Column('fld_c_dl', Float, default=0.0)
    Cdp = Column('fld_c_dp', Float, default=0.0)
    Cds = Column('fld_c_ds', Float, default=0.0)
    Cdt = Column('fld_c_dt', Float, default=0.0)
    Cdw = Column('fld_c_dw', Float, default=0.0)
    Cdy = Column('fld_c_dy', Float, default=0.0)
    Ce = Column('fld_c_e', Float, default=0.0)
    Cf = Column('fld_c_f', Float, default=0.0)
    Cg = Column('fld_c_g', Float, default=0.0)
    Cga = Column('fld_c_ga', Float, default=0.0)
    Cgl = Column('fld_c_gl', Float, default=0.0)
    Cgp = Column('fld_c_gp', Float, default=0.0)
    Cgs = Column('fld_c_gs', Float, default=0.0)
    Cgt = Column('fld_c_gt', Float, default=0.0)
    Cgv = Column('fld_c_gv', Float, default=0.0)
    Ch = Column('fld_c_h', Float, default=0.0)
    Ci = Column('fld_c_i', Float, default=0.0)
    Ck = Column('fld_c_k', Float, default=0.0)
    Cl = Column('fld_c_l', Float, default=0.0)
    Clc = Column('fld_c_lc', Float, default=0.0)
    Cm = Column('fld_c_m', Float, default=0.0)
    Cmu = Column('fld_c_mu', Float, default=0.0)
    Cn = Column('fld_c_n', Float, default=0.0)
    Cnp = Column('fld_c_np', Float, default=0.0)
    Cnw = Column('fld_c_nw', Float, default=0.0)
    Cp = Column('fld_c_p', Float, default=0.0)
    Cpd = Column('fld_c_pd', Float, default=0.0)
    Cpf = Column('fld_c_pf', Float, default=0.0)
    Cpv = Column('fld_c_pv', Float, default=0.0)
    Cq = Column('fld_c_q', Float, default=0.0)
    Cr = Column('fld_c_r', Float, default=0.0)
    Crd = Column('fld_c_rd', Float, default=0.0)
    Cs = Column('fld_c_s', Float, default=0.0)
    Csc = Column('fld_c_sc', Float, default=0.0)
    Csf = Column('fld_c_sf', Float, default=0.0)
    Cst = Column('fld_c_st', Float, default=0.0)
    Csv = Column('fld_c_sv', Float, default=0.0)
    Csw = Column('fld_c_sw', Float, default=0.0)
    Csz = Column('fld_c_sz', Float, default=0.0)
    Ct = Column('fld_c_t', Float, default=0.0)
    Cv = Column('fld_c_v', Float, default=0.0)
    Cw = Column('fld_c_w', Float, default=0.0)
    Cy = Column('fld_c_y', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='nswc')


class RTKDesignElectric(Base):
    """
    Class to represent the rtk_design_electric table in the RTK Program 
    database.
    
    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_design_electric'

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    application_id = Column('fld_application_id', Integer, default=0)
    area = Column('fld_area', Float, default=0.0)
    capacitance = Column('fld_capacitance', Float, default=0.0)
    configuration_id = Column('fld_configuration_id', Integer, default=0)
    construction_id = Column('fld_construction_id', Integer, default=0)
    contact_form_id = Column('fld_contact_form_id', Integer, default=0)
    contact_gauge = Column('fld_contact_gauge', Integer, default=0)
    contact_rating_id = Column('fld_contact_rating_id', Integer, default=0)
    current_operating = Column('fld_current_operating', Float, default=0.0)
    current_rated = Column('fld_current_rated', Float, default=0.0)
    current_ratio = Column('fld_current_ratio', Float, default=0.0)
    environment_active_id = Column('fld_environment_active_id', Integer,
                                   default=0)
    environment_dormant_id = Column('fld_environment_dormant_id', Integer,
                                    default=0)
    family_id = Column('fld_family_id', Integer, default=0)
    feature_size = Column('fld_feature_size', Float, default=0.0)
    frequency_operating = Column('fld_frequency_operating', Float, default=0.0)
    insert_id = Column('fld_insert_id', Integer, default=0)
    insulation_id = Column('fld_insulation_id', Integer, default=0)
    manufacturing_id = Column('fld_manufacturing_id', Integer, default=0)
    matching_id = Column('fld_matching_id', Integer, default=0)
    n_active_pins = Column('fld_n_active_pins', Integer, default=0)
    n_circuit_planes = Column('fld_n_circuit_planes', Integer, default=1)
    n_cycles = Column('fld_n_cycles', Integer, default=0)
    n_elements = Column('fld_n_elements', Integer, default=0)
    n_hand_soldered = Column('fld_n_hand_soldered', Integer, default=0)
    n_wave_soldered = Column('fld_n_wave_soldered', Integer, default=0)
    operating_life = Column('fld_operating_life', Float, default=0.0)
    overstress = Column('fld_overstress', Integer, default=0)
    package_id = Column('fld_package_id', Integer, default=0)
    power_operating = Column('fld_power_operating', Float, default=0.0)
    power_rated = Column('fld_power_rated', Float, default=0.0)
    power_ratio = Column('fld_power_ratio', Float, default=0.0)
    reason = Column('fld_reason', String(1024), default='')
    resistance = Column('fld_resistance', Float, default=0.0)
    specification_id = Column('fld_specification_id', Integer, default=0)
    technology_id = Column('fld_technology_id', Integer, default=0)
    temperature_case = Column('fld_temperature_case', Float, default=0.0)
    temperature_hot_spot = Column('fld_temperature_hot_spot', Float,
                                  default=0.0)
    temperature_junction = Column('fld_temperature_junction', Float,
                                  default=0.0)
    temperature_rated_max = Column('fld_temperature_rated_max', Float,
                                   default=0.0)
    temperature_rated_min = Column('fld_temperature_rated_min', Float,
                                   default=0.0)
    temperature_rise = Column('fld_temperature_rise', Float, default=0.0)
    theta_jc = Column('fld_theta_jc', Float, default=0.0)
    type_id = Column('fld_type_id', Integer, default=0)
    voltage_ac_operating = Column('fld_voltage_ac_operating', Float,
                                  default=0.0)
    voltage_dc_operating = Column('fld_voltage_dc_operating', Float,
                                  default=0.0)
    voltage_esd = Column('fld_voltage_esd', Float, default=0.0)
    voltage_rated = Column('fld_voltage_rated', Float, default=0.0)
    voltage_ratio = Column('fld_voltage_ratio', Float, default=0.0)
    weight = Column('fld_weight', Float, default=0.0)
    years_in_production = Column('fld_years_in_production', Integer, default=1)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware',
                            back_populates='design_electric')


class RTKDesignMechanic(Base):
    """
    Class to represent the rtk_design_mechanical table in the RTK Program 
    database.
    
    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_design_mechanic'

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    altitude_operating = Column('fld_altitude_operating', Float, default=0.0)
    application_id = Column('fld_application_id', Integer, default=0)
    balance_id = Column('fld_balance_id', Integer, default=0)
    clearance = Column('fld_clearance', Float, default=0.0)
    casing_id = Column('fld_casing_id', Integer, default=0)
    contact_pressure = Column('fld_contact_pressure', Float, default=0.0)
    deflection = Column('fld_deflection', Float, default=0.0)
    diameter_coil = Column('fld_diameter_coil', Float, default=0.0)
    diameter_inner = Column('fld_diameter_inner', Float, default=0.0)
    diameter_outer = Column('fld_diameter_outer', Float, default=0.0)
    diameter_wire = Column('fld_diameter_wire', Float, default=0.0)
    filter_size = Column('fld_filter_size', Float, default=0.0)
    flow_design = Column('fld_flow_design', Float, default=0.0)
    flow_operating = Column('fld_flow_operating', Float, default=0.0)
    frequency_operating = Column('fld_frequency_operating', Float, default=0.0)
    friction = Column('fld_friction', Float, default=0.0)
    impact_id = Column('fld_impact_id', Integer, default=0)
    leakage_allowable = Column('fld_leakage_allowable', Float, default=0.0)
    length = Column('fld_length', Float, default=0.0)
    length_compressed = Column('fld_length_compressed', Float, default=0.0)
    length_relaxed = Column('fld_length_relaxed', Float, default=0.0)
    load_design = Column('fld_load_design', Float, default=0.0)
    load_id = Column('fld_load_id', Integer, default=0)
    load_operating = Column('fld_load_operating', Float, default=0.0)
    lubrication_id = Column('fld_lubrication_id', Integer, default=0)
    manufacturing_id = Column('fld_manufacturing_id', Integer, default=0)
    material_id = Column('fld_material_id', Integer, default=0)
    meyer_hardness = Column('fld_meyer_hardness', Float, default=0.0)
    misalignment_angle = Column('fld_misalignment_angle', Float, default=0.0)
    n_ten = Column('fld_n_ten', Integer, default=0)
    n_cycles = Column('fld_n_cycles', Integer, default=0)
    n_elements = Column('fld_n_elements', Integer, default=0)
    offset = Column('fld_offset', Float, default=0.0)
    particle_size = Column('fld_particle_size', Float, default=0.0)
    pressure_contact = Column('fld_pressure_contact', Float, default=0.0)
    pressure_delta = Column('fld_pressure_delta', Float, default=0.0)
    pressure_downstream = Column('fld_pressure_downstream', Float, default=0.0)
    pressure_rated = Column('fld_pressure_rated', Float, default=0.0)
    pressure_upstream = Column('fld_pressure_upstream', Float, default=0.0)
    rpm_design = Column('fld_rpm_design', Float, default=0.0)
    rpm_operating = Column('fld_rpm_operating', Float, default=0.0)
    service_id = Column('fld_service_id', Integer, default=0)
    spring_index = Column('fld_spring_index', Float, default=0.0)
    surface_finish = Column('fld_surface_finish', Float, default=0.0)
    technology_id = Column('fld_technology_id', Integer, default=0)
    thickness = Column('fld_thickness', Float, default=0.0)
    torque_id = Column('fld_torque_id', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)
    viscosity_design = Column('fld_viscosity_design', Float, default=0.0)
    viscosity_dynamic = Column('fld_viscosity_dynamic', Float, default=0.0)
    water_per_cent = Column('fld_water_per_cent', Float, default=0.0)
    width_minimum = Column('fld_width_minimum', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware',
                            back_populates='design_mechanic')


class RTKMode(Base):
    """
    Class to represent the table rtk_mode in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_function.
    This table shares a Many-to-One relationship with rtk_hardware.
    This table shares a One-to-Many relationship with rtk_mechanism.
    """

    __tablename__ = 'rtk_mode'

    function_id = Column('fld_function_id', Integer,
                         ForeignKey('rtk_function.fld_function_id'),
                         nullable=False)
    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         nullable=False)
    mode_id = Column('fld_mode_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)

    critical_item = Column('fld_critial_item', Integer, default=0)
    description = Column('fld_description', String(512), default='')
    design_provisions = Column('fld_design_provisions', BLOB, default='')
    detection_method = Column('fld_detection_method', String(512), default='')
    effect_end = Column('fld_effect_end', String(512), default='')
    effect_local = Column('fld_effect_local', String(512), default='')
    effect_next = Column('fld_effect_next', String(512), default='')
    effect_probability = Column('fld_effect_probability', Float, default=0.0)
    hazard_rate_source = Column('fld_hazard_rate_source', String(512),
                                default='')
    isolation_method = Column('fld_isolation_method', String(512), default='')
    mission = Column('fld_mission', String(64), default='Default Mission')
    mission_phase = Column('fld_mission_phase', String(64), default='')
    mode_criticality = Column('fld_mode_criticality', Float, default=0.0)
    mode_hazard_rate = Column('fld_mode_hazard_rate', Float, default=0.0)
    mode_op_time = Column('fld_mode_op_time', Float, default=0.0)
    mode_probability = Column('fld_mode_probability', String(64), default='')
    mode_ratio = Column('fld_mode_ratio', Float, default=0.0)
    operator_actions = Column('fld_operator_actions', BLOB, default='')
    other_indications = Column('fld_other_indications', String(512),
                               default='')
    remarks = Column('fld_remarks', BLOB, default='')
    rpn_severity = Column('fld_rpn_severity', String(64), default='')
    rpn_severity_new = Column('fld_rpn_severity_new', String(64), default='')
    severity_class = Column('fld_severity_class', String(64), default='')
    single_point = Column('fld_single_point', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    function = relationship('RTKFunction', back_populates='mode')
    hardware = relationship('RTKHardware', back_populates='mode')
    mechanism = relationship('RTKMechanism', back_populates='mode')


class RTKMechanism(Base):
    """
    Class to represent the table rtk_mechanism in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_mode.
    This table shares a One-to-Many relationship with rtk_cause.
    This table shares a One-to-Many relationship with rtk_op_load.
    """

    __tablename__ = 'rtk_mechanism'

    mode_id = Column('fld_mode_id', Integer,
                     ForeignKey('rtk_mode.fld_mode_id'),
                     nullable=False)
    mechanism_id = Column('fld_mechanism_id', Integer, primary_key=True,
                          autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    pof_include = Column('fld_pof_include', Integer, default=1)
    rpn = Column('fld_rpn', Integer, default=0)
    rpn_detection = Column('fld_rpn_detection', Integer, default=0)
    rpn_detction_new = Column('fld_rpn_detection_new', Integer, default=0)
    rpn_new = Column('fld_rpn_new', Integer, default=0)
    rpn_occurrence = Column('fld_rpn_occurrence', Integer, default=0)
    rpn_occurrence_new = Column('fld_rpn_occurrence_new', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    mode = relationship('RTKMode', back_populates='mechanism')
    cause = relationship('RTKCause', back_populates='mechanism')
    op_load = relationship('RTKOpLoad', back_populates='mechanism')


class RTKCause(Base):
    """
    Class to represent the table rtk_cause in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_mechanism.
    This table shared a One-to-Many relationship with rtk_control.
    This table shared a One-to-Many relationship with rtk_action.
    """

    __tablename__ = 'rtk_cause'

    mechanism_id = Column('fld_mechanism_id', Integer,
                          ForeignKey('rtk_mechanism.fld_mechanism_id'),
                          nullable=False)
    cause_id = Column('fld_cause_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    rpn = Column('fld_rpn', Integer, default=0)
    rpn_detection = Column('fld_rpn_detection', Integer, default=0)
    rpn_detction_new = Column('fld_rpn_detection_new', Integer, default=0)
    rpn_new = Column('fld_rpn_new', Integer, default=0)
    rpn_occurrence = Column('fld_rpn_occurrence', Integer, default=0)
    rpn_occurrence_new = Column('fld_rpn_occurrence_new', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    mechanism = relationship('RTKMechanism', back_populates='cause')
    control = relationship('RTKControl', back_populates='cause')
    action = relationship('RTKAction', back_populates='cause')


class RTKControl(Base):
    """
    Class to represent the table rtk_control in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_control'

    cause_id = Column('fld_cause_id', Integer,
                      ForeignKey('rtk_cause.fld_cause_id'), nullable=False)
    control_id = Column('fld_control_id', Integer, primary_key=True,
                        autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    cause = relationship('RTKCause', back_populates='control')


class RTKAction(Base):
    """
    Class to represent the table rtk_action in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_cause.
    """

    __tablename__ = 'rtk_action'

    cause_id = Column('fld_cause_id', Integer,
                      ForeignKey('rtk_cause.fld_cause_id'), nullable=False)
    action_id = Column('fld_action_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    action_recommended = Column('fld_action_recommended', BLOB, default='')
    action_category = Column('fld_action_category', Integer, default=0)
    action_owner = Column('fld_action_owner', Integer, default=0)
    action_due_date = Column('fld_action_due_date', Date,
                             default=date.today() + timedelta(days=30))
    action_status_id = Column('fld_action_status', Integer, default=0)
    action_taken = Column('fld_action_taken', BLOB, default='')
    action_approved = Column('fld_action_approved', Integer, default=0)
    action_approve_date = Column('fld_action_approve_date', Date,
                                 default=date.today() + timedelta(days=30))
    action_closed = Column('fld_action_closed', Integer, default=0)
    action_close_date = Column('fld_action_close_date', Date,
                               default=date.today() + timedelta(days=30))

    # Define the relationships to other tables in the RTK Program database.
    cause = relationship('RTKCause', back_populates='action')


class RTKOpLoad(Base):
    """
    Class to represent the table rtk_op_load in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_mechanism.
    This table shares a One-to-Many relationship with rtk_op_stress.
    """

    __tablename__ = 'rtk_op_load'

    mechanism_id = Column('fld_mechanism_id', Integer,
                          ForeignKey('rtk_mechanism.fld_mechanism_id'),
                          nullable=False)
    load_id = Column('fld_load_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    damage_model = Column('fld_damage_model', Integer, default=0)
    priority_id = Column('fld_priority_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    mechanism = relationship('RTKMechanism', back_populates='op_load')
    op_stress = relationship('RTKOpStress', back_populates='op_load')


class RTKOpStress(Base):
    """
    Class to represent the table rtk_op_stress in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_op_load.
    """

    __tablename__ = 'rtk_op_stress'

    load_id = Column('fld_load_id', Integer,
                     ForeignKey('rtk_op_load.fld_load_id'), nullable=False)
    stress_id = Column('fld_stress_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    measurable_parameter = Column('fld_measurable_parameter', Integer,
                                  default=0)
    load_history = Column('fld_load_history', Integer, default=0)
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    op_load = relationship('RTKOpLoad', back_populates='op_stress')
    test_method = relationship('RTKTestMethod', back_populates='op_stress')


class RTKTestMethod(Base):
    """
    Class to represent the table rtk_test_method in the RTK Program database.
    
    This table shared a Many-to-One relationship with rtk_op_stress.
    """

    __tablename__ = 'rtk_test_method'

    stress_id = Column('fld_stress_id', Integer,
                       ForeignKey('rtk_op_stress.fld_stress_id'),
                       nullable=False)
    test_id = Column('fld_test_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)

    description = Column('fld_description', String(512), default='')
    boundary_conditions = Column('fld_boundary_conditions', String(512),
                                 default='')
    remarks = Column('fld_remarks', BLOB, default='')

    # Define the relationships to other tables in the RTK Program database.
    op_stress = relationship('RTKOpStress', back_populates='test_method')


class RTKSoftware(Base):
    """
    Class to represent the table rtk_software in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    This table shares
    """

    __tablename__ = 'rtk_software'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    software_id = Column('fld_software_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

    a = Column('fld_a', Float, default=0.0)
    aloc = Column('fld_aloc', Integer, default=0)
    am = Column('fld_am', Float, default=0.0)
    application_id = Column('fld_application_id', Integer, default=0)
    ax = Column('fld_ax', Integer, default=0)
    budget_test = Column('fld_budget_test', Float, default=0.0)
    budget_dev = Column('fld_budget_dev', Float, default=0.0)
    bx = Column('fld_bx', Integer, default=0)
    category_id = Column('fld_category_id', Integer, default=0)
    cb = Column('fld_cb', Integer, default=0)
    cx = Column('fld_cx', Integer, default=0)
    d = Column('fld_d', Float, default=0.0)
    dc = Column('fld_dc', Float, default=0.0)
    dd = Column('fld_dd', Integer, default=0)
    description = Column('fld_description', String(512), default='')
    development_id = Column('fld_development_id', Integer, default=0)
    dev_assess_type_id = Column('fld_dev_assess_type_id', Integer, default=0)
    df = Column('fld_df', Float, default=0.0)
    do = Column('fld_do', Float, default=0.0)
    dr = Column('fld_dr', Float, default=0.0)
    dr_eot = Column('fld_dr_eot', Integer, default=0)
    dr_test = Column('fld_dr_test', Integer, default=0)
    e = Column('fld_e', Float, default=0.0)
    ec = Column('fld_ec', Float, default=0.0)
    et = Column('fld_et', Float, default=0.0)
    ev = Column('fld_ev', Float, default=0.0)
    ew = Column('fld_ew', Float, default=0.0)
    f = Column('fld_f', Float, default=0.0)
    ft1 = Column('fld_ft1', Float, default=0.0)
    ft2 = Column('fld_ft2', Float, default=0.0)
    hloc = Column('fld_hloc', Integer, default=0)
    labor_hours_dev = Column('fld_hours_dev', Float, default=0.0)
    labor_hours_test = Column('fld_hours_test', Float, default=0.0)
    level = Column('fld_level', Integer, default=0)
    loc = Column('fld_loc', Integer, default=0)
    n_branches = Column('fld_n_branches', Integer, default=0)
    n_branches_test = Column('fld_n_branches_test', Integer, default=0)
    n_inputs = Column('fld_n_inputs', Integer, default=0)
    n_inputs_test = Column('fld_n_inputs_test', Integer, default=0)
    n_interfaces = Column('fld_n_interfaces', Integer, default=0)
    n_interfaces_test = Column('fld_n_interfaces_test', Integer, default=0)
    ncb = Column('fld_ncb', Integer, default=0)
    nm = Column('fld_nm', Integer, default=0)
    nm_test = Column('fld_nm_test', Integer, default=0)
    os = Column('fld_os', Float, default=0.0)
    parent_id = Column('fld_parent_id', Integer, default=0)
    phase_id = Column('fld_phase_id', Integer, default=0)
    ren_avg = Column('fld_ren_avg', Float, default=0.0)
    ren_eot = Column('fld_ren_eot', Float, default=0.0)
    rpfom = Column('fld_rpfom', Float, default=0.0)
    s1 = Column('fld_s1', Float, default=0.0)
    s2 = Column('fld_s2', Float, default=0.0)
    sa = Column('fld_sa', Float, default=0.0)
    schedule_dev = Column('fld_schedule_dev', Float, default=0.0)
    schedule_test = Column('fld_schedule_test', Float, default=0.0)
    sl = Column('fld_sl', Float, default=0.0)
    sm = Column('fld_sm', Float, default=0.0)
    sq = Column('fld_sq', Float, default=0.0)
    sr = Column('fld_sr', Float, default=0.0)
    st = Column('fld_st', Float, default=0.0)
    sx = Column('fld_sx', Float, default=0.0)
    t = Column('fld_t', Float, default=0.0)
    tc = Column('fld_tc', Float, default=0.0)
    tcl = Column('fld_tcl', Integer, default=0)
    te = Column('fld_te', Float, default=0.0)
    test_approach = Column('fld_test_approach', Integer, default=0)
    test_effort = Column('fld_test_effort', Integer, default=0)
    test_path = Column('fld_test_path', Integer, default=0)
    test_time = Column('fld_test_time', Float, default=0.0)
    test_time_eot = Column('fld_test_time_eot', Float, default=0.0)
    tm = Column('fld_tm', Float, default=0.0)
    um = Column('fld_um', Integer, default=0)
    wm = Column('fld_wm', Integer, default=0)
    xm = Column('fld_xm', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='software')
    development = relationship('RTKSoftwareDevelopment',
                               back_populates='software')
    srr_ssr = relationship('RTKSRRSSR', back_populates='software')
    pdr = relationship('RTKPDR', back_populates='software')
    cdr = relationship('RTKCDR', back_populates='software')
    trr = relationship('RTKTRR', back_populates='software')
    software_test = relationship('RTKSoftwareTest', back_populates='software')


class RTKSoftwareDevelopment(Base):
    """
    Class to represent the table rtk_software_development in the RTK Program
    database.
    
    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_software_development'

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    question_id = Column('fld_question_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    answer = Column('fld_answer', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='development')


class RTKSRRSSR(Base):
    """
    Class to represent the table rtk_srr_ssr in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_srr_ssr'

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    question_id = Column('fld_question_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    answer = Column('fld_answer', Integer, default=0)
    value = Column('fld_value', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='srr_ssr')


class RTKPDR(Base):
    """
    Class to represent the table rtk_pdr in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_pdr'

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    question_id = Column('fld_question_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    answer = Column('fld_answer', Integer, default=0)
    value = Column('fld_value', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='pdr')


class RTKCDR(Base):
    """
    Class to represent the table rtk_cdr in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_cdr'

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    question_id = Column('fld_question_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    answer = Column('fld_answer', Integer, default=0)
    value = Column('fld_value', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='cdr')


class RTKTRR(Base):
    """
    Class to represent the table rtk_trr in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_trr'

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    question_id = Column('fld_question_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)
    answer = Column('fld_answer', Integer, default=0)
    value = Column('fld_value', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='trr')


class RTKSoftwareTest(Base):
    """
    Class to represent the table rtk_software_test in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_software.
    """

    __tablename__ = 'rtk_software_test'

    software_id = Column('fld_software_id', Integer,
                         ForeignKey('rtk_software.fld_software_id'),
                         nullable=False)
    technique_id = Column('fld_technique_id', Integer, primary_key=True,
                          autoincrement=True, nullable=False)

    recommended = Column('fld_recommended', Integer, default=0)
    used = Column('fld_used', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    software = relationship('RTKSoftware', back_populates='software_test')


class RTKValidation(Base):
    """
    Class to represent the table rtk_validation in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    """

    __tablename__ = 'rtk_validation'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    validation_id = Column('fld_validation_id', Integer, primary_key=True,
                           autoincrement=True, nullable=False)

    acceptable_maximum = Column('fld_acceptable_maximum', Float, default=0.0)
    acceptable_mean = Column('fld_acceptable_mean', Float, default=0.0)
    acceptable_minimum = Column('fld_acceptable_minimum', Float, default=0.0)
    acceptable_variance = Column('fld_acceptable_variance', Float, default=0.0)
    confidence = Column('fld_confidence', Float, default=95.0)
    cost_average = Column('fld_cost_average', Float, default=0.0)
    cost_maximum = Column('fld_cost_maximum', Float, default=0.0)
    cost_mean = Column('fld_cost_mean', Float, default=0.0)
    cost_minimum = Column('fld_cost_minimum', Float, default=0.0)
    cost_variance = Column('fld_cost_variance', Float, default=0.0)
    date_end = Column('fld_date_end', Date,
                      default=date.today() + timedelta(days=30))
    date_start = Column('fld_date_start', Date, default=date.today())
    description = Column('fld_description', BLOB, default='')
    measurement_unit_id = Column('fld_measurement_unit_id', Integer, default=0)
    status_id = Column('fld_status', Float, default=0.0)
    task_type_id = Column('fld_type_id', Integer, default=0)
    task_specification = Column('fld_task_specification', String(512),
                                default='')
    time_average = Column('fld_time_average', Float, default=0.0)
    time_maximum = Column('fld_time_maximum', Float, default=0.0)
    time_mean = Column('fld_time_mean', Float, default=0.0)
    time_minimum = Column('fld_time_minimum', Float, default=0.0)
    time_variance = Column('fld_time_variance', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='validation')


class RTKIncident(Base):
    """
    Class to represent the table rtk_validation in the RTK Program datanase.
    
    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-One relationship with rtk_incident_detail.
    This table shares a One-to-Many relationship with rtk_incident_action.
    """

    __tablename__ = 'rtk_incident'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    incident_id = Column('fld_incident_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

    accepted = Column('fld_accepted', Integer, default=0)
    approved = Column('fld_approved', Integer, default=0)
    approved_by = Column('fld_approved_by', Integer, default=0)
    analysis = Column('fld_analysis', BLOB, default='')
    category_id = Column('fld_category_id', Integer, default=0)
    chargeable = Column('fld_chargeable', Integer, default=-1)
    chargeable_1 = Column('fld_chargeable_1', Integer, default=-1)
    chargeable_2 = Column('fld_chargeable_2', Integer, default=-1)
    chargeable_3 = Column('fld_chargeable_3', Integer, default=-1)
    chargeable_4 = Column('fld_chargeable_4', Integer, default=-1)
    chargeable_5 = Column('fld_chargeable_5', Integer, default=-1)
    chargeable_6 = Column('fld_chargeable_6', Integer, default=-1)
    chargeable_7 = Column('fld_chargeable_7', Integer, default=-1)
    chargeable_8 = Column('fld_chargeable_8', Integer, default=-1)
    chargeable_9 = Column('fld_chargeable_9', Integer, default=-1)
    chargeable_10 = Column('fld_chargeable_10', Integer, default=-1)
    complete = Column('fld_complete', Integer, default=0)
    complete_by = Column('fld_complete_by', Integer, default=0)
    cost = Column('fld_cost', Float, default=0)
    criticality_id = Column('fld_criticality_id', Integer, default=0)
    date_approved = Column('fld_date_approved', Date,
                           default=date.today() + timedelta(days=30))
    date_complete = Column('fld_date_complete', Date,
                           default=date.today() + timedelta(days=30))
    date_requested = Column('fld_date_requested', Date, default=date.today())
    date_reviewed = Column('fld_date_reviewed', Date,
                           default=date.today() + timedelta(days=30))
    description_long = Column('fld_description_long', BLOB, default='')
    description_short = Column('fld_description_short', String(512),
                               default='')
    detection_method_id = Column('fld_detection_method_id', Integer, default=0)
    execution_time = Column('fld_execution_time', Float, default=0)
    hardware_id = Column('fld_hardware_id', Integer, default=0)
    incident_age = Column('fld_incident_age', Integer, default=0)
    life_cycle_id = Column('fld_life_cycle_id', Integer, default=0)
    relevant = Column('fld_relevant', Integer, default=-1)
    relevant_1 = Column('fld_relevant_1', Integer, default=-1)
    relevant_2 = Column('fld_relevant_2', Integer, default=-1)
    relevant_3 = Column('fld_relevant_3', Integer, default=-1)
    relevant_4 = Column('fld_relevant_4', Integer, default=-1)
    relevant_5 = Column('fld_relevant_5', Integer, default=-1)
    relevant_6 = Column('fld_relevant_6', Integer, default=-1)
    relevant_7 = Column('fld_relevant_7', Integer, default=-1)
    relevant_8 = Column('fld_relevant_8', Integer, default=-1)
    relevant_9 = Column('fld_relevant_9', Integer, default=-1)
    relevant_10 = Column('fld_relevant_10', Integer, default=-1)
    relevant_11 = Column('fld_relevant_11', Integer, default=-1)
    relevant_12 = Column('fld_relevant_12', Integer, default=-1)
    relevant_13 = Column('fld_relevant_13', Integer, default=-1)
    relevant_14 = Column('fld_relevant_14', Integer, default=-1)
    relevant_15 = Column('fld_relevant_15', Integer, default=-1)
    relevant_16 = Column('fld_relevant_16', Integer, default=-1)
    relevant_17 = Column('fld_relevant_17', Integer, default=-1)
    relevant_18 = Column('fld_relevant_18', Integer, default=-1)
    relevant_19 = Column('fld_relevant_19', Integer, default=-1)
    relevant_20 = Column('fld_relevant_20', Integer, default=-1)
    remarks = Column('fld_remarks', BLOB, default='')
    request_by = Column('fld_request_by', Integer, default=0)
    reviewed = Column('fld_reviewed', Integer, default=0)
    reviewed_by = Column('fld_reviewed_by', Integer, default=0)
    software_id = Column('fld_software_id', Integer, default=0)
    status_id = Column('fld_status', Integer, default=0)
    test_case = Column('fld_test_case', String(512), default='')
    test_found = Column('fld_test_found', String(512), default='')
    type_id = Column('fld_type_id', Integer, default=0)
    unit = Column('fld_unit', String(256), default='')

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='incident')
    incident_detail = relationship('RTKIncidentDetail',
                                   back_populates='incident')
    incident_action = relationship('RTKIncidentAction',
                                   back_populates='incident')


class RTKIncidentDetail(Base):
    """
    Class to represent the table rtk_incident_detail in the RTK Program 
    database.
    
    This table shares a One-to-One relationship with rtk_incident.
    """

    __tablename__ = 'rtk_incident_detail'

    incident_id = Column('fld_incident_id', Integer,
                         ForeignKey('rtk_incident.fld_incident_id'),
                         primary_key=True, nullable=False)
    hardware_id = Column('fld_hardware_id', Integer, default=0)

    fld_age_at_incident = Column('fld_age_at_incident', Integer, default=0)
    fld_failure = Column('fld_failure', Integer, default=0)
    fld_suspension = Column('fld_suspension', Integer, default=0)
    fld_cnd_nff = Column('fld_cnd_nff', Integer, default=0)
    fld_occ_fault = Column('fld_occ_fault', Integer, default=0)
    fld_initial_installation = Column('fld_initial_installation', Integer,
                                      default=0)
    fld_interval_censored = Column('fld_interval_censored', Integer, default=0)
    fld_use_op_time = Column('fld_use_op_time', Integer, default=0)
    fld_use_cal_time = Column('fld_use_cal_time', Integer, default=0)
    fld_ttf = Column('fld_ttf', Float, default=0.0)
    fld_mode_type_id = Column('fld_mode_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    incident = relationship('RTKIncident', back_populates='incident_detail')


class RTKIncidentAction(Base):
    """
    Class to represent the table rtk_incident_action in the RTK Program
    database.
    
    This table shares a Many-to-One relationship with rtk_incident.
    """

    __tablename__ = 'rtk_incident_action'

    incident_id = Column('fld_incident_id', Integer,
                         ForeignKey('rtk_incident.fld_incident_id'),
                         nullable=False)
    action_id = Column('fld_action_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    action_owner = Column('fld_action_owner', Integer, default=0)
    action_prescribed = Column('fld_action_prescribed', BLOB, default='')
    action_taken = Column('fld_action_taken', BLOB, default='')
    approved = Column('fld_approved', Integer, default=0)
    approved_by = Column('fld_approved_by', Integer, default=0)
    approved_date = Column('fld_approved_date', Date,
                           default=date.today() + timedelta(days=30))
    closed = Column('fld_closed', Integer, default=0)
    closed_by = Column('fld_closed_by', Integer, default=0)
    closed_date = Column('fld_closed_date', Date,
                         default=date.today() + timedelta(days=30))
    due_date = Column('fld_due_date', Date,
                      default=date.today() + timedelta(days=30))
    status_id = Column('fld_status_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    incident = relationship('RTKIncident', back_populates='incident_action')


class RTKTest(Base):
    """
    Class to represent the table rtk_test in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relationship with rtk_growth_test.
    """

    __tablename__ = 'rtk_test'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    test_id = Column('fld_test_id', Integer, primary_key=True,
                     autoincrement=True, nullable=False)

    assess_model_id = Column('fld_assess_model_id', Integer, default=0)
    attachment = Column('fld_attachment', String(512), default='')
    avg_fef = Column('fld_avg_fef', Float, default=0.0)
    avg_growth = Column('fld_avg_growth', Float, default=0.0)
    avg_ms = Column('fld_avg_ms', Float, default=0.0)
    chi_square = Column('fld_chi_square', Float, default=0.0)
    confidence = Column('fld_confidence', Float, default=0.0)
    consumer_risk = Column('fld_consumer_risk', Float, default=0.0)
    cramer_vonmises = Column('fld_cramer_vonmises', Float, default=0.0)
    cum_failures = Column('fld_cum_failures', Integer, default=0)
    cum_mean = Column('fld_cum_mean', Float, default=0.0)
    cum_mean_ll = Column('fld_cum_mean_ll', Float, default=0.0)
    cum_mean_se = Column('fld_cum_mean_se', Float, default=0.0)
    cum_mean_ul = Column('fld_cum_mean_ul', Float, default=0.0)
    cum_time = Column('fld_cum_time', Float, default=0.0)
    description = Column('fld_description', BLOB, default='')
    grouped = Column('fld_grouped', Integer, default=0)
    group_interval = Column('fld_group_interval', Float, default=0.0)
    inst_mean = Column('fld_inst_mean', Float, default=0.0)
    inst_mean_ll = Column('fld_inst_mean_ll', Float, default=0.0)
    inst_mean_se = Column('fld_inst_mean_se', Float, default=0.0)
    inst_mean_ul = Column('fld_inst_mean_ul', Float, default=0.0)
    mg = Column('fld_mg', Float, default=0.0)
    mgp = Column('fld_mgp', Float, default=0.0)
    n_phases = Column('fld_n_phases', Integer, default=1)
    name = Column('fld_name', String(512), default='')
    plan_model_id = Column('fld_plan_model_id', Integer, default=0)
    prob = Column('fld_prob', Float, default=75.0)
    producer_risk = Column('fld_producer_risk', Float, default=0.0)
    scale = Column('fld_scale', Float, default=0.0)
    scale_ll = Column('fld_scale_ll', Float, default=0.0)
    scale_se = Column('fld_scale_se', Float, default=0.0)
    scale_ul = Column('fld_scale_ul', Float, default=0.0)
    shape = Column('fld_shape', Float, default=0.0)
    shape_ll = Column('fld_shape_ll', Float, default=0.0)
    shape_se = Column('fld_shape_se', Float, default=0.0)
    shape_ul = Column('fld_shape_ul', Float, default=0.0)
    tr = Column('fld_tr', Float, default=0.0)
    ttt = Column('fld_ttt', Float, default=0.0)
    ttff = Column('fld_ttff', Float, default=0.0)
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='test')
    growth = relationship('RTKGrowthTest', back_populates='test')


class RTKGrowthTest(Base):
    """
    Class to represent the table rtk_growth_test in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_test.
    """

    __tablename__ = 'rtk_growth_test'

    test_id = Column('fld_test_id', Integer,
                     ForeignKey('rtk_test.fld_test_id'), nullable=False)
    phase_id = Column('fld_phase_id', Integer, primary_key=True,
                      autoincrement=True, nullable=False)

    i_mi = Column('fld_i_mi', Float, default=0.0)
    i_mf = Column('fld_i_mf', Float, default=0.0)
    i_ma = Column('fld_i_ma', Float, default=0.0)
    i_num_fails = Column('fld_i_num_fails', Integer, default=0)
    p_growth_rate = Column('fld_p_growth_rate', Float, default=0.0)
    p_ms = Column('fld_p_ms', Float, default=0.0)
    p_fef_avg = Column('fld_p_fef_avg', Float, default=0.0)
    p_prob = Column('fld_p_prob', Float, default=0.0)
    p_mi = Column('fld_p_mi', Float, default=0.0)
    p_mf = Column('fld_p_mf', Float, default=0.0)
    p_ma = Column('fld_p_ma', Float, default=0.0)
    p_test_time = Column('fld_test_time', Float, default=0.0)
    p_num_fails = Column('fld_p_num_fails', Integer, default=0)
    p_start_date = Column('fld_p_start_date', Date, default=date.today())
    p_end_date = Column('fld_p_end_date', Date, default=date.today())
    p_weeks = Column('fld_p_weeks', Float, default=0.0)
    p_test_units = Column('fld_test_units', Integer, default=0)
    p_tpu = Column('fld_p_tpu', Float, default=0.0)
    p_tpupw = Column('fld_p_tpupw', Float, default=0.0)
    o_growth_rate = Column('fld_o_growth_rate', Float, default=0.0)
    o_ms = Column('fld_o_ms', Float, default=0.0)
    o_fef_avg = Column('fld_o_fef_avg', Float, default=0.0)
    o_mi = Column('fld_o_mi', Float, default=0.0)
    o_mf = Column('fld_o_mf', Float, default=0.0)
    o_ma = Column('fld_o_ma', Float, default=0.0)
    o_test_time = Column('fld_o_test_time', Float, default=0.0)
    o_num_fails = Column('fld_o_num_fails', Integer, default=0)
    o_ttff = Column('fld_o_ttff', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    test = relationship('RTKTest', back_populates='growth')


class RTKSurvival(Base):
    """
    Class to represent the table rtk_survival in the RTK Program database.
    
    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relatinship with rtk_survival_data.
    """

    __tablename__ = 'rtk_survival'

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    survival_id = Column('fld_survival_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

    hardware_id = Column('fld_hardware_id', Integer, default=0)

    description = Column('fld_description', String(512), default='')
    source_id = Column('fld_source_id', Integer, default=0)
    distribution_id = Column('fld_distribution_id', Integer, default=0)
    confidence = Column('fld_confidence', Float, default=75.0)
    confidence_type_id = Column('fld_confidence_type_id', Integer, default=0)
    confidence_method_id = Column('fld_confidence_method_id', Integer,
                                  default=0)
    fit_method_id = Column('fld_fit_method_id', Integer, default=0)
    rel_time = Column('fld_rel_time', Float, default=0.0)
    n_rel_points = Column('fld_n_rel_points', Integer, default=0)
    n_suspension = Column('fld_n_suspensions', Integer, default=0)
    n_failures = Column('fld_n_failures', Integer, default=0)
    scale_ll = Column('fld_scale_ll', Float, default=0.0)
    scale = Column('fld_scale', Float, default=0.0)
    scale_ul = Column('fld_scale_ul', Float, default=0.0)
    shape_ll = Column('fld_shape_ll', Float, default=0.0)
    shape = Column('fld_shape', Float, default=0.0)
    shape_ul = Column('fld_shape_ul', Float, default=0.0)
    location_ll = Column('fld_location_ll', Float, default=0.0)
    location = Column('fld_location', Float, default=0.0)
    location_ul = Column('fld_location_ul', Float, default=0.0)
    variance_1 = Column('fld_variance_1', Float, default=0.0)
    variance_2 = Column('fld_variance_2', Float, default=0.0)
    variance_3 = Column('fld_variance_3', Float, default=0.0)
    covariance_1 = Column('fld_covariance_1', Float, default=0.0)
    covariance_2 = Column('fld_covariance_2', Float, default=0.0)
    covariance_3 = Column('fld_covariance_3', Float, default=0.0)
    mhb = Column('fld_mhb', Float, default=0.0)
    lp = Column('fld_lp', Float, default=0.0)
    lr = Column('fld_lr', Float, default=0.0)
    aic = Column('fld_aic', Float, default=0.0)
    bic = Column('fld_bic', Float, default=0.0)
    mle = Column('fld_mle', Float, default=0.0)
    start_time = Column('fld_start_time', Float, default=0.0)
    start_date = Column('fld_start_date', Date, default=date.today())
    end_date = Column('fld_end_date', Date,
                      default=date.today() + timedelta(days=30))
    nevada_chart = Column('fld_nevada_chart', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='survival')
    data = relationship('RTKSurvivalData', back_populates='survival')


class RTKSurvivalData(Base):
    """
    Class to represent the table rtk_survival_data in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_survival.
    """

    __tablename__ = 'rtk_survival_data'

    survival_id = Column('fld_survival_id', Integer,
                         ForeignKey('rtk_survival.fld_survival_id'),
                         nullable=False)
    record_id = Column('fld_record_id', Integer, primary_key=True,
                       autoincrement=True, nullable=False)

    name = Column('fld_name', String(512), default='')
    source_id = Column('fld_source_id', Integer, default=0)
    failure_date = Column('fld_failure_date', Date, default=date.today())
    left_interval = Column('fld_left_interval', Float, default=0.0)
    right_interval = Column('fld_right_interval', Float, default=0.0)
    status_id = Column('fld_status_id', Integer, default=0)
    quantity = Column('fld_quantity', Integer, default=0)
    tbf = Column('fld_tbf', Float, default=0.0)
    mode_type_id = Column('fld_mode_type_id', Integer, default=0)
    nevada_chart = Column('fld_nevada_chart', Integer, default=0)
    ship_date = Column('fld_ship_date', Date, default=date.today())
    number_shipped = Column('fld_number_shipped', Integer, default=0)
    return_date = Column('fld_return_date', Date, default=date.today())
    number_returned = Column('fld_number_returned', Integer, default=0)
    user_float_1 = Column('fld_user_float_1', Float, default=0.0)
    user_float_2 = Column('fld_user_float_2', Float, default=0.0)
    user_float_3 = Column('fld_user_float_3', Float, default=0.0)
    user_integer_1 = Column('fld_user_integer_1', Integer, default=0)
    user_integer_2 = Column('fld_user_integer_2', Integer, default=0)
    user_integer_3 = Column('fld_user_integer_3', Integer, default=0)
    user_string_1 = Column('fld_user_string_1', String(512), default='')
    user_string_2 = Column('fld_user_string_2', String(512), default='')
    user_string_3 = Column('fld_user_string_3', String(512), default='')

    # Define the relationships to other tables in the RTK Program database.
    survival = relationship('RTKSurvival', back_populates='data')
