# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.semiconductor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_current_limit,
    do_check_power_limit,
    do_check_temperature_limit,
    do_check_voltage_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    *,
    current_ratio: float,
    power_ratio: float,
    quality_id: int,
    temperature_junction: float,
    type_id: int,
    voltage_ratio: float,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for semiconductors.

    :param environment_id: the index for the environment the semiconductor is operating
        in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the semiconductor to check derating.
    :param stress_limits: the dict containing the stress derating limits for
        semiconductors.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid quality ID, subcategory ID, or type ID.
    :raises: TypeError if a non-numeric value is passed for the current ratio, power
        ratio, junction temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = _get_semiconductor_subcategory(subcategory_id)
    _type = _get_semiconductor_type(subcategory_id, type_id)
    _quality = _get_semiconductor_quality(quality_id)

    try:
        # Check current limit.
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_current_limit(
                current_ratio,
                stress_limits[_subcategory][_type][_quality]["current"][environment_id],
            ),
        )

        # Check power limit for specific subcategories and types.
        if (
            _subcategory == "diode"
            and _type in ["schottky", "regulator", "suppressor"]
            or _subcategory == "transistor"
        ):
            _overstress, _reason = do_update_overstress_status(
                _overstress,
                _reason,
                do_check_power_limit(
                    power_ratio,
                    stress_limits[_subcategory][_type][_quality]["power"][
                        environment_id
                    ],
                ),
            )

            # Check junction temperature limit.
            _overstress, _reason = do_update_overstress_status(
                _overstress,
                _reason,
                do_check_temperature_limit(
                    temperature_junction,
                    stress_limits[_subcategory][_type][_quality]["temperature"][
                        environment_id
                    ],
                    0.0,
                ),
            )

            # Check voltage limit.
            _overstress, _reason = do_update_overstress_status(
                _overstress,
                _reason,
                do_check_voltage_limit(
                    voltage_ratio,
                    stress_limits[_subcategory][_type][_quality]["voltage"][
                        environment_id
                    ],
                ),
            )

        return _overstress, _reason
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid semiconductor environment ID "
            f"{environment_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"do_derating_analysis: Invalid semiconductor quality ID {quality_id}, "
            f"subcategory ID {subcategory_id}, or type ID {type_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid semiconductor current ratio type "
            f"{type(current_ratio)}, power ratio type {type(power_ratio)}, junction "
            f"temperature type {type(temperature_junction)}, or voltage ratio type "
            f"{type(voltage_ratio)}.  All should be <type 'float'>."
        ) from exc


def _get_semiconductor_subcategory(subcategory_id: int) -> str:
    """Retrieve the semiconductor subcategory based on the subcategory ID.

    :param subcategory_id: the subcategory ID of the semiconductor being checked for
        overstress.
    :return: the selected semiconductor subcategory name or an empty string when passed
        an invalid subcategory ID.
    :rtype: str
    """
    _subcategories = {
        1: "diode",
        3: "transistor",
        4: "transistor",
        6: "transistor",
        7: "transistor",
        8: "transistor",
        9: "transistor",
        10: "thyristor",
    }

    return _subcategories.get(subcategory_id, "")


def _get_semiconductor_type(subcategory_id: int, type_id: int) -> str:
    """Retrieve the semiconductor type based on the subcategory ID and type ID.

    :param subcategory_id: the subcategory ID of the semiconductor being checked for
        overstress.
    :param type_id: the type ID of the semiconductor being checked for overstress.
    :return: the selected semiconductor type name or an empty string when passed an
        invalid subcategory ID or type ID.
    :rtype: str
    """
    _type_mapping = {
        1: {
            1: "general_purpose",
            2: "general_purpose",
            3: "power_rectifier",
            4: "schottky",
            5: "power_rectifier",
            6: "suppressor",
            7: "regulator",
            8: "regulator",
        },
        3: "bjt",
        4: "fet",
        6: "bjt",
        7: "bjt",
        9: "fet",
    }
    _type = _type_mapping.get(subcategory_id, "")
    return _type.get(type_id, "") if isinstance(_type, dict) else _type  # type: ignore


def _get_semiconductor_quality(quality_id: int) -> str:
    """Retrieve the semiconductor quality based on the quality ID.

    :param quality_id: the quality ID of the semiconductor being checked for overstress.
    :return: the selected semiconductor quality name or an empty string when passed an
        invalid quality ID.
    :rtype: str
    """
    return {
        1: "jantx",
        2: "jantx",
        3: "military",
        4: "commercial",
        5: "commercial",
    }.get(quality_id, "")
