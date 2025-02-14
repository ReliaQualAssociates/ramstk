# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdk217f.models.inductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.inductor import (
    PART_COUNT_LAMBDA_B,
    PART_COUNT_PI_Q,
    PART_STRESS_PI_Q,
    PI_E,
    REF_TEMPS,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for an inductive device.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.

    :param attributes: the hardware attributes dict for the inductive device being
        calculated.
    :return: the hardware attributes dict with updated values.
    :rtype: dict
    :raises: KeyError when the hardware attributes dict is missing one or more keys.
    """
    try:
        attributes["piC"] = float(attributes["construction_id"])

        _power_input = (
            attributes["voltage_dc_operating"] * attributes["current_operating"]
        )
        if attributes["subcategory_id"] == 2 and attributes["specification_id"] == 2:
            attributes["temperature_rise"] = get_temperature_rise_spec_sheet(
                int(attributes["page_number"])
            )
        elif attributes["power_operating"] > 0.0 and attributes["area"] > 0.0:
            attributes["temperature_rise"] = (
                calculate_temperature_rise_power_loss_surface(
                    attributes["power_operating"], attributes["area"]
                )
            )
        elif attributes["power_operating"] > 0.0 and attributes["weight"] > 0.0:
            attributes["temperature_rise"] = (
                calculate_temperature_rise_power_loss_weight(
                    attributes["power_operating"], attributes["weight"]
                )
            )
        elif _power_input > 0.0 and attributes["weight"] > 0.0:
            attributes["temperature_rise"] = (
                calculate_temperature_rise_input_power_weight(
                    _power_input, attributes["weight"]
                )
            )
        else:
            attributes["temperature_rise"] = 0.0
        attributes["temperature_hot_spot"] = calculate_hot_spot_temperature(
            attributes["temperature_active"], attributes["temperature_rise"]
        )

        attributes["lambda_b"] = calculate_part_stress_lambda_b(attributes)

        attributes["hazard_rate_active"] = (
            attributes["lambda_b"] * attributes["piQ"] * attributes["piE"]
        )
        if attributes["subcategory_id"] == 2:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piC"]
            )

        return attributes
    except KeyError as err:
        raise KeyError(
            f"calculate_part_stress: Missing required inductive device attribute:"
            f" {err}."
        )


def calculate_hot_spot_temperature(
    temperature_active: float,
    temperature_rise: float,
) -> float:
    """Calculate the hot spot temperature.

    :param temperature_active: the inductive device's localized ambient temperature.
    :param temperature_rise: the temperature rise of the inductive device above ambient.
    :return: the calculated hot spot temperature.
    :rtype: float
    """
    return temperature_active + 1.1 * temperature_rise


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Calculate the part stress base hazard rate (lambdaB).

    This function calculates the MIL-HDBK-217FN2 base hazard rate for the parts stress
    method.

    :param attributes: the hardware attributes dict for the inductive device being
        calculated.
    :return: the calculated parts stress base hazard rate (lambdaB).
    :rtype: float
    :raises: KeyError when passed an invalid subcategory ID or insulation ID.
    """
    _insulation_id: int = attributes["insulation_id"]
    _subcategory_id: int = attributes["subcategory_id"]
    _temperature_hot_spot: float = attributes["temperature_hot_spot"]

    _dic_factors = {
        1: {
            1: [0.0018, 15.6],
            2: [0.002, 14.0],
            3: [0.0018, 8.7],
            4: [0.002, 10.0],
            5: [0.00125, 3.8],
            6: [0.00159, 8.4],
        },
        2: {
            1: [0.000335, 15.6],
            2: [0.000379, 14.0],
            3: [0.000319, 8.7],
            4: [0.00035, 10.0],
        },
    }

    try:
        _ref_temp = REF_TEMPS[_subcategory_id][_insulation_id]
        _f0 = _dic_factors[_subcategory_id][_insulation_id][0]
        _f1 = _dic_factors[_subcategory_id][_insulation_id][1]
        return _f0 * exp(((_temperature_hot_spot + 273.0) / _ref_temp) ** _f1)
    except KeyError:
        raise KeyError(
            f"calculate_part_stress_lambda_b: Invalid inductive device subcategory ID"
            f" {_subcategory_id} or insulation ID {_insulation_id}."
        )


def calculate_temperature_rise_input_power_weight(
    power_input: float,
    weight: float,
) -> float:
    """Calculate the temperature rise based on input power and xfmr weight.

    .. attention:: input power must be calculated by the calling function from
    voltage and current as it is not an attribute of an inductive device.

    :param power_input: the inductive device input power in watts.
    :param weight: the weight of the inductive device in pounds-force.
    :return: the calculated temperature rise in C.
    :rtype: float
    :raises: ZeroDivisionError when passed a weight=0.0.
    """
    try:
        return 2.1 * (power_input / weight**0.6766)
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "calculate_temperature_rise_input_power_weight: Inductive device weight "
            "must not be zero."
        )


def calculate_temperature_rise_power_loss_surface(
    power_operating: float,
    area: float,
) -> float:
    """Calculate the temperature rise based on the power loss and surface area.

    :param power_operating: the inductive device's power loss in watts.
    :param area: the inductive device's radiating surface area of the case in square
        inches.
    :return: the calculated temperature rise in C.
    :rtype: float
    :raises: ZeroDivisionError when passed an area=0.0.
    """
    try:
        return 125.0 * power_operating / area
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "calculate_temperature_rise_power_loss_surface: Inductive device area "
            "must not be zero."
        )


def calculate_temperature_rise_power_loss_weight(
    power_operating: float,
    weight: float,
) -> float:
    """Calculate the temperature rise based on the power loss and xfmr weight.

    :param power_operating: the inductive device's power loss in watts.
    :param weight: the weight of the inductive device in pounds-force.
    :return: the calculated temperature rise in C.
    :rtype: float
    :raises: ZeroDivisionError when passed a weight=0.0.
    """
    try:
        return 11.5 * (power_operating / weight**0.6766)
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "calculate_temperature_rise_power_loss_weight: Inductive device weight "
            "must not be zero."
        )


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the inductive device being
        calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _environment_id: int = attributes["environment_active_id"]
    _subcategory_id: int = attributes["subcategory_id"]

    try:
        return PI_E[_subcategory_id][_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid inductive device environment "
            f"ID {_environment_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_environment_factor: Invalid inductive device subcategory "
            f"ID {_subcategory_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate.
    The dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count
    base hazard rates.  Keys for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. family id; if the inductor subcategory is NOT family dependent, then
            the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |           Inductor            | MIL-HDBK-217F   |
    |       ID       |             Style             |    Section      |
    +================+===============================+=================+
    |        1       | Transformer                   |       11.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Coil                          |       11.2      |
    +----------------+-------------------------------+-----------------+

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param attributes: the hardware attributes dict for the inductive device being
    calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raises: KeyError when passed an invalid subcategory ID or family ID.
    :raises: IndexError when passed an invalid environment ID.
    """
    _environment_id = attributes["environment_active_id"]
    _family_id = attributes["family_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PART_COUNT_LAMBDA_B[_subcategory_id][_family_id][_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid inductive device environment "
            f"ID {_environment_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid inductive device family "
            f"ID {_family_id} or subcategory ID {_subcategory_id}."
        )


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part count quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the inductive device being
        calculated.
    :return: the selected part count quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]

    try:
        return PART_COUNT_PI_Q[_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid inductive device quality "
            f"ID {_quality_id}."
        )


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part stress quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the inductive device being
        calculated.
    :return: the selected part stress quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    :raises: KeyError when passed an invalid subcategory ID or family ID.
    """
    _family_id = attributes["family_id"]
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return (
            PART_STRESS_PI_Q[_subcategory_id][_family_id][_quality_id - 1]
            if _subcategory_id == 1
            else PART_STRESS_PI_Q[_subcategory_id][_quality_id - 1]
        )
    except IndexError:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid inductive device quality "
            f"ID {_quality_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_stress_quality_factor: Invalid inductive device "
            f"family ID {_family_id} or subcategory ID {_subcategory_id}."
        )


def get_temperature_rise_spec_sheet(page_number: int) -> float:
    """Retrieve the temperature rise.

    :param page_number: the inductive device specification sheet to retrieve the
        temperature rise for.
    :return: the selected temperature rise.
    :rtype: float
    :raises: KeyError when an invalid specification sheet is passed.
    """
    try:
        return {
            1: 15.0,
            2: 15.0,
            3: 15.0,
            4: 35.0,
            5: 15.0,
            6: 35.0,
            7: 15.0,
            8: 35.0,
            9: 15.0,
            10: 15.0,
            11: 35.0,
            12: 35.0,
            13: 15.0,
            14: 15.0,
        }[page_number]
    except KeyError:
        raise KeyError(
            f"get_temperature_rise_spec_sheet: Invalid inductive device "
            f"page number {page_number}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various inductive device parameters.

    :param attributes: the hardware attributes dict for the inductive device being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    if attributes["rated_temperature_max"] <= 0.0:
        attributes["rated_temperature_max"] = _set_default_rated_temperature(
            attributes["subcategory_id"]
        )

    if attributes["temperature_rise"] <= 0.0:
        attributes["temperature_rise"] = _set_default_temperature_rise(
            attributes["subcategory_id"],
            attributes["family_id"],
        )

    return attributes


def _set_default_rated_temperature(subcategory_id: int) -> float:
    """Set the default maximum rated temperature.

    :param subcategory_id: the inductive device subcategory ID.
    :return: the default maximum rated temperature.
    :rtype: float
    """
    return 130.0 if subcategory_id == 1 else 125.0


def _set_default_temperature_rise(
    subcategory_id: int,
    family_id: int,
) -> float:
    """Set the default inductive device temperature rise.

    :param subcategory_id: the inductive device subcategory ID.
    :param family_id: the inductive device family ID.
    :return: the default temperature rise.
    :rtype: float
    """
    return 30.0 if subcategory_id == 1 and family_id == 3 else 10.0
