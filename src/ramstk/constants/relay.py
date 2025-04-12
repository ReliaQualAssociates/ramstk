# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.constants.relay.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Relay constants module."""

# Standard Library Imports
from typing import Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _

# Constants for MIL-HDBK-217FN2 models
PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]]] = {
    1: {
        1: [
            0.13,
            0.28,
            2.1,
            1.1,
            3.8,
            1.1,
            1.4,
            1.9,
            2.0,
            7.0,
            0.66,
            3.5,
            10.0,
            0.0,
        ],
        2: [
            0.43,
            0.89,
            6.9,
            3.6,
            12.0,
            3.4,
            4.4,
            6.2,
            6.7,
            22.0,
            0.21,
            11.0,
            32.0,
            0.0,
        ],
        3: [
            0.13,
            0.26,
            2.1,
            1.1,
            3.8,
            1.1,
            1.4,
            1.9,
            2.0,
            7.0,
            0.66,
            3.5,
            10.0,
            0.0,
        ],
        4: [
            0.11,
            0.23,
            1.8,
            0.92,
            3.3,
            0.96,
            1.2,
            2.1,
            2.3,
            6.5,
            0.54,
            3.0,
            9.0,
            0.0,
        ],
        5: [
            0.29,
            0.60,
            4.8,
            2.4,
            8.2,
            2.3,
            2.9,
            4.1,
            4.5,
            15.0,
            0.14,
            7.6,
            22.0,
            0.0,
        ],
        6: [
            0.88,
            1.8,
            14.0,
            7.4,
            26.0,
            7.1,
            9.1,
            13.0,
            14.0,
            46.0,
            0.44,
            24.0,
            67.0,
            0.0,
        ],
    },
    2: {
        1: [
            0.40,
            1.2,
            4.8,
            2.4,
            6.8,
            4.8,
            7.6,
            8.4,
            13.0,
            9.2,
            0.16,
            4.8,
            13.0,
            240.0,
        ],
        2: [
            0.50,
            1.5,
            6.0,
            3.0,
            8.5,
            5.0,
            9.5,
            11.0,
            16.0,
            12.0,
            0.20,
            5.0,
            17.0,
            300.0,
        ],
    },
}
PART_COUNT_PI_Q: Dict[int, List[float]] = {1: [0.6, 3.0, 9.0], 2: [0.0, 1.0, 4.0]}
PART_STRESS_PI_Q: Dict[int, List[float]] = {
    1: [0.1, 0.3, 0.45, 0.6, 1.0, 1.5, 3.0],
    2: [1.0, 4.0],
}
PI_C: Dict[int, List[float]] = {1: [1.0, 1.5, 1.75, 2.0, 2.5, 3.0, 4.25, 5.5, 8.0]}
PI_E: Dict[int, Dict[int, List[float]] | List[float]] = {
    1: {
        1: [
            1.0,
            2.0,
            15.0,
            8.0,
            27.0,
            7.0,
            9.0,
            11.0,
            12.0,
            46.0,
            0.50,
            25.0,
            66.0,
            0.0,
        ],
        2: [
            2.0,
            5.0,
            44.0,
            24.0,
            78.0,
            15.0,
            20.0,
            28.0,
            38.0,
            140.0,
            1.0,
            72.0,
            200.0,
            0.0,
        ],
    },
    2: [
        1.0,
        3.0,
        12.0,
        6.0,
        17.0,
        12.0,
        19.0,
        21.0,
        32.0,
        23.0,
        0.4,
        12.0,
        33.0,
        590.0,
    ],
}
PI_F: Dict[int, Dict[int, Dict[int, List[float]]]] = {
    1: {
        1: {
            1: [4.0, 8.0],
            2: [6.0, 18.0],
            3: [1.0, 3.0],
            4: [4.0, 8.0],
            5: [7.0, 14.0],
            6: [7.0, 14.0],
        }
    },
    2: {
        1: {1: [3.0, 6.0], 2: [5.0, 10.0], 3: [6.0, 12.0]},
        2: {
            1: [5.0, 10.0],
            2: [2.0, 6.0],
            3: [6.0, 12.0],
            4: [100.0, 100.0],
            5: [10.0, 20.0],
        },
        3: {1: [10.0, 20.0], 2: [100.0, 100.0]},
        4: {1: [6.0, 12.0], 2: [1.0, 3.0]},
        5: {1: [25.0, 0.0], 2: [6.0, 0.0]},
        6: {1: [10.0, 20.0]},
        7: {1: [9.0, 12.0]},
        8: {1: [10.0, 20.0], 2: [5.0, 10.0], 3: [5.0, 10.0]},
    },
    3: {
        1: {1: [20.0, 40.0], 2: [5.0, 10.0]},
        2: {
            1: [3.0, 6.0],
            2: [1.0, 3.0],
            3: [2.0, 6.0],
            4: [3.0, 6.0],
            5: [2.0, 6.0],
            6: [2.0, 6.0],
        },
    },
    4: {1: {1: [7.0, 14.0], 2: [12.0, 24.0], 3: [10.0, 20.0], 4: [5.0, 10.0]}},
}

# Constants for GUI displays.
# Key is contact rating ID.  Index is application ID.
RELAY_APPLICATION_DICT: Dict[int, List[List[str]]] = {
    1: [[_("Dry Circuit")]],
    2: [
        [_("General Purpose")],
        [_("Sensitive (0 - 100mW)")],
        [_("Polarized")],
        [_("Vibrating Reed")],
        [_("High Speed")],
        [_("Thermal Time Delay")],
        [_("Electronic Time Delay, Non-Thermal")],
        [_("Magnetic Latching")],
    ],
    3: [
        [_("High Voltage")],
        [_("Medium Power")],
    ],
    4: [[_("Contactors, High Current")]],
}
# First key is contact rating ID, second key is application ID.
# Index is construction ID.
RELAY_CONSTRUCTION_DICT: Dict[int, Dict[int, List[List[str]]]] = {
    1: {
        1: [
            [_("Armature (Long)")],
            [_("Dry Reed")],
            [_("Mercury Wetted")],
            [_("Magnetic Latching")],
            [_("Balanced Armature")],
            [_("Solenoid")],
        ]
    },
    2: {
        1: [
            [_("Armature (Long)")],
            [_("Balanced Armature")],
            [_("Solenoid")],
        ],
        2: [
            [_("Armature (Long and Short)")],
            [_("Mercury Wetted")],
            [_("Magnetic Latching")],
            [_("Meter Movement")],
            [_("Balanced Armature")],
        ],
        3: [
            [_("Armature (Short)")],
            [_("Meter Movement")],
        ],
        4: [
            [_("Dry Reed")],
            [_("Mercury Wetted")],
        ],
        5: [
            [_("Armature (Balanced and Short)")],
            [_("Dry Reed")],
        ],
        6: [[_("Bimetal")]],
        8: [
            [_("Dry Reed")],
            [_("Mercury Wetted")],
            [_("Balanced Armature")],
        ],
    },
    3: {
        1: [
            [_("Vacuum (Glass)")],
            [_("Vacuum (Ceramic)")],
        ],
        2: [
            [_("Armature (Long and Short)")],
            [_("Mercury Wetted")],
            [_("Magnetic Latching")],
            [_("Mechanical Latching")],
            [_("Balanced Armature")],
            [_("Solenoid")],
        ],
    },
    4: {
        1: [
            [_("Armature (Short)")],
            [_("Magnetic Latching")],
            [_("Balanced Armature")],
            [_("Solenoid")],
        ]
    },
}
RELAY_QUALITY_DICT: Dict[int, List[List[str]]] = {
    1: [
        ["S"],
        ["R"],
        ["P"],
        ["M"],
        ["MIL-C-15305"],
        [_("Lower")],
    ],
    2: [
        ["MIL-SPEC"],
        [_("Lower")],
    ],
}
# Key is subcategory ID.  Index is type ID.
RELAY_TYPE_DICT: Dict[int, List[List[str]]] = {
    1: [
        [_("General Purpose")],
        [_("Contactor, High Current")],
        [_("Latching")],
        [_("Reed")],
        [_("Thermal, Bi-Metal")],
        [_("Meter Movement")],
    ],
    2: [
        [_("Solid State")],
        [_("Hybrid and Solid State Time Delay")],
    ],
}
# Index is the contact form ID.
RELAY_CONTACT_FORM_LIST: List[List[str]] = [
    ["SPST"],
    ["DPST"],
    ["SPDT"],
    ["3PST"],
    ["4PST"],
    ["DPDT"],
    ["3PDT"],
    ["4PDT"],
    ["6PDT"],
]
# Index is contact rating ID.
RELAY_CONTACT_RATING_LIST: List[List[str]] = [
    [_("Signal Current (low mV and mA)")],
    [_("0 - 5 Amp")],
    [_("5 - 20 Amp")],
    [_("20 - 600 Amp")],
]
# Index is the technology ID (load type).
RELAY_TECHNOLOGY_LIST: List[List[str]] = [
    [_("Resistive")],
    [_("Inductive")],
    [_("Lamp")],
]
