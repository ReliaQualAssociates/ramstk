#!/usr/bin/env python
"""
################
FMEA Mode Module
################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Mode.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Function to convert string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    elif('invalid literal' in message[0] or
         'could not convert string to float' in message[0]):   # Value error
        _error_code = 50
    else:                                   # Unhandled error
        _error_code = 1000

    return _error_code


class OutOfRangeError(Exception):
    """
    Exception raised when an input value is outside legal limits.
    """

    pass


class Model(object):
    """
    The Mode data model contains the attributes and methods of a FMEA failure
    mode.  A FMEA will consist of one or more Modes.  The attributes of a Mode
    are:

    :ivar assembly_id: default value: 0
    :ivar function_id: default value: 0
    :ivar mode_id: default value: 0
    :ivar description: default value: ''
    :ivar mission: default value: ''
    :ivar mission_phase: default value: ''
    :ivar local_effect: default value: ''
    :ivar next_effect: default value: ''
    :ivar end_effect: default value: ''
    :ivar detection_method: default value: ''
    :ivar other_indications: default value: ''
    :ivar isolation_method: default value: ''
    :ivar design_provisions: default value: ''
    :ivar operator_actions: default value: ''
    :ivar severity_class: default value: ''
    :ivar hazard_rate_source: default value: ''
    :ivar mode_probability: default value: ''
    :ivar effect_probability: default value: 1.0
    :ivar mode_ratio: default value: 0.0
    :ivar mode_hazard_rate: default value: 0.0
    :ivar mode_op_time: default value: 0.0
    :ivar mode_criticality: default value: 0.0
    :ivar rpn_severity: default value: 10
    :ivar rpn_severity_new: default value: 10
    :ivar critical_item: default value: 0
    :ivar single_point: default value: 0
    :ivar remarks: default value: ''
    """

    def __init__(self):
        """
        Method to initialize an Mode data model instance.
        """

        # Set public dict attribute default values.
        self.dicMechanisms = {}

        # Set public scalar attribute default values.
        self.assembly_id = 0
        self.function_id = 0
        self.mode_id = 0
        self.description = ''
        self.mission = ''
        self.mission_phase = ''
        self.local_effect = ''
        self.next_effect = ''
        self.end_effect = ''
        self.detection_method = ''
        self.other_indications = ''
        self.isolation_method = ''
        self.design_provisions = ''
        self.operator_actions = ''
        self.severity_class = ''
        self.hazard_rate_source = ''
        self.mode_probability = ''
        self.effect_probability = 1.0
        self.mode_ratio = 0.0
        self.mode_hazard_rate = 0.0
        self.mode_op_time = 0.0
        self.mode_criticality = 0.0
        self.rpn_severity = 10
        self.rpn_severity_new = 10
        self.critical_item = 0
        self.single_point = 0
        self.remarks = ''

    def set_attributes(self, values):
        """
        Method to set the Mode data model attributes.

        :param tuple values: values to assign to instance attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.assembly_id = int(values[0])
            self.function_id = int(values[1])
            self.mode_id = int(values[2])
            self.description = str(values[3])
            self.mission = str(values[4])
            self.mission_phase = str(values[5])
            self.local_effect = str(values[6])
            self.next_effect = str(values[7])
            self.end_effect = str(values[8])
            self.detection_method = str(values[9])
            self.other_indications = str(values[10])
            self.isolation_method = str(values[11])
            self.design_provisions = str(values[12])
            self.operator_actions = str(values[13])
            self.severity_class = str(values[14])
            self.hazard_rate_source = str(values[15])
            self.mode_probability = str(values[16])
            self.effect_probability = float(values[17])
            self.mode_ratio = float(values[18])
            self.mode_hazard_rate = float(values[19])
            self.mode_op_time = float(values[20])
            self.mode_criticality = float(values[21])
            self.rpn_severity = int(values[22])
            self.rpn_severity_new = int(values[23])
            self.critical_item = int(values[24])
            self.single_point = int(values[25])
            self.remarks = str(values[26])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mode data model
        attributes.

        :return: (self.assembly_id, self.function_id, self.mode_id,
                  self.description, self.mission, self.mission_phase,
                  self.local_effect, self.next_effect, self.end_effect,
                  self.detection_method, self.other_indications,
                  self.isolation_method, self.design_provisions,
                  self.operator_actions, self.severity_class,
                  self.hazard_rate_source, self.mode_probability,
                  self.effect_probability, self.mode_ratio,
                  self.mode_hazard_rate, self.mode_op_time,
                  self.mode_criticality, self.rpn_severity,
                  self.rpn_severity_new, self.critical_item, self.single_point,
                  self.remarks)
        :rtype: tuple
        """

        return(self.assembly_id, self.function_id, self.mode_id,
               self.description, self.mission, self.mission_phase,
               self.local_effect, self.next_effect, self.end_effect,
               self.detection_method, self.other_indications,
               self.isolation_method, self.design_provisions,
               self.operator_actions, self.severity_class,
               self.hazard_rate_source, self.mode_probability,
               self.effect_probability, self.mode_ratio,
               self.mode_hazard_rate, self.mode_op_time, self.mode_criticality,
               self.rpn_severity, self.rpn_severity_new, self.critical_item,
               self.single_point, self.remarks)

    def calculate(self, item_hr, ratio, op_time, effect_prob=1.0):
        """
        Calculate the Criticality for the Mode.

            Mode Criticality = Item Hazard Rate * Mode Ratio * Mode Operating Time * Effect Probability

        :param float item_hr: the hazard rate of the hardware item being
                              calculated.
        :param float ratio: the mode ratio of the failure mode being
                            calculated.
        :param float op_time: the operating time of the failure mode being
                              calculated.
        :keyword float effect_prob: the probability the selected end-effect
                                    will occur if the failure mode is
                                    experienced in the field.
        :return: (_mode_ratio, _mode_crit)
        :rtype: tuple
        """

        if not 0.0 <= item_hr:
            raise OutOfRangeError(_(u"Item hazard rate has a negative value."))
        if not 0.0 <= ratio <= 1.0:
            raise OutOfRangeError(_(u"Failure mode ratio is outside the range "
                                    u"of [0.0, 1.0]."))
        if not 0.0 <= op_time:
            raise OutOfRangeError(_(u"Failure mode operating time has a "
                                    u"negative value."))
        if not 0.0 <= effect_prob <= 1.0:
            raise OutOfRangeError(_(u"Failure effect probability is outside "
                                    u"the range [0.0, 1.0]."))

        _mode_hr = item_hr * ratio
        _mode_crit = _mode_hr * op_time * effect_prob

        if not 0.0 <= _mode_hr:
            raise OutOfRangeError(_(u"Failure mode hazard rate has a negative "
                                    u"value."))
        if not 0.0 <= _mode_crit:
            raise OutOfRangeError(_(u"Failure mode criticality has a negative "
                                    u"value."))

        return(_mode_hr, _mode_crit)


class Mode(object):
    """
    The Mode data controller provides an interface between the Mode data model
    and an RTK view model.  A single Mode data controller can control one or
    more Mode data models.  Currently the Mode data controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Mode data controller instance.
        """

        pass
