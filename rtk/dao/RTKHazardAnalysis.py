# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKHazardAnalysis.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKHazardAnalysis Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


class RTKHazardAnalysis(RTK_BASE):
    """
    Class to represent the rtk_hazard_analysis table in the RTK Program
    database.

    This table shares a Many-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_hazard_analysis'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('rtk_hardware.fld_hardware_id'),
        nullable=False)
    hazard_id = Column(
        'fld_hazard_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

    potential_hazard = Column('fld_potential_hazard', String(256), default='')
    potential_cause = Column('fld_potential_cause', String(512), default='')
    assembly_effect = Column('fld_assembly_effect', String(512), default='')
    assembly_severity_id = Column('fld_assembly_severity', Integer, default=4)
    assembly_probability_id = Column(
        'fld_assembly_probability', Integer, default=5)
    assembly_hri = Column('fld_assembly_hri', Integer, default=20)
    assembly_mitigation = Column('fld_assembly_mitigation', BLOB, default='')
    assembly_severity_id_f = Column(
        'fld_assembly_severity_f', Integer, default=4)
    assembly_probability_id_f = Column(
        'fld_assembly_probability_f', Integer, default=5)
    assembly_hri_f = Column('fld_assembly_hri_f', Integer, default=4)
    system_effect = Column('fld_system_effect', String(512), default='')
    system_severity_id = Column('fld_system_severity', Integer, default=4)
    system_probability_id = Column(
        'fld_system_probability', Integer, default=5)
    system_hri = Column('fld_system_hri', Integer, default=20)
    system_mitigation = Column('fld_system_mitigation', BLOB, default='')
    system_severity_id_f = Column('fld_system_severity_f', Integer, default=4)
    system_probability_id_f = Column(
        'fld_system_probability_f', Integer, default=5)
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
            self.potential_hazard = str(none_to_default(attributes[0], ''))
            self.potential_cause = str(none_to_default(attributes[1], ''))
            self.assembly_effect = str(none_to_default(attributes[2], ''))
            self.assembly_severity_id = int(none_to_default(attributes[3], 0))
            self.assembly_probability_id = int(
                none_to_default(attributes[4], 0))
            self.assembly_hri = int(none_to_default(attributes[5], 0))
            self.assembly_mitigation = str(none_to_default(attributes[6], ''))
            self.assembly_severity_id_f = int(
                none_to_default(attributes[7], 0))
            self.assembly_probability_id_f = int(
                none_to_default(attributes[8], 0))
            self.assembly_hri_f = int(none_to_default(attributes[9], 0))
            self.system_effect = str(none_to_default(attributes[10], ''))
            self.system_severity_id = int(none_to_default(attributes[11], 0))
            self.system_probability_id = int(
                none_to_default(attributes[12], 0))
            self.system_hri = int(none_to_default(attributes[13], 0))
            self.system_mitigation = str(none_to_default(attributes[14], ''))
            self.system_severity_id_f = int(none_to_default(attributes[15], 0))
            self.system_probability_id_f = int(
                none_to_default(attributes[16], 0))
            self.system_hri_f = int(none_to_default(attributes[17], 0))
            self.remarks = str(none_to_default(attributes[18], ''))
            self.function_1 = str(none_to_default(attributes[19], ''))
            self.function_2 = str(none_to_default(attributes[20], ''))
            self.function_3 = str(none_to_default(attributes[21], ''))
            self.function_4 = str(none_to_default(attributes[22], ''))
            self.function_5 = str(none_to_default(attributes[23], ''))
            self.result_1 = float(none_to_default(attributes[24], 0.0))
            self.result_2 = float(none_to_default(attributes[25], 0.0))
            self.result_3 = float(none_to_default(attributes[26], 0.0))
            self.result_4 = float(none_to_default(attributes[27], 0.0))
            self.result_5 = float(none_to_default(attributes[28], 0.0))
            self.user_blob_1 = str(none_to_default(attributes[29], ''))
            self.user_blob_2 = str(none_to_default(attributes[30], ''))
            self.user_blob_3 = str(none_to_default(attributes[31], ''))
            self.user_float_1 = float(none_to_default(attributes[32], 0.0))
            self.user_float_2 = float(none_to_default(attributes[33], 0.0))
            self.user_float_3 = float(none_to_default(attributes[34], 0.0))
            self.user_int_1 = int(none_to_default(attributes[35], 0))
            self.user_int_2 = int(none_to_default(attributes[36], 0))
            self.user_int_3 = int(none_to_default(attributes[37], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKHazardAnalysis.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKHazardAnalysis attributes."

        return _error_code, _msg
