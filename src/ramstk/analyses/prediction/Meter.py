# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Meter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Reliability Calculations Module."""

PART_COUNT_217F_LAMBDA_B = {
        1: [
            [
                10.0,
                20.0,
                120.0,
                70.0,
                180.0,
                50.0,
                80.0,
                160.0,
                250.0,
                260.0,
                5.0,
                140.0,
                380.0,
                0.0,
            ],
            [
                15.0,
                30.0,
                180.0,
                105.0,
                270.0,
                75.0,
                120.0,
                240.0,
                375.0,
                390.0,
                7.5,
                210.0,
                570.0,
                0.0,
            ],
            [
                40.0,
                80.0,
                480.0,
                280.0,
                720.0,
                200.0,
                320.0,
                640.0,
                1000.0,
                1040.0,
                20.0,
                560.0,
                1520.0,
                0.0,
            ],
        ],
        2: [
            [
                0.09,
                0.36,
                2.3,
                1.1,
                3.2,
                2.5,
                3.8,
                5.2,
                6.6,
                5.4,
                0.099,
                5.4,
                0.0,
                0.0,
            ],
            [
                0.15,
                0.61,
                2.8,
                1.8,
                5.4,
                4.3,
                6.4,
                8.9,
                11.0,
                9.2,
                0.17,
                9.2,
                0.0,
                0.0,
            ],
        ],
}
PART_STRESS_217F_LAMBDA_B = {1: [20.0, 30.0, 80.0], 2: 0.09}
PI_F = [1.0, 1.0, 2.8]


def _get_temperature_stress_factor(attributes):
    """
    Retrieve the temperature stress factor (piT).

    :param dict attributes: the attributes for the meter being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    try:
        _temperature_ratio = (
            attributes['temperature_active'] /
            attributes['temperature_rated_max']
        )
    except ZeroDivisionError:
        _temperature_ratio = 1.0

    if attributes['subcategory_id'] == 1:
        if 0.0 < _temperature_ratio <= 0.5:
            attributes['piT'] = 0.5
        elif 0.5 < _temperature_ratio <= 0.6:
            attributes['piT'] = 0.6
        elif 0.6 < _temperature_ratio <= 0.8:
            attributes['piT'] = 0.8
        elif 0.8 < _temperature_ratio <= 1.0:
            attributes['piT'] = 1.0

    return attributes


def _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes):
    """
    Calculate the part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param dict attributes: the attributes for the meter being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    if attributes['subcategory_id'] == 1:
        attributes['lambda_b'] = PART_STRESS_217F_LAMBDA_B[1][
            attributes['type_id'] - 1
        ]
    elif attributes['subcategory_id'] == 2:
        attributes['lambda_b'] = PART_STRESS_217F_LAMBDA_B[2]
    else:
        attributes['lambda_b'] = 0.0

    return attributes


def calculate_217f_part_count_lambda_b(attributes):
    r"""
    Calculate the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. type id; if the meter subcategory is NOT type dependent, then
            the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory \  |              Meter \          | MIL-HDBK-217F \ |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Elapsed Time                  |       12.4      |
    +----------------+-------------------------------+-----------------+
    |        2       | Panel                         |       18.1      |
    +----------------+-------------------------------+-----------------+

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param dict attributes: the attributes for the crystal being calculated.
    :return: _lst_base_hr; the list of base hazard rates.
    :rtype: list
    """
    try:
        _lst_base_hr = PART_COUNT_217F_LAMBDA_B[
            attributes['subcategory_id']
        ][
            attributes['type_id'] - 1
        ]
    except (IndexError, KeyError):
        _lst_base_hr = [0.0]

    return _lst_base_hr


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a meter.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :return: (attributes, _msg); the keyword argument (hardware attribute)
        dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes)
    attributes = _get_temperature_stress_factor(attributes)

    # Determine the application factor (piA) and function factor (piF).
    if attributes['subcategory_id'] == 2:
        attributes['piA'] = (1.7 if (attributes['type_id']) - (1) else 1.0)
        attributes['piF'] = PI_F[attributes['application_id'] - 1]

    _msg = do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piE']
    )
    if attributes['subcategory_id'] == 2:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piA'] *
            attributes['piF'] * attributes['piQ']
        )
    elif attributes['subcategory_id'] == 1:
        attributes['hazard_rate_active'] = (
            attributes['hazard_rate_active'] * attributes['piT']
        )

    return attributes, _msg


def do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the meter type which is why a WARKING message is
    issued rather than an ERROR message.

    :param dict attributes: the attributes for the meter being calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    if attributes['lambda_b'] <= 0.0:
        _msg = (
            "RAMSTK WARNING: Base hazard rate is 0.0 when calculating "
            "meter, hardware ID: {0:d}, subcategory ID: {1:d}, type "
            "ID: {3:d}, and active environment ID: {2:d}.\n"
        ).format(
            attributes['hardware_id'],
            attributes['subcategory_id'],
            attributes['environment_active_id'],
            attributes['type_id'],
        )

    if attributes['piQ'] <= 0.0:
        _msg = _msg + (
            "RAMSTK WARNING: piQ is 0.0 when calculating meter, "
            "hardware ID: {0:d}, quality ID: {1:d}.\n"
        ).format(
            attributes['hardware_id'],
            attributes['quality_id'],
        )

    if attributes['hazard_rate_method_id'] == 2:
        if attributes['piE'] <= 0.0:
            _msg = _msg + (
                "RAMSTK WARNING: piE is 0.0 when calculating meter, "
                "hardware ID: {0:d}, active environment ID: {1:d}.\n"
            ).format(
                attributes['hardware_id'],
                attributes['environment_active_id'],
            )

        if attributes['piA'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piA is 0.0 when calculating ' \
                'meter, hardware ID: {0:d}, ' \
                'type ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['type_id'],
                )

        if attributes['piF'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piF is 0.0 when calculating ' \
                'meter, hardware ID: {0:d}, ' \
                'application ID: {1:d}.\n'.format(
                    attributes['hardware_id'],
                    attributes['application_id'],
                )

        if attributes['piT'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piF is 0.0 when calculating ' \
                'meter, hardware ID: {0:d}, ' \
                'active temperature: {1:f}, and max rated temperature: ' \
                '{2:f}.\n'.format(
                    attributes['hardware_id'],
                    attributes['temperature_active'],
                    attributes['temperature_rated_max'],
                )

    return _msg
