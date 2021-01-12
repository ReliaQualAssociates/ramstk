# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.test_criticality.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the FMEA criticality module."""

# Third Party Imports
import pytest

# RAMSTK Package Imports
from ramstk.analyses import criticality
from ramstk.exceptions import OutOfRangeError

SOD = {
    'rpn_severity': 5,
    'rpn_occurrence': 8,
    'rpn_detection': 7
}


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_rpn():
    """calculate_rpn() should return the product of the three input values on success."""
    _rpn = criticality.calculate_rpn(SOD)

    assert _rpn == 280


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_rpn_out_of_range_severity_inputs():
    """calculate_rpn() raises OutOfRangeError for 11 < severity inputs < 0."""
    SOD['rpn_severity'] = 0
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_rpn(SOD)
    assert e.value.args[0] == ("RPN severity is outside the range [1, 10].")

    SOD['rpn_severity'] = 11
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_rpn(SOD)
    assert e.value.args[0] == ("RPN severity is outside the range [1, 10].")
    SOD['rpn_severity'] = 5

    SOD['rpn_occurrence'] = 0
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_rpn(SOD)
    assert e.value.args[0] == ("RPN occurrence is outside the range [1, 10].")

    SOD['rpn_occurrence'] = 11
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_rpn(SOD)
    assert e.value.args[0] == ("RPN occurrence is outside the range [1, 10].")
    SOD['rpn_occurrence'] = 8

    SOD['rpn_detection'] = 0
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_rpn(SOD)
    assert e.value.args[0] == ("RPN detection is outside the range [1, 10].")

    SOD['rpn_detection'] = 11
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_rpn(SOD)
    assert e.value.args[0] == ("RPN detection is outside the range [1, 10].")
    SOD['rpn_detection'] = 7

@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mode_hazard_rate():
    """calculate_mode_hazard_rate() should return the product of the item hazard rate and the mode ratio on success."""
    _mode_hr = criticality.calculate_mode_hazard_rate(0.000617, 0.35)

    assert _mode_hr == 0.00021595


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mode_hazard_rate_out_of_range_mode_ratio():
    """calculate_mode_hazard_rate() should raise an OutOfRangeError if the mode ratio is outside [0.0, 1.0]."""
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_mode_hazard_rate(0.000617, -0.35)
    assert e.value.args[0] == ("calculate_mode_hazard_rate() was passed a "
                               "failure mode ratio outside the range of "
                               "[0.0, 1.0].")

    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_mode_hazard_rate(0.000617, 1.35)
    assert e.value.args[0] == ("calculate_mode_hazard_rate() was passed a "
                               "failure mode ratio outside the range of "
                               "[0.0, 1.0].")


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mode_hazard_rate_out_of_range_item_hr():
    """calculate_mode_hazard_rate() should raise an OutOfRangeError if the item hazard rate is negative."""
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_mode_hazard_rate(-0.000617, 0.35)
    assert e.value.args[0] == ("calculate_mode_hazard_rate() was passed a "
                               "negative value for the item hazard rate.")


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mode_criticality():
    """calculate_mode_criticality() should return the product of the mode hazard rate, mode operating time, and effect probability on success."""
    _mode_crit = criticality.calculate_mode_criticality(0.00021595, 5.28, 0.75)

    assert _mode_crit == 0.000855162


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mode_criticality_out_of_range_op_time():
    """calculate_mode_criticality() should raise an OutOfRangeError when passed a negative value for operating time."""
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_mode_criticality(0.00021595, -5.28, 0.75)
    assert e.value.args[0] == ('calculate_mode_criticality() was passed a '
                               'negative value for failure mode operating '
                               'time.')


@pytest.mark.unit
@pytest.mark.calculation
def test_calculate_mode_criticality_out_of_range_eff_prob():
    """calculate_mode_criticality() should raise an OutOfRangeError when passed an effect probability outside the range [0.0, 1.0]."""
    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_mode_criticality(0.00021595, 5.28, -0.75)
    assert e.value.args[0] == ('calculate_mode_criticality() was passed a '
                               'failure effect probability outside the range '
                               'of [0.0, 1.0].')


    with pytest.raises(OutOfRangeError) as e:
        criticality.calculate_mode_criticality(0.00021595, 5.28, 1.75)
    assert e.value.args[0] == ('calculate_mode_criticality() was passed a '
                               'failure effect probability outside the range '
                               'of [0.0, 1.0].')
