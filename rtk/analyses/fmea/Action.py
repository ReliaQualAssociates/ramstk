#!/usr/bin/env python
"""
##################
FMEA Action Module
##################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Action.py is part of The RTK Project
#
# All rights reserved.

# Import other RTK modules.
try:
    import Utilities as _util
except ImportError:                         # pragma: no cover
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class Model(object):
    """
    The Action data model contains the attributes and methods of a FMEA
    action.  A Mechanism or a Cause will contain of one or more Actions.
    The attributes of an Action are:

    :ivar int mode_id: the ID of the failure Mode this Action is associated
                       with.
    :ivar int mechanism_id: the ID of the failure Mechanism this Action is
                            associated with.
    :ivar int cause_id: the ID of the failure Cause this Action is associated
                        with.
    :ivar int action_id: the ID of this Action.
    :ivar str action_recommended: the description of the recommended Action.
    :ivar int action_category: the index of the category of this Action.
    :ivar int action_owner: the index of the owner of this Action.
    :ivar int action_due_date: the ordinal due date of this Action.
    :ivar int action_status: the index of the status of this Action.
    :ivar str action_taken: the description of the Action actually taken.
    :ivar int action_approved: indicates whether or not the Action is approved.
    :ivar int action_approved_date: the ordinal date the Action was approved.
    :ivar int action_closed: indicates whether or not the Action is closed.
    :ivar int action_closed_date: the ordinal date the Action was closed.
    """

    def __init__(self):
        """
        Method to initialize an Action data model instance.
        """

        # Set public scalar attribute default values.
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.action_id = 0
        self.action_recommended = ''
        self.action_category = 0
        self.action_owner = 0
        self.action_due_date = 0
        self.action_status = 0
        self.action_taken = ''
        self.action_approved = 0
        self.action_approved_date = 0
        self.action_closed = 0
        self.action_closed_date = 0


class Action(object):
    """
    The Action data controller provides an interface between the Action data
    model and an RTK view model.  A single Action controller can control one
    or more Action data models.  Currently the Action controller is unused.
    """

    def __init__(self):
        """
        Method to initialize an Action data controller instance.
        """

        pass
