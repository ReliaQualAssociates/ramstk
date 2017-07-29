#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKHazardAnalysis.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKHazardAnalysis Table
==============================
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
    from dao.RTKCommonDB import RTK_BASE
except ImportError:
    from rtk.dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKHazardAnalysis(RTK_BASE):
    """
    Class to represent the rtk_hazard_analysis table in the RTK Program
    database.

    This table shares a Many-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_hazard_analysis'
    __table_args__ = {'extend_existing': True}

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
    assembly_hri_f = Column('fld_assembly_hri_f', Integer, default=4)
    system_effect = Column('fld_system_effect', String(512), default='')
    system_severity_id = Column('fld_system_severity', Integer, default=4)
    system_probability_id = Column('fld_system_probability', Integer,
                                   default=5)
    system_hri = Column('fld_system_hri', Integer, default=20)
    system_mitigation = Column('fld_system_mitigation', BLOB, default='')
    system_severity_id_f = Column('fld_system_severity_f', Integer, default=4)
    system_probability_id_f = Column('fld_system_probability_f', Integer,
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
    user_float_1 = Column('fld_user_float_1', Float, default=0.0)
    user_float_2 = Column('fld_user_float_2', Float, default=0.0)
    user_float_3 = Column('fld_user_float_3', Float, default=0.0)
    user_int_1 = Column('fld_user_int_1', Integer, default=0)
    user_int_2 = Column('fld_user_int_2', Integer, default=0)
    user_int_3 = Column('fld_user_int_3', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='hazard')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKHazardAnalysis data
        model attributes.

        :return: (hardware_id, hazard_id, potential_hazard, potential_cause,
                  assembly_effect, assembly_severity_id,
                  assembly_probability_id, assembly_hri, assembly_mitigation,
                  assembly_severity_id_f, assembly_probability_id_f,
                  assembly_hri_f, system_effect, system_severity_id,
                  system_probability_id, system_hri, system_mitigation,
                  system_severity_id_f, system_probability_id_f,
                  system_hri_f, remarks, function_1, function_2, function_3,
                  function_4, function_5, result_1, result_2, result_3,
                  result_4, result_5, user_blob_1, user_blob_2, user_blob_3,
                  user_float_1, user_float_2, user_float_3, user_int_1,
                  user_int_2, user_int_3)
        :rtype: tuple
        """

        _attributes = (self.hardware_id, self.hazard_id, self.potential_hazard,
                       self.potential_cause, self.assembly_effect,
                       self.assembly_severity_id, self.assembly_probability_id,
                       self.assembly_hri, self.assembly_mitigation,
                       self.assembly_severity_id_f,
                       self.assembly_probability_id_f, self.assembly_hri_f,
                       self.system_effect, self.system_severity_id,
                       self.system_probability_id, self.system_hri,
                       self.system_mitigation, self.system_severity_id_f,
                       self.system_probability_id_f, self.system_hri_f,
                       self.remarks, self.function_1, self.function_2,
                       self.function_3, self.function_4, self.function_5,
                       self.result_1, self.result_2, self.result_3,
                       self.result_4, self.result_5, self.user_blob_1,
                       self.user_blob_2, self.user_blob_3, self.user_float_1,
                       self.user_float_2, self.user_float_3, self.user_int_1,
                       self.user_int_2, self.user_int_3)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKHazardAnalysis data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKHazardAnalysis {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.potential_hazard = str(attributes[0])
            self.potential_cause = str(attributes[1])
            self.assembly_effect = str(attributes[2])
            self.assembly_severity_id = int(attributes[3])
            self.assembly_probability_id = int(attributes[4])
            self.assembly_hri = int(attributes[5])
            self.assembly_mitigation = str(attributes[6])
            self.assembly_severity_id_f = int(attributes[7])
            self.assembly_probability_id_f = int(attributes[8])
            self.assembly_hri_f = int(attributes[9])
            self.system_effect = str(attributes[10])
            self.system_severity_id = int(attributes[11])
            self.system_probability_id = int(attributes[12])
            self.system_hri = int(attributes[13])
            self.system_mitigation = str(attributes[14])
            self.system_severity_id_f = int(attributes[15])
            self.system_probability_id_f = int(attributes[16])
            self.system_hri_f = int(attributes[17])
            self.remarks = str(attributes[18])
            self.function_1 = str(attributes[19])
            self.function_2 = str(attributes[20])
            self.function_3 = str(attributes[21])
            self.function_4 = str(attributes[22])
            self.function_5 = str(attributes[23])
            self.result_1 = float(attributes[24])
            self.result_2 = float(attributes[25])
            self.result_3 = float(attributes[26])
            self.result_4 = float(attributes[27])
            self.result_5 = float(attributes[28])
            self.user_blob_1 = str(attributes[29])
            self.user_blob_2 = str(attributes[30])
            self.user_blob_3 = str(attributes[31])
            self.user_float_1 = float(attributes[32])
            self.user_float_2 = float(attributes[33])
            self.user_float_3 = float(attributes[34])
            self.user_int_1 = int(attributes[35])
            self.user_int_2 = int(attributes[36])
            self.user_int_3 = int(attributes[37])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKHazardAnalysis.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKHazardAnalysis attributes."

        return _error_code, _msg
