#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKFunction.py is part of The RTK Project
#
# All rights reserved.

"""
===============================================================================
The RTKFunction Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
try:
    from Utilities import error_handler, none_to_default
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.Utilities import error_handler, none_to_default
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKFunction(RTK_BASE):
    """
    Class to represent the rtk_function table in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relationship with rtk_mode.
    """

    __tablename__ = 'rtk_function'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    function_id = Column('fld_function_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

    availability_logistics = Column('fld_availability_logistics', Float,
                                    default=1.0)
    availability_mission = Column('fld_availability_mission', Float,
                                  default=1.0)
    cost = Column('fld_cost', Float, default=0.0)
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
            self.availability_logistics = float(none_to_default(values[0],
                                                                1.0))
            self.availability_mission = float(none_to_default(values[1], 1.0))
            self.cost = float(none_to_default(values[2], 0.0))
            self.function_code = str(none_to_default(values[3],
                                                     'Function Code'))
            self.hazard_rate_logistics = float(none_to_default(values[4], 0.0))
            self.hazard_rate_mission = float(none_to_default(values[5], 0.0))
            self.level = int(none_to_default(values[6], 0.0))
            self.mmt = float(none_to_default(values[7], 0.0))
            self.mcmt = float(none_to_default(values[8], 0.0))
            self.mpmt = float(none_to_default(values[9], 0.0))
            self.mtbf_logistics = float(none_to_default(values[10], 0.0))
            self.mtbf_mission = float(none_to_default(values[11], 0.0))
            self.mttr = float(none_to_default(values[12], 0.0))
            self.name = str(none_to_default(values[13], 'Function Name'))
            self.parent_id = int(none_to_default(values[14], 0))
            self.remarks = str(none_to_default(values[15], ''))
            self.safety_critical = int(none_to_default(values[16], 0))
            self.total_mode_count = int(none_to_default(values[17], 0))
            self.total_part_count = int(none_to_default(values[18], 0))
            self.type_id = int(none_to_default(values[19], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKFunction.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKFunction attributes."

        return _error_code, _msg
