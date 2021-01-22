# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.data.storage.RAMSTKNSWC.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKNSWC Table Module."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseTable


# pylint: disable=R0902
class RAMSTKNSWC(RAMSTK_BASE, RAMSTKBaseTable):
    """Class to represent ramstk_nswc table in the RAMSTK Program database.

    This table shares a One-to-One relationship with ramstk_hardware.
    """

    __defaults__ = {
        'Cac': 0.0,
        'Calt': 0.0,
        'Cb': 0.0,
        'Cbl': 0.0,
        'Cbt': 0.0,
        'Cbv': 0.0,
        'Cc': 0.0,
        'Ccf': 0.0,
        'Ccp': 0.0,
        'Ccs': 0.0,
        'Ccv': 0.0,
        'Ccw': 0.0,
        'Cd': 0.0,
        'Cdc': 0.0,
        'Cdl': 0.0,
        'Cdp': 0.0,
        'Cds': 0.0,
        'Cdt': 0.0,
        'Cdw': 0.0,
        'Cdy': 0.0,
        'Ce': 0.0,
        'Cf': 0.0,
        'Cg': 0.0,
        'Cga': 0.0,
        'Cgl': 0.0,
        'Cgp': 0.0,
        'Cgs': 0.0,
        'Cgt': 0.0,
        'Cgv': 0.0,
        'Ch': 0.0,
        'Ci': 0.0,
        'Ck': 0.0,
        'Cl': 0.0,
        'Clc': 0.0,
        'Cm': 0.0,
        'Cmu': 0.0,
        'Cn': 0.0,
        'Cnp': 0.0,
        'Cnw': 0.0,
        'Cp': 0.0,
        'Cpd': 0.0,
        'Cpf': 0.0,
        'Cpv': 0.0,
        'Cq': 0.0,
        'Cr': 0.0,
        'Crd': 0.0,
        'Cs': 0.0,
        'Csc': 0.0,
        'Csf': 0.0,
        'Cst': 0.0,
        'Csv': 0.0,
        'Csw': 0.0,
        'Csz': 0.0,
        'Ct': 0.0,
        'Cv': 0.0,
        'Cw': 0.0,
        'Cy': 0.0
    }
    __tablename__ = 'ramstk_nswc'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False,
    )

    Cac = Column('fld_c_ac', Float, default=__defaults__['Cac'])
    Calt = Column('fld_c_alt', Float, default=__defaults__['Calt'])
    Cb = Column('fld_c_b', Float, default=__defaults__['Cb'])
    Cbl = Column('fld_c_bl', Float, default=__defaults__['Cbl'])
    Cbt = Column('fld_c_bt', Float, default=__defaults__['Cbt'])
    Cbv = Column('fld_c_bv', Float, default=__defaults__['Cbv'])
    Cc = Column('fld_c_c', Float, default=__defaults__['Cc'])
    Ccf = Column('fld_c_cf', Float, default=__defaults__['Ccf'])
    Ccp = Column('fld_c_cp', Float, default=__defaults__['Ccp'])
    Ccs = Column('fld_c_cs', Float, default=__defaults__['Ccs'])
    Ccv = Column('fld_c_cv', Float, default=__defaults__['Ccv'])
    Ccw = Column('fld_c_cw', Float, default=__defaults__['Ccw'])
    Cd = Column('fld_c_d', Float, default=__defaults__['Cd'])
    Cdc = Column('fld_c_dc', Float, default=__defaults__['Cdc'])
    Cdl = Column('fld_c_dl', Float, default=__defaults__['Cdl'])
    Cdp = Column('fld_c_dp', Float, default=__defaults__['Cdp'])
    Cds = Column('fld_c_ds', Float, default=__defaults__['Cds'])
    Cdt = Column('fld_c_dt', Float, default=__defaults__['Cdt'])
    Cdw = Column('fld_c_dw', Float, default=__defaults__['Cdw'])
    Cdy = Column('fld_c_dy', Float, default=__defaults__['Cdy'])
    Ce = Column('fld_c_e', Float, default=__defaults__['Ce'])
    Cf = Column('fld_c_f', Float, default=__defaults__['Cf'])
    Cg = Column('fld_c_g', Float, default=__defaults__['Cg'])
    Cga = Column('fld_c_ga', Float, default=__defaults__['Cga'])
    Cgl = Column('fld_c_gl', Float, default=__defaults__['Cgl'])
    Cgp = Column('fld_c_gp', Float, default=__defaults__['Cgp'])
    Cgs = Column('fld_c_gs', Float, default=__defaults__['Cgs'])
    Cgt = Column('fld_c_gt', Float, default=__defaults__['Cgt'])
    Cgv = Column('fld_c_gv', Float, default=__defaults__['Cgv'])
    Ch = Column('fld_c_h', Float, default=__defaults__['Ch'])
    Ci = Column('fld_c_i', Float, default=__defaults__['Ci'])
    Ck = Column('fld_c_k', Float, default=__defaults__['Ck'])
    Cl = Column('fld_c_l', Float, default=__defaults__['Cl'])
    Clc = Column('fld_c_lc', Float, default=__defaults__['Clc'])
    Cm = Column('fld_c_m', Float, default=__defaults__['Cm'])
    Cmu = Column('fld_c_mu', Float, default=__defaults__['Cmu'])
    Cn = Column('fld_c_n', Float, default=__defaults__['Cn'])
    Cnp = Column('fld_c_np', Float, default=__defaults__['Cnp'])
    Cnw = Column('fld_c_nw', Float, default=__defaults__['Cnw'])
    Cp = Column('fld_c_p', Float, default=__defaults__['Cp'])
    Cpd = Column('fld_c_pd', Float, default=__defaults__['Cpd'])
    Cpf = Column('fld_c_pf', Float, default=__defaults__['Cpf'])
    Cpv = Column('fld_c_pv', Float, default=__defaults__['Cpv'])
    Cq = Column('fld_c_q', Float, default=__defaults__['Cq'])
    Cr = Column('fld_c_r', Float, default=__defaults__['Cr'])
    Crd = Column('fld_c_rd', Float, default=__defaults__['Crd'])
    Cs = Column('fld_c_s', Float, default=__defaults__['Cs'])
    Csc = Column('fld_c_sc', Float, default=__defaults__['Csc'])
    Csf = Column('fld_c_sf', Float, default=__defaults__['Csf'])
    Cst = Column('fld_c_st', Float, default=__defaults__['Cst'])
    Csv = Column('fld_c_sv', Float, default=__defaults__['Csv'])
    Csw = Column('fld_c_sw', Float, default=__defaults__['Csw'])
    Csz = Column('fld_c_sz', Float, default=__defaults__['Csz'])
    Ct = Column('fld_c_t', Float, default=__defaults__['Ct'])
    Cv = Column('fld_c_v', Float, default=__defaults__['Cv'])
    Cw = Column('fld_c_w', Float, default=__defaults__['Cw'])
    Cy = Column('fld_c_y', Float, default=__defaults__['Cy'])

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware = relationship(  # type: ignore
        'RAMSTKHardware',
        back_populates='nswc',
    )

    def get_attributes(self):
        """Retrieve the current values of the RAMSTKNSWC data model attributes.

        :return: {hardware_id, Cac, Calt, Cb, Cbl, Cbt, Cbv, Cc, Ccf, Ccp, Ccs,
                  Ccv, Ccw, Cd, Cdc, Cdl, Cdp, Cds, Cdw, Cdy, Ce, Cf, Cg, Cga,
                  Cgl, Cgp, Cgs, Cgt, Cgv, Ch, Ci, Ck, Cl, Clc, Cm, Cmu, Cn,
                  Cnp, Cnw, Cp, Cpd, Cpf, Cpv, Cq, Cr, Crd, Cs, Csc, Csf, Cst,
                  Csv, Csw, Csz, Ct, Cv, Cw, Cy} pairs.
        :rtype: dict
        """
        _attributes = {
            'hardware_id': self.hardware_id,
            'Cac': self.Cac,
            'Calt': self.Calt,
            'Cb': self.Cb,
            'Cbl': self.Cbl,
            'Cbt': self.Cbt,
            'Cbv': self.Cbv,
            'Cc': self.Cc,
            'Ccf': self.Ccf,
            'Ccp': self.Ccp,
            'Ccs': self.Ccs,
            'Ccv': self.Ccv,
            'Ccw': self.Ccw,
            'Cd': self.Cd,
            'Cdc': self.Cdc,
            'Cdl': self.Cdl,
            'Cdp': self.Cdp,
            'Cds': self.Cds,
            'Cdt': self.Cdt,
            'Cdw': self.Cdw,
            'Cdy': self.Cdy,
            'Ce': self.Ce,
            'Cf': self.Cf,
            'Cg': self.Cg,
            'Cga': self.Cga,
            'Cgl': self.Cgl,
            'Cgp': self.Cgp,
            'Cgs': self.Cgs,
            'Cgt': self.Cgt,
            'Cgv': self.Cgv,
            'Ch': self.Ch,
            'Ci': self.Ci,
            'Ck': self.Ck,
            'Cl': self.Cl,
            'Clc': self.Clc,
            'Cm': self.Cm,
            'Cmu': self.Cmu,
            'Cn': self.Cn,
            'Cnp': self.Cnp,
            'Cnw': self.Cnw,
            'Cp': self.Cp,
            'Cpd': self.Cpd,
            'Cpf': self.Cpf,
            'Cpv': self.Cpv,
            'Cq': self.Cq,
            'Cr': self.Cr,
            'Crd': self.Crd,
            'Cs': self.Cs,
            'Csc': self.Csc,
            'Csf': self.Csf,
            'Cst': self.Cst,
            'Csv': self.Csv,
            'Csw': self.Csw,
            'Csz': self.Csz,
            'Ct': self.Ct,
            'Cv': self.Cv,
            'Cw': self.Cw,
            'Cy': self.Cy,
        }

        return _attributes
