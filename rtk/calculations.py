#!/usr/bin/env python2
"""
This module contains various calculations used by the RTK Project.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       calculations.py is part of The RTK Project
#
# All rights reserved.

import gettext
import sys

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

# Add NLS support.
_ = gettext.gettext

# Import R library.
try:
    from rpy2 import robjects
    from rpy2.robjects import r as R
    from rpy2.robjects.packages import importr
    import rpy2.rlike.container as rlc
    import rpy2.rinterface as ri
    __USE_RPY__ = False
    __USE_RPY2__ = True
except ImportError:
    __USE_RPY__ = False
    __USE_RPY2__ = False

import numpy as np
from math import ceil, exp, log, sqrt

import configuration as _conf
import utilities as _util


def calculate_part(model):
    """
    Calculates the hazard rate for a component.

    :param model: the component's h(t) prediction model and the input
                  variables.  The keys are the model variables and the values
                  are the values of the variable in the key.
    :type model: dictionary
    :return: _lambdap, the calculated h(t).
    :rtype: float
    """

    _keys = model.keys()
    _values = model.values()

    for i in range(len(_keys)):
        vars()[_keys[i]] = _values[i]

    _lambdap = eval(model['equation'])

    return _lambdap


def overstressed(partmodel, partrow, systemmodel, systemrow):
    """
    Determines whether the component is overstressed based on derating
    rules.

    Currently only default derating rules from Reliability Toolkit:
    Commercial Practices Edition, Section 6.3.3 are used.

    +------------+----------------------------+-------------------+
    | Component  |                            |    Environment    |
    |   Type     |     Derating Parameter     | Severe  | Benign  |
    +============+============================+=========+=========+
    | Capacitor  | DC Voltage                 |   60%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Temp from Max Limit        |   10C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Circuit Bkr| Current                    |   80%   |   80%   |
    +------------+----------------------------+---------+---------+
    | Connectors | Voltage                    |   70%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Current                    |   70%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Insert Temp from Max Limit |   25C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Diodes     | Power Dissipation          |   70%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Max Junction Temperature   |  125C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Fiber      | Bend Radius                |  200%   |  200%   |
    | Optics     +----------------------------+---------+---------+
    |            | Cable Tension              |   50%   |   50%   |
    +------------+----------------------------+---------+---------+
    | Fuses      | Current (Maximum           |   50%   |   70%   |
    |            +----------------------------+---------+---------+
    |            | Capability)                |         |         |
    +------------+----------------------------+---------+---------+
    | Inductors  | Operating Current          |   60%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Dielectric Voltage         |   50%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Temp from Hot Spot         |   15C   |         |
    +------------+----------------------------+---------+---------+
    | Lamps      | Voltage                    |   94%   |   94%   |
    +------------+----------------------------+---------+---------+
    | Memories   | Supply Voltage             |  +/-5%  |  +/-5%  |
    |            +----------------------------+---------+---------+
    |            | Output Current             |   80%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Max Junction Temp          |  125C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Micro      | Supply Voltage             |  +/-5%  |  +/-5%  |
    | circuits   +----------------------------+---------+---------+
    |            | Fan Out                    |   80%   |   80%   |
    |            +----------------------------+---------+---------+
    |            | Max Junction Temp          |  125C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | GaAs Micro | Max Junction Temp          |  135C   |   N/A   |
    | circuits   +----------------------------+---------+---------+
    +------------+----------------------------+---------+---------+
    | Micro      | Supply Voltage             |  +/-5%  |  +/-5%  |
    | processors +----------------------------+---------+---------+
    |            | Fan Out                    |   80%   |   80%   |
    |            +----------------------------+---------+---------+
    |            | Max Junction Temp          |  125C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Photo      | Reverse Voltage            |   70%   |    70%  |
    | diode      +----------------------------+---------+---------+
    |            | Max Junction Temp          |  125C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Photo      | Max Junction Temp          |  125C   |   N/A   |
    | transistor |                            |         |         |
    +------------+----------------------------+---------+---------+
    | Relays     | Resistive Load Current     |   75%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Capacitive Load Current    |   75%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Inductive Load Current     |   40%   |   50%   |
    |            +----------------------------+---------+---------+
    |            | Contact Power              |   50%   |   60%   |
    +------------+----------------------------+---------+---------+
    | Resistors  | Power Dissipation          |   50%   |   80%   |
    |            +----------------------------+---------+---------+
    |            | Temp from Max Limit        |   30C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Transistor,| Power Dissipation          |   70%   |   90%   |
    | Silicon    +----------------------------+---------+---------+
    |            | Breakdown Voltage          |   75%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Max Junction Temp          |  125C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Transistor,| Power Dissipation          |   70%   |   90%   |
    | GaAs       +----------------------------+---------+---------+
    |            | Breakdown Voltage          |   70%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Max Junction Temp          |  135C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Thyristors | On-State Current           |   70%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Off-State Voltage          |   70%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Max Junction Temp          |  125C   |   N/A   |
    +------------+----------------------------+---------+---------+
    | Switches   | Resistive Load Current     |   75%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Capacitive Load Current    |   75%   |   90%   |
    |            +----------------------------+---------+---------+
    |            | Inductive Load Current     |   40%   |   50%   |
    |            +----------------------------+---------+---------+
    |            | Contact Power              |   50%   |   60%   |
    +------------+----------------------------+---------+---------+

    :param partmodel: the winParts full gtk.TreeModel().
    :type partmodel: gtk.TreeModel
    :param partrow: the currently selected gtk.TreeIter() in the winParts full
                    gtk.TreeModel().
    :type partrow: gtk.TreeIter
    :param systemmodel: the Hardware class gtk.TreeModel().
    :type systemmodel: gtk.TreeModel
    :param systemrow: the currently selected gtk.TreeIter() in the Hardware
                      class gtk.TreeModel().
    :type systemrow: gtk.TreeIter
    """

    # |------------------  <---- Knee Temperature
    # |                  \
    # |                   \
    # |                    \
    # |                     \  <---- Maximum Temperature
    # +------------------------
    overstress = False
    reason = ""
    r_index = 1
    harsh = True

    Eidx = systemmodel.get_value(systemrow, 22)
    Tknee = partmodel.get_value(partrow, 43)
    Tmax = partmodel.get_value(partrow, 55)
    Tmin = partmodel.get_value(partrow, 56)

    category = systemmodel.get_value(systemrow, 11)
    subcategory = systemmodel.get_value(systemrow, 78)

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if Eidx == 1 or Eidx == 2 or Eidx == 4 or Eidx == 11:
        harsh = False

    if category == 1:                       # Capacitor
        Voper = partmodel.get_value(partrow, 66)
        Vrate = partmodel.get_value(partrow, 94)
        Toper = systemmodel.get_value(systemrow, 80)

        if harsh:
            if Voper > 0.60 * Vrate:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 60% " \
                                                 "rated voltage.\n"
                r_index += 1
            if Tmax - Toper <= 10.0:
                overstress = True
                reason = reason + str(r_index) + ". Operating temperature " \
                                                 "within 10.0C of maximum " \
                                                 "rated temperature.\n"
                r_index += 1
        else:
            if Voper > 0.90 * Vrate:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 90% " \
                                                 "rated voltage.\n"
                r_index += 1

    elif category == 2:                     # Connection
        Tmax = partmodel.get_value(partrow, 55)
        Ioper = partmodel.get_value(partrow, 62)
        Voper = partmodel.get_value(partrow, 66)
        Irate = partmodel.get_value(partrow, 92)
        Vrate = partmodel.get_value(partrow, 94)
        Trise = partmodel.get_value(partrow, 107)
        Toper = partmodel.get_value(partrow, 80)

        if harsh:
            if Voper > 0.7 * Vrate:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 70% " \
                                                 "rated voltage.\n"
                r_index += 1
            if Ioper > 0.7 * Irate:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 70% " \
                                                 "rated current.\n"
                r_index += 1
            if (Trise + Toper - Tmax) < 25:
                overstress = True
                reason = reason + str(r_index) + ". Operating temperature " \
                                                 "within 25.0C of maximum " \
                                                 "rated temperature.\n"
                r_index += 1
        else:
            if Voper > 0.9 * Vrate:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 90% " \
                                                 "rated voltage.\n"
                r_index += 1
            if Ioper > 0.9 * Irate:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 90% " \
                                                 "rated current.\n"
                r_index += 1

    elif category == 3:                    # Inductive Device
        Ths = partmodel.get_value(partrow, 39)
        Ioper = partmodel.get_value(partrow, 62)
        Voper = partmodel.get_value(partrow, 66)
        Irate = partmodel.get_value(partrow, 92)
        Vrate = partmodel.get_value(partrow, 94)
        Toper = partmodel.get_value(partrow, 105)

        if harsh:
            if Ioper > 0.60 * Irate:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 60% " \
                                                 "rated current.\n"
                r_index += 1
            if Voper > 0.50 * Vrate:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 50% " \
                                                 "rated voltage.\n"
                r_index += 1
            if Ths - Toper < 15.0:
                overstress = True
                reason = reason + str(r_index) + ". Operating temperature " \
                                                 "within 15.0C of maximum " \
                                                 "rated temperature.\n"
                r_index += 1
        else:
            if Ioper > 0.90 * Irate:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 90% " \
                                                 "rated current.\n"
                r_index += 1
            if Voper > 0.90 * Vrate:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 90% " \
                                                 "rated voltage.\n"
                r_index += 1

    elif category == 4:                     # Integrated Circuit
        Tjunc = partmodel.get_value(partrow, 39)
        Ioper = partmodel.get_value(partrow, 62)
        Voper = partmodel.get_value(partrow, 66)
        Irate = partmodel.get_value(partrow, 92)
        Vrate = partmodel.get_value(partrow, 94)

        if subcategory < 3:                # GaAs
            if harsh:
                if Tjunc > 135.0:
                    overstress = True
                    reason = reason + str(r_index) + ". Junction temperature " \
                                                     "> 135.0C.\n"
                    r_index += 1
        else:
            if harsh:
                if Voper > 1.05 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > " \
                                                     "105% rated voltage.\n"
                    r_index += 1
                if Voper < 0.95 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage < " \
                                                     "95% rated voltage.\n"
                    r_index += 1
                if Ioper > 0.80 * Irate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > " \
                                                     "80% rated current.\n"
                    r_index += 1
                if Tjunc > 125.0:
                    overstress = True
                    reason = reason + str(r_index) + ". Junction temperature " \
                                                     "> 125.0C.\n"
                    r_index += 1
            else:
                if Voper > 1.05 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > " \
                                                     "105% rated voltage.\n"
                    r_index += 1
                if Voper < 0.95 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage < " \
                                                     "95% rated voltage.\n"
                    r_index += 1
                if Ioper > 0.90 * Irate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > " \
                                                     "90% rated current.\n"
                    r_index += 1

    elif category == 6:                    # Miscellaneous
        if subcategory == 80:              # Crystal
            print "Bug #113: No overstress calculations for crystals."
        elif subcategory == 81:            # Lamps
            Voper = partmodel.get_value(partrow, 66)
            Vrated = partmodel.get_value(partrow, 94)
            if Voper >= 0.94 * Vrated:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 94% " \
                                                 "rated voltage.\n"
                r_index += 1
        elif subcategory == 82:            # Fuse
            print "Bug #114: No overstress calculations for fuses."
        elif subcategory == 83:            # Filter
            print "Bug #115: No overstress calculations for filters."

    elif category == 7:                    # Relay
        Aidx = partmodel.get_value(partrow, 30)
        Ioper = partmodel.get_value(partrow, 62)
        Irated = partmodel.get_value(partrow, 92)

        if harsh:
            if Aidx == 1 and Ioper > 0.75 * Irated:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 75% " \
                                                 "rated current.\n"
                r_index += 1
            elif Aidx == 2 and Ioper > 0.75 * Irated:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 75% " \
                                                 "rated current.\n"
                r_index += 1
            elif Aidx == 3 and Ioper > 0.40 * Irated:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 40% " \
                                                 "rated current.\n"
                r_index += 1
        else:
            if Aidx == 1 and Ioper > 0.90 * Irated:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 90% " \
                                                 "rated current.\n"
                r_index += 1
            elif Aidx == 2 and Ioper > 0.90 * Irated:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 90% " \
                                                 "rated current.\n"
                r_index += 1
            elif Aidx == 3 and Ioper > 0.50 * Irated:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 50% " \
                                                 "rated current.\n"
                r_index += 1

    elif category == 8:                    # Resistor
        Poper = partmodel.get_value(partrow, 64)
        Prated = partmodel.get_value(partrow, 93)

        if harsh:
            if Poper > 0.5 * Prated:
                overstress = True
                reason = reason + str(r_index) + ". Operating power > 50% " \
                                                 "rated power.\n"
                r_index += 1
        else:
            if Poper > 0.8 * Prated:
                overstress = True
                reason = reason + str(r_index) + ". Operating power > 80% " \
                                                 "rated power.\n"
                r_index += 1

    elif category == 9:                    # Semiconductor
        Tjunc = partmodel.get_value(partrow, 39)
        Ioper = partmodel.get_value(partrow, 62)
        Poper = partmodel.get_value(partrow, 64)
        Voper = partmodel.get_value(partrow, 66)
        Irate = partmodel.get_value(partrow, 92)
        Prate = partmodel.get_value(partrow, 93)
        Vrate = partmodel.get_value(partrow, 94)

        if subcategory == 1 or subcategory == 2:    # Diodes
            if harsh:
                if Poper > 0.7 * Prate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > " \
                                                     "70% rated power.\n"
                    r_index += 1
                if Tjunc > 125.0:
                    overstress = True
                    reason = reason + str(r_index) + ". Junction " \
                                                     "temperature > 125.0C.\n"
                    r_index += 1
            else:
                if Poper > 0.9 * Prate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power " \
                                                     "> 90% rated power.\n"
                    r_index += 1

        elif subcategory > 2 and subcategory < 6:    # Optoelectronics
            if Voper > 0.70 * Vrate:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 70% " \
                                                 "rated voltage.\n"
                r_index += 1
            if Tjunc > 125.0:
                overstress = True
                reason = reason + str(r_index) + ". Junction temperature > " \
                                                 "125.0C.\n"
                r_index += 1

        elif subcategory == 6:             # Thyristor
            if harsh:
                if Ioper > 0.70 * Irate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > " \
                                                     "70% rated current.\n"
                    r_index += 1
                if Voper > 0.70 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > " \
                                                     "70% rated voltage.\n"
                    r_index += 1
                if Tjunc > 125.0:
                    overstress = True
                    reason = reason + str(r_index) + ". Junction " \
                                                     "temperature > 125.0C.\n"
                    r_index += 1
            else:
                if Ioper > 0.90 * Irate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > " \
                                                     "90% rated current.\n"
                    r_index += 1
                if Voper > 0.90 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > " \
                                                     "90% rated voltage.\n"
                    r_index += 1

        elif subcategory == 7:             # GaAs transistor
            if harsh:
                if Poper > 0.70 * Prate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > " \
                                                     "70% rated power.\n"
                    r_index += 1
                if Voper > 0.70 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage " \
                                                     "> 70% rated voltage.\n"
                    r_index += 1
                if Tjunc > 135.0:
                    overstress = True
                    reason = reason + str(r_index) + ". Junction " \
                                                     "temperature > 125.0C.\n"
                    r_index += 1
            else:
                if Poper > 0.90 * Prate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > " \
                                                     "90% rated power.\n"
                    r_index += 1
                if Voper > 0.90 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > " \
                                                     "90% rated voltage.\n"
                    r_index += 1

        elif subcategory > 7:              # Silicon transistor
            if harsh:
                if Poper > 0.70 * Prate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > " \
                                                     "70% rated power.\n"
                    r_index += 1
                if Voper > 0.75 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > " \
                                                     "70% rated voltage.\n"
                    r_index += 1
                if Tjunc > 125.0:
                    overstress = True
                    reason = reason + str(r_index) + ". Junction " \
                                                     "temperature > 125.0C.\n"
                    r_index += 1
            else:
                if Poper > 0.90 * Prate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating power > " \
                                                     "90% rated power.\n"
                    r_index += 1
                if Voper > 0.90 * Vrate:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating voltage > " \
                                                     "90% rated voltage.\n"
                    r_index += 1

    elif category == 10:                   # Switching Device
        Aidx = partmodel.get_value(partrow, 5)
        Ioper = partmodel.get_value(partrow, 62)
        Irated = partmodel.get_value(partrow, 92)

        if subcategory == 71:              # Circuit Breaker
            if Ioper > 0.8 * Irated:
                overstress = True
                reason = reason + str(r_index) + ". Operating current > 80% " \
                                                 "rated current.\n"
                r_index += 1

        else:
            if harsh:
                if Aidx == 1 and Ioper > 0.75 * Irated:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current " \
                                                     "> 75% rated current.\n"
                    r_index += 1
                elif Aidx == 2 and Ioper > 0.75 * Irated:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > " \
                                                     "75% rated current.\n"
                    r_index += 1
                elif Aidx == 3 and Ioper > 0.40 * Irated:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current > " \
                                                     "40% rated current.\n"
                    r_index += 1
            else:
                if Aidx == 1 and Ioper > 0.90 * Irated:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current " \
                                                     "> 90% rated current.\n"
                    r_index += 1
                elif Aidx == 2 and Ioper > 0.90 * Irated:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current " \
                                                     "> 90% rated current.\n"
                    r_index += 1
                elif Aidx == 3 and Ioper > 0.50 * Irated:
                    overstress = True
                    reason = reason + str(r_index) + ". Operating current " \
                                                     "> 50% rated current.\n"
                    r_index += 1

    return overstress, reason


def similar_hazard_rate(component, new_qual, new_environ, new_temp):
    """
    Calculates the estimated hazard rate of a similar item based on
    differences in quality level, environment, and operating temperature.

    All conversion factors come from Reliability Toolkit: Commercial Practices
    Edition, Section 6.3.3.

    To convert from quality A to quality B use conversion factors from
    Table 6.3.3-1 (reproduced below).

    +-------------+-----------+-----------+-----------+-----------+
    | Quality     |           | Full      |           |           |
    | Level       |   Space   | Military  | Ruggedized| Commercial|
    +=============+===========+===========+===========+===========+
    | Space       |    1.0    |    0.8    |    0.5    |    0.2    |
    +-------------+-----------+-----------+-----------+-----------+
    | Full        |    1.3    |    1.0    |    0.6    |    0.3    |
    | Military    |           |           |           |           |
    +-------------+-----------+-----------+-----------+-----------+
    | Ruggedized  |    2.0    |    1.7    |    1.0    |    0.4    |
    +-------------+-----------+-----------+-----------+-----------+
    | Commercial  |    5.0    |    3.3    |    2.5    |    1.0    |
    +-------------+-----------+-----------+-----------+-----------+

    To convert from environment A to environment B use the conversion
    factors from Table 6.3.3-2 (reproduced below).

    +-------------+-------+-------+-------+-------+-------+-------+
    | Environment |  GB   |  GM   |  NS   |  AIC  |  ARW  |  SF   |
    +=============+=======+=======+=======+=======+=======+=======+
    | GB          |  1.0  |  0.2  |  0.3  |  0.3  |  0.1  |  1.1  |
    +-------------+-------+-------+-------+-------+-------+-------+
    | GM          |  5.0  |  1.0  |  1.4  |  1.4  |  0.5  |  5.0  |
    +-------------+-------+-------+-------+-------+-------+-------+
    | NS          |  3.3  |  0.7  |  1.0  |  1.0  |  0.3  |  3.3  |
    +-------------+-------+-------+-------+-------+-------+-------+
    | AIC         |  3.3  |  0.7  |  1.0  |  1.0  |  0.3  |  3.3  |
    +-------------+-------+-------+-------+-------+-------+-------+
    | ARW         | 10.0  |  2.0  |  3.3  |  3.3  |  1.0  | 10.0  |
    +-------------+-------+-------+-------+-------+-------+-------+
    | SF          |  0.9  |  0.2  |  0.3  |  0.3  |  0.1  |  1.0  |
    +-------------+-------+-------+-------+-------+-------+-------+

    To convert from temperature A to temperature B (both in Celcius) use
    conversion factors from Table 6.3.3-3 (reproduced below).

    +------------+------+------+------+------+------+------+------+
    | Temperature| 10 C | 20 C | 30 C | 40 C | 50 C | 60 C | 70 C |
    +============+======+======+======+======+======+======+======+
    | 10 C       |  1.0 |  0.9 |  0.8 |  0.8 |  0.7 |  0.5 |  0.4 |
    +------------+------+------+------+------+------+------+------+
    | 20 C       |  1.1 |  1.0 |  0.9 |  0.8 |  0.7 |  0.6 |  0.5 |
    +------------+------+------+------+------+------+------+------+
    | 30 C       |  1.2 |  1.1 |  1.0 |  0.9 |  0.8 |  0.6 |  0.5 |
    +------------+------+------+------+------+------+------+------+
    | 40 C       |  1.3 |  1.2 |  1.1 |  1.0 |  0.9 |  0.7 |  0.6 |
    +------------+------+------+------+------+------+------+------+
    | 50 C       |  1.5 |  1.4 |  1.2 |  1.1 |  1.0 |  0.8 |  0.7 |
    +------------+------+------+------+------+------+------+------+
    | 60 C       |  1.9 |  1.7 |  1.6 |  1.5 |  1.2 |  1.0 |  0.8 |
    +------------+------+------+------+------+------+------+------+
    | 70 C       |  2.4 |  2.2 |  1.9 |  1.8 |  1.5 |  1.2 |  1.0 |
    +------------+------+------+------+------+------+------+------+

    :param component: the rtk.Component() class to perform calculations on.
    :type component: rtk.Component
    :param new_qual: the index of the quality level of the new item.
    :type new_qual: integer
    :param new_environ: the index of the environment of the new item.
    :type new_environ: integer
    :param new_temp: the index of the operating temperature of the new item.
    :type new_temp: integer
    :return: hr_similar; the estimated hazard rate for the new item.
    :rtype: float
    """

    qual_factor = [[1.0, 0.8, 0.5, 0.2],
                   [1.3, 1.0, 0.6, 0.3],
                   [2.0, 1.7, 1.0, 0.4],
                   [5.0, 3.3, 2.5, 1.0],
                   [1.0, 1.0, 1.0, 1.0]]

    if component.model.get_value(component.selected_row, 85) == 1:
        base_qual = 0
    elif component.model.get_value(component.selected_row, 85) == 2:
        base_qual = 1
    elif component.model.get_value(component.selected_row, 85) == 3:
        base_qual = 2
    elif component.model.get_value(component.selected_row, 85) == 4:
        base_qual = 3
    else:
        base_qual = 4

    quality = qual_factor[base_qual][new_qual]

    environ_factor = [[1.0, 0.2, 0.3, 0.3, 0.1, 1.1],
                      [5.0, 1.0, 1.4, 1.4, 0.5, 5.0],
                      [3.3, 0.7, 1.0, 1.0, 0.3, 3.3],
                      [3.3, 0.7, 1.0, 1.0, 0.3, 3.3],
                      [10.0, 2.0, 3.3, 3.3, 1.0, 10.0],
                      [0.9, 0.2, 0.3, 0.3, 0.1, 1.0],
                      [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]

    if component.system_model.get_value(
            component.system_selected_row, 22) == 1:
        base_environ = 0
    elif component.system_model.get_value(
            component.system_selected_row, 22) == 3:
        base_environ = 1
    elif component.system_model.get_value(
            component.system_selected_row, 22) == 4:
        base_environ = 2
    elif component.system_model.get_value(
            component.system_selected_row, 22) == 6:
        base_environ = 3
    elif component.system_model.get_value(
            component.system_selected_row, 22) == 10:
        base_environ = 4
    elif component.system_model.get_value(
            component.system_selected_row, 22) == 11:
        base_environ = 5
    else:
        base_environ = 6

    environ = environ_factor[base_environ][new_environ]

    temp_factor = [[1.0, 0.9, 0.8, 0.8, 0.7, 0.5, 0.4],
                   [1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
                   [1.2, 1.1, 1.0, 0.9, 0.8, 0.6, 0.5],
                   [1.3, 1.2, 1.1, 1.0, 0.9, 0.7, 0.6],
                   [1.5, 1.4, 1.2, 1.1, 1.0, 0.8, 0.7],
                   [1.9, 1.7, 1.6, 1.5, 1.2, 1.0, 0.8],
                   [2.4, 2.2, 1.9, 1.8, 1.5, 1.2, 1.0]]

    base_temp = component.system_model.get_value(
        component.system_selected_row, 80)
    temp = temp_factor[base_temp][new_temp]

    hr_similar = 1.0 / ((1.0 / component.system_model.get_value(
        component.system_selected_row, 28)) * quality * environ * temp)

    return hr_similar


def dormant_hazard_rate(category, subcategory, active_env, dormant_env,
                        lambdaa):
    """
    Calculates the dormant hazard rate based on active environment, dormant
    environment, and component category.

    All conversion factors come from Reliability Toolkit: Commercial
    Practices Edition, Section 6.3.4, Table 6.3.4-1 (reproduced below).

    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Component   |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
    | Category    |Active |Active  |Active  |Active |Active |Active |Active |
    |             |to     |to      |to      |to     |to     |to     |to     |
    |             |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
    |             |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
    +=============+=======+========+========+=======+=======+=======+=======+
    | Integrated  | 0.08  |  0.06  |  0.04  | 0.06  | 0.05  | 0.10  | 0.30  |
    | Circuits    |       |        |        |       |       |       |       |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Diodes      | 0.04  |  0.05  |  0.01  | 0.04  | 0.03  | 0.20  | 0.80  |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Transistors | 0.05  |  0.06  |  0.02  | 0.05  | 0.03  | 0.20  | 1.00  |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Capacitors  | 0.10  |  0.10  |  0.03  | 0.10  | 0.04  | 0.20  | 0.40  |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Resistors   | 0.20  |  0.06  |  0.03  | 0.10  | 0.06  | 0.50  | 1.00  |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Switches    | 0.40  |  0.20  |  0.10  | 0.40  | 0.20  | 0.80  | 1.00  |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Relays      | 0.20  |  0.20  |  0.04  | 0.30  | 0.08  | 0.40  | 0.90  |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Connectors  | 0.005 |  0.005 |  0.003 | 0.008 | 0.003 | 0.02  | 0.03  |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Circuit     | 0.04  |  0.02  |  0.01  | 0.03  | 0.01  | 0.08  | 0.20  |
    | Boards      |       |        |        |       |       |       |       |
    +-------------+-------+--------+--------+-------+-------+-------+-------+
    | Transformers| 0.20  |  0.20  |  0.20  | 0.30  | 0.30  | 0.50  | 1.00  |
    +-------------+-------+--------+--------+-------+-------+-------+-------+

    :param category: the component category index.
    :type category: integer
    :param subcategory: the component subcategory index.
    :type subcategory: integer
    :param active_env: the active environment index.
    :type active_env: integer
    :param dormant_env: the dormant environment index.
    :type dormant_env: integer
    :param lambdaa: the active hazard rate of the component.
    :type lambdaa: float
    :return: lambdad; the dormant hazard rate.
    :rtype: float
    """

    factor = [[0.08, 0.06, 0.04, 0.06, 0.05, 0.10, 0.30, 0.00],
              [0.04, 0.05, 0.01, 0.04, 0.03, 0.20, 0.80, 0.00],
              [0.05, 0.06, 0.02, 0.05, 0.03, 0.20, 1.00, 0.00],
              [0.10, 0.10, 0.03, 0.10, 0.04, 0.20, 0.40, 0.00],
              [0.20, 0.06, 0.03, 0.10, 0.06, 0.50, 1.00, 0.00],
              [0.40, 0.20, 0.10, 0.40, 0.20, 0.80, 1.00, 0.00],
              [0.20, 0.20, 0.04, 0.30, 0.08, 0.40, 0.90, 0.00],
              [0.005, 0.005, 0.003, 0.008, 0.003, 0.02, 0.03, 0.00],
              [0.04, 0.02, 0.01, 0.03, 0.01, 0.08, 0.20, 0.00],
              [0.20, 0.20, 0.20, 0.30, 0.30, 0.50, 1.00, 0.00]]

    # First find the component category/subcategory index.
    if category == 1:                       # Capacitor
        c_index = 3
    elif category == 2:                     # Connection
        c_index = 7
    elif category == 3:                     # Inductive Device.
        if subcategory > 1:                 # Transformer
            c_index = 9
    elif category == 4:                     # Integrated Circuit
        c_index = 0
    elif category == 7:                     # Relay
        c_index = 6
    elif category == 8:                     # Resistor
        c_index = 4
    elif category == 9:                     # Semiconductor
        if subcategory > 0 and subcategory < 7:     # Diode
            c_index = 1
        elif subcategory > 6 and subcategory < 14:  # Transistor
            c_index = 2
    elif category == 10:                    # Switching Device
        c_index = 5

    # Now find the appropriate active to passive environment index.
    if active_env > 0 and active_env < 4:   # Ground
        if dormant_env == 1:                # Ground
            e_index = 0
        else:
            e_index = 7
    elif active_env > 3 and active_env < 6:         # Naval
        if dormant_env == 1:                # Ground
            e_index = 4
        elif dormant_env == 2:              # Naval
            e_index = 3
        else:
            e_index = 7
    elif active_env > 5 and active_env < 11:        # Airborne
        if dormant_env == 1:                # Ground
            e_index = 2
        elif dormant_env == 3:              # Airborne
            e_index = 1
        else:
            e_index = 7
    elif active_env == 11:                  # Space
        if dormant_env == 1:                # Ground
            e_index = 6
        elif dormant_env == 4:              # Space
            e_index = 5
        else:
            e_index = 7

    try:
        lambdad = lambdaa * factor[c_index - 1][e_index]
    except IndexError:
        lambdad = 0.0

    return lambdad


def criticality_analysis(modeca, itemca, rpn):
    """
    Function to perform criticality calculations for FMECA.

    :param modeca: list containing inputs for the MIL-STD-1629A mode
                   criticality calculation.
    :type modeca: list of mixed types
    :param itemca: list containing inputs for the MIL-STD-1629A item
                   criticality calculation.
    :type itemca: list of mixed types
    :param rpn: list containing inputs for the automotive criticality
                calculation.
    :type rpn: list of mixed types
    :return: modeca, itemca, rpn
    :rtype: list, list, list
    """

    fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

    _item_crit = u''

    # First, calculate the mode criticality and assign result to position 4.
    # Second, calculate the mode failure rate and assign result to position 5.
    # Third, calculate the item criticality and assign result to position 6.
    _keys = modeca.keys()
    for i in range(len(_keys)):
        modeca[_keys[i]][4] = modeca[_keys[i]][0] * modeca[_keys[i]][1] * \
                              modeca[_keys[i]][2] * modeca[_keys[i]][3]
        modeca[_keys[i]][5] = modeca[_keys[i]][1] * modeca[_keys[i]][2]

    # Now calculate the item criticality in accordance with MIL-STD-1629A.
    _keys = itemca.keys()
    for i in range(len(_keys)):
        _cats = sorted(list(set([j[1] for j in itemca[_keys[i]]])))
        for k in range(len(_cats)):
            _crit = 0.0
            _modes = [j[0] for j in itemca[_keys[i]] if j[1] == _cats[k]]
            for l in range(len(_modes)):
                _crit += modeca[_modes[l]][4]

            if _cats[k] is not None and _cats[k] != '' and \
               _crit is not None and _crit != '':
                _item_crit = _item_crit + _util.none_to_string(_cats[k]) + \
                             ": " + \
                             str(fmt.format(_util.none_to_string(_crit))) + \
                             "\n"

        itemca[_keys[i]].append(_item_crit)

    # now calculate the rpn criticality.
    _keys = rpn.keys()
    for i in range(len(_keys)):
        rpn[_keys[i]][3] = rpn[_keys[i]][0] * rpn[_keys[i]][1] * \
                           rpn[_keys[i]][2]
        rpn[_keys[i]][7] = rpn[_keys[i]][4] * rpn[_keys[i]][5] * \
                           rpn[_keys[i]][6]

    return modeca, itemca, rpn


def beta_bounds(a, m, b, alpha):
    """
    Function to calculate the mean, standard error, and bounds on the mean of
    a beta distribution.  These are the project management estimators, not
    exact calculations.

    :param a: the minimum expected value.
    :type a: float
    :param m: most likely value.
    :type m: float
    :param b: the maximum expected value.
    :type b: float
    :param alpha: the desired confidence level.
    :type alpha: float
    :return: _meanll, _mean, _meanul; the calculated mean and bounds.
    :rtype: tuple of floats
    """

    from scipy.stats import norm            # pylint: disable=E0611

    if alpha < 0.0:
        _util.rtk_information(_(u"Confidence level take a value between 0 and "
                                u"100 inclusive [0, 100].  Please select and "
                                u"appropriate confidence level and try "
                                u"again."))
        return a, m, b, 0.0
    elif alpha > 1.0:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha / 100.0) / 2.0))
    else:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha) / 2.0))

    _mean = (a + 4.0 * m + b) / 6.0
    _sd = (b - a) / 6.0

    _meanll = _mean - _z_norm * _sd
    _meanul = _mean + _z_norm * _sd

    return _meanll, _mean, _meanul, _sd


def calculate_field_ttf(_dates_):
    """
    Function to calculate the time to failure (TTF) of field incidents.

    :param _dates_: tuple containing start and end date for calculating
                    time to failure.
    """

    from datetime import datetime

    _start = datetime(*time.strptime(_dates_[0], "%Y-%m-%d")[0:5]).date()
    _fail = datetime(*time.strptime(_dates_[1], "%Y-%m-%d")[0:5]).date()
    ttf = _fail - _start

    return ttf.days


def smooth_curve(x, y, num):
    """
    Function to produce smoothed plots where there are a small number of data
    points in the original data set.

    :param x: a numpy array of the raw x-values.
    :type x: numpy array
    :param y: a numpy array of the raw y-values.
    :type y: numpy array
    :param num: the number of points to generate.
    :type num: integer
    :return: _new_x, _new_y
    :rtype: list
    """

    from scipy.interpolate import spline    # pylint: disable=E0611

    _error = False
    x=np.array(x)
    y=np.array(y)
    # Create a new set of x values to be used for smoothing the data.  The new
    # x values are in the range of the minimum and maximum x values passed to
    # the function.  The number of new data points between these values is
    # determined by the value of parameter num.
    _new_x = np.linspace(x.min(), x.max(), num)     # pylint: disable=E1101

    # Attempt to create a new set of y values using the original x, original y,
    # and new x values.  If the operation is unsuccessful, create a list of
    # length num the new y, all set to zero.  Also set the error variable to
    # True.
    try:
        _new_y = spline(x, y, _new_x)
    except ValueError:
        _error = True
        _new_y = np.zeros(num)              # pylint: disable=E1101

    _new_x = _new_x.tolist()
    _new_y = _new_y.tolist()

    return _new_x, _new_y, _error


def theoretical_distribution(_data_, _distr_, _para_):
    """
    Function to generate data points from a theoretical distribution with the
    parameters provided.

    :param _data_: data set used to bound the theoretical distribution.
    :type _data_: list of floats
    :param _distr_: the name of the desired theoretical distribution.
    :type _distr_: string
    :param _para_: the parameters of the desired theoretical distribution.
    :type _para_: list of floats
    :return: theop
    :rtype: R object
    """

    Rbase = importr('base')

    # Create the R density and probabilty distribution names.
    ddistname = R.paste('d', _distr_, sep='')
    pdistname = R.paste('p', _distr_, sep='')

    # Calculate the minimum and maximum values for x.
    xminleft = min([i[0] for i in _data_ if i[0] != 'NA'])
    xminright = min([i[1] for i in _data_ if i[1] != 'NA'])
    x_min = min(xminleft, xminright)

    xmaxleft = max([i[0] for i in _data_ if i[0] != 'NA'])
    xmaxright = max([i[1] for i in _data_ if i[1] != 'NA'])
    x_max = max(xmaxleft, xmaxright)

    x_range = x_max - x_min
    x_min = x_min - 0.3 * x_range
    x_max = x_max + 0.3 * x_range

    # Create a list of probabilities for the theoretical distribution with the
    # estimated parameters.
    den = float(len(_data_))
    densfun = R.get(ddistname, mode='function')
    nm = R.names(_para_)
    f = R.formals(densfun)
    args = R.names(f)
    m = R.match(nm, args)
    s = R.seq(x_min, x_max, by=(x_max - x_min) / den)
    theop = Rbase.do_call(pdistname, R.c(R.list(s), _para_))    # pylint: disable=E1101

    return theop
