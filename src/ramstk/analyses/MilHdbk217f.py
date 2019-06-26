# -*- coding: utf-8 -*-
#
#       ramstk.analyses.MilHdbk217f.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""MilHdbk217f Calculations Class."""


# RAMSTK Package Imports
from ramstk.analyses.models.milhdbk217f import Capacitor


def _do_calculate_217f_part_count(**attributes):
    """
    Calculate the MIL-HDBK-217F parts count active hazard rate.

    :param dict attributes: the attributes dict for the component being
        calculated.
    :return: attributes; the attributes dict with updated values.
    :rtype: dict
    :raise: IndexError if there is no entry for the active environment ID.
    :raise: KeyError if there is no entry for category ID.
    """
    _part_count = {4: Capacitor.calculate_part_count,}

    _lst_lambda_b = _part_count[attributes['category_id']](**attributes)

    attributes['piQ'] = _get_part_count_quality_factor(attributes['category_id'], attributes['subcategory_id'], attributes['quality_id'])
    attributes['lambda_b'] = _lst_lambda_b[
        attributes['environment_active_id'] - 1
    ]

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ']
    )

    return attributes


def _do_calculate_217f_part_stress(**attributes):
    """
    Calculate the MIL-HDBK-217F parts stress active hazard rate.

    :param dict attributes: the attributes dict for the component being
        calculated.
    :return: attributes; the attributes dict with updated values.
    :rtype: dict
    :raise: IndexError if there is no entry for the active environment ID.
    :raise: KeyError if there is no entry for category ID.
    """
    _functions = {4: Capacitor.calculate_part_stress,}

    attributes['piE'] = _get_environment_factor(attributes['category_id'], attributes['environment_active_id'])
    attributes['piQ'] = _get_part_stress_quality_factor(attributes['category_id'], attributes['subcategory_id'], attributes['quality_id'])

    _part_stress = _functions[attributes['category_id']]

    return _part_stress(**attributes)


def _get_environment_factor(category_id, environment_active_id):
    """
    Retrieve the MIL-HDBK-217F environment factor (piE) for the component.

    :param int category_id: the category ID of the component.
    :param int environment_active_id: the active environment ID for the
        component.
    :return: _pi_e; the selected piE value.
    :rtype: float
    :raise: IndexError if there is no list entry for the passed active
        environment ID.
    :raise: KeyError if there is no piE list for the passed category ID.
    """
    _pi_e_lists = {4: Capacitor.PI_E,}

    return _pi_e_lists[category_id][environment_active_id - 1]


def _get_part_count_quality_factor(category_id, subcategory_id, quality_id):
    """
    Retrieve the MIL-HDBK-217F parts count quality factor (piQ).

    :param int category_id: the category ID of the component.
    :param int subcategory_id: the subcategory ID of the component.
    :param int quality_id: the quality level ID for the component.
    :return: _pi_q; the selected piQ value.
    :rtype: float
    :raise: IndexError if there is no list entry for the passed active
        environment ID.
    :raise: KeyError if there is no piQ list for the passed category ID.
    """
    _pi_q_lists = {4: Capacitor.PART_COUNT_PI_Q,}

    if category_id in [6, 7, 9, 10]:
        _pi_q = _pi_q_lists[category_id][subcategory_id][quality_id - 1]
    else:
        _pi_q = _pi_q_lists[category_id][quality_id - 1]

    return _pi_q


def _get_part_stress_quality_factor(category_id, subcategory_id, quality_id):
    """
    Retrieve the MIL-HDBK-217F part stress quality factor (piQ).

    :param int category_id: the category ID of the component.
    :param int subcategory_id: the subcategory ID of the component.
    :param int quality_id: the quality level ID for the component.
    :return: _pi_q; the selected piQ value.
    :rtype: float
    :raise: IndexError if there is no list entry for the passed quality ID.
    :raise: KeyError if there is no piQ list for the passed category ID.
    """
    _pi_q_lists = {4: Capacitor.PART_STRESS_PI_Q,}

    if category_id == 1:
        _pi_q = _pi_q_lists[category_id][quality_id - 1]
    else:
        _pi_q = _pi_q_lists[category_id][subcategory_id][quality_id - 1]

    return _pi_q


def do_calculate_active_hazard_rate(**attributes):
    """
    Calculate the active hazard rate for a hardware item.

    .. attention:: The programmer is responsible for ensuring appropriate
        stress analyses (e.g., voltage ratios) are performed and results
        assigned to the attributes dict prior to calling the MIL-HDBK-217F
        methods.

    .. important:: The calling object is responsible for handling any
        exceptions raised by or passed through this method.

    :return: attributes; the keyword argument (hardware attribute)
        dictionary with updated values.
    :rtype: dict
    """
    if attributes['hazard_rate_method_id'] == 1:
        attributes = _do_calculate_217f_part_count(**attributes)
    elif attributes['hazard_rate_method_id'] == 2:
        attributes = _do_calculate_217f_part_stress(**attributes)

    attributes['hazard_rate_active'] = (
        attributes['hazard_rate_active']
        + attributes['add_adj_factor']
    ) * \
        (attributes['duty_cycle'] / 100.0) * \
        attributes['mult_adj_factor'] * attributes['quantity']

    return attributes
