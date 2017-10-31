# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMilHdbkF.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKMilHdbkF Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship               # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE                  # pylint: disable=E0401


class RTKMilHdbkF(RTK_BASE):
    """
    Class to represent the rtk_mil_hdbk_f table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_mil_hdbk_f'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    # pylint: disable=invalid-name
    A1 = Column('fld_a_one', Float, default=0.0)
    # pylint: disable=invalid-name
    A2 = Column('fld_a_two', Float, default=0.0)
    # pylint: disable=invalid-name
    B1 = Column('fld_b_one', Float, default=0.0)
    # pylint: disable=invalid-name
    B2 = Column('fld_b_two', Float, default=0.0)
    # pylint: disable=invalid-name
    C1 = Column('fld_c_one', Float, default=0.0)
    # pylint: disable=invalid-name
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
            self.A1 = float(none_to_default(attributes[0], 0.0))
            self.A2 = float(none_to_default(attributes[1], 0.0))
            self.B1 = float(none_to_default(attributes[2], 0.0))
            self.B2 = float(none_to_default(attributes[3], 0.0))
            self.C1 = float(none_to_default(attributes[4], 0.0))
            self.C2 = float(none_to_default(attributes[5], 0.0))
            self.lambdaDB = float(none_to_default(attributes[6], 0.0))
            self.lambdaBP = float(none_to_default(attributes[7], 0.0))
            self.lambdaCYC = float(none_to_default(attributes[8], 0.0))
            self.lambdaEOS = float(none_to_default(attributes[9], 0.0))
            self.piA = float(none_to_default(attributes[10], 0.0))
            self.piC = float(none_to_default(attributes[11], 0.0))
            self.piCD = float(none_to_default(attributes[12], 0.0))
            self.piCF = float(none_to_default(attributes[13], 0.0))
            self.piCR = float(none_to_default(attributes[14], 0.0))
            self.piCV = float(none_to_default(attributes[15], 0.0))
            self.piCYC = float(none_to_default(attributes[16], 0.0))
            self.piE = float(none_to_default(attributes[17], 0.0))
            self.piF = float(none_to_default(attributes[18], 0.0))
            self.piI = float(none_to_default(attributes[19], 0.0))
            self.piK = float(none_to_default(attributes[20], 0.0))
            self.piL = float(none_to_default(attributes[21], 0.0))
            self.piM = float(none_to_default(attributes[22], 0.0))
            self.piMFG = float(none_to_default(attributes[23], 0.0))
            self.piN = float(none_to_default(attributes[24], 0.0))
            self.piNR = float(none_to_default(attributes[25], 0.0))
            self.piP = float(none_to_default(attributes[26], 0.0))
            self.piPT = float(none_to_default(attributes[27], 0.0))
            self.piQ = float(none_to_default(attributes[28], 0.0))
            self.piR = float(none_to_default(attributes[29], 0.0))
            self.piS = float(none_to_default(attributes[30], 0.0))
            self.piT = float(none_to_default(attributes[31], 0.0))
            self.piTAPS = float(none_to_default(attributes[32], 0.0))
            self.pi_u = float(none_to_default(attributes[33], 0.0))
            self.pi_v = float(none_to_default(attributes[34], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKMilHdbkF.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKMilHdbkF attributes."

        return _error_code, _msg
