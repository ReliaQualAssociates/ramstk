#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
the software of the RTK program.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       software.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale
import sys

# Plotting package.
import matplotlib
matplotlib.use('GTK')

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
import configuration as _conf
import utilities as _util
import widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

_ = gettext.gettext


def _test_selection_tree_edit(cell, path, position, model):
    """
    Called whenever a gtk.TreeView CellRenderer is edited for the
    test selection worksheet.

    :param cell: the gtk.CellRenderer() that was edited.
    :type cell: gtk.CellRenderer
    :param path: the gtk.Treeview() path of the gtk.CellRenderer() that was
                 edited.
    :type path: string
    :param position: the column position in the Software class gtk.TreeView()
                     of the edited gtk.CellRenderer().
    :type position: integer
    :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
    :type model: gtk.TreeModel
    :return: False if successful or True if an error is encountered.
    :rtype: boolean
    """

    model[path][position] = not cell.get_active()

    return False


def _set_risk_color(risk, module):
    """
    Function to find the hexadecimal code for the risk level colors.

    :param risk: dictionary containing the Software class risk factors.
    :type risk: dictionary
    :param module: the software id used as a key for accessing the correct risk
                   factors from the risk dictionary.
    :type module: integer
    :return: a dictionary containing the hexadecimal color values for each
             risk factor.
    :rtype: dictionary
    """

    _color = {}

    # Find the Application risk level.
    if risk[module][0] == 1.0:
        _color['A'] = '#90EE90'             # Green
    elif risk[module][0] == 2.0:
        _color['A'] = '#FFFF79'             # Yellow
    elif risk[module][0] == 3.0:
        _color['A'] = '#FFC0CB'             # Red
    else:
        _color['A'] = '#D3D3D3'             # Light grey

    # Find the Development risk level.
    if risk[module][1] == 0.5:
        _color['D'] = '#90EE90'             # Green
    elif risk[module][1] == 1.0:
        _color['D'] = '#FFFF79'             # Yellow
    elif risk[module][1] == 2.0:
        _color['D'] = '#FFC0CB'             # Red
    else:
        _color['D'] = '#D3D3D3'             # Light grey

    # Find the Anomaly Management risk level.
    if risk[module][2] == 0.9:
        _color['SA'] = '#90EE90'            # Green
    elif risk[module][2] == 1.1:
        _color['SA'] = '#FFC0CB'            # Red
    elif risk[module][2] == 1.0:
        _color['SA'] = '#FFFF79'            # Yellow
    elif risk[module][2] == 0.0:
        _color['SA'] = '#D3D3D3'            # Light grey

    # Find the Requirement Traceability risk level.
    if risk[module][3] == 0.9:
        _color['ST'] = '#90EE90'            # Green
    elif risk[module][3] == 1.0:
        _color['ST'] = '#FFFF79'            # Yellow
    elif risk[module][3] == 1.1:
        _color['ST'] = '#FFC0CB'            # Red
    else:
        _color['ST'] = '#D3D3D3'            # Light grey

    # Find the Software Quality risk level.
    if risk[module][4] == 1.0:
        _color['SQ'] = '#90EE90'            # Green
    elif risk[module][4] == 1.1:
        _color['SQ'] = '#FFC0CB'            # Red
    else:
        _color['SQ'] = '#D3D3D3'            # Light grey

    # Find the Language Type risk level.
    if risk[module][5] == 1.0:
        _color['SL'] = '#90EE90'            # Green
    elif risk[module][5] > 1.0 and risk[module][5] <= 1.2:
        _color['SL'] = '#FFFF79'            # Yellow
    elif risk[module][5] > 1.2:
        _color['SL'] = '#FFC0CB'            # Red
    else:
        _color['SL'] = '#D3D3D3'            # Light grey

    # Find the Complexity risk level.
    if risk[module][6] >= 0.8 and risk[module][6] < 1.0:
        _color['SX'] = '#90EE90'            # Green
    elif risk[module][6] >= 1.0 and risk[module][6] <= 1.2:
        _color['SX'] = '#FFFF79'            # Yellow
    elif risk[module][6] > 1.2:
        _color['SX'] = '#FFC0CB'            # Red
    else:
        _color['SX'] = '#D3D3D3'            # Light grey

    # Find the Modularity risk level.
    if risk[module][7] >= 0.9 and risk[module][7] < 1.2:
        _color['SM'] = '#90EE90'            # Green
    elif risk[module][7] >= 1.2 and risk[module][7] <= 1.5:
        _color['SM'] = '#FFFF79'            # Yellow
    elif risk[module][7] > 1.5:
        _color['SM'] = '#FFC0CB'            # Red
    else:
        _color['SM'] = '#D3D3D3'            # Light grey

    # Find the overall risk level.
    if risk[module][8] > 0.0 and risk[module][8] <= 1.5:
        _color['Risk'] = '#90EE90'          # Green
    elif risk[module][8] > 1.5 and risk[module][8] < 3.5:
        _color['Risk'] = '#FFFF79'          # Yellow
    elif risk[module][8] >= 3.5:
        _color['Risk'] = '#FFC0CB'          # Red
    else:
        _color['Risk'] = '#D3D3D3'          # Light grey

    return _color


def _calculate_app_risk(model, row):
    """
    Function to calculate Software risk due to application type.  This function
    uses a similar approach as RL-TR-92-52 for baseline fault density
    estimates.  The baseline application is Process Control software.  Every
    other application is ranked relative to Process Control using the values in
    RL-TR-92-52, Worksheet 0 for average fault density.

        Baseline (low) application risk (A) is assigned a 1.
        Medium risk is assigned a 2.
        High risk is assigned a 3.

    Application risks are defined as:

    +-------+------------------------------+----------+
    |       |                              | Relative |
    | Index |          Application         |   Risk   |
    +-------+------------------------------+----------+
    |   1   | Batch (General)              |   Low    |
    |   2   | Event Control                |   Low    |
    |   3   | Process Control              |   Low    |
    |   4   | Procedure Control            |  Medium  |
    |   5   | Navigation                   |   High   |
    |   6   | Flight Dynamics              |   High   |
    |   7   | Orbital Dynamics             |   High   |
    |   8   | Message Processing           |  Medium  |
    |   9   | Diagnostics                  |  Medium  |
    |  10   | Sensor and Signal Processing |  Medium  |
    |  11   | Simulation                   |   High   |
    |  12   | Database Management          |  Medium  |
    |  13   | Data Acquisition             |  Medium  |
    |  14   | Data Presentation            |  Medium  |
    |  15   | Decision and Planning Aids   |  Medium  |
    |  16   | Pattern and Image Processing |   High   |
    |  17   | System Software              |   High   |
    |  18   | Development Tools            |   High   |
    +-------+------------------------------+----------+

    :param row: the gtk.TreeIter() in the Software class gtk.TreeView() to
                calculate results for.
    :type row: gtk.TreeIter
    :return: the reliability prediction figure of merit (RPFOM).
    :rtype: float
    """

    _application = model.get_value(row, 4)

    if _application == 0:
        _A = 0.0
    elif _application in [5, 6, 7, 11, 16, 17, 18]:
        _A = 3.0
    elif _application in [4, 8, 9, 10, 12, 13, 14, 15]:
        _A = 2.0
    else:
        _A = 1.0

    return _A


def _calculate_development_risk(model, row, risk):
    """
    Function to calculate Software risk due to the development environment.
    This function uses the results of RL-TR-92-52, Worksheet 1B to determine
    the relative risk level.  The percentage of development environment
    characteristics (Dc) applicable to the system under development determine
    the risk level.

        Baseline (medium) development risk (D) is assigned a 1.
        Low development risk (Dc > 0.9) is assigned a 0.5.
        High development risk (Dc < 0.5) is assigned a 2.

    :param model: the Software class gtk.TreeModel()
    :type model: gtk.TreeModel
    :param row: the gtk.TreeIter() in the Software class gtk.TreeView() to
                calculate results for.
    :type row: gtk.TreeIter
    :param risk: dictionary containing the answers to the development
                 environment risk analysis questions.
    :type risk: dictionary
    :return: the reliability prediction figure of merit (RPFOM).
    :rtype: float
    """

    _A = _calculate_app_risk(model, row)

    _software_id = model.get_value(row, 1)

    _Dc = sum(risk[_software_id]) / 43.0
    if _Dc < 0.5:                    # High risk
        _D = 2.0
    elif _Dc > 0.9:                  # Low risk
        _D = 0.5
    else:
        _D = 1.0

    return _A, _D


def _calculate_srr_risk(model, row, risk):
    """
    Function to calculate Software risk due to anomaly management approach,
    requirements traceability, and software quality at the software
    requirements review phase.

    For anomaly management risk (SA), this function uses the results of
    RL-TR-92-52, Worksheet 2A to determine the relative risk level.  The risk
    is based on the percentage of anomaly management techniques used (AM).

        SA = 0.9 if AM > 0.6
        SA = 1.0 if 0.4 >= AM <= 0.6
        SA = 1.1 if AM < 0.4

    For requirements traceability risk (ST), this function uses the results of
    RL-TR-92-52, Worksheet 3A to determine the relative risk level.  The risk
    is based on whether or not requirements can be traced.

        ST = 1.0 if requirements can be traced
        ST = 1.1 otherwise

    For software quality risk (SQ), this function uses the results of
    RL-TR-92-52, Worksheet 4A to determine the relative risk level.  The risk
    is based on the percentage of quality control techniques used (DR).

        SQ = 1.0 if DR >= 0.5
        SQ = 1.1 if DR < 0.5

    :param model: the Software class gtk.TreeModel().
    :type model: gtk.TreeModel
    :param row: the gtk.TreeIter() in the Software class gtk.TreeView() to
                calculate results for.
    :type row: gtk.TreeIter
    :param risk: dictionary containing the answers to the software requirements
                 review risk analysis questions.
    :type risk: dictionary
    :return: the reliability prediction figure of merit (RPFOM).
    :rtype: float
    """

    _software_id = model.get_value(row, 1)
    _module = model.get_value(row, 3)

    # Calculate the Anomaly Management factor.
    _ratios = [0, 0, 0]
    try:
        if risk[_software_id][1] / risk[_software_id][0] == 1:
            _ratios[0] = 1
        if risk[_software_id][3] / risk[_software_id][2] == 1:
            _ratios[1] = 1
        if risk[_software_id][6] / risk[_software_id][5] == 1:
            _ratios[2] = 1
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when "
                                  u"calculating the anomaly management risk "
                                  u"for %s.  Perhaps you forgot to answer one "
                                  u"or more questions.  If the problem "
                                  u"persists, you may report it to "
                                  u"bugs@reliaqual.com.") % _module)

    _n_yes = sum(risk[_software_id][3:4]) + sum(risk[_software_id][7:]) + \
             sum(_ratios)     # noqa
    _AM = (19.0 - _n_yes) / 19.0
    if _AM < 0.4:                   # Low risk
        _SA = 0.9
    elif _AM > 0.6:                 # High risk
        _SA = 1.1
    else:
        _SA = 1.0

    # Calculate the Requirements Traceability factor.
    if risk[_software_id][22] == 1:    # Low risk
        _ST = 1.0
    else:
        _ST = 1.1

    # Calculate the Software Quality factor.
    _ratios = [0, 0]
    try:
        if risk[_software_id][9] / risk[_software_id][8] == 1:
            _ratios[0] = 1
        if risk[_software_id][11] / risk[_software_id][10] == 1:
            _ratios[1] = 1
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when "
                                  u"calculating the software quality risk for "
                                  u"%s.  Perhaps you forgot to answer one or "
                                  u"more questions.  If the problem persists, "
                                  u"you may report it to "
                                  u"bugs@reliaqual.com.") % _module)

    _n_yes = sum(risk[_software_id][:8]) + sum(risk[_software_id][12:]) + \
             sum(_ratios)    # noqa
    _DR = (25.0 - _n_yes) / 25.0
    if _DR < 0.5:                   # High risk
        _SQ = 1.1
    else:
        _SQ = 1.0

    return (_SA, _ST, _SQ)


def _calculate_pdr_risk(model, row, risk):
    """
    Function to calculate Software risk due to anomaly management approach,
    requirements traceability, and software quality at the preliminary design
    review.

    For anomaly management risk (SA), this function uses the results of
    RL-TR-92-52, Worksheet 2B to determine the relative risk level.  The risk
    is based on the percentage of anomaly management techniques used (AM).

        SA = 0.9 if AM > 0.6
        SA = 1.0 if 0.4 >= AM <= 0.6
        SA = 1.1 if AM < 0.4

    For requirements traceability risk (ST), this function uses the results of
    RL-TR-92-52, Worksheet 3B to determine the relative risk level.  The risk
    is based on whether or not requirements can be traced.

        ST = 1.0 if requirements can be traced
        ST = 1.1 otherwise

    For software quality risk (SQ), this function uses the results of
    RL-TR-92-52, Worksheet 4B to determine the relative risk level.  The risk
    is based on the percentage of quality control techniques used (DR).

        SQ = 1.0 if DR >= 0.5
        SQ = 1.1 if DR < 0.5

    :param model: the Software class gtk.TreeModel().
    :type model: gtk.TreeModel
    :param row: the gtk.TreeIter() in the Software class gtk.TreeView() to
                calculate results for.
    :type row: gtk.TreeIter
    :param risk: dictionary containing the answers to the preliminary design
                 review risk analysis questions.
    :type risk: dictionary
    :return: the reliability prediction figure of merit (RPFOM).
    :rtype: float
    """

    _software_id = model.get_value(row, 1)
    _module = model.get_value(row, 3)

    # Calculate the Anomaly Management factor.
    _n_yes = sum(risk[_software_id][i] for i in range(14))
    _AM = (14.0 - _n_yes) / 14.0
    if _AM < 0.4:                   # Low risk
        _SA = 0.9
    elif _AM > 0.6:                 # High risk
        _SA = 1.1
    else:
        _SA = 1.0

    # Calculate the Requirements Traceability factor.
    if risk[_software_id][14] == 1:          # Low risk
        _ST = 1.0
    else:
        _ST = 1.1

    # Calculate the Software Quality factor.
    _ratios = [0, 0, 0, 0, 0]
    try:
        if risk[_software_id][30] / (risk[_software_id][29] +
           risk[_software_id][30]) <= 0.3:
            _ratios[0] = 1
        if risk[_software_id][32] / risk[_software_id][31] > 0.5:
            _ratios[1] = 1
        if risk[_software_id][34] / risk[_software_id][33] > 0.5:
            _ratios[2] = 1
        if risk[_software_id][36] / risk[_software_id][35] > 0.5:
            _ratios[3] = 1
        if risk[_software_id][38] / risk[_software_id][37] > 0.75:
            _ratios[4] = 1
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when "
                                  u"calculating the software quality risk for "
                                  u"%s.  Perhaps you forgot to answer one or "
                                  u"more questions.  If the problem persists, "
                                  u"you may report it to "
                                  u"bugs@reliaqual.com.") % _module)

    _n_yes = sum(risk[_software_id][i] for i in range(15, 29)) + sum(_ratios)
    _DR = _n_yes / 25.0
    if _DR < 0.5:                   # High risk
        _SQ = 1.1
    else:
        _SQ = 1.0

    return (_SA, _ST, _SQ)


def _calculate_cdr_risk(model, row, risk):
    """
    Function to calculate Software risk due to anomaly management approach,
    requirements traceability, and software quality at critical design review.

    For anomaly management risk (SA), this function uses the results of
    RL-TR-92-52, Worksheet 2D to determine the relative risk level.  The risk
    is based on the percentage of anomaly management techniques used (AM).

        SA = 0.9 if AM > 0.6
        SA = 1.0 if 0.4 >= AM <= 0.6
        SA = 1.1 if AM < 0.4

    For requirements traceability risk (ST), this function uses the results of
    RL-TR-92-52, Worksheet 3C to determine the relative risk level.  The risk
    is based on whether or not requirements can be traced.

        ST = 1.0 if requirements can be traced
        ST = 1.1 otherwise

    For software quality risk (SQ), this function uses the results of
    RL-TR-92-52, Worksheet 4D to determine the relative risk level.  The risk
    is based on the percentage of quality control techniques used (DR).

        SQ = 1.0 if DR >= 0.5
        SQ = 1.1 if DR < 0.5

    :param model: the Software class gtk.TreeModel().
    :type model: gtk.TreeModel
    :param row: the gtk.TreeIter() in the Software class gtk.TreeView() to
                calculate results for.
    :type row: gtk.TreeIter
    :param risk: dictionary containing the answers to the critical design
                 review risk analysis questions.
    :type risk: dictionary
    :return: the reliability prediction figure of merit (RPFOM).
    :rtype: float
    """

    _software_id = model.get_value(row, 1)
    _level = model.get_value(row, 2)
    _module = model.get_value(row, 3)

    _SA = 1.0
    _ST = 1.1
    if _level == 2:                 # CSCI
        # Calculate the Anomaly Management factor.
        _n_yes = sum(risk[_software_id][i] for i in range(8))
        _AM = (8 - _n_yes) / 8.0

        if _AM < 0.4:               # Low risk
            _SA = 0.9
        elif _AM > 0.6:             # High risk
            _SA = 1.1

        # Calculate the Requirements Traceability factor.
        if risk[_software_id][8] == 1 and risk[_software_id][9] == 1:
            _ST = 1.0

        # Calculate the Software Quality factor.
        _ratios = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        try:
            if risk[_software_id][12] / risk[_software_id][11] <= 0.3:
                _ratios[0] = 1
            if risk[_software_id][13] / risk[_software_id][10] <= 0.3:
                _ratios[1] = 1
            if risk[_software_id][15] / risk[_software_id][14] <= 0.3:
                _ratios[2] = 1
            if risk[_software_id][16] / risk[_software_id][10] > 0.5:
                _ratios[3] = 1
            if risk[_software_id][18] / risk[_software_id][17] > 0.5:
                _ratios[4] = 1
            if risk[_software_id][20] / risk[_software_id][19] > 0.5:
                _ratios[5] = 1
            if risk[_software_id][22] / risk[_software_id][21] > 0.5:
                _ratios[6] = 1
            if risk[_software_id][23] / risk[_software_id][10] > 0.5:
                _ratios[7] = 1
            if risk[_software_id][24] / risk[_software_id][10] > 0.5:
                _ratios[8] = 1
            if risk[_software_id][26] / risk[_software_id][25] > 0.75:
                _ratios[9] = 1
            if risk[_software_id][27] / risk[_software_id][10] > 0.5:
                _ratios[10] = 1
            if risk[_software_id][28] / risk[_software_id][10] > 0.5:
                _ratios[11] = 1
            if risk[_software_id][29] / risk[_software_id][10] > 0.5:
                _ratios[12] = 1
            if risk[_software_id][30] / risk[_software_id][10] > 0.5:
                _ratios[13] = 1
            if risk[_software_id][31] / risk[_software_id][10] > 0.5:
                _ratios[14] = 1
            if risk[_software_id][32] / risk[_software_id][10] > 0.5:
                _ratios[15] = 1
            if risk[_software_id][33] / risk[_software_id][10] > 0.5:
                _ratios[16] = 1
            if risk[_software_id][34] / risk[_software_id][10] > 0.5:
                _ratios[17] = 1
        except ZeroDivisionError:
            _util.rtk_error(_(u"Attempted to divide by zero when "
                                      u"calculating the software quality risk "
                                      u"for %s.  Perhaps you forgot to answer "
                                      u"one or more questions.  If the "
                                      u"problem persists, you may report it "
                                      u"to bugs@reliaqual.com.") % _module)
    elif _level == 3:               # Unit
        # Calculate the Software Quality factor.
        _ratios = [0, 0, 0, 0, 0, 0, 0]
        try:
            if risk[_software_id][47] / risk[_software_id][46] <= 0.3:
                _ratios[0] = 1
            if risk[_software_id][34] / risk[_software_id][12] <= 0.3:
                _ratios[1] = 1
            if risk[_software_id][49] / risk[_software_id][48] <= 0.3:
                _ratios[2] = 1
            if risk[_software_id][50] / risk[_software_id][51] > 0.5:
                _ratios[3] = 1
            if risk[_software_id][53] / risk[_software_id][52] > 0.5:
                _ratios[4] = 1
            if risk[_software_id][55] / risk[_software_id][54] > 0.5:
                _ratios[5] = 1
            if risk[_software_id][57] / risk[_software_id][56] > 0.75:
                _ratios[6] = 1
        except ZeroDivisionError:
            _util.rtk_error(_(u"Attempted to divide by zero when "
                                      u"calculating the software quality risk "
                                      u"for %s.  Perhaps you forgot to answer "
                                      u"one or more questions.  If the "
                                      u"problem persists, you may report it "
                                      u"to bugs@reliaqual.com.") % _module)

    _n_yes = sum(risk[_software_id][i] for i in range(34, 36)) + sum(_ratios)
    _DR = _n_yes / 18.0
    if _DR < 0.5:                   # High risk
        _SQ = 1.1
    else:
        _SQ = 1.0

    return (_SA, _ST, _SQ)


def _calculate_trr_risk(model, row, risk):
    """
    Function to calculate Software risk due to anomaly management approach,
    software quality, language type, complexity, and modularity at test
    readiness review.

    For anomaly management risk (SA), this function uses the results of
    RL-TR-92-52, Worksheet 2D to determine the relative risk level.  The risk
    is based on the percentage of anomaly management techniques used (AM).

        SA = 0.9 if AM > 0.6
        SA = 1.0 if 0.4 >= AM <= 0.6
        SA = 1.1 if AM < 0.4

    For software quality risk (SQ), this function uses the results of
    RL-TR-92-52, Worksheet 4D to determine the relative risk level.  The risk
    is based on the percentage of quality control techniques used (DR).

        SQ = 1.0 if DR >= 0.5
        SQ = 1.1 if DR < 0.5

    For language type risk (SL), this function uses the results of RL-TR-92-52,
    Worksheet 8D to determine the relative risk level.  The risk is based on
    the percentage of code written in a higher order language (HLOC) and the
    percentage of code written in an assembly language (ALOC).

        SL = (HLOC / SLOC) + (1.4 * ALOC / SLOC)

    For software complexity risk (SX), this function uses the results of
    RL-TR-92-52, Worksheet 9D or 10D to determine the relative risk level.  The
    risk is based on the number of software units in a software module and the
    complexity of each unit.

        For software units:
            sx = # of conditional branching statements +
                 # of unconditional branching statements + 1

        For software modules:
            NM = number of units in module
            ax = # of units with sx >= 20
            bx = # of units with 7 <= sx < 20
            cx = # of units with sx < 7

            SX = (1.5 * ax + bx + 0.8 * cx) / NM

    For software modularity risk (SM), this function uses the results of
    RL-TR-92-52, Worksheet 9D to determine the relative risk level.  The risk
    is based on the number of software units in a software module and the SLOC
    in each unit.

        For software units:
            SM = 1.0

        For software modules:
            NM = number of units in module
            um = # of units in module with SLOC <= 100
            wm = # of units in module with 100 < SLOC <= 500
            xm = # of units in module with SLOC > 500

            SM = (0.9 * um + wm + 2.0 * xm) / NM

    :param model: the Software class gtk.TreeModel().
    :type model: gtk.TreeModel
    :param row: the gtk.TreeIter() in the Software class gtk.TreeView() to
                calculate results for.
    :type row: gtk.TreeIter
    :param risk: dictionary containing the answers to the test readiness review
                 risk analysis questions.
    :type risk: dictionary
    :return: the reliability prediction figure of merit (RPFOM).
    :rtype: float
    """

    _software_id = model.get_value(row, 1)
    _level = model.get_value(row, 2)
    _module = model.get_value(row, 3)

    _SA = 1.0
    _SQ = 1.0
    _SX = 1.0
    _SM = 1.0

    # Calculate the Language Type factor:
    #
    #   HLOC = SLOC - ALOC
    #   SL = HLOC / SLOC + 1.4 * ALOC / SLOC
    _SLOC = model.get_value(row, 19)
    _ALOC = model.get_value(row, 18)
    _HLOC = _SLOC - _ALOC
    try:
        _SL = (_HLOC / _SLOC) + (1.4 * _ALOC / _SLOC)
    except ZeroDivisionError:
        _util.rtk_error(_(u"Attempted to divide by zero when "
                                  u"calculating the software language risk "
                                  u"for %s.  Perhaps you forgot to answer one "
                                  u"or more questions.  If the problem "
                                  u"persists, you may report it to "
                                  u"bugs@reliaqual.com.") % _module)
        _SL = 1.4

    if _level == 2:                 # CSCI
        # Calculate the Software Complexity factor:
        #
        #   SX = (1.5 * ax + bx + 0.8 * cx) / NM
        _NM = model.get_value(row, 24)
        _ax = model.get_value(row, 21)
        _bx = model.get_value(row, 22)
        _cx = model.get_value(row, 23)
        try:
            _SX = (1.5 * _ax + _bx + 0.8 * _cx) / _NM
        except ZeroDivisionError:
            _util.rtk_error(_(u"Attempted to divide by zero when "
                                      u"calculating the software complexity "
                                      u"risk for %s.  Perhaps you forgot to "
                                      u"answer one or more questions.  If the "
                                      u"problem persists, you may report it "
                                      u"to bugs@reliaqual.com.") % _module)
            _SX = 1.5

        # Calculate the Software Modularity factor:
        #
        #   SM = (0.9 * um + wm + 2.0 * xm) / NM
        _um = model.get_value(row, 26)
        _wm = model.get_value(row, 27)
        _xm = model.get_value(row, 28)
        try:
            _SM = (0.9 * _um + _wm + 2.0 * _xm) / _NM
        except ZeroDivisionError:
            _util.rtk_error(_(u"Attempted to divide by zero when "
                                      u"calculating the software modularity "
                                      u"risk for %s.  Perhaps you forgot to "
                                      u"answer one or more questions.  If the "
                                      u"problem persists, you may report it "
                                      u"to bugs@reliaqual.com.") % _module)
            _SM = 2.0

    elif _level == 3:               # Unit
        # Calculate the Anomaly Management factor.
        _n_yes = risk[_software_id][7] + risk[_software_id][8]
        if _n_yes / 2.0 >= 0.5:      # Low risk
            _SA = 0.9
        elif _n_yes / 2.0 == 0.0:    # High risk
            _SA = 1.1

        # Calculate the Software Quality factor.
        _n_yes = sum(risk[_software_id][i] for i in range(9, 22))
        _DR = _n_yes / 14.0
        if _DR < 0.5:               # High risk
            _SQ = 1.1

        # Calculate the Software Complexity factor:
        #
        #   sx = cb + ncb + 1
        # _SX = _cb + _ncb + 1
        _SX = 1.0

    return (_SA, _SQ, _SL, _SX, _SM)


class Software(object):
    """
    The Software class represents the software items (modules and units) for
    the system being analyzed.
    """

    _csci_test_rankings = [[1, 0, 0, 0, 0, 0, '12', '1', '4', '1', '-', '-', 0, 0, ''],     # noqa
                           [0, 1, 0, 0, 0, 0, '18', '2', '6', '5', '-', '-', 0, 0, ''],     # noqa
                           [0, 0, 1, 0, 0, 0, '16', '3', '2', '2', '-', '-', 0, 0, ''],     # noqa
                           [0, 0, 0, 1, 0, 0, '32', '4', '3', '4', '2', '1', 0, 0, ''],     # noqa
                           [0, 0, 0, 0, 1, 0, '58', '5', '1', '3', '1', '2', 0, 0, ''],     # noqa
                           [0, 0, 0, 0, 0, 1, '44', '5', '5', '6', '3', '3', 0, 0, ''],     # noqa
                           [1, 0, 1, 0, 0, 0, '-', '2', '7', '1', '-', '-', 0, 0, ''],      # noqa
                           [0, 1, 1, 0, 0, 0, '-', '2', '7', '1', '-', '-', 0, 0, ''],      # noqa
                           [1, 1, 0, 0, 0, 0, '-', '1', '1', '3', '-', '-', 0, 0, ''],      # noqa
                           [0, 0, 1, 1, 0, 0, '-', '4', '6', '4', '7', '1', 0, 0, ''],      # noqa
                           [0, 1, 0, 0, 1, 0, '-', '10', '14', '5', '3', '3', 0, 0, ''],    # noqa
                           [1, 0, 0, 0, 1, 0, '-', '10', '14', '5', '3', '3', 0, 0, ''],    # noqa
                           [0, 0, 1, 0, 0, 1, '-', '5', '3', '7', '10', '2', 0, 0, ''],     # noqa
                           [1, 0, 0, 1, 0, 0, '-', '6', '10', '8', '7', '5', 0, 0, ''],     # noqa
                           [0, 1, 0, 1, 0, 0, '-', '6', '9', '9', '7', '5', 0, 0, ''],      # noqa
                           [0, 1, 1, 0, 1, 0, '-', '12', '12', '10', '3', '9', 0, 0, ''],   # noqa
                           [0, 0, 0, 1, 1, 0, '-', '13', '12', '11', '1', '10', 0, 0, ''],  # noqa
                           [1, 0, 0, 0, 0, 1, '-', '8', '3', '12', '10', '7', 0, 0, ''],    # noqa
                           [0, 1, 0, 0, 0, 1, '-', '8', '3', '12', '10', '7', 0, 0, ''],    # noqa
                           [0, 0, 0, 0, 1, 1, '-', '15', '11', '14', '1', '11', 0, 0, ''],  # noqa
                           [0, 0, 0, 1, 0, 1, '-', '13', '2', '15', '6', '12', 0, 0, '']]   # noqa

    _unit_test_rankings = [[1, 0, 0, 0, 0, 0, '6', '2', '2', '1', '-', '-', 'L', 'M', '', '', '', '', 'H', '', '', '', 0, 0, ''],       # noqa
                           [0, 1, 0, 0, 0, 0, '4', '1', '6', '2', '-', '-', '', 'L', '', '', '', '', '', '', '', '', 0, 0, ''],         # noqa
                           [0, 0, 1, 0, 0, 0, '8', '4', '1', '3', '-', '-', 'L', 'H', '', 'L', 'H', '', 'L', 'M', '', 'L', 0, 0, ''],   # noqa
                           [0, 0, 0, 1, 0, 0, '16', '3', '4', '4', '2', '1', 'L', 'L', '', 'L', 'H', '', '', 'H', '', 'L', 0, 0, ''],   # noqa
                           [0, 0, 0, 0, 1, 0, '29', '6', '3', '5', '1', '3', 'L', 'M', '', '', 'H', 'L', '', 'H', '', 'L', 0, 0, ''],   # noqa
                           [0, 0, 0, 0, 0, 1, '22', '5', '5', '6', '2', '2', 'L', '', 'L', '', 'M', 'L', '', 'M', '', 'L', 0, 0, ''],   # noqa
                           [1, 1, 0, 0, 0, 0, '-', '1', '9', '1', '-', '-', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],          # noqa
                           [1, 0, 1, 0, 0, 0, '-', '3', '1', '2', '-', '-', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],          # noqa
                           [0, 1, 1, 0, 0, 0, '-', '2', '7', '3', '-', '-', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],          # noqa
                           [1, 0, 0, 1, 0, 0, '-', '10', '2', '4', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],         # noqa
                           [0, 0, 1, 0, 0, 1, '-', '9', '4', '5', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],          # noqa
                           [1, 0, 0, 0, 0, 1, '-', '5', '5', '6', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],          # noqa
                           [1, 0, 0, 0, 1, 0, '-', '12', '3', '7', '3', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],         # noqa
                           [0, 0, 1, 1, 0, 0, '-', '6', '6', '8', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],          # noqa
                           [0, 0, 0, 1, 0, 1, '-', '7', '10', '8', '6', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],         # noqa
                           [0, 1, 0, 1, 0, 0, '-', '8', '12', '10', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],        # noqa
                           [0, 0, 0, 0, 1, 1, '-', '13', '11', '11', '1', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],       # noqa
                           [0, 1, 0, 0, 1, 0, '-', '11', '14', '12', '3', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],       # noqa
                           [0, 1, 0, 0, 0, 1, '-', '4', '15', '13', '7', '1', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],        # noqa
                           [0, 0, 1, 0, 1, 0, '-', '15', '8', '14', '37', '11', '', '', '', '', '', '', '', '', '', '', 0, 0, ''],      # noqa
                           [0, 0, 0, 1, 1, 0, '-', '14', '13', '15', '1', '11', '', '', '', '', '', '', '', '', '', '', 0, 0, '']]      # noqa

    def __init__(self, application):
        """
        Initializes the Software class.

        :param application: the current instance of the RTK application.
        """

        # Define private Software class scalar attributes.
        self._app = application
        self._selected_page = 0

        # Define private Software class dictionary attributes.
        self._dicSoftware = {}

        # Dictionaries to hold the answers to the risk factor questions.  The
        # dictionary key is the software id.  The values are lists of 0 and 1
        # indicating the answer to No or Yes questions or the value of
        # numerical questions.
        self._dic_dev_env = {}
        self._dic_srr = {}
        self._dic_pdr = {}
        self._dic_cdr = {}
        self._dic_trr = {}

        # Dictionary to hold risk factor values.  The key is the module name.
        # The values are lists of risk factors, where a list contains the
        # following factors:
        #   +-------+--------------------------+
        #   | Index |       Risk Factor        |
        #   +-------+--------------------------+
        #   |   0   | Application              |
        #   |   1   | Development environment  |
        #   |   2   | Anomaly management       |
        #   |   3   | Requirement traceability |
        #   |   4   | Quality control          |
        #   |   5   | Language type            |
        #   |   6   | Complexity               |
        #   |   7   | Modularity               |
        #   |   8   | Overall                  |
        #   +-------+--------------------------+
        self._dic_risk = {}

        # Define private Software class list attributes.

        # Define public Software class scalar attributes.
        self.revision_id = 0
        self.software_id = 0
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
        self.sm = 0.0
        self.df = 0.0
        self.sr = 0.0
        self.s2 = 0.0
        self.rpfom = 0.0
        self.parent_module = ''
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
        self.units = 0
        self.units_test = 0
        self.interfaces = 0
        self.interfaces_test = 0

        # Define public Software class dictionary attributes.

        # Create the main Software class treeview.
        (self.treeview,
         self._col_order) = _widg.make_treeview('Software', 15, self._app,
                                                None, _conf.RTK_COLORS[6],
                                                _conf.RTK_COLORS[7])

        # Software class Work Book toolbar widgets.
        self.btnAddItem = gtk.ToolButton()
        self.btnRemoveItem = gtk.ToolButton()
        self.btnAnalyze = gtk.ToolButton()
        self.btnSaveResults = gtk.ToolButton()

        # General Data page widgets.
        self.cmbApplication = _widg.make_combo(simple=True)
        self.cmbDevelopment = _widg.make_combo(simple=True)
        self.cmbLevel = _widg.make_combo(simple=True)
        self.cmbPhase = _widg.make_combo(simple=True)
        self.txtDescription = _widg.make_text_view(width=400)

        # Risk Analysis page widgets.
        self.nbkRiskAnalysis = gtk.Notebook()
        self.tvwRiskMap = gtk.TreeView()

        # Create the Development Environment tab widgets.
        self.chkDevEnvQ1 = _widg.make_check_button()
        self.chkDevEnvQ2 = _widg.make_check_button()
        self.chkDevEnvQ3 = _widg.make_check_button()
        self.chkDevEnvQ4 = _widg.make_check_button()
        self.chkDevEnvQ5 = _widg.make_check_button()
        self.chkDevEnvQ6 = _widg.make_check_button()
        self.chkDevEnvQ7 = _widg.make_check_button()
        self.chkDevEnvQ8 = _widg.make_check_button()
        self.chkDevEnvQ9 = _widg.make_check_button()
        self.chkDevEnvQ10 = _widg.make_check_button()
        self.chkDevEnvQ11 = _widg.make_check_button()
        self.chkDevEnvQ12 = _widg.make_check_button()
        self.chkDevEnvQ13 = _widg.make_check_button()
        self.chkDevEnvQ14 = _widg.make_check_button()
        self.chkDevEnvQ15 = _widg.make_check_button()
        self.chkDevEnvQ16 = _widg.make_check_button()
        self.chkDevEnvQ17 = _widg.make_check_button()
        self.chkDevEnvQ18 = _widg.make_check_button()
        self.chkDevEnvQ19 = _widg.make_check_button()
        self.chkDevEnvQ20 = _widg.make_check_button()
        self.chkDevEnvQ21 = _widg.make_check_button()
        self.chkDevEnvQ22 = _widg.make_check_button()
        self.chkDevEnvQ23 = _widg.make_check_button()
        self.chkDevEnvQ24 = _widg.make_check_button()
        self.chkDevEnvQ25 = _widg.make_check_button()
        self.chkDevEnvQ26 = _widg.make_check_button()
        self.chkDevEnvQ27 = _widg.make_check_button()
        self.chkDevEnvQ28 = _widg.make_check_button()
        self.chkDevEnvQ29 = _widg.make_check_button()
        self.chkDevEnvQ30 = _widg.make_check_button()
        self.chkDevEnvQ31 = _widg.make_check_button()
        self.chkDevEnvQ32 = _widg.make_check_button()
        self.chkDevEnvQ33 = _widg.make_check_button()
        self.chkDevEnvQ34 = _widg.make_check_button()
        self.chkDevEnvQ35 = _widg.make_check_button()
        self.chkDevEnvQ36 = _widg.make_check_button()
        self.chkDevEnvQ37 = _widg.make_check_button()
        self.chkDevEnvQ38 = _widg.make_check_button()
        self.chkDevEnvQ39 = _widg.make_check_button()
        self.chkDevEnvQ40 = _widg.make_check_button()
        self.chkDevEnvQ41 = _widg.make_check_button()
        self.chkDevEnvQ42 = _widg.make_check_button()
        self.chkDevEnvQ43 = _widg.make_check_button()

# ----- ----- Create the Requirements Review widgets ----- ----- #
        self.hpnSRR = gtk.HPaned()
        self.lblSRR = gtk.Label()

        # CSCI-level Yes/No from WS2A (16 questions)
        # CSCI-level quantity from WS2A (6 questions)
        self.chkSRRAMQ5 = _widg.make_check_button()
        self.chkSRRAMQ8 = _widg.make_check_button()
        self.chkSRRAMQ9 = _widg.make_check_button()
        self.chkSRRAMQ10 = _widg.make_check_button()
        self.chkSRRAMQ11 = _widg.make_check_button()
        self.chkSRRAMQ12 = _widg.make_check_button()
        self.chkSRRAMQ13 = _widg.make_check_button()
        self.chkSRRAMQ14 = _widg.make_check_button()
        self.chkSRRAMQ15 = _widg.make_check_button()
        self.chkSRRAMQ16 = _widg.make_check_button()
        self.chkSRRAMQ17 = _widg.make_check_button()
        self.chkSRRAMQ18 = _widg.make_check_button()
        self.chkSRRAMQ19 = _widg.make_check_button()
        self.chkSRRAMQ20 = _widg.make_check_button()
        self.chkSRRAMQ21 = _widg.make_check_button()
        self.chkSRRAMQ22 = _widg.make_check_button()

        self.txtSRRAMQ1 = _widg.make_entry(width=50)
        self.txtSRRAMQ2 = _widg.make_entry(width=50)
        self.txtSRRAMQ3 = _widg.make_entry(width=50)
        self.txtSRRAMQ4 = _widg.make_entry(width=50)
        self.txtSRRAMQ6 = _widg.make_entry(width=50)
        self.txtSRRAMQ7 = _widg.make_entry(width=50)

        # CSCI-level Yes/No from WS3A (1 question)
        self.chkSRRSTQ1 = _widg.make_check_button()

        # CSCI-level Yes/No from WS4A (23 questions)
        # CSCI-level quantity from WS4A (4 questions)
        self.chkSRRQCQ1 = _widg.make_check_button()
        self.chkSRRQCQ2 = _widg.make_check_button()
        self.chkSRRQCQ3 = _widg.make_check_button()
        self.chkSRRQCQ4 = _widg.make_check_button()
        self.chkSRRQCQ5 = _widg.make_check_button()
        self.chkSRRQCQ6 = _widg.make_check_button()
        self.chkSRRQCQ7 = _widg.make_check_button()
        self.chkSRRQCQ8 = _widg.make_check_button()
        self.chkSRRQCQ13 = _widg.make_check_button()
        self.chkSRRQCQ14 = _widg.make_check_button()
        self.chkSRRQCQ15 = _widg.make_check_button()
        self.chkSRRQCQ16 = _widg.make_check_button()
        self.chkSRRQCQ17 = _widg.make_check_button()
        self.chkSRRQCQ18 = _widg.make_check_button()
        self.chkSRRQCQ19 = _widg.make_check_button()
        self.chkSRRQCQ20 = _widg.make_check_button()
        self.chkSRRQCQ21 = _widg.make_check_button()
        self.chkSRRQCQ22 = _widg.make_check_button()
        self.chkSRRQCQ23 = _widg.make_check_button()
        self.chkSRRQCQ24 = _widg.make_check_button()
        self.chkSRRQCQ25 = _widg.make_check_button()
        self.chkSRRQCQ26 = _widg.make_check_button()
        self.chkSRRQCQ27 = _widg.make_check_button()

        self.txtSRRQCQ9 = _widg.make_entry(width=50)
        self.txtSRRQCQ10 = _widg.make_entry(width=50)
        self.txtSRRQCQ11 = _widg.make_entry(width=50)
        self.txtSRRQCQ12 = _widg.make_entry(width=50)

# ----- ----- Create the Preliminary Design Review widgets ----- ----- #
        self.hpnPDR = gtk.HPaned()
        self.lblPDR = gtk.Label()

        # CSCI-level Yes/No from WS2B (14 questions)
        self.chkPDRAMQ1 = _widg.make_check_button()
        self.chkPDRAMQ2 = _widg.make_check_button()
        self.chkPDRAMQ3 = _widg.make_check_button()
        self.chkPDRAMQ4 = _widg.make_check_button()
        self.chkPDRAMQ5 = _widg.make_check_button()
        self.chkPDRAMQ6 = _widg.make_check_button()
        self.chkPDRAMQ7 = _widg.make_check_button()
        self.chkPDRAMQ8 = _widg.make_check_button()
        self.chkPDRAMQ9 = _widg.make_check_button()
        self.chkPDRAMQ10 = _widg.make_check_button()
        self.chkPDRAMQ11 = _widg.make_check_button()
        self.chkPDRAMQ12 = _widg.make_check_button()
        self.chkPDRAMQ13 = _widg.make_check_button()
        self.chkPDRAMQ14 = _widg.make_check_button()

        # CSCI-level Yes/No from WS3B (1 question)
        self.chkPDRSTQ1 = _widg.make_check_button()

        # CSCI-level Yes/No from WS4B (14 questions)
        # CSCI-level quantity from WS4B (10 questions)
        self.chkPDRQCQ1 = _widg.make_check_button()
        self.chkPDRQCQ2 = _widg.make_check_button()
        self.chkPDRQCQ5 = _widg.make_check_button()
        self.chkPDRQCQ6 = _widg.make_check_button()
        self.chkPDRQCQ13 = _widg.make_check_button()
        self.chkPDRQCQ14 = _widg.make_check_button()
        self.chkPDRQCQ17 = _widg.make_check_button()
        self.chkPDRQCQ18 = _widg.make_check_button()
        self.chkPDRQCQ19 = _widg.make_check_button()
        self.chkPDRQCQ20 = _widg.make_check_button()
        self.chkPDRQCQ21 = _widg.make_check_button()
        self.chkPDRQCQ22 = _widg.make_check_button()
        self.chkPDRQCQ23 = _widg.make_check_button()
        self.chkPDRQCQ24 = _widg.make_check_button()

        self.txtPDRQCQ3 = _widg.make_entry(width=50)
        self.txtPDRQCQ4 = _widg.make_entry(width=50)
        self.txtPDRQCQ7 = _widg.make_entry(width=50)
        self.txtPDRQCQ8 = _widg.make_entry(width=50)
        self.txtPDRQCQ9 = _widg.make_entry(width=50)
        self.txtPDRQCQ10 = _widg.make_entry(width=50)
        self.txtPDRQCQ11 = _widg.make_entry(width=50)
        self.txtPDRQCQ12 = _widg.make_entry(width=50)
        self.txtPDRQCQ15 = _widg.make_entry(width=50)
        self.txtPDRQCQ16 = _widg.make_entry(width=50)

# ----- ----- Create the Critical Design Review widgets ----- ----- #
        self.hpnCDR = gtk.HPaned()
        self.lblCDR = gtk.Label()

        self.fraCDRCSCIAM = _widg.make_frame(_(u"Software Module Anomaly "
                                               u"Management"))
        self.fraCDRUnitAM = _widg.make_frame(_(u"Software Unit Anomaly "
                                               u"Management"))
        self.fraCDRCSCIQC = _widg.make_frame(_(u"Software Module Quality "
                                               u"Control"))
        self.fraCDRUnitQC = _widg.make_frame(_(u"Software Unit Quality "
                                               u"Control"))

        self.chkCDRAMQ3 = _widg.make_check_button()
        self.chkCDRAMQ4 = _widg.make_check_button()
        self.chkCDRAMQ5 = _widg.make_check_button()
        self.chkCDRAMQ6 = _widg.make_check_button()
        self.chkCDRAMQ7 = _widg.make_check_button()
        self.chkCDRAMQ9 = _widg.make_check_button()
        self.chkCDRAMQ10 = _widg.make_check_button()
        self.chkCDRAMQ11 = _widg.make_check_button()
        self.chkCDRSTQ1 = _widg.make_check_button()
        self.chkCDRSTQ2 = _widg.make_check_button()
        self.chkCDRUnitAMQ1 = _widg.make_check_button()
        self.chkCDRUnitAMQ2 = _widg.make_check_button()
        self.chkCDRUnitAMQ3 = _widg.make_check_button()
        self.chkCDRUnitAMQ4 = _widg.make_check_button()
        self.chkCDRUnitAMQ5 = _widg.make_check_button()
        self.chkCDRUnitAMQ6 = _widg.make_check_button()
        self.chkCDRUnitAMQ7 = _widg.make_check_button()
        self.chkCDRUnitAMQ8 = _widg.make_check_button()
        self.chkCDRUnitAMQ9 = _widg.make_check_button()
        self.chkCDRUnitAMQ10 = _widg.make_check_button()
        self.chkCDRUnitSTQ1 = _widg.make_check_button()
        self.chkCDRUnitQCQ3 = _widg.make_check_button()
        self.chkCDRUnitQCQ6 = _widg.make_check_button()
        self.chkCDRUnitQCQ13 = _widg.make_check_button()
        self.chkCDRUnitQCQ14 = _widg.make_check_button()
        self.chkCDRUnitQCQ17 = _widg.make_check_button()
        self.chkCDRUnitQCQ18 = _widg.make_check_button()
        self.chkCDRUnitQCQ19 = _widg.make_check_button()
        self.chkCDRUnitQCQ20 = _widg.make_check_button()
        self.chkCDRUnitQCQ21 = _widg.make_check_button()
        self.chkCDRUnitQCQ22 = _widg.make_check_button()
        self.chkCDRUnitQCQ23 = _widg.make_check_button()
        self.chkCDRUnitQCQ24 = _widg.make_check_button()

        self.txtCDRAMQ1 = _widg.make_entry(width=50)
        self.txtCDRAMQ2 = _widg.make_entry(width=50)
        self.txtCDRAMQ8 = _widg.make_entry(width=50)
        self.txtCDRQCQ1 = _widg.make_entry(width=50)
        self.txtCDRQCQ2 = _widg.make_entry(width=50)
        self.txtCDRQCQ3 = _widg.make_entry(width=50)
        self.txtCDRQCQ4 = _widg.make_entry(width=50)
        self.txtCDRQCQ5 = _widg.make_entry(width=50)
        self.txtCDRQCQ6 = _widg.make_entry(width=50)
        self.txtCDRQCQ7 = _widg.make_entry(width=50)
        self.txtCDRQCQ8 = _widg.make_entry(width=50)
        self.txtCDRQCQ9 = _widg.make_entry(width=50)
        self.txtCDRQCQ10 = _widg.make_entry(width=50)
        self.txtCDRQCQ11 = _widg.make_entry(width=50)
        self.txtCDRQCQ12 = _widg.make_entry(width=50)
        self.txtCDRQCQ13 = _widg.make_entry(width=50)
        self.txtCDRQCQ14 = _widg.make_entry(width=50)
        self.txtCDRQCQ15 = _widg.make_entry(width=50)
        self.txtCDRQCQ16 = _widg.make_entry(width=50)
        self.txtCDRQCQ17 = _widg.make_entry(width=50)
        self.txtCDRQCQ18 = _widg.make_entry(width=50)
        self.txtCDRQCQ19 = _widg.make_entry(width=50)
        self.txtCDRQCQ20 = _widg.make_entry(width=50)
        self.txtCDRQCQ21 = _widg.make_entry(width=50)
        self.txtCDRQCQ22 = _widg.make_entry(width=50)
        self.txtCDRQCQ23 = _widg.make_entry(width=50)
        self.txtCDRQCQ24 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ1 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ2 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ4 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ5 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ7 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ8 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ9 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ10 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ11 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ12 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ15 = _widg.make_entry(width=50)
        self.txtCDRUnitQCQ16 = _widg.make_entry(width=50)

# ----- ----- Create the Test Readiness Review widgets ----- ----- #
        self.hpnTRR = gtk.HPaned()
        self.lblTRR = gtk.Label()

        self.fraTRRCSCILT = _widg.make_frame(_(u"Software Module Language "
                                               u"Type, Complexity, &amp; "
                                               u"Modularity"))
        self.fraTRRUnitLT = _widg.make_frame(_(u"Software Unit Language "
                                               u"Type, Complexity, &amp; "
                                               u"Modularity"))
        self.fraTRRUnitQC = _widg.make_frame(_(u"Software Unit Quality "
                                               u"Control"))

        # Unit-level Yes/No from WS2C (2 questions)
        self.chkTRRUnitAMQ1 = _widg.make_check_button()
        self.chkTRRUnitAMQ2 = _widg.make_check_button()

        # Unit-level Yes/No from WS4C (14 questions)
        self.chkTRRUnitQCQ1 = _widg.make_check_button()
        self.chkTRRUnitQCQ2 = _widg.make_check_button()
        self.chkTRRUnitQCQ3 = _widg.make_check_button()
        self.chkTRRUnitQCQ4 = _widg.make_check_button()
        self.chkTRRUnitQCQ5 = _widg.make_check_button()
        self.chkTRRUnitQCQ6 = _widg.make_check_button()
        self.chkTRRUnitQCQ7 = _widg.make_check_button()
        self.chkTRRUnitQCQ8 = _widg.make_check_button()
        self.chkTRRUnitQCQ9 = _widg.make_check_button()
        self.chkTRRUnitQCQ10 = _widg.make_check_button()
        self.chkTRRUnitQCQ11 = _widg.make_check_button()
        self.chkTRRUnitQCQ12 = _widg.make_check_button()
        self.chkTRRUnitQCQ13 = _widg.make_check_button()
        self.chkTRRUnitQCQ14 = _widg.make_check_button()

        # CSCI-level quantity from WS8D and WS9D (4 questions)
        # Unit-level Yes/No from WS8D (3 questions)
        self.txtTRRLTCMQ1 = _widg.make_entry(width=50)
        self.txtTRRLTCMQ2 = _widg.make_entry(width=50)
        self.txtTRRLTCMQ3 = _widg.make_entry(width=50)
        self.txtTRRLTCMQ4 = _widg.make_entry(width=50)
        self.txtTRRUnitLTCMQ1 = _widg.make_entry(width=50)
        self.txtTRRUnitLTCMQ2 = _widg.make_entry(width=50)
        self.txtTRRUnitLTCMQ3 = _widg.make_entry(width=50)

        # Test Planning page widgets.
        self.cmbTCL = _widg.make_combo(simple=True)
        self.cmbTestPath = _widg.make_combo(simple=True)
        self.cmbTestEffort = _widg.make_combo(simple=True)
        self.cmbTestApproach = _widg.make_combo(simple=True)

        self.hpnTestPlanning = gtk.HPaned()

        self.lblTestPlanning = gtk.Label()

        self.scwTestSelectionMatrix = gtk.ScrolledWindow()

        self.tvwUnitTestSelectionMatrix = gtk.TreeView()
        self.tvwCSCITestSelectionMatrix = gtk.TreeView()

        self.txtLaborTest = _widg.make_entry(width=75)
        self.txtLaborDev = _widg.make_entry(width=75)
        self.txtBudgetTest = _widg.make_entry(width=75)
        self.txtBudgetDev = _widg.make_entry(width=75)
        self.txtScheduleTest = _widg.make_entry(width=75)
        self.txtScheduleDev = _widg.make_entry(width=75)
        self.txtBranches = _widg.make_entry(width=75)
        self.txtBranchesTest = _widg.make_entry(width=75)
        self.txtInputs = _widg.make_entry(width=75)
        self.txtInputsTest = _widg.make_entry(width=75)
        self.txtUnits = _widg.make_entry(width=75)
        self.txtUnitsTest = _widg.make_entry(width=75)
        self.txtInterfaces = _widg.make_entry(width=75)
        self.txtInterfacesTest = _widg.make_entry(width=75)

        # Reliability Estimation page widgets.
        self.txtFT1 = _widg.make_entry(width=75, editable=False)
        self.txtFT2 = _widg.make_entry(width=75, editable=False)
        self.txtRENAVG = _widg.make_entry(width=75, editable=False)
        self.txtRENEOT = _widg.make_entry(width=75, editable=False)
        self.txtEC = _widg.make_entry(width=75, editable=False)
        self.txtEV = _widg.make_entry(width=75, editable=False)
        self.txtET = _widg.make_entry(width=75, editable=False)
        self.txtOS = _widg.make_entry(width=75, editable=False)
        self.txtEW = _widg.make_entry(width=75, editable=False)
        self.txtE = _widg.make_entry(width=75, editable=False)
        self.txtF = _widg.make_entry(width=75, editable=False)

        gobject.idle_add(_util.long_call, self._app)

        # Put it all together.
        _toolbar = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxSoftware = gtk.VBox()
        self.vbxSoftware.pack_start(_toolbar, expand=False)
        self.vbxSoftware.pack_start(self.notebook)

        self.notebook.connect('switch-page', self._notebook_page_switched, 0)

    def create_tree(self):
        """
        Creates the Software gtk.Treeview and connects it to callback functions
        to handle editing.

        :return: the gtk.ScrolledWindow() container holding the Software class
                 gtk.TreeView().
        :rtype: gtk.ScrolledWindow
        """

        self.treeview.set_tooltip_text(_(u"Displays an indentured list (tree) "
                                         u"of software."))
        self.treeview.set_enable_tree_lines(True)

        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None, 0)
        self.treeview.connect('row_activated', self._treeview_row_changed, 0)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)

        return _scrollwindow

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Software class Work Book.

        :return: the gtk.Toolbar() used in the Software class gtk.NoteBook().
        :rtype: gtk.Toolbar
        """

        _toolbar = gtk.Toolbar()

        # Add sibling module button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new software module at the same "
                                   u"indenture level as the selected software "
                                   u"module."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._add_module, 0)
        _toolbar.insert(_button, 0)

        # Add child module button.
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Adds a new software module one indenture "
                                   u"level subordinate to the selected "
                                   u"software module."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._add_module, 1)
        _toolbar.insert(_button, 1)

        # Delete module button
        _button = gtk.ToolButton()
        _button.set_tooltip_text(_(u"Removes the currently selected software "
                                   u"module from the RTK Program Database."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/delete.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._delete_module)
        _toolbar.insert(_button, 2)

        _toolbar.insert(gtk.SeparatorToolItem(), 3)

        # Perform analysis button.  Depending on the notebook page selected
        # will determine which analysis is executed.
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnAnalyze.set_icon_widget(_image)
        self.btnAnalyze.set_name('Calculate')
        self.btnAnalyze.set_tooltip_text(_(u"Calculates software reliability "
                                           u"metrics."))
        self.btnAnalyze.connect('clicked', self.calculate)
        _toolbar.insert(self.btnAnalyze, 4)

        # Save results button.  Depending on the notebook page selected will
        # determine which results are saved.
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveResults.set_icon_widget(_image)
        self.btnSaveResults.set_name('Save')
        self.btnSaveResults.connect('clicked', self._toolbutton_pressed)
        _toolbar.insert(self.btnSaveResults, 5)

        _toolbar.show()

        self.btnAnalyze.hide()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Software class gtk.Notebook().

        :return: the Software class gtk.Notebook() used for the Work Book.
        :rtype: gtk.Notebook
        """

        def _create_general_data_page(self, notebook):
            """
            Function to create the Software class gtk.Notebook() page for
            displaying general data about the selected Software.

            :param self: the current instance of a Software class.
            :type self: Software class
            :param notebook: the Software class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"General Information"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the gtk.ComboBox() widgets.
            _query = "SELECT fld_level_desc FROM tbl_software_level"
            _results = self._app.COMDB.execute_query(_query,
                                                     None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbLevel, _results, True)

            _query = "SELECT fld_category_name FROM tbl_software_category"
            _results = self._app.COMDB.execute_query(_query,
                                                     None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbApplication, _results, True)

            _query = "SELECT fld_phase_desc FROM tbl_development_phase"
            _results = self._app.COMDB.execute_query(_query,
                                                     None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbPhase, _results, True)

            # Create the labels.
            _labels = [_(u"Module Description:"), _(u"Application Level:"),
                       _(u"Application Type:"), _(u"Development Phase:")]

            (_x_pos, _y_pos) = _widg.make_labels(_labels[1:], _fixed, 5, 110)
            _x_pos += 25

            # Place the widgets.
            self.txtDescription.set_tooltip_text(_(u"Enter a description of "
                                                   u"the selected software "
                                                   u"module."))
            self.cmbLevel.set_tooltip_text(_(u"Select the application level "
                                             u"of the selected software "
                                             u"module."))
            self.cmbApplication.set_tooltip_text(_(u"Select the application "
                                                   u"type of the selected "
                                                   u"software module."))
            self.cmbPhase.set_tooltip_text(_(u"Select the development phase "
                                             u"for the selected software "
                                             u"module."))

            _label = _widg.make_label(_labels[0])
            _fixed.put(_label, 5, 5)
            _fixed.put(self.txtDescription, _x_pos, 5)
            _fixed.put(self.cmbLevel, _x_pos, _y_pos[0])
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[1])
            _fixed.put(self.cmbPhase, _x_pos, _y_pos[2])

            _textbuffer = self.txtDescription.get_child().get_child()
            _textbuffer.connect('focus-out-event', self._callback_entry,
                                'text', 3)
            self.cmbLevel.connect('changed', self._callback_combo, 2)
            self.cmbApplication.connect('changed', self._callback_combo, 4)
            self.cmbPhase.connect('changed', self._callback_combo, 36)

            _fixed.show_all()

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"General\nData") +
                              "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays general information about "
                                      u"the selected software module."))
            notebook.insert_page(_frame,
                                 tab_label=_label,
                                 position=-1)

        def _create_risk_analysis_page(self, notebook):
            """
            Function to create the Software class gtk.Notebook() page for
            displaying the risk analysis for the selected Software.

            :param self: the current instance of a Software class.
            :type self: Software class
            :param notebook: the Software class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hpaned = gtk.HPaned()

            _hpaned.pack1(self.nbkRiskAnalysis, resize=True, shrink=True)
            _hpaned.pack2(self.tvwRiskMap, resize=True, shrink=True)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display risk analysis information.  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Add the gtk.Notebook() that guides the risk analysis.
            self._create_risk_analysis_notebook()

            # Add the risk map.
            _headings = [_(u"Software\nModule"), _(u"Application\nRisk"),
                         _(u"Organization\nRisk"),
                         _(u"Anomaly\nManagement\nRisk"),
                         _(u"Traceability\nRisk"),
                         _(u"Quality\nAssurance\nRisk"), _(u"Language\nRisk"),
                         _(u"Code\nComplexity\nRisk"), _(u"Modularity\nRisk"),
                         _(u"Overall\nRisk")]

            _model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING)
            self.tvwRiskMap.set_model(_model)
            self.tvwRiskMap.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

            _cell = gtk.CellRendererText()       # Cell background color.
            _cell.set_property('visible', False)
            _column = gtk.TreeViewColumn()
            _column.set_visible(False)
            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=0)

            self.tvwRiskMap.append_column(_column)

            for i in range(1, 11):
                _label = gtk.Label()
                _label.set_alignment(xalign=0.5, yalign=0.5)
                _label.set_justify(gtk.JUSTIFY_CENTER)
                _label.set_property('angle', 90)
                _label.set_markup("<span weight='bold'>" +
                                  _headings[i-1] +
                                  "</span>")
                _label.set_use_markup(True)
                _label.show_all()
                _column = gtk.TreeViewColumn()
                _column.set_widget(_label)
                _column.set_visible(True)
                _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
                _cell = gtk.CellRendererText()       # Cell background color.
                _cell.set_property('visible', True)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, background=i)
                if i == 1:
                    _column.set_attributes(_cell, text=i)

                self.tvwRiskMap.append_column(_column)

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Risk\nAnalysis") +
                              "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Allows assessment of the reliability "
                                      u"risk."))
            notebook.insert_page(_hpaned,
                                 tab_label=_label,
                                 position=-1)

            return False

        def _create_test_planning_page(self, notebook):
            """
            Function to create the Software class gtk.Notebook() page for
            displaying the risk analysis for the selected Software.

            :param self: the current instance of a Software class.
            :type self: Software class
            :param notebook: the Software class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _vpaned = gtk.VPaned()
            self.hpnTestPlanning.pack1(_vpaned, resize=True, shrink=True)

            # Add the test planning widgets to the upper left half.
            _fxdtopleft = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdtopleft)

            _frame = _widg.make_frame(label=_(u"Test Planning"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)
            _frame.show_all()

            _vpaned.pack1(_frame, resize=True, shrink=True)

            # Add the test effort widgets to the lower left half.
            _fxdbottomleft = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdbottomleft)

            _frame = _widg.make_frame(label=_(u"Test Effort &amp; Coverage"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _vpaned.pack2(_frame, resize=True, shrink=True)

            # Add the test technique selection widgets to the upper right half.
            self.scwTestSelectionMatrix.set_policy(gtk.POLICY_AUTOMATIC,
                                                   gtk.POLICY_AUTOMATIC)
            self.tvwCSCITestSelectionMatrix.set_grid_lines(
                gtk.TREE_VIEW_GRID_LINES_BOTH)
            self.tvwUnitTestSelectionMatrix.set_grid_lines(
                gtk.TREE_VIEW_GRID_LINES_BOTH)

            _frame = _widg.make_frame(label=_(u"Test Technique Selection"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(self.scwTestSelectionMatrix)

            self.hpnTestPlanning.pack2(_frame, resize=True, shrink=True)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display risk analysis information.  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the gtk.Combo()
            _list = [["Low"], ["Medium"], ["High"], ["Very High"]]
            _widg.load_combo(self.cmbTCL, _list, True)

            _list = [[_(u"Choose techniques based on software category")],
                     [_(u"Choose techniques based on types of software "
                        u"errors")]]
            _widg.load_combo(self.cmbTestPath, _list, True)

            _list = [[_(u"Alternative 1, Labor Hours")],
                     [_(u"Alternative 2, Budget")],
                     [_(u"Alternative 3, Schedule")]]
            _widg.load_combo(self.cmbTestEffort, _list, True)

            _list = [[_(u"Test Until Method is Exhausted")],
                     [_(u"Stopping Rules")]]
            _widg.load_combo(self.cmbTestApproach, _list, True)

            # Place the labels in the upper left pane.
            _labels = [_("Test Confidence Level:"), _("Test Path:"),
                       _("Test Effort:"), _("Test Approach:")]
            _max1 = 0
            (_max1, _y_pos1) = _widg.make_labels(_labels, _fxdtopleft,
                                                 5, 5, y_inc=30)

            # Place the labels in the lower left pane.  There are two columns
            # of information in the lower left pane.  First we place the left
            # hand column of labels and then the right hand column.  This gives
            # us two _x_pos values for placing the display widgets.
            _labels = [_("Labor Hours for Testing:"),
                       _("Labor Hours for Development:"),
                       _("Budget for Testing:"),
                       _("Budget for Development:"),
                       _("Working Days for Testing:"),
                       _("Working Days for Development:")]
            (_x_pos_left, _y_pos2) = _widg.make_labels(_labels, _fxdbottomleft,
                                                       5, 5, y_inc=25)
            _x_pos_left = max(_max1, _x_pos_left)
            _x_pos_left += 25

            _labels = [_("Number of Branches:"),
                       _("Number of Branches Tested:"), _("Number of Inputs:"),
                       _("Number of Inputs Tested:"), _("Number of Units:"),
                       _("Number of Units Tested:")]
#                       _("Number of Interfaces:"),
#                       _("Number of Interfaces Tested:"),
#                       _("Number of Requirements:"),
#                       _("Number of Requirements Tested:")]
            (_x_pos_right,
             _y_pos) = _widg.make_labels(_labels, _fxdbottomleft,
                                         _x_pos_left+105, 5)
            _x_pos_right += _x_pos_left + 130

            # Place the widgets in the upper left pane.
            self.cmbTCL.set_tooltip_text(_(u"Select the desired software test "
                                           u"confidence level."))
            self.cmbTestPath.set_tooltip_text(_(u"Select the path for "
                                                u"determining software "
                                                u"testing techniques."))
            self.cmbTestEffort.set_tooltip_text(_(u"Select the software test "
                                                  u"effort alternative."))
            self.cmbTestApproach.set_tooltip_text(_(u"Select the software "
                                                    u"test approach."))

            _fxdtopleft.put(self.cmbTCL, _x_pos_left, _y_pos1[0])
            _fxdtopleft.put(self.cmbTestPath, _x_pos_left, _y_pos1[1])
            _fxdtopleft.put(self.cmbTestEffort, _x_pos_left, _y_pos1[2])
            _fxdtopleft.put(self.cmbTestApproach, _x_pos_left, _y_pos1[3])

            self.cmbTCL.connect('changed', self._callback_combo, 37)
            self.cmbTestPath.connect('changed', self._callback_combo, 38)
            self.cmbTestEffort.connect('changed', self._callback_combo, 40)
            self.cmbTestApproach.connect('changed', self._callback_combo, 41)

            _fxdtopleft.show_all()

            # Place the widgets in the lower left pane.
            self.txtLaborTest.set_tooltip_text(_(u"Total number of labor "
                                                 u"hours for software "
                                                 u"testing."))
            self.txtLaborDev.set_tooltip_text(_(u"Total number of labor hours "
                                                u"entire software development "
                                                u"effort."))
            self.txtBudgetTest.set_tooltip_text(_(u"Total budget for software "
                                                  u"testing."))
            self.txtBudgetDev.set_tooltip_text(_(u"Total budget for entire "
                                                 u"software development "
                                                 u"effort."))
            self.txtScheduleTest.set_tooltip_text(_(u"Working days scheduled "
                                                    u"for software testing."))
            self.txtScheduleDev.set_tooltip_text(_(u"Working days scheduled "
                                                   u"for entire development "
                                                   u"effort."))

            self.txtBranches.set_tooltip_text(_(u"The total number of "
                                                u"execution branches in the "
                                                u"selected unit."))
            self.txtBranchesTest.set_tooltip_text(_(u"The total number of "
                                                    u"execution branches "
                                                    u"actually tested in the "
                                                    u"selected unit."))
            self.txtInputs.set_tooltip_text(_(u"The total number of inputs to "
                                              u"the selected unit."))
            self.txtInputsTest.set_tooltip_text(_(u"The total number of "
                                                  u"inputs to the selected "
                                                  u"unit actually tested."))
            self.txtUnits.set_tooltip_text(_(u"The total number of units in "
                                             u"the selected CSCI."))
            self.txtUnitsTest.set_tooltip_text(_(u"The total number of units "
                                                 u"in the selected CSCI "
                                                 u"actually tested."))
            self.txtInterfaces.set_tooltip_text(_(u"The total number of "
                                                  u"interfaces to the "
                                                  u"selected CSCI."))
            self.txtInterfacesTest.set_tooltip_text(_(u"The total number of "
                                                      u"interfaces in the "
                                                      u"selected CSCI "
                                                      u"actually tested."))

            _fxdbottomleft.put(self.txtLaborTest, _x_pos_left, _y_pos2[0])
            _fxdbottomleft.put(self.txtLaborDev, _x_pos_left, _y_pos2[1])
            _fxdbottomleft.put(self.txtBudgetTest, _x_pos_left, _y_pos2[2])
            _fxdbottomleft.put(self.txtBudgetDev, _x_pos_left, _y_pos2[3])
            _fxdbottomleft.put(self.txtScheduleTest, _x_pos_left, _y_pos2[4])
            _fxdbottomleft.put(self.txtScheduleDev, _x_pos_left, _y_pos2[5])

            _fxdbottomleft.put(self.txtBranches, _x_pos_right, _y_pos[0])
            _fxdbottomleft.put(self.txtBranchesTest, _x_pos_right, _y_pos[1])
            _fxdbottomleft.put(self.txtInputs, _x_pos_right, _y_pos[2])
            _fxdbottomleft.put(self.txtInputsTest, _x_pos_right, _y_pos[3])
            _fxdbottomleft.put(self.txtUnits, _x_pos_right, _y_pos[4])
            _fxdbottomleft.put(self.txtUnitsTest, _x_pos_right, _y_pos[5])
#            _fxdbottomleft.put(self.txtInterfaces, _x_pos_right, _y_pos[6])
#            _fxdbottomleft.put(self.txtInterfacesTest, _x_pos_right, _y_pos[7])

            self.txtLaborTest.connect('focus-out-event', self._callback_entry,
                                      'float', 42)
            self.txtLaborDev.connect('focus-out-event', self._callback_entry,
                                     'float', 43)
            self.txtBudgetTest.connect('focus-out-event',
                                       self._callback_entry, 'float', 44)
            self.txtBudgetDev.connect('focus-out-event',
                                      self._callback_entry, 'float', 45)
            self.txtScheduleTest.connect('focus-out-event',
                                         self._callback_entry, 'float', 46)
            self.txtScheduleDev.connect('focus-out-event',
                                        self._callback_entry, 'float', 47)

            self.txtBranches.connect('focus-out-event', self._callback_entry,
                                     'int', 48)
            self.txtBranchesTest.connect('focus-out-event',
                                         self._callback_entry, 'int', 49)
            self.txtInputs.connect('focus-out-event', self._callback_entry,
                                   'int', 50)
            self.txtInputsTest.connect('focus-out-event',
                                       self._callback_entry, 'int', 51)
            self.txtUnitsTest.connect('focus-out-event',
                                      self._callback_entry, 'int', 52)
            self.txtInterfaces.connect('focus-out-event',
                                       self._callback_entry, 'int', 53)
            self.txtInterfacesTest.connect('focus-out-event',
                                           self._callback_entry, 'int', 54)

            _fxdbottomleft.show_all()
            # Create and load the Test Matrix for CSCI-level testing.
            _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_STRING)
            self.tvwCSCITestSelectionMatrix.set_model(_model)
            self.tvwCSCITestSelectionMatrix.set_tooltip_text(_(u"Software "
                                                               u"module-level "
                                                               u"test "
                                                               u"technique "
                                                               u"selection "
                                                               u"matrix."))

            _headings = [_(u"Error/Anomaly\nDetection"),
                         _(u"Structure\nAnalysis &amp;\nDocumentation"),
                         _(u"Code\nReviews"), _(u"Functional\nTesting"),
                         _(u"Branch\nTesting"), _(u"Random\nTesting"),
                         _(u"Stopping\nRule (Hours)"), _(u"Average\nEffort"),
                         _(u"Average %\nErrors Found"),
                         _(u"Detection\nEfficiency"),
                         _(u"% Average\nCoverage"), _(u"Coverage\nEfficiency")]

            for i in range(len(_headings[:6])):
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 0)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.5)
                _label = gtk.Label()
                _label.set_alignment(xalign=0.5, yalign=0.5)
                _label.set_justify(gtk.JUSTIFY_CENTER)
                _label.set_property('angle', 90)
                _label.set_markup("<span weight='bold'>" +
                                  _headings[i] + "</span>")
                _label.set_use_markup(True)
                _label.show_all()
                _column = gtk.TreeViewColumn()
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=i)
                _column.set_clickable(True)
                _column.set_reorderable(True)
                _column.set_max_width(75)
                _column.set_sort_column_id(i)
                _column.set_widget(_label)
                self.tvwCSCITestSelectionMatrix.append_column(_column)

            for i in range(len(_headings[6:])):
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _cell.set_property('xalign', 0.5)
                _cell.set_property('yalign', 0.5)
                _label = gtk.Label()
                _label.set_alignment(xalign=0.5, yalign=0.5)
                _label.set_justify(gtk.JUSTIFY_CENTER)
                _label.set_property('angle', 90)
                _label.set_markup("<span weight='bold'>" +
                                  _headings[i + 6] + "</span>")
                _label.set_use_markup(True)
                _label.show_all()
                _column = gtk.TreeViewColumn()
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 6)
                _column.set_clickable(True)
                _column.set_reorderable(True)
                _column.set_max_width(75)
                _column.set_sort_column_id(i + 6)
                _column.set_widget(_label)
                self.tvwCSCITestSelectionMatrix.append_column(_column)

            _cell = gtk.CellRendererToggle()
            _cell.set_property('activatable', 1)
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.5)
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _(u"Recommended") +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.set_visible(False)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=12)
            _column.set_clickable(True)
            _column.set_max_width(75)
            _column.set_sort_column_id(12)
            _column.set_widget(_label)
            self.tvwCSCITestSelectionMatrix.append_column(_column)
            _cell.connect('toggled', _test_selection_tree_edit, 12, _model)

            _cell = gtk.CellRendererToggle()
            _cell.set_property('activatable', 1)
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.5)
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _(u"Selected") +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.set_visible(False)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=13)
            _column.set_clickable(True)
            _column.set_max_width(75)
            _column.set_sort_column_id(13)
            _column.set_widget(_label)
            self.tvwCSCITestSelectionMatrix.append_column(_column)
            _cell.connect('toggled', _test_selection_tree_edit, 13, _model)
# TODO: Append recommended and selected values from database for display.
            for i in range(len(self._csci_test_rankings)):
                _model.append(self._csci_test_rankings[i])

            # Create and load the Test Matrix for unit-level testing.
            _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_STRING, gobject.TYPE_STRING,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_STRING)
            self.tvwUnitTestSelectionMatrix.set_model(_model)
            self.tvwUnitTestSelectionMatrix.set_tooltip_text(_(u"Software "
                                                               u"unit-level "
                                                               u"test "
                                                               u"technique "
                                                               u"selection "
                                                               u"matrix."))

            _headings = [_(u"Error/Anomaly\nDetection"),
                         _(u"Structure\nAnalysis &amp;\nDocumentation"),
                         _(u"Code\nReviews"), _(u"Functional\nTesting"),
                         _(u"Branch\nTesting"), _(u"Random\nTesting"),
                         _(u"Stopping\nRule (Hours)"), _(u"Average\nEffort"),
                         _(u"Average %\nErrors Found"),
                         _(u"Detection\nEfficiency"),
                         _(u"% Average\nCoverage"),
                         _(u"Coverage\nEfficiency"),
                         _(u"Computational\nErrors"),
                         _(u"Logic\nErrors"), _(u"Data\nInput\nErrors"),
                         _(u"Data\nVerification\nErrors"),
                         _(u"Data\nHandling\nErrors"),
                         _(u"Data\nOutput\nErrors"),
                         _(u"Data\nDefinition\nErrors"),
                         _(u"Interface\nErrors"),
                         _(u"Database\nErrors"), _(u"Other\nErrors")]

            for i in range(len(_headings[:6])):
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 0)
                _label = gtk.Label()
                _label.set_alignment(xalign=0.5, yalign=0.5)
                _label.set_justify(gtk.JUSTIFY_CENTER)
                _label.set_property('angle', 90)
                _label.set_markup("<span weight='bold'>" +
                                  _headings[i] + "</span>")
                _label.set_use_markup(True)
                _label.show_all()
                _column = gtk.TreeViewColumn()
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=i)
                _column.set_clickable(True)
                _column.set_reorderable(True)
                _column.set_max_width(75)
                _column.set_sort_column_id(i)
                _column.set_widget(_label)
                self.tvwUnitTestSelectionMatrix.append_column(_column)

            for i in range(len(_headings[6:])):
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _label = gtk.Label()
                _label.set_alignment(xalign=0.5, yalign=0.5)
                _label.set_justify(gtk.JUSTIFY_CENTER)
                _label.set_property('angle', 90)
                _label.set_markup("<span weight='bold'>" +
                                  _headings[i + 6] + "</span>")
                _label.set_use_markup(True)
                _label.show_all()
                _column = gtk.TreeViewColumn()
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 6)
                _column.set_clickable(True)
                _column.set_reorderable(True)
                _column.set_max_width(75)
                _column.set_sort_column_id(i + 6)
                _column.set_widget(_label)
                self.tvwUnitTestSelectionMatrix.append_column(_column)

            _cell = gtk.CellRendererToggle()
            _cell.set_property('activatable', 1)
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _(u"Recommended") + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.set_visible(False)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=22)
            _column.set_clickable(True)
            _column.set_max_width(75)
            _column.set_sort_column_id(22)
            _column.set_widget(_label)
            self.tvwUnitTestSelectionMatrix.append_column(_column)
            _cell.connect('toggled', _test_selection_tree_edit, 22, _model)

            _cell = gtk.CellRendererToggle()
            _cell.set_property('activatable', 1)
            _label = gtk.Label()
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_property('angle', 90)
            _label.set_markup("<span weight='bold'>" +
                              _(u"Selected") + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.set_visible(False)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, active=23)
            _column.set_clickable(True)
            _column.set_max_width(75)
            _column.set_sort_column_id(23)
            _column.set_widget(_label)
            self.tvwUnitTestSelectionMatrix.append_column(_column)
            _cell.connect('toggled', _test_selection_tree_edit, 23, _model)

            for i in range(len(self._unit_test_rankings)):
                _model.append(self._unit_test_rankings[i])

            # Insert the tab.
            self.lblTestPlanning.set_markup("<span weight='bold'>" +
                                            _(u"Test\nPlanning") +
                                            "</span>")
            self.lblTestPlanning.set_alignment(xalign=0.5, yalign=0.5)
            self.lblTestPlanning.set_justify(gtk.JUSTIFY_CENTER)
            self.lblTestPlanning.show_all()
            self.lblTestPlanning.set_tooltip_text(_(u"Assists in planning of "
                                                    u"the software test "
                                                    u"program."))
            notebook.insert_page(self.hpnTestPlanning,
                                 tab_label=self.lblTestPlanning,
                                 position=-1)

            return False

        def _create_assessment_results_page(self, notebook):
            """
            Function to create the Software class gtk.Notebook() page for
            displaying reliability estimates for the selected Software.

            :param self: the current instance of a Software class.
            :type self: Software class
            :param notebook: the Software class gtk.Notebook() widget.
            :type notebook: gtk.Notebook
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Reliability Estimation "
                                              u"Results"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _labels = [_(u"Average FR During Test:"),
                       _(u"Failure Rate at EOT:"),
                       _(u"Average REN:"), _(u"EOT REN:"),
                       _(u"Number of Exception Conditions:"),
                       _(u"Input Variability:"), _(u"Total Execution Time:"),
                       _(u"OS Overhead Time:"), _(u"Workload:"),
                       _(u"Operating Environment Factor:"),
                       _(u"Estimated Failure Rate:")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 25

            self.txtFT1.set_tooltip_text(_(u"Displays the average failure "
                                           u"rate during test for the "
                                           u"selected software module."))
            self.txtFT2.set_tooltip_text(_(u"Displays the failure rate at the "
                                           u"end of test for the selected "
                                           u"software module."))
            self.txtRENAVG.set_tooltip_text(_(u"Displays the average "
                                              u"Reliability Estimation Number "
                                              u"(REN) for the selected "
                                              u"software module."))
            self.txtRENEOT.set_tooltip_text(_(u"Displays the end of test "
                                              u"Reliability Estimation Number "
                                              u"(REN) for the selected "
                                              u"software module."))
            self.txtEC.set_tooltip_text(_(u"Displays the number of exception "
                                          u"conditions for the selected "
                                          u"software module."))
            self.txtEV.set_tooltip_text(_(u"Displays the variability of input "
                                          u"for the selected software "
                                          u"module."))
            self.txtET.set_tooltip_text(_(u"Displays the total execution time "
                                          u"for the selected software "
                                          u"module."))
            self.txtOS.set_tooltip_text(_(u"Displays the operating system "
                                          u"overhead time for the selected "
                                          u"software module."))
            self.txtEW.set_tooltip_text(_(u"Displays the workload for the "
                                          u"selected software module."))
            self.txtE.set_tooltip_text(_(u"Displays the operating environment "
                                         u"factor for the selected software "
                                         u"module."))
            self.txtF.set_tooltip_text(_(u"Displays the estimated failure "
                                         u"rate for the selected software "
                                         u"module."))

            _fixed.put(self.txtFT1, _x_pos, _y_pos[0])
            _fixed.put(self.txtFT2, _x_pos, _y_pos[1])
            _fixed.put(self.txtRENAVG, _x_pos, _y_pos[2])
            _fixed.put(self.txtRENEOT, _x_pos, _y_pos[3])
            _fixed.put(self.txtEC, _x_pos, _y_pos[4])
            _fixed.put(self.txtEV, _x_pos, _y_pos[5])
            _fixed.put(self.txtET, _x_pos, _y_pos[6])
            _fixed.put(self.txtOS, _x_pos, _y_pos[7])
            _fixed.put(self.txtEW, _x_pos, _y_pos[8])
            _fixed.put(self.txtE, _x_pos, _y_pos[9])
            _fixed.put(self.txtF, _x_pos, _y_pos[10])

            self.txtEC.connect('focus-out-event', self._callback_entry,
                               'float', 63)
            self.txtET.connect('focus-out-event', self._callback_entry,
                               'float', 65)
            self.txtOS.connect('focus-out-event', self._callback_entry,
                               'float', 66)

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Reliability\nEstimation") +
                              "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays software reliability "
                                      u"estimation results."))
            notebook.insert_page(_frame,
                                 tab_label=_label,
                                 position=-1)

            return False

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        _create_general_data_page(self, _notebook)
        _create_risk_analysis_page(self, _notebook)
        _create_test_planning_page(self, _notebook)
# TODO: Implement the software reliability assessment page creation.
        #_create_assessment_results_page(self, _notebook)

        return _notebook

    def _create_risk_analysis_notebook(self):
        """
        Method to create the Software class risk analysis gtk.Notebook().

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _create_development_environment_page(self):
            """
            Funtion to create the development environment risk analysis
            page and add it to the risk analysis gtk.Notebook().
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hpaned = gtk.HPaned()

            _hbox_left = gtk.HBox()
            _hpaned.pack1(_hbox_left, resize=True, shrink=True)

            _hbox_right = gtk.HBox()
            _hpaned.pack2(_hbox_right, resize=True, shrink=True)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display risk analysis information.  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the organizational risk pane.
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Organization"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _hbox_left.pack_start(_frame)

            _labels = [_(u"There are separate design and coding "
                         u"organizations."),
                       _(u"There is an independent software test "
                         u"organization."),
                       _(u"There is an independent software quality assurance "
                         u"organization."),
                       _(u"There is an independent software configuration "
                         u"management organization."),
                       _(u"There is an independent software verification and "
                         u"validation organization."),
                       _(u"A structured programming team will develop the "
                         u"software."),
                       _(u"The educational level of the software team members "
                         u"is above average."),
                       _(u"The experience level of the software team members "
                         u"is above average.")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 45

            _fixed.put(self.chkDevEnvQ1, _x_pos, _y_pos[0])
            _fixed.put(self.chkDevEnvQ2, _x_pos, _y_pos[1])
            _fixed.put(self.chkDevEnvQ3, _x_pos, _y_pos[2])
            _fixed.put(self.chkDevEnvQ4, _x_pos, _y_pos[3])
            _fixed.put(self.chkDevEnvQ5, _x_pos, _y_pos[4])
            _fixed.put(self.chkDevEnvQ6, _x_pos, _y_pos[5])
            _fixed.put(self.chkDevEnvQ7, _x_pos, _y_pos[6])
            _fixed.put(self.chkDevEnvQ8, _x_pos, _y_pos[7])

            self.chkDevEnvQ1.connect('toggled', self._callback_check, 100)
            self.chkDevEnvQ2.connect('toggled', self._callback_check, 101)
            self.chkDevEnvQ3.connect('toggled', self._callback_check, 102)
            self.chkDevEnvQ4.connect('toggled', self._callback_check, 103)
            self.chkDevEnvQ5.connect('toggled', self._callback_check, 104)
            self.chkDevEnvQ6.connect('toggled', self._callback_check, 105)
            self.chkDevEnvQ7.connect('toggled', self._callback_check, 106)
            self.chkDevEnvQ8.connect('toggled', self._callback_check, 107)

            # Create the methods risk pane.
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Methods"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _hbox_left.pack_end(_frame)

            _labels = [_(u"Standards are defined and will be enforced."),
                       _(u"Software will be developed using a higher order "
                         u"language."),
                       _(u"The development process will include formal "
                         u"reviews (PDR, CDR, etc.)."),
                       _(u"The development process will include frequent "
                         u"walkthroughs."),
                       _(u"Development will take a top-down and structured "
                         u"approach."),
                       _(u"Unit development folders will be used."),
                       _(u"A software development library will be used."),
                       _(u"A formal change and error reporting process will "
                         u"be used."),
                       _(u"Progress and status will routinely be reported.")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 45

            _fixed.put(self.chkDevEnvQ9, _x_pos, _y_pos[0])
            _fixed.put(self.chkDevEnvQ10, _x_pos, _y_pos[1])
            _fixed.put(self.chkDevEnvQ11, _x_pos, _y_pos[2])
            _fixed.put(self.chkDevEnvQ12, _x_pos, _y_pos[3])
            _fixed.put(self.chkDevEnvQ13, _x_pos, _y_pos[4])
            _fixed.put(self.chkDevEnvQ14, _x_pos, _y_pos[5])
            _fixed.put(self.chkDevEnvQ15, _x_pos, _y_pos[6])
            _fixed.put(self.chkDevEnvQ16, _x_pos, _y_pos[7])
            _fixed.put(self.chkDevEnvQ17, _x_pos, _y_pos[8])

            self.chkDevEnvQ9.connect('toggled', self._callback_check, 108)
            self.chkDevEnvQ10.connect('toggled', self._callback_check, 109)
            self.chkDevEnvQ11.connect('toggled', self._callback_check, 110)
            self.chkDevEnvQ12.connect('toggled', self._callback_check, 111)
            self.chkDevEnvQ13.connect('toggled', self._callback_check, 112)
            self.chkDevEnvQ14.connect('toggled', self._callback_check, 113)
            self.chkDevEnvQ15.connect('toggled', self._callback_check, 114)
            self.chkDevEnvQ16.connect('toggled', self._callback_check, 115)
            self.chkDevEnvQ17.connect('toggled', self._callback_check, 116)

            # Create the documentation risk pane.
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Documentation"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _hbox_right.pack_start(_frame)

            _labels = [_(u"System requirements specifications will be "
                         u"documented."),
                       _(u"Software requirements specifications will be "
                         u"documented."),
                       _(u"Interface design specifications will be "
                         u"documented."),
                       _(u"Software design specification will be documented."),
                       _(u"Test plans, procedures, and reports will be "
                         u"documented."),
                       _(u"The software development plan will be documented."),
                       _(u"The software quality assurance plan will be "
                         u"documented."),
                       _(u"The software configuration management plan will be "
                         u"documented."),
                       _(u"A requirements traceability matrix will be used."),
                       _(u"The software version description will be "
                         u"documented."),
                       _(u"All software discrepancies will be documented.")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 45

            _fixed.put(self.chkDevEnvQ18, _x_pos, _y_pos[0])
            _fixed.put(self.chkDevEnvQ19, _x_pos, _y_pos[1])
            _fixed.put(self.chkDevEnvQ20, _x_pos, _y_pos[2])
            _fixed.put(self.chkDevEnvQ21, _x_pos, _y_pos[3])
            _fixed.put(self.chkDevEnvQ22, _x_pos, _y_pos[4])
            _fixed.put(self.chkDevEnvQ23, _x_pos, _y_pos[5])
            _fixed.put(self.chkDevEnvQ24, _x_pos, _y_pos[6])
            _fixed.put(self.chkDevEnvQ25, _x_pos, _y_pos[7])
            _fixed.put(self.chkDevEnvQ26, _x_pos, _y_pos[8])
            _fixed.put(self.chkDevEnvQ27, _x_pos, _y_pos[9])
            _fixed.put(self.chkDevEnvQ28, _x_pos, _y_pos[10])

            self.chkDevEnvQ18.connect('toggled', self._callback_check, 117)
            self.chkDevEnvQ19.connect('toggled', self._callback_check, 118)
            self.chkDevEnvQ20.connect('toggled', self._callback_check, 119)
            self.chkDevEnvQ21.connect('toggled', self._callback_check, 120)
            self.chkDevEnvQ22.connect('toggled', self._callback_check, 121)
            self.chkDevEnvQ23.connect('toggled', self._callback_check, 122)
            self.chkDevEnvQ24.connect('toggled', self._callback_check, 123)
            self.chkDevEnvQ25.connect('toggled', self._callback_check, 124)
            self.chkDevEnvQ26.connect('toggled', self._callback_check, 125)
            self.chkDevEnvQ27.connect('toggled', self._callback_check, 126)
            self.chkDevEnvQ28.connect('toggled', self._callback_check, 127)

            # Create the tools and test techniques risk pane.
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Tools &amp; Test Techniques"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _hbox_right.pack_end(_frame)

            _labels = [_(u"The software language requirements will be "
                         u"specified."),
                       _(u"Formal program design language will be used."),
                       _(u"Program design graphical techniques (flowcharts, "
                         u"HIPO, etc.) will be used."),
                       _(u"Simulation/emulation tools will be used."),
                       _(u"Configuration management tools will be used."),
                       _(u"A code auditing tool will be used."),
                       _(u"A data flow analyzer will be used."),
                       _(u"A programmer's workbench will be used."),
                       _(u"Measurement tools will be used."),
                       _(u"Software code reviews will be used."),
                       _(u"Software branch testing will be used."),
                       _(u"Random testing will be used."),
                       _(u"Functional testing will be used."),
                       _(u"Error and anomaly detection testing will be used."),
                       _(u"Structure analysis will be used.")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 45

            _fixed.put(self.chkDevEnvQ29, _x_pos, _y_pos[0])
            _fixed.put(self.chkDevEnvQ30, _x_pos, _y_pos[1])
            _fixed.put(self.chkDevEnvQ31, _x_pos, _y_pos[2])
            _fixed.put(self.chkDevEnvQ32, _x_pos, _y_pos[3])
            _fixed.put(self.chkDevEnvQ33, _x_pos, _y_pos[4])
            _fixed.put(self.chkDevEnvQ34, _x_pos, _y_pos[5])
            _fixed.put(self.chkDevEnvQ35, _x_pos, _y_pos[6])
            _fixed.put(self.chkDevEnvQ36, _x_pos, _y_pos[7])
            _fixed.put(self.chkDevEnvQ37, _x_pos, _y_pos[8])
            _fixed.put(self.chkDevEnvQ38, _x_pos, _y_pos[9])
            _fixed.put(self.chkDevEnvQ39, _x_pos, _y_pos[10])
            _fixed.put(self.chkDevEnvQ40, _x_pos, _y_pos[11])
            _fixed.put(self.chkDevEnvQ41, _x_pos, _y_pos[12])
            _fixed.put(self.chkDevEnvQ42, _x_pos, _y_pos[13])
            _fixed.put(self.chkDevEnvQ43, _x_pos, _y_pos[14])

            self.chkDevEnvQ29.connect('toggled', self._callback_check, 128)
            self.chkDevEnvQ30.connect('toggled', self._callback_check, 129)
            self.chkDevEnvQ31.connect('toggled', self._callback_check, 130)
            self.chkDevEnvQ32.connect('toggled', self._callback_check, 131)
            self.chkDevEnvQ33.connect('toggled', self._callback_check, 132)
            self.chkDevEnvQ34.connect('toggled', self._callback_check, 133)
            self.chkDevEnvQ35.connect('toggled', self._callback_check, 134)
            self.chkDevEnvQ36.connect('toggled', self._callback_check, 135)
            self.chkDevEnvQ37.connect('toggled', self._callback_check, 136)
            self.chkDevEnvQ38.connect('toggled', self._callback_check, 137)
            self.chkDevEnvQ39.connect('toggled', self._callback_check, 138)
            self.chkDevEnvQ40.connect('toggled', self._callback_check, 139)
            self.chkDevEnvQ41.connect('toggled', self._callback_check, 140)
            self.chkDevEnvQ42.connect('toggled', self._callback_check, 141)
            self.chkDevEnvQ43.connect('toggled', self._callback_check, 142)

            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Development\nEnvironment") +
                              "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_angle(90)
            _label.show_all()
            _label.set_tooltip_text(_(u"Assesses risk due to the development "
                                      u"environment."))
            self.nbkRiskAnalysis.insert_page(_hpaned,
                                             tab_label=_label,
                                             position=-1)

        def _create_srr_page(self):
            """
            Function to create the risk analysis page to be completed at the
            requirements review phase and add it to the risk analysis
            gtk.Notebook().
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display risk analysis information.  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the anomaly management risk pane.
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Anomaly Management"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            self.hpnSRR.pack1(_frame, resize=True, shrink=True)

            _labels = [_(u"Number of instances of different processes (or "
                         u"functions, subfunctions) which are required to be "
                         u"executed at the same time (i.e., concurrent "
                         u"processing):"),
                       _(u"Number of instances of concurrent processing "
                         u"required to be centrally controlled:"),
                       _(u"Number of error conditions required to be "
                         u"recognized/identified:"),
                       _(u"Number of recognized error conditions that require "
                         u"recovery or repair:"),
                       _(u"There is a standard for handling recognized errors "
                         u"such that all error conditions are passed to the "
                         u"calling function."),
                       _(u"Number of instances of the same process (or "
                         u"function, subfunction) being required to execute "
                         u"more than once for comparison purposes (i.e., "
                         u"polling of parallel or redundant processing "
                         u"results):"),
                       _(u"Number of instances of parallel/redundant "
                         u"processing that are required to be centrally "
                         u"controlled:"),
                       _(u"Error tolerances are specified for all applicable "
                         u"external input data (i.e., range of numerical "
                         u"values, legal  combinations of alphanumerical "
                         u"values)."),
                       _(u"There are requirements for detection of and/or "
                         u"recovery from all computational failures."),
                       _(u"There are requirements to range test all critical "
                         u"loop and multiple transfer index parameters before "
                         u"used."),
                       _(u"There are requirements to range test all critical "
                         u"subscript values before use."),
                       _(u"There are requirements to range test all critical "
                         u"output data before final outputting."),
                       _(u"There are requirements for recovery from all "
                         u"detected hardware faults."),
                       _(u"There are requirements for recovery from all I/O "
                         u"divide errors."),
                       _(u"There are requirements for recovery from all "
                         u"communication transmission errors."),
                       _(u"There are requirements for recovery from all "
                         u"failures to communicate with other nodes or other "
                         u"systems."),
                       _(u"There are requirements to periodically check "
                         u"adjacent nodes or operating system for operational "
                         u"status."),
                       _(u"There are requirements to provide a strategy for "
                         u"alternating routing of messages."),
                       _(u"There are requirements to ensure communication "
                         u"paths to all remaining nodes/communication links "
                         u"in the event of a failure of one node/link."),
                       _(u"There are requirements for maintaining the "
                         u"integrity of all data values following the "
                         u"occurence of anomalous conditions."),
                       _(u"There are requirements to enable all disconnected "
                         u"nodes to rejoin the network after recovery, such "
                         u"that the processing functions of the system are "
                         u"not interrupted."),
                       _(u"There are requirements to replicate all critical "
                         u"data at two or more distinct nodes.")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 45

            _fixed.put(self.txtSRRAMQ1, _x_pos, _y_pos[0])
            _fixed.put(self.txtSRRAMQ2, _x_pos, _y_pos[1])
            _fixed.put(self.txtSRRAMQ3, _x_pos, _y_pos[2])
            _fixed.put(self.txtSRRAMQ4, _x_pos, _y_pos[3])
            _fixed.put(self.chkSRRAMQ5, _x_pos, _y_pos[4])
            _fixed.put(self.txtSRRAMQ6, _x_pos, _y_pos[5])
            _fixed.put(self.txtSRRAMQ7, _x_pos, _y_pos[6])
            _fixed.put(self.chkSRRAMQ8, _x_pos, _y_pos[7])
            _fixed.put(self.chkSRRAMQ9, _x_pos, _y_pos[8])
            _fixed.put(self.chkSRRAMQ10, _x_pos, _y_pos[9])
            _fixed.put(self.chkSRRAMQ11, _x_pos, _y_pos[10])
            _fixed.put(self.chkSRRAMQ12, _x_pos, _y_pos[11])
            _fixed.put(self.chkSRRAMQ13, _x_pos, _y_pos[12])
            _fixed.put(self.chkSRRAMQ14, _x_pos, _y_pos[13])
            _fixed.put(self.chkSRRAMQ15, _x_pos, _y_pos[14])
            _fixed.put(self.chkSRRAMQ16, _x_pos, _y_pos[15])
            _fixed.put(self.chkSRRAMQ17, _x_pos, _y_pos[16])
            _fixed.put(self.chkSRRAMQ18, _x_pos, _y_pos[17])
            _fixed.put(self.chkSRRAMQ19, _x_pos, _y_pos[18])
            _fixed.put(self.chkSRRAMQ20, _x_pos, _y_pos[19])
            _fixed.put(self.chkSRRAMQ21, _x_pos, _y_pos[20])
            _fixed.put(self.chkSRRAMQ22, _x_pos, _y_pos[21])

            self.txtSRRAMQ1.connect('focus-out-event', self._callback_entry,
                                    'int', 200)
            self.txtSRRAMQ2.connect('focus-out-event', self._callback_entry,
                                    'int', 201)
            self.txtSRRAMQ3.connect('focus-out-event', self._callback_entry,
                                    'int', 202)
            self.txtSRRAMQ4.connect('focus-out-event', self._callback_entry,
                                    'int', 203)
            self.chkSRRAMQ5.connect('toggled', self._callback_check, 204)
            self.txtSRRAMQ6.connect('focus-out-event', self._callback_entry,
                                    'int', 205)
            self.txtSRRAMQ7.connect('focus-out-event', self._callback_entry,
                                    'int', 206)
            self.chkSRRAMQ8.connect('toggled', self._callback_check, 207)
            self.chkSRRAMQ9.connect('toggled', self._callback_check, 208)
            self.chkSRRAMQ10.connect('toggled', self._callback_check, 209)
            self.chkSRRAMQ11.connect('toggled', self._callback_check, 210)
            self.chkSRRAMQ12.connect('toggled', self._callback_check, 211)
            self.chkSRRAMQ13.connect('toggled', self._callback_check, 212)
            self.chkSRRAMQ14.connect('toggled', self._callback_check, 213)
            self.chkSRRAMQ15.connect('toggled', self._callback_check, 214)
            self.chkSRRAMQ16.connect('toggled', self._callback_check, 215)
            self.chkSRRAMQ17.connect('toggled', self._callback_check, 216)
            self.chkSRRAMQ18.connect('toggled', self._callback_check, 217)
            self.chkSRRAMQ19.connect('toggled', self._callback_check, 218)
            self.chkSRRAMQ20.connect('toggled', self._callback_check, 219)
            self.chkSRRAMQ21.connect('toggled', self._callback_check, 220)
            self.chkSRRAMQ22.connect('toggled', self._callback_check, 221)

            # Create the quality control risk pane.
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Software Quality Control"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            self.hpnSRR.pack2(_frame, resize=True, shrink=True)

            _labels = [_(u"There is a table(s) tracing all requirements to "
                         u"the parent system or subsystem specification."),
                       _(u"There are quantitative accuracy requirements for "
                         u"all inputs associated with each function."),
                       _(u"There are quantitative accuracy requirements for "
                         u"all outputs associated with each function."),
                       _(u"There are quantitative accuracy requirements for "
                         u"all constants associated with each function."),
                       _(u"The existing math library routines which are "
                         u"planned for use provide enough precision to "
                         u"support accuracy objectives."),
                       _(u"All processes and functions are partitioned to be "
                         u"logically complete and self contained so as to "
                         u"minimize interface complexity."),
                       _(u"There are requirements for each operational "
                         u"CPU/System to have a separate power source."),
                       _(u"There are requirements for the executive software "
                         u"to perform testing of its own operation and of the "
                         u"communication links, memory devices, and "
                         u"peripheral devices."),
                       _(u"All inputs, processing, and outputs are clearly "
                         u"and precisely defined."),
                       _(u"Number of data references that are identified:"),
                       _(u"Number of identified data references that are "
                         u"documented with regard to source, meaning, and "
                         u"format:"),
                       _(u"Number of data items that are identified (e.g., "
                         u"documented with regard to source, meaning, and "
                         u"format):"),
                       _(u"Number of data items that are referenced:"),
                       _(u"All defined functions have been referenced."),
                       _(u"All system functions allocated to this module have "
                         u"been allocated to software functions within this "
                         u"module."),
                       _(u"All referenced functions have been defined (i.e., "
                         u"documented with precise inputs, processing, and "
                         u"output requirements)."),
                       _(u"The flow of processing (algorithms) and all "
                         u"decision points (conditions and alternate paths) "
                         u"in the flow is described for all functions."),
                       _(u"Specific standards have been established for "
                         u"design representations (e.g., HIPO charts, program "
                         u"design language, flow charts, data flow "
                         u"diagrams)."),
                       _(u"Specific standards have been established for "
                         u"calling sequence protocol between software units."),
                       _(u"Specific standards have been established for "
                         u"external I/O protocol and format for all software "
                         u"units."),
                       _(u"Specific standards have been established for error "
                         u"handling for all software units."),
                       _(u"All references to the same function use a single, "
                         u"unique name."),
                       _(u"Specific standards have been established for all "
                         u"data representation in the design."),
                       _(u"Specific standards have been established for the "
                         u"naming of all data."),
                       _(u"Specific standards have been established for the "
                         u"definition and use of global variables."),
                       _(u"There are procedures for establishing consistency "
                         u"and concurrency of multiple copies (e.g., copies "
                         u"at different nodes) of the same software or "
                         u"database version."),
                       _(u"There are procedures for verifying consistency and "
                         u"concurrency of multiple copies (e.g., copies at "
                         u"different nodes) of the same software or database "
                         u"version."),
                       _(u"All references to the same data use a single, "
                         u"unique name.")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 45

            _fixed.put(self.chkSRRSTQ1, _x_pos, _y_pos[0])
            _fixed.put(self.chkSRRQCQ1, _x_pos, _y_pos[1])
            _fixed.put(self.chkSRRQCQ2, _x_pos, _y_pos[2])
            _fixed.put(self.chkSRRQCQ3, _x_pos, _y_pos[3])
            _fixed.put(self.chkSRRQCQ4, _x_pos, _y_pos[4])
            _fixed.put(self.chkSRRQCQ5, _x_pos, _y_pos[5])
            _fixed.put(self.chkSRRQCQ6, _x_pos, _y_pos[6])
            _fixed.put(self.chkSRRQCQ7, _x_pos, _y_pos[7])
            _fixed.put(self.chkSRRQCQ8, _x_pos, _y_pos[8])
            _fixed.put(self.txtSRRQCQ9, _x_pos, _y_pos[9])
            _fixed.put(self.txtSRRQCQ10, _x_pos, _y_pos[10])
            _fixed.put(self.txtSRRQCQ11, _x_pos, _y_pos[11])
            _fixed.put(self.txtSRRQCQ12, _x_pos, _y_pos[12])
            _fixed.put(self.chkSRRQCQ13, _x_pos, _y_pos[13])
            _fixed.put(self.chkSRRQCQ14, _x_pos, _y_pos[14])
            _fixed.put(self.chkSRRQCQ15, _x_pos, _y_pos[15])
            _fixed.put(self.chkSRRQCQ16, _x_pos, _y_pos[16])
            _fixed.put(self.chkSRRQCQ17, _x_pos, _y_pos[17])
            _fixed.put(self.chkSRRQCQ18, _x_pos, _y_pos[18])
            _fixed.put(self.chkSRRQCQ19, _x_pos, _y_pos[19])
            _fixed.put(self.chkSRRQCQ20, _x_pos, _y_pos[20])
            _fixed.put(self.chkSRRQCQ21, _x_pos, _y_pos[21])
            _fixed.put(self.chkSRRQCQ22, _x_pos, _y_pos[22])
            _fixed.put(self.chkSRRQCQ23, _x_pos, _y_pos[23])
            _fixed.put(self.chkSRRQCQ24, _x_pos, _y_pos[24])
            _fixed.put(self.chkSRRQCQ25, _x_pos, _y_pos[25])
            _fixed.put(self.chkSRRQCQ26, _x_pos, _y_pos[26])
            _fixed.put(self.chkSRRQCQ27, _x_pos, _y_pos[27])

            self.chkSRRSTQ1.connect('toggled', self._callback_check, 222)
            self.chkSRRQCQ1.connect('toggled', self._callback_check, 223)
            self.chkSRRQCQ2.connect('toggled', self._callback_check, 224)
            self.chkSRRQCQ3.connect('toggled', self._callback_check, 225)
            self.chkSRRQCQ4.connect('toggled', self._callback_check, 226)
            self.chkSRRQCQ5.connect('toggled', self._callback_check, 227)
            self.chkSRRQCQ6.connect('toggled', self._callback_check, 228)
            self.chkSRRQCQ7.connect('toggled', self._callback_check, 229)
            self.chkSRRQCQ8.connect('toggled', self._callback_check, 230)
            self.txtSRRQCQ9.connect('focus-out-event', self._callback_entry,
                                    'int', 231)
            self.txtSRRQCQ10.connect('focus-out-event', self._callback_entry,
                                     'int', 232)
            self.txtSRRQCQ11.connect('focus-out-event', self._callback_entry,
                                     'int', 233)
            self.txtSRRQCQ12.connect('focus-out-event', self._callback_entry,
                                     'int', 234)
            self.chkSRRQCQ13.connect('toggled', self._callback_check, 235)
            self.chkSRRQCQ14.connect('toggled', self._callback_check, 236)
            self.chkSRRQCQ15.connect('toggled', self._callback_check, 237)
            self.chkSRRQCQ16.connect('toggled', self._callback_check, 238)
            self.chkSRRQCQ17.connect('toggled', self._callback_check, 239)
            self.chkSRRQCQ18.connect('toggled', self._callback_check, 240)
            self.chkSRRQCQ19.connect('toggled', self._callback_check, 241)
            self.chkSRRQCQ20.connect('toggled', self._callback_check, 242)
            self.chkSRRQCQ21.connect('toggled', self._callback_check, 243)
            self.chkSRRQCQ22.connect('toggled', self._callback_check, 244)
            self.chkSRRQCQ23.connect('toggled', self._callback_check, 245)
            self.chkSRRQCQ24.connect('toggled', self._callback_check, 246)
            self.chkSRRQCQ25.connect('toggled', self._callback_check, 247)
            self.chkSRRQCQ26.connect('toggled', self._callback_check, 248)
            self.chkSRRQCQ27.connect('toggled', self._callback_check, 249)

            self.lblSRR.set_markup("<span weight='bold'>" +
                                   _("Requirements\nReview") +
                                   "</span>")
            self.lblSRR.set_alignment(xalign=0.5, yalign=0.5)
            self.lblSRR.set_justify(gtk.JUSTIFY_CENTER)
            self.lblSRR.set_angle(90)
            self.lblSRR.show_all()
            self.lblSRR.set_tooltip_text(_(u"Allows assessment of the "
                                           u"reliability risk at the "
                                           u"requirements review phase."))
            self.nbkRiskAnalysis.insert_page(self.hpnSRR,
                                             tab_label=self.lblSRR,
                                             position=-1)

            return False

        def _create_pdr_page(self):
            """
            Function to create the risk analysis page to be completed at the
            preliminary design review phase and add it to the risk analysis
            gtk.Notebook().
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display risk analysis information.  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the anomaly management risk pane.
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Anomaly Management"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            self.hpnPDR.pack1(_frame, resize=True, shrink=True)

            _labels = [_(u"There are provisions for recovery from all "
                         u"computational errors."),
                       _(u"There are provisions for recovery from all "
                         u"detected hardware faults (e.g., arithmetic faults, "
                         u"power failure, clock interrupt)."),
                       _(u"There are provisions for recovery from all I/O "
                         u"device errors."),
                       _(u"There are provisions for recovery from all "
                         u"communication transmission errors."),
                       _(u"Error checking information (e.g., checksum, parity "
                         u"bit) is computed and transmitted with all "
                         u"messages."),
                       _(u"Error checking information is computed and "
                         u"compared with all message receptions."),
                       _(u"Transmission retries are limited for all "
                         u"transmissions."),
                       _(u"There are provisions for recovery from all "
                         u"failures to communicate with other nodes or other "
                         u"systems."),
                       _(u"There are provisions to periodically check all "
                         u"adjacent nodes or operating systems for "
                         u"operational status."),
                       _(u"There are provisions for alternate routing of "
                         u"messages."),
                       _(u"Communication paths exist to all remaining "
                         u"nodes/links in the event of a failure of one "
                         u"node/link."),
                       _(u"The integrity of all data values is maintained "
                         u"following the occurence of anomalous conditions."),
                       _(u"All disconnected nodes can rejoin the network "
                         u"after recovery, such that the processing functions "
                         u"of the system are not interrupted."),
                       _(u"All critical data in the module is replicated at "
                         u"two or more distinct nodes")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 45

            _fixed.put(self.chkPDRAMQ1, _x_pos, _y_pos[0])
            _fixed.put(self.chkPDRAMQ2, _x_pos, _y_pos[1])
            _fixed.put(self.chkPDRAMQ3, _x_pos, _y_pos[2])
            _fixed.put(self.chkPDRAMQ4, _x_pos, _y_pos[3])
            _fixed.put(self.chkPDRAMQ5, _x_pos, _y_pos[4])
            _fixed.put(self.chkPDRAMQ6, _x_pos, _y_pos[5])
            _fixed.put(self.chkPDRAMQ7, _x_pos, _y_pos[6])
            _fixed.put(self.chkPDRAMQ8, _x_pos, _y_pos[7])
            _fixed.put(self.chkPDRAMQ9, _x_pos, _y_pos[8])
            _fixed.put(self.chkPDRAMQ10, _x_pos, _y_pos[9])
            _fixed.put(self.chkPDRAMQ11, _x_pos, _y_pos[10])
            _fixed.put(self.chkPDRAMQ12, _x_pos, _y_pos[11])
            _fixed.put(self.chkPDRAMQ13, _x_pos, _y_pos[12])
            _fixed.put(self.chkPDRAMQ14, _x_pos, _y_pos[13])

            self.chkPDRAMQ1.connect('toggled', self._callback_check, 300)
            self.chkPDRAMQ2.connect('toggled', self._callback_check, 301)
            self.chkPDRAMQ3.connect('toggled', self._callback_check, 302)
            self.chkPDRAMQ4.connect('toggled', self._callback_check, 303)
            self.chkPDRAMQ5.connect('toggled', self._callback_check, 304)
            self.chkPDRAMQ6.connect('toggled', self._callback_check, 305)
            self.chkPDRAMQ7.connect('toggled', self._callback_check, 306)
            self.chkPDRAMQ8.connect('toggled', self._callback_check, 307)
            self.chkPDRAMQ9.connect('toggled', self._callback_check, 308)
            self.chkPDRAMQ10.connect('toggled', self._callback_check, 309)
            self.chkPDRAMQ11.connect('toggled', self._callback_check, 310)
            self.chkPDRAMQ12.connect('toggled', self._callback_check, 311)
            self.chkPDRAMQ13.connect('toggled', self._callback_check, 312)
            self.chkPDRAMQ14.connect('toggled', self._callback_check, 313)

            # Create the software quality control risk pane.
            _fixed = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed)

            _frame = _widg.make_frame(label=_(u"Software Quality Control"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            self.hpnPDR.pack2(_frame, resize=True, shrink=True)

            _labels = [_(u"There is a table tracing all the top-level CSC "
                         u"allocated requirements to the parent CSCI "
                         u"specification."),
                       _(u"The numerical techniques used in implementing "
                         u"applicable functions provide enough precision to "
                         u"support accuracy objectives."),
                       _(u"All processes and functions are partitioned to be "
                         u"logically complete and self-contained so as to "
                         u"minimize interface complexity."),
                       _(u"Estimated process time typically spent executing "
                         u"the entire module:"),
                       _(u"Estimated process time typically spent in "
                         u"execution of hardware and device interface "
                         u"protocol:"),
                       _(u"The executive software performs testing of its own "
                         u"operation and of the communication links, memory "
                         u"devices, and peripheral devices."),
                       _(u"All inputs, processing, and outputs are clearly "
                         u"and precisely defined."),
                       _(u"Number of data references that are defined:"),
                       _(u"Number of identified data references that are "
                         u"documented with regard to source, meaning, and "
                         u"format:"),
                       _(u"Number of data items that are defined (i.e., "
                         u"documented with regard to source, meaning, and "
                         u"format):"),
                       _(u"Number of data items that are referenced:"),
                       _(u"Number of data references that are identified:"),
                       _(u"Number of identified data references that are "
                         u"computed or obtained from an external source "
                         u"(e.g., referencing global data with preassigned "
                         u"values, input parameters with preassigned "
                         u"values):"),
                       _(u"Number of software discrepancy reports have been "
                         u"recorded, to date:"),
                       _(u"Number of software discrepancy reports have been "
                         u"closed, to date:"),
                       _(u"All functions of this module been allocated to "
                         u"top-level module."),
                       _(u"All conditions and alternative processing options "
                         u"are defined for each decision point."),
                       _(u"Design representations are in the formats of the "
                         u"established standard."),
                       _(u"All references to the same top-level module use a "
                         u"single, unique name."),
                       _(u"All data representation complies with the "
                         u"established standard."),
                       _(u"The naming of all data complies with the "
                         u"established standard."),
                       _(u"The definition and use of all global variables is "
                         u"in accordange with the established standard."),
                       _(u"There are procedures for establishing consistency "
                         u"and concurrency of multiple copies of the same "
                         u"software or data base version."),
                       _(u"There are procedures for verifying the consistency "
                         u"and concurrency of multiples copies of the same "
                         u"software or data base version."),
                       _(u"All references to the same data use a single, "
                         u"unique name.")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5)
            _x_pos += 45

            _fixed.put(self.chkPDRSTQ1, _x_pos, _y_pos[0])
            _fixed.put(self.chkPDRQCQ1, _x_pos, _y_pos[1])
            _fixed.put(self.chkPDRQCQ2, _x_pos, _y_pos[2])
            _fixed.put(self.txtPDRQCQ3, _x_pos, _y_pos[3])
            _fixed.put(self.txtPDRQCQ4, _x_pos, _y_pos[4])
            _fixed.put(self.chkPDRQCQ5, _x_pos, _y_pos[5])
            _fixed.put(self.chkPDRQCQ6, _x_pos, _y_pos[6])
            _fixed.put(self.txtPDRQCQ7, _x_pos, _y_pos[7])
            _fixed.put(self.txtPDRQCQ8, _x_pos, _y_pos[8])
            _fixed.put(self.txtPDRQCQ9, _x_pos, _y_pos[9])
            _fixed.put(self.txtPDRQCQ10, _x_pos, _y_pos[10])
            _fixed.put(self.txtPDRQCQ11, _x_pos, _y_pos[11])
            _fixed.put(self.txtPDRQCQ12, _x_pos, _y_pos[12])
            _fixed.put(self.chkPDRQCQ13, _x_pos, _y_pos[13])
            _fixed.put(self.chkPDRQCQ14, _x_pos, _y_pos[14])
            _fixed.put(self.txtPDRQCQ15, _x_pos, _y_pos[15])
            _fixed.put(self.txtPDRQCQ16, _x_pos, _y_pos[16])
            _fixed.put(self.chkPDRQCQ17, _x_pos, _y_pos[17])
            _fixed.put(self.chkPDRQCQ18, _x_pos, _y_pos[18])
            _fixed.put(self.chkPDRQCQ19, _x_pos, _y_pos[19])
            _fixed.put(self.chkPDRQCQ20, _x_pos, _y_pos[20])
            _fixed.put(self.chkPDRQCQ21, _x_pos, _y_pos[21])
            _fixed.put(self.chkPDRQCQ22, _x_pos, _y_pos[22])
            _fixed.put(self.chkPDRQCQ23, _x_pos, _y_pos[23])
            _fixed.put(self.chkPDRQCQ24, _x_pos, _y_pos[24])

            self.chkPDRSTQ1.connect('toggled', self._callback_check, 314)
            self.chkPDRQCQ1.connect('toggled', self._callback_check, 315)
            self.chkPDRQCQ2.connect('toggled', self._callback_check, 316)
            self.txtPDRQCQ3.connect('focus-out-event', self._callback_entry,
                                    'int', 317)
            self.txtPDRQCQ4.connect('focus-out-event', self._callback_entry,
                                    'int', 318)
            self.chkPDRQCQ5.connect('toggled', self._callback_check, 319)
            self.chkPDRQCQ6.connect('toggled', self._callback_check, 320)
            self.txtPDRQCQ7.connect('focus-out-event', self._callback_entry,
                                    'int', 321)
            self.txtPDRQCQ8.connect('focus-out-event', self._callback_entry,
                                    'int', 322)
            self.txtPDRQCQ9.connect('focus-out-event', self._callback_entry,
                                    'int', 323)
            self.txtPDRQCQ10.connect('focus-out-event', self._callback_entry,
                                     'int', 324)
            self.txtPDRQCQ11.connect('focus-out-event', self._callback_entry,
                                     'int', 325)
            self.txtPDRQCQ12.connect('focus-out-event', self._callback_entry,
                                     'int', 326)
            self.chkPDRQCQ13.connect('toggled', self._callback_check, 327)
            self.chkPDRQCQ14.connect('toggled', self._callback_check, 327)
            self.txtPDRQCQ15.connect('focus-out-event', self._callback_entry,
                                     'int', 329)
            self.txtPDRQCQ16.connect('focus-out-event', self._callback_entry,
                                     'int', 330)
            self.chkPDRQCQ17.connect('toggled', self._callback_check, 331)
            self.chkPDRQCQ18.connect('toggled', self._callback_check, 332)
            self.chkPDRQCQ19.connect('toggled', self._callback_check, 333)
            self.chkPDRQCQ20.connect('toggled', self._callback_check, 334)
            self.chkPDRQCQ21.connect('toggled', self._callback_check, 335)
            self.chkPDRQCQ22.connect('toggled', self._callback_check, 336)
            self.chkPDRQCQ23.connect('toggled', self._callback_check, 337)
            self.chkPDRQCQ24.connect('toggled', self._callback_check, 338)

            self.lblPDR.set_markup("<span weight='bold'>" +
                                   _("Preliminary\nDesign\nReview") +
                                   "</span>")
            self.lblPDR.set_alignment(xalign=0.5, yalign=0.5)
            self.lblPDR.set_justify(gtk.JUSTIFY_CENTER)
            self.lblPDR.set_angle(90)
            self.lblPDR.show_all()
            self.lblPDR.set_tooltip_text(_(u"Allows assessment of the "
                                           u"reliability risk at the "
                                           u"preliminary design review."))
            self.nbkRiskAnalysis.insert_page(self.hpnPDR,
                                             tab_label=self.lblPDR,
                                             position=-1)

            return False

        def _create_cdr_page(self):
            """
            Function to create the risk analysis page to be completed at the
            critical design review phase and add it to the risk analysis
            gtk.Notebook().
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build the module-level containers and include them in the page
            # by default.
            _fxdcsciam = gtk.Fixed()
            _fxdcsciqc = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdcsciam)

            self.fraCDRCSCIAM.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraCDRCSCIAM.add(_scrollwindow)

            self.hpnCDR.pack1(self.fraCDRCSCIAM, resize=True, shrink=True)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdcsciqc)

            self.fraCDRCSCIQC.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraCDRCSCIQC.add(_scrollwindow)

            self.hpnCDR.pack2(self.fraCDRCSCIQC, resize=True, shrink=True)

            # Build the unit-level containers.
            _fxdunitam = gtk.Fixed()
            _fxdunitqc = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdunitam)

            self.fraCDRUnitAM.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraCDRUnitAM.add(_scrollwindow)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdunitqc)

            self.fraCDRUnitQC.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraCDRUnitQC.add(_scrollwindow)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display risk analysis information.  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the anomaly management risk pane for CSCI.
            _labels = [_(u"Number of units in this module:"),
                       _(u"Number of units in this module, when an error "
                         u"condition is detected, in which resolution "
                         u"the error is not determined by the calling unit:"),
                       _(u"The value of all external inputs with range "
                         u"specifications are checked with respect to the "
                         u"specified range prior to use."),
                       _(u"All external inputs are checked with respect to "
                         u"specified conflicting requests prior to use."),
                       _(u"All external inputs are checked with respect to "
                         u"specified illegal combinations prior to use."),
                       _(u"All external inputs are checked for reasonableness "
                         u"before processing begins."),
                       _(u"All detected errors, with respect to applicable "
                         u"external inputs, are reported before processing "
                         u"begins."),
                       _(u"Number of units in this module that do not perform "
                         u"a check to determine that all data is available "
                         u"before processing begins:"),
                       _(u"Critical loop and multiple transfer index "
                         u"parameters (e.g., supporting a mission-critical "
                         u"system function) are checked for out-of-range "
                         u"values before use."),
                       _(u"All critical subscripts (e.g., supporting a "
                         u"mission-critical system function) are checked for "
                         u"out-of-range values before use."),
                       _(u"All critical output data (e.g., supporting a "
                         u"mission-critical system function) are checked for "
                         u"reasonable values prior to final outputting.")]
            (_x_pos,
             _y_pos) = _widg.make_labels(_labels, _fxdcsciam, 5, 5)
            _x_pos += 45

            _fxdcsciam.put(self.txtCDRAMQ1, _x_pos, _y_pos[0])
            _fxdcsciam.put(self.txtCDRAMQ2, _x_pos, _y_pos[1])
            _fxdcsciam.put(self.chkCDRAMQ3, _x_pos, _y_pos[2])
            _fxdcsciam.put(self.chkCDRAMQ4, _x_pos, _y_pos[3])
            _fxdcsciam.put(self.chkCDRAMQ5, _x_pos, _y_pos[4])
            _fxdcsciam.put(self.chkCDRAMQ6, _x_pos, _y_pos[5])
            _fxdcsciam.put(self.chkCDRAMQ7, _x_pos, _y_pos[6])
            _fxdcsciam.put(self.txtCDRAMQ8, _x_pos, _y_pos[7])
            _fxdcsciam.put(self.chkCDRAMQ9, _x_pos, _y_pos[8])
            _fxdcsciam.put(self.chkCDRAMQ10, _x_pos, _y_pos[9])
            _fxdcsciam.put(self.chkCDRAMQ11, _x_pos, _y_pos[10])

            self.txtCDRAMQ1.connect('focus-out-event', self._callback_entry,
                                    'int', 400)
            self.txtCDRAMQ2.connect('focus-out-event', self._callback_entry,
                                    'int', 401)
            self.chkCDRAMQ3.connect('toggled', self._callback_check, 402)
            self.chkCDRAMQ4.connect('toggled', self._callback_check, 403)
            self.chkCDRAMQ5.connect('toggled', self._callback_check, 404)
            self.chkCDRAMQ6.connect('toggled', self._callback_check, 405)
            self.chkCDRAMQ7.connect('toggled', self._callback_check, 406)
            self.txtCDRAMQ8.connect('focus-out-event', self._callback_entry,
                                    'int', 407)
            self.chkCDRAMQ9.connect('toggled', self._callback_check, 408)
            self.chkCDRAMQ10.connect('toggled', self._callback_check, 409)
            self.chkCDRAMQ11.connect('toggled', self._callback_check, 410)

            # Create the anomaly management risk pane for units.
            _labels = [_(u"When an error condition is detected, the "
                         u"resolution of the error is not determined by this "
                         u"unit."),
                       _(u"The values of all applicable external inputs with "
                         u"range specifications are checked with respect to "
                         u"specified range prior to use in this unit."),
                       _(u"All applicable external inputs are checked with "
                         u"respect to specified conflicting requests prior "
                         u"to use in this unit."),
                       _(u"All applicable external inputs are checked with "
                         u"respect to specified illegal combinations prior to "
                         u"use in this unit."),
                       _(u"All applicable external inputs are checked for "
                         u"reasonableness before processing begins in this "
                         u"unit."),
                       _(u"All detected errors, with respect to applicable "
                         u"external inputs, are reported before processing "
                         u"begins in this unit."),
                       _(u"This unit does not perform a check to determine "
                         u"that all data is available before processing "
                         u"begins."),
                       _(u"Critical loop and multiple transfer index "
                         u"parameters (e.g., supporting a mission-critical "
                         u"system function) are checked for out-of-range "
                         u"values before use in this unit."),
                       _(u"All critical subscripts (e.g., supporting a "
                         u"mission-critical system function) are checked for "
                         u"out-of-range values before use in this unit."),
                       _(u"All critical output data (e.g., supporting a "
                         u"mission-critical system function) are checked for "
                         u"reasonable values prior to final outputting by "
                         u"this unit.")]
            (_x_pos,
             _y_pos) = _widg.make_labels(_labels, _fxdunitam, 5, 5)
            _x_pos += 45

            _fxdunitam.put(self.chkCDRUnitAMQ1, _x_pos, _y_pos[0])
            _fxdunitam.put(self.chkCDRUnitAMQ2, _x_pos, _y_pos[1])
            _fxdunitam.put(self.chkCDRUnitAMQ3, _x_pos, _y_pos[2])
            _fxdunitam.put(self.chkCDRUnitAMQ4, _x_pos, _y_pos[3])
            _fxdunitam.put(self.chkCDRUnitAMQ5, _x_pos, _y_pos[4])
            _fxdunitam.put(self.chkCDRUnitAMQ6, _x_pos, _y_pos[5])
            _fxdunitam.put(self.chkCDRUnitAMQ7, _x_pos, _y_pos[6])
            _fxdunitam.put(self.chkCDRUnitAMQ8, _x_pos, _y_pos[7])
            _fxdunitam.put(self.chkCDRUnitAMQ9, _x_pos, _y_pos[8])
            _fxdunitam.put(self.chkCDRUnitAMQ10, _x_pos, _y_pos[9])

            self.chkCDRUnitAMQ1.connect('toggled', self._callback_check, 437)
            self.chkCDRUnitAMQ2.connect('toggled', self._callback_check, 438)
            self.chkCDRUnitAMQ3.connect('toggled', self._callback_check, 439)
            self.chkCDRUnitAMQ4.connect('toggled', self._callback_check, 440)
            self.chkCDRUnitAMQ5.connect('toggled', self._callback_check, 441)
            self.chkCDRUnitAMQ6.connect('toggled', self._callback_check, 442)
            self.chkCDRUnitAMQ7.connect('toggled', self._callback_check, 443)
            self.chkCDRUnitAMQ8.connect('toggled', self._callback_check, 444)
            self.chkCDRUnitAMQ9.connect('toggled', self._callback_check, 445)
            self.chkCDRUnitAMQ10.connect('toggled', self._callback_check, 446)

            # Create the software quality control risk pane for CSCI.
            _labels = [_(u"The description of each software unit identifies "
                         u"all the requirements that the unit helps satisfy."),
                       _(u"The decomposition of top-level modules into "
                         u"lower-level modules and software units is "
                         u"graphically depicted."),
                       _(u"Estimated executable lines of source code in this "
                         u"module:"),
                       _(u"Estimated executable lines of source code "
                         u"necessary to handle hardware and device interface "
                         u"protocol in this module:"),
                       _(u"Number of units in this module that perform "
                         u"processing of hardware and/or device interface "
                         u"protocol:"),
                       _(u"Estimated processing time typically spent "
                         u"executing this module:"),
                       _(u"Estimated processing time typically spent in "
                         u"execution of hardware and device interface "
                         u"protocol in this module:"),
                       _(u"Number of units that clearly and precisely define "
                         u"all inputs, processing, and outputs:"),
                       _(u"Data references identified in this module:"),
                       _(u"Identified data references that are documented "
                         u"with regard to source, meaning, and format in this "
                         u"module:"),
                       _(u"Data items that are defined (i.e., documented with "
                         u"regard to source, meaning, and format) in this "
                         u"module:"),
                       _(u"Data items are referenced in this module:"),
                       _(u"Data references identified in this module:"),
                       _(u"Identified data references that are computed or "
                         u"obtained from an external source (e.g., "
                         u"referencing global data with preassigned values, "
                         u"input parameters with preassigned values) in this "
                         u"module:"),
                       _(u"Number of units that define all conditions and "
                         u"alternative processing options for each decision "
                         u"point:"),
                       _(u"Number of units in which all parameters in the "
                         u"argument list are used:"),
                       _(u"Number of software discrepancy reports recorded, "
                         u"to date, for this module:"),
                       _(u"Number of software discrepancy reports recorded "
                         u"that have been closed, to date, for this module:"),
                       _(u"Number of units in which all design "
                         u"representations are in the formats of the "
                         u"established standard:"),
                       _(u"Number of units in which the inter-unit calling "
                         u"sequence protocol complies with the standard:"),
                       _(u"Number of units in which the I/O protocol and "
                         u"format complies with the established standard:"),
                       _(u"Number of units in which the handling of errors "
                         u"complies with the established standard:"),
                       _(u"Number of units in which all references to the "
                         u"unit use the same, unique name:"),
                       _(u"Number of units in which the naming of all data "
                         u"complies with the established standard:"),
                       _(u"Number of units in which is the definition and use "
                         u"of all global variables is in accordance with the "
                         u"established standard:"),
                       _(u"Number of units in which references to the same "
                         u"data use a single, unique name:")]
            (_x_pos,
             _y_pos) = _widg.make_labels(_labels, _fxdcsciqc, 5, 5)
            _x_pos += 45

            _fxdcsciqc.put(self.chkCDRSTQ1, _x_pos, _y_pos[0])
            _fxdcsciqc.put(self.chkCDRSTQ2, _x_pos, _y_pos[1])
            _fxdcsciqc.put(self.txtCDRQCQ1, _x_pos, _y_pos[2])
            _fxdcsciqc.put(self.txtCDRQCQ2, _x_pos, _y_pos[3])
            _fxdcsciqc.put(self.txtCDRQCQ3, _x_pos, _y_pos[4])
            _fxdcsciqc.put(self.txtCDRQCQ4, _x_pos, _y_pos[5])
            _fxdcsciqc.put(self.txtCDRQCQ5, _x_pos, _y_pos[6])
            _fxdcsciqc.put(self.txtCDRQCQ6, _x_pos, _y_pos[7])
            _fxdcsciqc.put(self.txtCDRQCQ7, _x_pos, _y_pos[8])
            _fxdcsciqc.put(self.txtCDRQCQ8, _x_pos, _y_pos[9])
            _fxdcsciqc.put(self.txtCDRQCQ9, _x_pos, _y_pos[10])
            _fxdcsciqc.put(self.txtCDRQCQ10, _x_pos, _y_pos[11])
            _fxdcsciqc.put(self.txtCDRQCQ11, _x_pos, _y_pos[12])
            _fxdcsciqc.put(self.txtCDRQCQ12, _x_pos, _y_pos[13])
            _fxdcsciqc.put(self.txtCDRQCQ13, _x_pos, _y_pos[14])
            _fxdcsciqc.put(self.txtCDRQCQ14, _x_pos, _y_pos[15])
            _fxdcsciqc.put(self.txtCDRQCQ15, _x_pos, _y_pos[16])
            _fxdcsciqc.put(self.txtCDRQCQ16, _x_pos, _y_pos[17])
            _fxdcsciqc.put(self.txtCDRQCQ17, _x_pos, _y_pos[18])
            _fxdcsciqc.put(self.txtCDRQCQ18, _x_pos, _y_pos[19])
            _fxdcsciqc.put(self.txtCDRQCQ19, _x_pos, _y_pos[20])
            _fxdcsciqc.put(self.txtCDRQCQ20, _x_pos, _y_pos[21])
            _fxdcsciqc.put(self.txtCDRQCQ21, _x_pos, _y_pos[22])
            _fxdcsciqc.put(self.txtCDRQCQ22, _x_pos, _y_pos[23])
            _fxdcsciqc.put(self.txtCDRQCQ23, _x_pos, _y_pos[24])
            _fxdcsciqc.put(self.txtCDRQCQ24, _x_pos, _y_pos[25])

            self.chkCDRSTQ1.connect('toggled', self._callback_check, 411)
            self.chkCDRSTQ2.connect('toggled', self._callback_check, 412)
            self.txtCDRQCQ1.connect('focus-out-event', self._callback_entry,
                                    'int', 413)
            self.txtCDRQCQ2.connect('focus-out-event', self._callback_entry,
                                    'int', 414)
            self.txtCDRQCQ3.connect('focus-out-event', self._callback_entry,
                                    'int', 415)
            self.txtCDRQCQ4.connect('focus-out-event', self._callback_entry,
                                    'int', 416)
            self.txtCDRQCQ5.connect('focus-out-event', self._callback_entry,
                                    'int', 417)
            self.txtCDRQCQ6.connect('focus-out-event', self._callback_entry,
                                    'int', 418)
            self.txtCDRQCQ7.connect('focus-out-event', self._callback_entry,
                                    'int', 419)
            self.txtCDRQCQ8.connect('focus-out-event', self._callback_entry,
                                    'int', 420)
            self.txtCDRQCQ9.connect('focus-out-event', self._callback_entry,
                                    'int', 421)
            self.txtCDRQCQ10.connect('focus-out-event', self._callback_entry,
                                     'int', 422)
            self.txtCDRQCQ11.connect('focus-out-event', self._callback_entry,
                                     'int', 423)
            self.txtCDRQCQ12.connect('focus-out-event', self._callback_entry,
                                     'int', 424)
            self.txtCDRQCQ13.connect('focus-out-event', self._callback_entry,
                                     'int', 425)
            self.txtCDRQCQ14.connect('focus-out-event', self._callback_entry,
                                     'int', 426)
            self.txtCDRQCQ15.connect('focus-out-event', self._callback_entry,
                                     'int', 427)
            self.txtCDRQCQ16.connect('focus-out-event', self._callback_entry,
                                     'int', 428)
            self.txtCDRQCQ17.connect('focus-out-event', self._callback_entry,
                                     'int', 429)
            self.txtCDRQCQ18.connect('focus-out-event', self._callback_entry,
                                     'int', 430)
            self.txtCDRQCQ19.connect('focus-out-event', self._callback_entry,
                                     'int', 431)
            self.txtCDRQCQ20.connect('focus-out-event', self._callback_entry,
                                     'int', 432)
            self.txtCDRQCQ21.connect('focus-out-event', self._callback_entry,
                                     'int', 433)
            self.txtCDRQCQ22.connect('focus-out-event', self._callback_entry,
                                     'int', 434)
            self.txtCDRQCQ23.connect('focus-out-event', self._callback_entry,
                                     'int', 435)
            self.txtCDRQCQ24.connect('focus-out-event', self._callback_entry,
                                     'int', 436)

            # Create the quality control risk pane for units.
            _labels = [_(u"The description of this software unit identifies "
                         u"all the requirements that the unit helps satisfy."),
                       _(u"Estimated executable lines of source code in this "
                         u"unit:"),
                       _(u"Estimated executable lines of source code "
                         u"necessary to handle hardware and device interface "
                         u"protocol in this unit:"),
                       _(u"This unit performs processing of hardware and/or "
                         u"device interface protocols."),
                       _(u"Estimated processing time typically spent "
                         u"executing this unit:"),
                       _(u"Estimated processing time typically spent in "
                         u"execution of hardware and device interface "
                         u"protocol in this unit:"),
                       _(u"All inputs, processing, and outputs are clearly "
                         u"and precisely defined."),
                       _(u"Data references identified in this unit:"),
                       _(u"Identified data references that are documented "
                         u"with regard to source, meaning, and format in this "
                         u"unit:"),
                       _(u"Data items that are defined (i.e., documented with "
                         u"regard to source, meaning, and format) in this "
                         u"unit:"),
                       _(u"Data items are referenced in this unit:"),
                       _(u"Data references identified in this unit:"),
                       _(u"Identified data references that are computed or "
                         u"obtained from an external source (e.g., "
                         u"referencing global data with preassigned values, "
                         u"input parameters with preassigned values) in this "
                         u"unit:"),
                       _(u"All conditions and alternative processing options "
                         u"for each decision point are defined."),
                       _(u"All parameters in the argument list are used."),
                       _(u"Number of software discrepancy reports recorded, "
                         u"to date, for this unit:"),
                       _(u"Number of software discrepancy reports recorded "
                         u"that have been closed, to date, for this unit:"),
                       _(u"All design representations are in the formats of "
                         u"the established standard."),
                       _(u"The calling sequence protocol (between units) "
                         u"complies with the established standard."),
                       _(u"The I/O protocol and format complies with the "
                         u"established standard."),
                       _(u"The handling of errors complies with the "
                         u"established standard."),
                       _(u"All references to the unit use the same, unique "
                         u"name."),
                       _(u"The naming of all data complies with the "
                         u"established standard."),
                       _(u"The definition and use of all global variables is "
                         u"in accordance with the established standard."),
                       _(u"References to the same data use a single, unique "
                         u"name.")]
            (_x_pos,
             _y_pos) = _widg.make_labels(_labels, _fxdunitqc, 5, 5)
            _x_pos += 45

            _fxdunitqc.put(self.chkCDRUnitSTQ1, _x_pos, _y_pos[0])
            _fxdunitqc.put(self.txtCDRUnitQCQ1, _x_pos, _y_pos[1])
            _fxdunitqc.put(self.txtCDRUnitQCQ2, _x_pos, _y_pos[2])
            _fxdunitqc.put(self.chkCDRUnitQCQ3, _x_pos, _y_pos[3])
            _fxdunitqc.put(self.txtCDRUnitQCQ4, _x_pos, _y_pos[4])
            _fxdunitqc.put(self.txtCDRUnitQCQ5, _x_pos, _y_pos[5])
            _fxdunitqc.put(self.chkCDRUnitQCQ6, _x_pos, _y_pos[6])
            _fxdunitqc.put(self.txtCDRUnitQCQ7, _x_pos, _y_pos[7])
            _fxdunitqc.put(self.txtCDRUnitQCQ8, _x_pos, _y_pos[8])
            _fxdunitqc.put(self.txtCDRUnitQCQ9, _x_pos, _y_pos[9])
            _fxdunitqc.put(self.txtCDRUnitQCQ10, _x_pos, _y_pos[10])
            _fxdunitqc.put(self.txtCDRUnitQCQ11, _x_pos, _y_pos[11])
            _fxdunitqc.put(self.txtCDRUnitQCQ12, _x_pos, _y_pos[12])
            _fxdunitqc.put(self.chkCDRUnitQCQ13, _x_pos, _y_pos[13])
            _fxdunitqc.put(self.chkCDRUnitQCQ14, _x_pos, _y_pos[14])
            _fxdunitqc.put(self.txtCDRUnitQCQ15, _x_pos, _y_pos[15])
            _fxdunitqc.put(self.txtCDRUnitQCQ16, _x_pos, _y_pos[16])
            _fxdunitqc.put(self.chkCDRUnitQCQ17, _x_pos, _y_pos[17])
            _fxdunitqc.put(self.chkCDRUnitQCQ18, _x_pos, _y_pos[18])
            _fxdunitqc.put(self.chkCDRUnitQCQ19, _x_pos, _y_pos[19])
            _fxdunitqc.put(self.chkCDRUnitQCQ20, _x_pos, _y_pos[20])
            _fxdunitqc.put(self.chkCDRUnitQCQ21, _x_pos, _y_pos[21])
            _fxdunitqc.put(self.chkCDRUnitQCQ22, _x_pos, _y_pos[22])
            _fxdunitqc.put(self.chkCDRUnitQCQ23, _x_pos, _y_pos[23])
            _fxdunitqc.put(self.chkCDRUnitQCQ24, _x_pos, _y_pos[24])

            self.chkCDRUnitSTQ1.connect('toggled', self._callback_check, 447)
            self.txtCDRUnitQCQ1.connect('focus-out-event',
                                        self._callback_entry, 'int', 448)
            self.txtCDRUnitQCQ2.connect('focus-out-event',
                                        self._callback_entry, 'int', 449)
            self.chkCDRUnitQCQ3.connect('toggled', self._callback_check, 450)
            self.txtCDRUnitQCQ4.connect('focus-out-event',
                                        self._callback_entry, 'int', 451)
            self.txtCDRUnitQCQ5.connect('focus-out-event',
                                        self._callback_entry, 'int', 452)
            self.chkCDRUnitQCQ6.connect('toggled', self._callback_check, 453)
            self.txtCDRUnitQCQ7.connect('focus-out-event',
                                        self._callback_entry, 'int', 454)
            self.txtCDRUnitQCQ8.connect('focus-out-event',
                                        self._callback_entry, 'int', 455)
            self.txtCDRUnitQCQ9.connect('focus-out-event',
                                        self._callback_entry, 'int', 456)
            self.txtCDRUnitQCQ10.connect('focus-out-event',
                                         self._callback_entry, 'int', 457)
            self.txtCDRUnitQCQ11.connect('focus-out-event',
                                         self._callback_entry, 'int', 458)
            self.txtCDRUnitQCQ12.connect('focus-out-event',
                                         self._callback_entry, 'int', 459)
            self.chkCDRUnitQCQ13.connect('toggled', self._callback_check, 460)
            self.chkCDRUnitQCQ14.connect('toggled', self._callback_check, 461)
            self.txtCDRUnitQCQ15.connect('focus-out-event',
                                         self._callback_entry, 'int', 462)
            self.txtCDRUnitQCQ16.connect('focus-out-event',
                                         self._callback_entry, 'int', 463)
            self.chkCDRUnitQCQ17.connect('toggled', self._callback_check, 464)
            self.chkCDRUnitQCQ18.connect('toggled', self._callback_check, 465)
            self.chkCDRUnitQCQ19.connect('toggled', self._callback_check, 466)
            self.chkCDRUnitQCQ20.connect('toggled', self._callback_check, 467)
            self.chkCDRUnitQCQ21.connect('toggled', self._callback_check, 468)
            self.chkCDRUnitQCQ22.connect('toggled', self._callback_check, 469)
            self.chkCDRUnitQCQ23.connect('toggled', self._callback_check, 470)
            self.chkCDRUnitQCQ24.connect('toggled', self._callback_check, 471)

            self.lblCDR.set_markup("<span weight='bold'>" +
                                   _(u"Critical\nDesign\nReview") +
                                   "</span>")
            self.lblCDR.set_alignment(xalign=0.5, yalign=0.5)
            self.lblCDR.set_justify(gtk.JUSTIFY_CENTER)
            self.lblCDR.set_angle(90)
            self.lblCDR.show_all()
            self.lblCDR.set_tooltip_text(_(u"Allows assessment of the "
                                           u"reliability risk at the critical "
                                           u"design review."))
            self.nbkRiskAnalysis.insert_page(self.hpnCDR,
                                             tab_label=self.lblCDR,
                                             position=-1)

            return False

        def _create_trr_page(self):
            """
            Function to create the risk analysis page to be completed at the
            test readiness review phase and add it to the risk analysis
            gtk.Notebook().
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build the module-level containers and set them as the default
            # to display.
            _fxdcscilt = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdcscilt)

            self.fraTRRCSCILT.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraTRRCSCILT.add(_scrollwindow)

            self.hpnTRR.pack1(self.fraTRRCSCILT, resize=True, shrink=True)

            # Build the unit-level containers.
            _fxdunitlt = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdunitlt)

            self.fraTRRUnitLT.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraTRRUnitLT.add(_scrollwindow)

            _fxdunitqc = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fxdunitqc)

            self.fraTRRUnitQC.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            self.fraTRRUnitQC.add(_scrollwindow)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display risk analysis information.  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the language type, modularity, and complexity risk pane
            # for CSCI.
            _labels = [_(u"Number of units in this module:"),
                       _(u"Total executable lines of source code in this "
                         u"module:"),
                       _(u"Total assembly language lines of code in this "
                         u"module:"),
                       _(u"Total higher order language lines of code in this "
                         u"module:")]
            (_x_pos,
             _y_pos) = _widg.make_labels(_labels, _fxdcscilt, 5, 5)
            _x_pos += 45

            _fxdcscilt.put(self.txtTRRLTCMQ1, _x_pos, _y_pos[0])
            _fxdcscilt.put(self.txtTRRLTCMQ2, _x_pos, _y_pos[1])
            _fxdcscilt.put(self.txtTRRLTCMQ3, _x_pos, _y_pos[2])
            _fxdcscilt.put(self.txtTRRLTCMQ4, _x_pos, _y_pos[3])

            self.txtTRRLTCMQ1.connect('focus-out-event', self._callback_entry,
                                      'int', 500)
            self.txtTRRLTCMQ2.connect('focus-out-event', self._callback_entry,
                                      'int', 501)
            self.txtTRRLTCMQ3.connect('focus-out-event', self._callback_entry,
                                      'int', 502)
            self.txtTRRLTCMQ4.connect('focus-out-event', self._callback_entry,
                                      'int', 503)

            # Create the language type, modularity, and complexity risk pane
            # for the unit.
            _labels = [_(u"Total executable lines of source code in this "
                         u"unit:"),
                       _(u"Total assembly language lines of code in this "
                         u"unit:"),
                       _(u"Total higher order language lines of code in this "
                         u"unit:")]
            (_x_pos,
             _y_pos) = _widg.make_labels(_labels, _fxdunitlt, 5, 5)
            _x_pos += 45

            _fxdunitlt.put(self.txtTRRUnitLTCMQ1, _x_pos, _y_pos[0])
            _fxdunitlt.put(self.txtTRRUnitLTCMQ2, _x_pos, _y_pos[1])
            _fxdunitlt.put(self.txtTRRUnitLTCMQ3, _x_pos, _y_pos[2])

            self.txtTRRUnitLTCMQ1.connect('focus-out-event',
                                          self._callback_entry, 'int', 504)
            self.txtTRRUnitLTCMQ2.connect('focus-out-event',
                                          self._callback_entry, 'int', 505)
            self.txtTRRUnitLTCMQ3.connect('focus-out-event',
                                          self._callback_entry, 'int', 506)

            # Create the quality control and anomaly management risk pane for
            # the unit.
            _labels = [_(u"When an error condition is detected in this unit, "
                         u"resolution of the error is determined by this "
                         u"unit."),
                       _(u"A check is performed before processing begins to "
                         u"determine that all data is available."),
                       _(u"All inputs, processing, and outputs are clearly "
                         u"and precisely defined for this unit."),
                       _(u"All data references in this unit are defined."),
                       _(u"All data references in this unit are identified."),
                       _(u"All conditions and alternative processing options "
                         u"in this unit are defined for each decision point."),
                       _(u"All parameters in the argument list for this unit "
                         u"are used."),
                       _(u"All design representations in this unit are in the "
                         u"formats of the established standard."),
                       _(u"The between unit calling sequence protocol in this "
                         u"unit complies with the established standard."),
                       _(u"The I/O protocol and format in this unit complies "
                         u"with the established standard."),
                       _(u"The handling of errors in this unit complies with "
                         u"the established standard."),
                       _(u"All references to this unit use the same, unique "
                         u"name."),
                       _(u"All data representation in this unit complies with "
                         u"the established standard."),
                       _(u"The naming of all data in this unit complies with "
                         u"the established standard."),
                       _(u"The definition and use of all global variables in "
                         u"this unit is in accordance with the established "
                         u"standard."),
                       _(u"All references to the same data in this unit use a "
                         u"single, unique name.")]
            (_x_pos,
             _y_pos) = _widg.make_labels(_labels, _fxdunitqc, 5, 5)
            _x_pos += 45

            _fxdunitqc.put(self.chkTRRUnitAMQ1, _x_pos, _y_pos[0])
            _fxdunitqc.put(self.chkTRRUnitAMQ2, _x_pos, _y_pos[1])
            _fxdunitqc.put(self.chkTRRUnitQCQ1, _x_pos, _y_pos[2])
            _fxdunitqc.put(self.chkTRRUnitQCQ2, _x_pos, _y_pos[3])
            _fxdunitqc.put(self.chkTRRUnitQCQ3, _x_pos, _y_pos[4])
            _fxdunitqc.put(self.chkTRRUnitQCQ4, _x_pos, _y_pos[5])
            _fxdunitqc.put(self.chkTRRUnitQCQ5, _x_pos, _y_pos[6])
            _fxdunitqc.put(self.chkTRRUnitQCQ6, _x_pos, _y_pos[7])
            _fxdunitqc.put(self.chkTRRUnitQCQ7, _x_pos, _y_pos[8])
            _fxdunitqc.put(self.chkTRRUnitQCQ8, _x_pos, _y_pos[9])
            _fxdunitqc.put(self.chkTRRUnitQCQ9, _x_pos, _y_pos[10])
            _fxdunitqc.put(self.chkTRRUnitQCQ10, _x_pos, _y_pos[11])
            _fxdunitqc.put(self.chkTRRUnitQCQ11, _x_pos, _y_pos[12])
            _fxdunitqc.put(self.chkTRRUnitQCQ12, _x_pos, _y_pos[13])
            _fxdunitqc.put(self.chkTRRUnitQCQ13, _x_pos, _y_pos[14])
            _fxdunitqc.put(self.chkTRRUnitQCQ14, _x_pos, _y_pos[15])

            self.chkTRRUnitAMQ1.connect('toggled', self._callback_check, 507)
            self.chkTRRUnitAMQ2.connect('toggled', self._callback_check, 508)
            self.chkTRRUnitQCQ1.connect('toggled', self._callback_check, 509)
            self.chkTRRUnitQCQ2.connect('toggled', self._callback_check, 510)
            self.chkTRRUnitQCQ3.connect('toggled', self._callback_check, 511)
            self.chkTRRUnitQCQ4.connect('toggled', self._callback_check, 512)
            self.chkTRRUnitQCQ5.connect('toggled', self._callback_check, 513)
            self.chkTRRUnitQCQ6.connect('toggled', self._callback_check, 514)
            self.chkTRRUnitQCQ7.connect('toggled', self._callback_check, 515)
            self.chkTRRUnitQCQ8.connect('toggled', self._callback_check, 516)
            self.chkTRRUnitQCQ9.connect('toggled', self._callback_check, 517)
            self.chkTRRUnitQCQ10.connect('toggled', self._callback_check, 518)
            self.chkTRRUnitQCQ11.connect('toggled', self._callback_check, 519)
            self.chkTRRUnitQCQ12.connect('toggled', self._callback_check, 520)
            self.chkTRRUnitQCQ13.connect('toggled', self._callback_check, 521)
            self.chkTRRUnitQCQ14.connect('toggled', self._callback_check, 522)

            self.lblTRR.set_markup("<span weight='bold'>" +
                                   _(u"Test\nReadiness\nReview") +
                                   "</span>")
            self.lblTRR.set_alignment(xalign=0.5, yalign=0.5)
            self.lblTRR.set_justify(gtk.JUSTIFY_CENTER)
            self.lblTRR.set_angle(90)
            self.lblTRR.show_all()
            self.lblTRR.set_tooltip_text(_(u"Allows assessment of the "
                                           u"reliability risk at the test "
                                           u"readiness review."))
            self.nbkRiskAnalysis.insert_page(self.hpnTRR,
                                             tab_label=self.lblTRR,
                                             position=-1)

            return False

        self.nbkRiskAnalysis.set_tab_pos(gtk.POS_RIGHT)

        _create_development_environment_page(self)
        _create_srr_page(self)
        _create_pdr_page(self)
        _create_cdr_page(self)
        _create_trr_page(self)

        self.nbkRiskAnalysis.connect('switch_page',
                                     self._notebook_page_switched, 1)

        return False

    def load_tree(self):
        """
        Method to load the Software clas gtk.TreeModel() with system
        information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _query = "SELECT * FROM tbl_software " \
                 "WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        try:
            _n_assemblies = len(_results)
        except TypeError:
            return True

        _model = self.treeview.get_model()
        _model.clear()
        for i in range(_n_assemblies):
            _values = [_results[i][0]]
            self._dicSoftware[_results[i][1]] = \
                _util.tuple_to_list(_results[i][2:], _values)
            if _results[i][34] == '-':      # It's the top level element.
                _piter = None
            elif _results[i][34] != '-':    # It's a child element.
                _piter = _model.get_iter_from_string(_results[i][34])

            _model.append(_piter, _results[i])

        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            _col = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _col)

        self.treeview.set_cursor('0', None, False)
        self.treeview.expand_all()

        return False

    def load_notebook(self):
        """
        Method to load the Software class gtk.Notebook().

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _load_general_data_page(self):
            """
            Function to load the gtk.Widgets() with general information about
            the Software class.
            """

            (_model, _row) = self.treeview.get_selection().get_selected()

            if _row is not None:
                self.cmbLevel.set_active(int(self.level_id))
                _buffer = self.txtDescription.get_child().get_child().get_buffer()  # noqa
                try:
                    _buffer.set_text(self.description)
                except TypeError:
                    _buffer.set_text("")
                self.cmbApplication.set_active(int(self.application_id))
                # self.cmbDevelopment.set_active(int(self.development_id))
                self.cmbPhase.set_active(int(self.phase_id))

                self.cmbTCL.set_active(int(self.tcl))
                self.cmbTestPath.set_active(int(self.test_path))

            return False

        def _load_risk_analysis_page(self):
            """
            Function to load the widgets on the Risk Analysis gtk.Notebook()
            page.

            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _error = False

            (_model, _row) = self.treeview.get_selection().get_selected()
            _software_id = _model.get_value(_row, 1)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the risk analysis dictionaries.                            #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Retrieve the development environment risk answers.
            _query = "SELECT * FROM tbl_software_development \
                      ORDER BY fld_software_id, fld_question_id"
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx)
            try:
                _n_development = len(_results)
            except TypeError:
                _n_development = 0
                _error = True

            # Populate the development environment risk dictionary.
            for i in xrange(1, _n_development, 43):
                _list = [y[2] for y in _results if y[0] == _results[i][0]]
                self._dic_dev_env[_results[i][0]] = _list

            # Retrieve the requirements review risk answers.
            _query = "SELECT * FROM tbl_srr_ssr \
                      ORDER BY fld_software_id, fld_question_id"
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx)
            try:
                _n_requirements = len(_results)
            except TypeError:
                _n_requirements = 0
                _error = True

            # Populate the requirements review risk dictionary.  If the input
            # is a numerical input, assign the value of the third response
            # field returned from the database.
            for i in xrange(0, _n_requirements, 50):
                _list = [y[2] for y in _results if y[0] == _results[i][0]]
                for j in [0, 1, 2, 3, 5, 6, 25, 26, 31, 32, 33, 34]:
                    _list[j] = _results[i+j][3]
                self._dic_srr[_results[i][0]] = _list

            # Retrieve the preliminary design review risk answers.
            _query = "SELECT * FROM tbl_pdr \
                      ORDER BY fld_software_id, fld_question_id"
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx)
            try:
                _n_pdr = len(_results)
            except TypeError:
                _n_pdr = 0
                _error = True

            # Populate the preliminary design review risk dictionary.  If the
            # input is a numerical input, assign the value of the third
            # response field returned from the database.
            for i in xrange(0, _n_pdr, 39):
                _list = [y[2] for y in _results if y[0] == _results[i][0]]
                for j in [17, 18, 21, 22, 23, 24, 25, 26, 29, 30]:
                    _list[j] = _results[i+j][3]
                self._dic_pdr[_results[i][0]] = _list

            # Retrieve the critical design review risk answers.
            _query = "SELECT * FROM tbl_cdr \
                      ORDER BY fld_software_id, fld_question_id"
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx)
            try:
                _n_cdr = len(_results)
            except TypeError:
                _n_cdr = 0
                _error = True

            # Populate the critical design review risk dictionary.  If the
            # input is a Yes/No input, assign the value of the second response
            # field returned from the database.
            for i in xrange(0, _n_cdr, 72):
                _list = [y[3] for y in _results if y[0] == _results[i][0]]
                for j in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 37, 38, 39, 40, 41,
                          42, 43, 44, 45, 46, 47, 50, 53, 60, 61, 64, 65, 66,
                          67, 68, 69, 70, 71]:
                    _list[j] = _results[i+j][2]
                self._dic_cdr[_results[i][0]] = _list

            # Retrieve the test readiness review risk answers.
            _query = "SELECT * FROM tbl_trr \
                      ORDER BY fld_software_id, fld_question_id"
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx)
            try:
                _n_trr = len(_results)
            except TypeError:
                _n_trr = 0
                _error = True

            # Populate the test readiness review risk dictionary.  If the input
            # is a numerical input, assign the value of the third response
            # field returned from the database.
            for i in range(0, _n_trr, 24):
                _list = [y[2] for y in _results if y[0] == _results[i][0]]
                for j in [0, 1, 2, 3, 4, 5, 6]:
                    _list[j] = _results[i+j][3]
                    self._dic_trr[_results[i][0]] = _list

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the risk analysis widgets.                                 #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            self.chkDevEnvQ1.set_active(self._dic_dev_env[_software_id][0])
            self.chkDevEnvQ2.set_active(self._dic_dev_env[_software_id][1])
            self.chkDevEnvQ3.set_active(self._dic_dev_env[_software_id][2])
            self.chkDevEnvQ4.set_active(self._dic_dev_env[_software_id][3])
            self.chkDevEnvQ5.set_active(self._dic_dev_env[_software_id][4])
            self.chkDevEnvQ6.set_active(self._dic_dev_env[_software_id][5])
            self.chkDevEnvQ7.set_active(self._dic_dev_env[_software_id][6])
            self.chkDevEnvQ8.set_active(self._dic_dev_env[_software_id][7])
            self.chkDevEnvQ9.set_active(self._dic_dev_env[_software_id][8])
            self.chkDevEnvQ10.set_active(self._dic_dev_env[_software_id][9])
            self.chkDevEnvQ11.set_active(self._dic_dev_env[_software_id][10])
            self.chkDevEnvQ12.set_active(self._dic_dev_env[_software_id][11])
            self.chkDevEnvQ13.set_active(self._dic_dev_env[_software_id][12])
            self.chkDevEnvQ14.set_active(self._dic_dev_env[_software_id][13])
            self.chkDevEnvQ15.set_active(self._dic_dev_env[_software_id][14])
            self.chkDevEnvQ16.set_active(self._dic_dev_env[_software_id][15])
            self.chkDevEnvQ17.set_active(self._dic_dev_env[_software_id][16])
            self.chkDevEnvQ18.set_active(self._dic_dev_env[_software_id][17])
            self.chkDevEnvQ19.set_active(self._dic_dev_env[_software_id][18])
            self.chkDevEnvQ20.set_active(self._dic_dev_env[_software_id][19])
            self.chkDevEnvQ21.set_active(self._dic_dev_env[_software_id][20])
            self.chkDevEnvQ22.set_active(self._dic_dev_env[_software_id][21])
            self.chkDevEnvQ23.set_active(self._dic_dev_env[_software_id][22])
            self.chkDevEnvQ24.set_active(self._dic_dev_env[_software_id][23])
            self.chkDevEnvQ25.set_active(self._dic_dev_env[_software_id][24])
            self.chkDevEnvQ26.set_active(self._dic_dev_env[_software_id][25])
            self.chkDevEnvQ27.set_active(self._dic_dev_env[_software_id][26])
            self.chkDevEnvQ28.set_active(self._dic_dev_env[_software_id][27])
            self.chkDevEnvQ29.set_active(self._dic_dev_env[_software_id][28])
            self.chkDevEnvQ30.set_active(self._dic_dev_env[_software_id][29])
            self.chkDevEnvQ31.set_active(self._dic_dev_env[_software_id][30])
            self.chkDevEnvQ32.set_active(self._dic_dev_env[_software_id][31])
            self.chkDevEnvQ33.set_active(self._dic_dev_env[_software_id][32])
            self.chkDevEnvQ34.set_active(self._dic_dev_env[_software_id][33])
            self.chkDevEnvQ35.set_active(self._dic_dev_env[_software_id][34])
            self.chkDevEnvQ36.set_active(self._dic_dev_env[_software_id][35])
            self.chkDevEnvQ37.set_active(self._dic_dev_env[_software_id][36])
            self.chkDevEnvQ38.set_active(self._dic_dev_env[_software_id][37])
            self.chkDevEnvQ39.set_active(self._dic_dev_env[_software_id][38])
            self.chkDevEnvQ40.set_active(self._dic_dev_env[_software_id][39])
            self.chkDevEnvQ41.set_active(self._dic_dev_env[_software_id][40])
            self.chkDevEnvQ42.set_active(self._dic_dev_env[_software_id][41])
            self.chkDevEnvQ43.set_active(self._dic_dev_env[_software_id][42])

            self.txtSRRAMQ1.set_text(str(self._dic_srr[_software_id][0]))
            self.txtSRRAMQ2.set_text(str(self._dic_srr[_software_id][1]))
            self.txtSRRAMQ3.set_text(str(self._dic_srr[_software_id][2]))
            self.txtSRRAMQ4.set_text(str(self._dic_srr[_software_id][3]))
            self.chkSRRAMQ5.set_active(self._dic_srr[_software_id][4])
            self.txtSRRAMQ6.set_text(str(self._dic_srr[_software_id][5]))
            self.txtSRRAMQ7.set_text(str(self._dic_srr[_software_id][6]))
            self.chkSRRAMQ8.set_active(self._dic_srr[_software_id][7])
            self.chkSRRAMQ9.set_active(self._dic_srr[_software_id][8])
            self.chkSRRAMQ10.set_active(self._dic_srr[_software_id][9])
            self.chkSRRAMQ11.set_active(self._dic_srr[_software_id][10])
            self.chkSRRAMQ12.set_active(self._dic_srr[_software_id][11])
            self.chkSRRAMQ13.set_active(self._dic_srr[_software_id][12])
            self.chkSRRAMQ14.set_active(self._dic_srr[_software_id][13])
            self.chkSRRAMQ15.set_active(self._dic_srr[_software_id][14])
            self.chkSRRAMQ16.set_active(self._dic_srr[_software_id][15])
            self.chkSRRAMQ17.set_active(self._dic_srr[_software_id][16])
            self.chkSRRAMQ18.set_active(self._dic_srr[_software_id][17])
            self.chkSRRAMQ19.set_active(self._dic_srr[_software_id][18])
            self.chkSRRAMQ20.set_active(self._dic_srr[_software_id][19])
            self.chkSRRAMQ21.set_active(self._dic_srr[_software_id][20])
            self.chkSRRAMQ22.set_active(self._dic_srr[_software_id][21])
            self.chkSRRSTQ1.set_active(self._dic_srr[_software_id][22])
            self.chkSRRQCQ1.set_active(self._dic_srr[_software_id][23])
            self.chkSRRQCQ2.set_active(self._dic_srr[_software_id][24])
            self.chkSRRQCQ3.set_active(self._dic_srr[_software_id][25])
            self.chkSRRQCQ4.set_active(self._dic_srr[_software_id][26])
            self.chkSRRQCQ5.set_active(self._dic_srr[_software_id][27])
            self.chkSRRQCQ6.set_active(self._dic_srr[_software_id][28])
            self.chkSRRQCQ7.set_active(self._dic_srr[_software_id][29])
            self.chkSRRQCQ8.set_active(self._dic_srr[_software_id][30])
            self.txtSRRQCQ9.set_text(str(self._dic_srr[_software_id][31]))
            self.txtSRRQCQ10.set_text(str(self._dic_srr[_software_id][32]))
            self.txtSRRQCQ11.set_text(str(self._dic_srr[_software_id][33]))
            self.txtSRRQCQ12.set_text(str(self._dic_srr[_software_id][34]))
            self.chkSRRQCQ13.set_active(self._dic_srr[_software_id][35])
            self.chkSRRQCQ14.set_active(self._dic_srr[_software_id][36])
            self.chkSRRQCQ15.set_active(self._dic_srr[_software_id][37])
            self.chkSRRQCQ16.set_active(self._dic_srr[_software_id][38])
            self.chkSRRQCQ17.set_active(self._dic_srr[_software_id][39])
            self.chkSRRQCQ18.set_active(self._dic_srr[_software_id][40])
            self.chkSRRQCQ19.set_active(self._dic_srr[_software_id][41])
            self.chkSRRQCQ20.set_active(self._dic_srr[_software_id][42])
            self.chkSRRQCQ21.set_active(self._dic_srr[_software_id][43])
            self.chkSRRQCQ22.set_active(self._dic_srr[_software_id][44])
            self.chkSRRQCQ23.set_active(self._dic_srr[_software_id][45])
            self.chkSRRQCQ24.set_active(self._dic_srr[_software_id][46])
            self.chkSRRQCQ25.set_active(self._dic_srr[_software_id][47])
            self.chkSRRQCQ26.set_active(self._dic_srr[_software_id][48])
            self.chkSRRQCQ27.set_active(self._dic_srr[_software_id][49])

            self.chkPDRAMQ1.set_active(self._dic_pdr[_software_id][0])
            self.chkPDRAMQ2.set_active(self._dic_pdr[_software_id][1])
            self.chkPDRAMQ3.set_active(self._dic_pdr[_software_id][2])
            self.chkPDRAMQ4.set_active(self._dic_pdr[_software_id][3])
            self.chkPDRAMQ5.set_active(self._dic_pdr[_software_id][4])
            self.chkPDRAMQ6.set_active(self._dic_pdr[_software_id][5])
            self.chkPDRAMQ7.set_active(self._dic_pdr[_software_id][6])
            self.chkPDRAMQ8.set_active(self._dic_pdr[_software_id][7])
            self.chkPDRAMQ9.set_active(self._dic_pdr[_software_id][8])
            self.chkPDRAMQ10.set_active(self._dic_pdr[_software_id][9])
            self.chkPDRAMQ11.set_active(self._dic_pdr[_software_id][10])
            self.chkPDRAMQ12.set_active(self._dic_pdr[_software_id][11])
            self.chkPDRAMQ13.set_active(self._dic_pdr[_software_id][12])
            self.chkPDRAMQ14.set_active(self._dic_pdr[_software_id][13])
            self.chkPDRSTQ1.set_active(self._dic_pdr[_software_id][14])
            self.chkPDRQCQ1.set_active(self._dic_pdr[_software_id][15])
            self.chkPDRQCQ2.set_active(self._dic_pdr[_software_id][16])
            self.txtPDRQCQ3.set_text(str(self._dic_pdr[_software_id][17]))
            self.txtPDRQCQ4.set_text(str(self._dic_pdr[_software_id][18]))
            self.chkPDRQCQ5.set_active(self._dic_pdr[_software_id][19])
            self.chkPDRQCQ6.set_active(self._dic_pdr[_software_id][20])
            self.txtPDRQCQ7.set_text(str(self._dic_pdr[_software_id][21]))
            self.txtPDRQCQ8.set_text(str(self._dic_pdr[_software_id][22]))
            self.txtPDRQCQ9.set_text(str(self._dic_pdr[_software_id][23]))
            self.txtPDRQCQ10.set_text(str(self._dic_pdr[_software_id][24]))
            self.txtPDRQCQ11.set_text(str(self._dic_pdr[_software_id][25]))
            self.txtPDRQCQ12.set_text(str(self._dic_pdr[_software_id][26]))
            self.chkPDRQCQ13.set_active(self._dic_pdr[_software_id][27])
            self.chkPDRQCQ14.set_active(self._dic_pdr[_software_id][28])
            self.txtPDRQCQ15.set_text(str(self._dic_pdr[_software_id][29]))
            self.txtPDRQCQ16.set_text(str(self._dic_pdr[_software_id][30]))
            self.chkPDRQCQ17.set_active(self._dic_pdr[_software_id][31])
            self.chkPDRQCQ18.set_active(self._dic_pdr[_software_id][32])
            self.chkPDRQCQ19.set_active(self._dic_pdr[_software_id][33])
            self.chkPDRQCQ20.set_active(self._dic_pdr[_software_id][34])
            self.chkPDRQCQ21.set_active(self._dic_pdr[_software_id][35])
            self.chkPDRQCQ22.set_active(self._dic_pdr[_software_id][36])
            self.chkPDRQCQ23.set_active(self._dic_pdr[_software_id][37])
            self.chkPDRQCQ24.set_active(self._dic_pdr[_software_id][38])

            self.txtCDRAMQ1.set_text(str(self._dic_cdr[_software_id][0]))
            self.txtCDRAMQ2.set_text(str(self._dic_cdr[_software_id][1]))
            self.chkCDRAMQ3.set_active(self._dic_cdr[_software_id][2])
            self.chkCDRAMQ4.set_active(self._dic_cdr[_software_id][3])
            self.chkCDRAMQ5.set_active(self._dic_cdr[_software_id][4])
            self.chkCDRAMQ6.set_active(self._dic_cdr[_software_id][5])
            self.chkCDRAMQ7.set_active(self._dic_cdr[_software_id][6])
            self.txtCDRAMQ8.set_text(str(self._dic_cdr[_software_id][7]))
            self.chkCDRAMQ9.set_active(self._dic_cdr[_software_id][8])
            self.chkCDRAMQ10.set_active(self._dic_cdr[_software_id][9])
            self.chkCDRAMQ11.set_active(self._dic_cdr[_software_id][10])
            self.chkCDRSTQ1.set_active(self._dic_cdr[_software_id][11])
            self.chkCDRSTQ2.set_active(self._dic_cdr[_software_id][12])
            self.txtCDRQCQ1.set_text(str(self._dic_cdr[_software_id][13]))
            self.txtCDRQCQ2.set_text(str(self._dic_cdr[_software_id][14]))
            self.txtCDRQCQ3.set_text(str(self._dic_cdr[_software_id][15]))
            self.txtCDRQCQ4.set_text(str(self._dic_cdr[_software_id][16]))
            self.txtCDRQCQ5.set_text(str(self._dic_cdr[_software_id][17]))
            self.txtCDRQCQ6.set_text(str(self._dic_cdr[_software_id][18]))
            self.txtCDRQCQ7.set_text(str(self._dic_cdr[_software_id][19]))
            self.txtCDRQCQ8.set_text(str(self._dic_cdr[_software_id][20]))
            self.txtCDRQCQ9.set_text(str(self._dic_cdr[_software_id][21]))
            self.txtCDRQCQ10.set_text(str(self._dic_cdr[_software_id][22]))
            self.txtCDRQCQ11.set_text(str(self._dic_cdr[_software_id][23]))
            self.txtCDRQCQ12.set_text(str(self._dic_cdr[_software_id][24]))
            self.txtCDRQCQ13.set_text(str(self._dic_cdr[_software_id][25]))
            self.txtCDRQCQ14.set_text(str(self._dic_cdr[_software_id][26]))
            self.txtCDRQCQ15.set_text(str(self._dic_cdr[_software_id][27]))
            self.txtCDRQCQ16.set_text(str(self._dic_cdr[_software_id][28]))
            self.txtCDRQCQ17.set_text(str(self._dic_cdr[_software_id][29]))
            self.txtCDRQCQ18.set_text(str(self._dic_cdr[_software_id][30]))
            self.txtCDRQCQ19.set_text(str(self._dic_cdr[_software_id][31]))
            self.txtCDRQCQ20.set_text(str(self._dic_cdr[_software_id][32]))
            self.txtCDRQCQ21.set_text(str(self._dic_cdr[_software_id][33]))
            self.txtCDRQCQ22.set_text(str(self._dic_cdr[_software_id][34]))
            self.txtCDRQCQ23.set_text(str(self._dic_cdr[_software_id][35]))
            self.txtCDRQCQ24.set_text(str(self._dic_cdr[_software_id][36]))
            self.chkCDRUnitAMQ1.set_active(self._dic_cdr[_software_id][37])
            self.chkCDRUnitAMQ2.set_active(self._dic_cdr[_software_id][38])
            self.chkCDRUnitAMQ3.set_active(self._dic_cdr[_software_id][39])
            self.chkCDRUnitAMQ4.set_active(self._dic_cdr[_software_id][40])
            self.chkCDRUnitAMQ5.set_active(self._dic_cdr[_software_id][41])
            self.chkCDRUnitAMQ6.set_active(self._dic_cdr[_software_id][42])
            self.chkCDRUnitAMQ7.set_active(self._dic_cdr[_software_id][43])
            self.chkCDRUnitAMQ8.set_active(self._dic_cdr[_software_id][44])
            self.chkCDRUnitAMQ9.set_active(self._dic_cdr[_software_id][45])
            self.chkCDRUnitAMQ10.set_active(self._dic_cdr[_software_id][46])
            self.chkCDRUnitSTQ1.set_active(self._dic_cdr[_software_id][47])
            self.txtCDRUnitQCQ1.set_text(str(self._dic_cdr[_software_id][48]))
            self.txtCDRUnitQCQ2.set_text(str(self._dic_cdr[_software_id][49]))
            self.chkCDRUnitQCQ3.set_active(self._dic_cdr[_software_id][50])
            self.txtCDRUnitQCQ4.set_text(str(self._dic_cdr[_software_id][51]))
            self.txtCDRUnitQCQ5.set_text(str(self._dic_cdr[_software_id][52]))
            self.chkCDRUnitQCQ6.set_active(self._dic_cdr[_software_id][53])
            self.txtCDRUnitQCQ7.set_text(str(self._dic_cdr[_software_id][54]))
            self.txtCDRUnitQCQ8.set_text(str(self._dic_cdr[_software_id][55]))
            self.txtCDRUnitQCQ9.set_text(str(self._dic_cdr[_software_id][56]))
            self.txtCDRUnitQCQ10.set_text(str(self._dic_cdr[_software_id][57]))
            self.txtCDRUnitQCQ11.set_text(str(self._dic_cdr[_software_id][58]))
            self.txtCDRUnitQCQ12.set_text(str(self._dic_cdr[_software_id][59]))
            self.chkCDRUnitQCQ13.set_active(self._dic_cdr[_software_id][60])
            self.chkCDRUnitQCQ14.set_active(self._dic_cdr[_software_id][61])
            self.txtCDRUnitQCQ15.set_text(str(self._dic_cdr[_software_id][62]))
            self.txtCDRUnitQCQ16.set_text(str(self._dic_cdr[_software_id][63]))
            self.chkCDRUnitQCQ17.set_active(self._dic_cdr[_software_id][64])
            self.chkCDRUnitQCQ18.set_active(self._dic_cdr[_software_id][65])
            self.chkCDRUnitQCQ19.set_active(self._dic_cdr[_software_id][66])
            self.chkCDRUnitQCQ20.set_active(self._dic_cdr[_software_id][67])
            self.chkCDRUnitQCQ21.set_active(self._dic_cdr[_software_id][68])
            self.chkCDRUnitQCQ22.set_active(self._dic_cdr[_software_id][69])
            self.chkCDRUnitQCQ23.set_active(self._dic_cdr[_software_id][70])
            self.chkCDRUnitQCQ24.set_active(self._dic_cdr[_software_id][71])

            self.txtTRRLTCMQ1.set_text(str(self._dic_trr[_software_id][0]))
            self.txtTRRLTCMQ2.set_text(str(self._dic_trr[_software_id][1]))
            self.txtTRRLTCMQ3.set_text(str(self._dic_trr[_software_id][2]))
            self.txtTRRLTCMQ4.set_text(str(self._dic_trr[_software_id][3]))
            self.txtTRRUnitLTCMQ1.set_text(str(self._dic_trr[_software_id][4]))
            self.txtTRRUnitLTCMQ2.set_text(str(self._dic_trr[_software_id][5]))
            self.txtTRRUnitLTCMQ3.set_text(str(self._dic_trr[_software_id][6]))
            self.chkTRRUnitAMQ1.set_active(self._dic_trr[_software_id][7])
            self.chkTRRUnitAMQ2.set_active(self._dic_trr[_software_id][8])
            self.chkTRRUnitQCQ1.set_active(self._dic_trr[_software_id][9])
            self.chkTRRUnitQCQ2.set_active(self._dic_trr[_software_id][10])
            self.chkTRRUnitQCQ3.set_active(self._dic_trr[_software_id][11])
            self.chkTRRUnitQCQ4.set_active(self._dic_trr[_software_id][12])
            self.chkTRRUnitQCQ5.set_active(self._dic_trr[_software_id][13])
            self.chkTRRUnitQCQ6.set_active(self._dic_trr[_software_id][14])
            self.chkTRRUnitQCQ7.set_active(self._dic_trr[_software_id][15])
            self.chkTRRUnitQCQ8.set_active(self._dic_trr[_software_id][16])
            self.chkTRRUnitQCQ9.set_active(self._dic_trr[_software_id][17])
            self.chkTRRUnitQCQ10.set_active(self._dic_trr[_software_id][18])
            self.chkTRRUnitQCQ11.set_active(self._dic_trr[_software_id][19])
            self.chkTRRUnitQCQ12.set_active(self._dic_trr[_software_id][20])
            self.chkTRRUnitQCQ13.set_active(self._dic_trr[_software_id][21])
            self.chkTRRUnitQCQ14.set_active(self._dic_trr[_software_id][22])

            if _error:
                _util.rtk_error(_(u"Unable to retrieve all risk "
                                          u"analysis information for "
                                          u"software module '%s'.") %
                                        self.description)
                return True
            else:
                return False

        def _load_test_planning_page(self):
            """
            Function to load the widgets on the Test Planning gtk.Notebook()
            page.
            """

            # Set the values of all the gtk.Combo() and gtk.Entry() widgets.
            self.cmbTCL.set_active(int(self.tcl))
            self.cmbTestPath.set_active(int(self.test_path))
            self.cmbTestEffort.set_active(int(self.test_effort))
            self.cmbTestApproach.set_active(int(self.test_approach))
            self.txtLaborTest.set_text(str(self.labor_hours_test))
            self.txtLaborDev.set_text(str(self.labor_hours_dev))
            self.txtBudgetTest.set_text(str(self.budget_test))
            self.txtBudgetDev.set_text(str(self.budget_dev))
            self.txtScheduleTest.set_text(str(self.schedule_test))
            self.txtScheduleDev.set_text(str(self.schedule_dev))
            self.txtBranches.set_text(str(self.branches))
            self.txtBranchesTest.set_text(str(self.branches_test))
            self.txtInputs.set_text(str(self.inputs))
            self.txtInputsTest.set_text(str(self.inputs_test))
            self.txtUnits.set_text(str(self.units))
            self.txtUnitsTest.set_text(str(self.units_test))
            self.txtInterfaces.set_text(str(self.interfaces))
            self.txtInterfacesTest.set_text(str(self.interfaces_test))

            # Remove any existing Test Matrices.
            if self.scwTestSelectionMatrix.get_child() is not None:
                self.scwTestSelectionMatrix.remove(
                    self.scwTestSelectionMatrix.get_child())
            _frame = self.hpnTestPlanning.get_child2()
            _label = _frame.get_label_widget()

            # Set the correct test coverage gtk.Entry widgets editable
            # depending on the application level of the selected software.
            if self.level_id == 2:              # Module
                self.txtBranches.props.editable = False
                self.txtBranches.set_sensitive(False)
                self.txtBranchesTest.props.editable = False
                self.txtBranchesTest.set_sensitive(False)
                self.txtInputs.props.editable = False
                self.txtInputs.set_sensitive(False)
                self.txtInputsTest.props.editable = False
                self.txtInputsTest.set_sensitive(False)
                self.txtUnits.props.editable = True
                self.txtUnits.set_sensitive(True)
                self.txtUnitsTest.props.editable = True
                self.txtUnitsTest.set_sensitive(True)
                self.txtInterfaces.props.editable = True
                self.txtInterfaces.set_sensitive(True)
                self.txtInterfacesTest.props.editable = True
                self.txtInterfacesTest.set_sensitive(True)
                self.scwTestSelectionMatrix.add(
                    self.tvwCSCITestSelectionMatrix)
                _label.set_markup("<span weight='bold'>" +
                                  _(u"Module Level Test Technique Selection") +
                                  "</span>")
                _frame.show_all()
            elif self.level_id == 3:            # Unit
                self.txtBranches.props.editable = True
                self.txtBranches.set_sensitive(True)
                self.txtBranchesTest.props.editable = True
                self.txtBranchesTest.set_sensitive(True)
                self.txtInputs.props.editable = True
                self.txtInputs.set_sensitive(True)
                self.txtInputsTest.props.editable = True
                self.txtInputsTest.set_sensitive(True)
                self.txtUnits.props.editable = False
                self.txtUnits.set_sensitive(False)
                self.txtUnitsTest.props.editable = False
                self.txtUnitsTest.set_sensitive(False)
                self.txtInterfaces.props.editable = False
                self.txtInterfaces.set_sensitive(False)
                self.txtInterfacesTest.props.editable = False
                self.txtInterfacesTest.set_sensitive(False)
                self.scwTestSelectionMatrix.add(
                    self.tvwUnitTestSelectionMatrix)
                _label.set_markup("<span weight='bold'>" +
                                  _(u"Unit Level Test Technique Selection") +
                                  "</span>")
                _frame.show_all()
            else:
                self.txtBranches.props.editable = False
                self.txtBranches.set_sensitive(False)
                self.txtBranchesTest.props.editable = False
                self.txtBranchesTest.set_sensitive(False)
                self.txtInputs.props.editable = False
                self.txtInputs.set_sensitive(False)
                self.txtInputsTest.props.editable = False
                self.txtInputsTest.set_sensitive(False)
                self.txtUnits.props.editable = False
                self.txtUnits.set_sensitive(False)
                self.txtUnitsTest.props.editable = False
                self.txtUnitsTest.set_sensitive(False)
                self.txtInterfaces.props.editable = False
                self.txtInterfaces.set_sensitive(False)
                self.txtInterfacesTest.props.editable = False
                self.txtInterfacesTest.set_sensitive(False)
                _label.set_markup("<span weight='bold'></span>")
                _frame.hide()

            return False

        def _load_assessment_results_page(self):
            """
            Loads the gtk.Entry widgets with software reliability aestimation
            results information for the SOFTWARE Object.
            """

            fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

            self.txtFT1.set_text(str(fmt.format(self.ft1)))
            self.txtFT2.set_text(str(fmt.format(self.ft2)))
            self.txtRENAVG.set_text(str(fmt.format(self.ren_avg)))
            self.txtRENEOT.set_text(str(fmt.format(self.ren_eot)))
            self.txtEC.set_text(str(fmt.format(self.ec)))
            self.txtEV.set_text(str(fmt.format(self.ev)))
            self.txtET.set_text(str(fmt.format(self.et)))
            self.txtOS.set_text(str(fmt.format(self.os)))
            self.txtEW.set_text(str(fmt.format(self.ew)))
            self.txtE.set_text(str(fmt.format(self.e_risk)))
            self.txtF.set_text(str(fmt.format(self.failure_rate)))

            return False

        (_model, _row) = self.treeview.get_selection().get_selected()

        # Get the application level ID and development phase ID.
        self.level_id = _model.get_value(_row, 2)

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxSoftware)
        self._app.winWorkBook.show_all()

        # Always display the General Data page and Development Environment page
        _load_general_data_page(self)
        _load_risk_analysis_page(self)

        # If the selected software item is the system, hide the Test Selection
        # page.  Otherwise, show the Test Selection page.
        _n_pages = self.notebook.get_n_pages()
        if self.level_id > 1:
            _load_test_planning_page(self)
            if _n_pages < 3:
                self.notebook.insert_page(self.hpnTestPlanning,
                                          tab_label=self.lblTestPlanning,
                                          position=2)
        else:
            if _n_pages == 3:
                self.notebook.remove_page(2)

# TODO: Implement the software reliability assessment page loading.
        # _load_assessment_results_page(self)

        # Figure out which pages to show in the risk analysis and load the
        # risk map.
        self._show_risk_analysis_page()
        self._load_risk_map()

        self.notebook.set_current_page(self._selected_page)

        _title = _("RTK Work Book: Analyzing %s") % _model.get_value(_row, 3)
        self._app.winWorkBook.set_title(_title)

        return False

    def _load_risk_map(self):
        """
        Method to load the Software class Risk Map.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Load the risk matrix.
        _query = "SELECT fld_software_id, fld_description, fld_a, fld_d, \
                         fld_sa, fld_st, fld_sq, fld_sl, fld_sx, fld_sm, \
                         fld_rpfom, fld_parent_module \
                  FROM tbl_software \
                  WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        try:
            _n_modules = len(_results)
        except TypeError:
            _n_modules = 0
            return True

        _model = self.tvwRiskMap.get_model()
        _model.clear()
        for i in range(_n_modules):
            _data = [_results[i][0], _results[i][1]]
            self._dic_risk[_results[i][0]] = [_results[i][2], _results[i][3],
                                              _results[i][4], _results[i][5],
                                              _results[i][6], _results[i][7],
                                              _results[i][8], _results[i][9],
                                              _results[i][10]]

            # Get the hexidecimal color code for each risk factor.
            _color = _set_risk_color(self._dic_risk, _results[i][0])

            if _results[i][11] == '-':      # It's the top level element.
                _piter = None
            else:                           # It's a child element.
                _piter = _model.get_iter_from_string(_results[i][11])

            _data.append(_color['A'])
            _data.append(_color['D'])
            _data.append(_color['SA'])
            _data.append(_color['ST'])
            _data.append(_color['SQ'])
            _data.append(_color['SL'])
            _data.append(_color['SX'])
            _data.append(_color['SM'])
            _data.append(_color['Risk'])

            _model.append(_piter, _data)

        self.tvwRiskMap.expand_all()

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the Software class gtk.TreeView().

        :param columns: a list of integers representing the column numbers to
                        update.
        :type columns: list of integers
        :param values: a list of new values for the Software class
                       gtk.TreeModel().
        :type values: list
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        for i in columns:
            _model.set_value(_row, i, values[i])

        return False

    def _update_attributes(self):
        """
        Method to update the Software class attributes.
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        self.revision_id = _model.get_value(_row, self._col_order[0])
        self.software_id = _model.get_value(_row, self._col_order[1])
        self.level_id = _model.get_value(_row, self._col_order[2])
        self.description = _model.get_value(_row, self._col_order[3])
        self.application_id = _model.get_value(_row, self._col_order[4])
        self.development_id = _model.get_value(_row, self._col_order[5])
        self.a_risk = _model.get_value(_row, self._col_order[6])
        self.do = _model.get_value(_row, self._col_order[7])
        self.dd = _model.get_value(_row, self._col_order[8])
        self.dc = _model.get_value(_row, self._col_order[9])
        self.d_risk = _model.get_value(_row, self._col_order[10])
        self.am = _model.get_value(_row, self._col_order[11])
        self.sa = _model.get_value(_row, self._col_order[12])
        self.st = _model.get_value(_row, self._col_order[13])
        self.dr = _model.get_value(_row, self._col_order[14])
        self.sq = _model.get_value(_row, self._col_order[15])
        self.s1 = _model.get_value(_row, self._col_order[16])
        self.hloc = _model.get_value(_row, self._col_order[17])
        self.aloc = _model.get_value(_row, self._col_order[18])
        self.sloc = _model.get_value(_row, self._col_order[19])
        self.sl = _model.get_value(_row, self._col_order[20])
        self.ax = _model.get_value(_row, self._col_order[21])
        self.bx = _model.get_value(_row, self._col_order[22])
        self.cx = _model.get_value(_row, self._col_order[23])
        self.nm = _model.get_value(_row, self._col_order[24])
        self.sx = _model.get_value(_row, self._col_order[25])
        self.um = _model.get_value(_row, self._col_order[26])
        self.wm = _model.get_value(_row, self._col_order[27])
        self.xm = _model.get_value(_row, self._col_order[28])
        self.sm = _model.get_value(_row, self._col_order[29])
        self.df = _model.get_value(_row, self._col_order[30])
        self.sr = _model.get_value(_row, self._col_order[31])
        self.s2 = _model.get_value(_row, self._col_order[32])
        self.rpfom = _model.get_value(_row, self._col_order[33])
        self.parent_module = _model.get_value(_row, self._col_order[34])
        self.dev_assess_type = _model.get_value(_row, self._col_order[35])
        self.phase_id = _model.get_value(_row, self._col_order[36])
        self.tcl = _model.get_value(_row, self._col_order[37])
        self.test_path = _model.get_value(_row, self._col_order[38])
        self.category = _model.get_value(_row, self._col_order[39])
        self.test_effort = _model.get_value(_row, self._col_order[40])
        self.test_approach = _model.get_value(_row, self._col_order[41])
        self.labor_hours_test = _model.get_value(_row, self._col_order[42])
        self.labor_hours_dev = _model.get_value(_row, self._col_order[43])
        self.budget_test = _model.get_value(_row, self._col_order[44])
        self.budget_dev = _model.get_value(_row, self._col_order[45])
        self.schedule_test = _model.get_value(_row, self._col_order[46])
        self.schedule_dev = _model.get_value(_row, self._col_order[47])
        self.branches = _model.get_value(_row, self._col_order[48])
        self.branches_test = _model.get_value(_row, self._col_order[49])
        self.inputs = _model.get_value(_row, self._col_order[50])
        self.inputs_test = _model.get_value(_row, self._col_order[51])
        self.nm_test = _model.get_value(_row, self._col_order[52])
        self.interfaces = _model.get_value(_row, self._col_order[53])
        self.interfaces_test = _model.get_value(_row, self._col_order[54])
        self.te = _model.get_value(_row, self._col_order[55])
        self.tm = _model.get_value(_row, self._col_order[56])
        self.tc = _model.get_value(_row, self._col_order[57])
        self.t_risk = _model.get_value(_row, self._col_order[58])
        self.ft1 = _model.get_value(_row, self._col_order[59])
        self.ft2 = _model.get_value(_row, self._col_order[60])
        self.ren_avg = _model.get_value(_row, self._col_order[61])
        self.ren_eot = _model.get_value(_row, self._col_order[62])
        self.ec = _model.get_value(_row, self._col_order[63])
        self.ev = _model.get_value(_row, self._col_order[64])
        self.et = _model.get_value(_row, self._col_order[65])
        self.os = _model.get_value(_row, self._col_order[66])
        self.ew = _model.get_value(_row, self._col_order[67])
        self.e_risk = _model.get_value(_row, self._col_order[68])
        self.failure_rate = _model.get_value(_row, self._col_order[69])
        self.failure_rate = _model.get_value(_row, self._col_order[69])

        return False

    def _update_risk_map(self, model, __path, row):
        """
        Method to update the Software class Risk Map when the risk is
        re-calculated.

        :param model: the Software calss Risk Map gtk.TreeModel().
        :type model: gtk.TreeModel
        :param __path: the path of the selected row in the Software class Risk
                       Map gtk.TreeView().
        :type __path: string
        :param row: the selected Software class gtk.TreeIter() from the risk
                    map gtk.TreeModel().
        :type row: gtk.TreeIter
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _module = model.get_value(row, 0)
        _color = _set_risk_color(self._dic_risk, _module)

        model.set_value(row, 2, _color['A'])
        model.set_value(row, 3, _color['D'])
        model.set_value(row, 4, _color['SA'])
        model.set_value(row, 5, _color['ST'])
        model.set_value(row, 6, _color['SQ'])
        model.set_value(row, 7, _color['SL'])
        model.set_value(row, 8, _color['SX'])
        model.set_value(row, 9, _color['SM'])
        model.set_value(row, 10, _color['Risk'])

        return False

    def _show_risk_analysis_page(self):
        """
        Method to insert and remove pages from the Risk Analysis gtk.Notebook()
        depending on the application level and development phase.  This allows
        the user to only be presented with the risk analysis questions
        pertinent to the development phase.

    Show the pages according to the following:
    +------------------------------+--------+----+-----+-----+-----+-----+
    |             Phase            | Level  | DE | SRR | PDR | CDR | TRR |
    +------------------------------+--------+----+-----+-----+-----+-----+
    | Any                          | System | X  |     |     |     |     |
    +------------------------------+--------+----+-----+-----+-----+-----+
    | Concept/Planning             | Module | X  |     |     |     |     |
    | Software Requirements Review | Module | X  |  X  |     |     |     |
    | Preliminary Design Review    | Module | X  |  X  |  X  |     |     |
    | Critical Design Review       | Module | X  |  X  |  X  |  X  |     |
    | Test Readiness Review        | Module | X  |  X  |  X  |  X  |  X  |
    +------------------------------+--------+----+-----+-----+-----+-----+
    | Concept/Planning             | Unit   | X  |     |     |     |     |
    | Software Requirements Review | Unit   | X  |     |     |     |     |
    | Preliminary Design Review    | Unit   | X  |     |     |     |     |
    | Critical Design Review       | Unit   | X  |     |     |  X  |     |
    | Test Readiness Review        | Unit   | X  |     |     |  X  |  X  |
    +------------------------------+--------+----+-----+-----+-----+-----+

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _show_page(notebook, child, label):
            """
            Function to show a page in a gtk.Notebook().

            :param notebook: the gtk.Notebook() to add the page to.
            :type notebook: gtk.Notebook
            :param child: the child gtk.Widget() to add to the gtk.Notebook()
                          page.
            :type child: gtk.Widget
            :param label: the gtk.Label() to use as the label for the
                          gtk.Notebook() tab.
            :type label: gtk.Label
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            notebook.insert_page(child, tab_label=label, position=-1)

            return False

        def _repack(container, child1=None, child2=None):
            """
            Function to remove existing gtk.Widget() from a container and then
            pack new child gtk.Widget() into the container.

            :param container: a container type gtk.Widget(); typically a
                              gtk.Box() or gtk.Paned().
            :type container: gtk.Widget
            :param child1: a gtk.Widget().
            :type child1: gtk.Widget
            :param child2: a gtk.Widget().
            :type child2: gtk.Widget
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # Remove existing children from the container.
            if container.get_child1() is not None:
                container.remove(container.get_child1())

            if container.get_child2() is not None:
                container.remove(container.get_child2())

            # Pack the new children into the container.
            if child1 is not None:
                container.pack1(child1, resize=True, shrink=True)

            if child2 is not None:
                container.pack2(child2, resize=True, shrink=True)

            container.show_all()

            return False

        # Remove all but the development environment risk analysis page.
        self.nbkRiskAnalysis.remove_page(4)
        self.nbkRiskAnalysis.remove_page(3)
        self.nbkRiskAnalysis.remove_page(2)
        self.nbkRiskAnalysis.remove_page(1)

        # This is the software requirements review (SRR) phase.
        if self.phase_id == 2:
            if self.level_id == 2:          # Module
                _show_page(self.nbkRiskAnalysis, self.hpnSRR, self.lblSRR)

        # This is the preliminary design review (PDR) phase.
        elif self.phase_id == 3:
            if self.level_id == 2:          # Module
                _show_page(self.nbkRiskAnalysis, self.hpnSRR, self.lblSRR)
                _show_page(self.nbkRiskAnalysis, self.hpnPDR, self.lblPDR)

        # This is the critical design review (CDR) phase.
        elif self.phase_id == 4:
            if self.hpnCDR.get_child1() is not None:
                self.hpnCDR.remove(self.hpnCDR.get_child1())
            if self.hpnCDR.get_child2() is not None:
                self.hpnCDR.remove(self.hpnCDR.get_child2())

            if self.level_id == 2:          # Module
                _repack(self.hpnCDR, self.fraCDRCSCIAM, self.fraCDRCSCIQC)

                _show_page(self.nbkRiskAnalysis, self.hpnSRR, self.lblSRR)
                _show_page(self.nbkRiskAnalysis, self.hpnPDR, self.lblPDR)
                _show_page(self.nbkRiskAnalysis, self.hpnCDR, self.lblCDR)

            elif self.level_id == 3:        # Unit
                _repack(self.hpnCDR, self.fraCDRUnitAM, self.fraCDRUnitQC)
                _show_page(self.nbkRiskAnalysis, self.hpnCDR, self.lblCDR)

        # This is the test readiness review (TRR) phase.
        elif self.phase_id == 5:
            if self.hpnTRR.get_child1() is not None:
                self.hpnTRR.remove(self.hpnTRR.get_child1())
            if self.hpnTRR.get_child2() is not None:
                self.hpnTRR.remove(self.hpnTRR.get_child2())

            if self.level_id == 2:          # Module
                _repack(self.hpnCDR, self.fraCDRCSCIAM, self.fraCDRCSCIQC)
                _repack(self.hpnTRR, self.fraTRRCSCILT)

                _show_page(self.nbkRiskAnalysis, self.hpnSRR, self.lblSRR)
                _show_page(self.nbkRiskAnalysis, self.hpnPDR, self.lblPDR)
                _show_page(self.nbkRiskAnalysis, self.hpnCDR, self.lblCDR)
                _show_page(self.nbkRiskAnalysis, self.hpnTRR, self.lblTRR)

            elif self.level_id == 3:        # Unit
                _repack(self.hpnCDR, self.fraCDRUnitAM, self.fraCDRUnitQC)
                _repack(self.hpnTRR, self.fraTRRUnitLT, self.fraTRRUnitQC)
                _show_page(self.nbkRiskAnalysis, self.hpnCDR, self.lblCDR)
                _show_page(self.nbkRiskAnalysis, self.hpnTRR, self.lblTRR)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Software class
        gtk.TreeView().

        :param treeview: the Software class gtk.TreeView().
        :type treeview: gtk.TreeView
        :param event: the gtk.gdk.Event() that called this function (the
                      important attribute is which mouse button was clicked).
                      1 = left
                      2 = scrollwheel
                      3 = right
                      4 = forward
                      5 = backward
                      8 =
                      9 =
        :type event: gtk.gdk.Event
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if event.button == 1:
            self._treeview_row_changed(treeview, None, 0, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, __treeview, __path, __column, index):
        """
        Callback function to handle events for the Software class
        gtk.Treeview().  It is called whenever the Software class
        gtk.TreeView() is clicked or a row is activated.  It will save the
        previously selected row in the Software class gtk.TreeView().  Then it
        loads the Software class.

        :param __treeview: one of the Software class gtk.TreeView().
        :type __treeview: gtk.TreeView
        :param __path: the activated row's path.
        :type __path: string
        :param __column: the activated gtk.TreeViewColumn().
        :type __column: gtk.TreeViewColumn
        :param index: determines which Software class gtk.TreeView() had the
                      change:
                      0 = main treeview
                      1 = incident list treeview
                      2 = incident action list treeview
        :type index: integer
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Save the previously selected row in the Software tree.
        if index == 0:                      # The main software treeview.
            # if self._selected_row is not None:
                # path_ = _model.get_path(_row)
                # self._save_line_item(self.model, path_, self._selected_row)

            (_model, _row) = self.treeview.get_selection().get_selected()

            if _row is not None:
                self._update_attributes()
                self.load_notebook()

                # Build the queries to select the reliability tests and program
                # incidents associated with the selected Software.
                _qryIncidents = "SELECT * FROM tbl_incident \
                                 WHERE fld_software_id=%d" % self.software_id

                # self._app.winParts.load_incident_tree(_qryIncidents)

                return False
            else:
                return True

    def _add_module(self, __button, level):
        """
        Adds a new Software module to the Program's database.

        :param __button: the gtk.Button() that called this function.
        :type __button: gtk.Button
        :param level: the level of Software module to add.
                      0 = sibling
                      1 = child
        :type level: integer
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()
        if level == 0:
            _iter = _model.iter_parent(_row)
            _parent = _model.get_string_from_iter(_iter)
            _n_new_module = _util.add_items(title=_(u"RTK - Add Sibling "
                                                    u"Modules"),
                                            prompt=_(u"How many sibling "
                                                     u"modules to add?"))
        elif level == 1:
            _parent = _model.get_string_from_iter(_row)
            _n_new_module = _util.add_items(title=_(u"RTK - Child Modules"),
                                            prompt=_(u"How many child modules "
                                                     u"to add?"))

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        for i in range(_n_new_module):
            # Create the default description of the assembly.
            _descrip = str(_conf.RTK_PREFIX[16]) + ' ' + \
                       str(_conf.RTK_PREFIX[17])    # noqa

            # Increment the assembly index.
            _conf.RTK_PREFIX[17] = _conf.RTK_PREFIX[17] + 1

            # First we add the module to the software table.
            _query = "INSERT INTO tbl_software \
                      (fld_revision_id, fld_parent_module, \
                       fld_description) \
                      VALUES (%d, '%s', '%s')" % \
                     (self._app.REVISION.revision_id, _parent, _descrip)
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx,
                                                  commit=True)

            if not _results:
                self._app.debug_log.error("software.py: Failed to add new "
                                          "module to software table.")
                return True

            # Retrienve the ID of the newly created module.
            if _conf.BACKEND == 'mysql':
                _query_ = "SELECT LAST_INSERT_ID()"
            elif _conf.BACKEND == 'sqlite3':
                _query_ = "SELECT seq \
                           FROM sqlite_sequence \
                           WHERE name='tbl_software'"

            _new_id_ = self._app.DB.execute_query(_query_,
                                                  None,
                                                  self._app.ProgCnx)
            _new_id_ = _new_id_[0][0]

            if _new_id_ == '':
                self._app.debug_log.error("software.py: Failed to retrieve "
                                          "new software module ID.")
                return True

            # Add the new software module to the Development Environment risk
            # analysis table.
            for i in range(43):
                _query = "INSERT INTO tbl_software_development \
                          (fld_software_id, fld_question_id) \
                          VALUES (%d, %d)" % (_new_id_, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            # Add the new software module to the Requirements Review risk
            # analysis table.
            for i in range(50):
                _query = "INSERT INTO tbl_srr_ssr \
                          (fld_software_id, fld_question_id) \
                          VALUES (%d, %d)" % (_new_id_, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            # Add the new software module to the Preliminary Design Review risk
            # analysis table.
            for i in range(39):
                _query = "INSERT INTO tbl_pdr \
                      (fld_software_id, fld_question_id) \
                      VALUES (%d, %d)" % (_new_id_, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            # Add the new software module to the Critical Design Review risk
            # analysis table.
            for i in range(72):
                _query = "INSERT INTO tbl_cdr \
                      (fld_software_id, fld_question_id) \
                      VALUES (%d, %d)" % (_new_id_, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            # Add the new software module to the Test Readiness Review risk
            # analysis table.
            for i in range(25):
                _query = "INSERT INTO tbl_trr \
                          (fld_software_id, fld_question_id) \
                          VALUES (%d, %d)" % (_new_id_, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            # Add the new software module to the test table.
            for i in range(21):
                _query = "INSERT INTO tbl_software_tests \
                          (fld_software_id, fld_technique_id) \
                          VALUES (%d, %d)" % (_new_id_, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

        self.load_tree()

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)  # @UndefinedVariable

        return False

    def _delete_module(self, __widget):
        """
        Deletes the currently selected software modules from the Program's
        database.

        :param __widget: the gtk.Widget() that called this function.
        :type __widget: gtk.Widget
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        # First delete all of the children from the software table.
        _query = "DELETE FROM tbl_software \
                  WHERE fld_parent_module=%d" % \
                 _model.get_string_from_iter(_row)
        _results_ = self._app.DB.execute_query(_query,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("software.py: Failed to delete module "
                                      "from software table.")
            return True

        # Second delete the parent from the software table.
        _query = "DELETE FROM tbl_software \
                  WHERE fld_revision_id=%d \
                  AND fld_software_id=%d" % \
                 (self._app.REVISION.revision_id, self.software_id)
        _results_ = self._app.DB.execute_query(_query,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("software.py: Failed to delete module "
                                      "from software table.")
            return True

        self.load_tree()

        return False

    def save_software(self):
        """
        Saves the Software class gtk.TreeView() information to the open RTK
        Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _save_line(model, __path, row, self):
            """
            Saves each row in the Software class gtk.TreeModel to the open RTK
            program database.

            :param model: the Software class gtk.TreeModel().
            :type model: gtk.TreeModel
            :param __path: the path of the active row in the Software class
                           gtk.TreeModel().
            :type __path: string
            :param row: the selected row in the Software class gtk.TreeView().
            :type row: gtk.TreeIter
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _values = (model.get_value(row, self._col_order[2]),
                       model.get_value(row, self._col_order[3]),
                       model.get_value(row, self._col_order[4]),
                       model.get_value(row, self._col_order[5]),
                       model.get_value(row, self._col_order[6]),
                       model.get_value(row, self._col_order[7]),
                       model.get_value(row, self._col_order[8]),
                       model.get_value(row, self._col_order[9]),
                       model.get_value(row, self._col_order[10]),
                       model.get_value(row, self._col_order[11]),
                       model.get_value(row, self._col_order[12]),
                       model.get_value(row, self._col_order[13]),
                       model.get_value(row, self._col_order[14]),
                       model.get_value(row, self._col_order[15]),
                       model.get_value(row, self._col_order[16]),
                       model.get_value(row, self._col_order[17]),
                       model.get_value(row, self._col_order[18]),
                       model.get_value(row, self._col_order[19]),
                       model.get_value(row, self._col_order[20]),
                       model.get_value(row, self._col_order[21]),
                       model.get_value(row, self._col_order[22]),
                       model.get_value(row, self._col_order[23]),
                       model.get_value(row, self._col_order[24]),
                       model.get_value(row, self._col_order[25]),
                       model.get_value(row, self._col_order[26]),
                       model.get_value(row, self._col_order[27]),
                       model.get_value(row, self._col_order[28]),
                       model.get_value(row, self._col_order[29]),
                       model.get_value(row, self._col_order[30]),
                       model.get_value(row, self._col_order[31]),
                       model.get_value(row, self._col_order[32]),
                       model.get_value(row, self._col_order[33]),
                       model.get_value(row, self._col_order[34]),
                       model.get_value(row, self._col_order[35]),
                       model.get_value(row, self._col_order[36]),
                       model.get_value(row, self._col_order[37]),
                       model.get_value(row, self._col_order[38]),
                       model.get_value(row, self._col_order[39]),
                       model.get_value(row, self._col_order[40]),
                       model.get_value(row, self._col_order[41]),
                       model.get_value(row, self._col_order[42]),
                       model.get_value(row, self._col_order[43]),
                       model.get_value(row, self._col_order[44]),
                       model.get_value(row, self._col_order[45]),
                       model.get_value(row, self._col_order[46]),
                       model.get_value(row, self._col_order[47]),
                       model.get_value(row, self._col_order[48]),
                       model.get_value(row, self._col_order[49]),
                       model.get_value(row, self._col_order[50]),
                       model.get_value(row, self._col_order[51]),
                       model.get_value(row, self._col_order[52]),
                       model.get_value(row, self._col_order[53]),
                       model.get_value(row, self._col_order[54]),
                       model.get_value(row, self._col_order[55]),
                       model.get_value(row, self._col_order[56]),
                       model.get_value(row, self._col_order[57]),
                       model.get_value(row, self._col_order[58]),
                       model.get_value(row, self._col_order[59]),
                       model.get_value(row, self._col_order[60]),
                       model.get_value(row, self._col_order[61]),
                       model.get_value(row, self._col_order[62]),
                       model.get_value(row, self._col_order[63]),
                       model.get_value(row, self._col_order[64]),
                       model.get_value(row, self._col_order[65]),
                       model.get_value(row, self._col_order[66]),
                       model.get_value(row, self._col_order[67]),
                       model.get_value(row, self._col_order[68]),
                       model.get_value(row, self._col_order[69]),
                       model.get_value(row, self._col_order[0]),
                       model.get_value(row, self._col_order[1]))

            _query = "UPDATE tbl_software \
                      SET fld_level_id=%d, fld_description='%s', \
                          fld_application_id=%d, fld_development_id=%d, \
                          fld_a=%f, fld_do=%f, fld_dd=%d, fld_dc=%f, \
                          fld_d=%f, fld_am=%f, fld_sa=%f, fld_st=%f, \
                          fld_dr=%f, fld_sq=%f, fld_s1=%f, fld_hloc=%d, \
                          fld_aloc=%d, fld_loc=%d, fld_sl=%f, fld_ax=%d, \
                          fld_bx=%d, fld_cx=%d, fld_nm=%d, fld_sx=%f, \
                          fld_um=%d, fld_wm=%d, fld_xm=%d, fld_sm=%f, \
                          fld_df=%f, fld_sr=%f, fld_s2=%f, fld_rpfom=%f, \
                          fld_parent_module='%s', fld_dev_assess_type=%d, \
                          fld_phase_id=%d, fld_tcl=%d, fld_test_path=%d, \
                          fld_category=%d, fld_test_effort=%d, \
                          fld_test_approach=%d, fld_labor_hours_test=%f, \
                          fld_labor_hours_dev=%f, fld_budget_test=%f, \
                          fld_budget_dev=%f, fld_schedule_test=%f, \
                          fld_schedule_dev=%f, fld_branches=%d, \
                          fld_branches_test=%d, fld_inputs=%d, \
                          fld_inputs_test=%d, fld_nm_test=%d, \
                          fld_interfaces=%d, fld_interfaces_test=%d, \
                          fld_te=%f, fld_tc=%f, fld_tm=%f, fld_t=%f, \
                          fld_ft1=%f, fld_ft2=%f, fld_ren_avg=%f, \
                          fld_ren_eot=%f, fld_ec=%f, fld_ev=%f, fld_et=%f, \
                          fld_os=%f, fld_ew=%f, fld_e=%f, fld_f=%f \
                  WHERE fld_revision_id=%d AND fld_software_id=%d" % _values
            _results = self._app.DB.execute_query(_query,
                                                  None,
                                                  self._app.ProgCnx,
                                                  commit=True)

            if not _results:
                _util.rtk_error(_(u"Failed to save information for "
                                          u"software module %s.  If the "
                                          u"problem persists you can report "
                                          u"it to bugs@reliaqual.com.") %
                                        model.get_value(row,
                                                        self._col_order[3]))
                return True

            return False

        _model = self.treeview.get_model()
        _model.foreach(_save_line, self)

        return False

    def _save_risk_analysis(self):
        """
        Method to save the answers to the Risk Analysis questions on the
        currently selected tab in the risk analysis gtk.NoteBook().

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
# TODO: Add a transaction before saving all the risk Q & A stuff.
        def _save_development_env(self):
            """
            Function to save development environment information to the open
            RTK program database.

            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            for i in range(43):
                _query = "UPDATE tbl_software_development \
                          SET fld_y=%d \
                          WHERE fld_software_id=%d \
                          AND fld_question_id=%d" % \
                         (self._dic_dev_env[self.software_id][i],
                          self.software_id, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        def _save_srr(self):
            """
            Function to save software requirements review information to the
            open RTK program database.

            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            for i in range(50):
                if i not in [0, 1, 2, 3, 5, 6, 25, 26, 31, 32, 33, 34]:
                    _query = "UPDATE tbl_srr_ssr \
                              SET fld_y=%d \
                              WHERE fld_software_id=%d \
                              AND fld_question_id=%d" % \
                             (self._dic_srr[self.software_id][i],
                              self.software_id, i)
                else:
                    _query = "UPDATE tbl_srr_ssr \
                              SET fld_value=%d \
                              WHERE fld_software_id=%d \
                              AND fld_question_id=%d" % \
                             (self._dic_srr[self.software_id][i],
                              self.software_id, i)

                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        def _save_pdr(self):
            """
            Function to save preliminary design review information to the open
            RTK program database.

            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            for i in range(39):
                if i not in [17, 18, 21, 22, 23, 24, 25, 26, 29, 30]:
                    _query = "UPDATE tbl_pdr \
                              SET fld_y=%d \
                              WHERE fld_software_id=%d \
                              AND fld_question_id=%d" % \
                             (self._dic_pdr[self.software_id][i],
                              self.software_id, i)
                else:
                    _query = "UPDATE tbl_pdr \
                              SET fld_value=%d \
                              WHERE fld_software_id=%d \
                              AND fld_question_id=%d" % \
                             (self._dic_pdr[self.software_id][i],
                              self.software_id, i)

                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        def _save_cdr(self):
            """
            Function to save critical design review information to the open
            RTK program database.

            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            for i in range(72):
                if i in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 37, 38, 39, 40, 41,
                         42, 43, 44, 45, 46, 47, 50, 53, 60, 61, 64, 65, 66,
                         67, 68, 69, 70, 71]:
                    _query = "UPDATE tbl_cdr \
                              SET fld_y=%d \
                              WHERE fld_software_id=%d \
                              AND fld_question_id=%d" % \
                             (self._dic_cdr[self.software_id][i],
                              self.software_id, i)
                else:
                    _query = "UPDATE tbl_cdr \
                              SET fld_value=%d \
                              WHERE fld_software_id=%d \
                              AND fld_question_id=%d" % \
                             (self._dic_cdr[self.software_id][i],
                              self.software_id, i)

                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        def _save_trr(self):
            """
            Function to save test readiness review information to the open
            RTK program database.

            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            for i in [0, 1, 2, 3, 4, 5, 6]:
                _query = "UPDATE tbl_trr \
                          SET fld_value=%d \
                          WHERE fld_software_id=%d \
                          AND fld_question_id=%d" % \
                         (self._dic_trr[self.software_id][i],
                          self.software_id, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            for i in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                      23, 24]:
                _query = "UPDATE tbl_trr \
                          SET fld_y=%d \
                          WHERE fld_software_id=%d \
                          AND fld_question_id=%d" % \
                         (self._dic_trr[self.software_id][i],
                          self.software_id, i)
                self._app.DB.execute_query(_query,
                                           None,
                                           self._app.ProgCnx,
                                           commit=True)

            return False

        # Find the currently selected tab in the Risk Analysis gtk.NoteBook().
        # If the software item being analyzed is unit-level and the selected
        # tab is not the Development Environment tab, then add two to account
        # for the lack of SRR and PDR tabs for software units.
        _page = self.nbkRiskAnalysis.get_current_page()
        if self.level_id == 3 and _page > 0:
            _page += 2

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        # Save the correct results.
        if _page == 0:
            if _save_development_env(self):
                self._app.debug_log.error("software.py: Failed to save "
                                          "Development Environment answers.")
        elif _page == 1:
            if _save_srr(self):
                self._app.debug_log.error("software.py: Failed to save "
                                          "Requirements Review answers.")
        elif _page == 2:
            if _save_pdr(self):
                self._app.debug_log.error("software.py: Failed to save "
                                          "Preliminary Design Review answers.")
        elif _page == 3:
            if _save_cdr(self):
                self._app.debug_log.error("software.py: Failed to save "
                                          "Critical Design Review answers.")
        elif _page == 4:
            if _save_trr(self):
                self._app.debug_log.error("software.py: Failed to save "
                                          "Test Readiness Review answers.")

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _save_test_techniques(self):
        """
        Method to save the test techniques for the currently selected
        software module.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        _software_id = _model.get_value(_row, self._col_order[1])

        _model.set_value(_row, 37, self.cmbTCL.get_active())
        _model.set_value(_row, 38, self.cmbTestPath.get_active())

        _values = (_model.get_value(_row, self._col_order[37]),
                   _model.get_value(_row, self._col_order[38]),
                   _model.get_value(_row, self._col_order[40]),
                   _model.get_value(_row, self._col_order[41]),
                   _model.get_value(_row, self._col_order[42]),
                   _model.get_value(_row, self._col_order[43]),
                   _model.get_value(_row, self._col_order[44]),
                   _model.get_value(_row, self._col_order[45]),
                   _model.get_value(_row, self._col_order[46]),
                   _model.get_value(_row, self._col_order[47]),
                   _model.get_value(_row, self._col_order[48]),
                   _model.get_value(_row, self._col_order[49]),
                   _model.get_value(_row, self._col_order[50]),
                   _model.get_value(_row, self._col_order[51]),
                   _model.get_value(_row, self._col_order[52]),
                   _model.get_value(_row, self._col_order[53]),
                   _model.get_value(_row, self._col_order[54]),
                   _software_id)
        _query = "UPDATE tbl_software \
                  SET fld_tcl=%d, fld_test_path=%d, fld_test_effort=%d, \
                      fld_test_approach=%d, fld_labor_hours_test=%f, \
                      fld_labor_hours_dev=%f, fld_budget_test=%f, \
                      fld_budget_dev=%f, fld_schedule_test=%f, \
                      fld_schedule_dev=%f, fld_branches=%d, \
                      fld_branches_test=%d, fld_inputs=%d, \
                      fld_inputs_test=%d, fld_nm_test=%d, fld_interfaces=%d, \
                      fld_interfaces_test=%d \
                  WHERE fld_software_id=%d" % _values
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx,
                                              commit=True)

        if not _results:
            _util.rtk_error(_(u"Failed to save test selection "
                                      u"information to the open RTK program "
                                      u"database."))
            return True
# TODO: Save recommended and selected values to database.
        #_model = self.tvwCSCITestSelectionMatrix.get_model()

        return False

    def _callback_check(self, check, index):
        """
        Callback function to retrieve and save gtk.CheckButton() changes.

        :param check: the gtk.CheckButton() that called the function.
        :type check: gtk.CheckButton
        :param index: the position in the applicable Software class dictionary
                      associated with the data from the calling checkbutton.
        :type index: integer
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        if index < 100:                     # Main Software Tree.
            _model.set_value(_row, index, check.get_active())

            self._update_attributes()

        # Risk analysis checkbutton handling.
        elif index >= 100 and index < 200:  # Development Environment.
            self._dic_dev_env[self.software_id][index - 100] = \
                _util.string_to_boolean(check.get_active())
        elif index >= 200 and index < 300:  # Requirements Review.
            self._dic_srr[self.software_id][index - 200] = \
                _util.string_to_boolean(check.get_active())
        elif index >= 300 and index < 400:  # Preliminary Design Review.
            self._dic_pdr[self.software_id][index - 300] = \
                _util.string_to_boolean(check.get_active())
        elif index >= 400 and index < 500:  # Critical Design Review.
            self._dic_cdr[self.software_id][index - 400] = \
                _util.string_to_boolean(check.get_active())
        elif index >= 500 and index < 600:  # Test Readiness Review.
            self._dic_trr[self.software_id][index - 500] = \
                _util.string_to_boolean(check.get_active())

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save combobox changes.

        :param combo: the gtk.ComboBox() that called the function.
        :type combo: gtk.ComboBox
        :param index: the position in the Software class gtk.TreeView()
                      associated with the data from the calling gtk.ComboBox().
        :type index: integer
        :return: False if successful and True if an error is encountered.
        :rtype: boolean
        """

        _combo_state = combo.get_active()

        (_model, _row) = self.treeview.get_selection().get_selected()

        if index < 100:
            if index == 2:                  # Software level
                # Remove the existing Test Selection Matrix and add the
                # correct one.
                if self.scwTestSelectionMatrix.get_child() is not None:
                    self.scwTestSelectionMatrix.remove(
                        self.scwTestSelectionMatrix.get_child())
                if self.application_id == 2:    # CSCI
                    self.scwTestSelectionMatrix.add(
                        self.tvwCSCITestSelectionMatrix)
                elif self.application_id == 3:  # Unit
                    self.scwTestSelectionMatrix.add(
                        self.tvwUnitTestSelectionMatrix)
                self.scwTestSelectionMatrix.show_all()
            # elif index == 4:              # Application type
            #     self.model.set_value(self._selected_row, 6,
            #                          self._fault_density[i])
            # elif index == 5:              # Development environment
            #     self.model.set_value(self._selected_row, 7, self._do[i])
            elif index == 40:               # Test effort
                if _combo_state == 1:
                    self.txtLaborTest.props.editable = True
                    self.txtLaborTest.set_sensitive(True)
                    self.txtLaborDev.props.editable = True
                    self.txtLaborDev.set_sensitive(True)
                    self.txtBudgetTest.props.editable = False
                    self.txtBudgetTest.set_sensitive(False)
                    self.txtBudgetDev.props.editable = False
                    self.txtBudgetDev.set_sensitive(False)
                    self.txtScheduleTest.props.editable = False
                    self.txtScheduleTest.set_sensitive(False)
                    self.txtScheduleDev.props.editable = False
                    self.txtScheduleDev.set_sensitive(False)
                elif _combo_state == 2:
                    self.txtLaborTest.props.editable = False
                    self.txtLaborTest.set_sensitive(False)
                    self.txtLaborDev.props.editable = False
                    self.txtLaborDev.set_sensitive(False)
                    self.txtBudgetTest.props.editable = True
                    self.txtBudgetTest.set_sensitive(True)
                    self.txtBudgetDev.props.editable = True
                    self.txtBudgetDev.set_sensitive(True)
                    self.txtScheduleTest.props.editable = False
                    self.txtScheduleTest.set_sensitive(False)
                    self.txtScheduleDev.props.editable = False
                    self.txtScheduleDev.set_sensitive(False)
                elif _combo_state == 3:
                    self.txtLaborTest.props.editable = False
                    self.txtLaborTest.set_sensitive(False)
                    self.txtLaborDev.props.editable = False
                    self.txtLaborDev.set_sensitive(False)
                    self.txtBudgetTest.props.editable = False
                    self.txtBudgetTest.set_sensitive(False)
                    self.txtBudgetDev.props.editable = False
                    self.txtBudgetDev.set_sensitive(False)
                    self.txtScheduleTest.props.editable = True
                    self.txtScheduleTest.set_sensitive(True)
                    self.txtScheduleDev.props.editable = True
                    self.txtScheduleDev.set_sensitive(True)

            _model.set_value(_row, index, _combo_state)

            self._update_attributes()

            if index == 2 or index == 36:
                self._show_risk_analysis_page()

        return False

    def _callback_entry(self, entry, __event, convert, index):
        """
        Callback function to retrieve and save Software class gtk.Entry()
        changes.

        :param entry: the gtk.Entry() that called the function.
        :type entry: gtk.Entry
        :param __event: the gtk.gdk.Event() that called the function.
        :type __event: gtk.gdk.Event
        :param convert: the data type to convert the entry contents to.
        :type convert: string
        :param index: the position in the Software class gtk.TreeView()
                      associated with the data from the calling entry.
        :type index: integer
        :return: False if successful and True if an error is encountered.
        :rtype: boolean
        """

        from datetime import datetime

        (_model, _row) = self.treeview.get_selection().get_selected()

        if convert == 'text':
            if index == 3:
                _buffer = self.txtDescription.get_child().get_child().get_buffer()  # noqa
                _text = _buffer.get_text(*_buffer.get_bounds())
            else:
                _text = entry.get_text()

        elif convert == 'int':
            try:
                _text = int(entry.get_text())
            except ValueError:
                _text = 0

        elif convert == 'float':
            _text = float(entry.get_text().replace('$', ''))

        elif convert == 'date':
            _text = datetime.strptime(entry.get_text(), '%Y-%m-%d').toordinal()

        if index < 100:                   # Software information.
            # Calculate the number of higher order language lines of code.
            if index == 18:
                ALOC = _model.get_value(_row, 18)
                SLOC = _model.get_value(_row, 19)
                HLOC = SLOC - _text
                try:
                    SL = (float(HLOC) / float(_text)) + \
                         1.4 * (float(ALOC) / float(_text))     # noqa
                except ZeroDivisionError:
                    SL = 0.0
                # self.txtHLOC.set_text(str(HLOC))
                _model.set_value(_row, 17, HLOC)
                _model.set_value(_row, 20, SL)
            elif index == 19:
                ALOC = _model.get_value(_row, 18)
                SLOC = _model.get_value(_row, 19)
                HLOC = _text - ALOC
                try:
                    SL = (float(HLOC) / float(_text)) + \
                         1.4 * (float(ALOC) / float(_text))     # noqa
                except ZeroDivisionError:
                    SL = 0.0
                # self.txtHLOC.set_text(str(HLOC))
                _model.set_value(_row, 17, HLOC)
                _model.set_value(_row, 20, SL)

            # Update the Software Tree.
            _model.set_value(_row, index, _text)

            self._update_attributes()

        # Risk analysis entry handling.
        elif index >= 200 and index < 300:  # Requirements review
            self._dic_srr[self.software_id][index - 200] = _text
        elif index >= 300 and index < 400:  # Preliminary design review
            self._dic_pdr[self.software_id][index - 300] = _text
        elif index >= 400 and index < 500:  # Critical design review
            self._dic_cdr[self.software_id][index - 400] = _text
        elif index >= 500 and index < 600:  # Test readiness review
            self._dic_trr[self.software_id][index - 500] = _text

        return False

    def _notebook_page_switched(self, __notebook, __page, page_num, index):
        """
        Called whenever the Software class Work Book page is changed.

        :param __notebook: the Software class gtk.Notebook().
        :type __notebook: gtk.Notebook
        :param __page: the newly selected page widget.
        :type __page: gtk.Widget
        :param page_num: the newly selected page number.
                         0 = General Data
                         1 = Risk Analysis
                         2 = Test Selection
                         3 = Assessment Results
        :type page_num: integer
        :param index: which gtk.Notebook() called this method.
        :type index: integer
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if index == 0:                      # Main gtk.Notebook
            if page_num == 1:               # Risk Analysis
                self.btnAnalyze.show()
                self.btnSaveResults.set_tooltip_text(_(u"Saves risk analysis "
                                                       u"information for the "
                                                       u"selected software "
                                                       u"unit or module."))
            elif page_num == 2:             # Test planning
                self.btnAnalyze.show()
                self.btnSaveResults.set_tooltip_text(_(u"Saves test planning "
                                                       u"information for the "
                                                       u"selected software "
                                                       u"unit or module."))
            elif page_num == 3:             # Reliability estimation
                self.btnAnalyze.hide()
                self.btnSaveResults.set_tooltip_text(_(u"Saves reliability "
                                                       u"estimates for the "
                                                       u"selected software "
                                                       u"unit or module."))
            else:                           # Everything else
                self.btnAnalyze.hide()
                self.btnSaveResults.set_tooltip_text(_(u"Saves the selected "
                                                       u"software module."))

        self._selected_page = page_num

        return False

    def _toolbutton_pressed(self, button):
        """
        Method to react to the Software class gtk.ToolButton clicked events.

        :param button: the gtk.ToolButton() that was pressed.
        :type button: gtk.ToolButton
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _button = button.get_name()
        _page = self.notebook.get_current_page()

        if _page == 1:                      # Risk Analysis
            if _button == 'Save':
                self._save_risk_analysis()
        elif _page == 2:                    # Test planning
            if _button == 'Save':
                self._save_test_techniques()
        elif _page == 3:                    # Reliability estimation
            if _button == 'Save':
                self.save_software()
        else:                               # Everything else
            if _button == 'Save':
                self.save_software()

        return False

    def calculate(self, __button):
        """
        Method to calculate metrics for the Software class.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: gtk.ToolButton
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _count_units(model, __path, row, self):
            """
            Function to sum unit-level answers for the parent module-level
            module.

            :param model: the Software class gtk.TreeModel().
            :type model: gtk.TreeModel
            :param __path: the currently active path in the Software class
                           gtk.TreeModel()
            :type __path: tuple
            :param row: the currently active gtk.TreeIter() in the Software
                        class gtk.TreeModel().
            :type row: gtk.TreeIter
            :param self: the current instance of the RTK application.
            :type self: RTK instance
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _software_id = model.get_value(row, 1)
            _level_id = model.get_value(row, 2)
            _phase_id = model.get_value(row, 36)
            _path = model.get_string_from_iter(row)

            # Count the total number of direct child units units in the module.
            _query = "SELECT COUNT(fld_parent_module) \
                      FROM tbl_software \
                      WHERE fld_parent_module='%s'" % _path
            _nm = self._app.DB.execute_query(_query,
                                             None,
                                             self._app.ProgCnx)[0][0]

            _loc = 0
            _aloc = 0
            _hloc = 0
            if _phase_id == 4:              # CDR
                if _level_id == 2:          # Module
                    for i in [37, 43, 51, 54, 61, 62, 65, 66, 67, 68, 69, 70,
                              71, 72]:
                        _query = "SELECT COUNT(t2.fld_y) \
                                  FROM tbl_software AS t1 \
                                  INNER JOIN tbl_cdr AS t2 \
                                  ON t2.fld_software_id=t1.fld_software_id \
                                  WHERE t2.fld_question_id=%d \
                                  AND t1.fld_parent_module='%s'" % (i, _path)
                        _count = self._app.DB.execute_query(_query,
                                                            None,
                                                            self._app.ProgCnx)
                        try:
                            _count = _count[0][0] + 0
                        except TypeError:
                            _count = 0

                        _query = "UPDATE tbl_cdr \
                                  SET fld_value=%d \
                                  WHERE fld_software_id=%d \
                                  AND fld_question_id=%d" % \
                                 (_count, _software_id, i)
                        self._app.DB.execute_query(_query,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

                    for i in [49, 50, 52, 53, 55, 56, 57, 58, 59, 60, 63, 64]:
                        _query = "SELECT SUM(t2.fld_value) \
                                  FROM tbl_software AS t1 \
                                  INNER JOIN tbl_cdr AS t2 \
                                  ON t2.fld_software_id=t1.fld_software_id \
                                  WHERE t2.fld_question_id=%d \
                                  AND t1.fld_parent_module='%s'" % (i, _path)
                        _count = self._app.DB.execute_query(_query,
                                                            None,
                                                            self._app.ProgCnx)
                        try:
                            _count = _count[0][0] + 0
                        except TypeError:
                            _count = 0

                        _query = "UPDATE tbl_cdr \
                                  SET fld_value=%d \
                                  WHERE fld_software_id=%d \
                                  AND fld_question_id=%d" % \
                                 (_count, _software_id, i)
                        self._app.DB.execute_query(_query,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

                        # Get the count of lines of code
                        if i == 49:
                            _loc = _count

                elif _level_id == 3:        # Unit
                    # All we have at the unit level is the lines of code in
                    # the unit.
                    _query = "SELECT fld_value \
                              FROM tbl_cdr \
                              WHERE fld_software_id=%d \
                              AND fld_question_id=49" % _software_id
                    _loc = self._app.DB.execute_query(_query,
                                                      None,
                                                      self._app.ProgCnx)
                    try:
                        _loc[0][0] + 0
                    except TypeError:
                        _loc = 0

            elif _phase_id == 5:            # TRR
                if _level_id == 2:          # Module
                    for i in range(4, 7):
                        _query = "SELECT SUM(t2.fld_value) \
                                  FROM tbl_software AS t1 \
                                  INNER JOIN tbl_trr AS t2 \
                                  ON t2.fld_software_id=t1.fld_software_id \
                                  WHERE t2.fld_question_id=%d \
                                  AND t1.fld_parent_module='%s'" % (i, _path)
                        _count = self._app.DB.execute_query(_query,
                                                            None,
                                                            self._app.ProgCnx)
                        try:
                            _count = _count[0][0] + 0
                        except TypeError:
                            _count = 0

                        _query = "UPDATE tbl_trr \
                                  SET fld_value=%d \
                                  WHERE fld_software_id=%d \
                                  AND fld_question_id=%d" % \
                                 (_count, _software_id, i - 3)
                        self._app.DB.execute_query(_query,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

                        # Update the lines of code counts in the gtk.TreeView()
                        # and the open RTK program database.
                        if i == 4:
                            _loc = _count
                        elif i == 5:
                            _aloc = _count

                        _hloc = _loc - _aloc

                elif _level_id == 3:        # Unit
                    # All we have at the unit level is the lines of code in
                    # the unit.
                    for i in range(4, 7):
                        _query = "SELECT fld_value \
                                  FROM tbl_trr \
                                  WHERE fld_software_id=%d \
                                  AND fld_question_id=%d" % (_software_id, i)
                        _count = self._app.DB.execute_query(_query,
                                                            None,
                                                            self._app.ProgCnx)

                        if i == 4:
                            _loc = _count[0][0]
                        elif i == 5:
                            _aloc = _count[0][0]

                        _hloc = _loc - _aloc

            # Update the Software class gtk.TreeView().
            model.set_value(row, 17, _hloc)
            model.set_value(row, 18, _aloc)
            model.set_value(row, 19, _loc)
            model.set_value(row, 24, _nm)

            # Update the open RTK program database.
            _query = "UPDATE tbl_software \
                      SET fld_hloc=%d, fld_aloc=%d, fld_loc=%d, fld_nm=%d \
                      WHERE fld_software_id=%d" % \
                     (_hloc, _aloc, _loc, _nm, _software_id)
            self._app.DB.execute_query(_query,
                                       None,
                                       self._app.ProgCnx,
                                       commit=True)

            return False

        def _calculate_risk(model, __path, row, self):
            """
            Function to calculate the Software class risk levels.  The
            algorithms used are based on the methodology presented in
            RL-TR-92-52, "SOFTWARE RELIABILITY, MEASUREMENT, AND TESTING
            Guidebook for Software Reliability Measurement and Testing."
            Rather than attempting to estimate the software failure rate, RTK
            provides a risk index for the software based on the same factors
            used in RL-TR-92-52 for estimating software failure rates.  RTK
            also provides test planning guidance in a similar manner as
            RL-TR-92-52.

            :param model: the Software class gtk.TreeModel().
            :type model: gtk.TreeModel
            :param __path: the path of the selected row in the Software class
                           gtk.TreeView().
            :type __path: string
            :param row: the gtk.Iter() in the Software class gtk.TreeView() for
                        which to calculate the risk.
            :type row: gtk.Iter
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _A = 0.0
            _D = 0.0
            _SA = 0.0
            _ST = 0.0
            _SQ = 0.0
            _SL = 0.0
            _SX = 0.0
            _SM = 0.0

            _software_id = model.get_value(row, 1)
            _level_id = model.get_value(row, 2)
            _phase_id = model.get_value(row, 36)

            if _phase_id == 2 and _level_id == 2:
                (_A, _D) = _calculate_development_risk(model, row,
                                                       self._dic_dev_env)
                (_SA, _ST, _SQ) = _calculate_srr_risk(model, row, self._dic_srr)
                _rpfom = _A * _D * _SA * _ST * _SQ
            elif _phase_id == 3 and _level_id == 2:
                (_A, _D) = _calculate_development_risk(model, row,
                                                       self._dic_dev_env)
                (_SA, _ST, _SQ) = _calculate_pdr_risk(model, row, self._dic_pdr)
                _rpfom = _A * _D * _SA * _ST * _SQ
            elif _phase_id == 4 and _level_id > 1:
                (_A, _D) = _calculate_development_risk(model, row,
                                                       self._dic_dev_env)
                (_SA, _ST, _SQ) = _calculate_cdr_risk(model, row, self._dic_cdr)
            elif _phase_id == 5 and _level_id > 1:
                (_A, _D) = _calculate_development_risk(model, row,
                                                       self._dic_dev_env)
                (_SA, _SQ, _SL, _SX, _SM) = _calculate_trr_risk(model, row,
                                                                self._dic_trr)
                _rpfom = _A * _D * _SA * _SQ * _SL * _SX * _SM
            else:
                (_A, _D) = _calculate_development_risk(model, row,
                                                       self._dic_dev_env)
                _rpfom = _A * _D

            self._dic_risk[_software_id][0] = _A
            self._dic_risk[_software_id][1] = _D
            self._dic_risk[_software_id][2] = _SA
            self._dic_risk[_software_id][3] = _ST
            self._dic_risk[_software_id][4] = _SQ
            self._dic_risk[_software_id][5] = _SL
            self._dic_risk[_software_id][6] = _SX
            self._dic_risk[_software_id][7] = _SM
            self._dic_risk[_software_id][8] = _rpfom

            model.set_value(row, self._col_order[6], _A)
            model.set_value(row, self._col_order[10], _D)
            model.set_value(row, self._col_order[12], _SA)
            model.set_value(row, self._col_order[13], _ST)
            model.set_value(row, self._col_order[15], _SQ)
            model.set_value(row, self._col_order[20], _SL)
            model.set_value(row, self._col_order[25], _SX)
            model.set_value(row, self._col_order[29], _SM)
            model.set_value(row, self._col_order[33], _rpfom)

            return False

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        _model = self.treeview.get_model()

        # Calculate risk factors for each row.
        _model.foreach(_count_units, self)
        _model.foreach(_calculate_risk, self)

        # Find the overall system-level risk.
        _row = _model.get_iter_root()
        _rpfom = sum([_v[8] for _v in self._dic_risk.values()]) / \
                 float(len(self._dic_risk.values()))    # noqa

        self._dic_risk[_model.get_value(_row, 1)][8] = _rpfom
        _model.set_value(_row, self._col_order[33], _rpfom)

        # Update the risk map.
        _model = self.tvwRiskMap.get_model()
        _model.foreach(self._update_risk_map)

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _calculate_risk_reduction(self):
        """
        Method to calculate the risk reduction due to testing.  The algorithms
        used are based on the methodology presented in RL-TR-92-52, "SOFTWARE
        RELIABILITY, MEASUREMENT, AND TESTING Guidebook for Software
        Reliability Measurement and Testing."  Rather than attempting to
        estimate the software failure rate, RTK provides a risk index for the
        software based on the same factors used in RL-TR-92-52 for estimating
        software failure rates.  RTK also provides test planning guidance in
        the same manner as RL-TR-92-52.

        :return: the reliability risk reduction factor.
        :rtype: float
        """

        # Calculate the risk reduction due to the test effort.
        if self.cmbTestEffort.get_active() == 1:    # Labor hours
            _test_effort = float(self.txtLaborTest.get_text())
            _total_effort = float(self.txtLaborDev.get_text())
        elif self.cmbTestEffort.get_active() == 2:  # Budget
            _test_effort = float(self.txtBudgetTest.get_text())
            _total_effort = float(self.txtBudgetDev.get_text())
        elif self.cmbTestEffort.get_active() == 3:  # Schedule
            _test_effort = float(self.txtScheduleTest.get_text())
            _total_effort = float(self.txtScheduleDev.get_text())

        _c = _test_effort / _total_effort
        _TE = 0.4 / _c
        if _test_effort / _total_effort > 0.4:
            _TE = 0.9

        # Calculate the risk reduction due to test methods used.
        _TU = 1.0
        _TT = 1.0
        _TM = 1.0
        if _TU / _TT > 0.75:
            _TM = 0.9
        elif _TU / _TT < 0.5:
            _TM = 1.1

        # Calculate the risk reduction due to test coverage.
        _TP = int(self.txtBranches.get_text())
        _PT = int(self.txtBranchesTest.get_text())
        _TI = int(self.txtInputs.get_text())
        _IT = int(self.txtInputsTest.get_text())
        _NM = int(self.txtUnits.get_text())
        _MT = int(self.txtUnitsTest.get_text())
        _TC = int(self.txtInterfaces.get_text())
        _CT = int(self.txtInterfacesTest.get_text())

        if self.level_id == 2:        # Module
            _VS = ((_MT / _NM) + (_CT / _TC)) / 2.0
        elif self.level_id == 3:      # Unit
            _VS = ((_PT / _TP) + (_IT / _TI)) / 2.0
        _TC = 1.0 / _VS

        self._dic_risk['TE'] = _TE
        self._dic_risk['TM'] = _TM
        self._dic_risk['TC'] = _TC

        return _TE * _TM * _TC
