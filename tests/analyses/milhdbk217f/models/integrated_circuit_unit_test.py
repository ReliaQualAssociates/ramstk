# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.integrated_circuit_unit_test.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the integrated circuit module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import integratedcircuit


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
)
def test_set_default_junction_temperature(environment_id):
    """Should return the default junction temperature for the active environment ID."""
    _temp_junction = integratedcircuit._set_default_junction_temperature(
        0.0, 25.0, environment_id
    )

    assert (
        _temp_junction
        == {
            1: 50.0,
            2: 60.0,
            3: 65.0,
            4: 60.0,
            5: 65.0,
            6: 75.0,
            7: 75.0,
            8: 90.0,
            9: 90.0,
            10: 75.0,
            11: 50.0,
            12: 65.0,
            13: 75.0,
            14: 60.0,
            15: 25.0,
        }[environment_id]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_set_default_values(
    test_attributes_integrated_circuit,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_integrated_circuit["package_id"] = 0
    test_attributes_integrated_circuit["environment_active_id"] = 3
    test_attributes_integrated_circuit["temperature_junction"] = 0.0
    test_attributes_integrated_circuit["years_in_production"] = -5
    _attributes = integratedcircuit.set_default_values(
        test_attributes_integrated_circuit
    )

    assert isinstance(_attributes, dict)
    assert _attributes["package_id"] == 1
    assert _attributes["temperature_junction"] == 65.0
    assert _attributes["years_in_production"] == 2


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_set_default_values_none_needed(
    test_attributes_integrated_circuit,
):
    """Should set default values for each parameter <= 0.0."""
    test_attributes_integrated_circuit["package_id"] = 2
    test_attributes_integrated_circuit["environment_active_id"] = 3
    test_attributes_integrated_circuit["temperature_junction"] = 38.65
    test_attributes_integrated_circuit["years_in_production"] = 5
    _attributes = integratedcircuit.set_default_values(
        test_attributes_integrated_circuit
    )

    assert isinstance(_attributes, dict)
    assert _attributes["package_id"] == 2
    assert _attributes["temperature_junction"] == 38.65
    assert _attributes["years_in_production"] == 5


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("n_elements", [100, 300, 1000, 10000])
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_linear(
    environment_active_id,
    n_elements,
    test_attributes_integrated_circuit,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_integrated_circuit["environment_active_id"] = environment_active_id
    test_attributes_integrated_circuit["n_elements"] = n_elements
    test_attributes_integrated_circuit["subcategory_id"] = 1
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        test_attributes_integrated_circuit
    )

    assert isinstance(_lambda_b, float)
    if n_elements == 100:
        assert (
            _lambda_b
            == [
                0.0095,
                0.024,
                0.039,
                0.034,
                0.049,
                0.057,
                0.062,
                0.12,
                0.13,
                0.076,
                0.0095,
                0.044,
                0.096,
                1.1,
            ][environment_active_id - 1]
        )
    elif n_elements == 300:
        assert (
            _lambda_b
            == [
                0.0170,
                0.041,
                0.065,
                0.054,
                0.078,
                0.100,
                0.110,
                0.22,
                0.24,
                0.130,
                0.0170,
                0.072,
                0.150,
                1.4,
            ][environment_active_id - 1]
        )
    elif n_elements == 1000:
        assert (
            _lambda_b
            == [
                0.0330,
                0.074,
                0.110,
                0.092,
                0.130,
                0.190,
                0.190,
                0.41,
                0.44,
                0.220,
                0.0330,
                0.120,
                0.260,
                2.0,
            ][environment_active_id - 1]
        )
    elif n_elements == 10000:
        assert (
            _lambda_b
            == [
                0.0500,
                0.120,
                0.180,
                0.150,
                0.210,
                0.300,
                0.300,
                0.63,
                0.67,
                0.350,
                0.0500,
                0.190,
                0.410,
                3.4,
            ][environment_active_id - 1]
        )


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements", [100, 1000, 3000, 10000, 30000, 60000])
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_logic(
    technology_id,
    environment_active_id,
    n_elements,
    test_attributes_integrated_circuit,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_integrated_circuit["environment_active_id"] = environment_active_id
    test_attributes_integrated_circuit["n_elements"] = n_elements
    test_attributes_integrated_circuit["subcategory_id"] = 2
    test_attributes_integrated_circuit["technology_id"] = technology_id
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        test_attributes_integrated_circuit
    )

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: {
                100: [
                    0.0036,
                    0.012,
                    0.024,
                    0.024,
                    0.035,
                    0.025,
                    0.030,
                    0.032,
                    0.049,
                    0.047,
                    0.0036,
                    0.030,
                    0.069,
                    1.20,
                ],
                1000: [
                    0.0060,
                    0.020,
                    0.038,
                    0.037,
                    0.055,
                    0.039,
                    0.048,
                    0.051,
                    0.077,
                    0.074,
                    0.0060,
                    0.046,
                    0.110,
                    1.90,
                ],
                3000: [
                    0.0110,
                    0.035,
                    0.066,
                    0.065,
                    0.097,
                    0.070,
                    0.085,
                    0.091,
                    0.140,
                    0.130,
                    0.0110,
                    0.082,
                    0.190,
                    3.30,
                ],
                10000: [
                    0.0330,
                    0.120,
                    0.220,
                    0.220,
                    0.330,
                    0.230,
                    0.280,
                    0.300,
                    0.460,
                    0.440,
                    0.0330,
                    0.280,
                    0.650,
                    12.0,
                ],
                30000: [
                    0.0520,
                    0.170,
                    0.330,
                    0.330,
                    0.480,
                    0.340,
                    0.420,
                    0.450,
                    0.680,
                    0.650,
                    0.0520,
                    0.410,
                    0.950,
                    17.0,
                ],
                60000: [
                    0.0750,
                    0.230,
                    0.440,
                    0.430,
                    0.630,
                    0.460,
                    0.560,
                    0.610,
                    0.900,
                    0.850,
                    0.0750,
                    0.530,
                    1.200,
                    21.0,
                ],
            },
            2: {
                100: [
                    0.0057,
                    0.015,
                    0.027,
                    0.027,
                    0.039,
                    0.029,
                    0.035,
                    0.039,
                    0.056,
                    0.052,
                    0.0057,
                    0.033,
                    0.074,
                    1.20,
                ],
                1000: [
                    0.0100,
                    0.028,
                    0.045,
                    0.043,
                    0.062,
                    0.049,
                    0.057,
                    0.068,
                    0.092,
                    0.083,
                    0.0100,
                    0.053,
                    0.120,
                    1.90,
                ],
                3000: [
                    0.0190,
                    0.047,
                    0.080,
                    0.077,
                    0.110,
                    0.088,
                    0.100,
                    0.120,
                    0.170,
                    0.150,
                    0.0190,
                    0.095,
                    0.210,
                    3.30,
                ],
                10000: [
                    0.0490,
                    0.140,
                    0.250,
                    0.240,
                    0.360,
                    0.270,
                    0.320,
                    0.360,
                    0.510,
                    0.480,
                    0.0490,
                    0.300,
                    0.690,
                    12.0,
                ],
                30000: [
                    0.0840,
                    0.220,
                    0.390,
                    0.370,
                    0.540,
                    0.420,
                    0.490,
                    0.560,
                    0.790,
                    0.720,
                    0.0840,
                    0.460,
                    1.000,
                    17.0,
                ],
                60000: [
                    0.1300,
                    0.310,
                    0.530,
                    0.510,
                    0.730,
                    0.590,
                    0.690,
                    0.820,
                    1.100,
                    0.980,
                    0.1300,
                    0.830,
                    1.400,
                    21.0,
                ],
            },
        }[technology_id][n_elements][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements_id", [0, 1, 2])
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_pal_pla(
    technology_id,
    environment_active_id,
    n_elements_id,
    test_attributes_integrated_circuit,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_integrated_circuit["environment_active_id"] = environment_active_id
    test_attributes_integrated_circuit["n_elements"] = {
        1: [200, 1000, 5000],
        2: [16000, 64000, 256000, 1000000],
    }[technology_id][n_elements_id]
    test_attributes_integrated_circuit["subcategory_id"] = 3
    test_attributes_integrated_circuit["technology_id"] = technology_id

    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        test_attributes_integrated_circuit
    )

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: {
                1: [
                    0.0061,
                    0.016,
                    0.029,
                    0.027,
                    0.040,
                    0.032,
                    0.037,
                    0.044,
                    0.061,
                    0.054,
                    0.0061,
                    0.034,
                    0.076,
                    1.2,
                ],
                2: [
                    0.0110,
                    0.028,
                    0.048,
                    0.046,
                    0.065,
                    0.054,
                    0.063,
                    0.077,
                    0.100,
                    0.089,
                    0.0110,
                    0.057,
                    0.120,
                    1.9,
                ],
                3: [
                    0.0220,
                    0.052,
                    0.087,
                    0.082,
                    0.120,
                    0.099,
                    0.110,
                    0.140,
                    0.190,
                    0.160,
                    0.0220,
                    0.100,
                    0.220,
                    3.3,
                ],
            },
            2: {
                1: [
                    0.0046,
                    0.018,
                    0.035,
                    0.035,
                    0.052,
                    0.035,
                    0.044,
                    0.044,
                    0.070,
                    0.070,
                    0.0046,
                    0.044,
                    0.100,
                    1.9,
                ],
                2: [
                    0.0056,
                    0.021,
                    0.042,
                    0.042,
                    0.062,
                    0.042,
                    0.052,
                    0.053,
                    0.084,
                    0.083,
                    0.0056,
                    0.052,
                    0.120,
                    2.3,
                ],
                3: [
                    0.0061,
                    0.022,
                    0.043,
                    0.042,
                    0.063,
                    0.043,
                    0.054,
                    0.055,
                    0.086,
                    0.084,
                    0.0081,
                    0.053,
                    0.130,
                    2.3,
                ],
            },
        }[technology_id][n_elements_id + 1][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements_id", [0, 1, 2])
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_mup_muc(
    technology_id,
    environment_active_id,
    n_elements_id,
    test_attributes_integrated_circuit,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_integrated_circuit["environment_active_id"] = environment_active_id
    test_attributes_integrated_circuit["n_elements"] = [8, 16, 32][n_elements_id]
    test_attributes_integrated_circuit["subcategory_id"] = 4
    test_attributes_integrated_circuit["technology_id"] = technology_id

    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        test_attributes_integrated_circuit
    )

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: {
                1: [
                    0.028,
                    0.061,
                    0.098,
                    0.091,
                    0.13,
                    0.12,
                    0.13,
                    0.17,
                    0.22,
                    0.18,
                    0.028,
                    0.11,
                    0.24,
                    3.30,
                ],
                2: [
                    0.052,
                    0.110,
                    0.180,
                    0.160,
                    0.23,
                    0.21,
                    0.24,
                    0.32,
                    0.39,
                    0.31,
                    0.052,
                    0.20,
                    0.41,
                    5.60,
                ],
                3: [
                    0.110,
                    0.230,
                    0.360,
                    0.330,
                    0.47,
                    0.44,
                    0.49,
                    0.65,
                    0.81,
                    0.65,
                    0.110,
                    0.42,
                    0.86,
                    12.0,
                ],
            },
            2: {
                1: [
                    0.048,
                    0.089,
                    0.130,
                    0.120,
                    0.16,
                    0.16,
                    0.17,
                    0.24,
                    0.28,
                    0.22,
                    0.048,
                    0.15,
                    0.28,
                    3.40,
                ],
                2: [
                    0.093,
                    0.170,
                    0.240,
                    0.220,
                    0.29,
                    0.30,
                    0.32,
                    0.45,
                    0.52,
                    0.40,
                    0.093,
                    0.27,
                    0.50,
                    5.60,
                ],
                3: [
                    0.190,
                    0.340,
                    0.490,
                    0.450,
                    0.60,
                    0.61,
                    0.66,
                    0.90,
                    1.10,
                    0.82,
                    0.190,
                    0.54,
                    1.00,
                    12.0,
                ],
            },
        }[technology_id][n_elements_id + 1][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [5, 8],
)
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements_id", [0, 1, 2, 3])
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_rom_sram(
    subcategory_id,
    technology_id,
    environment_active_id,
    n_elements_id,
    test_attributes_integrated_circuit,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_integrated_circuit["environment_active_id"] = environment_active_id
    test_attributes_integrated_circuit["n_elements"] = [16000, 64000, 256000, 100000][
        n_elements_id
    ]
    test_attributes_integrated_circuit["subcategory_id"] = subcategory_id
    test_attributes_integrated_circuit["technology_id"] = technology_id
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        test_attributes_integrated_circuit
    )

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            5: {
                1: {
                    1: [
                        0.010,
                        0.028,
                        0.050,
                        0.046,
                        0.067,
                        0.062,
                        0.070,
                        0.10,
                        0.13,
                        0.096,
                        0.010,
                        0.058,
                        0.13,
                        1.9,
                    ],
                    2: [
                        0.017,
                        0.043,
                        0.071,
                        0.063,
                        0.091,
                        0.095,
                        0.110,
                        0.18,
                        0.21,
                        0.140,
                        0.017,
                        0.081,
                        0.18,
                        2.3,
                    ],
                    3: [
                        0.028,
                        0.065,
                        0.100,
                        0.085,
                        0.120,
                        0.150,
                        0.180,
                        0.30,
                        0.33,
                        0.190,
                        0.028,
                        0.110,
                        0.23,
                        2.3,
                    ],
                    4: [
                        0.053,
                        0.120,
                        0.180,
                        0.150,
                        0.210,
                        0.270,
                        0.290,
                        0.56,
                        0.61,
                        0.330,
                        0.053,
                        0.190,
                        0.39,
                        3.4,
                    ],
                },
                2: {
                    1: [
                        0.0047,
                        0.018,
                        0.036,
                        0.035,
                        0.053,
                        0.037,
                        0.045,
                        0.048,
                        0.074,
                        0.071,
                        0.0047,
                        0.044,
                        0.11,
                        1.9,
                    ],
                    2: [
                        0.0059,
                        0.022,
                        0.043,
                        0.042,
                        0.063,
                        0.045,
                        0.055,
                        0.060,
                        0.090,
                        0.086,
                        0.0059,
                        0.053,
                        0.13,
                        2.3,
                    ],
                    3: [
                        0.0067,
                        0.023,
                        0.045,
                        0.044,
                        0.066,
                        0.048,
                        0.059,
                        0.068,
                        0.099,
                        0.089,
                        0.0067,
                        0.055,
                        0.13,
                        2.3,
                    ],
                    4: [
                        0.0110,
                        0.036,
                        0.068,
                        0.066,
                        0.098,
                        0.075,
                        0.090,
                        0.110,
                        0.150,
                        0.140,
                        0.0110,
                        0.083,
                        0.20,
                        3.3,
                    ],
                },
            },
            8: {
                1: {
                    1: [
                        0.0075,
                        0.023,
                        0.043,
                        0.041,
                        0.060,
                        0.050,
                        0.058,
                        0.077,
                        0.10,
                        0.084,
                        0.0075,
                        0.052,
                        0.12,
                        1.9,
                    ],
                    2: [
                        0.0120,
                        0.033,
                        0.058,
                        0.054,
                        0.079,
                        0.072,
                        0.083,
                        0.120,
                        0.15,
                        0.110,
                        0.0120,
                        0.069,
                        0.15,
                        2.3,
                    ],
                    3: [
                        0.0180,
                        0.045,
                        0.074,
                        0.065,
                        0.095,
                        0.100,
                        0.110,
                        0.190,
                        0.22,
                        0.140,
                        0.0180,
                        0.084,
                        0.18,
                        2.3,
                    ],
                    4: [
                        0.0330,
                        0.079,
                        0.130,
                        0.110,
                        0.160,
                        0.180,
                        0.200,
                        0.350,
                        0.39,
                        0.240,
                        0.0330,
                        0.140,
                        0.30,
                        3.4,
                    ],
                },
                2: {
                    1: [
                        0.0079,
                        0.022,
                        0.038,
                        0.034,
                        0.050,
                        0.048,
                        0.054,
                        0.083,
                        0.10,
                        0.073,
                        0.0079,
                        0.044,
                        0.098,
                        1.4,
                    ],
                    2: [
                        0.0140,
                        0.034,
                        0.057,
                        0.050,
                        0.073,
                        0.077,
                        0.085,
                        0.140,
                        0.17,
                        0.110,
                        0.0140,
                        0.065,
                        0.140,
                        1.8,
                    ],
                    3: [
                        0.0230,
                        0.053,
                        0.084,
                        0.071,
                        0.100,
                        0.120,
                        0.130,
                        0.250,
                        0.27,
                        0.160,
                        0.0230,
                        0.092,
                        0.190,
                        1.9,
                    ],
                    4: [
                        0.0430,
                        0.092,
                        0.140,
                        0.110,
                        0.160,
                        0.220,
                        0.230,
                        0.460,
                        0.49,
                        0.260,
                        0.0430,
                        0.150,
                        0.300,
                        2.3,
                    ],
                },
            },
        }[subcategory_id][technology_id][n_elements_id + 1][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [6, 7],
)
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("n_elements_id", [0, 1, 2, 3])
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_prom_dram(
    subcategory_id,
    environment_active_id,
    n_elements_id,
    test_attributes_integrated_circuit,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_integrated_circuit["environment_active_id"] = environment_active_id
    test_attributes_integrated_circuit["n_elements"] = [16000, 64000, 256000, 100000][
        n_elements_id
    ]
    test_attributes_integrated_circuit["subcategory_id"] = subcategory_id
    test_attributes_integrated_circuit["technology_id"] = 2
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        test_attributes_integrated_circuit
    )

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            6: {
                1: [
                    0.0049,
                    0.018,
                    0.036,
                    0.036,
                    0.053,
                    0.037,
                    0.046,
                    0.049,
                    0.075,
                    0.072,
                    0.0048,
                    0.045,
                    0.11,
                    1.9,
                ],
                2: [
                    0.0061,
                    0.022,
                    0.044,
                    0.043,
                    0.064,
                    0.046,
                    0.056,
                    0.062,
                    0.093,
                    0.087,
                    0.0062,
                    0.054,
                    0.13,
                    2.3,
                ],
                3: [
                    0.0072,
                    0.024,
                    0.048,
                    0.045,
                    0.067,
                    0.051,
                    0.061,
                    0.073,
                    0.100,
                    0.092,
                    0.0072,
                    0.057,
                    0.13,
                    2.3,
                ],
                4: [
                    0.0120,
                    0.038,
                    0.071,
                    0.068,
                    0.100,
                    0.080,
                    0.095,
                    0.120,
                    0.180,
                    0.140,
                    0.0120,
                    0.086,
                    0.20,
                    3.3,
                ],
            },
            7: {
                1: [
                    0.0040,
                    0.014,
                    0.027,
                    0.027,
                    0.040,
                    0.029,
                    0.035,
                    0.040,
                    0.059,
                    0.055,
                    0.0040,
                    0.034,
                    0.080,
                    1.4,
                ],
                2: [
                    0.0055,
                    0.019,
                    0.039,
                    0.034,
                    0.051,
                    0.039,
                    0.047,
                    0.056,
                    0.079,
                    0.070,
                    0.0055,
                    0.043,
                    0.100,
                    1.7,
                ],
                3: [
                    0.0074,
                    0.023,
                    0.043,
                    0.040,
                    0.060,
                    0.049,
                    0.058,
                    0.076,
                    0.100,
                    0.084,
                    0.0074,
                    0.051,
                    0.120,
                    1.9,
                ],
                4: [
                    0.0110,
                    0.032,
                    0.057,
                    0.053,
                    0.077,
                    0.070,
                    0.080,
                    0.120,
                    0.150,
                    0.110,
                    0.0110,
                    0.067,
                    0.150,
                    2.3,
                ],
            },
        }[subcategory_id][n_elements_id + 1][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements_id", [0, 1])
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_gaas(
    environment_active_id,
    n_elements_id,
    technology_id,
    test_attributes_integrated_circuit,
):
    """Returns a float value for the parts count base hazard rate on success."""
    test_attributes_integrated_circuit["environment_active_id"] = environment_active_id
    test_attributes_integrated_circuit["n_elements"] = {1: [10, 100], 2: [1000, 10000]}[
        technology_id
    ][n_elements_id]
    test_attributes_integrated_circuit["subcategory_id"] = 9
    test_attributes_integrated_circuit["technology_id"] = technology_id
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        test_attributes_integrated_circuit
    )

    assert isinstance(_lambda_b, float)
    assert (
        _lambda_b
        == {
            1: {
                1: [
                    0.019,
                    0.034,
                    0.046,
                    0.039,
                    0.052,
                    0.065,
                    0.068,
                    0.11,
                    0.12,
                    0.076,
                    0.019,
                    0.049,
                    0.086,
                    0.61,
                ],
                2: [
                    0.025,
                    0.047,
                    0.067,
                    0.058,
                    0.079,
                    0.091,
                    0.097,
                    0.15,
                    0.17,
                    0.11,
                    0.025,
                    0.073,
                    0.14,
                    1.3,
                ],
            },
            2: {
                1: [
                    0.0085,
                    0.030,
                    0.057,
                    0.057,
                    0.084,
                    0.060,
                    0.073,
                    0.080,
                    0.12,
                    0.11,
                    0.0085,
                    0.071,
                    0.17,
                    3.0,
                ],
                2: [
                    0.0140,
                    0.053,
                    0.100,
                    0.100,
                    0.150,
                    0.110,
                    0.130,
                    0.140,
                    0.22,
                    0.21,
                    0.0140,
                    0.130,
                    0.31,
                    5.5,
                ],
            },
        }[technology_id][n_elements_id + 1][environment_active_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_invalid_environment_id(
    test_attributes_integrated_circuit,
):
    """Raises an IndexError when passed an invalid active environment ID."""
    test_attributes_integrated_circuit["environment_active_id"] = 22
    with pytest.raises(
        IndexError,
        match=r"get_part_count_lambda_b: Invalid integrated circuit environment ID 22.",
    ):
        integratedcircuit.get_part_count_lambda_b(test_attributes_integrated_circuit)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_invalid_technology_id(
    test_attributes_integrated_circuit,
):
    """Raises a KeyError when passed an unknown technology ID."""
    test_attributes_integrated_circuit["subcategory_id"] = 2
    test_attributes_integrated_circuit["technology_id"] = 22
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid integrated circuit subcategory ID 2 "
        r"or technology ID 22.",
    ):
        integratedcircuit.get_part_count_lambda_b(test_attributes_integrated_circuit)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_part_count_lambda_b_invalid_subcategory_id(
    test_attributes_integrated_circuit,
):
    """Raises a KeyError when passed an unknown technology ID."""
    test_attributes_integrated_circuit["subcategory_id"] = 22
    with pytest.raises(
        KeyError,
        match=r"get_part_count_lambda_b: Invalid integrated circuit subcategory ID 22 "
        r"or technology ID 1.",
    ):
        integratedcircuit.get_part_count_lambda_b(test_attributes_integrated_circuit)


@pytest.mark.unit
@pytest.mark.parametrize("quality_id", [1, 2, 3])
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_quality_factor(
    quality_id,
    test_attributes_integrated_circuit,
):
    """Returns a float value for the quality factor on success."""
    test_attributes_integrated_circuit["quality_id"] = quality_id
    _pi_q = integratedcircuit.get_quality_factor(test_attributes_integrated_circuit)

    assert isinstance(_pi_q, float)
    assert _pi_q == {1: 0.25, 2: 1.0, 3: 2.0}[quality_id]


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_quality_factor_invalid_quality_id(
    test_attributes_integrated_circuit,
):
    """Raises an IndexError when passed an invalid quality ID.."""
    test_attributes_integrated_circuit["quality_id"] = 12
    with pytest.raises(
        IndexError,
        match=r"get_quality_factor: Invalid integrated circuit quality ID 12.",
    ):
        integratedcircuit.get_quality_factor(test_attributes_integrated_circuit)


@pytest.mark.unit
@pytest.mark.parametrize(
    "environment_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
)
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_environment_factor(
    environment_id,
    test_attributes_integrated_circuit,
):
    """Returned a float value for the environment factor (piE) on success."""
    test_attributes_integrated_circuit["environment_active_id"] = environment_id
    _pi_e = integratedcircuit.get_environment_factor(test_attributes_integrated_circuit)

    assert isinstance(_pi_e, float)
    assert (
        _pi_e
        == [
            0.5,
            2.0,
            4.0,
            4.0,
            6.0,
            4.0,
            5.0,
            5.0,
            8.0,
            8.0,
            0.5,
            5.0,
            12.0,
            220.0,
        ][environment_id - 1]
    )


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_get_environment_factor_invalid_environment_id(
    test_attributes_integrated_circuit,
):
    """Returned a float value for the environment factor (piE) on success."""
    test_attributes_integrated_circuit["environment_active_id"] = 57
    with pytest.raises(
        IndexError,
        match=r"get_environment_factor: Invalid integrated circuit environment ID 57.",
    ):
        integratedcircuit.get_environment_factor(test_attributes_integrated_circuit)


@pytest.mark.unit
def test_calculate_junction_temperature():
    """Returns a float value for Tj on success."""
    _t_j = integratedcircuit.calculate_junction_temperature(48.2, 0.038, 125.0)

    assert isinstance(_t_j, float)
    assert _t_j == 52.95


@pytest.mark.unit
@pytest.mark.parametrize("subcategory_id", [1, 2, 9])
def test_calculate_temperature_factor(subcategory_id):
    """calculate_temperature_factor() should return a float value for piT on success."""
    _pi_t = integratedcircuit.calculate_temperature_factor(subcategory_id, 1, 1, 52.95)

    assert isinstance(_pi_t, float)
    assert _pi_t == pytest.approx(
        {
            1: 1.03977861,
            2: 0.42248352,
            9: 4.7711982e-07,
        }[subcategory_id]
    )


@pytest.mark.unit
def test_calculate_temperature_factor_invalid_subcategory_id():
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"calculate_temperature_factor: Invalid integrated circuit "
        r"subcategory ID 14.",
    ):
        integratedcircuit.calculate_temperature_factor(14, 1, 1, 52.95)


@pytest.mark.unit
def test_calculate_temperature_factor_invalid_family_id():
    """Raises an IndexError when passed an invalid family ID."""
    with pytest.raises(
        IndexError,
        match=r"calculate_temperature_factor: Invalid integrated circuit family "
        r"ID 21 or type ID 1.",
    ):
        integratedcircuit.calculate_temperature_factor(2, 21, 1, 52.95)


@pytest.mark.unit
def test_calculate_temperature_factor_invalid_type_id():
    """Raises an IndexError when passed an invalid type ID."""
    with pytest.raises(
        IndexError,
        match=r"calculate_temperature_factor: Invalid integrated circuit "
        r"family ID 1 or type ID 21.",
    ):
        integratedcircuit.calculate_temperature_factor(9, 1, 21, 52.95)


@pytest.mark.unit
@pytest.mark.parametrize(
    "subcategory_id",
    [2, 3, 9],
)
@pytest.mark.parametrize(
    "technology_id",
    [1, 11],
)
def test_get_die_complexity_factor(
    subcategory_id,
    technology_id,
):
    """Returns a float value for C1 on success."""
    if subcategory_id == 3 and technology_id == 11:
        _n_elements = 64000
    else:
        _n_elements = 1000
    if subcategory_id != 2 and technology_id == 11:
        technology_id = 2

    _c1 = integratedcircuit.get_die_complexity_factor(
        subcategory_id, technology_id, 1, _n_elements
    )

    assert isinstance(_c1, float)
    assert (
        _c1
        == {
            2: {1: 0.005, 11: 0.02},
            3: {1: 0.021, 2: 0.0017},
            9: {1: 7.2, 2: 51.0},
        }[
            subcategory_id
        ][technology_id]
    )


@pytest.mark.unit
def test_get_die_complexity_factor_invalid_subcategory_id():
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"get_die_complexity_factor: Invalid integrated circuit application ID "
        r"1, subcategory ID 14, or technology ID 1.",
    ):
        integratedcircuit.get_die_complexity_factor(14, 1, 1, 100)


@pytest.mark.unit
def test_get_die_complexity_factor_invalid_technology_id():
    """Raises a KeyError when passed an invalid subcategory ID."""
    with pytest.raises(
        KeyError,
        match=r"get_die_complexity_factor: Invalid integrated circuit application "
        r"ID 1, subcategory ID 3, or technology ID 5.",
    ):
        integratedcircuit.get_die_complexity_factor(3, 5, 1, 100)


@pytest.mark.unit
def test_get_die_complexity_factor_invalid_application_id():
    """Raises a KeyError when passed an invalid application ID."""
    with pytest.raises(
        KeyError,
        match=r"get_die_complexity_factor: Invalid integrated circuit application "
        r"ID 10, subcategory ID 9, or technology ID 1.",
    ):
        integratedcircuit.get_die_complexity_factor(9, 1, 10, 100)


@pytest.mark.unit
def test_get_die_complexity_factor_invalid_n_elements():
    """Uses the breakpoint value for the closest number of elements when passed a non-
    key number of elements."""
    _c1 = integratedcircuit.get_die_complexity_factor(3, 1, 1, 50)

    assert isinstance(_c1, float)
    assert _c1 == 0.01


@pytest.mark.unit
@pytest.mark.parametrize(
    "package_id",
    [1, 4, 5, 6, 7],
)
def test_calculate_package_factor(package_id):
    """calculate_package_factor() should return a float value for C2 on success."""
    _c2 = integratedcircuit.calculate_package_factor(package_id, 14)

    assert isinstance(_c2, float)
    assert _c2 == pytest.approx(
        {
            1: 0.0048414596,
            4: 0.0048405626,
            5: 0.0036565733,
            6: 0.0060372423,
            7: 0.0062247337,
        }[package_id]
    )


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2, 3])
def test_get_error_correction_factor(type_id):
    """get_error_correction_factor() should return a float value for piECC on
    success."""
    _pi_ecc = integratedcircuit.get_error_correction_factor(type_id)

    assert isinstance(_pi_ecc, float)
    assert _pi_ecc == {1: 1.0, 2: 0.72, 3: 0.68}[type_id]


@pytest.mark.unit
def test_get_error_correction_factor_invalid_type_id():
    """Raises a KeyError when passed an invalid type ID."""
    with pytest.raises(
        KeyError,
        match=r"get_error_correction_factor: Invalid integrated circuit type ID 13.",
    ):
        integratedcircuit.get_error_correction_factor(13)


@pytest.mark.unit
@pytest.mark.parametrize("construction_id", [1, 2, 3])
@pytest.mark.parametrize("n_cycles", [10000, 350000])
def test_calculate_lambda_cyclic_factors(construction_id, n_cycles):
    """Returns a tuple float values for A1, A2, B1, and B2 on success."""
    (_a_1, _a_2, _b_1, _b_2) = integratedcircuit.calculate_lambda_cyclic_factors(
        n_cycles, construction_id, 16000, 52.95
    )

    assert isinstance(_a_1, float)
    assert isinstance(_a_2, float)
    assert isinstance(_b_1, float)
    assert isinstance(_b_2, float)
    if construction_id == 1:
        assert _a_1 == {10000: 0.06817, 350000: 2.3859500000000002}[n_cycles]
        assert _a_2 == 0.0
        assert _b_1 == pytest.approx(0.89324453)
        assert _b_2 == 0.0
    elif construction_id == 2 and n_cycles == 10000:
        assert _a_1 == 0.06817
        assert _a_2 == 2.3
        assert _b_1 == pytest.approx(0.54018825)
        assert _b_2 == pytest.approx(0.97681617)
    elif construction_id == 2 and n_cycles == 350000:
        assert _a_1 == pytest.approx(2.38595)
        assert _a_2 == 1.1
        assert _b_1 == pytest.approx(0.54018825)
        assert _b_2 == pytest.approx(0.97681617)
    else:
        assert _a_1 == {10000: 0.06817, 350000: 2.3859500000000002}[n_cycles]
        assert _a_2 == 0.0
        assert _b_1 == 0.0
        assert _b_2 == 0.0


@pytest.mark.unit
def test_get_application_factor():
    """Returns a float value for piA on success."""
    _pi_a = integratedcircuit.get_application_factor(1, 2)

    assert isinstance(_pi_a, float)
    assert _pi_a == 3.0


@pytest.mark.unit
def test_get_application_factor_invalid_type_id():
    """Raises a KeyError when passed an invalid type ID."""
    with pytest.raises(
        KeyError,
        match=r"get_application_factor: Invalid integrated circuit type ID 13.",
    ):
        integratedcircuit.get_application_factor(13, 2)


@pytest.mark.unit
def test_get_application_factor_invalid_application_id():
    """Raises an IndexError when passed an invalid application ID."""
    with pytest.raises(
        IndexError,
        match=r"get_application_factor: Invalid integrated circuit application ID 22.",
    ):
        integratedcircuit.get_application_factor(1, 22)


@pytest.mark.unit
@pytest.mark.parametrize("type_id", [1, 2])
def test_get_die_base_hazard_rate(type_id):
    """get_die_base_hazard_rate() should return a float value for lambdaBD on
    success."""
    _lambda_bd = integratedcircuit.get_die_base_hazard_rate(type_id)

    assert isinstance(_lambda_bd, float)
    assert _lambda_bd == {1: 0.16, 2: 0.24}[type_id]


@pytest.mark.unit
def test_calculate_package_base_hazard_rate():
    """Returns a float value for lambdaBP on success."""
    _lambda_bp = integratedcircuit.calculate_package_base_hazard_rate(32)

    assert isinstance(_lambda_bp, float)
    assert _lambda_bp == 0.0027504


@pytest.mark.unit
def test_calculate_die_complexity_factor():
    """Returns a float value for piCD on success."""
    _pi_cd = integratedcircuit.calculate_die_complexity_factor(0.4, 1.25)

    assert isinstance(_pi_cd, float)
    assert _pi_cd == pytest.approx(3.48076190)


@pytest.mark.unit
def test_calculate_die_complexity_factor_zero_feature():
    """Raises a ZeroDivisionError when passed a feature size=0.0."""
    with pytest.raises(
        ZeroDivisionError,
        match=r"calculate_die_complexity_factor: Integrated circuit feature size must "
        r"be greater than zero.",
    ):
        integratedcircuit.calculate_die_complexity_factor(0.4, 0.0)


@pytest.mark.unit
def test_calculate_eos_hazard_rate():
    """calculate_eos_hazard_rate() should return a float value for lambdaEOS on
    success."""
    _lambda_eos = integratedcircuit.calculate_eos_hazard_rate(2000)

    assert isinstance(_lambda_eos, float)
    assert _lambda_eos == pytest.approx(0.043625050)


@pytest.mark.unit
@pytest.mark.parametrize("manufacturing_id", [1, 2])
def test_get_manufacturing_process_factor(manufacturing_id):
    """Returns a float value for piMFG on success."""
    _pi_mfg = integratedcircuit.get_manufacturing_process_factor(manufacturing_id)

    assert isinstance(_pi_mfg, float)
    assert _pi_mfg == {1: 0.55, 2: 2.0}[manufacturing_id]


@pytest.mark.unit
@pytest.mark.parametrize("package_id", [1, 2, 3, 7, 8, 9])
def test_get_package_type_correction_factor(package_id):
    """get_package_type_correction_factor() should return a float value for piPt on
    success."""
    _pi_pt = integratedcircuit.get_package_type_correction_factor(package_id)

    assert isinstance(_pi_pt, float)
    assert _pi_pt == {1: 1.0, 7: 1.3, 2: 2.2, 8: 2.9, 3: 4.7, 9: 6.1}[package_id]


@pytest.mark.unit
def test_get_package_type_correction_factor_invalid_package_id():
    """Raises a KeyError when passed an invalid package ID."""
    with pytest.raises(
        KeyError,
        match=r"get_package_type_correction_factor: Invalid integrated circuit "
        r"package ID 12.",
    ):
        integratedcircuit.get_package_type_correction_factor(12)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_calculate_part_stress(
    test_attributes_integrated_circuit,
):
    """calculate_part_stress() should return a the attributes dict updated with
    calculated values."""
    test_attributes_integrated_circuit["subcategory_id"] = 1
    _attributes = integratedcircuit.calculate_part_stress(
        test_attributes_integrated_circuit
    )

    assert isinstance(_attributes, dict)
    assert _attributes["piL"] == pytest.approx(0.73699794)
    assert _attributes["C1"] == 0.01
    assert _attributes["C2"] == pytest.approx(0.011822791)
    assert _attributes["temperature_junction"] == 53.05
    assert _attributes["piT"] == pytest.approx(1.04718497)
    assert _attributes["hazard_rate_active"] == pytest.approx(0.032862208)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_calculate_part_stress_gaas(
    test_attributes_integrated_circuit,
):
    """calculate_part_stress() should return a the attributes dict updated with
    calculated values."""
    test_attributes_integrated_circuit["subcategory_id"] = 9
    test_attributes_integrated_circuit["n_elements"] = 1000
    _attributes = integratedcircuit.calculate_part_stress(
        test_attributes_integrated_circuit
    )

    assert isinstance(_attributes, dict)
    assert _attributes["piL"] == pytest.approx(0.73699794)
    assert _attributes["C1"] == 4.5
    assert _attributes["C2"] == pytest.approx(0.011822791)
    assert _attributes["temperature_junction"] == 53.05
    assert _attributes["piT"] == pytest.approx(4.84999145e-07)
    assert _attributes["piA"] == 3.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.017436396)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_calculate_part_stress_vlsi(
    test_attributes_integrated_circuit,
):
    """calculate_part_stress() should return a the attributes dict updated with
    calculated values."""
    test_attributes_integrated_circuit["subcategory_id"] = 10
    test_attributes_integrated_circuit["n_elements"] = 100
    _attributes = integratedcircuit.calculate_part_stress(
        test_attributes_integrated_circuit
    )

    assert isinstance(_attributes, dict)
    assert _attributes["lambdaBD"] == 0.16
    assert _attributes["lambdaBP"] == 0.0027504
    assert _attributes["lambdaEOS"] == pytest.approx(0.043625050)
    assert _attributes["temperature_junction"] == 53.05
    assert _attributes["piCD"] == pytest.approx(9.88380952)
    assert _attributes["piMFG"] == 0.55
    assert _attributes["piPT"] == 1.0
    assert _attributes["hazard_rate_active"] == pytest.approx(0.35719656)


@pytest.mark.unit
@pytest.mark.usefixtures("test_attributes_integrated_circuit")
def test_calculate_part_stress_invalid_subcategory_id(
    test_attributes_integrated_circuit,
):
    """Raises a KeyError when passed an invalid subcategory ID."""
    test_attributes_integrated_circuit.pop("subcategory_id")
    with pytest.raises(
        KeyError,
        match=r"calculate_part_stress: Missing required integrated circuit "
        r"attribute: \'subcategory_id\'.",
    ):
        integratedcircuit.calculate_part_stress(test_attributes_integrated_circuit)
