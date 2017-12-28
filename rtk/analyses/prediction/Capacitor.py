#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.analyses.prediction.mil_hdbk_217f.Capacitor.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Capacitor MIL-HDBK-217F Package."""

import Configuration
import Utilities

lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

def calculate(self, **kwargs):
    """
    Calculate the hazard rate for the Capacitor data model.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    hr_model = kwargs['equation']
    piQ = kwargs['piQ']
    piE = kwargs['piE']
    lambdab = kwargs['lambdab']

    for _key in hr_model:
        vars()[_key] = hr_model[_key]

    hr_active = eval(hr_model['equation'])
    hr_active = (hr_active + self.add_adj_factor) * \
                (self.duty_cycle / 100.0) * \
                self.mult_adj_factor * self.quantity
    hr_active = hr_active / Configuration.FRMULT

    # Calculate overstresses.
    self._overstressed()

    # Calculate operating point ratios.
    self.current_ratio = self.operating_current / self.rated_current
    self.voltage_ratio = (self.operating_voltage + self.acvapplied) / \
                         self.rated_voltage
    self.power_ratio = self.operating_power / self.rated_power

    return False

def _overstressed(self):
    """
    Determine whether the Capacitor is overstressed.

    This determination is based on it's rated values and operating environment.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _reason_num = 1
    _reason = ''

    _harsh = True

    self.overstress = False

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if self.environment_active in [1, 2, 4, 11]:
        _harsh = False

    if _harsh:
        if self.operating_voltage > 0.60 * self.rated_voltage:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                            _(u". Operating voltage > 60% rated voltage.\n")
            _reason_num += 1
        if self.max_rated_temperature - self.temperature_active <= 10.0:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                            _(u". Operating temperature within 10.0C of "
                            u"maximum rated temperature.\n")
            _reason_num += 1
    else:
        if self.operating_voltage > 0.90 * self.rated_voltage:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                            _(u". Operating voltage > 90% rated voltage.\n")
            _reason_num += 1

    self.reason = _reason

    return False
