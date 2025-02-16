# type: ignore
# pylint: disable=invalid-name
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.semiconductor.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from math import exp, log, sqrt
from typing import Dict, List, Union

# RAMSTK Package Imports
from ramstk.constants.semiconductor import (
    CASE_TEMPERATURE,
    PART_COUNT_LAMBDA_B_DICT,
    PART_COUNT_LAMBDA_B_LIST,
    PART_COUNT_PI_Q,
    PART_COUNT_PI_Q_HF_DIODE,
    PART_STRESS_PI_Q,
    PART_STRESS_PI_Q_HF_DIODE,
    PI_C,
    PI_E,
    PI_M,
    PI_T_DICT,
    PI_T_LIST,
    PI_T_SCALAR,
    THETA_JC,
)


# pylint: disable=too-many-locals
def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a semiconductor.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the hardware attributes dict with updated values.
    :rtype: dict
    :raises: IndexError when passed an invalid construction ID or matching ID.
    :raises: KeyError when the attribute dict is missing one or more keys.
    """
    _construction_id = attributes["construction_id"]
    _matching_id = attributes["matching_id"]

    try:
        attributes["temperature_junction"] = calculate_junction_temperature(
            attributes["environment_active_id"],
            attributes["package_id"],
            attributes["temperature_case"],
            attributes["theta_jc"],
            attributes["power_operating"],
        )
        attributes["piT"] = calculate_temperature_factor(
            attributes["subcategory_id"],
            attributes["type_id"],
            attributes["voltage_ratio"],
            attributes["temperature_junction"],
        )
        attributes = calculate_power_rating_factor(attributes)

        # Retrieve the construction factor (piC).
        attributes["piC"] = PI_C[_construction_id - 1]

        # Retrieve the matching network factor (piM).
        attributes["piM"] = PI_M[_matching_id - 1]

        # Calculate forward current factor (piI) and power degradation factor (piP)
        attributes["piI"] = attributes["current_operating"] ** 0.68
        attributes["piP"] = 1.0 / (2.0 * (1.0 - attributes["power_ratio"]))

        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"]
            * attributes["piT"]
            * attributes["piQ"]
            * attributes["piE"]
        )

        if attributes["subcategory_id"] == 1:
            attributes = calculate_electrical_stress_factor(attributes)
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piS"] * attributes["piC"]
            )
        elif attributes["subcategory_id"] == 2:
            attributes = calculate_application_factor(attributes)
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piA"] * attributes["piR"]
            )
        elif attributes["subcategory_id"] == 3:
            attributes = calculate_application_factor(attributes)
            attributes = calculate_electrical_stress_factor(attributes)
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piA"]
                * attributes["piR"]
                * attributes["piS"]
            )
        elif attributes["subcategory_id"] == 4:
            attributes = calculate_application_factor(attributes)
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piA"]
            )
        elif attributes["subcategory_id"] in [6, 10]:
            attributes = calculate_electrical_stress_factor(attributes)
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piR"] * attributes["piS"]
            )
        elif attributes["subcategory_id"] in [7, 8]:
            attributes = calculate_application_factor(attributes)
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piA"] * attributes["piM"]
            )
        elif attributes["subcategory_id"] == 13:
            attributes = calculate_application_factor(attributes)
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piI"]
                * attributes["piA"]
                * attributes["piP"]
            )

        return attributes
    except IndexError as exc:
        raise IndexError(
            f"calculate_part_stress: Invalid semiconductor construction "
            f"ID {_construction_id} or matching ID {_matching_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"calculate_part_stress: Missing required semiconductor attribute: {exc}."
        ) from exc


def calculate_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the application factor (piA).

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    :raises: IndexError when passed an invalid application ID.
    :raises: ValueError when passed a duty cycle less than 0.0.
    """
    _application_id = attributes["application_id"]
    _duty_cycle = attributes["duty_cycle"]
    _power_rated = attributes["power_rated"]
    _subcategory_id = attributes["subcategory_id"]
    _functions = {
        2: _get_section_6_2_application_factor,
        3: _get_section_6_3_application_factor,
        4: _get_section_6_4_application_factor,
        7: _get_section_6_7_application_factor,
        8: _get_section_6_8_application_factor,
        13: _get_section_6_13_application_factor,
    }

    try:
        return _functions[_subcategory_id](attributes)
    except IndexError as exc:
        raise IndexError(
            f"calculate_application_factor: Invalid semiconductor "
            f"application ID {_application_id}."
        ) from exc
    except ValueError as exc:
        raise ValueError(
            f"calculate_application_factor: Semiconductor duty cycle {_duty_cycle} "
            f"must be a value greater than or equal to 0.0."
        ) from exc


def calculate_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the electrical stress factor (piS).

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    :raises: KeyError when passed an invalid subcategory ID or type ID.
    """
    _subcategory_id = attributes["subcategory_id"]
    _type_id = attributes["type_id"]

    _functions = {
        1: _get_section_6_1_electrical_stress_factor,
        3: _get_section_6_3_electrical_stress_factor,
        6: _get_section_6_6_electrical_stress_factor,
        10: _get_section_6_10_electrical_stress_factor,
    }

    try:
        return _functions[_subcategory_id](attributes)
    except KeyError as exc:
        raise KeyError(
            f"calculate_electrical_stress_factor: Invalid "
            f"semiconductor subcategory ID {_subcategory_id} or type ID "
            f"{_type_id}."
        ) from exc


def calculate_junction_temperature(
    environment_active_id: int,
    package_id: int,
    temperature_case: float,
    theta_jc: float,
    power_operating: float,
) -> float:
    """Calculate the junction temperature.

    .. note:: This function will also estimate the case temperature if it is
        passed in at less than or equal to zero.

    .. note:: This function will also estimate the junction-case thermal
        resistance (thetaJC) if it is passed in at less than or equal to zero.

    :param environment_active_id: the semiconductor environment ID.
    :param package_id: the semiconductor package ID.
    :param temperature_case: the semiconductor case temperature.
    :param theta_jc: the semiconductor junction-case thermal resistance.
    :param power_operating: the semiconductor operating power.
    :return: the calculated junction temperature.
    :rtype: float
    :raises: IndexError when passed an invalid active environment ID when the case
        temperature is passed at <=0.0 or an invalid package ID when the
        junction-case thermal resistance is passed at <=0.0.
    """
    try:
        if temperature_case <= 0.0:
            temperature_case = CASE_TEMPERATURE[environment_active_id - 1]

        if theta_jc <= 0.0:
            theta_jc = THETA_JC[package_id - 1]

        return temperature_case + theta_jc * power_operating
    except IndexError as exc:
        raise IndexError(
            f"calculate_junction_temperature: Invalid semiconductor "
            f"environment ID {environment_active_id} or package ID "
            f"{package_id}."
        ) from exc


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part stress base hazard rate (lambdaB).

    This function calculates the MIL-HDBK-217FN2 base hazard rate for the parts stress
    method.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the calculated part stress base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid type ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _application_id = attributes["application_id"]
    _frequency_operating = attributes["frequency_operating"]
    _n_elements = attributes["n_elements"]
    _power_operating = attributes["power_operating"]
    _subcategory_id = attributes["subcategory_id"]
    _type_id = attributes["type_id"]

    # noinspection SpellCheckingInspection
    _dic_lambdab_scalar: Dict[int, float] = {
        3: 0.00074,
        5: 0.0083,
        6: 0.18,
        10: 0.0022,
    }
    # noinspection SpellCheckingInspection
    _dic_lambdab_list: Dict[int, List[float]] = {
        1: [0.0038, 0.0010, 0.069, 0.003, 0.005, 0.0013, 0.0034, 0.002],
        2: [0.22, 0.18, 0.0023, 0.0081, 0.027, 0.0025, 0.0025],
        4: [0.012, 0.0045],
        9: [0.06, 0.023],
        11: [
            0.0055,
            0.004,
            0.0025,
            0.013,
            0.013,
            0.0064,
            0.0033,
            0.017,
            0.017,
            0.0086,
            0.0013,
            0.00023,
        ],
        13: [3.23, 5.65],
    }

    try:
        if _subcategory_id in {3, 5, 6, 10}:
            _lambda_b = _dic_lambdab_scalar[_subcategory_id]
        elif _subcategory_id == 7:
            _lambda_b = 0.032 * exp(
                0.354 * _frequency_operating + 0.00558 * _power_operating
            )
        elif _subcategory_id == 8:
            if 1.0 < _frequency_operating <= 10.0 and _power_operating < 0.1:
                _lambda_b = 0.052
            else:
                _lambda_b = 0.0093 * exp(
                    0.429 * _frequency_operating + 0.486 * _power_operating
                )
        elif _subcategory_id == 12:
            if _application_id in {1, 3}:
                _lambda_b = 0.00043 * _n_elements + 0.000043
            else:
                _lambda_b = 0.00043 * _n_elements
        else:
            _lambda_b = _dic_lambdab_list[_subcategory_id][_type_id - 1]

        return _lambda_b
    except IndexError as exc:
        raise IndexError(
            f"calculate_part_stress_lambda_b: Invalid semiconductor type ID {_type_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"calculate_part_stress_lambda_b: Invalid semiconductor "
            f"subcategory ID {_subcategory_id}."
        ) from exc


def calculate_power_rating_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the power rating factor (piR).

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    :raises: TypeError when passed a string for the rated power or rated current.
    :raises: ValueError when passed a rated power <=0.0.
    """
    _rated_current = attributes["current_rated"]
    _rated_power = attributes["power_rated"]
    try:
        if attributes["subcategory_id"] == 2:
            attributes = _get_section_6_2_power_rating_factor(attributes)
        elif attributes["subcategory_id"] == 3:
            attributes = _get_section_6_3_power_rating_factor(attributes)
        elif attributes["subcategory_id"] == 6:
            attributes = _get_section_6_6_power_rating_factor(attributes)
        elif attributes["subcategory_id"] == 10:
            attributes["piR"] = attributes["current_rated"] ** 0.4
        else:
            attributes["piR"] = 0.0

        return attributes
    except TypeError as exc:
        raise TypeError(
            f"calculate_power_rating_factor: Semiconductor rated power "
            f"{type(_rated_power)} and rated current "
            f"{type(_rated_current)} must be numerical types."
        ) from exc
    except ValueError as exc:
        raise ValueError(
            f"calculate_power_rating_factor: Semiconductor rated power "
            f"{_rated_power} must be a value greater than 0.0."
        ) from exc


def calculate_temperature_factor(
    subcategory_id: int,
    type_id: int,
    voltage_ratio: float,
    temperature_junction: float,
) -> float:
    """Calculate the temperature factor (piT).

    :param subcategory_id: the semiconductor subcategory ID.
    :param type_id: the semiconductor type ID.
    :param voltage_ratio: the semiconductor ratio of operating to rated voltage.
    :param temperature_junction: the semiconductor junction temperature.
    :return: the calculated temperature factor (piT).
    :rtype: float
    :raises: IndexError when passed an invalid type ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    try:
        if subcategory_id in {1, 2}:
            _factors = PI_T_LIST[subcategory_id][type_id - 1]
        elif subcategory_id == 7:
            _factors = PI_T_DICT[type_id]
        else:
            _factors = PI_T_SCALAR[subcategory_id]

        if subcategory_id != 7:
            return exp(-_factors * (1.0 / (temperature_junction + 273.0) - 1.0 / 298.0))

        _f0, _f1, _f2 = _factors
        return (
            _f1 * exp(-_f0 * (1.0 / (temperature_junction + 273.0) - 1.0 / 298.0))
            if voltage_ratio <= 0.4
            else (
                _f2
                * (voltage_ratio - 0.35)
                * exp(-_f0 * (1.0 / (temperature_junction + 273.0) - 1.0 / 298.0))
            )
        )
    except IndexError as exc:
        raise IndexError(
            f"calculate_temperature_factor: Invalid semiconductor type "
            f"ID {type_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"calculate_temperature_factor: Invalid semiconductor "
            f"subcategory ID {subcategory_id}."
        ) from exc


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _environment_active_id = attributes["environment_active_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        return PI_E[_subcategory_id][_environment_active_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_environment_factor: Invalid semiconductor environment "
            f"ID {_environment_active_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"get_environment_factor: Invalid semiconductor subcategory "
            f"ID {_subcategory_id}."
        ) from exc


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate.
    The dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base
    hazard rates.  Keys for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. type id; if the semiconductor subcategory is type dependent.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |          Semiconductor        | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Diode, Low Frequency          |        6.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Diode, High Frequency         |        6.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | Transistor, Low Frequency,    |        6.3      |
    |                | Bipolar                       |                 |
    +----------------+-------------------------------+-----------------+
    |        4       | Transistor, Low Frequency,    |        6.4      |
    |                | Si FET                        |                 |
    +----------------+-------------------------------+-----------------+
    |        5       | Transistor, Unijunction       |        6.5      |
    +----------------+-------------------------------+-----------------+
    |        6       | Transistor, High Frequency,   |        6.6      |
    |                | Low Noise,Bipolar             |                 |
    +----------------+-------------------------------+-----------------+
    |        7       | Transistor, High Frequency,   |        6.7      |
    |                | High Power, Bipolar           |                 |
    +----------------+-------------------------------+-----------------+
    |        8       | Transistor, High Frequency,   |        6.8      |
    |                | GaAs FET                      |                 |
    +----------------+-------------------------------+-----------------+
    |        9       | Transistor, High Frequency,   |        6.9      |
    |                | Si FET                        |                 |
    +----------------+-------------------------------+-----------------+
    |       10       | Thyristor/SCR                 |       6.10      |
    +----------------+-------------------------------+-----------------+
    |       11       | Optoelectronic, Detector,     |       6.11      |
    |                | Isolator, Emitter             |                 |
    +----------------+-------------------------------+-----------------+
    |       12       | Optoelectronic, Alphanumeric  |       6.12      |
    |                | Display                       |                 |
    +----------------+-------------------------------+-----------------+
    |       13       | Optoelectronic, Laser Diode   |       6.13      |
    +----------------+-------------------------------+-----------------+

    :param attributes: the hardware attributes dict for the semiconductor being
    calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raise: IndexError when passed an invalid active environment ID.
    :raise: KeyError when passed an invalid subcategory ID or type ID.
    """
    _environment_active_id = attributes["environment_active_id"]
    _subcategory_id = attributes["subcategory_id"]
    _type_id = attributes["type_id"]

    try:
        if _subcategory_id in {1, 2, 3, 8, 11, 13}:
            return PART_COUNT_LAMBDA_B_DICT[_subcategory_id][_type_id][
                _environment_active_id - 1
            ]
        return PART_COUNT_LAMBDA_B_LIST[_subcategory_id][_environment_active_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid semiconductor environment "
            f"ID {_environment_active_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid semiconductor subcategory "
            f"ID {_subcategory_id} or type ID {_type_id}."
        ) from exc


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part count quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the selected part count quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _quality_id = attributes["quality_id"]
    _type_id = attributes["type_id"]
    _subcategory_id = attributes["subcategory_id"]

    try:
        if _subcategory_id == 2 and _type_id == 5:
            return PART_COUNT_PI_Q_HF_DIODE[1][_quality_id - 1]
        elif _subcategory_id == 2:
            return PART_COUNT_PI_Q_HF_DIODE[0][_quality_id - 1]
        return PART_COUNT_PI_Q[_subcategory_id][_quality_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_part_count_quality factor: Invalid semiconductor "
            f"quality ID {_quality_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"get_part_count_quality_factor: Invalid semiconductor "
            f"subcategory ID {_subcategory_id}."
        ) from exc


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part stress quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the selected part stress quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    :raises: KeyError when passed an invalid subcategory ID or type ID.
    """
    _quality_id = attributes["quality_id"]
    _subcategory_id = attributes["subcategory_id"]
    _type_id = attributes["type_id"]

    try:
        if _subcategory_id == 2:
            return PART_STRESS_PI_Q_HF_DIODE[_type_id][_quality_id - 1]
        return PART_STRESS_PI_Q[_subcategory_id][_quality_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid semiconductor "
            f"quality ID {_quality_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"get_part_stress_quality_factor: Invalid semiconductor "
            f"subcategory ID {_subcategory_id} or type ID {_type_id}."
        ) from exc


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various semiconductor parameters.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    if attributes["subcategory_id"] in {4, 9} and attributes["type_id"] <= 0:
        attributes["type_id"] = 1

    if attributes["subcategory_id"] == 1 and attributes["construction_id"] <= 0:
        attributes["construction_id"] = 1

    attributes["application_id"] = _set_default_application_id(
        attributes["application_id"],
        attributes["subcategory_id"],
        attributes["type_id"],
    )

    attributes["power_rated"] = _set_default_rated_power(
        attributes["power_rated"],
        attributes["subcategory_id"],
        attributes["type_id"],
    )

    attributes["voltage_ratio"] = _set_default_voltage_ratio(
        attributes["voltage_ratio"],
        attributes["subcategory_id"],
        attributes["type_id"],
    )

    return attributes


def _get_section_6_1_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piS and set default values for low frequency diodes.

    This function is for MIL-HDBK-217F, Section 6.2 devices.  The voltage stress ratio
    default value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    if attributes["type_id"] < 5:
        attributes["voltage_ratio"] = attributes["voltage_ratio"] or 0.7
        if attributes["voltage_ratio"] <= 0.3:
            attributes["piS"] = 0.054
        else:
            attributes["piS"] = attributes["voltage_ratio"] ** 2.43
    else:
        attributes["piS"] = 1.0

    return attributes


def _get_section_6_2_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piA and set default values for high frequency diodes.

    This function is for MIL-HDBK-217F, Section 6.2 devices.  The application ID default
    value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["application_id"] = attributes["application_id"] or 2

    if attributes["type_id"] != 6:
        attributes["application_id"] = attributes["application_id"] or 3

    attributes["piA"] = [
        0.5,
        2.5,
        1.0,
    ][attributes["application_id"] - 1]

    return attributes


def _get_section_6_2_power_rating_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piR and set default values for high frequency diodes.

    This function is for MIL-HDBK-217F, Section 6.3 devices.  The rated power default
    value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    if attributes["type_id"] == 4:
        attributes["power_rated"] = attributes["power_rated"] or 1000.0
        attributes["piR"] = 0.326 * log(attributes["power_rated"]) - 0.25
    else:
        attributes["piR"] = 1.0

    return attributes


def _get_section_6_3_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piA and set default values for low frequency, low power BJT transistors.

    This function is for MIL-HDBK-217F, Section 6.3 devices.  The application ID default
    value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["application_id"] = (
        attributes["application_id"]
        or {
            0: 0,
            1: 2,
            2: 1,
        }[attributes["type_id"]]
    )

    attributes["piA"] = [
        1.5,
        0.7,
    ][attributes["application_id"] - 1]

    return attributes


def _get_section_6_3_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piS and set default values for low frequency, low power BJT transistors.

    This function is for MIL-HDBK-217F, Section 6.3 devices.  The voltage stress ratio
    default value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["voltage_ratio"] = (
        attributes["voltage_ratio"]
        or {
            0: 0.0,
            1: 0.5,
            2: 0.8,
        }[attributes["type_id"]]
    )

    attributes["piS"] = 0.045 * exp(3.1 * attributes["voltage_ratio"])

    return attributes


def _get_section_6_3_power_rating_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piR and set default values for low frequency, low power BJT transistors.

    This function is for MIL-HDBK-217F, Section 6.3 devices.  The rated power default
    value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["power_rated"] = (
        attributes["power_rated"]
        or {
            0: 0.0,
            1: 0.5,
            2: 100.0,
        }[attributes["type_id"]]
    )

    if attributes["power_rated"] < 0.1:
        attributes["piR"] = 0.43
    else:
        attributes["piR"] = attributes["power_rated"] ** 0.37

    return attributes


def _get_section_6_4_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piA and set default values for low frequency silicon FET transistors.

    This function is for MIL-HDBK-217F, Section 6.4 devices.  The application ID default
    value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["application_id"] = attributes["application_id"] or 2

    attributes["piA"] = [
        1.5,
        0.7,
        2.0,
        4.0,
        8.0,
        10.0,
    ][attributes["application_id"] - 1]

    return attributes


def _get_section_6_6_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piS and set default values for high frequency, low noise BJT transistors.

    This function is for MIL-HDBK-217F, Section 6.6 devices.  The voltage stress ratio
    default value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["voltage_ratio"] = attributes["voltage_ratio"] or 0.7

    attributes["piS"] = 0.045 * exp(3.1 * attributes["voltage_ratio"])

    return attributes


def _get_section_6_6_power_rating_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piR and set default values for high frequency, low noise BJT transistors.

    This function is for MIL-HDBK-217F, Section 6.6 devices.  The rated power default
    value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["power_rated"] = attributes["power_rated"] or 0.5

    if attributes["power_rated"] < 0.1:
        attributes["piR"] = 0.43
    else:
        attributes["piR"] = attributes["power_rated"] ** 0.37

    return attributes


def _get_section_6_7_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piA and set default values for high frequency and high power BJT transistors.

    This function is for MIL-HDBK-217F, Section 6.7 devices.  The application ID and the
    duty cycle default values are also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["application_id"] = attributes["application_id"] or 2
    attributes["duty_cycle"] = attributes["duty_cycle"] or 0.2

    if attributes["application_id"] == 1:
        attributes["piA"] = 7.6
    else:
        attributes["piA"] = 0.06 * (attributes["duty_cycle"] / 100.0) + 0.4

    return attributes


def _get_section_6_8_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piA and set default values for GaAs FET transistors.

    This function is for MIL-HDBK-217F, Section 6.8 devices.  The application ID default
    value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["application_id"] = attributes["application_id"] or 1

    attributes["piA"] = [
        1.0,
        4.0,
    ][attributes["application_id"] - 1]

    return attributes


def _get_section_6_10_electrical_stress_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piS and set default values for thyristors and SCR.

    This function is for MIL-HDBK-217F, Section 6.10 devices.  The rated current and
    voltage stress ratio default value is also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["current_rated"] = attributes["current_rated"] or 1.0
    attributes["voltage_ratio"] = attributes["voltage_ratio"] or 0.7

    if attributes["voltage_ratio"] <= 0.3:
        attributes["piS"] = 0.1
    else:
        attributes["piS"] = attributes["voltage_ratio"] ** 1.9

    return attributes


def _get_section_6_13_application_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Get piA and set default values for laser diodes.

    This function is for MIL-HDBK-217F, Section 6.13 devices.  The application ID and
    the duty cycle default values are also set.

    :param attributes: the hardware attributes dict for the semiconductor being
        calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["application_id"] = attributes["application_id"] or 2
    attributes["duty_cycle"] = attributes["duty_cycle"] or 0.6

    if attributes["application_id"] == 1:
        attributes["piA"] = 4.4
    else:
        attributes["piA"] = sqrt(attributes["duty_cycle"] / 100.0)

    return attributes


def _set_default_application_id(
    application_id: int,
    subcategory_id: int,
    type_id: int,
) -> int:
    """Set the default application ID.

    :param application_id: the semiconductor application ID.
    :param subcategory_id: the semiconductor subcategory ID.
    :param type_id: the semiconductor type ID.
    :return: the default application ID.
    :rtype: int
    """
    if application_id > 0:
        return application_id

    try:
        return {
            2: {
                6: 2,
            },
            3: {
                1: 2,
                2: 1,
            },
            4: {
                1: 2,
            },
            7: {
                1: 2,
            },
            8: {
                1: 1,
                2: 2,
            },
        }[subcategory_id][type_id]
    except KeyError:
        return 0


def _set_default_rated_power(
    power_rated: float, subcategory_id: int, type_id: int
) -> float:
    """Set the default rated power.

    :param power_rated: the semiconductor rated power.
    :param subcategory_id: the semiconductor subcategory ID.
    :param type_id: the semiconductor type ID.
    :return: the default rated power.
    :rtype: float
    """
    if power_rated > 0.0:
        return power_rated

    try:
        return {
            2: {
                4: 1000.0,
            },
            3: {
                1: 0.5,
                2: 100.0,
            },
            6: {
                1: 0.5,
            },
            7: {
                1: 100.0,
            },
            8: {
                2: 1.0,
            },
        }[subcategory_id][type_id]
    except KeyError:
        return 0.0


def _set_default_voltage_ratio(
    voltage_ratio: float, subcategory_id: int, type_id: int
) -> float:
    """Set the default voltage ratio.

    :param voltage_ratio: the semiconductor voltage ratio.
    :param subcategory_id: the semiconductor subcategory ID.
    :param type_id: the semiconductor type ID.
    :return: the default voltage ratio.
    :rtype: float
    """
    if voltage_ratio > 0.0:
        return voltage_ratio

    try:
        return {
            1: {
                1: 0.7,
                2: 0.7,
                3: 0.7,
                4: 0.7,
                5: 0.7,
            },
            3: {
                1: 0.5,
                2: 0.8,
            },
            6: {
                1: 0.7,
                2: 0.45,
            },
            13: {
                1: 0.5,
                2: 0.5,
            },
        }[subcategory_id][type_id]
    except KeyError:
        return 1.0
