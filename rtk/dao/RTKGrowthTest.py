# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKGrowthTest.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKGrowthTest Table
===============================================================================
"""

from datetime import date
# pylint: disable=E0401
from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


class RTKGrowthTest(RTK_BASE):
    """
    Class to represent the table rtk_growth_test in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_test.
    """

    __tablename__ = 'rtk_growth_test'
    __table_args__ = {'extend_existing': True}

    test_id = Column(
        'fld_test_id',
        Integer,
        ForeignKey('rtk_test.fld_test_id'),
        nullable=False)
    phase_id = Column(
        'fld_phase_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

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

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKGrowthTest data model
        attributes.

        :return: (test_id, phase_id, i_mi, i_mf, i_ma, i_num_fails,
                  p_growth_rate, p_ms, p_fef_avg, p_prob, p_mi, p_mf, p_ma ,
                  p_test_time, p_num_fails, p_start_date, p_end_date, p_weeks,
                  p_test_units, p_tpu, p_tpupw, o_growth_rate, o_ms, o_fef_avg,
                  o_mi, o_mf, o_ma, o_test_time, o_num_fails, o_ttff)
        :rtype: tuple
        """

        _attributes = (self.test_id, self.phase_id, self.i_mi, self.i_mf,
                       self.i_ma, self.i_num_fails, self.p_growth_rate,
                       self.p_ms, self.p_fef_avg, self.p_prob, self.p_mi,
                       self.p_mf, self.p_ma, self.p_test_time,
                       self.p_num_fails, self.p_start_date, self.p_end_date,
                       self.p_weeks, self.p_test_units, self.p_tpu,
                       self.p_tpupw, self.o_growth_rate, self.o_ms,
                       self.o_fef_avg, self.o_mi, self.o_mf, self.o_ma,
                       self.o_test_time, self.o_num_fails, self.o_ttff)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKGrowthTest data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKGrowthTest {0:d} attributes.". \
               format(self.phase_id)

        try:
            self.i_mi = float(none_to_default(attributes[0], 0.0))
            self.i_mf = float(none_to_default(attributes[1], 0.0))
            self.i_ma = float(none_to_default(attributes[2], 0.0))
            self.i_num_fails = int(none_to_default(attributes[3], 0))
            self.p_growth_rate = float(none_to_default(attributes[4], 0.0))
            self.p_ms = float(none_to_default(attributes[5], 0.0))
            self.p_fef_avg = float(none_to_default(attributes[6], 0.0))
            self.p_prob = float(none_to_default(attributes[7], 0.0))
            self.p_mi = float(none_to_default(attributes[8], 0.0))
            self.p_mf = float(none_to_default(attributes[9], 0.0))
            self.p_ma = float(none_to_default(attributes[10], 0.0))
            self.p_test_time = float(none_to_default(attributes[11], 0.0))
            self.p_num_fails = float(none_to_default(attributes[12], 0.0))
            self.p_start_date = none_to_default(attributes[13], date.today())
            self.p_end_date = none_to_default(attributes[14], date.today())
            self.p_weeks = float(none_to_default(attributes[15], 0.0))
            self.p_test_units = int(none_to_default(attributes[16], 0))
            self.p_tpu = float(none_to_default(attributes[17], 0.0))
            self.p_tpupw = float(none_to_default(attributes[18], 0.0))
            self.o_growth_rate = float(none_to_default(attributes[19], 0.0))
            self.o_ms = float(none_to_default(attributes[20], 0.0))
            self.o_fef_avg = float(none_to_default(attributes[21], 0.0))
            self.o_mi = float(none_to_default(attributes[22], 0.0))
            self.o_mf = float(none_to_default(attributes[23], 0.0))
            self.o_ma = float(none_to_default(attributes[24], 0.0))
            self.o_test_time = float(none_to_default(attributes[25], 0.0))
            self.o_num_fails = int(none_to_default(attributes[26], 0))
            self.o_ttff = float(none_to_default(attributes[27], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKGrowthTest.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKGrowthTest attributes."

        return _error_code, _msg
