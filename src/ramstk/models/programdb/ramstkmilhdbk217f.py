# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.data.storage.RAMSTKMilHdbkF.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMilHdbkF Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


class RAMSTKMilHdbkF(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_mil_hdbk_f table in RAMSTK Program database.

    This table shares a One-to-One relationship with ramstk_hardware.
    """

    __defaults__ = {
        'A1': 0.0,
        'A2': 0.0,
        'B1': 0.0,
        'B2': 0.0,
        'C1': 0.0,
        'C2': 0.0,
        'lambdaBD': 0.0,
        'lambdaBP': 0.0,
        'lambdaCYC': 0.0,
        'lambdaEOS': 0.0,
        'piA': 0.0,
        'piC': 0.0,
        'piCD': 0.0,
        'piCF': 0.0,
        'piCR': 0.0,
        'piCV': 0.0,
        'piCYC': 0.0,
        'piE': 0.0,
        'piF': 0.0,
        'piI': 0.0,
        'piK': 0.0,
        'piL': 0.0,
        'piM': 0.0,
        'piMFG': 0.0,
        'piN': 0.0,
        'piNR': 0.0,
        'piP': 0.0,
        'piPT': 0.0,
        'piQ': 0.0,
        'piR': 0.0,
        'piS': 0.0,
        'piT': 0.0,
        'piTAPS': 0.0,
        'piU': 0.0,
        'piV': 0.0
    }
    __tablename__ = 'ramstk_mil_hdbk_f'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False,
    )

    A1 = Column('fld_a_one', Float, default=__defaults__['A1'])
    A2 = Column('fld_a_two', Float, default=__defaults__['A2'])
    B1 = Column('fld_b_one', Float, default=__defaults__['B1'])
    B2 = Column('fld_b_two', Float, default=__defaults__['B2'])
    C1 = Column('fld_c_one', Float, default=__defaults__['C1'])
    C2 = Column('fld_c_two', Float, default=__defaults__['C2'])
    lambdaBD = Column('fld_lambda_bd', Float, default=__defaults__['lambdaBD'])
    lambdaBP = Column('fld_lambda_bp', Float, default=__defaults__['lambdaBP'])
    lambdaCYC = Column('fld_lambda_cyc',
                       Float,
                       default=__defaults__['lambdaCYC'])
    lambdaEOS = Column('fld_lambda_eos',
                       Float,
                       default=__defaults__['lambdaEOS'])
    piA = Column('fld_pi_a', Float, default=__defaults__['piA'])
    piC = Column('fld_pi_c', Float, default=__defaults__['piC'])
    piCD = Column('fld_pi_cd', Float, default=__defaults__['piCD'])
    piCF = Column('fld_pi_cf', Float, default=__defaults__['piCF'])
    piCR = Column('fld_pi_cr', Float, default=__defaults__['piCR'])
    piCV = Column('fld_pi_cv', Float, default=__defaults__['piCV'])
    piCYC = Column('fld_pi_cyc', Float, default=__defaults__['piCYC'])
    piE = Column('fld_pi_e', Float, default=__defaults__['piE'])
    piF = Column('fld_pi_f', Float, default=__defaults__['piF'])
    piI = Column('fld_pi_i', Float, default=__defaults__['piI'])
    piK = Column('fld_pi_k', Float, default=__defaults__['piK'])
    piL = Column('fld_pi_l', Float, default=__defaults__['piL'])
    piM = Column('fld_pi_m', Float, default=__defaults__['piM'])
    piMFG = Column('fld_pi_mfg', Float, default=__defaults__['piMFG'])
    piN = Column('fld_pi_n', Float, default=__defaults__['piN'])
    piNR = Column('fld_pi_nr', Float, default=__defaults__['piNR'])
    piP = Column('fld_pi_p', Float, default=__defaults__['piP'])
    piPT = Column('fld_pi_pt', Float, default=__defaults__['piPT'])
    piQ = Column('fld_pi_q', Float, default=__defaults__['piQ'])
    piR = Column('fld_pi_r', Float, default=__defaults__['piR'])
    piS = Column('fld_pi_s', Float, default=__defaults__['piS'])
    piT = Column('fld_pi_t', Float, default=__defaults__['piT'])
    piTAPS = Column('fld_pi_taps', Float, default=__defaults__['piTAPS'])
    piU = Column('fld_pi_u', Float, default=__defaults__['piU'])
    piV = Column('fld_pi_v', Float, default=__defaults__['piV'])

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware = relationship(  # type: ignore
        'RAMSTKHardware',
        back_populates='milhdbkf',
    )

    def get_attributes(self):
        """Retrieve the current values of RAMSTKMilHdbkF data model attributes.

        :return: {hardware_id, A2, A2, B1, B2, C1, C2, lambdaBD, lambdaBP,
                  lambdaCYC, lambdaEOS, piA, piC, piCD, piCF, piCR, piCV,
                  piCYC, piE, piF, piI, piK, piL, piM, piMFG, piN, piNR, piP,
                  piPT, piQ, piR, piS, piT, piTAPS, piU, piV} pairs.
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
            'piV': self.piV,
        }

        return _attributes
