#!/usr/bin/env python
"""
###################
FMEA Control Module
###################
"""

# -*- coding: utf-8 -*-
#
#       rtk.analyses.fmea.Control.py is part of The RTK Project
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
    The Control data model contains the attributes and methods of a FMEA
    control.  A Mechanism or a Cause will consist of one or more Controls.
    The attributes of a Control are:

    :ivar int mode_id: the ID of the failure Mode this Control is associated
                       with.
    :ivar int mechanism_id: the ID of the failure Mechanism this Control is
                            associated with.
    :ivar int cause_id: the ID of the failure Cause this Control is associated
                        with.
    :ivar int control_id: the ID of this Control.
    :ivar str description: the description of this Control.
    :ivar int control_type: the type of Control
    """

    def __init__(self):
        """
        Method to initialize a Control data model instance.
        """

        # Set public scalar attribute default values.
        self.mode_id = 0
        self.mechanism_id = 0
        self.cause_id = 0
        self.control_id = 0
        self.description = ''
        self.control_type = 0


class Control(object):
    """
    The Control data controller provides an interface between the Control data
    model and an RTK view model.  A single Control controller can control one
    or more Control data models.  Currently the Control controller is unused.
    """

    def __init__(self):
        """
        Method to initialize a Control data controller instance.
        """

        pass
