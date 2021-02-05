# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.Dormancy.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Dormancy Calculations Module."""

# Standard Library Imports
from typing import List, Union

# Third Party Imports
import numpy as np

DORMANT_HR_MULT = np.array([[[0.0, 0.08, 0.0, 0.0], [0.0, 0.08, 0.0, 0.0],
                             [0.0, 0.08, 0.0, 0.0], [0.0, 0.05, 0.06, 0.0],
                             [0.0, 0.05, 0.06, 0.0], [0.06, 0.04, 0.0, 0.0],
                             [0.06, 0.04, 0.0, 0.0], [0.06, 0.04, 0.0, 0.0],
                             [0.06, 0.04, 0.0, 0.0], [0.06, 0.04, 0.0, 0.0],
                             [0.0, 0.3, 0.0, 0.1]],
                            [[[0.0, 0.0], [0.04, 0.05], [0.0, 0.0], [0.0,
                                                                     0.0]],
                             [[0.0, 0.0], [0.04, 0.05], [0.0, 0.0], [0.0,
                                                                     0.0]],
                             [[0.0, 0.0], [0.04, 0.05], [0.0, 0.0], [0.0,
                                                                     0.0]],
                             [[0.0, 0.0], [0.03, 0.03], [0.04, 0.05],
                              [0.0, 0.0]],
                             [[0.0, 0.0], [0.03, 0.03], [0.04, 0.05],
                              [0.0, 0.0]],
                             [[0.05, 0.06], [0.01, 0.02], [0.0, 0.0],
                              [0.0, 0.0]],
                             [[0.05, 0.06], [0.01, 0.02], [0.0, 0.0],
                              [0.0, 0.0]],
                             [[0.05, 0.06], [0.01, 0.02], [0.0, 0.0],
                              [0.0, 0.0]],
                             [[0.05, 0.06], [0.01, 0.02], [0.0, 0.0],
                              [0.0, 0.0]],
                             [[0.05, 0.06], [0.01, 0.02], [0.0, 0.0],
                              [0.0, 0.0]],
                             [[0.0, 0.0], [0.8, 1.0], [0.0, 0.0], [0.2, 0.2]]],
                            [[0.0, 0.2, 0.0, 0.0], [0.0, 0.2, 0.0, 0.0],
                             [0.0, 0.2, 0.0, 0.0], [0.0, 0.06, 0.1, 0.0],
                             [0.0, 0.06, 0.1, 0.0], [0.06, 0.2, 0.0, 0.0],
                             [0.06, 0.2, 0.0, 0.0], [0.06, 0.2, 0.0, 0.0],
                             [0.06, 0.2, 0.0, 0.0], [0.06, 0.2, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.5]],
                            [[0.0, 0.1, 0.0, 0.0], [0.0, 0.1, 0.0, 0.0],
                             [0.0, 0.1, 0.0, 0.0], [0.0, 0.04, 0.1, 0.0],
                             [0.0, 0.04, 0.1, 0.0], [0.1, 0.03, 0.0, 0.0],
                             [0.1, 0.03, 0.0, 0.0], [0.1, 0.03, 0.0, 0.0],
                             [0.1, 0.03, 0.0, 0.0], [0.1, 0.03, 0.0, 0.0],
                             [0.0, 0.4, 0.0, 0.2]],
                            [[0.0, 0.2, 0.0, 0.0], [0.0, 0.2, 0.0, 0.0],
                             [0.0, 0.2, 0.0, 0.0], [0.0, 0.3, 0.3, 0.0],
                             [0.0, 0.3, 0.3, 0.0], [0.2, 0.2, 0.0, 0.0],
                             [0.2, 0.2, 0.0, 0.0], [0.2, 0.2, 0.0, 0.0],
                             [0.2, 0.2, 0.0, 0.0], [0.2, 0.2, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.5]],
                            [[0.0, 0.2, 0.0, 0.0], [0.0, 0.2, 0.0, 0.0],
                             [0.0, 0.2, 0.0, 0.0], [0.0, 0.08, 0.3, 0.0],
                             [0.0, 0.08, 0.3, 0.0], [0.2, 0.04, 0.0, 0.0],
                             [0.2, 0.04, 0.0, 0.0], [0.2, 0.04, 0.0, 0.0],
                             [0.2, 0.04, 0.0, 0.0], [0.2, 0.04, 0.0, 0.0],
                             [0.0, 0.9, 0.0, 0.4]],
                            [[0.0, 0.4, 0.0, 0.0], [0.0, 0.4, 0.0, 0.0],
                             [0.0, 0.4, 0.0, 0.0], [0.0, 0.2, 0.4, 0.0],
                             [0.0, 0.2, 0.4, 0.0], [0.2, 0.1, 0.0, 0.0],
                             [0.2, 0.1, 0.0, 0.0], [0.2, 0.1, 0.0, 0.0],
                             [0.2, 0.1, 0.0, 0.0], [0.2, 0.1, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.8]],
                            [[0.0, 0.005, 0.0, 0.0], [0.0, 0.005, 0.0, 0.0],
                             [0.0, 0.005, 0.0, 0.0], [0.0, 0.003, 0.008, 0.0],
                             [0.0, 0.003, 0.008, 0.0],
                             [0.0005, 0.003, 0.0, 0.0],
                             [0.0005, 0.003, 0.0, 0.0],
                             [0.0005, 0.003, 0.0, 0.0],
                             [0.0005, 0.003, 0.0, 0.0],
                             [0.0005, 0.003, 0.0, 0.0], [0.0, 0.03, 0.0,
                                                         0.02]]])


def do_calculate_dormant_hazard_rate(hw_info: List[Union[int, float]],
                                     env_info: List[int]) -> float:
    """Calculate the dormant hazard rate for a hardware item.

    .. attention:: The semiconductor category will return a list of two
        dormancy multipliers.  The value at index 0 is for diodes and the
        value at index 1 is for transistors.

    .. important:: The calling object is responsible for handling any
        exceptions raised by or passed through this method.

    .. note:: All conversion factors come from Reliability Toolkit:
        Commercial Practices Edition, Section 6.3.4, Table 6.3.4-1.

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
    if hw_info[0] == 2:
        if hw_info[1] in [1, 2]:
            _dormant_hr_mult = DORMANT_HR_MULT[hw_info[0] - 1][env_info[0]
                                                               - 1][env_info[1]
                                                                    - 1][0]
        else:
            _dormant_hr_mult = DORMANT_HR_MULT[hw_info[0] - 1][env_info[0]
                                                               - 1][env_info[1]
                                                                    - 1][1]
    else:
        _dormant_hr_mult = DORMANT_HR_MULT[hw_info[0] - 1][env_info[0]
                                                           - 1][env_info[1]
                                                                - 1]

    return _dormant_hr_mult * hw_info[2]
