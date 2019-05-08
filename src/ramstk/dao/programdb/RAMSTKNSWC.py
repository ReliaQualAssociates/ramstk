# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKNSWC.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKNSWC Table Module."""

from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

# Import other RAMSTK modules.
from ramstk.Utilities import none_to_default
from ramstk.dao.RAMSTKCommonDB import RAMSTK_BASE


# pylint: disable=R0902
class RAMSTKNSWC(RAMSTK_BASE):
    """
    Class to represent ramstk_nswc table in the RAMSTK Program database.

    This table shares a One-to-One relationship with ramstk_hardware.
    """

    __tablename__ = 'ramstk_nswc'
    __table_args__ = {'extend_existing': True}

    hardware_id = Column(
        'fld_hardware_id',
        Integer,
        ForeignKey('ramstk_hardware.fld_hardware_id'),
        primary_key=True,
        nullable=False)

    Cac = Column('fld_c_ac', Float, default=0.0)
    Calt = Column('fld_c_alt', Float, default=0.0)
    Cb = Column('fld_c_b', Float, default=0.0)  # pylint: disable=C0103
    Cbl = Column('fld_c_bl', Float, default=0.0)
    Cbt = Column('fld_c_bt', Float, default=0.0)
    Cbv = Column('fld_c_bv', Float, default=0.0)
    Cc = Column('fld_c_c', Float, default=0.0)  # pylint: disable=C0103
    Ccf = Column('fld_c_cf', Float, default=0.0)
    Ccp = Column('fld_c_cp', Float, default=0.0)
    Ccs = Column('fld_c_cs', Float, default=0.0)
    Ccv = Column('fld_c_cv', Float, default=0.0)
    Ccw = Column('fld_c_cw', Float, default=0.0)
    Cd = Column('fld_c_d', Float, default=0.0)  # pylint: disable=C0103
    Cdc = Column('fld_c_dc', Float, default=0.0)
    Cdl = Column('fld_c_dl', Float, default=0.0)
    Cdp = Column('fld_c_dp', Float, default=0.0)
    Cds = Column('fld_c_ds', Float, default=0.0)
    Cdt = Column('fld_c_dt', Float, default=0.0)
    Cdw = Column('fld_c_dw', Float, default=0.0)
    Cdy = Column('fld_c_dy', Float, default=0.0)
    Ce = Column('fld_c_e', Float, default=0.0)  # pylint: disable=C0103
    Cf = Column('fld_c_f', Float, default=0.0)  # pylint: disable=C0103
    Cg = Column('fld_c_g', Float, default=0.0)  # pylint: disable=C0103
    Cga = Column('fld_c_ga', Float, default=0.0)
    Cgl = Column('fld_c_gl', Float, default=0.0)
    Cgp = Column('fld_c_gp', Float, default=0.0)
    Cgs = Column('fld_c_gs', Float, default=0.0)
    Cgt = Column('fld_c_gt', Float, default=0.0)
    Cgv = Column('fld_c_gv', Float, default=0.0)
    Ch = Column('fld_c_h', Float, default=0.0)  # pylint: disable=C0103
    Ci = Column('fld_c_i', Float, default=0.0)  # pylint: disable=C0103
    Ck = Column('fld_c_k', Float, default=0.0)  # pylint: disable=C0103
    Cl = Column('fld_c_l', Float, default=0.0)  # pylint: disable=C0103
    Clc = Column('fld_c_lc', Float, default=0.0)
    Cm = Column('fld_c_m', Float, default=0.0)  # pylint: disable=C0103
    Cmu = Column('fld_c_mu', Float, default=0.0)
    Cn = Column('fld_c_n', Float, default=0.0)  # pylint: disable=C0103
    Cnp = Column('fld_c_np', Float, default=0.0)
    Cnw = Column('fld_c_nw', Float, default=0.0)
    Cp = Column('fld_c_p', Float, default=0.0)  # pylint: disable=C0103
    Cpd = Column('fld_c_pd', Float, default=0.0)
    Cpf = Column('fld_c_pf', Float, default=0.0)
    Cpv = Column('fld_c_pv', Float, default=0.0)
    Cq = Column('fld_c_q', Float, default=0.0)  # pylint: disable=C0103
    Cr = Column('fld_c_r', Float, default=0.0)  # pylint: disable=C0103
    Crd = Column('fld_c_rd', Float, default=0.0)
    Cs = Column('fld_c_s', Float, default=0.0)  # pylint: disable=C0103
    Csc = Column('fld_c_sc', Float, default=0.0)
    Csf = Column('fld_c_sf', Float, default=0.0)
    Cst = Column('fld_c_st', Float, default=0.0)
    Csv = Column('fld_c_sv', Float, default=0.0)
    Csw = Column('fld_c_sw', Float, default=0.0)
    Csz = Column('fld_c_sz', Float, default=0.0)
    Ct = Column('fld_c_t', Float, default=0.0)  # pylint: disable=C0103
    Cv = Column('fld_c_v', Float, default=0.0)  # pylint: disable=C0103
    Cw = Column('fld_c_w', Float, default=0.0)  # pylint: disable=C0103
    Cy = Column('fld_c_y', Float, default=0.0)  # pylint: disable=C0103

    # Define the relationships to other tables in the RAMSTK Program database.
    hardware = relationship('RAMSTKHardware', back_populates='nswc')

    def get_attributes(self):
        """
        Retrieve the current values of the RAMSTKNSWC data model attributes.

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
            'Cy': self.Cy
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set the current values of the RAMSTKNSWC data model attributes.

        :param dict attributes: dict of values to assign to the instance
                                attributes.
        :return: (_error_code, _msg); the error code and error message.
        :rtype: tuple
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating RAMSTKNSWC {0:d} attributes.". \
               format(self.hardware_id)

        try:
            self.Cac = float(none_to_default(attributes['Cac'], 0.0))
            self.Calt = float(none_to_default(attributes['Calt'], 0.0))
            self.Cb = float(none_to_default(attributes['Cb'], 0.0))
            self.Cbl = float(none_to_default(attributes['Cbl'], 0.0))
            self.Cbt = float(none_to_default(attributes['Cbt'], 0.0))
            self.Cbv = float(none_to_default(attributes['Cbv'], 0.0))
            self.Cc = float(none_to_default(attributes['Cc'], 0.0))
            self.Ccf = float(none_to_default(attributes['Ccf'], 0.0))
            self.Ccp = float(none_to_default(attributes['Ccp'], 0.0))
            self.Ccs = float(none_to_default(attributes['Ccs'], 0.0))
            self.Ccv = float(none_to_default(attributes['Ccv'], 0.0))
            self.Ccw = float(none_to_default(attributes['Ccw'], 0.0))
            self.Cd = float(none_to_default(attributes['Cd'], 0.0))
            self.Cdc = float(none_to_default(attributes['Cdc'], 0.0))
            self.Cdl = float(none_to_default(attributes['Cdl'], 0.0))
            self.Cdp = float(none_to_default(attributes['Cdp'], 0.0))
            self.Cds = float(none_to_default(attributes['Cds'], 0.0))
            self.Cdt = float(none_to_default(attributes['Cdt'], 0.0))
            self.Cdw = float(none_to_default(attributes['Cdw'], 0.0))
            self.Cdy = float(none_to_default(attributes['Cdy'], 0.0))
            self.Ce = float(none_to_default(attributes['Ce'], 0.0))
            self.Cf = float(none_to_default(attributes['Cf'], 0.0))
            self.Cg = float(none_to_default(attributes['Cg'], 0.0))
            self.Cga = float(none_to_default(attributes['Cga'], 0.0))
            self.Cgl = float(none_to_default(attributes['Cgl'], 0.0))
            self.Cgp = float(none_to_default(attributes['Cgp'], 0.0))
            self.Cgs = float(none_to_default(attributes['Cgs'], 0.0))
            self.Cgt = float(none_to_default(attributes['Cgt'], 0.0))
            self.Cgv = float(none_to_default(attributes['Cgv'], 0.0))
            self.Ch = float(none_to_default(attributes['Ch'], 0.0))
            self.Ci = float(none_to_default(attributes['Ci'], 0.0))
            self.Ck = float(none_to_default(attributes['Ck'], 0.0))
            self.Cl = float(none_to_default(attributes['Cl'], 0.0))
            self.Clc = float(none_to_default(attributes['Clc'], 0.0))
            self.Cm = float(none_to_default(attributes['Cm'], 0.0))
            self.Cmu = float(none_to_default(attributes['Cmu'], 0.0))
            self.Cn = float(none_to_default(attributes['Cn'], 0.0))
            self.Cnp = float(none_to_default(attributes['Cnp'], 0.0))
            self.Cnw = float(none_to_default(attributes['Cnw'], 0.0))
            self.Cp = float(none_to_default(attributes['Cp'], 0.0))
            self.Cpd = float(none_to_default(attributes['Cpd'], 0.0))
            self.Cpf = float(none_to_default(attributes['Cpf'], 0.0))
            self.Cpv = float(none_to_default(attributes['Cpv'], 0.0))
            self.Cq = float(none_to_default(attributes['Cq'], 0.0))
            self.Cr = float(none_to_default(attributes['Cr'], 0.0))
            self.Crd = float(none_to_default(attributes['Crd'], 0.0))
            self.Cs = float(none_to_default(attributes['Cs'], 0.0))
            self.Csc = float(none_to_default(attributes['Csc'], 0.0))
            self.Csf = float(none_to_default(attributes['Csf'], 0.0))
            self.Cst = float(none_to_default(attributes['Cst'], 0.0))
            self.Csv = float(none_to_default(attributes['Csv'], 0.0))
            self.Csw = float(none_to_default(attributes['Csw'], 0.0))
            self.Csz = float(none_to_default(attributes['Csz'], 0.0))
            self.Ct = float(none_to_default(attributes['Ct'], 0.0))
            self.Cv = float(none_to_default(attributes['Cv'], 0.0))
            self.Cw = float(none_to_default(attributes['Cw'], 0.0))
            self.Cy = float(none_to_default(attributes['Cy'], 0.0))
        except KeyError as _err:
            _error_code = 40
            _msg = "RAMSTK ERROR: Missing attribute {0:s} in attribute " \
                   "dictionary passed to " \
                   "RAMSTKNSWC.set_attributes().".format(str(_err))

        return _error_code, _msg
