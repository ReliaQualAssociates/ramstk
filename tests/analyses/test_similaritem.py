# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_similaritem.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the similar item assessment module."""

# Standard Library Imports
from collections import OrderedDict

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import similaritem

TEST_SIA = OrderedDict({
    _key: None
    for _key in [
        'hr', 'pi1', 'pi2', 'pi3', 'pi3', 'pi4', 'pi5', 'pi6', 'pi7', 'pi8',
        'pi9', 'pi10', 'uf1', 'uf2', 'uf3', 'uf4', 'uf5', 'ui1', 'ui2', 'ui3',
        'ui4', 'ui5', 'equation1', 'equation2', 'equation3', 'equation4',
        'equation5', 'res1', 'res2', 'res3', 'res4', 'res5'
    ]
})
TEST_SIA['hr'] = 0.0003825


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_topic_633():
    """calculate_topic_633() should return a tuple of change factors and the result of the calculation on success."""
    environment = {'from': 4, 'to': 6}
    quality = {'from': 2, 'to': 3}
    temperature = {'from': 38.0, 'to': 27.5}

    (_change_factor_1, _change_factor_2, _change_factor_3,
     _result_1) = similaritem.calculate_topic_633(environment, quality,
                                                  temperature, 0.000003335)
    assert _change_factor_1 == 0.6
    assert _change_factor_2 == 3.3
    assert _change_factor_3 == 1.1
    assert _result_1 == pytest.approx(1.5312213e-06)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_topic_633_quality_key_error():
    """calculate_topic_633() should raise a KeyError when passed a quality dict that is missing a from or to key."""
    environment = {'from': 4, 'to': 6}
    quality = {'from': 2}
    temperature = {'from': 38.0, 'to': 27.5}

    with pytest.raises(KeyError):
        (_change_factor_1, _change_factor_2, _change_factor_3,
         _result_1) = similaritem.calculate_topic_633(environment, quality,
                                                      temperature, 0.000003335)

    quality = {'from': 2, 'to': '3'}

    with pytest.raises(KeyError):
        (_change_factor_1, _change_factor_2, _change_factor_3,
         _result_1) = similaritem.calculate_topic_633(environment, quality,
                                                      temperature, 0.000003335)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_topic_633_environment_key_error():
    """calculate_topic_633() should raise a KeyError when passed an environment dict that is missing a from or to key."""
    environment = {'to': 6}
    quality = {'from': 2, 'to': 4}
    temperature = {'from': 38.0, 'to': 27.5}

    with pytest.raises(KeyError):
        (_change_factor_1, _change_factor_2, _change_factor_3,
         _result_1) = similaritem.calculate_topic_633(environment, quality,
                                                      temperature, 0.000003335)

    environment = {'from': '4', 'to': 6}

    with pytest.raises(KeyError):
        (_change_factor_1, _change_factor_2, _change_factor_3,
         _result_1) = similaritem.calculate_topic_633(environment, quality,
                                                      temperature, 0.000003335)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_topic_633_temperature_key_error():
    """calculate_topic_633() should raise a KeyError when passed a temperature dict that is missing a from or to key."""
    environment = {'from': 4, 'to': 6}
    quality = {'from': 2, 'to': 4}
    temperature = {'from': 38.0}

    with pytest.raises(KeyError):
        (_change_factor_1, _change_factor_2, _change_factor_3,
         _result_1) = similaritem.calculate_topic_633(environment, quality,
                                                      temperature, 0.000003335)


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_topic_633_temperature_string_value():
    """calculate_topic_633() should raise a TypeError when passed a string for one or more temperature values."""
    environment = {'from': 4, 'to': 6}
    quality = {'from': 2, 'to': 4}
    temperature = {'from': '38.0', 'to': 27.5}

    with pytest.raises(TypeError):
        (_change_factor_1, _change_factor_2, _change_factor_3,
         _result_1) = similaritem.calculate_topic_633(environment, quality,
                                                      temperature, 0.000003335)


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_change_factors():
    """set_user_defined_change_factors() should return an updated similar item assessment dict on success."""
    _sia = similaritem.set_user_defined_change_factors(
        TEST_SIA, [1.2, 3.4, 5.6, 7.8, 9.10, 11.12, 13.14, 15.16, 17.18, 19.2])

    assert isinstance(_sia, dict)
    assert _sia['pi1'] == 1.2
    assert _sia['pi2'] == 3.4
    assert _sia['pi3'] == 5.6
    assert _sia['pi4'] == 7.8
    assert _sia['pi5'] == 9.10
    assert _sia['pi6'] == 11.12
    assert _sia['pi7'] == 13.14
    assert _sia['pi8'] == 15.16
    assert _sia['pi9'] == 17.18
    assert _sia['pi10'] == 19.20


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_change_factors_set_unused_none():
    """set_user_defined_change_factors() should set unused factors to None."""
    _sia = similaritem.set_user_defined_change_factors(
        TEST_SIA, [1.2, 3.4, 5.6, 7.8, 9.10])

    assert isinstance(_sia, dict)
    assert _sia['pi1'] == 1.2
    assert _sia['pi2'] == 3.4
    assert _sia['pi3'] == 5.6
    assert _sia['pi4'] == 7.8
    assert _sia['pi5'] == 9.10
    assert _sia['pi6'] == 0.0
    assert _sia['pi7'] == 0.0
    assert _sia['pi8'] == 0.0
    assert _sia['pi9'] == 0.0
    assert _sia['pi10'] == 0.0

@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_floats():
    """set_user_defined_floats() should return an updated similar item assessment dict on success."""
    _sia = similaritem.set_user_defined_floats(
        TEST_SIA, [3.4, 7.8, 11.12, 15.16, 19.2])

    assert isinstance(_sia, dict)
    assert _sia['uf1'] == 3.4
    assert _sia['uf2'] == 7.8
    assert _sia['uf3'] == 11.12
    assert _sia['uf4'] == 15.16
    assert _sia['uf5'] == 19.2


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_floats_set_unused_none():
    """set_user_defined_floats() should set unused floats to None."""
    _sia = similaritem.set_user_defined_floats(
        TEST_SIA, [3.4, 7.8])

    assert isinstance(_sia, dict)
    assert _sia['uf1'] == 3.4
    assert _sia['uf2'] == 7.8
    assert _sia['uf3'] == 0.0
    assert _sia['uf4'] == 0.0
    assert _sia['uf5'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_ints():
    """set_user_defined_ints() should return an updated similar item assessment dict on success."""
    _sia = similaritem.set_user_defined_ints(
        TEST_SIA, [3.4, 7.8, 11.12, 15.16, 19.2])

    assert isinstance(_sia, dict)
    assert _sia['ui1'] == 3
    assert _sia['ui2'] == 7
    assert _sia['ui3'] == 11
    assert _sia['ui4'] == 15
    assert _sia['ui5'] == 19


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_ints_set_unused_none():
    """set_user_defined_ints() should set unused ints to None."""
    _sia = similaritem.set_user_defined_ints(
        TEST_SIA, [3.4, 7.8, 11.12])

    assert isinstance(_sia, dict)
    assert _sia['ui1'] == 3
    assert _sia['ui2'] == 7
    assert _sia['ui3'] == 11
    assert _sia['ui4'] == 0
    assert _sia['ui5'] == 0


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_functions():
    """set_user_defined_functions() should return an updated similar item assessment dict on success."""
    _sia = similaritem.set_user_defined_functions(
        TEST_SIA, ['hr*pi1*pi2*uf1', 'ui1+ui2', 'res2*pi4', 'res1-uf3', 'hr*(pi3+pi5)'])

    assert isinstance(_sia, dict)
    assert _sia['equation1'] == 'hr*pi1*pi2*uf1'
    assert _sia['equation2'] == 'ui1+ui2'
    assert _sia['equation3'] == 'res2*pi4'
    assert _sia['equation4'] == 'res1-uf3'
    assert _sia['equation5'] == 'hr*(pi3+pi5)'


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_functions_set_unused_none():
    """set_user_defined_functions() should set unused functiosn to None."""
    _sia = similaritem.set_user_defined_functions(
        TEST_SIA, ['hr*pi1*pi2*uf1', 'ui1+ui2'])

    assert isinstance(_sia, dict)
    assert _sia['equation1'] == 'hr*pi1*pi2*uf1'
    assert _sia['equation2'] == 'ui1+ui2'
    assert _sia['equation3'] == ''
    assert _sia['equation4'] == ''
    assert _sia['equation5'] == ''


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_results():
    """set_user_defined_results() should return an updated similar item assessment dict on success."""
    _sia = similaritem.set_user_defined_results(
        TEST_SIA, [3.4, 7.8, 11.12, 15.16, 19.2])

    assert isinstance(_sia, dict)
    assert _sia['res1'] == 3.4
    assert _sia['res2'] == 7.8
    assert _sia['res3'] == 11.12
    assert _sia['res4'] == 15.16
    assert _sia['res5'] == 19.2


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_results_set_unused_none():
    """set_user_defined_results() should set unused results to None."""
    _sia = similaritem.set_user_defined_results(
        TEST_SIA, [3.4, 7.8, 11.12, 15.16])

    assert isinstance(_sia, dict)
    assert _sia['res1'] == 3.4
    assert _sia['res2'] == 7.8
    assert _sia['res3'] == 11.12
    assert _sia['res4'] == 15.16
    assert _sia['res5'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_user_defined():
    """calculate_user_defined() should return an updated similar item assessment dict on success."""
    _sia = similaritem.set_user_defined_change_factors(
        TEST_SIA, [1.2, 3.4, 5.6, 7.8, 9.10, 11.12, 13.14, 15.16, 17.18, 19.2])
    _sia = similaritem.set_user_defined_functions(
        _sia, ['hr*pi1*pi2*uf1', 'ui1+ui2', 'res2*pi4', 'res1-uf3', 'hr*(pi3+pi5)'])
    _sia = similaritem.calculate_user_defined(_sia)

    assert isinstance(_sia, dict)
    assert _sia['res1'] == pytest.approx(0.00530604)
    assert _sia['res2'] == 10
    assert _sia['res3'] == 78.0
    assert _sia['res4'] == pytest.approx(0.00530604)
    assert _sia['res5'] == pytest.approx(0.00562275)
