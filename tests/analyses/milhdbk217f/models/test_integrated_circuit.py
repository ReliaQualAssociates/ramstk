# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.models.test_integrated_circuit.py is part of
#       The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the integrated circuit module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import integratedcircuit

ATTRIBUTES = {
    'category_id': 1,
    'subcategory_id': 1,
    'application_id': 2,
    'area': 0.5,
    'environment_active_id': 3,
    'family_id': 2,
    'feature_size': 0.8,
    'manufacturing_id': 1,
    'n_elements': 100,
    'n_active_pins': 32,
    'package_id': 1,
    'power_operating': 0.038,
    'technology_id': 1,
    'temperature_case': 48.3,
    'theta_jc': 125,
    'type_id': 1,
    'voltage_esd': 2000,
    'years_in_production': 3,
    'piE': 1.0,
    'piQ': 2.0
}


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("n_elements", [100, 300, 1000, 10000])
def test_get_part_count_lambda_b_linear(environment_active_id, n_elements):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        n_elements,
        id_keys={
            'subcategory_id': 1,
            'environment_active_id': environment_active_id,
            'technology_id': -1
        })

    assert isinstance(_lambda_b, float)
    if n_elements == 100:
        assert _lambda_b == [
            0.0095, 0.024, 0.039, 0.034, 0.049, 0.057, 0.062, 0.12, 0.13,
            0.076, 0.0095, 0.044, 0.096, 1.1
        ][environment_active_id - 1]
    elif n_elements == 300:
        assert _lambda_b == [
            0.0170, 0.041, 0.065, 0.054, 0.078, 0.100, 0.110, 0.22, 0.24,
            0.130, 0.0170, 0.072, 0.150, 1.4
        ][environment_active_id - 1]
    elif n_elements == 1000:
        assert _lambda_b == [
            0.0330, 0.074, 0.110, 0.092, 0.130, 0.190, 0.190, 0.41, 0.44,
            0.220, 0.0330, 0.120, 0.260, 2.0
        ][environment_active_id - 1]
    elif n_elements == 10000:
        assert _lambda_b == [
            0.0500, 0.120, 0.180, 0.150, 0.210, 0.300, 0.300, 0.63, 0.67,
            0.350, 0.0500, 0.190, 0.410, 3.4
        ][environment_active_id - 1]


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements", [100, 1000, 3000, 10000, 30000, 60000])
def test_get_part_count_lambda_b_logic(technology_id, environment_active_id,
                                       n_elements):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        n_elements,
        id_keys={
            'subcategory_id': 2,
            'environment_active_id': environment_active_id,
            'technology_id': technology_id
        })

    assert isinstance(_lambda_b, float)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements_id", [0, 1, 2])
def test_get_part_count_lambda_b_pal_pla(technology_id, environment_active_id,
                                         n_elements_id):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _n_elements = {
        1: [200, 1000, 5000],
        2: [16000, 64000, 256000, 1000000]
    }[technology_id][n_elements_id]

    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        _n_elements,
        id_keys={
            'subcategory_id': 3,
            'environment_active_id': environment_active_id,
            'technology_id': technology_id
        })

    assert isinstance(_lambda_b, float)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements", [8, 16, 32])
def test_get_part_count_lambda_b_mup_muc(technology_id, environment_active_id,
                                         n_elements):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        n_elements,
        id_keys={
            'subcategory_id': 4,
            'environment_active_id': environment_active_id,
            'technology_id': technology_id
        })

    assert isinstance(_lambda_b, float)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [5, 8],
)
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements", [16000, 64000, 256000, 100000])
def test_get_part_count_lambda_b_rom_sram(subcategory_id, technology_id,
                                          environment_active_id, n_elements):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        n_elements,
        id_keys={
            'subcategory_id': subcategory_id,
            'environment_active_id': environment_active_id,
            'technology_id': technology_id
        })

    assert isinstance(_lambda_b, float)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [6, 7],
)
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("n_elements", [16000, 64000, 256000, 100000])
def test_get_part_count_lambda_b_prom_dram(subcategory_id,
                                           environment_active_id, n_elements):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        n_elements,
        id_keys={
            'subcategory_id': subcategory_id,
            'environment_active_id': environment_active_id,
            'technology_id': 2
        })

    assert isinstance(_lambda_b, float)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "environment_active_id",
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
)
@pytest.mark.parametrize("technology_id", [1, 2])
@pytest.mark.parametrize("n_elements_id", [0, 1])
def test_get_part_count_lambda_b_gaas(environment_active_id, n_elements_id,
                                      technology_id):
    """get_part_count_lambda_b() should return a float value for the parts count base hazard rate on success."""
    _n_elements = {
        1: [10, 100],
        2: [1000, 10000]
    }[technology_id][n_elements_id]
    _lambda_b = integratedcircuit.get_part_count_lambda_b(
        _n_elements,
        id_keys={
            'subcategory_id': 9,
            'environment_active_id': environment_active_id,
            'technology_id': technology_id
        })

    assert isinstance(_lambda_b, float)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_environment():
    """get_part_count_lambda_b() should raise an IndexError when passed an unknown active environment."""
    with pytest.raises(ValueError):
        _lambda_b = integratedcircuit.get_part_count_lambda_b(
            300,
            id_keys={
                'subcategory_id': 3,
                'environment_active_id': 22,
                'technology_id': 2
            })


@pytest.mark.unit
@pytest.mark.calculation
def test_get_part_count_lambda_b_no_technology():
    """get_part_count_lambda_b() should raise a KeyError when passed an unknown technology_id."""
    with pytest.raises(KeyError):
        _lambda_b = integratedcircuit.get_part_count_lambda_b(
            300,
            id_keys={
                'subcategory_id': 3,
                'environment_active_id': 2,
                'technology_id': 4
            })


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_count_linear():
    """calculate_part_count() should return a float value for the parts count base hazard rate on success."""
    _lambda_b = integratedcircuit.calculate_part_count(**ATTRIBUTES)

    assert isinstance(_lambda_b, float)
    assert _lambda_b == 0.039


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "subcategory_id",
    [2, 3, 9],
)
@pytest.mark.parametrize(
    "technology_id",
    [1, 11],
)
def test_get_die_complexity_factor(subcategory_id, technology_id):
    """get_die_complexity_factor() should return a float value for C1 on success."""
    if subcategory_id == 3 and technology_id == 11:
        _n_elements = 64000
    else:
        _n_elements = 1000
    if subcategory_id != 2 and technology_id == 11:
        technology_id = 2

    _c1 = integratedcircuit.get_die_complexity_factor(subcategory_id,
                                                      technology_id, 1,
                                                      _n_elements)

    assert isinstance(_c1, float)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_die_complexity_factor_no_subcategory():
    """get_die_complexity_factor() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _c1 = integratedcircuit.get_die_complexity_factor(14, 1, 1, 100)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_die_complexity_factor_no_technology():
    """get_die_complexity_factor() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _c1 = integratedcircuit.get_die_complexity_factor(3, 5, 1, 100)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_die_complexity_factor_no_application():
    """get_die_complexity_factor() should raise a KeyError when passed an unknown application ID."""
    with pytest.raises(KeyError):
        _c1 = integratedcircuit.get_die_complexity_factor(9, 1, 10, 100)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_die_complexity_factor_unknown_n_elements():
    """get_die_complexity_factor() should raise a ValueError when passed an unknown number of elements."""
    with pytest.raises(ValueError):
        _c1 = integratedcircuit.get_die_complexity_factor(1, 1, 1, 10930)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize(
    "package_id",
    [1, 4, 5, 6, 7],
)
def test_calculate_package_factor(package_id):
    """calculate_package_factor() should return a float value for C2 on success."""
    _c2 = integratedcircuit.calculate_package_factor(package_id, 14)

    assert isinstance(_c2, float)
    if package_id == 1:
        assert _c2 == pytest.approx(0.0048414596)
    elif package_id == 4:
        assert _c2 == pytest.approx(0.0048405626)
    elif package_id == 5:
        assert _c2 == pytest.approx(0.0036565733)
    elif package_id == 6:
        assert _c2 == pytest.approx(0.0060372423)
    elif package_id == 7:
        assert _c2 == pytest.approx(0.0062247337)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_junction_temperature():
    """calculate_junction_temperature() should return a float value for Tj on success."""
    _t_j = integratedcircuit.calculate_junction_temperature(48.2, 0.038, 125.0)

    assert isinstance(_t_j, float)
    assert _t_j == 52.95


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("subcategory_id", [1, 2, 9])
def test_calculate_temperature_factor(subcategory_id):
    """calculate_temperature_factor() should return a float value for piT on success."""
    _pi_t = integratedcircuit.calculate_temperature_factor(
        subcategory_id, 1, 1, 52.95)

    assert isinstance(_pi_t, float)
    if subcategory_id == 1:
        assert _pi_t == pytest.approx(1.03977861)
    elif subcategory_id == 2:
        assert _pi_t == pytest.approx(0.42248352)
    elif subcategory_id == 9:
        assert _pi_t == pytest.approx(4.7711982e-07)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_factor_no_subcategory():
    """calculate_temperature_factor() should raise a KeyError when passed an unknown subcategory ID."""
    with pytest.raises(KeyError):
        _pi_t = integratedcircuit.calculate_temperature_factor(14, 1, 1, 52.95)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_factor_no_family():
    """calculate_temperature_factor() should raise an IndexError when passed an unknown family ID."""
    with pytest.raises(IndexError):
        _pi_t = integratedcircuit.calculate_temperature_factor(2, 21, 1, 52.95)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_temperature_factor_no_type():
    """calculate_temperature_factor() should raise an IndexError when passed an unknown type ID."""
    with pytest.raises(IndexError):
        _pi_t = integratedcircuit.calculate_temperature_factor(9, 1, 21, 52.95)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_application_factor():
    """get_application_factor() should return a float value for piA on success."""
    _pi_a = integratedcircuit.get_application_factor(1, 2)

    assert isinstance(_pi_a, float)
    assert _pi_a == 3.0


@pytest.mark.unit
@pytest.mark.calculation
def test_get_application_factor_no_type():
    """get_application_factor() should raise a KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        _pi_a = integratedcircuit.get_application_factor(13, 2)


@pytest.mark.unit
@pytest.mark.calculation
def test_get_application_factor_no_application():
    """get_application_factor() should raise an IndexError when passed an unknown application ID."""
    with pytest.raises(IndexError):
        _pi_a = integratedcircuit.get_application_factor(1, 22)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("type_id", [1, 2, 3])
def test_get_error_correction_factor(type_id):
    """get_error_correction_factor() should return a float value for piECC on success."""
    _pi_ecc = integratedcircuit.get_error_correction_factor(type_id)

    assert isinstance(_pi_ecc, float)
    if type_id == 1:
        assert _pi_ecc == 1.0
    elif type_id == 2:
        assert _pi_ecc == 0.72
    elif type_id == 3:
        assert _pi_ecc == 0.68


@pytest.mark.unit
@pytest.mark.calculation
def test_get_error_correction_factor_no_type():
    """get_error_correction_factor() should raise a KeyError when passed an unknown type ID."""
    with pytest.raises(KeyError):
        _pi_a = integratedcircuit.get_error_correction_factor(13)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("construction_id", [1, 2, 3])
@pytest.mark.parametrize("n_cycles", [10000, 350000])
def test_calculate_lambda_cyclic_factors(construction_id, n_cycles):
    """calculate_lambda_cyclic_factors() should return a tuple float values for A1, A2, B1, and B2 on success."""
    (_a_1, _a_2, _b_1,
     _b_2) = integratedcircuit.calculate_lambda_cyclic_factors(
         n_cycles, construction_id, 16000, 52.95)

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
@pytest.mark.calculation
@pytest.mark.parametrize("type_id", [1, 2])
def test_get_die_base_hazard_rate(type_id):
    """get_die_base_hazard_rate() should return a float value for lambdaBD on success."""
    _lambda_bd = integratedcircuit.get_die_base_hazard_rate(type_id)

    assert isinstance(_lambda_bd, float)
    if type_id == 1:
        assert _lambda_bd == 0.16
    else:
        assert _lambda_bd == 0.24


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("manufacturing_id", [1, 2])
def test_get_manufacturing_process_factor(manufacturing_id):
    """get_manufacturing_process_factor() should return a float value for piMFG on success."""
    _pi_mfg = integratedcircuit.get_manufacturing_process_factor(
        manufacturing_id)

    assert isinstance(_pi_mfg, float)
    if manufacturing_id == 1:
        assert _pi_mfg == 0.55
    else:
        assert _pi_mfg == 2.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_die_complexity_factor():
    """calculate_die_complexity_factor() should return a float value for piCD on success."""
    _pi_cd = integratedcircuit.calculate_die_complexity_factor(0.4, 1.25)

    assert isinstance(_pi_cd, float)
    assert _pi_cd == pytest.approx(3.48076190)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_die_complexity_factor_zero_feature():
    """calculate_die_complexity_factor() should raise a ZeroDivisionError when passed a feature size=0.0."""
    with pytest.raises(ZeroDivisionError):
        _pi_cd = integratedcircuit.calculate_die_complexity_factor(0.4, 0.0)


@pytest.mark.unit
@pytest.mark.calculation
@pytest.mark.parametrize("package_id", [1, 2, 3, 7, 8, 9])
def test_get_package_type_correction_factor(package_id):
    """get_package_type_correction_factor() should return a float value for piPt on success."""
    _pi_pt = integratedcircuit.get_package_type_correction_factor(package_id)

    assert isinstance(_pi_pt, float)
    assert _pi_pt == {
        1: 1.0,
        7: 1.3,
        2: 2.2,
        8: 2.9,
        3: 4.7,
        9: 6.1
    }[package_id]


@pytest.mark.unit
@pytest.mark.calculation
def test_get_package_type_correction_factor_no_package():
    """get_package_type_correction_factor() should raise a KeyError when passed an unknown package ID."""
    with pytest.raises(KeyError):
        _pi_pt = integratedcircuit.get_package_type_correction_factor(12)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_package_base_hazard_rate():
    """calculate_package_base_hazard_rate() should return a float value for lambdaBP on success."""
    _lambda_bp = integratedcircuit.calculate_package_base_hazard_rate(32)

    assert isinstance(_lambda_bp, float)
    assert _lambda_bp == 0.0027504


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_eos_hazard_rate():
    """calculate_eos_hazard_rate() should return a float value for lambdaEOS on success."""
    _lambda_eos = integratedcircuit.calculate_eos_hazard_rate(2000)

    assert isinstance(_lambda_eos, float)
    assert _lambda_eos == pytest.approx(0.043625050)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress():
    """calculate_part_stress() should return a the attributes dict updated with calculated values."""
    ATTRIBUTES['subcategory_id'] = 1
    _attributes = integratedcircuit.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['piL'] == pytest.approx(0.73699794)
    assert _attributes['C1'] == 0.01
    assert _attributes['C2'] == pytest.approx(0.011822791)
    assert _attributes['temperature_junction'] == 53.05
    assert _attributes['piT'] == pytest.approx(1.04718497)
    assert _attributes['hazard_rate_active'] == pytest.approx(0.032862208)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_gaas():
    """calculate_part_stress() should return a the attributes dict updated with calculated values."""
    ATTRIBUTES['subcategory_id'] = 9
    ATTRIBUTES['n_elements'] = 1000
    _attributes = integratedcircuit.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['piL'] == pytest.approx(0.73699794)
    assert _attributes['C1'] == 4.5
    assert _attributes['C2'] == pytest.approx(0.011822791)
    assert _attributes['temperature_junction'] == 53.05
    assert _attributes['piT'] == pytest.approx(4.84999145e-07)
    assert _attributes['piA'] == 3.0
    assert _attributes['hazard_rate_active'] == pytest.approx(0.017436396)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_part_stress_vlsi():
    """calculate_part_stress() should return a the attributes dict updated with calculated values."""
    ATTRIBUTES['subcategory_id'] = 10
    ATTRIBUTES['n_elements'] = 100
    _attributes = integratedcircuit.calculate_part_stress(**ATTRIBUTES)

    assert isinstance(_attributes, dict)
    assert _attributes['lambdaBD'] == 0.16
    assert _attributes['lambdaBP'] == 0.0027504
    assert _attributes['lambdaEOS'] == pytest.approx(0.043625050)
    assert _attributes['temperature_junction'] == 53.05
    assert _attributes['piCD'] == pytest.approx(9.88380952)
    assert _attributes['piMFG'] == 0.55
    assert _attributes['piPT'] == 1.0
    assert _attributes['hazard_rate_active'] == pytest.approx(0.35719656)
