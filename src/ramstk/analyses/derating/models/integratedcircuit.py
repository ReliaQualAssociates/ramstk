# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.integratedcircuit.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_current_limit,
    do_check_temperature_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    *,
    current_ratio: float,
    package_id: int,
    technology_id: int,
    temperature_junction: float,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for integrated circuits.

    :param environment_id: the index for the environment the integrated circuit is
        operating in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the integrated circuit being checked
        for overstress.
    :param stress_limits: the dict containing the stress derating limits for integrated
        circuits.
    :param current_ratio: the operating to rated current ratio of the integrated circuit
        being checked for overstress.
    :param package_id: the package ID of the integrated circuit being checked for
        overstress.
    :param technology_id: the technology ID of the integrated circuit being checked for
        overstress.
    :param temperature_junction: the junctions temperature of the integrated circuit
        being checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid subcategory ID, package ID, or technology
        ID.
    :raises: TypeError when passed a non-numeric value for the current ratio or junction
        temperature.
    """
    _overstress: int = 0
    _reason: str = ""

    try:
        # Map subcategory, technology, and package IDs.
        _subcategory = {
            1: "digital",
            2: "linear",
            3: "microprocessor",
            4: "memory",
        }[subcategory_id]
        _technology = {
            1: "bipolar",
            2: "mos",
        }[technology_id]
        _package = {
            1: "hermetic",
            2: "hermetic",
            3: "hermetic",
            4: "plastic1",
            5: "plastic1",
            6: "plastic1",
            7: "plastic2",
            8: "plastic2",
            9: "plastic2",
        }[package_id]

        _overstress, _reason = do_check_current_limit(
            current_ratio,
            stress_limits[_subcategory][_technology][_package]["current"][
                environment_id
            ],
        )

        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_temperature_limit(
                temperature_junction,
                stress_limits[_subcategory][_technology][_package]["temperature"][
                    environment_id
                ],
                0.0,  # No delta for temperature check
            ),
        )

        return _overstress, _reason
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid integrated circuit "
            f"environment ID {environment_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"do_derating_analysis: Invalid integrated circuit package ID "
            f"{package_id}, subcategory ID {subcategory_id}, or technology ID "
            f"{technology_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid integrated circuit current "
            f"ratio type {type(current_ratio)} or junction temperature "
            f"{type(temperature_junction)}."
        ) from exc
