# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.constants.inductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductive devices MIL-HDBK-217F Constants Module."""

# Standard Library Imports
from typing import Dict, List

PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]]] = {
    1: {
        1: [
            0.0035,
            0.023,
            0.049,
            0.019,
            0.065,
            0.027,
            0.037,
            0.041,
            0.052,
            0.11,
            0.0018,
            0.053,
            0.16,
            2.3,
        ],
        2: [
            0.0071,
            0.046,
            0.097,
            0.038,
            0.13,
            0.055,
            0.073,
            0.081,
            0.10,
            0.22,
            0.035,
            0.11,
            0.31,
            4.7,
        ],
        3: [
            0.023,
            0.16,
            0.35,
            0.13,
            0.45,
            0.21,
            0.27,
            0.35,
            0.45,
            0.82,
            0.011,
            0.37,
            1.2,
            16.0,
        ],
        4: [
            0.028,
            0.18,
            0.39,
            0.15,
            0.52,
            0.22,
            0.29,
            0.33,
            0.42,
            0.88,
            0.015,
            0.42,
            1.2,
            19.0,
        ],
    },
    2: {
        1: [
            0.0017,
            0.0073,
            0.023,
            0.0091,
            0.031,
            0.011,
            0.015,
            0.016,
            0.022,
            0.052,
            0.00083,
            0.25,
            0.073,
            1.1,
        ],
        2: [
            0.0033,
            0.015,
            0.046,
            0.018,
            0.061,
            0.022,
            0.03,
            0.033,
            0.044,
            0.10,
            0.0017,
            0.05,
            0.15,
            2.2,
        ],
    },
}
PART_COUNT_PI_Q: List[float] = [0.25, 1.0, 10.0]
PART_STRESS_PI_Q: Dict[int, Dict[int, List[float]] | List[float]] = {
    1: {1: [1.5, 5.0], 2: [3.0, 7.5], 3: [8.0, 30.0], 4: [12.0, 30.0]},
    2: [0.03, 0.1, 0.3, 1.0, 4.0, 20.0],
}
PI_E: Dict[int, List[float]] = {
    1: [
        1.0,
        6.0,
        12.0,
        5.0,
        16.0,
        6.0,
        8.0,
        7.0,
        9.0,
        24.0,
        0.5,
        13.0,
        34.0,
        610.0,
    ],
    2: [
        1.0,
        4.0,
        12.0,
        5.0,
        16.0,
        5.0,
        7.0,
        6.0,
        8.0,
        24.0,
        0.5,
        13.0,
        34.0,
        610.0,
    ],
}
REF_TEMPS: Dict[int, Dict[int, float]] = {
    1: {1: 329.0, 2: 352.0, 3: 364.0, 4: 400.0, 5: 398.0, 6: 477.0},
    2: {1: 329.0, 2: 352.0, 3: 364.0, 4: 409.0},
}
