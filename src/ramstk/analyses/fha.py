# -*- coding: utf-8 -*-
#
#       ramstk.analyses.fha.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Functional Hazards Analysis (FHA) Module."""

# Standard Library Imports
import re
from typing import Any, Dict, List

# Third Party Imports
from sympy import SympifyError, symbols, sympify

# RAMSTK Package Imports
from ramstk.exceptions import OutOfRangeError

PROBABILITY = {
    "Level E - Extremely Unlikely": 1,
    "Level D - Remote": 2,
    "Level C - Occasional": 3,
    "Level B - Reasonably Probable": 4,
    "Level A - Frequent": 5,
}
SEVERITY = {
    "Insignificant": 1,
    "Slight": 2,
    "Low": 3,
    "Medium": 4,
    "High": 5,
    "Major": 6,
}
VALID_VARIABLES = {
    "hr",
    "pi1",
    "pi2",
    "pi3",
    "pi4",
    "pi5",
    "uf1",
    "uf2",
    "uf3",
    "ui1",
    "ui2",
    "ui3",
    "res1",
    "res2",
    "res3",
    "res4",
    "res5",
    "0",
}


def calculate_hri(probability: str, severity: str) -> int:
    """Calculate the hazard risk index (HRI).

    .. note:: See MIL-STD-882.

    :param probability: the hazard probability expressed in text.
    :param severity: the hazard severity expressed in text.
    :return: _hri; the calculated hazard risk index.
    :rtype: int
    :raise: OutOfRangeError if passed an unknown probability or severity
        description.
    """
    try:
        return PROBABILITY[probability] * SEVERITY[severity]
    except KeyError as _error:
        raise OutOfRangeError(
            (f"Unknown hazard probability ({probability}) or severity ({severity}).")
        ) from _error


def calculate_user_defined(fha: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate the user-defined hazards analysis.

    :param fha: the user-defined functional hazards assessment dict.  The
        calling method/function should create the fha dict as follows:

        fha = OrderedDict({
            _key: None
            for _key in [
                'uf1', 'uf2', 'uf3', 'ui1', 'ui2', 'ui3', 'equation1',
                'equation2', 'equation3', 'equation4', 'equation5', 'res1',
                'res2', 'res3', 'res4', 'res5'
                ]
            })

    :return: fha; the functional hazards assessment dict with updated results.
    :rtype: dict
    """
    (uf1, uf2, uf3, ui1, ui2, ui3, res1, res2, res3, res4, res5) = symbols(
        "uf1 uf2 uf3 ui1 ui2 ui3 res1 res2 res3 res4 res5"
    )

    for _idx in range(1, 6):
        _equation_key = f"equation{_idx}"
        _equation = fha.get(_equation_key, "0.0")

        # If the equation is empty, replace it with "0.0".
        if not _equation.strip():
            fha[_equation_key] = "0.0"
        else:
            # Validate the equation if it's not empty.
            _do_validate_equation(_equation)

        # Safely evaluate the equation using sympify
        try:
            fha[f"res{_idx}"] = sympify(_equation).evalf(
                subs={
                    uf1: fha["uf1"],
                    uf2: fha["uf2"],
                    uf3: fha["uf3"],
                    ui1: fha["ui1"],
                    ui2: fha["ui2"],
                    ui3: fha["ui3"],
                    res1: fha["res1"],
                    res2: fha["res2"],
                    res3: fha["res3"],
                    res4: fha["res4"],
                    res5: fha["res5"],
                }
            )
        except SympifyError as exc:
            raise ValueError(f"Invalid syntax in equation{_idx}: {_equation}") from exc

    return fha


def set_user_defined_floats(fha: Dict[str, Any], floats: List[float]) -> Dict[str, Any]:
    """Set the user-defined float values for the user-defined calculations.

    :param fha: the functional hazard assessment dict.
    :param list floats: the list of float values.
    :return: fha; the functional hazard assessment dict with updated float values.
    :rtype: dict
    """
    for _idx in range(3):
        fha[f"uf{_idx + 1}"] = float(floats[_idx]) if _idx < len(floats) else 0.0

    return fha


def set_user_defined_ints(fha: Dict[str, Any], ints: List[int]) -> Dict[str, Any]:
    """Set the user-defined integer values for the user-defined calculations.

    :param fha: the functional hazard assessment dict.
    :param list ints: the list of integer values.
    :return: fha; the functional hazard assessment dict with updated integer values.
    :rtype: dict
    """
    for _idx in range(3):
        fha[f"ui{_idx + 1}"] = int(ints[_idx]) if _idx < len(ints) else 0

    return fha


def set_user_defined_functions(
    fha: Dict[str, Any], functions: List[str]
) -> Dict[str, Any]:
    """Set the user-defined functions for the user-defined calculations.

    .. note:: by default we set the function equal to 0.0.  This prevents Sympy
        errors resulting from empty strings.

    :param fha: the functional hazard assessment dict.
    :param list functions: the list of functions; list items are str.
    :return: fha; the functional hazard assessment dict with updated functions.
    :rtype: dict
    """
    for _idx in range(5):
        try:
            _key = list(fha.keys())[_idx + 6]
            _equation = str(functions[_idx]).strip()

            # If the function is an empty string, replace it with "0.0".
            if not _equation:
                fha[_key] = "0.0"
            else:
                # Validate non-empty equations
                _do_validate_equation(_equation)
                fha[_key] = _equation

        except IndexError:
            # If functions list doesn't contain enough elements, set the remaining
            # to "0.0".
            fha[_key] = "0.0"

    return fha


def set_user_defined_results(
    fha: Dict[str, Any], results: List[float]
) -> Dict[str, Any]:
    """Set the user-defined results for the user-defined calculations.

    This allows the use of the results fields to be manually set to float values by the
    user essentially creating five more user-defined float values.

    :param fha: the functional hazard assessment dict.
    :param list results: the list of results.
    :return: fha; the functional hazard assessment dict with updated results.
    :rtype: dict
    """
    for _idx in range(5):
        fha[f"res{_idx + 1}"] = float(results[_idx]) if _idx < len(results) else 0.0

    return fha


def _do_validate_equation(equation: str) -> None:
    """Validate that the equation contains only valid variables.

    :param equation: The equation to validate.
    :type equation: str
    :raises ValueError: If the equation contains invalid variables.
    """
    # Find all the variable names in the equation (alphanumeric strings).
    _variables = set(re.findall(r"\b\w+\b", equation))

    # Check if there are any variables not in the allowed set.
    _invalid_vars = _variables - VALID_VARIABLES

    if _invalid_vars:
        raise ValueError(
            f"Invalid variables found in equation: {', '.join(_invalid_vars)}"
        )
