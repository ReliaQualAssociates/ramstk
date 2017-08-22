#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKTest.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
===============================================================================
The RTKTest Table
===============================================================================
"""

# Import the database models.
from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RTK modules.
from Utilities import error_handler, none_to_default
from dao.RTKCommonDB import RTK_BASE

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class RTKTest(RTK_BASE):
    """
    Class to represent the table rtk_test in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relationship with rtk_growth_test.
    """

    __tablename__ = 'rtk_test'
    __table_args__ = {'extend_existing': True}

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

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKTest data model
        attributes.

        :return: (revision_id, test_id, assess_model_id, attachment, avg_fef,
                  avg_growth, avg_ms, chi_square, confidence, consumer_risk,
                  cramer_vonmises, cum_failures, cum_mean, cum_mean_ll,
                  cum_mean_se, cum_mean_ul, cum_time, description, grouped,
                  group_interval, inst_mean, inst_mean_ll, inst_mean_se,
                  inst_mean_ul, mg, mgp, n_phases, name, plan_model_id, prob,
                  producer_risk, scale, scale_ll, scale_se, scale_ul, shape,
                  shape_ll, shape_se, shape_ul, tr, ttt, ttff, type_id)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.test_id, self.assess_model_id,
                       self.attachment, self.avg_fef, self.avg_growth,
                       self.avg_ms, self.chi_square, self.confidence,
                       self.consumer_risk, self.cramer_vonmises,
                       self.cum_failures, self.cum_mean, self.cum_mean_ll,
                       self.cum_mean_se, self.cum_mean_ul, self.cum_time,
                       self.description, self.grouped, self.group_interval,
                       self.inst_mean, self.inst_mean_ll, self.inst_mean_se,
                       self.inst_mean_ul, self.mg, self.mgp, self.n_phases,
                       self.name, self.plan_model_id, self.prob,
                       self.producer_risk, self.scale, self.scale_ll,
                       self.scale_se, self.scale_ul, self.shape, self.shape_ll,
                       self.shape_se, self.shape_ul, self.tr, self.ttt,
                       self.ttff, self.type_id)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKTest data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKTest {0:d} attributes.". \
               format(self.test_id)

        try:
            self.assess_model_id = int(attributes[0])
            self.attachment = str(attributes[1])
            self.avg_fef = float(attributes[2])
            self.avg_growth = float(attributes[3])
            self.avg_ms = float(attributes[4])
            self.chi_square = float(attributes[5])
            self.confidence = float(attributes[6])
            self.consumer_risk = float(attributes[7])
            self.cramer_vonmises = float(attributes[8])
            self.cum_failures = int(attributes[9])
            self.cum_mean = float(attributes[10])
            self.cum_mean_ll = float(attributes[11])
            self.cum_mean_se = float(attributes[12])
            self.cum_mean_ul = float(attributes[13])
            self.cum_time = float(attributes[14])
            self.description = str(attributes[15])
            self.grouped = int(attributes[16])
            self.group_interval = float(attributes[17])
            self.inst_mean = float(attributes[18])
            self.inst_mean_ll = float(attributes[19])
            self.inst_mean_se = float(attributes[20])
            self.inst_mean_ul = float(attributes[21])
            self.mg = float(attributes[22])
            self.mgp = float(attributes[23])
            self.n_phases = int(attributes[24])
            self.name = str(attributes[25])
            self.plan_model_id = int(attributes[26])
            self.prob = float(attributes[27])
            self.producer_risk = float(attributes[28])
            self.scale = float(attributes[29])
            self.scale_ll = float(attributes[30])
            self.scale_se = float(attributes[31])
            self.scale_ul = float(attributes[32])
            self.shape = float(attributes[33])
            self.shape_ll = float(attributes[34])
            self.shape_se = float(attributes[35])
            self.shape_ul = float(attributes[36])
            self.tr = float(attributes[37])
            self.ttt = float(attributes[38])
            self.ttff = float(attributes[39])
            self.type_id = int(attributes[40])
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKTest.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKTest attributes."

        return _error_code, _msg
