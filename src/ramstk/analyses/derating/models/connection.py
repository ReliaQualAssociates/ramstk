# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.connection.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import do_check_current_limit


def do_derating_analysis(
    environment_id: int,
    stress_limits: Dict[str, List[float]],
    *,
    current_ratio: float,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for connections.

    :param environment_id: the index for the environment the connection is operating in;
        0=protected, 1=normal, 2=severe.
    :param stress_limits: the dict containing the stress derating limits for
        connections.
    :param current_ratio: the operating to rated current ratio of the connection being
        checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: TypeError when passed a non-numeric current ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    try:
        return do_check_current_limit(
            current_ratio,
            stress_limits["current"][environment_id],
        )
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid connection environment ID "
            f"{environment_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid connection current ratio "
            f"type {type(current_ratio)}.  Should be <type 'float'>."
        ) from exc
