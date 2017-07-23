#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSurvivalData.py is part of The RTK Project
#
# All rights reserved.

"""
The RTKSurvivalData Package.
"""

from datetime import date

# Import the database models.
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
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


class RTKSurvivalData(Base):
    """
    Class to represent the table rtk_survival_data in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_survival.
    """

    __tablename__ = 'rtk_survival_data'
    __table_args__ = {'extend_existing': True}

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

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSurvivalData data model
        attributes.

        :return: (survival_id, record_id, name, source_id, failure_date,
                  left_interval, right_interval, status_id, quantity, tbf,
                  mode_type_id, nevada_chart, ship_date, number_shipped,
                  return_date, number_returned, user_float_1, user_float_2,
                  user_float_3, user_integer_1, user_integer_2, user_integer_3,
                  user_string_1, user_string_2, user_string_3)
        :rtype: tuple
        """

        _attributes = (self.survival_id, self.record_id, self.name,
                       self.source_id, self.failure_date, self.left_interval,
                       self.right_interval, self.status_id, self.quantity,
                       self.tbf, self.mode_type_id, self.nevada_chart,
                       self.ship_date, self.number_shipped, self.return_date,
                       self.number_returned, self.user_float_1,
                       self.user_float_2, self.user_float_3,
                       self.user_integer_1, self.user_integer_2,
                       self.user_integer_3, self.user_string_1,
                       self.user_string_2, self.user_string_3)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKSurvivalData data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSurvivalData {0:d} attributes.". \
               format(self.record_id)

        try:
            self.name = str(attributes[0])
            self.source_id = int(attributes[1])
            self.failure_date = attributes[2]
            self.left_interval = float(attributes[3])
            self.right_interval = float(attributes[4])
            self.status_id = int(attributes[5])
            self.quantity = int(attributes[6])
            self.tbf = float(attributes[7])
            self.mode_type_id = int(attributes[8])
            self.nevada_chart = int(attributes[9])
            self.ship_date = attributes[10]
            self.number_shipped = int(attributes[11])
            self.return_date = attributes[12]
            self.number_returned = int(attributes[13])
            self.user_float_1 = float(attributes[14])
            self.user_float_2 = float(attributes[15])
            self.user_float_3 = float(attributes[16])
            self.user_integer_1 = int(attributes[17])
            self.user_integer_2 = int(attributes[18])
            self.user_integer_3 = int(attributes[19])
            self.user_string_1 = str(attributes[20])
            self.user_string_2 = str(attributes[21])
            self.user_string_3 = str(attributes[22])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSurvivalData.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSurvivalData attributes."

        return _error_code, _msg
