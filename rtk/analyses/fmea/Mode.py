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
