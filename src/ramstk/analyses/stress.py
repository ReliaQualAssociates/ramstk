# -*- coding: utf-8 -*-
#
#       ramstk.analyses.Stress.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Stress Calculations Module."""


def calculate_stress_ratio(stress_operating, stress_rated):
    """Calculate the operating electrical stress ratio of a device.

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
    >>> calculate_stress_ratio(0.382, 0.0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: float division by zero

    Stress inputs must not be strings:
    >>>  calculate_stress_ratio(0.382, '3.2')
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for /: 'float' and 'str'

    :param stress_operating: the device's operating level of the stress.
    :param stress_rated: the devices's rated stress.
    :return: _stress_ratio; the ratio of operating stress to rated stress.
    :rtype: float
    :raise: TypeError if an input value is non-numerical.
    :raise: ZeroDivisionError if the rated stress is zero.
    """
    return stress_operating / stress_rated
