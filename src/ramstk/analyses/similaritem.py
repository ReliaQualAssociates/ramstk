# -*- coding: utf-8 -*-
#
#       ramstk.analyses.similaritem.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Reliability Similar Item Assessment Module."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple, Type

# Third Party Imports
from sympy import symbols, sympify

ENVIRONMENT_FROM_TO: Dict[Tuple[int, int], float] = {
    (0, 0): 1.0,
    (1, 1): 1.0,
    (1, 2): 0.2,
    (1, 3): 0.3,
    (1, 4): 0.3,
    (1, 5): 0.1,
    (1, 6): 1.1,
    (2, 1): 5.0,
    (2, 2): 1.0,
    (2, 3): 1.4,
    (2, 4): 1.4,
    (2, 5): 0.5,
    (2, 6): 5.0,
    (3, 1): 3.3,
    (3, 2): 0.7,
    (3, 3): 1.0,
    (3, 4): 1.0,
    (3, 5): 0.3,
    (3, 6): 3.3,
    (4, 1): 3.3,
    (4, 2): 0.7,
    (4, 3): 1.0,
    (4, 4): 1.0,
    (4, 5): 0.3,
    (4, 6): 3.3,
    (5, 1): 10.0,
    (5, 2): 2.0,
    (5, 3): 3.3,
    (5, 4): 3.3,
    (5, 5): 1.0,
    (5, 6): 10.0,
    (6, 1): 0.9,
    (6, 2): 0.2,
    (6, 3): 0.3,
    (6, 4): 0.3,
    (6, 5): 0.1,
    (6, 6): 1.0,
}
QUALITY_FROM_TO: Dict[Tuple[int, int], float] = {
    (0, 0): 1.0,
    (1, 1): 1.0,
    (1, 2): 0.8,
    (1, 3): 0.5,
    (1, 4): 0.2,
    (2, 1): 1.3,
    (2, 2): 1.0,
    (2, 3): 0.6,
    (2, 4): 0.3,
    (3, 1): 2.0,
    (3, 2): 1.7,
    (3, 3): 1.0,
    (3, 4): 0.4,
    (4, 1): 5.0,
    (4, 2): 3.3,
    (4, 3): 2.5,
    (4, 4): 1.0,
}
TEMPERATURE_FROM_TO: Dict[Tuple[float, float], float] = {
    (10.0, 10.0): 1.0,
    (10.0, 20.0): 0.9,
    (10.0, 30.0): 0.8,
    (10.0, 40.0): 0.8,
    (10.0, 50.0): 0.7,
    (10.0, 60.0): 0.5,
    (10.0, 70.0): 0.4,
    (20.0, 10.0): 1.1,
    (20.0, 20.0): 1.0,
    (20.0, 30.0): 0.9,
    (20.0, 40.0): 0.8,
    (20.0, 50.0): 0.7,
    (20.0, 60.0): 0.6,
    (20.0, 70.0): 0.5,
    (30.0, 10.0): 1.2,
    (30.0, 20.0): 1.1,
    (30.0, 30.0): 1.0,
    (30.0, 40.0): 0.9,
    (30.0, 50.0): 0.8,
    (30.0, 60.0): 0.6,
    (30.0, 70.0): 0.5,
    (40.0, 10.0): 1.3,
    (40.0, 20.0): 1.2,
    (40.0, 30.0): 1.1,
    (40.0, 40.0): 1.0,
    (40.0, 50.0): 0.9,
    (40.0, 60.0): 0.7,
    (40.0, 70.0): 0.6,
    (50.0, 10.0): 1.5,
    (50.0, 20.0): 1.4,
    (50.0, 30.0): 1.2,
    (50.0, 40.0): 1.1,
    (50.0, 50.0): 1.0,
    (50.0, 60.0): 0.8,
    (50.0, 70.0): 0.7,
    (60.0, 10.0): 1.9,
    (60.0, 20.0): 1.7,
    (60.0, 30.0): 1.6,
    (60.0, 40.0): 1.5,
    (60.0, 50.0): 1.2,
    (60.0, 60.0): 1.0,
    (60.0, 70.0): 0.8,
    (70.0, 10.0): 2.4,
    (70.0, 20.0): 2.2,
    (70.0, 30.0): 1.9,
    (70.0, 40.0): 1.8,
    (70.0, 50.0): 1.5,
    (70.0, 60.0): 1.2,
    (70.0, 70.0): 1.0,
}


# noinspection PyTypeChecker
def calculate_topic_633(
    environment: Dict[str, float],
    quality: Dict[str, float],
    temperature: Dict[str, float],
    hazard_rate: float,
) -> Tuple[float, float, float, float]:
    """Calculate the Similar Item analysis using Topic 6.3.3 approach.

    This method calculates the new hazard rate using the approach found
    in The Reliability Toolkit: Commercial Practices Edition, Topic 6.3.3.

    :param environment: the active environment ID for the from and to
        environments.
    :param quality: the quality level ID for the from and to quality.
    :param temperature: the ambient operating temperature (in C) for the
        from and to temperatures.
    :param hazard_rate: the current hazard rate of the hardware item
        being calculated.
    :return: (_change_factor_1, _change_factor_2, _change_factor_3, _result_1);
        the three change factors (quality, environment, and temperature) and
        the assessment result.
    :rtype: tuple
    :raise: KeyError if passed an environment, quality, or temperature dict
        that is missing the from, to, or both keys.
    :raise: TypeError if passed a string value for either temperature.
    """
    # Convert user-supplied temperatures to whole values used in Topic 633.
    temperature["from"] = _do_validate_temperature(temperature["from"])
    temperature["to"] = _do_validate_temperature(temperature["to"])

    _change_factor_1 = QUALITY_FROM_TO[
        (quality["from"], quality["to"])  # type: ignore
    ]  # type: ignore
    _change_factor_2 = ENVIRONMENT_FROM_TO[
        (environment["from"], environment["to"])  # type: ignore
    ]  # type: ignore
    _change_factor_3 = TEMPERATURE_FROM_TO[(temperature["from"], temperature["to"])]

    _result_1 = float(
        hazard_rate / (_change_factor_1 * _change_factor_2 * _change_factor_3)
    )

    return _change_factor_1, _change_factor_2, _change_factor_3, _result_1


# pylint: disable=too-many-locals
def calculate_user_defined(sia: Dict[str, int | float | str]):
    """Calculate the user-defined similar item analysis.

    :param sia: the user-defined similar item assessment dict.  The
        calling method/function should create the sia dict as follows:

        sia = OrderedDict({
            _key: None
            for _key in [
                'hr', 'pi1', 'pi2', 'pi3', 'pi3', 'pi4', 'pi5', 'pi6', 'pi7',
                'pi8', 'pi9', 'pi10', 'uf1', 'uf2', 'uf3', 'uf4', 'uf5', 'ui1',
                'ui2', 'ui3', 'ui4', 'ui5', 'equation1', 'equation2',
                'equation3', 'equation4', 'equation5', 'res1', 'res2', 'res3',
                'res4', 'res5'
                ]
            })

    :return: sia; the similar item assessment dict with updated results.
    :rtype: dict
    """
    _symbol_list = [
        "hr",
        "pi1",
        "pi2",
        "pi3",
        "pi4",
        "pi5",
        "pi6",
        "pi7",
        "pi8",
        "pi9",
        "pi10",
        "uf1",
        "uf2",
        "uf3",
        "uf4",
        "uf5",
        "ui1",
        "ui2",
        "ui3",
        "ui4",
        "ui5",
        "res1",
        "res2",
        "res3",
        "res4",
        "res5",
    ]
    _symbols_dict = symbols(" ".join(_symbol_list))

    for _idx in range(1, 6):
        _equation_key = f"equation{_idx}"
        _equation = str(sia.get(_equation_key, "0.0"))

        # Validate the equation.
        sia[_equation_key] = _do_validate_equation(_equation)

        # Loop through each result field (res1, res2, ..., res5)
        _result_key = f"res{_idx}"

        if (
            _equation_key in sia and sia[_equation_key]
        ):  # Check if equation exists and is not empty
            sia[_result_key] = sympify(sia[_equation_key]).evalf(
                subs={
                    _symbols_dict[j]: sia[_symbol_list[j]]
                    for j in range(len(_symbol_list))
                }
            )
        else:
            sia[_result_key] = 0.0  # Default to 0.0 if equation is empty

    return sia


def set_user_defined_change_factors(
    sia: Dict[str, float], factors: List[float]
) -> Dict[str, float]:
    """Set the change factors for the user-defined calculations.

    :param sia: the similar item assessment dict.
    :param list factors: the list of change factors; the list items are float or int.
    :return: sia; the similar item assessment dict with updated factor values.
    :rtype: dict
    """
    _do_update_sia_values(sia, factors, 1, 10, 0.0, float)
    return sia


def set_user_defined_floats(
    sia: Dict[str, float], floats: List[float]
) -> Dict[str, float]:
    """Set the user-defined float values for the user-defined calculations.

    :param sia: the similar item assessment dict.
    :param list floats: the list of float values.
    :return: sia; the similar item assessment dict with updated float values.
    :rtype: dict
    """
    _do_update_sia_values(sia, floats, 11, 15, 0.0, float)
    return sia


def set_user_defined_ints(sia: Dict[str, int], ints: List[int]) -> Dict[str, int]:
    """Set the user-defined integer values for the user-defined calculations.

    :param sia: the similar item assessment dict.
    :param list ints: the list of integer values.
    :return: sia; the similar item assessment dict with updated integer values.
    :rtype: dict
    """
    _do_update_sia_values(sia, ints, 16, 20, 0, int)
    return sia


def set_user_defined_functions(
    sia: Dict[str, str], functions: List[str]
) -> Dict[str, str]:
    """Set the user-defined functions for the user-defined calculations.

    :param sia: the similar item assessment dict.
    :param list functions: the list of functions; list items are str.
    :return: sia; the similar item assessment dict with updated functions.
    :rtype: dict
    """
    _do_update_sia_values(sia, functions, 21, 25, "", str)
    return sia


def set_user_defined_results(
    sia: Dict[str, float], results: List[float]
) -> Dict[str, float]:
    """Set the user-defined results for the user-defined calculations.

    This allows the use of the results fields to be manually set to float values by the
    user essentially creating five more user-defined float values.

    :param sia: the similar item assessment dict.
    :param list results: the list of results.
    :return: sia; the similar item assessment dict with updated results.
    :rtype: dict
    """
    _do_update_sia_values(sia, results, 26, 30, 0.0, float)
    return sia


# ruff: noqa: PLR0913
def _do_update_sia_values(
    sia: Dict[str, Any],
    values: List[Any],
    start_idx: int,
    end_idx: int,
    default_value: Any,
    value_type: Type,
) -> None:
    """Update the SIA dictionary with values from a list.

    Functions also converts them to the specified type.

    :param sia: the similar item assessment dict.
    :param values: the list of values to insert into `sia`.
    :param start_idx: the start index in the SIA dictionary.
    :param end_idx: the end index in the SIA dictionary.
    :param default_value: the default value to use when the value list runs out of
        items.
    :param value_type: the type to which the values should be converted (int or float).
    """
    for _idx in range(start_idx, end_idx + 1):
        _key = list(sia.keys())[_idx]
        try:
            sia[_key] = value_type(values[_idx - start_idx])
        except (IndexError, ValueError, TypeError):
            sia[_key] = value_type(default_value)


def _do_validate_equation(equation: str) -> str:
    """Validate and return the equation or a default value."""
    return equation if equation.strip() else "0.0"


def _do_validate_temperature(temp: float) -> float:
    """Ensure the temperature is a valid number; round to the nearest multiple of 10."""
    if not isinstance(temp, (int, float)):
        raise TypeError(f"Temperature must be a number, got {type(temp)}")
    return round(temp / 10.0) * 10.0
