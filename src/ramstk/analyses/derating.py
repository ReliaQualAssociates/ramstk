# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Derating Calculations Module."""


def check_overstress(op_stress, limits):
    """Check if an operating condition results in an overstressed condition.

    Checks if the operating stress is less than the lower limit or greater than
    the upper limit.  Limits and operating stresses may be integers or floats.

    >>> check_overstress(0.625, {'mild': [0.0, 0.9], 'harsh': [0.0, 0.75]})
    {'mild': [False, False], 'harsh': [False, False]}
    >>> check_overstress(-0.625, {'mild': [0.0, 0.9], 'harsh': [0.0, 0.75]})
    {'mild': [True, False], 'harsh': [True, False]}
    >>> check_overstress(0.825, {'mild': [0.0, 0.9], 'harsh': [0.0, 0.75]})
    {'mild': [False, False], 'harsh': [False, True]}
    >>> check_overstress(0.825, {'mild': [0, 0.9], 'harsh': [0, 0.75]})
    {'mild': [False, False], 'harsh': [False, True]}
    >>> check_overstress(1, {'mild': [0, 0.9], 'harsh': [0, 0.75]})
    {'mild': [False, True], 'harsh': [False, True]}

    Limits must be lists:
    >>> check_overstress(0.825, {'mild': 0.9, 'harsh': 0.75})
    Traceback (most recent call last):
        ...
    TypeError: 'float' object is not subscriptable

    And those lists must contain a lower and upper limit:
    check_overstress(0.825, {'mild': [0.9], 'harsh': [0.75]})
    Traceback (most recent call last):
        ...
    IndexError: list index out of range

    Limit values must not be strings:
    check_overstress(0.825, {'mild': [0.0, '0.9'], 'harsh': [0.0, 0.75]})
    Traceback (most recent call last):
        ...
    TypeError: '>' not supported between instances of 'float' and 'str'

    The programmer must ensure the operating stress and limits are provided in
    the proper format.  For example:

        op_stress = (operating current / rated current) with limits provided as
        decimals.
        op_stress = (operating temperature - maximum junction temperature) with
        limits provided as a delta T.

    :param op_stress: the level of the operating stress.
    :param limits: a dict containing the stress limits.  Key is the name
        of the environment (mild, harsh, protected, etc.) and the value is a
        list of [lower limit, upper limit].
    :return: _overstress; dict of indicators whether or not an overstress
        condition exists.  Key is the environment type (mild, harsh, protected,
        etc.) and the value is a list of booleans for each limit.
    :rtype: dict
    :raise: IndexError if a limit value has too few items in the list.
    :raise: TypeError if a limit value is not a list of numericals.
    """
    _overstress = {}

    for key in limits:
        _overstress[key] = [False, False]
        if op_stress < limits[key][0]:
            _overstress[key][0] = True
        if op_stress > limits[key][1]:
            _overstress[key][1] = True

    return _overstress
