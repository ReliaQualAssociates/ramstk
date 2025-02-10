# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.integratedcircuit.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit MIL-HDBK-217F Constants and Calculations Module."""

# Standard Library Imports
from math import exp, log
from typing import Dict, Tuple, Union

# RAMSTK Package Imports
from ramstk.constants.integrated_circuit import (
    ACTIVATION_ENERGY,
    C1,
    C2,
    PART_COUNT_LAMBDA_B,
    PI_A,
    PI_E,
    PI_PT,
    PI_Q,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a integrated circuit.

    This function calculates the MIL-HDBK-217F hazard rate using the part stress method.

    :param attributes: the hardware attribute dict for the integrated circuit to be
        calculated.
    :return: attributes; the hardware attribute dict with updated values..
    :rtype: dict
    """
    try:
        attributes["temperature_junction"] = calculate_junction_temperature(
            attributes["temperature_case"],
            attributes["power_operating"],
            attributes["theta_jc"],
        )
        attributes["piT"] = calculate_temperature_factor(
            attributes["subcategory_id"],
            attributes["family_id"],
            attributes["type_id"],
            attributes["temperature_junction"],
        )
        attributes["piL"] = 0.01 * exp(5.35 - 0.35 * attributes["years_in_production"])

        if attributes["subcategory_id"] in [1, 2, 3, 4]:
            attributes["C1"] = get_die_complexity_factor(
                attributes["subcategory_id"],
                attributes["technology_id"],
                attributes["application_id"],
                attributes["n_elements"],
            )
            attributes["C2"] = calculate_package_factor(
                attributes["package_id"], attributes["n_active_pins"]
            )
            attributes["hazard_rate_active"] = (
                (
                    attributes["C1"] * attributes["piT"]
                    + attributes["C2"] * attributes["piE"]
                )
                * attributes["piQ"]
                * attributes["piL"]
            )
        elif attributes["subcategory_id"] in [5, 6, 7, 8]:
            attributes["C1"] = get_die_complexity_factor(
                attributes["subcategory_id"],
                attributes["technology_id"],
                attributes["application_id"],
                attributes["n_elements"],
            )
            attributes["C2"] = calculate_package_factor(
                attributes["package_id"], attributes["n_active_pins"]
            )
            if attributes["subcategory_id"] == 6:
                attributes["piECC"] = get_error_correction_factor(attributes["type_id"])
                (_a_1, _a_2, _b_1, _b_2) = calculate_lambda_cyclic_factors(
                    attributes["n_cycles"],
                    attributes["construction_id"],
                    attributes["n_elements"],
                    attributes["temperature_junction"],
                )
                attributes["lambda_cyc"] = (
                    _a_1 * _b_1 + (_a_2 * _b_2 / attributes["piQ"])
                ) * attributes["piECC"]
            else:
                attributes["lambda_cyc"] = 0.0

            attributes["hazard_rate_active"] = (
                (
                    attributes["C1"] * attributes["piT"]
                    + attributes["C2"] * attributes["piE"]
                    + attributes["lambda_cyc"]
                )
                * attributes["piQ"]
                * attributes["piL"]
            )

        elif attributes["subcategory_id"] == 9:
            attributes["C1"] = get_die_complexity_factor(
                attributes["subcategory_id"],
                attributes["technology_id"],
                attributes["application_id"],
                attributes["n_elements"],
            )
            attributes["C2"] = calculate_package_factor(
                attributes["package_id"], attributes["n_active_pins"]
            )
            attributes["piA"] = get_application_factor(
                attributes["type_id"], attributes["application_id"]
            )
            attributes["hazard_rate_active"] = (
                (
                    attributes["C1"] * attributes["piT"] * attributes["piA"]
                    + attributes["C2"] * attributes["piE"]
                )
                * attributes["piQ"]
                * attributes["piL"]
            )
        elif attributes["subcategory_id"] == 10:
            attributes["lambdaBD"] = get_die_base_hazard_rate(attributes["type_id"])
            attributes["lambdaBP"] = calculate_package_base_hazard_rate(
                attributes["n_active_pins"]
            )
            attributes["lambdaEOS"] = calculate_eos_hazard_rate(
                attributes["voltage_esd"]
            )
            attributes["piCD"] = calculate_die_complexity_factor(
                attributes["area"], attributes["feature_size"]
            )
            attributes["piMFG"] = get_manufacturing_process_factor(
                attributes["manufacturing_id"]
            )
            attributes["piPT"] = get_package_type_correction_factor(
                attributes["package_id"]
            )

            attributes["hazard_rate_active"] = (
                attributes["lambdaBD"]
                * attributes["piMFG"]
                * attributes["piT"]
                * attributes["piCD"]
                + attributes["lambdaBP"]
                * attributes["piE"]
                * attributes["piQ"]
                * attributes["piPT"]
                + attributes["lambdaEOS"]
            )

        return attributes
    except KeyError as err:
        raise KeyError(
            f"calculate_part_stress: Missing required integrated circuit attribute:"
            f" {err}."
        )


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Calculate the part stress base hazard rate.

    This is always zero for integrated circuits, but we keep this function so the
    functions in milhdbk217f work.

    :param attributes: the hardware attribute dict for the integrated circuit to be
        calculated.
    :return: 0.0
    :rtype: float
    """
    return 0.0


def calculate_die_complexity_factor(
    area: float,
    feature_size: float,
) -> float:
    """Calculate the die complexity correction factor (piCD).

    :param area: the area of the die in sq. cm.
    :param feature_size: the size of the die features in microns.
    :return: _pi_cd; the die complexity factor.
    :rtype: float
    :raises: ZeroDivisionError if feature_size is zero.
    """
    try:
        return ((area / 0.21) * (2.0 / feature_size) ** 2.0 * 0.64) + 0.36
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "calculate_die_complexity_factor: Integrated circuit feature size must be "
            "greater than zero."
        )


def calculate_eos_hazard_rate(voltage_esd: float) -> float:
    """Calculate the electrical overstress hazard rate (lambdaEOS).

    :param voltage_esd: the ESD withstand voltage.
    :return: _lambda_eos; the electrical overstress hazard rate.
    :rtype: float
    """
    return (-log(1.0 - 0.00057 * exp(-0.0002 * voltage_esd))) / 0.00876


def calculate_junction_temperature(
    temperature_case: float,
    power_operating: float,
    theta_jc: float,
) -> float:
    """Calculate the junction temperature (Tj).

    :param temperature_case: the temperature of the IC case in C.
    :param power_operating: the operating power if the IC in W.
    :param theta_jc: the junction-case thermal resistance in C / W.
    :return: _t_j; the calculate junction temperature in C.
    :rtype: float
    """
    return temperature_case + power_operating * theta_jc


def calculate_lambda_cyclic_factors(
    n_cycles: int,
    construction_id: int,
    n_elements: int,
    temperature_junction: float,
) -> Tuple[float, float, float, float]:
    """Calculate the write cycle hazard rate A and B factors for EEPROMs.

    :param n_cycles: the expected number of lifetime write cycles.
    :param construction_id: the construction type identifier.
    :param n_elements: the number of elements (bits) in the memory device.
    :param temperature_junction: the junction temperature in C.
    :return: (_a_1, _a_2, _b_1, _b_2); the calculated factors.
    :rtype: tuple
    """
    # Calculate the A1 factor for lambda_CYC.
    _a_1 = 6.817e-6 * n_cycles

    # Find the A2, B1, and B2 factors for lambda_CYC.
    _a_2 = 0.0
    if construction_id == 1:
        _b_1 = ((n_elements / 16000.0) ** 0.5) * (
            exp(
                (-0.15 / 8.63e-5)
                * ((1.0 / (temperature_junction + 273.0)) - (1.0 / 333.0))
            )
        )
        _b_2 = 0.0
    elif construction_id == 2:
        _a_2 = 1.1 if 300000 < n_cycles <= 400000 else 2.3
        _b_1 = ((n_elements / 64000.0) ** 0.25) * (
            exp(
                (0.1 / 8.63e-5)
                * ((1.0 / (temperature_junction + 273.0)) - (1.0 / 303.0))
            )
        )
        _b_2 = ((n_elements / 64000.0) ** 0.25) * (
            exp(
                (-0.12 / 8.63e-5)
                * ((1.0 / (temperature_junction + 273.0)) - (1.0 / 303.0))
            )
        )
    else:
        _b_1 = 0.0
        _b_2 = 0.0

    return _a_1, _a_2, _b_1, _b_2


def calculate_package_base_hazard_rate(n_active_pins: int) -> float:
    """Calculate the package base hazard rate (lambdaBP).

    :param n_active_pins: the number of active (current carrying) pins.
    :return: _lambda_bd; the calculated package base hazard rate.
    :rtype: float
    """
    return 0.0022 + (1.72e-5 * n_active_pins)


def calculate_package_factor(
    package_id: int,
    n_active_pins: int,
) -> float:
    """Calculate the package factor (C2).

    :param package_id: the package type identifier.
    :param n_active_pins: the number of active (current carying) pins in the
        application.
    :return: _c2; the calculated package factor.
    :rtype: float
    """
    if package_id in {1, 2, 3}:
        _package = 1
    elif package_id == 4:
        _package = 2
    elif package_id == 5:
        _package = 3
    elif package_id == 6:
        _package = 4
    else:
        _package = 5

    _f0 = C2[_package][0]
    _f1 = C2[_package][1]

    return _f0 * (n_active_pins**_f1)


def calculate_temperature_factor(
    subcategory_id: int,
    family_id: int,
    type_id: int,
    temperature_junction: float,
) -> float:
    """Calculate the temperature factor (piT).

    :param subcategory_id: the subcategory identifier.
    :param family_id: the IC family identifier.
    :param type_id: the IC type identifier.
    :param temperature_junction: the junction temperature in C.
    :return: _pi_t; the calculated temperature factor.
    :rtype: float
    :raises: KeyError if passed an unknown subcategory ID.
    :raises: IndexError if passed an unknown family ID or type ID.
    """
    try:
        if subcategory_id == 2:
            _ref_temp = 296.0
            _ea = ACTIVATION_ENERGY[subcategory_id][family_id - 1]
        elif subcategory_id == 9:
            _ref_temp = 423.0
            _ea = ACTIVATION_ENERGY[subcategory_id][type_id - 1]
        else:
            _ref_temp = 296.0
            _ea = ACTIVATION_ENERGY[subcategory_id]

        return 0.1 * exp(
            (-_ea / 8.617e-5)
            * ((1.0 / (temperature_junction + 273)) - (1.0 / _ref_temp))
        )
    except IndexError:
        raise IndexError(
            f"calculate_temperature_factor: Invalid integrated circuit "
            f"family ID {family_id} or type ID {type_id}."
        )
    except KeyError:
        raise KeyError(
            f"calculate_temperature_factor: Invalid integrated circuit "
            f"subcategory ID {subcategory_id}."
        )


def get_application_factor(
    type_id: int,
    application_id: int,
) -> float:
    """Retrieve the application factor (piA).

    :param type_id: the IC type identifier.
    :param application_id: the IC application identifier.
    :return: _pi_a; the retrieved application factor.
    :rtype: float
    :raises: IndexError if passed an unknown application ID.
    :raises: KeyError if passed an unknown type ID.
    """
    try:
        return PI_A[type_id][application_id - 1]
    except IndexError:
        raise IndexError(
            f"get_application_factor: Invalid integrated circuit "
            f"application ID {application_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_application_factor: Invalid integrated circuit type ID {type_id}."
        )


def get_die_base_hazard_rate(type_id: int) -> float:
    """Retrieve the base hazard rate for a VHISC/VLSI die.

    :param type_id: the VHISC/VLSI type identifier.
    :return: _lambda_bd; the base die hazard rate.
    :rtype: float
    """
    return 0.16 if type_id == 1 else 0.24


def get_die_complexity_factor(
    subcategory_id: int,
    technology_id: int,
    application_id: int,
    n_elements: int,
) -> float:
    """Retrieve the die complexity hazard rate (C1).

    :param subcategory_id: the subcategory identifier.
    :param technology_id: the technology identifier.
    :param application_id: the application identifier.
    :param n_elements: the number of elements (transistors/gates) in the device.
    :return: _c1; the selected die complexity factor.
    :rtype: float
    :raises: KeyError if passed an unknown subcategory ID, technology ID, or application
        ID.
    :raises: ValueError if passed a number of elements not associated with the
        breakpoints in MIL-HDBK-217F.
    """
    _dic_breakpoints = {
        1: [100, 300, 1000, 10000],
        2: [100, 1000, 3000, 10000, 30000, 60000],
        3: {
            1: [200, 1000, 5000],
            2: [16000, 64000, 256000, 1000000],
        },
        4: [8, 16, 32],
        5: [16000, 64000, 256000, 100000],
        6: [16000, 64000, 256000, 100000],
        7: [16000, 64000, 256000, 100000],
        8: [16000, 64000, 256000, 100000],
        9: {1: [10, 1000], 2: [1000, 10000]},
    }

    try:
        if subcategory_id == 2 and technology_id == 11:
            _technology = 2
        elif subcategory_id == 2:
            _technology = 1
        else:
            _technology = technology_id

        if subcategory_id == 3:
            _lst_index = _dic_breakpoints[subcategory_id][_technology]
        elif subcategory_id == 9:
            _lst_index = _dic_breakpoints[subcategory_id][application_id]
        else:
            _lst_index = _dic_breakpoints[subcategory_id]

        # This will retrieve the breakpoint value for the number of elements
        # closest (round up) to the number of elements passed.
        _index = min(
            range(len(_lst_index)), key=lambda i: abs(_lst_index[i] - n_elements)
        )

        return C1[subcategory_id][_technology - 1][_index]
    except KeyError:
        raise KeyError(
            f"get_die_complexity_factor: Invalid integrated circuit "
            f"application ID {application_id}, subcategory ID "
            f"{subcategory_id}, or technology ID {technology_id}."
        )
    except ValueError:
        raise ValueError(
            f"get_die_complexity_factor: Invalid number of integrated "
            f"circuit elements {n_elements}."
        )


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]):
    """Retrieve the environment factor (piE) for the passed environment ID."""
    _environment_id = attributes["environment_active_id"]

    try:
        return PI_E[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid integrated circuit "
            f"environment ID {_environment_id}."
        )


def get_error_correction_factor(type_id: int) -> float:
    """Retrieve the error code correction factor (piECC).

    :param type_id: the error correction type identifier.
    :return: _pi_ecc; the value of piECC.
    :rtype: float
    :raises: KeyError if passed an invalid type_id.
    """
    try:
        return {1: 1.0, 2: 0.72, 3: 0.68}[type_id]
    except KeyError:
        raise KeyError(
            f"get_error_correction_factor: Invalid integrated circuit type "
            f"ID {type_id}."
        )


def get_manufacturing_process_factor(manufacturing_id: int) -> float:
    """Retrieve teh the manufacturing process correction factor (piMFG).

    :param manufacturing_id: the manufacturing process identifier.
    :return: _pi_mfg; the manufacturing process correction factor.
    :rtype: float
    """
    return 0.55 if manufacturing_id == 1 else 2.0


def get_package_type_correction_factor(package_id: int) -> float:
    """Retrieve the package type correction factor (piPT).

    :param package_id: the package type identifier.
    :return: _pi_pt; the package type correction factor.
    :rtype: float
    :raises: KeyError if passed an unknown package ID.
    """
    try:
        return PI_PT[package_id]
    except KeyError:
        raise KeyError(
            f"get_package_type_correction_factor: Invalid integrated "
            f"circuit package ID {package_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Calculate parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. technology id; if the IC subcategory is NOT technology dependent,
            then the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |       Integrated Circuit      | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Linear                        |        5.1      |
    +----------------+-------------------------------+-----------------+
    |        2       | Logic                         |        5.1      |
    +----------------+-------------------------------+-----------------+
    |        3       | PAL/PLA                       |        5.1      |
    +----------------+-------------------------------+-----------------+
    |        4       | Microprocessor/Microcontroller|        5.1      |
    +----------------+-------------------------------+-----------------+
    |        5       | Memory, ROM                   |        5.2      |
    +----------------+-------------------------------+-----------------+
    |        6       | Memory, EEPROM                |        5.2      |
    +----------------+-------------------------------+-----------------+
    |        7       | Memory, DRAM                  |        5.2      |
    +----------------+-------------------------------+-----------------+
    |        8       | Memory, SRAM                  |        5.2      |
    +----------------+-------------------------------+-----------------+
    |        9       | GaAS                          |        5.4      |
    +----------------+-------------------------------+-----------------+
    |       10       | VHSIC/VLSI                    |        5.3      |
    +----------------+-------------------------------+-----------------+

    :param attributes: the hardware attributes dict for the integrated circuit being
        calculated.
    :return: _base_hr; the parts count base hazard rate.
    :rtype: float
    :raises: IndexError if passed an invalid active environment ID.
    :raises: KeyError if passed an invalid subcategory ID or technology ID
        (where used).
    :raises: ValueError if passed a number of elements not associated with the
        breakpoints in MIL-HDBK-217F.
    """
    _environment_id = attributes["environment_active_id"]
    _n_elements = attributes["n_elements"]
    _subcategory_id = attributes["subcategory_id"]
    _technology_id = attributes["technology_id"]

    # Dictionary containing the number of element breakpoints for determining
    # the base hazard rate list to use.
    _dic_breakpoints = {
        1: [100, 300, 1000, 10000],
        2: [100, 1000, 3000, 10000, 30000, 60000],
        3: {
            1: [200, 1000, 5000],
            2: [16000, 64000, 256000, 1000000],
        },
        4: [8, 16, 32],
        5: [16000, 64000, 256000, 100000],
        6: [16000, 64000, 256000, 100000],
        7: [16000, 64000, 256000, 100000],
        8: [16000, 64000, 256000, 100000],
        9: {
            1: [10, 100],
            2: [1000, 10000],
        },
    }

    try:
        if _subcategory_id in {3, 9}:
            _index = (
                _dic_breakpoints[_subcategory_id][_technology_id].index(_n_elements) + 1
            )
        else:
            _lst_index = _dic_breakpoints[_subcategory_id]
            _index = (
                min(
                    range(len(_lst_index)),
                    key=lambda i: abs(_lst_index[i] - _n_elements),
                )
                + 1
            )

        return (
            PART_COUNT_LAMBDA_B[_subcategory_id][_index][_environment_id - 1]
            if _subcategory_id == 1
            else PART_COUNT_LAMBDA_B[_subcategory_id][_technology_id][_index][
                _environment_id - 1
            ]
        )
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid integrated circuit environment "
            f"ID {_environment_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid integrated circuit subcategory "
            f"ID {_subcategory_id} or technology ID {_technology_id}."
        )
    except ValueError:
        raise ValueError(
            f"get_part_count_lambda_b: Invalid number of integrated circuit "
            f"elements {_n_elements} for subcategory ID {_subcategory_id}."
        )


def get_quality_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the quality factor (piQ).

    :param attributes: the hardware attributes dict for the integrated circuit being
        calculated.
    :return: the quality factor for the passed quality ID.
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id: int = attributes["quality_id"]

    try:
        return PI_Q[_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_quality_factor: Invalid integrated circuit quality ID {_quality_id}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    :param attributes: the attribute dict for the integrated circuit being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["years_in_production"] <= 0.0:
        attributes["years_in_production"] = 2.0

    if attributes["package_id"] <= 0:
        attributes["package_id"] = 1

    attributes["temperature_junction"] = _set_default_junction_temperature(
        attributes["temperature_junction"],
        attributes["temperature_case"],
        attributes["environment_active_id"],
    )

    return attributes


def _set_default_junction_temperature(
    temperature_junction: float,
    temperature_case: float,
    environment_active_id: int,
) -> float:
    """Set the default junction temperature for integrated circuits.

    :param temperature_junction: the current junction temperature.
    :param temperature_case: the current case temperature of the integrated circuit with
        missing defaults.
    :param environment_active_id: the active operating environment ID of the integrated
        circuit with missing defaults.
    :return: _temperature_junction
    :rtype: float
    """
    if temperature_junction > 0.0:
        return temperature_junction

    try:
        return {
            1: 50.0,
            2: 60.0,
            3: 65.0,
            4: 60.0,
            5: 65.0,
            6: 75.0,
            7: 75.0,
            8: 90.0,
            9: 90.0,
            10: 75.0,
            11: 50.0,
            12: 65.0,
            13: 75.0,
            14: 60.0,
        }[environment_active_id]
    except KeyError:
        return temperature_case
