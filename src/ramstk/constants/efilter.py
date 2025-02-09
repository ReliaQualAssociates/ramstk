# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.constants.efilter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Electronic Filter MIL-HDBK-217F Constants Module."""


PART_COUNT_LAMBDA_B = {
    1: [
        0.022,
        0.044,
        0.13,
        0.088,
        0.20,
        0.15,
        0.20,
        0.24,
        0.29,
        0.24,
        0.018,
        0.15,
        0.33,
        2.6,
    ],
    2: [
        0.12,
        0.24,
        0.72,
        0.48,
        1.1,
        0.84,
        1.1,
        1.3,
        1.6,
        1.3,
        0.096,
        0.84,
        1.8,
        1.4,
    ],
    3: [
        0.27,
        0.54,
        1.6,
        1.1,
        2.4,
        1.9,
        2.4,
        3.0,
        3.5,
        3.0,
        0.22,
        1.9,
        4.1,
        32.0,
    ],
}
PART_STRESS_LAMBDA_B = {1: 0.022, 2: 0.12, 3: 0.12, 4: 0.27}
PI_E = [
    1.0,
    2.0,
    6.0,
    4.0,
    9.0,
    7.0,
    9.0,
    11.0,
    13.0,
    11.0,
    0.8,
    7.0,
    15.0,
    120.0,
]
PI_Q = [1.0, 2.9]
