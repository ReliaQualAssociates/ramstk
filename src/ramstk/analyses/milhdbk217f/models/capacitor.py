# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.mil_hdbk_217f.models.capacitor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.capacitor import (
    CAPACITANCE_FACTORS,
    DEFAULT_CAPACITANCE,
    LAMBDA_B_FACTORS,
    PART_COUNT_LAMBDA_B,
    PART_COUNT_PI_Q,
    PART_STRESS_PI_Q,
    PI_C,
    PI_CF,
    PI_E,
    REF_TEMPS,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a capacitor.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.

    :param attributes: the hardware attributes dict for the capacitor being calculated.
    :return: the hardware attributes dict with updated values.
    :rtype: dict
    :raises: KeyError when the hardware attributes dict is missing one or more keys.
    """
    try:
        attributes["piCV"] = calculate_capacitance_factor(
            attributes["subcategory_id"], attributes["capacitance"]
        )

        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"] * attributes["piCV"]
        )
        if attributes["subcategory_id"] == 12:
            attributes["piSR"] = calculate_series_resistance_factor(
                attributes["resistance"],
                attributes["voltage_dc_operating"],
                attributes["voltage_ac_operating"],
            )
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piSR"]
            )
        elif attributes["subcategory_id"] == 13:
            attributes["piC"] = get_construction_factor(attributes["construction_id"])
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piC"]
            )
        elif attributes["subcategory_id"] == 19:
            attributes["piCF"] = get_configuration_factor(
                attributes["configuration_id"]
            )
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piCF"]
                / attributes["piCV"]
            )

        return attributes
    except KeyError as exc:
        raise KeyError(
            f"calculate_part_stress: Missing required capacitor attribute: {exc}."
        ) from exc


def calculate_capacitance_factor(
    subcategory_id: int,
    capacitance: float,
) -> float:
    """Calculate the capacitance factor (piCV).

    :param subcategory_id: the capacitor subcategory ID.
    :param capacitance: the capacitor's capacitance value in Farads.
    :return: the calculated capacitance factor (piCV).
    :rtype: float
    :raises: KeyError when passed an invalid subcategory ID.
    """
    try:
        _f0, _f1 = CAPACITANCE_FACTORS[subcategory_id]
        return _f0 * capacitance**_f1
    except KeyError as exc:
        raise KeyError(
            f"calculate_capacitance_factor: Invalid capacitor subcategory "
            f"ID: {subcategory_id}."
        ) from exc


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Calculate the part stress base hazard rate (lambdaB).

    This function calculates the MIL-HDBK-217FN2 base hazard rate for the parts stress
    method.

    :param attributes: the hardware attributes dict for the capacitor being calculated.
    :return: the calculated part stress base hazard rate (lambdaB).
    :rtype: float
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _subcategory_id = attributes["subcategory_id"]
    _temperature_active = attributes["temperature_active"]
    _temperature_rated_max = attributes["temperature_rated_max"]
    _voltage_ratio = attributes["voltage_ratio"]

    try:
        _ref_temp = REF_TEMPS.get(_temperature_rated_max, min(REF_TEMPS.values()))
        _f0, _f1, _f2, _f3, _f4 = LAMBDA_B_FACTORS[_subcategory_id]
        return (
            _f0
            * ((_voltage_ratio / _f1) ** _f2 + 1.0)
            * exp(_f3 * ((_temperature_active + 273.0) / _ref_temp) ** _f4)
        )
    except KeyError as exc:
        raise KeyError(
            f"calculate_part_stress_lambda_b: Invalid capacitor subcategory "
            f"ID  {_subcategory_id}."
        ) from exc


def calculate_series_resistance_factor(
    resistance: float,
    voltage_dc_operating: float,
    voltage_ac_operating: float,
) -> float:
    """Calculate the series resistance factor (piSR).

    :param resistance: the capacitor's equivalent series resistance.
    :param voltage_dc_operating: the capacitor operating DC voltage.
    :param voltage_ac_operating: the capacitor operating ac voltage (ripple voltage).
    :return: the calculated series resistance factor (piSR).
    :rtype: tuple
    :raises: TypeError when passed a non-numerical input.
    :raises: ZeroDivisionError when passed both ac and DC voltages = 0.0.
    """
    if not all(
        isinstance(x, (int, float)) and x >= 0
        for x in [resistance, voltage_dc_operating, voltage_ac_operating]
    ):
        raise TypeError(
            f"calculate_series_resistance_factor: Capacitor resistance "
            f"({resistance}) and voltage ({voltage_ac_operating}, "
            f"{voltage_dc_operating}) values must be non-negative numbers."
        )

    if voltage_dc_operating == 0 and voltage_ac_operating == 0:
        raise ZeroDivisionError(
            "calculate_series_resistance_factor: Capacitor ac voltage and DC voltage "
            "cannot both be zero."
        )

    _thresholds = [(0.1, 0.33), (0.2, 0.27), (0.4, 0.20), (0.6, 0.13), (0.8, 0.10)]
    _ckt_resistance = resistance / (voltage_dc_operating + voltage_ac_operating)

    return next(
        (
            _factor
            for _threshold, _factor in _thresholds
            if _ckt_resistance <= _threshold
        ),
        0.066,
    )


def get_configuration_factor(
    configuration_id: int,
) -> float:
    """Retrieve the configuration factor (piCF) for the passed construction ID.

    :param configuration_id: the capacitor configuration ID.
    :return: the selected configuration factor (piCF).
    :rtype: float
    :raises: KeyError when passed an invalid configuration ID.
    """
    try:
        return PI_CF[configuration_id]
    except KeyError as exc:
        raise KeyError(
            f"get_configuration_factor: Invalid capacitor configuration "
            f"ID {configuration_id}."
        ) from exc


def get_construction_factor(
    construction_id: int,
) -> float:
    """Retrieve the configuration factor (piC) for the passed construction ID.

    :param construction_id: the capacitor construction ID.
    :return: the selected construction factor (piC).
    :rtype: float
    :raises: KeyError when passed an invalid construction ID.
    """
    try:
        return PI_C[construction_id]
    except KeyError as exc:
        raise KeyError(
            f"get_construction_factor: Invalid capacitor construction ID "
            f"{construction_id}."
        ) from exc


def get_environment_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the capacitor being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PI_E[_environment_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_environment_factor: Invalid capacitor environment "
            f"ID {_environment_id}."
        ) from exc


def get_part_count_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate.  The
    dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base
    hazard rates.  Keys for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. specification id; if the capacitor subcategory is specification dependent.

    Subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory ID |         Capacitor Style       | MIL-HDBK-217F   |
    |                |                               | Section         |
    +================+===============================+=================+
    |        1       | Fixed, Paper, Bypass (CA, CP) |       10.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Fixed, Feed-Through (CZ, CZR) |       10.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | Fixed, Paper and Plastic      |       10.3      |
    |                | Film (CPV, CQ, CQR)           |                 |
    +----------------+-------------------------------+-----------------+
    |        4       | Fixed, Metallized Paper,      |       10.4      |
    |                | Paper-Plastic and Plastic     |                 |
    |                | (CH, CHR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |        5       | Fixed, Plastic and            |       10.5      |
    |                | Metallized Plastic (CFR)      |                 |
    +----------------+-------------------------------+-----------------+
    |        6       | Fixed, Super-Metallized       |       10.6      |
    |                | Plastic (CRH)                 |                 |
    +----------------+-------------------------------+-----------------+
    |        7       | Fixed, Mica (CM, CMR)         |       10.7      |
    +----------------+-------------------------------+-----------------+
    |        8       | Fixed, Mica, Button (CB)      |       10.8      |
    +----------------+-------------------------------+-----------------+
    |        9       | Fixed, Glass (CY, CYR)        |       10.9      |
    +----------------+-------------------------------+-----------------+
    |       10       | Fixed, Ceramic, General       |      10.10      |
    |                | Purpose (CK, CKR)             |                 |
    +----------------+-------------------------------+-----------------+
    |       11       | Fixed, Ceramic, Temperature   |      10.11      |
    |                | Compensating and Chip         |                 |
    |                | (CC, CCR, CDR)                |                 |
    +----------------+-------------------------------+-----------------+
    |       12       | Fixed, Electrolytic,          |      10.12      |
    |                | Tantalum, Solid (CSR)         |                 |
    +----------------+-------------------------------+-----------------+
    |       13       | Fixed, Electrolytic,          |      10.13      |
    |                | Tantalum, Non-Solid (CL, CLR) |                 |
    +----------------+-------------------------------+-----------------+
    |       14       | Fixed, Electrolytic,          |      10.14      |
    |                | Aluminum (CU, CUR)            |                 |
    +----------------+-------------------------------+-----------------+
    |       15       | Fixed, Electrolytic (Dry),    |      10.15      |
    |                | Aluminum (CE)                 |                 |
    +----------------+-------------------------------+-----------------+
    |       16       | Variable, Ceramic (CV)        |      10.16      |
    +----------------+-------------------------------+-----------------+
    |       17       | Variable, Piston Type (PC)    |      10.17      |
    +----------------+-------------------------------+-----------------+
    |       18       | Variable, Air Trimmer (CT)    |      10.18      |
    +----------------+-------------------------------+-----------------+
    |       19       | Variable and Fixed, Gas or    |      10.19      |
    |                | Vacuum (CG)                   |                 |
    +----------------+-------------------------------+-----------------+

    :param attributes: the hardware attributes dict for the capacitor being calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raise: KeyError when passed an invalid subcategory ID or specification ID.
    """
    _environment_active_id: int = attributes["environment_active_id"]
    _specification_id: int = attributes["specification_id"]
    _subcategory_id: int = attributes["subcategory_id"]

    try:
        return (
            PART_COUNT_LAMBDA_B[_subcategory_id][_specification_id][
                _environment_active_id - 1
            ]
            if _subcategory_id == 1
            else PART_COUNT_LAMBDA_B[_subcategory_id][_environment_active_id - 1]
        )
    except KeyError as exc:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid capacitor subcategory "
            f"ID {_subcategory_id} or specification ID {_specification_id}."
        ) from exc


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve the part count quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the capacitor being calculated.
    :return: the selected part count quality factor (pIQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]

    try:
        return PART_COUNT_PI_Q[_quality_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid capacitor quality "
            f"ID {_quality_id}."
        ) from exc


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve the part stress quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the capacitor being calculated.
    :return: the selected part stress quality factor (piQ).
    :rtype: float
    :raises: KeyError when passed an invalid subcategory ID.
    :raises: IndexError when passed an invalid quality ID.
    """
    _subcategory_id = attributes["subcategory_id"]
    _quality_id = attributes["quality_id"]

    try:
        return PART_STRESS_PI_Q[_subcategory_id][_quality_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid capacitor quality "
            f"ID {_quality_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"get_part_stress_quality_factor: Invalid capacitor subcategory "
            f"ID {_subcategory_id}."
        ) from exc


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various capacitor parameters.

    :param attributes: the hardware attributes dict for the capacitor being calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    if attributes.get("capacitance", 0) <= 0.0:
        attributes["capacitance"] = _set_default_capacitance(
            attributes.get("subcategory_id", 1), attributes.get("style_id", 1)
        )

    if attributes.get("piCV", 0) <= 0.0:
        attributes["piCV"] = _set_default_capacitance_factor(
            attributes.get("subcategory_id", 1)
        )

    if attributes.get("temperature_rated_max", 0) <= 0.0:
        attributes["temperature_rated_max"] = _set_default_rated_temperature(
            attributes.get("subcategory_id", 1), attributes.get("style_id", 1)
        )

    if attributes.get("voltage_ratio", 0) <= 0.0:
        attributes["voltage_ratio"] = 0.5

    return attributes


def _set_default_capacitance(
    subcategory_id: int,
    style_id: int,
) -> float:
    """Set the default value for the capacitance.

    :param subcategory_id: the capacitor subcategory ID.
    :param style_id: the capacitor style ID.
    :return: the default capacitance.
    :rtype: float
    :raises: KeyError when passed an invalid subcategory ID.
    :raises: IndexError when passed an invalid style ID.
    """
    try:
        return (
            DEFAULT_CAPACITANCE.get(subcategory_id, [1.0])[style_id - 1]
            if subcategory_id == 3
            else DEFAULT_CAPACITANCE.get(subcategory_id, 1.0)
        )
    except IndexError as exc:
        raise IndexError(
            f"_set_default_capacitance: Invalid capacitor style ID {style_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"_set_default_capacitance: Invalid capacitor subcategory "
            f"ID {subcategory_id}."
        ) from exc


def _set_default_capacitance_factor(
    subcategory_id: int,
) -> float:
    """Set the default value for the capacitance factor (piCV).

    :param subcategory_id: the capacitor subcategory ID.
    :return: the default capacitance factor (piCV).
    :rtype: float
    """
    return 1.3 if subcategory_id in {14, 15} else 0.0 if subcategory_id > 15 else 1.0


def _set_default_rated_temperature(
    subcategory_id: int,
    style_id: int,
) -> float:
    """Set the default value for the rated temperature.

    :param subcategory_id: the capacitor subcategory ID.
    :param style_id: the capacitor style ID.
    :return: the default rated temperature.
    :rtype: float
    :raises: IndexError when passed an invalid style ID.
    """
    try:
        return (
            [125.0, 85.0][style_id - 1]
            if subcategory_id == 1
            else 85.0 if subcategory_id in {15, 16, 18, 19} else 125.0
        )
    except IndexError as exc:
        raise IndexError(
            f"_set_default_rated_temperature: Invalid capacitor style ID {style_id}."
        ) from exc
