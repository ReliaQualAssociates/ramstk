# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.derating.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Derating Calculations Module."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Local Imports
from .models import (
    capacitor,
    connection,
    inductor,
    integratedcircuit,
    lamp,
    relay,
    resistor,
    semiconductor,
    switch,
)


def do_check_overstress(
    category: str,
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    **kwargs,
) -> Tuple[int, str]:
    """Perform a derating analysis.

    :param category: the category nome of the component being checked for overstress.
    :param environment_id: the environment ID for the component being checked for
        overstress.
    :param subcategory_id: the subcategory ID for the component being checked for
        overstress.
    :param stress_limits: the dict containing the component stress limit information.
    :return: whether the component being checked is overstressed and an overstress
        reason string.
    :rtype: tuple
    :raises: KeyError when passed an invalid environment ID, subcategory ID, or type ID.
    :raises: TypeError when passed a non-numeric value for the current ratio, power
        ratio, junction temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    try:
        _environment: int = {
            1: 0,
            2: 1,
            3: 2,
            4: 0,
            5: 2,
            6: 1,
            7: 1,
            8: 2,
            9: 2,
            10: 1,
            11: 0,
            12: 1,
            13: 2,
        }[environment_id]

        if category == "capacitor":
            _overstress, _reason = capacitor.do_derating_analysis(
                _environment,
                subcategory_id,
                stress_limits,  # type: ignore[arg-type]
                specification_id=kwargs.get("specification_id", 0),
                temperature_case=kwargs.get("temperature_case", 30.0),
                temperature_rated_max=kwargs.get("temperature_rated_max", 70.0),
                voltage_ratio=kwargs.get("voltage_ratio", 0.0),
            )
        elif category == "connection":
            _overstress, _reason = connection.do_derating_analysis(
                _environment,
                stress_limits,  # type: ignore[arg-type]
                current_ratio=kwargs.get("current_ratio", 0.0),
            )
        elif category == "inductor":
            _overstress, _reason = inductor.do_derating_analysis(
                _environment,
                subcategory_id,
                stress_limits,  # type: ignore[arg-type]
                current_ratio=kwargs.get("current_ratio", 0.0),
                family_id=kwargs.get("family_id", 0),
                temperature_hot_spot=kwargs.get("temperature_hot_spot", 30.0),
                temperature_rated_max=kwargs.get("temperature_rated_max", 70.0),
                voltage_ratio=kwargs.get("voltage_ratio", 0.0),
            )
        elif category == "integrated_circuit":
            _overstress, _reason = integratedcircuit.do_derating_analysis(
                _environment,
                subcategory_id,
                stress_limits,  # type: ignore[arg-type]
                current_ratio=kwargs.get("current_ratio", 0.0),
                package_id=kwargs.get("package_id", 0),
                technology_id=kwargs.get("technology_id", 0),
                temperature_junction=kwargs.get("temperature_junction", 70.0),
            )
        elif category == "miscellaneous":
            _overstress, _reason = lamp.do_derating_analysis(
                _environment,
                subcategory_id,
                stress_limits,  # type: ignore[arg-type]
                current_ratio=kwargs.get("current_ratio", 0.0),
            )
        elif category == "relay":
            _overstress, _reason = relay.do_derating_analysis(
                _environment,
                stress_limits,  # type: ignore[arg-type]
                current_ratio=kwargs.get("current_ratio", 0.0),
                temperature_active=kwargs.get("temperature_active", 30.0),
                temperature_rated_max=kwargs.get("temperature_rated_max", 85.0),
                type_id=kwargs.get("type_id", 0),
            )
        elif category == "resistor":
            _overstress, _reason = resistor.do_derating_analysis(
                _environment,
                subcategory_id,
                stress_limits,  # type: ignore[arg-type]
                power_rated=kwargs.get("power_rated", 0.0),
                power_ratio=kwargs.get("power_ratio", 0.0),
                temperature_case=kwargs.get("temperature_case", 30.0),
                temperature_knee=kwargs.get("temperature_knee", 70.0),
                temperature_rated_max=kwargs.get("temperature_rated_max", 150.0),
                voltage_ratio=kwargs.get("voltage_ratio", 0.0),
            )
        elif category == "semiconductor":
            _overstress, _reason = semiconductor.do_derating_analysis(
                _environment,
                subcategory_id,
                stress_limits,  # type: ignore[arg-type]
                current_ratio=kwargs.get("current_ratio", 0.0),
                power_ratio=kwargs.get("power_ratio", 0.0),
                quality_id=kwargs.get("quality_id", 1),
                temperature_junction=kwargs.get("temperature_junction", 70.0),
                type_id=kwargs.get("type_id", 0),
                voltage_ratio=kwargs.get("voltage_ratio", 0.0),
            )
        elif category == "switch":
            _overstress, _reason = switch.do_derating_analysis(
                _environment,
                stress_limits,  # type: ignore[arg-type]
                application_id=kwargs.get("application_id", 0),
                current_ratio=kwargs.get("current_ratio", 0.0),
                power_ratio=kwargs.get("power_ratio", 0.0),
            )

        return _overstress, _reason
    except KeyError as exc:
        raise KeyError(
            f"do_check_overstress: Invalid {category} environment ID {environment_id} "
            f"or subcategory ID {subcategory_id}."
        ) from exc
