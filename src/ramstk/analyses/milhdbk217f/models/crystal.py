# -*- coding: utf-8 -*-
#
#       ramstk.analyses.models.milhdbk217f..Crystal.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Crystal MIL-HDBK-217F Constants and Calculations Module."""

PART_COUNT_LAMBDA_B = [
    0.032, 0.096, 0.32, 0.19, 0.51, 0.38, 0.54, 0.70, 0.90, 0.74, 0.016, 0.42,
    1.0, 16.0
]
PART_COUNT_PI_Q = [1.0, 3.4]
PART_STRESS_PI_Q = [1.0, 2.1]
PI_E = [
    1.0, 3.0, 10.0, 6.0, 16.0, 12.0, 17.0, 22.0, 28.0, 23.0, 0.5, 13.0, 32.0,
    500.0
]


def calculate_part_count(**attributes):
    """
    Wrap get_part_count_lambda_b().

    This wrapper allows us to pass an attributes dict from a generic parts
    count function.

    :param dict attributes: the attributes for the crystal being calculated.
    :return: _base_hr; the list of base hazard rates.
    :rtype: float
    """
    return get_part_count_lambda_b(attributes['environment_active_id'], )


def calculate_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a crystal.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :param dict attributes: the attributes for the crystal being calculated.
    :return: attributes; the keyword argument (hardware attribute)
             dictionary with updated values.
    :rtype: dict
    """
    attributes['lambda_b'] = 0.013 * attributes['frequency_operating']**0.23

    attributes['hazard_rate_active'] = (attributes['lambda_b']
                                        * attributes['piQ']
                                        * attributes['piE'])

    return attributes


def get_part_count_lambda_b(environment_active_id):
    """
    Retrieve the part count base hazard rate for a crystal.

    :param int environment_active_id: the active environment identifier.
    :return: _base_hr; the part count base hazard rate for the active
        environment.
    :rtype: float
    :raise: IndexError if passed an unknown active environment ID.
    """
    return PART_COUNT_LAMBDA_B[environment_active_id - 1]
