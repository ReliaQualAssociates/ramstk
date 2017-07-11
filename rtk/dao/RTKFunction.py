#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKFunction.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKFunction Package.
"""

# Import the database models.
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
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
    name = Column('fld_name', String(256), default='Function Name')
    parent_id = Column('fld_parent_id', Integer, default=0)
    remarks = Column('fld_remarks', BLOB, default='')
    safety_critical = Column('fld_safety_critical', Integer, default=0)
    total_mode_count = Column('fld_mode_count', Integer, default=0)
    total_part_count = Column('fld_part_count', Integer, default=0)
    type_id = Column('fld_type_id', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='function')
    mode = relationship('RTKMode', back_populates='function')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKFunction data model
        attributes.

        :return: (revision_id, function_id, availability_logistics,
                  availability_mission, cost, function_code,
                  hazard_rate_logistics, hazard_rate_mission, level, mmt, mcmt,
                  mpmt, mtbf_logistics, mtbf_mission, mttr, name, parent_id,
                  remarks, safety_critical, total_mode_count, total_part_count,
                  type_id)
        :rtype: tuple
        """

        _values = (self.revision_id, self.function_id,
                   self.availability_logistics, self.availability_mission,
                   self.cost, self.function_code, self.hazard_rate_logistics,
                   self.hazard_rate_mission, self.level, self.mmt,
                   self.mcmt, self.mpmt, self.mtbf_logistics,
                   self.mtbf_mission, self.mttr, self.name, self.parent_id,
                   self.remarks, self.safety_critical, self.total_mode_count,
                   self.total_part_count, self.type_id)

        return _values

    def set_attributes(self, values):
        """
        Method to set the RTKFunction data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKFunction {0:d} attributes.". \
               format(self.function_id)

        try:
            self.availability_logistics = float(values[0])
            self.availability_mission = float(values[1])
            self.cost = float(values[2])
            self.function_code = str(values[3])
            self.hazard_rate_logistics = float(values[4])
            self.hazard_rate_mission = float(values[5])
            self.level = int(values[6])
            self.mmt = float(values[7])
            self.mcmt = float(values[8])
            self.mpmt = float(values[9])
            self.mtbf_logistics = float(values[10])
            self.mtbf_mission = float(values[11])
            self.mttr = float(values[12])
            self.name = str(values[13])
            self.parent_id = int(values[14])
            self.remarks = str(values[15])
            self.safety_critical = int(values[16])
            self.total_mode_count = int(values[17])
            self.total_part_count = int(values[18])
            self.type_id = int(values[19])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKFunction.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKFunction attributes."

        return _error_code, _msg

    def calculate_reliability(self):
        """
        Method to calculate the logistics MTBF and mission MTBF.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # Calculate the logistics MTBF.
        try:
            self.mtbf_logistics = 1.0 / self.hazard_rate_logistics
        except(ZeroDivisionError, OverflowError):
            self.mtbf_logistics = 0.0
            _msg = "RTK ERROR: Zero Division or Overflow Error when " \
                   " calculating the logistics MTBF in RTKFunction.  " \
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
                   "calculating the mission MTBF in RTKFunction.  Mission " \
                   "hazard rate: {0:f}.".format(self.hazard_rate_logistics)
            Configuration.RTK_DEBUG_LOG.error(_msg)
            _return = True

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
