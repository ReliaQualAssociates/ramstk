# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.,ilhdbk217f.models.IntegratedCircuit.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp, log
from typing import Any, Dict, Tuple

ACTIVATION_ENERGY = {
    1:
    0.65,
    2: [
        0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.45, 0.45, 0.5, 0.5, 0.6, 0.6,
        0.6
    ],
    3:
    0.65,
    4:
    0.65,
    5:
    0.6,
    6:
    0.6,
    7:
    0.6,
    8:
    0.6,
    9: [1.5, 1.4],
    10:
    0.35
}
C1 = {
    1: [[0.01, 0.02, 0.04, 0.06], [0.01, 0.02, 0.04, 0.06]],
    2: [[0.0025, 0.005, 0.01, 0.02, 0.04, 0.08],
        [0.01, 0.02, 0.04, 0.08, 0.16, 0.29]],
    3: [[0.01, 0.021, 0.042], [0.00085, 0.0017, 0.0034, 0.0068]],
    4: [[0.06, 0.12, 0.24, 0.48], [0.14, 0.28, 0.56, 1.12]],
    5: [[0.00065, 0.0013, 0.0026, 0.0052], [0.0094, 0.019, 0.038, 0.075]],
    6: [[0.00085, 0.0017, 0.0034, 0.0068], [0.0, 0.0, 0.0, 0.0]],
    7: [[0.0013, 0.0025, 0.005, 0.01], [0.0, 0.0, 0.0, 0.0]],
    8: [[0.0078, 0.016, 0.031, 0.062], [0.0052, 0.011, 0.021, 0.042]],
    9: [[4.5, 7.2], [25.0, 51.0]]
}
C2 = {
    1: [2.8E-4, 1.08],
    2: [9.0E-5, 1.51],
    3: [3.0E-5, 1.82],
    4: [3.0E-5, 2.01],
    5: [3.6E-4, 1.08]
}
PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.0095, 0.024, 0.039, 0.034, 0.049, 0.057, 0.062, 0.12, 0.13,
            0.076, 0.0095, 0.044, 0.096, 1.1
        ],
        2: [
            0.0170, 0.041, 0.065, 0.054, 0.078, 0.100, 0.110, 0.22, 0.24,
            0.130, 0.0170, 0.072, 0.150, 1.4
        ],
        3: [
            0.0330, 0.074, 0.110, 0.092, 0.130, 0.190, 0.190, 0.41, 0.44,
            0.220, 0.0330, 0.120, 0.260, 2.0
        ],
        4: [
            0.0500, 0.120, 0.180, 0.150, 0.210, 0.300, 0.300, 0.63, 0.67,
            0.350, 0.0500, 0.190, 0.410, 3.4
        ]
    },
    2: {
        1: {
            1: [
                0.0036, 0.012, 0.024, 0.024, 0.035, 0.025, 0.030, 0.032, 0.049,
                0.047, 0.0036, 0.030, 0.069, 1.20
            ],
            2: [
                0.0060, 0.020, 0.038, 0.037, 0.055, 0.039, 0.048, 0.051, 0.077,
                0.074, 0.0060, 0.046, 0.110, 1.90
            ],
            3: [
                0.0110, 0.035, 0.066, 0.065, 0.097, 0.070, 0.085, 0.091, 0.140,
                0.130, 0.0110, 0.082, 0.190, 3.30
            ],
            4: [
                0.0330, 0.120, 0.220, 0.220, 0.330, 0.230, 0.280, 0.300, 0.460,
                0.440, 0.0330, 0.280, 0.650, 12.0
            ],
            5: [
                0.0520, 0.170, 0.330, 0.330, 0.480, 0.340, 0.420, 0.450, 0.680,
                0.650, 0.0520, 0.410, 0.950, 17.0
            ],
            6: [
                0.0750, 0.230, 0.440, 0.430, 0.630, 0.460, 0.560, 0.610, 0.900,
                0.850, 0.0750, 0.530, 1.200, 21.0
            ]
        },
        2: {
            1: [
                0.0057, 0.015, 0.027, 0.027, 0.039, 0.029, 0.035, 0.039, 0.056,
                0.052, 0.0057, 0.033, 0.074, 1.20
            ],
            2: [
                0.0100, 0.028, 0.045, 0.043, 0.062, 0.049, 0.057, 0.068, 0.092,
                0.083, 0.0100, 0.053, 0.120, 1.90
            ],
            3: [
                0.0190, 0.047, 0.080, 0.077, 0.110, 0.088, 0.100, 0.120, 0.170,
                0.150, 0.0190, 0.095, 0.210, 3.30
            ],
            4: [
                0.0490, 0.140, 0.250, 0.240, 0.360, 0.270, 0.320, 0.360, 0.510,
                0.480, 0.0490, 0.300, 0.690, 12.0
            ],
            5: [
                0.0840, 0.220, 0.390, 0.370, 0.540, 0.420, 0.490, 0.560, 0.790,
                0.720, 0.0840, 0.460, 1.000, 17.0
            ],
            6: [
                0.1300, 0.310, 0.530, 0.510, 0.730, 0.590, 0.690, 0.820, 1.100,
                0.980, 0.1300, 0.830, 1.400, 21.0
            ]
        }
    },
    3: {
        1: {
            1: [
                0.0061, 0.016, 0.029, 0.027, 0.040, 0.032, 0.037, 0.044, 0.061,
                0.054, 0.0061, 0.034, 0.076, 1.2
            ],
            2: [
                0.0110, 0.028, 0.048, 0.046, 0.065, 0.054, 0.063, 0.077, 0.100,
                0.089, 0.0110, 0.057, 0.120, 1.9
            ],
            3: [
                0.0220, 0.052, 0.087, 0.082, 0.120, 0.099, 0.110, 0.140, 0.190,
                0.160, 0.0220, 0.100, 0.220, 3.3
            ]
        },
        2: {
            1: [
                0.0046, 0.018, 0.035, 0.035, 0.052, 0.035, 0.044, 0.044, 0.070,
                0.070, 0.0046, 0.044, 0.100, 1.9
            ],
            2: [
                0.0056, 0.021, 0.042, 0.042, 0.062, 0.042, 0.052, 0.053, 0.084,
                0.083, 0.0056, 0.052, 0.120, 2.3
            ],
            3: [
                0.0061, 0.022, 0.043, 0.042, 0.063, 0.043, 0.054, 0.055, 0.086,
                0.084, 0.0081, 0.053, 0.130, 2.3
            ],
            4: [
                0.0095, 0.033, 0.064, 0.063, 0.094, 0.065, 0.080, 0.083, 0.130,
                0.130, 0.0095, 0.079, 0.190, 3.3
            ]
        }
    },
    4: {
        1: {
            1: [
                0.028, 0.061, 0.098, 0.091, 0.13, 0.12, 0.13, 0.17, 0.22, 0.18,
                0.028, 0.11, 0.24, 3.30
            ],
            2: [
                0.052, 0.110, 0.180, 0.160, 0.23, 0.21, 0.24, 0.32, 0.39, 0.31,
                0.052, 0.20, 0.41, 5.60
            ],
            3: [
                0.110, 0.230, 0.360, 0.330, 0.47, 0.44, 0.49, 0.65, 0.81, 0.65,
                0.110, 0.42, 0.86, 12.0
            ]
        },
        2: {
            1: [
                0.048, 0.089, 0.130, 0.120, 0.16, 0.16, 0.17, 0.24, 0.28, 0.22,
                0.048, 0.15, 0.28, 3.40
            ],
            2: [
                0.093, 0.170, 0.240, 0.220, 0.29, 0.30, 0.32, 0.45, 0.52, 0.40,
                0.093, 0.27, 0.50, 5.60
            ],
            3: [
                0.190, 0.340, 0.490, 0.450, 0.60, 0.61, 0.66, 0.90, 1.10, 0.82,
                0.190, 0.54, 1.00, 12.0
            ]
        }
    },
    5: {
        1: {
            1: [
                0.010, 0.028, 0.050, 0.046, 0.067, 0.062, 0.070, 0.10, 0.13,
                0.096, 0.010, 0.058, 0.13, 1.9
            ],
            2: [
                0.017, 0.043, 0.071, 0.063, 0.091, 0.095, 0.110, 0.18, 0.21,
                0.140, 0.017, 0.081, 0.18, 2.3
            ],
            3: [
                0.028, 0.065, 0.100, 0.085, 0.120, 0.150, 0.180, 0.30, 0.33,
                0.190, 0.028, 0.110, 0.23, 2.3
            ],
            4: [
                0.053, 0.120, 0.180, 0.150, 0.210, 0.270, 0.290, 0.56, 0.61,
                0.330, 0.053, 0.190, 0.39, 3.4
            ]
        },
        2: {
            1: [
                0.0047, 0.018, 0.036, 0.035, 0.053, 0.037, 0.045, 0.048, 0.074,
                0.071, 0.0047, 0.044, 0.11, 1.9
            ],
            2: [
                0.0059, 0.022, 0.043, 0.042, 0.063, 0.045, 0.055, 0.060, 0.090,
                0.086, 0.0059, 0.053, 0.13, 2.3
            ],
            3: [
                0.0067, 0.023, 0.045, 0.044, 0.066, 0.048, 0.059, 0.068, 0.099,
                0.089, 0.0067, 0.055, 0.13, 2.3
            ],
            4: [
                0.0110, 0.036, 0.068, 0.066, 0.098, 0.075, 0.090, 0.110, 0.150,
                0.140, 0.0110, 0.083, 0.20, 3.3
            ]
        }
    },
    6: {
        2: {
            1: [
                0.0049, 0.018, 0.036, 0.036, 0.053, 0.037, 0.046, 0.049, 0.075,
                0.072, 0.0048, 0.045, 0.11, 1.9
            ],
            2: [
                0.0061, 0.022, 0.044, 0.043, 0.064, 0.046, 0.056, 0.062, 0.093,
                0.087, 0.0062, 0.054, 0.13, 2.3
            ],
            3: [
                0.0072, 0.024, 0.048, 0.045, 0.067, 0.051, 0.061, 0.073, 0.100,
                0.092, 0.0072, 0.057, 0.13, 2.3
            ],
            4: [
                0.0120, 0.038, 0.071, 0.068, 0.100, 0.080, 0.095, 0.120, 0.180,
                0.140, 0.0120, 0.086, 0.20, 3.3
            ]
        }
    },
    7: {
        2: {
            1: [
                0.0040, 0.014, 0.027, 0.027, 0.040, 0.029, 0.035, 0.040, 0.059,
                0.055, 0.0040, 0.034, 0.080, 1.4
            ],
            2: [
                0.0055, 0.019, 0.039, 0.034, 0.051, 0.039, 0.047, 0.056, 0.079,
                0.070, 0.0055, 0.043, 0.100, 1.7
            ],
            3: [
                0.0074, 0.023, 0.043, 0.040, 0.060, 0.049, 0.058, 0.076, 0.100,
                0.084, 0.0074, 0.051, 0.120, 1.9
            ],
            4: [
                0.0110, 0.032, 0.057, 0.053, 0.077, 0.070, 0.080, 0.120, 0.150,
                0.110, 0.0110, 0.067, 0.150, 2.3
            ]
        }
    },
    8: {
        1: {
            1: [
                0.0075, 0.023, 0.043, 0.041, 0.060, 0.050, 0.058, 0.077, 0.10,
                0.084, 0.0075, 0.052, 0.12, 1.9
            ],
            2: [
                0.0120, 0.033, 0.058, 0.054, 0.079, 0.072, 0.083, 0.120, 0.15,
                0.110, 0.0120, 0.069, 0.15, 2.3
            ],
            3: [
                0.0180, 0.045, 0.074, 0.065, 0.095, 0.100, 0.110, 0.190, 0.22,
                0.140, 0.0180, 0.084, 0.18, 2.3
            ],
            4: [
                0.0330, 0.079, 0.130, 0.110, 0.160, 0.180, 0.200, 0.350, 0.39,
                0.240, 0.0330, 0.140, 0.30, 3.4
            ]
        },
        2: {
            1: [
                0.0079, 0.022, 0.038, 0.034, 0.050, 0.048, 0.054, 0.083, 0.10,
                0.073, 0.0079, 0.044, 0.098, 1.4
            ],
            2: [
                0.0140, 0.034, 0.057, 0.050, 0.073, 0.077, 0.085, 0.140, 0.17,
                0.110, 0.0140, 0.065, 0.140, 1.8
            ],
            3: [
                0.0230, 0.053, 0.084, 0.071, 0.100, 0.120, 0.130, 0.250, 0.27,
                0.160, 0.0230, 0.092, 0.190, 1.9
            ],
            4: [
                0.0430, 0.092, 0.140, 0.110, 0.160, 0.220, 0.230, 0.460, 0.49,
                0.260, 0.0430, 0.150, 0.300, 2.3
            ]
        }
    },
    9: {
        1: {
            1: [
                0.019, 0.034, 0.046, 0.039, 0.052, 0.065, 0.068, 0.11, 0.12,
                0.076, 0.019, 0.049, 0.086, 0.61
            ],
            2: [
                0.025, 0.047, 0.067, 0.058, 0.079, 0.091, 0.097, 0.15, 0.17,
                0.11, 0.025, 0.073, 0.14, 1.3
            ]
        },
        2: {
            1: [
                0.0085, 0.030, 0.057, 0.057, 0.084, 0.060, 0.073, 0.080, 0.12,
                0.11, 0.0085, 0.071, 0.17, 3.0
            ],
            2: [
                0.0140, 0.053, 0.100, 0.100, 0.150, 0.110, 0.130, 0.140, 0.22,
                0.21, 0.0140, 0.130, 0.31, 5.5
            ]
        }
    }
}
PI_A = {1: [1.0, 3.0, 3.0], 2: [1.0]}
PI_E = [
    0.5, 2.0, 4.0, 4.0, 6.0, 4.0, 5.0, 5.0, 8.0, 8.0, 0.5, 5.0, 12.0, 220.0
]
PI_PT = {1: 1.0, 7: 1.3, 2: 2.2, 8: 2.9, 3: 4.7, 9: 6.1}
PI_Q = [0.25, 1.0, 2.0]


def calculate_die_complexity_factor(area: float, feature_size: float) -> float:
    """Calculate the die complexity correction factor (piCD).

    :param area: the area of the die in sq. cm.
    :param feature_size: the size of the die features in microns.
    :return: _pi_cd; the die complexity factor.
    :rtype: float
    :raise: ZeroDivisionError if feature_size is zero.
    """
    return ((area / 0.21) * (2.0 / feature_size)**2.0 * 0.64) + 0.36


def calculate_junction_temperature(temperature_case: float,
                                   power_operating: float,
                                   theta_jc: float) -> float:
    """Calculate the junction temperature (Tj).

    :param temperature_case: the temperature of the IC case in C.
    :param power_operating: the operating power if the IC in W.
    :param theta_jc: the junction-case thermal resistance in C / W.
    :return: _t_j; the calculate junction temperature in C.
    :rtype: float
    """
    return temperature_case + power_operating * theta_jc


def calculate_lambda_cyclic_factors(
        n_cycles: int, construction_id: int, n_elements: int,
        temperature_junction: float) -> Tuple[float, float, float, float]:
    """Calculate the write cycle hazard rate A and B factors for EEPROMs.

    :param n_cycles: the expected number of lifetime write cycles.
    :param construction_id: the construction type identifier.
    :param n_elements: the number of elements (bits) in the memory device.
    :param temperature_junction: the junction temperature in C.
    :return: (_a_1, _a_2, _b_1, _b_2); the calculated factors.
    :rtype: tuple
    """
    # Calculate the A1 factor for lambda_CYC.
    _a_1 = 6.817E-6 * n_cycles

    # Find the A2, B1, and B2 factors for lambda_CYC.
    _a_2 = 0.0
    if construction_id == 1:
        _b_1 = ((n_elements / 16000.0)**0.5) * (exp(
            (-0.15 / 8.63E-5) * ((1.0 / (temperature_junction + 273.0)) -
                                 (1.0 / 333.0))))
        _b_2 = 0.0
    elif construction_id == 2:
        if 300000 < n_cycles <= 400000:
            _a_2 = 1.1
        else:
            _a_2 = 2.3

        _b_1 = ((n_elements / 64000.0)**0.25) * (exp(
            (0.1 / 8.63E-5) * ((1.0 / (temperature_junction + 273.0)) -
                               (1.0 / 303.0))))
        _b_2 = ((n_elements / 64000.0)**0.25) * (exp(
            (-0.12 / 8.63E-5) * ((1.0 / (temperature_junction + 273.0)) -
                                 (1.0 / 303.0))))
    else:
        _b_1 = 0.0
        _b_2 = 0.0

    return _a_1, _a_2, _b_1, _b_2


def calculate_temperature_factor(subcategory_id: int, family_id: int,
                                 type_id: int,
                                 temperature_junction: float) -> float:
    """Calculate the temperature factor (piT).

    :param subcategory_id: the subcategory identifier.
    :param family_id: the IC family identifier.
    :param type_id: the IC type identifier.
    :param temperature_junction: the junction temperature in C.
    :return: _pi_t; the calculated temperature factor.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID.
    :raise: IndexError if passed an unknown family ID or type ID.
    """
    if subcategory_id == 2:
        _ref_temp = 296.0
        _ea = ACTIVATION_ENERGY[subcategory_id][family_id - 1]
    elif subcategory_id == 9:
        _ref_temp = 423.0
        _ea = ACTIVATION_ENERGY[subcategory_id][type_id - 1]
    else:
        _ref_temp = 296.0
        _ea = ACTIVATION_ENERGY[subcategory_id]

    return 0.1 * exp((-_ea / 8.617E-5) * ((1.0 /
                                           (temperature_junction + 273)) -
                                          (1.0 / _ref_temp)))


def calculate_eos_hazard_rate(voltage_esd: float) -> float:
    """Calculate the electrical overstress hazard rate (lambdaEOS).

    :param voltage_esd: the ESD withstand voltage.
    :return: _lambda_eos; the electrical overstress hazard rate.
    :rtype: float
    """
    return (-log(1.0 - 0.00057 * exp(-0.0002 * voltage_esd))) / 0.00876


def calculate_package_base_hazard_rate(n_active_pins: int) -> float:
    """Calculate the package base hazard rate (lambdaBP).

    :param n_active_pins: the number of active (current carrying) pins.
    :return: _lambda_bd; the calculated package base hazard rate.
    :rtype: float
    """
    return 0.0022 + (1.72E-5 * n_active_pins)


def calculate_package_factor(package_id: int, n_active_pins: int) -> float:
    """Calculate the package factor (C2).

    :param package_id: the package type identifier.
    :param n_active_pins: the number of active (current carying) pins in
        the application.
    :result: _c2; the calculated package factor.
    :rtype: float
    """
    if package_id in [1, 2, 3]:
        _package = 1
    elif package_id == 4:
        _package = 2
    elif package_id == 5:
        _package = 3
    elif package_id == 6:
        _package = 4
    else:
        _package = 5

    _f0 = C2[_package][0]
    _f1 = C2[_package][1]

    return _f0 * (n_active_pins**_f1)


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param attributes: the attributes for the integrated circuit being
        calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(attributes['n_elements'],
                                   id_keys={
                                       'subcategory_id':
                                       attributes['subcategory_id'],
                                       'environment_active_id':
                                       attributes['environment_active_id'],
                                       'technology_id':
                                       attributes['technology_id']
                                   })


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress active hazard rate for a integrated circuit.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values.
    :rtype: dict
    """
    attributes['temperature_junction'] = calculate_junction_temperature(
        attributes['temperature_case'], attributes['power_operating'],
        attributes['theta_jc'])
    attributes['piT'] = calculate_temperature_factor(
        attributes['subcategory_id'], attributes['family_id'],
        attributes['type_id'], attributes['temperature_junction'])
    attributes['piL'] = 0.01 * exp(5.35
                                   - 0.35 * attributes['years_in_production'])

    if attributes['subcategory_id'] in [1, 2, 3, 4]:
        attributes['C1'] = get_die_complexity_factor(
            attributes['subcategory_id'], attributes['technology_id'],
            attributes['application_id'], attributes['n_elements'])
        attributes['C2'] = calculate_package_factor(
            attributes['package_id'], attributes['n_active_pins'])
        attributes['hazard_rate_active'] = (
            (attributes['C1'] * attributes['piT']
             + attributes['C2'] * attributes['piE']) * attributes['piQ']
            * attributes['piL'])
    elif attributes['subcategory_id'] in [5, 6, 7, 8]:
        attributes['C1'] = get_die_complexity_factor(
            attributes['subcategory_id'], attributes['technology_id'],
            attributes['application_id'], attributes['n_elements'])
        attributes['C2'] = calculate_package_factor(
            attributes['package_id'], attributes['n_active_pins'])
        if attributes['subcategory_id'] == 6:
            attributes['piECC'] = get_error_correction_factor(
                attributes['type_id'])
            (_a_1, _a_2, _b_1, _b_2) = calculate_lambda_cyclic_factors(
                attributes['n_cycles'], attributes['construction_id'],
                attributes['n_elements'], attributes['temperature_junction'])
            attributes['lambda_cyc'] = ((_a_1 * _b_1 +
                                         (_a_2 * _b_2 / attributes['piQ']))
                                        * attributes['piECC'])
        else:
            attributes['lambda_cyc'] = 0.0

        attributes['hazard_rate_active'] = (
            (attributes['C1'] * attributes['piT']
             + attributes['C2'] * attributes['piE'] + attributes['lambda_cyc'])
            * attributes['piQ'] * attributes['piL'])

    elif attributes['subcategory_id'] == 9:
        attributes['C1'] = get_die_complexity_factor(
            attributes['subcategory_id'], attributes['technology_id'],
            attributes['application_id'], attributes['n_elements'])
        attributes['C2'] = calculate_package_factor(
            attributes['package_id'], attributes['n_active_pins'])
        attributes['piA'] = get_application_factor(
            attributes['type_id'], attributes['application_id'])
        attributes['hazard_rate_active'] = (
            (attributes['C1'] * attributes['piT'] * attributes['piA']
             + attributes['C2'] * attributes['piE']) * attributes['piQ']
            * attributes['piL'])
    elif attributes['subcategory_id'] == 10:
        attributes['lambdaBD'] = get_die_base_hazard_rate(
            attributes['type_id'])
        attributes['lambdaBP'] = calculate_package_base_hazard_rate(
            attributes['n_active_pins'])
        attributes['lambdaEOS'] = calculate_eos_hazard_rate(
            attributes['voltage_esd'])
        attributes['piCD'] = calculate_die_complexity_factor(
            attributes['area'], attributes['feature_size'])
        attributes['piMFG'] = get_manufacturing_process_factor(
            attributes['manufacturing_id'])
        attributes['piPT'] = get_package_type_correction_factor(
            attributes['package_id'])

        attributes['hazard_rate_active'] = (
            attributes['lambdaBD'] * attributes['piMFG'] * attributes['piT']
            * attributes['piCD'] + attributes['lambdaBP'] * attributes['piE']
            * attributes['piQ'] * attributes['piPT'] + attributes['lambdaEOS'])

    return attributes


def get_application_factor(type_id: int, application_id: int) -> float:
    """Retrieve the application factor (piA).

    :param type_id: the IC type identifier.
    :param application_id: the IC application identifier.
    :return: _pi_a; the retrieved application factor.
    :rtype: float
    :raise: IndexError if passed an unknown application ID.
    :raise: KeyError if passed an unknown type ID.
    """
    return PI_A[type_id][application_id - 1]


def get_die_complexity_factor(subcategory_id: int, technology_id: int,
                              application_id: int, n_elements: int) -> float:
    """Retrieve the die complexity hazard rate (C1).

    :param subcategory_id: the subcategory identifier.
    :param technology_id: the technology identifier.
    :param application_id: the application identifier.
    :param n_elements: the number of elements (transistors/gates) in the
        device.
    :return: _c1; the selected die complexity factor.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID, technology ID, or
        application ID.
    :raise: ValueError if passed a number of elements not associated with the
        breakpoints in MIL-HDBK-217F.
    """
    _dic_breakpoints = {
        1: [100, 300, 1000, 10000],
        2: [100, 1000, 3000, 10000, 30000, 60000],
        3: {
            1: [200, 1000, 5000],
            2: [16000, 64000, 256000, 1000000],
        },
        4: [8, 16, 32],
        5: [16000, 64000, 256000, 100000],
        6: [16000, 64000, 256000, 100000],
        7: [16000, 64000, 256000, 100000],
        8: [16000, 64000, 256000, 100000],
        9: {
            1: [10, 1000],
            2: [1000, 10000]
        }
    }

    if subcategory_id == 2 and technology_id == 11:
        _technology = 2
    elif subcategory_id == 2 and technology_id != 11:
        _technology = 1
    else:
        _technology = technology_id

    if subcategory_id == 3:
        _lst_index = _dic_breakpoints[subcategory_id][_technology]
    elif subcategory_id == 9:
        _lst_index = _dic_breakpoints[subcategory_id][application_id]
    else:
        _lst_index = _dic_breakpoints[subcategory_id]

    # This will retrieve the breakpoint value for the number of elements
    # closest (round up) to the number of elements passed.
    _index = min(range(len(_lst_index)),
                 key=lambda i: abs(_lst_index[i] - n_elements))

    return C1[subcategory_id][_technology - 1][_index]


def get_die_base_hazard_rate(type_id: int) -> float:
    """Retrieve the base hazard rate for a VHISC/VLSI die.

    :param type_id: the VHISC/VLSI type identifier.
    :return: _lambda_bd; the base die hazard rate.
    :rtype: float
    """
    if type_id == 1:
        _lambda_bd = 0.16
    else:
        _lambda_bd = 0.24

    return _lambda_bd


def get_error_correction_factor(type_id: int) -> float:
    """Retrieve the error code correction factor (piECC).

    :param type_id: the error correction type identifier.
    :return: _pi_ecc; the value of piECC.
    :rtype: float
    :raise: KeyError if passed an unknown type_id.
    """
    return {1: 1.0, 2: 0.72, 3: 0.68}[type_id]


def get_manufacturing_process_factor(manufacturing_id: int) -> float:
    """Retrive teh the manufacturing process correction factor (piMFG).

    :param manufacturing_id: the manufacturing process identifier.
    :return: _pi_mfg; the manufacturing process correction factor.
    :rtype: float
    """
    if manufacturing_id == 1:
        _pi_mfg = 0.55
    else:
        _pi_mfg = 2.0

    return _pi_mfg


def get_package_type_correction_factor(package_id: int) -> float:
    """Retrieve the package type correction factor (piPT).

    :param package_id: the package type identifier.
    :return: _pi_pt; the package type correction factor.
    :rtype: float
    :raise: KeyError if passed an unknown package ID.
    """
    return PI_PT[package_id]


def get_part_count_lambda_b(n_elements: int, id_keys: Dict[str, int]) -> float:
    """Calculate parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. technology id; if the IC subcategory is NOT technology dependent,
            then the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |       Integrated Circuit      | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Linear                        |        5.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Logic                         |        5.1      |
    +----------------+-------------------------------+-----------------+
    |        3       | PAL/PLA                       |        5.1      |
    +----------------+-------------------------------+-----------------+
    |        4       | Microprocessor/Microcontroller|        5.1      |
    +----------------+-------------------------------+-----------------+
    |        5       | Memory, ROM                   |        5.2      |
    +----------------+-------------------------------+-----------------+
    |        6       | Memory, EEPROM                |        5.2      |
    +----------------+-------------------------------+-----------------+
    |        7       | Memory, DRAM                  |        5.2      |
    +----------------+-------------------------------+-----------------+
    |        8       | Memory, SRAM                  |        5.2      |
    +----------------+-------------------------------+-----------------+
    |        9       | GaAS                          |        5.4      |
    +----------------+-------------------------------+-----------------+
    |       10       | VHSIC/VLSI                    |        5.3      |
    +----------------+-------------------------------+-----------------+

    :param n_elements: the number of elements (transistors/gates) in the
        device.
    :param id_keys: the ID's used as keys when selecting
        the base hazard rate.  The keys are subcategory_id,
        environment_active_id, and technology_id.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    :raise: KeyError if passed an unknown subcategory ID or technology ID
        (where used).
    :raise: ValueError if passed a number of elements not associated with the
        breakpoints in MIL-HDBK-217F.
    """
    # Dictionary containing the number of element breakpoints for determining
    # the base hazard rate list to use.
    _dic_breakpoints = {
        1: [100, 300, 1000, 10000],
        2: [100, 1000, 3000, 10000, 30000, 60000],
        3: {
            1: [200, 1000, 5000],
            2: [16000, 64000, 256000, 1000000]
        },
        4: [8, 16, 32],
        5: [16000, 64000, 256000, 100000],
        6: [16000, 64000, 256000, 100000],
        7: [16000, 64000, 256000, 100000],
        8: [16000, 64000, 256000, 100000],
        9: {
            1: [10, 100],
            2: [1000, 10000]
        }
    }

    if id_keys['subcategory_id'] in [3, 9]:
        _index = _dic_breakpoints[id_keys['subcategory_id']][
            id_keys['technology_id']].index(n_elements) + 1
    else:
        _lst_index = _dic_breakpoints[id_keys['subcategory_id']]
        _index = min(range(len(_lst_index)),
                     key=lambda i: abs(_lst_index[i] - n_elements)) + 1

    if id_keys['subcategory_id'] == 1:
        _base_hr = PART_COUNT_LAMBDA_B[id_keys['subcategory_id']][_index][
            id_keys['environment_active_id'] - 1]
    else:
        _base_hr = PART_COUNT_LAMBDA_B[id_keys['subcategory_id']][
            id_keys['technology_id']][_index][id_keys['environment_active_id']
                                              - 1]

    return _base_hr
