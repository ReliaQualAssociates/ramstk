# pylint: disable=invalid-name, protected-access
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_derating.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the electrical stress module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import Derating


@pytest.mark.unit
@pytest.mark.calculation
def test_check_overstress():
    """check_overstress() should return a dict of environ:condition pairs on success."""
    _overstress = Derating.check_overstress(
        0.625, {
            'mild': [0.0, 0.9],
            'harsh': [0.0, 0.75],
        },
    )

    assert _overstress['mild'] == [False, False]
    assert _overstress['harsh'] == [False, False]


@pytest.mark.unit
@pytest.mark.calculation
def test_check_overstress_under_limit():
    """check_overstress() should return a dict of environ:condition pairs on success with the below lower limit set to True."""
    _overstress = Derating.check_overstress(
        -0.625, {
            'mild': [0.0, 0.9],
            'harsh': [0.0, 0.75],
        },
    )

    assert _overstress['mild'] == [True, False]
    assert _overstress['harsh'] == [True, False]


@pytest.mark.unit
@pytest.mark.calculation
def test_check_overstress_over_limit_harsh():
    """check_overstress() should return a dict of environ:condition pairs on success with the above upper limit set to True for a harsh environment."""
    _overstress = Derating.check_overstress(
        0.825, {
            'mild': [0.0, 0.9],
            'harsh': [0.0, 0.75],
        },
    )

    assert _overstress['mild'] == [False, False]
    assert _overstress['harsh'] == [False, True]


@pytest.mark.unit
@pytest.mark.calculation
def test_check_overstress_over_limit_harsh_mild():
    """check_overstress() should return a dict of environ:condition pairs on success with the above upper limit set to True for both mild and harsh environments."""
    _overstress = Derating.check_overstress(
        0.925, {
            'mild': [0.0, 0.9],
            'harsh': [0.0, 0.75],
        },
    )

    assert _overstress['mild'] == [False, True]
    assert _overstress['harsh'] == [False, True]


@pytest.mark.unit
@pytest.mark.calculation
def test_check_overstress_limits_not_lists():
    """check_overstress() should raise a TypeError if the limits passed are not a list."""
    with pytest.raises(TypeError):
        _overstress = Derating.check_overstress(
            0.625, {
                'mild': 0.9,
                'harsh': 0.75,
            },
        )


@pytest.mark.unit
@pytest.mark.calculation
def test_check_overstress_only_one_limit():
    """check_overstress() should raise an IndexError if only one limit is passed in the list."""
    with pytest.raises(IndexError):
        _overstress = Derating.check_overstress(
            0.625, {
                'mild': [
                    0.9,
                ],
                'harsh': [
                    0.75,
                ],
            },
        )


@pytest.mark.unit
@pytest.mark.calculation
def test_check_overstress_string_input():
    """check_overstress() should raise an TypeError if a limit or stress is passed as string."""
    with pytest.raises(TypeError):
        _overstress = Derating.check_overstress(
            0.625, {
                'mild': [0.0, '0.9'],
                'harsh': [0.0, 0.75],
            },
        )

    with pytest.raises(TypeError):
        _overstress = Derating.check_overstress(
            '0.625', {
                'mild': [0.0, 0.9],
                'harsh': [0.0, 0.75],
            },
        )


@pytest.mark.unit
@pytest.mark.calculation
def test_check_overstress_more_than_two_environs():
    """check_overstress() should work with any number of environments passed."""
    _overstress = Derating.check_overstress(
        0.625, {
            'mild': [0.0, 0.9],
            'harsh': [0.0, 0.75],
            'protected': [0.5, 0.8],
            'daddy_doyle': [0.25, 0.75],
        },
    )

    assert _overstress['mild'] == [False, False]
    assert _overstress['harsh'] == [False, False]
    assert _overstress['protected'] == [False, False]
    assert _overstress['daddy_doyle'] == [False, False]
