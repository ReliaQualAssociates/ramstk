# pylint: disable=invalid-name
# -*- coding: utf-8 -*-
#
#       tests.analyses.prediction.test_integrated_circuit.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the integrated circuit module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.data import HARDWARE_ATTRIBUTES, RAMSTK_STRESS_LIMITS
from ramstk.analyses.prediction import Component, IntegratedCircuit

ATTRIBUTES = HARDWARE_ATTRIBUTES.copy()

ATTRIBUTES['category_id'] = 1
ATTRIBUTES['environment_dormant_id'] = 3
ATTRIBUTES['add_adj_factor'] = 0.0
ATTRIBUTES['mult_adj_factor'] = 1.0
ATTRIBUTES['duty_cycle'] = 100.0
ATTRIBUTES['quantity'] = 1

PART_COUNT_LAMBDA_B = {
    1: {
        1: {
            1: [
                0.0095, 0.024, 0.039, 0.034, 0.049, 0.057, 0.062, 0.12, 0.13,
                0.076, 0.0095, 0.044, 0.096, 1.1,
            ],
            2: [
                0.0170, 0.041, 0.065, 0.054, 0.078, 0.100, 0.110, 0.22, 0.24,
                0.130, 0.0170, 0.072, 0.150, 1.4,
            ],
            3: [
                0.0330, 0.074, 0.110, 0.092, 0.130, 0.190, 0.190, 0.41, 0.44,
                0.220, 0.0330, 0.120, 0.260, 2.0,
            ],
            4: [
                0.0500, 0.120, 0.180, 0.150, 0.210, 0.300, 0.300, 0.63, 0.67,
                0.350, 0.0500, 0.190, 0.410, 3.4,
            ],
        },
        2: {
            1: [
                0.0095, 0.024, 0.039, 0.034, 0.049, 0.057, 0.062, 0.12, 0.13,
                0.076, 0.0095, 0.044, 0.096, 1.1,
            ],
            2: [
                0.0170, 0.041, 0.065, 0.054, 0.078, 0.100, 0.110, 0.22, 0.24,
                0.130, 0.0170, 0.072, 0.150, 1.4,
            ],
            3: [
                0.0330, 0.074, 0.110, 0.092, 0.130, 0.190, 0.190, 0.41, 0.44,
                0.220, 0.0330, 0.120, 0.260, 2.0,
            ],
            4: [
                0.0500, 0.120, 0.180, 0.150, 0.210, 0.300, 0.300, 0.63, 0.67,
                0.350, 0.0500, 0.190, 0.410, 3.4,
            ],
        },
    },
    2: {
        1: {
            1: [
                0.0036, 0.012, 0.024, 0.024, 0.035, 0.025, 0.030, 0.032, 0.049,
                0.047, 0.0036, 0.030, 0.069, 1.20,
            ],
            2: [
                0.0060, 0.020, 0.038, 0.037, 0.055, 0.039, 0.048, 0.051, 0.077,
                0.074, 0.0060, 0.046, 0.110, 1.90,
            ],
            3: [
                0.0110, 0.035, 0.066, 0.065, 0.097, 0.070, 0.085, 0.091, 0.140,
                0.130, 0.0110, 0.082, 0.190, 3.30,
            ],
            4: [
                0.0330, 0.120, 0.220, 0.220, 0.330, 0.230, 0.280, 0.300, 0.460,
                0.440, 0.0330, 0.280, 0.650, 12.0,
            ],
            5: [
                0.0520, 0.170, 0.330, 0.330, 0.480, 0.340, 0.420, 0.450, 0.680,
                0.650, 0.0520, 0.410, 0.950, 17.0,
            ],
            6: [
                0.0750, 0.230, 0.440, 0.430, 0.630, 0.460, 0.560, 0.610, 0.900,
                0.850, 0.0750, 0.530, 1.200, 21.0,
            ],
        },
        2: {
            1: [
                0.0057, 0.015, 0.027, 0.027, 0.039, 0.029, 0.035, 0.039, 0.056,
                0.052, 0.0057, 0.033, 0.074, 1.20,
            ],
            2: [
                0.0100, 0.028, 0.045, 0.043, 0.062, 0.049, 0.057, 0.068, 0.092,
                0.083, 0.0100, 0.053, 0.120, 1.90,
            ],
            3: [
                0.0190, 0.047, 0.080, 0.077, 0.110, 0.088, 0.100, 0.120, 0.170,
                0.150, 0.0190, 0.095, 0.210, 3.30,
            ],
            4: [
                0.0490, 0.140, 0.250, 0.240, 0.360, 0.270, 0.320, 0.360, 0.510,
                0.480, 0.0490, 0.300, 0.690, 12.0,
            ],
            5: [
                0.0840, 0.220, 0.390, 0.370, 0.540, 0.420, 0.490, 0.560, 0.790,
                0.720, 0.0840, 0.460, 1.000, 17.0,
            ],
            6: [
                0.1300, 0.310, 0.530, 0.510, 0.730, 0.590, 0.690, 0.820, 1.100,
                0.980, 0.1300, 0.830, 1.400, 21.0,
            ],
        },
    },
    3: {
        1: {
            1: [
                0.0061, 0.016, 0.029, 0.027, 0.040, 0.032, 0.037, 0.044, 0.061,
                0.054, 0.0061, 0.034, 0.076, 1.2,
            ],
            2: [
                0.0110, 0.028, 0.048, 0.046, 0.065, 0.054, 0.063, 0.077, 0.100,
                0.089, 0.0110, 0.057, 0.120, 1.9,
            ],
            3: [
                0.0220, 0.052, 0.087, 0.082, 0.120, 0.099, 0.110, 0.140, 0.190,
                0.160, 0.0220, 0.100, 0.220, 3.3,
            ],
        },
        2: {
            1: [
                0.0046, 0.018, 0.035, 0.035, 0.052, 0.035, 0.044, 0.044, 0.070,
                0.070, 0.0046, 0.044, 0.100, 1.9,
            ],
            2: [
                0.0056, 0.021, 0.042, 0.042, 0.062, 0.042, 0.052, 0.053, 0.084,
                0.083, 0.0056, 0.052, 0.120, 2.3,
            ],
            3: [
                0.0061, 0.022, 0.043, 0.042, 0.063, 0.043, 0.054, 0.055, 0.086,
                0.084, 0.0081, 0.053, 0.130, 2.3,
            ],
            4: [
                0.0095, 0.033, 0.064, 0.063, 0.094, 0.065, 0.080, 0.083, 0.130,
                0.130, 0.0095, 0.079, 0.190, 3.3,
            ],
        },
    },
    4: {
        1: {
            1: [
                0.028, 0.061, 0.098, 0.091, 0.13, 0.12, 0.13, 0.17, 0.22, 0.18,
                0.028, 0.11, 0.24, 3.30,
            ],
            2: [
                0.052, 0.110, 0.180, 0.160, 0.23, 0.21, 0.24, 0.32, 0.39, 0.31,
                0.052, 0.20, 0.41, 5.60,
            ],
            3: [
                0.110, 0.230, 0.360, 0.330, 0.47, 0.44, 0.49, 0.65, 0.81, 0.65,
                0.110, 0.42, 0.86, 12.0,
            ],
        },
        2: {
            1: [
                0.048, 0.089, 0.130, 0.120, 0.16, 0.16, 0.17, 0.24, 0.28, 0.22,
                0.048, 0.15, 0.28, 3.40,
            ],
            2: [
                0.093, 0.170, 0.240, 0.220, 0.29, 0.30, 0.32, 0.45, 0.52, 0.40,
                0.093, 0.27, 0.50, 5.60,
            ],
            3: [
                0.190, 0.340, 0.490, 0.450, 0.60, 0.61, 0.66, 0.90, 1.10, 0.82,
                0.190, 0.54, 1.00, 12.0,
            ],
        },
    },
    5: {
        1: {
            1: [
                0.010, 0.028, 0.050, 0.046, 0.067, 0.062, 0.070, 0.10, 0.13,
                0.096, 0.010, 0.058, 0.13, 1.9,
            ],
            2: [
                0.017, 0.043, 0.071, 0.063, 0.091, 0.095, 0.110, 0.18, 0.21,
                0.140, 0.017, 0.081, 0.18, 2.3,
            ],
            3: [
                0.028, 0.065, 0.100, 0.085, 0.120, 0.150, 0.180, 0.30, 0.33,
                0.190, 0.028, 0.110, 0.23, 2.3,
            ],
            4: [
                0.053, 0.120, 0.180, 0.150, 0.210, 0.270, 0.290, 0.56, 0.61,
                0.330, 0.053, 0.190, 0.39, 3.4,
            ],
        },
        2: {
            1: [
                0.0047, 0.018, 0.036, 0.035, 0.053, 0.037, 0.045, 0.048, 0.074,
                0.071, 0.0047, 0.044, 0.11, 1.9,
            ],
            2: [
                0.0059, 0.022, 0.043, 0.042, 0.063, 0.045, 0.055, 0.060, 0.090,
                0.086, 0.0059, 0.053, 0.13, 2.3,
            ],
            3: [
                0.0067, 0.023, 0.045, 0.044, 0.066, 0.048, 0.059, 0.068, 0.099,
                0.089, 0.0067, 0.055, 0.13, 2.3,
            ],
            4: [
                0.0110, 0.036, 0.068, 0.066, 0.098, 0.075, 0.090, 0.110, 0.150,
                0.140, 0.0110, 0.083, 0.20, 3.3,
            ],
        },
    },
    6: {
        2: {
            1: [
                0.0049, 0.018, 0.036, 0.036, 0.053, 0.037, 0.046, 0.049, 0.075,
                0.072, 0.0048, 0.045, 0.11, 1.9,
            ],
            2: [
                0.0061, 0.022, 0.044, 0.043, 0.064, 0.046, 0.056, 0.062, 0.093,
                0.087, 0.0062, 0.054, 0.13, 2.3,
            ],
            3: [
                0.0072, 0.024, 0.048, 0.045, 0.067, 0.051, 0.061, 0.073, 0.100,
                0.092, 0.0072, 0.057, 0.13, 2.3,
            ],
            4: [
                0.0120, 0.038, 0.071, 0.068, 0.100, 0.080, 0.095, 0.120, 0.180,
                0.140, 0.0120, 0.086, 0.20, 3.3,
            ],
        },
    },
    7: {
        2: {
            1: [
                0.0040, 0.014, 0.027, 0.027, 0.040, 0.029, 0.035, 0.040, 0.059,
                0.055, 0.0040, 0.034, 0.080, 1.4,
            ],
            2: [
                0.0055, 0.019, 0.039, 0.034, 0.051, 0.039, 0.047, 0.056, 0.079,
                0.070, 0.0055, 0.043, 0.100, 1.7,
            ],
            3: [
                0.0074, 0.023, 0.043, 0.040, 0.060, 0.049, 0.058, 0.076, 0.100,
                0.084, 0.0074, 0.051, 0.120, 1.9,
            ],
            4: [
                0.0110, 0.032, 0.057, 0.053, 0.077, 0.070, 0.080, 0.120, 0.150,
                0.110, 0.0110, 0.067, 0.150, 2.3,
            ],
        },
    },
    8: {
        1: {
            1: [
                0.0075, 0.023, 0.043, 0.041, 0.060, 0.050, 0.058, 0.077, 0.10,
                0.084, 0.0075, 0.052, 0.12, 1.9,
            ],
            2: [
                0.0120, 0.033, 0.058, 0.054, 0.079, 0.072, 0.083, 0.120, 0.15,
                0.110, 0.0120, 0.069, 0.15, 2.3,
            ],
            3: [
                0.0180, 0.045, 0.074, 0.065, 0.095, 0.100, 0.110, 0.190, 0.22,
                0.140, 0.0180, 0.084, 0.18, 2.3,
            ],
            4: [
                0.0330, 0.079, 0.130, 0.110, 0.160, 0.180, 0.200, 0.350, 0.39,
                0.240, 0.0330, 0.140, 0.30, 3.4,
            ],
        },
        2: {
            1: [
                0.0079, 0.022, 0.038, 0.034, 0.050, 0.048, 0.054, 0.083, 0.10,
                0.073, 0.0079, 0.044, 0.098, 1.4,
            ],
            2: [
                0.0140, 0.034, 0.057, 0.050, 0.073, 0.077, 0.085, 0.140, 0.17,
                0.110, 0.0140, 0.065, 0.140, 1.8,
            ],
            3: [
                0.0230, 0.053, 0.084, 0.071, 0.100, 0.120, 0.130, 0.250, 0.27,
                0.160, 0.0230, 0.092, 0.190, 1.9,
            ],
            4: [
                0.0430, 0.092, 0.140, 0.110, 0.160, 0.220, 0.230, 0.460, 0.49,
                0.260, 0.0430, 0.150, 0.300, 2.3,
            ],
        },
    },
    9: {
        1: {
            1: [
                0.019, 0.034, 0.046, 0.039, 0.052, 0.065, 0.068, 0.11, 0.12,
                0.076, 0.019, 0.049, 0.086, 0.61,
            ],
            2: [
                0.025, 0.047, 0.067, 0.058, 0.079, 0.091, 0.097, 0.15, 0.17,
                0.11, 0.025, 0.073, 0.14, 1.3,
            ],
        },
        2: {
            1: [
                0.0085, 0.030, 0.057, 0.057, 0.084, 0.060, 0.073, 0.080, 0.12,
                0.11, 0.0085, 0.071, 0.17, 3.0,
            ],
            2: [
                0.0140, 0.053, 0.100, 0.100, 0.150, 0.110, 0.130, 0.140, 0.22,
                0.21, 0.0140, 0.130, 0.31, 5.5,
            ],
        },
    },
}

PART_COUNT_PIQ = [0.25, 1.0, 2.0]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("quality_id", [1, 2, 3])
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
def test_calculate_mil_hdbk_217f_part_count(
        technology_id, quality_id,
        environment_active_id,
):
    """calculate_mil_hdbk_217f_part_count() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 1
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['technology_id'] = technology_id
    ATTRIBUTES['n_elements'] = 100
    ATTRIBUTES['quality_id'] = quality_id
    ATTRIBUTES['environment_active_id'] = environment_active_id

    try:
        lambda_b = PART_COUNT_LAMBDA_B[ATTRIBUTES['subcategory_id']][
            ATTRIBUTES['technology_id']
        ][1][environment_active_id - 1]
    except (KeyError, IndexError):
        lambda_b = 0.0
    piQ = PART_COUNT_PIQ[quality_id - 1]

    _attributes, _msg = IntegratedCircuit.calculate_217f_part_count(
        **ATTRIBUTES,
    )

    assert isinstance(_attributes, dict)
    if lambda_b == 0.0:
        assert _msg == (
            'RAMSTK WARNING: Base hazard rate is 0.0 when '
            'calculating integrated circuit, hardware ID: 6'
        )
    else:
        assert _msg == ''
    assert _attributes['lambda_b'] == lambda_b
    assert _attributes['piQ'] == piQ
    assert _attributes['hazard_rate_active'] == lambda_b * piQ


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_subcategory():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the subcategory ID is missing."""
    ATTRIBUTES['subcategory_id'] = 0
    ATTRIBUTES['technology_id'] = 1
    ATTRIBUTES['n_elements'] = 100
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = IntegratedCircuit.calculate_217f_part_count(
        **ATTRIBUTES,
    )

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'integrated circuit, hardware ID: 6'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.25
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_technology():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the technology ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['technology_id'] = 10
    ATTRIBUTES['n_elements'] = 100
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = IntegratedCircuit.calculate_217f_part_count(
        **ATTRIBUTES,
    )

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'integrated circuit, hardware ID: 6'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.25
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_environment():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the active environment ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['technology_id'] = 1
    ATTRIBUTES['n_elements'] = 100
    ATTRIBUTES['quality_id'] = 1
    ATTRIBUTES['environment_active_id'] = 44

    _attributes, _msg = IntegratedCircuit.calculate_217f_part_count(
        **ATTRIBUTES,
    )

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: Base hazard rate is 0.0 when calculating '
        'integrated circuit, hardware ID: 6'
    )
    assert _attributes['lambda_b'] == 0.0
    assert _attributes['piQ'] == 0.25
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_count_missing_quality():
    """calculate_mil_hdbk_217f_part_count() should return an error message when the quality ID is missing."""
    ATTRIBUTES['subcategory_id'] = 1
    ATTRIBUTES['technology_id'] = 1
    ATTRIBUTES['n_elements'] = 100
    ATTRIBUTES['quality_id'] = 10
    ATTRIBUTES['environment_active_id'] = 1

    _attributes, _msg = IntegratedCircuit.calculate_217f_part_count(
        **ATTRIBUTES,
    )

    assert isinstance(_attributes, dict)
    assert _msg == (
        'RAMSTK WARNING: piQ is 0.0 when calculating integrated '
        'circuit, hardware ID: 6'
    )
    assert _attributes['lambda_b'] == 0.0095
    assert _attributes['piQ'] == 0.0
    assert _attributes['hazard_rate_active'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['subcategory_id'] = 2
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['technology_id'] = 1
    ATTRIBUTES['package_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['power_operating'] = 0.05
    ATTRIBUTES['n_elements'] = 2000
    ATTRIBUTES['n_active_pins'] = 16
    ATTRIBUTES['years_in_production'] = 1
    ATTRIBUTES['temperature_case'] = 40.0
    ATTRIBUTES['power_operating'] = 0.05
    ATTRIBUTES['theta_jc'] = 30.0

    _attributes, _msg = IntegratedCircuit.calculate_217f_part_stress(
        **ATTRIBUTES,
    )

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['C1'], 0.06)
    assert pytest.approx(_attributes['C2'], 0.005921936)
    assert pytest.approx(_attributes['piT'], 0.4477441)
    assert pytest.approx(_attributes['piL'], 1.4841316)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 4.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.075026401)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mil_hdbk_217f_part_stress_gaas():
    """calculate_mil_hdbk_217f_part_stress() should return a dictionary of updated values on success when calculating a GaAs device."""
    ATTRIBUTES['hazard_rate_method_id'] = 2
    ATTRIBUTES['subcategory_id'] = 9
    ATTRIBUTES['environment_active_id'] = 4
    ATTRIBUTES['quality_id'] = 2
    ATTRIBUTES['technology_id'] = 1
    ATTRIBUTES['type_id'] = 2
    ATTRIBUTES['application_id'] = 1
    ATTRIBUTES['package_id'] = 2
    ATTRIBUTES['temperature_active'] = 32.0
    ATTRIBUTES['temperature_rated_max'] = 85.0
    ATTRIBUTES['power_operating'] = 0.05
    ATTRIBUTES['n_elements'] = 2000
    ATTRIBUTES['n_active_pins'] = 16
    ATTRIBUTES['years_in_production'] = 1
    ATTRIBUTES['temperature_case'] = 40.0
    ATTRIBUTES['power_operating'] = 0.05
    ATTRIBUTES['theta_jc'] = 30.0

    _attributes, _msg = IntegratedCircuit.calculate_217f_part_stress(
        **ATTRIBUTES,
    )

    assert isinstance(_attributes, dict)
    assert _msg == ''
    assert pytest.approx(_attributes['C1'], 7.2)
    assert pytest.approx(_attributes['C2'], 0.01686627)
    assert pytest.approx(_attributes['piT'], 1.7590156E-07)
    assert _attributes['piA'] == 1.0
    assert pytest.approx(_attributes['piL'], 1.4841316)
    assert _attributes['piQ'] == 1.0
    assert _attributes['piE'] == 4.0
    assert pytest.approx(_attributes['hazard_rate_active'], 0.1001327)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [5.0, 3.3])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_under_voltage(voltage_rated, environment_active_id):
    """overstressed() should return True when voltage < 0.95 rated in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.005
    ATTRIBUTES['current_rated'] = 0.01
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 3.2
    ATTRIBUTES['power_operating'] = 0.0
    ATTRIBUTES['power_rated'] = 0.1
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id
    ATTRIBUTES['temperature_junction'] = 89.4

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 3.3:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 5.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating voltage < 95% rated '
            'voltage.\n'
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("voltage_rated", [5.0, 3.3])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_over_voltage(voltage_rated, environment_active_id):
    """overstressed() should return True when voltage < 0.95 rated in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.005
    ATTRIBUTES['current_rated'] = 0.01
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 4.95
    ATTRIBUTES['power_operating'] = 0.0
    ATTRIBUTES['power_rated'] = 0.1
    ATTRIBUTES['voltage_rated'] = voltage_rated
    ATTRIBUTES['environment_active_id'] = environment_active_id
    ATTRIBUTES['temperature_junction'] = 89.4

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if voltage_rated == 5.0:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif voltage_rated == 3.3:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating voltage > 105% rated '
            'voltage.\n'
        )


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("temperature_junction", [28.7, 138.0])
@pytest.mark.parametrize(
    "environment_active_id",
    [3, 5, 6, 7, 8, 9, 10, 12, 13, 14],
)
def test_temperature_overstress_harsh_environment(
        temperature_junction,
        environment_active_id,
):
    """overstressed() should return True when hot spot temperature is within 15C of rated temperature in a harsh environment and False otherwise."""
    ATTRIBUTES['current_operating'] = 0.18
    ATTRIBUTES['current_rated'] = 0.5
    ATTRIBUTES['voltage_rated'] = 5.0
    ATTRIBUTES['voltage_ac_operating'] = 0.005
    ATTRIBUTES['voltage_dc_operating'] = 4.95
    ATTRIBUTES['temperature_rated_max'] = 125.0
    ATTRIBUTES['power_operating'] = 0.0
    ATTRIBUTES['power_rated'] = 0.1
    ATTRIBUTES['temperature_junction'] = temperature_junction
    ATTRIBUTES['environment_active_id'] = environment_active_id

    _attributes = Component.do_calculate_stress_ratios(**ATTRIBUTES)
    _attributes = Component.do_check_overstress(RAMSTK_STRESS_LIMITS, **_attributes)

    assert isinstance(_attributes, dict)
    if temperature_junction == 28.7:
        assert not _attributes['overstress']
        assert _attributes['reason'] == ''
    elif temperature_junction == 138.0:
        assert _attributes['overstress']
        assert _attributes['reason'] == (
            '1. Operating temperature > 125.0C '
            'Junction temperature limit in harsh '
            'environment.\n'
        )
