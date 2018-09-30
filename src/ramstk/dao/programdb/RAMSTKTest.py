# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKTest.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RAMSTKTest Table
===============================================================================
"""

from sqlalchemy import BLOB, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import error_handler, none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


class RAMSTKTest(RAMSTK_BASE):
    """
    Class to represent the table ramstk_test in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision.
    This table shares a One-to-Many relationship with ramstk_growth_test.
    """

    __tablename__ = 'ramstk_test'
    __table_args__ = {'extend_existing': True}

    revision_id = Column(
        'fld_revision_id',
        Integer,
        ForeignKey('ramstk_revision.fld_revision_id'),
        nullable=False)
    test_id = Column(
        'fld_test_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False)

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
    # pylint: disable=invalid-name
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

    # Define the relationships to other tables in the RAMSTK Program database.
    revision = relationship('RAMSTKRevision', back_populates='test')
    growth = relationship('RAMSTKGrowthTest', back_populates='test')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RAMSTKTest data model
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
        Method to set the RAMSTKTest data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKTest {0:d} attributes.". \
               format(self.test_id)

        try:
            self.assess_model_id = int(none_to_default(attributes[0], 0))
            self.attachment = str(none_to_default(attributes[1], ''))
            self.avg_fef = float(none_to_default(attributes[2], 0.0))
            self.avg_growth = float(none_to_default(attributes[3], 0.0))
            self.avg_ms = float(none_to_default(attributes[4], 0.0))
            self.chi_square = float(none_to_default(attributes[5], 0.0))
            self.confidence = float(none_to_default(attributes[6], 0.0))
            self.consumer_risk = float(none_to_default(attributes[7], 0.0))
            self.cramer_vonmises = float(none_to_default(attributes[8], 0.0))
            self.cum_failures = int(none_to_default(attributes[9], 0))
            self.cum_mean = float(none_to_default(attributes[10], 0.0))
            self.cum_mean_ll = float(none_to_default(attributes[11], 0.0))
            self.cum_mean_se = float(none_to_default(attributes[12], 0.0))
            self.cum_mean_ul = float(none_to_default(attributes[13], 0.0))
            self.cum_time = float(none_to_default(attributes[14], 0.0))
            self.description = str(none_to_default(attributes[15], ''))
            self.grouped = int(none_to_default(attributes[16], 0))
            self.group_interval = float(none_to_default(attributes[17], 0.0))
            self.inst_mean = float(none_to_default(attributes[18], 0.0))
            self.inst_mean_ll = float(none_to_default(attributes[19], 0.0))
            self.inst_mean_se = float(none_to_default(attributes[20], 0.0))
            self.inst_mean_ul = float(none_to_default(attributes[21], 0.0))
            self.mg = float(none_to_default(attributes[22], 0.0))
            self.mgp = float(none_to_default(attributes[23], 0.0))
            self.n_phases = int(none_to_default(attributes[24], 1))
            self.name = str(none_to_default(attributes[25], ''))
            self.plan_model_id = int(none_to_default(attributes[26], 0))
            self.prob = float(none_to_default(attributes[27], 75.0))
            self.producer_risk = float(none_to_default(attributes[28], 0.0))
            self.scale = float(none_to_default(attributes[29], 0.0))
            self.scale_ll = float(none_to_default(attributes[30], 0.0))
            self.scale_se = float(none_to_default(attributes[31], 0.0))
            self.scale_ul = float(none_to_default(attributes[32], 0.0))
            self.shape = float(none_to_default(attributes[33], 0.0))
            self.shape_ll = float(none_to_default(attributes[34], 0.0))
            self.shape_se = float(none_to_default(attributes[35], 0.0))
            self.shape_ul = float(none_to_default(attributes[36], 0.0))
            self.tr = float(none_to_default(attributes[37], 0.0))
            self.ttt = float(none_to_default(attributes[38], 0.0))
            self.ttff = float(none_to_default(attributes[39], 0.0))
            self.type_id = int(none_to_default(attributes[40], 0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Insufficient number of input values to " \
                   "RAMSTKTest.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RAMSTK ERROR: Incorrect data type when converting one or " \
                   "more RAMSTKTest attributes."

        return _error_code, _msg
