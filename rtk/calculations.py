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

    @param model: the component's h(t) prediction model and the input
                  variables.  The keys are the model variables and the values
                  are the values of the variable in the key.
    @type model: dictionary
    @return: _lambdap, the calculated h(t).
    @rtype: float
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

      Component  |                            |    Environment    |
        Type     |     Derating Parameter     | Severe  | Benign  |
    -------------+----------------------------+---------+---------+
     Capacitor   | DC Voltage                 |   60%   |   90%   |
                 | Temp from Max Limit        |   10C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Circuit Bkr | Current                    |   80%   |   80%   |
    -------------+----------------------------+---------+---------+
     Connectors  | Voltage                    |   70%   |   90%   |
                 | Current                    |   70%   |   90%   |
                 | Insert Temp from Max Limit |   25C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Diodes      | Power Dissipation          |   70%   |   90%   |
                 | Max Junction Temperature   |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Fiber Optics| Bend Radius                |  200%   |  200%   |
                 | Cable Tension              |   50%   |   50%   |
    -------------+----------------------------+---------+---------+
     Fuses       | Current (Maximum           |   50%   |   70%   |
                 | Capability)                |         |         |
    -------------+----------------------------+---------+---------+
     Inductors   | Operating Current          |   60%   |   90%   |
                 | Dielectric Voltage         |   50%   |   90%   |
                 | Temp from Hot Spot         |   15C   |         |
    -------------+----------------------------+---------+---------+
     Lamps       | Voltage                    |   94%   |   94%   |
    -------------+----------------------------+---------+---------+
     Memories    | Supply Voltage             |  +/-5%  |  +/-5%  |
                 | Output Current             |   80%   |   90%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Micro-      | Supply Voltage             |  +/-5%  |  +/-5%  |
     circuits    | Fan Out                    |   80%   |   80%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     GaAs Micro- | Max Junction Temp          |  135C   |   N/A   |
     circuits    |                            |         |         |
    -------------+----------------------------+---------+---------+
     Micro-      | Supply Voltage             |  +/-5%  |  +/-5%  |
     processors  | Fan Out                    |   80%   |   80%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Photo-      | Reverse Voltage            |   70%   |    70%  |
     diode       | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Photo-      | Max Junction Temp          |  125C   |   N/A   |
     transistor  |                            |         |         |
    -------------+----------------------------+---------+---------+
     Relays      | Resistive Load Current     |   75%   |   90%   |
                 | Capacitive Load Current    |   75%   |   90%   |
                 | Inductive Load Current     |   40%   |   50%   |
                 | Contact Power              |   50%   |   60%   |
    -------------+----------------------------+---------+---------+
     Resistors   | Power Dissipation          |   50%   |   80%   |
                 | Temp from Max Limit        |   30C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Transistor, | Power Dissipation          |   70%   |   90%   |
     Silicon     | Breakdown Voltage          |   75%   |   90%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Transistor, | Power Dissipation          |   70%   |   90%   |
     GaAs        | Breakdown Voltage          |   70%   |   90%   |
                 | Max Junction Temp          |  135C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Thyristors  | On-State Current           |   70%   |   90%   |
                 | Off-State Voltage          |   70%   |   90%   |
                 | Max Junction Temp          |  125C   |   N/A   |
    -------------+----------------------------+---------+---------+
     Switches    | Resistive Load Current     |   75%   |   90%   |
                 | Capacitive Load Current    |   75%   |   90%   |
                 | Inductive Load Current     |   40%   |   50%   |
                 | Contact Power              |   50%   |   60%   |
    -------------+----------------------------+---------+---------+

    @param partmodel: the winParts full gtk.TreeModel().
    @type partmodel: gtk.TreeModel
    @param partrow: the currently selected gtk.TreeIter() in the winParts full
                    gtk.TreeModel().
    @type partrow: gtk.TreeIter
    @param systemmodel: the Hardware class gtk.TreeModel().
    @type systemmodel: gtk.TreeModel
    @param systemrow: the currently selected gtk.TreeIter() in the Hardware
                      class gtk.TreeModel().
    @type systemrow: gtk.TreeIter
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
            # TODO: Overstress calculations for crystals.
            print "TODO: Overstress calculations for crystals."
        elif subcategory == 81:            # Lamps
            Voper = partmodel.get_value(partrow, 66)
            Vrated = partmodel.get_value(partrow, 94)
            if Voper >= 0.94 * Vrated:
                overstress = True
                reason = reason + str(r_index) + ". Operating voltage > 94% " \
                                                 "rated voltage.\n"
                r_index += 1
        elif subcategory == 82:            # Fuse
            # TODO: Overstress calculations for fuses.
            print "TODO: Overstress calculations for fuses."
        elif subcategory == 83:            # Filter
            # TODO: Overstress calculations for filters.
            print "TODO: Overstress calculations for filters."

    elif category == 7:                    # Relay
        # TODO: Add contact power overstress calculations for relays
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
# TODO: Add temperature limit overstress calculations for resistors
# TODO: Add voltage ratio overstress calculations for variable resistors.
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
# TODO: Add contact power overstress calculations for switches
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

                  |           |    Full   |           |           |
                  |   Space   |  Military | Ruggedized| Commercial|
    --------------+-----------+-----------+-----------+-----------+
    Space         |    1.0    |    0.8    |    0.5    |    0.2    |
    --------------+-----------+-----------+-----------+-----------+
    Full Military |    1.3    |    1.0    |    0.6    |    0.3    |
    --------------+-----------+-----------+-----------+-----------+
    Ruggedized    |    2.0    |    1.7    |    1.0    |    0.4    |
    --------------+-----------+-----------+-----------+-----------+
    Commercial    |    5.0    |    3.3    |    2.5    |    1.0    |
    --------------+-----------+-----------+-----------+-----------+

    To convert from environment A to environment B use the conversion
    factors from Table 6.3.3-2 (reproduced below).

                  |  GB   |  GM   |  NS   |  AIC  |  ARW  |  SF   |
    --------------+-------+-------+-------+-------+-------+-------+
    GB            |  1.0  |  0.2  |  0.3  |  0.3  |  0.1  |  1.1  |
    --------------+-------+-------+-------+-------+-------+-------+
    GM            |  5.0  |  1.0  |  1.4  |  1.4  |  0.5  |  5.0  |
    --------------+-------+-------+-------+-------+-------+-------+
    NS            |  3.3  |  0.7  |  1.0  |  1.0  |  0.3  |  3.3  |
    --------------+-------+-------+-------+-------+-------+-------+
    AIC           |  3.3  |  0.7  |  1.0  |  1.0  |  0.3  |  3.3  |
    --------------+-------+-------+-------+-------+-------+-------+
    ARW           | 10.0  |  2.0  |  3.3  |  3.3  |  1.0  | 10.0  |
    --------------+-------+-------+-------+-------+-------+-------+
    SF            |  0.9  |  0.2  |  0.3  |  0.3  |  0.1  |  1.0  |
    --------------+-------+-------+-------+-------+-------+-------+

    To convert from temperature A to temperature B (both in Celcius) use
    conversion factors from Table 6.3.3-3 (reproduced below).

                 |  10  |  20  |  30  |  40  |  50  |  60  |  70  |
    -------------+------+------+------+------+------+------+------+
    10           |  1.0 |  0.9 |  0.8 |  0.8 |  0.7 |  0.5 |  0.4 |
    -------------+------+------+------+------+------+------+------+
    20           |  1.1 |  1.0 |  0.9 |  0.8 |  0.7 |  0.6 |  0.5 |
    -------------+------+------+------+------+------+------+------+
    30           |  1.2 |  1.1 |  1.0 |  0.9 |  0.8 |  0.6 |  0.5 |
    -------------+------+------+------+------+------+------+------+
    40           |  1.3 |  1.2 |  1.1 |  1.0 |  0.9 |  0.7 |  0.6 |
    -------------+------+------+------+------+------+------+------+
    50           |  1.5 |  1.4 |  1.2 |  1.1 |  1.0 |  0.8 |  0.7 |
    -------------+------+------+------+------+------+------+------+
    60           |  1.9 |  1.7 |  1.6 |  1.5 |  1.2 |  1.0 |  0.8 |
    -------------+------+------+------+------+------+------+------+
    70           |  2.4 |  2.2 |  1.9 |  1.8 |  1.5 |  1.2 |  1.0 |
    -------------+------+------+------+------+------+------+------+

    @param component: the rtk.Component() class to perform calculations on.
    @type component: rtk.Component
    @param new_qual: the index of the quality level of the new item.
    @type new_qual: integer
    @param new_environ: the index of the environment of the new item.
    @type new_environ: integer
    @param new_temp: the index of the operating temperature of the new item.
    @type new_temp: integer
    @return: hr_similar; the estimated hazard rate for the new item.
    @rtype: float
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

                  |Ground |Airborne|Airborne|Naval  |Naval  |Space  |Space  |
                  |Active |Active  |Active  |Active |Active |Active |Active |
                  |to     |to      |to      |to     |to     |to     |to     |
                  |Ground |Airborne|Ground  |Naval  |Ground |Space  |Ground |
                  |Passive|Passive |Passive |Passive|Passive|Passive|Passive|
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Integrated    | 0.08  |  0.06  |  0.04  | 0.06  | 0.05  | 0.10  | 0.30  |
    Circuits      |       |        |        |       |       |       |       |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Diodes        | 0.04  |  0.05  |  0.01  | 0.04  | 0.03  | 0.20  | 0.80  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Transistors   | 0.05  |  0.06  |  0.02  | 0.05  | 0.03  | 0.20  | 1.00  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Capacitors    | 0.10  |  0.10  |  0.03  | 0.10  | 0.04  | 0.20  | 0.40  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Resistors     | 0.20  |  0.06  |  0.03  | 0.10  | 0.06  | 0.50  | 1.00  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Switches      | 0.40  |  0.20  |  0.10  | 0.40  | 0.20  | 0.80  | 1.00  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Relays        | 0.20  |  0.20  |  0.04  | 0.30  | 0.08  | 0.40  | 0.90  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Connectors    | 0.005 |  0.005 |  0.003 | 0.008 | 0.003 | 0.02  | 0.03  |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Circuit       | 0.04  |  0.02  |  0.01  | 0.03  | 0.01  | 0.08  | 0.20  |
    Boards        |       |        |        |       |       |       |       |
    --------------+-------+--------+--------+-------+-------+-------+-------+
    Transformers  | 0.20  |  0.20  |  0.20  | 0.30  | 0.30  | 0.50  | 1.00  |
    --------------+-------+--------+--------+-------+-------+-------+-------+

    @param category: the component category index.
    @type category: integer
    @param subcategory: the component subcategory index.
    @type subcategory: integer
    @param active_env: the active environment index.
    @type active_env: integer
    @param dormant_env: the dormant environment index.
    @type dormant_env: integer
    @param lambdaa: the active hazard rate of the component.
    @type lambdaa: float
    @return: lambdad; the dormant hazard rate.
    @rtype: float
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

    @param modeca: list containing inputs for the MIL-STD-1629A mode
                   criticality calculation.
    @type modeca: list of mixed types
    @param itemca: list containing inputs for the MIL-STD-1629A item
                   criticality calculation.
    @type itemca: list of mixed types
    @param rpn: list containing inputs for the automotive criticality
                calculation.
    @type rpn: list of mixed types
    @return: modeca, itemca, rpn
    @rtype: list, list, list
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


def calculate_rg_phase(T1, MTBFi, MTBFf, MTBFa, GR, MS, FEF, Prob, ti, fix):
    """
    Function to calculate the values for an individual reliability growth
    phase.

    @param T1: the length of the first test phase.
    @type T1: float
    @param MTBFi: the inital MTBF for the test phase.
    @type MTBFi: float
    @param MTBFf: the final MTBF for the test phase.
    @type MTBFf: float
    @param MTBFa: the average MTBF for the test phase.
    @type MTBFa: float
    @param GR: the average growth rate across the entire test program.
    @type GR: float
    @param MS: the management strategy for this program.
    @type MS: float
    @param FEF: the average FEF for this program.
    @type FEF: float
    @param Prob: the probability of seeing one failure.
    @type Prob: float
    @param ti: the growth start time; time to first fix for this program.
    @type t1: float
    @param fix: list of True/False indicating which parameters are fixed when
                calculating results for each test phase.
                0 = Program probability
                1 = Management strategy
                2 = Time to first failure
                3 = Total test time for test phase
                4 = Test phase initial MTBF
                5 = Test phase final MTBF
                6 = Growth rate
    @type fix: list of booleans
    @return: GRi, T1, MTBFi, MTBFf; growth rate, test time, initial MTBF,
                                    final MTBF for the test phase.
    @rtype: float, float, float, float
    """

    # Calculate the average growth rate for the phase.
    if not fix[6]:
        try:
            GRi = -log(T1 / ti) - 1.0 + \
                  sqrt((1.0 + log(T1 / ti))**2.0 + 2.0 * log(MTBFf / MTBFi))
        except(ValueError, ZeroDivisionError):
            GRi = 0.0
    else:
        GRi = GR

    # Calculate initial MTBF for the phase.
    if not fix[4]:
        try:
            MTBFi = (-1.0 * ti * MS) / log(1.0 - Prob)
        except(ValueError, ZeroDivisionError):
            try:
                MTBFi = MTBFf / exp(GRi * (0.5 * GRi + log(T1 / ti) + 1.0))
            except(ValueError, ZeroDivisionError):
                try:
                    MTBFi = (ti * (T1 / ti)**(1.0 - GRi)) / Ni
                except(ValueError, ZeroDivisionError):
                    MTBFi = 0.0

    # Calculate final MTBF for the phase.
    if not fix[5]:
        try:
            MTBFf = MTBFi * exp(GRi * (0.5 * GRi + log(T1 / ti) + 1.0))
        except (ValueError, ZeroDivisionError):
            MTBFf = 0.0

    # Calculate total test time for the phase.
    if not fix[3]:
        try:
            T1 = exp(log(ti) +
                     1.0 / GRi * (log(MTBFf / MTBFi) + log(1.0 - GRi)))
        except(ValueError, ZeroDivisionError):
            T1 = 0.0

    return GRi, T1, MTBFi, MTBFf


def crow_amsaa(F, X, alpha, _grouped=False):
    """
    Function to estimate the parameters (beta and lambda) of the Crow-AMSAA
    continuous model using either the Option for Individual Failure Data
    (default) or the Option for Grouped Failure Data.

    Estimates or calculates the following:
     - beta: Crow-AMSAA shape parameter.
     - lambda: Crow-AMSAA scale parameter.
     - Instantaneous failure intensity: FIi = lambda * beta * T^(beta - 1)
     - Cumulative failure intensity: FIc = lambda * T^(beta - 1)
     - Instantaneous MTBF: MTBFi = 1.0 / lambda * beta * T^(beta - 1)
     - Cumulative MTBF: MTBFc = 1.0 / lambda * T^(beta - 1)
     - chi square: value of the chi square test statistic.
     - Cm: value of the Cramer-von Mises test statistc.

    @param F: list of failure counts.
    @type F: list of integers.
    @param X: list of failures times.
    @type X: list of floats.
    @param alpha: the confidence level for calculations.
    @type alpha: float
    @param _grouped: indicates whether or not to use grouped data.
    @type _grouped: boolean
    @return: (_beta_hat, _lambda_hat, _rhoc_hat, _rhoi_hat, _muc_hat, _mui_hat)
             where each returned variable is a list of lists.  There is an
             internal list for each failure time passed to the function.  These
             internal lists = [Lower Bound, Point, Upper Bound] for each
             variable.
    @rtype: mixed tuple
    """

    from numpy import matrix                # pylint: disable=E0611
    from scipy.optimize import fsolve       # pylint: disable=E0611
    from scipy.stats import norm            # pylint: disable=E0611

    # Define the function that will be set equal to zero and solved for beta.
    def _beta(b, f, t, logt):
        """
        Function for estimating the beta value from grouped data.
        """

        return(sum(f[1:] * ((t[1:]**b * logt[1:] - t[:-1]**b * logt[:-1]) /
                            (t[1:]**b - t[:-1]**b) - log(max(t)))))

    # Find the total time on test.
    TTT = X[-1]
    FFF = sum(F)

    _ei = 0.0
    _chi_square = 0.0
    _Cm = 0.0

    _beta_hat = []
    _lambda_hat = []
    _rhoc_hat = []
    _rhoi_hat = []
    _muc_hat = []
    _mui_hat = []

    # Get the standard normal value for the desired confidence.
    _z_norm = abs(norm.ppf(alpha))

    __failures = np.array([0], float)       # pylint: disable=E1101
    __times = np.array([0], float)          # pylint: disable=E1101
    __logt = np.array([0], float)           # pylint: disable=E1101

    for i in range(len(F)):
        __beta = [0.0, 0.0, 0.0]
        __lambda = [0.0, 0.0, 0.0]
        __rhoi = [0.0, 0.0, 0.0]
        __rhoc = [0.0, 0.0, 0.0]
        __muc = [0.0, 0.0, 0.0]
        __mui = [0.0, 0.0, 0.0]
        __var = [[0.0, 0.0], [0.0, 0.0]]

        if not _grouped:
            logX = [log(x) for x in X[:i+1]]

            # Estimate the value of beta.
            try:
                __beta[1] = (sum(F[:i+1]) /
                             (sum(F[:i+1]) * log(X[i]) - sum(logX)))
            except ZeroDivisionError:
                __beta[1] = 1.0

            # Using this estimated beta, estimate the value of lambda.
            __lambda[1] = sum(F[:i+1]) / X[i]**__beta[1]

            # Calculate the chi-square statistic to test for trend.
            _chi_square = 2.0 * FFF / __beta[1]

        elif _grouped:
            __failures = np.append(__failures, F[i])    # pylint: disable=E1101
            __times = np.append(__times, X[i])          # pylint: disable=E1101
            __logt = np.append(__logt, log(X[i]))       # pylint: disable=E1101

            # Estimate the value of beta.
            __beta[1] = fsolve(_beta, 1.0,
                               args=(__failures, __times, __logt))[0]

            # Using this estimated beta, estimate the value of lambda.
            __lambda[1] = (sum(F[:i+1]) / (X[:i+1])**__beta[1]).tolist()[-1]

            # Calculate the chi-square statistic to test for trend.
            _NPi = sum(F[:i+1]) * X[i] / max(X)
            _chi_square += (sum(F[:i+1]) - _NPi)**2.0 / (_NPi)

        # Calculate the variance-covariance matrix for the model
        # parameters.  The matrix is a list of lists:
        #
        #       __var = [[Var Lambda, Cov],
        #                [Cov, Var Beta]]
        __var[0][0] = sum(F[:i+1]) / __lambda[1]**2.0
        __var[1][1] = (sum(F[:i+1]) / __beta[1]**2.0) + \
                      __lambda[1] * X[i]**__beta[1] * log(X[i])**2.0
        __var[0][1] = X[i]**__beta[1] * log(X[i])
        __var[1][0] = __var[0][1]
        __var = matrix(__var).I.tolist()

        # Calculate the Fisher matrix bounds on each AMSAA parameter.
        __lambda[0] = __lambda[1] * exp(-_z_norm * sqrt(__var[0][0]) /
                                        __lambda[1])
        __lambda[2] = __lambda[1] * exp(_z_norm * sqrt(__var[0][0]) /
                                        __lambda[1])

        __beta[0] = __beta[1] * exp(-_z_norm * sqrt(__var[1][1]) /
                                    __beta[1])
        __beta[2] = __beta[1] * exp(_z_norm * sqrt(__var[1][1]) /
                                    __beta[1])

        _beta_hat.append(__beta)
        _lambda_hat.append(__lambda)

        # Calculate the instantaneous failure intensity at time T.
        __rhoi[1] = __lambda[1] * __beta[1] * X[i]**(__beta[1] - 1.0)

        # Calculate the Fisher matrix bounds on the instantaneous failure
        # intensity.
        _del_beta = __lambda[1] * X[i]**(__beta[1] - 1.0) + \
                    __lambda[1] * __beta[1] * \
                    X[i]**(__beta[1] - 1.0) * log(X[i])
        _del_lambda = __beta[1] * X[i]**(__beta[1] - 1.0)
        _var = _del_beta**2.0 * __var[1][1] + \
               _del_lambda**2.0 * __var[0][0] + \
               2.0 * _del_beta * _del_lambda * __var[0][1]

        __rhoi[0] = __rhoi[1] * exp(-_z_norm * sqrt(_var) / __rhoi[1])
        __rhoi[2] = __rhoi[1] * exp(_z_norm * sqrt(_var) / __rhoi[1])

        _rhoi_hat.append(__rhoi)

        # Calculate the cumulative failure intensity at time T.
        __rhoc[1] = __lambda[1] * (X[i])**(__beta[1] - 1.0)

        # Calculate the Fisher matrix bounds on the cumulative failure
        # intensity.
        _del_beta = __lambda[1] * X[i]**(__beta[1] - 1.0) * log(X[i])
        _del_lambda = X[i]**(__beta[1] - 1.0)
        _var = _del_beta**2.0 * __var[1][1] + \
               _del_lambda**2.0 * __var[0][0] + \
               2.0 * _del_beta * _del_lambda * __var[0][1]

        __rhoc[0] = __rhoc[1] * exp(-_z_norm * sqrt(_var) / __rhoc[1])
        __rhoc[2] = __rhoc[1] * exp(_z_norm * sqrt(_var) / __rhoc[1])

        _rhoc_hat.append(__rhoc)

        # Calculate the instantaneous MTBF at time T.
        __mui[1] = X[i]**(1.0 - __beta[1]) / (__lambda[1] * __beta[1])

        # Calculate the Fisher matrix bounds on the instantaneous MTBF.
        _del_beta = (-(X[i]**(1.0 - __beta[1])) /
                     (__lambda[1] * __beta[1]**2.0)) - \
                    ((X[i]**(1.0 - __beta[1]) * log(X[i])) /
                     (__lambda[1] * __beta[1]))
        _del_lambda = -(X[i]**(1.0 - __beta[1])) / \
                      (__lambda[1]**2.0 * __beta[1])
        _var = _del_beta**2.0 * __var[1][1] + \
               _del_lambda**2.0 * __var[0][0] + \
               2.0 * _del_beta * _del_lambda * __var[0][1]

        __mui[0] = __mui[1] * exp(-_z_norm * sqrt(_var) / __mui[1])
        __mui[2] = __mui[1] * exp(_z_norm * sqrt(_var) / __mui[1])

        _mui_hat.append(__mui)

        # Calculate the cumulative MTBF at time T.
        __muc[1] = X[i]**(1.0 - __beta[1]) / __lambda[1]

        # Calculate the Fisher matrix bounds on the cumulative MTBF.
        _del_beta = (-1.0 / __lambda[1]) * \
                    X[i]**(1.0 - __beta[1]) * log(X[i])
        _del_lambda = (-1.0 / __lambda[1]**2.0) * X[i]**(1.0 - __beta[1])
        _var = _del_beta**2.0 * __var[1][1] + \
               _del_lambda**2.0 * __var[0][0] + \
               2.0 * _del_beta * _del_lambda * __var[0][1]

        __muc[0] = __muc[1] * exp(-_z_norm * sqrt(_var) / __muc[1])
        __muc[2] = __muc[1] * exp(_z_norm * sqrt(_var) / __muc[1])

        _muc_hat.append(__muc)

        # Calculate the Cramer-von Mises statistic to test for model
        # applicability.
        _beta_bar = (sum(F[:i+1]) - 1) * __beta[1] / sum(F[:i+1])

        _ei += ((X[i] / TTT**_beta_bar) -
                ((2.0 * i - 1.0) / (2.0 * sum(F[:i+1]))))**2.0
        _Cm = _ei / (12.0 * sum(F[:i+1]))

    return(_beta_hat, _lambda_hat, _rhoc_hat, _rhoi_hat, _muc_hat, _mui_hat,
           _chi_square, _Cm)


def moving_average(data, n=3):
    """
    Function to calculate the moving average of a data set.

    @param data: the data set for which to find the moving average.
    @type data: list of floats or integers
    @param n: the desired period.
    @type n: integer
    @return: the nth period moving average of data.
    @rtype: float
    """

    _cumsum = np.cumsum(data, dtype=float)  # pylint: disable=E1101

    return (_cumsum[n - 1:] - _cumsum[:1 - n]) / n


def beta_bounds(a, m, b, alpha):
    """
    Function to calculate the mean, standard error, and bounds on the mean of
    a beta distribution.  These are the project management estimators, not
    exact calculations.

    @param a: the minimum expected value.
    @type a: float
    @param m: most likely value.
    @type m: float
    @param b: the maximum expected value.
    @type b: float
    @param alpha: the desired confidence level.
    @type alpha: float
    @return: _meanll, _mean, _meanul; the calculated mean and bounds.
    @rtype: tuple of floats
    """

    from scipy.stats import norm            # pylint: disable=E0611

    if alpha < 0.0:
        _util.rtk_information(_(u"Confidence level take a value between 0 and "
                                u"1 inclusive [0, 1].  Please select and "
                                u"appropriate confidence level and try "
                                u"again."))
        return a, m, b, 0.0
    elif alpha > 1.0:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha / 100.0) / 2.0))
    else:
        _z_norm = norm.ppf(1.0 - ((1.0 - alpha / 100.0) / 2.0))

    _mean = (a + 4.0 * m + b) / 6.0
    _sd = (b - a) / 6.0

    _meanll = _mean - _z_norm * _sd
    _meanul = _mean + _z_norm * _sd

    return _meanll, _mean, _meanul, _sd


def calculate_field_ttf(_dates_):
    """
    Function to calculate the time to failure (TTF) of field incidents.

    @param _dates_: tuple containing start and end date for calculating
                    time to failure.
    """

    from datetime import datetime

    _start = datetime(*time.strptime(_dates_[0], "%Y-%m-%d")[0:5]).date()
    _fail = datetime(*time.strptime(_dates_[1], "%Y-%m-%d")[0:5]).date()
    ttf = _fail - _start

    return ttf.days


def kaplan_meier(_dataset_, _reltime_, _conf_=0.75, _type_=3):
    """
    Function to calculate the Kaplan-Meier survival function estimates.

    @param dataset: list of tuples where each tuple is in the form of:
                    (Left of Interval, Right of Interval, Event Status) and
                    event status are:
                    0 = right censored
                    1 = event at time
                    2 = left censored
                    3 = interval censored
    @param reltime: time at which to stop analysis (helps eliminate stretched
                    plots due to small number of events at high hours).
    @param conf: the confidence level of the KM estimates (default is 75%).
    @param type: the confidence interval type for the KM estimates.
    @return: _KM, a list of lists where each inner list has the following
                  information:

                   0 = total number of subjects in each curve.
                   1 = the time points at which the curve has a step.
                   2 = the number of subjects at risk at t.
                   3 = the number of events that occur at time t.
                   4 = the number of subjects that enter at time t (counting
                       process data only).
                   5 = the estimate of survival at time t+0. This may be a
                       vector or a matrix.
                   6 = type of survival censoring.
                   7 = the standard error of the cumulative hazard or
                       -log(survival).
                   8 = upper confidence limit for the survival curve.
                   9 = lower confidence limit for the survival curve.
                  10 = the approximation used to compute the confidence limits.
                  11 = the level of the confidence limits, e.g. 90 or 95%.
                  12 = the returned value from the na.action function, if any.
                       It will be used in the printout of the curve, e.g., the
                       number of observations deleted due to missing values.
    @rtype: list
    """

    from scipy.stats import norm            # pylint: disable=E0611

    # Eliminate zero time failures and failures occurring after any
    # user-supplied upper limit.
    _dataset_ = [i for i in _dataset_ if i[0] >= 0.0]
    if _reltime_ != 0.0:
        _dataset_ = [i for i in _dataset_ if i[0] <= _reltime_]
        times = [i[0] for i in _dataset_ if i[0] <= _reltime_]
        times2 = [i[1] for i in _dataset_ if i[0] <= _reltime_]
        status = [i[2] for i in _dataset_ if i[0] <= _reltime_]

    for i in range(len(status)):
        if status[i] == "Right Censored":
            status[i] = 0
        elif status[i] == "Left Censored":
            status[i] = 2
        elif status[i] == "Interval Censored":
            status[i] = 3
        else:
            status[i] = 1

    # If Rpy2 is available, we will use that to perform the KM estimations.
    if __USE_RPY__:
        print "Probably using Windoze."

    elif __USE_RPY2__:
        survival = importr('survival')

        times = robjects.FloatVector(times)
        times2 = robjects.FloatVector(times2)
        status = robjects.IntVector(status)

        surv = survival.Surv(times, times2, type='interval2')   # pylint: disable=E1101
        robjects.globalenv['surv'] = surv
        fmla = robjects.Formula('surv ~ 1')
        _KM_ = survival.survfit(fmla)       # pylint: disable=E1101

        # Every subject must have a censored time to use survrec.
        # survrec = importr('survrec')
        # units = robjects.StrVector(units)
        # survr = survrec.Survr(units, times2, status2)
        # fit = survrec.wc_fit(survr)

        return _KM_

    else:

        # Determine the confidence bound z-value.
        _z_norm_ = norm.ppf(_conf_)

        # Get the total number of events.
        _n_ = len(_dataset_)
        N = _n_

        _KM_ = []
        _Sh_ = 1.0
        muhat = 0.0
        var = 0.0
        z = 0.0
        ti = float(_dataset_[0][0])
        tj = 0.0
        i = 0

        while _n_ > 0:
            # Find the total number of failures and
            # suspensions in interval [i - 1, i].
            _d_ = len([t for t in _dataset_
                       if t[0] == _dataset_[i][0] and t[1] == 1])
            _s_ = len([t for t in _dataset_
                       if t[0] == _dataset_[i][0] and t[1] == 0])

            # Estimate the probability of failing in interval [i - 1, i].
            _Si_ = 1.0 - (float(_d_) / float(_n_))

            # Estimate the probability of survival up to time i [S(ti)].
            _Sh_ = _Si_ * _Sh_

            # Calculate the standard error for S(ti).
            z = z + 1.0 / ((_n_ - _d_ + 1) * _n_)
            _se_ = sqrt(_Si_ * _Si_ * z)

            # Calculate confidence bounds for S(ti).
            _ll_ = _Sh_ - _z_norm_ * _se_
            _ul_ = _Sh_ + _z_norm_ * _se_
            if _type_ == 1 or _ul_ > 1.0:
                _ul_ = _Sh_
            if _type_ == 2 or _ll_ < 0.0:
                _ll_ = _Sh_

            # Calculate the cumulative hazard rate.
            try:
                _H_ = -log(_Sh_)
            except ValueError:
                _H_ = _H_

            # Calculate the mean.
            muhat = muhat + _Sh_ * (ti - tj)
            tj = ti
            ti = _dataset_[i][0]

            _KM_.append([ti, _n_, _d_, _Si_, _Sh_, _se_, _ll_, _ul_, _H_,
                         muhat, var])
            # if(_s_ > 0):
            #    _KM_.append([str(_dataset_[i][0]) + '+', _n_, _s_, '-', _Sh_,
            #                 _se_, _ll_, _ul_, _H_])

            _n_ = _n_ - _d_ - _s_
            i = i + _d_ + _s_

        return _KM_


def mean_cumulative_function(units, times, data, _conf_=0.75):
    """
    This function estimates the mean cumulative function (MCF) for a population
    of items.

    @param units: list of unique unit ID's in the data set.
    @type units: list
    @param times: list of unique failure times in the data set.
    @type times: list of floats
    @param data: a data.frame or matrix where:
                 Column 0 is the failed unit id.
                 Column 1 is the left of the interval.
                 Column 2 is the right of the interval.
                 Column 3 is the interarrival time.
    @type data: R data.frame
    @param conf: the confidence level of the MCF estimates (default is 75%).
    @type conf: float
    @return: MCF
    @rtype: list of lists
    """

    from scipy.stats import norm            # pylint: disable=E0611

    # Determine the confidence bound z-value.
    _z_norm_ = norm.ppf(_conf_)

    _m_ = len(units)
    _n_ = len(times)

    datad = []

    for i in range(len(data)):
        datad.append(data[i])
    data = np.asarray(data)                 # pylint: disable=E1101
    datad = np.asarray(datad)               # pylint: disable=E1101

    _d_ = np.zeros(shape=(_m_, _n_))        # pylint: disable=E1101
    _delta_ = np.zeros(shape=(_m_, _n_))    # pylint: disable=E1101

    for i in range(_n_):
        # Array of indices with failure times equal to the current unique
        # failure time.
        k = np.where(data[:, 2] == str(times[i]))    # pylint: disable=E1101

        # List of units whose failure time is equal to the current unique
        # failure time.
        _u_ = np.array(data[k, 0])[0].tolist()      # pylint: disable=E1101
        for j in range(len(_u_)):
            k = [a for a, x in enumerate(units) if x == _u_[j]]
            _delta_[k, 0:i+1] = 1

    for i in range(_n_):
        # Array of indices with failure times equal to the current unique
        # failure time.
        k = np.where(datad[:, 2] == str(times[i]))   # pylint: disable=E1101

        # List of units whose failure time is equal to the current unique
        # failure time.
        _u_ = np.array(datad[k, 0])[0].tolist()      # pylint: disable=E1101
        for j in range(len(_u_)):
            k = [a for a, x in enumerate(units) if x == _u_[j]]
            _d_[k, i] += 1

    _delta_ = _delta_.transpose()
    _d_ = _d_.transpose()

    _delta_dot = _delta_.sum(axis=1)
    _d_dot = (_d_ * _delta_).sum(axis=1)
    _d_bar = _d_dot / _delta_dot

    _MCF_ = []
    _x_ = (_delta_.transpose() / _delta_dot).transpose()
    _y_ = (_d_.transpose() - _d_bar).transpose()
    muhatp = 0.0
    _llp_ = 0.0
    _ulp_ = 0.0
    for i in range(len(times)):
        muhat = _d_bar[0:i+1].sum(axis=0)

        # Estimate the variance.
        _z_ = (_x_[0:i+1] * _y_[0:i+1])
        _var_ = ((_z_.sum(axis=0))**2).sum(axis=0)

        # Calculate the lower and upper bound on the MCF.
        _ll_ = muhat - _z_norm_ * sqrt(_var_)
        _ul_ = muhat + _z_norm_ * sqrt(_var_)

        # Estimate the cumulative MTBF.
        _mtbfc_ = times[i] / muhat
        _mtbfcll_ = times[i] / _ul_
        _mtbfcul_ = times[i] / _ll_

        # Estimate the instantaneous MTBF.
        if i > 0:
            _mtbfi_ = (times[i] - times[i - 1]) / (muhat - muhatp)
            _mtbfill_ = (times[i] - times[i - 1]) / (_ul_ - _ulp_)
            _mtbfiul_ = (times[i] - times[i - 1]) / (_ll_ - _llp_)
        else:
            _mtbfi_ = times[i] / (muhat - muhatp)
            _mtbfill_ = times[i] / (_ul_ - _ulp_)
            _mtbfiul_ = times[i] / (_ll_ - _llp_)

        muhatp = muhat
        _llp_ = _ll_
        _ulp_ = _ul_

        _MCF_.append([times[i], _delta_[i], _d_[i], _delta_dot[i], _d_dot[i],
                      _d_bar[i], _var_, _ll_, _ul_, muhat, _mtbfc_, _mtbfcll_,
                      _mtbfcul_, _mtbfi_, _mtbfill_, _mtbfiul_])

    return _MCF_


def parametric_fit(_dataset_, _starttime_, _reltime_, _fitmeth_,
                   _dist_='exponential'):
    """
    Function to fit data to a parametric distribution and estimate the
    parameters.

    @param _dataset_: the data set to fit.
    @type _dataset_: list of floats
    @param _reltime_: the maximum time to include in the fit.  Used to exclude
                      outliers.
    @type _reltime_: float
    @param _fitmeth_: method used to fit data to the selected distribution.
                      1 = rank regression
                      2 = maximum likelihood estimation (MLE)
    @type _fitmeth_: integer
    @param _dist_: the noun name of the distribution to fit.  Defaults to
                   the exponential distribution.
    @type _dist_: string
    @return: fit
    @rtype: R.Survival.SurvReg object
    """

    # Eliminate zero time failures and failures occurring after any
    # user-supplied upper limit.
    _dataset_ = [i for i in _dataset_ if i[2] > _starttime_]
    _dataset_ = [i for i in _dataset_ if i[2] <= _reltime_]

    if __USE_RPY__:
        print "Probably using Windoze."

    elif __USE_RPY2__:

        Rbase = importr('base')

        if _fitmeth_ == 1:                  # MLE
            if _dist_ == 'exponential':
                _dist_ = 'exp'
            elif _dist_ == 'lognormal':
                _dist_ = 'lnorm'
            elif _dist_ == 'normal':
                _dist_ = 'norm'

            left = [i[1] for i in _dataset_]
            right = [i[2] for i in _dataset_]
            for i in range(len(_dataset_)):
                if _dataset_[i][4] == 0:
                    right[i] = 'NA'
                elif _dataset_[i][4] == 1:
                    left[i] = right[i]
                elif _dataset_[i][4] == 2:
                    left[i] = 'NA'

            od = rlc.OrdDict([('left', robjects.FloatVector(left)),
                              ('right', robjects.FloatVector(right))])

            censdata = robjects.DataFrame(od)
            n_row = Rbase.nrow(censdata)    # pylint: disable=E1101
            if n_row[0] > 1:
                fitdistrplus = importr('fitdistrplus')
                try:
                    fit = fitdistrplus.fitdistcens(censdata, _dist_)    # pylint: disable=E1101
                except ri.RRuntimeError:
                    return True

                #para=R.list(scale=fit[0][1], shape=fit[0][0])
                #fitdistrplus.plotdistcens(censdata, _dist_, para)
            else:
                return True

        elif _fitmeth_ == 2:                # Regression
            if _dist_ == 'normal':
                _dist_ = 'gaussian'

            if _reltime_ != 0.0:
                time = [i[1] + 0.01 for i in _dataset_ if i[2] <= _reltime_]
                time2 = [i[2] + 0.01 for i in _dataset_ if i[2] <= _reltime_]
                status = [i[4] for i in _dataset_ if i[2] <= _reltime_]

            survival = importr('survival')

            for i in range(len(status)):
                if status[i] == 'Right Censored':
                    status[i] = 0
                elif status[i] == 'Event':
                    status[i] = 1
                elif status[i] == 'Left Censored':
                    status[i] = 2
                else:
                    status[i] = 3

            time = robjects.FloatVector(time)
            time2 = robjects.FloatVector(time2)
            status = robjects.IntVector(status)

            surv = survival.Surv(time, time2, status, type='interval')  # pylint: disable=E1101
            robjects.globalenv['surv'] = surv
            formula = robjects.Formula('surv ~ 1')

            fit = survival.survreg(formula, dist=_dist_)    # pylint: disable=E1101

    else:
        print "No R"

    return fit


def smooth_curve(x, y, num):
    """
    Function to produce smoothed plots where there are a small number of data
    points in the original data set.

    @param x: a numpy array of the raw x-values.
    @type x: numpy array
    @param y: a numpy array of the raw y-values.
    @type y: numpy array
    @param num: the number of points to generate.
    @type num: integer
    @return: _new_x, _new_y
    @rtype: list
    """

    from scipy.interpolate import spline    # pylint: disable=E0611

    _error = False

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

    @param _data_: data set used to bound the theoretical distribution.
    @type _data_: list of floats
    @param _distr_: the name of the desired theoretical distribution.
    @type _distr_: string
    @param _para_: the parameters of the desired theoretical distribution.
    @type _para_: list of floats
    @return: theop
    @rtype: R object
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
