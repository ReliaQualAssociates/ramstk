# -*- coding: utf-8 -*-
#
#       ramstk.analyses.Stress.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Stress Calculations Module."""

# <requirement module="analyses">
#   <name>Analyses file location</name>
#   <description>Each type of analyses shall have a single file in the analyses
#   directory such that it can be imported as
#   from ramstk.analyses import [name of analysis].  This file may contain
#   functions, classes, or both as necessary to implement the
#   analysis.</description>
#   <example>analyses/MilHdbk217f.py contains the class MilHdbk217F.  This
#   class contains methods to perform the MIL-HDBK-217F parts count and parts
#   stress analyses.</example>
# </requirement>
# <requirement module="analyses">
#   <name>Analyses model location</name>
#   <description>For analyses that rely on engineering or mathematical models
#   and/or constants specific to each component type, the associated models
#   and constants shall reside in a single file for each component type in the
#   `analyses/models/[analysis name]` directory.</description>
#   <example>The MIL-HDBK-217F models for capacitors reside in
#   `analyses/models/milhdbk217f/Capacitor.py`.</example>
# </requirement>


def calculate_stress_ratio(stress_operating, stress_rated):
    """
    Calculate the operating electrical stress ratio of a device.

    Inputs can be floats, integers, or a combination.

    >>> calculate_stress_ratio(0.382, 1.29)
    0.2961240310077519
    >>> calculate_stress_ratio(1, 2)
    0.5
    >>> calculate_stress_ratio(0.382, 2)
    0.191
    >>> calculate_stress_ratio(1, 1.29)
    0.7751937984496123

    Rated stress must not be zero:
    >>> calculate_stress_ratio(0.382, 0.o)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: float division by zero

    Stress inputs must not be strings:
    >>>  calculate_stress_ratio(0.382, '3.2')
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for /: 'float' and 'str'

    :param float stress_operating: the device's operating level of the stress.
    :param float stress_rated: the devices's rated stress.
    :return: _stress_ratio; the ratio of operating stress to rated stress.
    :rtype: float
    :raise: TypeError if an input value is non-numerical.
    :raise: ZeroDivisionError if the rated stress is zero.
    """
    return stress_operating / stress_rated
