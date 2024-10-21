# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.mil_hdbk_217f.models.capacitor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.capacitor.constants import (
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


def calculate_part_count(**attributes: Dict[str, Union[float, int, str]]) -> float:
    """Wrap get_part_count_lambda_b_list function.

    This wrapper allows us to pass an attribute dict from a generic parts count
    function.

    :param attributes: the attributes for the capacitor being calculated.
    :return: _base_hr; the base hazard rate.
    :rtype: float :raise: KeyError if passed an unknown subcategory ID or specification
        ID.
    """
    return (
        get_part_count_lambda_b(
            attributes["subcategory_id"],
            attributes["environment_active_id"],
            attributes["specification_id"],
        )
        * PART_COUNT_PI_Q[attributes["quality_id"]]
    )


def calculate_part_stress(
    **attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a capacitor.

    :param attributes: the attributes for the capacitor being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary with
        updated values.
    :rtype: dict :raise: KeyError if the attribute dict is missing one or more keys.
    """
    attributes["lambda_b"] = calculate_part_stress_lambda_b(
        attributes["subcategory_id"],
        attributes["temperature_rated_max"],
        attributes["temperature_active"],
        attributes["voltage_ratio"],
    )
    attributes["piQ"] = PART_STRESS_PI_Q[attributes["subcategory_id"]][
        attributes["quality_id"]
    ]
    attributes["piE"] = PI_E[attributes["environment_id"]]
    attributes["piCV"] = calculate_capacitance_factor(
        attributes["subcategory_id"], attributes["capacitance"]
    )

    attributes["hazard_rate_active"] = (
        attributes["lambda_b"]
        * attributes["piQ"]
        * attributes["piE"]
        * attributes["piCV"]
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
        attributes["piCF"] = get_configuration_factor(attributes["configuration_id"])
        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"] * attributes["piCF"] / attributes["piCV"]
        )

    return attributes


def calculate_capacitance_factor(
    subcategory_id: int,
    capacitance: float,
) -> float:
    """Calculate the capacitance factor (piCV).

    :param subcategory_id: the capacitor subcategory identifier.
    :param capacitance: the capacitance value in Farads.
    :return: _pi_cv; the calculated capacitance factor.
    :rtype: float :raise: KeyError if passed an unknown subcategory ID.
    """
    _f0 = CAPACITANCE_FACTORS[subcategory_id][0]
    _f1 = CAPACITANCE_FACTORS[subcategory_id][1]
    return _f0 * capacitance**_f1


def calculate_part_stress_lambda_b(
    subcategory_id: int,
    temperature_rated_max: float,
    temperature_active: float,
    voltage_ratio: float,
) -> float:
    """Calculate part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    :param subcategory_id: the capacitor subcategory identifier.
    :param temperature_rated_max: the maximum rated temperature of the capacitor.
    :param temperature_active: the operating ambient temperature of the capacitor.
    :param voltage_ratio: the ratio of operating to rated voltage for the capacitor.
    :return: _base_hr; the calculates base hazard rate.
    :rtype: float :raise: KeyError if passed an unknown subcategory ID.
    """
    # This will retrieve the reference temperature for the maximum rated
    # temperature closest (round up) to one of the keys in the REF_TEMPS dict.
    _ref_temp = REF_TEMPS.get(
        temperature_rated_max,
        REF_TEMPS[min(REF_TEMPS.keys(), key=lambda k: abs(k - temperature_rated_max))],
    )
    _f0 = LAMBDA_B_FACTORS[subcategory_id][0]
    _f1 = LAMBDA_B_FACTORS[subcategory_id][1]
    _f2 = LAMBDA_B_FACTORS[subcategory_id][2]
    _f3 = LAMBDA_B_FACTORS[subcategory_id][3]
    _f4 = LAMBDA_B_FACTORS[subcategory_id][4]
    return (
        _f0
        * ((voltage_ratio / _f1) ** _f2 + 1.0)
        * exp(_f3 * ((temperature_active + 273.0) / _ref_temp) ** _f4)
    )


def calculate_series_resistance_factor(
    resistance: float,
    voltage_dc_operating: float,
    voltage_ac_operating: float,
) -> float:
    """Calculate the series resistance factor (piSR).

    :param resistance: the equivalent series resistance of the capacitor.
    :param voltage_dc_operating: the operating DC voltage.
    :param voltage_ac_operating: the operating ac voltage (ripple voltage).
    :return: _pi_sr, _error_msg; the series resistance factor and any error message
        raised by this function.
    :rtype: tuple :raise: TypeError if passed a non-numerical input. :raise:
        ZeroDivisionError if passed both ac and DC voltages = 0.0.
    """
    _thresholds = [
        (0.1, 0.33),
        (0.2, 0.27),
        (0.4, 0.20),
        (0.6, 0.13),
        (0.8, 0.10),
    ]

    _ckt_resistance = resistance / (voltage_dc_operating + voltage_ac_operating)

    return next(
        (
            _factor
            for _threshold, _factor in _thresholds
            if _ckt_resistance <= _threshold
        ),
        0.066,
    )


def get_configuration_factor(configuration_id: int) -> float:
    """Retrieve the configuration factor (piCF) for the capacitor.

    :param configuration_id: the capacitor configuration identifier.
    :return: _pi_cf; the configuration factor value.
    :rtype: float :raise: KeyError if passed an unknown configuration ID.
    """
    return PI_CF[configuration_id]


def get_construction_factor(construction_id: int) -> float:
    """Retrieve the configuration factor (piC) for the capacitor.

    :param construction_id: the capacitor construction identifier.
    :return: _pi_c; the construction factor value.
    :rtype: float :raise: KeyError if passed an unknown construction ID.
    """
    return PI_C[construction_id]


def get_part_count_lambda_b(
    subcategory_id: int,
    environment_active_id: int,
    specification_id: int = -1,
) -> float:
    """Retrieve the MIL-HDBK-217F parts count base hazard rate (lambda b).

    The dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217F parts count
    base hazard rates.  Keys are for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. specification id; if the capacitor subcategory is NOT specification
           dependent, then pass -1 for the specification ID key.

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

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param subcategory_id: the capacitor subcategory identifier.
    :param environment_active_id: the ID of the active (operating)
        environment.
    :param specification_id: the capacitor specification identifier.
        Default is -1.
    :return: _base_hr; the MIL-HDBK-217F part count base hazard rate.
    :rtype: float
    :raise: KeyError if passed an unknown subcategory ID or specification ID.
    """
    return (
        PART_COUNT_LAMBDA_B[subcategory_id][specification_id][environment_active_id - 1]
        if subcategory_id == 1
        else PART_COUNT_LAMBDA_B[subcategory_id][environment_active_id - 1]
    )


def set_default_values(
    **attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    :param attributes: the attribute dict for the capacitor being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["capacitance"] <= 0.0:
        attributes["capacitance"] = _set_default_capacitance(
            attributes["subcategory_id"],
            attributes["style_id"],
        )

    if attributes["piCV"] <= 0.0:
        attributes["piCV"] = _set_default_picv(attributes["subcategory_id"])

    if attributes["temperature_rated_max"] <= 0.0:
        attributes["temperature_rated_max"] = _set_default_rated_temperature(
            attributes["subcategory_id"],
            attributes["style_id"],
        )

    if attributes["voltage_ratio"] <= 0.0:
        attributes["voltage_ratio"] = 0.5

    return attributes


def _set_default_capacitance(
    subcategory_id: int,
    style_id: int,
) -> float:
    """Set the default value of the capacitance.

    :param subcategory_id:
    :param style_id:
    :return: _capacitance
    :rtype: float
    :raises: KeyError if passed a subcategory ID outside the bounds.
    :raises: IndexError if passed a style ID outside the bounds when subcategory ID is
        equal to three.
    """
    if subcategory_id == 3:
        return DEFAULT_CAPACITANCE[subcategory_id][style_id - 1]

    return DEFAULT_CAPACITANCE[subcategory_id]


def _set_default_picv(subcategory_id: int) -> float:
    """Set the default piCV value.

    :param subcategory_id: the subcategory ID of the capacitor with missing defaults.
    :return: _pi_cv
    :rtype: float
    """
    if subcategory_id in {14, 15}:
        return 1.3
    elif subcategory_id > 15:
        return 0.0
    return 1.0


def _set_default_rated_temperature(
    subcategory_id: int,
    style_id: int,
) -> float:
    if subcategory_id == 1:
        return [125.0, 85.0][style_id - 1]
    elif subcategory_id in {15, 16, 18, 19}:
        return 85.0
    return 125.0
