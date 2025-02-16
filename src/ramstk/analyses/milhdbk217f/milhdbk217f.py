# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.milhdbk217f.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""milhdbk217f Calculations Class."""

# Standard Library Imports
from typing import Callable, Dict, Optional, TypedDict, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Local Imports
from .models import (
    capacitor,
    connection,
    crystal,
    efilter,
    fuse,
    inductor,
    integratedcircuit,
    lamp,
    meter,
    relay,
    resistor,
    semiconductor,
    switch,
)


# noinspection PyTypeChecker
def do_predict_active_hazard_rate(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Calculate the active hazard rate for a hardware item.

    .. attention:: The programmer is responsible for ensuring appropriate
        stress analyses (e.g., voltage ratios) are performed and results
        assigned to the attribute dict prior to calling the MIL-HDBK-217F
        methods.

    .. important:: The calling object is responsible for handling any
        exceptions raised by or passed through this method.

    :param attributes: the hardware attributes dict for the component being calculated.
    :return: the calculated active hazard rate.
    :rtype: float
    """
    attributes = _set_default_values(attributes)

    try:
        if attributes["hazard_rate_method_id"] == 1:
            attributes = _do_calculate_part_count(attributes)
        elif attributes["hazard_rate_method_id"] == 2:
            attributes = _do_calculate_part_stress(attributes)

        pub.sendMessage(
            "succeed_predict_reliability",
            attributes=attributes,
        )
        pub.sendMessage(
            "request_set_all_milhdbk217f_attributes",
            attributes=attributes,
        )
        pub.sendMessage(
            "request_set_all_reliability_attributes",
            attributes=attributes,
        )
    except (TypeError, ValueError) as err:
        _do_handle_prediction_failure(
            "reliability",
            attributes,
            f"{err}.",
        )
    except ZeroDivisionError as err:
        _do_handle_prediction_failure(
            "reliability",
            attributes,
            f"{err}",
        )

    return attributes["hazard_rate_active"]


# noinspection PyTypeChecker
def _do_calculate_part_count(
    attributes: Dict[str, Union[float, int, str]],
) -> TypedDict:
    """Calculate the MIL-HDBK-217F parts count active hazard rate.

    :param attributes: the hardware attributes dict for the component being calculated.
    :return: the updated hardware attributes.
    :rtype: dict
    :raises: IndexError when there is no entry for the active environment ID.
    :raises: KeyError when there is no entry for category ID or subcategory ID.
    """
    attributes["lambda_b"] = _get_lambda_b(attributes)
    attributes["piQ"] = _get_quality_factor(attributes)

    attributes["hazard_rate_active"] = attributes["lambda_b"] * attributes["piQ"]

    return attributes


# noinspection PyTypeChecker
def _do_calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Calculate the MIL-HDBK-217F parts stress active hazard rate.

    :param attributes: the hardware attributes dict for the component being calculated.
    :return: attributes; the attribute dict with updated values.
    :rtype: dict
    :raises: IndexError if there is no entry for the active environment ID.
    :raises: KeyError if there is no entry for category ID or subcategory ID.
    """
    _part_stress = _get_function(
        {
            1: integratedcircuit.calculate_part_stress,
            2: semiconductor.calculate_part_stress,
            3: resistor.calculate_part_stress,
            4: capacitor.calculate_part_stress,
            5: inductor.calculate_part_stress,
            6: relay.calculate_part_stress,
            7: switch.calculate_part_stress,
            8: connection.calculate_part_stress,
            9: meter.calculate_part_stress,
            10: {
                1: crystal.calculate_part_stress,
                2: efilter.calculate_part_stress,
                3: fuse.calculate_part_stress,
                4: lamp.calculate_part_stress,
            },
        },
        attributes["category_id"],
        attributes["subcategory_id"],
    )

    attributes["lambda_b"] = _get_lambda_b(attributes)
    attributes["piE"] = _get_environment_factor(attributes)
    attributes["piQ"] = _get_quality_factor(attributes)
    attributes["hazard_rate_active"] = (
        attributes["lambda_b"] * attributes["piQ"] * attributes["piE"]
    )

    return _part_stress(attributes)


def _do_handle_prediction_failure(
    error_type: str,
    attributes: Dict[str, Union[float, int, str]],
    additional_info: str = "",
) -> None:
    """Handle the failure of a hazard rate prediction and publish an error message.

    :param error_type: the type of RAMSTK error message being passed.
    :param attributes: the hardware attributes dict for the component being calculated.
    :param additional_info: any additional information to append to the base error
        message.
    """
    error_message = (
        f"Failed to predict MIL-HDBK-217F hazard rate for hardware ID "
        f"{attributes['hardware_id']}; category ID = {attributes['category_id']}, "
        f"subcategory ID = {attributes['subcategory_id']}.  Error message was:"
    )
    if additional_info:
        error_message += f" {additional_info}"
    pub.sendMessage(f"fail_predict_{error_type}", error_message=error_message)


def _get_environment_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve environment factor (piE).

    :param attributes: the hardware attributes dict for the component being calculated.
    :return: the selected environment factor (piE).
    :rtype: float
    """
    _pi_e_func = _get_function(
        {
            1: integratedcircuit.get_environment_factor,
            2: semiconductor.get_environment_factor,
            3: resistor.get_environment_factor,
            4: capacitor.get_environment_factor,
            5: inductor.get_environment_factor,
            6: relay.get_environment_factor,
            7: switch.get_environment_factor,
            8: connection.get_environment_factor,
            9: meter.get_environment_factor,
            10: {
                1: crystal.get_environment_factor,
                2: efilter.get_environment_factor,
                3: fuse.get_environment_factor,
                4: lamp.get_environment_factor,
            },
        },
        attributes.get("category_id"),
        attributes.get("subcategory_id"),
    )
    return _pi_e_func(attributes)


def _get_function(
    func_dict: Dict,
    category_id: int,
    subcategory_id: Optional[int] = None,
) -> Callable:
    """Retrieve the appropriate function based on category and subcategory IDs.

    :param func_dict: the dictionary of functions to select from.
    :param category_id: the category ID of the component being calculated.
    :param subcategory_id: teh subcategory ID of the component being calculated.
    :return: the function to be used by the calling function.
    :rtype: Callable
    """
    try:
        return (
            func_dict[category_id][subcategory_id]
            if category_id == 10 and subcategory_id
            else func_dict[category_id]
        )
    except KeyError as exc:
        raise KeyError(
            f"Invalid category_id {category_id} or subcategory_id {subcategory_id}"
        ) from exc


def _get_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve base hazard rate (lambdaB) for part count or part stress calculations.

    :param attributes: the hardware attributes dict for the component being calculated.
    :return: the selected or calculated part count or part stress base hazard rate (
    lambdaB).
    rtype: fl
    """
    lambda_b_dict = {
        1: {
            1: integratedcircuit.get_part_count_lambda_b,
            2: semiconductor.get_part_count_lambda_b,
            3: resistor.get_part_count_lambda_b,
            4: capacitor.get_part_count_lambda_b,
            5: inductor.get_part_count_lambda_b,
            6: relay.get_part_count_lambda_b,
            7: switch.get_part_count_lambda_b,
            8: connection.get_part_count_lambda_b,
            9: meter.get_part_count_lambda_b,
            10: {
                1: crystal.get_part_count_lambda_b,
                2: efilter.get_part_count_lambda_b,
                3: fuse.get_part_count_lambda_b,
                4: lamp.get_part_count_lambda_b,
            },
        },
        2: {
            1: integratedcircuit.calculate_part_stress_lambda_b,
            2: semiconductor.calculate_part_stress_lambda_b,
            3: resistor.calculate_part_stress_lambda_b,
            4: capacitor.calculate_part_stress_lambda_b,
            5: inductor.calculate_part_stress_lambda_b,
            6: relay.calculate_part_stress_lambda_b,
            7: switch.calculate_part_stress_lambda_b,
            8: connection.calculate_part_stress_lambda_b,
            9: meter.get_part_stress_lambda_b,
            10: {
                1: crystal.calculate_part_stress_lambda_b,
                2: efilter.get_part_stress_lambda_b,
                3: fuse.get_part_stress_lambda_b,
                4: lamp.calculate_part_stress_lambda_b,
            },
        },
    }
    lambda_b_func = _get_function(
        lambda_b_dict[attributes["hazard_rate_method_id"]],
        attributes["category_id"],
        attributes.get("subcategory_id"),
    )
    return lambda_b_func(attributes)


def _get_quality_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve quality factor (piQ) for part count or part stress calculation.

    :param attributes: the hardware attributes dict for the component being calculated.
    :return: the selected part count or part stress quality factor (piQ).
    """
    if attributes["category_id"] == 10 and attributes["subcategory_id"] in {3, 4}:
        return 1.0

    if attributes["hazard_rate_method_id"] == 2:
        if attributes["category_id"] in {7, 8}:
            return 1.0

        if attributes["category_id"] == 9 and attributes["subcategory_id"] == 1:
            return 1.0

    _pi_q_dict = {
        1: {  # Part count method
            1: integratedcircuit.get_quality_factor,
            2: semiconductor.get_part_count_quality_factor,
            3: resistor.get_part_count_quality_factor,
            4: capacitor.get_part_count_quality_factor,
            5: inductor.get_part_count_quality_factor,
            6: relay.get_part_count_quality_factor,
            7: switch.get_part_count_quality_factor,
            8: connection.get_part_count_quality_factor,
            9: meter.get_part_count_quality_factor,
            10: {
                1: crystal.get_part_count_quality_factor,
                2: efilter.get_quality_factor,
            },
        },
        2: {  # Part stress method
            1: integratedcircuit.get_quality_factor,
            2: semiconductor.get_part_stress_quality_factor,
            3: resistor.get_part_stress_quality_factor,
            4: capacitor.get_part_stress_quality_factor,
            5: inductor.get_part_stress_quality_factor,
            6: relay.get_part_stress_quality_factor,
            7: switch.get_part_stress_quality_factor,
            8: connection.get_part_stress_quality_factor,
            9: meter.get_part_stress_quality_factor,
            10: {
                1: crystal.get_part_stress_quality_factor,
                2: efilter.get_quality_factor,
            },
        },
    }
    _pi_q_func = _get_function(
        _pi_q_dict[attributes["hazard_rate_method_id"]],
        attributes["category_id"],
        attributes.get("subcategory_id"),
    )

    return _pi_q_func(attributes)


def _set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set default values for parameters <= 0.0.

    :param attributes: the hardware attributes dict for the component being calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    _default_values = {
        1: integratedcircuit.set_default_values,
        2: semiconductor.set_default_values,
        3: resistor.set_default_values,
        4: capacitor.set_default_values,
        5: inductor.set_default_values,
        6: relay.set_default_values,
        7: switch.set_default_values,
        8: connection.set_default_values,
        9: meter.set_default_values,
        10: {
            1: crystal.set_default_values,
            2: efilter.set_default_values,
            3: fuse.set_default_values,
            4: lamp.set_default_values,
        },
    }[attributes["category_id"]]

    return _default_values(attributes)
