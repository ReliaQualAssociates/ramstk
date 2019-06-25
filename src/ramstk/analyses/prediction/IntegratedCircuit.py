# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.IntegratedCircuit.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Reliability Calculations Module."""

# Standard Library Imports
from math import exp, log

ACTIVATION_ENERGY = {
    1:
    0.65,
    2: [
        0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.45, 0.45, 0.5, 0.5, 0.6,
        0.6, 0.6,
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
}
PART_COUNT_217F_LAMBDA_B = {
    1: {
        1: {
            1: [
                0.0095, 0.024, 0.039, 0.034, 0.049, 0.057, 0.062, 0.12,
                0.13, 0.076, 0.0095, 0.044, 0.096, 1.1,
            ],
            2: [
                0.0170, 0.041, 0.065, 0.054, 0.078, 0.100, 0.110, 0.22,
                0.24, 0.130, 0.0170, 0.072, 0.150, 1.4,
            ],
            3: [
                0.0330, 0.074, 0.110, 0.092, 0.130, 0.190, 0.190, 0.41,
                0.44, 0.220, 0.0330, 0.120, 0.260, 2.0,
            ],
            4: [
                0.0500, 0.120, 0.180, 0.150, 0.210, 0.300, 0.300, 0.63,
                0.67, 0.350, 0.0500, 0.190, 0.410, 3.4,
            ],
        },
        2: {
            1: [
                0.0095, 0.024, 0.039, 0.034, 0.049, 0.057, 0.062, 0.12,
                0.13, 0.076, 0.0095, 0.044, 0.096, 1.1,
            ],
            2: [
                0.0170, 0.041, 0.065, 0.054, 0.078, 0.100, 0.110, 0.22,
                0.24, 0.130, 0.0170, 0.072, 0.150, 1.4,
            ],
            3: [
                0.0330, 0.074, 0.110, 0.092, 0.130, 0.190, 0.190, 0.41,
                0.44, 0.220, 0.0330, 0.120, 0.260, 2.0,
            ],
            4: [
                0.0500, 0.120, 0.180, 0.150, 0.210, 0.300, 0.300, 0.63,
                0.67, 0.350, 0.0500, 0.190, 0.410, 3.4,
            ],
        },
    },
    2: {
        1: {
            1: [
                0.0036, 0.012, 0.024, 0.024, 0.035, 0.025, 0.030, 0.032,
                0.049, 0.047, 0.0036, 0.030, 0.069, 1.20,
            ],
            2: [
                0.0060, 0.020, 0.038, 0.037, 0.055, 0.039, 0.048, 0.051,
                0.077, 0.074, 0.0060, 0.046, 0.110, 1.90,
            ],
            3: [
                0.0110, 0.035, 0.066, 0.065, 0.097, 0.070, 0.085, 0.091,
                0.140, 0.130, 0.0110, 0.082, 0.190, 3.30,
            ],
            4: [
                0.0330, 0.120, 0.220, 0.220, 0.330, 0.230, 0.280, 0.300,
                0.460, 0.440, 0.0330, 0.280, 0.650, 12.0,
            ],
            5: [
                0.0520, 0.170, 0.330, 0.330, 0.480, 0.340, 0.420, 0.450,
                0.680, 0.650, 0.0520, 0.410, 0.950, 17.0,
            ],
            6: [
                0.0750, 0.230, 0.440, 0.430, 0.630, 0.460, 0.560, 0.610,
                0.900, 0.850, 0.0750, 0.530, 1.200, 21.0,
            ],
        },
        2: {
            1: [
                0.0057, 0.015, 0.027, 0.027, 0.039, 0.029, 0.035, 0.039,
                0.056, 0.052, 0.0057, 0.033, 0.074, 1.20,
            ],
            2: [
                0.0100, 0.028, 0.045, 0.043, 0.062, 0.049, 0.057, 0.068,
                0.092, 0.083, 0.0100, 0.053, 0.120, 1.90,
            ],
            3: [
                0.0190, 0.047, 0.080, 0.077, 0.110, 0.088, 0.100, 0.120,
                0.170, 0.150, 0.0190, 0.095, 0.210, 3.30,
            ],
            4: [
                0.0490, 0.140, 0.250, 0.240, 0.360, 0.270, 0.320, 0.360,
                0.510, 0.480, 0.0490, 0.300, 0.690, 12.0,
            ],
            5: [
                0.0840, 0.220, 0.390, 0.370, 0.540, 0.420, 0.490, 0.560,
                0.790, 0.720, 0.0840, 0.460, 1.000, 17.0,
            ],
            6: [
                0.1300, 0.310, 0.530, 0.510, 0.730, 0.590, 0.690, 0.820,
                1.100, 0.980, 0.1300, 0.830, 1.400, 21.0,
            ],
        },
    },
    3: {
        1: {
            1: [
                0.0061, 0.016, 0.029, 0.027, 0.040, 0.032, 0.037, 0.044,
                0.061, 0.054, 0.0061, 0.034, 0.076, 1.2,
            ],
            2: [
                0.0110, 0.028, 0.048, 0.046, 0.065, 0.054, 0.063, 0.077,
                0.100, 0.089, 0.0110, 0.057, 0.120, 1.9,
            ],
            3: [
                0.0220, 0.052, 0.087, 0.082, 0.120, 0.099, 0.110, 0.140,
                0.190, 0.160, 0.0220, 0.100, 0.220, 3.3,
            ],
        },
        2: {
            1: [
                0.0046, 0.018, 0.035, 0.035, 0.052, 0.035, 0.044, 0.044,
                0.070, 0.070, 0.0046, 0.044, 0.100, 1.9,
            ],
            2: [
                0.0056, 0.021, 0.042, 0.042, 0.062, 0.042, 0.052, 0.053,
                0.084, 0.083, 0.0056, 0.052, 0.120, 2.3,
            ],
            3: [
                0.0061, 0.022, 0.043, 0.042, 0.063, 0.043, 0.054, 0.055,
                0.086, 0.084, 0.0081, 0.053, 0.130, 2.3,
            ],
            4: [
                0.0095, 0.033, 0.064, 0.063, 0.094, 0.065, 0.080, 0.083,
                0.130, 0.130, 0.0095, 0.079, 0.190, 3.3,
            ],
        },
    },
    4: {
        1: {
            1: [
                0.028, 0.061, 0.098, 0.091, 0.13, 0.12, 0.13, 0.17, 0.22,
                0.18, 0.028, 0.11, 0.24, 3.30,
            ],
            2: [
                0.052, 0.110, 0.180, 0.160, 0.23, 0.21, 0.24, 0.32, 0.39,
                0.31, 0.052, 0.20, 0.41, 5.60,
            ],
            3: [
                0.110, 0.230, 0.360, 0.330, 0.47, 0.44, 0.49, 0.65, 0.81,
                0.65, 0.110, 0.42, 0.86, 12.0,
            ],
        },
        2: {
            1: [
                0.048, 0.089, 0.130, 0.120, 0.16, 0.16, 0.17, 0.24, 0.28,
                0.22, 0.048, 0.15, 0.28, 3.40,
            ],
            2: [
                0.093, 0.170, 0.240, 0.220, 0.29, 0.30, 0.32, 0.45, 0.52,
                0.40, 0.093, 0.27, 0.50, 5.60,
            ],
            3: [
                0.190, 0.340, 0.490, 0.450, 0.60, 0.61, 0.66, 0.90, 1.10,
                0.82, 0.190, 0.54, 1.00, 12.0,
            ],
        },
    },
    5: {
        1: {
            1: [
                0.010, 0.028, 0.050, 0.046, 0.067, 0.062, 0.070, 0.10,
                0.13, 0.096, 0.010, 0.058, 0.13, 1.9,
            ],
            2: [
                0.017, 0.043, 0.071, 0.063, 0.091, 0.095, 0.110, 0.18,
                0.21, 0.140, 0.017, 0.081, 0.18, 2.3,
            ],
            3: [
                0.028, 0.065, 0.100, 0.085, 0.120, 0.150, 0.180, 0.30,
                0.33, 0.190, 0.028, 0.110, 0.23, 2.3,
            ],
            4: [
                0.053, 0.120, 0.180, 0.150, 0.210, 0.270, 0.290, 0.56,
                0.61, 0.330, 0.053, 0.190, 0.39, 3.4,
            ],
        },
        2: {
            1: [
                0.0047, 0.018, 0.036, 0.035, 0.053, 0.037, 0.045, 0.048,
                0.074, 0.071, 0.0047, 0.044, 0.11, 1.9,
            ],
            2: [
                0.0059, 0.022, 0.043, 0.042, 0.063, 0.045, 0.055, 0.060,
                0.090, 0.086, 0.0059, 0.053, 0.13, 2.3,
            ],
            3: [
                0.0067, 0.023, 0.045, 0.044, 0.066, 0.048, 0.059, 0.068,
                0.099, 0.089, 0.0067, 0.055, 0.13, 2.3,
            ],
            4: [
                0.0110, 0.036, 0.068, 0.066, 0.098, 0.075, 0.090, 0.110,
                0.150, 0.140, 0.0110, 0.083, 0.20, 3.3,
            ],
        },
    },
    6: {
        2: {
            1: [
                0.0049, 0.018, 0.036, 0.036, 0.053, 0.037, 0.046, 0.049,
                0.075, 0.072, 0.0048, 0.045, 0.11, 1.9,
            ],
            2: [
                0.0061, 0.022, 0.044, 0.043, 0.064, 0.046, 0.056, 0.062,
                0.093, 0.087, 0.0062, 0.054, 0.13, 2.3,
            ],
            3: [
                0.0072, 0.024, 0.048, 0.045, 0.067, 0.051, 0.061, 0.073,
                0.100, 0.092, 0.0072, 0.057, 0.13, 2.3,
            ],
            4: [
                0.0120, 0.038, 0.071, 0.068, 0.100, 0.080, 0.095, 0.120,
                0.180, 0.140, 0.0120, 0.086, 0.20, 3.3,
            ],
        },
    },
    7: {
        2: {
            1: [
                0.0040, 0.014, 0.027, 0.027, 0.040, 0.029, 0.035, 0.040,
                0.059, 0.055, 0.0040, 0.034, 0.080, 1.4,
            ],
            2: [
                0.0055, 0.019, 0.039, 0.034, 0.051, 0.039, 0.047, 0.056,
                0.079, 0.070, 0.0055, 0.043, 0.100, 1.7,
            ],
            3: [
                0.0074, 0.023, 0.043, 0.040, 0.060, 0.049, 0.058, 0.076,
                0.100, 0.084, 0.0074, 0.051, 0.120, 1.9,
            ],
            4: [
                0.0110, 0.032, 0.057, 0.053, 0.077, 0.070, 0.080, 0.120,
                0.150, 0.110, 0.0110, 0.067, 0.150, 2.3,
            ],
        },
    },
    8: {
        1: {
            1: [
                0.0075, 0.023, 0.043, 0.041, 0.060, 0.050, 0.058, 0.077,
                0.10, 0.084, 0.0075, 0.052, 0.12, 1.9,
            ],
            2: [
                0.0120, 0.033, 0.058, 0.054, 0.079, 0.072, 0.083, 0.120,
                0.15, 0.110, 0.0120, 0.069, 0.15, 2.3,
            ],
            3: [
                0.0180, 0.045, 0.074, 0.065, 0.095, 0.100, 0.110, 0.190,
                0.22, 0.140, 0.0180, 0.084, 0.18, 2.3,
            ],
            4: [
                0.0330, 0.079, 0.130, 0.110, 0.160, 0.180, 0.200, 0.350,
                0.39, 0.240, 0.0330, 0.140, 0.30, 3.4,
            ],
        },
        2: {
            1: [
                0.0079, 0.022, 0.038, 0.034, 0.050, 0.048, 0.054, 0.083,
                0.10, 0.073, 0.0079, 0.044, 0.098, 1.4,
            ],
            2: [
                0.0140, 0.034, 0.057, 0.050, 0.073, 0.077, 0.085, 0.140,
                0.17, 0.110, 0.0140, 0.065, 0.140, 1.8,
            ],
            3: [
                0.0230, 0.053, 0.084, 0.071, 0.100, 0.120, 0.130, 0.250,
                0.27, 0.160, 0.0230, 0.092, 0.190, 1.9,
            ],
            4: [
                0.0430, 0.092, 0.140, 0.110, 0.160, 0.220, 0.230, 0.460,
                0.49, 0.260, 0.0430, 0.150, 0.300, 2.3,
            ],
        },
    },
    9: {
        1: {
            1: [
                0.019, 0.034, 0.046, 0.039, 0.052, 0.065, 0.068, 0.11,
                0.12, 0.076, 0.019, 0.049, 0.086, 0.61,
            ],
            2: [
                0.025, 0.047, 0.067, 0.058, 0.079, 0.091, 0.097, 0.15,
                0.17, 0.11, 0.025, 0.073, 0.14, 1.3,
            ],
        },
        2: {
            1: [
                0.0085, 0.030, 0.057, 0.057, 0.084, 0.060, 0.073, 0.080,
                0.12, 0.11, 0.0085, 0.071, 0.17, 3.0,
            ],
            2: [
                0.0140, 0.053, 0.100, 0.100, 0.150, 0.110, 0.130, 0.140,
                0.22, 0.21, 0.0140, 0.130, 0.31, 5.5,
            ],
        },
    },
}
C1 = {
    1: [[0.01, 0.02, 0.04, 0.06], [0.01, 0.02, 0.04, 0.06]],
    2: [
        [0.0025, 0.005, 0.01, 0.02, 0.04, 0.08],
        [0.01, 0.02, 0.04, 0.08, 0.16, 0.29],
    ],
    3: [[0.01, 0.021, 0.042], [0.00085, 0.0017, 0.0034, 0.0068]],
    4: [[0.06, 0.12, 0.24, 0.48], [0.14, 0.28, 0.56, 1.12]],
    5: [[0.00065, 0.0013, 0.0026, 0.0052], [0.0094, 0.019, 0.038, 0.075]],
    6: [[0.00085, 0.0017, 0.0034, 0.0068], [0.0, 0.0, 0.0, 0.0]],
    7: [[0.0013, 0.0025, 0.005, 0.01], [0.0, 0.0, 0.0, 0.0]],
    8: [[0.0078, 0.016, 0.031, 0.062], [0.0052, 0.011, 0.021, 0.042]],
    9: [[4.5, 7.2], [25.0, 51.0]],
}
C2 = {
    1: [2.8E-4, 1.08],
    2: [9.0E-5, 1.51],
    3: [3.0E-5, 1.82],
    4: [3.0E-5, 2.01],
    5: [3.6E-4, 1.08],
}
PI_A = {1: [1.0, 3.0, 3.0], 2: [1.0]}
PI_PT = {1: 1.0, 7: 1.3, 2: 2.2, 8: 2.9, 3: 4.7, 9: 6.1}


def _calculate_package_hazard_rate(attributes):
    """Calculate the package hazard rate (C2)."""
    if attributes['package_id'] in [1, 2, 3]:
        _package = 1
    elif attributes['package_id'] == 4:
        _package = 2
    elif attributes['package_id'] == 5:
        _package = 3
    elif attributes['package_id'] == 6:
        _package = 4
    else:
        _package = 5

    try:
        _f0 = C2[_package][0]
        _f1 = C2[_package][1]
        attributes['C2'] = _f0 * (attributes['n_active_pins']**_f1)
    except KeyError:
        attributes['C2'] = 0.0

    return attributes


def _calculate_die_complexity_hazard_rate(attributes):
    """Calculate the die complexity hazard rate (C1)."""
    _dic_breakpoints = {
        1: [100, 300, 1000],
        2: [100, 1000, 3000, 10000, 30000],
        3: {
            1: [200, 1000],
            2: [500, 1000, 5000],
        },
        4: [8, 16, 32],
        5: [16000, 64000, 256000],
        6: [16000, 64000, 256000],
        7: [16000, 64000, 256000],
        8: [16000, 64000, 256000],
        9: {
            1: [
                100, 1000,
            ],
            2: [
                1000, 10000,
            ],
        },
    }

    # Categorize the technology.
    if attributes['subcategory_id'] == 2 and attributes['technology_id'] == 11:
        _technology = 2
    elif (
            attributes['subcategory_id'] == 2
            and attributes['technology_id'] != 11
    ):
        _technology = 1
    else:
        _technology = attributes['technology_id']

    try:
        if attributes['subcategory_id'] == 3:
            _index = _dic_breakpoints[attributes['subcategory_id']][
                _technology
            ].index(attributes['n_elements'])
        if attributes['subcategory_id'] == 9:
            _index = _dic_breakpoints[attributes['subcategory_id']][
                attributes['application_id']
            ].index(attributes['n_elements'])
        else:
            _index = _dic_breakpoints[
                attributes['subcategory_id']
            ].index(attributes['n_elements'])

        attributes['C1'] = C1[attributes['subcategory_id']][
            _technology - 1
        ][_index]

    except(KeyError, ValueError):
        attributes['C1'] = 0.0

    return attributes


def _calculate_lambda_cyclic(**attributes):
    """Calculate the write cycle hazard rate for EEPROMs."""
    attributes = _get_error_correction_factor(attributes)

    # Calculate the A1 factor for lambda_CYC.
    attributes['A1'] = 6.817E-6 * attributes['n_cycles']

    # Find the A2, B1, and B2 factors for lambda_CYC.
    attributes['A2'] = 0.0
    if attributes['construction_id'] == 1:
        attributes['B1'] = ((attributes['n_elements'] / 16000.0)**0.5) * (
            exp(
                (-0.15 / 8.63E-5) * (
                    (1.0 / (attributes['temperature_junction'] + 273.0))
                    - (1.0 / 333.0)
                ),
            )
        )
        attributes['B2'] = 0.0
    elif attributes['construction_id'] == 2:
        if (
                attributes['n_cycles'] > 300000
                and attributes['n_cycles'] <= 400000
        ):
            attributes['A2'] = 1.1
        else:
            attributes['A2'] = 2.3

        attributes['B1'] = ((attributes['n_elements'] / 64000.0)**0.25) * (
            exp(
                (0.1 / 8.63E-5) * (
                    (1.0 / (attributes['temperature_junction'] + 273.0))
                    - (1.0 / 303.0)
                ),
            )
        )
        attributes['B2'] = ((attributes['n_elements'] / 64000.0)**0.25) * (
            exp(
                (-0.12 / 8.63E-5) * (
                    (1.0 / (attributes['temperature_junction'] + 273.0))
                    - (1.0 / 303.0)
                ),
            )
        )
    else:
        attributes['B1'] = 0.0
        attributes['B2'] = 0.0

    if attributes['subcategory_id'] == 6:
        attributes['lambda_cyc'] = (
            (
                attributes['A1'] * attributes['B1']
                + (attributes['A2'] * attributes['B2'] / attributes['piQ'])
            ) * attributes['piECC']
        )
    else:
        attributes['lambda_cyc'] = 0.0

    return attributes


def _calculate_temperature_factor(**attributes):
    """Calculate the temperature factor."""
    if attributes['subcategory_id'] == 2:
        _ref_temp = 296.0
        _ea = ACTIVATION_ENERGY[attributes['subcategory_id']][
            attributes['family_id'] - 1
        ]
    elif attributes['subcategory_id'] == 9:
        _ref_temp = 423.0
        _ea = ACTIVATION_ENERGY[
            attributes['subcategory_id']
        ][
            attributes['type_id'] - 1
        ]
    else:
        _ref_temp = 296.0
        try:
            _ea = ACTIVATION_ENERGY[attributes['subcategory_id']]
        except KeyError:
            _ea = 0.0
    attributes['temperature_junction'] = (
        attributes['temperature_case'] +
        attributes['power_operating'] * attributes['theta_jc']
    )
    attributes['piT'] = 0.1 * exp((-_ea / 8.617E-5) * (
        (1.0 / (attributes['temperature_junction'] + 273))
        - (1.0 / _ref_temp)
    ))

    return attributes


def _calculate_vhisc_vlsi_variables(attributes):
    """Calculate the extra variables for VHSIC/VLSI integrated circuits."""
    # Determine the die base hazard rate.
    if attributes['type_id'] == 1:
        attributes['lambdaBD'] = 0.16
    else:
        attributes['lambdaBD'] = 0.24

    # Determine the manufacturing process correction factor (piMFG).
    if attributes['manufacturing_id'] == 1:
        attributes['piMFG'] = 0.55
    else:
        attributes['piMFG'] = 2.0

    # Calculate the die complexity correction factor.
    attributes['piCD'] = (
        (attributes['area'] / 0.21)
        * (2.0 / attributes['feature_size'])**2.0 * 0.64
    ) + 0.36

    # Determine the package type correction factor (piPT).
    try:
        attributes['piPT'] = PI_PT[attributes['package_id']]
    except KeyError:
        attributes['piPT'] = 1.0

    # Calculate the package base hazard rate.
    attributes[
        'lambdaBP'
    ] = 0.0022 + (1.72E-5 * attributes['n_active_pins'])

    # Calculate the electrical overstress hazard rate.
    attributes['lambdaEOS'] = (
        -log(1.0 - 0.00057 * exp(-0.0002 * attributes['voltage_esd']))
    ) / 0.00876

    return attributes


def _get_error_correction_factor(attributes):
    """Retrieve the error code correction factor (piECC) for."""
    if attributes['type_id'] == 1:
        attributes['piECC'] = 1.0
    elif attributes['type_id'] == 2:
        attributes['piECC'] = 0.72
    elif attributes['type_id'] == 3:
        attributes['piECC'] = 0.68
    else:
        attributes['piECC'] = 0.0

    return attributes


def calculate_217f_part_count_lambda_b(attributes):
    r"""
    Calculate the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. technology id; if the IC subcategory is NOT technology dependent,
            then the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory \  |       Integrated Circuit \    | MIL-HDBK-217F \ |
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

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param dict attributes: the attributes for the crystal being calculated.
    :return: _lst_base_hr; the list of base hazard rates.
    :rtype: list
    """
    # Dictionary containing the number of element breakpoints for determining
    # the base hazard rate list to use.
    _dic_breakpoints = {
        1: [100, 300, 1000],
        2: [100, 1000, 3000, 10000, 30000],
        3: {
            1: [200, 1000],
            2: [16000, 64000, 256000],
        },
        4: [8, 16, 32],
        5: [16000, 64000, 256000],
        6: [16000, 64000, 256000],
        7: [16000, 64000, 256000],
        8: [16000, 64000, 256000],
        9: {
            1: [
                10,
            ],
            2: [
                1000,
            ],
        },
    }

    try:
        if attributes['subcategory_id'] in [3, 9]:
            _breaks = _dic_breakpoints[attributes['subcategory_id']][
                attributes['technology_id']
            ]
        else:
            _breaks = _dic_breakpoints[attributes['subcategory_id']]

        _idx = -1
        for _idx, _value in enumerate(_breaks):
            _diff = _value - attributes['n_elements']
            if len(_breaks) == 1 and _diff < 0:
                _idx += 1
                break
            elif _diff >= 0:
                break

        _index = _idx + 1
        _lst_base_hr = PART_COUNT_217F_LAMBDA_B[attributes['subcategory_id']][
            attributes[
                'technology_id'
            ]
        ][_index]
    except KeyError:
        _lst_base_hr = [0.0]

    return _lst_base_hr


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a integrated circuit.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
        dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_die_complexity_hazard_rate(attributes)
    attributes = _calculate_package_hazard_rate(attributes)
    attributes = _calculate_temperature_factor(**attributes)
    attributes[
        'piL'
    ] = 0.01 * exp(5.35 - 0.35 * attributes['years_in_production'])
    try:
        attributes['piA'] = PI_A[attributes['type_id']][
            attributes['application_id'] - 1
        ]
    except(IndexError, KeyError):
        attributes['piA'] = 0.0

    _msg = do_check_variables(attributes)

    if attributes['subcategory_id'] in [1, 2, 3, 4]:
        attributes['hazard_rate_active'] = (
            (
                attributes['C1'] * attributes['piT'] + attributes['C2']
                * attributes['piE']
            ) * attributes['piQ'] * attributes['piL']
        )
    elif attributes['subcategory_id'] in [5, 6, 7, 8]:
        attributes = _calculate_lambda_cyclic(**attributes)
        attributes['hazard_rate_active'] = (
            (
                attributes['C1'] * attributes['piT']
                + attributes['C2'] * attributes['piE']
                + attributes['lambda_cyc']
            ) * attributes['piQ'] * attributes['piL']
        )
    elif attributes['subcategory_id'] == 9:
        attributes['hazard_rate_active'] = (
            (
                attributes['C1'] * attributes['piT'] * attributes['piA']
                + attributes['C2'] * attributes['piE']
            ) * attributes['piQ'] * attributes['piL']
        )
    elif attributes['subcategory_id'] == 10:
        attributes = _calculate_vhisc_vlsi_variables(attributes)
        attributes['hazard_rate_active'] = (
            attributes['lambdaBD'] * attributes['piMFG'] * attributes['piT']
            * attributes['piCD'] + attributes['lambdaBP'] * attributes['piE']
            * attributes['piQ'] * attributes['piPT'] + attributes['lambdaEOS']
        )

    return attributes, _msg


def do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the integrated circuit type which is why a WARKING message
    is issued rather than an ERROR message.

    :param dict attributes: the attributes for the integrated circuit being
        calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    _messages = {
        'piQ': (
            'RAMSTK WARNING: piQ is 0.0 when calculating '
            'integrated circuit, hardware ID: {0:d}, '
            'quality ID: {1:d}.\n'
        ).format(
            attributes['hardware_id'],
            attributes['quality_id'],
        ),
        'lambda_b': (
            'RAMSTK WARNING: Base hazard rate is 0.0 when '
            'calculating integrated circuit, hardware ID: '
            '{0:d}.\n'
        ).format(attributes['hardware_id']),
        'C1': (
            'RAMSTK WARNING: C1 is 0.0 when calculating '
            'integrated circuit, hardware ID: {0:d}, '
            'application ID: {1:d}, '
            'technology ID: {2:d}.\n'
        ).format(
            attributes['hardware_id'],
            attributes['application_id'],
            attributes['technology_id'],
        ),
        'C2': (
            'RAMSTK WARNING: C2 is 0.0 when calculating '
            'integrated circuit, hardware ID: {0:d}, '
            'package ID: {1:d}, '
            '# active pins: {2:d}.\n'
        ).format(
            attributes['hardware_id'],
            attributes['package_id'],
            attributes['n_active_pins'],
        ),
        'piA': (
            'RAMSTK WARNING: piA is 0.0 when calculating '
            'integrated circuit, hardware ID: {0:d}, '
            'application ID: {1:d}.\n'
        ).format(
            attributes['hardware_id'],
            attributes['application_id'],
        ),
        'piE': (
            'RAMSTK WARNING: piE is 0.0 when calculating '
            'integrated circuit, hardware ID: {0:d}, '
            'environment ID: {1:d}.\n'
        ).format(
            attributes['hardware_id'],
            attributes['environment_active_id'],
        ),
        'piL': (
            'RAMSTK WARNING: piL is 0.0 when calculating '
            'integrated circuit, hardware ID: {0:d}, '
            'years in production: {1:f}.\n'
        ).format(
            attributes['hardware_id'],
            attributes['years_in_production'],
        ),
        'piT': (
            'RAMSTK WARNING: piT is 0.0 when calculating '
            'integrated circuit, hardware ID: {0:d}, '
            'application ID: {1:d}, '
            'type ID: {2:d}.\n'
        ).format(
            attributes['hardware_id'],
            attributes['application_id'],
            attributes['type_id'],
        ),
    }

    _variables = ['piQ', ]

    if attributes['hazard_rate_method_id'] == 1:
        _variables.append('lambda_b')
    if attributes['hazard_rate_method_id'] == 2:
        _variables.append('C1')
        _variables.append('C2')
        _variables.append('piA')
        _variables.append('piE')
        _variables.append('piL')
        _variables.append('piT')

    for _var in _variables:
        if attributes[_var] <= 0.0:
            _msg = _msg + _messages[_var]

    return _msg
