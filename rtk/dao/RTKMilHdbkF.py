#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMilHdbkF.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKMilHdbkF Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer
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


class RTKMilHdbkF(Base):
    """
    Class to represent the rtk_mil_hdbk_f table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_mil_hdbk_f'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    A1 = Column('fld_a_one', Float, default=0.0)
    A2 = Column('fld_a_two', Float, default=0.0)
    B1 = Column('fld_b_one', Float, default=0.0)
    B2 = Column('fld_b_two', Float, default=0.0)
    C1 = Column('fld_c_one', Float, default=0.0)
    C2 = Column('fld_c_two', Float, default=0.0)
    lambdaDB = Column('fld_lambda_bd', Float, default=0.0)
    lambdaBP = Column('fld_lambda_bp', Float, default=0.0)
    lambdaCYC = Column('fld_lambda_cyc', Float, default=0.0)
    lambdaEOS = Column('fld_lambda_eos', Float, default=0.0)
    piA = Column('fld_pi_a', Float, default=0.0)
    piC = Column('fld_pi_c', Float, default=0.0)
    piCD = Column('fld_pi_cd', Float, default=0.0)
    piCF = Column('fld_pi_cf', Float, default=0.0)
    piCR = Column('fld_pi_cr', Float, default=0.0)
    piCV = Column('fld_pi_cv', Float, default=0.0)
    piCYC = Column('fld_pi_cyc', Float, default=0.0)
    piE = Column('fld_pi_e', Float, default=0.0)
    piF = Column('fld_pi_f', Float, default=0.0)
    piI = Column('fld_pi_i', Float, default=0.0)
    piK = Column('fld_pi_k', Float, default=0.0)
    piL = Column('fld_pi_l', Float, default=0.0)
    piM = Column('fld_pi_m', Float, default=0.0)
    piMFG = Column('fld_pi_mfg', Float, default=0.0)
    piN = Column('fld_pi_n', Float, default=0.0)
    piNR = Column('fld_pi_nr', Float, default=0.0)
    piP = Column('fld_pi_p', Float, default=0.0)
    piPT = Column('fld_pi_pt', Float, default=0.0)
    piQ = Column('fld_pi_q', Float, default=0.0)
    piR = Column('fld_pi_r', Float, default=0.0)
    piS = Column('fld_pi_s', Float, default=0.0)
    piT = Column('fld_pi_t', Float, default=0.0)
    piTAPS = Column('fld_pi_taps', Float, default=0.0)
    pi_u = Column('fld_pi_u', Float, default=0.0)
    pi_v = Column('fld_pi_v', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='milhdbkf')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKMilHdbkF data model
        attributes.

        :return: (hardware_id, availability_alloc, env_factor, goal_measure_id,
                  hazard_rate_alloc, hazard_rate_goal, included, int_factor,
                  method_id, mtbf_alloc, mtbf_goal, n_sub_systems,
                  n_sub_elements, parent_id, percent_wt_factor,
                  reliability_alloc, reliability_goal, op_time_factor,
                  soa_factor, weight_factor)
        :rtype: tuple
        """

        _attributes = (self.hardware_id, self.A1, self.A2, self.B1, self.B2,
                       self.C1, self.C2, self.lambdaDB, self.lambdaBP,
                       self.lambdaCYC, self.lambdaEOS, self.piA, self.piC,
                       self.piCD, self.piCF, self.piCR, self.piCV, self.piCYC,
                       self.piE, self.piF, self.piI, self.piK, self.piL,
                       self.piM, self.piMFG, self.piN, self.piNR, self.piP,
                       self.piPT, self.piQ, self.piR, self.piS, self.piT,
                       self.piTAPS, self.pi_u, self.pi_v)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKMilHdbkF data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMilHdbkF {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.A1 = float(attributes[0])
            self.A2 = float(attributes[1])
            self.B1 = float(attributes[2])
            self.B2 = float(attributes[3])
            self.C1 = float(attributes[4])
            self.C2 = float(attributes[5])
            self.lambdaDB = float(attributes[6])
            self.lambdaBP = float(attributes[7])
            self.lambdaCYC = float(attributes[8])
            self.lambdaEOS = float(attributes[9])
            self.piA = float(attributes[10])
            self.piC = float(attributes[11])
            self.piCD = float(attributes[12])
            self.piCF = float(attributes[13])
            self.piCR = float(attributes[14])
            self.piCV = float(attributes[15])
            self.piCYC = float(attributes[16])
            self.piE = float(attributes[17])
            self.piF = float(attributes[18])
            self.piI = float(attributes[19])
            self.piK = float(attributes[20])
            self.piL = float(attributes[21])
            self.piM = float(attributes[22])
            self.piMFG = float(attributes[23])
            self.piN = float(attributes[24])
            self.piNR = float(attributes[25])
            self.piP = float(attributes[26])
            self.piPT = float(attributes[27])
            self.piQ = float(attributes[28])
            self.piR = float(attributes[29])
            self.piS = float(attributes[30])
            self.piT = float(attributes[31])
            self.piTAPS = float(attributes[32])
            self.pi_u = float(attributes[33])
            self.pi_v = float(attributes[34])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMilHdbkF.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMilHdbkF attributes."

        return _error_code, _msg

