# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.capacitor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_temperature_limit,
    do_check_voltage_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str | None, Dict[str, List[float]]],
    *,
    specification_id: int,
    temperature_case: float,
    temperature_rated_max: float,
    voltage_ratio: float,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for capacitors.

    :param environment_id: the index for the environment the capacitor is operating in;
        0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the capacitor being checked for
        overstress.
    :param stress_limits: the dict containing the stress derating limits for capacitors.
    :param specification_id: the specification ID of the capacitor being checked for
        overstress.
    :param temperature_case: the operating case temperature of the capacitor being
        checked for overstress.
    :param temperature_rated_max: the rated maximum temperature of the capacitor being
        checked for overstress.
    :param voltage_ratio: the operating to rated voltage ratio of the capacitor being
        checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: TypeError when passed a non-numeric case temperature or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = _get_subcategory_name(
        subcategory_id,
        specification_id,
    )

    try:
        # Check temperature limits
        _overstress, _reason = do_check_temperature_limit(
            temperature_case,
            temperature_rated_max,
            stress_limits[_subcategory]["temperature"][environment_id],
        )

        # Check voltage limits
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_voltage_limit(
                voltage_ratio,
                stress_limits[_subcategory]["voltage"][environment_id],
            ),
        )

        return _overstress, _reason
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid capacitor environment ID "
            f"{environment_id}."
        ) from exc
    except KeyError as exc:
        raise KeyError(
            f"_do_derating_analysis: Invalid capacitor specification ID "
            f"{specification_id} or subcategory ID {subcategory_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid capacitor case temperature type "
            f"{type(temperature_case)} or voltage ratio type {type(voltage_ratio)}.  "
            f"Both should be <class 'float'>."
        ) from exc


def _get_subcategory_name(
    subcategory_id: int,
    specification_id: int,
) -> str:
    """Retrieve the capacitor subcategory string name.

    :param subcategory_id: the subcategory ID of the capacitor being checked for
        overstress.
    :param specification_id: the specification ID of the capacitor being checked for
        overstress.
    :return: the selected name of the capacitor subcategory or empty string if passed an
        invalid specification ID or subcategory ID.
    :rtype: str
    """
    if subcategory_id in [11, 12]:
        return (
            {  # type: ignore[union-attr]
                11: {
                    1: "temp_comp_ceramic",
                    2: "ceramic_chip",
                },
                12: {
                    1: "tantalum_solid",
                    2: "tantalum_chip",
                },
            }
            .get(subcategory_id)
            .get(specification_id, "")
        )
    else:
        return {
            1: "paper",
            2: "paper",
            3: "plastic",
            4: "metallized",
            5: "metallized",
            6: "metallized",
            7: "mica",
            8: "mica_button",
            9: "glass",
            10: "ceramic_fixed",
            13: "tantalum_wet",
            14: "aluminum",
            15: "aluminum_dry",
            16: "ceramic_variable",
            17: "piston",
            18: "trimmer",
            19: "vacuum",
        }.get(subcategory_id, "")
