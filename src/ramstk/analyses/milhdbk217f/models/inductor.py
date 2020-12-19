# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Inductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductor MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Any, Dict, List

PART_COUNT_LAMBDA_B = {
    1: {
        1: [
            0.0035, 0.023, 0.049, 0.019, 0.065, 0.027, 0.037, 0.041, 0.052,
            0.11, 0.0018, 0.053, 0.16, 2.3
        ],
        2: [
            0.0071, 0.046, 0.097, 0.038, 0.13, 0.055, 0.073, 0.081, 0.10, 0.22,
            0.035, 0.11, 0.31, 4.7
        ],
        3: [
            0.023, 0.16, 0.35, 0.13, 0.45, 0.21, 0.27, 0.35, 0.45, 0.82, 0.011,
            0.37, 1.2, 16.0
        ],
        4: [
            0.028, 0.18, 0.39, 0.15, 0.52, 0.22, 0.29, 0.33, 0.42, 0.88, 0.015,
            0.42, 1.2, 19.0
        ]
    },
    2: {
        1: [
            0.0017, 0.0073, 0.023, 0.0091, 0.031, 0.011, 0.015, 0.016, 0.022,
            0.052, 0.00083, 0.25, 0.073, 1.1
        ],
        2: [
            0.0033, 0.015, 0.046, 0.018, 0.061, 0.022, 0.03, 0.033, 0.044,
            0.10, 0.0017, 0.05, 0.15, 2.2
        ]
    }
}
PART_COUNT_PI_Q = [0.25, 1.0, 10.0]
PART_STRESS_PI_Q = {
    1: {
        1: [1.5, 5.0],
        2: [3.0, 7.5],
        3: [8.0, 30.0],
        4: [12.0, 30.0]
    },
    2: [0.03, 0.1, 0.3, 1.0, 4.0, 20.0]
}
PI_E = {
    1: [
        1.0, 6.0, 12.0, 5.0, 16.0, 6.0, 8.0, 7.0, 9.0, 24.0, 0.5, 13.0, 34.0,
        610.0
    ],
    2: [
        1.0, 4.0, 12.0, 5.0, 16.0, 5.0, 7.0, 6.0, 8.0, 24.0, 0.5, 13.0, 34.0,
        610.0
    ]
}
REF_TEMPS = {
    1: {
        1: 329.0,
        2: 352.0,
        3: 364.0,
        4: 400.0,
        5: 398.0,
        6: 477.0
    },
    2: {
        1: 329.0,
        2: 352.0,
        3: 364.0,
        4: 409.0
    }
}


def calculate_hot_spot_temperature(temperature_active: float,
                                   temperature_rise: float) -> float:
    """Calculate the coil or transformer hot spot temperature.

    :return: _temperature_hot_spot; the calculate hot spot temperature.
    :rtype: float
    """
    return temperature_active + 1.1 * temperature_rise


def calculate_part_count(**attributes: Dict[str, Any]) -> float:
    """Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param attributes: the attributes for the connection being calculated.
    :return: _base_hr; the parts count base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(
        id_keys={
            'subcategory_id': attributes['subcategory_id'],
            'family_id': attributes['family_id'],
            'environment_active_id': attributes['environment_active_id']
        })


def calculate_part_stress(**attributes: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the part stress hazard rate for a inductor.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values.
    :rtype: dict
    """
    attributes['piC'] = float(attributes['construction_id'])
    attributes['piQ'] = get_part_stress_quality_factor(
        attributes['subcategory_id'], attributes['quality_id'],
        attributes['family_id'])

    _power_input = attributes['voltage_dc_operating'] * attributes[
        'current_operating']
    if (attributes['subcategory_id'] == 2
            and attributes['specification_id'] == 2):
        attributes['temperature_rise'] = get_temperature_rise_spec_sheet(
            attributes['page_number'])
    elif (attributes['power_operating'] > 0.0 and attributes['area'] > 0.0):
        attributes['temperature_rise'] = (
            calculate_temperature_rise_power_loss_surface(
                attributes['power_operating'], attributes['area']))
    elif (attributes['power_operating'] > 0.0 and attributes['weight'] > 0.0):
        attributes[
            'temperature_rise'] = calculate_temperature_rise_power_loss_weight(
                attributes['power_operating'], attributes['weight'])
    elif (_power_input > 0.0 and attributes['weight'] > 0.0):
        attributes['temperature_rise'] = (
            calculate_temperature_rise_input_power_weight(
                _power_input, attributes['weight']))
    else:
        attributes['temperature_rise'] = 0.0
    attributes['temperature_hot_spot'] = calculate_hot_spot_temperature(
        attributes['temperature_active'], attributes['temperature_rise'])
    attributes['lambda_b'] = calculate_part_stress_lambda_b(
        attributes['subcategory_id'], attributes['insulation_id'],
        attributes['temperature_hot_spot'])

    attributes['hazard_rate_active'] = (attributes['lambda_b']
                                        * attributes['piQ']
                                        * attributes['piE'])
    if attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (attributes['hazard_rate_active']
                                            * attributes['piC'])

    return attributes


def calculate_part_stress_lambda_b(subcategory_id: int, insulation_id: int,
                                   temperature_hot_spot: float) -> float:
    """Calculate part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param attributes: the attributes for the connection being calculated.
    :return: _lambda_b; the calculate parts stress lambda_b.
    :rtype: float
    :raise: KeyError when passed an unknown subcategory ID or insulation ID.
    """
    _dic_factors = {
        1: {
            1: [0.0018, 15.6],
            2: [0.002, 14.0],
            3: [0.0018, 8.7],
            4: [0.002, 10.0],
            5: [0.00125, 3.8],
            6: [0.00159, 8.4]
        },
        2: {
            1: [0.000335, 15.6],
            2: [0.000379, 14.0],
            3: [0.000319, 8.7],
            4: [0.00035, 10.0]
        }
    }

    _ref_temp = REF_TEMPS[subcategory_id][insulation_id]
    _f0 = _dic_factors[subcategory_id][insulation_id][0]
    _f1 = _dic_factors[subcategory_id][insulation_id][1]
    _lambda_b = _f0 * exp(((temperature_hot_spot + 273.0) / _ref_temp)**_f1)

    return _lambda_b


def calculate_temperature_rise_input_power_weight(power_input: float,
                                                  weight: float) -> float:
    """Calculate the temperature rise based on input power and xfmr weight.

    .. attention:: input power must be calculated by the calling function from
    voltage and current as it is not an attribute of an inductive device.

    :param power_input: the input power in W.
    :param weight: the weight of the xfmr in lbf.
    :retur: _temperature_rise; the calculated temperature rise in C.
    :rtype: float
    :raise: ZeroDivisionError if passed an weight=0.0.
    """
    return 2.1 * (power_input / weight**0.6766)


def calculate_temperature_rise_power_loss_surface(power_operating: float,
                                                  area: float) -> float:
    """Calculate the temperature rise based on the power loss and surface area.

    :param power_operating: the power loss in W.
    :param area: the radiating surface area of the case in sq. inches.
    :return: _temperature_rise; the calculated temperature rise in C.
    :rtype: float
    :raise: ZeroDivisionError if passed an area=0.0.
    """
    return 125.0 * power_operating / area


def calculate_temperature_rise_power_loss_weight(power_operating: float,
                                                 weight: float) -> float:
    """Calculate the temperature rise based on the power loss and xfmr weight.

    :param power_operating: the power loss in W.
    :param weight: the weight of the device in lbf.
    :return: _temperature_rise; the calculated temperature rise in C.
    :rtype: float
    :raise: ZeroDivisionError if passed an weight=0.0.
    """
    return 11.5 * (power_operating / weight**0.6766)


def get_part_count_lambda_b(id_keys: Dict[str, int]) -> List[float]:
    """Retrieve the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

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

    :param id_keys: the ID's used as keys when selecting
        the base hazard rate.  The keys are subcategory_id,
        environment_active_id, and family_id.
    :return: _base_hr; the list of part count base hazard rate.
    :rtype: list
    :raise: KeyError if passed an unknown subcategory ID or family ID.
    :raise: IndexError if passed an unknown active environment ID.
    """
    return PART_COUNT_LAMBDA_B[id_keys['subcategory_id']][
        id_keys['family_id']][id_keys['environment_active_id'] - 1]


def get_part_stress_quality_factor(subcategory_id: int, quality_id: int,
                                   family_id: int) -> float:
    """Select the MIL-HDBK-217F quality factor for the inductor device.

    :param subcategory_id: the subcategory identifier.
    :param quality_id: the quality level identifier.
    :param family_id: the device family identifier.
    :return: _pi_q; the selected quality factor
    :rtype: float
    :raise: IndexError if passed an unknown quality ID.
    :raise: KeyError if passed an unknown subcategory ID or family ID.
    """
    if subcategory_id == 1:
        _pi_q = PART_STRESS_PI_Q[subcategory_id][family_id][quality_id - 1]
    else:
        _pi_q = PART_STRESS_PI_Q[subcategory_id][quality_id - 1]

    return _pi_q


def get_temperature_rise_spec_sheet(page_number: int) -> float:
    """Retrieve the temperature rise based on the spec sheet from MIL-C-39010.

    :param page_number: the spec sheet to retrieve the temperature rise
        for.
    :return: _temperature_rise; the spec sheet temperature rise.
    :rtype: float
    :raise: KeyError if an unknown spec sheet is passed.
    """
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
        14: 15.0
    }[page_number]
