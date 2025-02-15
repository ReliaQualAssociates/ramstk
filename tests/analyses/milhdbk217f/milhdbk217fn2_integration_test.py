# pylint: skip-file
# type: ignore
# -*- coding: utf-8 -*-
#
#       tests.analyses.milhdbk217f.milhdbk217f_integration_test.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test class for the milhdbk217f class."""

# Third Party Imports
import pytest
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses.milhdbk217f import milhdbk217f


@pytest.mark.integration
@pytest.mark.parametrize("hazard_rate_method_id", [1, 2, 3])
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_active_hazard_rate(
    hazard_rate_method_id,
    test_attributes,
):
    """Returns the hardware attributes dict with updated values on success."""
    test_attributes["hazard_rate_method_id"] = hazard_rate_method_id

    def on_message(attributes):
        assert isinstance(attributes, dict)
        assert (
            attributes["hazard_rate_active"]
            == {1: 0.00036, 2: 0.07457229625679276, 3: 0.0}[
                attributes["hazard_rate_method_id"]
            ]
        )
        print(
            f"\033[36m\n\tsucceed_predict_reliability topic was broadcast for "
            f"hazard rate method {hazard_rate_method_id}."
        )

    pub.subscribe(on_message, "succeed_predict_reliability")

    milhdbk217f.do_predict_active_hazard_rate(test_attributes)


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_active_hazard_rate_none_type_input(
    test_attributes,
):
    """Raises a ZeroDivisionError when passed NOne inputs for various parameters."""
    test_attributes["category_id"] = 2
    test_attributes["subcategory_id"] = 2
    test_attributes["n_elements"] = None
    test_attributes["power_operating"] = None
    test_attributes["type_id"] = 4
    test_attributes["hazard_rate_method_id"] = 2

    def on_message(error_message):
        assert error_message == (
            "Failed to predict MIL-HDBK-217F hazard rate for hardware ID 12; category "
            "ID = 2, subcategory ID = 2.  Error message was: unsupported operand "
            "type(s) for *: 'float' and 'NoneType'."
        )
        print(
            "\033[35m\n\tfail_predict_reliability topic was broadcast on None type "
            "input."
        )

    pub.subscribe(on_message, "fail_predict_reliability")

    milhdbk217f.do_predict_active_hazard_rate(test_attributes)


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_active_hazard_rate_zero_input(
    test_attributes,
):
    """Raises a ZeroDivisionError when passed 0.0 input for various components."""
    test_attributes["category_id"] = 4
    test_attributes["subcategory_id"] = 12
    test_attributes["voltage_ac_operating"] = 0.0
    test_attributes["voltage_dc_operating"] = 0.0
    test_attributes["hazard_rate_method_id"] = 2

    def on_message(error_message):
        assert error_message == (
            "Failed to predict MIL-HDBK-217F hazard rate for hardware ID 12; "
            "category ID = 4, subcategory ID = 12.  Error message was: "
            "calculate_series_resistance_factor: Capacitor ac voltage and DC voltage "
            "cannot both be zero."
        )
        print(
            "\033[35m\n\tfail_predict_reliability topic was broadcast on zero "
            "division."
        )

    pub.subscribe(on_message, "fail_predict_reliability")

    milhdbk217f.do_predict_active_hazard_rate(test_attributes)
