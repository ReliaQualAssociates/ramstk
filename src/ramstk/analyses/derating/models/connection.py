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
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for connections.

    :param environment_id: the index for the environment the connection is operating in;
        0=protected, 1=normal, 2=severe.
    :param stress_limits: the dict containing the stress derating limits for
        connections.
    :return: _overstress, _reason
    :rtype: tuple :raise: IndexError if an unknown environment ID is passed. :raise:
        TypeError if a non-numeric value is passed for the current ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    # Check current limits
    _overstress, _reason = do_check_current_limit(
        kwargs["current_ratio"],
        stress_limits["current"][environment_id],
    )

    return _overstress, _reason
