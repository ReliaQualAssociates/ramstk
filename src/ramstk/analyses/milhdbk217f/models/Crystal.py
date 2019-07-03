# -*- coding: utf-8 -*-
#
#       ramstk.analyses.models.milhdbk217f..Crystal.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Crystal MIL-HDBK-217F Constants and Calculations Module."""

# <requirement>
#   <module>ramstk</module>
#   <name>Exceptions not used for flow control</name>
#   <description>Exceptions shall not be used for flow control.</description>
#   <rationale></rationale>
# </requirement>
# <requirement>
#   <module>ramstk</module>
#   <name>Handle exceptions at the level that knows how to handle them</name>
#   <description>Exceptions shall be handled at the lowest level there is
#   sufficient information to handle the exception.</description>
#   <rationale>Exceptions need to be handled at the level that can produce an
#   informative error log message as well as an informative error, warning, or
#   information dialog for the user.</rationale>
# </requirement>
# <requirement>
#    <module>ramstk</module>
#    <name>Do not handle programming exceptions</name>
#    <description>Exceptions such as IndexError, TypeError, KeyError, and
#    NameError are programming errors and should not be handled by RAMSTK, they
#    should be handled by the programmer.</description>
#    <rationale>Handling programming exceptions simply hides bugs.</rationale>
# </requirement>
# <requirement>
#   <module>ramstk</module>
#   <name>Document the exceptions thrown by a function/method</name>
#   <description>Add :raise: directives to the docstrings of functions and
#   methods to describe all the exceptions that function/method could raise.
#   This includes programming exceptions.  Each exception should briefly
#   describe what condition(s) will throw that exception.</description>
#   <rationale>Documenting raised exceptions ensures the programmer of client
#   functions/methods prevents passing bad inputs and is aware of the possible
#   need to handle a run-time/user exception in their code.</rationale>
# </requirement>
# <requirement>
#   <module>ramstk</module>
#   <name>Dict keys start with one (1)</name>
#   <description>When using integer dict keys, start with one (1).
#   </description>
#   <rationale>Integer-keyed dicts are often associated with input variables
#   whose value is the index in a combobox.  Since comboboxes always contain
#   a blank in position zero, starting the dict index at 1 provides a 1:1
#   correlation.</rationale>
# </requirement>

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
