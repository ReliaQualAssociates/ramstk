# -*- coding: utf-8 -*-
#
#       ramstk.analyses.Dormancy.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Dormancy Calculations Module."""

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


def do_calculate_dormant_hazard_rate(
        category_id,
        subcategory_id,
        environment_active_id,
        environment_dormant_id,
        hazard_rate_active,
):
    r"""
    Calculate the dormant hazard rate for a hardware item.

    .. attention:: The semiconductor category will return a list of two
        dormancy multipliers.  The value at index 0 is for diodes and the
        value at index 1 is for transistors.

    .. important:: The calling object is responsible for handling any
        exceptions raised by or passed through this method.

    .. note:: All conversion factors come from Reliability Toolkit:
        Commercial Practices Edition, Section 6.3.4, Table 6.3.4-1.

    Environment indexes are:

    +-------------------------+-------------------------+
    | environment_active_id \ |   Active Environment \  |
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
    |         12 - 13         | Missile  \              |
    |                         | (no conversion factors) |
    +-------------------------+-------------------------+

    +--------------------------+-------------------------+
    | environment_dormant_id \ |   Active Environment \  |
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

    :param int category_id: the component category ID; used as index 0.
    :param int subcategory_id: the component subcategory ID; used as index
        3 for semiconductors.
    :param int environment_active_id: the active environment ID per the
        table above; used as index 1.
    :param int environment_dormant_id: the dormant (storage) environment ID
        per the table above; used as index 2.
    :param float hazard_rate_active: the active hazard rate of the component.
    :return: _hr_dormant; the calculated dormant hazard rate.
    :rtype: float
    :raise: IndexError if an indexing argument asks for a non-existent index.
    """
    if category_id == 2:
        if subcategory_id in [1, 2]:
            _dormant_hr_mult = DORMANT_HR_MULT[category_id
                                               - 1][environment_active_id
                                                    - 1][environment_dormant_id
                                                         - 1][0]
        else:
            _dormant_hr_mult = DORMANT_HR_MULT[category_id
                                               - 1][environment_active_id
                                                    - 1][environment_dormant_id
                                                         - 1][1]
    else:
        _dormant_hr_mult = DORMANT_HR_MULT[category_id
                                           - 1][environment_active_id
                                                - 1][environment_dormant_id
                                                     - 1]

    return _dormant_hr_mult * hazard_rate_active
