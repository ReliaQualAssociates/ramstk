# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.derating.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Derating Calculations Module."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Local Imports
from .models import (
    capacitor,
    connection,
    inductor,
    integratedcircuit,
    lamp,
    semiconductor,
)


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


# pylint: disable=inconsistent-return-statements
def do_check_overstress(
    category: str,
    environment_id: int,
    subcategory_id,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    **kwargs,
) -> Tuple[int, str]:
    """Perform a derating analysis.

    :param category:
    :param environment_id:
    :param subcategory_id:
    :param stress_limits:
    :return: _overstress, _reason
    :rtype: tuple
    """
    _environment = {
        1: 0,
        2: 1,
        3: 2,
        4: 0,
        5: 2,
        6: 1,
        7: 1,
        8: 2,
        9: 2,
        10: 1,
        11: 0,
        12: 1,
        13: 2,
    }[environment_id]

    if category == "capacitor":
        return capacitor.do_derating_analysis(
            _environment,
            subcategory_id,
            stress_limits,
            specification_id=kwargs.get("specification_id", 0),
            temperature_case=kwargs.get("temperature_case", 30.0),
            temperature_rated_max=kwargs.get("temperature_rated_max", 70.0),
            voltage_ratio=kwargs.get("voltage_ratio", 0.0),
        )
    elif category == "connection":
        return connection.do_derating_analysis(
            _environment,
            stress_limits,
            current_ratio=kwargs.get("current_ratio", 0.0),
            temperature_hot_spot=kwargs.get("temperature_hot_spot", 30.0),
            temperature_rated_max=kwargs.get("temperature_rated_max", 70.0),
            voltage_ratio=kwargs.get("voltage_ratio", 0.0),
        )
    elif category == "inductor":
        return inductor.do_derating_analysis(
            _environment,
            subcategory_id,
            stress_limits,
            family_id=kwargs.get("family_id", 0),
        )
    elif category == "integrated_circuit":
        return integratedcircuit.do_derating_analysis(
            _environment,
            subcategory_id,
            stress_limits,
            current_ratio=kwargs.get("current_ratio", 0.0),
            package_id=kwargs.get("package_id", 0),
            technology_id=kwargs.get("technology_id", 0),
            temperature_junction=kwargs.get("temperature_junction", 70.0),
        )
    elif category == "miscellaneous":
        return lamp.do_derating_analysis(
            _environment,
            subcategory_id,
            stress_limits,
            current_ratio=kwargs.get("current_ratio", 0.0),
        )
    elif category == "semiconductor":
        return semiconductor.do_derating_analysis(
            _environment,
            subcategory_id,
            stress_limits,
            current_ratio=kwargs.get("current_ratio", 0.0),
            power_ratio=kwargs.get("power_ratio", 0.0),
            quality_id=kwargs.get("quality_id", 1),
            temperature_junction=kwargs.get("temperature_junction", 70.0),
            voltage_ratio=kwargs.get("voltage_ratio", 0.0),
        )
