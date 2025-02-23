# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.constants.meter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter MIL-HDBK-217F Constants Module."""

# Standard Library Imports
from typing import Dict, List

PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]]] = {
    1: {
        1: [
            10.0,
            20.0,
            120.0,
            70.0,
            180.0,
            50.0,
            80.0,
            160.0,
            250.0,
            260.0,
            5.0,
            140.0,
            380.0,
            0.0,
        ],
        2: [
            15.0,
            30.0,
            180.0,
            105.0,
            270.0,
            75.0,
            120.0,
            240.0,
            375.0,
            390.0,
            7.5,
            210.0,
            570.0,
            0.0,
        ],
        3: [
            40.0,
            80.0,
            480.0,
            280.0,
            720.0,
            200.0,
            320.0,
            640.0,
            1000.0,
            1040.0,
            20.0,
            560.0,
            1520.0,
            0.0,
        ],
    },
    2: {
        1: [
            0.09,
            0.36,
            2.3,
            1.1,
            3.2,
            2.5,
            3.8,
            5.2,
            6.6,
            5.4,
            0.099,
            5.4,
            0.0,
            0.0,
        ],
        2: [
            0.15,
            0.61,
            2.8,
            1.8,
            5.4,
            4.3,
            6.4,
            8.9,
            11.0,
            9.2,
            0.17,
            9.2,
            0.0,
            0.0,
        ],
    },
}
PART_COUNT_PI_Q: Dict[int, List[float]] = {1: [1.0, 1.0], 2: [1.0, 3.4]}
PART_STRESS_LAMBDA_B: Dict[int, List[float] | float] = {1: [20.0, 30.0, 80.0], 2: 0.09}
PART_STRESS_PI_Q: List[float] = [1.0, 3.4]
PI_E: Dict[int, List[float]] = {
    1: [
        1.0,
        2.0,
        12.0,
        7.0,
        18.0,
        5.0,
        8.0,
        16.0,
        25.0,
        26.0,
        0.5,
        14.0,
        38.0,
        0.0,
    ],
    2: [
        1.0,
        4.0,
        25.0,
        12.0,
        35.0,
        28.0,
        42.0,
        58.0,
        73.0,
        60.0,
        1.1,
        60.0,
        0.0,
        0.0,
    ],
}
PI_F: List[float] = [1.0, 1.0, 2.8]
