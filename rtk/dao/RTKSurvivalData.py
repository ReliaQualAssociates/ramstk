# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSurvivalData.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKSurvivalData Table
===============================================================================
"""

from datetime import date

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  

# Import other RTK modules.
from rtk.Utilities import error_handler, none_to_default  
from rtk.dao.RTKCommonDB import RTK_BASE  


class RTKSurvivalData(RTK_BASE):
    """
    Class to represent the table rtk_survival_data in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_survival.
    """

    __tablename__ = 'rtk_survival_data'
    __table_args__ = {'extend_existing': True}

    survival_id = Column(
        'fld_survival_id',
        Integer,
        ForeignKey('rtk_survival.fld_survival_id'),
        nullable=False)
    record_id = Column(
        'fld_record_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

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
            self.name = str(none_to_default(attributes[0], ''))
            self.source_id = int(none_to_default(attributes[1], 0))
            self.failure_date = none_to_default(attributes[2], date.today())
            self.left_interval = float(none_to_default(attributes[3], 0.0))
            self.right_interval = float(none_to_default(attributes[4], 0.0))
            self.status_id = int(none_to_default(attributes[5], 0))
            self.quantity = int(none_to_default(attributes[6], 0))
            self.tbf = float(none_to_default(attributes[7], 0.0))
            self.mode_type_id = int(none_to_default(attributes[8], 0))
            self.nevada_chart = int(none_to_default(attributes[9], 0))
            self.ship_date = none_to_default(attributes[10], date.today())
            self.number_shipped = int(none_to_default(attributes[11], 0))
            self.return_date = none_to_default(attributes[12], date.today())
            self.number_returned = int(none_to_default(attributes[13], 0))
            self.user_float_1 = float(none_to_default(attributes[14], 0.0))
            self.user_float_2 = float(none_to_default(attributes[15], 0.0))
            self.user_float_3 = float(none_to_default(attributes[16], 0.0))
            self.user_integer_1 = int(none_to_default(attributes[17], 0))
            self.user_integer_2 = int(none_to_default(attributes[18], 0))
            self.user_integer_3 = int(none_to_default(attributes[19], 0))
            self.user_string_1 = str(none_to_default(attributes[20], ''))
            self.user_string_2 = str(none_to_default(attributes[21], ''))
            self.user_string_3 = str(none_to_default(attributes[22], ''))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSurvivalData.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSurvivalData attributes."

        return _error_code, _msg
