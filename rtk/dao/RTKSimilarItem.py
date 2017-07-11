#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSimilarItem.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKSimilarItem Package.
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

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSimilarItem data model
        attributes.

        :return: (hardware_id, change_description_1, change_description_2,
                  change_description_3, change_description_4,
                  change_description_5, change_description_6,
                  change_description_7, change_description_8,
                  change_description_9, change_description_10, change_factor_1,
                  change_factor_2, change_factor_3, change_factor_4,
                  change_factor_5, change_factor_6, change_factor_7,
                  change_factor_8, change_factor_9, change_factor_10,
                  environment_from_id, environment_to_id, function_1,
                  function_2, function_3, function_4, function_5, method_id,
                  parent_id, quality_from_id, quality_to_id, result_1,
                  result_2, result_3, result_4, result_5, temperature_from,
                  temperature_to, user_blob_1, user_blob_2, user_blob_3,
                  user_blob_4, user_blob_5, user_float_1, user_float_2,
                  user_float_3, user_float_4, user_float_5, user_int_1,
                  user_int_2, user_int_3, user_int_4, user_int_5)
        :rtype: tuple
        """

        _values = (self.hardware_id, self.change_description_1,
                   self.change_description_2, self.change_description_3,
                   self.change_description_4, self.change_description_5,
                   self.change_description_6, self.change_description_7,
                   self.change_description_8, self.change_description_9,
                   self.change_description_10, self.change_factor_1,
                   self.change_factor_2, self.change_factor_3,
                   self.change_factor_4, self.change_factor_5,
                   self.change_factor_6, self.change_factor_7,
                   self.change_factor_8, self.change_factor_9,
                   self.change_factor_10, self.environment_from_id,
                   self.environment_to_id, self.function_1, self.function_2,
                   self.function_3, self.function_4, self.function_5,
                   self.method_id, self.parent_id, self.quality_from_id,
                   self.quality_to_id, self.result_1, self.result_2,
                   self.result_3, self.result_4, self.result_5,
                   self.temperature_from, self.temperature_to,
                   self.user_blob_1, self.user_blob_2, self.user_blob_3,
                   self.user_blob_4, self.user_blob_5, self.user_float_1,
                   self.user_float_2, self.user_float_3, self.user_float_4,
                   self.user_float_5, self.user_int_1, self.user_int_2,
                   self.user_int_3, self.user_int_4, self.user_int_5)

        return _values

    def set_attributes(self, attributes):
        """
        Method to set the RTKSimilarItem data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSimilarItem {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.change_description_1 = str(attributes[0])
            self.change_description_2 = str(attributes[1])
            self.change_description_3 = str(attributes[2])
            self.change_description_4 = str(attributes[3])
            self.change_description_5 = str(attributes[4])
            self.change_description_6 = str(attributes[5])
            self.change_description_7 = str(attributes[6])
            self.change_description_8 = str(attributes[7])
            self.change_description_9 = str(attributes[8])
            self.change_description_10 = str(attributes[9])
            self.change_factor_1 = float(attributes[10])
            self.change_factor_2 = float(attributes[11])
            self.change_factor_3 = float(attributes[12])
            self.change_factor_4 = float(attributes[13])
            self.change_factor_5 = float(attributes[14])
            self.change_factor_6 = float(attributes[15])
            self.change_factor_7 = float(attributes[16])
            self.change_factor_8 = float(attributes[17])
            self.change_factor_9 = float(attributes[18])
            self.change_factor_10 = float(attributes[19])
            self.environment_from_id = int(attributes[20])
            self.environment_to_id = int(attributes[21])
            self.function_1 = str(attributes[22])
            self.function_2 = str(attributes[23])
            self.function_3 = str(attributes[24])
            self.function_4 = str(attributes[25])
            self.function_5 = str(attributes[26])
            self.method_id = int(attributes[27])
            self.parent_id = int(attributes[28])
            self.quality_from_id = int(attributes[29])
            self.quality_to_id = int(attributes[30])
            self.result_1 = float(attributes[31])
            self.result_2 = float(attributes[32])
            self.result_3 = float(attributes[33])
            self.result_4 = float(attributes[34])
            self.result_5 = float(attributes[35])
            self.temperature_from = float(attributes[36])
            self.temperature_to = float(attributes[37])
            self.user_blob_1 = str(attributes[38])
            self.user_blob_2 = str(attributes[39])
            self.user_blob_3 = str(attributes[40])
            self.user_blob_4 = str(attributes[41])
            self.user_blob_5 = str(attributes[42])
            self.user_float_1 = float(attributes[43])
            self.user_float_2 = float(attributes[44])
            self.user_float_3 = float(attributes[45])
            self.user_float_4 = float(attributes[46])
            self.user_float_5 = float(attributes[47])
            self.user_int_1 = int(attributes[48])
            self.user_int_2 = int(attributes[49])
            self.user_int_3 = int(attributes[50])
            self.user_int_4 = int(attributes[51])
            self.user_int_5 = int(attributes[52])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSimilarItem.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSimilarItem attributes."

        return _error_code, _msg
