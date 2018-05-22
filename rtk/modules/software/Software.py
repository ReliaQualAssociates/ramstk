#!/usr/bin/env python
"""
################################
Software Package Software Module
################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.Software.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
except ImportError:  # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:  # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _calculate_application_risk(module):
    """
    Function to calculate Software risk due to application type.  This
    function uses a similar approach as RL-TR-92-52 for baseline fault
    density estimates.  The baseline application is Process Control
    software.  Every other application is ranked relative to Process
    Control using the values in RL-TR-92-52, Worksheet 0 for average fault
    density.

    Baseline (low) application risk (A) is assigned a 1.
    Medium risk is assigned a 2.
    High risk is assigned a 3.

    Application risks are defined as:

    +-------+------------------------------+----------+
    |       |                              | Relative |
    | Index |          Application         |   Risk   |
    +-------+------------------------------+----------+
    |   1   | Batch (General)              |   Low    |
    +-------+------------------------------+----------+
    |   2   | Event Control                |   Low    |
    +-------+------------------------------+----------+
    |   3   | Process Control              |   Low    |
    +-------+------------------------------+----------+
    |   4   | Procedure Control            |  Medium  |
    +-------+------------------------------+----------+
    |   5   | Navigation                   |   High   |
    +-------+------------------------------+----------+
    |   6   | Flight Dynamics              |   High   |
    +-------+------------------------------+----------+
    |   7   | Orbital Dynamics             |   High   |
    +-------+------------------------------+----------+
    |   8   | Message Processing           |  Medium  |
    +-------+------------------------------+----------+
    |   9   | Diagnostics                  |  Medium  |
    +-------+------------------------------+----------+
    |  10   | Sensor and Signal Processing |  Medium  |
    +-------+------------------------------+----------+
    |  11   | Simulation                   |   High   |
    +-------+------------------------------+----------+
    |  12   | Database Management          |  Medium  |
    +-------+------------------------------+----------+
    |  13   | Data Acquisition             |  Medium  |
    +-------+------------------------------+----------+
    |  14   | Data Presentation            |  Medium  |
    +-------+------------------------------+----------+
    |  15   | Decision and Planning Aids   |  Medium  |
    +-------+------------------------------+----------+
    |  16   | Pattern and Image Processing |   High   |
    +-------+------------------------------+----------+
    |  17   | System Software              |   High   |
    +-------+------------------------------+----------+
    |  18   | Development Tools            |   High   |
    +-------+------------------------------+----------+

    :param module: the :py:class:`rtk.software.CSCI.Model` or
                   :py:class:`rtk.software.Unit.Model` data model to calculate.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    if module.application_id == 0:
        module.a_risk = 0.0
    elif module.application_id in [5, 6, 7, 11, 16, 17, 18]:
        module.a_risk = 3.0
    elif module.application_id in [4, 8, 9, 10, 12, 13, 14, 15]:
        module.a_risk = 2.0
    else:
        module.a_risk = 1.0

    return False


def _calculate_development_risk(module):
    """
    Function to calculate Software risk due to the development environment.
    This function uses the results of RL-TR-92-52, Worksheet 1B to
    determine the relative risk level.  The percentage of development
    environment characteristics (Dc) applicable to the system under
    development determine the risk level.

        Baseline (medium) development risk (D) is assigned a 1.
        Low development risk (Dc > 0.9) is assigned a 0.5.
        High development risk (Dc < 0.5) is assigned a 2.

    :param module: the :py:class:`rtk.software.CSCI.Model` or
                   :py:class:`rtk.software.Unit.Model` data model to calculate.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    module.dc = sum(module.lst_development) / 43.0
    if module.dc < 0.5:  # High risk
        module.d_risk = 2.0
    elif module.dc > 0.9:  # Low risk
        module.d_risk = 0.5
    else:
        module.d_risk = 1.0

    return False


def _calculate_anomaly_risk(module):
    """
    Function to calculate Software risk due to anomaly management approach.

    For anomaly management risk (SA), this function uses the results of
    RL-TR-92-52, Worksheet 2A, 2B, 2C, or 2D to determine the relative risk
    level.  The risk is based on the percentage of anomaly management
    techniques used (AM).

        SA = 0.9 if AM > 0.6
        SA = 1.0 if 0.4 >= AM <= 0.6
        SA = 1.1 if AM < 0.4

    :param module: the :py:class:`rtk.software.CSCI.Model` or
                   :py:class:`rtk.software.Unit.Model` data model to calculate.
    :return: _error_code
    :rtype: int
    """
    # TODO: Consider re-writing _calculate_anomaly_risk; current McCabe Complexity metric = 10.
    _error_code = 0

    if module.phase_id == 2:  # Requirements review
        _ratios = [0, 0, 0]
        try:
            if (module.lst_anomaly_mgmt[0][1] /
                    module.lst_anomaly_mgmt[0][0]) == 1:
                _ratios[0] = 1
            if (module.lst_anomaly_mgmt[0][3] /
                    module.lst_anomaly_mgmt[0][2]) == 1:
                _ratios[1] = 1
            if (module.lst_anomaly_mgmt[0][6] /
                    module.lst_anomaly_mgmt[0][5]) == 1:
                _ratios[2] = 1
        except ZeroDivisionError:
            _error_code = 10

        _n_yes = module.lst_anomaly_mgmt[0][4] + \
                 sum(module.lst_anomaly_mgmt[0][7:]) + sum(_ratios)
        module.am = (19.0 - _n_yes) / 19.0

    elif module.phase_id == 3:  # Preliminary design review
        _n_yes = sum(module.lst_anomaly_mgmt[1][i] for i in range(14))
        module.am = (14.0 - _n_yes) / 14.0

    if module.am < 0.4:  # Low risk
        module.sa = 0.9
    elif module.am > 0.6:  # High risk
        module.sa = 1.1
    else:
        module.sa = 1.0

    return _error_code


def _calculate_traceability_risk(module):
    """
    Function to calculate Software risk due to requirements traceability.

    For requirements traceability risk (ST), this function uses the results
    of RL-TR-92-52, Worksheet 3B to determine the relative risk level.  The
    risk is based on whether or not requirements can be traced.

        ST = 1.0 if requirements can be traced
        ST = 1.1 otherwise

    :param module: the :py:class:`rtk.software.CSCI.Model` or
                   :py:class:`rtk.software.Unit.Model` data model to calculate.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """
    # TODO: Consider re-writing _calculate_traceability_risk; current McCabe Complexity metric = 10.
    if module.phase_id == 2:  # Requirements review
        if module.lst_traceability[0][0] == 1:  # Low risk
            module.st = 1.0
        else:
            module.st = 1.1

    elif module.phase_id == 3:  # Preliminary design review
        if module.lst_traceability[1][0] == 1:  # Low risk
            module.st = 1.0
        else:
            module.st = 1.1

    elif module.phase_id == 4:  # Critical design review
        if (module.lst_traceability[2][0] == 1
                and module.lst_traceability[2][1] == 1):  # Low risk
            module.st = 1.0
        else:
            module.st = 1.1

    return False


def _calculate_quality_risk(module):
    """
    Function to calculate Software risk due to software quality.

    For software quality risk (SQ), this function uses the results of
    RL-TR-92-52, Worksheet 4A to determine the relative risk level.  The
    risk is based on the percentage of quality control techniques used
    (DR).

        SQ = 1.0 if DR >= 0.5
        SQ = 1.1 if DR < 0.5

    :param module: the :py:class:`rtk.software.CSCI.Model` or
                   :py:class:`rtk.software.Unit.Model` data model to calculate.
    :return: _error_code
    :rtype: int
    """
    # WARNING: Refactor _calculate_quality_risk; current McCabe Complexity metric = 12.
    _error_code = 0

    if module.phase_id == 2:  # Requirements review
        _ratios = [0, 0]
        try:
            if module.lst_sftw_quality[0][9] / \
               module.lst_sftw_quality[0][8] == 1:
                _ratios[0] = 1
            if module.lst_sftw_quality[0][11] / \
               module.lst_sftw_quality[0][10] == 1:
                _ratios[1] = 1
        except ZeroDivisionError:
            _error_code = 10

        _n_yes = sum(module.lst_sftw_quality[0][:8]) + \
                 sum(module.lst_sftw_quality[0][12:]) + \
                 sum(_ratios)
        module.dr = (25.0 - _n_yes) / 25.0

    elif module.phase_id == 3:  # Preliminary design review
        _ratios = [0, 0, 0, 0, 0]
        try:
            if (module.lst_sftw_quality[1][3] /
                (module.lst_sftw_quality[1][2] + module.lst_sftw_quality[1][3])
                ) <= 0.3:
                _ratios[0] = 1
            if (module.lst_sftw_quality[1][7] /
                    module.lst_sftw_quality[1][6]) > 0.5:
                _ratios[1] = 1
            if (module.lst_sftw_quality[1][9] /
                    module.lst_sftw_quality[1][8]) > 0.5:
                _ratios[2] = 1
            if (module.lst_sftw_quality[1][11] /
                    module.lst_sftw_quality[1][10]) > 0.5:
                _ratios[3] = 1
            if (module.lst_sftw_quality[1][15] /
                    module.lst_sftw_quality[1][14]) > 0.75:
                _ratios[4] = 1
        except ZeroDivisionError:
            _error_code = 10

        _n_yes = sum(module.lst_sftw_quality[1][:2]) + \
                 sum(module.lst_sftw_quality[1][4:6]) + \
                 sum(module.lst_sftw_quality[1][12:14]) + \
                 sum(module.lst_sftw_quality[1][16:24]) + \
                 sum(_ratios)
        module.dr = (19.0 - _n_yes) / 19.0

    if module.dr < 0.5:  # High risk
        module.sq = 1.1
    else:
        module.sq = 1.0

    return _error_code


def _calculate_language_type_risk(module):
    """
    Function to calculate Software risk due to the programming language type.

    For language type risk (SL), this method uses the results of
    RL-TR-92-52, Worksheet 8D to determine the relative risk level.  The
    risk is based on the percentage of code written in a higher order
    language (HLOC) and the percentage of code written in an assembly
    language (ALOC).

    SL = (HLOC / SLOC) + (1.4 * ALOC / SLOC)

    :param module: the :py:class:`rtk.software.CSCI.Model` or
                   :py:class:`rtk.software.Unit.Model` data model to calculate.
    :return: _error_code
    :rtype: int
    """

    # Calculate the Language Type factor:
    #
    #   HLOC = SLOC - ALOC
    #   SL = HLOC / SLOC + 1.4 * ALOC / SLOC

    _error_code = 0

    module.hloc = module.sloc - module.aloc
    try:
        module.sl = (module.hloc / module.sloc) + \
                    (1.4 * module.aloc / module.sloc)
    except ZeroDivisionError:
        _error_code = 10
        module.sl = 1.4

    return _error_code


def _calculate_risk_reduction(module):
    """
    Function to calculate the risk reduction due to testing.  The algorithms
    used are based on the methodology presented in RL-TR-92-52, "SOFTWARE
    RELIABILITY, MEASUREMENT, AND TESTING Guidebook for Software
    Reliability Measurement and Testing."  Rather than attempting to
    estimate the software failure rate, RTK provides a risk index for the
    software based on the same factors used in RL-TR-92-52 for estimating
    software failure rates.  RTK also provides test planning guidance in
    the same manner as RL-TR-92-52.

    :param module: the :py:class:`rtk.software.CSCI.Model` or
                   :py:class:`rtk.software.Unit.Model` data model to calculate.

    :return: _error_code
    :rtype: int
    """
    # WARNING: Refactor _calculate_risk_reduction; current McCabe Complexity metric = 13.
    _error_code = 0

    # Calculate the risk reduction due to the test effort.
    try:
        if module.test_effort == 1:  # Labor hours
            _test_ratio = float(module.labor_hours_test) / \
                          float(module.labor_hours_dev)
        elif module.test_effort == 2:  # Budget
            _test_ratio = float(module.budget_test) / \
                          float(module.budget_dev)
        elif module.test_effort == 3:  # Schedule
            _test_ratio = float(module.schedule_test) / \
                          float(module.schedule_dev)
        else:
            _test_ratio = 1.0
    except ZeroDivisionError:
        _error_code = 10
        _test_ratio = 0.0

    module.te = 1.0
    if _test_ratio > 0.4:
        module.te = 0.9

    # Calculate the risk reduction due to test methods used.
    module.tm = 1.0
    module.tu = sum([_tu[0] for _tu in module.lst_test_selection])
    module.tt = sum([_tt[1] for _tt in module.lst_test_selection])
    try:
        if module.tu / module.tt > 0.75:
            module.tm = 0.9
        elif module.tu / module.tt < 0.5:
            module.tm = 1.1
    except ZeroDivisionError:
        _error_code = 10

    # Calculate the risk reduction due to test coverage.
    try:
        if module.level_id == 2:  # Module
            _VS = ((float(module.nm_test) / float(module.nm)) + (float(
                module.interfaces_test) / float(module.interfaces))) / 2.0
        elif module.level_id == 3:  # Unit
            _VS = ((float(module.branches_test) / float(module.branches)) +
                   (float(module.inputs_test) / float(module.inputs))) / 2.0
        else:
            _VS = 1.0
    except ZeroDivisionError:
        _error_code = 10
        _VS = 1.0

    module.tc = 1.0 / _VS

    module.t_risk = module.te * module.tm * module.tc

    return _error_code


def _calculate_reliability_estimation_number(module):
    """
    Function to calculate the reliability estimation number (REN) of the
    selected software module.  The methodology is outlined in RL-TR-92-52,
    Section 300.

    :param module: the :py:class:`rtk.software.CSCI.Model` or
                   :py:class:`rtk.software.Unit.Model` data model to calculate.

    :return: _error_code
    :rtype: int
    """

    _error_code = 0

    try:
        module.ew = module.et / float(module.et - module.os)
    except ZeroDivisionError:
        _error_code = 10

    module.ev = 0.1 + 4.5 * module.ec

    module.e_risk = module.ew * module.ev

    try:
        module.ft1 = module.dr_test / module.test_time
    except ZeroDivisionError:
        _error_code = 10

    try:
        module.ft2 = module.dr_eot / module.test_time_eot
    except ZeroDivisionError:
        _error_code = 10

    _T1 = 0.02 * module.t_risk
    _T2 = 0.14 * module.t_risk

    module.ren_avg = module.ft1 * _T1
    module.ren_eot = module.ft2 * _T2

    return _error_code


class Model(object):  # pylint: disable=R0902
    """
    The Software data model contains the attributes and methods of a Software
    item.  The Software class is a meta-class for the Assembly and Component
    classes.  A :py:class:`rtk.software.BoM.Model` will consist of one or more
    Software items.  The attributes of a Software item are:

    :ivar list lst_development: list to hold the answers to the development
                                environment questions.
    :ivar list lst_anomaly_mgmt: list to hold the answers to the anomaly
                                 management technique questions.
    :ivar list lst_traceability: list to hold the answers to the requirements
                                 traceability questions.
    :ivar list lst_sftw_quality: list to hold the answers to the software
                                 quality questions.
    :ivar list lst_modularity: list to hold the answers to the software
                               modularity questions.
    :ivar dict dicCSCI: dictionary of the CSCI data models that are children of
                        this data model.  Key is the Software ID; value is a
                        pointer to the CSCI data model instance.
    :ivar dict dicUnits: dictionary of the Unit data models that are children
                         of this data model.  Key is the Software ID; value is
                         a pointer to the Unit data model instance.
    :ivar int revision_id: the ID of the Revision the Software module is
                           associated with.
    :ivar int software_id: the ID of the Software module.
    :ivar int level_id: the index of the indenture level of the Software
                        module.  1 = System, 2 = CSCI, 3 = Unit.
    :ivar str description: the description of the Software module.
    :ivar int application_id: the index of the application type of the Software
                              module.
    :ivar int development_id: the index of the development phase of the
                              Software module.
    :ivar float a_risk: the application risk factor.
    :ivar float do: the fault density multiplier.
    :ivar int dd: the number of data items used in the Software module.
    :ivar float dc: the ratio of number of development tools used with the
                    Software module to all possible tools.
    :ivar float d_risk: the development environment risk factor.
    :ivar float am: the percent of anomaly management questions with 'Yes'
                    answers.
    :ivar float sa: the anomaly management factor.
    :ivar float st: the requirements traceability factor.
    :ivar float dr: the number of Software quality questions with 'No' answers.
    :ivar float sq: the quality review factor.
    :ivar float s1: the requirements and design representation metric.
                    S1 = SA * ST * SQ
    :ivar int hloc: the number of lines of code in the Software module written
                    in a higher-order language.
    :ivar int aloc: the number of lines of code in the Software module written
                    in assembly language.
    :ivar int sloc: the total number of lines of code in the Software module.
    :ivar float sl: the language type factor.
                    SL = HLOC / SLOC + 1.4 * ALOC / SLOC
    :ivar int ax: the number of modules with complexity >= 20.
    :ivar int bx: the number of modules with 7 <= complexity < 20.
    :ivar int cx: the number of modules with complexity < 7.
    :ivar int nm: the total number of modules in the Software module.
    :ivar float sx: the code complexity factor.
                    SX = (1.5 * AX + BX + 0.8 * CX) / NM
    :ivar int um: the number of modules with LOC <= 100.
    :ivar int wm: the number of modules with 100 < LOC <= 500.
    :ivar int xm: the number of modules with 500 < LOC.
    :ivar float sm: the code modularity factor.
                    SM = (0.9 * UM + WM + 2 * XM) / NM
    :ivar float df: the percentage of standards review questions with 'No'
                    answers.
    :ivar float sr: the standards review factor.
    :ivar float s2: the Software implementation metric.
                    S2 = SL * SX * SM * SR
    :ivar float rpfom: the calculated Reliability Prediction Figure of Merit.
    :ivar int parent_id: the Software ID of the parent Software module.
    :ivar int dev_assess_type: the index in development assessment type list.
    :ivar int phase_id: the index in the development phase list.
    :ivar int tcl: the index of the test confidence level.
    :ivar int test_path: the index in the test path list.
    :ivar int category: the index in the Software category list.
    :ivar int test_effort: the index in the test effort list.
    :ivar int test_approach: the index in the test approach list.
    :ivar float labor_hours_test: the number of labor hours dedicated to
                                  testing the Software module.
    :ivar float labor_hours_dev: the number of labor hours dedicated to
                                 developing the Software module.
    :ivar float budget_test: the money budgeted for testing the Software
                             module.
    :ivar float budget_dev: the money budgeted for developing the Software
                            module.
    :ivar float schedule_test: the calendar time dedicated to testing the
                               Software module.
    :ivar float schedule_dev: the calendar time dedicated to developing the
                              Software module.
    :ivar int branches: the number of branch statements in the Software module.
    :ivar int branches_test: the number of branch statements in the Software
                             module that will be tested.
    :ivar int inputs: the number of input variables to the Software module.
    :ivar int inputs_test: the number of input variables to the Software
                           module that will be tested.
    :ivar int nm_test: the number of Software units comprising the Software
                       CSCI that will be tested.
    :ivar int interfaces: the number of interfaces to other Software modules.
    :ivar int interfaces_test: the number of interfaces to other Software
                               modules that will be tested.
    :ivar float te: the test effort factor.
    :ivar float tm: the test methodology factor.
    :ivar float tc: the test coverage factor.
    :ivar float t_risk: the test risk factor.
    :ivar float ft1: the average failure rate during test.
    :ivar float ft2: the failure rate at the end of test.
    :ivar float ren_avg: the average reliability estimation number during test.
    :ivar float ren_eot: the reliability estimation number at end of test.
    :ivar float ec: the number of exception conditions in the Software module.
    :ivar float ev: the variability of input factor.
    :ivar float et: the total execution time of the Software module.
    :ivar float os: the operating system overhead time.
    :ivar float ew: the workload factor.
    :ivar e_risk: the operating environment risk factor.
    :ivar float failure_rate: the estimated failure rate of the Software
                              module.
    :ivar int units: the number of Software units comprising the Software CSCI.
    :ivar int units_test: the number of Software units comprising the Software
                          CSCI that will be tested.
    :ivar int cb: the number of conditional branches in the Software module.
    :ivar int ncb: the number of non-conditional branches in the Software
                   module.
    :ivar int dr_test: the number of discrepency reports crreated to date
                       during test.
    :ivar float test_time: the test time to date.
    :ivar int dr_eot: the total number of discrepency reports crreated at end
                      of test.
    :ivar float test_time_eot: the total test time at end of test.
    """

    def __init__(self):
        """
        Method to initialize a Software data model instance.
        """

        # Lists to hold the answers to the risk factor questions.  The values
        # are lists of 0 and 1 indicating the answer to No or Yes questions or
        # the value of numerical questions.
        self.lst_development = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        self.lst_anomaly_mgmt = [[
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0]]
        self.lst_traceability = [[0], [0], [0, 0]]
        self.lst_sftw_quality = [[
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0
        ], [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0
        ], [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0
        ], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.lst_modularity = [0, 0, 0, 0, 0, 0]
        self.lst_test_selection = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [
            0, 0
        ], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                   [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                   [0, 0], [0, 0]]

        # Define public dictionary attributes.
        self.dicCSCI = {}
        self.dicUnits = {}
        self.dicErrors = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.revision_id = None
        self.software_id = None
        self.level_id = 0
        self.description = ""
        self.application_id = 0
        self.development_id = 0
        self.a_risk = 0.0
        self.do = 0.0
        self.dd = 0
        self.dc = 0.0
        self.d_risk = 0.0
        self.am = 0.0
        self.sa = 0.0
        self.st = 0.0
        self.dr = 0.0
        self.sq = 0.0
        self.s1 = 0.0
        self.hloc = 0
        self.aloc = 0
        self.sloc = 0
        self.sl = 0.0
        self.ax = 0
        self.bx = 0
        self.cx = 0
        self.nm = 0
        self.sx = 0.0
        self.um = 0
        self.wm = 0
        self.xm = 0
        self.sm = 1.0
        self.df = 0.0
        self.sr = 0.0
        self.s2 = 0.0
        self.rpfom = 0.0
        self.parent_id = 0
        self.dev_assess_type = 0
        self.phase_id = 0
        self.tcl = 0
        self.test_path = 0
        self.category = 0
        self.test_effort = 0
        self.test_approach = 0
        self.labor_hours_test = 0.0
        self.labor_hours_dev = 0.0
        self.budget_test = 0.0
        self.budget_dev = 0.0
        self.schedule_test = 0.0
        self.schedule_dev = 0.0
        self.branches = 0
        self.branches_test = 0
        self.inputs = 0
        self.inputs_test = 0
        self.nm_test = 0
        self.interfaces = 0
        self.interfaces_test = 0
        self.te = 0.0
        self.tm = 0.0
        self.tc = 0.0
        self.t_risk = 0.0
        self.ft1 = 0.0
        self.ft2 = 0.0
        self.ren_avg = 0.0
        self.ren_eot = 0.0
        self.ec = 0.0
        self.ev = 0.0
        self.et = 0.0
        self.os = 0.0
        self.ew = 0.0
        self.e_risk = 0.0
        self.failure_rate = 0.0
        self.cb = 0
        self.ncb = 0
        self.dr_test = 0
        self.test_time = 0.0
        self.dr_eot = 0
        self.test_time_eot = 0.0
        self.units = 0
        self.units_test = 0

    def calculate(self, module):
        """
        Method to iterively calculate various software attributes.

        :param module: the :py:class:`rtk.software.CSCI.Model` or
                       :py:class:`rtk.software.Unit.Model` to calculate.
        :return: _error_codes
        :rtype: list
        """

        _error_codes = [0, 0, 0, 0, 0]

        # First we calculate all the software Units that are direct children of
        # the current CSCI.
        try:
            _units = module.dicUnits[module.software_id]
        except KeyError:
            _units = []

        for _unit in _units:
            self.dicErrors[_unit.software_id] = self.calculate(_unit)

            _unit.calculate_complexity_risk()
            _unit.calculate_modularity_risk()

            if _unit.phase_id in [4, 5]:
                _error_codes[0] = _calculate_anomaly_risk(module)
                _error_codes[1] = _calculate_quality_risk(module)
            if _unit.phase_id == 5:
                _error_codes[2] = _calculate_language_type_risk(module)

            _unit.s1 = _unit.sa * _unit.st * _unit.sq
            _unit.s2 = _unit.sl * _unit.sm * _unit.sx
            _unit.rpfom = _unit.a_risk * _unit.d_risk * _unit.s1 * _unit.s2

        # Next we calculate all the software CSCI that are direct children of
        # the current CSCI.
        try:
            _cscis = module.dicCSCI[module.software_id]
        except KeyError:
            _cscis = []

        for _csci in _cscis:
            self.dicErrors[_csci.software_id] = self.calculate(_csci)

            _csci.calculate_complexity_risk()
            _csci.calculate_modularity_risk()

            if _csci.phase_id in [2, 3, 4, 5]:
                _error_codes[0] = _calculate_anomaly_risk(module)
                _error_codes[1] = _calculate_quality_risk(module)
                _calculate_traceability_risk(module)
            if _csci.phase_id in [4, 5]:
                _error_codes[2] = _calculate_language_type_risk(module)

            _csci.s1 = _csci.sa * _csci.st * _csci.sq
            _csci.s2 = _csci.sl * _csci.sm * _csci.sx
            _csci.rpfom = _csci.a_risk * _csci.d_risk * _csci.s1 * _csci.s2

        _calculate_application_risk(module)
        _calculate_development_risk(module)

        _error_codes[3] = _calculate_risk_reduction(module)
        _error_codes[4] = _calculate_reliability_estimation_number(module)

        return _error_codes


class Software(object):
    """
    The Software data controller provides an interface between the Software
    data model and an RTK view model.  A single Software controller can manage
    one or more Software data models.
    """

    def __init__(self):
        """
        Method to initialize a Software data controller instance.
        """

        pass
