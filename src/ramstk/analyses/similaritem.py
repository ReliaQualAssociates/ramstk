# -*- coding: utf-8 -*-
#
#       ramstk.analyses.SimilarItem.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Reliability Similar Item Assessment Module."""

# Standard Library Imports
from typing import Dict, List, Tuple

# Third Party Imports
# noinspection PyPackageRequirements
from sympy import symbols, sympify  # type: ignore

ENVIRONMENT_FROM_TO: Dict[Tuple[int, int], float] = {
    (0, 0): 1.0,
    (1, 1): 1.0,
    (1, 2): 0.2,
    (1, 3): 0.3,
    (1, 4): 0.3,
    (1, 5): 0.1,
    (1, 6): 1.1,
    (2, 1): 5.0,
    (2, 2): 1.0,
    (2, 3): 1.4,
    (2, 4): 1.4,
    (2, 5): 0.5,
    (2, 6): 5.0,
    (3, 1): 3.3,
    (3, 2): 0.7,
    (3, 3): 1.0,
    (3, 4): 1.0,
    (3, 5): 0.3,
    (3, 6): 3.3,
    (4, 1): 3.3,
    (4, 2): 0.7,
    (4, 3): 1.0,
    (4, 4): 1.0,
    (4, 5): 0.3,
    (4, 6): 3.3,
    (5, 1): 10.0,
    (5, 2): 2.0,
    (5, 3): 3.3,
    (5, 4): 3.3,
    (5, 5): 1.0,
    (5, 6): 10.0,
    (6, 1): 0.9,
    (6, 2): 0.2,
    (6, 3): 0.3,
    (6, 4): 0.3,
    (6, 5): 0.1,
    (6, 6): 1.0,
}
QUALITY_FROM_TO: Dict[Tuple[int, int], float] = {
    (0, 0): 1.0,
    (1, 1): 1.0,
    (1, 2): 0.8,
    (1, 3): 0.5,
    (1, 4): 0.2,
    (2, 1): 1.3,
    (2, 2): 1.0,
    (2, 3): 0.6,
    (2, 4): 0.3,
    (3, 1): 2.0,
    (3, 2): 1.7,
    (3, 3): 1.0,
    (3, 4): 0.4,
    (4, 1): 5.0,
    (4, 2): 3.3,
    (4, 3): 2.5,
    (4, 4): 1.0,
}
TEMPERATURE_FROM_TO: Dict[Tuple[float, float], float] = {
    (10.0, 10.0): 1.0,
    (10.0, 20.0): 0.9,
    (10.0, 30.0): 0.8,
    (10.0, 40.0): 0.8,
    (10.0, 50.0): 0.7,
    (10.0, 60.0): 0.5,
    (10.0, 70.0): 0.4,
    (20.0, 10.0): 1.1,
    (20.0, 20.0): 1.0,
    (20.0, 30.0): 0.9,
    (20.0, 40.0): 0.8,
    (20.0, 50.0): 0.7,
    (20.0, 60.0): 0.6,
    (20.0, 70.0): 0.5,
    (30.0, 10.0): 1.2,
    (30.0, 20.0): 1.1,
    (30.0, 30.0): 1.0,
    (30.0, 40.0): 0.9,
    (30.0, 50.0): 0.8,
    (30.0, 60.0): 0.6,
    (30.0, 70.0): 0.5,
    (40.0, 10.0): 1.3,
    (40.0, 20.0): 1.2,
    (40.0, 30.0): 1.1,
    (40.0, 40.0): 1.0,
    (40.0, 50.0): 0.9,
    (40.0, 60.0): 0.7,
    (40.0, 70.0): 0.6,
    (50.0, 10.0): 1.5,
    (50.0, 20.0): 1.4,
    (50.0, 30.0): 1.2,
    (50.0, 40.0): 1.1,
    (50.0, 50.0): 1.0,
    (50.0, 60.0): 0.8,
    (50.0, 70.0): 0.7,
    (60.0, 10.0): 1.9,
    (60.0, 20.0): 1.7,
    (60.0, 30.0): 1.6,
    (60.0, 40.0): 1.5,
    (60.0, 50.0): 1.2,
    (60.0, 60.0): 1.0,
    (60.0, 70.0): 0.8,
    (70.0, 10.0): 2.4,
    (70.0, 20.0): 2.2,
    (70.0, 30.0): 1.9,
    (70.0, 40.0): 1.8,
    (70.0, 50.0): 1.5,
    (70.0, 60.0): 1.2,
    (70.0, 70.0): 1.0
}


# noinspection PyTypeChecker
def calculate_topic_633(
        environment: Dict[str, float], quality: Dict[str, float],
        temperature: Dict[str, float],
        hazard_rate: float) -> Tuple[float, float, float, float]:
    """Calculate the Similar Item analysis using Topic 6.3.3 approach.

    This method calculates the new hazard rate using the approach found
    in The Reliability Toolkit: Commercial Practices Edition, Topic 6.3.3.

    :param environment: the active environment ID for the from and to
        environments.
    :param quality: the quality level ID for the from and to quality.
    :param temperature: the ambient operating temperature (in C) for the
        from and to temperatures.
    :param hazard_rate: the current hazard rate of the hardware item
        being calculated.
    :return: (_change_factor_1, _change_factor_2, _change_factor_3, _result_1);
        the three change factors (quality, environment, and temperature) and
        the assessment result.
    :rtype: tuple
    :raise: KeyError if passed an environment, quality, or temperature dict
        that is missing the from, to, or both keys.
    :raise: TypeError if passed a string value for either temperature.
    """
    # Convert user-supplied temperatures to whole values used in Topic 633.
    temperature['from'] = round(temperature['from'] / 10.0) * 10.0
    temperature['to'] = round(temperature['to'] / 10.0) * 10.0

    _change_factor_1 = QUALITY_FROM_TO[(
        quality['from'],  # type: ignore
        quality['to'])]  # type: ignore
    _change_factor_2 = ENVIRONMENT_FROM_TO[(
        environment['from'],  # type: ignore
        environment['to'])]  # type: ignore
    _change_factor_3 = TEMPERATURE_FROM_TO[(temperature['from'],
                                            temperature['to'])]

    _result_1 = float(hazard_rate /
                      (_change_factor_1 * _change_factor_2 * _change_factor_3))

    return _change_factor_1, _change_factor_2, _change_factor_3, _result_1


# pylint: disable=too-many-locals
def calculate_user_defined(sia: Dict[str, float]):
    """Calculate the user-defined similar item analysis.

    :param sia: the user-defined similar item assessment dict.  The
        calling method/function should create the sia dict as follows:

        sia = OrderedDict({
            _key: None
            for _key in [
                'hr', 'pi1', 'pi2', 'pi3', 'pi3', 'pi4', 'pi5', 'pi6', 'pi7',
                'pi8', 'pi9', 'pi10', 'uf1', 'uf2', 'uf3', 'uf4', 'uf5', 'ui1',
                'ui2', 'ui3', 'ui4', 'ui5', 'equation1', 'equation2',
                'equation3', 'equation4', 'equation5', 'res1', 'res2', 'res3',
                'res4', 'res5'
                ]
            })

    :return: sia; the similar item assessment dict with updated results.
    :rtype: dict
    """
    (hr, pi1, pi2, pi3, pi4, pi5, pi6, pi7, pi8, pi9, pi10, uf1, uf2, uf3, uf4,
     uf5, ui1, ui2, ui3, ui4, ui5, res1, res2, res3, res4, res5) = symbols(
         'hr pi1 pi2 pi3 pi4 pi5 pi6 pi7 pi8 pi9 pi10 uf1 uf2 uf3 uf4 uf5 ui1 '
         'ui2 ui3 ui4 ui5 res1 res2 res3 res4 res5')

    # The subs argument needs to be passed as a dict of sia values just like
    # it is below.  This will result in duplicate code warnings, but passing
    # it like this is required to allow the use of the results in subsequent
    # calculations.
    # pylint: disable=eval-used
    sia['res1'] = sympify(sia['equation1']).evalf(
        subs={
            hr: sia['hr'],
            pi1: sia['pi1'],
            pi2: sia['pi2'],
            pi3: sia['pi3'],
            pi4: sia['pi4'],
            pi5: sia['pi5'],
            pi6: sia['pi6'],
            pi7: sia['pi7'],
            pi8: sia['pi8'],
            pi9: sia['pi9'],
            pi10: sia['pi10'],
            uf1: sia['uf1'],
            uf2: sia['uf2'],
            uf3: sia['uf3'],
            uf4: sia['uf4'],
            uf5: sia['uf5'],
            ui1: sia['ui1'],
            ui2: sia['ui2'],
            ui3: sia['ui3'],
            ui4: sia['ui4'],
            ui5: sia['ui5'],
            res1: sia['res1'],
            res2: sia['res2'],
            res3: sia['res3'],
            res4: sia['res4'],
            res5: sia['res5']
        })
    sia['res2'] = sympify(sia['equation2']).evalf(
        subs={
            hr: sia['hr'],
            pi1: sia['pi1'],
            pi2: sia['pi2'],
            pi3: sia['pi3'],
            pi4: sia['pi4'],
            pi5: sia['pi5'],
            pi6: sia['pi6'],
            pi7: sia['pi7'],
            pi8: sia['pi8'],
            pi9: sia['pi9'],
            pi10: sia['pi10'],
            uf1: sia['uf1'],
            uf2: sia['uf2'],
            uf3: sia['uf3'],
            uf4: sia['uf4'],
            uf5: sia['uf5'],
            ui1: sia['ui1'],
            ui2: sia['ui2'],
            ui3: sia['ui3'],
            ui4: sia['ui4'],
            ui5: sia['ui5'],
            res1: sia['res1'],
            res2: sia['res2'],
            res3: sia['res3'],
            res4: sia['res4'],
            res5: sia['res5']
        })
    sia['res3'] = sympify(sia['equation3']).evalf(
        subs={
            hr: sia['hr'],
            pi1: sia['pi1'],
            pi2: sia['pi2'],
            pi3: sia['pi3'],
            pi4: sia['pi4'],
            pi5: sia['pi5'],
            pi6: sia['pi6'],
            pi7: sia['pi7'],
            pi8: sia['pi8'],
            pi9: sia['pi9'],
            pi10: sia['pi10'],
            uf1: sia['uf1'],
            uf2: sia['uf2'],
            uf3: sia['uf3'],
            uf4: sia['uf4'],
            uf5: sia['uf5'],
            ui1: sia['ui1'],
            ui2: sia['ui2'],
            ui3: sia['ui3'],
            ui4: sia['ui4'],
            ui5: sia['ui5'],
            res1: sia['res1'],
            res2: sia['res2'],
            res3: sia['res3'],
            res4: sia['res4'],
            res5: sia['res5']
        })
    sia['res4'] = sympify(sia['equation4']).evalf(
        subs={
            hr: sia['hr'],
            pi1: sia['pi1'],
            pi2: sia['pi2'],
            pi3: sia['pi3'],
            pi4: sia['pi4'],
            pi5: sia['pi5'],
            pi6: sia['pi6'],
            pi7: sia['pi7'],
            pi8: sia['pi8'],
            pi9: sia['pi9'],
            pi10: sia['pi10'],
            uf1: sia['uf1'],
            uf2: sia['uf2'],
            uf3: sia['uf3'],
            uf4: sia['uf4'],
            uf5: sia['uf5'],
            ui1: sia['ui1'],
            ui2: sia['ui2'],
            ui3: sia['ui3'],
            ui4: sia['ui4'],
            ui5: sia['ui5'],
            res1: sia['res1'],
            res2: sia['res2'],
            res3: sia['res3'],
            res4: sia['res4'],
            res5: sia['res5']
        })
    sia['res5'] = sympify(sia['equation5']).evalf(
        subs={
            hr: sia['hr'],
            pi1: sia['pi1'],
            pi2: sia['pi2'],
            pi3: sia['pi3'],
            pi4: sia['pi4'],
            pi5: sia['pi5'],
            pi6: sia['pi6'],
            pi7: sia['pi7'],
            pi8: sia['pi8'],
            pi9: sia['pi9'],
            pi10: sia['pi10'],
            uf1: sia['uf1'],
            uf2: sia['uf2'],
            uf3: sia['uf3'],
            uf4: sia['uf4'],
            uf5: sia['uf5'],
            ui1: sia['ui1'],
            ui2: sia['ui2'],
            ui3: sia['ui3'],
            ui4: sia['ui4'],
            ui5: sia['ui5'],
            res1: sia['res1'],
            res2: sia['res2'],
            res3: sia['res3'],
            res4: sia['res4'],
            res5: sia['res5']
        })

    return sia


def set_user_defined_change_factors(sia: Dict[str, float],
                                    factors: List[float]) -> Dict[str, float]:
    """Set the change factors for the user-defined calculations.

    :param sia: the similar item assessment dict.
    :param list factors: the list of change factors; the list items are float
        or int.
    :return: sia; the similar item assessment dict with updated factor values.
    :rtype: dict
    """
    # Get the change factor values.
    for _idx in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        _key = list(sia.keys())[_idx]
        try:
            sia[_key] = factors[_idx - 1]
        except IndexError:
            sia[_key] = 0.0

    return sia


def set_user_defined_floats(sia: Dict[str, float],
                            floats: List[float]) -> Dict[str, float]:
    """Set the user-defined float values for the user-defined calculations.

    :param sia: the similar item assessment dict.
    :param list floats: the list of float values.
    :return: sia; the similar item assessment dict with updated float values.
    :rtype: dict
    """
    for _idx in [11, 12, 13, 14, 15]:
        _key = list(sia.keys())[_idx]
        try:
            sia[_key] = float(floats[_idx - 11])
        except IndexError:
            sia[_key] = 0.0

    return sia


def set_user_defined_ints(sia: Dict[str, int],
                          ints: List[int]) -> Dict[str, int]:
    """Set the user-defined integer values for the user-defined calculations.

    :param sia: the similar item assessment dict.
    :param list ints: the list of integer values.
    :return: sia; the similar item assessment dict with updated integer values.
    :rtype: dict
    """
    for _idx in [16, 17, 18, 19, 20]:
        _key = list(sia.keys())[_idx]
        try:
            sia[_key] = int(ints[_idx - 16])
        except IndexError:
            sia[_key] = 0

    return sia


def set_user_defined_functions(sia: Dict[str, str],
                               functions: List[str]) -> Dict[str, str]:
    """Set the user-defined functions for the user-defined calculations.

    :param sia: the similar item assessment dict.
    :param list functions: the list of functions; list items are str.
    :return: sia; the similar item assessment dict with updated functions.
    :rtype: dict
    """
    for _idx in [21, 22, 23, 24, 25]:
        _key = list(sia.keys())[_idx]
        try:
            sia[_key] = str(functions[_idx - 21])
        except IndexError:
            sia[_key] = ''

    return sia


def set_user_defined_results(sia: Dict[str, float],
                             results: List[float]) -> Dict[str, float]:
    """Set the user-defined results for the user-defined calculations.

    This allows the use of the results fields to be manually set to float
    values by the user essentially creating five more user-defined float
    values.

    :param sia: the similar item assessment dict.
    :param list results: the list of results.
    :return: sia; the similar item assessment dict with updated results.
    :rtype: dict
    """
    for _idx in [26, 27, 28, 29, 30]:
        _key = list(sia.keys())[_idx]
        try:
            sia[_key] = results[_idx - 26]
        except IndexError:
            sia[_key] = 0.0

    return sia
