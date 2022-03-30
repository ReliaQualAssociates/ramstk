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
@pytest.mark.usefixtures("test_attributes")
@pytest.mark.parametrize("hazard_rate_method_id", [1, 2, 3])
def test_do_calculate_active_hazard_rate(hazard_rate_method_id, test_attributes):
    """do_calculate_active_hazard_rate() should return the component attribute dict
    with updated values on success."""
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
            f"hazard rate method {attributes['hazard_rate_method_id']}."
        )

    pub.subscribe(on_message, "succeed_predict_reliability")

    milhdbk217f.do_predict_active_hazard_rate(**test_attributes)


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_active_hazard_rate_negative_input(test_attributes):
    """do_calculate_active_hazard_rate() should raise a ZeroDivisionError when passed a
    negative input for various components."""
    test_attributes["category_id"] = 2
    test_attributes["subcategory_id"] = 2
    test_attributes["n_elements"] = None
    test_attributes["power_operating"] = None
    test_attributes["type_id"] = 4
    test_attributes["hazard_rate_method_id"] = 2

    def on_message(error_message):
        assert error_message == (
            "Failed to predict MIL-HDBK-217F hazard rate for "
            "hardware ID 12; one or more inputs has a "
            "negative or missing value. Hardware item "
            "category ID=2, subcategory ID=2, rated "
            "power=0.75, number of elements=None."
        )
        print(
            "\033[35m\n\tfail_predict_reliability topic was broadcast on negative "
            "input."
        )

    pub.subscribe(on_message, "fail_predict_reliability")

    milhdbk217f.do_predict_active_hazard_rate(**test_attributes)


@pytest.mark.integration
@pytest.mark.usefixtures("test_attributes")
def test_do_calculate_active_hazard_rate_zero_input(test_attributes):
    """do_calculate_active_hazard_rate() should raise a ZeroDivisionError when passed
    an input equal to 0.0 for various components."""
    test_attributes["category_id"] = 4
    test_attributes["subcategory_id"] = 12
    test_attributes["voltage_ac_operating"] = 0.0
    test_attributes["voltage_dc_operating"] = 0.0
    test_attributes["hazard_rate_method_id"] = 2

    def on_message(error_message):
        assert error_message == (
            "Failed to predict MIL-HDBK-217F hazard rate for hardware ID 12; one or "
            "more inputs has a value of 0.0.  Hardware item category ID=4, subcategory "
            "ID=12, operating ac voltage=0.0, operating DC voltage=0.0, operating "
            "temperature=45.0, temperature rise=10.0, rated maximum temperature=105.0, "
            "feature size=1.5, surface area=1.5, and item weight=0.5."
        )
        print(
            "\033[35m\n\tfail_predict_reliability topic was broadcast on zero "
            "division."
        )

    pub.subscribe(on_message, "fail_predict_reliability")

    milhdbk217f.do_predict_active_hazard_rate(**test_attributes)
