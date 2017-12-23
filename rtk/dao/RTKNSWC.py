# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKNSWC.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
===============================================================================
The RTKNSWC Table
===============================================================================
"""
# pylint: disable=E0401
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship  # pylint: disable=E0401

# Import other RTK modules.
from Utilities import error_handler, none_to_default  # pylint: disable=E0401
from dao.RTKCommonDB import RTK_BASE  # pylint: disable=E0401


# pylint: disable=R0902
class RTKNSWC(RTK_BASE):
    """
    Class to represent the rtk_nswc table in the RTK Program database.

    This table shares a One-to-One relationship with rtk_hardware.
    """

    __tablename__ = 'rtk_nswc'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('rtk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

    Cac = Column('fld_c_ac', Float, default=0.0)
    Calt = Column('fld_c_alt', Float, default=0.0)
    Cb = Column('fld_c_b', Float, default=0.0)  # pylint: disable=invalid-name
    Cbl = Column('fld_c_bl', Float, default=0.0)
    Cbt = Column('fld_c_bt', Float, default=0.0)
    Cbv = Column('fld_c_bv', Float, default=0.0)
    Cc = Column('fld_c_c', Float, default=0.0)  # pylint: disable=invalid-name
    Ccf = Column('fld_c_cf', Float, default=0.0)
    Ccp = Column('fld_c_cp', Float, default=0.0)
    Ccs = Column('fld_c_cs', Float, default=0.0)
    Ccv = Column('fld_c_cv', Float, default=0.0)
    Ccw = Column('fld_c_cw', Float, default=0.0)
    Cd = Column('fld_c_d', Float, default=0.0)  # pylint: disable=invalid-name
    Cdc = Column('fld_c_dc', Float, default=0.0)
    Cdl = Column('fld_c_dl', Float, default=0.0)
    Cdp = Column('fld_c_dp', Float, default=0.0)
    Cds = Column('fld_c_ds', Float, default=0.0)
    Cdt = Column('fld_c_dt', Float, default=0.0)
    Cdw = Column('fld_c_dw', Float, default=0.0)
    Cdy = Column('fld_c_dy', Float, default=0.0)
    Ce = Column('fld_c_e', Float, default=0.0)  # pylint: disable=invalid-name
    Cf = Column('fld_c_f', Float, default=0.0)  # pylint: disable=invalid-name
    Cg = Column('fld_c_g', Float, default=0.0)  # pylint: disable=invalid-name
    Cga = Column('fld_c_ga', Float, default=0.0)
    Cgl = Column('fld_c_gl', Float, default=0.0)
    Cgp = Column('fld_c_gp', Float, default=0.0)
    Cgs = Column('fld_c_gs', Float, default=0.0)
    Cgt = Column('fld_c_gt', Float, default=0.0)
    Cgv = Column('fld_c_gv', Float, default=0.0)
    Ch = Column('fld_c_h', Float, default=0.0)  # pylint: disable=invalid-name
    Ci = Column('fld_c_i', Float, default=0.0)  # pylint: disable=invalid-name
    Ck = Column('fld_c_k', Float, default=0.0)  # pylint: disable=invalid-name
    Cl = Column('fld_c_l', Float, default=0.0)  # pylint: disable=invalid-name
    Clc = Column('fld_c_lc', Float, default=0.0)
    Cm = Column('fld_c_m', Float, default=0.0)  # pylint: disable=invalid-name
    Cmu = Column('fld_c_mu', Float, default=0.0)
    Cn = Column('fld_c_n', Float, default=0.0)  # pylint: disable=invalid-name
    Cnp = Column('fld_c_np', Float, default=0.0)
    Cnw = Column('fld_c_nw', Float, default=0.0)
    Cp = Column('fld_c_p', Float, default=0.0)  # pylint: disable=invalid-name
    Cpd = Column('fld_c_pd', Float, default=0.0)
    Cpf = Column('fld_c_pf', Float, default=0.0)
    Cpv = Column('fld_c_pv', Float, default=0.0)
    Cq = Column('fld_c_q', Float, default=0.0)  # pylint: disable=invalid-name
    Cr = Column('fld_c_r', Float, default=0.0)  # pylint: disable=invalid-name
    Crd = Column('fld_c_rd', Float, default=0.0)
    Cs = Column('fld_c_s', Float, default=0.0)  # pylint: disable=invalid-name
    Csc = Column('fld_c_sc', Float, default=0.0)
    Csf = Column('fld_c_sf', Float, default=0.0)
    Cst = Column('fld_c_st', Float, default=0.0)
    Csv = Column('fld_c_sv', Float, default=0.0)
    Csw = Column('fld_c_sw', Float, default=0.0)
    Csz = Column('fld_c_sz', Float, default=0.0)
    Ct = Column('fld_c_t', Float, default=0.0)  # pylint: disable=invalid-name
    Cv = Column('fld_c_v', Float, default=0.0)  # pylint: disable=invalid-name
    Cw = Column('fld_c_w', Float, default=0.0)  # pylint: disable=invalid-name
    Cy = Column('fld_c_y', Float, default=0.0)  # pylint: disable=invalid-name

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
            self.Cac = float(none_to_default(attributes[0], 0.0))
            self.Calt = float(none_to_default(attributes[1], 0.0))
            self.Cb = float(none_to_default(attributes[2], 0.0))
            self.Cbl = float(none_to_default(attributes[3], 0.0))
            self.Cbt = float(none_to_default(attributes[4], 0.0))
            self.Cbv = float(none_to_default(attributes[5], 0.0))
            self.Cc = float(none_to_default(attributes[6], 0.0))
            self.Ccf = float(none_to_default(attributes[7], 0.0))
            self.Ccp = float(none_to_default(attributes[8], 0.0))
            self.Ccs = float(none_to_default(attributes[9], 0.0))
            self.Ccv = float(none_to_default(attributes[10], 0.0))
            self.Ccw = float(none_to_default(attributes[11], 0.0))
            self.Cd = float(none_to_default(attributes[12], 0.0))
            self.Cdc = float(none_to_default(attributes[13], 0.0))
            self.Cdl = float(none_to_default(attributes[14], 0.0))
            self.Cdp = float(none_to_default(attributes[15], 0.0))
            self.Cds = float(none_to_default(attributes[16], 0.0))
            self.Cdt = float(none_to_default(attributes[17], 0.0))
            self.Cdw = float(none_to_default(attributes[18], 0.0))
            self.Cdy = float(none_to_default(attributes[19], 0.0))
            self.Ce = float(none_to_default(attributes[20], 0.0))
            self.Cf = float(none_to_default(attributes[21], 0.0))
            self.Cg = float(none_to_default(attributes[22], 0.0))
            self.Cg = float(none_to_default(attributes[23], 0.0))
            self.Cgl = float(none_to_default(attributes[24], 0.0))
            self.Cgp = float(none_to_default(attributes[25], 0.0))
            self.Cgs = float(none_to_default(attributes[26], 0.0))
            self.Cgt = float(none_to_default(attributes[27], 0.0))
            self.Cgv = float(none_to_default(attributes[28], 0.0))
            self.Ch = float(none_to_default(attributes[29], 0.0))
            self.Ci = float(none_to_default(attributes[30], 0.0))
            self.Ck = float(none_to_default(attributes[31], 0.0))
            self.Cl = float(none_to_default(attributes[32], 0.0))
            self.Clc = float(none_to_default(attributes[33], 0.0))
            self.Cm = float(none_to_default(attributes[34], 0.0))
            self.Cmu = float(none_to_default(attributes[35], 0.0))
            self.Cn = float(none_to_default(attributes[36], 0.0))
            self.Cnp = float(none_to_default(attributes[37], 0.0))
            self.Cnw = float(none_to_default(attributes[38], 0.0))
            self.Cp = float(none_to_default(attributes[39], 0.0))
            self.Cpd = float(none_to_default(attributes[40], 0.0))
            self.Cpf = float(none_to_default(attributes[41], 0.0))
            self.Cpv = float(none_to_default(attributes[42], 0.0))
            self.Cq = float(none_to_default(attributes[43], 0.0))
            self.Cr = float(none_to_default(attributes[44], 0.0))
            self.Crd = float(none_to_default(attributes[45], 0.0))
            self.Cs = float(none_to_default(attributes[46], 0.0))
            self.Csc = float(none_to_default(attributes[47], 0.0))
            self.Csf = float(none_to_default(attributes[48], 0.0))
            self.Cst = float(none_to_default(attributes[49], 0.0))
            self.Csv = float(none_to_default(attributes[50], 0.0))
            self.Csw = float(none_to_default(attributes[51], 0.0))
            self.Csz = float(none_to_default(attributes[52], 0.0))
            self.Ct = float(none_to_default(attributes[53], 0.0))
            self.Cv = float(none_to_default(attributes[54], 0.0))
            self.Cw = float(none_to_default(attributes[55], 0.0))
            self.Cy = float(none_to_default(attributes[56], 0.0))
        except IndexError as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKNSWC.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKNSWC attributes."

        return _error_code, _msg
