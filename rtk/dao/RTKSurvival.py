#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSurvival.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKSurvival Table
==============================
"""

from datetime import date, timedelta

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


class RTKSurvival(Base):
    """
    Class to represent the table rtk_survival in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    This table shares a One-to-Many relatinship with rtk_survival_data.
    """

    __tablename__ = 'rtk_survival'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    survival_id = Column('fld_survival_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

    hardware_id = Column('fld_hardware_id', Integer,  default=0)
    description = Column('fld_description', String(512), default='')
    source_id = Column('fld_source_id', Integer, default=0)
    distribution_id = Column('fld_distribution_id', Integer, default=0)
    confidence = Column('fld_confidence', Float, default=75.0)
    confidence_type_id = Column('fld_confidence_type_id', Integer, default=0)
    confidence_method_id = Column('fld_confidence_method_id', Integer,
                                  default=0)
    fit_method_id = Column('fld_fit_method_id', Integer, default=0)
    rel_time = Column('fld_rel_time', Float, default=0.0)
    n_rel_points = Column('fld_n_rel_points', Integer, default=0)
    n_suspension = Column('fld_n_suspensions', Integer, default=0)
    n_failures = Column('fld_n_failures', Integer, default=0)
    scale_ll = Column('fld_scale_ll', Float, default=0.0)
    scale = Column('fld_scale', Float, default=0.0)
    scale_ul = Column('fld_scale_ul', Float, default=0.0)
    shape_ll = Column('fld_shape_ll', Float, default=0.0)
    shape = Column('fld_shape', Float, default=0.0)
    shape_ul = Column('fld_shape_ul', Float, default=0.0)
    location_ll = Column('fld_location_ll', Float, default=0.0)
    location = Column('fld_location', Float, default=0.0)
    location_ul = Column('fld_location_ul', Float, default=0.0)
    variance_1 = Column('fld_variance_1', Float, default=0.0)
    variance_2 = Column('fld_variance_2', Float, default=0.0)
    variance_3 = Column('fld_variance_3', Float, default=0.0)
    covariance_1 = Column('fld_covariance_1', Float, default=0.0)
    covariance_2 = Column('fld_covariance_2', Float, default=0.0)
    covariance_3 = Column('fld_covariance_3', Float, default=0.0)
    mhb = Column('fld_mhb', Float, default=0.0)
    lp = Column('fld_lp', Float, default=0.0)
    lr = Column('fld_lr', Float, default=0.0)
    aic = Column('fld_aic', Float, default=0.0)
    bic = Column('fld_bic', Float, default=0.0)
    mle = Column('fld_mle', Float, default=0.0)
    start_time = Column('fld_start_time', Float, default=0.0)
    start_date = Column('fld_start_date', Date, default=date.today())
    end_date = Column('fld_end_date', Date,
                      default=date.today() + timedelta(days=30))
    nevada_chart = Column('fld_nevada_chart', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='survival')
    data = relationship('RTKSurvivalData', back_populates='survival')

    def get_attributes(self):
        """
        Retrieves the current values of the RTKSurvival data model attributes.

        :return: (revision_id, survival_id, hardware_id, description,
                  source_id, distribution_id, confidence, confidence_type_id,
                  confidence_method_id, fit_method_id, rel_time, n_rel_points,
                  n_suspension, n_failures, scale_ll, scale, scale_ul,
                  shape_ll, shape, shape_ul, location_ll, location,
                  location_ul, variance_1, variance_2, variance_3,
                  covariance_1, covariance_2, covariance_3, mhb, lp, lr, aic,
                  bic, mle, start_time, start_date, end_date, nevada_chart)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.survival_id, self.hardware_id,
                       self.description, self.source_id, self.distribution_id,
                       self.confidence, self.confidence_type_id,
                       self.confidence_method_id, self.fit_method_id,
                       self.rel_time, self.n_rel_points, self.n_suspension,
                       self.n_failures, self.scale_ll, self.scale,
                       self.scale_ul, self.shape_ll, self.shape, self.shape_ul,
                       self.location_ll, self.location, self.location_ul,
                       self.variance_1, self.variance_2, self.variance_3,
                       self.covariance_1, self.covariance_2, self.covariance_3,
                       self.mhb, self.lp, self.lr, self.aic, self.bic,
                       self.mle, self.start_time, self.start_date,
                       self.end_date, self.nevada_chart)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKSurvival data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSurvival {0:d} attributes.". \
               format(self.survival_id)

        try:
            self.hardware_id = int(attributes[0])
            self.description = str(attributes[1])
            self.source_id = int(attributes[2])
            self.distribution_id = int(attributes[3])
            self.confidence = float(attributes[4])
            self.confidence_type_id = int(attributes[5])
            self.confidence_method_id = int(attributes[6])
            self.fit_method_id = int(attributes[7])
            self.rel_time = float(attributes[8])
            self.n_rel_points = int(attributes[9])
            self.n_suspension = int(attributes[10])
            self.n_failures = int(attributes[11])
            self.scale_ll = float(attributes[12])
            self.scale = float(attributes[13])
            self.scale_ul = float(attributes[14])
            self.shape_ll = float(attributes[15])
            self.shape = float(attributes[16])
            self.shape_ul = float(attributes[17])
            self.location_ll = float(attributes[18])
            self.location = float(attributes[19])
            self.location_ul = float(attributes[20])
            self.variance_1 = float(attributes[21])
            self.variance_2 = float(attributes[22])
            self.variance_3 = float(attributes[23])
            self.covariance_1 = float(attributes[24])
            self.covariance_2 = float(attributes[25])
            self.covariance_3 = float(attributes[26])
            self.mhb = float(attributes[27])
            self.lp = float(attributes[28])
            self.lr = float(attributes[29])
            self.aic = float(attributes[30])
            self.bic = float(attributes[31])
            self.mle = float(attributes[32])
            self.start_time = float(attributes[33])
            self.start_date = attributes[34]
            self.end_date = attributes[35]
            self.nevada_chart = int(attributes[36])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSurvival.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSurvival attributes."

        return _error_code, _msg
