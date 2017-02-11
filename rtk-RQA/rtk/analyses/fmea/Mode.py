#!/usr/bin/env python
"""
################
FMEA Mode Module
################
"""

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
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class OutOfRangeError(Exception):
    """
    Exception raised when an input value is outside legal limits.
    """

    def __init__(self, message):
        """
        Method to initialize OutOfRangeError instance.
        """

        Exception.__init__(self)

        self.message = message


class Model(object):
    """
    The Mode data model contains the attributes and methods of a FMEA failure
    mode.  A FMEA will consist of one or more Modes.  The attributes of a Mode
    are:

    :ivar int assembly_id: the ID of the Hardware item the Mode is associated
                           with.
    :ivar int function_id: the ID of the Function the Mode is associated with.
    :ivar int mode_id: the ID of the failure Mode.
    :ivar str description: the description of the failure Mode.
    :ivar str mission: the Mission the failure Mode is applicable to.
    :ivar str mission_phase: the Mission Phase the failure Mode is applicable
                             to.
    :ivar str local_effect: the effect of the failure Mode on the immediate
                            piece of Hardware or Function.
    :ivar str next_effect: the effect of the failure Mode on the next higher
                           level piece of Hardware or Function.
    :ivar str end_effect: the worst-case system-level effect of the the failure
                          Mode.
    :ivar str detection_method: the method used to detect the failure Mode when
                                it occurs.
    :ivar str other_indications: indications the failure Mode has occurred.
    :ivar str isolation_method: the method used to isolate the failure Mode
                                during troubleshooting when the failure Mode
                                occurs.
    :ivar str design_provisions: design provisions intended to address the
                                 failure Mode.
    :ivar str operator_actions: action(s) the operator can take to mitigate the
                                failure Mode.
    :ivar str severity_class: the MIL-HDBK-1629A severity classification of the
                              failure Mode.
    :ivar str hazard_rate_source: the source of the hazard rate data for the
                                  failure Mode.
    :ivar str mode_probability: the MIL-STD-1629A categorical failure Mode
                                probability.
    :ivar float effect_probability: the probability the worst-case effect is
                                    the effect actually experienced.
    :ivar float mode_ratio: the ratio of this failure Mode to all failure Modes
                            the Hardware item is susceptible to.
    :ivar float mode_hazard_rate: the hazard rate of the failure Mode.
    :ivar float mode_op_time: the operating time the failure Mode is of
                              concern.
    :ivar float mode_criticality: the MIL-STD-1629A criticality of the failure
                                  Mode.
    :ivar int rpn_severity: the RPN severity rating of the failure Mode before
                            taking action.
    :ivar int rpn_severity_new: the RPN severity rating of the failure Mode
                                after taking action.
    :ivar int critical_item: indicates whether or not this failure Mode causes
                             the Hardware item to be critical.
    :ivar int single_point: indicates whether or not this failure Mode causes
                            the Hardware item to be a single point of failure.
    :ivar str remarks: any remarks associated with the failure Mode.
    """

    def __init__(self):
        """
        Method to initialize an Mode data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicMechanisms = {}

        # Define public list attributes.

        # Define public scalar attributes.
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
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."
        except ValueError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Wrong input data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Mode data model
        attributes.

        :return: (assembly_id, function_id, mode_id, description, mission,
                  mission_phase, local_effect, next_effect, end_effect,
                  detection_method, other_indications, isolation_method,
                  design_provisions, operator_actions, severity_class,
                  hazard_rate_source, mode_probability, effect_probability,
                  mode_ratio, mode_hazard_rate, mode_op_time, mode_criticality,
                  rpn_severity, rpn_severity_new, critical_item, single_point,
                  remarks)
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

    def calculate(self, item_hr):
        """
        Calculate the Criticality for the Mode.

            Mode Criticality = Item Hazard Rate * Mode Ratio * \
                               Mode Operating Time * Effect Probability

        :param float item_hr: the hazard rate of the hardware item being
                              calculated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if item_hr < 0.0:
            _return = True
            raise OutOfRangeError(_(u"Item hazard rate has a negative value."))
        if not 0.0 <= self.mode_ratio <= 1.0:
            _return = True
            raise OutOfRangeError(_(u"Failure mode ratio is outside the range "
                                    u"of [0.0, 1.0]."))
        if self.mode_op_time < 0.0:
            _return = True
            raise OutOfRangeError(_(u"Failure mode operating time has a "
                                    u"negative value."))
        if not 0.0 <= self.effect_probability <= 1.0:
            _return = True
            raise OutOfRangeError(_(u"Failure effect probability is outside "
                                    u"the range [0.0, 1.0]."))

        self.mode_hazard_rate = item_hr * self.mode_ratio
        self.mode_criticality = self.mode_hazard_rate * self.mode_op_time * \
                                self.effect_probability

        if self.mode_hazard_rate < 0.0:
            _return = True
            raise OutOfRangeError(_(u"Failure mode hazard rate has a negative "
                                    u"value."))
        if not self.mode_criticality > 0.0:
            _return = True
            raise OutOfRangeError(_(u"Failure mode criticality has a negative "
                                    u"value."))

        return _return


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
