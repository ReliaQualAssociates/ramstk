# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Reliability Calculations Module."""

# Standard Library Imports
from math import exp
from typing import Dict, List, Tuple, Union

# RAMSTK Package Imports
from ramstk.constants.resistor import (
    PART_COUNT_LAMBDA_B,
    PART_COUNT_PI_Q,
    PART_STRESS_PI_Q,
    PI_C,
    PI_E,
    PI_R,
    PI_V,
    REF_TEMPS,
    REF_TEMPS_FILM,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a resistor.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.

    :param attributes: the hardware attributes dict for the resistor being calculated.
    :return: the hardware attributes dict with updated values.
    :rtype: dict
    :raises: KeyError when the attribute dict is missing one or more keys.
    """
    try:
        attributes["piR"] = get_resistance_factor(
            attributes["subcategory_id"],
            attributes["specification_id"],
            attributes["family_id"],
            attributes["resistance"],
        )
        attributes["temperature_case"], attributes["piT"] = (
            calculate_temperature_factor(
                attributes["temperature_active"],
                attributes["power_ratio"],
            )
        )

        # Calculate the voltage factor and taps factor (piTAPS).
        if attributes["subcategory_id"] in [9, 10, 11, 12, 13, 14, 15]:
            attributes["piV"] = get_voltage_factor(
                attributes["subcategory_id"],
                attributes["voltage_ratio"],
            )
            attributes["piTAPS"] = (attributes["n_elements"] ** 1.5 / 25.0) + 0.792

        # Determine the construction class factor (piC).
        if attributes["subcategory_id"] in [10, 12]:
            attributes["piC"] = PI_C[attributes["subcategory_id"]][
                attributes["construction_id"] - 1
            ]

        if attributes["subcategory_id"] == 4:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piT"]
                * attributes["n_elements"]
            )
        elif attributes["subcategory_id"] in [9, 11, 13, 14, 15]:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piTAPS"]
                * attributes["piR"]
                * attributes["piV"]
            )
        elif attributes["subcategory_id"] in [10, 12]:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piTAPS"]
                * attributes["piC"]
                * attributes["piR"]
                * attributes["piV"]
            )
        elif attributes["subcategory_id"] != 8:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piR"]
            )

        return attributes
    except KeyError as err:
        raise KeyError(
            f"calculate_part_stress: Missing required resistor attribute: {err}."
        )


# pylint: disable=too-many-locals
def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Calculate the part stress base hazard rate (lambdaB).

    This function calculates the MIL-HDBK-217FN2 base hazard rate for the parts stress
    method.

    :param attributes: the hardware attributes dict for the resistor to be calculated.
    :return: the calculated part stress base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid type ID.
    :raises: KeyError when passed an invalid specification ID or subcategory ID.
    """
    _power_ratio = attributes["power_ratio"]
    _specification_id = attributes["specification_id"]
    _subcategory_id = attributes["subcategory_id"]
    _temperature_active = attributes["temperature_active"]
    _type_id = attributes["type_id"]

    try:
        if _subcategory_id == 4:
            return 0.00006

        if _subcategory_id == 8:
            return _get_type_factor(_type_id)

        if _subcategory_id == 2:
            _factors, _ref_temp = _get_film_factors_and_temp(_specification_id)
        else:
            _factors, _ref_temp = _get_factors_and_temp(_subcategory_id)

        _f0, _f1, _f2, _f3, _f4, _f5 = _factors
        return (
            _f0
            * exp(_f1 * ((_temperature_active + 273.0) / _ref_temp)) ** _f2
            * exp(
                ((_power_ratio / _f3) * ((_temperature_active + 273.0) / 273.0)) ** _f4
            )
            ** _f5
        )
    except IndexError:
        raise IndexError(
            f"calculate_part_stress_lambda_b: Invalid resistor type ID {_type_id}."
        )
    except KeyError:
        raise KeyError(
            f"calculate_part_stress_lambda_b: Invalid resistor "
            f"specification ID {_specification_id} or subcategory_id {_subcategory_id}."
        )


def calculate_temperature_factor(
    temperature_active: float,
    power_ratio: float,
) -> Tuple[float, float]:
    """Calculate the case temperature and temperature factor (piT).

    :param temperature_active: the resistor ambient operating temperature in C.
    :param power_ratio: the resistor ratio of operating to rated power.
    :return: the calculated case temperature and the temperature factor (piT).
    :rtype: tuple
    """
    _temperature_case: float = temperature_active + 55.0 * power_ratio
    _pi_t: float = exp(-4056.0 * ((1.0 / (_temperature_case + 273.0)) - 1.0 / 298.0))

    return _temperature_case, _pi_t


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the resistor being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _environment_active_id = attributes["environment_active_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PI_E[_subcategory_id][_environment_active_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid resistor environment ID "
            f"{_environment_active_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_environment_id: Invalid resistor subcategory ID "
            f"{_subcategory_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate.  The
    dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base
    hazard rates.  Keys for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. specification id; if the resistor subcategory is specification dependent.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    |  Subcategory   |            Resistor           | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Fixed, Composition (RC, RCR)  |        9.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Fixed, Film (RL, RLR, RN,     |        9.2      |
    |                | RNC, RNN, RNR)                |                 |
    +----------------+-------------------------------+-----------------+
    |        3       | Fixed, Film, Power (RD)       |        9.3      |
    +----------------+-------------------------------+-----------------+
    |        4       | Fixed, Film, Network (RZ)     |        9.4      |
    +----------------+-------------------------------+-----------------+
    |        5       | Fixed, Wirewound (RB, RBR)    |        9.5      |
    +----------------+-------------------------------+-----------------+
    |        6       | Fixed, Wirewound, Power       |        9.6      |
    |                | (RW, RWR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |        7       | Fixed, Wirewound, Power,      |        9.7      |
    |                | Chassis Mounted (RE, RER)     |                 |
    +----------------+-------------------------------+-----------------+
    |        8       | Thermistor                    |        9.8      |
    +----------------+-------------------------------+-----------------+
    |        9       | Variable, Wirewound (RT, RTR) |        9.9      |
    +----------------+-------------------------------+-----------------+
    |       10       | Variable, Wirewound,          |       9.10      |
    |                | Precision (RR)                |                 |
    +----------------+-------------------------------+-----------------+
    |       11       | Variable, Wirewound,          |       9.11      |
    |                | Semiprecision (RA, RK)        |                 |
    +----------------+-------------------------------+-----------------+
    |       12       | Variable, Wirewound, Power    |       9.12      |
    |                | (RP)                          |                 |
    +----------------+-------------------------------+-----------------+
    |       13       | Variable, Non-Wirewound       |       9.13      |
    |                | (RJ, RJR)                     |                 |
    +----------------+-------------------------------+-----------------+
    |       14       | Variable, Composition (RV)    |       9.14      |
    +----------------+-------------------------------+-----------------+
    |       15       | Variable,Non-Wirewound,       |       9.15      |
    |                | Film and Precision (RQ, RVC)  |                 |
    +----------------+-------------------------------+-----------------+

    :param attributes: the hardware attributes dict for the resistor being calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid active environment ID.
    :raises: KeyError when passed an invalid subcategory ID or specification ID:
    """
    _environment_active_id = attributes["environment_active_id"]
    _specification_id = attributes["specification_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        if _subcategory_id in {2, 6}:
            # noinspection PyUnresolvedReferences
            return PART_COUNT_LAMBDA_B[_subcategory_id][_specification_id][
                _environment_active_id - 1
            ]
        return PART_COUNT_LAMBDA_B[_subcategory_id][_environment_active_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid resistor environment ID "
            f"{_environment_active_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid resistor specification ID "
            f"{_specification_id} or subcategory ID {_subcategory_id}."
        )


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part count quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the resistor being calculated.
    :return: the selected part count quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]

    try:
        return PART_COUNT_PI_Q[_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid resistor quality ID {_quality_id}."
        )


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part stress quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the resistor being calculated.
    :return: the selected part stress quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PART_STRESS_PI_Q[_subcategory_id][_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid resistor quality "
            f"ID {_quality_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_stress_quality_factor: Invalid resistor subcategory "
            f"ID {_subcategory_id}."
        )


def get_resistance_factor(
    subcategory_id: int,
    specification_id: int,
    family_id: int,
    resistance: float,
) -> float:
    """Retrieve the resistance factor (piR).

    :param subcategory_id: the resistor subcategory ID.
    :param specification_id: the resistor's governing specification ID.
    :param family_id: the resistor family ID.
    :param resistance: the resistor's resistance in ohms.
    :return: the selected resistance factor (piR).
    :rtype: float
    :raises: IndexError when passed an invalid family ID or specification ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _pi_r = 0.0
    _dic_breakpoints = {
        1: [1.0e5, 1.0e6, 1.0e7],
        2: [1.0e5, 1.0e6, 1.0e7],
        3: [100.0, 1.0e5, 1.0e6],
        5: [1.0e4, 1.0e5, 1.0e6],
        6: [
            [500.0, 1.0e3, 5.0e3, 7.5e3, 1.0e4, 1.5e4, 2.0e4],
            [100.0, 1.0e3, 1.0e4, 1.0e5, 1.5e5, 2.0e5],
        ],
        7: [500.0, 1.0e3, 5.0e3, 1.0e4, 2.0e4],
        9: [2.0e3, 5.0e3],
        10: [1.0e4, 2.0e4, 5.0e4, 1.0e5, 2.0e5],
        11: [2.0e3, 5.0e3],
        12: [2.0e3, 5.0e3],
        13: [5.0e4, 1.0e5, 2.0e5, 5.0e5],
        14: [5.0e4, 1.0e5, 2.0e5, 5.0e5],
        15: [1.0e4, 5.0e4, 2.0e5, 1.0e6],
    }

    try:
        if subcategory_id not in [4, 8]:
            _index = -1
            if subcategory_id == 6:
                _breaks = _dic_breakpoints[subcategory_id][specification_id - 1]
            else:
                _breaks = _dic_breakpoints[subcategory_id]

            for _index, _value in enumerate(_breaks):
                _diff = _value - resistance
                if (len(_breaks) == 1 and _diff < 0) or _diff >= 0:
                    break

            # Resistance factor (piR) dictionary of values.  The key is the
            # subcategory ID.  The index in the returned list is the resistance
            # range breakpoint (breakpoint values are in _lst_breakpoints below).
            # For subcategory ID 6 and 7, the specification ID selects the correct
            # set of lists, then the style ID selects the proper list of piR values
            # and then the resistance range breakpoint is used to select
            if subcategory_id in {6, 7}:
                # noinspection PyUnresolvedReferences
                _pi_r = PI_R[subcategory_id][specification_id - 1][family_id - 1][
                    _index + 1
                ]
            else:
                _pi_r = PI_R[subcategory_id][_index + 1]

        return _pi_r
    except IndexError:
        raise IndexError(
            f"get_resistance_factor: Invalid resistor family ID "
            f"{family_id} or specification ID {specification_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_resistance_factor: Invalid resistor subcategory ID "
            f"{subcategory_id}."
        )


def get_voltage_factor(
    subcategory_id: int,
    voltage_ratio: float,
) -> float:
    """Retrieve the voltage factor (piV).

    :param subcategory_id: the resistor subcategory ID.
    :param voltage_ratio: the resistor's ratio of voltages on each half of the
        potentiometer.
    :return: the selected voltage factor (piV).
    :rtype: float
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _index = -1
    _breaks = [0.0]
    if subcategory_id in {9, 10, 11, 12}:
        _breaks = [0.1, 0.2, 0.6, 0.7, 0.8, 0.9]
    elif subcategory_id in {13, 14, 15}:
        _breaks = [0.8, 0.9]

    for _index, _value in enumerate(_breaks):
        _diff = _value - voltage_ratio
        if (
            (len(_breaks) == 1 and _diff < 0.0)
            or (_index == 0 and _diff >= 0.0)
            or _diff >= 0
        ):
            break

    try:
        return PI_V[subcategory_id][_index]
    except KeyError:
        raise KeyError(
            f"get_voltage_factor: Invalid resistor subcategory ID {subcategory_id}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various resistor parameters.

    :param attributes: the hardware attributes dict for the resistor being calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    if attributes["power_ratio"] <= 0.0:
        attributes["power_ratio"] = 0.5

    attributes["resistance"] = _set_default_resistance(
        attributes["resistance"],
        attributes["subcategory_id"],
    )

    attributes["n_elements"] = _set_default_elements(
        attributes["n_elements"], attributes["subcategory_id"]
    )

    if attributes["subcategory_id"] == 4 and attributes["temperature_case"] <= 0.0:
        attributes["temperature_case"] = attributes["temperature_active"] + 28.0

    return attributes


def _get_factors_and_temp(subcategory_id: int) -> Tuple[List[float], float]:
    """Retrieve factors and reference temperature for non-film resistors.

    :param subcategory_id: the resistor subcategory ID.
    :return: the list of calculation factors and the reference temperature.
    :rtype: tuple
    """
    _dic_factors: Dict[int, List[float]] = {
        1: [4.5e-9, 12.0, 1.0, 0.6, 1.0, 1.0],
        3: [7.33e-3, 0.202, 2.6, 1.45, 0.89, 1.3],
        5: [0.0031, 1.0, 10.0, 1.0, 1.0, 1.5],
        6: [0.00148, 1.0, 2.0, 0.5, 1.0, 1.0],
        7: [0.00015, 2.64, 1.0, 0.466, 1.0, 1.0],
        8: [0.021, 0.065, 0.105, 0.0, 0.0, 0.0],
        9: [0.0062, 1.0, 5.0, 1.0, 1.0, 1.0],
        10: [0.0735, 1.03, 4.45, 2.74, 3.51, 1.0],
        11: [0.0398, 0.514, 5.28, 1.44, 4.46, 1.0],
        12: [0.0481, 0.334, 4.66, 1.47, 2.83, 1.0],
        13: [0.019, 0.445, 7.3, 2.69, 2.46, 1.0],
        14: [0.0246, 0.459, 9.3, 2.32, 5.3, 1.0],
        15: [0.018, 1.0, 7.4, 2.55, 3.6, 1.0],
    }

    ref_temp = REF_TEMPS[subcategory_id]
    return _dic_factors[subcategory_id], ref_temp


def _get_film_factors_and_temp(specification_id: int) -> Tuple[List[float], float]:
    """Retrieve factors and reference temperature for film resistors.

    :param specification_id: the resistor specification ID.
    :return: the list of calculation factors and the reference temperature.
    :rtype: tuple
    """
    _dic_factors_film: Dict[int, List[float]] = {
        1: [3.25e-4, 1.0, 3.0, 1.0, 1.0, 1.0],
        2: [3.25e-4, 1.0, 3.0, 1.0, 1.0, 1.0],
        3: [5.0e-5, 3.5, 1.0, 1.0, 1.0, 1.0],
        4: [5.0e-5, 3.5, 1.0, 1.0, 1.0, 1.0],
    }
    ref_temp = REF_TEMPS_FILM[specification_id]
    return _dic_factors_film[specification_id], ref_temp


def _get_type_factor(type_id: int) -> float:
    """Retrieve the type factor for subcategory 8.

    :param type_id: the resistor type ID.
    :return: the selected type factor.
    :rtype: float
    """
    return [0.021, 0.065, 0.105][type_id - 1]


def _set_default_resistance(resistance: float, subcategory_id: int) -> float:
    """Set the default resistance.

    :param resistance: the resistor's resistance.
    :param subcategory_id: the resistor subcategory ID.
    :return: the default resistance.
    :rtype: float
    """
    if resistance > 0.0:
        return resistance
    return {
        1: 1000000.0,
        2: 1000000.0,
        3: 100.0,
        4: 1000.0,
        5: 100000.0,
        6: 5000.0,
        7: 5000.0,
        8: 1000.0,
        9: 5000.0,
        10: 50000.0,
        11: 5000.0,
        12: 5000.0,
        13: 200000.0,
        14: 200000.0,
        15: 200000.0,
    }[subcategory_id]


def _set_default_elements(n_elements: int, subcategory_id: int) -> float:
    """Set the default number of elements.

    :param n_elements: the resistor number of elements.
    :param subcategory_id: the resistor subcategory ID.
    :return: the default number of elements.
    :rtype: int
    """
    if n_elements > 0:
        return n_elements
    return {
        1: 0,
        2: 0,
        3: 0,
        4: 10,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 3,
        10: 3,
        11: 3,
        12: 3,
        13: 3,
        14: 3,
        15: 3,
    }[subcategory_id]
