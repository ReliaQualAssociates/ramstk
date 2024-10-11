# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.Dormancy.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Dormancy Calculations Module."""

# Standard Library Imports
from typing import List, Optional, Union

DORMANT_HR_MULTIPLIER = {
    "ground": {
        "ground": [0.08, [0.04, 0.05], 0.2, 0.1, 0.2, 0.2, 0.4, 0.005],
    },
    "airborne": {
        "airborne": [0.06, [0.05, 0.06], 0.06, 0.1, 0.2, 0.2, 0.2, 0.005],
        "ground": [0.04, [0.01, 0.02], 0.03, 0.03, 0.2, 0.04, 0.1, 0.003],
    },
    "naval": {
        "naval": [0.06, [0.04, 0.05], 0.1, 0.1, 0.3, 0.3, 0.4, 0.008],
        "ground": [0.05, [0.03, 0.03], 0.06, 0.04, 0.3, 0.08, 0.2, 0.003],
    },
    "space": {
        "space": [0.1, [0.2, 0.2], 0.5, 0.2, 0.5, 0.4, 0.8, 0.02],
        "ground": [0.3, [0.8, 1.0], 1.0, 0.4, 1.0, 0.9, 1.0, 0.03],
    },
}
ENVIRONMENTS_ACTIVE = [
    "ground",
    "ground",
    "ground",
    "naval",
    "naval",
    "airborne",
    "airborne",
    "airborne",
    "airborne",
    "airborne",
    "space",
    "missile",
    "missile",
]
ENVIRONMENTS_DORMANT = [
    "ground",
    "naval",
    "airborne",
    "space",
]


def get_environment_type(env_id: int, is_active: bool) -> Optional[str]:
    """Get the environment type based on the environment ID.

    :param env_id: the index in the environment list.
    :param is_active: indicates whether or not to use the ENVIRONMENTS_ACTIVE list.
    :return: the name of the environment associated with the end_id.
    :rtype: str
    """
    _index = env_id - 1
    if is_active:
        if _index < len(ENVIRONMENTS_ACTIVE):
            return ENVIRONMENTS_ACTIVE[_index]
    elif _index < len(ENVIRONMENTS_DORMANT):
        return ENVIRONMENTS_DORMANT[_index]
    return None


def get_dormant_hr_multiplier(
    hw_info: List[Union[int, float]], env_active: str, env_dormant: str
) -> float:
    """Get the dormant hazard rate multiplier based on hardware and environment info.

    :param hw_info: the list of information relative to the hardware item to calculate
        the dormant hazard rate. Index 0 is the category ID, index 1 is the subcategory
        ID, and index 3 is the predicted hazard rate.
    :param env_active: the name of the active environment.
    :param env_dormant: the name of the dormant environment.
    :return: the dormant hazard rate multiplier.
    :rtype: float
    """
    _category_id = hw_info[0] - 1
    _subcategory_id = hw_info[1] - 1

    if _category_id > 7:
        return 0.0
    try:
        if _category_id == 1:  # Semiconductor
            if _subcategory_id in [0, 1]:  # Diode or transistor
                return DORMANT_HR_MULTIPLIER[env_active][env_dormant][_category_id][
                    _subcategory_id
                ]
            else:
                return 0.0
        return DORMANT_HR_MULTIPLIER[env_active][env_dormant][_category_id]
    except KeyError:
        return 0.0


def do_calculate_dormant_hazard_rate(
    hw_info: List[Union[int, float]], env_info: List[int]
) -> float:
    """Calculate the dormant hazard rate for a hardware item.

    .. attention:: The semiconductor category will return a list of two
        dormancy multipliers.  The value at index 0 is for diodes and the
        value at index 1 is for transistors.

    .. important:: The calling object is responsible for handling any
        exceptions raised by or passed through this method.

    .. note:: All conversion factors come from Reliability Toolkit:
        Commercial Practices Edition, Section 6.3.4, Table 6.3.4-1.

    Hardware categories are:
    - 1 = integrated circuit
    - 2 = semiconductor
    - 3 = resistor
    - 4 = capacitor
    - 5 = inductor
    - 6 = relay
    - 7 = switch
    - 8 = connection
    - 9 = meter
    - 10 = miscellaneous

    Environment indexes are:

    +-------------------------+-------------------------+
    | environment_active_id   |   Active Environment    |
    |     in attributes       |           Type          |
    +=========================+=========================+
    |          1 - 3          | Ground                  |
    +-------------------------+-------------------------+
    |          4 - 5          | Naval                   |
    +-------------------------+-------------------------+
    |         6 - 10          | Airborne                |
    +-------------------------+-------------------------+
    |           11            | Space                   |
    +-------------------------+-------------------------+
    |         12 - 13         | Missile                 |
    |                         | (no conversion factors) |
    +-------------------------+-------------------------+

    +--------------------------+-------------------------+
    | environment_dormant_id   |   Active Environment    |
    |      in attributes       |           Type          |
    +==========================+=========================+
    |             1            | Ground                  |
    +--------------------------+-------------------------+
    |             2            | Naval                   |
    +--------------------------+-------------------------+
    |             3            | Airborne                |
    +--------------------------+-------------------------+
    |             4            | Space                   |
    +--------------------------+-------------------------+

    :param hw_info: the list of information relative to the hardware item
        to calculate the dormant hazard rate.  Index 0 is the category ID,
        index 1 is the subcategory ID, and index 3 is the predicted hazard
        rate.
    :param env_info: the list of environment information.  Index 0
        is the active environment ID per the table above and index 2 is the
        dormant (storage) environment ID per the table above.
    :rtype: float
    :raise: IndexError if an indexing argument asks for a non-existent index.
    """
    _env_active = get_environment_type(env_info[0], True)
    _env_dormant = get_environment_type(env_info[1], False)

    if _env_active is None or _env_dormant is None:
        return 0.0

    _dormant_hr_multiplier = get_dormant_hr_multiplier(
        hw_info, _env_active, _env_dormant
    )

    return _dormant_hr_multiplier * hw_info[2]
