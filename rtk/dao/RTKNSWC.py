#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKNSWC.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKNSWC Table
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


class RTKNSWC(Base):
    """
    Class to represent the rtk_nswc table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_nswc'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column('fld_hardware_id', Integer,
                         ForeignKey('rtk_hardware.fld_hardware_id'),
                         primary_key=True, nullable=False)

    Cac = Column('fld_c_ac', Float, default=0.0)
    Calt = Column('fld_c_alt', Float, default=0.0)
    Cb = Column('fld_c_b', Float, default=0.0)
    Cbl = Column('fld_c_bl', Float, default=0.0)
    Cbt = Column('fld_c_bt', Float, default=0.0)
    Cbv = Column('fld_c_bv', Float, default=0.0)
    Cc = Column('fld_c_c', Float, default=0.0)
    Ccf = Column('fld_c_cf', Float, default=0.0)
    Ccp = Column('fld_c_cp', Float, default=0.0)
    Ccs = Column('fld_c_cs', Float, default=0.0)
    Ccv = Column('fld_c_cv', Float, default=0.0)
    Ccw = Column('fld_c_cw', Float, default=0.0)
    Cd = Column('fld_c_d', Float, default=0.0)
    Cdc = Column('fld_c_dc', Float, default=0.0)
    Cdl = Column('fld_c_dl', Float, default=0.0)
    Cdp = Column('fld_c_dp', Float, default=0.0)
    Cds = Column('fld_c_ds', Float, default=0.0)
    Cdt = Column('fld_c_dt', Float, default=0.0)
    Cdw = Column('fld_c_dw', Float, default=0.0)
    Cdy = Column('fld_c_dy', Float, default=0.0)
    Ce = Column('fld_c_e', Float, default=0.0)
    Cf = Column('fld_c_f', Float, default=0.0)
    Cg = Column('fld_c_g', Float, default=0.0)
    Cga = Column('fld_c_ga', Float, default=0.0)
    Cgl = Column('fld_c_gl', Float, default=0.0)
    Cgp = Column('fld_c_gp', Float, default=0.0)
    Cgs = Column('fld_c_gs', Float, default=0.0)
    Cgt = Column('fld_c_gt', Float, default=0.0)
    Cgv = Column('fld_c_gv', Float, default=0.0)
    Ch = Column('fld_c_h', Float, default=0.0)
    Ci = Column('fld_c_i', Float, default=0.0)
    Ck = Column('fld_c_k', Float, default=0.0)
    Cl = Column('fld_c_l', Float, default=0.0)
    Clc = Column('fld_c_lc', Float, default=0.0)
    Cm = Column('fld_c_m', Float, default=0.0)
    Cmu = Column('fld_c_mu', Float, default=0.0)
    Cn = Column('fld_c_n', Float, default=0.0)
    Cnp = Column('fld_c_np', Float, default=0.0)
    Cnw = Column('fld_c_nw', Float, default=0.0)
    Cp = Column('fld_c_p', Float, default=0.0)
    Cpd = Column('fld_c_pd', Float, default=0.0)
    Cpf = Column('fld_c_pf', Float, default=0.0)
    Cpv = Column('fld_c_pv', Float, default=0.0)
    Cq = Column('fld_c_q', Float, default=0.0)
    Cr = Column('fld_c_r', Float, default=0.0)
    Crd = Column('fld_c_rd', Float, default=0.0)
    Cs = Column('fld_c_s', Float, default=0.0)
    Csc = Column('fld_c_sc', Float, default=0.0)
    Csf = Column('fld_c_sf', Float, default=0.0)
    Cst = Column('fld_c_st', Float, default=0.0)
    Csv = Column('fld_c_sv', Float, default=0.0)
    Csw = Column('fld_c_sw', Float, default=0.0)
    Csz = Column('fld_c_sz', Float, default=0.0)
    Ct = Column('fld_c_t', Float, default=0.0)
    Cv = Column('fld_c_v', Float, default=0.0)
    Cw = Column('fld_c_w', Float, default=0.0)
    Cy = Column('fld_c_y', Float, default=0.0)

    # Define the relationships to other tables in the RTK Program database.
    hardware = relationship('RTKHardware', back_populates='nswc')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKNSWC data model
        attributes.

        :return: (hardware_id, availability_alloc, env_factor, goal_measure_id,
                  hazard_rate_alloc, hazard_rate_goal, included, int_factor,
                  method_id, mtbf_alloc, mtbf_goal, n_sub_systems,
                  n_sub_elements, parent_id, percent_wt_factor,
                  reliability_alloc, reliability_goal, op_time_factor,
                  soa_factor, weight_factor)
        :rtype: tuple
        """

        _attributes = (self.hardware_id, self.Cac, self.Calt, self.Cb,
                       self.Cbl, self.Cbt, self.Cbv, self.Cc, self.Ccf,
                       self.Ccp, self.Ccs, self.Ccv, self.Ccw, self.Cd,
                       self.Cdc, self.Cdl, self.Cdp, self.Cds, self.Cdt,
                       self.Cdw, self.Cdy, self.Ce, self.Cf, self.Cg, self.Cg,
                       self.Cgl, self.Cgp, self.Cgs, self.Cgt, self.Cgv,
                       self.Ch, self.Ci, self.Ck, self.Cl, self.Clc, self.Cm,
                       self.Cmu, self.Cn, self.Cnp, self.Cnw, self.Cp,
                       self.Cpd, self.Cpf, self.Cpv, self.Cq, self.Cr,
                       self.Crd, self.Cs, self.Csc, self.Csf, self.Cst,
                       self.Csv, self.Csw, self.Csz, self.Ct, self.Cv, self.Cw,
                       self.Cy)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKNSWC data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKNSWC {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.Cac = float(attributes[0])
            self.Calt = float(attributes[1])
            self.Cb = float(attributes[2])
            self.Cbl = float(attributes[3])
            self.Cbt = float(attributes[4])
            self.Cbv = float(attributes[5])
            self.Cc = float(attributes[6])
            self.Ccf = float(attributes[7])
            self.Ccp = float(attributes[8])
            self.Ccs = float(attributes[9])
            self.Ccv = float(attributes[10])
            self.Ccw = float(attributes[11])
            self.Cd = float(attributes[12])
            self.Cdc = float(attributes[13])
            self.Cdl = float(attributes[14])
            self.Cdp = float(attributes[15])
            self.Cds = float(attributes[16])
            self.Cdt = float(attributes[17])
            self.Cdw = float(attributes[18])
            self.Cdy = float(attributes[19])
            self.Ce = float(attributes[20])
            self.Cf = float(attributes[21])
            self.Cg = float(attributes[22])
            self.Cg = float(attributes[23])
            self.Cgl = float(attributes[24])
            self.Cgp = float(attributes[25])
            self.Cgs = float(attributes[26])
            self.Cgt = float(attributes[27])
            self.Cgv = float(attributes[28])
            self.Ch = float(attributes[29])
            self.Ci = float(attributes[30])
            self.Ck = float(attributes[31])
            self.Cl = float(attributes[32])
            self.Clc = float(attributes[33])
            self.Cm = float(attributes[34])
            self.Cmu = float(attributes[35])
            self.Cn = float(attributes[36])
            self.Cnp = float(attributes[37])
            self.Cnw = float(attributes[38])
            self.Cp = float(attributes[39])
            self.Cpd = float(attributes[40])
            self.Cpf = float(attributes[41])
            self.Cpv = float(attributes[42])
            self.Cq = float(attributes[43])
            self.Cr = float(attributes[44])
            self.Crd = float(attributes[45])
            self.Cs = float(attributes[46])
            self.Csc = float(attributes[47])
            self.Csf = float(attributes[48])
            self.Cst = float(attributes[49])
            self.Csv = float(attributes[50])
            self.Csw = float(attributes[51])
            self.Csz = float(attributes[52])
            self.Ct = float(attributes[53])
            self.Cv = float(attributes[54])
            self.Cw = float(attributes[55])
            self.Cy = float(attributes[56])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKNSWC.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKNSWC attributes."

        return _error_code, _msg
