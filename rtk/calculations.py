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

# Add NLS support.
_ = gettext.gettext

import numpy as np

import Configuration as _conf
import Utilities as _util


def calculate_part(model):
    """
    Calculates the hazard rate for a component.

    :param dict model: the component's h(t) prediction model and the input
                       variables.  The keys are the model variables and the
                       values are the values of the variable in the key.
    :return: _lambdap, the calculated h(t).
    :rtype: float
    """
# TODO: Move to Hardware class.
    _keys = model.keys()
    _values = model.values()

    for i in range(len(_keys)):
        vars()[_keys[i]] = _values[i]

    _lambdap = eval(model['equation'])      # pylint: disable=W0123

    return _lambdap


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
# TODO: Move to Similar Item class.
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


def dormant_hazard_rate(component):
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

    :param :class: `rtk.hardware.Component` component: the rtk.Component() data
                                                       model to calculate.
    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """
# TODO: Move to each component type class.
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
    if component.category_id == 1:                       # Capacitor
        c_index = 3
    elif component.category_id == 2:                     # Connection
        c_index = 7
    elif component.category_id == 3:                     # Inductive Device.
        if component.subcategory_id > 1:                 # Transformer
            c_index = 9
    elif component.category_id == 4:                     # Integrated Circuit
        c_index = 0
    elif component.category_id == 7:                     # Relay
        c_index = 6
    elif component.category_id == 8:                     # Resistor
        c_index = 4
    elif component.category_id == 9:                     # Semiconductor
        if component.subcategory_id > 0 and \
           component.subcategory_id < 7:                 # Diode
            c_index = 1
        elif component.subcategory_id > 6 and \
             component.subcategory_id < 14:     # Transistor
            c_index = 2
    elif component.category_id == 10:           # Switching Device
        c_index = 5

    # Now find the appropriate active to passive environment index.
    if component.environment_active > 0 and \
       component.environment_active < 4:        # Ground
        if component.environment_dormant == 1:  # Ground
            e_index = 0
        else:
            e_index = 7
    elif component.environment_active > 3 and \
         component.environment_active < 6:      # Naval
        if component.environment_dormant == 1:  # Ground
            e_index = 4
        elif component.environment_dormant == 2:    # Naval
            e_index = 3
        else:
            e_index = 7
    elif component.environment_active > 5 and \
         component.environment_active < 11:     # Airborne
        if component.environment_dormant == 1:  # Ground
            e_index = 2
        elif component.environment_dormant == 3:    # Airborne
            e_index = 1
        else:
            e_index = 7
    elif component.environment_active == 11:    # Space
        if component.environment_dormant == 1:  # Ground
            e_index = 6
        elif component.environment_dormant == 4:    # Space
            e_index = 5
        else:
            e_index = 7

    try:
        component.hazard_rate_dormant = component.hazard_rate_active * \
                                        factor[c_index - 1][e_index]
        return False
    except IndexError:
        component.hazard_rate_dormant = 0.0
        return True
    except UnboundLocalError:
        component.hazard_rate_dormant = 0.0
        return True


def calculate_field_ttf(dates):
    """
    Function to calculate the time to failure (TTF) of field incidents.

    :param tuple dates: tuple containing start and end date for calculating
                        time to failure.
    :return: _ttf.days; the number of days between the start and end date.
    :rtype: float
    """
# TODO: Move to Incident class.
    from datetime import datetime

    _start = datetime.strptime(dates[0], "%Y-%m-%d")
    _fail = datetime.strptime(dates[1], "%Y-%m-%d")
    _ttf = _fail - _start
    print _ttf.days
    return _ttf.days
