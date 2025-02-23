# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.constants.resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor MIL-HDBK-217F Constants Module."""

# Standard Library Imports
from typing import Dict, List

PART_COUNT_LAMBDA_B: Dict[int, List[float]] = {
    1: [
        0.0005,
        0.0022,
        0.0071,
        0.0037,
        0.012,
        0.0052,
        0.0065,
        0.016,
        0.025,
        0.025,
        0.00025,
        0.0098,
        0.035,
        0.36,
    ],
    2: {
        1: [
            0.0012,
            0.0027,
            0.011,
            0.0054,
            0.020,
            0.0063,
            0.013,
            0.018,
            0.033,
            0.030,
            0.00025,
            0.014,
            0.044,
            0.69,
        ],
        2: [
            0.0012,
            0.0027,
            0.011,
            0.0054,
            0.020,
            0.0063,
            0.013,
            0.018,
            0.033,
            0.030,
            0.00025,
            0.014,
            0.044,
            0.69,
        ],
        3: [
            0.0014,
            0.0031,
            0.013,
            0.0061,
            0.023,
            0.0072,
            0.014,
            0.021,
            0.038,
            0.034,
            0.00028,
            0.016,
            0.050,
            0.78,
        ],
        4: [
            0.0014,
            0.0031,
            0.013,
            0.0061,
            0.023,
            0.0072,
            0.014,
            0.021,
            0.038,
            0.034,
            0.00028,
            0.016,
            0.050,
            0.78,
        ],
    },
    3: [
        0.012,
        0.025,
        0.13,
        0.062,
        0.21,
        0.078,
        0.10,
        0.19,
        0.24,
        0.32,
        0.0060,
        0.18,
        0.47,
        8.2,
    ],
    4: [
        0.0023,
        0.0066,
        0.031,
        0.013,
        0.055,
        0.022,
        0.043,
        0.077,
        0.15,
        0.10,
        0.0011,
        0.055,
        0.15,
        1.7,
    ],
    5: [
        0.0085,
        0.018,
        0.10,
        0.045,
        0.16,
        0.15,
        0.17,
        0.30,
        0.38,
        0.26,
        0.0068,
        0.13,
        0.37,
        5.4,
    ],
    6: {
        1: [
            0.014,
            0.031,
            0.16,
            0.077,
            0.26,
            0.073,
            0.15,
            0.19,
            0.39,
            0.42,
            0.0042,
            0.21,
            0.62,
            9.4,
        ],
        2: [
            0.013,
            0.028,
            0.15,
            0.070,
            0.24,
            0.065,
            0.13,
            0.18,
            0.35,
            0.38,
            0.0038,
            0.19,
            0.56,
            8.6,
        ],
    },
    7: [
        0.008,
        0.18,
        0.096,
        0.045,
        0.15,
        0.044,
        0.088,
        0.12,
        0.24,
        0.25,
        0.004,
        0.13,
        0.37,
        5.5,
    ],
    8: [
        0.065,
        0.32,
        1.4,
        0.71,
        1.6,
        0.71,
        1.9,
        1.0,
        2.7,
        2.4,
        0.032,
        1.3,
        3.4,
        62.0,
    ],
    9: [
        0.025,
        0.055,
        0.35,
        0.15,
        0.58,
        0.16,
        0.26,
        0.35,
        0.58,
        1.1,
        0.013,
        0.52,
        1.6,
        24.0,
    ],
    10: [
        0.33,
        0.73,
        7.0,
        2.9,
        12.0,
        3.5,
        5.3,
        7.1,
        9.8,
        23.0,
        0.16,
        11.0,
        33.0,
        510.0,
    ],
    11: [
        0.15,
        0.35,
        3.1,
        1.2,
        5.4,
        1.9,
        2.8,
        0.0,
        0.0,
        9.0,
        0.075,
        0.0,
        0.0,
        0.0,
    ],
    12: [
        0.15,
        0.34,
        2.9,
        1.2,
        5.0,
        1.6,
        2.4,
        0.0,
        0.0,
        7.6,
        0.076,
        0.0,
        0.0,
        0.0,
    ],
    13: [
        0.043,
        0.15,
        0.75,
        0.35,
        1.3,
        0.39,
        0.78,
        1.8,
        2.8,
        2.5,
        0.21,
        1.2,
        3.7,
        49.0,
    ],
    14: [
        0.05,
        0.11,
        1.1,
        0.45,
        1.7,
        2.8,
        4.6,
        4.6,
        7.5,
        3.3,
        0.025,
        1.5,
        4.7,
        67.0,
    ],
    15: [
        0.048,
        0.16,
        0.76,
        0.36,
        1.3,
        0.36,
        0.72,
        1.4,
        2.2,
        2.3,
        0.024,
        1.2,
        3.4,
        52.0,
    ],
}
PART_COUNT_PI_Q: List[float] = [0.030, 0.10, 0.30, 1.0, 3.0, 10.0]
PART_STRESS_PI_Q: Dict[int, List[float]] = {
    1: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
    2: [0.03, 0.1, 0.3, 1.0, 5.0, 5.0, 15.0],
    3: [1.0, 3.0],
    4: [1.0, 3.0],
    5: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
    6: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
    7: [0.03, 0.1, 0.3, 1.0, 5.0, 15.0],
    8: [1.0, 15.0],
    9: [0.02, 0.06, 0.2, 0.6, 3.0, 10.0],
    10: [2.5, 5.0],
    11: [2.0, 4.0],
    12: [2.0, 4.0],
    13: [0.02, 0.06, 0.2, 0.6, 3.0, 10.0],
    14: [2.5, 5.0],
    15: [2.0, 4.0],
}
PI_C: Dict[int, List[float]] = {10: [2.0, 1.0, 3.0, 1.5], 12: [2.0, 1.0]}
PI_E: Dict[int, List[float]] = {
    1: [
        1.0,
        3.0,
        8.0,
        5.0,
        13.0,
        4.0,
        5.0,
        7.0,
        11.0,
        19.0,
        0.5,
        11.0,
        27.0,
        490.0,
    ],
    2: [
        1.0,
        2.0,
        8.0,
        4.0,
        14.0,
        4.0,
        8.0,
        10.0,
        18.0,
        19.0,
        0.2,
        10.0,
        28.0,
        510.0,
    ],
    3: [
        1.0,
        2.0,
        10.0,
        5.0,
        17.0,
        6.0,
        8.0,
        14.0,
        18.0,
        25.0,
        0.5,
        14.0,
        36.0,
        660.0,
    ],
    4: [
        1.0,
        2.0,
        10.0,
        5.0,
        17.0,
        6.0,
        8.0,
        14.0,
        18.0,
        25.0,
        0.5,
        14.0,
        36.0,
        660.0,
    ],
    5: [
        1.0,
        2.0,
        11.0,
        5.0,
        18.0,
        15.0,
        18.0,
        28.0,
        35.0,
        27.0,
        0.8,
        14.0,
        38.0,
        610.0,
    ],
    6: [
        1.0,
        2.0,
        10.0,
        5.0,
        16.0,
        4.0,
        8.0,
        9.0,
        18.0,
        23.0,
        0.3,
        13.0,
        34.0,
        610.0,
    ],
    7: [
        1.0,
        2.0,
        10.0,
        5.0,
        16.0,
        4.0,
        8.0,
        9.0,
        18.0,
        23.0,
        0.5,
        13.0,
        34.0,
        610.0,
    ],
    8: [
        1.0,
        5.0,
        21.0,
        11.0,
        24.0,
        11.0,
        30.0,
        16.0,
        42.0,
        37.0,
        0.5,
        20.0,
        53.0,
        950.0,
    ],
    9: [
        1.0,
        2.0,
        12.0,
        6.0,
        20.0,
        5.0,
        8.0,
        9.0,
        15.0,
        33.0,
        0.5,
        18.0,
        48.0,
        870.0,
    ],
    10: [
        1.0,
        2.0,
        18.0,
        8.0,
        30.0,
        8.0,
        12.0,
        13.0,
        18.0,
        53.0,
        0.5,
        29.0,
        76.0,
        1400.0,
    ],
    11: [
        1.0,
        2.0,
        16.0,
        7.0,
        28.0,
        8.0,
        12.0,
        0.0,
        0.0,
        38.0,
        0.5,
        0.0,
        0.0,
        0.0,
    ],
    12: [
        1.0,
        3.0,
        16.0,
        7.0,
        28.0,
        8.0,
        12.0,
        0.0,
        0.0,
        38.0,
        0.5,
        0.0,
        0.0,
        0.0,
    ],
    13: [
        1.0,
        3.0,
        14.0,
        6.0,
        24.0,
        5.0,
        7.0,
        12.0,
        18.0,
        39.0,
        0.5,
        22.0,
        57.0,
        1000.0,
    ],
    14: [
        1.0,
        2.0,
        19.0,
        8.0,
        29.0,
        40.0,
        65.0,
        48.0,
        78.0,
        46.0,
        0.5,
        25.0,
        66.0,
        1200.0,
    ],
    15: [
        1.0,
        3.0,
        14.0,
        7.0,
        24.0,
        6.0,
        12.0,
        20.0,
        30.0,
        39.0,
        0.5,
        22.0,
        57.0,
        1000.0,
    ],
}
PI_R: Dict[int, List[float] | List[List[float]]] = {
    1: [1.0, 1.1, 1.6, 2.5],
    2: [1.0, 1.1, 1.6, 2.5],
    3: [1.0, 1.2, 1.3, 3.5],
    5: [1.0, 1.7, 3.0, 5.0],
    6: [
        [
            [1.0, 1.0, 1.2, 1.2, 1.6, 1.6, 1.6, 0.0],
            [1.0, 1.0, 1.0, 1.2, 1.6, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 1.6],
            [1.0, 1.2, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.6, 1.6, 0.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.1, 1.2, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0, 0.0, 0.0],
        ],
        [
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
            [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 2.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
            [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 2.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.2, 0.0, 0.0],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.5, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.4, 1.6, 0.0],
            [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
            [1.0, 1.0, 1.0, 1.4, 1.6, 2.0],
            [1.0, 1.0, 1.4, 2.4, 0.0, 0.0],
            [1.0, 1.0, 1.2, 2.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
            [1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 1.2, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.0, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.4, 0.0, 0.0, 0.0],
            [1.0, 1.2, 1.5, 0.0, 0.0, 0.0],
            [1.0, 1.2, 0.0, 0.0, 0.0, 0.0],
        ],
    ],
    7: [
        [
            [1.0, 1.2, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.2, 1.6, 0.0],
            [1.0, 1.0, 1.0, 1.1, 1.2, 1.6],
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
            [1.0, 1.0, 1.0, 1.0, 1.2, 1.6],
        ],
        [
            [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.2, 1.6, 0.0, 0.0, 0.0],
            [1.0, 1.0, 1.2, 1.6, 0.0, 0.0],
            [1.0, 1.0, 1.1, 1.2, 1.4, 0.0],
            [1.0, 1.0, 1.0, 1.2, 1.6, 0.0],
            [1.0, 1.0, 1.0, 1.1, 1.4, 0.0],
        ],
    ],
    9: [1.0, 1.4, 2.0],
    10: [1.0, 1.1, 1.4, 2.0, 2.5, 3.5],
    11: [1.0, 1.4, 2.0],
    12: [1.0, 1.4, 2.0],
    13: [1.0, 1.1, 1.2, 1.4, 1.8],
    14: [1.0, 1.1, 1.2, 1.4, 1.8],
    15: [1.0, 1.1, 1.2, 1.4, 1.8],
}
PI_V: Dict[int, List[float]] = {
    9: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    10: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    11: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    12: [1.1, 1.05, 1.0, 1.1, 1.22, 1.4, 2.0],
    13: [1.0, 1.05, 1.2],
    14: [1.0, 1.05, 1.2],
    15: [1.0, 1.05, 1.2],
}
REF_TEMPS: Dict[int, float] = {
    1: 343.0,
    3: 298.0,
    5: 398.0,
    6: 298.0,
    7: 298.0,
    9: 358.0,
    10: 358.0,
    11: 313.0,
    12: 298.0,
    13: 358.0,
    14: 343.0,
    15: 343.0,
}
REF_TEMPS_FILM: Dict[int, float] = {1: 343.0, 2: 343.0, 3: 398.0, 4: 398.0}
