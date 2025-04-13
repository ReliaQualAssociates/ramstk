# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.constants.connection.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection constants module."""

# Standard Library Imports
from typing import Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _

# Constants for MIL-HDBK-217FN2 models.
PART_COUNT_LAMBDA_B: Dict[int, Dict[int, List[float]] | List[float]] = {
    1: {
        1: [
            0.011,
            0.14,
            0.11,
            0.069,
            0.20,
            0.058,
            0.098,
            0.23,
            0.34,
            0.37,
            0.0054,
            0.16,
            0.42,
            6.8,
        ],
        2: [
            0.012,
            0.015,
            0.13,
            0.075,
            0.21,
            0.06,
            0.1,
            0.22,
            0.32,
            0.38,
            0.0061,
            0.18,
            0.54,
            7.3,
        ],
    },
    2: [
        0.0054,
        0.021,
        0.055,
        0.035,
        0.10,
        0.059,
        0.11,
        0.085,
        0.16,
        0.19,
        0.0027,
        0.078,
        0.21,
        3.4,
    ],
    3: [
        0.0019,
        0.0058,
        0.027,
        0.012,
        0.035,
        0.015,
        0.023,
        0.021,
        0.025,
        0.048,
        0.00097,
        0.027,
        0.070,
        1.3,
    ],
    4: [
        0.053,
        0.11,
        0.37,
        0.69,
        0.27,
        0.27,
        0.43,
        0.85,
        1.5,
        1.0,
        0.027,
        0.53,
        1.4,
        27.0,
    ],
    5: {
        1: [
            0.0026,
            0.0052,
            0.018,
            0.010,
            0.029,
            0.010,
            0.016,
            0.016,
            0.021,
            0.042,
            0.0013,
            0.023,
            0.062,
            1.1,
        ],
        2: [
            0.00014,
            0.00028,
            0.00096,
            0.00056,
            0.0015,
            0.00056,
            0.00084,
            0.00084,
            0.0011,
            0.0022,
            0.00007,
            0.0013,
            0.0034,
            0.059,
        ],
        3: [
            0.00026,
            0.00052,
            0.0018,
            0.0010,
            0.0029,
            0.0010,
            0.0016,
            0.0016,
            0.0021,
            0.0042,
            0.00013,
            0.0023,
            0.0062,
            0.11,
        ],
        4: [
            0.000050,
            0.000100,
            0.000350,
            0.000200,
            0.000550,
            0.000200,
            0.000300,
            0.000300,
            0.000400,
            0.000800,
            0.000025,
            0.000450,
            0.001200,
            0.021000,
        ],
        5: [
            0.0000035,
            0.000007,
            0.000025,
            0.000014,
            0.000039,
            0.000014,
            0.000021,
            0.000021,
            0.000028,
            0.000056,
            0.0000018,
            0.000031,
            0.000084,
            0.0015,
        ],
        6: [
            0.00012,
            0.00024,
            0.00084,
            0.00048,
            0.0013,
            0.00048,
            0.00072,
            0.00072,
            0.00096,
            0.0019,
            0.00005,
            0.0011,
            0.0029,
            0.050,
        ],
        7: [
            0.000069,
            0.000138,
            0.000483,
            0.000276,
            0.000759,
            0.000276,
            0.000414,
            0.000414,
            0.000552,
            0.001104,
            0.000035,
            0.000621,
            0.001656,
            0.02898,
        ],
    },
}
PART_COUNT_PI_Q: List[float] = [1.0, 2.0]
PART_STRESS_LAMBDA_B: Dict[int, List[float]] = {
    4: [0.000041, 0.00026],
    5: [0.0026, 0.00014, 0.00026, 0.00005, 0.0000035, 0.00012, 0.000069],
}
PART_STRESS_PI_Q: Dict[int, List[float]] = {4: [1.0, 2.0], 5: [1.0, 1.0, 2.0, 20.0]}

# The environment factor lists are:
#      1. Connectors, General, MIL-SPEC [subcategory ID = 1, quality ID = 1]
#      2. Connectors, General, Lower Quality [subcategory ID = 1, quality ID = 2]
#      3. Connectors, PCB, MIL-SPEC [subcategory ID = 2, quality ID = 1]
#      4. Connectors, PCB, Lower Quality [subcategory ID = 2, quality ID = 2]
#      5. Connectors, IC Socket [subcategory ID = 3]
#      6. Interconnections, Plated Through Hole [subcategory ID = 4]
#      7. Connections, Other [subcategory ID = 5]
PI_E: Dict[int, Dict[int, List[float]] | List[float]] = {
    1: {
        1: [
            1.0,
            1.0,
            8.0,
            5.0,
            13.0,
            3.0,
            5.0,
            8.0,
            12.0,
            19.0,
            0.5,
            10.0,
            27.0,
            490.0,
        ],
        2: [
            2.0,
            5.0,
            21.0,
            10.0,
            27.0,
            12.0,
            18.0,
            17.0,
            25.0,
            37.0,
            0.8,
            20.0,
            54.0,
            970.0,
        ],
    },
    2: {
        1: [
            1.0,
            3.0,
            8.0,
            5.0,
            13.0,
            6.0,
            11.0,
            6.0,
            11.0,
            19.0,
            0.5,
            10.0,
            27.0,
            490.0,
        ],
        2: [
            2.0,
            7.0,
            17.0,
            10.0,
            26.0,
            14.0,
            22.0,
            14.0,
            22.0,
            37.0,
            0.8,
            20.0,
            54.0,
            970.0,
        ],
    },
    3: [
        1.0,
        3.0,
        14.0,
        6.0,
        18.0,
        8.0,
        12.0,
        11.0,
        13.0,
        25.0,
        0.5,
        14.0,
        36.0,
        650.0,
    ],
    4: [
        1.0,
        2.0,
        7.0,
        5.0,
        13.0,
        5.0,
        8.0,
        16.0,
        28.0,
        19.0,
        0.5,
        10.0,
        27.0,
        500.0,
    ],
    5: [
        1.0,
        2.0,
        7.0,
        4.0,
        11.0,
        4.0,
        6.0,
        6.0,
        8.0,
        16.0,
        0.5,
        9.0,
        24.0,
        420.0,
    ],
}
PI_K: List[float] = [1.0, 1.5, 2.0, 3.0, 4.0]
REF_TEMPS: Dict[int, float] = {1: 473.0, 2: 423.0, 3: 373.0, 4: 358.0, 5: 423.0}
INSERT_TEMP_FACTORS: Dict[int, float] = {
    12: 0.1,
    16: 0.274,
    20: 0.64,
    22: 0.989,
    26: 2.1,
}
LAMBDA_B_FACTORS: Dict[int, List[float]] = {
    1: [0.2, -1592.0, 5.36],
    2: [0.431, -2073.6, 4.66],
    3: [0.19, -1298.0, 4.25],
    4: [0.77, -1528.8, 4.72],
    5: [0.216, -2073.6, 4.66],
}
FACTOR_KEYS: Dict[int, Dict[int, List[int]]] = {
    1: {
        1: [2, 2, 2, 2, 2, 2],
        2: [2, 2, 2, 2, 2, 2],
        3: [1, 1, 1, 2, 2, 2, 2, 2, 2],
        4: [1, 1, 1, 2, 2, 2, 2, 2, 2],
        5: [1, 1, 1, 2, 2, 2, 2, 2, 2],
    },
    2: {
        1: [2, 2, 2, 2, 2, 2, 4, 4, 4],
        2: [1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 4, 4],
        3: [1, 1, 1, 2, 2, 2, 2, 2, 2],
        4: [1, 1, 1, 2, 2, 2, 2, 2, 2],
        5: [2, 2, 2, 2, 2, 2],
        6: [2, 2, 2, 2, 2, 2],
    },
    3: {1: [2, 2, 2, 2, 2, 2, 4, 4, 4], 2: [2, 2, 2, 2, 2, 2, 4, 4, 4]},
    4: {
        1: [3, 3],
        2: [3, 3],
        3: [3, 3],
        4: [3, 3],
        5: [3, 3],
        6: [3, 3],
        7: [3, 3],
        8: [3, 3, 2, 2, 2, 2, 2, 2],
    },
    5: {1: [3, 3, 2, 2, 2, 2, 2, 2]},
}

# Constants for GUI displays.
INSERT_A_LIST: List[List[str]] = [
    [_("Vitreous Glass")],
    [_("Alumina Ceramic")],
    [_("Polyimide")],
]
INSERT_B_LIST: List[List[str]] = [
    [_("Diallylphtalate")],
    [_("Melamine")],
    [_("Flourosilicone")],
    [_("Silicone Rubber")],
    [_("Polysulfone")],
    [_("Epoxy Resin")],
]
INSERT_C_LIST: List[List[str]] = [
    [_("Polytetraflourethylene (Teflon)")],
    [_("Chlorotriflourethylene (Kel-f)")],
]
INSERT_D_LIST: List[List[str]] = [
    [_("Polyamide (Nylon)")],
    [_("Polychloroprene (Neoprene)")],
    [_("Polyethylene")],
]
# CONNECTION_INSERT_DICT: Nested dictionary structure
# Key 1: Connection type
# Key 2: Insert type
# Value: List of insert materials
CONNECTION_INSERT_DICT: Dict[int, Dict[int, List[List[str]]]] = {
    1: {
        1: INSERT_B_LIST,
        2: INSERT_B_LIST,
        3: INSERT_A_LIST + INSERT_B_LIST,
        4: INSERT_A_LIST + INSERT_B_LIST,
        5: INSERT_A_LIST + INSERT_B_LIST,
    },
    2: {
        1: INSERT_B_LIST + INSERT_D_LIST,
        2: INSERT_A_LIST + INSERT_B_LIST + INSERT_D_LIST,
        3: INSERT_A_LIST + INSERT_B_LIST,
        4: INSERT_A_LIST + INSERT_B_LIST,
        5: INSERT_B_LIST,
        6: INSERT_B_LIST,
    },
    3: {
        1: INSERT_B_LIST + INSERT_D_LIST,
        2: INSERT_B_LIST + INSERT_D_LIST,
    },
    4: {
        1: INSERT_C_LIST,
        2: INSERT_C_LIST,
        3: INSERT_C_LIST,
        4: INSERT_C_LIST,
        5: INSERT_C_LIST,
        6: INSERT_C_LIST,
        7: INSERT_C_LIST,
        8: INSERT_B_LIST + INSERT_C_LIST,
    },
    5: {
        1: INSERT_B_LIST + INSERT_C_LIST,
    },
}
CONNECTION_QUALITY_DICT: Dict[int, List[List[str]]] = {
    1: [["MIL-SPEC"], [_("Lower")]],
    2: [["MIL-SPEC"], [_("Lower")]],
    4: [[_("MIL-SPEC or comparable IPC standards")], [_("Lower")]],
    5: [
        [_("Automated")],
        [_("Manual, Upper")],
        [_("Manual, Standard")],
        [_("Manual, Lower")],
    ],
}
CONNECTION_SPECIFICATION_DICT: Dict[int, List[List[str]]] = {
    1: [
        [_("MIL-C-24308")],
        [_("MIL-C-28748")],
        [_("MIL-C-28804")],
        [_("MIL-C-83513")],
        [_("MIL-C-83733")],
    ],
    2: [
        [_("MIL-C-5015")],
        [_("MIL-C-26482")],
        [_("MIL-C-28840")],
        [_("MIL-C-38999")],
        [_("MIL-C-81511")],
        [_("MIL-C-83723")],
    ],
    3: [[_("MIL-C-3767")], [_("MIL-C-22992")]],
    4: [
        [_("MIL-C-3607")],
        [_("MIL-C-3643")],
        [_("MIL-C-3650")],
        [_("MIL-C-3655")],
        [_("MIL-C-25516")],
        [_("MIL-C-39012")],
        [_("MIL-C-55235")],
        [_("MIL-C-55339")],
    ],
    5: [[_("MIL-C-49142")]],
}
CONNECTION_TYPE_DICT: Dict[int, List[List[str]]] = {
    1: [
        [_("Rack and Panel")],
        [_("Circular")],
        [_("Power")],
        [_("Coaxial")],
        [_("Triaxial")],
    ],
    4: [
        [_("PWA/PCB with PTHs")],
        [
            _(
                "Discrete Wiring with Electroless Deposited PTH (<3 Levels "
                "of Circuitry)"
            )
        ],
    ],  # noqa
    5: [
        [_("Hand Solder w/o Wrapping")],
        [_("Hand Solder w/ Wrapping")],
        [_("Crimp")],
        [_("Weld")],
        [_("Solderless Wrap")],
        [_("Clip Termination")],
        [_("Reflow Solder")],
    ],
}
