#!/usr/bin/env python
"""
#################
FMEA Cause Module
#################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Cause.py is part of The RTK Project
#
# All rights reserved.

# Import other RTK modules.
try:
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Utilities as Utilities

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Cause data model contains the attributes and methods of a FMEA cause.
    A Mechanism will consist of one or more Causes.  The attributes of a Cause
    are:

    :ivar dict dicControls: Dictionary of the Controls associated with the
                            Cause. Key is the Control ID, value is a pointer to
                            the instance of the Control data model.
    :ivar dict dicActions: Dictionary of the Actions associated with the Cause.
                           Key is the Action ID, value is a pointer to the
                           instance of the Action data model.
    :ivar int mode_id: the ID of the failure Mode this Cause is associated
                       with.
    :ivar int mechanism_id: the ID of the failure Mechanism this Cause is
                            associated with.
    :ivar int cause_id: the ID of the failure Cause.
    :ivar str description: the description of the failure Cause.
    """

    def __init__(self):
        """
        Method to initialize a Cause data model instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dictionary attributes.
        self.dicControls = {}
        self.dicActions = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.description = ''
        self.rpn_occurrence = 9
        self.rpn_detection = 9
        self.rpn = 1000
        self.rpn_occurrence_new = 9
        self.rpn_detection_new = 9
        self.rpn_new = 1000


class Cause(object):
    """
    The Cause data controller provides an interface between the Cause data
    model and an RTK view model.  A single Cause controller can control one or
    more Cause data models.  Currently the Cause controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Cause controller instance.
        """

        pass
