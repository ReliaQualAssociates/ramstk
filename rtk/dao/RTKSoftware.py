#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKSoftware.py is part of The RTK Project
#
# All rights reserved.

"""
==============================
The RTKSoftware Table
==============================
"""

# Import the database models.
from sqlalchemy import Column, Float, ForeignKey, Integer, String
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


class RTKSoftware(Base):
    """
    Class to represent the table rtk_software in the RTK Program database.

    This table shares a Many-to-One relationship with rtk_revision.
    This table shares
    """

    __tablename__ = 'rtk_software'
    __table_args__ = {'extend_existing': True}

    revision_id = Column('fld_revision_id', Integer,
                         ForeignKey('rtk_revision.fld_revision_id'),
                         nullable=False)
    software_id = Column('fld_software_id', Integer, primary_key=True,
                         autoincrement=True, nullable=False)

    a = Column('fld_a', Float, default=0.0)
    aloc = Column('fld_aloc', Integer, default=0)
    am = Column('fld_am', Float, default=0.0)
    application_id = Column('fld_application_id', Integer, default=0)
    ax = Column('fld_ax', Integer, default=0)
    budget_test = Column('fld_budget_test', Float, default=0.0)
    budget_dev = Column('fld_budget_dev', Float, default=0.0)
    bx = Column('fld_bx', Integer, default=0)
    category_id = Column('fld_category_id', Integer, default=0)
    cb = Column('fld_cb', Integer, default=0)
    cx = Column('fld_cx', Integer, default=0)
    d = Column('fld_d', Float, default=0.0)
    dc = Column('fld_dc', Float, default=0.0)
    dd = Column('fld_dd', Integer, default=0)
    description = Column('fld_description', String(512), default='')
    development_id = Column('fld_development_id', Integer, default=0)
    dev_assess_type_id = Column('fld_dev_assess_type_id', Integer, default=0)
    df = Column('fld_df', Float, default=0.0)
    do = Column('fld_do', Float, default=0.0)
    dr = Column('fld_dr', Float, default=0.0)
    dr_eot = Column('fld_dr_eot', Integer, default=0)
    dr_test = Column('fld_dr_test', Integer, default=0)
    e = Column('fld_e', Float, default=0.0)
    ec = Column('fld_ec', Float, default=0.0)
    et = Column('fld_et', Float, default=0.0)
    ev = Column('fld_ev', Float, default=0.0)
    ew = Column('fld_ew', Float, default=0.0)
    f = Column('fld_f', Float, default=0.0)
    ft1 = Column('fld_ft1', Float, default=0.0)
    ft2 = Column('fld_ft2', Float, default=0.0)
    hloc = Column('fld_hloc', Integer, default=0)
    labor_hours_dev = Column('fld_hours_dev', Float, default=0.0)
    labor_hours_test = Column('fld_hours_test', Float, default=0.0)
    level = Column('fld_level', Integer, default=0)
    loc = Column('fld_loc', Integer, default=0)
    n_branches = Column('fld_n_branches', Integer, default=0)
    n_branches_test = Column('fld_n_branches_test', Integer, default=0)
    n_inputs = Column('fld_n_inputs', Integer, default=0)
    n_inputs_test = Column('fld_n_inputs_test', Integer, default=0)
    n_interfaces = Column('fld_n_interfaces', Integer, default=0)
    n_interfaces_test = Column('fld_n_interfaces_test', Integer, default=0)
    ncb = Column('fld_ncb', Integer, default=0)
    nm = Column('fld_nm', Integer, default=0)
    nm_test = Column('fld_nm_test', Integer, default=0)
    os = Column('fld_os', Float, default=0.0)
    parent_id = Column('fld_parent_id', Integer, default=0)
    phase_id = Column('fld_phase_id', Integer, default=0)
    ren_avg = Column('fld_ren_avg', Float, default=0.0)
    ren_eot = Column('fld_ren_eot', Float, default=0.0)
    rpfom = Column('fld_rpfom', Float, default=0.0)
    s1 = Column('fld_s1', Float, default=0.0)
    s2 = Column('fld_s2', Float, default=0.0)
    sa = Column('fld_sa', Float, default=0.0)
    schedule_dev = Column('fld_schedule_dev', Float, default=0.0)
    schedule_test = Column('fld_schedule_test', Float, default=0.0)
    sl = Column('fld_sl', Float, default=0.0)
    sm = Column('fld_sm', Float, default=0.0)
    sq = Column('fld_sq', Float, default=0.0)
    sr = Column('fld_sr', Float, default=0.0)
    st = Column('fld_st', Float, default=0.0)
    sx = Column('fld_sx', Float, default=0.0)
    t = Column('fld_t', Float, default=0.0)
    tc = Column('fld_tc', Float, default=0.0)
    tcl = Column('fld_tcl', Integer, default=0)
    te = Column('fld_te', Float, default=0.0)
    test_approach = Column('fld_test_approach', Integer, default=0)
    test_effort = Column('fld_test_effort', Integer, default=0)
    test_path = Column('fld_test_path', Integer, default=0)
    test_time = Column('fld_test_time', Float, default=0.0)
    test_time_eot = Column('fld_test_time_eot', Float, default=0.0)
    tm = Column('fld_tm', Float, default=0.0)
    um = Column('fld_um', Integer, default=0)
    wm = Column('fld_wm', Integer, default=0)
    xm = Column('fld_xm', Integer, default=0)

    # Define the relationships to other tables in the RTK Program database.
    revision = relationship('RTKRevision', back_populates='software')
    development = relationship('RTKSoftwareDevelopment',
                               back_populates='software')
    review = relationship('RTKSoftwareReview', back_populates='software')
    software_test = relationship('RTKSoftwareTest', back_populates='software')

    def get_attributes(self):
        """
        Method to retrieve the current values of the RTKSoftware data model
        attributes.

        :return: (revision_id, software_id, a, aloc, am, application_id, ax,
                  budget_test, budget_dev, bx, category_id, cb, cx, d, dc, dd,
                  description, development_id, dev_assess_type_id, df, do, dr,
                  dr_eot, dr_test, e, ec, et, ev, ew, f, ft1, ft2, hloc,
                  labor_hours_dev, labor_hours_test, level, loc, n_branches,
                  n_branches_test, n_inputs, n_inputs_test, n_interfaces,
                  n_interfaces_test, ncb, nm, nm_test, os, parent_id, phase_id,
                  ren_avg, ren_eot, rpfom, s1, s2, sa, schedule_dev,
                  schedule_test, sl, sm, sq, sr, st, sx, t, tc, tcl, te,
                  test_approach, test_effort, test_path, test_time,
                  test_time_eot, tm, um, wm, xm)
        :rtype: tuple
        """

        _attributes = (self.revision_id, self.software_id, self.a, self.aloc,
                       self.am, self.application_id, self.ax, self.budget_test,
                       self.budget_dev, self.bx, self.category_id, self.cb,
                       self.cx, self.d, self.dc, self.dd, self.description,
                       self.development_id, self.dev_assess_type_id, self.df,
                       self.do, self.dr, self.dr_eot, self.dr_test, self.e,
                       self.ec, self.et, self.ev, self.ew, self.f, self.ft1,
                       self.ft2, self.hloc, self.labor_hours_dev,
                       self.labor_hours_test, self.level, self.loc,
                       self.n_branches, self.n_branches_test, self.n_inputs,
                       self.n_inputs_test, self.n_interfaces,
                       self.n_interfaces_test, self.ncb, self.nm, self.nm_test,
                       self.os, self.parent_id, self.phase_id, self.ren_avg,
                       self.ren_eot, self.rpfom, self.s1, self.s2, self.sa,
                       self.schedule_dev, self.schedule_test, self.sl, self.sm,
                       self.sq, self.sr, self.st, self.sx, self.t, self.tc,
                       self.tcl, self.te, self.test_approach, self.test_effort,
                       self.test_path, self.test_time, self.test_time_eot,
                       self.tm, self.um, self.wm, self.xm)

        return _attributes

    def set_attributes(self, attributes):
        """
        Method to set the RTKSoftware data model attributes.

        :param tuple attributes: tuple of values to assign to the instance
                                 attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating RTKSoftware {0:d} attributes.". \
               format(self.software_id)

        try:
            self.a = float(attributes[0])
            self.aloc = int(attributes[1])
            self.am = float(attributes[2])
            self.application_id = int(attributes[3])
            self.ax = int(attributes[4])
            self.budget_test = float(attributes[5])
            self.budget_dev = float(attributes[6])
            self.bx = int(attributes[7])
            self.category_id = int(attributes[8])
            self.cb = int(attributes[9])
            self.cx = int(attributes[10])
            self.d = float(attributes[11])
            self.dc = float(attributes[12])
            self.dd = int(attributes[13])
            self.description = str(attributes[14])
            self.development_id = int(attributes[15])
            self.dev_assess_type_id = int(attributes[16])
            self.df = float(attributes[17])
            self.do = float(attributes[18])
            self.dr = float(attributes[19])
            self.dr_eot = int(attributes[20])
            self.dr_test = int(attributes[21])
            self.e = float(attributes[22])
            self.ec = float(attributes[23])
            self.et = float(attributes[24])
            self.ev = float(attributes[25])
            self.ew = float(attributes[26])
            self.f = float(attributes[27])
            self.ft1 = float(attributes[28])
            self.ft2 = float(attributes[29])
            self.hloc = int(attributes[30])
            self.labor_hours_dev = float(attributes[31])
            self.labor_hours_test = float(attributes[32])
            self.level = int(attributes[33])
            self.loc = int(attributes[34])
            self.n_branches = int(attributes[35])
            self.n_branches_test = int(attributes[36])
            self.n_inputs = int(attributes[37])
            self.n_inputs_test = int(attributes[38])
            self.n_interfaces = int(attributes[39])
            self.n_interfaces_test = int(attributes[40])
            self.ncb = int(attributes[41])
            self.nm = int(attributes[42])
            self.nm_test = int(attributes[43])
            self.os = float(attributes[44])
            self.parent_id = int(attributes[45])
            self.phase_id = int(attributes[46])
            self.ren_avg = float(attributes[47])
            self.ren_eot = float(attributes[48])
            self.rpfom = float(attributes[49])
            self.s1 = float(attributes[50])
            self.s2 = float(attributes[51])
            self.sa = float(attributes[52])
            self.schedule_dev = float(attributes[53])
            self.schedule_test = float(attributes[54])
            self.sl = float(attributes[55])
            self.sm = float(attributes[56])
            self.sq = float(attributes[57])
            self.sr = float(attributes[58])
            self.st = float(attributes[59])
            self.sx = float(attributes[60])
            self.t = float(attributes[61])
            self.tc = float(attributes[62])
            self.tcl = int(attributes[63])
            self.te = float(attributes[64])
            self.test_approach = int(attributes[65])
            self.test_effort = int(attributes[66])
            self.test_path = int(attributes[67])
            self.test_time = float(attributes[68])
            self.test_time_eot = float(attributes[69])
            self.tm = float(attributes[70])
            self.um = int(attributes[71])
            self.wm = int(attributes[72])
            self.xm = int(attributes[73])
        except IndexError as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Insufficient number of input values to " \
                   "RTKSoftware.set_attributes()."
        except (TypeError, ValueError) as _err:
            _error_code = Utilities.error_handler(_err.args)
            _msg = "RTK ERROR: Incorrect data type when converting one or " \
                   "more RTKSoftware attributes."

        return _error_code, _msg
