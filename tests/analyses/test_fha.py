# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_fha.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the FHA module."""

# Standard Library Imports
from collections import OrderedDict

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import fha
from ramstk.exceptions import OutOfRangeError

TEST_FHA = OrderedDict({
    _key: None
    for _key in [
        'uf1', 'uf2', 'uf3', 'ui1', 'ui2', 'ui3', 'equation1', 'equation2',
        'equation3', 'equation4', 'equation5', 'res1', 'res2', 'res3', 'res4',
        'res5'
    ]
})


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_hri():
    """calculate_hri() should return the product of probability and severity on success."""
    assert fha.calculate_hri('Level A - Frequent', 'Medium') == 20


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_hri_unknown_probability():
    """calculate_hri() should raise a KeyError when passed an unknown probability description."""
    with pytest.raises(OutOfRangeError) as e:
        fha.calculate_hri('shibboly-biboly-boo', 'Medium')
    assert e.value.args[0] == ("calculate_hri() was passed an unknown hazard "
                               "probability (shibboly-biboly-boo) or severity "
                               "(Medium) description.")


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_hri_unknown_severity():
    """calculate_hri() should raise a KeyError when passed an unknown probability description."""
    with pytest.raises(OutOfRangeError) as e:
        fha.calculate_hri('Level A - Frequent', 'shibboly-biboly-boo')
    assert e.value.args[0] == ("calculate_hri() was passed an unknown hazard "
                               "probability (Level A - Frequent) or severity "
                               "(shibboly-biboly-boo) description.")


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_floats():
    """set_user_defined_floats() should return an updated similar item assessment dict on success."""
    _fha = fha.set_user_defined_floats(TEST_FHA, [3.4, 7.8, 11.12])

    assert isinstance(_fha, dict)
    assert _fha['uf1'] == 3.4
    assert _fha['uf2'] == 7.8
    assert _fha['uf3'] == 11.12


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_floats_set_unused_zero():
    """set_user_defined_floats() should set unused floats to zero."""
    _fha = fha.set_user_defined_floats(TEST_FHA, [3.4, 7.8])

    assert isinstance(_fha, dict)
    assert _fha['uf1'] == 3.4
    assert _fha['uf2'] == 7.8
    assert _fha['uf3'] == 0.0


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_ints():
    """set_user_defined_ints() should return an updated similar item assessment dict on success."""
    _fha = fha.set_user_defined_ints(TEST_FHA, [4, 7, 11])

    assert isinstance(_fha, dict)
    assert _fha['ui1'] == 4
    assert _fha['ui2'] == 7
    assert _fha['ui3'] == 11


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_ints_set_unused_zero():
    """set_user_defined_ints() should set unused ints to zero."""
    _fha = fha.set_user_defined_ints(TEST_FHA, [4])

    assert isinstance(_fha, dict)
    assert _fha['ui1'] == 4
    assert _fha['ui2'] == 0
    assert _fha['ui3'] == 0


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_functions():
    """set_user_defined_functions() should return an updated functional hazzard assessment dict on success."""
    _fha = fha.set_user_defined_functions(
        TEST_FHA,
        ['hr*pi1*pi2*uf1', 'ui1+ui2', 'res2*pi4', 'res1-uf3', 'hr*(pi3+pi5)'])

    assert isinstance(_fha, dict)
    assert _fha['equation1'] == 'hr*pi1*pi2*uf1'
    assert _fha['equation2'] == 'ui1+ui2'
    assert _fha['equation3'] == 'res2*pi4'
    assert _fha['equation4'] == 'res1-uf3'
    assert _fha['equation5'] == 'hr*(pi3+pi5)'


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_functions_set_unused_empty():
    """set_user_defined_functions() should set unused functions to an empty string."""
    _fha = fha.set_user_defined_functions(TEST_FHA,
                                          ['hr*pi1*pi2*uf1', 'ui1+ui2'])

    assert isinstance(_fha, dict)
    assert _fha['equation1'] == 'hr*pi1*pi2*uf1'
    assert _fha['equation2'] == 'ui1+ui2'
    assert _fha['equation3'] == '0.0'
    assert _fha['equation4'] == '0.0'
    assert _fha['equation5'] == '0.0'


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_results():
    """set_user_defined_results() should return an updated similar item assessment dict on success."""
    _fha = fha.set_user_defined_results(TEST_FHA,
                                        [3.4, 7.8, 11.12, 15.16, 19.2])

    assert isinstance(_fha, dict)
    assert _fha['res1'] == 3.4
    assert _fha['res2'] == 7.8
    assert _fha['res3'] == 11.12
    assert _fha['res4'] == 15.16
    assert _fha['res5'] == 19.2


@pytest.mark.unit
@pytest.mark.calculation
def test_set_user_defined_results_set_unused_zero():
    """set_user_defined_results() should set unused results to zero."""
    _fha = fha.set_user_defined_results(TEST_FHA, [3.4, 7.8, 11.12, 15.16])

    assert isinstance(_fha, dict)
    assert _fha['res1'] == 3.4
    assert _fha['res2'] == 7.8
    assert _fha['res3'] == 11.12
    assert _fha['res4'] == 15.16
    assert _fha['res5'] == 0.0


@pytest.mark.unit
def test_calculate_user_defined():
    """calculate() should return False when calculating user-defined risks."""
    _fha = fha.set_user_defined_functions(
        TEST_FHA,
        ['uf1*uf2', 'ui1+ui2', 'res2*uf3', 'res1-uf3', 'res1*(ui3+uf1)'])

    _fha = fha.calculate_user_defined(_fha)
    assert _fha['res1'] == 26.52
    assert _fha['res2'] == 4
    assert _fha['res3'] == 0.0
    assert _fha['res4'] == 26.52
    assert _fha['res5'] == pytest.approx(90.168)
