# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKMilHdbkF.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKMilHdbkF Table Module."""  # pragma: no cover

from sqlalchemy import Column, Float, ForeignKey, Integer  # pragma: no cover
from sqlalchemy.orm import relationship

# Import other RTK modules.
from rtk.Utilities import none_to_default

from rtk.dao.RTKCommonDB import RTK_BASE  # pragma: no cover


class RTKMilHdbkF(RTK_BASE):
    """
    Class to represent the rtk_mil_hdbk_f table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_mil_hdbk_f'
    __table_args__ = {'extend_existing': True}  # pragma: no cover

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('rtk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

    A1 = Column('fld_a_one', Float, default=0.0)  # pylint: disable=C0103
    A2 = Column('fld_a_two', Float, default=0.0)  # pylint: disable=C0103
    B1 = Column('fld_b_one', Float, default=0.0)  # pylint: disable=C0103
    B2 = Column('fld_b_two', Float, default=0.0)  # pylint: disable=C0103
    C1 = Column('fld_c_one', Float, default=0.0)  # pylint: disable=C0103
    C2 = Column('fld_c_two', Float, default=0.0)  # pylint: disable=C0103
    lambdaBD = Column('fld_lambda_bd', Float, default=0.0)
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
    piU = Column('fld_pi_u', Float, default=0.0)
    piV = Column('fld_pi_v', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='milhdbkf')

    def get_attributes(self):
        """
        Retrieve the current values of the RTKMilHdbkF data model attributes.

        :return: {hardware_id, availability_alloc, env_factor, goal_measure_id,
                  hazard_rate_alloc, hazard_rate_goal, included, int_factor,
                  method_id, mtbf_alloc, mtbf_goal, n_sub_systems,
                  n_sub_elements, parent_id, percent_wt_factor,
                  reliability_alloc, reliability_goal, op_time_factor,
                  soa_factor, weight_factor} pairs.
        :rtype: dict
        """
        _attributes = {
            'hardware_id': self.hardware_id,
            'A1': self.A1,
            'A2': self.A2,
            'B1': self.B1,
            'B2': self.B2,
            'C1': self.C1,
            'C2': self.C2,
            'lambdaBD': self.lambdaBD,
            'lambdaBP': self.lambdaBP,
            'lambdaCYC': self.lambdaCYC,
            'lambdaEOS': self.lambdaEOS,
            'piA': self.piA,
            'piC': self.piC,
            'piCD': self.piCD,
            'piCF': self.piCF,
            'piCR': self.piCR,
            'piCV': self.piCV,
            'piCYC': self.piCYC,
            'piE': self.piE,
            'piF': self.piF,
            'piI': self.piI,
            'piK': self.piK,
            'piL': self.piL,
            'piM': self.piM,
            'piMFG': self.piMFG,
            'piN': self.piN,
            'piNR': self.piNR,
            'piP': self.piP,
            'piPT': self.piPT,
            'piQ': self.piQ,
            'piR': self.piR,
            'piS': self.piS,
            'piT': self.piT,
            'piTAPS': self.piTAPS,
            'piU': self.piU,
            'piV': self.piV
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RTKMilHdbkF data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKMilHdbkF {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.A1 = float(none_to_default(attributes['A1'], 0.0))
            self.A2 = float(none_to_default(attributes['A2'], 0.0))
            self.B1 = float(none_to_default(attributes['B1'], 0.0))
            self.B2 = float(none_to_default(attributes['B2'], 0.0))
            self.C1 = float(none_to_default(attributes['C1'], 0.0))
            self.C2 = float(none_to_default(attributes['C2'], 0.0))
            self.lambdaBD = float(none_to_default(attributes['lambdaBD'], 0.0))
            self.lambdaBP = float(none_to_default(attributes['lambdaBP'], 0.0))
            self.lambdaCYC = float(
                none_to_default(attributes['lambdaCYC'], 0.0))
            self.lambdaEOS = float(
                none_to_default(attributes['lambdaEOS'], 0.0))
            self.piA = float(none_to_default(attributes['piA'], 0.0))
            self.piC = float(none_to_default(attributes['piC'], 0.0))
            self.piCD = float(none_to_default(attributes['piCD'], 0.0))
            self.piCF = float(none_to_default(attributes['piCF'], 0.0))
            self.piCR = float(none_to_default(attributes['piCR'], 0.0))
            self.piCV = float(none_to_default(attributes['piCV'], 0.0))
            self.piCYC = float(none_to_default(attributes['piCYC'], 0.0))
            self.piE = float(none_to_default(attributes['piE'], 0.0))
            self.piF = float(none_to_default(attributes['piF'], 0.0))
            self.piI = float(none_to_default(attributes['piI'], 0.0))
            self.piK = float(none_to_default(attributes['piK'], 0.0))
            self.piL = float(none_to_default(attributes['piL'], 0.0))
            self.piM = float(none_to_default(attributes['piM'], 0.0))
            self.piMFG = float(none_to_default(attributes['piMFG'], 0.0))
            self.piN = float(none_to_default(attributes['piN'], 0.0))
            self.piNR = float(none_to_default(attributes['piNR'], 0.0))
            self.piP = float(none_to_default(attributes['piP'], 0.0))
            self.piPT = float(none_to_default(attributes['piPT'], 0.0))
            self.piQ = float(none_to_default(attributes['piQ'], 0.0))
            self.piR = float(none_to_default(attributes['piR'], 0.0))
            self.piS = float(none_to_default(attributes['piS'], 0.0))
            self.piT = float(none_to_default(attributes['piT'], 0.0))
            self.piTAPS = float(none_to_default(attributes['piTAPS'], 0.0))
            self.piU = float(none_to_default(attributes['piU'], 0.0))
            self.piV = float(none_to_default(attributes['piV'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RTKMilHdbkF.set_attributes().".format(_err)

        return _error_code, _msg
