#!/usr/bin/env python
"""
################################
Software Package Software Module
################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.software.Software.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    import rtk.utilities as _util

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Converts string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code

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

    :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.

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

    :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    module.dc = sum(module.lst_development) / 43.0
    if module.dc < 0.5:                     # High risk
        module.d_risk = 2.0
    elif module.dc > 0.9:                   # Low risk
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

    :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    if module.phase_id == 2:                # Requirements review
        _ratios = [0, 0, 0]
        try:
            if module.lst_anomaly_mgmt[0][1] / \
                module.lst_anomaly_mgmt[0][0] == 1:
                _ratios[0] = 1
            if module.lst_anomaly_mgmt[0][3] / \
                module.lst_anomaly_mgmt[0][2] == 1:
                _ratios[1] = 1
            if module.lst_anomaly_mgmt[0][6] / \
                module.lst_anomaly_mgmt[0][5] == 1:
                _ratios[2] = 1
        except ZeroDivisionError:
            _util.rtk_error(_(u"Attempted to divide by zero when "
                              u"calculating the anomaly management risk "
                              u"for {0:s}.  Perhaps you forgot to answer one "
                              u"or more questions.").format(
                                  module.description))

        _n_yes = module.lst_anomaly_mgmt[0][4] + \
                 sum(module.lst_anomaly_mgmt[0][7:]) + sum(_ratios)
        module.am = (19.0 - _n_yes) / 19.0

    elif module.phase_id == 3:              # Preliminary design review
        _n_yes = sum(module.lst_anomaly_mgmt[1][i] for i in range(14))
        module.am = (14.0 - _n_yes) / 14.0

    if module.am < 0.4:                     # Low risk
        module.sa = 0.9
    elif module.am > 0.6:                   # High risk
        module.sa = 1.1
    else:
        module.sa = 1.0

    return False

def _calculate_traceability_risk(module):
    """
    Function to calculate Software risk due to requirements traceability.

    For requirements traceability risk (ST), this function uses the results
    of RL-TR-92-52, Worksheet 3B to determine the relative risk level.  The
    risk is based on whether or not requirements can be traced.

        ST = 1.0 if requirements can be traced
        ST = 1.1 otherwise

    :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    if module.phase_id == 2:            # Requirements review
        if module.lst_traceability[0][0] == 1:  # Low risk
            module.st = 1.0
        else:
            module.st = 1.1

    elif module.phase_id == 3:          # Preliminary design review
        if module.lst_traceability[1][0] == 1:  # Low risk
            module.st = 1.0
        else:
            module.st = 1.1

    elif module.phase_id == 4:          # Critical design review
        if(module.lst_traceability[2][0] == 1 and
           module.lst_traceability[2][1] == 1):     # Low risk
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

    :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    if module.phase_id == 2:                # Requirements review
        _ratios = [0, 0]
        try:
            if module.lst_sftw_quality[0][9] / \
               module.lst_sftw_quality[0][8] == 1:
                _ratios[0] = 1
            if module.lst_sftw_quality[0][11] / \
               module.lst_sftw_quality[0][10] == 1:
                _ratios[1] = 1
        except ZeroDivisionError:
            _util.rtk_error(_(u"Attempted to divide by zero when "
                              u"calculating the software quality risk for "
                              u"{0:s}.  Perhaps you forgot to answer one or "
                              u"more questions.").format(module.description))

        _n_yes = sum(module.lst_sftw_quality[0][:8]) + \
                 sum(module.lst_sftw_quality[0][12:]) + \
                 sum(_ratios)
        module.dr = (25.0 - _n_yes) / 25.0

    elif module.phase_id == 3:              # Preliminary design review
        _ratios = [0, 0, 0, 0, 0]
        try:
            if module.lst_sftw_quality[1][3] / \
               (module.lst_sftw_quality[1][2] +
                module.lst_sftw_quality[1][3]) <= 0.3:
                _ratios[0] = 1
            if module.lst_sftw_quality[1][7] / \
               module.lst_sftw_quality[1][6] > 0.5:
                _ratios[1] = 1
            if module.lst_sftw_quality[1][9] / \
               module.lst_sftw_quality[1][8] > 0.5:
                _ratios[2] = 1
            if module.lst_sftw_quality[1][11] / \
               module.lst_sftw_quality[1][10] > 0.5:
                _ratios[3] = 1
            if module.lst_sftw_quality[1][15] / \
               module.lst_sftw_quality[1][14] > 0.75:
                _ratios[4] = 1
        except ZeroDivisionError:
            _util.rtk_error(_(u"Attempted to divide by zero when "
                              u"calculating the software quality risk for "
                              u"{0:s}.  Perhaps you forgot to answer one "
                              u"or more questions.").format(
                                  module.description))

        _n_yes = sum(module.lst_sftw_quality[1][:2]) + \
                 sum(module.lst_sftw_quality[1][4:6]) + \
                 sum(module.lst_sftw_quality[1][12:14]) + \
                 sum(module.lst_sftw_quality[1][16:24]) + \
                 sum(_ratios)
        module.dr = (19.0 - _n_yes) / 19.0

    if module.dr < 0.5:                     # High risk
        module.sq = 1.1
    else:
        module.sq = 1.0

    return False

def _calculate_language_type_risk(module):
    """
    Function to calculate Software risk due to the programming language type.

    For language type risk (SL), this method uses the results of
    RL-TR-92-52, Worksheet 8D to determine the relative risk level.  The
    risk is based on the percentage of code written in a higher order
    language (HLOC) and the percentage of code written in an assembly
    language (ALOC).

    SL = (HLOC / SLOC) + (1.4 * ALOC / SLOC)

    :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    # Calculate the Language Type factor:
    #
    #   HLOC = SLOC - ALOC
    #   SL = HLOC / SLOC + 1.4 * ALOC / SLOC
    module.hloc = module.sloc - module.aloc
    try:
        module.sl = (module.hloc / module.sloc) + \
                    (1.4 * module.aloc / module.sloc)
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when calculating "
                          u"the software language risk for {0:s}.  Perhaps "
                          u"you forgot to answer one or more "
                          u"questions.").format(module.description))
        module.sl = 1.4

    return False

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

    :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    # Calculate the risk reduction due to the test effort.
    try:
        if module.test_effort == 1:         # Labor hours
            _test_ratio = float(module.labor_hours_test) / \
                          float(module.labor_hours_dev)
        elif module.test_effort == 2:       # Budget
            _test_ratio = float(module.budget_test) / \
                          float(module.budget_dev)
        elif module.test_effort == 3:       # Schedule
            _test_ratio = float(module.schedule_test) / \
                          float(module.schedule_dev)
        else:
            _test_ratio = 1.0
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when "
                          u"calculating the test effort risk "
                          u"reduction for {0:s}.  Perhaps you forgot "
                          u"to answer one or more questions.").format(
                              module.description))

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
        _util.rtk_error(_(u"Attempted to divide by zero when "
                          u"calculating the test method risk "
                          u"reduction for {0:s}.  Perhaps you forgot "
                          u"to answer one or more questions.").format(
                              module.description))

    # Calculate the risk reduction due to test coverage.
    try:
        if module.level_id == 2:            # Module
            _VS = ((float(module.nm_test) / float(module.nm)) + \
                   (float(module.interfaces_test) / \
                    float(module.interfaces))) / 2.0
        elif module.level_id == 3:          # Unit
            _VS = ((float(module.branches_test) / float(module.branches)) + \
                   (float(module.inputs_test) / float(module.inputs))) / 2.0
        else:
            _VS = 1.0
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when "
                          u"calculating the test coverage risk "
                          u"reduction for {0:s}.  Perhaps you forgot "
                          u"to answer one or more questions.").format(
                              module.description))
        _VS = 1.0
    module.tc = 1.0 / _VS

    module.t_risk = module.te * module.tm * module.tc

    return False

def _calculate_reliability_estimation_number(module):
    """
    Function to calculate the reliability estimation number (REN) of the
    selected software module.  The methodology is outlined in RL-TR-92-52,
    Section 300.

    :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    try:
        module.ew = module.et / float(module.et - module.os)
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when calculating "
                          u"the workload for {0:s}.  Perhaps you forgot "
                          u"to provide one or more inputs.").format(
                              module.description))

    module.ev = 0.1 + 4.5 * module.ec

    module.e_risk = module.ew * module.ev

    try:
        module.ft1 = module.dr_test / module.test_time
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when calculating "
                          u"the average failure rate during test for "
                          u"{0:s}.  Perhaps you forgot to provide one or "
                          u"more inputs.").format(module.description))
    try:
        module.ft2 = module.dr_eot / module.test_time_eot
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when calculating "
                          u"the average failure rate at end of test for "
                          u"{0:s}.  Perhaps you forgot to provide one or "
                          u"more inputs.").format(module.description))

    _T1 = 0.02 * module.t_risk
    _T2 = 0.14 * module.t_risk

    module.ren_avg = module.ft1 * _T1
    module.ren_eot = module.ft2 * _T2

    return False

# TODO: Fix all docstrings; copy-paste errors.
class Model(object):                        # pylint: disable=R0902
    """
    The Software data model contains the attributes and methods of a Software
    item.  The Software class is a meta-class for the Assembly and Component
    classes.  A :class:`rtk.software.BoM` will consist of one or more Software
    items.  The attributes of a Software item are:

    :ivar lst_development: list to hold the answers to the development
                           environment questions.
    :ivar lst_anomaly_mgmt: list to hold the answers to the anomaly management
                            technique questions.
    :ivar lst_traceability: list to hold the answers to the requirements
                            traceability questions.
    :ivar lst_sftw_quality: list to hold the answers to the software quality
                            questions.
    :ivar lst_modularity: list to hold the answers to the software modularity
                          questions.

    :ivar dicCSCI: dictionary of the CSCI data models that are children of this
                   data model.  Key is the Software ID; value is a pointer to
                   the CSCI data model instance.
    :ivar dicUnits: dictionary of the Unit data models that are children
                    of this data model.  Key is the Software ID; value is a
                    pointer to the Unit data model instance.

    :ivar revision_id: ID of the Revision the software module is associated with. default value: None
    :ivar software_id: default value: None
    :ivar level_id: default value: 0
    :ivar description: default value: ""
    :ivar application_id: default value: 0
    :ivar development_id: default value: 0
    :ivar a_risk: default value: 0.0
    :ivar do: default value: 0.0
    :ivar dd: default value: 0
    :ivar dc: default value: 0.0
    :ivar d_risk: default value: 0.0
    :ivar am: default value: 0.0
    :ivar sa: default value: 0.0
    :ivar st: default value: 0.0
    :ivar dr: default value: 0.0
    :ivar sq: default value: 0.0
    :ivar s1: default value: 0.0
    :ivar hloc: default value: 0
    :ivar aloc: default value: 0
    :ivar sloc: default value: 0
    :ivar sl: default value: 0.0
    :ivar ax: default value: 0
    :ivar bx: default value: 0
    :ivar cx: default value: 0
    :ivar nm: default value: 0
    :ivar sx: default value: 0.0
    :ivar um: default value: 0
    :ivar wm: default value: 0
    :ivar xm: default value: 0
    :ivar sm: default value: 0.0
    :ivar df: default value: 0.0
    :ivar sr: default value: 0.0
    :ivar s2: default value: 0.0
    :ivar rpfom: default value: 0.0
    :ivar parent_id: default value: 0
    :ivar dev_assess_type: default value: 0
    :ivar phase_id: default value: 0
    :ivar tcl: default value: 0
    :ivar test_path: default value: 0
    :ivar category: default value: 0
    :ivar test_effort: default value: 0
    :ivar test_approach: default value: 0
    :ivar labor_hours_test: default value: 0.0
    :ivar labor_hours_dev: default value: 0.0
    :ivar budget_test: default value: 0.0
    :ivar budget_dev: default value: 0.0
    :ivar schedule_test: default value: 0.0
    :ivar schedule_dev: default value: 0.0
    :ivar branches: default value: 0
    :ivar branches_test: default value: 0
    :ivar inputs: default value: 0
    :ivar inputs_test: default value: 0
    :ivar nm_test: default value: 0
    :ivar interfaces: default value: 0
    :ivar interfaces_test: default value: 0
    :ivar te: default value: 0.0
    :ivar tm: default value: 0.0
    :ivar tc: default value: 0.0
    :ivar t_risk: default value: 0.0
    :ivar ft1: default value: 0.0
    :ivar ft2: default value: 0.0
    :ivar ren_avg: default value: 0.0
    :ivar ren_eot: default value: 0.0
    :ivar ec: default value: 0.0
    :ivar ev: default value: 0.0
    :ivar et: default value: 0.0
    :ivar os: default value: 0.0
    :ivar ew: default value: 0.0
    :ivar e_risk: default value: 0.0
    :ivar failure_rate: default value: 0.0
    :ivar units: default value: 0
    :ivar units_test: default value: 0
    :ivar cb: default value: 0
    :ivar ncb: default value: 0
    :ivar dr_test: default value: 0
    :ivar test_time: default value: 0.0
    :ivar dr_eot: default value: 0
    :ivar test_time_eot: default value: 0.0
    """

    def __init__(self):
        """
        Initialize a Software data model instance.
        """

        # Lists to hold the answers to the risk factor questions.  The values
        # are lists of 0 and 1 indicating the answer to No or Yes questions or
        # the value of numerical questions.
        self.lst_development = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.lst_anomaly_mgmt = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0]]
        self.lst_traceability = [[0], [0], [0, 0]]
        self.lst_sftw_quality = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.lst_modularity = [0, 0, 0, 0, 0, 0]
        self.lst_test_selection = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                   [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                   [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                   [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                                   [0, 0]]

        # Initialize public dictionary attributes.
        self.dicCSCI = {}
        self.dicUnits = {}

        # Initialize public instance scalar attributes.
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

    def set_attributes(self, values):
        """
        Sets the Software data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.software_id = int(values[1])
            self.level_id = int(values[2])
            self.description = str(values[3])
            self.application_id = int(values[4])
            self.development_id = int(values[5])
            self.a_risk = float(values[6])
            self.do = float(values[7])
            self.dd = int(values[8])
            self.dc = float(values[9])
            self.d_risk = float(values[10])
            self.am = float(values[11])
            self.sa = float(values[12])
            self.st = float(values[13])
            self.dr = float(values[14])
            self.sq = float(values[15])
            self.s1 = float(values[16])
            self.hloc = int(values[17])
            self.aloc = int(values[18])
            self.sloc = int(values[19])
            self.sl = float(values[20])
            self.ax = int(values[21])
            self.bx = int(values[22])
            self.cx = int(values[23])
            self.nm = int(values[24])
            self.sx = float(values[25])
            self.um = int(values[26])
            self.wm = int(values[27])
            self.xm = int(values[28])
            self.sm = float(values[29])
            self.df = float(values[30])
            self.sr = float(values[31])
            self.s2 = float(values[32])
            self.rpfom = float(values[33])
            self.parent_id = int(values[34])
            self.dev_assess_type = int(values[35])
            self.phase_id = int(values[36])
            self.tcl = int(values[37])
            self.test_path = int(values[38])
            self.category = int(values[39])
            self.test_effort = int(values[40])
            self.test_approach = int(values[41])
            self.labor_hours_test = float(values[42])
            self.labor_hours_dev = float(values[43])
            self.budget_test = float(values[44])
            self.budget_dev = float(values[45])
            self.schedule_test = float(values[46])
            self.schedule_dev = float(values[47])
            self.branches = int(values[48])
            self.branches_test = int(values[49])
            self.inputs = int(values[50])
            self.inputs_test = int(values[51])
            self.nm_test = int(values[52])
            self.interfaces = int(values[53])
            self.interfaces_test = int(values[54])
            self.te = float(values[55])
            self.tm = float(values[56])
            self.tc = float(values[57])
            self.t_risk = float(values[58])
            self.ft1 = float(values[59])
            self.ft2 = float(values[60])
            self.ren_avg = float(values[61])
            self.ren_eot = float(values[62])
            self.ec = float(values[63])
            self.ev = float(values[64])
            self.et = float(values[65])
            self.os = float(values[66])
            self.ew = float(values[67])
            self.e_risk = float(values[68])
            self.failure_rate = float(values[69])
            self.cb = int(values[70])
            self.ncb = int(values[71])
            self.dr_test = int(values[72])
            self.test_time = float(values[73])
            self.dr_eot = int(values[74])
            self.test_time_eot = float(values[75])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Software data model attributes.

        :return: (revision_id, software_id, level_id, description,
                  application_id, development_id, a_risk, do, dd, dc, d_risk,
                  am, sa, st, dr, sq, s1, hloc, aloc, sloc, sl, ax, bx, cx, nm,
                  sx, um, wm, xm, sm, df, sr, s2, rpfom, parent_module,
                  dev_assess_type, phase_id, tcl, test_path, category,
                  test_effort, test_approach, labor_hours_test,
                  labor_hours_dev, budget_test, budget_dev, schedule_test,
                  schedule_dev, branches, branches_test, inputs, inputs_test,
                  nm_test, interfaces, interfaces_test, te, tm, tc, t_risk,
                  ft1, ft2, ren_avg, ren_eot, ec, ev, et, os, ew, e_risk,
                  failure_rate, cb, ncb, dr_test, test_time, dr_eot,
                  test_time_eot)
        :rtype: tuple
        """

        _values = (self.revision_id, self.software_id, self.level_id,
                   self.description, self.application_id, self.development_id,
                   self.a_risk, self.do, self.dd, self.dc, self.d_risk,
                   self.am, self.sa, self.st, self.dr, self.sq, self.s1,
                   self.hloc, self.aloc, self.sloc, self.sl, self.ax, self.bx,
                   self.cx, self.nm, self.sx, self.um, self.wm, self.xm,
                   self.sm, self.df, self.sr, self.s2, self.rpfom,
                   self.parent_id, self.dev_assess_type, self.phase_id,
                   self.tcl, self.test_path, self.category, self.test_effort,
                   self.test_approach, self.labor_hours_test,
                   self.labor_hours_dev, self.budget_test, self.budget_dev,
                   self.schedule_test, self.schedule_dev, self.branches,
                   self.branches_test, self.inputs, self.inputs_test,
                   self.nm_test, self.interfaces, self.interfaces_test,
                   self.te, self.tm, self.tc, self.t_risk, self.ft1, self.ft2,
                   self.ren_avg, self.ren_eot, self.ec, self.ev, self.et,
                   self.os, self.ew, self.e_risk, self.failure_rate,
                   self.cb, self.ncb, self.dr_test, self.test_time,
                   self.dr_eot, self.test_time_eot)

        return _values

    def calculate(self, module):
        """
        Iterively calculates various software attributes.

        :param module: the :py:class:`rtk.software.CSCI` or :py:class:`rtk.software.Unit` data model to calculate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # First we calculate all the software Units that are direct children of
        # the current CSCI.
        try:
            _units = module.dicUnits[module.software_id]
        except KeyError:
            _units = []

        for _unit in _units:
            self.calculate(_unit)

            _unit.calculate_complexity_risk()
            _unit.calculate_modularity_risk()

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
            self.calculate(_csci)

            _csci.calculate_complexity_risk()
            _csci.calculate_modularity_risk()

            _csci.s1 = _csci.sa * _csci.st * _csci.sq
            _csci.s2 = _csci.sl * _csci.sm * _csci.sx
            _csci.rpfom = _csci.a_risk * _csci.d_risk * _csci.s1 * _csci.s2

        _calculate_application_risk(module)
        _calculate_development_risk(module)
        if module.phase_id in [2, 3, 4, 5]:
            _calculate_anomaly_risk(module)
            _calculate_traceability_risk(module)
            _calculate_quality_risk(module)
        if module.phase_id in [4, 5]:
            _calculate_language_type_risk(module)

        _calculate_risk_reduction(module)
        _calculate_reliability_estimation_number(module)

        return False


class Software(object):
    """
    The Software data controller provides an interface between the Software
    data model and an RTK view model.  A single Software controller can manage
    one or more Software data models.
    """

    def __init__(self):
        """
        Initializes an Software data controller instance.
        """

        pass
